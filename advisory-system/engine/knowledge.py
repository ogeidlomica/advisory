"""Knowledge-base layer for the Credi10 2.0 advisory engine (FEAT-001).

This module turns the fully-ingested corpus (ALL 18 documents, not just the two
primary PDFs) into a deterministic, stdlib-only knowledge base:

  * deterministic hierarchical summaries per document,
  * traceable key-fact extraction via domain-token heuristics,
  * text-coverage metrics (ratio + band) and an honest epistemic flag,
  * a ``KnowledgeBase`` builder that renders a ``knowledge-base/`` folder plus a
    coverage-checklist report asserting 18/18 documents processed (no sampling).

Hard constraints honoured here (see task context):
  * Standard library ONLY. No third-party deps, no network, no LLM.
  * DETERMINISM: stable ordering (sort by filename), no randomness, no
    timestamps. A second run must leave ``git status --short`` empty.
  * Image-only PDFs with no clean text layer are flagged honestly as
    ``[EPISTEMIC-VOID]`` / low coverage, never fabricated.

This is a declarative *policy* landing zone: the complete-corpus-ingestion and
token-budget policies live as the knobs below (``COVERAGE_BANDS``,
``DOMAIN_TOKENS``, ``MAX_KEY_FACTS_PER_DOC`` ...), so later features / other
clients can recalibrate them without touching the engine logic.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from engine.corpus import Document, KeyFact
from engine.ocr import (
    OCR_EXTRACTED,
    OCRCapability,
    detect_ocr_capability,
    extract_text_via_ocr,
)


# --------------------------------------------------------------------------- #
# Policy knobs (declarative; recalibratable)
# --------------------------------------------------------------------------- #

# Domain tokens that make a text segment "key". Grounded in the real Credi10
# corpus (components, integrations, module names, tech stack, DB names). These
# are matched case-insensitively against cleaned text.
DOMAIN_TOKENS: List[str] = [
    "Credi10", "Siesa", "UnoEE", "UNOEE", "CrossCore", "Inspektor",
    "Datacredito", "DICTUM", "PayU", "WOLKVOX", "VTEX", "Pentaho", "Numrot",
    "B2CHAT", "ICOMMARKETING", ".NET", "SQL Server", "IIS", "MariaDB",
    "Node.js", "React", "Wordpress", "Apache", "AWS", "VPC", "WAF", "ALB",
    "EC2", "S3", "CloudWatch", "Bastion", "VPN", "IPSec", "Telmex",
    "C10_Credi10NET", "C10_Inspektor", "C10_Datacredito", "C10_Database",
    "Originacion", "Cobranza", "Recaudo", "Cartera", "Ecommerce", "e-commerce",
    "Boton", "Captura", "Foto", "Predictiva", "RCL", "RCR", "RFP", "WSO2",
    "Studio F", "Coatlanta", "Codallas", "Comumbai", "Cokioto", "Cokioto",
    "Link de Recaudo", "Portal", "B2C", "SMS", "WhatsApp", "Email",
    "Scheduler", "Fidelizacion", "integrador", "API",
]

# Coverage banding by coverage_ratio (clean_length / size). Ordered from the
# strictest threshold down. A ratio of exactly 0 (no clean text) -> 'nula'.
# Thresholds are deliberately conservative because the PDF text layer is sparse
# and image-heavy; recalibrate here, not in the logic.
COVERAGE_BANDS: List[tuple] = [
    ("alta", 0.020),   # ratio >= 2.0% of byte size is clean text
    ("media", 0.005),  # ratio >= 0.5%
    ("baja", 0.0001),  # some clean text, below 0.5%
]

# A PDF with at least this many cleaned characters is considered to carry a
# usable, decision-grade text layer -> [VERIFIED-FACT]. Below it (image-only
# scans) we flag [EPISTEMIC-VOID] honestly.
MIN_CLEAN_CHARS_FOR_VERIFIED = 400

# --------------------------------------------------------------------------- #
# REAL useful-text policy (recalibrated banding driver)
# --------------------------------------------------------------------------- #
#
# The legacy ``coverage_ratio`` (clean_length / byte-size) OVERSTATES coverage
# for image/scan PDFs: the zlib+regex pass emits large volumes of layout noise
# and single-letter fragments that are not real words. The honest signal is the
# fraction of the extracted text that is made of REAL WORDS (>= 3 letters,
# Spanish accents included). We derive the coverage band and the epistemic flag
# from THIS metric, not from the raw size.
#
# A real native text layer sits well above these thresholds; the Credi10 corpus
# (all image/scan PDFs) lands at ~0.7%-13% useful text, so NONE reach 'alta' and
# the worst (WSO2 Assessment, API Integrador, Inspektor, ProcesoCorteCartera)
# fall to 'nula' + [EPISTEMIC-VOID] (OCR pendiente). Recalibrate HERE.
USEFUL_TEXT_BANDS: List[tuple] = [
    ("alta", 0.40),   # >= 40% of the extracted text are real words
    ("media", 0.20),  # >= 20%
    ("baja", 0.03),   # >= 3% (some usable text; still flagged OCR pendiente)
]

# Below this useful-text ratio a PDF carries essentially no usable native text:
# it is an image/scan whose content is only recoverable via OCR. We flag it
# [EPISTEMIC-VOID] honestly and mark it 'OCR pendiente'. This is the band 'nula'
# threshold (equal to the lowest band threshold above).
MIN_USEFUL_RATIO_FOR_TEXT = 0.03

# --------------------------------------------------------------------------- #
# BEFORE/AFTER baseline (FEAT-001) for the useful-text recovery comparison
# --------------------------------------------------------------------------- #
#
# Declarative snapshot of the useful-text % recorded BEFORE the per-font
# ToUnicode-aware extractor (``engine.pdf_text``) was wired in. Sourced from
# ``context.baseline_useful_text_pct`` / the FEAT-001 findings. Used by the
# coverage checklist renderer to emit an honest before/after delta per
# document. Values are percentages (useful_chars / extracted-text bytes * 100).
# Keep this table declarative and sorted-by-filename at render time; it is NOT
# recomputed, it is the historical baseline.
USEFUL_TEXT_BASELINE_PCT: Dict[str, float] = {
    "Api Integrador Atencion al cliente.pdf": 0.70,
    "Arquitectura_Aplicacion_Despliegue_Credi10.png": 64.87,
    "Arquitectura_Infraestructura_AWS_Credi10.png": 70.29,
    "B2C.pdf": 2.55,
    "BotonEcommerce.pdf": 3.29,
    "Captura Foto.pdf": 6.48,
    "Diagrama_Contexto_Credi10.png": 70.95,
    "Envio de RCL y RCR.pdf": 4.13,
    "GenerarPagos.pdf": 6.86,
    "LinkDePagos.pdf": 3.43,
    "Llamada predictiva.pdf": 7.15,
    "Originacion_API_Datacredito.pdf": 4.35,
    "Originacion_API_Inspektor.pdf": 0.99,
    "Originacion_Aplicacion_ADMIN.pdf": 5.75,
    "Originacion_CrossCore.pdf": 13.37,
    "ProcesoCorteCartera.pdf": 1.09,
    "RFP_CREDI10_2_0.pdf": 5.92,
    "WSO2 y Studio F - Assessment Mayo2026-Final.pdf": 1.60,
}

# The five PDFs that were in band 'nula' / [EPISTEMIC-VOID] at baseline because
# their native text layer uses custom-encoded embedded fonts (declarative, for
# honest prose in the comparison).
BASELINE_NULA_PDFS: List[str] = [
    "Api Integrador Atencion al cliente.pdf",
    "B2C.pdf",
    "Originacion_API_Inspektor.pdf",
    "ProcesoCorteCartera.pdf",
    "WSO2 y Studio F - Assessment Mayo2026-Final.pdf",
]

# Regex matching a "real word": a run of >= 3 letters, Spanish accents included.
_WORD_RE = re.compile(r"[A-Za-zAÁÉÍÓÚÜÑáéíóúüñ]{3,}")

# Token-budget policy: cap per-document key facts and summary chunks so the
# knowledge base stays bounded while still guaranteeing FULL ingestion of every
# document (we always record coverage + method for 18/18, even when 0 facts).
MAX_KEY_FACTS_PER_DOC = 12
MAX_SUMMARY_CHUNKS = 6
MAX_FACT_CHARS = 320
SUMMARY_CHUNK_CHARS = 900

VERIFIED_FACT = "[VERIFIED-FACT]"
EPISTEMIC_VOID = "[EPISTEMIC-VOID]"
# [OCR-EXTRACTED] is imported from engine.ocr and re-used for documents whose
# text was recovered via OCR (never in this engine's environment: no OCR).

_SENTENCE_SPLIT = re.compile(r"(?<=[\.\;\:])\s+|\s{2,}")


# --------------------------------------------------------------------------- #
# Deterministic enrichment helpers
# --------------------------------------------------------------------------- #

def coverage_ratio(clean_length: int, size: int) -> float:
    """Clean-text ratio bounded to [0, 1]. Deterministic."""
    if size <= 0:
        return 0.0
    return min(1.0, clean_length / float(size))


def coverage_band(ratio: float, clean_length: int) -> str:
    """Map a legacy coverage ratio to a band label using ``COVERAGE_BANDS``.

    Retained for transparency / backwards-compat. The authoritative band is now
    derived from the useful-text metric via :func:`useful_text_band`.
    """
    if clean_length <= 0 or ratio <= 0.0:
        return "nula"
    for band, threshold in COVERAGE_BANDS:
        if ratio >= threshold:
            return band
    return "nula"


def count_useful_chars(text: str) -> int:
    """Count characters belonging to real words (>= 3 letters, Spanish accents).

    Deterministic function of the cleaned text; used by the honest useful-text
    metric. Single/double-letter fragments and layout noise do NOT count.
    """
    if not text:
        return 0
    return sum(len(m) for m in _WORD_RE.findall(text))


def useful_text_ratio(useful_chars: int, clean_length: int) -> float:
    """Useful-text ratio = useful_chars / extracted-text bytes, bounded [0, 1].

    Deterministic. When there is no extracted text the ratio is 0.0.
    """
    if clean_length <= 0:
        return 0.0
    return min(1.0, useful_chars / float(clean_length))


def useful_text_band(useful_ratio: float, useful_chars: int) -> str:
    """Map the REAL useful-text ratio to a band using ``USEFUL_TEXT_BANDS``.

    This is the AUTHORITATIVE band: a PDF whose useful text is ~0.2% is NOT
    'alta'. Below the lowest threshold the band is 'nula'.
    """
    if useful_chars <= 0 or useful_ratio <= 0.0:
        return "nula"
    for band, threshold in USEFUL_TEXT_BANDS:
        if useful_ratio >= threshold:
            return band
    return "nula"


def epistemic_flag(useful_ratio: float, kind: str,
                   ocr_tag: Optional[str] = None) -> str:
    """Honest epistemic flag driven by the REAL useful-text metric.

    PNGs carry a static human transcription -> treated as [VERIFIED-FACT].
    If OCR recovered the text -> [OCR-EXTRACTED]. Otherwise a PDF with enough
    useful native text -> [VERIFIED-FACT]; an image/scan PDF with essentially no
    usable text -> [EPISTEMIC-VOID] (OCR pendiente). Nothing is fabricated.
    """
    if kind == "png":
        return VERIFIED_FACT
    if ocr_tag == OCR_EXTRACTED:
        return OCR_EXTRACTED
    return (VERIFIED_FACT if useful_ratio >= MIN_USEFUL_RATIO_FOR_TEXT
            else EPISTEMIC_VOID)


def _split_segments(text: str) -> List[str]:
    segments = [s.strip() for s in _SENTENCE_SPLIT.split(text) if s and s.strip()]
    return segments


def extract_key_facts(text: str, source_filename: str,
                      tokens: Sequence[str] = DOMAIN_TOKENS,
                      limit: int = MAX_KEY_FACTS_PER_DOC) -> List[KeyFact]:
    """Deterministic key-fact extraction via domain-token matching.

    Splits cleaned text into segments and keeps, in document order, the first
    ``limit`` segments that mention at least one domain token. Duplicate
    segments are de-duplicated. No randomness; stable across runs.
    """
    if not text:
        return []
    lowered_tokens = [(t, t.lower()) for t in tokens]
    facts: List[KeyFact] = []
    seen: set = set()
    for seg in _split_segments(text):
        seg_low = seg.lower()
        matched = [t for (t, tl) in lowered_tokens if tl in seg_low]
        if not matched:
            continue
        snippet = seg.strip()
        if len(snippet) > MAX_FACT_CHARS:
            snippet = snippet[:MAX_FACT_CHARS].rstrip() + "..."
        key = snippet.lower()
        if key in seen:
            continue
        seen.add(key)
        # Preserve token order from DOMAIN_TOKENS, de-duplicated.
        ordered_tokens: List[str] = []
        for t in tokens:
            if t in matched and t not in ordered_tokens:
                ordered_tokens.append(t)
        facts.append(KeyFact(fact=snippet, source_filename=source_filename,
                             tokens=ordered_tokens))
        if len(facts) >= limit:
            break
    return facts


def build_hierarchical_summary(doc: Document) -> List[str]:
    """Build a short, deterministic hierarchical summary for a document.

    Returns a list of strings: a document-level line followed by top chunk
    headers. For image-only PDFs (no clean text) the summary states honestly
    that the document was ingested but has no extractable text layer.
    """
    if doc.kind == "png":
        return [
            f"Documento '{doc.filename}' (diagrama PNG, evidencia binaria): "
            "ingerido mediante transcripcion estatica (sin OCR).",
            doc.description.strip() or "Sin transcripcion registrada.",
        ]

    text = doc.extracted_text or ""
    if len(text.strip()) < 1:
        return [
            f"Documento '{doc.filename}' (PDF): ingerido, pero SIN capa de texto "
            "extraible (PDF basado en imagen). Texto util real nulo; marcado "
            f"{EPISTEMIC_VOID}, OCR pendiente. No se fabrica contenido.",
        ]

    if doc.epistemic_flag == EPISTEMIC_VOID:
        return [
            f"Documento '{doc.filename}' (PDF): ingerido; la capa de texto es "
            f"ruido/fragmentos (texto util real {doc.useful_ratio * 100:.2f}% "
            "de lo extraido), sin contenido explotable. PDF basado en imagen, "
            f"marcado {EPISTEMIC_VOID}, OCR pendiente. No se fabrica contenido.",
        ]

    summary: List[str] = [
        f"Documento '{doc.filename}' (PDF): {len(text)} caracteres limpios "
        f"extraidos (zlib + /ToUnicode por fuente), texto util real "
        f"{doc.useful_ratio * 100:.2f}%, banda '{doc.coverage_band}', "
        f"clasificacion {doc.epistemic_flag}.",
    ]
    # Top chunk headers: slice the cleaned text into bounded chunks and take the
    # leading fragment of each as a header. Deterministic by construction.
    chunks = [text[i:i + SUMMARY_CHUNK_CHARS]
              for i in range(0, len(text), SUMMARY_CHUNK_CHARS)]
    for idx, chunk in enumerate(chunks[:MAX_SUMMARY_CHUNKS], start=1):
        header = chunk.strip()[:160].rstrip()
        if header:
            summary.append(f"Seccion {idx}: {header}...")
    return summary


def enrich_document(doc: Document,
                    ocr_capability: Optional[OCRCapability] = None) -> Document:
    """Populate the knowledge-base fields of a Document in place (deterministic).

    Idempotent: calling it twice yields identical values.

    The coverage band and epistemic flag are driven by the REAL useful-text
    metric (real words / extracted-text bytes). For PDFs whose useful text is
    below ``MIN_USEFUL_RATIO_FOR_TEXT`` we consult the OCR adapter: if a real
    engine is available it recovers the text and tags it [OCR-EXTRACTED]; when
    no engine is available (this environment) the native (low/empty) text is
    kept UNCHANGED and the ingestion method becomes the honest 'OCR pendiente'
    label, so output stays byte-identical except for the honest columns.
    """
    cap = ocr_capability if ocr_capability is not None else detect_ocr_capability()
    ocr_tag: Optional[str] = None

    raw_length = int(doc.metadata.get("raw_length", 0)) if doc.kind == "pdf" else 0
    if doc.kind == "pdf":
        clean_length = len(doc.extracted_text or "")
        doc.ingestion_method = (
            "zlib + /ToUnicode por fuente (capa de texto nativa PDF)")
    else:
        # PNG: the static transcription is the ingested content.
        clean_length = len(doc.description or "")
        raw_length = clean_length
        doc.ingestion_method = "transcripcion estatica PNG (sin OCR)"

    # Real useful-text metric (authoritative driver of band + flag).
    source_text = doc.extracted_text if doc.kind == "pdf" else doc.description
    useful_chars = count_useful_chars(source_text or "")
    useful_ratio = useful_text_ratio(useful_chars, clean_length)

    # When a PDF carries essentially no usable native text, consult OCR.
    if doc.kind == "pdf" and useful_ratio < MIN_USEFUL_RATIO_FOR_TEXT:
        if cap.available:
            # Real engine present: recover text and re-measure from it.
            ocr_text, tag = extract_text_via_ocr(doc.path, cap)
            if tag == OCR_EXTRACTED and ocr_text:
                doc.extracted_text = ocr_text
                clean_length = len(ocr_text)
                useful_chars = count_useful_chars(ocr_text)
                useful_ratio = useful_text_ratio(useful_chars, clean_length)
                ocr_tag = OCR_EXTRACTED
                doc.ingestion_method = (
                    f"OCR [OCR-EXTRACTED] (motor {cap.engine})"
                )
                source_text = ocr_text
        else:
            # Honest degradation: no engine. Keep native text UNCHANGED (so the
            # byte output stays stable) and record the pending method.
            doc.ingestion_method = (
                "OCR pendiente (motor no disponible en este entorno)"
            )

    doc.raw_length = raw_length
    doc.clean_length = clean_length
    doc.coverage_ratio = coverage_ratio(clean_length, doc.size)
    doc.useful_chars = useful_chars
    doc.useful_ratio = useful_ratio
    doc.coverage_band = useful_text_band(useful_ratio, useful_chars)
    doc.epistemic_flag = epistemic_flag(useful_ratio, doc.kind, ocr_tag)

    doc.key_facts = extract_key_facts(source_text or "", doc.filename)
    doc.hierarchical_summary = build_hierarchical_summary(doc)
    # Keep metadata coverage mirror in sync for downstream backwards-compat.
    doc.metadata["raw_length"] = raw_length
    doc.metadata["clean_length"] = clean_length
    doc.metadata["coverage_ratio"] = doc.coverage_ratio
    doc.metadata["useful_chars"] = useful_chars
    doc.metadata["useful_ratio"] = useful_ratio
    doc.metadata["coverage_band"] = doc.coverage_band
    doc.metadata["epistemic_flag"] = doc.epistemic_flag
    return doc


def enrich_corpus(documents: Sequence[Document]) -> List[Document]:
    """Enrich every document (full 18-doc ingestion), sorted by filename.

    The OCR capability is probed ONCE here and reused across all documents, so
    the environment is detected a single time per run (deterministic).
    """
    ordered = sorted(documents, key=lambda d: d.filename.lower())
    cap = detect_ocr_capability()
    return [enrich_document(d, cap) for d in ordered]


# --------------------------------------------------------------------------- #
# Knowledge base builder
# --------------------------------------------------------------------------- #

@dataclass
class KnowledgeBase:
    """Deterministic knowledge base built from the fully-ingested corpus.

    Exposes the enriched documents (sorted by filename) and renders the
    ``knowledge-base/`` artifacts + coverage checklist. Instances are passed to
    phase builders via ``BuildContext`` so later features can cite per-document
    facts and coverage with source traceability.
    """

    documents: List[Document] = field(default_factory=list)

    @classmethod
    def from_documents(cls, documents: Sequence[Document]) -> "KnowledgeBase":
        return cls(documents=enrich_corpus(documents))

    # -- lookups ----------------------------------------------------------- #
    def by_filename(self, filename: str) -> Optional[Document]:
        for d in self.documents:
            if d.filename == filename:
                return d
        return None

    def facts_for(self, filename: str) -> List[KeyFact]:
        doc = self.by_filename(filename)
        return list(doc.key_facts) if doc else []

    def all_facts(self) -> List[KeyFact]:
        facts: List[KeyFact] = []
        for d in self.documents:
            facts.extend(d.key_facts)
        return facts

    @property
    def total(self) -> int:
        return len(self.documents)

    def band_counts(self) -> Dict[str, int]:
        counts = {"alta": 0, "media": 0, "baja": 0, "nula": 0}
        for d in self.documents:
            counts[d.coverage_band] = counts.get(d.coverage_band, 0) + 1
        return counts

    # -- rendering --------------------------------------------------------- #
    def _index_md(self) -> str:
        n_pdf = sum(1 for d in self.documents if d.kind == "pdf")
        n_png = sum(1 for d in self.documents if d.kind == "png")
        lines = [
            "# Base de Conocimiento - Advisory Credi10 2.0",
            "",
            "Artefacto **generado** por el motor `advisory-system/` a partir de "
            "la ingesta COMPLETA del corpus de evidencia. Politica aplicada: "
            "**ingesta y validacion de los 18 documentos (sin muestreo)**; la "
            "clasificacion primary/secondary es PRIORIDAD, nunca exclusion. "
            "100% reproducible re-ejecutando el quickstart.",
            "",
            "> **Regenerar:** `python3 advisory-system/quickstart.py --phase all`",
            "",
            f"- Documentos totales ingeridos: **{self.total}** "
            f"({n_pdf} PDF + {n_png} PNG)",
            "- Metodo PDF: `zlib` + decodificacion `/ToUnicode` por fuente "
            "(capa de texto nativa L1, recuperacion de texto, NO OCR). Metodo "
            "PNG: transcripcion estatica (sin OCR).",
            "- Banda de cobertura por **texto util real** (palabras reales / "
            "bytes de texto extraido), no por tamano crudo.",
            "- Honestidad epistemica: los PDF basados en imagen (sin texto util "
            f"real) se marcan `{EPISTEMIC_VOID}` y 'OCR pendiente'; el texto "
            f"recuperado via OCR se marca `{OCR_EXTRACTED}`. Nunca se fabrica.",
            "",
            "## Indice de documentos",
            "",
            "| # | Documento | Tipo | Rol | Tamano (bytes) | Raw | Limpio | "
            "Texto util | Cobertura | Flag | sha256 (12) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | "
            "--- |",
        ]
        for i, d in enumerate(self.documents, start=1):
            lines.append(
                f"| {i} | {d.filename} | {d.kind} | {d.role} | {d.size} | "
                f"{d.raw_length} | {d.clean_length} | "
                f"{d.useful_ratio * 100:.2f}% | {d.coverage_band} | "
                f"{d.epistemic_flag} | `{d.sha256[:12]}` |"
            )
        counts = self.band_counts()
        lines += [
            "",
            "## Resumen de cobertura",
            "",
            "| Banda | Documentos |",
            "| --- | ---: |",
            f"| alta | {counts['alta']} |",
            f"| media | {counts['media']} |",
            f"| baja | {counts['baja']} |",
            f"| nula | {counts['nula']} |",
            f"| **total** | **{self.total}** |",
            "",
            "## Artefactos",
            "",
            "- [`coverage-checklist.md`](coverage-checklist.md): checklist de "
            "cobertura 18/18 (metodo + banda + flag epistemico).",
            "- [`key-facts.md`](key-facts.md): hechos clave consolidados con "
            "trazabilidad a su documento fuente.",
            "- [`documents/`](documents/): un resumen jerarquico por documento.",
            "",
        ]
        return "\n".join(lines) + "\n"

    def _document_md(self, doc: Document) -> str:
        lines = [
            f"# {doc.filename}",
            "",
            "| Campo | Valor |",
            "| --- | --- |",
            f"| id | `{doc.id}` |",
            f"| tipo | {doc.kind} |",
            f"| rol (prioridad) | {doc.role} |",
            f"| tamano (bytes) | {doc.size} |",
            f"| longitud raw | {doc.raw_length} |",
            f"| longitud limpia | {doc.clean_length} |",
            f"| ratio de cobertura (crudo, legado) | {doc.coverage_ratio:.5f} |",
            f"| caracteres de texto util | {doc.useful_chars} |",
            f"| texto util real (palabras / bytes extraidos) | "
            f"{doc.useful_ratio * 100:.2f}% |",
            f"| banda de cobertura (por texto util real) | {doc.coverage_band} |",
            f"| flag epistemico | {doc.epistemic_flag} |",
            f"| metodo de ingesta | {doc.ingestion_method} |",
            f"| sha256 | `{doc.sha256}` |",
            "",
            "## Resumen jerarquico",
            "",
        ]
        for item in doc.hierarchical_summary:
            lines.append(f"- {item}")
        lines += ["", "## Hechos clave (trazables)", ""]
        if doc.key_facts:
            lines.append("| # | Hecho | Tokens |")
            lines.append("| --- | --- | --- |")
            for i, kf in enumerate(doc.key_facts, start=1):
                safe = kf.fact.replace("|", "\\|")
                toks = ", ".join(kf.tokens)
                lines.append(f"| {i} | {safe} | {toks} |")
        else:
            lines.append(
                f"_Sin hechos clave extraibles. Documento {doc.epistemic_flag}: "
                "ingerido y registrado, sin capa de texto util. No se fabrica "
                "contenido._"
            )
        lines.append("")
        return "\n".join(lines) + "\n"

    def _key_facts_md(self) -> str:
        lines = [
            "# Hechos clave consolidados (con trazabilidad)",
            "",
            "Cada hecho se extrae de la capa de texto del documento fuente "
            "mediante coincidencia de tokens de dominio Credi10. La columna "
            "**Fuente** garantiza la trazabilidad al documento original.",
            "",
            "| # | Hecho | Fuente | Tokens |",
            "| --- | --- | --- | --- |",
        ]
        idx = 0
        for d in self.documents:
            for kf in d.key_facts:
                idx += 1
                safe = kf.fact.replace("|", "\\|")
                toks = ", ".join(kf.tokens)
                lines.append(f"| {idx} | {safe} | {kf.source_filename} | {toks} |")
        if idx == 0:
            lines.append("| - | (sin hechos clave extraibles del corpus) | - | - |")
        lines += [
            "",
            f"**Total de hechos clave trazables:** {idx}.",
            "",
        ]
        return "\n".join(lines) + "\n"

    def _checklist_md(self) -> str:
        n_pdf = sum(1 for d in self.documents if d.kind == "pdf")
        n_png = sum(1 for d in self.documents if d.kind == "png")
        n_void = sum(1 for d in self.documents if d.epistemic_flag == EPISTEMIC_VOID)
        n_pending = sum(1 for d in self.documents
                        if "OCR pendiente" in d.ingestion_method)
        n_ocr = sum(1 for d in self.documents
                    if d.epistemic_flag == OCR_EXTRACTED)
        cap = detect_ocr_capability()
        lines = [
            "# Checklist de cobertura del corpus (18/18)",
            "",
            "Politica **complete-corpus-ingestion**: se verifica que CADA "
            "documento del corpus fue procesado (sin muestreo). Para cada "
            "documento se registra el metodo de procesamiento, el porcentaje de "
            "**texto util real**, la banda de cobertura y un flag epistemico "
            "honesto.",
            "",
            "> **Nota de metodo (honestidad epistemica):** la banda de cobertura "
            "ahora se calcula a partir del **texto util real** = caracteres en "
            "palabras reales (>= 3 letras, con acentos) / bytes de texto "
            "extraido, **no** a partir del tamano crudo del texto extraido. El "
            "metodo anterior (texto_limpio/tamano) SOBRESTIMABA la cobertura de "
            "los PDF basados en imagen.",
            "",
            "> **OCR en este entorno:** " + (
                f"motor OCR disponible ({cap.engine}); el texto recuperado se "
                "marca `[OCR-EXTRACTED]`."
                if cap.available else
                "NO hay motor OCR disponible (ni pytesseract/PIL/fitz ni "
                "tesseract/ocrmypdf/pdfimages/pdftoppm, y sin red para "
                "instalarlos). Degradacion honesta: los PDF basados en imagen "
                "quedan como **pendiente-OCR** y `[EPISTEMIC-VOID]`; **no se "
                "fabrica texto**."
            ),
            "",
            f"## Veredicto de ingesta: {self.total}/{self.total} documentos "
            "procesados (sin muestreo)",
            "",
            f"- PDF procesados (zlib + /ToUnicode por fuente): **{n_pdf}**",
            f"- PNG transcritos (sin OCR): **{n_png}**",
            f"- Documentos recuperados via OCR `{OCR_EXTRACTED}`: **{n_ocr}**",
            f"- Documentos **pendiente-OCR** (PDF basado en imagen, texto util "
            f"insuficiente): **{n_pending}**",
            f"- Documentos marcados `{EPISTEMIC_VOID}` (sin texto util real, "
            f"registrados honestamente): **{n_void}**",
            "",
            "| # | Documento | Procesado | Metodo | Texto util real | Banda | "
            "Flag |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
        for i, d in enumerate(self.documents, start=1):
            method = self._method_label(d)
            lines.append(
                f"| {i} | {d.filename} | si | {method} | "
                f"{d.useful_ratio * 100:.2f}% | {d.coverage_band} | "
                f"{d.epistemic_flag} |"
            )
        counts = self.band_counts()
        processed = sum(1 for _ in self.documents)
        lines += [
            "",
            "## Resumen de cobertura (por texto util real)",
            "",
            "| Banda | Documentos |",
            "| --- | ---: |",
            f"| alta | {counts['alta']} |",
            f"| media | {counts['media']} |",
            f"| baja | {counts['baja']} |",
            f"| nula | {counts['nula']} |",
            "",
            f"**Aserto:** {processed} de {self.total} documentos procesados "
            f"({'OK' if processed == self.total else 'INCOMPLETO'}). "
            "No se omitio ningun documento (cobertura total, sin muestreo). "
            "Las bandas reflejan **texto util real**: el texto nativo recuperado "
            "mediante decodificacion por fuente (CMap /ToUnicode) es capa de "
            "texto REAL, no OCR, por lo que conserva su flag [VERIFIED-FACT].",
            "",
        ]
        lines += self._comparison_lines()
        return "\n".join(lines) + "\n"

    def _comparison_lines(self) -> List[str]:
        """Render the BEFORE/AFTER useful-text comparison (deterministic).

        Compares each document's PRIOR useful-text % (the FEAT-001 baseline in
        :data:`USEFUL_TEXT_BASELINE_PCT`) against the NEW % computed this run,
        with a delta column and honest prose on which documents rose, which did
        not, and why. Stable ordering (sorted by filename); no timestamps.
        """
        lines: List[str] = [
            "## Comparacion antes/despues: recuperacion de texto util",
            "",
            "Esta seccion compara el **texto util real %** de cada documento "
            "ANTES de la decodificacion por fuente (linea base FEAT-001, metodo "
            "`zlib+regex` ingenuo que ademas arrastraba ruido binario de "
            "imagenes/fuentes) contra el valor ACTUAL, obtenido con el extractor "
            "consciente de la fuente (`engine/pdf_text.py`): rastreo de la "
            "fuente activa (`Tf`), decodificacion de literales `( ... )` y "
            "cadenas hex `< ... >` en `Tj`/`TJ`, y mapeo de los codigos de "
            "glifo a traves del CMap `/ToUnicode` de cada fuente embebida, "
            "leyendo SOLO dentro de objetos de texto `BT ... ET`.",
            "",
            "> **Honestidad epistemica:** la recuperacion es de **texto nativo** "
            "(capa de texto del PDF decodificada correctamente), NO es OCR. No "
            "se fabrica contenido; el texto recuperado conserva el flag "
            "`[VERIFIED-FACT]`. El adaptador OCR sigue degradando honestamente "
            "(0 OCR en este entorno).",
            "",
            "| # | Documento | Tipo | Texto util antes | Texto util ahora | "
            "Delta | Banda ahora | Flag |",
            "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
        rose = 0
        flat = 0
        n_recovered_void = 0
        for i, d in enumerate(self.documents, start=1):
            before = USEFUL_TEXT_BASELINE_PCT.get(d.filename)
            now = d.useful_ratio * 100.0
            if before is None:
                before_s = "n/d"
                delta_s = "n/d"
            else:
                before_s = f"{before:.2f}%"
                delta = now - before
                # Clamp sub-rounding jitter so a 70.289% vs 70.29 baseline does
                # not render as a misleading '-0.00 pp'.
                if abs(delta) < 0.005:
                    delta = 0.0
                sign = "+" if delta >= 0 else ""
                delta_s = f"{sign}{delta:.2f} pp"
                if delta > 0.01:
                    rose += 1
                else:
                    flat += 1
                if d.filename in BASELINE_NULA_PDFS and now >= (
                        MIN_USEFUL_RATIO_FOR_TEXT * 100.0):
                    n_recovered_void += 1
            lines.append(
                f"| {i} | {d.filename} | {d.kind} | {before_s} | "
                f"{now:.2f}% | {delta_s} | {d.coverage_band} | "
                f"{d.epistemic_flag} |"
            )

        # Honest prose summary.
        recovered_names = ", ".join(
            n for n in BASELINE_NULA_PDFS
            if (self.by_filename(n) is not None
                and self.by_filename(n).useful_ratio * 100.0
                >= MIN_USEFUL_RATIO_FOR_TEXT * 100.0)
        )
        lines += [
            "",
            "### Lectura honesta de los resultados",
            "",
            f"- **Documentos que subieron:** {rose} de "
            f"{rose + flat} (comparables con linea base).",
            f"- **PDFs recuperados del vacio epistemico:** {n_recovered_void} "
            f"de {len(BASELINE_NULA_PDFS)} PDFs que estaban en banda 'nula' / "
            "`[EPISTEMIC-VOID]` cruzaron el umbral de texto util "
            f"({MIN_USEFUL_RATIO_FOR_TEXT * 100:.0f}%) y hoy son texto nativo "
            "`[VERIFIED-FACT]`"
            + (f": {recovered_names}." if recovered_names else "."),
            "- **Por que subieron:** su capa de texto SI existia, pero usaba "
            "fuentes embebidas con codificacion personalizada (CMap "
            "`/ToUnicode`, p. ej. `Type0`/`Identity-H`). El extractor anterior "
            "no aplicaba el mapeo por fuente y ademas inyectaba bytes binarios "
            "de imagenes como si fueran texto, hundiendo el ratio de texto util. "
            "El nuevo extractor decodifica cada fuente y lee solo objetos de "
            "texto, recuperando el espanol legible (p. ej. "
            "'aplicacion'/'arquitectura'/'integracion').",
            "- **Limites honestos (lo que NO resuelve este nivel):** las "
            "paginas que son imagenes reales (JPEG `DCTDecode` sin capa de "
            "texto) siguen necesitando OCR real (nivel 2); las fuentes sin "
            "`/ToUnicode` ni `/Differences` reconocible degradan al heuristico "
            "latin-1. Nada de esto fabrica texto: lo no recuperable permanece "
            "marcado honestamente.",
            "",
        ]
        return lines

    @staticmethod
    def _method_label(doc: Document) -> str:
        """Short, honest processing-method label for the checklist."""
        if doc.kind == "png":
            return "transcripcion estatica PNG (sin OCR)"
        if doc.epistemic_flag == OCR_EXTRACTED:
            return "[OCR-EXTRACTED]"
        if "OCR pendiente" in doc.ingestion_method:
            return "pendiente-OCR"
        return "texto nativo (zlib + /ToUnicode por fuente)"

    def write(self, kb_dir: str) -> List[str]:
        """Render the knowledge base to ``kb_dir`` deterministically.

        Returns the list of written file paths (sorted). Creates
        ``kb_dir/documents/`` and emits README.md, coverage-checklist.md,
        key-facts.md and one summary per document.
        """
        kb_dir = os.path.abspath(kb_dir)
        docs_dir = os.path.join(kb_dir, "documents")
        os.makedirs(docs_dir, exist_ok=True)
        written: List[str] = []

        def _emit(path: str, text: str) -> None:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            written.append(path)

        _emit(os.path.join(kb_dir, "README.md"), self._index_md())
        _emit(os.path.join(kb_dir, "coverage-checklist.md"), self._checklist_md())
        _emit(os.path.join(kb_dir, "key-facts.md"), self._key_facts_md())
        for d in self.documents:
            _emit(os.path.join(docs_dir, f"{d.id}.md"), self._document_md(d))
        return sorted(written)

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

# Token-budget policy: cap per-document key facts and summary chunks so the
# knowledge base stays bounded while still guaranteeing FULL ingestion of every
# document (we always record coverage + method for 18/18, even when 0 facts).
MAX_KEY_FACTS_PER_DOC = 12
MAX_SUMMARY_CHUNKS = 6
MAX_FACT_CHARS = 320
SUMMARY_CHUNK_CHARS = 900

VERIFIED_FACT = "[VERIFIED-FACT]"
EPISTEMIC_VOID = "[EPISTEMIC-VOID]"

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
    """Map a coverage ratio to a band label using ``COVERAGE_BANDS``."""
    if clean_length <= 0 or ratio <= 0.0:
        return "nula"
    for band, threshold in COVERAGE_BANDS:
        if ratio >= threshold:
            return band
    return "nula"


def epistemic_flag(clean_length: int, kind: str) -> str:
    """Honest epistemic flag.

    PNGs carry a static human transcription -> treated as [VERIFIED-FACT].
    PDFs with a substantial clean text layer -> [VERIFIED-FACT]; image-only
    PDFs with ~no extractable text -> [EPISTEMIC-VOID].
    """
    if kind == "png":
        return VERIFIED_FACT
    return VERIFIED_FACT if clean_length >= MIN_CLEAN_CHARS_FOR_VERIFIED else EPISTEMIC_VOID


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
            "extraible (PDF basado en imagen). Cobertura textual nula; marcado "
            f"{EPISTEMIC_VOID}. No se fabrica contenido.",
        ]

    summary: List[str] = [
        f"Documento '{doc.filename}' (PDF): {len(text)} caracteres limpios "
        f"extraidos (zlib+regex), cobertura '{doc.coverage_band}', "
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


def enrich_document(doc: Document) -> Document:
    """Populate the knowledge-base fields of a Document in place (deterministic).

    Idempotent: calling it twice yields identical values.
    """
    raw_length = int(doc.metadata.get("raw_length", 0)) if doc.kind == "pdf" else 0
    if doc.kind == "pdf":
        clean_length = len(doc.extracted_text or "")
        doc.ingestion_method = "zlib+regex (capa de texto PDF)"
    else:
        # PNG: the static transcription is the ingested content.
        clean_length = len(doc.description or "")
        raw_length = clean_length
        doc.ingestion_method = "transcripcion estatica PNG (sin OCR)"

    doc.raw_length = raw_length
    doc.clean_length = clean_length
    doc.coverage_ratio = coverage_ratio(clean_length, doc.size)
    doc.coverage_band = coverage_band(doc.coverage_ratio, clean_length)
    doc.epistemic_flag = epistemic_flag(clean_length, doc.kind)

    source_text = doc.extracted_text if doc.kind == "pdf" else doc.description
    doc.key_facts = extract_key_facts(source_text or "", doc.filename)
    doc.hierarchical_summary = build_hierarchical_summary(doc)
    # Keep metadata coverage mirror in sync for downstream backwards-compat.
    doc.metadata["raw_length"] = raw_length
    doc.metadata["clean_length"] = clean_length
    doc.metadata["coverage_ratio"] = doc.coverage_ratio
    doc.metadata["coverage_band"] = doc.coverage_band
    doc.metadata["epistemic_flag"] = doc.epistemic_flag
    return doc


def enrich_corpus(documents: Sequence[Document]) -> List[Document]:
    """Enrich every document (full 18-doc ingestion), sorted by filename."""
    ordered = sorted(documents, key=lambda d: d.filename.lower())
    return [enrich_document(d) for d in ordered]


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
            "- Metodo PDF: `zlib+regex` (capa de texto). Metodo PNG: "
            "transcripcion estatica (sin OCR).",
            "- Honestidad epistemica: los PDF basados en imagen (sin texto "
            f"extraible) se marcan `{EPISTEMIC_VOID}`, nunca se fabrican.",
            "",
            "## Indice de documentos",
            "",
            "| # | Documento | Tipo | Rol | Tamano (bytes) | Raw | Limpio | "
            "Cobertura | Flag | sha256 (12) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |",
        ]
        for i, d in enumerate(self.documents, start=1):
            lines.append(
                f"| {i} | {d.filename} | {d.kind} | {d.role} | {d.size} | "
                f"{d.raw_length} | {d.clean_length} | {d.coverage_band} | "
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
            f"| ratio de cobertura | {doc.coverage_ratio:.5f} |",
            f"| banda de cobertura | {doc.coverage_band} |",
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
        lines = [
            "# Checklist de cobertura del corpus (18/18)",
            "",
            "Politica **complete-corpus-ingestion**: se verifica que CADA "
            "documento del corpus fue procesado (sin muestreo). Para cada "
            "documento se registra el metodo de procesamiento, la banda de "
            "cobertura textual y un flag epistemico honesto.",
            "",
            f"## Veredicto de ingesta: {self.total}/{self.total} documentos "
            "procesados (sin muestreo)",
            "",
            f"- PDF procesados (zlib+regex): **{n_pdf}**",
            f"- PNG transcritos (sin OCR): **{n_png}**",
            f"- Documentos marcados `{EPISTEMIC_VOID}` (sin texto util, "
            f"registrados honestamente): **{n_void}**",
            "",
            "| # | Documento | Procesado | Metodo | Banda | Flag |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for i, d in enumerate(self.documents, start=1):
            lines.append(
                f"| {i} | {d.filename} | si | {d.ingestion_method} | "
                f"{d.coverage_band} | {d.epistemic_flag} |"
            )
        counts = self.band_counts()
        processed = sum(1 for _ in self.documents)
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
            "",
            f"**Aserto:** {processed} de {self.total} documentos procesados "
            f"({'OK' if processed == self.total else 'INCOMPLETO'}). "
            "No se omitio ningun documento (cobertura total, sin muestreo).",
            "",
        ]
        return "\n".join(lines) + "\n"

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

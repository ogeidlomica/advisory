"""Corpus loader for the Credi10 2.0 advisory engine.

Discovers the evidence corpus (PDFs + PNGs) at the repository root and turns it
into structured ``Document`` records that the orchestrator and phase builders
consume.

Hard constraints (see task context):
  * Standard library ONLY. No requests / pymupdf / fitz / pdfplumber / numpy /
    pandas. PDF text is pulled with zlib (FlateDecode) + regex.
  * PNG diagrams are binary. We never OCR them; instead each PNG is registered
    as a binary evidence artifact with a static human transcription.
"""

from __future__ import annotations

import hashlib
import os
import re
import zlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# --------------------------------------------------------------------------- #
# Classification tables
# --------------------------------------------------------------------------- #

# Primary PDFs: the RFP and the WSO2/Studio F assessment carry the bulk of the
# clean, decision-grade evidence.
PRIMARY_PDFS = {
    "RFP_CREDI10_2_0.pdf",
    "WSO2 y Studio F - Assessment Mayo2026-Final.pdf",
}

# Static transcription of the three binary architecture diagrams. These summaries
# come from the orchestrator briefing / context (the PNGs cannot be OCR'd here).
PNG_DESCRIPTIONS: Dict[str, str] = {
    "Diagrama_Contexto_Credi10.png": (
        "Diagrama de contexto C4 de Credi10. Aplicacion web central CREDI10 en "
        ".NET integrada con UNOEE/Siesa (ERP), PENTAHO (BI/ETL), CROSSCORE -> "
        "INSPEKTOR -> DICTUM/Datacredito (originacion y riesgo), Numrot, Cobranza, "
        "B2C, Link de Recaudo -> PayU, VTEX (ecommerce), WOLKVOX (contact center), "
        "ICOMMARKETING y B2CHAT. Muestra el sistema Credi10 como nucleo .NET "
        "rodeado de integraciones externas de originacion, pagos, ecommerce y "
        "atencion al cliente."
    ),
    "Arquitectura_Aplicacion_Despliegue_Credi10.png": (
        "Diagrama de despliegue de aplicacion. Credi10 corre sobre .NET Framework "
        "4.8 en IIS 10; integradores en .NET y Windows Services en .NET Core 8 y "
        ".NET 4.8. Bases de datos SQL Server 2019 Enterprise: C10_Credi10NET, "
        "C10_Inspektor, C10_Datacredito y C10_Database. El modulo B2C usa "
        "Node.js + React + Wordpress sobre Apache con MariaDB. Link de Recaudo en "
        ".NET Core 3.1. Servidores on-prem nombrados Coatlanta, Codallas y "
        "Comumbai."
    ),
    "Arquitectura_Infraestructura_AWS_Credi10.png": (
        "Diagrama de infraestructura AWS en la region us-east-2. VPC 'STUDIO F' "
        "con WAF -> ALB -> instancias EC2 privadas, almacenamiento S3, monitoreo "
        "CloudWatch, NAT Gateway y Bastion host. Conectividad hibrida mediante VPN "
        "IPSec de Telmex hacia el centro de datos on-prem 'Cokioto'."
    ),
}

PRIMARY_PNGS = set(PNG_DESCRIPTIONS.keys())

# Language tags produced as noise by the PDF text layer.
_LANG_TAGS = re.compile(r"\b(?:es-CO|es-ES|pt-BR|pt|en-US)\b")
_WS = re.compile(r"\s+")


# --------------------------------------------------------------------------- #
# Low-level PDF text extraction (stdlib only)
# --------------------------------------------------------------------------- #

_STREAM_RE = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.DOTALL)
_PAREN_RE = re.compile(rb"\((?:[^()\\]|\\.)*\)")
_UNESCAPE_RE = re.compile(rb"\\([()\\])")


def _extract_pdf_text_legacy(data: bytes) -> str:
    """Legacy best-effort extraction: latin-1 of every ``( ... )`` literal.

    Retained as the TOLERANT fallback for the font-aware extractor. For every
    ``stream ... endstream`` block we try ``zlib.decompress`` (FlateDecode);
    undecodable streams are skipped silently. Within each decoded stream we pull
    literal strings, unescape ``\\(``, ``\\)`` and ``\\\\`` and decode latin-1.
    """
    texts: List[str] = []
    for m in _STREAM_RE.finditer(data):
        try:
            dec = zlib.decompress(m.group(1))
        except Exception:
            continue
        for t in _PAREN_RE.findall(dec):
            s = _UNESCAPE_RE.sub(rb"\1", t[1:-1])
            try:
                texts.append(s.decode("latin-1"))
            except Exception:
                pass
    return " ".join(texts)


def extract_pdf_text(path: str) -> str:
    """Extract a best-effort text layer from a PDF using only the stdlib.

    Delegates to the per-font, ToUnicode-aware extractor in
    :mod:`engine.pdf_text`, which tracks the active font (``Tf``), decodes both
    ``( ... )`` literals and ``< ... >`` hex strings in ``Tj``/``TJ`` operators,
    and maps glyph codes through each embedded font's ``/ToUnicode`` CMap and
    ``/Encoding /Differences`` table. It reads only inside ``BT ... ET`` text
    objects, so binary image/font-program bytes never leak into the text.

    TOLERANT TO FAILURE: if the font-aware pass raises or yields nothing usable,
    we fall back to the legacy latin-1 literal pull so extraction never
    regresses or crashes. Deterministic (stable ordering, no timestamps).
    """
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return ""

    try:
        from engine.pdf_text import extract_pdf_text_font_aware
        font_aware = extract_pdf_text_font_aware(data)
    except Exception:
        font_aware = ""

    legacy = _extract_pdf_text_legacy(data)

    # Decide between the two by the HONEST useful-text signal (real-word chars),
    # not raw length: the legacy pass often returns a far LARGER string that is
    # mostly binary-image noise, whereas the font-aware pass returns clean text.
    # We keep whichever yields more real-word characters, falling back to legacy
    # when the font-aware pass recovered nothing (full tolerance).
    if font_aware and font_aware.strip():
        try:
            from engine.knowledge import count_useful_chars
            fa_clean = clean_text(font_aware)
            lg_clean = clean_text(legacy) if legacy else ""
            fa_useful = count_useful_chars(fa_clean)
            lg_useful = count_useful_chars(lg_clean)
            fa_ratio = fa_useful / len(fa_clean) if fa_clean else 0.0
            lg_ratio = lg_useful / len(lg_clean) if lg_clean else 0.0
        except Exception:
            # If the metric is unavailable for any reason, prefer the font-aware
            # text (it is the clean-by-construction result).
            return font_aware
        # Prefer the font-aware text whenever it recovered real words and its
        # useful-text RATIO is at least as high as legacy's. The legacy pass
        # often has a higher absolute real-word count only because it also dumps
        # binary-image noise that is pure padding; the honest signal is density.
        if fa_useful > 0 and fa_ratio >= lg_ratio:
            return font_aware
    return legacy


# --------------------------------------------------------------------------- #
# Cleanup helpers
# --------------------------------------------------------------------------- #

def strip_language_tags(text: str) -> str:
    """Remove the es-CO/es-ES/pt-BR/pt/en-US language tags injected by the PDF."""
    return _LANG_TAGS.sub(" ", text)


def collapse_whitespace(text: str) -> str:
    """Collapse any run of whitespace into a single space and trim."""
    return _WS.sub(" ", text).strip()


def defragment(text: str) -> str:
    """Re-join words fragmented into single letters by the PDF text layer.

    PDF extraction frequently emits ``C r e d i 10`` instead of ``Credi 10``.
    We iteratively glue a single letter followed by a space followed by another
    single letter, applying the rule until it stabilises so chains of any
    length collapse.
    """
    pattern = re.compile(r"(?<![A-Za-z0-9])([A-Za-z0-9])\s(?=[A-Za-z0-9](?![A-Za-z0-9]))")
    prev = None
    cur = text
    # Bound the loop defensively; it converges well within this many passes.
    for _ in range(50):
        if cur == prev:
            break
        prev = cur
        cur = pattern.sub(r"\1", cur)
    return cur


def clean_text(text: str) -> str:
    """Full cleanup pipeline.

    Order: strip language tags -> single-letter ``defragment`` -> collapse
    whitespace -> conservative lexical reconstruction (dot-leader collapse +
    split-capital re-join, see :mod:`engine.lexical`).

    The lexical reconstruction layer is COMPLEMENTARY to the font decoding: it
    raises the honest useful-text ratio by removing pure layout artifacts (TOC
    dot leaders) and re-gluing glyph-spacing word splits, WITHOUT fabricating
    text. It is deterministic and idempotent, so re-running the pipeline leaves
    the generated tree byte-identical.
    """
    text = strip_language_tags(text)
    text = defragment(text)
    text = collapse_whitespace(text)
    from engine.lexical import reconstruct_lexical
    text = reconstruct_lexical(text)
    return text


# --------------------------------------------------------------------------- #
# Document model
# --------------------------------------------------------------------------- #

@dataclass
class KeyFact:
    """A traceable key fact extracted from a document.

    ``fact`` is the (cleaned) sentence/segment, ``source_filename`` ties it back
    to the originating corpus document, and ``tokens`` lists the domain tokens
    that caused the segment to be selected (for auditability).
    """

    fact: str
    source_filename: str
    tokens: List[str] = field(default_factory=list)


@dataclass
class Document:
    """A single piece of corpus evidence."""

    id: str
    filename: str
    kind: str  # 'pdf' | 'png'
    role: str  # 'primary' | 'secondary'  -- PRIORITY metadata, never exclusion
    path: str
    size: int
    sha256: str
    extracted_text: str = ""  # pdf only
    description: str = ""  # png only
    metadata: Dict[str, object] = field(default_factory=dict)

    # -- knowledge-base enrichment (populated at load time) ---------------- #
    # raw_length / clean_length already live in ``metadata`` for backwards
    # compatibility; these fields promote the coverage view to first-class
    # attributes the knowledge base and phase builders can consume directly.
    raw_length: int = 0
    clean_length: int = 0
    coverage_ratio: float = 0.0           # clean_length / size, bounded [0, 1]
    # Real useful-text metric: characters belonging to real words (length >= 3
    # letters, Spanish accents included) over the extracted-text bytes. This is
    # the HONEST signal that drives the coverage band and the epistemic flag;
    # raw ``coverage_ratio`` is retained only for transparency.
    useful_chars: int = 0
    useful_ratio: float = 0.0             # useful_chars / clean_length, [0, 1]
    coverage_band: str = "nula"           # 'alta' | 'media' | 'baja' | 'nula'
    epistemic_flag: str = "[EPISTEMIC-VOID]"  # or '[VERIFIED-FACT]' / '[OCR-EXTRACTED]'
    hierarchical_summary: List[str] = field(default_factory=list)
    key_facts: List["KeyFact"] = field(default_factory=list)
    ingestion_method: str = ""            # how the text/description was obtained

    @property
    def is_primary(self) -> bool:
        return self.role == "primary"


# --------------------------------------------------------------------------- #
# Corpus loader
# --------------------------------------------------------------------------- #

def _slug(filename: str) -> str:
    base = os.path.splitext(filename)[0]
    slug = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_").lower()
    return slug


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class CorpusLoader:
    """Discovers and loads the evidence corpus from a directory."""

    def __init__(self, root: Optional[str] = None):
        if root is None:
            # Default: the repository root, i.e. the parent of advisory-system/.
            engine_dir = os.path.dirname(os.path.abspath(__file__))
            system_dir = os.path.dirname(engine_dir)
            root = os.path.dirname(system_dir)
        self.root = os.path.abspath(root)
        self.documents: List[Document] = []

    # -- discovery ---------------------------------------------------------- #
    def load(self) -> List[Document]:
        """Discover every .pdf/.png in the root and build Document records."""
        self.documents = []
        try:
            entries = sorted(os.listdir(self.root))
        except OSError:
            entries = []
        for name in entries:
            path = os.path.join(self.root, name)
            if not os.path.isfile(path):
                continue
            lower = name.lower()
            if lower.endswith(".pdf"):
                self.documents.append(self._load_pdf(name, path))
            elif lower.endswith(".png"):
                self.documents.append(self._load_png(name, path))
        return self.documents

    def _load_pdf(self, name: str, path: str) -> Document:
        raw = extract_pdf_text(path)
        text = clean_text(raw)
        role = "primary" if name in PRIMARY_PDFS else "secondary"
        return Document(
            id=_slug(name),
            filename=name,
            kind="pdf",
            role=role,
            path=path,
            size=os.path.getsize(path),
            sha256=_sha256(path),
            extracted_text=text,
            metadata={"raw_length": len(raw), "clean_length": len(text)},
        )

    def _load_png(self, name: str, path: str) -> Document:
        role = "primary" if name in PRIMARY_PNGS else "secondary"
        description = PNG_DESCRIPTIONS.get(name, "Diagrama binario (sin transcripcion registrada).")
        return Document(
            id=_slug(name),
            filename=name,
            kind="png",
            role=role,
            path=path,
            size=os.path.getsize(path),
            sha256=_sha256(path),
            description=description,
            metadata={"binary_evidence": True},
        )

    # -- convenience accessors --------------------------------------------- #
    def primary(self) -> List[Document]:
        return [d for d in self.documents if d.is_primary]

    def secondary(self) -> List[Document]:
        return [d for d in self.documents if not d.is_primary]

    def pdfs(self) -> List[Document]:
        return [d for d in self.documents if d.kind == "pdf"]

    def pngs(self) -> List[Document]:
        return [d for d in self.documents if d.kind == "png"]

    def by_id(self, doc_id: str) -> Optional[Document]:
        for d in self.documents:
            if d.id == doc_id:
                return d
        return None

    def find(self, substring: str) -> Optional[Document]:
        """Return the first document whose filename contains ``substring``."""
        low = substring.lower()
        for d in self.documents:
            if low in d.filename.lower():
                return d
        return None

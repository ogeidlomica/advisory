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


def extract_pdf_text(path: str) -> str:
    """Extract a best-effort text layer from a PDF using only the stdlib.

    For every ``stream ... endstream`` block we try ``zlib.decompress`` (the
    FlateDecode filter). Undecodable streams are skipped silently so the loader
    never crashes on image-heavy PDFs. Within each decoded stream we pull the
    literal strings of ``Tj``/``TJ`` operators (text between parentheses),
    unescape ``\\(``, ``\\)`` and ``\\\\`` and decode as latin-1.
    """
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return ""
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
    """Full cleanup pipeline: strip tags -> defragment -> collapse whitespace."""
    text = strip_language_tags(text)
    text = defragment(text)
    text = collapse_whitespace(text)
    return text


# --------------------------------------------------------------------------- #
# Document model
# --------------------------------------------------------------------------- #

@dataclass
class Document:
    """A single piece of corpus evidence."""

    id: str
    filename: str
    kind: str  # 'pdf' | 'png'
    role: str  # 'primary' | 'secondary'
    path: str
    size: int
    sha256: str
    extracted_text: str = ""  # pdf only
    description: str = ""  # png only
    metadata: Dict[str, object] = field(default_factory=dict)

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

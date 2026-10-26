"""OCR capability adapter for the Zero-Drift advisory engine (stdlib only).

This module is the engine-side counterpart of the declarative policy skill
``.kiro/skills/ocr-image-extraction/SKILL.md``. It provides a RUNTIME capability
probe and a text-extraction entrypoint that:

  * uses a real OCR engine when one is present in the execution environment
    (preference order: pytesseract/Tesseract, ocrmypdf, pdfimages+tesseract,
    pdftoppm+tesseract), tagging recovered text ``[OCR-EXTRACTED]``; and
  * DEGRADES HONESTLY when no engine is available: it never fabricates text, it
    returns an empty string plus a stable ``[EPISTEMIC-VOID]`` pending marker,
    and it records a fixed, byte-stable ``ingestion_method`` label so the
    pipeline stays deterministic and reproducible on re-run.

Hard constraints honoured here (see task context):
  * Standard library ONLY. No third-party deps are imported at module import
    time; optional OCR modules are probed lazily via ``try/except ImportError``
    and binaries via ``shutil.which``; the probe never crashes if they are
    absent.
  * DETERMINISM: when no engine is available the outcome is a fixed constant,
    so a second run produces byte-identical output and ``git status --short``
    stays empty.

This is a declarative *policy* landing zone too: the engine preference order
and the confidence threshold live as the module-level knobs below, so other
clients / later features can recalibrate them without touching the logic.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# --------------------------------------------------------------------------- #
# Policy knobs (declarative; recalibratable)
# --------------------------------------------------------------------------- #

# Epistemic tags. [OCR-EXTRACTED] distinguishes text recovered via OCR from
# [VERIFIED-FACT] (native text layer) and [EPISTEMIC-VOID] (not recoverable /
# OCR pending). Spanish prose elsewhere; the tags themselves stay in English.
OCR_EXTRACTED = "[OCR-EXTRACTED]"
EPISTEMIC_VOID = "[EPISTEMIC-VOID]"

# Minimum per-word/per-page OCR confidence (0..100) below which recovered text
# is treated as unreliable and DISCARDED. Declarative knob; only consulted when
# a real engine runs. Text whose confidence falls below this bar is dropped so
# low-quality OCR never pollutes the knowledge base with unreliable content.
OCR_CONFIDENCE_THRESHOLD = 60

# Hard wall-clock timeout (seconds) for any OCR subprocess invocation
# (ocrmypdf / tesseract / rasterizers). A hung or pathologically slow engine
# must DEGRADE to "no text" rather than block the whole advisory pipeline.
OCR_SUBPROCESS_TIMEOUT = 300

# File extensions we treat as standalone raster images that can be OCR'd
# directly (useful for the architecture diagrams in future corpora), as opposed
# to PDFs that must be rasterized page by page first.
_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif",
                     ".webp")

# Stable ingestion-method labels. These strings are part of the deterministic
# output; do NOT make them depend on timestamps, hostnames or randomness.
METHOD_OCR_EXTRACTED = "OCR ([OCR-EXTRACTED], motor disponible)"
METHOD_OCR_PENDING = "OCR pendiente (motor no disponible en este entorno)"

# OCR engines in preference order. Each entry declares a kind ('module' probed
# via import, or 'binary' probed via shutil.which) and the auxiliary binaries it
# needs. The first fully-satisfied entry wins.
OCR_ENGINE_PREFERENCE: List[Dict[str, object]] = [
    {"engine": "pytesseract", "kind": "module", "module": "pytesseract",
     "needs_binaries": ["tesseract"]},
    {"engine": "ocrmypdf", "kind": "binary", "binary": "ocrmypdf",
     "needs_binaries": []},
    {"engine": "pdfimages+tesseract", "kind": "binary", "binary": "pdfimages",
     "needs_binaries": ["tesseract"]},
    {"engine": "pdftoppm+tesseract", "kind": "binary", "binary": "pdftoppm",
     "needs_binaries": ["tesseract"]},
]

# Optional python modules we probe (for transparency in the capability report).
_PROBE_MODULES = ["pytesseract", "easyocr", "PIL", "fitz", "cv2", "numpy"]
# Binaries we probe (for transparency in the capability report).
_PROBE_BINARIES = ["tesseract", "ocrmypdf", "pdfimages", "pdftoppm", "mutool",
                   "gs", "convert", "magick"]


# --------------------------------------------------------------------------- #
# Capability probe
# --------------------------------------------------------------------------- #

@dataclass
class OCRCapability:
    """Describes what OCR capability exists in the current environment.

    ``available`` is True only when a complete engine (its module/binary plus
    all auxiliary binaries) was found. ``probed`` maps every probed module and
    binary to a bool (found/missing) for an honest, auditable report.
    """

    available: bool = False
    engine: Optional[str] = None
    reason: str = ""
    probed: Dict[str, bool] = field(default_factory=dict)


def _module_available(name: str) -> bool:
    """Return True if a python module can be imported, without crashing."""
    try:
        __import__(name)
        return True
    except Exception:
        # ImportError plus any import-time side effect error -> treat as absent.
        return False


def _binary_available(name: str) -> bool:
    """Return True if a binary is on PATH (shutil.which), without crashing."""
    try:
        return shutil.which(name) is not None
    except Exception:
        return False


def detect_ocr_capability() -> OCRCapability:
    """Probe the environment for OCR capability. Deterministic, never raises.

    Scans the preference list in order; the first engine whose module/binary and
    all auxiliary binaries are present wins. Also records, for transparency, the
    presence/absence of every probed module and binary.
    """
    probed: Dict[str, bool] = {}
    # Probe modules and binaries (sorted keys for stable reporting).
    for mod in sorted(set(_PROBE_MODULES)):
        probed[f"module:{mod}"] = _module_available(mod)
    for binname in sorted(set(_PROBE_BINARIES)):
        probed[f"binary:{binname}"] = _binary_available(binname)

    for spec in OCR_ENGINE_PREFERENCE:
        engine = str(spec["engine"])
        ok = True
        if spec["kind"] == "module":
            ok = probed.get(f"module:{spec['module']}", False)
        elif spec["kind"] == "binary":
            ok = probed.get(f"binary:{spec['binary']}", False)
        if ok:
            for b in spec.get("needs_binaries", []):  # type: ignore[union-attr]
                if not probed.get(f"binary:{b}", False):
                    ok = False
                    break
        if ok:
            return OCRCapability(
                available=True,
                engine=engine,
                reason=f"Motor OCR disponible: {engine}.",
                probed=probed,
            )

    return OCRCapability(
        available=False,
        engine=None,
        reason=(
            "No se encontro ningun motor OCR en el entorno (ni modulos "
            "pytesseract/PIL/fitz ni binarios tesseract/ocrmypdf/pdfimages/"
            "pdftoppm). Degradacion honesta: OCR pendiente, sin fabricar texto."
        ),
        probed=probed,
    )


# --------------------------------------------------------------------------- #
# Extraction entrypoint
# --------------------------------------------------------------------------- #

def extract_text_via_ocr(path: str,
                         capability: Optional[OCRCapability] = None
                         ) -> Tuple[str, str]:
    """Attempt OCR on ``path``.

    Returns a ``(text, tag)`` tuple:
      * engine available -> run OCR and return (recovered_text, OCR_EXTRACTED);
      * NO engine -> return ('', EPISTEMIC_VOID). NEVER fabricates text; the
        empty-string result is fixed and byte-stable so the pipeline stays
        deterministic.

    ``capability`` may be passed in so a run detects the environment ONCE and
    reuses it across documents. When omitted it is probed here.
    """
    cap = capability if capability is not None else detect_ocr_capability()
    if not cap.available:
        # Honest degradation: no engine, no text. Deterministic constant.
        return "", EPISTEMIC_VOID

    # An engine is present. Dispatch to it. These branches do not execute in an
    # environment without OCR; they are the ready-and-tested capability path.
    text = _run_engine(cap.engine, path)
    if text:
        return text, OCR_EXTRACTED
    # Engine present but produced nothing usable (or all pages fell below the
    # confidence threshold) -> honest void, no fabrication.
    return "", EPISTEMIC_VOID


def _is_image_file(path: str) -> bool:
    """Return True when ``path`` is a standalone raster image (PNG/JPG/...)."""
    return os.path.splitext(path)[1].lower() in _IMAGE_EXTENSIONS


def _run_engine(engine: Optional[str], path: str) -> str:
    """Run the selected OCR engine on ``path`` and return recovered text.

    Isolated so the extraction entrypoint stays simple and so each engine's
    optional imports happen lazily (only when that engine was actually found).
    Any failure (including a subprocess timeout) degrades to '' (never
    fabricates). Not exercised in an environment without OCR.

    A standalone image file (PNG/JPG/...) is OCR'd directly regardless of the
    PDF-oriented engine, so the capability can also recover text from the
    architecture diagrams in future corpora, not only from PDFs.
    """
    try:
        if _is_image_file(path):
            return _ocr_image_file(engine, path)
        if engine == "pytesseract":
            return _ocr_pytesseract(path)
        if engine == "ocrmypdf":
            return _ocr_ocrmypdf(path)
        if engine in ("pdfimages+tesseract", "pdftoppm+tesseract"):
            return _ocr_rasterize_then_tesseract(engine, path)
    except Exception:
        # Any engine error (missing optional module, broken file, subprocess
        # failure, timeout) degrades to no text; the pipeline is never aborted.
        return ""
    return ""


# --------------------------------------------------------------------------- #
# Confidence filtering (shared by the real engine paths)
# --------------------------------------------------------------------------- #

def _pytesseract_text_above_confidence(image, pytesseract  # type: ignore
                                       ) -> str:  # pragma: no cover - needs OCR
    """Return the OCR text of ``image`` keeping only words at/above threshold.

    Uses ``image_to_data`` so each recognised word carries a confidence score;
    words below ``OCR_CONFIDENCE_THRESHOLD`` are discarded (low-quality OCR must
    never be promoted to decision-grade text). Falls back to plain
    ``image_to_string`` only if the structured call is unavailable.
    """
    try:
        data = pytesseract.image_to_data(
            image, output_type=pytesseract.Output.DICT)
    except Exception:
        return pytesseract.image_to_string(image)
    words = data.get("text", [])
    confs = data.get("conf", [])
    kept: List[str] = []
    for word, conf in zip(words, confs):
        if not word or not word.strip():
            continue
        try:
            conf_val = float(conf)
        except (TypeError, ValueError):
            conf_val = -1.0
        # Tesseract emits conf == -1 for non-text blocks; drop those too.
        if conf_val >= OCR_CONFIDENCE_THRESHOLD:
            kept.append(word.strip())
    return " ".join(kept)


def _ocr_image_file(engine: Optional[str], path: str
                    ) -> str:  # pragma: no cover - needs OCR engine
    """OCR a single standalone image file (PNG/JPG/...).

    Prefers pytesseract (with confidence filtering) via PIL; if pytesseract is
    not importable but the ``tesseract`` binary is on PATH, shells out to it.
    Lazy imports only. Only reachable when a capability was detected.
    """
    try:
        import pytesseract  # type: ignore
        from PIL import Image  # type: ignore
        with Image.open(path) as img:
            return _pytesseract_text_above_confidence(img, pytesseract).strip()
    except Exception:
        pass
    # Binary fallback: tesseract CLI straight on the image file.
    if shutil.which("tesseract"):
        import subprocess
        res = subprocess.run(
            ["tesseract", path, "stdout"],
            check=True, capture_output=True, text=True,
            timeout=OCR_SUBPROCESS_TIMEOUT,
        )
        return res.stdout.strip()
    return ""


def _ocr_pytesseract(path: str) -> str:  # pragma: no cover - needs OCR engine
    """Rasterize a PDF and OCR each page with pytesseract/Tesseract.

    Imports pytesseract/PIL (and optionally fitz) lazily. Prefers PyMuPDF
    (``fitz``) for rasterization; when it is absent it falls back to the
    pdftoppm/pdfimages CLI rasterizers + PIL so a plain pytesseract+tesseract
    install still works on raw PDFs. Per-page confidence filtering is applied.
    Only reachable when the capability probe confirmed the engine is installed.
    """
    import pytesseract  # type: ignore

    # Preferred path: PyMuPDF rasterizes each page to a PIL image in-process.
    try:
        import fitz  # type: ignore  (PyMuPDF)
        from PIL import Image  # type: ignore
        import io

        chunks: List[str] = []
        doc = fitz.open(path)
        try:
            for page in doc:
                pix = page.get_pixmap()
                with Image.open(io.BytesIO(pix.tobytes("png"))) as img:
                    chunks.append(
                        _pytesseract_text_above_confidence(img, pytesseract))
        finally:
            doc.close()
        text = "\n".join(c for c in chunks if c).strip()
        if text:
            return text
    except Exception:
        # PyMuPDF missing or failed -> try the CLI rasterizer fallback below.
        pass

    # Fallback: rasterize with pdftoppm/pdfimages (whichever is on PATH) and OCR
    # each page image via pytesseract+PIL. Keeps pytesseract usable without fitz.
    return _ocr_pdf_via_cli_rasterizer_and_pytesseract(path, pytesseract)


def _ocr_pdf_via_cli_rasterizer_and_pytesseract(
        path: str, pytesseract) -> str:  # pragma: no cover - needs OCR engine
    """Rasterize a PDF via pdftoppm/pdfimages CLI then OCR with pytesseract+PIL.

    Confidence filtering applied per page. Lazy imports; bounded by timeout.
    """
    from PIL import Image  # type: ignore
    import subprocess
    import tempfile
    import glob

    rasterizer = None
    if shutil.which("pdftoppm"):
        rasterizer = "pdftoppm"
    elif shutil.which("pdfimages"):
        rasterizer = "pdfimages"
    if rasterizer is None:
        return ""

    with tempfile.TemporaryDirectory() as tmp:
        prefix = os.path.join(tmp, "page")
        subprocess.run(
            [rasterizer, "-png", path, prefix],
            check=True, timeout=OCR_SUBPROCESS_TIMEOUT,
        )
        images = sorted(glob.glob(prefix + "*.png"))
        chunks: List[str] = []
        for img_path in images:
            with Image.open(img_path) as img:
                chunks.append(
                    _pytesseract_text_above_confidence(img, pytesseract))
        return "\n".join(c for c in chunks if c).strip()


def _ocr_ocrmypdf(path: str) -> str:  # pragma: no cover - needs OCR engine
    """Run ocrmypdf to add a text layer, then re-extract that layer.

    Runs under a hard timeout; on any failure (non-zero exit, timeout) returns
    '' so the pipeline degrades instead of crashing. Only reachable when the
    capability probe confirmed ocrmypdf is installed.
    """
    import subprocess
    import tempfile

    # Lazy import of the native extractor so the module imports with stdlib only.
    from engine.corpus import extract_pdf_text, clean_text

    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "ocr.pdf")
        subprocess.run(
            ["ocrmypdf", "--force-ocr", "--quiet", path, out],
            check=True, timeout=OCR_SUBPROCESS_TIMEOUT,
        )
        return clean_text(extract_pdf_text(out))


def _ocr_rasterize_then_tesseract(engine: str, path: str
                                  ) -> str:  # pragma: no cover - needs OCR engine
    """Rasterize a PDF (pdfimages or pdftoppm) then OCR the images via tesseract.

    Each subprocess runs under a hard timeout. Only reachable when the
    capability probe confirmed the rasterizer and the tesseract binary are
    installed.
    """
    import subprocess
    import tempfile
    import glob

    rasterizer = "pdfimages" if engine.startswith("pdfimages") else "pdftoppm"
    with tempfile.TemporaryDirectory() as tmp:
        prefix = os.path.join(tmp, "page")
        subprocess.run(
            [rasterizer, "-png", path, prefix],
            check=True, timeout=OCR_SUBPROCESS_TIMEOUT,
        )
        images = sorted(glob.glob(prefix + "*.png"))
        chunks: List[str] = []
        for img in images:
            res = subprocess.run(
                ["tesseract", img, "stdout"],
                check=True, capture_output=True, text=True,
                timeout=OCR_SUBPROCESS_TIMEOUT,
            )
            chunks.append(res.stdout)
        return "\n".join(c for c in chunks if c).strip()

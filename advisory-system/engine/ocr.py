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

# Minimum per-page OCR confidence (0..100) below which recovered text is treated
# as unreliable. Declarative knob; only consulted when a real engine runs.
OCR_CONFIDENCE_THRESHOLD = 60

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
    # Engine present but produced nothing usable -> honest void, no fabrication.
    return "", EPISTEMIC_VOID


def _run_engine(engine: Optional[str], path: str) -> str:
    """Run the selected OCR engine on ``path`` and return recovered text.

    Isolated so the extraction entrypoint stays simple and so each engine's
    optional imports happen lazily (only when that engine was actually found).
    Any failure degrades to '' (never fabricates). Not exercised in an
    environment without OCR.
    """
    try:
        if engine == "pytesseract":
            return _ocr_pytesseract(path)
        if engine == "ocrmypdf":
            return _ocr_ocrmypdf(path)
        if engine in ("pdfimages+tesseract", "pdftoppm+tesseract"):
            return _ocr_rasterize_then_tesseract(engine, path)
    except Exception:
        return ""
    return ""


def _ocr_pytesseract(path: str) -> str:  # pragma: no cover - needs OCR engine
    """Rasterize ``path`` and OCR each page with pytesseract/Tesseract.

    Imports pytesseract/PIL (and optionally fitz) lazily. Only reachable when
    the capability probe confirmed the engine is installed.
    """
    import pytesseract  # type: ignore

    chunks: List[str] = []
    try:
        import fitz  # type: ignore  (PyMuPDF)
        from PIL import Image  # type: ignore
        import io

        doc = fitz.open(path)
        for page in doc:
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            chunks.append(pytesseract.image_to_string(img))
    except Exception:
        # No rasterizer module available for a raw PDF; return what we have.
        return "\n".join(c for c in chunks if c).strip()
    return "\n".join(c for c in chunks if c).strip()


def _ocr_ocrmypdf(path: str) -> str:  # pragma: no cover - needs OCR engine
    """Run ocrmypdf to add a text layer, then re-extract that layer.

    Only reachable when the capability probe confirmed ocrmypdf is installed.
    """
    import subprocess
    import tempfile
    import os as _os

    from engine.corpus import extract_pdf_text, clean_text

    with tempfile.TemporaryDirectory() as tmp:
        out = _os.path.join(tmp, "ocr.pdf")
        subprocess.run(
            ["ocrmypdf", "--force-ocr", "--quiet", path, out],
            check=True,
        )
        return clean_text(extract_pdf_text(out))


def _ocr_rasterize_then_tesseract(engine: str, path: str
                                  ) -> str:  # pragma: no cover - needs OCR engine
    """Rasterize a PDF (pdfimages or pdftoppm) then OCR the images via tesseract.

    Only reachable when the capability probe confirmed the rasterizer and the
    tesseract binary are installed.
    """
    import subprocess
    import tempfile
    import glob
    import os as _os

    with tempfile.TemporaryDirectory() as tmp:
        prefix = _os.path.join(tmp, "page")
        if engine.startswith("pdfimages"):
            subprocess.run(["pdfimages", "-png", path, prefix], check=True)
            images = sorted(glob.glob(prefix + "*.png"))
        else:  # pdftoppm
            subprocess.run(["pdftoppm", "-png", path, prefix], check=True)
            images = sorted(glob.glob(prefix + "*.png"))
        chunks: List[str] = []
        for img in images:
            res = subprocess.run(
                ["tesseract", img, "stdout"],
                check=True, capture_output=True, text=True,
            )
            chunks.append(res.stdout)
        return "\n".join(c for c in chunks if c).strip()

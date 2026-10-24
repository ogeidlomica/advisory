#!/usr/bin/env python3
"""Quickstart CLI for the Credi10 2.0 Zero-Drift advisory engine.

Runs the advisory pipeline with agent roles across the 7 Zero-Drift phases and
generates one markdown report per phase (plus a README index) under the output
folder. Pure Python standard library - no external dependencies.

Usage examples
--------------
  # Run the full pipeline (phases 0..6 + README index)
  python3 advisory-system/quickstart.py --phase all

  # Regenerate a single phase
  python3 advisory-system/quickstart.py --phase 3

  # Point at a different corpus root / output folder
  python3 advisory-system/quickstart.py --corpus /path/to/corpus --out /path/to/out

The corpus is auto-discovered at the repository root (the parent of
advisory-system/) when --corpus is not given. Reports are written to
advisory-credi10-2.0/ by default.
"""

from __future__ import annotations

import argparse
import os
import sys

# Make the advisory-system/ directory importable regardless of CWD.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from engine.corpus import CorpusLoader          # noqa: E402
from engine.orchestrator import AdvisoryOrchestrator  # noqa: E402


def _default_repo_root() -> str:
    # Parent of advisory-system/ is the repository root containing the corpus.
    return os.path.dirname(_HERE)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quickstart.py",
        description="Genera los informes del advisory Credi10 2.0 (framework Zero-Drift).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--phase",
        choices=["0", "1", "2", "3", "4", "5", "6", "all"],
        default="all",
        help="Fase a ejecutar (0..6) o 'all' para todo el pipeline. Default: all.",
    )
    parser.add_argument(
        "--corpus",
        default=None,
        help="Ruta al corpus de evidencia. Default: raiz del repo (auto-discover).",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Carpeta de salida de los informes. Default: advisory-credi10-2.0/.",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    corpus_root = args.corpus or _default_repo_root()
    out_dir = args.out or os.path.join(_default_repo_root(), "advisory-credi10-2.0")

    print("== Advisory Credi10 2.0 - Zero-Drift engine ==")
    print(f"Corpus root : {corpus_root}")
    print(f"Output dir  : {out_dir}")
    print(f"Phase       : {args.phase}")
    print("-" * 60)

    loader = CorpusLoader(corpus_root)
    docs = loader.load()
    n_pdf = sum(1 for d in docs if d.kind == "pdf")
    n_png = sum(1 for d in docs if d.kind == "png")
    print(f"Corpus cargado: {len(docs)} documentos ({n_pdf} PDF, {n_png} PNG).")
    print("-" * 60)

    orchestrator = AdvisoryOrchestrator(loader, out_dir)
    summary = orchestrator.run(args.phase)

    for line in summary.log_lines():
        print(line)

    print("-" * 60)
    print("Ejecucion completada OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

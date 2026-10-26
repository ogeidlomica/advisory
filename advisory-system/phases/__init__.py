"""Per-phase report builders.

FEAT-001 ships minimal placeholder builders so the pipeline runs green. Later
features (FEAT-002/003/004) replace these per-phase builders with corpus-grounded
content. Each builder is a callable ``builder(ctx) -> str`` returning the full
markdown body for its phase report.

The placeholder builders are intentionally kept in ``builders.py`` so they can be
swapped out phase-by-phase without touching the engine.
"""

from phases.builders import BUILDERS, build_readme  # noqa: F401

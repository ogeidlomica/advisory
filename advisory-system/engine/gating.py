"""Stage-gate evaluation for the Zero-Drift engine.

The orchestrator used to pass ``gate_satisfied=True`` unconditionally, so every
QG-0..QG-6 printed GO and the No-Go branch was dead code. This module replaces
that placeholder with a small, deterministic evaluator that derives the gate
verdict from *objective, checkable* properties of the report body that was
actually generated for the phase (plus, where applicable, the Hilo Dorado
traceability encoded in that body).

``evaluate_gate(phase, body)`` returns ``(satisfied, reasons)``:

  * ``satisfied`` is ``True`` only when the body honours the structural
    contract every report must satisfy and any phase-specific traceability
    condition holds.
  * ``reasons`` lists the concrete failures (empty when satisfied). It feeds the
    No-Go verdict line so a failing report explains *why* it is No-Go.

Stdlib only; no third-party imports.
"""

from __future__ import annotations

import re
from typing import List, Set, Tuple

# --------------------------------------------------------------------------- #
# Structural contract tokens
# --------------------------------------------------------------------------- #

# Epistemic honesty tags used across the reports (English tags over Spanish
# prose). A report must carry at least one so claims are explicitly qualified.
_EPISTEMIC_TAG_RE = re.compile(
    r"\[(DOC-ASSUMPTION|DOC-CONFLICT|EPISTEMIC-VOID|INFERENCE|VERIFIED|DOC-[A-Z]+)\]"
)

# Hilo Dorado element ids, e.g. DRV-001, GAP-012, ROI-003.
_ID_RE = {
    "DRV": re.compile(r"DRV-\d+"),
    "GAP": re.compile(r"GAP-\d+"),
    "REL": re.compile(r"REL-\d+"),
    "ROI": re.compile(r"ROI-\d+"),
}


def _distinct_ids(body: str, stage: str) -> Set[str]:
    return set(_ID_RE[stage].findall(body))


def _ids_on_each_line(body: str, needle_stage: str, companion_stage: str) -> List[str]:
    """Return the ``needle`` ids that never share a line with a ``companion`` id.

    Used for document-level traceability: e.g. every ROI id must appear on at
    least one line that also names a DRV id (its driver ancestor). Ids that
    satisfy this on any single line are considered traceable.
    """
    needle_re = _ID_RE[needle_stage]
    companion_re = _ID_RE[companion_stage]
    traced: Set[str] = set()
    present: Set[str] = set()
    for line in body.splitlines():
        found = needle_re.findall(line)
        if not found:
            continue
        present.update(found)
        if companion_re.search(line):
            traced.update(found)
    return sorted(present - traced)


# --------------------------------------------------------------------------- #
# Structural contract
# --------------------------------------------------------------------------- #

def structural_reasons(phase, body: str) -> List[str]:
    """Return reasons the body breaks the universal structural contract."""
    reasons: List[str] = []

    if body.count("```mermaid") < 1:
        reasons.append("Falta al menos un diagrama ```mermaid```.")

    # A markdown table row starts with a pipe at the beginning of a line.
    if not any(line.lstrip().startswith("|") for line in body.splitlines()):
        reasons.append("Falta al menos una tabla markdown.")

    if not _EPISTEMIC_TAG_RE.search(body):
        reasons.append(
            "Falta al menos una etiqueta epistemica "
            "([DOC-ASSUMPTION]/[DOC-CONFLICT]/[EPISTEMIC-VOID]/...)."
        )

    gate_id = phase.gate.id
    if f"Veredicto {gate_id}" not in body:
        reasons.append(f"Falta el andamiaje de veredicto 'Veredicto {gate_id}'.")

    return reasons


# --------------------------------------------------------------------------- #
# Phase-specific Hilo Dorado conditions
# --------------------------------------------------------------------------- #

def traceability_reasons(phase, body: str) -> List[str]:
    """Phase-specific No-Go conditions tied to the Hilo Dorado.

    QG-3: every GAP must be relieved (co-occur with a REL) and every REL must
          trace to a DRV (co-occur with a DRV). Models the declared No-Go
          "hay gaps sin reliever o relievers sin trazabilidad a un driver".
    QG-6: every ROI/outcome must trace to a DRV ancestor. Models the declared
          No-Go "el ROI ... rompe el Hilo Dorado".
    """
    reasons: List[str] = []
    gate_id = phase.gate.id

    if gate_id == "QG-3":
        if not _distinct_ids(body, "GAP"):
            reasons.append("No se declararon gaps (GAP-xxx) en el informe.")
        orphan_gaps = _ids_on_each_line(body, "GAP", "REL")
        if orphan_gaps:
            reasons.append(
                "Gaps sin reliever trazable: " + ", ".join(orphan_gaps) + "."
            )
        orphan_rels = _ids_on_each_line(body, "REL", "DRV")
        if orphan_rels:
            reasons.append(
                "Relievers sin trazabilidad a un driver: "
                + ", ".join(orphan_rels) + "."
            )

    elif gate_id == "QG-6":
        if not _distinct_ids(body, "ROI"):
            reasons.append("No se declararon outcomes/ROI (ROI-xxx) en el informe.")
        orphan_rois = _ids_on_each_line(body, "ROI", "DRV")
        if orphan_rois:
            reasons.append(
                "Outcomes/ROI sin ancestro driver (Hilo Dorado roto): "
                + ", ".join(orphan_rois) + "."
            )

    return reasons


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def evaluate_gate(phase, body: str) -> Tuple[bool, List[str]]:
    """Evaluate the phase's stage-gate against the generated report body.

    Returns ``(satisfied, reasons)``. ``satisfied`` is ``True`` only when the
    structural contract holds and every phase-specific traceability condition
    passes; ``reasons`` enumerates the failures otherwise.
    """
    reasons: List[str] = []
    reasons.extend(structural_reasons(phase, body))
    reasons.extend(traceability_reasons(phase, body))
    return (not reasons, reasons)

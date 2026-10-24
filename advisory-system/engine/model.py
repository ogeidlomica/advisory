"""Zero-Drift domain model: Roles, Cells, Phases, Quality Gates and the
Hilo Dorado (Golden Thread) traceability chain.

Everything here is declarative data wrapped in small dataclasses so that the
orchestrator and the per-phase report builders can consume it uniformly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# --------------------------------------------------------------------------- #
# Roles & Cells
# --------------------------------------------------------------------------- #

GOVERNANCE = "Comite de Gobierno"
CELL_DISCOVERY = "Celula 1 - Discovery"
CELL_DESIGN = "Celula 2 - Diseno"
CELL_VALUE = "Celula 3 - Valor y Habilitacion"


@dataclass
class Role:
    """A Zero-Drift role, expressed as declarative data."""

    code: str
    name: str
    scope: str          # core responsibility
    income: str         # inputs consumed
    outcome: str        # output deliverables
    verifies: List[str] = field(default_factory=list)  # phase ids this role verifies
    cell: str = ""

    @property
    def is_verifier(self) -> bool:
        return bool(self.verifies)


# --------------------------------------------------------------------------- #
# Quality Gates
# --------------------------------------------------------------------------- #

@dataclass
class Gate:
    """A stage-gate (QG-0 .. QG-6)."""

    id: str
    name: str
    criteria: List[str] = field(default_factory=list)
    nogo_condition: str = ""

    def verdict(self, satisfied: bool, reasons: Optional[List[str]] = None) -> str:
        """Return a human Go / No-Go verdict line for the report footer.

        When ``satisfied`` is ``False`` the verdict names the declared No-Go
        condition and, if ``reasons`` are supplied, the concrete checks that
        failed (as computed by ``engine.gating.evaluate_gate``).
        """
        if satisfied:
            return f"{self.id} :: GO - Criterios de salida satisfechos."
        detail = self.nogo_condition
        if reasons:
            detail = f"{detail} [{'; '.join(reasons)}]"
        return f"{self.id} :: NO-GO - {detail}"


# --------------------------------------------------------------------------- #
# Phases
# --------------------------------------------------------------------------- #

@dataclass
class Phase:
    """A Zero-Drift phase (Fase 0 .. Fase 6)."""

    id: str                 # '0','1','2','3','4','5','6'
    name: str
    leaders: List[str]      # role codes producing the phase (Responsible)
    verifier: str           # role code gating the phase (Verifier)
    deliverables: List[str] # deliverable codes E0.1 ..
    gate: Gate
    filename: str           # report filename
    accountable: str = "EM" # Accountable owner by default
    consulted: List[str] = field(default_factory=list)
    informed: List[str] = field(default_factory=list)
    builder: Optional[object] = None  # report-builder callable, wired later


# --------------------------------------------------------------------------- #
# RACI-V helper
# --------------------------------------------------------------------------- #

@dataclass
class RaciV:
    """RACI-V assignment for a phase (Producer R separated from Verifier V)."""

    responsible: List[str]
    accountable: str
    consulted: List[str]
    informed: List[str]
    verifier: str

    def as_rows(self) -> List[tuple]:
        return [
            ("R - Responsible", ", ".join(self.responsible)),
            ("A - Accountable", self.accountable),
            ("C - Consulted", ", ".join(self.consulted) or "-"),
            ("I - Informed", ", ".join(self.informed) or "-"),
            ("V - Verifier", self.verifier),
        ]


def raci_v_for(phase: Phase) -> RaciV:
    """Derive the RACI-V matrix for a phase from its declarative data."""
    return RaciV(
        responsible=list(phase.leaders),
        accountable=phase.accountable,
        consulted=list(phase.consulted),
        informed=list(phase.informed),
        verifier=phase.verifier,
    )


# --------------------------------------------------------------------------- #
# Hilo Dorado (Golden Thread) traceability
# --------------------------------------------------------------------------- #

# Ordered stages of the traceability chain. Each generated element carries a
# unique id prefixed by the stage code so lineage is auditable end to end.
GOLDEN_THREAD_STAGES = [
    ("DRV", "Driver", "1"),            # Fase 1
    ("CAP", "Capability", "1"),        # Fase 1
    ("BMK", "Benchmark", "2"),         # Fase 2
    ("GAP", "Pain/Gap", "3"),          # Fase 3
    ("REL", "Reliever", "3"),          # Fase 3
    ("ABB", "ABB/Context", "3.5"),     # Fase 3.5
    ("SBB", "SBB/Spec/Story", "4"),    # Fase 4
    ("WAV", "Size/Wave", "5"),         # Fase 5
    ("ROI", "ROI/Outcome", "6"),       # Fase 6
]


@dataclass
class ThreadLink:
    """A single element in the Hilo Dorado with lineage to its parent."""

    id: str
    stage: str      # stage code (DRV, CAP, ...)
    phase: str      # phase id where it is produced
    label: str      # human description
    parent: Optional[str] = None  # id of the upstream element


class GoldenThread:
    """Links trace IDs across phases to keep the Hilo Dorado auditable."""

    def __init__(self):
        self.links: List[ThreadLink] = []
        self._counters: Dict[str, int] = {}

    @staticmethod
    def stage_for(code: str) -> Optional[tuple]:
        for stage in GOLDEN_THREAD_STAGES:
            if stage[0] == code:
                return stage
        return None

    def next_id(self, stage_code: str) -> str:
        n = self._counters.get(stage_code, 0) + 1
        self._counters[stage_code] = n
        return f"{stage_code}-{n:03d}"

    def add(self, stage_code: str, label: str, parent: Optional[str] = None) -> ThreadLink:
        info = self.stage_for(stage_code)
        phase = info[2] if info else "?"
        link = ThreadLink(
            id=self.next_id(stage_code),
            stage=stage_code,
            phase=phase,
            label=label,
            parent=parent,
        )
        self.links.append(link)
        return link

    def chain(self, link_id: str) -> List[ThreadLink]:
        """Return the lineage from the given element back to its root driver."""
        index = {l.id: l for l in self.links}
        out: List[ThreadLink] = []
        cur = index.get(link_id)
        seen = set()
        while cur and cur.id not in seen:
            seen.add(cur.id)
            out.append(cur)
            cur = index.get(cur.parent) if cur.parent else None
        return list(reversed(out))

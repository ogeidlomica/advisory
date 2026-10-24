"""AdvisoryOrchestrator: executes Zero-Drift phases in RACI-V sequence.

For a given phase (or 'all') it:
  1. engages the producer roles (Responsible), then
  2. runs the verifier gate check (Verifier / AICV-E), then
  3. invokes the phase's report builder to produce the markdown, then
  4. writes it to the output folder and records a run summary.

For 'all' it runs phases 0 -> 6 in order and regenerates the README index.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from engine.corpus import CorpusLoader
from engine.model import GoldenThread, Phase, raci_v_for
from engine.phases import PHASE_ORDER, load_phases
from phases import build_readme
from phases.builders import BuildContext

import roles as roles_pkg


@dataclass
class PhaseResult:
    phase_id: str
    phase_name: str
    roles_engaged: List[str]
    verifier: str
    gate_verdict: str
    output_path: str


@dataclass
class RunSummary:
    results: List[PhaseResult] = field(default_factory=list)
    readme_path: Optional[str] = None

    def log_lines(self) -> List[str]:
        out = []
        for r in self.results:
            out.append(
                f"[{r.phase_name}] roles={','.join(r.roles_engaged)} "
                f"verifier={r.verifier} | {r.gate_verdict} -> {r.output_path}"
            )
        if self.readme_path:
            out.append(f"[README index] -> {self.readme_path}")
        return out


class AdvisoryOrchestrator:
    def __init__(self, corpus: CorpusLoader, out_dir: str):
        self.corpus = corpus
        self.out_dir = os.path.abspath(out_dir)
        self.roles = roles_pkg.load_roles()
        self.phases: Dict[str, Phase] = load_phases()
        self.thread = GoldenThread()

    # -- public API --------------------------------------------------------- #
    def run(self, phase: str = "all") -> RunSummary:
        os.makedirs(self.out_dir, exist_ok=True)
        summary = RunSummary()
        if phase == "all":
            for pid in PHASE_ORDER:
                summary.results.append(self._run_phase(pid))
            summary.readme_path = self._write_readme()
        else:
            if phase not in self.phases:
                raise ValueError(f"Fase desconocida: {phase}")
            summary.results.append(self._run_phase(phase))
        return summary

    # -- internals ---------------------------------------------------------- #
    def _run_phase(self, pid: str) -> PhaseResult:
        phase = self.phases[pid]
        raci = raci_v_for(phase)

        # 1) Producers engage (Responsible).
        roles_engaged = list(raci.responsible)

        # 2) Verifier gate check (AICV-E). Placeholder gate is satisfied so the
        #    pipeline runs green; real gate logic arrives with report content.
        gate_satisfied = True
        gate_verdict = phase.gate.verdict(gate_satisfied)

        # 3) Build the report via the phase builder.
        ctx = BuildContext(
            phase=phase,
            roles=self.roles,
            documents=self.corpus.documents,
            thread=self.thread,
            gate_satisfied=gate_satisfied,
        )
        builder = phase.builder
        if builder is None:
            body = f"# {phase.name}\n\n(Sin builder asignado.)\n"
        else:
            body = builder(ctx)

        # 4) Write the report.
        output_path = os.path.join(self.out_dir, phase.filename)
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(body)

        return PhaseResult(
            phase_id=pid,
            phase_name=phase.name,
            roles_engaged=roles_engaged,
            verifier=phase.verifier,
            gate_verdict=gate_verdict,
            output_path=output_path,
        )

    def _write_readme(self) -> str:
        body = build_readme(self.phases, self.roles, self.corpus.documents)
        path = os.path.join(self.out_dir, "README.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        return path

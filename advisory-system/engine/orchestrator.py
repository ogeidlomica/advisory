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
from engine.gating import evaluate_gate
from engine.knowledge import KnowledgeBase
from engine.model import GoldenThread, Phase, raci_v_for
from engine.phases import CATALOG_FILENAME, PHASE_ORDER, load_phases
from phases import build_readme
from phases import catalog as catalog_mod
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
    kb_dir: Optional[str] = None
    kb_file_count: int = 0
    catalog_path: Optional[str] = None

    def log_lines(self) -> List[str]:
        out = []
        if self.kb_dir:
            out.append(
                f"[Base de Conocimiento] {self.kb_file_count} archivos -> {self.kb_dir}"
            )
        for r in self.results:
            out.append(
                f"[{r.phase_name}] roles={','.join(r.roles_engaged)} "
                f"verifier={r.verifier} | {r.gate_verdict} -> {r.output_path}"
            )
        if self.catalog_path:
            out.append(f"[Catalogo HU/Gherkin] -> {self.catalog_path}")
        if self.readme_path:
            out.append(f"[README index] -> {self.readme_path}")
        return out


class AdvisoryOrchestrator:
    def __init__(self, corpus: CorpusLoader, out_dir: str,
                 kb_dir: Optional[str] = None):
        self.corpus = corpus
        self.out_dir = os.path.abspath(out_dir)
        # The knowledge base lives at the repository root (sibling of
        # advisory-system/ and of the reports folder). Default: parent of
        # out_dir, i.e. the repo root, under knowledge-base/.
        if kb_dir is None:
            kb_dir = os.path.join(os.path.dirname(self.out_dir), "knowledge-base")
        self.kb_dir = os.path.abspath(kb_dir)
        self.roles = roles_pkg.load_roles()
        self.phases: Dict[str, Phase] = load_phases()
        self.thread = GoldenThread()
        # Full 18-doc ingestion -> deterministic knowledge base. Built once so
        # every phase builder sees the same enriched documents.
        self.knowledge_base = KnowledgeBase.from_documents(self.corpus.documents)
        self.kb_paths: List[str] = []

    # -- public API --------------------------------------------------------- #
    def run(self, phase: str = "all") -> RunSummary:
        os.makedirs(self.out_dir, exist_ok=True)
        summary = RunSummary()
        if phase == "all":
            # Generate the knowledge base + coverage checklist before the
            # phase reports so downstream builders consume a populated KB.
            self.kb_paths = self.knowledge_base.write(self.kb_dir)
            summary.kb_dir = self.kb_dir
            summary.kb_file_count = len(self.kb_paths)
            for pid in PHASE_ORDER:
                summary.results.append(self._run_phase(pid))
            # Auxiliary exhaustive HU/Gherkin catalog (FEAT-003), complement of
            # Phase 4, written deterministically from phases/modules.py.
            summary.catalog_path = self._write_catalog()
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

        # 2) Build the report via the phase builder. The builder renders its
        #    verdict line from ctx.gate_satisfied, which does not exist until
        #    the body does, so we build optimistically (assumed GO) and then
        #    evaluate the real gate from the produced body in step 3.
        ctx = BuildContext(
            phase=phase,
            roles=self.roles,
            documents=self.corpus.documents,
            thread=self.thread,
            gate_satisfied=True,
            knowledge_base=self.knowledge_base,
        )
        builder = phase.builder
        if builder is None:
            body = f"# {phase.name}\n\n(Sin builder asignado.)\n"
        else:
            body = builder(ctx)

        # 3) Verifier gate check (AICV-E). The gate is COMPUTED from the body:
        #    structural contract (mermaid, table, epistemic tag, verdict
        #    scaffold) plus phase-specific Hilo Dorado traceability. If the
        #    computed verdict differs from the optimistic one the builder
        #    printed, patch the body so the printed 'Veredicto QG-x' tells the
        #    truth.
        gate_satisfied, gate_reasons = evaluate_gate(phase, body)
        gate_verdict = phase.gate.verdict(gate_satisfied, gate_reasons)
        if not gate_satisfied:
            body = self._patch_verdict(body, phase, gate_verdict)

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

    @staticmethod
    def _patch_verdict(body: str, phase: Phase, gate_verdict: str) -> str:
        """Rewrite the printed 'Veredicto QG-x' line to the computed verdict.

        Builders render the verdict optimistically (GO) because they run before
        the gate is evaluated. When the gate computes NO-GO we rewrite that one
        line so the on-disk report matches the real result, without disturbing
        the rest of the structural contract.
        """
        marker = f"**Veredicto {phase.gate.id}:**"
        out_lines = []
        patched = False
        for line in body.splitlines():
            if not patched and marker in line:
                prefix = line[: line.index(marker) + len(marker)]
                out_lines.append(f"{prefix} {gate_verdict}")
                patched = True
            else:
                out_lines.append(line)
        patched_body = "\n".join(out_lines)
        if body.endswith("\n") and not patched_body.endswith("\n"):
            patched_body += "\n"
        return patched_body

    def _write_catalog(self) -> str:
        body = catalog_mod.build(self.knowledge_base)
        path = os.path.join(self.out_dir, CATALOG_FILENAME)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        return path

    def _write_readme(self) -> str:
        body = build_readme(self.phases, self.roles, self.corpus.documents)
        path = os.path.join(self.out_dir, "README.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        return path

"""Placeholder report builders (FEAT-001).

Each builder receives a ``BuildContext`` and returns the full markdown body for
its phase. The placeholders are deliberately minimal but still satisfy the
structural contract every phase report must honour:

  * at least one ```mermaid``` diagram block,
  * at least one markdown table,
  * a Go/No-Go gate verdict line at the end,
  * the AICV-E / RACI-V framing so later features can enrich in place.

FEAT-002/003/004 will replace individual entries in ``BUILDERS`` with
corpus-grounded content without changing the engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

from engine.model import Phase, raci_v_for


@dataclass
class BuildContext:
    """Everything a phase builder needs to render its report."""

    phase: Phase
    roles: Dict[str, object]       # code -> Role
    documents: List[object]        # Document records from the corpus
    thread: object                 # GoldenThread instance
    gate_satisfied: bool = True


# --------------------------------------------------------------------------- #
# Shared rendering helpers
# --------------------------------------------------------------------------- #

def _raci_table(ctx: BuildContext) -> str:
    raci = raci_v_for(ctx.phase)
    lines = ["| Dimension RACI-V | Roles |", "| --- | --- |"]
    for dim, val in raci.as_rows():
        lines.append(f"| {dim} | {val} |")
    return "\n".join(lines)


def _deliverables_table(ctx: BuildContext) -> str:
    lines = ["| Codigo | Entregable |", "| --- | --- |"]
    for code in ctx.phase.deliverables:
        lines.append(f"| {code} | Entregable {code} (contenido en features posteriores) |")
    return "\n".join(lines)


def _gate_block(ctx: BuildContext) -> str:
    gate = ctx.phase.gate
    rows = ["| Criterio de salida |", "| --- |"]
    for c in gate.criteria:
        rows.append(f"| {c} |")
    verdict = gate.verdict(ctx.gate_satisfied)
    return (
        f"## Stage-Gate {gate.id} - {gate.name}\n\n"
        + "\n".join(rows)
        + f"\n\n**No-Go si:** {gate.nogo_condition}\n\n"
        + f"> **Veredicto {gate.id}:** {verdict}\n"
    )


def _roles_line(ctx: BuildContext) -> str:
    names = []
    for code in ctx.phase.leaders:
        role = ctx.roles.get(code)
        names.append(f"{code} ({role.name})" if role else code)
    return ", ".join(names)


def _mermaid(ctx: BuildContext) -> str:
    leaders = " & ".join(ctx.phase.leaders)
    return (
        "```mermaid\n"
        "flowchart LR\n"
        f'    P["{ctx.phase.name}"] --> R["Productores: {leaders}"]\n'
        f'    R --> V["Verificador: {ctx.phase.verifier} (AICV-E)"]\n'
        f'    V --> G["{ctx.phase.gate.id}: {ctx.phase.gate.name}"]\n'
        "```\n"
    )


def _base_report(ctx: BuildContext, intro: str) -> str:
    phase = ctx.phase
    parts = [
        f"# {phase.name}",
        "",
        "> *(Contenido placeholder generado por FEAT-001; el contenido "
        "fundamentado en el corpus llega en features posteriores.)*",
        "",
        intro,
        "",
        "## Liderazgo y RACI-V",
        "",
        f"Roles productores: {_roles_line(ctx)}.",
        f"Verificador (V): **{phase.verifier}**. Accountable (A): **{phase.accountable}**.",
        "",
        _raci_table(ctx),
        "",
        "## Diagrama de fase",
        "",
        _mermaid(ctx),
        "",
        "## Entregables",
        "",
        _deliverables_table(ctx),
        "",
        _gate_block(ctx),
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# Per-phase placeholder builders
# --------------------------------------------------------------------------- #

def build_phase0(ctx: BuildContext) -> str:
    # FEAT-002: corpus-grounded content lives in phases/phase0.py.
    from phases import phase0
    return phase0.build(ctx)


def build_phase1(ctx: BuildContext) -> str:
    # FEAT-002: corpus-grounded content lives in phases/phase1.py.
    from phases import phase1
    return phase1.build(ctx)


def build_phase2(ctx: BuildContext) -> str:
    # FEAT-002: corpus-grounded content lives in phases/phase2.py.
    from phases import phase2
    return phase2.build(ctx)


def build_phase3(ctx: BuildContext) -> str:
    # FEAT-003: corpus-grounded content lives in phases/phase3.py.
    from phases import phase3
    return phase3.build(ctx)


def build_phase4(ctx: BuildContext) -> str:
    # FEAT-003: corpus-grounded content lives in phases/phase4.py.
    from phases import phase4
    return phase4.build(ctx)


def build_phase5(ctx: BuildContext) -> str:
    return _base_report(
        ctx,
        "Esta fase define el roadmap por olas, la estimacion de tamano, el RAID "
        "y el modelo operativo de habilitacion.",
    )


def build_phase6(ctx: BuildContext) -> str:
    return _base_report(
        ctx,
        "Esta fase cuantifica el caso de negocio: ROI y outcomes contra los "
        "indicadores del RFP, cerrando el Hilo Dorado.",
    )


BUILDERS: Dict[str, Callable[[BuildContext], str]] = {
    "0": build_phase0,
    "1": build_phase1,
    "2": build_phase2,
    "3": build_phase3,
    "4": build_phase4,
    "5": build_phase5,
    "6": build_phase6,
}


# --------------------------------------------------------------------------- #
# README index builder
# --------------------------------------------------------------------------- #

def build_readme(phases: Dict[str, Phase], roles: Dict[str, object], documents: List[object]) -> str:
    from engine.phases import PHASE_ORDER

    n_pdf = sum(1 for d in documents if d.kind == "pdf")
    n_png = sum(1 for d in documents if d.kind == "png")

    lines = [
        "# Advisory Credi10 2.0 - Framework Zero-Drift",
        "",
        "> *(Index placeholder generado por FEAT-001; se enriquece en features "
        "posteriores.)*",
        "",
        "Este directorio contiene los informes del advisory ejecutado con el "
        "framework **Zero-Drift** (Comite de Gobierno + 3 Celulas, 17 roles, "
        "7 fases con stage-gates QG-0..QG-6, RACI-V, AICV-E y Hilo Dorado).",
        "",
        "## Corpus de evidencia",
        "",
        f"- Documentos PDF: **{n_pdf}**",
        f"- Diagramas PNG (evidencia binaria): **{n_png}**",
        "",
        "## Informes por fase",
        "",
        "| Fase | Informe | Lider(es) | Verificador | Gate |",
        "| --- | --- | --- | --- | --- |",
    ]
    for pid in PHASE_ORDER:
        ph = phases[pid]
        lines.append(
            f"| {ph.name} | [{ph.filename}]({ph.filename}) | "
            f"{', '.join(ph.leaders)} | {ph.verifier} | {ph.gate.id} |"
        )
    lines += [
        "",
        "## Flujo de fases (Hilo Dorado)",
        "",
        "```mermaid",
        "flowchart LR",
        '    F0["Fase 0<br/>Higiene"] --> F1["Fase 1<br/>AS-IS"]',
        '    F1 --> F2["Fase 2<br/>Estado del Arte"]',
        '    F2 --> F3["Fase 3+3.5<br/>Gaps"]',
        '    F3 --> F4["Fase 4<br/>TO-BE"]',
        '    F4 --> F5["Fase 5<br/>Roadmap/RAID"]',
        '    F5 --> F6["Fase 6<br/>Caso de Negocio"]',
        "```",
        "",
    ]
    return "\n".join(lines) + "\n"

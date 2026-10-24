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
    knowledge_base: object = None  # engine.knowledge.KnowledgeBase (may be None)


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
    # FEAT-004: corpus-grounded content lives in phases/phase5.py.
    from phases import phase5
    return phase5.build(ctx)


def build_phase6(ctx: BuildContext) -> str:
    # FEAT-004: corpus-grounded content lives in phases/phase6.py.
    from phases import phase6
    return phase6.build(ctx)


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
    """Genera el indice (README.md) del directorio de informes del advisory."""
    from engine.phases import PHASE_ORDER
    import roles as roles_pkg

    n_pdf = sum(1 for d in documents if d.kind == "pdf")
    n_png = sum(1 for d in documents if d.kind == "png")

    committee = roles_pkg.committee()
    cells = roles_pkg.cells()

    def role_label(code: str) -> str:
        role = roles.get(code)
        return f"{code} ({role.name})" if role else code

    lines = [
        "# Advisory Credi10 2.0 - Framework Zero-Drift",
        "",
        "Este directorio contiene los **informes del advisory Credi10 2.0**, "
        "generados automaticamente por el motor `advisory-system/` a partir del "
        "corpus de evidencia (RFP, assessment WSO2/Studio F y diagramas de "
        "arquitectura). Cada informe corresponde a una fase del framework "
        "**Zero-Drift** y es 100% reproducible re-ejecutando el quickstart.",
        "",
        "> **Regenerar todos los informes:**",
        ">",
        "> ```bash",
        "> python3 advisory-system/quickstart.py --phase all",
        "> ```",
        "",
        "## El framework Zero-Drift",
        "",
        "Zero-Drift organiza el advisory como un **Comite de Gobierno** mas "
        "**3 Celulas** de trabajo, con **17 roles** declarativos, **7 fases** "
        "con stage-gates **QG-0..QG-6**, separacion productor/verificador "
        "(**RACI-V**), gobierno de calidad **AICV-E** (a cargo del AM) y un "
        "**Hilo Dorado** de trazabilidad que conecta cada driver del RFP con un "
        "outcome de negocio.",
        "",
        f"- **Comite de Gobierno:** {', '.join(role_label(c) for c in committee)}.",
    ]
    for cell_name, members in cells.items():
        lines.append(f"- **{cell_name}:** {', '.join(members)}.")
    lines += [
        f"- **Roles totales:** {len(roles)} (catalogo declarativo en "
        "`advisory-system/roles/roles.json`).",
        "",
        "## Corpus de evidencia",
        "",
        f"- Documentos PDF analizados: **{n_pdf}**",
        f"- Diagramas PNG (evidencia binaria transcrita): **{n_png}**",
        "",
        "## Informes por fase",
        "",
        "| Fase | Informe | Entregables | Lider(es) | Verificador | Gate |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for pid in PHASE_ORDER:
        ph = phases[pid]
        lines.append(
            f"| {ph.name} | [{ph.filename}]({ph.filename}) | "
            f"{', '.join(ph.deliverables)} | {', '.join(ph.leaders)} | "
            f"{ph.verifier} | {ph.gate.id} |"
        )
    from engine.phases import CATALOG_FILENAME
    lines += [
        "",
        "## Catalogo complementario",
        "",
        "Ademas de los 7 informes por fase, el motor genera un catalogo "
        "**exhaustivo de Historias de Usuario + BDD/Gherkin** que cubre TODO el "
        "universo de modulos de Credi10 (sin muestreo), complemento de la Fase 4:",
        "",
        f"- [`{CATALOG_FILENAME}`]({CATALOG_FILENAME}): HU + criterios Gherkin "
        "(happy path + casos borde) por modulo, desde la fuente unica de verdad "
        "`advisory-system/phases/modules.py` (reutilizada por la estimacion por "
        "modulo de la Fase 5).",
        "",
        "## Hilo Dorado (F1 -> F6)",
        "",
        "La trazabilidad end-to-end encadena: Driver (F1) -> Capability (F1) -> "
        "Benchmark (F2) -> Gap (F3) -> Reliever (F3) -> ABB (F3.5) -> SBB (F4) "
        "-> Ola/WAV (F5) -> ROI/Outcome (F6).",
        "",
        "```mermaid",
        "flowchart LR",
        '    DRV["DRV<br/>Drivers RFP (F1)"] --> CAP["CAP<br/>Capabilities (F1)"]',
        '    CAP --> BMK["BMK<br/>Benchmarks (F2)"]',
        '    BMK --> GAP["GAP<br/>Gaps (F3)"]',
        '    GAP --> REL["REL<br/>Relievers (F3)"]',
        '    REL --> ABB["ABB<br/>ABBs (F3.5)"]',
        '    ABB --> SBB["SBB<br/>SBBs (F4)"]',
        '    SBB --> WAV["WAV<br/>Olas (F5)"]',
        '    WAV --> ROI["ROI<br/>Outcomes (F6)"]',
        "```",
        "",
        "## Flujo de fases y stage-gates",
        "",
        "```mermaid",
        "flowchart LR",
        '    F0["Fase 0<br/>Higiene (QG-0)"] --> F1["Fase 1<br/>AS-IS (QG-1)"]',
        '    F1 --> F2["Fase 2<br/>Estado del Arte (QG-2)"]',
        '    F2 --> F3["Fase 3+3.5<br/>Gaps (QG-3)"]',
        '    F3 --> F4["Fase 4<br/>TO-BE (QG-4)"]',
        '    F4 --> F5["Fase 5<br/>Roadmap/RAID (QG-5)"]',
        '    F5 --> F6["Fase 6<br/>Caso de Negocio (QG-6)"]',
        "```",
        "",
        "## Como regenerar",
        "",
        "- Todo el pipeline (7 informes + este indice): "
        "`python3 advisory-system/quickstart.py --phase all`",
        "- Una sola fase (ej. Fase 3): "
        "`python3 advisory-system/quickstart.py --phase 3`",
        "- Opciones: `--corpus <ruta>` para otro corpus, `--out <ruta>` para "
        "otra carpeta de salida.",
        "",
        "La documentacion del motor (estrategia, arquitectura y pruebas) esta "
        "en [`advisory-system/README.md`](../advisory-system/README.md).",
        "",
    ]
    return "\n".join(lines) + "\n"

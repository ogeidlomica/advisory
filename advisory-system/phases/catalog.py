"""Catalogo EXHAUSTIVO de Historias de Usuario + BDD/Gherkin (FEAT-003).

Renderiza ``advisory-credi10-2.0/04b-catalogo-historias.md`` a partir de la
unica fuente de verdad declarativa ``phases/modules.py`` (``MODULES``). Cubre
TODO el universo de modulos Credi10 (sin muestreo): cada modulo aporta al menos
una historia de usuario con criterios de aceptacion BDD/Gherkin en espanol
(Dado/Cuando/Entonces) que cubren happy path Y al menos un caso borde /
excepcion (Exception Storming), cada historia con un id trazable del Hilo
Dorado.

Es un ARTEFACTO DE DOCUMENTACION (spec de diseno para la siguiente etapa),
generado por el motor del advisory; no es codigo de la solucion.

El archivo cumple el contrato estructural de los informes: >= 1 bloque
```mermaid```, >= 1 tabla markdown, >= 1 etiqueta epistemica y una linea
'Veredicto QG-4b'. La completitud (len(MODULES) == modulos renderizados) es
testeable.

Determinismo: todo el contenido deriva de datos estaticos ordenados; sin
aleatoriedad ni timestamps.
"""

from __future__ import annotations

from typing import List

from phases import modules as modules_mod
from phases.modules import GherkinScenario, Module, MODULES


CATALOG_FILENAME = "04b-catalogo-historias.md"


# --------------------------------------------------------------------------- #
# Render helpers
# --------------------------------------------------------------------------- #

def _coverage_overview() -> str:
    rows = [
        "| Metrica de cobertura | Valor |",
        "| --- | ---: |",
        f"| Modulos declarados (fuente unica `phases/modules.py`) | "
        f"{modules_mod.module_count()} |",
        f"| Historias de usuario (HU) | {modules_mod.story_count()} |",
        f"| Escenarios Gherkin (happy + borde) | "
        f"{modules_mod.story_count() * 2} |",
    ]
    return "\n".join(rows)


def _modules_index_table() -> str:
    rows = [
        "| Modulo | Nombre | Bounded Context | ABBs | Historias | Fuente (KB) |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for m in MODULES:
        hu = ", ".join(s.id for s in m.stories)
        rows.append(
            f"| {m.id} | {m.name} | {m.bounded_context} | "
            f"{', '.join(m.abbs)} | {hu} | {m.source} |"
        )
    return "\n".join(rows)


def _coverage_mermaid() -> str:
    # Mapa de cobertura: cada bounded context agrupa sus modulos. Flowchart
    # como fallback seguro y determinista.
    by_ctx: dict = {}
    for m in MODULES:
        by_ctx.setdefault(m.bounded_context, []).append(m)
    lines = ["```mermaid", "flowchart TB"]
    for ci, (ctx_name, mods) in enumerate(sorted(by_ctx.items()), start=1):
        safe_ctx = ctx_name.replace(" ", "_").replace("/", "_").replace("-", "_")
        lines.append(f'    subgraph C{ci}["{ctx_name}"]')
        for m in mods:
            lines.append(f'        {m.id.replace("-", "_")}["{m.id} {m.name}"]')
        lines.append("    end")
    lines.append("```")
    return "\n".join(lines)


def _gherkin_scenario(scn: GherkinScenario) -> List[str]:
    out: List[str] = [f"  Escenario: {scn.titulo}"]
    for i, step in enumerate(scn.dado):
        kw = "Dado" if i == 0 else "Y"
        out.append(f"    {kw} {step}")
    for i, step in enumerate(scn.cuando):
        kw = "Cuando" if i == 0 else "Y"
        out.append(f"    {kw} {step}")
    for i, step in enumerate(scn.entonces):
        kw = "Entonces" if i == 0 else "Y"
        out.append(f"    {kw} {step}")
    return out


def _module_section(m: Module) -> List[str]:
    parts: List[str] = [
        f"### {m.id} - {m.name}",
        "",
        f"- **Bounded Context:** {m.bounded_context}",
        f"- **Componentes:** {m.components}",
        f"- **ABBs (Hilo Dorado):** {', '.join(m.abbs)}",
        f"- **Fuente (Base de Conocimiento):** `{m.source}`",
        "",
    ]
    for s in m.stories:
        parts += [
            f"**{s.id} - Historia de usuario**",
            "",
            f"> Como **{s.rol}** quiero **{s.quiero}** para **{s.para}**.",
            "",
            "```gherkin",
            "# language: es",
            f"Caracteristica: {m.name} ({s.id})",
            "",
        ]
        parts.extend(_gherkin_scenario(s.happy))
        parts.append("")
        parts.extend(_gherkin_scenario(s.edge))
        parts += ["```", ""]
    return parts


# --------------------------------------------------------------------------- #
# Public builder
# --------------------------------------------------------------------------- #

def build(knowledge_base=None) -> str:
    """Render the exhaustive HU/Gherkin catalog markdown (deterministic).

    ``knowledge_base`` is accepted for signature symmetry with phase builders
    and to cite coverage; it may be ``None`` (the catalog degrades gracefully).
    """
    kb_note = ""
    if knowledge_base is not None:
        try:
            kb_note = (
                f" La ingesta de la Base de Conocimiento cubre "
                f"**{knowledge_base.total}** documentos (sin muestreo), lo que "
                "sustenta la trazabilidad de cada historia a su documento fuente."
            )
        except Exception:
            kb_note = ""

    parts: List[str] = [
        "# Catalogo Exhaustivo de Historias de Usuario y Specs BDD/Gherkin",
        "",
        "> Complemento de la **Fase 4 (Diseno TO-BE)** del framework "
        "**Zero-Drift**. Cataloga, **sin muestreo**, TODO el universo de modulos "
        "de Credi10 2.0. Cada modulo aporta al menos una **Historia de Usuario** "
        "con criterios de aceptacion **BDD/Gherkin** en espanol "
        "(Dado/Cuando/Entonces) que cubren el **happy path** y al menos un "
        "**caso borde/excepcion** (Exception Storming), cada una con un id "
        "trazable del **Hilo Dorado**. Es documentacion (spec para la siguiente "
        "etapa), generada por el motor del advisory."
        + kb_note,
        "",
        "> **Fuente unica de verdad:** el listado de modulos es el dato "
        "declarativo `advisory-system/phases/modules.py` (`MODULES`), reutilizado "
        "por este catalogo y por la **estimacion por modulo** de la Fase 5. La "
        "completitud es testeable: numero de modulos renderizados == "
        "`len(MODULES)`.",
        "",
        "> Las viabilidades/umbrales que no estan explicitos en el corpus se "
        "marcan [DOC-ASSUMPTION]; cuando no hay base documental se marca "
        "[EPISTEMIC-VOID]. Nunca se fabrica evidencia [VERIFIED-FACT].",
        "",
        "## Cobertura del catalogo",
        "",
        _coverage_overview(),
        "",
        "## Mapa de cobertura por Bounded Context",
        "",
        _coverage_mermaid(),
        "",
        "## Indice de modulos del universo Credi10",
        "",
        _modules_index_table(),
        "",
        "## Historias de usuario + Gherkin por modulo",
        "",
    ]

    for m in MODULES:
        parts.extend(_module_section(m))

    # Cierre + veredicto estructural (QG-4b): el catalogo esta completo si cada
    # modulo declarado tiene al menos una historia con happy + borde.
    complete = all(len(m.stories) >= 1 for m in MODULES)
    missing_edge = [
        s.id for m in MODULES for s in m.stories
        if s.happy is None or s.edge is None
    ]
    satisfied = complete and not missing_edge
    verdict = "GO" if satisfied else "NO-GO"
    detail = (
        f"cobertura {modules_mod.module_count()}/"
        f"{modules_mod.module_count()} modulos con happy path + caso borde"
        if satisfied else
        "faltan historias o escenarios borde: " + ", ".join(missing_edge)
    )

    parts += [
        "## Veredicto de cobertura",
        "",
        "| Criterio de cobertura del catalogo | Estado |",
        "| --- | --- |",
        "| Todos los modulos declarados tienen >= 1 historia | "
        + ("Satisfecho" if complete else "No satisfecho") + " |",
        "| Cada historia cubre happy path + caso borde (Exception Storming) | "
        + ("Satisfecho" if not missing_edge else "No satisfecho") + " |",
        "| El listado de modulos es la unica fuente de verdad (phases/modules.py) | "
        "Satisfecho |",
        "",
        f"> **Veredicto QG-4b:** {verdict} - {detail}.",
        "",
    ]
    return "\n".join(parts) + "\n"

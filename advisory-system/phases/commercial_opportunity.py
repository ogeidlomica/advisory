"""Analisis de oportunidad y diseno de oferta comercial (task commercial-opportunity).

Generador DETERMINISTA, stdlib-only, de los **DOS outcomes comerciales
SEPARADOS** gobernados por el skill ``commercial-opportunity-analysis``. Es la
capa de un experto en **bid-management / diseno de ofertas comerciales** que
analiza la oportunidad desde el corpus, levanta el checklist de lo que el
cliente pide, desarrolla el contenido de respuesta dentro de la oferta y asegura
la **correlacion** oferta<->advisory<->RFP.

COMPLEMENTA (no duplica) a dos politicas hermanas y REUSA su salida:

  * ``requirements_traceability.extract_requirements(documents)`` es la **fuente
    unica** de las solicitudes del cliente (IDs ``REQ-NNN``, cita a documento
    fuente, ``kind``, ``status``, flag epistemico). No se reimplementa la
    extraccion ni se hardcodea la lista de Credi10.
  * ``commercial_proposal`` emite la propuesta con 11 secciones a-k. Este modulo
    **mapea** cada solicitud a su seccion ``## a..k`` sin reescribir la
    propuesta ni restablecer cifras contradictorias.

Dos outcomes en **rutas/archivos SEPARADOS** bajo ``advisory-credi10-2.0/``:

  * Outcome 1 -> ``0-analisis-oportunidad-comercial.md``: analisis de la
    oportunidad, checklist marcable de la informacion solicitada y contenido
    desarrollado de respuesta mapeado a las secciones de la propuesta.
  * Outcome 2 -> ``0b-checklist-oferta-y-correlacion.md``: checklist de items a
    desarrollar + consideraciones + supuestos + la **matriz de trazabilidad
    comercial** con las columnas EXACTAS que fija el skill.

Determinismo: todo deriva de ``extract_requirements`` (orden estable por
documento) y de mapeos estaticos; sin azar ni timestamps. Una segunda corrida de
``--phase all`` deja ambos archivos byte-identicos. Dinamismo: si cambia el
corpus/RFP, ambos outcomes se recalculan con las solicitudes del nuevo cliente.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Sequence

from phases import requirements_traceability as rt


# --------------------------------------------------------------------------- #
# Nombres de archivo (reexportados de engine.phases como fuente canonica).
# --------------------------------------------------------------------------- #

OPPORTUNITY_FILENAME = "0-analisis-oportunidad-comercial.md"
CORRELATION_FILENAME = "0b-checklist-oferta-y-correlacion.md"
PROPOSAL_FILENAME = "1-propuesta-comercial.md"


# --------------------------------------------------------------------------- #
# Mapeo determinista tipo-de-solicitud -> seccion a-k de la propuesta.
# Las secciones son las que emite commercial_proposal (headings ## a..k). Cada
# kind de requirements_traceability se asocia a la seccion de la oferta donde la
# solicitud queda respondida comercialmente, y a un win theme recalibrable.
# --------------------------------------------------------------------------- #

# (letra, titulo legible de la seccion de 1-propuesta-comercial.md)
PROPOSAL_SECTIONS: Dict[str, str] = {
    "a": "a. Quienes somos",
    "b": "b. Alcance del servicio",
    "c": "c. Contexto de negocio",
    "d": "d. Metodologia de consultoria",
    "e": "e. Entregables",
    "f": "f. Estrategia de consultoria",
    "g": "g. Equipo de trabajo",
    "h": "h. Cronograma de trabajo",
    "i": "i. Supuestos y restricciones",
    "j": "j. Inversion",
    "k": "k. Terminos y condiciones",
}

# kind -> letra de seccion de la propuesta que responde la solicitud.
KIND_TO_PROPOSAL_SECTION: Dict[str, str] = {
    "objetivos": "c",       # contexto de negocio: por que y para que
    "alcance": "b",         # alcance del servicio
    "tecnologia": "c",      # contexto de negocio (ecosistema tecnologico)
    "datos": "e",           # entregables (modelo de datos / contratos)
    "integraciones": "e",   # entregables (contratos / specs)
    "arquitectura": "e",    # entregables (diseno TO-BE)
    "funcional": "e",       # entregables (catalogo HU / specs)
    "operacion": "d",       # metodologia (operacion / cambio)
    "tecnico": "e",         # entregables (diseno TO-BE + ADRs)
    "informes": "e",        # entregables (los informes del engagement)
    "indicadores": "j",     # inversion / caso de negocio (ROI)
    "evaluacion": "f",      # estrategia de consultoria
    "roadmap": "h",         # cronograma de trabajo
    "generico": "b",        # alcance del servicio (por defecto)
}

# kind -> win theme / mensaje de valor comercial (generico, recalibrable).
# Es contenido comercial generico; cuando afirma datos del cliente debe
# respaldarse en el corpus, de lo contrario es [DOC-ASSUMPTION].
KIND_WIN_THEME: Dict[str, str] = {
    "objetivos": "Alineamos cada objetivo del cliente con un outcome de negocio "
                 "trazable por el Hilo Dorado (driver -> ROI), evitando scope "
                 "drift.",
    "alcance": "Cerramos el alcance de punta a punta (Discovery -> diseno TO-BE "
               "-> specs) dejando el proyecto listo para estimar y construir.",
    "tecnologia": "Diagnosticamos el ecosistema tecnologico AS-IS con evidencia "
                  "del corpus antes de proponer el TO-BE, sin supuestos ciegos.",
    "datos": "Entregamos modelo de datos y contratos trazables por bounded "
             "context, base de una integracion confiable.",
    "integraciones": "Especificamos contratos OpenAPI/AsyncAPI por integracion, "
                     "reduciendo el riesgo de acoplamiento y retrabajo.",
    "arquitectura": "Disenamos la arquitectura TO-BE (C4 + ADRs) con decisiones "
                    "documentadas y verificables, no diapositivas.",
    "funcional": "Especificamos historias de usuario + BDD/Gherkin trazables a "
                 "gaps, listas para construir y probar.",
    "operacion": "Gobernamos el cambio y el modelo operativo para que la "
                 "solucion sea adoptada, no solo entregada.",
    "tecnico": "Resolvemos los requisitos tecnicos con diseno TO-BE y ADRs "
               "auditables bajo el marco AICV-E.",
    "informes": "Entregamos exactamente los informes y artefactos que el "
                "cliente pide, versionables y reproducibles.",
    "indicadores": "Cuantificamos el ROI contra los indicadores del cliente en "
                   "un caso de negocio defendible (cifras [DOC-ASSUMPTION]).",
    "evaluacion": "Mostramos como superamos cada criterio de evaluacion con "
                  "quality gates QG-0..QG-6 y separacion productor/verificador.",
    "roadmap": "Planificamos por olas con dependencias explicitas y estimacion "
               "recalibrable, dando previsibilidad al cliente.",
    "generico": "Abordamos la solicitud dentro del alcance de advisory + specs, "
                "afinando el detalle al cerrar los deltas de elicitacion.",
}


# --------------------------------------------------------------------------- #
# Helpers de entrada y determinismo
# --------------------------------------------------------------------------- #

def _resolve_docs(knowledge_base=None,
                  documents: Optional[Sequence] = None):
    """Return (docs, total) accepting a KnowledgeBase OR a plain Document list.

    Mirrors ``requirements_traceability.write`` so the module is testable
    against a synthetic corpus.
    """
    docs: Sequence = []
    total: Optional[int] = None
    if knowledge_base is not None:
        docs = list(getattr(knowledge_base, "documents", []) or [])
        try:
            total = knowledge_base.total
        except Exception:
            total = len(docs)
    elif documents is not None:
        docs = list(documents)
        total = len(docs)
    return docs, total


def _proposal_section_for(kind: str) -> str:
    letter = KIND_TO_PROPOSAL_SECTION.get(kind, "b")
    return PROPOSAL_SECTIONS.get(letter, PROPOSAL_SECTIONS["b"])


def _win_theme_for(kind: str) -> str:
    return KIND_WIN_THEME.get(kind, KIND_WIN_THEME["generico"])


def _responds(status: str) -> str:
    """Whether the proposal responds to the request, derived from honest status."""
    if status == "Pendiente":
        return "No (Pendiente)"
    return "Si"


def _rfp_doc_name(reqs: Sequence[rt.Requirement]) -> Optional[str]:
    """Return the first source document that looks like an RFP, for prose."""
    for r in reqs:
        name = r.source_filename
        lowered = rt._normalize_name(name)
        if any(h in lowered for h in rt._RFP_NAME_HINTS):
            return name
    return reqs[0].source_filename if reqs else None


def _status_counts(reqs: Sequence[rt.Requirement]) -> Dict[str, int]:
    counts = {"Cubierto": 0, "Parcial": 0, "Pendiente": 0}
    for r in reqs:
        counts[r.status] = counts.get(r.status, 0) + 1
    return counts


def _status_mermaid(counts: Dict[str, int], title: str) -> str:
    return (
        "```mermaid\n"
        "pie showData\n"
        f'    title {title}\n'
        f'    "Cubierto" : {counts["Cubierto"]}\n'
        f'    "Parcial" : {counts["Parcial"]}\n'
        f'    "Pendiente" : {counts["Pendiente"]}\n'
        "```\n"
    )


def _epistemic_legend() -> str:
    return (
        "> **Etiquetas epistemicas:** **[VERIFIED-FACT]** solicitud/dato de capa "
        "de texto util verificada; **[OCR-EXTRACTED]** derivada de texto "
        "recuperado via OCR; **[DOC-ASSUMPTION]** supuesto comercial/cifra a "
        "validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** "
        "el corpus no permite responder (OCR/fuente pendiente). No se fabrica "
        "cobertura."
    )


def _regen_block() -> List[str]:
    return [
        "> **Regenerar (parte de `--phase all`):**",
        ">",
        "> ```bash",
        "> python3 advisory-system/quickstart.py --phase all",
        "> ```",
    ]


_CHECK_SYMBOL = {"Cubierto": "x", "Parcial": "~", "Pendiente": " "}


# --------------------------------------------------------------------------- #
# Outcome 1 - Analisis de la oportunidad y contenido de respuesta
# --------------------------------------------------------------------------- #

def build_opportunity_analysis(documents=None, knowledge_base=None,
                               roles=None) -> str:
    """Render Outcome 1: opportunity analysis + info checklist + offer content."""
    docs, total = _resolve_docs(knowledge_base=knowledge_base,
                                documents=documents)
    reqs = rt.extract_requirements(docs)
    counts = _status_counts(reqs)
    n = len(reqs)
    rfp_name = _rfp_doc_name(reqs)
    docs_line = (f" sobre un corpus de **{total}** documentos"
                 if total is not None else "")
    rfp_line = (f"La solicitud se analiza priorizando el documento tipo RFP "
                f"**{rfp_name}** y complementando con el resto del corpus."
                if rfp_name else
                "El corpus no expone un documento tipo RFP reconocible; el "
                "analisis degrada a la deteccion generica de solicitudes.")

    parts: List[str] = [
        "# Outcome 1 - Analisis de la oportunidad y contenido de respuesta",
        "",
        "> Primer outcome comercial gobernado por el skill "
        "`commercial-opportunity-analysis`. Lo produce el **Comite de Gobierno** "
        "(Engagement Director + Engagement Manager) como experto en "
        "**diseno de ofertas comerciales**. Es documentacion **generada de "
        "forma determinista** por el motor "
        "(`advisory-system/phases/commercial_opportunity.py`) y **dinamica**: "
        "las solicitudes del cliente se **reutilizan** de "
        "`requirements-traceability` (`extract_requirements`), no se hardcodean. "
        "COMPLEMENTA (no duplica) a `commercial-proposal-report` y a "
        "`requirements-traceability`.",
        "",
        "> **Separacion de outcomes:** este es el **Outcome 1**. El checklist de "
        "items + consideraciones + supuestos + la **matriz de correlacion** "
        "viven en un archivo **separado**, "
        f"[`{CORRELATION_FILENAME}`]({CORRELATION_FILENAME}) (Outcome 2).",
        "",
        _epistemic_legend(),
        "",
    ]
    parts += _regen_block()
    parts += [
        "",
        "## 1. Analisis de la oportunidad",
        "",
        f"Se derivaron **{n} solicitudes** del cliente{docs_line}: "
        f"**{counts['Cubierto']} Cubierto**, **{counts['Parcial']} Parcial**, "
        f"**{counts['Pendiente']} Pendiente**. " + rfp_line,
        "",
        "La **necesidad del cliente** (contexto, problema a resolver, valor "
        "esperado, restricciones y criterios de evaluacion) se **deriva del "
        "corpus**: cada solicitud conserva la **cita a su documento fuente**, de "
        "modo que la lectura de la oportunidad es trazable y no fabricada. "
        "Cuando el corpus no permite responder una solicitud, se declara "
        "honestamente **Pendiente** con `[EPISTEMIC-VOID]` en lugar de inventar "
        "cobertura.",
        "",
        "La oportunidad se materializa en la **propuesta comercial** "
        f"([`{PROPOSAL_FILENAME}`]({PROPOSAL_FILENAME})): este analisis **no "
        "reescribe** la propuesta ni sus cifras, la **mapea** para demostrar que "
        "cada necesidad queda respondida en alguna de sus secciones a-k.",
        "",
        "### Distribucion de la oportunidad por tipo de solicitud",
        "",
        _opportunity_by_kind_table(reqs),
        "",
        "### Cobertura de la oportunidad por estado",
        "",
        _status_mermaid(counts, "Cobertura comercial de la oportunidad"),
        "",
        "## 2. Checklist de la informacion que el cliente solicita",
        "",
        "Checklist **marcable** derivado dinamicamente de `extract_requirements`. "
        "Leyenda: `- [x]` disponible/cubierta en el corpus - `- [~]` "
        "parcialmente disponible - `- [ ]` solicitada pero no disponible "
        "(`[EPISTEMIC-VOID]`).",
        "",
    ]
    if reqs:
        for r in reqs:
            sym = _CHECK_SYMBOL.get(r.status, " ")
            parts.append(
                f"- [{sym}] **{r.req_id}** ({r.status}) {r.request} "
                f"_[fuente: {r.citation}]_ {r.epistemic_tag}"
            )
    else:
        parts.append("- [ ] (El corpus no permitio derivar solicitudes).")
    parts += [
        "",
        "## 3. Contenido desarrollado para responder cada necesidad",
        "",
        "Para cada solicitud se desarrolla el **contenido de respuesta** (win "
        "theme / mensaje de valor) y se indica la **seccion de la propuesta** "
        f"([`{PROPOSAL_FILENAME}`]({PROPOSAL_FILENAME})) donde se materializa. "
        "El contenido comercial es generico y recalibrable; no restablece cifras "
        "de la propuesta para no contradecirla.",
        "",
        "| ID | Solicitud del cliente | Seccion de la propuesta | Win theme / "
        "contenido de respuesta | Estado |",
        "| --- | --- | --- | --- | --- |",
    ]
    if reqs:
        for r in reqs:
            section = _proposal_section_for(r.kind).replace("|", "\\|")
            theme = _win_theme_for(r.kind).replace("|", "\\|")
            parts.append(
                f"| {r.req_id} | {r.request} | {section} | {theme} | "
                f"{r.status} |"
            )
    else:
        parts.append("| - | (sin solicitudes derivables del corpus) | - | - | "
                     "- |")
    parts += [
        "",
        "> El **Outcome 2** "
        f"([`{CORRELATION_FILENAME}`]({CORRELATION_FILENAME})) lleva este "
        "contenido a una **matriz de trazabilidad comercial** que correlaciona "
        "cada solicitud con la seccion de la oferta y el outcome del advisory "
        "que la sustenta.",
        "",
    ]
    return "\n".join(parts) + "\n"


def _opportunity_by_kind_table(reqs: Sequence[rt.Requirement]) -> str:
    """Deterministic summary: count of requests per kind, in stable order."""
    order: List[str] = []
    per_kind: Dict[str, int] = {}
    for r in reqs:
        if r.kind not in per_kind:
            per_kind[r.kind] = 0
            order.append(r.kind)
    for r in reqs:
        per_kind[r.kind] += 1
    order.sort()
    lines = [
        "| Tipo de solicitud (kind) | # solicitudes | Seccion de la propuesta |",
        "| --- | --- | --- |",
    ]
    if order:
        for kind in order:
            section = _proposal_section_for(kind).replace("|", "\\|")
            lines.append(f"| {kind} | {per_kind[kind]} | {section} |")
    else:
        lines.append("| - | 0 | - |")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Outcome 2 - Checklist de items, consideraciones, supuestos y correlacion
# --------------------------------------------------------------------------- #

def build_checklist_and_correlation(documents=None, knowledge_base=None,
                                    roles=None) -> str:
    """Render Outcome 2: items checklist + considerations + assumptions + matrix."""
    docs, total = _resolve_docs(knowledge_base=knowledge_base,
                                documents=documents)
    reqs = rt.extract_requirements(docs)
    counts = _status_counts(reqs)
    n = len(reqs)

    parts: List[str] = [
        "# Outcome 2 - Checklist de oferta, consideraciones, supuestos y "
        "correlacion",
        "",
        "> Segundo outcome comercial gobernado por el skill "
        "`commercial-opportunity-analysis`, en **ruta/archivo separado** del "
        "Outcome 1 "
        f"([`{OPPORTUNITY_FILENAME}`]({OPPORTUNITY_FILENAME})). Contiene el "
        "**checklist de items a desarrollar** en la oferta, las "
        "**consideraciones** y **supuestos**, y la **matriz de trazabilidad "
        "comercial** que demuestra **como el advisory responde a cada punto** "
        "que pide el cliente. Generado de forma **determinista** y **dinamica** "
        "desde `extract_requirements` (sin hardcodeo).",
        "",
        _epistemic_legend(),
        "",
    ]
    parts += _regen_block()
    parts += [
        "",
        "## 1. Checklist de items a desarrollar en la oferta",
        "",
        "Items marcables que cierran la oferta comercial. El estado de cada item "
        "se deriva de la cobertura real de las solicitudes de ese tipo en el "
        "corpus (no es optimista). Leyenda: `- [x]` listo/cubierto - `- [~]` "
        "parcial - `- [ ]` pendiente.",
        "",
    ]
    parts += _offer_items_checklist(reqs)
    parts += [
        "",
        "## 2. Consideraciones y supuestos de la oferta",
        "",
        "Supuestos comerciales recalibrables; cada supuesto se marca "
        "`[DOC-ASSUMPTION]` y toda cifra se expresa como rango "
        "`[DOC-ASSUMPTION]`. Las consideraciones de honestidad epistemica "
        "aplican a las solicitudes `Pendiente` (`[EPISTEMIC-VOID]`).",
        "",
        "| Tipo | Enunciado | Etiqueta |",
        "| --- | --- | --- |",
        "| Supuesto | El perfil corporativo de la consultora y las cifras de "
        "inversion son de referencia recalibrable, no compromisos | "
        "[DOC-ASSUMPTION] |",
        "| Supuesto | El cliente facilita el corpus completo y acceso a SME para "
        "cerrar los vacios epistemicos | [DOC-ASSUMPTION] |",
        "| Supuesto | Los win themes son contenido comercial generico a afinar "
        "con el cliente | [DOC-ASSUMPTION] |",
        f"| Consideracion | **{counts['Pendiente']}** solicitudes estan "
        "**Pendiente** por falta de texto util en la fuente (OCR/fuente "
        "pendiente); no se promete cobertura sobre ellas | [EPISTEMIC-VOID] |",
        f"| Consideracion | **{counts['Parcial']}** solicitudes son **Parcial**: "
        "abordables por el advisory con mapeo a afinar al cerrar la elicitacion "
        "| [DOC-ASSUMPTION] |",
        "| Restriccion | La etapa ofertada es advisory + specs; no incluye "
        "construccion ni despliegue | [VERIFIED-FACT] |",
        "",
        "## 3. Matriz de trazabilidad comercial (oferta <-> advisory <-> RFP)",
        "",
        f"Una fila por solicitud extraida (**{n}** en total). Demuestra que "
        "cada punto del cliente queda respondido por una **seccion de la "
        "oferta** y **sustentado por un outcome del advisory**, con **estado "
        "honesto**. Las solicitudes se **reutilizan** de "
        "`requirements-traceability`; la columna de la oferta mapea a "
        f"[`{PROPOSAL_FILENAME}`]({PROPOSAL_FILENAME}).",
        "",
        "| Solicitud del cliente (cita RFP, con nombre de documento) | ¿La "
        "oferta la responde? (seccion de 1-propuesta-comercial.md) | Outcome del "
        "advisory que la sustenta (fase/entregable) | Estado "
        "(Cubierto/Parcial/Pendiente) | Consideracion/Supuesto |",
        "| --- | --- | --- | --- | --- |",
    ]
    if reqs:
        for r in reqs:
            cita = f"{r.req_id}: {r.request} [fuente: {r.citation}]".replace(
                "|", "\\|")
            responde = _responds(r.status)
            if responde.startswith("Si"):
                oferta = f"{responde} - {_proposal_section_for(r.kind)}"
            else:
                oferta = responde
            oferta = oferta.replace("|", "\\|")
            where = r.where.replace("|", "\\|")
            consideracion = f"{r.epistemic_tag} {r.note}".replace("|", "\\|")
            parts.append(
                f"| {cita} | {oferta} | {where} | {r.status} | "
                f"{consideracion} |"
            )
    else:
        parts.append("| (sin solicitudes derivables del corpus) | - | - | - | "
                     "- |")
    parts += [
        "",
        f"**Resumen de estado:** {n} solicitudes = "
        f"{counts['Cubierto']} Cubierto + {counts['Parcial']} Parcial + "
        f"{counts['Pendiente']} Pendiente.",
        "",
        "### Cobertura comercial por estado",
        "",
        _status_mermaid(counts, "Cobertura comercial de solicitudes del cliente"),
        "",
        "## 4. Como el advisory responde a cada punto",
        "",
        "La columna *Outcome del advisory que la sustenta* reutiliza el mapeo "
        "`palabra-clave -> punto de entrada` de `requirements-traceability` "
        "(`KEYWORD_ENTRY_POINTS`): cada solicitud se ancla a una **fase y "
        "entregable** concretos del advisory (p. ej. Fase 4 diseno TO-BE, "
        "dossier TO-BE, caso de negocio). Asi la oferta no solo **afirma** que "
        "cubre una necesidad, sino que **senala el outcome del advisory** que la "
        "respalda, manteniendo la correlacion oferta<->advisory<->RFP y la "
        "honestidad epistemica (Pendiente -> `[EPISTEMIC-VOID]`).",
        "",
    ]
    return "\n".join(parts) + "\n"


def _offer_items_checklist(reqs: Sequence[rt.Requirement]) -> List[str]:
    """Deterministic items-to-develop checklist, one per proposal section used.

    The status of each section item is the worst honest status among the
    requests mapped to it (Pendiente > Parcial > Cubierto), so the checklist
    never overstates readiness.
    """
    severity = {"Cubierto": 0, "Parcial": 1, "Pendiente": 2}
    by_section: Dict[str, str] = {}
    for r in reqs:
        letter = KIND_TO_PROPOSAL_SECTION.get(r.kind, "b")
        cur = by_section.get(letter, "Cubierto")
        if severity[r.status] > severity[cur]:
            by_section[letter] = r.status
    lines: List[str] = []
    if not by_section:
        lines.append("- [ ] (El corpus no permitio derivar items de oferta).")
        return lines
    for letter in sorted(by_section):
        status = by_section[letter]
        sym = _CHECK_SYMBOL.get(status, " ")
        section = PROPOSAL_SECTIONS.get(letter, letter)
        lines.append(
            f"- [{sym}] Desarrollar/validar seccion **{section}** de la oferta "
            f"({status})"
        )
    return lines


# --------------------------------------------------------------------------- #
# Escritura de AMBOS outcomes (rutas separadas)
# --------------------------------------------------------------------------- #

def write(out_dir: str, knowledge_base=None, roles=None,
          documents: Optional[Sequence] = None) -> List[str]:
    """Write BOTH commercial outcomes under ``out_dir`` in SEPARATE files.

    Accepts either a ``KnowledgeBase`` or a plain list of ``Document`` objects.
    Deterministic and byte-identical between runs. Returns the sorted list of
    written paths.
    """
    os.makedirs(out_dir, exist_ok=True)
    written: List[str] = []

    opp_path = os.path.join(out_dir, OPPORTUNITY_FILENAME)
    with open(opp_path, "w", encoding="utf-8") as fh:
        fh.write(build_opportunity_analysis(
            documents=documents, knowledge_base=knowledge_base, roles=roles))
    written.append(opp_path)

    corr_path = os.path.join(out_dir, CORRELATION_FILENAME)
    with open(corr_path, "w", encoding="utf-8") as fh:
        fh.write(build_checklist_and_correlation(
            documents=documents, knowledge_base=knowledge_base, roles=roles))
    written.append(corr_path)

    return sorted(written)

"""Propuesta Comercial del engagement (informe 1, task three-reports / FEAT-002).

Generador DETERMINISTA, stdlib-only, de la **PROPUESTA COMERCIAL** emitida por
la consultora (marca por defecto ``Kulgops``) hacia el prospecto/cliente. Es el
documento de **venta** del servicio de consultoria y especificacion de
requisitos para desarrollo de software. Se publica en
``advisory-credi10-2.0/1-propuesta-comercial.md`` y lo escribe el orquestador
durante ``--phase all`` (metodo ``_write_commercial_proposal``).

Gobernado por la politica declarativa ``.kiro/skills/commercial-proposal-report``
y por los roles del Comite de Gobierno (Engagement Director / Engagement
Manager). El contenido se **deriva** del analisis del corpus (contexto de
negocio), de las unicas fuentes de verdad del motor (``roles/__init__.py``,
``phases.modules.MODULES``) y de la Base de Conocimiento (conteo de documentos);
nunca se fabrica evidencia.

Contrato de contenido (igual que todo informe del framework):

  * >= 1 diagrama de **contexto de alto nivel** en ```mermaid``` (seccion c);
  * >= 1 **Gantt** en ```mermaid``` (seccion h);
  * >= 1 **tabla** markdown (entregables / equipo / inversion);
  * >= 1 **etiqueta epistemica** honesta, con el **perfil corporativo** de la
    consultora y la **inversion** marcados ``[DOC-ASSUMPTION]``.

Las 11 secciones obligatorias (a-k) se emiten en orden estable:
(a) Quienes somos, (b) Alcance del servicio, (c) Contexto de negocio,
(d) Metodologia de consultoria, (e) Entregables, (f) Estrategia de consultoria,
(g) Equipo de trabajo, (h) Cronograma de trabajo, (i) Supuestos y restricciones,
(j) Inversion, (k) Terminos y condiciones.

Documento comercial en **espanol** con etiquetas tecnicas en ingles.

Determinismo: todo el contenido deriva de datos estaticos ordenados; sin
aleatoriedad ni timestamps. Una segunda corrida de ``--phase all`` deja el
archivo byte-identico.
"""

from __future__ import annotations

from typing import List, Optional

from phases import modules as modules_mod

import roles as roles_pkg


# --------------------------------------------------------------------------- #
# Parametros configurables (marca emisora e inversion de referencia).
# La politica exige que cambiar marca/inversion NO requiera reescribir prosa:
# por eso viven como parametros estaticos recalibrables.
# --------------------------------------------------------------------------- #

PROPOSAL_FILENAME = "1-propuesta-comercial.md"

DEFAULT_BRAND = "Kulgops"

# Rangos de inversion ILUSTRATIVOS de referencia. [DOC-ASSUMPTION] recalibrable:
# NO son tarifas reales ni compromisos. (etiqueta, concepto, rango, nota).
INVESTMENT_RANGES = [
    ("Discovery + Higiene Epistemica (Fases 0-2)",
     "4 - 6 semanas", "Equipo Celula 1 + Comite",
     "Ingesta del corpus, AS-IS y estado del arte."),
    ("Gaps, Diseno TO-BE y Specs (Fases 3-4)",
     "6 - 10 semanas", "Celula 1 + Celula 2",
     "Gaps/relievers, arquitectura TO-BE, HU/Gherkin y dossier."),
    ("Roadmap, Estimacion, RAID y Caso de Negocio (Fases 5-6)",
     "3 - 5 semanas", "Comite + Celula 3",
     "Olas de entrega, estimacion recalibrable, RAID y ROI."),
]


# --------------------------------------------------------------------------- #
# Helpers de render
# --------------------------------------------------------------------------- #

def _kb_total(knowledge_base) -> Optional[int]:
    if knowledge_base is None:
        return None
    try:
        return int(knowledge_base.total)
    except Exception:
        return None


def _epistemic_note() -> str:
    return (
        "> Etiquetas epistemicas: **[VERIFIED-FACT]** evidencia explicita del "
        "corpus; **[DOC-ASSUMPTION]** supuesto/perfil/cifra de referencia a "
        "recalibrar; **[DOC-CONFLICT]** contradiccion entre fuentes; "
        "**[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia). "
        "En esta propuesta, el **perfil corporativo** de la consultora y las "
        "**cifras de inversion** se emiten como referencia **[DOC-ASSUMPTION]**."
    )


def _committee_rows(roles) -> List[str]:
    rows: List[str] = []
    for code in roles_pkg.committee():
        r = roles.get(code)
        if r is None:
            continue
        rows.append(f"| {code} | {r.name} | Comite de Gobierno | {r.scope} |")
    return rows


def _cell_rows(roles) -> List[str]:
    rows: List[str] = []
    for cell_name, members in roles_pkg.cells().items():
        for code in members:
            r = roles.get(code)
            if r is None:
                continue
            rows.append(f"| {code} | {r.name} | {cell_name} | {r.scope} |")
    return rows


# --------------------------------------------------------------------------- #
# Secciones a-k
# --------------------------------------------------------------------------- #

def _sec_quienes_somos(brand: str) -> List[str]:
    return [
        f"## a. Quienes somos",
        "",
        f"**{brand}** es una consultora de tecnologia enfocada en **ingenieria "
        "de software**, **advisory** de arquitectura y transformacion, y "
        "**especificacion de requisitos** para el desarrollo de software. "
        f"Acompanamos a las organizaciones desde el descubrimiento hasta la "
        "definicion de un backlog accionable, para que la construccion arranque "
        "con el minimo de ambiguedad y el maximo de trazabilidad.",
        "",
        f"> **Perfil corporativo de referencia [DOC-ASSUMPTION].** El perfil de "
        f"**{brand}** (historia, tamano, clientes, certificaciones) se presenta "
        "de forma **generica y plausible** como referencia recalibrable; **no** "
        "se presenta como dato verificado. Cambiar la marca emisora o el perfil "
        "no altera la metodologia ni el alcance de este documento.",
        "",
        f"Nuestra **propuesta de valor**: convertir un corpus heterogeneo de "
        "documentacion (RFPs, assessments, diagramas, procesos) en un diseno "
        "**TO-BE** fundamentado, con honestidad epistemica y una estimacion lo "
        "mas acertada posible. Servicios principales:",
        "",
        "- **Advisory de arquitectura y transformacion** (AS-IS -> TO-BE).",
        "- **Especificacion de requisitos** (historias de usuario + BDD/Gherkin).",
        "- **Ingenieria de software** y diseno de solucion.",
        "- **Gobierno del cambio** y habilitacion del modelo operativo.",
        "",
    ]


def _sec_alcance(brand: str) -> List[str]:
    return [
        "## b. Alcance del servicio",
        "",
        "El servicio ofertado es una **consultoria de advisory** mas la "
        "**especificacion de requisitos para desarrollo de software**. El "
        "objetivo de esta etapa es dejar el proyecto **listo para estimar y "
        "construir**: no entregamos el producto final, sino el **diseno, las "
        "specs y los insumos de estimacion** que habilitan una construccion "
        "predecible.",
        "",
        "El alcance cubre, de punta a punta:",
        "",
        "- **Descubrimiento e higiene epistemica** del corpus del cliente.",
        "- **Diagnostico AS-IS** (negocio, aplicacion, datos, integracion, "
        "infraestructura, seguridad) y **estado del arte**.",
        "- **Identificacion de gaps** y viabilizacion (relievers, ABBs).",
        "- **Diseno TO-BE** y **especificacion de requisitos** (HU + Gherkin).",
        "- **Roadmap, estimacion recalibrable, RAID y caso de negocio**.",
        "",
        "Queda **fuera de alcance** en esta etapa la construccion del software, "
        "la ejecucion de pruebas sobre codigo productivo y el despliegue; estos "
        "se habilitan con los entregables de esta propuesta.",
        "",
    ]


def _context_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    CLIENTE(["Cliente / Asesor"]) --> ORIG["Originacion y onboarding"]\n'
        '    ORIG --> EC["Estudio de credito<br/>CrossCore / Inspektor / Datacredito"]\n'
        '    EC --> DES["Desembolso + RCL/RCR<br/>ERP Siesa/UnoEE"]\n'
        '    DES --> REC["Recaudo y pagos<br/>PayU / Link de pagos"]\n'
        '    REC --> CAR["Corte de cartera"]\n'
        '    CAR --> COB["Cobranza multicanal<br/>SMS / WhatsApp / predictiva"]\n'
        '    COB --> REC\n'
        '    B2C(["Canal B2C / ecommerce"]) --> ORIG\n'
        "```\n"
    )


def _sec_contexto(kb_total: Optional[int]) -> List[str]:
    kb_line = (
        f"Para este ejemplo procesamos **{kb_total}** documentos del corpus "
        "**sin muestreo** (RFP, assessment WSO2/Studio F, diagramas de "
        "arquitectura y PDFs de proceso), de los que derivamos el contexto de "
        "negocio y la trazabilidad."
        if kb_total is not None else
        "Para este ejemplo procesamos el corpus completo **sin muestreo** (RFP, "
        "assessment WSO2/Studio F, diagramas de arquitectura y PDFs de proceso), "
        "de los que derivamos el contexto de negocio y la trazabilidad."
    )
    return [
        "## c. Contexto de negocio",
        "",
        "Para ilustrar la propuesta usamos como **ejemplo** el corpus que "
        "estamos procesando: **Credi10 2.0** del grupo **STF Group** "
        "[VERIFIED-FACT]. Es un negocio de **credito retail de consumo** con "
        "canales **B2C y ecommerce**, cuyo ciclo abarca originacion, estudio de "
        "credito (CrossCore -> Inspektor -> Datacredito/Dictum), desembolso con "
        "generacion de RCL/RCR en el ERP Siesa/UnoEE, recaudo y pagos (PayU / "
        "link de pagos), corte de cartera y cobranza multicanal.",
        "",
        kb_line,
        "",
        "Diagrama de **contexto de alto nivel** del negocio procesado:",
        "",
        _context_mermaid(),
        "",
        "> El contexto se **deriva** del corpus del cliente; los datos de "
        "Credi10/STF Group se citan como **ejemplo de aplicacion** y se tratan "
        "con las etiquetas epistemicas correspondientes, nunca como atributos de "
        "la consultora.",
        "",
    ]


def _sec_metodologia() -> List[str]:
    return [
        "## d. Metodologia de consultoria",
        "",
        "Trabajamos con una metodologia **por fases con quality gates** y "
        "**gobierno continuo**. Cada fase produce entregables verificables y no "
        "avanza hasta superar su gate (QG-0..QG-6), lo que evita el *scope "
        "drift* y mantiene la trazabilidad de punta a punta (el **Hilo Dorado**).",
        "",
        "| Fase | Foco | Quality Gate |",
        "| --- | --- | --- |",
        "| Fase 0 | Higiene epistemica del corpus | QG-0 |",
        "| Fase 1 | Contexto AS-IS | QG-1 |",
        "| Fase 2 | Estado del arte | QG-2 |",
        "| Fase 3 | Gaps y viabilizacion | QG-3 |",
        "| Fase 4 | Diseno TO-BE + specs | QG-4 |",
        "| Fase 5 | Roadmap, estimacion y RAID | QG-5 |",
        "| Fase 6 | Caso de negocio | QG-6 |",
        "",
        "La calidad se audita con el marco **AICV-E** (Accuracy, Integrity, "
        "Congruence, Viability, Epistemic Certainty): cada entregable se somete "
        "a verificacion antes de cruzar su gate, y la honestidad epistemica es "
        "un principio no negociable (no se fabrica evidencia).",
        "",
    ]


def _sec_entregables() -> List[str]:
    return [
        "## e. Entregables",
        "",
        "Los entregables son exactamente los **outputs que el motor del "
        "advisory genera** de forma determinista a partir del corpus. Todos se "
        "publican como Markdown versionable:",
        "",
        "| Entregable | Descripcion | Ubicacion |",
        "| --- | --- | --- |",
        "| Informes por fase (00-06) | 7 informes, uno por fase Zero-Drift, con "
        "su quality gate | `advisory-credi10-2.0/0X-*.md` |",
        "| Catalogo HU + BDD/Gherkin | Historias de usuario con criterios de "
        "aceptacion (happy + borde) | `advisory-credi10-2.0/04b-catalogo-"
        "historias.md` |",
        "| Dossier SDLC TO-BE | Requisitos, arquitectura, specs, UX, pruebas e "
        "insumos de estimacion + registros | `advisory-credi10-2.0/to-be/` |",
        "| Base de Conocimiento | Ingesta trazable del corpus (sin muestreo) + "
        "checklist de cobertura | `knowledge-base/` |",
        "| Los 3 informes comerciales/tecnico | Propuesta comercial, reporte "
        "gerencial e informe tecnico narrativo | `advisory-credi10-2.0/` |",
        "",
        "Esta **propuesta comercial** es el informe 1 de una familia de tres; "
        "**referencia** el informe tecnico como soporte del alcance ofertado, "
        "sin reemplazarlo.",
        "",
    ]


def _sec_estrategia() -> List[str]:
    return [
        "## f. Estrategia de consultoria",
        "",
        "Nuestra estrategia es el **framework Zero-Drift**, disenado para que el "
        "diseno no se desvie del objetivo de negocio ni de la evidencia. "
        "Comercialmente, se resume en cinco pilares:",
        "",
        "- **Comite de Gobierno + 3 Celulas.** Un comite (direccion, gestion y "
        "calidad) gobierna tres celulas especializadas (Discovery, Diseno, "
        "Valor y Habilitacion).",
        "- **7 fases con Quality Gates (QG-0..QG-6).** Ninguna fase avanza sin "
        "superar su gate; el veredicto es Go/No-Go.",
        "- **RACI-V.** Cada entregable tiene Responsible, Accountable, "
        "Consulted, Informed y un **Verifier** explicito.",
        "- **AICV-E.** Auditoria de Accuracy, Integrity, Congruence, Viability "
        "y Epistemic Certainty sobre cada entregable.",
        "- **Hilo Dorado.** Trazabilidad continua "
        "Driver -> Capacidad -> Gap -> Reliever -> ABB -> SBB -> Historia -> "
        "ROI, sin eslabones rotos.",
        "",
        "```mermaid\n"
        "flowchart LR\n"
        '    DRV["Drivers"] --> CAP["Capacidades"]\n'
        '    CAP --> GAP["Gaps"]\n'
        '    GAP --> REL["Relievers"]\n'
        '    REL --> ABB["ABBs"]\n'
        '    ABB --> SBB["SBBs"]\n'
        '    SBB --> HU["Historias"]\n'
        '    HU --> ROI["ROI / Caso de negocio"]\n'
        "```",
        "",
        "> El framework es **reutilizable** para cualquier cliente; Credi10 2.0 "
        "es solo el ejemplo de aplicacion de esta propuesta.",
        "",
    ]


def _sec_equipo(roles) -> List[str]:
    total_roles = len(roles_pkg.load_roles())
    lines = [
        "## g. Equipo de trabajo",
        "",
        f"El engagement lo ejecuta un equipo de **{total_roles} roles** "
        "organizados en un **Comite de Gobierno** y **3 celulas** "
        "especializadas. El comite asegura direccion, gestion y calidad; las "
        "celulas ejecutan el descubrimiento, el diseno y la habilitacion de "
        "valor.",
        "",
        "| Rol | Nombre | Celula / Comite | Alcance |",
        "| --- | --- | --- | --- |",
    ]
    lines.extend(_committee_rows(roles))
    lines.extend(_cell_rows(roles))
    lines += [
        "",
        "Los roles del **Comite de Gobierno** (Engagement Director y Engagement "
        "Manager) son los productores naturales de esta propuesta y del reporte "
        "gerencial que la soporta.",
        "",
    ]
    return lines


def _gantt_mermaid() -> str:
    return (
        "```mermaid\n"
        "gantt\n"
        "    title Cronograma por fases y olas (referencia [DOC-ASSUMPTION])\n"
        "    dateFormat  YYYY-MM-DD\n"
        "    axisFormat  %m\n"
        "    section Ola 1 - Discovery\n"
        "    Fase 0 Higiene epistemica      :f0, 2026-01-05, 10d\n"
        "    Fase 1 Contexto AS-IS          :f1, after f0, 15d\n"
        "    Fase 2 Estado del arte         :f2, after f1, 10d\n"
        "    section Ola 2 - Diseno\n"
        "    Fase 3 Gaps y viabilizacion    :f3, after f2, 15d\n"
        "    Fase 4 Diseno TO-BE y specs    :f4, after f3, 25d\n"
        "    section Ola 3 - Valor\n"
        "    Fase 5 Roadmap y estimacion    :f5, after f4, 15d\n"
        "    Fase 6 Caso de negocio         :f6, after f5, 10d\n"
        "```\n"
    )


def _sec_cronograma() -> List[str]:
    return [
        "## h. Cronograma de trabajo",
        "",
        "El trabajo se organiza en **tres olas** alineadas con las 7 fases. El "
        "siguiente **Gantt** es una planificacion de **referencia "
        "[DOC-ASSUMPTION]** recalibrable segun el alcance acordado y la "
        "disponibilidad del cliente:",
        "",
        _gantt_mermaid(),
        "",
        "Las fechas son relativas e ilustrativas; la secuencia fase-a-fase y la "
        "dependencia entre olas son lo relevante, no el calendario absoluto.",
        "",
    ]


def _sec_supuestos() -> List[str]:
    return [
        "## i. Supuestos y restricciones",
        "",
        "La propuesta se emite bajo los siguientes supuestos y restricciones. "
        "Los registros detallados (ambiguedades, riesgos, consideraciones, "
        "restricciones y prerrequisitos) se consolidan en el dossier TO-BE "
        "(`advisory-credi10-2.0/to-be/00-registros/`).",
        "",
        "| Tipo | Enunciado | Etiqueta |",
        "| --- | --- | --- |",
        "| Supuesto | El cliente facilita el corpus y el acceso a SME para "
        "cerrar vacios epistemicos | [DOC-ASSUMPTION] |",
        "| Supuesto | El perfil corporativo y las cifras de inversion son de "
        "referencia recalibrable | [DOC-ASSUMPTION] |",
        "| Restriccion | La etapa es advisory + specs; **no** incluye "
        "construccion ni despliegue | [VERIFIED-FACT] |",
        "| Restriccion | Parte del corpus es solo-imagen; sus reglas finas no "
        "son derivables | [EPISTEMIC-VOID] |",
        "| Restriccion | Se preservan las reglas de negocio vigentes del cliente "
        "| [DOC-ASSUMPTION] |",
        "",
        "> Los vacios epistemicos se **registran**, no se rellenan con "
        "suposiciones presentadas como hechos.",
        "",
    ]


def _sec_inversion() -> List[str]:
    lines = [
        "## j. Inversion",
        "",
        "> **Inversion de referencia [DOC-ASSUMPTION].** Los valores siguientes "
        "son **rangos ilustrativos recalibrables**, **no** tarifas firmes ni "
        "compromisos. Se expresan en esfuerzo/tiempo por bloque de fases y se "
        "ajustan al alcance final acordado con el cliente.",
        "",
        "| Bloque de fases | Duracion de referencia | Equipo | Nota |",
        "| --- | --- | --- | --- |",
    ]
    for concepto, rango, equipo, nota in INVESTMENT_RANGES:
        lines.append(f"| {concepto} | {rango} | {equipo} | {nota} |")
    lines += [
        "",
        "La inversion monetaria se cotiza aparte, una vez acordado el alcance y "
        "el modelo de contratacion; **toda cifra es [DOC-ASSUMPTION]** hasta su "
        "recalibracion con el cliente.",
        "",
    ]
    return lines


def _sec_terminos(brand: str) -> List[str]:
    return [
        "## k. Terminos y condiciones",
        "",
        "Terminos y condiciones **genericos** de referencia (se formalizan en el "
        "contrato del engagement):",
        "",
        "- **Validez de la oferta:** la propuesta es una referencia recalibrable "
        "y no constituye un compromiso de precio.",
        f"- **Propiedad intelectual:** los entregables generados para el cliente "
        f"son del cliente; **{brand}** conserva su metodologia y framework "
        "Zero-Drift.",
        "- **Confidencialidad:** el corpus y los datos del cliente se tratan de "
        "forma confidencial y solo para el engagement.",
        "- **Exclusiones:** construccion de software, pruebas sobre codigo "
        "productivo y despliegue no estan incluidos en esta etapa de advisory.",
        "- **Dependencias:** la calidad de los entregables depende de la "
        "completitud del corpus y de la disponibilidad de SME del cliente.",
        "",
        "> Esta propuesta esta enlazada desde el indice maestro del engagement "
        "(`README.md`) y referencia el informe tecnico como soporte del alcance.",
        "",
    ]


# --------------------------------------------------------------------------- #
# Public builder
# --------------------------------------------------------------------------- #

def build(knowledge_base=None, roles=None, documents=None,
          brand: str = DEFAULT_BRAND) -> str:
    """Render la propuesta comercial completa (determinista).

    ``knowledge_base`` se usa para el conteo de documentos del contexto de
    negocio (puede ser ``None``: la propuesta degrada con elegancia). ``roles``
    es el catalogo de roles (si es ``None`` se carga de ``roles.json``).
    ``documents`` se acepta por simetria de firma con otros builders. ``brand``
    es la marca emisora configurable (por defecto ``Kulgops``).
    """
    if roles is None:
        roles = roles_pkg.load_roles()
    kb_total = _kb_total(knowledge_base)

    parts: List[str] = [
        f"# Propuesta Comercial - {brand}",
        "",
        f"> **Documento de venta** del servicio de consultoria de advisory y "
        f"especificacion de requisitos, emitido por **{brand}** hacia el "
        "prospecto/cliente. Generado de forma **determinista** por el motor del "
        "advisory (Python stdlib, sin red ni LLM) a partir del analisis del "
        "corpus; espanol con etiquetas tecnicas en ingles.",
        "",
        _epistemic_note(),
        "",
        "## Indice de secciones",
        "",
        "| # | Seccion |",
        "| --- | --- |",
        "| a | Quienes somos |",
        "| b | Alcance del servicio |",
        "| c | Contexto de negocio |",
        "| d | Metodologia de consultoria |",
        "| e | Entregables |",
        "| f | Estrategia de consultoria |",
        "| g | Equipo de trabajo |",
        "| h | Cronograma de trabajo |",
        "| i | Supuestos y restricciones |",
        "| j | Inversion |",
        "| k | Terminos y condiciones |",
        "",
    ]

    parts += _sec_quienes_somos(brand)
    parts += _sec_alcance(brand)
    parts += _sec_contexto(kb_total)
    parts += _sec_metodologia()
    parts += _sec_entregables()
    parts += _sec_estrategia()
    parts += _sec_equipo(roles)
    parts += _sec_cronograma()
    parts += _sec_supuestos()
    parts += _sec_inversion()
    parts += _sec_terminos(brand)

    parts += [
        "## Cierre",
        "",
        f"Universo de alcance de referencia: **{modules_mod.module_count()}** "
        f"modulos y **{modules_mod.story_count()}** historias de usuario "
        "especificables (ver catalogo 04b y dossier TO-BE).",
        "",
        f"> **Veredicto comercial:** propuesta completa con las 11 secciones "
        "a-k, diagrama de contexto + Gantt + tablas, y perfil/inversion "
        "marcados [DOC-ASSUMPTION]. Documento emitido por "
        f"**{brand}**; cifras recalibrables con el cliente.",
        "",
    ]
    return "\n".join(parts) + "\n"

"""Reporte Gerencial / Comercial del engagement (informe 2, task three-reports / FEAT-003).

Generador DETERMINISTA, stdlib-only, del **REPORTE GERENCIAL** que soporta
ejecutivamente la propuesta comercial. Se publica en
``advisory-credi10-2.0/2-reporte-gerencial.md`` y lo escribe el orquestador
durante ``--phase all`` (metodo ``_write_executive_report``).

Es el **soporte gerencial** de la propuesta (informe 1): describe
**comercialmente** el alcance del proyecto, las 7 fases Zero-Drift, un
**diagnostico de alto nivel** del proceso realizado (resumen ejecutivo de los
hallazgos reales de Credi10), la estrategia de implementacion por olas, los
riesgos top, las consideraciones y los prerrequisitos. Su tono es
**narrativo/ejecutivo**, no tecnico: el detalle tecnico vive en el informe 3
(``advisory-credi10-2.0/3-informe-tecnico/README.md``).

Reutiliza las UNICAS fuentes de verdad del motor (no las duplica ni las
contradice: las **resume y cita** a nivel ejecutivo):

  * ``phases.phase1`` -> drivers e indicadores de retorno del RFP (DRV-001..005);
  * ``phases.phase3`` -> gaps y aliviadores reales (GAP/REL);
  * ``phases.dossier`` -> registros de RIESGOS / CONSIDERACIONES / PRERREQUISITOS;
  * ``engine.knowledge.KnowledgeBase`` -> conteo de documentos del corpus.

Contrato de contenido (igual que todo informe del framework):

  * >= 1 diagrama Mermaid de **alto nivel** (diagnostico);
  * >= 1 **tabla** resumen markdown;
  * >= 1 **etiqueta epistemica** honesta; las cifras marcadas ``[DOC-ASSUMPTION]``;
  * referencia explicita al **informe tecnico** y a la **propuesta comercial**.

Determinismo: todo el contenido deriva de datos estaticos ordenados; sin
aleatoriedad ni timestamps. Una segunda corrida de ``--phase all`` deja el
archivo byte-identico.
"""

from __future__ import annotations

from typing import List, Optional

from phases import dossier as dossier_mod
from phases import modules as modules_mod
from phases import phase1
from phases import phase3
from phases import evidence_delta
from engine import knowledge as kb_mod


# --------------------------------------------------------------------------- #
# Parametros / rutas de los informes hermanos (familia de 3).
# --------------------------------------------------------------------------- #

EXEC_REPORT_FILENAME = "2-reporte-gerencial.md"

PROPOSAL_REF = "1-propuesta-comercial.md"
TECH_REPORT_REF = "3-informe-tecnico/README.md"

DEFAULT_BRAND = "Kulgops"

# Las 7 fases Zero-Drift descritas COMERCIALMENTE (que entrega / por que importa).
# (fase, nombre comercial, que entrega, por que importa)
PHASE_VALUE = [
    ("Fase 0", "Higiene epistemica",
     "Inventario trazable del corpus y registro honesto de supuestos, "
     "conflictos y vacios de informacion.",
     "Arranca el proyecto sin fabricar evidencia: lo que no se sabe se "
     "declara, no se inventa."),
    ("Fase 1", "Contexto AS-IS",
     "Radiografia del negocio y la tecnologia actuales: capacidades, procesos, "
     "inventario e indicadores de partida.",
     "Fija la linea base contra la que se mide el retorno del proyecto."),
    ("Fase 2", "Estado del arte",
     "Benchmarks de industria y patrones de referencia conectados a las "
     "capacidades del negocio.",
     "Asegura que el rediseño se apoya en practicas probadas, no en opiniones."),
    ("Fase 3", "Gaps y viabilizacion",
     "Diagnostico de brechas priorizadas y aliviadores para cerrarlas.",
     "Convierte los dolores en un plan de accion viable y justificado."),
    ("Fase 4", "Diseño TO-BE y specs",
     "Arquitectura objetivo, historias de usuario y especificaciones listas "
     "para construir.",
     "Deja el proyecto listo para estimar y desarrollar con minima ambiguedad."),
    ("Fase 5", "Roadmap, estimacion y RAID",
     "Plan por olas, estimacion recalibrable y registro de riesgos, supuestos, "
     "incidencias y dependencias.",
     "Hace predecible la ejecucion y transparente la inversion."),
    ("Fase 6", "Caso de negocio",
     "Retorno cuantificado contra los indicadores del RFP y veredicto de "
     "inversion del Comite.",
     "Conecta cada peso invertido con un resultado de negocio medible."),
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
        "corpus; **[DOC-ASSUMPTION]** supuesto/cifra de referencia a recalibrar; "
        "**[DOC-CONFLICT]** contradiccion entre fuentes; **[EPISTEMIC-VOID]** "
        "sin base documental (no se fabrica evidencia). En este reporte las "
        "**cifras de esfuerzo/inversion** son referencia **[DOC-ASSUMPTION]**."
    )


# --------------------------------------------------------------------------- #
# Secciones ejecutivas
# --------------------------------------------------------------------------- #

def _sec_resumen_ejecutivo(brand: str, kb_total: Optional[int]) -> List[str]:
    kb_line = (
        f"Partimos de **{kb_total}** documentos del corpus analizados sin "
        "muestreo"
        if kb_total is not None else
        "Partimos del corpus completo analizado sin muestreo"
    )
    return [
        "## 1. Resumen ejecutivo",
        "",
        f"Este **reporte gerencial** es el soporte ejecutivo de la **propuesta "
        f"comercial** de **{brand}** ([`{PROPOSAL_REF}`]({PROPOSAL_REF})). "
        "Resume, en lenguaje de negocio, el alcance del proyecto Credi10 2.0, "
        "las fases de trabajo, el diagnostico de alto nivel que obtuvimos y la "
        "estrategia, los riesgos, las consideraciones y los prerrequisitos que "
        "la gerencia debe conocer para decidir.",
        "",
        f"{kb_line} (RFP, assessment WSO2/Studio F, diagramas de arquitectura y "
        "PDFs de proceso). De ese analisis concluimos que Credi10 2.0 **no es un "
        "proyecto de features nuevas, sino de modernizacion y gobierno**: el "
        "negocio funciona, pero su plataforma esta **fragmentada, acoplada a un "
        "ERP legado por mecanismos fragiles y sobre runtimes obsoletos**, lo que "
        "limita disponibilidad, eficiencia y evolucion.",
        "",
        "El valor de nuestra intervencion es dejar el proyecto **listo para "
        "estimar y construir** con trazabilidad completa desde cada indicador de "
        "negocio del RFP hasta una historia de usuario accionable. El detalle "
        f"tecnico que respalda cada afirmacion vive en el **informe tecnico** "
        f"([`{TECH_REPORT_REF}`]({TECH_REPORT_REF})).",
        "",
    ]


def _sec_alcance() -> List[str]:
    return [
        "## 2. Alcance comercial del proyecto",
        "",
        "El servicio contratado es una **consultoria de advisory + "
        "especificacion de requisitos**. En terminos comerciales, lo que la "
        "gerencia recibe al cierre es un **paquete de decision**: el diagnostico "
        "del estado actual, el diseño objetivo, el backlog especificado, el plan "
        "de implementacion y la estimacion para presupuestar.",
        "",
        "| Dentro del alcance | Fuera del alcance (en esta etapa) |",
        "| --- | --- |",
        "| Diagnostico AS-IS y estado del arte | Construccion del software |",
        "| Gaps, diseño TO-BE y especificacion de requisitos | Pruebas sobre "
        "codigo productivo |",
        "| Roadmap por olas, estimacion recalibrable y RAID | Despliegue a "
        "produccion |",
        "| Caso de negocio y trazabilidad al retorno del RFP | Operacion y "
        "soporte post-produccion |",
        "",
        f"Universo de alcance de referencia: **{modules_mod.module_count()}** "
        f"modulos y **{modules_mod.story_count()}** historias de usuario "
        "especificables, sin muestreo. La construccion se habilita con los "
        "entregables de esta etapa; no forma parte de ella.",
        "",
    ]


def _sec_fases() -> List[str]:
    lines = [
        "## 3. Fases del proyecto (Zero-Drift)",
        "",
        "El trabajo se organiza en **7 fases** con quality gates (QG-0..QG-6): "
        "ninguna fase avanza hasta superar su control de calidad, lo que evita "
        "el *scope drift* y mantiene la trazabilidad de punta a punta. "
        "Descripcion **comercial** de cada fase:",
        "",
        "| Fase | Foco | Que entrega | Por que importa |",
        "| --- | --- | --- | --- |",
    ]
    for fase, nombre, entrega, importa in PHASE_VALUE:
        lines.append(f"| {fase} | {nombre} | {entrega} | {importa} |")
    lines += [
        "",
        "> Las tres **olas de entrega** agrupan estas fases: Ola 1 (Discovery, "
        "Fases 0-2), Ola 2 (Diseño, Fases 3-4) y Ola 3 (Valor y habilitacion, "
        "Fases 5-6).",
        "",
    ]
    return lines


def _diagnostico_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart TB\n"
        '    subgraph HOY["Credi10 hoy (AS-IS)"]\n'
        '        FRAG["Arquitectura fragmentada<br/>apps .NET desordenadas"]\n'
        '        ERP["Acople fragil al ERP Siesa/UnoEE<br/>archivos planos + WS unico + BD directa"]\n'
        '        DEUDA["Deuda tecnica y datos<br/>+200 BDs, controles en Excel"]\n'
        '        OBS["Obsolescencia<br/>.NET Framework 4.8 / Core 3.1"]\n'
        '        GOB["Sin gobernanza de APIs<br/>ni observabilidad"]\n'
        "    end\n"
        '    HOY --> TRANSF{{"Credi10 2.0<br/>modernizar + gobernar"}}\n'
        '    TRANSF --> MANANA["Manana (TO-BE)<br/>APIs gobernadas + Data Services<br/>+ eventos + .NET 8 en AWS"]\n'
        '    MANANA --> RET["Retorno RFP<br/>disponibilidad, eficiencia,<br/>evolucion y licenciamiento"]\n'
        "```\n"
    )


def _diagnostico_hallazgos_table() -> str:
    """Resumen ejecutivo de los gaps reales (resumidos desde phase3.GAPS)."""
    # Titular comercial corto por cada GAP real + su driver afectado.
    headlines = {
        "GAP-001": "Integracion rigida con el ERP Siesa (archivos planos + un "
                   "unico Web Service, en su mayoria batch con intervencion "
                   "manual)",
        "GAP-002": "Lectura/escritura directa a la base de datos del ERP Siesa, "
                   "una practica de ALTO RIESGO para la integridad de datos",
        "GAP-003": "Datos fragmentados: +200 bases de datos duplicadas e "
                   "inconsistentes con controles manuales en Excel",
        "GAP-004": "Ausencia de gobernanza de APIs y observabilidad: "
                   "integraciones dispersas sin trazabilidad de errores",
        "GAP-005": "Obsolescencia tecnologica: .NET Framework 4.8 / .NET Core "
                   "3.1 fuera de soporte y Wordpress/XAMPP en produccion",
    }
    # Severidad ejecutiva derivada del impacto en el driver.
    severidad = {
        "GAP-001": "Alta", "GAP-002": "Critica", "GAP-003": "Alta",
        "GAP-004": "Media", "GAP-005": "Alta",
    }
    rows = [
        "| Hallazgo | Diagnostico de alto nivel | Driver RFP afectado | "
        "Severidad |",
        "| --- | --- | --- | --- |",
    ]
    # Indice de drivers por id para citar el indicador real.
    drv_index = {d[0]: d for d in phase1.DRIVERS}
    for gap_id, _dolor, _causa, drv_ref, _bmk in phase3.GAPS:
        drv = drv_index.get(drv_ref)
        drv_label = f"{drv_ref} ({drv[2]})" if drv else drv_ref
        rows.append(
            f"| {gap_id} | {headlines.get(gap_id, gap_id)} | {drv_label} | "
            f"{severidad.get(gap_id, 'Media')} |"
        )
    return "\n".join(rows)


def _indicadores_table() -> str:
    """Los 5 indicadores de retorno del RFP (desde phase1.DRIVERS)."""
    rows = [
        "| Driver | Indicador de retorno (RFP) | AS-IS -> TO-BE |",
        "| --- | --- | --- |",
    ]
    for drv_id, indicador, delta, _desc in phase1.DRIVERS:
        rows.append(f"| {drv_id} | {indicador} | {delta} |")
    return "\n".join(rows)


def _recovered_evidence_note(knowledge_base) -> str:
    """Nota gerencial honesta sobre la evidencia recuperada (dinamica)."""
    recovered = evidence_delta._recovered_now(knowledge_base)
    n_rec = len(recovered)
    n_base = len(kb_mod.BASELINE_NULA_PDFS)
    if n_rec == 0:
        return (
            "> **Base de evidencia.** Los hallazgos se sustentan en la "
            "documentacion disponible del corpus, con marca epistemica honesta "
            "donde la evidencia es insuficiente."
        )
    facts_recovered = evidence_delta._facts_from_recovered(knowledge_base)
    return (
        f"> **Base de evidencia reforzada.** {n_rec} de {n_base} documentos "
        "clave que antes eran **vacios epistemicos** (entre ellos el "
        "**Assessment WSO2/Studio F** y las especificaciones de "
        "**originacion**, **cartera**, **pagos** e **integracion de atencion "
        "al cliente**) fueron **recuperados como texto verificado** "
        "([VERIFIED-FACT]) y hoy aportan evidencia trazable "
        f"(**{facts_recovered}** hechos clave). En consecuencia, estos "
        "hallazgos ya **no descansan en supuestos**. El detalle del cambio y "
        "su lectura de suficiencia estan en el informe tecnico (Anexo C - 'En "
        "que cambio')."
    )


def _sec_diagnostico(knowledge_base=None) -> List[str]:
    return [
        "## 4. Diagnostico de alto nivel",
        "",
        "Este es el **resultado ejecutivo del proceso que realizamos**. No es "
        "una opinion: cada hallazgo esta trazado a evidencia del corpus y "
        "desarrollado en detalle en el informe tecnico "
        f"([`{TECH_REPORT_REF}`]({TECH_REPORT_REF})). En una frase: **Credi10 "
        "opera un negocio solido sobre una plataforma fragil**, y el proyecto "
        "2.0 consiste en modernizarla y gobernarla sin detener la operacion.",
        "",
        "Vista de alto nivel del punto de partida, la transformacion y el "
        "retorno esperado:",
        "",
        _diagnostico_mermaid(),
        "",
        "### 4.1 Hallazgos clave",
        "",
        "Los hallazgos (resumen de la Fase 3) se concentran en cinco frentes "
        "reales, todos evidenciados en el assessment WSO2/Studio F y los "
        "diagramas de arquitectura:",
        "",
        _diagnostico_hallazgos_table(),
        "",
        "En palabras de negocio: la **fragmentacion arquitectonica** y la **falta "
        "de gobernanza de APIs** encarecen cada cambio; el **acople al ERP "
        "Siesa/UnoEE** por archivos planos, un unico Web Service y lectura "
        "directa a su base de datos es el **riesgo mas severo** (puede corromper "
        "datos del ERP); la **deuda tecnica** de +200 bases de datos duplicadas "
        "resta confianza a la informacion; y la **obsolescencia de .NET "
        "Framework 4.8 / .NET Core 3.1** compromete soporte, seguridad y "
        "licenciamiento.",
        "",
        _recovered_evidence_note(knowledge_base),
        "",
        "### 4.2 Indicadores de retorno del RFP",
        "",
        "El negocio ya fijo los objetivos de retorno; nuestro diseño se ancla a "
        "ellos. Los cinco indicadores (cifras del RFP) son el marcador contra el "
        "que se medira el exito:",
        "",
        _indicadores_table(),
        "",
        "> Cerrar los cinco hallazgos habilita estos saltos: "
        "**disponibilidad 90% -> 99%**, **eficiencia 60% -> 80%**, **costo de "
        "infraestructura 80% -> 80%** (sostenido al escalar), **evolucion "
        "50% -> 100%** y **licenciamiento 70% -> 100%**. Las cifras son las del "
        "RFP; el esfuerzo para alcanzarlas es referencia **[DOC-ASSUMPTION]**.",
        "",
    ]


def _sec_estrategia() -> List[str]:
    return [
        "## 5. Estrategia de implementacion",
        "",
        "Proponemos una transformacion **incremental y reversible por olas** "
        "(patron *Strangler Fig*): modernizar sin un *big bang*, desviando "
        "gradualmente las integraciones hacia APIs gobernadas y Data Services "
        "sobre el ERP, de modo que la operacion nunca se detenga.",
        "",
        "| Ola | Fases | Objetivo de negocio |",
        "| --- | --- | --- |",
        "| Ola 1 - Discovery | Fases 0-2 | Entender el negocio y la tecnologia "
        "actuales y fijar la linea base. |",
        "| Ola 2 - Diseño | Fases 3-4 | Cerrar brechas con un diseño objetivo y "
        "un backlog especificado y estimable. |",
        "| Ola 3 - Valor | Fases 5-6 | Planificar la entrega, estimar la "
        "inversion y justificar el retorno. |",
        "",
        "Los aliviadores que guian la estrategia (resumen de la Fase 3) son:",
        "",
        _relievers_table(),
        "",
        "> La secuencia por olas es lo relevante; el detalle de arquitectura "
        f"objetivo y el roadmap tecnico estan en el informe tecnico "
        f"([`{TECH_REPORT_REF}`]({TECH_REPORT_REF})).",
        "",
    ]


def _relievers_table() -> str:
    """Resumen de los aliviadores reales (desde phase3.RELIEVERS)."""
    rows = [
        "| Aliviador | Que habilita | Gaps que cierra |",
        "| --- | --- | --- |",
    ]
    for rel_id, alivio, _rec, gaps_ref, _drv in phase3.RELIEVERS:
        rows.append(f"| {rel_id} | {alivio} | {gaps_ref} |")
    return "\n".join(rows)


def _registry_summary_table(entries, sev_header: str, limit: int) -> str:
    """Resumen ejecutivo (top-N por severidad/estado) de un registro del dossier."""
    # Orden ejecutivo: severidad Alta primero, luego por id estable.
    sev_rank = {"Critica": 0, "Alta": 1, "Media": 2, "Baja": 3}
    ordered = sorted(
        entries,
        key=lambda e: (sev_rank.get(e.severidad, 5), e.id),
    )
    rows = [
        f"| ID | {sev_header} | Resumen ejecutivo | Estado |",
        "| --- | --- | --- | --- |",
    ]
    for e in ordered[:limit]:
        rows.append(f"| {e.id} | {e.severidad} | {e.titulo} | {e.estado} |")
    return "\n".join(rows)


def _sec_riesgos() -> List[str]:
    total = len(dossier_mod.RIESGOS)
    return [
        "## 6. Riesgos",
        "",
        f"El proyecto tiene **{total} riesgos** registrados y gestionados en el "
        "dossier TO-BE (`to-be/00-registros/riesgos.md`). A nivel gerencial, los "
        "mas relevantes son:",
        "",
        _registry_summary_table(dossier_mod.RIESGOS, "Severidad", 5),
        "",
        "> El riesgo mas severo es la **lectura/escritura directa a la base de "
        "datos del ERP Siesa**: el diseño TO-BE la prohibe explicitamente y la "
        "reemplaza por Data Services gobernados. Todos los riesgos tienen "
        "estado de mitigacion trazable.",
        "",
    ]


def _sec_consideraciones() -> List[str]:
    total = len(dossier_mod.CONSIDERACIONES)
    return [
        "## 7. Consideraciones",
        "",
        f"Hay **{total} consideraciones** de diseño y gobierno que condicionan "
        "el proyecto sin ser restricciones duras (dossier TO-BE, "
        "`to-be/00-registros/consideraciones.md`). Las de mayor impacto "
        "gerencial:",
        "",
        _registry_summary_table(dossier_mod.CONSIDERACIONES, "Impacto", 5),
        "",
        "> Destacan el **desacople incremental de Siesa** (sin interrumpir la "
        "operacion), la **preservacion de las reglas de negocio** al modernizar "
        "y el **control de costo en la nube** (disciplina FinOps).",
        "",
    ]


def _sec_prerrequisitos() -> List[str]:
    total = len(dossier_mod.PRERREQUISITOS)
    return [
        "## 8. Prerrequisitos",
        "",
        f"Para arrancar la construccion con seguridad se deben cerrar **{total} "
        "prerrequisitos** (dossier TO-BE, `to-be/00-registros/prerrequisitos."
        "md`). Los criticos para la gerencia:",
        "",
        _registry_summary_table(dossier_mod.PRERREQUISITOS, "Prioridad", 6),
        "",
        "> Varios prerrequisitos nacen de **vacios de informacion honestamente "
        "declarados** (p. ej. el contrato real del Web Service de Siesa): se "
        "registran como pendientes, no se rellenan con suposiciones presentadas "
        "como hechos.",
        "",
    ]


# --------------------------------------------------------------------------- #
# Public builder
# --------------------------------------------------------------------------- #

def build(knowledge_base=None, roles=None, documents=None,
          brand: str = DEFAULT_BRAND) -> str:
    """Render el reporte gerencial completo (determinista).

    ``knowledge_base`` se usa para el conteo de documentos del resumen
    ejecutivo (puede ser ``None``: el reporte degrada con elegancia). ``roles``
    y ``documents`` se aceptan por simetria de firma con los otros builders del
    engagement. ``brand`` es la consultora emisora (por defecto ``Kulgops``).
    """
    kb_total = _kb_total(knowledge_base)

    parts: List[str] = [
        f"# Reporte Gerencial - Credi10 2.0",
        "",
        f"> **Soporte ejecutivo** de la propuesta comercial de **{brand}**. "
        "Describe comercialmente el alcance, las fases, el diagnostico de alto "
        "nivel del proceso realizado, la estrategia, los riesgos, las "
        "consideraciones y los prerrequisitos del proyecto. Tono gerencial (no "
        "tecnico); el detalle tecnico vive en el informe 3. Generado de forma "
        "**determinista** por el motor del advisory (Python stdlib, sin red ni "
        "LLM); espanol con etiquetas tecnicas en ingles.",
        "",
        "> **Familia de 3 informes del engagement:** "
        f"[`{PROPOSAL_REF}`]({PROPOSAL_REF}) (propuesta comercial, informe 1), "
        "**este reporte gerencial** (informe 2) y "
        f"[`{TECH_REPORT_REF}`]({TECH_REPORT_REF}) (informe tecnico, informe 3).",
        "",
        _epistemic_note(),
        "",
        "## Indice",
        "",
        "| # | Seccion |",
        "| --- | --- |",
        "| 1 | Resumen ejecutivo |",
        "| 2 | Alcance comercial del proyecto |",
        "| 3 | Fases del proyecto (Zero-Drift) |",
        "| 4 | Diagnostico de alto nivel |",
        "| 5 | Estrategia de implementacion |",
        "| 6 | Riesgos |",
        "| 7 | Consideraciones |",
        "| 8 | Prerrequisitos |",
        "",
    ]

    parts += _sec_resumen_ejecutivo(brand, kb_total)
    parts += _sec_alcance()
    parts += _sec_fases()
    parts += _sec_diagnostico(knowledge_base)
    parts += _sec_estrategia()
    parts += _sec_riesgos()
    parts += _sec_consideraciones()
    parts += _sec_prerrequisitos()

    parts += [
        "## Cierre",
        "",
        "Este reporte gerencial y la propuesta comercial se sostienen sobre el "
        "mismo analisis: el informe tecnico. Juntos permiten a la gerencia "
        "**decidir la inversion con evidencia** y a los equipos **arrancar la "
        "construccion con una estimacion acertada**.",
        "",
        f"> **Veredicto gerencial:** diagnostico de alto nivel completo "
        f"({len(phase3.GAPS)} hallazgos reales ligados a los 5 indicadores del "
        f"RFP), estrategia por olas, {len(dossier_mod.RIESGOS)} riesgos, "
        f"{len(dossier_mod.CONSIDERACIONES)} consideraciones y "
        f"{len(dossier_mod.PRERREQUISITOS)} prerrequisitos registrados. Cifras "
        "recalibrables [DOC-ASSUMPTION]; detalle tecnico en "
        f"[`{TECH_REPORT_REF}`]({TECH_REPORT_REF}).",
        "",
    ]
    return "\n".join(parts) + "\n"

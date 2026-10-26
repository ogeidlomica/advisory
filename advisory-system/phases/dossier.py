"""Dossier TO-BE del proyecto Credi10 2.0 (FEAT-002, task TO-BE dossier).

Generador DETERMINISTA, stdlib-only, del **dossier de proyecto TO-BE**
organizado con **una subcarpeta por etapa/practica del SDLC**:

  * ``01-requisitos/``        requisitos funcionales + NFR ISO 25010 + reglas
  * ``02-arquitectura/``      vistas TO-BE por nivel arquitectonico
  * ``03-specs/``             contratos API/datos + specs por modulo
  * ``04-ux/``                service blueprints, journeys, wireflows
  * ``05-pruebas/``           estrategia, matriz, casos, Dry-Run, aceptacion
  * ``06-insumos-estimacion/`` descomposicion + tabla parametrica recalibrable

y, de forma transversal, los **registros** del proyecto en TODOS los niveles
arquitectonicos ({negocio, aplicacion, datos, integracion, infraestructura,
seguridad}):

  * ``00-registros/ambiguedades.md``
  * ``00-registros/riesgos.md``
  * ``00-registros/consideraciones.md``
  * ``00-registros/restricciones.md``
  * ``00-registros/prerrequisitos.md``

Reutiliza las UNICAS fuentes de verdad existentes (no las duplica, las cita):
``phases.modules.MODULES`` (MOD-01..MOD-17 con historias BDD/Gherkin),
``phases.phase4.SBBS`` (SBB-001..008), ``phases.phase3`` (GAPS/RELIEVERS/ABBS)
y la Base de Conocimiento (``engine.knowledge.KnowledgeBase``) para fundamentar
el contenido y marcar honestamente los [EPISTEMIC-VOID].

Es DOCUMENTACION generada por el motor del advisory (no codigo de la solucion).
Cada capitulo cumple el contrato estructural de los informes: >= 1 bloque
```mermaid```, >= 1 tabla markdown y >= 1 etiqueta epistemica. Las cifras de
esfuerzo llevan [DOC-ASSUMPTION].

Determinismo: todo el contenido deriva de datos estaticos ordenados; sin
aleatoriedad ni timestamps. Un segundo ``--phase all`` consecutivo deja el
arbol byte-identico.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

from phases import modules as modules_mod
from phases.modules import MODULES
from phases import phase3
from phases.phase4 import SBBS


# --------------------------------------------------------------------------- #
# Constantes de estructura (una subcarpeta por etapa del SDLC + registros).
# --------------------------------------------------------------------------- #

DOSSIER_DIRNAME = "to-be"

REGISTROS_DIR = "00-registros"
STAGE_DIRS = {
    "requisitos": "01-requisitos",
    "arquitectura": "02-arquitectura",
    "specs": "03-specs",
    "ux": "04-ux",
    "pruebas": "05-pruebas",
    "estimacion": "06-insumos-estimacion",
}

# Niveles arquitectonicos permitidos para los registros transversales.
NIVELES = ["negocio", "aplicacion", "datos", "integracion", "infraestructura",
           "seguridad"]


# --------------------------------------------------------------------------- #
# Modelo declarativo de entradas de registro transversal.
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class RegistryEntry:
    """Entrada de un registro transversal del proyecto.

    * ``id``        identificador estable (AMB-/RSK-/CON-/RST-/PRE-xxx).
    * ``nivel``     nivel arquitectonico (uno de ``NIVELES``).
    * ``titulo``    enunciado corto.
    * ``descripcion`` detalle fundamentado en el corpus.
    * ``severidad`` severidad/impacto (Alta/Media/Baja o similar).
    * ``estado``    estado de gestion (Abierto/Mitigando/Aceptado/...).
    * ``etiqueta``  etiqueta epistemica donde aplique (puede ser "").
    * ``fuente``    documento/fase del corpus que la sustenta.
    """

    id: str
    nivel: str
    titulo: str
    descripcion: str
    severidad: str
    estado: str
    etiqueta: str
    fuente: str


# --------------------------------------------------------------------------- #
# Registros transversales (datos estaticos derivados del analisis del corpus).
# Cada lista esta ordenada de forma estable por id.
# --------------------------------------------------------------------------- #

AMBIGUEDADES: List[RegistryEntry] = [
    RegistryEntry(
        "AMB-001", "negocio",
        "Alcance: universo Studio F vs. universo Credi10",
        "El assessment WSO2/Studio F describe +150 aplicaciones .NET y +200 "
        "bases de datos a nivel grupo Studio F, mientras el corpus de Credi10 "
        "evidencia ~20 componentes/modulos (MOD-01..MOD-17 + diagramas). No es "
        "claro cuanto del universo Studio F entra en el alcance de Credi10 2.0.",
        "Alta", "Abierto", "[DOC-CONFLICT]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; RFP_CREDI10_2_0.pdf"),
    RegistryEntry(
        "AMB-002", "integracion",
        "Contrato real del Web Service unico de Siesa",
        "El Assessment WSO2/Studio F (texto nativo recuperado, [VERIFIED-FACT]) "
        "confirma un UNICO Web Service y archivos planos batch contra "
        "Siesa/UnoEE (GAP-001); lo que el documento recuperado NO detalla son "
        "las operaciones, esquemas y SLAs de ese WS, por lo que el alcance "
        "exacto del desacople sigue siendo el vacio residual [EPISTEMIC-VOID] a "
        "cerrar con el cliente.",
        "Alta", "Abierto", "[EPISTEMIC-VOID]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; Envio_de_RCL_y_RCR.pdf"),
    RegistryEntry(
        "AMB-003", "aplicacion",
        "Reglas finas de los procesos recuperados del texto nativo",
        "Varios documentos de proceso (Captura Foto, Llamada predictiva, Boton "
        "Ecommerce, entre otros) tenian fuentes de codificacion personalizada; "
        "su capa de texto nativa fue recuperada y hoy es banda 'alta' "
        "[VERIFIED-FACT]. La ambiguedad residual ya NO es de legibilidad sino "
        "de detalle: algunas reglas finas de negocio no quedan explicitas en el "
        "texto recuperado y deben ratificarse con negocio ([DOC-ASSUMPTION]); "
        "no se fabrican.",
        "Media", "Abierto", "[DOC-ASSUMPTION]",
        "Base de Conocimiento (knowledge-base/): documentos de banda 'alta'"),
    RegistryEntry(
        "AMB-004", "datos",
        "Umbrales de scoring y decision del estudio de credito",
        "El flujo CrossCore -> Inspektor -> Datacredito/Dictum esta evidenciado, "
        "pero los umbrales de score para APROBADO/RECHAZADO/REVISION y la regla "
        "de no-hit (EX-03) no aparecen en el corpus; deben confirmarse con "
        "negocio.",
        "Media", "Abierto", "[DOC-ASSUMPTION]",
        "Originacion_CrossCore.pdf; Originacion_API_Datacredito.pdf"),
    RegistryEntry(
        "AMB-005", "seguridad",
        "Requisitos de cumplimiento (habeas data / PCI) no explicitos",
        "El manejo de datos de buros de credito y de pagos (PayU) sugiere "
        "obligaciones de proteccion de datos y PCI, pero el corpus no detalla "
        "requisitos de cumplimiento; se marca como supuesto a validar.",
        "Media", "Abierto", "[DOC-ASSUMPTION]",
        "Originacion_API_Datacredito.pdf; LinkDePagos.pdf"),
]

RIESGOS: List[RegistryEntry] = [
    RegistryEntry(
        "RSK-001", "datos",
        "Lectura/escritura directa a la BD del ERP Siesa",
        "Practica de ALTO RIESGO evidenciada en el assessment: por la lentitud "
        "del WS unico se accede directo a la base de datos del ERP Siesa "
        "(GAP-002), con riesgo de corrupcion de datos e indisponibilidad. El "
        "TO-BE lo prohibe via Data Services (ADR-002, SBB-002).",
        "Alta", "Mitigando", "[VERIFIED-FACT]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; Fase 3 (GAP-002)"),
    RegistryEntry(
        "RSK-002", "infraestructura",
        "Obsolescencia de runtime .NET Framework 4.8 y .NET Core 3.1",
        "Componentes criticos corren sobre .NET Framework 4.8 y .NET Core 3.1, "
        "ambos fuera de soporte (GAP-005), con riesgo de seguridad y "
        "mantenibilidad. El TO-BE migra a .NET 8 (ADR-003, SBB-006).",
        "Alta", "Mitigando", "[VERIFIED-FACT]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; Fase 3 (GAP-005)"),
    RegistryEntry(
        "RSK-003", "infraestructura",
        "Dependencia de la VPN IPSec con Telmex",
        "La conectividad hacia servicios/erp depende de un tunel VPN IPSec con "
        "Telmex; es un punto unico de dependencia operativa descrito en la "
        "arquitectura de infraestructura AWS.",
        "Media", "Abierto", "[VERIFIED-FACT]",
        "Arquitectura_Infraestructura_AWS_Credi10.png"),
    RegistryEntry(
        "RSK-004", "infraestructura",
        "Licenciamiento de SQL Server Enterprise",
        "El stack de datos usa SQL Server (edicion Enterprise), con riesgo de "
        "costo/cumplimiento de licenciamiento al escalar o consolidar las +200 "
        "BDs; debe gobernarse en el caso de negocio.",
        "Media", "Abierto", "[DOC-ASSUMPTION]",
        "Arquitectura_Infraestructura_AWS_Credi10.png; Assessment WSO2/Studio F"),
    RegistryEntry(
        "RSK-005", "integracion",
        "Integracion fragmentada por batch y archivos planos",
        "La integracion con Siesa es en su mayoria batch por archivos planos y "
        "un WS unico (GAP-001), con falta de sincronizacion y errores que "
        "requieren intervencion manual; riesgo de latencia e inconsistencia.",
        "Alta", "Mitigando", "[VERIFIED-FACT]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; Fase 3 (GAP-001)"),
    RegistryEntry(
        "RSK-006", "datos",
        "Inconsistencia por +200 bases de datos duplicadas",
        "A nivel grupo existen +200 BDs duplicadas/inconsistentes con logica "
        "repetida y controles manuales en Excel (GAP-003); riesgo de datos "
        "poco confiables. El TO-BE define fuente unica de verdad (ADR-005, "
        "SBB-007).",
        "Alta", "Mitigando", "[VERIFIED-FACT]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; Fase 3 (GAP-003)"),
    RegistryEntry(
        "RSK-007", "aplicacion",
        "Portal B2C sobre Wordpress/XAMPP en produccion",
        "El canal B2C corre parcialmente sobre Wordpress/XAMPP en produccion "
        "(GAP-005), ampliando la superficie de ataque y la fragilidad "
        "operativa; el TO-BE lo moderniza a .NET 8 (SBB-006).",
        "Media", "Mitigando", "[VERIFIED-FACT]",
        "B2C.pdf; Fase 3 (GAP-005)"),
    RegistryEntry(
        "RSK-008", "seguridad",
        "Integraciones dispersas sin trazabilidad de errores",
        "Las integraciones viven en servicios de Windows y cronjobs sin gestion "
        "centralizada ni observabilidad (GAP-004); riesgo de incidentes opacos "
        "y MTTR elevado. El TO-BE centraliza con API Management y observabilidad "
        "(SBB-001, SBB-005).",
        "Media", "Mitigando", "[VERIFIED-FACT]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; Fase 3 (GAP-004)"),
    RegistryEntry(
        "RSK-009", "negocio",
        "Riesgo de desfase por specs recuperadas aun sin ratificar",
        "La capa de texto nativa del corpus de proceso fue recuperada (hoy "
        "banda 'alta' [VERIFIED-FACT]); el riesgo residual ya NO es de "
        "legibilidad sino de que las specs recuperadas (originacion, cartera, "
        "pagos, integracion WSO2) no se ratifiquen 1:1 con el negocio antes de "
        "construir, lo que puede derivar en retrabajo de alcance.",
        "Media", "Abierto", "[DOC-ASSUMPTION]",
        "Base de Conocimiento (knowledge-base/coverage-checklist.md)"),
]

CONSIDERACIONES: List[RegistryEntry] = [
    RegistryEntry(
        "CON-001", "integracion",
        "Desacople incremental de Siesa (patron Strangler Fig)",
        "El desacople del WS unico/archivos planos debe ser incremental "
        "(Strangler Fig) desviando por Data Services + eventos sin interrumpir "
        "la operacion (SBB-002, SBB-003).",
        "Alta", "Vigente", "[DOC-ASSUMPTION]",
        "Fase 4 (ADR-002); Fase 3 (REL-001/REL-002)"),
    RegistryEntry(
        "CON-002", "aplicacion",
        "Preservar reglas de negocio al modernizar",
        "El RFP exige preservar las reglas de negocio existentes (RN-01..RN-04) "
        "al migrar a .NET 8 y a servicios de dominio; considerar pruebas de "
        "equivalencia funcional.",
        "Alta", "Vigente", "[VERIFIED-FACT]",
        "RFP_CREDI10_2_0.pdf; Fase 3 (reglas de negocio)"),
    RegistryEntry(
        "CON-003", "infraestructura",
        "Estrategia cloud AWS con control de costo",
        "El TO-BE despliega en AWS (VPC, ALB, WAF, contenedores) con "
        "escalamiento elastico; considerar IaC y disciplina FinOps para no "
        "degradar el costo (DRV-003, 80% -> 80%).",
        "Media", "Vigente", "[DOC-ASSUMPTION]",
        "Arquitectura_Infraestructura_AWS_Credi10.png; Fase 4 (ADR-006, SBB-008)"),
    RegistryEntry(
        "CON-004", "seguridad",
        "Modelo zero-trust y cifrado de datos sensibles",
        "El manejo de datos de buros y pagos obliga a considerar autenticacion "
        "fuerte en el API Gateway, cifrado extremo a extremo y minimizacion de "
        "datos (Threat Modeling STRIDE de la Fase 4).",
        "Alta", "Vigente", "[DOC-ASSUMPTION]",
        "Fase 4 (Threat Modeling); Originacion_API_Datacredito.pdf"),
    RegistryEntry(
        "CON-005", "datos",
        "Gobierno de dominios de datos (fuente unica de verdad)",
        "Consolidar las +200 BDs implica definir duenio por dominio y consumo "
        "via API/eventos en lugar de replicar bases; considerar migracion y "
        "CDC donde aplique (SBB-007).",
        "Media", "Vigente", "[DOC-ASSUMPTION]",
        "Fase 4 (ADR-005); Fase 3 (GAP-003)"),
    RegistryEntry(
        "CON-006", "negocio",
        "Omnicanalidad de atencion y cobranza",
        "Los canales Wolkvox/B2Chat (atencion) y SMS/WhatsApp/Email + llamada "
        "predictiva (cobranza) deben integrarse de forma consistente con el "
        "bus de eventos para evitar mensajes duplicados.",
        "Media", "Vigente", "[DOC-ASSUMPTION]",
        "Api_Integrador_Atencion_al_cliente.pdf; Llamada_predictiva.pdf"),
]

RESTRICCIONES: List[RegistryEntry] = [
    RegistryEntry(
        "RST-001", "aplicacion",
        "Preservar las reglas de negocio existentes",
        "Requisito del RFP: la modernizacion no puede alterar las reglas de "
        "negocio vigentes (RN-01..RN-04); es una restriccion dura del proyecto.",
        "Alta", "Activa", "[VERIFIED-FACT]",
        "RFP_CREDI10_2_0.pdf"),
    RegistryEntry(
        "RST-002", "negocio",
        "Continuidad operativa durante la transformacion",
        "La operacion de originacion, pagos, recaudo y cobranza no puede "
        "detenerse; la migracion debe ser incremental y reversible por ola.",
        "Alta", "Activa", "[DOC-ASSUMPTION]",
        "RFP_CREDI10_2_0.pdf; Fase 5 (olas de entrega)"),
    RegistryEntry(
        "RST-003", "integracion",
        "Integracion obligatoria con el ERP Siesa/UnoEE",
        "Siesa/UnoEE permanece como ERP; el TO-BE debe integrarse con el (via "
        "Data Services + eventos) y jamas escribir directo a su BD (ADR-002).",
        "Alta", "Activa", "[VERIFIED-FACT]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; Envio_de_RCL_y_RCR.pdf"),
    RegistryEntry(
        "RST-004", "infraestructura",
        "Ventanas de mantenimiento y conectividad Telmex",
        "Los procesos batch (p. ej. corte de cartera) y la dependencia de la "
        "VPN IPSec con Telmex imponen ventanas y restricciones de conectividad "
        "para despliegues y cortes.",
        "Media", "Activa", "[DOC-ASSUMPTION]",
        "ProcesoCorteCartera.pdf; Arquitectura_Infraestructura_AWS_Credi10.png"),
    RegistryEntry(
        "RST-005", "datos",
        "Cumplimiento en el tratamiento de datos de credito y pago",
        "El tratamiento de datos de buros (Datacredito/Inspektor) y de pagos "
        "(PayU) restringe el diseno a practicas de proteccion de datos y "
        "trazabilidad; se asume habeas data/PCI a confirmar.",
        "Alta", "Activa", "[DOC-ASSUMPTION]",
        "Originacion_API_Datacredito.pdf; LinkDePagos.pdf"),
    RegistryEntry(
        "RST-006", "seguridad",
        "Stack tecnologico objetivo acotado (.NET 8 + WSO2 + AWS)",
        "Las decisiones de arquitectura (ADR-001..006) fijan el stack objetivo "
        "(.NET 8, WSO2 API/Integration Platform, AWS, SQL Server); cualquier "
        "alternativa es recalibrable pero restringe el diseno base.",
        "Media", "Activa", "[DOC-ASSUMPTION]",
        "Fase 4 (ADR-001, ADR-004, ADR-006)"),
]

PRERREQUISITOS: List[RegistryEntry] = [
    RegistryEntry(
        "PRE-001", "integracion",
        "Especificacion del contrato del WS/Data Services de Siesa",
        "El Assessment WSO2/Studio F recuperado ([VERIFIED-FACT]) confirma el "
        "WS unico y los archivos planos, pero antes de construir el desacople "
        "se requiere la especificacion real de las operaciones del ERP Siesa "
        "(detalle hoy [EPISTEMIC-VOID]) para definir los Data Services "
        "(SBB-002).",
        "Alta", "Pendiente", "[EPISTEMIC-VOID]",
        "AMB-002; WSO2 y Studio F - Assessment Mayo2026-Final.pdf"),
    RegistryEntry(
        "PRE-002", "datos",
        "Inventario y clasificacion de las +200 bases de datos",
        "La consolidacion a fuente unica de verdad (SBB-007) requiere primero "
        "inventariar y clasificar las +200 BDs duplicadas por dominio.",
        "Alta", "Pendiente", "[VERIFIED-FACT]",
        "WSO2 y Studio F - Assessment Mayo2026-Final.pdf; Fase 3 (GAP-003)"),
    RegistryEntry(
        "PRE-003", "negocio",
        "Confirmacion de umbrales de scoring y reglas de decision",
        "El negocio debe confirmar los umbrales de APROBADO/RECHAZADO/REVISION "
        "y la regla de no-hit antes de automatizar el estudio de credito "
        "(AMB-004).",
        "Alta", "Pendiente", "[DOC-ASSUMPTION]",
        "AMB-004; Originacion_API_Datacredito.pdf"),
    RegistryEntry(
        "PRE-004", "infraestructura",
        "Cuenta AWS, VPC y conectividad Telmex habilitadas",
        "El despliegue TO-BE requiere la cuenta AWS, red (VPC/ALB/WAF) y el "
        "tunel VPN IPSec con Telmex operativos antes de la primera ola.",
        "Media", "Pendiente", "[VERIFIED-FACT]",
        "Arquitectura_Infraestructura_AWS_Credi10.png"),
    RegistryEntry(
        "PRE-005", "seguridad",
        "Definicion de requisitos de cumplimiento (habeas data / PCI)",
        "Antes del diseno de seguridad detallado se deben confirmar los "
        "requisitos de cumplimiento aplicables al tratamiento de datos de "
        "credito y pagos (AMB-005, RST-005).",
        "Media", "Pendiente", "[DOC-ASSUMPTION]",
        "AMB-005; RST-005"),
    RegistryEntry(
        "PRE-006", "aplicacion",
        "Base de pruebas de equivalencia de reglas de negocio",
        "Para preservar RN-01..RN-04 (RST-001) al migrar a .NET 8 se requiere "
        "una base de casos de prueba de equivalencia funcional del legado.",
        "Media", "Pendiente", "[DOC-ASSUMPTION]",
        "RST-001; RFP_CREDI10_2_0.pdf"),
]


REGISTRIES = [
    ("ambiguedades", "AMB", "Ambiguedades", AMBIGUEDADES,
     "Severidad", "Ambiguedades del proyecto que requieren decision o "
     "aclaracion antes de comprometer alcance."),
    ("riesgos", "RSK", "Riesgos", RIESGOS,
     "Severidad", "Riesgos del proyecto con su severidad, estado de mitigacion "
     "y trazabilidad al Hilo Dorado (GAP/SBB/ADR)."),
    ("consideraciones", "CON", "Consideraciones", CONSIDERACIONES,
     "Impacto", "Consideraciones de diseno y gobierno que condicionan el TO-BE "
     "sin ser restricciones duras."),
    ("restricciones", "RST", "Restricciones", RESTRICCIONES,
     "Severidad", "Restricciones duras del proyecto (RFP, legado, "
     "cumplimiento) que acotan el diseno."),
    ("prerrequisitos", "PRE", "Prerrequisitos", PRERREQUISITOS,
     "Prioridad", "Prerrequisitos que deben cumplirse antes de construir/"
     "desplegar cada frente."),
]


# --------------------------------------------------------------------------- #
# Helpers de render
# --------------------------------------------------------------------------- #

def _kb_total(knowledge_base) -> Optional[int]:
    if knowledge_base is None:
        return None
    try:
        return knowledge_base.total
    except Exception:
        return None


def _registry_table(entries: List[RegistryEntry], sev_header: str) -> str:
    rows = [
        f"| ID | Nivel | Titulo | Descripcion | {sev_header} | Estado | "
        "Etiqueta | Fuente |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for e in sorted(entries, key=lambda x: x.id):
        etiqueta = e.etiqueta if e.etiqueta else "-"
        rows.append(
            f"| {e.id} | {e.nivel} | {e.titulo} | {e.descripcion} | "
            f"{e.severidad} | {e.estado} | {etiqueta} | {e.fuente} |"
        )
    return "\n".join(rows)


def _registry_level_mermaid(prefix: str, entries: List[RegistryEntry]) -> str:
    """Mapa Mermaid que agrupa las entradas por nivel arquitectonico."""
    by_level: dict = {}
    for e in entries:
        by_level.setdefault(e.nivel, []).append(e.id)
    lines = ["```mermaid", "flowchart TB", f'    ROOT["{prefix} por nivel"]']
    for i, nivel in enumerate(NIVELES, start=1):
        ids = sorted(by_level.get(nivel, []))
        if not ids:
            continue
        node = f"N{i}"
        lines.append(f'    ROOT --> {node}["{nivel}: {", ".join(ids)}"]')
    lines.append("```")
    return "\n".join(lines)


def _epistemic_note() -> str:
    return (
        "> Etiquetas epistemicas: **[VERIFIED-FACT]** evidencia explicita del "
        "corpus; **[DOC-ASSUMPTION]** supuesto a validar; **[DOC-CONFLICT]** "
        "contradiccion entre fuentes; **[EPISTEMIC-VOID]** sin base documental "
        "(no se fabrica evidencia)."
    )


def _niveles_line() -> str:
    return (
        "Niveles arquitectonicos cubiertos: "
        + ", ".join(f"**{n}**" for n in NIVELES) + "."
    )


# --------------------------------------------------------------------------- #
# Registros transversales (00-registros/*.md)
# --------------------------------------------------------------------------- #

def build_registry(key: str) -> str:
    slug, prefix, titulo, entries, sev_header, intro = next(
        r for r in REGISTRIES if r[0] == key
    )
    kinds = sorted({e.etiqueta for e in entries if e.etiqueta})
    parts: List[str] = [
        f"# Registro transversal: {titulo} ({prefix}-xxx)",
        "",
        f"> {intro} Registro **transversal** del dossier TO-BE Credi10 2.0, con "
        "una entrada por fila, cada una con **ID**, **nivel arquitectonico**, "
        "**severidad/impacto**, **estado** y **etiqueta epistemica** donde "
        "aplique. Generado de forma determinista por el motor del advisory.",
        "",
        _niveles_line(),
        "",
        _epistemic_note(),
        "",
        "## Mapa por nivel arquitectonico",
        "",
        _registry_level_mermaid(titulo, entries),
        "",
        f"## Tabla de {titulo.lower()}",
        "",
        _registry_table(entries, sev_header),
        "",
        "## Resumen",
        "",
        f"| Metrica | Valor |",
        "| --- | ---: |",
        f"| Entradas registradas | {len(entries)} |",
        f"| Niveles con al menos una entrada | "
        f"{len({e.nivel for e in entries})} de {len(NIVELES)} |",
        f"| Etiquetas epistemicas presentes | "
        f"{', '.join(kinds) if kinds else 'ninguna'} |",
        "",
        f"> **Veredicto de completitud:** registro {prefix} con "
        f"{len(entries)} entradas, todas con ID + nivel + severidad + estado.",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# 01-requisitos
# --------------------------------------------------------------------------- #

def _functional_requirements_table() -> str:
    rows = [
        "| RF | Modulo | Bounded Context | Requisito funcional (desde HU) | "
        "ABBs | Fuente (KB) |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for i, m in enumerate(MODULES, start=1):
        hu = m.stories[0] if m.stories else None
        req = hu.quiero if hu else m.name
        rows.append(
            f"| RF-{i:02d} | {m.id} | {m.bounded_context} | {req} | "
            f"{', '.join(m.abbs)} | {m.source} |"
        )
    return "\n".join(rows)


def _nfr_iso25010_table() -> str:
    rows = [
        "| Caracteristica ISO 25010 | NFR TO-BE | Objetivo (indicador RFP) | "
        "SBB habilitador |",
        "| --- | --- | --- | --- |",
        "| Fiabilidad (disponibilidad) | Disponibilidad de servicios criticos | "
        "90% -> 99% (DRV-001) | SBB-001, SBB-005 |",
        "| Eficiencia de desempenio | Latencia de estudio/recaudo | 60% -> 80% "
        "(DRV-002); sin linea base instrumentada hoy [EPISTEMIC-VOID] | "
        "SBB-002, SBB-003 |",
        "| Compatibilidad | Integracion estandarizada (APIs + eventos) | "
        "Retirar archivos planos y WS unico | SBB-001, SBB-003 |",
        "| Mantenibilidad | Reglas centralizadas sin duplicar | 50% -> 100% "
        "(DRV-004) | SBB-004, SBB-007 |",
        "| Seguridad | Zero-trust, cifrado y trazabilidad | Cerrar brechas de "
        "gobernanza | SBB-001, SBB-005 |",
        "| Portabilidad | Runtime contenerizado .NET 8 | 70% -> 100% (DRV-005) "
        "| SBB-006, SBB-008 |",
    ]
    return "\n".join(rows)


def _business_rules_table() -> str:
    rows = [
        "| Regla | Descripcion | Preservacion (requisito RFP) |",
        "| --- | --- | --- |",
        "| RN-01 | El estudio encadena CrossCore -> Inspektor -> "
        "Datacredito/Dictum antes de decidir | Preservar [VERIFIED-FACT] |",
        "| RN-02 | Una solicitud rechazada en cualquier buro detiene el flujo | "
        "Preservar [VERIFIED-FACT] |",
        "| RN-03 | El desembolso genera RCL/RCR en UnoEE y se timbra con Numrot "
        "| Preservar [VERIFIED-FACT] |",
        "| RN-04 | El recaudo solo se marca aplicado tras confirmacion de PayU | "
        "Preservar [VERIFIED-FACT] |",
    ]
    return "\n".join(rows)


def _golden_thread_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    DRV["DRV-00x<br/>Drivers RFP"] --> CAP["CAP<br/>Capacidades"]\n'
        '    CAP --> GAP["GAP-001..005<br/>Gaps (Fase 3)"]\n'
        '    GAP --> REL["REL-001..004<br/>Aliviadores"]\n'
        '    REL --> ABB["ABB-001..006<br/>ABBs"]\n'
        '    ABB --> SBB["SBB-001..008<br/>SBBs (Fase 4)"]\n'
        '    SBB --> RF["RF-xx<br/>Requisitos funcionales"]\n'
        "```\n"
    )


def build_requisitos(knowledge_base=None) -> str:
    total = _kb_total(knowledge_base)
    kb_line = (
        f"La trazabilidad se apoya en la Base de Conocimiento (**{total}** "
        "documentos ingeridos sin muestreo)."
        if total is not None else
        "La trazabilidad se apoya en la Base de Conocimiento del advisory."
    )
    parts: List[str] = [
        "# 01 - Requisitos (TO-BE Credi10 2.0)",
        "",
        "> Capitulo de **requisitos** del dossier TO-BE. Deriva los requisitos "
        "funcionales de la unica fuente de verdad de modulos "
        "(`advisory-system/phases/modules.py`, MOD-01..MOD-17), define los NFR "
        "ISO 25010 ligados a los indicadores del RFP, lista las reglas de "
        "negocio a preservar y traza todo al **Hilo Dorado** "
        "(DRV -> CAP -> GAP -> REL -> ABB -> SBB). " + kb_line,
        "",
        _epistemic_note(),
        "",
        "## Trazabilidad al Hilo Dorado",
        "",
        _golden_thread_mermaid(),
        "",
        "## Requisitos funcionales por modulo",
        "",
        f"Universo completo: **{modules_mod.module_count()}** modulos "
        f"(sin muestreo), **{modules_mod.story_count()}** historias de usuario "
        "(ver `03-specs/` y el catalogo 04b).",
        "",
        _functional_requirements_table(),
        "",
        "## Requisitos no funcionales (ISO/IEC 25010)",
        "",
        _nfr_iso25010_table(),
        "",
        "## Reglas de negocio a preservar",
        "",
        "Un requisito del RFP es **preservar las reglas de negocio existentes**:",
        "",
        _business_rules_table(),
        "",
        "> **Veredicto de cobertura:** requisitos funcionales para los "
        f"{modules_mod.module_count()} modulos declarados, NFR ISO 25010 "
        "ligados a DRV-001..DRV-005 y reglas RN-01..RN-04 preservadas.",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# 02-arquitectura
# --------------------------------------------------------------------------- #

def _arch_negocio_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    CL(["Cliente / Asesor"]) --> ORIG[Originacion]\n'
        "    ORIG --> EC[Estudio de Credito]\n"
        "    EC --> DES[Desembolso + RCL/RCR]\n"
        "    DES --> REC[Recaudo PayU]\n"
        "    REC --> CAR[Corte de Cartera]\n"
        "    CAR --> COB[Cobranza multicanal]\n"
        "    COB --> REC\n"
        "```\n"
    )


def _arch_c4_container_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    GW{{API Gateway / WSO2<br/>SBB-001}}\n'
        '    subgraph DOM["Servicios de dominio .NET 8 - SBB-004"]\n'
        "        ORIG[Originacion]\n"
        "        EC[Estudio de Credito]\n"
        "        PAG[Pagos]\n"
        "        REC[Recaudo]\n"
        "        COB[Cobranza]\n"
        "    end\n"
        "    BUS[(Bus de eventos<br/>SBB-003)]\n"
        "    DS[Data Services Siesa<br/>SBB-002]\n"
        "    GW --> ORIG & EC & PAG & REC & COB\n"
        "    EC --> BUS\n"
        "    REC --> BUS\n"
        "    BUS --> DS\n"
        "    DS --> SIESA[(ERP Siesa/UnoEE)]\n"
        "```\n"
    )


def _arch_datos_erd() -> str:
    return (
        "```mermaid\n"
        "erDiagram\n"
        "    CLIENTE ||--o{ SOLICITUD : origina\n"
        "    SOLICITUD ||--|| ESTUDIO_CREDITO : evalua\n"
        "    SOLICITUD ||--o{ OBLIGACION : genera\n"
        "    OBLIGACION ||--o{ LINK_RECAUDO : cobra\n"
        "    LINK_RECAUDO ||--o{ PAGO : concilia\n"
        "    OBLIGACION ||--o{ CORTE_CARTERA : consolida\n"
        "    CLIENTE {\n"
        "        string documento PK\n"
        "    }\n"
        "    ESTUDIO_CREDITO {\n"
        "        string id_estudio PK\n"
        "        string decision\n"
        "    }\n"
        "    PAGO {\n"
        "        string id_pago PK\n"
        "        string referencia_payu\n"
        "    }\n"
        "```\n"
    )


def _arch_integracion_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    subgraph ASIS["AS-IS (a desacoplar)"]\n'
        "        WS[WS unico Siesa]\n"
        "        FLAT[Archivos planos batch]\n"
        "    end\n"
        '    subgraph TOBE["TO-BE gobernado"]\n'
        "        GW{{API Gateway SBB-001}}\n"
        "        BUS[(Bus de eventos SBB-003)]\n"
        "        DS[Data Services Siesa SBB-002]\n"
        "    end\n"
        "    WS -. reemplaza .-> DS\n"
        "    FLAT -. reemplaza .-> BUS\n"
        "    GW --> BUS --> DS --> SIESA[(ERP Siesa/UnoEE)]\n"
        "```\n"
    )


def _arch_infra_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart TB\n"
        '    subgraph AWS["AWS (VPC)"]\n'
        "        WAF[WAF] --> ALB[ALB]\n"
        "        ALB --> ECS[Contenedores .NET 8<br/>ECS/EKS - SBB-008]\n"
        "        ECS --> SQL[(SQL Server)]\n"
        "        ECS --> OBS[Observabilidad CloudWatch<br/>SBB-005]\n"
        "    end\n"
        "    TELMEX[VPN IPSec Telmex] --> AWS\n"
        "    ECS --> SIESA[(ERP Siesa/UnoEE)]\n"
        "```\n"
    )


def _arch_seguridad_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        "    USER([Cliente / Asesor]) --> GW{{API Gateway<br/>authn/authz SBB-001}}\n"
        "    GW --> SVC[Servicios de dominio .NET 8]\n"
        "    SVC --> OBS[Logging/auditoria SBB-005]\n"
        "    SVC --> ENC[Cifrado de datos sensibles]\n"
        "    ENC --> SQL[(SQL Server)]\n"
        "```\n"
    )


def _arch_levels_table() -> str:
    rows = [
        "| Nivel arquitectonico | Vista TO-BE | Elementos clave | SBB / ADR |",
        "| --- | --- | --- | --- |",
        "| Negocio | Cadena de valor credito | Originacion -> Estudio -> "
        "Desembolso -> Recaudo -> Cartera -> Cobranza | - |",
        "| Aplicacion (C4 N1-3) | Servicios de dominio tras API Gateway | "
        "WSO2 + .NET 8 por bounded context | SBB-001, SBB-004 |",
        "| Datos | ERD por bounded context + fuente unica de verdad | "
        "Consolidar +200 BDs | SBB-007, ADR-005 |",
        "| Integracion | APIs + eventos, desacople de Siesa | Data Services + "
        "bus de eventos | SBB-002, SBB-003, ADR-002 |",
        "| Infraestructura | AWS objetivo | VPC/ALB/WAF, contenedores, VPN "
        "Telmex, SQL Server | SBB-008, ADR-006 |",
        "| Seguridad | Zero-trust transversal | authn/authz, cifrado, "
        "trazabilidad STRIDE | SBB-001, SBB-005 |",
    ]
    return "\n".join(rows)


def build_arquitectura(knowledge_base=None) -> str:
    parts: List[str] = [
        "# 02 - Arquitectura TO-BE multinivel (Credi10 2.0)",
        "",
        "> Capitulo de **arquitectura** del dossier TO-BE. Presenta vistas por "
        "nivel arquitectonico (negocio, aplicacion con C4 N1-3, datos con ERD "
        "por bounded context, integracion con desacople de Siesa, "
        "infraestructura AWS objetivo y seguridad). **Reutiliza y enlaza** la "
        "Fase 4 (`../../04-diseno-to-be.md`: C4, ADR-001..006, ERD, "
        "OpenAPI/AsyncAPI) sin contradecirla; aqui se consolidan las vistas por "
        "nivel.",
        "",
        _epistemic_note(),
        "",
        _niveles_line(),
        "",
        "## Resumen por nivel arquitectonico",
        "",
        _arch_levels_table(),
        "",
        "## Nivel negocio",
        "",
        _arch_negocio_mermaid(),
        "",
        "## Nivel aplicacion (C4 contenedores)",
        "",
        "Vista de contenedores coherente con los diagramas C4 N1-3 de la "
        "Fase 4 (no se duplican; se enlazan en `../../04-diseno-to-be.md`):",
        "",
        _arch_c4_container_mermaid(),
        "",
        "## Nivel datos (ERD por bounded context)",
        "",
        _arch_datos_erd(),
        "",
        "## Nivel integracion (desacople de Siesa)",
        "",
        "El cuello de botella AS-IS (WS unico + archivos planos, GAP-001) se "
        "reemplaza por Data Services gobernados (SBB-002) y un bus de eventos "
        "(SBB-003); nunca acceso directo a la BD del ERP (ADR-002):",
        "",
        _arch_integracion_mermaid(),
        "",
        "## Nivel infraestructura (AWS objetivo)",
        "",
        _arch_infra_mermaid(),
        "",
        "## Nivel seguridad",
        "",
        _arch_seguridad_mermaid(),
        "",
        "> **Veredicto de cobertura:** seis niveles arquitectonicos con vista "
        "TO-BE, trazados a SBB-001..008 y ADR-001..006 de la Fase 4.",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# 03-specs
# --------------------------------------------------------------------------- #

def _openapi_estudio_snippet() -> str:
    return (
        "```yaml\n"
        "openapi: 3.0.3\n"
        "info:\n"
        "  title: Credi10 2.0 - Estudio de Credito\n"
        "  version: 1.0.0\n"
        "paths:\n"
        "  /estudio-credito:\n"
        "    post:\n"
        "      summary: Inicia el estudio (CrossCore -> Inspektor -> Datacredito)\n"
        "      responses:\n"
        "        '200':\n"
        "          description: Decision APROBADO/RECHAZADO/REVISION + score\n"
        "        '424':\n"
        "          description: Buro no disponible\n"
        "```\n"
    )


def _asyncapi_pago_snippet() -> str:
    return (
        "```yaml\n"
        "asyncapi: 2.6.0\n"
        "info:\n"
        "  title: Credi10 2.0 - Evento PagoAplicado\n"
        "  version: 1.0.0\n"
        "channels:\n"
        "  recaudo/pago-aplicado:\n"
        "    subscribe:\n"
        "      message:\n"
        "        name: PagoAplicado\n"
        "        payload:\n"
        "          type: object\n"
        "          properties:\n"
        "            idPago: { type: string }\n"
        "            referenciaPayU: { type: string }\n"
        "```\n"
    )


def _specs_modules_table() -> str:
    rows = [
        "| Modulo | Spec de contrato (resumen) | Tipo | Integracion | HU |",
        "| --- | --- | --- | --- | --- |",
    ]
    for m in MODULES:
        hu = ", ".join(s.id for s in m.stories)
        rows.append(
            f"| {m.id} {m.name} | {m.components} | API/evento | {m.bounded_context} "
            f"| {hu} |"
        )
    return "\n".join(rows)


def _specs_data_schema_table() -> str:
    rows = [
        "| Entidad | Atributos clave | Bounded Context |",
        "| --- | --- | --- |",
        "| CLIENTE | documento (PK), nombre | Transversal |",
        "| SOLICITUD | id_solicitud (PK), documento (FK), estado | Originacion |",
        "| ESTUDIO_CREDITO | id_estudio (PK), decision, score | Estudio de "
        "Credito |",
        "| OBLIGACION | id_obligacion (PK), saldo | Cartera |",
        "| LINK_RECAUDO | id_link (PK), monto, estado | Recaudo |",
        "| PAGO | id_pago (PK), referencia_payu | Recaudo |",
    ]
    return "\n".join(rows)


def _specs_integration_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        "    EC[Estudio de Credito] -- OpenAPI --> GW{{API Gateway}}\n"
        "    GW -- REST --> BUROS[CrossCore/Inspektor/Datacredito]\n"
        "    REC[Recaudo] -- AsyncAPI PagoAplicado --> BUS[(Bus de eventos)]\n"
        "    BUS --> DS[Data Services Siesa]\n"
        "```\n"
    )


def build_specs(knowledge_base=None) -> str:
    parts: List[str] = [
        "# 03 - Specs y contratos (TO-BE Credi10 2.0)",
        "",
        "> Capitulo de **especificaciones** del dossier TO-BE: contratos API "
        "(OpenAPI/AsyncAPI esbozados), esquemas de datos, specs por modulo y "
        "specs de integracion. Las historias BDD/Gherkin completas (happy path "
        "+ casos borde) por modulo viven en el **catalogo exhaustivo 04b** "
        "(`../../04b-catalogo-historias.md`) y se reutilizan aqui sin "
        "duplicarlas. Los contratos detallados estan en la Fase 4 "
        "(`../../04-diseno-to-be.md`).",
        "",
        _epistemic_note(),
        "",
        "## Contrato API sincrono (OpenAPI esbozado)",
        "",
        _openapi_estudio_snippet(),
        "",
        "## Contrato asincrono (AsyncAPI esbozado)",
        "",
        _asyncapi_pago_snippet(),
        "",
        "## Esquema de datos (resumen)",
        "",
        _specs_data_schema_table(),
        "",
        "## Specs por modulo (universo completo)",
        "",
        f"Cobertura: **{modules_mod.module_count()}** modulos, "
        f"**{modules_mod.story_count()}** HU con Gherkin (ver 04b).",
        "",
        _specs_modules_table(),
        "",
        "## Spec de integracion",
        "",
        _specs_integration_mermaid(),
        "",
        "> **Veredicto de cobertura:** contratos sincronos y asincronos "
        "esbozados, esquema de datos y specs para los "
        f"{modules_mod.module_count()} modulos, enlazados al catalogo 04b.",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# 04-ux
# --------------------------------------------------------------------------- #

def _ux_journey_mermaid() -> str:
    return (
        "```mermaid\n"
        "journey\n"
        "    title Customer journey - Originacion y pago\n"
        "    section Originacion\n"
        "      Enviar solicitud: 4: Cliente\n"
        "      Capturar foto documento: 3: Cliente\n"
        "      Recibir decision: 4: Cliente\n"
        "    section Pago\n"
        "      Abrir link de recaudo: 4: Cliente\n"
        "      Pagar en PayU: 5: Cliente\n"
        "      Ver saldo actualizado: 5: Cliente\n"
        "```\n"
    )


def _ux_wireflow_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        "    S1[Formulario solicitud] --> S2[Captura foto]\n"
        "    S2 --> S3[Pantalla decision]\n"
        "    S3 -- Aprobado --> S4[Oferta y aceptacion]\n"
        "    S4 --> S5[Link de recaudo PayU]\n"
        "    S3 -- Revision --> S6[Mensaje en revision]\n"
        "    S3 -- Rechazado --> S7[Mensaje de rechazo]\n"
        "```\n"
    )


def _ux_blueprint_table() -> str:
    rows = [
        "| Capa del Service Blueprint | Originacion -> Recaudo |",
        "| --- | --- |",
        "| Evidencia fisica | Formulario web, confirmacion, link de pago |",
        "| Acciones del cliente | Enviar solicitud, aceptar oferta, pagar en "
        "PayU |",
        "| Frontstage (UX) | Pantalla solicitud, decision, pago (portal B2C) |",
        "| Backstage | Orquestacion de buros, motor de reglas, RCL/RCR |",
        "| Procesos de soporte | Data Services Siesa, bus de eventos, "
        "observabilidad |",
    ]
    return "\n".join(rows)


def _ux_journeys_table() -> str:
    rows = [
        "| Journey | Canal | Modulos | Resultado esperado |",
        "| --- | --- | --- | --- |",
        "| Originacion | Asesor / web | MOD-05, MOD-11, MOD-02..04 | Solicitud "
        "decidida y trazable |",
        "| Pagos / Recaudo | PayU / link | MOD-06, MOD-08 | Pago conciliado |",
        "| B2C autoservicio | Portal B2C | MOD-09, MOD-10 | Cliente paga sin "
        "asesor |",
        "| Cobranza | SMS/WhatsApp/Email/llamada | MOD-13, MOD-14 | Promesa de "
        "pago registrada |",
    ]
    return "\n".join(rows)


def build_ux(knowledge_base=None) -> str:
    parts: List[str] = [
        "# 04 - UX y experiencia TO-BE (Credi10 2.0)",
        "",
        "> Capitulo de **UX** del dossier TO-BE: service blueprints, customer "
        "journeys y wireflows/arquitectura de informacion para los flujos de "
        "**originacion, pagos, B2C y cobranza**. Las pantallas se describen de "
        "forma Mermaid/descriptiva (no hay mockups de alta fidelidad en el "
        "corpus [EPISTEMIC-VOID]).",
        "",
        _epistemic_note(),
        "",
        "## Customer journey (originacion y pago)",
        "",
        _ux_journey_mermaid(),
        "",
        "## Wireflow / arquitectura de informacion",
        "",
        _ux_wireflow_mermaid(),
        "",
        "## Service Blueprint",
        "",
        _ux_blueprint_table(),
        "",
        "## Journeys por flujo",
        "",
        _ux_journeys_table(),
        "",
        "> **Veredicto de cobertura:** blueprint + journey + wireflow para "
        "originacion, pagos, B2C y cobranza, trazados a los modulos MOD-xx.",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# 05-pruebas
# --------------------------------------------------------------------------- #

def _test_strategy_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart TB\n"
        "    U[Unitarias] --> I[Integracion de contratos]\n"
        "    I --> E2E[End-to-end por journey]\n"
        "    E2E --> NFR[Pruebas NFR: carga, seguridad]\n"
        "    NFR --> DR[Dry-Run / Tabletop AICV-E]\n"
        "    DR --> UAT[Aceptacion de negocio]\n"
        "```\n"
    )


def _test_coverage_matrix() -> str:
    rows = [
        "| Modulo | HU | Caso happy | Caso borde (Exception Storming) | "
        "Nivel de prueba |",
        "| --- | --- | --- | --- | --- |",
    ]
    for m in MODULES:
        for s in m.stories:
            rows.append(
                f"| {m.id} | {s.id} | {s.happy.titulo} | {s.edge.titulo} | "
                "Unit + Integracion + E2E |"
            )
    return "\n".join(rows)


def _test_dryrun_table() -> str:
    rows = [
        "| Eslabon de la cadena de validacion | Artefacto |",
        "| --- | --- |",
        "| Evento | Cliente envia solicitud de credito |",
        "| Pantalla UX | Formulario -> pantalla de decision |",
        "| Regla Gherkin | Escenario happy path del estudio (HU-02..04) |",
        "| Contrato API | POST /estudio-credito |",
        "| Componente C4 | Servicio Estudio de Credito (.NET 8, SBB-004) |",
        "| Tabla/Entidad BD | ESTUDIO_CREDITO (decision, score) |",
        "| Respuesta al usuario | APROBADO/RECHAZADO/REVISION (umbral "
        "[DOC-ASSUMPTION]) |",
    ]
    return "\n".join(rows)


def _test_acceptance_table() -> str:
    rows = [
        "| Criterio de aceptacion | Fuente | Estado objetivo |",
        "| --- | --- | --- |",
        "| Cada HU cubre happy path + caso borde | 04b / modules.py | "
        "Obligatorio |",
        "| Reglas RN-01..RN-04 preservadas | RFP | Obligatorio |",
        "| Nunca acceso directo a la BD de Siesa | ADR-002 | Obligatorio |",
        "| Disponibilidad objetivo 99% en criticos | DRV-001 | Objetivo |",
    ]
    return "\n".join(rows)


def build_pruebas(knowledge_base=None) -> str:
    parts: List[str] = [
        "# 05 - Estrategia y plan de pruebas (TO-BE Credi10 2.0)",
        "",
        "> Capitulo de **pruebas** del dossier TO-BE: estrategia por niveles, "
        "matriz de cobertura derivada de las HU/Gherkin "
        "(`../../04b-catalogo-historias.md`), plan de **Dry-Run / Tabletop** "
        "(gobierno AICV-E) y criterios de aceptacion. Cada HU aporta un caso "
        "happy y al menos un caso borde (Exception Storming).",
        "",
        _epistemic_note(),
        "",
        "## Estrategia de pruebas por niveles",
        "",
        _test_strategy_mermaid(),
        "",
        "## Matriz de cobertura (HU -> casos)",
        "",
        f"Cobertura: **{modules_mod.module_count()}** modulos, "
        f"**{modules_mod.story_count()}** HU, "
        f"**{modules_mod.story_count() * 2}** escenarios (happy + borde).",
        "",
        _test_coverage_matrix(),
        "",
        "## Plan de Dry-Run / Tabletop",
        "",
        "Cadena de validacion extremo a extremo (Evento -> UX -> Gherkin -> API "
        "-> C4 -> BD -> respuesta), ejecutada por el verificador (AM):",
        "",
        _test_dryrun_table(),
        "",
        "## Criterios de aceptacion",
        "",
        _test_acceptance_table(),
        "",
        "> **Veredicto de cobertura:** estrategia + matriz para "
        f"{modules_mod.story_count()} HU + plan de Dry-Run + criterios de "
        "aceptacion trazables al RFP y a los ADR.",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# 06-insumos-estimacion
# --------------------------------------------------------------------------- #

def _estimation_breakdown_table() -> str:
    rows = [
        "| Modulo | Bounded Context | Frentes de trabajo | Talla (T-Shirt) "
        "[DOC-ASSUMPTION] | Dependencias |",
        "| --- | --- | --- | --- | --- |",
    ]
    for m in MODULES:
        rows.append(
            f"| {m.id} {m.name} | {m.bounded_context} | "
            "Dev / Data / Integracion / QA / DevOps / Cambio | M "
            f"[DOC-ASSUMPTION] | {', '.join(m.abbs)} |"
        )
    return "\n".join(rows)


def _parametric_table() -> str:
    rows = [
        "| Parametro recalibrable | Valor base [DOC-ASSUMPTION] | Nota |",
        "| --- | --- | --- |",
        "| Factor por talla S / M / L / XL | 0.5 / 1 / 2 / 4 | Multiplicador "
        "relativo, recalibrable |",
        "| Esfuerzo base por modulo (person-months) | 1.0 pm | Ancla de la "
        "tabla; ajustar con historicos |",
        "| Factor de integracion Siesa | +0.5 pm | Sobrecosto por desacople del "
        "WS/archivos planos |",
        "| Factor de migracion .NET 8 | +0.3 pm | Por obsolescencia .NET 4.8 / "
        "Core 3.1 |",
        "| Contingencia por vacios no documentales | +15% | Por mediciones "
        "ausentes (SLA/latencia, costos) y specs recuperadas aun sin ratificar "
        "1:1 [DOC-ASSUMPTION]; ya no por PDFs solo-imagen |",
    ]
    return "\n".join(rows)


def _estimation_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    MOD["Modulos MOD-01..17"] --> DESC["Descomposicion por frente"]\n'
        '    DESC --> PARAM["Tabla parametrica recalibrable"]\n'
        '    PARAM --> EST["Estimacion por modulo (Fase 5)"]\n'
        '    EST --> WAV["Olas de entrega (Fase 5)"]\n'
        "```\n"
    )


def _assumptions_table() -> str:
    rows = [
        "| ID | Supuesto de estimacion | Etiqueta |",
        "| --- | --- | --- |",
        "| SUP-01 | Todas las cifras de esfuerzo son indicativas y recalibrables "
        "| [DOC-ASSUMPTION] |",
        "| SUP-02 | El contrato real del WS de Siesa no esta en el corpus; su "
        "esfuerzo se estima con contingencia | [EPISTEMIC-VOID] |",
        "| SUP-03 | Los umbrales de scoring se confirmaran con negocio "
        "(PRE-003) | [DOC-ASSUMPTION] |",
        "| SUP-04 | La consolidacion de +200 BDs requiere inventario previo "
        "(PRE-002) | [DOC-ASSUMPTION] |",
    ]
    return "\n".join(rows)


def build_estimacion(knowledge_base=None) -> str:
    parts: List[str] = [
        "# 06 - Insumos de estimacion (TO-BE Credi10 2.0)",
        "",
        "> Capitulo de **insumos de estimacion** del dossier TO-BE: "
        "descomposicion por modulo y frente de trabajo, una **tabla parametrica "
        "recalibrable**, los supuestos [DOC-ASSUMPTION] y las dependencias. "
        "**Consolida y enlaza** la estimacion detallada de la **Fase 5** "
        "(`../../05-roadmap-estimacion-raid.md`, T-Shirt + WSJF + person-months "
        "+ olas) sin contradecirla. **Todas las cifras de esfuerzo son "
        "[DOC-ASSUMPTION]** (el corpus no trae cifras de esfuerzo reales).",
        "",
        _epistemic_note(),
        "",
        "## Mapa de insumos de estimacion",
        "",
        _estimation_mermaid(),
        "",
        "## Descomposicion por modulo",
        "",
        f"Universo completo: **{modules_mod.module_count()}** modulos (misma "
        "fuente unica que la Fase 5, `phases/modules.py`).",
        "",
        _estimation_breakdown_table(),
        "",
        "## Tabla parametrica recalibrable",
        "",
        "Todas las cifras son [DOC-ASSUMPTION] y se recalibran con historicos "
        "del equipo; no son compromisos:",
        "",
        _parametric_table(),
        "",
        "## Supuestos de estimacion",
        "",
        _assumptions_table(),
        "",
        "> **Veredicto de cobertura:** descomposicion de los "
        f"{modules_mod.module_count()} modulos + tabla parametrica recalibrable "
        "+ supuestos, todo enlazado a la Fase 5; cifras [DOC-ASSUMPTION].",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# README del dossier
# --------------------------------------------------------------------------- #

def _structure_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart TB\n"
        '    ROOT["to-be/ (dossier del proyecto)"]\n'
        '    ROOT --> R00["00-registros/<br/>ambiguedades, riesgos,<br/>'
        'consideraciones, restricciones, prerrequisitos"]\n'
        '    ROOT --> R01["01-requisitos/"]\n'
        '    ROOT --> R02["02-arquitectura/"]\n'
        '    ROOT --> R03["03-specs/"]\n'
        '    ROOT --> R04["04-ux/"]\n'
        '    ROOT --> R05["05-pruebas/"]\n'
        '    ROOT --> R06["06-insumos-estimacion/"]\n'
        "```\n"
    )


def _structure_table() -> str:
    rows = [
        "| Etapa SDLC | Carpeta | Contenido |",
        "| --- | --- | --- |",
        f"| Registros transversales | `{REGISTROS_DIR}/` | ambiguedades, "
        "riesgos, consideraciones, restricciones, prerrequisitos (todos los "
        "niveles) |",
        f"| Requisitos | `{STAGE_DIRS['requisitos']}/` | RF por modulo + NFR "
        "ISO 25010 + reglas de negocio + trazabilidad |",
        f"| Arquitectura | `{STAGE_DIRS['arquitectura']}/` | vistas TO-BE por "
        "nivel (negocio/aplicacion/datos/integracion/infra/seguridad) |",
        f"| Specs | `{STAGE_DIRS['specs']}/` | contratos API/eventos, esquemas "
        "de datos, specs por modulo |",
        f"| UX | `{STAGE_DIRS['ux']}/` | blueprints, journeys, wireflows |",
        f"| Pruebas | `{STAGE_DIRS['pruebas']}/` | estrategia, matriz, "
        "Dry-Run, aceptacion |",
        f"| Insumos de estimacion | `{STAGE_DIRS['estimacion']}/` | "
        "descomposicion + tabla parametrica + supuestos |",
    ]
    return "\n".join(rows)


def _registries_summary_table() -> str:
    rows = [
        "| Registro | Archivo | Entradas | Niveles cubiertos |",
        "| --- | --- | --- | --- |",
    ]
    for slug, prefix, titulo, entries, _sev, _intro in REGISTRIES:
        niveles = len({e.nivel for e in entries})
        rows.append(
            f"| {titulo} | `{REGISTROS_DIR}/{slug}.md` | {len(entries)} | "
            f"{niveles} de {len(NIVELES)} |"
        )
    return "\n".join(rows)


def build_readme(knowledge_base=None) -> str:
    total = _kb_total(knowledge_base)
    kb_line = (
        f"Fundamentado en la Base de Conocimiento (**{total}** documentos del "
        "corpus, sin muestreo)."
        if total is not None else
        "Fundamentado en la Base de Conocimiento del advisory."
    )
    n_registros = sum(len(r[3]) for r in REGISTRIES)
    parts: List[str] = [
        "# Dossier de proyecto TO-BE - Credi10 2.0",
        "",
        "> **Dossier TO-BE** generado de forma **determinista** por el motor del "
        "advisory (`advisory-system/phases/dossier.py`), organizado con **una "
        "subcarpeta por etapa/practica del SDLC** mas **registros "
        "transversales** del proyecto en todos los niveles arquitectonicos. "
        "No es un documento escrito a mano: se regenera con el quickstart. "
        + kb_line,
        "",
        "> **Regenerar el dossier (parte de `--phase all`):**",
        ">",
        "> ```bash",
        "> python3 advisory-system/quickstart.py --phase all",
        "> ```",
        "",
        "El dossier reutiliza las unicas fuentes de verdad del motor "
        "(`phases/modules.py` MOD-01..MOD-17, `phase4.py` SBB-001..008, "
        "`phase3.py` GAP/REL/ABB y los indicadores del RFP), de modo que no "
        "duplica contenido sino que lo consolida por etapa del SDLC.",
        "",
        _epistemic_note(),
        "",
        "## Estructura por etapa del SDLC",
        "",
        _structure_mermaid(),
        "",
        _structure_table(),
        "",
        "## Registros transversales (todos los niveles arquitectonicos)",
        "",
        _niveles_line(),
        "",
        _registries_summary_table(),
        "",
        "## Capitulos del dossier",
        "",
        f"- [`{STAGE_DIRS['requisitos']}/requisitos.md`]"
        f"({STAGE_DIRS['requisitos']}/requisitos.md)",
        f"- [`{STAGE_DIRS['arquitectura']}/arquitectura.md`]"
        f"({STAGE_DIRS['arquitectura']}/arquitectura.md)",
        f"- [`{STAGE_DIRS['specs']}/specs.md`]({STAGE_DIRS['specs']}/specs.md)",
        f"- [`{STAGE_DIRS['ux']}/ux.md`]({STAGE_DIRS['ux']}/ux.md)",
        f"- [`{STAGE_DIRS['pruebas']}/pruebas.md`]"
        f"({STAGE_DIRS['pruebas']}/pruebas.md)",
        f"- [`{STAGE_DIRS['estimacion']}/insumos-estimacion.md`]"
        f"({STAGE_DIRS['estimacion']}/insumos-estimacion.md)",
        "",
        "## Relacion con los informes por fase",
        "",
        "El dossier NO reemplaza los informes por fase "
        "(`../00..06-*.md` y `../04b-catalogo-historias.md`): los consolida en "
        "una vista orientada a **ejecutar el proyecto** por etapa del SDLC y "
        "enlaza a ellos para el detalle (C4/ADR/ERD, Gherkin, estimacion).",
        "",
        f"> **Veredicto QG-dossier:** GO - dossier con 6 etapas del SDLC + "
        f"registros transversales ({n_registros} entradas) en los "
        f"{len(NIVELES)} niveles arquitectonicos, generado deterministamente.",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# Escritura del arbol del dossier
# --------------------------------------------------------------------------- #

def write(out_root: str, knowledge_base=None) -> List[str]:
    """Escribe el dossier TO-BE bajo ``<out_root>/to-be/`` y devuelve los paths.

    Crea las subcarpetas (una por etapa del SDLC + ``00-registros/``), escribe
    cada capitulo y cada registro, y el ``README.md`` del dossier. Idempotente
    y byte-identico entre corridas (``os.makedirs(..., exist_ok=True)``,
    contenido estatico ordenado). Devuelve la lista de paths escritos, ordenada.
    """
    base = os.path.join(out_root, DOSSIER_DIRNAME)
    os.makedirs(base, exist_ok=True)
    os.makedirs(os.path.join(base, REGISTROS_DIR), exist_ok=True)
    for d in STAGE_DIRS.values():
        os.makedirs(os.path.join(base, d), exist_ok=True)

    written: List[str] = []

    def _emit(relpath: str, body: str) -> None:
        path = os.path.join(base, relpath)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        written.append(path)

    # README del dossier.
    _emit("README.md", build_readme(knowledge_base))

    # Registros transversales.
    for slug, _prefix, _titulo, _entries, _sev, _intro in REGISTRIES:
        _emit(os.path.join(REGISTROS_DIR, f"{slug}.md"), build_registry(slug))

    # Capitulos por etapa del SDLC.
    _emit(os.path.join(STAGE_DIRS["requisitos"], "requisitos.md"),
          build_requisitos(knowledge_base))
    _emit(os.path.join(STAGE_DIRS["arquitectura"], "arquitectura.md"),
          build_arquitectura(knowledge_base))
    _emit(os.path.join(STAGE_DIRS["specs"], "specs.md"),
          build_specs(knowledge_base))
    _emit(os.path.join(STAGE_DIRS["ux"], "ux.md"),
          build_ux(knowledge_base))
    _emit(os.path.join(STAGE_DIRS["pruebas"], "pruebas.md"),
          build_pruebas(knowledge_base))
    _emit(os.path.join(STAGE_DIRS["estimacion"], "insumos-estimacion.md"),
          build_estimacion(knowledge_base))

    return sorted(written)

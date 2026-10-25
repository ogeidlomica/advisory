"""Informe Tecnico narrativo multinivel - Credi10 2.0 (FEAT-004, task three-reports).

Generador DETERMINISTA, stdlib-only, del **tercer informe** del engagement: el
**informe tecnico** rediseñado a una estructura **multinivel y narrativa** bajo
``advisory-credi10-2.0/3-informe-tecnico/``.

Estructura (gobernada por el skill ``technical-narrative-multilevel``):

  * ``README.md``                 indice navegable + hilo narrativo/storytelling
    que conecta Fase 0 -> 6 y explica como el advisory habilita una estimacion
    lo mas acertada posible; Mermaid del flujo de fases y del Hilo Dorado.
  * UNA SUBCARPETA POR FASE (las 7 fases Zero-Drift en orden):
      - ``fase-0-higiene-epistemica/``
      - ``fase-1-contexto-as-is/``
      - ``fase-2-estado-del-arte/``
      - ``fase-3-gaps-y-viabilizacion/``
      - ``fase-4-diseno-to-be/``
      - ``fase-5-roadmap-estimacion-raid/``
      - ``fase-6-caso-de-negocio/``
  * VARIOS ARCHIVOS POR TEMA (nivel 2) dentro de cada fase, cada uno con
    jerarquia interna H1 (tema) -> H2 (subtema) -> H3 (sub-subtema) y, sobre
    todo, **NARRATIVA/ANALISIS sustancial en prosa** (regla dura del skill): no
    solo tablas y Mermaid, sino interpretacion de los hallazgos y sus
    implicaciones para la **estimacion**, la **estrategia de implementacion** y
    los **riesgos**.

Reutiliza (NO duplica) las unicas fuentes de verdad del motor:
``phases.phase0..phase6`` (datos estructurados + tablas/diagramas),
``phases.modules.MODULES`` y ``phases.dossier`` (vista de ejecucion TO-BE). El
informe tecnico **reorganiza y enriquece** los informes planos por fase
(``00..06`` + ``04b``), que se conservan como vista compacta canonica de cada
fase; esta carpeta es la **vista multinivel navegable** que los integra con
narrativa. El **dossier TO-BE** (``to-be/``) se **enlaza** inequivocamente desde
el indice como la vista orientada a ejecucion, sin duplicar su arbol.

Determinismo: todo el contenido deriva de datos estaticos ordenados; sin
aleatoriedad ni timestamps; ``os.makedirs(..., exist_ok=True)``. Una segunda
corrida de ``--phase all`` deja el arbol byte-identico.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, List, Optional

from phases import phase0, phase1, phase2, phase3
from phases import phase4
from phases import phase5
from phases import phase6
from phases import modules as modules_mod
from phases.modules import MODULES
from phases import requirements_traceability
from phases import extraction_architecture


# --------------------------------------------------------------------------- #
# Constantes de estructura (una subcarpeta por fase, en orden Zero-Drift).
# --------------------------------------------------------------------------- #

TECH_REPORT_DIRNAME = "3-informe-tecnico"

# (slug de carpeta, titulo legible, informe plano de respaldo)
PHASE_DIRS: List[tuple] = [
    ("fase-0-higiene-epistemica", "Fase 0 - Higiene Epistemica",
     "../../00-higiene-epistemica.md"),
    ("fase-1-contexto-as-is", "Fase 1 - Contexto AS-IS",
     "../../01-contexto-as-is.md"),
    ("fase-2-estado-del-arte", "Fase 2 - Estado del Arte",
     "../../02-estado-del-arte.md"),
    ("fase-3-gaps-y-viabilizacion", "Fase 3 + 3.5 - Gaps y Viabilizacion",
     "../../03-gaps-y-viabilizacion.md"),
    ("fase-4-diseno-to-be", "Fase 4 - Diseno TO-BE",
     "../../04-diseno-to-be.md"),
    ("fase-5-roadmap-estimacion-raid", "Fase 5 - Roadmap, Estimacion y RAID",
     "../../05-roadmap-estimacion-raid.md"),
    ("fase-6-caso-de-negocio", "Fase 6 - Caso de Negocio",
     "../../06-caso-de-negocio.md"),
]


# --------------------------------------------------------------------------- #
# Helpers de render compartidos.
# --------------------------------------------------------------------------- #

def _epistemic_note() -> str:
    return (
        "> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita "
        "del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; "
        "**[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base "
        "documental (no se fabrica evidencia)."
    )


def _golden_thread_line() -> str:
    return (
        "> **Hilo Dorado:** la trazabilidad end-to-end encadena "
        "Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> "
        "Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que "
        "cada decision tecnica de este informe es trazable hasta un indicador "
        "de retorno del RFP."
    )


def _kb_total(knowledge_base) -> Optional[int]:
    if knowledge_base is None:
        return None
    try:
        return knowledge_base.total
    except Exception:
        return None


@dataclass(frozen=True)
class Theme:
    """Un tema (archivo nivel 2) dentro de una fase."""
    slug: str          # nombre de archivo sin extension
    title: str         # titulo H1 del archivo
    builder: Callable[[dict], str]  # recibe ctx dict -> markdown


# El cuerpo de cada tema se arma con una estructura comun: encabezado del tema
# (H1), nota epistemica + hilo dorado, y luego secciones H2/H3 con narrativa
# sustancial intercalada con las tablas/diagramas reutilizados de las fases.

def _theme_header(title: str, phase_title: str, backing: str,
                  lead_prose: List[str]) -> List[str]:
    """Encabezado estandar de un archivo de tema: H1 + contexto + narrativa."""
    parts: List[str] = [
        f"# {title}",
        "",
        f"> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de "
        f"**{phase_title}**. Vista narrativa que reorganiza y **enriquece** el "
        f"informe plano de respaldo ([vista compacta de la fase]({backing})); "
        "aqui el foco es la **interpretacion** de los hallazgos y sus "
        "implicaciones para la **estimacion**, la **estrategia de "
        "implementacion** y los **riesgos**.",
        "",
        _epistemic_note(),
        "",
        _golden_thread_line(),
        "",
        "## Que estamos mirando y por que importa",
        "",
    ]
    parts.extend(lead_prose)
    parts.append("")
    return parts


def _closing(estimation: List[str], strategy: List[str],
             risks: List[str]) -> List[str]:
    """Cierre estandar: tres H2 de analisis obligatorio (narrativa densa)."""
    parts: List[str] = [
        "## Implicaciones para la estimacion",
        "",
    ]
    parts.extend(estimation)
    parts += [
        "",
        "## Implicaciones para la estrategia de implementacion",
        "",
    ]
    parts.extend(strategy)
    parts += [
        "",
        "## Riesgos e incertidumbre",
        "",
    ]
    parts.extend(risks)
    parts.append("")
    return parts


def _emit(parts: List[str]) -> str:
    return "\n".join(parts) + "\n"


# =========================================================================== #
# FASE 0 - Higiene Epistemica
# =========================================================================== #

_P0 = "Fase 0 - Higiene Epistemica"
_P0B = "../../00-higiene-epistemica.md"


def _t_f0_corpus(ctx) -> str:
    total = _kb_total(ctx.get("knowledge_base"))
    total_txt = (f"**{total}** documentos" if total is not None
                 else "el corpus completo")
    parts = _theme_header(
        "Corpus, trazabilidad y cobertura de evidencia", _P0, _P0B,
        [
            "Antes de analizar nada, el advisory establece la **higiene "
            "epistemica**: que sabemos, con que evidencia y con que grado de "
            f"confianza. Se ingirio {total_txt} (RFP, assessment WSO2/Studio F "
            "y los tres diagramas de arquitectura) de forma COMPLETA y sin "
            "muestreo, y cada afirmacion que entra al analisis queda anclada a "
            "su documento fuente con su huella `sha256`. Esta disciplina no es "
            "burocracia: es el cimiento de una estimacion defendible. Un "
            "advisory que no distingue hecho de supuesto termina estimando "
            "sobre arena, y es exactamente ese riesgo el que esta fase elimina "
            "antes de que cueste caro.",
            "",
            "La consecuencia practica es que **la calidad de la evidencia se "
            "convierte en un parametro de la estimacion**: los frentes "
            "sustentados por evidencia fuerte se pueden tallar con confianza, "
            "mientras que los frentes sustentados por PDFs de proceso que son "
            "mayormente imagen arrastran una contingencia explicita. Mirar el "
            "corpus con honestidad es, por tanto, el primer acto de gestion de "
            "riesgo del proyecto.",
        ])
    parts += [
        "## Inventario y clasificacion epistemica",
        "",
        "El inventario de evidencia y la clasificacion de afirmaciones con las "
        "cuatro etiquetas (verificado / supuesto / conflicto / vacio) es la "
        "foto cruda de lo que el corpus permite afirmar:",
        "",
        phase0._epistemic_table(),
        "",
        "### Lectura analitica de la clasificacion",
        "",
        "La tabla cuenta una historia: el **stack tecnologico y la topologia** "
        "(componentes .NET, bases SQL Server, infraestructura AWS, "
        "integraciones de contexto) estan bien soportados por los diagramas y "
        "se etiquetan [VERIFIED-FACT], mientras que casi todo lo **cuantitativo "
        "de negocio** (lineas base de disponibilidad, costos, volumetria de "
        "integraciones) cae en [EPISTEMIC-VOID]. Esa asimetria es decisiva: "
        "podemos estimar el **esfuerzo de construccion** con relativa "
        "confianza, pero NO podemos todavia comprometer el **retorno economico** "
        "sin cerrar los vacios. La estimacion honesta separa esas dos cosas.",
        "",
        "## Supuestos y vacios que marcan el ritmo del proyecto",
        "",
        "Los vacios y supuestos no se ocultan: se vuelven una **agenda de "
        "elicitacion** con responsable asignado. Cada pregunta abierta que no "
        "se cierra a tiempo es una fuente potencial de retrabajo y, por tanto, "
        "de desfase de cronograma.",
        "",
        phase0._elicitation_agenda(),
    ]
    parts += _closing(
        estimation=[
            "La higiene epistemica fija el **nivel de confianza** de cada cifra "
            "aguas abajo. Donde la evidencia es fuerte, la talla T-Shirt se "
            "puede comprometer; donde hay [EPISTEMIC-VOID] (p. ej. la linea "
            "base del 90% de disponibilidad o el contrato real del Web Service "
            "de Siesa), la estimacion carga una **contingencia explicita** y se "
            "marca [DOC-ASSUMPTION]. Sin esta fase la estimacion pareceria mas "
            "precisa de lo que realmente es, que es el peor error posible.",
        ],
        strategy=[
            "La estrategia de implementacion arranca por **cerrar deltas**: las "
            "preguntas de la agenda de elicitacion (DEL-01..DEL-06) deben "
            "resolverse en el arranque, porque condicionan el alcance real. En "
            "particular, el conflicto de alcance Studio F vs. Credi10 (DEL-03) "
            "define cuanto del universo entra en el proyecto y, por tanto, el "
            "tamanio de todas las olas.",
        ],
        risks=[
            "El riesgo dominante de esta fase es el **riesgo de alcance**: si el "
            "conflicto +150 apps / +200 BDs (nivel grupo) vs. ~20 componentes "
            "(Credi10) no se resuelve, cualquier estimacion puede desviarse por "
            "un factor grande. Se mitiga tratando el delta como prerrequisito "
            "duro antes de comprometer fechas. [DOC-CONFLICT]",
        ])
    return _emit(parts)


def _t_f0_grafo(ctx) -> str:
    parts = _theme_header(
        "Grafo de conceptos y modelo mental del ecosistema", _P0, _P0B,
        [
            "El grafo preliminar de conceptos traduce la evidencia dispersa en "
            "un **modelo mental compartido** del ecosistema Credi10: la "
            "aplicacion nucleo .NET, sus integradores (CrossCore, Inspektor, "
            "Datacredito), los workers, las bases de datos y las integraciones "
            "externas. Este mapa es el lenguaje comun que todas las fases "
            "siguientes usan para no 'derivar' (zero-drift) hacia "
            "interpretaciones divergentes.",
            "",
            "Importa para la estimacion porque revela de un vistazo **donde se "
            "concentra el acoplamiento**: el nodo ERP Siesa/UnoEE y los "
            "integradores de buros son centros de gravedad que atraen esfuerzo "
            "e incertidumbre. Verlos temprano permite secuenciar el trabajo "
            "para atacar primero esos cuellos de botella.",
        ])
    parts += [
        "## Mapa del ecosistema (grafo preliminar)",
        "",
        phase0._concept_graph(),
        "",
        "### Que nos dice el grafo",
        "",
        "El grafo evidencia una **arquitectura centrada en un nucleo .NET** del "
        "que cuelgan integradores y workers, con el ERP Siesa y los buros como "
        "dependencias externas criticas. No hay una capa de integracion "
        "gobernada: cada flecha es una integracion punto a punto. Esa topologia "
        "es precisamente la que la Fase 3 convertira en gaps y la Fase 4 en "
        "building blocks de solucion.",
        "",
        "### Centros de gravedad del ecosistema",
        "",
        "| Nodo | Rol en el ecosistema | Por que concentra esfuerzo/riesgo |",
        "| --- | --- | --- |",
        "| Nucleo Credi10 .NET | Aplicacion central | Orquesta casi todo; su "
        "modernizacion toca muchos flujos |",
        "| ERP Siesa / UnoEE | Sistema de registro | Punto de mayor "
        "acoplamiento (WS unico + BD directa) |",
        "| Integradores de buros | CrossCore/Inspektor/Datacredito | "
        "Integracion sincrona critica del estudio de credito |",
        "| Bases de datos SQL Server | Persistencia | Dispersion/duplicacion a "
        "nivel grupo (consolidacion pendiente) |",
    ]
    parts += _closing(
        estimation=[
            "El grado de acoplamiento visible en el grafo es un **predictor de "
            "esfuerzo**: cuantas mas flechas convergen en un nodo (Siesa, "
            "buros), mayor el costo de desacoplarlo con seguridad. El modelo "
            "mental permite anticipar que MOD-16 (integracion Siesa) sera el "
            "modulo mas pesado, algo que la Fase 5 confirma con talla XL.",
        ],
        strategy=[
            "La estrategia se ordena alrededor de los centros de gravedad del "
            "grafo: primero una capa de integracion gobernada y el desacople de "
            "Siesa, luego los dominios que dependen de ella. El grafo justifica "
            "por que los enablers van al inicio del roadmap.",
        ],
        risks=[
            "El riesgo es subestimar el efecto domino de un nodo central: tocar "
            "Siesa sin un contrato claro puede propagar fallos a originacion, "
            "pagos y cartera. El grafo hace ese riesgo visible y, por tanto, "
            "gestionable. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


# =========================================================================== #
# FASE 1 - Contexto AS-IS
# =========================================================================== #

_P1 = "Fase 1 - Contexto AS-IS"
_P1B = "../../01-contexto-as-is.md"


def _t_f1_negocio(ctx) -> str:
    parts = _theme_header(
        "Contexto de negocio: drivers y capacidades", _P1, _P1B,
        [
            "El contexto de negocio ancla todo el advisory en los **cinco "
            "indicadores de retorno del RFP** (disponibilidad 90% -> 99%, "
            "eficiencia 60% -> 80%, costo de infraestructura 80% -> 80%, "
            "evolucion/escalamiento 50% -> 100% y licenciamiento 70% -> 100%). "
            "Estos drivers no son adorno: son los criterios contra los que se "
            "juzgara el exito del proyecto y, por tanto, el norte que ordena la "
            "priorizacion. Cada capacidad de negocio (originacion, desembolso, "
            "pagos, cartera, cobranza, canales, integracion) se cuelga de un "
            "driver, de modo que el esfuerzo tecnico siempre responde a un "
            "'para que' de negocio.",
            "",
            "Entender esta jerarquia es lo que permite estimar con criterio: no "
            "todas las capacidades valen lo mismo, y el valor de negocio de "
            "cada una (via su driver) es el numerador del WSJF que la Fase 5 "
            "usa para secuenciar las olas.",
        ])
    parts += [
        "## Drivers estrategicos (indicadores del RFP)",
        "",
        phase1._drivers_table(),
        "",
        "### Interpretacion de los drivers",
        "",
        "Dos drivers son de **continuidad** (disponibilidad y eficiencia) y "
        "pesan sobre la operacion diaria; dos son de **evolucion** "
        "(escalamiento y licenciamiento) y pesan sobre la sostenibilidad; uno "
        "es de **disciplina de costo**. La estimacion debe equilibrar ambos "
        "mundos: entregar continuidad temprano (para capturar valor rapido) sin "
        "hipotecar la evolucion. El indicador de costo 80% -> 80% es revelador: "
        "no se pide ahorrar, se pide **no degradar el costo al escalar**, lo "
        "que empuja hacia practicas FinOps desde el diseno.",
        "",
        "## Mapa de capacidades y arbol de motivadores",
        "",
        phase1._capability_map(),
        "",
        phase1._capabilities_table(),
        "",
        phase1._motivators_tree(),
    ]
    parts += _closing(
        estimation=[
            "El valor de negocio por capacidad (heredado del driver) alimenta "
            "directamente la priorizacion WSJF de la Fase 5. Capacidades "
            "ligadas a disponibilidad (DRV-001) y eficiencia (DRV-002) obtienen "
            "mayor Cost of Delay y, por tanto, se estiman y planifican primero.",
        ],
        strategy=[
            "La estrategia entrega valor por **capacidad de negocio**, no por "
            "componente tecnico aislado: cada ola cierra un arco de capacidad "
            "(p. ej. originacion + estudio de credito) para que el negocio "
            "perciba resultado, en linea con el principio de continuidad "
            "operativa del RFP.",
        ],
        risks=[
            "El riesgo es optimizar un driver a costa de otro (p. ej. escalar "
            "sin control de costo, violando DRV-003). La trazabilidad "
            "capacidad -> driver mantiene la tension visible y evita decisiones "
            "locales que rompan un indicador global. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


def _t_f1_procesos(ctx) -> str:
    parts = _theme_header(
        "Procesos de negocio AS-IS (BPMN) y metricas base", _P1, _P1B,
        [
            "El flujo operativo real de Credi10 va de la **originacion** al "
            "**estudio de credito** (CrossCore -> Inspektor -> "
            "Datacredito/Dictum), luego **desembolso** (RCL/RCR en UnoEE, "
            "timbrado Numrot), **pagos/recaudo** (Link de Recaudo -> PayU), "
            "**corte de cartera** y **cobranza omnicanal**. Mapear este proceso "
            "extremo a extremo es indispensable porque **el proceso es la "
            "unidad de valor**: la estimacion y el roadmap se organizan "
            "alrededor de tramos de este flujo, no de componentes sueltos.",
            "",
            "La narrativa clave es que el proceso esta encadenado: una "
            "interrupcion en el estudio de credito paraliza el desembolso y, "
            "aguas abajo, el recaudo. Esa dependencia secuencial explica por "
            "que la disponibilidad (DRV-001) es tan critica y por que el "
            "desacople de las integraciones es el enabler que desbloquea todo.",
        ])
    parts += [
        "## Proceso BPMN AS-IS (extremo a extremo)",
        "",
        phase1._value_chain_bpmn(),
        "",
        "### Lectura del flujo",
        "",
        "El diagrama muestra un proceso lineal con una bifurcacion de decision "
        "(aprobado/rechazado) y un ciclo de cobranza. Los puntos de mayor "
        "riesgo operativo son las **llamadas sincronas a buros** (si uno cae, "
        "se detiene el estudio) y la **escritura a Siesa** en el desembolso. "
        "Ambos se convierten en requisitos no funcionales de resiliencia en el "
        "TO-BE.",
        "",
        "## Metricas baseline AS-IS",
        "",
        phase1._baseline_metrics_table(),
        "",
        "### Que falta medir",
        "",
        "Las metricas confirman los objetivos del RFP pero exponen un vacio: la "
        "**latencia del estudio de credito no esta instrumentada** "
        "[EPISTEMIC-VOID]. No se puede mejorar lo que no se mide, asi que "
        "instrumentar observabilidad es un prerrequisito, no un lujo.",
    ]
    parts += _closing(
        estimation=[
            "Estimar por tramos del proceso (originacion, estudio, desembolso, "
            "recaudo, cartera, cobranza) da una descomposicion natural que se "
            "mapea a los modulos MOD-xx de la Fase 5. La ausencia de metricas "
            "de latencia obliga a estimar algunos NFR con [DOC-ASSUMPTION] y "
            "contingencia.",
        ],
        strategy=[
            "La estrategia respeta el orden del proceso pero inserta primero los "
            "enablers transversales (observabilidad, integracion gobernada) "
            "para no reconstruir cada tramo sobre bases inestables.",
        ],
        risks=[
            "El riesgo operativo es la **propagacion de fallos** por el "
            "encadenamiento sincrono del proceso. El TO-BE lo mitiga con "
            "eventos y resiliencia; mientras tanto, cualquier ola debe preservar "
            "la continuidad del flujo (restriccion del RFP).",
        ])
    return _emit(parts)


def _t_f1_ecosistema(ctx) -> str:
    parts = _theme_header(
        "Ecosistema tecnologico y de datos AS-IS", _P1, _P1B,
        [
            "El inventario tecnologico y de datos es la **radiografia del "
            "terreno** sobre el que se construira. Credi10 corre sobre .NET "
            "Framework 4.8 e IIS, con integradores en .NET, Link de Recaudo en "
            ".NET Core 3.1, workers mixtos y un canal B2C sobre Node.js/React y "
            "Wordpress/XAMPP. Los datos viven en SQL Server 2019 Enterprise y "
            "MariaDB. Conocer cada pieza con precision es lo que convierte una "
            "estimacion en algo mas que una corazonada.",
            "",
            "La lectura narrativa es que conviven **dos generaciones "
            "tecnologicas**: componentes modernos (.NET 8 en algunos workers) "
            "junto a marcos fuera de soporte (.NET 4.8, .NET Core 3.1, "
            "Wordpress). Esa heterogeneidad encarece el mantenimiento y es el "
            "corazon del driver de evolucion (DRV-004) y licenciamiento "
            "(DRV-005).",
        ])
    parts += [
        "## Inventario tecnologico",
        "",
        phase1._tech_inventory_table(),
        "",
        "## Inventario de datos",
        "",
        phase1._data_inventory_table(),
        "",
        "### Lo que implica el inventario de datos",
        "",
        "La dispersion de bases de datos (y, a nivel grupo, las +200 BDs "
        "duplicadas) anticipa un frente de **consolidacion de datos** que la "
        "Fase 4 resuelve con una fuente unica de verdad por dominio. Es uno de "
        "los frentes de mayor incertidumbre porque el corpus no detalla el "
        "esquema real de cada base.",
    ]
    parts += _closing(
        estimation=[
            "El inventario permite tallar el esfuerzo de **migracion de "
            "runtime** (cuantos componentes salen de .NET 4.8 / Core 3.1) y de "
            "**consolidacion de datos**. Ambos frentes se marcan con factores "
            "de acople legado en la tabla parametrica de la Fase 5.",
        ],
        strategy=[
            "La estrategia modera el riesgo migrando por dominio (no big-bang) y "
            "retirando primero los componentes fuera de soporte, que son los de "
            "mayor riesgo de seguridad y licenciamiento.",
        ],
        risks=[
            "El riesgo es la **deuda tecnica oculta**: esquemas de datos no "
            "documentados y dependencias implicitas entre componentes legados. "
            "Se mitiga con un inventario y clasificacion previos como "
            "prerrequisito. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


def _t_f1_deuda(ctx) -> str:
    parts = _theme_header(
        "Deuda tecnica y riesgos del AS-IS", _P1, _P1B,
        [
            "La deuda tecnica del AS-IS no es una lista de quejas: es el "
            "**motor del caso de negocio**. Cada item de deuda (runtime "
            "obsoleto, lectura directa a la BD del ERP, Wordpress en "
            "produccion, integraciones dispersas, +200 BDs duplicadas) se "
            "traduce mas adelante en un gap, un reliever y un bloque de "
            "solucion. Interpretar la deuda es, en realidad, dimensionar el "
            "trabajo de modernizacion.",
            "",
            "El hilo narrativo con la fase anterior es directo: la higiene "
            "epistemica verifico estas practicas de alto riesgo como hechos "
            "[VERIFIED-FACT]; aqui las ordenamos por impacto en los drivers "
            "para que la priorizacion sea defendible.",
        ])
    parts += [
        "## Catalogo de deuda tecnica",
        "",
        phase1._tech_debt_table(),
        "",
        "### De la deuda a la decision",
        "",
        "La deuda de **acceso directo a la BD del ERP Siesa** (DT-04) es la mas "
        "peligrosa porque combina alto riesgo de integridad con alto "
        "acoplamiento; por eso el TO-BE la prohibe explicitamente (ADR-002). La "
        "obsolescencia de runtime (DT-01, DT-02) es la mas extensa en esfuerzo "
        "porque toca muchos componentes. Esta distincion riesgo vs. esfuerzo es "
        "la que permite secuenciar: primero lo peligroso, luego lo extenso.",
    ]
    parts += _closing(
        estimation=[
            "Cada item de deuda se convierte en un multiplicador de esfuerzo en "
            "la estimacion por modulo (factor de acople legado = 1,20 en la "
            "tabla parametrica de la Fase 5). La deuda es, literalmente, un "
            "parametro de la ecuacion de estimacion.",
        ],
        strategy=[
            "La estrategia prioriza por **riesgo x impacto en drivers**: las "
            "practicas de alto riesgo (BD directa, Wordpress en produccion) se "
            "atacan en las primeras olas aunque su esfuerzo sea moderado, "
            "porque su costo de inaccion es alto.",
        ],
        risks=[
            "El meta-riesgo es que la deuda tecnica crezca mas rapido de lo que "
            "se paga. Por eso el roadmap intercala modernizacion con entrega de "
            "valor y no la pospone al final.",
        ])
    return _emit(parts)


# =========================================================================== #
# FASE 2 - Estado del Arte
# =========================================================================== #

_P2 = "Fase 2 - Estado del Arte"
_P2B = "../../02-estado-del-arte.md"


def _t_f2_benchmarks(ctx) -> str:
    parts = _theme_header(
        "Benchmarks de industria y comparativo AS-IS", _P2, _P2B,
        [
            "El estado del arte conecta la realidad de Credi10 con los "
            "**patrones de referencia** del credito de consumo y fintech: "
            "integracion API-led con gestion centralizada de APIs (eco directo "
            "de la recomendacion del assessment WSO2), arquitectura "
            "event-driven, cloud-native, observabilidad/SRE, zero-trust y "
            "automatizacion/IA. El valor de esta fase es que **evita reinventar "
            "la rueda**: cada gap se medira contra una practica reconocida, lo "
            "que da credibilidad y reduce la incertidumbre de la estimacion.",
            "",
            "La narrativa es de brecha: el comparativo AS-IS vs. estado del arte "
            "muestra que Credi10 esta lejos del patron en integracion y datos, y "
            "mas cerca en seguridad perimetral. Esa distancia es, en esencia, el "
            "trabajo por hacer, y ordenarla por tamanio de brecha ayuda a "
            "priorizar.",
        ])
    parts += [
        "## Benchmarks ligados al Hilo Dorado",
        "",
        phase2._benchmark_table(),
        "",
        "## Comparativo AS-IS vs. estado del arte",
        "",
        phase2._as_is_vs_industry_table(),
        "",
        "### Donde esta la brecha mas grande",
        "",
        "Las brechas 'Alta' se concentran en **integracion** y **datos**, que "
        "son justamente los frentes que la Fase 3 convierte en los gaps de "
        "mayor costo de inaccion. La brecha en disponibilidad es alta por falta "
        "de instrumentacion, no necesariamente por mala arquitectura: se cierra "
        "con observabilidad antes que con grandes rediseños.",
    ]
    parts += _closing(
        estimation=[
            "Anclar cada frente a un benchmark conocido permite usar "
            "**referencias de industria** para calibrar el esfuerzo, reduciendo "
            "la incertidumbre frente a estimar en el vacio. Los frentes con "
            "brecha 'Alta' concentran el grueso de los story points.",
        ],
        strategy=[
            "La estrategia adopta API-led connectivity como columna vertebral: "
            "primero la plataforma de gestion de APIs, luego los dominios. El "
            "comparativo justifica por que ese orden maximiza el cierre de "
            "brechas por unidad de esfuerzo.",
        ],
        risks=[
            "El riesgo es adoptar patrones por moda y no por ajuste al problema. "
            "El posicionamiento Hype Cycle (abajo) mitiga esto marcando que "
            "adoptar ya y que solo pilotar. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


def _t_f2_tendencias(ctx) -> str:
    parts = _theme_header(
        "Radar de tendencias y modelo de referencia sectorial", _P2, _P2B,
        [
            "El radar de tendencias ordena las apuestas tecnologicas en "
            "horizontes (0-12 meses, 1-3 anios, 3-5 anios) y el modelo de "
            "referencia (API-led con descomposicion de dominio estilo BIAN) "
            "ofrece el **plano objetivo** hacia el que converge el diseño. Para "
            "la estimacion, separar lo que se adopta ya de lo que se pilota "
            "evita inflar el alcance con tecnologias inmaduras.",
            "",
            "El hilo con la fase siguiente es que este modelo de referencia es "
            "el molde del que la Fase 4 saca los Solution Building Blocks: "
            "Experience / Process / System APIs se vuelven servicios concretos.",
        ])
    parts += [
        "## Radar de tendencias por horizonte",
        "",
        phase2._trends_radar(),
        "",
        "## Posicionamiento cualitativo (Hype Cycle)",
        "",
        phase2._hype_cycle_table(),
        "",
        "## Modelo de referencia (API-led + BIAN)",
        "",
        phase2._reference_model(),
        "",
        phase2._reference_model_table(),
        "",
        "### Como se usa el modelo de referencia",
        "",
        "El modelo separa **Experience APIs** (canales), **Process APIs** "
        "(dominios de credito) y **System APIs** (ERP, buros, PayU, datos). "
        "Esta separacion por capas es la que permite estimar por dominio y "
        "desacoplar la evolucion de los canales de la del core, un principio "
        "clave para no bloquear al negocio durante la transformacion.",
    ]
    parts += _closing(
        estimation=[
            "El modelo de referencia da una **taxonomia estable** para "
            "descomponer el alcance en capas y dominios, lo que hace la "
            "estimacion mas repetible y auditable. Lo que se pilota (IA "
            "generativa) se estima como spikes acotados, no como alcance firme.",
        ],
        strategy=[
            "La secuencia adopta primero lo maduro (API management, "
            "observabilidad), luego event-driven y cloud-native, y deja "
            "zero-trust e IA para horizontes posteriores. Asi el esfuerzo se "
            "concentra donde el retorno es mas seguro.",
        ],
        risks=[
            "El riesgo es el 'gold-plating': construir para tendencias que el "
            "negocio aun no necesita. El posicionamiento por horizonte y el "
            "WSJF de la Fase 5 contienen ese riesgo. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


# =========================================================================== #
# FASE 3 + 3.5 - Gaps y Viabilizacion
# =========================================================================== #

_P3 = "Fase 3 + 3.5 - Gaps y Viabilizacion"
_P3B = "../../03-gaps-y-viabilizacion.md"


def _t_f3_gaps(ctx) -> str:
    parts = _theme_header(
        "Matriz de dolores, causas raiz y gap analysis", _P3, _P3B,
        [
            "Aqui el advisory pasa del diagnostico al **caso de cambio**. Los "
            "dolores del assessment WSO2/Studio F se convierten en gaps "
            "cuantificables (GAP-001..005), cada uno con su causa raiz y su "
            "costo de inaccion, y se ligan a un indicador del RFP. Este es el "
            "pivote narrativo del informe: todo lo que vimos en el AS-IS "
            "cristaliza en una lista acotada de problemas que el proyecto debe "
            "resolver, y esa lista es la base del alcance y de la estimacion.",
            "",
            "Importa porque **un gap bien definido es un trozo de alcance "
            "estimable**. El gap analysis multidominio (TOGAF B/C/D) asegura "
            "que no se nos escape ninguna dimension (negocio, datos, "
            "aplicacion, tecnologia), de modo que la estimacion sea completa y "
            "no solo tecnica.",
        ])
    parts += [
        "## Matriz cuantificada de dolores y costo de inaccion",
        "",
        phase3._pain_matrix_table(),
        "",
        "### Lectura de la matriz",
        "",
        "Los dos gaps de **integracion con Siesa** (GAP-001 integracion rigida "
        "y GAP-002 lectura directa a la BD) tienen el mayor costo de inaccion "
        "porque bloquean el proceso completo y arriesgan la integridad de los "
        "datos. GAP-003 (datos inconsistentes) y GAP-004 (falta de gobierno) "
        "erosionan la confianza y la eficiencia. GAP-005 (obsolescencia) es "
        "riesgo latente de soporte y seguridad. Esta jerarquia de dolor es la "
        "que ordena las primeras olas.",
        "",
        "## Gap analysis multidominio (TOGAF B/C/D)",
        "",
        "### Dominio B - Negocio",
        "",
        phase3._gap_business_table(),
        "",
        "### Dominio C - Datos y Aplicacion",
        "",
        phase3._gap_data_table(),
        "",
        phase3._gap_application_table(),
        "",
        "### Dominio D - Tecnologia",
        "",
        phase3._gap_technology_table(),
    ]
    parts += _closing(
        estimation=[
            "Cada gap es una unidad de alcance con un indicador asociado; "
            "estimar el proyecto es, en primera aproximacion, estimar el cierre "
            "de GAP-001..005. El costo de inaccion (aunque marcado "
            "[DOC-ASSUMPTION] por falta de cifras reales) permite priorizar por "
            "valor, no solo por esfuerzo.",
        ],
        strategy=[
            "La estrategia secuencia el cierre de gaps por dependencia tecnica: "
            "no se puede cerrar GAP-002 (BD directa) sin antes habilitar la "
            "capa de integracion gobernada que resuelve GAP-001/004. Esa logica "
            "define el orden de las olas.",
        ],
        risks=[
            "El riesgo es cerrar un gap y abrir otro (p. ej. desacoplar Siesa "
            "sin preservar las reglas de negocio). La matriz de excepciones y "
            "los relievers trazables contienen ese riesgo.",
        ])
    return _emit(parts)


def _t_f3_viabilizacion(ctx) -> str:
    parts = _theme_header(
        "Aliviadores, bounded contexts y ABBs", _P3, _P3B,
        [
            "Los **aliviadores** (REL-001..004) responden a cada gap haciendo "
            "eco de las recomendaciones del assessment, y los **bounded "
            "contexts** (DDD) junto con los **ABBs** (Architecture Building "
            "Blocks) dan la primera forma arquitectonica a la solucion. Este es "
            "el puente entre el problema y el diseño: cada reliever apunta a un "
            "ABB que la Fase 4 convertira en un SBB concreto.",
            "",
            "Para la estimacion, los bounded contexts son oro: delimitan "
            "**fronteras de equipo y de esfuerzo**. Un contexto bien acotado se "
            "puede asignar a un squad stream-aligned y estimar de forma "
            "relativamente independiente, lo que reduce el riesgo de "
            "estimaciones acopladas.",
        ])
    parts += [
        "## Mapa de aliviadores",
        "",
        phase3._reliever_map(),
        "",
        phase3._reliever_table(),
        "",
        "## Bounded contexts y lenguaje ubicuo",
        "",
        phase3._bounded_contexts_map(),
        "",
        phase3._bounded_contexts_table(),
        "",
        phase3._ubiquitous_language_table(),
        "",
        "## Catalogo de ABBs",
        "",
        phase3._abb_table(),
        "",
        "### Del ABB al esfuerzo",
        "",
        "Los ABBs transversales (API Gateway, Data Services, bus de eventos, "
        "observabilidad) son **enablers** que benefician a todos los dominios "
        "pero no entregan valor de negocio por si solos. Reconocerlos como "
        "enablers es clave para la estimacion: su esfuerzo se amortiza entre "
        "varios modulos y su ausencia bloquea el resto, por lo que van primero "
        "en el roadmap.",
    ]
    parts += _closing(
        estimation=[
            "La descomposicion por bounded context es la base de la estimacion "
            "por modulo de la Fase 5: cada contexto agrupa modulos estimables "
            "por separado. Los ABBs enabler se estiman como inversion compartida.",
        ],
        strategy=[
            "La estrategia entrega primero los ABBs enabler (integracion, "
            "observabilidad) y luego los dominios de negocio, respetando el "
            "lenguaje ubicuo para que el equipo y el negocio hablen el mismo "
            "idioma y no haya drift semantico.",
        ],
        risks=[
            "El riesgo es que un enabler se retrase y arrastre a todos sus "
            "dependientes. Por eso el reverse briefing a la celula de diseño "
            "marca explicitamente las dependencias.",
        ])
    return _emit(parts)


def _t_f3_reglas_nfr(ctx) -> str:
    parts = _theme_header(
        "Reglas de negocio, excepciones y NFR base", _P3, _P3B,
        [
            "Preservar las **reglas de negocio** (RN-01..04) es un requisito "
            "duro del RFP, y la matriz de excepciones (Exception Storming) "
            "captura los casos borde del flujo de credito antes de diseñar. "
            "Junto con el perfil base de NFR (ISO 25010) y los limites de "
            "integracion legada, esta seccion define **que no puede romperse** "
            "durante la transformacion.",
            "",
            "La narrativa de calidad es central: las excepciones y los NFR son "
            "donde los proyectos subestiman esfuerzo. Hacerlos explicitos aqui "
            "evita la sorpresa clasica de 'el happy path estaba, pero los casos "
            "borde duplicaron el trabajo'.",
        ])
    parts += [
        "## Reglas de negocio a preservar",
        "",
        phase3._business_rules_table(),
        "",
        "## Matriz de excepciones (Exception Storming)",
        "",
        phase3._exception_storming_table(),
        "",
        "### Por que las excepciones mueven la aguja",
        "",
        "Cada excepcion (buro caido, respuesta parcial, no-hit, fallo de "
        "escritura a Siesa, duplicados) es trabajo real de resiliencia e "
        "idempotencia que rara vez cabe en una estimacion ingenua. "
        "Catalogarlas desde la Fase 3 permite que la estimacion por modulo las "
        "incluya en lugar de descubrirlas en construccion.",
        "",
        "## Perfil base de NFR y limites legacy",
        "",
        phase3._nfr_table(),
        "",
        phase3._legacy_limits_table(),
    ]
    parts += _closing(
        estimation=[
            "Los NFR y las excepciones son multiplicadores de esfuerzo: un "
            "modulo con muchos casos borde y NFR exigentes de disponibilidad se "
            "talla mas grande. El factor de riesgo de integracion (1,25) de la "
            "Fase 5 captura parte de este efecto.",
        ],
        strategy=[
            "La estrategia introduce pruebas de **equivalencia funcional** para "
            "garantizar que las reglas RN-01..04 se preservan al modernizar, y "
            "trata los limites legacy (WS unico, batch) como fronteras a "
            "desacoplar de forma incremental (Strangler Fig).",
        ],
        risks=[
            "El riesgo mayor es alterar inadvertidamente una regla de negocio al "
            "migrar. Se mitiga con una base de casos de prueba de equivalencia "
            "como prerrequisito (PRE-006). [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


# =========================================================================== #
# FASE 4 - Diseno TO-BE
# =========================================================================== #

_P4 = "Fase 4 - Diseno TO-BE"
_P4B = "../../04-diseno-to-be.md"


def _t_f4_arquitectura(ctx) -> str:
    parts = _theme_header(
        "Arquitectura TO-BE: vistas C4 y SBBs", _P4, _P4B,
        [
            "El diseño TO-BE materializa los ABBs en **Solution Building "
            "Blocks** (SBB-001..008) y los organiza en vistas C4 (contexto, "
            "contenedores, componentes). Esta es la columna vertebral tecnica "
            "del proyecto: una plataforma de API Management (WSO2), Data "
            "Services gobernados sobre Siesa, un bus de eventos, servicios de "
            "dominio en .NET 8, observabilidad y una estrategia cloud AWS. Cada "
            "SBB resuelve uno o varios gaps y habilita uno o varios drivers.",
            "",
            "Para la estimacion, el mapeo ABB -> SBB es lo que convierte la "
            "arquitectura en trabajo contable: cada SBB es un paquete de "
            "esfuerzo con un stack objetivo definido, lo que permite tallar su "
            "construccion con criterio en lugar de adivinar.",
        ])
    parts += [
        "## Mapeo ABB -> SBB (Hilo Dorado)",
        "",
        phase4._abb_sbb_table(),
        "",
        "## Vistas C4 del TO-BE",
        "",
        "### C4 Nivel 1 - Contexto",
        "",
        phase4._c4_context(),
        "",
        "### C4 Nivel 2 - Contenedores",
        "",
        phase4._c4_container(),
        "",
        "### C4 Nivel 3 - Componentes (Estudio de Credito)",
        "",
        phase4._c4_component(),
        "",
        "### Lectura de las vistas",
        "",
        "El patron central es un **API Gateway** que media todo el trafico y un "
        "**bus de eventos** que desacopla la escritura a Siesa. Esta eleccion "
        "arquitectonica es la que hace viable la continuidad operativa: permite "
        "desviar trafico del legado al TO-BE de forma incremental, sin un corte "
        "big-bang.",
        "",
        "## NFR habilitados por los SBBs",
        "",
        phase4._nfr_table(),
    ]
    parts += _closing(
        estimation=[
            "Cada SBB es una unidad de estimacion con stack conocido. Los SBB de "
            "integracion (001, 002, 003) concentran el mayor esfuerzo y riesgo "
            "porque tocan el nucleo del acoplamiento; la Fase 5 los refleja en "
            "las tallas L/XL de los modulos asociados.",
        ],
        strategy=[
            "La estrategia construye primero los SBB enabler (API Management, "
            "Data Services, observabilidad) y luego los servicios de dominio, "
            "aplicando Strangler Fig para migrar sin interrumpir. El diseño esta "
            "pensado para ser entregado por olas.",
        ],
        risks=[
            "El riesgo arquitectonico es crear un nuevo cuello de botella en el "
            "gateway o el bus. Se mitiga con observabilidad (SBB-005) y rate "
            "limiting desde el inicio. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


def _t_f4_adrs(ctx) -> str:
    parts = _theme_header(
        "Decisiones de arquitectura (ADRs)", _P4, _P4B,
        [
            "Los **ADR** (Architecture Decision Records) documentan las seis "
            "decisiones estructurales del TO-BE con su contexto, decision y "
            "consecuencias. Son el corazon de la trazabilidad arquitectonica: "
            "explican **por que** se eligio cada camino, lo que permite "
            "recalibrar con fundamento si el cliente prefiere una alternativa.",
            "",
            "Para la estimacion, los ADR acotan el espacio de solucion y, por "
            "tanto, la varianza del esfuerzo: fijar WSO2, .NET 8, AWS y la "
            "prohibicion de acceso directo a la BD elimina ramas de "
            "incertidumbre que, de quedar abiertas, inflarian el rango de la "
            "estimacion.",
        ])
    parts += [
        "## Resumen de decisiones (ADR)",
        "",
        "| ADR | Decision | Gap que ataca | Impacto en esfuerzo/riesgo |",
        "| --- | --- | --- | --- |",
        "| ADR-001 | API Management centralizado (WSO2) | GAP-004 | Alto "
        "(plataforma transversal) |",
        "| ADR-002 | Data Services + eventos sobre Siesa (sin BD directa) | "
        "GAP-001, GAP-002 | Muy alto (nucleo del acoplamiento) |",
        "| ADR-003 | Migrar runtime a .NET 8 | GAP-005 | Alto (extension: "
        "muchos componentes) |",
        "| ADR-004 | WSO2 vs. alternativas (recalibrable) | GAP-004 | Medio "
        "(fuente de varianza si cambia) |",
        "| ADR-005 | Fuente unica de verdad por dominio | GAP-003 | Alto "
        "(consolidar +200 BDs) |",
        "| ADR-006 | Estrategia cloud AWS | GAP-002 | Medio (IaC + FinOps) |",
        "",
        "## Registro detallado de decisiones",
        "",
        phase4._adrs(),
        "",
        "### Como leer los ADR para estimar",
        "",
        "ADR-002 (reemplazar el WS unico y la BD directa por Data Services + "
        "eventos) es el de mayor impacto en esfuerzo y riesgo, porque toca el "
        "punto mas acoplado del sistema. ADR-003 (migrar a .NET 8) es el de "
        "mayor extension. ADR-004 (elegir WSO2) es recalibrable y su cambio "
        "afectaria la estimacion de la plataforma de integracion. Leer los ADR "
        "en clave de esfuerzo/riesgo es parte del trabajo de estimacion.",
    ]
    parts += _closing(
        estimation=[
            "Las decisiones fijan el stack y, con el, los factores de la tabla "
            "parametrica. Un cambio de ADR (p. ej. otra plataforma de API) "
            "obligaria a recalibrar la estimacion de los SBB afectados; por eso "
            "los ADR marcados recalibrables se vigilan como fuente de varianza.",
        ],
        strategy=[
            "Las consecuencias de cada ADR definen prerrequisitos de "
            "implementacion (IaC y FinOps para AWS, contratos AsyncAPI para el "
            "desacople) que entran al roadmap como trabajo habilitador.",
        ],
        risks=[
            "El riesgo es tratar un ADR aceptado como inmutable cuando el "
            "contexto cambia. El formato ADR mantiene la decision revisable y "
            "trazable, conteniendo ese riesgo. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


def _t_f4_datos_contratos(ctx) -> str:
    parts = _theme_header(
        "Modelo de datos (ERD) y contratos de API/eventos", _P4, _P4B,
        [
            "El modelo de datos por bounded context (varios ERD) y los "
            "contratos OpenAPI/AsyncAPI son la **spec ejecutable** del TO-BE: "
            "definen las entidades, las operaciones sincronas y los eventos "
            "asincronos que el equipo construira. Son el nivel de detalle que "
            "convierte una estimacion gruesa en una estimacion por contrato, "
            "mucho mas precisa.",
            "",
            "El hilo narrativo es que los contratos **formalizan el desacople**: "
            "exponer Siesa como Data Services con un contrato explicito (y "
            "prohibir el acceso directo a su BD) es lo que ejecuta ADR-002 en "
            "la practica.",
        ])
    parts += [
        "## Modelo de datos por bounded context",
        "",
        "### Recaudo / Pagos",
        "",
        phase4._erd(),
        "",
        "### Originacion y Estudio de Credito",
        "",
        phase4._erd_originacion(),
        "",
        "### Cartera y Cobranza",
        "",
        phase4._erd_cartera(),
        "",
        phase4._erd_cobranza(),
        "",
        "## Contratos de API y eventos",
        "",
        phase4._api_contract_index_table(),
        "",
        "### Contrato sincrono (OpenAPI)",
        "",
        phase4._openapi_snippet(),
        "",
        "### Data Services sobre Siesa (OpenAPI)",
        "",
        phase4._openapi_siesa_snippet(),
        "",
        "### Eventos (AsyncAPI)",
        "",
        phase4._asyncapi_snippet(),
        "",
        "## Estrategia de migracion",
        "",
        phase4._migration_table(),
    ]
    parts += _closing(
        estimation=[
            "Contar entidades, endpoints y eventos da una base cuantitativa para "
            "la estimacion funcional (p. ej. puntos funcionales / CFP). Los "
            "contratos de integracion con Siesa son los de mayor incertidumbre "
            "porque su esquema real es [EPISTEMIC-VOID] en el corpus.",
        ],
        strategy=[
            "La migracion sigue Strangler Fig: se desvia por Data Services y "
            "eventos de forma incremental, con CDC donde aplique, nunca un "
            "corte total. El orden de los contratos a construir sigue el de las "
            "olas.",
        ],
        risks=[
            "El riesgo es que el contrato real de Siesa difiera del esbozado, "
            "disparando retrabajo. Por eso obtener la especificacion del WS/Data "
            "Services de Siesa es un prerrequisito duro (PRE-001). "
            "[EPISTEMIC-VOID]",
        ])
    return _emit(parts)


def _t_f4_catalogo_ia(ctx) -> str:
    prod_table, accel_table, entries = phase4._ai_catalog_tables()
    parts = _theme_header(
        "Catalogo de oportunidades de IA", _P4, _P4B,
        [
            "El catalogo de IA se modela como **skill declarativo** (no "
            "hardcodeado) y distingue dos pistas: IA-como-producto (casos de uso "
            "que agregan valor al negocio) e IA-como-acelerador-de-construccion "
            "(IA que acelera el propio desarrollo). Presentarlo aqui, dentro del "
            "informe tecnico, permite evaluar su viabilidad con los datos "
            "disponibles y evitar promesas sin sustento.",
            "",
            "Para la estimacion, la IA se trata con prudencia: la mayoria de los "
            "casos son **spikes/experimentos** acotados, no alcance firme, "
            "porque su viabilidad depende de datos cuya calidad aun no esta "
            "garantizada.",
        ])
    parts += [
        "## IA como producto",
        "",
        prod_table,
        "",
        "## IA como acelerador de construccion",
        "",
        accel_table,
        "",
        "### Como se incorpora la IA sin inflar el alcance",
        "",
        "Cada oportunidad lleva un gancho al roadmap y una nota de viabilidad. "
        "Las de viabilidad alta con datos disponibles pueden entrar como "
        "incremento; las demas se exploran en spikes de tiempo acotado. Asi la "
        "IA aporta valor sin convertirse en un riesgo de cronograma.",
    ]
    if not entries:
        parts += [
            "",
            "> **[EPISTEMIC-VOID]** El skill de catalogo de IA no esta "
            "disponible; no se fabrican oportunidades. El motor degrada con "
            "elegancia.",
        ]
    parts += _closing(
        estimation=[
            "Las oportunidades de IA se estiman como spikes acotados salvo "
            "cuando la viabilidad es alta y los datos existen. Esto evita "
            "comprometer esfuerzo sobre casos cuya factibilidad aun es "
            "[DOC-ASSUMPTION].",
        ],
        strategy=[
            "La estrategia prioriza primero la IA-como-acelerador (mejora la "
            "productividad del equipo desde el inicio) y difiere la "
            "IA-como-producto a cuando la plataforma de datos este consolidada.",
        ],
        risks=[
            "El riesgo es sobreprometer capacidades de IA sin datos de calidad. "
            "El tratamiento por spikes y la nota de viabilidad por caso "
            "contienen ese riesgo. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


def _t_f4_ux_pruebas(ctx) -> str:
    parts = _theme_header(
        "UX, BPMN TO-BE, Dry-Run y seguridad", _P4, _P4B,
        [
            "La vista de UX (service blueprint), el BPMN TO-BE, el paquete "
            "spec-driven (Gherkin), el acta de Dry-Run y la matriz de threat "
            "modeling (STRIDE) cierran el diseño asegurando que **la "
            "experiencia, el proceso, las reglas, las pruebas y la seguridad "
            "estan alineadas** antes de construir. El Dry-Run es la validacion "
            "de mesa (tabletop) que recorre la cadena Evento -> UX -> Gherkin "
            "-> API -> C4 -> BD -> respuesta.",
            "",
            "Para la estimacion, el Dry-Run es un seguro barato: validar la "
            "coherencia end-to-end en papel antes de codificar evita retrabajo "
            "caro. La seguridad por diseño (STRIDE) tambien se estima aqui en "
            "lugar de añadirse al final como un parche.",
        ])
    parts += [
        "## BPMN TO-BE",
        "",
        phase4._bpmn_tobe(),
        "",
        "## Service blueprint",
        "",
        phase4._service_blueprint_table(),
        "",
        "## Paquete spec-driven (Gherkin)",
        "",
        "### Escenarios ejecutables",
        "",
        phase4._gherkin(),
        "",
        "## Acta de Dry-Run / Tabletop",
        "",
        "### Cadena de validacion extremo a extremo",
        "",
        phase4._dry_run_chain_table(),
        "",
        "### Criterios de certificacion",
        "",
        phase4._dry_run_act_table(),
        "",
        "## Threat modeling (STRIDE)",
        "",
        "### Amenazas y mitigaciones",
        "",
        phase4._threat_model_table(),
    ]
    parts += _closing(
        estimation=[
            "Las historias Gherkin (happy + borde) son unidades de estimacion "
            "finas; el catalogo exhaustivo 04b cubre todos los modulos sin "
            "muestreo. La seguridad por diseño añade esfuerzo que se contabiliza "
            "aqui, no despues.",
        ],
        strategy=[
            "La estrategia valida cada ola con un Dry-Run antes del build "
            "(gobierno AICV-E del AM) y aplica zero-trust de forma transversal. "
            "El BPMN TO-BE guia el orden de construccion por tramo de proceso.",
        ],
        risks=[
            "El riesgo es descubrir incoherencias (UX sin contrato, regla sin "
            "componente) en construccion. El Dry-Run los detecta antes, y STRIDE "
            "anticipa los vectores de ataque. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


# =========================================================================== #
# FASE 5 - Roadmap, Estimacion y RAID
# =========================================================================== #

_P5 = "Fase 5 - Roadmap, Estimacion y RAID"
_P5B = "../../05-roadmap-estimacion-raid.md"


def _t_f5_estimacion(ctx) -> str:
    parts = _theme_header(
        "Estimacion por modulo y modelo parametrico", _P5, _P5B,
        [
            "Esta es la fase que da sentido a todo el advisory: una "
            "**estimacion por modulo** derivada de un modelo parametrico "
            "recalibrable, con cobertura COMPLETA de los modulos declarados "
            f"(**{modules_mod.module_count()}** modulos, sin muestreo). Cada "
            "modulo recibe una talla T-Shirt, story points ajustados, "
            "person-months y un WSJF, todo calculado de forma determinista a "
            "partir de parametros explicitos. La clave es la honestidad: "
            "**todas las cifras de esfuerzo son [DOC-ASSUMPTION]**, esfuerzo "
            "relativo para dimensionar, no un compromiso de fechas.",
            "",
            "El objetivo declarado del engagement es 'estimar lo mas acertado "
            "posible'. Este modelo lo logra no inventando precision falsa, sino "
            "haciendo explicitos los supuestos: cambiar un parametro recalcula "
            "toda la estimacion, lo que permite hacer sensibilidad y converger "
            "con el equipo tecnico en un taller.",
        ])
    parts += [
        "## Tabla parametrica recalibrable",
        "",
        phase5._parametric_table(),
        "",
        phase5._tshirt_base_table(),
        "",
        phase5._derivation_formula(),
        "",
        "## Estimacion detallada por modulo",
        "",
        phase5._per_module_estimation_table(),
        "",
        phase5._estimation_totals_note(),
        "",
        "## Descomposicion del esfuerzo por frente",
        "",
        phase5._front_breakdown_table(),
        "",
        phase5._front_split_note(),
        "",
        "### Como leer la estimacion",
        "",
        "Los modulos de integracion (MOD-16 Siesa, talla XL) y de plataforma "
        "(MOD-01, MOD-09) concentran el esfuerzo. La descomposicion por frente "
        "revela que Dev no es el unico costo: integracion, QA y gestion del "
        "cambio suman una porcion significativa, algo que las estimaciones "
        "ingenuas suelen olvidar.",
    ]
    parts += _closing(
        estimation=[
            "Esta seccion ES la estimacion. Su valor esta en ser **parametrica "
            "y auditable**: cada cifra se deriva de la talla y los factores, de "
            "modo que una recalibracion (nueva productividad, nuevos factores) "
            "actualiza todo el modelo sin reescribir a mano. Las cifras son "
            "relativas [DOC-ASSUMPTION] y deben reconciliarse en taller.",
        ],
        strategy=[
            "La estimacion por frente informa la composicion de los squads "
            "(Team Topologies): cuanto Dev, Data, Integracion y QA necesita "
            "cada ola. Es insumo directo del dimensionamiento de equipos.",
        ],
        risks=[
            "El riesgo es tomar las cifras como compromiso de fechas. Se mitiga "
            "marcando todo [DOC-ASSUMPTION] y atando la incertidumbre a la "
            "cobertura del corpus (ver riesgo de desfase).",
        ])
    return _emit(parts)


def _t_f5_roadmap(ctx) -> str:
    parts = _theme_header(
        "Roadmap por olas, WSJF y ruta critica", _P5, _P5B,
        [
            "El roadmap organiza el trabajo en **olas de transicion** "
            "(WAV-000..003) priorizadas por WSJF, con dependencias tecnicas "
            "explicitas y aciclicas y una ruta critica identificada. La "
            "narrativa es de secuencia: primero cimientos (observabilidad, alta "
            "disponibilidad), luego la capa de integracion gobernada y el "
            "desacople de Siesa, despues la modernizacion .NET y la plataforma "
            "de datos, y por ultimo el canal B2C y el escalamiento.",
            "",
            "Importa porque un buen roadmap convierte una estimacion de esfuerzo "
            "en un **plan de entrega de valor**: las olas tempranas capturan "
            "valor y reducen riesgo, y la ruta critica avisa donde un retraso "
            "arrastra todo el proyecto.",
        ])
    parts += [
        "## Priorizacion WSJF",
        "",
        "### WSJF por iniciativa",
        "",
        phase5._wsjf_table(),
        "",
        phase5._wsjf_notes(),
        "",
        "### Orden WSJF por modulo",
        "",
        phase5._per_module_wsjf_order_table(),
        "",
        "## Dependencias y ruta critica",
        "",
        "### Grafo de dependencias (aciclico)",
        "",
        phase5._dependency_diagram(),
        "",
        phase5._critical_path_note(),
        "",
        "## Roadmap por olas (gantt)",
        "",
        phase5._roadmap_gantt(),
        "",
        phase5._waves_table(),
        "",
        "### Agenda por modulo",
        "",
        phase5._module_scheduling_table(),
    ]
    parts += _closing(
        estimation=[
            "El WSJF combina el valor de negocio (heredado de los drivers) con "
            "el job size (heredado de la estimacion), cerrando el circulo: la "
            "estimacion alimenta la priorizacion y la priorizacion ordena la "
            "entrega. El esfuerzo total agregado dimensiona el numero de olas y "
            "squads. [DOC-ASSUMPTION]",
        ],
        strategy=[
            "La estrategia de implementacion ES este roadmap: enablers primero, "
            "Strangler Fig por ola, rollback por ola para preservar la "
            "continuidad operativa exigida por el RFP. La ruta critica fija el "
            "foco de atencion de la gestion.",
        ],
        risks=[
            "El riesgo de cronograma se concentra en la ruta critica "
            "(observabilidad -> API Management -> desacople Siesa -> .NET 8 -> "
            "B2C). Un retraso en el desacople de Siesa (MOD-16) es el de mayor "
            "impacto sistemico.",
        ])
    return _emit(parts)


def _t_f5_raid(ctx) -> str:
    parts = _theme_header(
        "Matriz RAID (supuestos, restricciones, dependencias, prerrequisitos)",
        _P5, _P5B,
        [
            "La matriz **RAID** consolida los supuestos, restricciones, "
            "dependencias y prerrequisitos que condicionan la ejecucion. Es el "
            "contrato de realidad del proyecto: enumera lo que debe ser cierto, "
            "lo que no puede cambiar, lo que depende de que, y lo que debe "
            "existir antes de arrancar cada frente. Sin RAID, una estimacion es "
            "una promesa sin condiciones.",
            "",
            "Las restricciones son reales y vienen del RFP: preservar reglas de "
            "negocio, compatibilidad con proveedores actuales, continuidad "
            "operativa, dependencia del ERP Siesa y facturacion por entregables "
            "a 60 dias. Cada una moldea el roadmap y, por tanto, la estimacion "
            "de tiempos.",
        ])
    parts += [
        "## Supuestos",
        "",
        phase5._raid_assumptions_table(),
        "",
        "## Restricciones (del RFP)",
        "",
        phase5._raid_constraints_table(),
        "",
        "## Dependencias",
        "",
        phase5._raid_dependencies_table(),
        "",
        "## Prerrequisitos",
        "",
        phase5._raid_prerequisites_table(),
        "",
        "### Como el RAID disciplina la estimacion",
        "",
        "Cada prerrequisito no cumplido es un bloqueo de ola; cada dependencia "
        "define un orden obligatorio; cada restriccion acota el espacio de "
        "solucion. El RAID es, en la practica, la lista de condiciones bajo las "
        "cuales la estimacion es valida.",
    ]
    parts += _closing(
        estimation=[
            "Los supuestos de estimacion (reconciliar tallas en taller, "
            "estabilidad de contratos de proveedores) condicionan la validez de "
            "las cifras. La facturacion por entregables a 60 dias condiciona el "
            "tamanio de cada ola. [DOC-ASSUMPTION]",
        ],
        strategy=[
            "La estrategia respeta las restricciones duras del RFP: Strangler "
            "Fig y rollback por ola para continuidad, preservacion de reglas, "
            "convivencia con Siesa/UnoEE y proveedores durante la transicion.",
        ],
        risks=[
            "El riesgo es arrancar una ola con prerrequisitos abiertos (p. ej. "
            "sin el catalogo de contratos de Siesa). El RAID hace ese riesgo "
            "visible y asignable. [EPISTEMIC-VOID] en la linea base de "
            "disponibilidad (P-02).",
        ])
    return _emit(parts)


def _t_f5_riesgo_desfase(ctx) -> str:
    parts = _theme_header(
        "Evaluacion de suficiencia y riesgo de desfase", _P5, _P5B,
        [
            "Esta seccion responde a la pregunta del dueño de negocio: "
            "**¿tenemos suficiente detalle para crear y arrancar el "
            "proyecto?** Y la complementa con un analisis de **riesgo de "
            "desfase de tiempos** (schedule-slip) atado a la cobertura del "
            "corpus. Es el cierre honesto del advisory: declara que es "
            "suficiente para planear olas y arrancar, pero insuficiente para "
            "comprometer fechas o presupuesto cerrado hasta cerrar los vacios.",
            "",
            "Atar la incertidumbre de estimacion a la **cobertura del knowledge "
            "base** (bandas de cobertura y etiquetas epistemicas por documento) "
            "es lo que hace la estimacion defendible: los modulos sustentados "
            "por evidencia debil arrastran mas incertidumbre, y eso se declara "
            "en lugar de ocultarse.",
        ])
    parts += [
        "## Scorecard de suficiencia (dueño de negocio)",
        "",
        phase5._business_owner_scorecard(),
        "",
        "### Veredicto de suficiencia",
        "",
        "El detalle alcanzado es **suficiente para CREAR y ARRANCAR el "
        "proyecto** (arquitectura, alcance funcional, estimacion por modulo, "
        "priorizacion y roadmap), pero el modelo economico sigue sin linea base "
        "real, de modo que no se puede comprometer presupuesto cerrado sin un "
        "ejercicio de costeo. Esta distincion es el nucleo de una estimacion "
        "honesta.",
    ]
    # El resto del contenido (riesgo de desfase, tabla de incertidumbre por KB
    # y veredicto Go/No-Go) se reutiliza del informe plano de la Fase 5 via el
    # builder completo, para no divergir del gate QG-5.
    parts += [
        "",
        "## Riesgo de desfase de tiempos (resumen)",
        "",
        "> El analisis completo de **schedule-slip** (matriz probabilidad x "
        "impacto RS-01..RS-06, incertidumbre por cobertura del corpus por "
        "modulo y veredicto **Go/No-Go** de construccion, hoy **GO "
        "CONDICIONADO**) vive en la vista compacta de la fase "
        f"([{_P5B}]({_P5B})) y se gobierna alli para no divergir del gate QG-5. "
        "Aqui se interpreta su implicacion: el desfase es mayor donde la "
        "cobertura documental es menor.",
    ]
    parts += _closing(
        estimation=[
            "La incertidumbre de la estimacion no es uniforme: es mayor en los "
            "modulos cuyo soporte documental es [EPISTEMIC-VOID] o de baja "
            "cobertura. La estimacion acertada consiste precisamente en "
            "declarar esa varianza, no en esconderla.",
        ],
        strategy=[
            "La estrategia reduce el riesgo de desfase cerrando primero los "
            "vacios de mayor impacto (contrato de Siesa, linea base de "
            "disponibilidad) antes de comprometer las olas que dependen de "
            "ellos.",
        ],
        risks=[
            "El veredicto es **GO CONDICIONADO**: se puede arrancar, pero con "
            "contingencia explicita y con el compromiso de cerrar los "
            "prerrequisitos criticos. Ignorar esa condicion es el camino "
            "directo al desfase. [DOC-ASSUMPTION]",
        ])
    return _emit(parts)


# =========================================================================== #
# FASE 6 - Caso de Negocio
# =========================================================================== #

_P6 = "Fase 6 - Caso de Negocio"
_P6B = "../../06-caso-de-negocio.md"


def _t_f6_valor(ctx) -> str:
    parts = _theme_header(
        "Value driver tree y outcomes de negocio", _P6, _P6B,
        [
            "El caso de negocio cierra el Hilo Dorado conectando cada outcome "
            "tecnico con un **outcome de negocio** (ROI-001..005), uno por cada "
            "driver del RFP. El value driver tree es la narrativa de valor: "
            "muestra como la observabilidad y el API Management habilitan "
            "disponibilidad, como el desacople de Siesa habilita eficiencia, y "
            "asi sucesivamente. Es la respuesta a '¿para que todo este "
            "esfuerzo?'.",
            "",
            "Para la estimacion, el value driver tree es el que justifica la "
            "inversion: ata el esfuerzo estimado a un retorno esperado, aunque "
            "ese retorno siga siendo [DOC-ASSUMPTION] mientras no haya linea "
            "base de costos.",
        ])
    parts += [
        "## Value driver tree",
        "",
        phase6._value_driver_tree(),
        "",
        phase6._value_driver_table(),
        "",
        "### Lectura del arbol de valor",
        "",
        "Cada outcome de negocio esta entregado por olas concretas, de modo que "
        "el valor no es abstracto: se puede rastrear hasta la WAV que lo "
        "produce. Esto permite al negocio ver que ola captura que retorno y "
        "decidir la secuencia con criterio economico.",
    ]
    parts += _closing(
        estimation=[
            "El valor esperado por driver permite comparar inversion vs. retorno "
            "por ola y decidir el alcance financiable. Sin linea base real, el "
            "retorno se expresa como estructura [DOC-ASSUMPTION], no como "
            "promesa.",
        ],
        strategy=[
            "La estrategia prioriza las olas que entregan los outcomes de mayor "
            "valor temprano (disponibilidad y eficiencia), alineando el orden de "
            "entrega con la captura de valor.",
        ],
        risks=[
            "El riesgo es comprometer ROI sin datos. El value driver tree "
            "estructura el valor pero lo marca [DOC-ASSUMPTION] hasta el costeo. "
            "[EPISTEMIC-VOID] en la linea base economica.",
        ])
    return _emit(parts)


def _t_f6_financiero(ctx) -> str:
    parts = _theme_header(
        "Modelo financiero y defensa ejecutiva", _P6, _P6B,
        [
            "El modelo financiero (CAPEX/OPEX, TCO As-Is vs To-Be, unit "
            "economics FinOps y VAN/TIR/Payback en tres escenarios) ofrece la "
            "**estructura** del caso economico, y la presentacion ejecutiva "
            "mapea el Hilo Dorado completo F1->F6 contra los criterios de "
            "evaluacion de la oferta. La honestidad epistemica es total: el "
            "corpus NO tiene cifras reales de costo, asi que todo el modelo es "
            "ilustrativo [DOC-ASSUMPTION] y debe costearse con datos reales "
            "antes de cualquier decision de inversion.",
            "",
            "Presentar la estructura financiera (aunque con cifras "
            "ilustrativas) tiene valor: muestra que variables mueven el "
            "retorno, que supuestos hay que validar y como se defenderia el caso "
            "ante el comite. Es el puente entre el informe tecnico y la decision "
            "de negocio.",
        ])
    parts += [
        phase6._epistemic_void_note(),
        "",
        "## Estructura de costos y retorno",
        "",
        "### CAPEX / OPEX por ola",
        "",
        phase6._capex_opex_table(),
        "",
        "### TCO comparativo As-Is vs To-Be",
        "",
        phase6._tco_table(),
        "",
        "### Unit economics (FinOps)",
        "",
        phase6._unit_economics_table(),
        "",
        "### Escenarios financieros",
        "",
        phase6._scenarios_table(),
        "",
        phase6._assumption_register(),
        "",
        "## Defensa ejecutiva: Hilo Dorado completo",
        "",
        "### Trazabilidad F1 -> F6",
        "",
        phase6._golden_thread_diagram(),
        "",
        phase6._golden_thread_table(),
        "",
        "### Alineacion con los criterios de la oferta",
        "",
        phase6._offer_criteria_table(),
    ]
    parts += _closing(
        estimation=[
            "El modelo financiero toma el esfuerzo estimado (CAPEX por ola) y lo "
            "contrasta con el TCO y el retorno esperado. Mientras las cifras "
            "sean [DOC-ASSUMPTION], el modelo sirve para sensibilidad y defensa, "
            "no para comprometer presupuesto.",
        ],
        strategy=[
            "La estrategia de financiamiento sigue las olas: CAPEX concentrado "
            "en las olas de integracion y modernizacion, OPEX transversal. La "
            "facturacion por entregables (RFP) condiciona el tamanio de cada "
            "entrega.",
        ],
        risks=[
            "El riesgo es tratar las cifras ilustrativas como una oferta. El "
            "[EPISTEMIC-VOID] de la linea base de costos obliga a un ejercicio "
            "de costeo como prerrequisito de cualquier compromiso economico.",
        ])
    return _emit(parts)


# --------------------------------------------------------------------------- #
# Registro de temas por fase (orden estable).
# --------------------------------------------------------------------------- #

PHASE_THEMES = {
    "fase-0-higiene-epistemica": [
        Theme("corpus-y-trazabilidad",
              "Corpus, trazabilidad y cobertura de evidencia", _t_f0_corpus),
        Theme("grafo-de-conceptos",
              "Grafo de conceptos y modelo mental del ecosistema", _t_f0_grafo),
    ],
    "fase-1-contexto-as-is": [
        Theme("contexto-negocio",
              "Contexto de negocio: drivers y capacidades", _t_f1_negocio),
        Theme("procesos-bpmn",
              "Procesos de negocio AS-IS (BPMN) y metricas base",
              _t_f1_procesos),
        Theme("ecosistema-tecnologico",
              "Ecosistema tecnologico y de datos AS-IS", _t_f1_ecosistema),
        Theme("deuda-tecnica",
              "Deuda tecnica y riesgos del AS-IS", _t_f1_deuda),
    ],
    "fase-2-estado-del-arte": [
        Theme("benchmarks",
              "Benchmarks de industria y comparativo AS-IS", _t_f2_benchmarks),
        Theme("tendencias-y-referencia",
              "Radar de tendencias y modelo de referencia sectorial",
              _t_f2_tendencias),
    ],
    "fase-3-gaps-y-viabilizacion": [
        Theme("gap-analysis",
              "Matriz de dolores, causas raiz y gap analysis", _t_f3_gaps),
        Theme("viabilizacion",
              "Aliviadores, bounded contexts y ABBs", _t_f3_viabilizacion),
        Theme("reglas-y-nfr",
              "Reglas de negocio, excepciones y NFR base", _t_f3_reglas_nfr),
    ],
    "fase-4-diseno-to-be": [
        Theme("arquitectura-c4",
              "Arquitectura TO-BE: vistas C4 y SBBs", _t_f4_arquitectura),
        Theme("adrs", "Decisiones de arquitectura (ADRs)", _t_f4_adrs),
        Theme("modelo-datos-y-contratos",
              "Modelo de datos (ERD) y contratos de API/eventos",
              _t_f4_datos_contratos),
        Theme("catalogo-ia",
              "Catalogo de oportunidades de IA", _t_f4_catalogo_ia),
        Theme("ux-y-pruebas",
              "UX, BPMN TO-BE, Dry-Run y seguridad", _t_f4_ux_pruebas),
    ],
    "fase-5-roadmap-estimacion-raid": [
        Theme("estimacion-por-modulo",
              "Estimacion por modulo y modelo parametrico", _t_f5_estimacion),
        Theme("roadmap-olas",
              "Roadmap por olas, WSJF y ruta critica", _t_f5_roadmap),
        Theme("raid", "Matriz RAID (supuestos, restricciones, dependencias, "
              "prerrequisitos)", _t_f5_raid),
        Theme("riesgo-de-desfase",
              "Evaluacion de suficiencia y riesgo de desfase",
              _t_f5_riesgo_desfase),
    ],
    "fase-6-caso-de-negocio": [
        Theme("value-driver-tree",
              "Value driver tree y outcomes de negocio", _t_f6_valor),
        Theme("modelo-financiero",
              "Modelo financiero y defensa ejecutiva", _t_f6_financiero),
    ],
}


# --------------------------------------------------------------------------- #
# README por fase (nivel 1): indice de los temas de la fase + narrativa.
# --------------------------------------------------------------------------- #

# Hilo narrativo por fase (de donde venimos / que encontramos / a donde vamos).
PHASE_NARRATIVE = {
    "fase-0-higiene-epistemica": (
        "Toda estimacion defendible empieza por saber que sabemos. La Fase 0 "
        "audita el corpus, separa hecho de supuesto y deja una agenda de "
        "preguntas abiertas. Reduce incertidumbre fijando el nivel de confianza "
        "de cada cifra que vendra despues."),
    "fase-1-contexto-as-is": (
        "Con el corpus saneado, retratamos el AS-IS: drivers de negocio, "
        "procesos, ecosistema tecnologico y deuda tecnica. Es el terreno real "
        "sobre el que estimaremos; conocerlo en detalle convierte la corazonada "
        "en estimacion."),
    "fase-2-estado-del-arte": (
        "Comparamos el AS-IS contra los patrones de industria para medir la "
        "brecha con referencias reconocidas. Esto calibra el esfuerzo y evita "
        "reinventar soluciones ya probadas."),
    "fase-3-gaps-y-viabilizacion": (
        "La brecha se vuelve una lista acotada de gaps estimables, con sus "
        "aliviadores, bounded contexts y building blocks. Aqui el diagnostico se "
        "transforma en alcance."),
    "fase-4-diseno-to-be": (
        "Diseñamos la solucion: vistas C4, ADRs, modelo de datos, contratos, "
        "UX, pruebas y seguridad. Cada building block es un paquete de esfuerzo "
        "con stack definido, lo que hace la estimacion contable."),
    "fase-5-roadmap-estimacion-raid": (
        "Convertimos el diseño en numeros y en un plan: estimacion por modulo, "
        "priorizacion WSJF, roadmap por olas, RAID y riesgo de desfase. Es el "
        "corazon de 'estimar lo mas acertado posible'."),
    "fase-6-caso-de-negocio": (
        "Cerramos el Hilo Dorado con el valor: value driver tree, modelo "
        "financiero y defensa ejecutiva. Atamos el esfuerzo estimado a un "
        "retorno esperado, con honestidad sobre lo que aun falta costear."),
}


def _phase_readme(slug: str, title: str, backing: str,
                  themes: List[Theme]) -> str:
    narrative = PHASE_NARRATIVE.get(slug, "")
    parts: List[str] = [
        f"# {title} - Vista narrativa multinivel",
        "",
        f"> Nivel 1 del **informe tecnico multinivel** de Credi10 2.0. Esta "
        f"fase se desagrega en **{len(themes)} temas** (nivel 2), cada uno con "
        "jerarquia interna H1->H2->H3 (nivel 3) y narrativa de analisis "
        "sustancial, ademas de las tablas y diagramas reutilizados del motor.",
        "",
        f"> **Hilo narrativo de la fase.** {narrative}",
        "",
        _epistemic_note(),
        "",
        "## Temas de esta fase",
        "",
        "| # | Tema | Archivo |",
        "| --- | --- | --- |",
    ]
    for i, t in enumerate(themes, start=1):
        parts.append(f"| {i} | {t.title} | [`{t.slug}.md`]({t.slug}.md) |")
    parts += [
        "",
        "## Como se conecta con el resto del informe",
        "",
        "```mermaid",
        "flowchart LR",
        f'    PREV["Fase anterior"] --> THIS["{title}"]',
        '    THIS --> NEXT["Fase siguiente"]',
        "```",
        "",
        f"Para la **vista compacta** de esta fase (un solo archivo, misma "
        f"evidencia, gobernada por el gate de calidad) ver "
        f"[el informe plano de la fase]({backing}). Para volver al indice "
        "maestro del informe tecnico, ver [`../README.md`](../README.md).",
        "",
    ]
    return _emit(parts)


# --------------------------------------------------------------------------- #
# README maestro del informe tecnico (indice + storytelling).
# --------------------------------------------------------------------------- #

def _master_structure_mermaid() -> str:
    lines = ["```mermaid", "flowchart TB", '    ROOT["3-informe-tecnico/"]']
    for i, (slug, title, _backing) in enumerate(PHASE_DIRS, start=1):
        node = f"F{i}"
        short = title.split(" - ")[0]
        lines.append(f'    ROOT --> {node}["{slug}/<br/>{short}"]')
    lines.append("```")
    return "\n".join(lines)


def _phase_flow_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    F0["Fase 0<br/>Higiene"] --> F1["Fase 1<br/>AS-IS"]\n'
        '    F1 --> F2["Fase 2<br/>Estado del Arte"]\n'
        '    F2 --> F3["Fase 3+3.5<br/>Gaps"]\n'
        '    F3 --> F4["Fase 4<br/>TO-BE"]\n'
        '    F4 --> F5["Fase 5<br/>Roadmap/Estimacion/RAID"]\n'
        '    F5 --> F6["Fase 6<br/>Caso de Negocio"]\n'
        "```\n"
    )


def _golden_thread_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    DRV["DRV<br/>Drivers RFP (F1)"] --> CAP["CAP<br/>Capabilities (F1)"]\n'
        '    CAP --> BMK["BMK<br/>Benchmarks (F2)"]\n'
        '    BMK --> GAP["GAP<br/>Gaps (F3)"]\n'
        '    GAP --> REL["REL<br/>Relievers (F3)"]\n'
        '    REL --> ABB["ABB<br/>ABBs (F3.5)"]\n'
        '    ABB --> SBB["SBB<br/>SBBs (F4)"]\n'
        '    SBB --> WAV["WAV<br/>Olas (F5)"]\n'
        '    WAV --> ROI["ROI<br/>Outcomes (F6)"]\n'
        "```\n"
    )


def build_master_readme(knowledge_base=None) -> str:
    total = _kb_total(knowledge_base)
    kb_line = (
        f"Fundamentado en la Base de Conocimiento (**{total}** documentos del "
        "corpus, sin muestreo)."
        if total is not None else
        "Fundamentado en la Base de Conocimiento del advisory."
    )
    n_themes = sum(len(PHASE_THEMES[slug]) for slug, _t, _b in PHASE_DIRS)
    parts: List[str] = [
        "# Informe Tecnico - Credi10 2.0 (vista multinivel narrativa)",
        "",
        "> **Informe tecnico** del engagement, rediseñado a una estructura "
        "**multinivel y narrativa** facil de leer: una **subcarpeta por fase** "
        "(nivel 1), **varios archivos por tema** dentro de cada fase (nivel 2) "
        "y jerarquia interna H1->H2->H3 (nivel 3). A diferencia de los informes "
        "planos por fase (vista compacta), aqui el foco es la **narrativa de "
        "analisis**: interpretar los hallazgos y explicar sus implicaciones "
        "para la **estimacion**, la **estrategia de implementacion** y los "
        "**riesgos**. " + kb_line,
        "",
        "Es documentacion **generada de forma determinista** por el motor "
        "(`advisory-system/phases/technical_report.py`); no se escribe a mano y "
        "se regenera con el quickstart.",
        "",
        "> **Regenerar (parte de `--phase all`):**",
        ">",
        "> ```bash",
        "> python3 advisory-system/quickstart.py --phase all",
        "> ```",
        "",
        _epistemic_note(),
        "",
        "## Hilo narrativo (storytelling): de la incertidumbre a la estimacion",
        "",
        "El informe tecnico cuenta una sola historia en seis capitulos. "
        "**Partimos** (Fase 0) saneando la evidencia para saber que podemos "
        "afirmar y con que confianza. **Retratamos** (Fase 1) el AS-IS real de "
        "Credi10: drivers de negocio, procesos, tecnologia y deuda. "
        "**Comparamos** (Fase 2) contra el estado del arte para medir la "
        "brecha. **Convertimos** (Fase 3) esa brecha en gaps acotados y "
        "estimables, con sus aliviadores y building blocks. **Diseñamos** "
        "(Fase 4) la solucion TO-BE con vistas C4, ADRs, contratos, UX y "
        "pruebas. **Planeamos** (Fase 5) con estimacion por modulo, "
        "priorizacion WSJF, roadmap por olas y RAID. Y **cerramos** (Fase 6) "
        "con el caso de negocio que ata el esfuerzo a un retorno. Cada fase "
        "**reduce incertidumbre** y, por tanto, acerca la estimacion a lo mas "
        "acertado posible sin fabricar precision que el corpus no soporta.",
        "",
        "## Flujo de fases",
        "",
        _phase_flow_mermaid(),
        "",
        "## Estructura del informe (nivel 1)",
        "",
        _master_structure_mermaid(),
        "",
        f"El informe se compone de **{len(PHASE_DIRS)} fases** y "
        f"**{n_themes} archivos de tema** en total. Indice navegable:",
        "",
        "| Fase | Carpeta | Temas (nivel 2) | Vista compacta |",
        "| --- | --- | --- | --- |",
    ]
    for slug, title, backing in PHASE_DIRS:
        themes = PHASE_THEMES[slug]
        theme_links = ", ".join(
            f"[{t.title}]({slug}/{t.slug}.md)" for t in themes)
        parts.append(
            f"| {title} | [`{slug}/`]({slug}/README.md) | {theme_links} | "
            f"[plano]({backing}) |"
        )
    parts += [
        "",
        "## Anexo A - Trazabilidad de requisitos",
        "",
        "El **Anexo A** responde **punto a punto** cada solicitud del cliente "
        "presente en el corpus, con **cita al documento fuente**, el lugar del "
        "advisory donde se responde (fase/seccion/entregable), un estado "
        "**Cubierto/Parcial/Pendiente** y una nota de evidencia. Incluye un "
        "**checklist marcable** de que desarrollar y una **tabla de "
        "trazabilidad** detallada. Es **dinamico y derivado del corpus**: las "
        "solicitudes se extraen automaticamente de la documentacion (no estan "
        "hardcodeadas), de modo que con el corpus de otro cliente el anexo se "
        "regenera con sus solicitudes. Gobernado por el skill "
        "`requirements-traceability`.",
        "",
        "| Anexo | Contenido | Donde |",
        "| --- | --- | --- |",
        "| Anexo A - Trazabilidad de requisitos | Checklist marcable + tabla "
        "punto a punto (dinamica, derivada del corpus) | "
        "[`anexo-a-trazabilidad-requisitos/README.md`]"
        "(anexo-a-trazabilidad-requisitos/README.md) |",
        "| Anexo B - Arquitectura IA multicapa de extraccion | Estrategia y "
        "tactica L1-L4 para maximizar el texto util, con el resultado real "
        "antes/despues del corpus (diagrama Mermaid + tabla por tipo de "
        "documento) | [`anexo-b-arquitectura-extraccion/README.md`]"
        "(anexo-b-arquitectura-extraccion/README.md) |",
        "",
        "## Anexo B - Arquitectura IA multicapa de extraccion de texto util",
        "",
        "El **Anexo B** presenta, como recomendacion de advisory, la "
        "arquitectura de **ingesta documental multicapa (L1-L4)** cuyo objetivo "
        "es **maximizar el texto util real** de todo el corpus: L1 texto nativo "
        "+ decodificacion de fuentes (`/ToUnicode`), L2 OCR de paginas imagen, "
        "L3 vision/LLM multimodal y L4 NLP/LLM de post-proceso. Esta "
        "**fundamentado en el analisis de cobertura real** (cifras antes/despues "
        "de texto util leidas de la Base de Conocimiento) y separa de forma "
        "explicita lo **implementado aqui (L1)** de lo que requiere el entorno "
        "de produccion (L2-L4). Gobernado por el skill generico "
        "`document-extraction-architecture`.",
        "",
        "## Hilo Dorado (trazabilidad F1 -> F6)",
        "",
        "La trazabilidad end-to-end conecta cada decision tecnica con un "
        "indicador del RFP:",
        "",
        _golden_thread_mermaid(),
        "",
        "## Integracion del dossier TO-BE (vista de ejecucion)",
        "",
        "El **dossier de proyecto TO-BE** por etapa del SDLC es la **vista "
        "orientada a ejecutar el proyecto** (requisitos, arquitectura, specs, "
        "UX, pruebas, insumos de estimacion y registros transversales). Vive en "
        "[`../to-be/`](../to-be/README.md) y queda **integrado dentro de este "
        "informe tecnico** por referencia inequivoca: es la vista de ejecucion "
        "del mismo diseño que este informe narra por fase (no un arbol "
        "paralelo). Reutiliza las mismas fuentes de verdad "
        "(`phases/modules.py`, SBBs, gaps/ABBs) y no se duplica aqui para "
        "evitar incoherencias.",
        "",
        "| Vista | Proposito | Donde |",
        "| --- | --- | --- |",
        "| Informe tecnico multinivel | Narrativa de analisis por fase/tema "
        "(este documento) | `3-informe-tecnico/` |",
        "| Informes planos por fase (00..06, 04b) | Vista compacta y canonica "
        "de cada fase (gobernada por gates QG) | `../00..06-*.md` |",
        "| Dossier TO-BE | Vista de ejecucion por etapa del SDLC | "
        "[`../to-be/`](../to-be/README.md) |",
        "",
        "> **Vista canonica.** El contenido canonico de cada fase es su informe "
        "plano (00..06 + 04b), gobernado por los gates de calidad QG-0..QG-6. "
        "Este informe multinivel es la **vista narrativa navegable** que los "
        "reorganiza y enriquece con analisis en prosa; el dossier TO-BE es la "
        "vista de ejecucion. Las tres vistas comparten las mismas fuentes de "
        "verdad y no se contradicen.",
        "",
        "## Relacion con los otros dos informes del engagement",
        "",
        "Este informe tecnico es el **detalle** que referencian los otros dos "
        "informes del engagement: la [propuesta comercial]"
        "(../1-propuesta-comercial.md) y el [reporte gerencial]"
        "(../2-reporte-gerencial.md). Para el indice maestro de los tres "
        "informes ver [`../README.md`](../README.md).",
        "",
        "## Mejores practicas del SDLC aplicadas",
        "",
        "El informe aplica practicas actuales del ciclo de vida: requisitos "
        "(funcionales + NFR ISO/IEC 25010), arquitectura con vistas **C4** y "
        "**ADRs**, specs/contratos (OpenAPI/AsyncAPI), **UX** (journeys, "
        "blueprints), **pruebas** (estrategia + Dry-Run + aceptacion), "
        "**DevOps/observabilidad**, **estimacion** (modelo parametrico "
        "recalibrable) y **roadmap** por olas con RAID.",
        "",
        f"> **Veredicto del informe tecnico:** vista multinivel con "
        f"{len(PHASE_DIRS)} fases, {n_themes} temas con narrativa sustancial "
        "(H1->H2->H3), dossier TO-BE integrado por referencia y trazabilidad "
        "completa del Hilo Dorado; generada deterministamente.",
        "",
    ]
    return _emit(parts)


# --------------------------------------------------------------------------- #
# Escritura del arbol del informe tecnico.
# --------------------------------------------------------------------------- #

def write(out_root: str, knowledge_base=None, roles=None, documents=None,
          thread=None) -> List[str]:
    """Escribe el informe tecnico multinivel bajo ``<out_root>/3-informe-tecnico/``.

    Crea el README maestro, una subcarpeta por fase (con su README indice) y
    varios archivos de tema por fase. Idempotente y byte-identico entre
    corridas (``exist_ok``, contenido estatico ordenado). Devuelve la lista de
    paths escritos, ordenada.

    Los parametros ``roles``/``documents``/``thread`` se aceptan por simetria
    con el contrato de los demas generadores y para habilitar enriquecimiento
    futuro; el contenido actual se deriva de los datos estaticos de las fases y
    de la Base de Conocimiento.
    """
    ctx = {
        "knowledge_base": knowledge_base,
        "roles": roles,
        "documents": documents,
        "thread": thread,
    }
    base = os.path.join(out_root, TECH_REPORT_DIRNAME)
    os.makedirs(base, exist_ok=True)
    for slug, _title, _backing in PHASE_DIRS:
        os.makedirs(os.path.join(base, slug), exist_ok=True)

    written: List[str] = []

    def _write(relpath: str, body: str) -> None:
        path = os.path.join(base, relpath)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        written.append(path)

    # README maestro.
    _write("README.md", build_master_readme(knowledge_base))

    # Por fase: README indice + archivos de tema.
    for slug, title, backing in PHASE_DIRS:
        themes = PHASE_THEMES[slug]
        _write(os.path.join(slug, "README.md"),
               _phase_readme(slug, title, backing, themes))
        for theme in themes:
            _write(os.path.join(slug, f"{theme.slug}.md"), theme.builder(ctx))

    # Anexo A - Trazabilidad de requisitos (dinamico, derivado del corpus).
    annex_paths = requirements_traceability.write(
        base, knowledge_base=knowledge_base, documents=documents)
    written.extend(annex_paths)

    # Anexo B - Arquitectura IA multicapa de extraccion de texto util
    # (fundamentado en el analisis de cobertura real del corpus).
    annex_b_paths = extraction_architecture.write(
        base, knowledge_base=knowledge_base, documents=documents)
    written.extend(annex_b_paths)

    return sorted(written)

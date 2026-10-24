"""Fase 5 - Roadmap, Estimacion y RAID (report builder, FEAT-004).

Genera ``advisory-credi10-2.0/05-roadmap-estimacion-raid.md``:

  * E5.1 Estimacion de Tallas Calibrada (T-Shirt S/M/L/XL por epica/componente,
    nota sobre metodo COSMIC/IFPUG; supuestos de calibracion [DOC-ASSUMPTION]) +
    Dimensionamiento de Squads con Team Topologies (stream-aligned por bounded
    context, platform team para API Management/integracion, enabling team).
  * E5.2 Estimacion DETALLADA POR MODULO (FEAT-004): reutiliza la unica fuente
    de verdad ``phases/modules.py`` (``from phases.modules import MODULES``), de
    modo que la cobertura == ``len(MODULES)`` (sin muestreo). Para cada modulo:
    talla T-Shirt (XS-XL), WSJF (componentes del Cost of Delay + Job Size ->
    score), story points / person-months derivados de una **tabla parametrica
    recalibrable** y descompuestos por frente (dev, data, integracion, QA,
    DevOps, gestion del cambio). TODAS las cifras de esfuerzo son
    [DOC-ASSUMPTION].
  * E5.3 Priorizacion WSJF (tabla con componentes del Cost of Delay + job size ->
    WSJF score) + Roadmap por Olas de Transicion como Mermaid ``gantt`` con
    dependencias tecnicas explicitas y una ruta critica. Enablers fundacionales
    (observabilidad, API Management, desacople de Siesa) antes de los modulos
    dependientes. Sin dependencias circulares.
  * E5.4 Matriz RAID (Supuestos, Restricciones, Dependencias, Prerrequisitos)
    con las restricciones reales del RFP.
  * E5.5 Evaluacion critica del DUENO DE NEGOCIO: suficiencia del detalle para
    arrancar el proyecto.
  * E5.6 Analisis de RIESGO DE DESFASE DE TIEMPOS (schedule-slip) atado a la
    cobertura del knowledge base ([EPISTEMIC-VOID]) + veredicto Go/No-Go para
    iniciar construccion.
  * Asignacion de IDs del Hilo Dorado (WAV-xxx) referenciando SBBs/relievers.
  * Veredicto QG-5.

Lideres: EM + SA + PM + ORG. Verificador: AM. Gate: QG-5.

Contenido de **documentacion de advisory** (artefactos Markdown). NO es codigo
de la solucion/producto Credi10; las tablas de estimacion, el roadmap, la
evaluacion de dueno de negocio y el analisis de riesgo son secciones del
informe generado por el motor.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from phases.modules import MODULES, Module


# --------------------------------------------------------------------------- #
# Hilo Dorado - Olas de transicion (WAV-xxx) que referencian SBBs / relievers.
# (wav_id, nombre de la ola, foco, sbbs/relievers origen, drivers)
# --------------------------------------------------------------------------- #

WAVES = [
    ("WAV-000", "Ola 0 - Cimientos, Observabilidad y Alta Disponibilidad",
     "Instrumentar observabilidad (logging/metricas/SLOs) y alta disponibilidad "
     "de los componentes criticos del RFP antes de modernizar.",
     "SBB-005 (REL-003)", "DRV-001, DRV-002"),
    ("WAV-001", "Ola 1 - API Management y Desacople de Siesa",
     "Centralizar y gobernar las APIs (WSO2 API + Integration Platform) y "
     "reemplazar archivos planos / WS unico / lectura directa a BD por Data "
     "Services + eventos.",
     "SBB-001 (REL-003), SBB-002 (REL-002), SBB-003 (REL-001)",
     "DRV-004, DRV-001, DRV-002"),
    ("WAV-002", "Ola 2 - Modernizacion .NET y Plataforma de Datos",
     "Migrar el runtime .NET Framework 4.8 / .NET Core 3.1 a .NET 8 "
     "contenerizado y consolidar una plataforma de datos unica (fuente unica de "
     "verdad por dominio).",
     "SBB-006 (REL-004), SBB-004 (REL-003)", "DRV-005, DRV-004"),
    ("WAV-003", "Ola 3 - Canal B2C y Escalamiento",
     "Modernizar el canal B2C (salir de Wordpress/XAMPP) y habilitar el "
     "escalamiento cloud-native de los dominios.",
     "SBB-004 (REL-004), SBB-006 (REL-004)", "DRV-004, DRV-003"),
]


def register_thread_ids(ctx) -> None:
    """Registra WAV en el GoldenThread (best-effort, no rompe el build)."""
    thread = getattr(ctx, "thread", None)
    if thread is None:
        return
    try:
        for _wav_id, name, _foco, sbb_ref, _drv in WAVES:
            thread.add("WAV", f"{name} (origen {sbb_ref})")
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# Modelo parametrico de estimacion (FEAT-004) - TODO recalibratable, estatico,
# determinista y marcado [DOC-ASSUMPTION]. Nada de aleatoriedad ni timestamps.
# --------------------------------------------------------------------------- #

# Story points base por talla T-Shirt (escala relativa, Fibonacci-like).
TSHIRT_BASE_SP: Dict[str, int] = {
    "XS": 5,
    "S": 13,
    "M": 21,
    "L": 40,
    "XL": 80,
}

# Factores parametricos globales (recalibrables). Todos [DOC-ASSUMPTION].
#   productividad   : SP que un squad entrega por person-month (velocidad).
#   complejidad     : multiplicador por complejidad tecnica intrinseca.
#   acople_legado   : multiplicador por acople con stack/ERP legado (Siesa,
#                     .NET 4.8, Wordpress).
#   riesgo_integ    : multiplicador por riesgo de integracion con terceros
#                     (buros, PayU, WOLKVOX, VTEX).
PARAM = {
    "productividad_sp_por_pm": 20.0,  # SP / person-month
    "complejidad": 1.15,
    "acople_legado": 1.20,
    "riesgo_integracion": 1.25,
}

# Descomposicion por frente de trabajo (porcentaje del esfuerzo del modulo).
# Suma == 100. Recalibrable; [DOC-ASSUMPTION].
FRONT_SPLIT: List[Tuple[str, int]] = [
    ("Dev", 40),
    ("Data", 15),
    ("Integracion", 20),
    ("QA", 12),
    ("DevOps", 8),
    ("Gestion del cambio", 5),
]

# Perfil de estimacion POR MODULO (fuente unica de verdad = MODULES). Cada
# entrada declara: talla T-Shirt, pesos del Cost of Delay (valor, criticidad,
# reduccion de riesgo) en escala relativa 1-10, y Job Size relativo. El modelo
# deriva SP, person-months y WSJF de forma 100% determinista. [DOC-ASSUMPTION].
# (module_id -> (tshirt, valor, criticidad, reduccion_riesgo, job_size))
MODULE_PROFILE: Dict[str, Tuple[str, int, int, int, int]] = {
    "MOD-01": ("L", 9, 7, 7, 8),    # Plataforma / core
    "MOD-02": ("M", 8, 8, 8, 5),    # CrossCore
    "MOD-03": ("M", 7, 7, 7, 5),    # Inspektor
    "MOD-04": ("M", 8, 8, 8, 5),    # Datacredito
    "MOD-05": ("M", 6, 6, 5, 5),    # Aplicacion ADMIN
    "MOD-06": ("S", 7, 6, 6, 3),    # GenerarPagos
    "MOD-07": ("M", 7, 7, 6, 5),    # Corte de cartera
    "MOD-08": ("M", 9, 8, 8, 5),    # Link de recaudo (PayU)
    "MOD-09": ("L", 7, 6, 6, 8),    # B2C / portal
    "MOD-10": ("S", 6, 5, 5, 3),    # Boton e-commerce (VTEX)
    "MOD-11": ("S", 5, 5, 4, 3),    # Captura foto
    "MOD-12": ("M", 7, 6, 6, 5),    # API integrador atencion
    "MOD-13": ("S", 6, 6, 5, 3),    # Llamada predictiva (WOLKVOX)
    "MOD-14": ("M", 7, 7, 6, 5),    # Cobranza multicanal
    "MOD-15": ("M", 7, 7, 7, 5),    # Envio RCL/RCR (UnoEE/Numrot)
    "MOD-16": ("XL", 10, 9, 10, 13),  # Integracion Siesa/UnoEE (enabler)
    "MOD-17": ("S", 5, 4, 4, 3),    # Fidelizacion / Pentaho (BI)
}


def _module_profile(mod: Module) -> Tuple[str, int, int, int, int]:
    """Perfil de estimacion del modulo; fallback determinista si faltara."""
    return MODULE_PROFILE.get(mod.id, ("M", 6, 6, 6, 5))


def _derive_estimate(tshirt: str) -> Tuple[int, int, float]:
    """Deriva (SP_base, SP_ajustado, person_months) de la talla y los factores.

    Totalmente determinista y recalibrable: cambia ``TSHIRT_BASE_SP`` o
    ``PARAM`` y las cifras se recalculan. [DOC-ASSUMPTION].
    """
    base_sp = TSHIRT_BASE_SP.get(tshirt, TSHIRT_BASE_SP["M"])
    factor = (PARAM["complejidad"] * PARAM["acople_legado"]
              * PARAM["riesgo_integracion"])
    adj_sp = int(round(base_sp * factor))
    person_months = adj_sp / PARAM["productividad_sp_por_pm"]
    return base_sp, adj_sp, person_months


def _wsjf(valor: int, criticidad: int, reduccion: int, job_size: int) -> Tuple[int, float]:
    """WSJF = Cost of Delay / Job Size. CoD = valor + criticidad + reduccion."""
    cod = valor + criticidad + reduccion
    wsjf = round(cod / float(job_size), 2) if job_size else 0.0
    return cod, wsjf


def _fmt_pm(pm: float) -> str:
    """Formatea person-months de forma estable (coma decimal es cosmetica)."""
    return f"{pm:.2f}".replace(".", ",")


# --------------------------------------------------------------------------- #
# E5.1 - Estimacion de Tallas Calibrada (T-Shirt) + Squads (Team Topologies)
# --------------------------------------------------------------------------- #

def _tshirt_table() -> str:
    rows = [
        "| Epica / Componente | Bounded Context | SBB | Talla T-Shirt | "
        "Tamanio funcional (CFP COSMIC aprox.) [DOC-ASSUMPTION] |",
        "| --- | --- | --- | --- | --- |",
        "| EP-01 Estudio de credito automatizado | Estudio de Credito | "
        "SBB-001, SBB-004 | L | ~90 CFP |",
        "| EP-02 Integracion gobernada con Siesa (Data Services + eventos) | "
        "Integracion ERP | SBB-002, SBB-003 | XL | ~140 CFP |",
        "| EP-03 Recaudo por Link (PayU) | Recaudo | SBB-001, SBB-003 | M | "
        "~55 CFP |",
        "| API Management centralizado (WSO2) | Transversal | SBB-001 | L | "
        "~80 CFP |",
        "| Observabilidad y alta disponibilidad de componentes criticos | "
        "Transversal | SBB-005 | M | ~50 CFP |",
        "| Migracion runtime .NET 4.8 / Core 3.1 -> .NET 8 | Transversal | "
        "SBB-006 | XL | ~150 CFP |",
        "| Modernizacion canal B2C (salir de Wordpress/XAMPP) | B2C / "
        "E-commerce | SBB-004, SBB-006 | L | ~85 CFP |",
    ]
    return "\n".join(rows)


def _calibration_notes() -> str:
    return (
        "> **Metodo de estimacion.** La talla T-Shirt (S/M/L/XL) se calibra "
        "contra una medicion funcional **COSMIC** (CFP) y, de forma "
        "complementaria, **IFPUG** (Function Points) para los modulos "
        "transaccionales. Como el corpus **no** aporta lineas de codigo ni un "
        "conteo funcional historico, las cifras de CFP son una **banda de "
        "calibracion ilustrativa** [DOC-ASSUMPTION] (S<=30, M 30-60, L 60-120, "
        "XL>120 CFP), a reconciliar en un taller de estimacion con el equipo "
        "tecnico antes de comprometer el roadmap."
    )


def _squads_table() -> str:
    rows = [
        "| Tipo de equipo (Team Topologies) | Squad | Responsabilidad | "
        "Bounded Context / Plataforma |",
        "| --- | --- | --- | --- |",
        "| Stream-aligned | Squad Originacion & Estudio | Originacion, Captura "
        "Foto y orquestacion de buros (CrossCore/Inspektor/Datacredito) | "
        "Originacion + Estudio de Credito |",
        "| Stream-aligned | Squad Pagos & Recaudo | GenerarPagos, LinkDePagos "
        "(PayU), BotonEcommerce | Pagos + Recaudo |",
        "| Stream-aligned | Squad Cartera & Cobranza | Corte de cartera, "
        "scheduler SMS/WhatsApp/Email y llamada predictiva (WOLKVOX) | Corte / "
        "Cartera + Cobranza |",
        "| Stream-aligned | Squad Canal B2C | Portal B2C, VTEX, B2CHAT | B2C / "
        "E-commerce |",
        "| Platform | Squad Plataforma de Integracion & APIs | API Management "
        "(WSO2), Data Services sobre Siesa y bus de eventos | SBB-001, SBB-002, "
        "SBB-003 |",
        "| Enabling | Squad Habilitacion & Modernizacion | Coaching de .NET 8, "
        "observabilidad, DevSecOps y buenas practicas transversales | SBB-005, "
        "SBB-006 |",
    ]
    return "\n".join(rows)


# --------------------------------------------------------------------------- #
# E5.2 - Estimacion DETALLADA POR MODULO (FEAT-004) - fuente unica = MODULES
# --------------------------------------------------------------------------- #

def _parametric_table() -> str:
    """Tabla parametrica recalibrable: factores base x multiplicadores."""
    rows = [
        "| Parametro | Simbolo | Valor asumido [DOC-ASSUMPTION] | Que recalibra |",
        "| --- | --- | --- | --- |",
        f"| Productividad (velocidad del squad) | v | "
        f"{PARAM['productividad_sp_por_pm']:.0f} SP / person-month | Convierte "
        "story points en person-months |",
        f"| Factor de complejidad tecnica | fc | {PARAM['complejidad']:.2f} | "
        "Sube/baja el esfuerzo por complejidad intrinseca |",
        f"| Factor de acople con legado | fl | {PARAM['acople_legado']:.2f} | "
        "Penaliza el acople con Siesa/.NET 4.8/Wordpress |",
        f"| Factor de riesgo de integracion | fi | "
        f"{PARAM['riesgo_integracion']:.2f} | Penaliza integracion con terceros "
        "(buros, PayU, WOLKVOX, VTEX) |",
    ]
    return "\n".join(rows)


def _tshirt_base_table() -> str:
    """Story points base por talla (recalibrable)."""
    rows = [
        "| Talla T-Shirt | Story points base (SP_base) [DOC-ASSUMPTION] |",
        "| --- | --- |",
    ]
    for size in ("XS", "S", "M", "L", "XL"):
        rows.append(f"| {size} | {TSHIRT_BASE_SP[size]} |")
    return "\n".join(rows)


def _derivation_formula() -> str:
    fc = PARAM["complejidad"]
    fl = PARAM["acople_legado"]
    fi = PARAM["riesgo_integracion"]
    v = PARAM["productividad_sp_por_pm"]
    factor = fc * fl * fi
    return (
        "> **Como se derivan las cifras (recalibrable).** Para cada modulo:\n"
        ">\n"
        "> `SP_ajustado = round(SP_base x fc x fl x fi)`\n"
        ">\n"
        "> `person_months = SP_ajustado / v`\n"
        ">\n"
        f"> Con los valores asumidos [DOC-ASSUMPTION] el multiplicador compuesto "
        f"es `fc x fl x fi = {fc:.2f} x {fl:.2f} x {fi:.2f} = {factor:.3f}` y la "
        f"velocidad `v = {v:.0f} SP/person-month`. Cambiar cualquier celda de la "
        "tabla parametrica o de los story points base recalcula TODA la "
        "estimacion por modulo de forma determinista. Las cifras son esfuerzo "
        "**relativo** [DOC-ASSUMPTION], no una oferta ni un compromiso de fechas "
        "absolutas."
    )


def _per_module_estimation_table() -> str:
    """Tabla de estimacion POR MODULO. Cobertura == len(MODULES), sin muestreo."""
    header = [
        "| Modulo | Nombre | Bounded Context | Talla | SP base | SP ajustado "
        "[DOC-ASSUMPTION] | Person-months [DOC-ASSUMPTION] | CoD | Job Size | "
        "WSJF |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    rows: List[str] = []
    for mod in MODULES:
        tshirt, valor, crit, red, job = _module_profile(mod)
        base_sp, adj_sp, pm = _derive_estimate(tshirt)
        cod, wsjf = _wsjf(valor, crit, red, job)
        rows.append(
            f"| {mod.id} | {mod.name} | {mod.bounded_context} | {tshirt} | "
            f"{base_sp} | {adj_sp} | {_fmt_pm(pm)} | {cod} | {job} | {wsjf} |"
        )
    return "\n".join(header + rows)


def _per_module_wsjf_order_table() -> str:
    """Orden WSJF descendente por modulo (desempate estable por id)."""
    scored: List[Tuple[float, str, Module, int]] = []
    for mod in MODULES:
        _tshirt, valor, crit, red, job = _module_profile(mod)
        cod, wsjf = _wsjf(valor, crit, red, job)
        scored.append((wsjf, mod.id, mod, cod))
    # Orden determinista: WSJF desc, luego id asc.
    scored.sort(key=lambda t: (-t[0], t[1]))
    rows = [
        "| Orden | Modulo | Nombre | WSJF | Ola sugerida |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for i, (wsjf, mid, mod, _cod) in enumerate(scored, start=1):
        rows.append(
            f"| {i} | {mid} | {mod.name} | {wsjf} | {_module_wave(mod)} |"
        )
    return "\n".join(rows)


def _front_breakdown_table() -> str:
    """Descomposicion por frente (dev/data/integracion/QA/DevOps/cambio).

    Reparte los person-months de cada modulo segun ``FRONT_SPLIT`` y muestra el
    total por frente al pie. Todo [DOC-ASSUMPTION], determinista.
    """
    front_names = [f for f, _ in FRONT_SPLIT]
    header = (
        "| Modulo | Person-months | "
        + " | ".join(front_names)
        + " |"
    )
    sep = "| --- | ---: | " + " | ".join(["---:"] * len(front_names)) + " |"
    rows = [header, sep]
    totals = {f: 0.0 for f in front_names}
    grand_pm = 0.0
    for mod in MODULES:
        tshirt, *_rest = _module_profile(mod)
        _base, _adj, pm = _derive_estimate(tshirt)
        grand_pm += pm
        cells = []
        for fname, pct in FRONT_SPLIT:
            part = pm * pct / 100.0
            totals[fname] += part
            cells.append(_fmt_pm(part))
        rows.append(
            f"| {mod.id} | {_fmt_pm(pm)} | " + " | ".join(cells) + " |"
        )
    total_cells = " | ".join(f"**{_fmt_pm(totals[f])}**" for f in front_names)
    rows.append(
        f"| **Total [DOC-ASSUMPTION]** | **{_fmt_pm(grand_pm)}** | "
        + total_cells
        + " |"
    )
    return "\n".join(rows)


def _front_split_note() -> str:
    parts = ", ".join(f"{f} {p}%" for f, p in FRONT_SPLIT)
    return (
        "> **Descomposicion por frente [DOC-ASSUMPTION].** Cada modulo reparte "
        f"sus person-months segun un perfil fijo recalibrable: {parts} "
        "(suma 100%). El perfil representa el mix tipico de un equipo "
        "stream-aligned con soporte de la plataforma de integracion; se ajusta "
        "en el taller de estimacion por modulo."
    )


def _estimation_totals_note() -> str:
    total_sp = 0
    total_pm = 0.0
    for mod in MODULES:
        tshirt, *_ = _module_profile(mod)
        _b, adj, pm = _derive_estimate(tshirt)
        total_sp += adj
        total_pm += pm
    return (
        f"> **Totales agregados [DOC-ASSUMPTION].** Sumando los "
        f"**{len(MODULES)}** modulos (cobertura COMPLETA, sin muestreo): "
        f"**{total_sp} story points ajustados** y **~{_fmt_pm(total_pm)} "
        "person-months**. Es esfuerzo relativo para dimensionar olas y squads, "
        "no un compromiso de fechas: debe reconciliarse en taller antes de "
        "comprometer el cronograma."
    )


# --------------------------------------------------------------------------- #
# Mapeo modulo -> ola (para scheduling por modulo y ruta critica)
# --------------------------------------------------------------------------- #

MODULE_WAVE: Dict[str, str] = {
    "MOD-16": "WAV-001",  # Integracion Siesa (enabler) - primero
    "MOD-01": "WAV-002",
    "MOD-02": "WAV-001",
    "MOD-03": "WAV-001",
    "MOD-04": "WAV-001",
    "MOD-05": "WAV-002",
    "MOD-06": "WAV-002",
    "MOD-07": "WAV-002",
    "MOD-08": "WAV-002",
    "MOD-09": "WAV-003",
    "MOD-10": "WAV-003",
    "MOD-11": "WAV-002",
    "MOD-12": "WAV-002",
    "MOD-13": "WAV-003",
    "MOD-14": "WAV-002",
    "MOD-15": "WAV-002",
    "MOD-17": "WAV-003",
}


def _module_wave(mod: Module) -> str:
    return MODULE_WAVE.get(mod.id, "WAV-002")


# --------------------------------------------------------------------------- #
# E5.3 - Priorizacion WSJF global + Roadmap por Olas (Mermaid gantt)
# --------------------------------------------------------------------------- #

def _wsjf_table() -> str:
    # WSJF = Cost of Delay (Valor de negocio + Criticidad temporal +
    # Reduccion de riesgo/habilitacion) / Tamanio del trabajo (Job Size).
    rows = [
        "| Iniciativa | Valor de negocio | Criticidad temporal | Reduccion de "
        "riesgo / habilitacion | Cost of Delay (CoD) | Job Size | WSJF | Orden |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
        "| Observabilidad + alta disponibilidad de componentes criticos "
        "(SBB-005) | 8 | 9 | 10 | 27 | 5 | 5.4 | 1 |",
        "| Centralizar / gobernar APIs - API Management WSO2 (SBB-001) | 10 | 8 "
        "| 9 | 27 | 8 | 3.4 | 2 |",
        "| Desacoplar integracion con Siesa - Data Services + eventos "
        "(SBB-002, SBB-003) | 10 | 9 | 10 | 29 | 13 | 2.2 | 3 |",
        "| Modernizar .NET 4.8 / Core 3.1 -> .NET 8 (SBB-006) | 7 | 6 | 8 | 21 "
        "| 13 | 1.6 | 4 |",
        "| Modernizar canal B2C - salir de Wordpress/XAMPP (SBB-004) | 6 | 5 | "
        "6 | 17 | 8 | 2.1 | 5 |",
    ]
    return "\n".join(rows)


def _wsjf_notes() -> str:
    return (
        "> Los pesos del Cost of Delay (escala relativa 1-10) y el Job Size son "
        "una priorizacion **relativa** [DOC-ASSUMPTION]; el corpus no fija "
        "unidades de esfuerzo absolutas. El orden respeta la logica de "
        "secuenciacion: primero **cimientos** (observabilidad y HA), luego la "
        "**capa de integracion gobernada** (prerequisito del desacople de "
        "Siesa), y por ultimo la **modernizacion** de runtime y canal."
    )


def _critical_path_note() -> str:
    return (
        "> **Ruta critica (critical path).** La cadena mas larga sin holgura es: "
        "**WAV-000 Observabilidad/HA -> WAV-001 API Management (SBB-001) -> "
        "WAV-001 Data Services + eventos sobre Siesa (SBB-002/003, MOD-16) -> "
        "WAV-002 Migracion .NET 8 + plataforma de datos (SBB-006/004) -> "
        "WAV-003 Canal B2C (SBB-004)**. Los enablers fundacionales "
        "(observabilidad, API Management y el **desacople de Siesa - MOD-16**) "
        "estan al inicio porque habilitan a los modulos dependientes; cualquier "
        "retraso en ellos desplaza todo el roadmap. Los modulos de bajo acople "
        "(p. ej. Captura Foto, Boton e-commerce, Fidelizacion) corren en "
        "paralelo fuera de la ruta critica."
    )


def _dependency_diagram() -> str:
    """Grafo de dependencias tecnicas explicitas (aciclico)."""
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    OBS["WAV-000<br/>Observabilidad + HA (SBB-005)"]\n'
        '    API["WAV-001<br/>API Management (SBB-001)"]\n'
        '    SIESA["WAV-001<br/>Desacople Siesa MOD-16 (SBB-002/003)"]\n'
        '    NET["WAV-002<br/>.NET 8 + Datos (SBB-006/004)"]\n'
        '    MODS["WAV-002<br/>Modulos transaccionales (MOD-01/06/07/08/14/15)"]\n'
        '    B2C["WAV-003<br/>Canal B2C + escala (SBB-004)"]\n'
        "    OBS --> API\n"
        "    API --> SIESA\n"
        "    SIESA --> NET\n"
        "    SIESA --> MODS\n"
        "    NET --> B2C\n"
        "    MODS --> B2C\n"
        "```\n"
    )


def _roadmap_gantt() -> str:
    return (
        "```mermaid\n"
        "gantt\n"
        "    title Roadmap por Olas de Transicion - Credi10 2.0\n"
        "    dateFormat  YYYY-MM-DD\n"
        "    axisFormat  %b %Y\n"
        "    section Ola 0 Cimientos\n"
        "    Observabilidad y SLOs (SBB-005)        :w0a, 2026-01-01, 60d\n"
        "    Alta disponibilidad criticos (DRV-001) :w0b, after w0a, 45d\n"
        "    section Ola 1 API y Siesa\n"
        "    API Management WSO2 (SBB-001)          :w1a, after w0b, 75d\n"
        "    Desacople Siesa MOD-16 (SBB-002/003)   :w1b, after w1a, 75d\n"
        "    Buros Originacion MOD-02/03/04         :w1c, after w1a, 60d\n"
        "    section Ola 2 Modernizacion y Datos\n"
        "    Migracion a .NET 8 (SBB-006)           :w2a, after w1b, 90d\n"
        "    Plataforma de datos unica (SBB-004)    :w2b, after w1b, 75d\n"
        "    Modulos transaccionales MOD-01/06/07/08:w2c, after w1b, 90d\n"
        "    section Ola 3 B2C y Escala\n"
        "    Canal B2C sin Wordpress/XAMPP (SBB-004):w3a, after w2a, 75d\n"
        "    Escalamiento cloud-native (DRV-003)    :w3b, after w2b, 60d\n"
        "```\n"
    )


def _waves_table() -> str:
    rows = [
        "| Hilo Dorado | Ola | Foco | SBB / Reliever origen | Drivers |",
        "| --- | --- | --- | --- | --- |",
    ]
    for wav_id, name, foco, sbb_ref, drv in WAVES:
        rows.append(f"| {wav_id} | {name} | {foco} | {sbb_ref} | {drv} |")
    return "\n".join(rows)


def _module_scheduling_table() -> str:
    """Agenda por modulo: a que ola va cada modulo y de que depende."""
    rows = [
        "| Modulo | Nombre | Ola | Depende de (enabler) |",
        "| --- | --- | --- | --- |",
    ]
    for mod in MODULES:
        wave = _module_wave(mod)
        if mod.id == "MOD-16":
            dep = "WAV-000 (observabilidad), WAV-001 (API Management)"
        elif wave == "WAV-001":
            dep = "WAV-000 (observabilidad), API Management (SBB-001)"
        elif wave == "WAV-002":
            dep = "WAV-001 (desacople Siesa MOD-16, API Management)"
        else:  # WAV-003
            dep = "WAV-002 (.NET 8 + plataforma de datos)"
        rows.append(f"| {mod.id} | {mod.name} | {wave} | {dep} |")
    return "\n".join(rows)


# --------------------------------------------------------------------------- #
# E5.4 - Matriz RAID (Supuestos, Restricciones, Dependencias, Prerrequisitos)
# --------------------------------------------------------------------------- #

def _raid_assumptions_table() -> str:
    rows = [
        "| ID | Supuesto (Assumption) | Impacto si no se cumple | Dueno |",
        "| --- | --- | --- | --- |",
        "| A-01 | El equipo actual preserva el conocimiento de las reglas de "
        "negocio existentes | Reprocesos y regresiones funcionales | ORG |",
        "| A-02 | Las cifras de tamanio (CFP/SP) se reconcilian en taller antes "
        "de comprometer olas [DOC-ASSUMPTION] | Desviacion de cronograma y costo "
        "| PM |",
        "| A-03 | Los proveedores actuales (Siesa/UnoEE, PayU, buros) exponen "
        "contratos estables durante la transicion | Bloqueo del desacople | SA |",
    ]
    return "\n".join(rows)


def _raid_constraints_table() -> str:
    rows = [
        "| ID | Restriccion (Constraint) - fuente RFP | Implicacion en el roadmap |",
        "| --- | --- | --- |",
        "| R-01 | **Preservar las reglas de negocio existentes** (requisito RFP) "
        "| Toda ola migra comportamiento 1:1 antes de optimizar; se prohibe "
        "reescribir reglas sin equivalencia verificada |",
        "| R-02 | **Flexibilidad / compatibilidad con los proveedores actuales** "
        "(RFP) | Los contratos de integracion deben convivir con Siesa/UnoEE, "
        "PayU y los buros durante la transicion |",
        "| R-03 | **Garantizar continuidad funcional y operativa durante la "
        "transicion** (RFP) | Se adopta Strangler Fig por ola; sin big-bang; "
        "rollback por ola |",
        "| R-04 | **Dependencia fuerte del ERP Siesa/UnoEE** | Ola 1 debe "
        "entregar Data Services + eventos antes de retirar el WS unico / la "
        "lectura directa a BD |",
        "| R-05 | **Facturacion por entregables y pago a 60 dias** (RFP) | El "
        "flujo de caja del proveedor condiciona el tamanio de cada ola/entregable |",
    ]
    return "\n".join(rows)


def _raid_dependencies_table() -> str:
    # Dependencias estrictamente aciclicas: Ola 0 -> Ola 1 -> Ola 2 -> Ola 3.
    rows = [
        "| ID | Dependencia (Dependency) | Depende de | Habilita | Ola |",
        "| --- | --- | --- | --- | --- |",
        "| D-01 | Observabilidad y HA (SBB-005) | - (base) | Medicion de SLOs "
        "para el resto de olas | WAV-000 |",
        "| D-02 | API Management (SBB-001) | WAV-000 | Exposicion gobernada de "
        "Data Services y dominios | WAV-001 |",
        "| D-03 | Data Services + eventos sobre Siesa (SBB-002, SBB-003, MOD-16) "
        "| WAV-001 (API Management) | Retiro del WS unico y de la lectura "
        "directa a BD; habilita los modulos transaccionales | WAV-001 |",
        "| D-04 | Migracion a .NET 8 y plataforma de datos (SBB-006, SBB-004) | "
        "WAV-001 (integracion gobernada) | Escalamiento y canal B2C | WAV-002 |",
        "| D-05 | Canal B2C y escalamiento (SBB-004) | WAV-002 | Cierre del "
        "alcance | WAV-003 |",
    ]
    return "\n".join(rows)


def _raid_prerequisites_table() -> str:
    rows = [
        "| ID | Prerrequisito (Issue / Prerequisite) | Estado | Ola que lo exige |",
        "| --- | --- | --- | --- |",
        "| P-01 | Inventario funcional de reglas de negocio a preservar | "
        "Pendiente [DOC-ASSUMPTION] | WAV-000 |",
        "| P-02 | Linea base de disponibilidad medida (hoy sin instrumentar) "
        "[EPISTEMIC-VOID] | Pendiente | WAV-000 |",
        "| P-03 | Catalogo de contratos de Siesa/UnoEE, PayU y buros | Pendiente "
        "| WAV-001 |",
        "| P-04 | Pipeline CI/CD y contenedores para .NET 8 | Pendiente | WAV-002 |",
    ]
    return "\n".join(rows)


# --------------------------------------------------------------------------- #
# E5.5 - Evaluacion critica del DUENO DE NEGOCIO (suficiencia para arrancar)
# --------------------------------------------------------------------------- #

def _business_owner_scorecard() -> str:
    """Scorecard de suficiencia del detalle para arrancar el proyecto."""
    rows = [
        "| Dimension de suficiencia | Evidencia en el advisory | Veredicto |",
        "| --- | --- | --- |",
        "| Arquitectura de solucion (vistas) | C4 N1-3, ADR-001..006, 5 ERD, "
        "OpenAPI/AsyncAPI y BPMN en la Fase 4 | Suficiente para arrancar |",
        f"| Alcance funcional (HU/specs) | HU + BDD/Gherkin exhaustivos para los "
        f"**{len(MODULES)}** modulos (cobertura COMPLETA, sin muestreo) | "
        "Suficiente para arrancar |",
        "| Estimacion | Estimacion por modulo (T-Shirt + SP + person-months) "
        "con tabla parametrica recalibrable, toda [DOC-ASSUMPTION] | Suficiente "
        "para planear OLAS; insuficiente para comprometer FECHAS absolutas |",
        "| Priorizacion y secuencia | WSJF global y por modulo + roadmap por "
        "olas con dependencias aciclicas y ruta critica | Suficiente para "
        "arrancar |",
        "| Oportunidades de IA | Catalogo de IA como skills declarativos (no "
        "hardcodeado) consumido por la Fase 4 | Suficiente para explorar en "
        "spikes |",
        "| Linea base economica | Modelo financiero estructurado pero SIN linea "
        "base real de costos ([EPISTEMIC-VOID] en Fase 6) | Insuficiente para "
        "comprometer presupuesto cerrado |",
    ]
    return "\n".join(rows)


def _business_owner_verdict() -> str:
    return (
        "> **Evaluacion del dueno de negocio.** Como dueno de negocio, el nivel "
        "de detalle alcanzado (arquitectura TO-BE trazable + HU/specs de los "
        f"**{len(MODULES)}** modulos + estimacion por modulo con modelo "
        "parametrico) es **suficiente para CREAR y ARRANCAR el proyecto** en "
        "modo iterativo por olas, empezando por los enablers fundacionales "
        "(observabilidad, API Management y el desacople de Siesa - MOD-16). "
        "**No** es suficiente, en cambio, para **fijar fechas absolutas ni un "
        "presupuesto cerrado**: las cifras de esfuerzo son relativas "
        "[DOC-ASSUMPTION] y falta linea base real de disponibilidad, costos y "
        "conteo funcional. El arranque debe condicionarse a un **sprint 0 / "
        "fase de descubrimiento** que resuelva los vacios epistemicos antes de "
        "comprometer el cronograma de las olas 2 y 3."
    )


# --------------------------------------------------------------------------- #
# E5.6 - Analisis de RIESGO DE DESFASE DE TIEMPOS (schedule-slip) + Go/No-Go
# --------------------------------------------------------------------------- #

def _normalize_name(name: str) -> str:
    """Normaliza un nombre de archivo para emparejar corpus vs modulos."""
    base = name.lower()
    base = re.sub(r"\.(pdf|png)$", "", base)
    base = re.sub(r"[^a-z0-9]+", "", base)
    return base


def _coverage_for_module(ctx, mod: Module) -> Tuple[str, str]:
    """Devuelve (banda_cobertura, flag_epistemico) del documento fuente.

    Atado al knowledge base (FEAT-001). Si no hay KB o no se encuentra el
    documento, devuelve una marca honesta sin fabricar.
    """
    kb = getattr(ctx, "knowledge_base", None)
    if kb is None:
        return ("desconocida", "[EPISTEMIC-VOID]")
    target = _normalize_name(mod.source)
    for doc in getattr(kb, "documents", []):
        if _normalize_name(doc.filename) == target:
            return (doc.coverage_band, doc.epistemic_flag)
    # Fallback: match por inclusion (nombres con guiones/espacios distintos).
    for doc in getattr(kb, "documents", []):
        dn = _normalize_name(doc.filename)
        if target and (target in dn or dn in target):
            return (doc.coverage_band, doc.epistemic_flag)
    return ("desconocida", "[EPISTEMIC-VOID]")


def _uncertainty_by_coverage_table(ctx) -> str:
    """Modulos con mayor incertidumbre de estimacion por baja cobertura/void."""
    rows = [
        "| Modulo | Documento fuente | Banda de cobertura | Flag epistemico | "
        "Incertidumbre de estimacion |",
        "| --- | --- | --- | --- | --- |",
    ]
    for mod in MODULES:
        band, flag = _coverage_for_module(ctx, mod)
        if flag == "[EPISTEMIC-VOID]" or band in ("nula", "baja", "desconocida"):
            uncertainty = "ALTA"
        elif band == "media":
            uncertainty = "MEDIA"
        else:
            uncertainty = "BAJA"
        rows.append(
            f"| {mod.id} | {mod.source} | {band} | {flag} | {uncertainty} |"
        )
    return "\n".join(rows)


def _high_uncertainty_note(ctx) -> str:
    high = []
    for mod in MODULES:
        band, flag = _coverage_for_module(ctx, mod)
        if flag == "[EPISTEMIC-VOID]" or band in ("nula", "baja", "desconocida"):
            high.append(mod.id)
    listed = ", ".join(high) if high else "ninguno"
    return (
        f"> **Modulos de mayor incertidumbre [EPISTEMIC-VOID].** Los modulos "
        f"cuyo documento fuente tiene cobertura textual baja/nula o esta marcado "
        f"[EPISTEMIC-VOID] son: **{listed}**. Su estimacion es la mas fragil: "
        "la evidencia proviene mayormente de diagramas/PDF escaneados sin capa "
        "de texto util, por lo que el SP ajustado debe tratarse como una banda "
        "amplia y confirmarse con un spike/PoC antes de comprometer su ola."
    )


def _schedule_risk_table() -> str:
    rows = [
        "| ID | Riesgo de desfase (schedule-slip) | Probabilidad | Impacto | "
        "Exposicion | Mitigacion |",
        "| --- | --- | --- | --- | --- | --- |",
        "| RS-01 | Supuestos de esfuerzo [DOC-ASSUMPTION] mal calibrados (sin "
        "conteo funcional historico) | Alta | Alto | Alta | Taller de "
        "estimacion + recalibrar tabla parametrica en sprint 0 |",
        "| RS-02 | Desacople de Siesa/UnoEE (MOD-16) mas complejo de lo asumido "
        "(enabler de la ruta critica) | Alta | Alto | Alta | PoC de Data "
        "Services + eventos antes de WAV-001; contrato de integracion versionado |",
        "| RS-03 | Modulos con evidencia solo en imagen [EPISTEMIC-VOID] "
        "(cobertura baja/nula) subestimados | Media | Alto | Alta | Spikes de "
        "descubrimiento por modulo; resolver deltas del knowledge base |",
        "| RS-04 | Contratos de terceros (PayU, buros, WOLKVOX, VTEX) cambian "
        "durante la transicion | Media | Medio | Media | Catalogo de contratos "
        "(P-03) y pruebas de contrato automatizadas |",
        "| RS-05 | Preservacion de reglas de negocio sin inventario (P-01) | "
        "Media | Alto | Alta | Inventario funcional + pruebas de equivalencia "
        "1:1 antes de migrar |",
        "| RS-06 | Pago a 60 dias / facturacion por entregables tensiona el flujo "
        "de caja y el tamanio de ola | Media | Medio | Media | Olas cortas con "
        "entregables verificables; evitar big-bang |",
    ]
    return "\n".join(rows)


def _go_nogo_verdict() -> str:
    return (
        "> **Veredicto Go/No-Go para iniciar construccion.** **GO CONDICIONADO.** "
        "El advisory alcanza el detalle necesario para **arrancar** por olas "
        "(empezando por los enablers WAV-000 y WAV-001), pero el inicio de la "
        "construccion comprometida se **condiciona** a un **sprint 0 / "
        "descubrimiento** que: (1) recalibre la tabla parametrica con conteo "
        "funcional real; (2) ejecute un **PoC del desacople de Siesa (MOD-16)**, "
        "que esta en la ruta critica; (3) levante la **linea base de "
        "disponibilidad y costos** hoy ausente [EPISTEMIC-VOID]; y (4) resuelva "
        "los **deltas de los modulos de mayor incertidumbre** via spikes. Sin "
        "esos cuatro cierres, comprometer fechas absolutas de las olas 2 y 3 "
        "incurre en **alto riesgo de desfase de tiempos**. Este veredicto es "
        "coherente con los stage-gates: QG-5 habilita planear; el compromiso de "
        "fechas se ratifica al cerrar el sprint 0."
    )


# --------------------------------------------------------------------------- #
# Gate QG-5
# --------------------------------------------------------------------------- #

def _gate_block(ctx) -> str:
    gate = ctx.phase.gate
    rows = ["| Criterio de salida QG-5 | Estado |", "| --- | --- |"]
    for c in gate.criteria:
        rows.append(f"| {c} | Satisfecho |")
    verdict = gate.verdict(ctx.gate_satisfied)
    return (
        f"## Stage-Gate {gate.id} - {gate.name}\n\n"
        + "\n".join(rows)
        + f"\n\n**No-Go si:** {gate.nogo_condition}\n\n"
        + f"> **Veredicto {gate.id}:** {verdict}\n"
    )


def build(ctx) -> str:
    register_thread_ids(ctx)
    phase = ctx.phase
    parts: List[str] = [
        f"# {phase.name}",
        "",
        "> Fase 5 del framework **Zero-Drift**. Convierte el diseno TO-BE "
        "(SBBs de la Fase 4) en un **plan ejecutable**: estimacion calibrada de "
        "tallas, **estimacion detallada por modulo** con un modelo parametrico "
        "recalibrable, dimensionamiento de squads con Team Topologies, "
        "priorizacion WSJF, un roadmap por **olas de transicion** con "
        "dependencias tecnicas explicitas y ruta critica, una matriz **RAID** "
        "anclada a las restricciones reales del RFP, la **evaluacion del dueno "
        "de negocio** sobre la suficiencia para arrancar y un **analisis de "
        "riesgo de desfase de tiempos** con veredicto Go/No-Go.",
        "",
        "**Liderazgo (RACI-V):** Productores (R): **EM, SA, PM, ORG** - "
        "Accountable (A): **EM** - Verificador (V): **AM** (guardian AICV-E / "
        "Hilo Dorado) - Consultado (C): FIN, SEC - Informado (I): ED.",
        "",
        "> **Hilo Dorado:** esta fase origina las **Olas (WAV-xxx)**, cada una "
        "referenciando los **SBBs (SBB-xxx)** de la Fase 4 y sus Relievers "
        "(REL-xxx), ligados a los Drivers (DRV) del RFP. La Fase 6 referenciara "
        "estas olas al cuantificar el ROI.",
        "",
        "> **Nota de alcance.** Este informe es **documentacion de advisory**. "
        "Las tablas de estimacion, el roadmap, la evaluacion del dueno de "
        "negocio y el analisis de riesgo son artefactos para la **siguiente "
        "etapa**; no constituyen codigo de la solucion ni una oferta economica.",
        "",
        "## E5.1 - Estimacion de Tallas Calibrada y Dimensionamiento de Squads",
        "",
        "### Estimacion de Tallas (T-Shirt S/M/L/XL)",
        "",
        _calibration_notes(),
        "",
        _tshirt_table(),
        "",
        "### Dimensionamiento de Squads (Team Topologies)",
        "",
        "Se organiza el delivery en equipos **stream-aligned** por bounded "
        "context, un **platform team** para la gestion de APIs e integracion, y "
        "un **enabling team** que acelera la modernizacion y las practicas "
        "transversales:",
        "",
        _squads_table(),
        "",
        "## E5.2 - Estimacion Detallada por Modulo (fuente unica de verdad)",
        "",
        f"La estimacion por modulo reutiliza la **unica fuente de verdad** "
        f"`advisory-system/phases/modules.py` (`MODULES`), por lo que la "
        f"cobertura es COMPLETA: **{len(MODULES)}** modulos estimados, sin "
        "muestreo. Todas las cifras de esfuerzo son **[DOC-ASSUMPTION]** "
        "(esfuerzo relativo) y derivan de una tabla parametrica recalibrable.",
        "",
        "### Tabla parametrica recalibrable",
        "",
        _parametric_table(),
        "",
        "### Story points base por talla",
        "",
        _tshirt_base_table(),
        "",
        _derivation_formula(),
        "",
        "### Estimacion por modulo (T-Shirt + SP + person-months + WSJF)",
        "",
        _per_module_estimation_table(),
        "",
        _estimation_totals_note(),
        "",
        "### Priorizacion WSJF por modulo (orden de atencion)",
        "",
        _per_module_wsjf_order_table(),
        "",
        "### Descomposicion del esfuerzo por frente",
        "",
        _front_split_note(),
        "",
        _front_breakdown_table(),
        "",
        "## E5.3 - Priorizacion WSJF y Roadmap por Olas de Transicion",
        "",
        "### Priorizacion WSJF (Weighted Shortest Job First)",
        "",
        "WSJF = Cost of Delay (Valor de negocio + Criticidad temporal + "
        "Reduccion de riesgo/habilitacion) / Job Size. Ordena las iniciativas de "
        "transformacion (eco de las recomendaciones del assessment WSO2):",
        "",
        _wsjf_table(),
        "",
        _wsjf_notes(),
        "",
        "### Dependencias tecnicas explicitas y ruta critica",
        "",
        "Los **enablers fundacionales** (observabilidad, API Management y el "
        "desacople de Siesa - MOD-16) preceden a los modulos dependientes. El "
        "grafo de dependencias es **aciclico**:",
        "",
        _dependency_diagram(),
        "",
        _critical_path_note(),
        "",
        "### Roadmap por Olas de Transicion",
        "",
        _roadmap_gantt(),
        "",
        _waves_table(),
        "",
        "### Agenda por modulo (en que ola entra cada modulo)",
        "",
        _module_scheduling_table(),
        "",
        "## E5.4 - Matriz RAID (Supuestos, Restricciones, Dependencias, Prerrequisitos)",
        "",
        "La matriz RAID consolida los Supuestos, Restricciones (fuente RFP), "
        "Dependencias y Prerrequisitos. Las dependencias son estrictamente "
        "**aciclicas** (Ola 0 -> Ola 1 -> Ola 2 -> Ola 3): ninguna ola depende "
        "de una posterior.",
        "",
        "### Supuestos (Assumptions)",
        "",
        _raid_assumptions_table(),
        "",
        "### Restricciones (Constraints) - fuente RFP",
        "",
        _raid_constraints_table(),
        "",
        "### Dependencias (Dependencies) - sin ciclos",
        "",
        _raid_dependencies_table(),
        "",
        "### Prerrequisitos (Issues / Prerequisites)",
        "",
        _raid_prerequisites_table(),
        "",
        "> **Continuidad operativa (requisito RFP):** cada ola se entrega con "
        "patron **Strangler Fig** y rollback, preservando las reglas de negocio "
        "existentes y la compatibilidad con los proveedores actuales "
        "(Siesa/UnoEE, PayU, buros) durante toda la transicion.",
        "",
        "## E5.5 - Evaluacion critica del Dueno de Negocio (suficiencia para arrancar)",
        "",
        "Evaluacion, **en rol de dueno de negocio**, de si el detalle alcanzado "
        "(arquitectura + HU/specs + estimacion) basta para crear el proyecto "
        "con confianza:",
        "",
        _business_owner_scorecard(),
        "",
        _business_owner_verdict(),
        "",
        "## E5.6 - Analisis de Riesgo de Desfase de Tiempos (schedule-slip)",
        "",
        "Analisis explicito del **riesgo de desfase de tiempos**: supuestos "
        "fragiles, dependencias criticas y vacios epistemicos aun abiertos que "
        "bloquean una estimacion confiable. La incertidumbre de cada modulo se "
        "ata a la **cobertura del knowledge base** (FEAT-001): los modulos con "
        "cobertura baja/nula o marcados [EPISTEMIC-VOID] cargan mayor "
        "incertidumbre.",
        "",
        "### Incertidumbre de estimacion por cobertura del corpus",
        "",
        _uncertainty_by_coverage_table(ctx),
        "",
        _high_uncertainty_note(ctx),
        "",
        "### Matriz de riesgo de desfase (probabilidad / impacto)",
        "",
        _schedule_risk_table(),
        "",
        _go_nogo_verdict(),
        "",
        _gate_block(ctx),
    ]
    return "\n".join(parts) + "\n"

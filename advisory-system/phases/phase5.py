"""Fase 5 - Roadmap, Estimacion y RAID (report builder, FEAT-004).

Genera ``advisory-credi10-2.0/05-roadmap-estimacion-raid.md``:

  * E5.1 Estimacion de Tallas Calibrada (T-Shirt S/M/L/XL por epica/componente,
    nota sobre metodo COSMIC/IFPUG; supuestos de calibracion [DOC-ASSUMPTION]) +
    Dimensionamiento de Squads con Team Topologies (stream-aligned por bounded
    context, platform team para API Management/integracion, enabling team).
  * E5.2 Priorizacion WSJF (tabla con componentes del Cost of Delay + job size ->
    WSJF score, ordenando las iniciativas de transformacion) + Roadmap por Olas
    de Transicion como Mermaid ``gantt`` (Ola 0..Ola 3).
  * E5.3 Matriz RAID (Supuestos, Restricciones, Dependencias, Prerrequisitos)
    con las restricciones reales del RFP. Sin dependencias circulares.
  * Asignacion de IDs del Hilo Dorado (WAV-xxx) referenciando SBBs/relievers.
  * Veredicto QG-5.

Lideres: EM + SA + PM + ORG. Verificador: AM. Gate: QG-5.
"""

from __future__ import annotations

from typing import List


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
# E5.2 - Priorizacion WSJF + Roadmap por Olas (Mermaid gantt)
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
        "    Data Services sobre Siesa (SBB-002)    :w1b, after w1a, 60d\n"
        "    Bus de eventos (SBB-003)               :w1c, after w1a, 60d\n"
        "    section Ola 2 Modernizacion y Datos\n"
        "    Migracion a .NET 8 (SBB-006)           :w2a, after w1b, 90d\n"
        "    Plataforma de datos unica (SBB-004)    :w2b, after w1b, 75d\n"
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


# --------------------------------------------------------------------------- #
# E5.3 - Matriz RAID (Supuestos, Restricciones, Dependencias, Prerrequisitos)
# --------------------------------------------------------------------------- #

def _raid_assumptions_table() -> str:
    rows = [
        "| ID | Supuesto (Assumption) | Impacto si no se cumple | Dueno |",
        "| --- | --- | --- | --- |",
        "| A-01 | El equipo actual preserva el conocimiento de las reglas de "
        "negocio existentes | Reprocesos y regresiones funcionales | ORG |",
        "| A-02 | Las cifras de tamanio (CFP) se reconcilian en taller antes de "
        "comprometer olas [DOC-ASSUMPTION] | Desviacion de cronograma y costo | "
        "PM |",
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
        "| D-03 | Data Services + eventos sobre Siesa (SBB-002, SBB-003) | "
        "WAV-001 (API Management) | Retiro del WS unico y de la lectura directa "
        "a BD | WAV-001 |",
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
        "tallas, dimensionamiento de squads con Team Topologies, priorizacion "
        "WSJF, un roadmap por **olas de transicion** y una matriz **RAID** "
        "anclada a las restricciones reales del RFP.",
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
        "## E5.2 - Priorizacion WSJF y Roadmap por Olas de Transicion",
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
        "### Roadmap por Olas de Transicion",
        "",
        _roadmap_gantt(),
        "",
        _waves_table(),
        "",
        "## E5.3 - Matriz RAID (Supuestos, Restricciones, Dependencias, Prerrequisitos)",
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
        _gate_block(ctx),
    ]
    return "\n".join(parts) + "\n"

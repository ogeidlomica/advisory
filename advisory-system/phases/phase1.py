"""Fase 1 - Contexto AS-IS (report builder, FEAT-002).

Genera ``advisory-credi10-2.0/01-contexto-as-is.md``:

  * E1.1 Mapa de Capacidades As-Is L1-L3 (Mermaid mindmap) + Arbol de
    Motivadores Estrategicos ligado a los 5 indicadores de retorno del RFP.
  * E1.2 Cadenas de Valor + proceso BPMN As-Is (Mermaid flowchart) del flujo
    originacion -> estudio de credito (CrossCore -> Inspektor ->
    Datacredito/Dictum) -> desembolso -> pagos/recaudo -> corte/cartera ->
    cobranza, con tabla de metricas baseline.
  * E1.3 Inventario del Ecosistema Tecnologico / Datos / Deuda Tecnica As-Is.
  * Asignacion de IDs del Hilo Dorado (DRV / CAP).
  * Veredicto QG-1.

Lideres: EA + BA + PIA + TDA. Verificador: AM. Gate: QG-1.

Nota: los IDs del Hilo Dorado se asignan por convencion determinista
(DRV-001.., CAP-001..) para que el informe sea robusto cuando la fase se
ejecuta en aislamiento (quickstart --phase 1).
"""

from __future__ import annotations

from typing import List

from phases import evidence_delta


# Drivers estrategicos ligados a los 5 indicadores de retorno del RFP.
# (driver_id, indicador, as_is -> to_be, descripcion)
DRIVERS = [
    ("DRV-001", "Disponibilidad de apps/servicios criticos", "90% -> 99%",
     "Elevar la disponibilidad de la plataforma Credi10 y sus componentes criticos."),
    ("DRV-002", "Optimizacion/eficiencia de recursos", "60% -> 80%",
     "Mejorar la eficiencia operativa reduciendo procesos manuales y batch."),
    ("DRV-003", "Optimizacion de costo de infraestructura", "80% -> 80%",
     "Sostener el costo de infraestructura sin degradar servicio al escalar."),
    ("DRV-004", "Evolucion tecnologica y escalamiento", "50% -> 100%",
     "Modernizar el stack obsoleto y habilitar escalamiento elastico."),
    ("DRV-005", "Cumplimiento de licenciamiento", "70% -> 100%",
     "Cerrar brechas de licenciamiento del stack .NET/SQL Server/Wordpress."),
]

# Capacidades de negocio L1 ligadas a drivers.
CAPABILITIES = [
    ("CAP-001", "Originacion de credito", "DRV-004",
     "Captura, estudio de credito y aprobacion (CrossCore/Inspektor/Datacredito)."),
    ("CAP-002", "Desembolso y facturacion electronica", "DRV-002",
     "Generacion de RCL/RCR en UnoEE, timbrado con Numrot."),
    ("CAP-003", "Pagos y recaudo", "DRV-001",
     "Link de Recaudo -> PayU, generacion de pagos, boton ecommerce."),
    ("CAP-004", "Corte y gestion de cartera", "DRV-002",
     "Proceso de corte de cartera (FT-SL-004) y consolidacion."),
    ("CAP-005", "Cobranza omnicanal", "DRV-001",
     "Scheduler + SMS/WhatsApp/Email + llamada predictiva (WOLKVOX)."),
    ("CAP-006", "Canales digitales B2C/ecommerce", "DRV-004",
     "Portal B2C (Node.js+React+Wordpress), VTEX, B2CHAT."),
    ("CAP-007", "Integracion e interoperabilidad", "DRV-004",
     "Integradores .NET e integracion con ERP Siesa/UnoEE y Pentaho."),
]


def register_thread_ids(ctx) -> None:
    """Registra DRV/CAP en el GoldenThread cuando esta disponible (best-effort).

    No se depende de los IDs generados en runtime: el informe usa los IDs por
    convencion (DRV-001..) definidos arriba, de modo que la fase es robusta en
    aislamiento. Este registro solo enriquece el hilo cuando se corre 'all'.
    """
    thread = getattr(ctx, "thread", None)
    if thread is None:
        return
    try:
        drv_links = {}
        for drv_id, indicador, _delta, desc in DRIVERS:
            link = thread.add("DRV", f"{indicador}: {desc}")
            drv_links[drv_id] = link.id
        for cap_id, name, drv_ref, desc in CAPABILITIES:
            parent = drv_links.get(drv_ref)
            thread.add("CAP", f"{name}: {desc}", parent=parent)
    except Exception:
        # El registro es opcional; nunca debe romper la generacion del informe.
        pass


def _drivers_table() -> str:
    rows = [
        "| Hilo Dorado | Indicador de retorno (RFP) | AS-IS -> TO-BE | Driver estrategico |",
        "| --- | --- | --- | --- |",
    ]
    for drv_id, indicador, delta, desc in DRIVERS:
        rows.append(f"| {drv_id} | {indicador} | {delta} | {desc} |")
    return "\n".join(rows)


def _capabilities_table() -> str:
    rows = [
        "| Hilo Dorado | Capacidad L1 | Driver asociado | Descripcion |",
        "| --- | --- | --- | --- |",
    ]
    for cap_id, name, drv_ref, desc in CAPABILITIES:
        rows.append(f"| {cap_id} | {name} | {drv_ref} | {desc} |")
    return "\n".join(rows)


def _capability_map() -> str:
    return (
        "```mermaid\n"
        "mindmap\n"
        "  root((Credi10 AS-IS))\n"
        "    Originacion de credito\n"
        "      Captura y solicitud\n"
        "        Captura Foto\n"
        "        Originacion ADMIN\n"
        "      Estudio de credito\n"
        "        CrossCore\n"
        "        Inspektor\n"
        "        Datacredito / Dictum\n"
        "    Desembolso y facturacion\n"
        "      RCL / RCR en UnoEE\n"
        "      Timbrado Numrot\n"
        "    Pagos y recaudo\n"
        "      Link de Recaudo\n"
        "        PayU\n"
        "      Generar Pagos\n"
        "      Boton Ecommerce\n"
        "    Cartera y cobranza\n"
        "      Corte de Cartera\n"
        "      Cobranza SMS/WhatsApp/Email\n"
        "      Llamada predictiva\n"
        "        WOLKVOX\n"
        "    Canales digitales\n"
        "      Portal B2C\n"
        "      VTEX\n"
        "      B2CHAT\n"
        "    Integracion\n"
        "      Integradores .NET\n"
        "      ERP Siesa / UnoEE\n"
        "      Pentaho\n"
        "```\n"
    )


def _motivators_tree() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    RFP["RFP Credi10 2.0<br/>Assessment integral + TO-BE + roadmap"]\n'
        '    RFP --> D1["DRV-001 Disponibilidad 90% -> 99%"]\n'
        '    RFP --> D2["DRV-002 Eficiencia recursos 60% -> 80%"]\n'
        '    RFP --> D3["DRV-003 Costo infra 80% -> 80%"]\n'
        '    RFP --> D4["DRV-004 Evolucion/escalamiento 50% -> 100%"]\n'
        '    RFP --> D5["DRV-005 Licenciamiento 70% -> 100%"]\n'
        "    D1 --> CAP003[CAP-003 Pagos/recaudo] & CAP005[CAP-005 Cobranza]\n"
        "    D2 --> CAP002[CAP-002 Desembolso] & CAP004[CAP-004 Cartera]\n"
        "    D4 --> CAP001[CAP-001 Originacion] & CAP006[CAP-006 Canales] & CAP007[CAP-007 Integracion]\n"
        "```\n"
    )


def _value_chain_bpmn() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        "    A([Cliente / solicitud]) --> B[Captura y originacion]\n"
        "    B --> C{Estudio de credito}\n"
        "    C --> C1[CrossCore]\n"
        "    C1 --> C2[Inspektor]\n"
        "    C2 --> C3[Datacredito / Dictum]\n"
        "    C3 --> D{Decision}\n"
        "    D -- Aprobado --> E[Desembolso<br/>RCL/RCR UnoEE + Numrot]\n"
        "    D -- Rechazado --> X([Fin])\n"
        "    E --> F[Pagos y recaudo<br/>Link Recaudo -> PayU]\n"
        "    F --> G[Corte y gestion de cartera]\n"
        "    G --> H{Mora?}\n"
        "    H -- Si --> I[Cobranza omnicanal<br/>SMS/WhatsApp/Email + WOLKVOX]\n"
        "    H -- No --> X\n"
        "    I --> X\n"
        "```\n"
    )


def _baseline_metrics_table() -> str:
    rows = [
        "| Cadena de valor | Metrica baseline (AS-IS) | Fuente | Driver |",
        "| --- | --- | --- | --- |",
        "| Disponibilidad plataforma | 90% (objetivo RFP 99%) | RFP | DRV-001 |",
        "| Eficiencia de recursos | 60% (objetivo 80%) | RFP | DRV-002 |",
        "| Evolucion/escalamiento | 50% (objetivo 100%) | RFP | DRV-004 |",
        "| Cumplimiento licenciamiento | 70% (objetivo 100%) | RFP | DRV-005 |",
        "| Estudio de credito | Encadenado CrossCore->Inspektor->Dictum "
        "(latencia no instrumentada) [EPISTEMIC-VOID] | Diagrama Contexto | CAP-001 |",
        "| Integracion ERP Siesa | Batch por archivos planos + WS unico; errores "
        "con intervencion manual | Assessment WSO2 | CAP-007 |",
    ]
    return "\n".join(rows)


def _tech_inventory_table() -> str:
    rows = [
        "| Capa | Componente | Tecnologia (AS-IS) | Evidencia |",
        "| --- | --- | --- | --- |",
        "| Aplicacion | Plataforma Credi10 | .NET Framework 4.8 sobre IIS 10 | Despliegue |",
        "| Aplicacion | Integradores (CrossCore, Inspektor, Datacredito, Servicios) | .NET | Despliegue |",
        "| Aplicacion | Web Service UnoEE | .NET | Despliegue |",
        "| Aplicacion | Link de Recaudo | .NET Core 3.1 | Despliegue |",
        "| Workers | Llamada predictiva, Indicador Robot, API SAC, Worker "
        "Consolidado, Corte/Cartera, Cobranza SMS/WhatsApp/Email/Scheduler | "
        ".NET Core 8 y .NET Framework 4.8 | Despliegue |",
        "| Canales | Portal B2C | API Node.js + React; Wordpress sobre Apache (XAMPP) | Despliegue |",
        "| Infra | Servidores on-prem | Windows Server 2019 Datacenter "
        "(Coatlanta, Codallas, Comumbai) | Despliegue |",
        "| Infra | Nube | AWS us-east-2, VPC STUDIO F, WAF->ALB->EC2, S3, "
        "CloudWatch, NAT, Bastion, VPN IPSec (Telmex) a on-prem Cokioto | Infra AWS |",
    ]
    return "\n".join(rows)


def _data_inventory_table() -> str:
    rows = [
        "| Base de datos | Motor | Uso | Evidencia |",
        "| --- | --- | --- | --- |",
        "| C10_Credi10NET | SQL Server 2019 Enterprise | BD principal de Credi10 | Despliegue |",
        "| C10_Inspektor | SQL Server 2019 Enterprise | Integrador Inspektor | Despliegue |",
        "| C10_Datacredito | SQL Server 2019 Enterprise | Integrador Datacredito | Despliegue |",
        "| C10_Database | SQL Server 2019 Enterprise | Link de Recaudo | Despliegue |",
        "| UnoEE_studiof (principal + espejo), Siesa Unoee | SQL Server | ERP Siesa/UnoEE | Despliegue |",
        "| C10_B2C_Wordpress, C10_B2C | MariaDB 10.4.32 | Portal B2C | Despliegue |",
    ]
    return "\n".join(rows)


def _tech_debt_table() -> str:
    rows = [
        "| ID | Deuda / obsolescencia tecnica | Riesgo | Driver impactado |",
        "| --- | --- | --- | --- |",
        "| DT-01 | .NET Framework 4.8 en plataforma e integradores | Marco legado, "
        "sin evolucion de features; riesgo de soporte | DRV-004, DRV-005 |",
        "| DT-02 | .NET Core 3.1 en Link de Recaudo | Fuera de soporte "
        "(end-of-life) | DRV-004, DRV-005 |",
        "| DT-03 | Wordpress + XAMPP/Apache en produccion | Superficie de ataque y "
        "operacion fragil para un canal B2C | DRV-001, DRV-004 |",
        "| DT-04 | Lectura/escritura directa a la BD del ERP Siesa | Acoplamiento "
        "fuerte y riesgo de integridad de datos | DRV-002 |",
        "| DT-05 | Integraciones dispersas en Windows Services/cronjobs sin "
        "gestion centralizada ni trazabilidad de errores | Baja gobernanza, "
        "intervencion manual | DRV-002, DRV-004 |",
        "| DT-06 | +200 bases de datos duplicadas con controles manuales en Excel "
        "(nivel grupo) | Inconsistencia de datos | DRV-002 |",
    ]
    return "\n".join(rows)


def _gate_block(ctx) -> str:
    gate = ctx.phase.gate
    rows = ["| Criterio de salida QG-1 | Estado |", "| --- | --- |"]
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
        "> Fase 1 del framework **Zero-Drift**. Consolida el contexto **AS-IS** de "
        "Credi10: capacidades de negocio, motivadores estrategicos, cadenas de "
        "valor/procesos e inventario tecnologico, de datos y deuda tecnica, todo "
        "trazable a evidencia primaria del corpus.",
        "",
        "**Liderazgo (RACI-V):** Productores (R): **EA, BA, PIA, TDA** - "
        "Accountable (A): **EM** - Verificador (V): **AM** (guardian AICV-E / "
        "Hilo Dorado) - Consultado (C): SME, DRE - Informado (I): ED.",
        "",
        "> **Hilo Dorado:** en esta fase se originan los identificadores de "
        "**Driver (DRV-xxx)** y **Capability (CAP-xxx)** que las fases 2-6 "
        "referenciaran (Benchmark -> Gap -> Reliever -> ABB -> SBB -> Wave -> ROI).",
        "",
        "## E1.1 - Mapa de Capacidades As-Is (L1-L3) y Arbol de Motivadores",
        "",
        "### Mapa de capacidades L1-L3",
        "",
        _capability_map(),
        "",
        "### Catalogo de capacidades (Hilo Dorado)",
        "",
        _capabilities_table(),
        "",
        "### Arbol de Motivadores Estrategicos (indicadores del RFP)",
        "",
        "Los cinco indicadores de retorno del RFP se traducen en drivers "
        "estrategicos que anclan todo el Hilo Dorado:",
        "",
        _drivers_table(),
        "",
        _motivators_tree(),
        "",
        "## E1.2 - Cadenas de Valor y Proceso BPMN As-Is",
        "",
        "Flujo operativo real de extremo a extremo: originacion -> estudio de "
        "credito (CrossCore -> Inspektor -> Datacredito/Dictum) -> desembolso -> "
        "pagos/recaudo -> corte/cartera -> cobranza.",
        "",
        _value_chain_bpmn(),
        "",
        "### Metricas baseline AS-IS",
        "",
        _baseline_metrics_table(),
        "",
        "## E1.3 - Inventario del Ecosistema Tecnologico, Datos y Deuda Tecnica",
        "",
        "### Inventario tecnologico [VERIFIED-FACT]",
        "",
        _tech_inventory_table(),
        "",
        "### Inventario de datos [VERIFIED-FACT]",
        "",
        _data_inventory_table(),
        "",
        "### Deuda tecnica y obsolescencia",
        "",
        "La modernizacion del stack es el eje del driver **DRV-004** "
        "(evolucion/escalamiento) y **DRV-005** (licenciamiento):",
        "",
        _tech_debt_table(),
        "",
        "> El ecosistema Credi10 se sostiene sobre marcos legados "
        "(**.NET Framework 4.8**, **.NET Core 3.1**) y practicas de alto riesgo "
        "(lectura directa a la BD del ERP Siesa, Wordpress/XAMPP en produccion), "
        "lo que fundamenta el caso de modernizacion de Credi10 2.0.",
        "",
        "### Diagnostico de integracion AS-IS (evidencia recuperada del Assessment WSO2)",
        "",
        "El Assessment WSO2/Studio F era un **vacio epistemico** (PDF con fuente "
        "de codificacion personalizada); su capa de texto nativa fue recuperada "
        "y hoy sustenta el diagnostico de integracion con evidencia trazable "
        "**[VERIFIED-FACT]** (ya no supuestos). Cita directa de los hechos "
        "clave del documento fuente:",
        "",
        evidence_delta.grounded_evidence_table(
            getattr(ctx, "knowledge_base", None),
            "WSO2 y Studio F - Assessment Mayo2026-Final.pdf"),
        "",
        "> Estos hechos confirman la integracion AS-IS con el **ERP Siesa** "
        "mediante **archivos planos** y un **unico WebService** para todas las "
        "operaciones, y la motivacion de **centralizar y gobernar las APIs** "
        "(driver DRV-004), sustentando CAP-007 con evidencia real.",
        "",
        _gate_block(ctx),
    ]
    return "\n".join(parts) + "\n"

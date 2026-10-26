"""Fase 0 - Higiene Epistemica (report builder, FEAT-002).

Genera ``advisory-credi10-2.0/00-higiene-epistemica.md`` con contenido real
fundamentado en el corpus Credi10 2.0:

  * E0.1 Reporte de Higiene Epistemica: tabla que clasifica afirmaciones
    reales del corpus con las 4 etiquetas [VERIFIED-FACT] / [DOC-ASSUMPTION] /
    [DOC-CONFLICT] / [EPISTEMIC-VOID], incluyendo la tension de alcance WSO2
    (+150 apps .NET / +200 BDs a nivel Studio F) vs. los ~20 componentes
    acotados de Credi10 en los diagramas.
  * E0.2 Grafo Preliminar de Conceptos (Mermaid) + Agenda de Elicitacion por
    Deltas.
  * Veredicto QG-0 (Go/No-Go).

Lideres: AM + TDA + DRE. Verificador: EM. Gate: QG-0.
"""

from __future__ import annotations

from typing import List


def _corpus_inventory_table(ctx) -> str:
    """Tabla de inventario del corpus con trazabilidad (sha256 abreviado)."""
    rows = [
        "| # | Evidencia | Tipo | Rol | SHA-256 (abrev.) | Bytes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for i, d in enumerate(sorted(ctx.documents, key=lambda x: (x.role != "primary", x.filename)), 1):
        sha = (d.sha256[:12] + "...") if d.sha256 else "-"
        rows.append(f"| {i} | {d.filename} | {d.kind.upper()} | {d.role} | `{sha}` | {d.size:,} |")
    return "\n".join(rows)


def _epistemic_table() -> str:
    rows = [
        "| ID | Afirmacion del corpus | Fuente primaria | Etiqueta |",
        "| --- | --- | --- | --- |",
        "| HE-01 | Credi10 corre sobre .NET Framework 4.8 en IIS 10; integradores "
        "(CrossCore, Inspektor, Datacredito, Servicios) en .NET y Windows "
        "Services en .NET Core 8 / .NET 4.8. | Diagrama de Despliegue (PNG) | "
        "[VERIFIED-FACT] |",
        "| HE-02 | Bases de datos SQL Server 2019 Enterprise: C10_Credi10NET "
        "(principal), C10_Inspektor, C10_Datacredito, C10_Database (Link de "
        "Recaudo); UnoEE_studiof (principal + espejo), Siesa Unoee. | Diagrama de "
        "Despliegue (PNG) | [VERIFIED-FACT] |",
        "| HE-03 | Portal B2C: API en Node.js + React y Wordpress sobre Apache "
        "(XAMPP) con BDs MariaDB 10.4.32 (C10_B2C_Wordpress, C10_B2C); Link de "
        "Recaudo en .NET Core 3.1. | Diagrama de Despliegue (PNG) | [VERIFIED-FACT] |",
        "| HE-04 | Integraciones de contexto: UNOEE/Siesa (ERP), PENTAHO, "
        "CROSSCORE -> INSPEKTOR -> DICTUM/Datacredito, Numrot, Link de Recaudo -> "
        "PayU, VTEX, WOLKVOX, ICOMMARKETING, B2CHAT (mayoria JSON/HTTP). | "
        "Diagrama de Contexto C4 (PNG) | [VERIFIED-FACT] |",
        "| HE-05 | Infraestructura AWS en us-east-2, VPC STUDIO F, flujo "
        "Internet Gateway -> WAF -> ALB -> EC2 privados (Coatlanta/Codallas/"
        "Comumbai), S3, CloudWatch, NAT, Bastion y VPN IPSec (Telmex) a on-prem "
        "Cokioto. | Diagrama de Infraestructura AWS (PNG) | [VERIFIED-FACT] |",
        "| HE-06 | El RFP 'Proyecto Credi10 2.0' (STF Group S.A., Cali/Yumbo, "
        "emitido 20-ago-2026) fija indicadores de retorno: disponibilidad "
        "90%->99%, eficiencia de recursos 60%->80%, costo infraestructura "
        "80%->80%, evolucion/escalamiento 50%->100%, licenciamiento 70%->100%. | "
        "RFP_CREDI10_2_0.pdf | [VERIFIED-FACT] |",
        "| HE-07 | El assessment WSO2/Studio F describe arquitectura fragmentada "
        "con +150 aplicaciones .NET y +200 bases de datos con informacion "
        "duplicada e inconsistente. | WSO2 y Studio F - Assessment Mayo2026 | "
        "[VERIFIED-FACT] |",
        "| HE-08 | Pain de integracion con ERP Siesa: integraciones rigidas por "
        "archivos planos, un unico Web Service para todas las operaciones, "
        "mayoria batch, y lectura/escritura directa a la BD del ERP por lentitud "
        "del WS (practica de alto riesgo). | WSO2 y Studio F - Assessment | "
        "[VERIFIED-FACT] |",
        "| HE-09 | El universo '+150 apps .NET / +200 BDs' del assessment es a "
        "nivel Studio F / grupo completo, mientras que los diagramas acotan "
        "Credi10 a ~20 componentes. Diferencia de ALCANCE que debe resolverse "
        "antes de dimensionar. | WSO2 Assessment vs. Diagramas Credi10 | "
        "[DOC-CONFLICT] |",
        "| HE-10 | El numero objetivo de disponibilidad (99%) presupone un "
        "baseline del 90%, pero el corpus no aporta una medicion real "
        "(instrumentacion, ventana, SLA) que lo sustente. | RFP_CREDI10_2_0.pdf | "
        "[EPISTEMIC-VOID] |",
        "| HE-11 | No hay cifras reales de costo de infraestructura ni de gasto "
        "de licenciamiento actual en el corpus; los indicadores 80%->80% y "
        "70%->100% carecen de linea base cuantificada. | RFP_CREDI10_2_0.pdf | "
        "[EPISTEMIC-VOID] |",
        "| HE-12 | La mayoria de las integraciones de contexto se marcan "
        "'JSON/HTTP', pero el corpus no detalla contratos, versiones de API ni "
        "volumetria/transaccionalidad por integracion. | Diagrama de Contexto | "
        "[EPISTEMIC-VOID] |",
        "| HE-13 | Se asume que las reglas de negocio existentes (originacion, "
        "corte de cartera, cobranza) deben preservarse 1:1 en Credi10 2.0, segun "
        "el requisito funcional del RFP, pero su especificacion detallada no esta "
        "en el corpus. | RFP_CREDI10_2_0.pdf | [DOC-ASSUMPTION] |",
        "| HE-14 | Se asume que los 13 PDFs de proceso (Originacion, GenerarPagos "
        "FT-SL-003, ProcesoCorteCartera FT-SL-004, LinkDePagos FT-SL-011, B2C, "
        "etc.) reflejan el AS-IS vigente; son imagen-pesados y su texto es "
        "evidencia secundaria de soporte. | PDFs de proceso | [DOC-ASSUMPTION] |",
    ]
    return "\n".join(rows)


def _concept_graph() -> str:
    return (
        "```mermaid\n"
        "graph TD\n"
        '    C10["CREDI10 .NET<br/>(.NET Framework 4.8 / IIS 10)"]\n'
        "    subgraph Integradores[\"Integradores .NET\"]\n"
        "        CC[CrossCore]\n"
        "        INS[Inspektor]\n"
        "        DTC[Datacredito]\n"
        "        SRV[Servicios Integrador]\n"
        "    end\n"
        "    subgraph Datos[\"Bases de datos\"]\n"
        '        DB1["C10_Credi10NET<br/>SQL Server 2019"]\n'
        "        DB2[C10_Inspektor]\n"
        "        DB3[C10_Datacredito]\n"
        '        DB4["C10_Database<br/>(Link Recaudo)"]\n'
        '        DB5["C10_B2C / C10_B2C_Wordpress<br/>MariaDB 10.4.32"]\n'
        "    end\n"
        "    subgraph Workers[\"Windows Services (.NET 8 / 4.8)\"]\n"
        "        W1[Corte/Cartera]\n"
        "        W2[Cobranza SMS/WhatsApp/Email/Scheduler]\n"
        "        W3[Llamada predictiva]\n"
        "        W4[Worker Consolidado / API SAC]\n"
        "    end\n"
        "    subgraph Ext[\"Integraciones externas\"]\n"
        "        ERP[UNOEE / Siesa ERP]\n"
        "        PEN[Pentaho]\n"
        "        DIC[Dictum / Datacredito]\n"
        "        PAYU[Link de Recaudo -> PayU]\n"
        "        VTEX[VTEX ecommerce]\n"
        "        WLK[WOLKVOX contact center]\n"
        "        ICM[ICOMMARKETING]\n"
        "        B2CH[B2CHAT]\n"
        "    end\n"
        "    B2C[Portal B2C<br/>Node.js + React + Wordpress]\n"
        "    C10 --> Integradores\n"
        "    C10 --> Datos\n"
        "    C10 --> Workers\n"
        "    C10 --> ERP\n"
        "    C10 --> PEN\n"
        "    CC --> INS --> DIC\n"
        "    C10 --> PAYU\n"
        "    C10 --> VTEX\n"
        "    C10 --> WLK\n"
        "    C10 --> ICM\n"
        "    C10 --> B2CH\n"
        "    C10 --> B2C\n"
        "    B2C --> DB5\n"
        "    Integradores --> Datos\n"
        "```\n"
    )


def _elicitation_agenda() -> str:
    rows = [
        "| ID | Pregunta abierta (delta) | Vacio/Conflicto que cierra | Responsable |",
        "| --- | --- | --- | --- |",
        "| DEL-01 | Cual es la medicion real de disponibilidad actual y bajo que "
        "SLA/ventana se calculo el 90%? | HE-10 [EPISTEMIC-VOID] | Cliente / EM |",
        "| DEL-02 | Cuales son los costos reales de infraestructura AWS/on-prem y "
        "el gasto de licenciamiento vigente? | HE-11 [EPISTEMIC-VOID] | FIN / Cliente |",
        "| DEL-03 | Que subconjunto exacto de los +150 apps y +200 BDs pertenece "
        "al perimetro Credi10 vs. al grupo Studio F? | HE-09 [DOC-CONFLICT] | "
        "EA / TDA |",
        "| DEL-04 | Que contratos, versiones y volumetria tiene cada integracion "
        "JSON/HTTP de contexto? | HE-12 [EPISTEMIC-VOID] | DA / TDA |",
        "| DEL-05 | Donde esta la especificacion detallada de las reglas de "
        "negocio a preservar (originacion, corte, cobranza)? | HE-13 "
        "[DOC-ASSUMPTION] | BA / DRE |",
        "| DEL-06 | Que operaciones usan hoy lectura/escritura directa a la BD del "
        "ERP y cual es su criticidad? | HE-08 [VERIFIED-FACT] | DA / SEC |",
    ]
    return "\n".join(rows)


def _gate_block(ctx) -> str:
    gate = ctx.phase.gate
    rows = ["| Criterio de salida QG-0 | Estado |", "| --- | --- |"]
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
    phase = ctx.phase
    n_pdf = sum(1 for d in ctx.documents if d.kind == "pdf")
    n_png = sum(1 for d in ctx.documents if d.kind == "png")
    n_primary = sum(1 for d in ctx.documents if d.role == "primary")

    parts: List[str] = [
        f"# {phase.name}",
        "",
        "> Fase 0 del framework **Zero-Drift**. Objetivo: establecer la higiene "
        "epistemica del corpus Credi10 2.0 antes de cualquier analisis, "
        "separando hechos verificados de supuestos, conflictos y vacios.",
        "",
        "**Liderazgo (RACI-V):** Productores (R): **AM, TDA, DRE** - "
        "Accountable (A): **EM** - Verificador (V): **EM** - "
        "Consultado (C): ED - Informado (I): EA, BA.",
        "",
        f"El corpus auditado contiene **{n_pdf} PDFs** y **{n_png} diagramas PNG** "
        f"({n_primary} artefactos primarios: RFP, Assessment WSO2/Studio F y los "
        "3 diagramas de arquitectura).",
        "",
        "## E0.1 - Reporte de Higiene Epistemica",
        "",
        "### Inventario de evidencia (trazabilidad)",
        "",
        _corpus_inventory_table(ctx),
        "",
        "### Clasificacion epistemica de afirmaciones",
        "",
        "Cada afirmacion relevante del corpus se etiqueta como [VERIFIED-FACT] "
        "(hecho verificable en fuente primaria), [DOC-ASSUMPTION] (supuesto "
        "razonable no probado), [DOC-CONFLICT] (tension/diferencia entre fuentes) "
        "o [EPISTEMIC-VOID] (vacio de informacion que impide concluir).",
        "",
        _epistemic_table(),
        "",
        "> **Conflicto de alcance clave (HE-09 / [DOC-CONFLICT]):** el assessment "
        "WSO2/Studio F cuantifica **+150 aplicaciones .NET** y **+200 bases de "
        "datos** a nivel del **grupo Studio F**, mientras que los diagramas de "
        "contexto y despliegue acotan **Credi10** a ~20 componentes. No es una "
        "contradiccion de hecho sino una **diferencia de alcance** que debe "
        "resolverse (DEL-03) antes de dimensionar el TO-BE.",
        "",
        "## E0.2 - Grafo Preliminar de Conceptos",
        "",
        "Mapa inicial del ecosistema Credi10 (aplicacion nucleo, integradores, "
        "datos, workers e integraciones externas) construido a partir de los "
        "diagramas de contexto y despliegue:",
        "",
        _concept_graph(),
        "",
        "### Agenda de Elicitacion por Deltas",
        "",
        "Preguntas abiertas que cierran los vacios/conflictos registrados; son el "
        "insumo de la sesion de elicitacion con el cliente:",
        "",
        _elicitation_agenda(),
        "",
        _gate_block(ctx),
    ]
    return "\n".join(parts) + "\n"

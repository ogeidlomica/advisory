"""Fase 4 - Diseno TO-BE y Spec Ejecutable (report builder, FEAT-003).

Genera ``advisory-credi10-2.0/04-diseno-to-be.md``:

  * E4.1 Mapeo ABB -> SBB + Diagramas C4 N1-N3 (Mermaid flowchart) + ADRs
    (>= 3 decisiones reales) + NFRs.
  * E4.2 Modelo de Datos ERD/DDD (Mermaid erDiagram del contexto Recaudo/Pagos)
    + Contratos OpenAPI/AsyncAPI (snippets) + Estrategia de Migracion.
  * E4.3 BPMN To-Be (Mermaid flowchart) + Service Blueprint + notas de
    Prototipos UX/UI.
  * E4.4 Paquete Spec-Driven: Historias BDD/Gherkin en espanol (Dado/Cuando/
    Entonces) cubriendo happy path + casos borde.
  * E4.5 Acta de Certificacion Dry-Run + Matriz de Threat Modeling siguiendo la
    cadena de validacion Evento -> Pantalla UX -> Regla Gherkin -> Contrato API
    -> Componente C4 -> Tabla/Entidad BD -> Respuesta al usuario.
  * Asignacion de IDs del Hilo Dorado (SBB-xxx) referenciando ABBs.
  * Veredicto QG-4.

Lideres: SA + DA + PM + UX. Verificador/Dry-Run: AM. Gate: QG-4.
"""

from __future__ import annotations

from typing import List


# --------------------------------------------------------------------------- #
# Hilo Dorado - SBBs (SBB-xxx) que referencian ABBs de la Fase 3.5.
# (sbb_id, Solution Building Block, abb_origen, stack/tecnologia TO-BE)
# --------------------------------------------------------------------------- #

SBBS = [
    ("SBB-001", "API Gateway + plataforma de API Management (WSO2 API Platform + "
     "Integration Platform)", "ABB-001", "WSO2 API Manager / Integration"),
    ("SBB-002", "Data Services sobre el ERP Siesa (reemplazan la lectura directa "
     "a la BD)", "ABB-002", ".NET 8 Data Services + WSO2 Data Services"),
    ("SBB-003", "Bus de eventos / mensajeria para sincronizacion con Siesa",
     "ABB-003", "Broker de eventos (AsyncAPI)"),
    ("SBB-004", "Microservicios de dominio (.NET 8) por bounded context",
     "ABB-004", ".NET 8 contenerizado"),
    ("SBB-005", "Observabilidad y trazabilidad (logging/metricas/SLOs)",
     "ABB-005", "CloudWatch + stack de observabilidad"),
    ("SBB-006", "Migracion de runtime .NET Framework 4.8 / .NET Core 3.1 -> "
     ".NET 8", "ABB-006", ".NET 8 / contenedores"),
]


def register_thread_ids(ctx) -> None:
    """Registra SBB en el GoldenThread (best-effort, no rompe el build)."""
    thread = getattr(ctx, "thread", None)
    if thread is None:
        return
    try:
        for sbb_id, name, abb_ref, _stack in SBBS:
            # El parent se referencia por convencion (ABB-xxx) en texto; aqui
            # solo se registra el SBB para enriquecer el hilo cuando corre 'all'.
            thread.add("SBB", f"{name} (origen {abb_ref})")
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# E4.1 - Mapeo ABB -> SBB, C4, ADRs, NFRs
# --------------------------------------------------------------------------- #

def _abb_sbb_table() -> str:
    rows = [
        "| Hilo Dorado | SBB (Solution Building Block) | ABB origen | Stack TO-BE |",
        "| --- | --- | --- | --- |",
    ]
    for sbb_id, name, abb_ref, stack in SBBS:
        rows.append(f"| {sbb_id} | {name} | {abb_ref} | {stack} |")
    return "\n".join(rows)


def _c4_context() -> str:
    # C4 Nivel 1 (Contexto) representado como flowchart (fallback seguro).
    return (
        "```mermaid\n"
        "flowchart TB\n"
        '    Cliente(["Cliente / Asesor"])\n'
        '    subgraph SYS["Credi10 2.0 (sistema)"]\n'
        "        GW{{API Gateway / Management - SBB-001}}\n"
        "    end\n"
        "    Buros[CrossCore / Inspektor / Datacredito]\n"
        "    PayU[PayU]\n"
        "    Siesa[ERP Siesa / UnoEE]\n"
        "    Cliente --> GW\n"
        "    GW --> Buros\n"
        "    GW --> PayU\n"
        "    GW --> Siesa\n"
        "```\n"
    )


def _c4_container() -> str:
    # C4 Nivel 2 (Contenedores) representado como flowchart.
    return (
        "```mermaid\n"
        "flowchart LR\n"
        '    GW{{API Gateway / Management<br/>SBB-001}}\n'
        '    subgraph DOM["Servicios de dominio .NET 8 - SBB-004"]\n'
        "        ORIG[Originacion]\n"
        "        EC[Estudio de Credito]\n"
        "        PAG[Pagos]\n"
        "        REC[Recaudo]\n"
        "    end\n"
        "    BUS[(Bus de eventos<br/>SBB-003)]\n"
        "    DS[Data Services sobre Siesa<br/>SBB-002]\n"
        "    OBS[Observabilidad<br/>SBB-005]\n"
        "    GW --> ORIG & EC & PAG & REC\n"
        "    EC --> BUS\n"
        "    PAG --> BUS\n"
        "    REC --> BUS\n"
        "    BUS --> DS\n"
        "    DS --> Siesa[(ERP Siesa/UnoEE)]\n"
        "    ORIG -.-> OBS\n"
        "    EC -.-> OBS\n"
        "```\n"
    )


def _c4_component() -> str:
    # C4 Nivel 3 (Componentes) del servicio Estudio de Credito.
    return (
        "```mermaid\n"
        "flowchart TB\n"
        '    subgraph EC["Servicio Estudio de Credito (.NET 8) - SBB-004"]\n'
        "        API[Endpoint POST /estudio-credito]\n"
        "        ORQ[Orquestador de buros]\n"
        "        RN[Motor de reglas de negocio]\n"
        "        PUB[Publicador de eventos]\n"
        "    end\n"
        "    API --> ORQ\n"
        "    ORQ --> CC[Cliente CrossCore]\n"
        "    ORQ --> IN[Cliente Inspektor]\n"
        "    ORQ --> DC[Cliente Datacredito/Dictum]\n"
        "    ORQ --> RN\n"
        "    RN --> PUB\n"
        "    PUB --> BUS[(Bus de eventos SBB-003)]\n"
        "```\n"
    )


def _adrs() -> str:
    return (
        "### ADR-001: Adoptar una plataforma de API Management centralizada\n\n"
        "- **Estado:** Aceptada.\n"
        "- **Contexto:** Las integraciones viven dispersas en servicios de "
        "Windows y cronjobs sin gestion centralizada ni trazabilidad (GAP-004).\n"
        "- **Decision:** Adoptar WSO2 API Platform + Integration Platform como "
        "capa unica de gestion de APIs (SBB-001), eco de la recomendacion 5.2 "
        "del assessment.\n"
        "- **Consecuencias:** Gobernanza, trazabilidad y seguridad centralizadas; "
        "introduce una dependencia de plataforma a operar. Liga a DRV-004.\n\n"
        "### ADR-002: Reemplazar la integracion de archivos planos / WS unico de "
        "Siesa por Data Services + eventos\n\n"
        "- **Estado:** Aceptada.\n"
        "- **Contexto:** Siesa se integra por archivos planos batch y un unico "
        "Web Service, con la practica de ALTO RIESGO de leer/escribir directo a "
        "la BD del ERP (GAP-001, GAP-002).\n"
        "- **Decision:** Exponer el ERP Siesa como **Data Services** gobernados "
        "(SBB-002) y sincronizar via un **bus de eventos** (SBB-003); prohibir "
        "el acceso directo a la BD del ERP.\n"
        "- **Consecuencias:** Elimina el cuello de botella y el riesgo de "
        "integridad; requiere definir contratos AsyncAPI. Liga a DRV-001/DRV-002.\n\n"
        "### ADR-003: Migrar el runtime .NET Framework 4.8 / .NET Core 3.1 a .NET 8\n\n"
        "- **Estado:** Aceptada.\n"
        "- **Contexto:** Componentes criticos corren sobre .NET Framework 4.8 y "
        ".NET Core 3.1 (fuera de soporte), con Wordpress/XAMPP en produccion "
        "(GAP-005).\n"
        "- **Decision:** Migrar los servicios a **.NET 8** contenerizado "
        "(SBB-006) y retirar Wordpress/XAMPP del canal B2C.\n"
        "- **Consecuencias:** Cierra brechas de soporte y licenciamiento; implica "
        "esfuerzo de migracion por ola. Liga a DRV-005/DRV-004.\n"
    )


def _nfr_table() -> str:
    rows = [
        "| NFR TO-BE | Objetivo | SBB que lo habilita | Driver |",
        "| --- | --- | --- | --- |",
        "| Disponibilidad | 90% -> 99% | SBB-001, SBB-005 | DRV-001 |",
        "| Eficiencia de recursos | 60% -> 80% (latencia base sin instrumentar "
        "hoy [EPISTEMIC-VOID]) | SBB-002, SBB-003 | DRV-002 |",
        "| Costo de infraestructura | 80% -> 80% (sin degradar) | SBB-004 | DRV-003 |",
        "| Evolucion/escalamiento | 50% -> 100% | SBB-004, SBB-006 | DRV-004 |",
        "| Licenciamiento | 70% -> 100% | SBB-006 | DRV-005 |",
    ]
    return "\n".join(rows)


# --------------------------------------------------------------------------- #
# E4.2 - Modelo de Datos + Contratos + Migracion
# --------------------------------------------------------------------------- #

def _erd() -> str:
    return (
        "```mermaid\n"
        "erDiagram\n"
        "    CLIENTE ||--o{ SOLICITUD : origina\n"
        "    SOLICITUD ||--|| ESTUDIO_CREDITO : evalua\n"
        "    SOLICITUD ||--o{ OBLIGACION : genera\n"
        "    OBLIGACION ||--o{ LINK_RECAUDO : cobra\n"
        "    LINK_RECAUDO ||--o{ PAGO : concilia\n"
        "    CLIENTE {\n"
        "        string documento PK\n"
        "        string nombre\n"
        "    }\n"
        "    SOLICITUD {\n"
        "        string id_solicitud PK\n"
        "        string documento FK\n"
        "        string estado\n"
        "    }\n"
        "    ESTUDIO_CREDITO {\n"
        "        string id_estudio PK\n"
        "        string id_solicitud FK\n"
        "        string decision\n"
        "        int score\n"
        "    }\n"
        "    OBLIGACION {\n"
        "        string id_obligacion PK\n"
        "        decimal saldo\n"
        "    }\n"
        "    LINK_RECAUDO {\n"
        "        string id_link PK\n"
        "        string id_obligacion FK\n"
        "        decimal monto\n"
        "        string estado\n"
        "    }\n"
        "    PAGO {\n"
        "        string id_pago PK\n"
        "        string id_link FK\n"
        "        string referencia_payu\n"
        "    }\n"
        "```\n"
    )


def _openapi_snippet() -> str:
    return (
        "```yaml\n"
        "openapi: 3.0.3\n"
        "info:\n"
        "  title: Credi10 2.0 - Estudio de Credito\n"
        "  version: 1.0.0\n"
        "paths:\n"
        "  /estudio-credito:\n"
        "    post:\n"
        "      summary: Inicia el estudio de credito (CrossCore -> Inspektor -> Datacredito)\n"
        "      requestBody:\n"
        "        required: true\n"
        "        content:\n"
        "          application/json:\n"
        "            schema:\n"
        "              type: object\n"
        "              required: [documento, idSolicitud]\n"
        "              properties:\n"
        "                documento: { type: string }\n"
        "                idSolicitud: { type: string }\n"
        "      responses:\n"
        "        '200':\n"
        "          description: Decision del estudio\n"
        "          content:\n"
        "            application/json:\n"
        "              schema:\n"
        "                type: object\n"
        "                properties:\n"
        "                  idEstudio: { type: string }\n"
        "                  decision: { type: string, enum: [APROBADO, RECHAZADO, REVISION] }\n"
        "                  score: { type: integer }\n"
        "        '424':\n"
        "          description: Buro no disponible (CrossCore/Inspektor/Datacredito)\n"
        "```\n"
    )


def _asyncapi_snippet() -> str:
    return (
        "```yaml\n"
        "asyncapi: 2.6.0\n"
        "info:\n"
        "  title: Credi10 2.0 - Eventos de integracion Siesa\n"
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
        "            idObligacion: { type: string }\n"
        "            referenciaPayU: { type: string }\n"
        "            monto: { type: number }\n"
        "```\n"
    )


def _migration_table() -> str:
    rows = [
        "| Elemento legado | Estrategia de migracion | SBB destino |",
        "| --- | --- | --- |",
        "| WS unico + archivos planos de Siesa | Strangler Fig: desviar por Data "
        "Services + eventos de forma incremental | SBB-002, SBB-003 |",
        "| Lectura directa a la BD del ERP Siesa | Prohibir y reemplazar por Data "
        "Services; CDC donde aplique | SBB-002 |",
        "| .NET Framework 4.8 / .NET Core 3.1 | Migracion por dominio a .NET 8 "
        "contenerizado | SBB-006, SBB-004 |",
        "| Integraciones Windows/cronjobs | Reencaminar por API Gateway + bus de "
        "eventos | SBB-001, SBB-003 |",
    ]
    return "\n".join(rows)


# --------------------------------------------------------------------------- #
# E4.3 - BPMN To-Be + Service Blueprint + UX
# --------------------------------------------------------------------------- #

def _bpmn_tobe() -> str:
    return (
        "```mermaid\n"
        "flowchart LR\n"
        "    A([Cliente solicita credito]) --> B[UX: Formulario de solicitud]\n"
        "    B --> C[API Gateway SBB-001]\n"
        "    C --> D[Servicio Estudio de Credito]\n"
        "    D --> E{Decision}\n"
        "    E -- Aprobado --> F[Desembolso + RCL/RCR via Data Services Siesa]\n"
        "    E -- Revision --> R[Cola de revision manual]\n"
        "    E -- Rechazado --> X([Fin])\n"
        "    F --> G[Recaudo: Link de Recaudo -> PayU]\n"
        "    G --> H[Evento PagoAplicado al bus]\n"
        "    H --> X\n"
        "    R --> X\n"
        "```\n"
    )


def _service_blueprint_table() -> str:
    rows = [
        "| Capa del Service Blueprint | Actividad (flujo estudio -> recaudo) |",
        "| --- | --- |",
        "| Evidencia fisica | Formulario web, confirmacion de aprobacion, link de pago |",
        "| Acciones del cliente | Enviar solicitud, aceptar oferta, pagar en PayU |",
        "| Frontstage (UX) | Pantalla de solicitud, pantalla de decision, pantalla de pago |",
        "| Backstage | Orquestacion de buros, motor de reglas, generacion de RCL/RCR |",
        "| Procesos de soporte | Data Services Siesa, bus de eventos, observabilidad |",
    ]
    return "\n".join(rows)


# --------------------------------------------------------------------------- #
# E4.4 - Paquete Spec-Driven (Gherkin en espanol)
# --------------------------------------------------------------------------- #

def _gherkin() -> str:
    return (
        "```gherkin\n"
        "# language: es\n"
        "Caracteristica: Estudio de credito en Credi10 2.0\n"
        "\n"
        "  Escenario: Aprobacion con buros disponibles (happy path)\n"
        "    Dado un cliente con documento \"CC123\" y una solicitud \"SOL-1\"\n"
        "    Cuando se invoca POST /estudio-credito con el documento y la solicitud\n"
        "    Y CrossCore, Inspektor y Datacredito responden correctamente\n"
        "    Entonces la decision es \"APROBADO\"\n"
        "    Y se publica el evento de estudio en el bus\n"
        "\n"
        "  Escenario: Buro no disponible (caso borde EX-01)\n"
        "    Dado un cliente con documento \"CC124\" y una solicitud \"SOL-2\"\n"
        "    Cuando se invoca POST /estudio-credito\n"
        "    Y CrossCore agota el tiempo de espera\n"
        "    Entonces el servicio responde con estado 424\n"
        "    Y la solicitud queda encolada sin perderse\n"
        "\n"
        "  Escenario: Escritura a Siesa falla (caso borde EX-04)\n"
        "    Dado una solicitud \"SOL-3\" aprobada\n"
        "    Cuando falla la escritura al ERP Siesa\n"
        "    Entonces nunca se escribe directo a la base de datos del ERP\n"
        "    Y se publica un evento para reintentar via Data Services\n"
        "```\n"
    )


# --------------------------------------------------------------------------- #
# E4.5 - Acta de Certificacion Dry-Run + Threat Modeling
# --------------------------------------------------------------------------- #

def _dry_run_chain_table() -> str:
    rows = [
        "| Eslabon de la cadena de validacion | Artefacto concreto |",
        "| --- | --- |",
        "| Evento | Cliente envia solicitud de credito |",
        "| Pantalla UX | Formulario de solicitud -> pantalla de decision |",
        "| Regla Gherkin | Escenario \"Aprobacion con buros disponibles\" "
        "(Dado/Cuando/Entonces) |",
        "| Contrato API (payload JSON) | `POST /estudio-credito` "
        "`{ \"documento\": \"CC123\", \"idSolicitud\": \"SOL-1\" }` |",
        "| Componente C4 | Servicio Estudio de Credito (.NET 8, SBB-004) + API "
        "Gateway (SBB-001) |",
        "| Tabla/Entidad BD | ESTUDIO_CREDITO (id_estudio, id_solicitud, "
        "decision, score) |",
        "| Respuesta al usuario | Decision APROBADO/RECHAZADO/REVISION con score "
        "(umbral de score [DOC-ASSUMPTION], a confirmar con negocio) |",
    ]
    return "\n".join(rows)


def _threat_model_table() -> str:
    rows = [
        "| Amenaza (STRIDE) | Vector | Mitigacion | SBB |",
        "| --- | --- | --- | --- |",
        "| Spoofing | Suplantacion de cliente o asesor | Autenticacion fuerte en "
        "el API Gateway | SBB-001 |",
        "| Tampering | Manipulacion directa de la BD del ERP Siesa | Prohibir "
        "acceso directo; solo Data Services | SBB-002 |",
        "| Repudiation | Falta de trazabilidad de operaciones | Logging y "
        "auditoria centralizada | SBB-005 |",
        "| Information disclosure | Fuga de datos de buros | Cifrado extremo a "
        "extremo y minimizacion | SBB-001 |",
        "| Denial of service | Saturacion del WS unico de Siesa | Bus de eventos "
        "+ rate limiting en el gateway | SBB-003, SBB-001 |",
        "| Elevation of privilege | Escalamiento via integraciones dispersas | "
        "Zero-trust y segmentacion por dominio | SBB-004 |",
    ]
    return "\n".join(rows)


def _dry_run_act_table() -> str:
    rows = [
        "| Criterio de Dry-Run / Tabletop (AM) | Resultado |",
        "| --- | --- |",
        "| Cada SBB mapea a un ABB trazable | OK |",
        "| Cada historia Gherkin cubre happy path + casos borde | OK |",
        "| Contratos API/eventos definidos (OpenAPI/AsyncAPI) | OK |",
        "| Cadena Evento -> UX -> Gherkin -> API -> C4 -> BD -> respuesta completa | OK |",
        "| Reglas de negocio preservadas (requisito RFP) | OK |",
    ]
    return "\n".join(rows)


# --------------------------------------------------------------------------- #
# Gate QG-4
# --------------------------------------------------------------------------- #

def _gate_block(ctx) -> str:
    gate = ctx.phase.gate
    rows = ["| Criterio de salida QG-4 | Estado |", "| --- | --- |"]
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
        "> Fase 4 del framework **Zero-Drift**. Disena el **TO-BE** de "
        "Credi10 2.0: mapea los ABBs a SBBs concretos, define la arquitectura "
        "C4, las decisiones (ADRs), el modelo de datos, los contratos, el "
        "proceso BPMN y el paquete Spec-Driven (Gherkin), todo certificado por "
        "un **Dry-Run / Tabletop** del AM antes de construir.",
        "",
        "**Liderazgo (RACI-V):** Productores (R): **SA, DA, PM, UX** - "
        "Accountable (A): **EM** - Verificador / Dry-Run (V): **AM** - "
        "Consultado (C): AIA, SEC - Informado (I): ED.",
        "",
        "> **Hilo Dorado:** esta fase origina **SBBs (SBB-xxx)**, cada uno "
        "referenciando un **ABB (ABB-xxx)** de la Fase 3.5 y ligado a un Driver "
        "(DRV) del RFP.",
        "",
        "## E4.1 - Mapeo ABB -> SBB, Arquitectura C4, ADRs y NFRs",
        "",
        "### Mapeo ABB -> SBB (Hilo Dorado)",
        "",
        _abb_sbb_table(),
        "",
        "### C4 Nivel 1 - Contexto",
        "",
        _c4_context(),
        "",
        "### C4 Nivel 2 - Contenedores",
        "",
        _c4_container(),
        "",
        "### C4 Nivel 3 - Componentes (Estudio de Credito)",
        "",
        _c4_component(),
        "",
        "### Architecture Decision Records (ADRs)",
        "",
        _adrs(),
        "",
        "### NFRs TO-BE",
        "",
        _nfr_table(),
        "",
        "## E4.2 - Modelo de Datos (ERD/DDD), Contratos y Migracion",
        "",
        "### Modelo de datos - contexto Recaudo/Pagos",
        "",
        _erd(),
        "",
        "### Contrato OpenAPI - POST /estudio-credito",
        "",
        _openapi_snippet(),
        "",
        "### Contrato AsyncAPI - evento de recaudo",
        "",
        _asyncapi_snippet(),
        "",
        "### Estrategia de migracion",
        "",
        _migration_table(),
        "",
        "## E4.3 - Proceso BPMN To-Be, Service Blueprint y UX",
        "",
        "### BPMN To-Be (estudio de credito -> recaudo)",
        "",
        _bpmn_tobe(),
        "",
        "### Service Blueprint",
        "",
        _service_blueprint_table(),
        "",
        "> **Prototipos UX/UI:** pantalla de solicitud (captura de documento), "
        "pantalla de decision (APROBADO/RECHAZADO/REVISION con score) y pantalla "
        "de pago (redireccion a PayU). Disenadas por UX para minimizar pasos "
        "manuales (DRV-002).",
        "",
        "## E4.4 - Paquete Spec-Driven (Historias BDD / Gherkin)",
        "",
        "Historias en Gherkin espanol (Dado/Cuando/Entonces) que cubren el "
        "happy path y los casos borde del Exception Storming (EX-01, EX-04):",
        "",
        _gherkin(),
        "",
        "## E4.5 - Acta de Certificacion Dry-Run y Threat Modeling",
        "",
        "### Cadena de validacion (Dry-Run / Tabletop del AM)",
        "",
        "El AM recorre la cadena completa Evento -> Pantalla UX -> Regla Gherkin "
        "-> Contrato API (payload JSON) -> Componente C4 -> Tabla/Entidad BD -> "
        "Respuesta al usuario:",
        "",
        _dry_run_chain_table(),
        "",
        "### Matriz de Threat Modeling (SEC, STRIDE)",
        "",
        _threat_model_table(),
        "",
        "### Acta de certificacion",
        "",
        _dry_run_act_table(),
        "",
        "> El Dry-Run certifica que cada SBB es trazable a un ABB y que la cadena "
        "Evento -> respuesta esta completa, preservando las reglas de negocio; "
        "se habilita el build.",
        "",
        _gate_block(ctx),
    ]
    return "\n".join(parts) + "\n"

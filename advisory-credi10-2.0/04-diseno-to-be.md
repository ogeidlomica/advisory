# Fase 4 - Diseno TO-BE

> Fase 4 del framework **Zero-Drift**. Disena el **TO-BE** de Credi10 2.0: mapea los ABBs a SBBs concretos, define la arquitectura C4, las decisiones (ADRs), el modelo de datos, los contratos, el proceso BPMN y el paquete Spec-Driven (Gherkin), todo certificado por un **Dry-Run / Tabletop** del AM antes de construir.

**Liderazgo (RACI-V):** Productores (R): **SA, DA, PM, UX** - Accountable (A): **EM** - Verificador / Dry-Run (V): **AM** - Consultado (C): AIA, SEC - Informado (I): ED.

> **Hilo Dorado:** esta fase origina **SBBs (SBB-xxx)**, cada uno referenciando un **ABB (ABB-xxx)** de la Fase 3.5 y ligado a un Driver (DRV) del RFP.

> **Trazabilidad (Base de Conocimiento):** el diseno TO-BE se fundamenta en la ingesta COMPLETA de **18** documentos (`knowledge-base/`). Fuentes principales de esta fase: `RFP_CREDI10_2_0.pdf`, `WSO2 y Studio F - Assessment Mayo2026-Final.pdf`, `Originacion_CrossCore.pdf`, `LinkDePagos.pdf`. Las cifras/umbrales sin dato explicito en el corpus se marcan [DOC-ASSUMPTION].

> **Catalogo exhaustivo de Historias de Usuario + Gherkin:** la cobertura completa (sin muestreo) de TODOS los modulos de Credi10 vive en el artefacto complementario [`04b-catalogo-historias.md`](04b-catalogo-historias.md), generado desde la fuente unica de verdad `advisory-system/phases/modules.py`.

## E4.1 - Mapeo ABB -> SBB, Arquitectura C4, ADRs y NFRs

### Mapeo ABB -> SBB (Hilo Dorado)

| Hilo Dorado | SBB (Solution Building Block) | ABB origen | Stack TO-BE |
| --- | --- | --- | --- |
| SBB-001 | API Gateway + plataforma de API Management (WSO2 API Platform + Integration Platform) | ABB-001 | WSO2 API Manager / Integration |
| SBB-002 | Data Services sobre el ERP Siesa (reemplazan la lectura directa a la BD) | ABB-002 | .NET 8 Data Services + WSO2 Data Services |
| SBB-003 | Bus de eventos / mensajeria para sincronizacion con Siesa | ABB-003 | Broker de eventos (AsyncAPI) |
| SBB-004 | Microservicios de dominio (.NET 8) por bounded context | ABB-004 | .NET 8 contenerizado |
| SBB-005 | Observabilidad y trazabilidad (logging/metricas/SLOs) | ABB-005 | CloudWatch + stack de observabilidad |
| SBB-006 | Migracion de runtime .NET Framework 4.8 / .NET Core 3.1 -> .NET 8 | ABB-006 | .NET 8 / contenedores |
| SBB-007 | Fuente unica de verdad por dominio (consolidar las +200 BDs duplicadas) | ABB-004 | SQL Server consolidado + dominios de datos |
| SBB-008 | Estrategia cloud AWS (VPC, ALB/WAF, escalamiento, contenedores) | ABB-006 | AWS (VPC, ALB, WAF, ECS/EKS) |

> Las vistas C4 siguientes son el **TO-BE** de Credi10 2.0 (complementan las transcripciones AS-IS de contexto/despliegue/AWS de la Fase 1).

### C4 Nivel 1 (TO-BE) - Contexto

```mermaid
flowchart TB
    Cliente(["Cliente / Asesor"])
    subgraph SYS["Credi10 2.0 (sistema)"]
        GW{{API Gateway / Management - SBB-001}}
    end
    Buros[CrossCore / Inspektor / Datacredito]
    PayU[PayU]
    Siesa[ERP Siesa / UnoEE]
    Cliente --> GW
    GW --> Buros
    GW --> PayU
    GW --> Siesa
```


### C4 Nivel 2 (TO-BE) - Contenedores

```mermaid
flowchart LR
    GW{{API Gateway / Management<br/>SBB-001}}
    subgraph DOM["Servicios de dominio .NET 8 - SBB-004"]
        ORIG[Originacion]
        EC[Estudio de Credito]
        PAG[Pagos]
        REC[Recaudo]
    end
    BUS[(Bus de eventos<br/>SBB-003)]
    DS[Data Services sobre Siesa<br/>SBB-002]
    OBS[Observabilidad<br/>SBB-005]
    GW --> ORIG & EC & PAG & REC
    EC --> BUS
    PAG --> BUS
    REC --> BUS
    BUS --> DS
    DS --> Siesa[(ERP Siesa/UnoEE)]
    ORIG -.-> OBS
    EC -.-> OBS
```


### C4 Nivel 3 (TO-BE) - Componentes (Estudio de Credito)

```mermaid
flowchart TB
    subgraph EC["Servicio Estudio de Credito (.NET 8) - SBB-004"]
        API[Endpoint POST /estudio-credito]
        ORQ[Orquestador de buros]
        RN[Motor de reglas de negocio]
        PUB[Publicador de eventos]
    end
    API --> ORQ
    ORQ --> CC[Cliente CrossCore]
    ORQ --> IN[Cliente Inspektor]
    ORQ --> DC[Cliente Datacredito/Dictum]
    ORQ --> RN
    RN --> PUB
    PUB --> BUS[(Bus de eventos SBB-003)]
```


### Architecture Decision Records (ADRs)

### ADR-001: Adoptar una plataforma de API Management centralizada

- **Estado:** Aceptada.
- **Contexto:** Las integraciones viven dispersas en servicios de Windows y cronjobs sin gestion centralizada ni trazabilidad (GAP-004).
- **Decision:** Adoptar WSO2 API Platform + Integration Platform como capa unica de gestion de APIs (SBB-001), eco de la recomendacion 5.2 del assessment.
- **Consecuencias:** Gobernanza, trazabilidad y seguridad centralizadas; introduce una dependencia de plataforma a operar. Liga a DRV-004.

### ADR-002: Reemplazar la integracion de archivos planos / WS unico de Siesa por Data Services + eventos

- **Estado:** Aceptada.
- **Contexto:** Siesa se integra por archivos planos batch y un unico Web Service, con la practica de ALTO RIESGO de leer/escribir directo a la BD del ERP (GAP-001, GAP-002).
- **Decision:** Exponer el ERP Siesa como **Data Services** gobernados (SBB-002) y sincronizar via un **bus de eventos** (SBB-003); prohibir el acceso directo a la BD del ERP.
- **Consecuencias:** Elimina el cuello de botella y el riesgo de integridad; requiere definir contratos AsyncAPI. Liga a DRV-001/DRV-002.

### ADR-003: Migrar el runtime .NET Framework 4.8 / .NET Core 3.1 a .NET 8

- **Estado:** Aceptada.
- **Contexto:** Componentes criticos corren sobre .NET Framework 4.8 y .NET Core 3.1 (fuera de soporte), con Wordpress/XAMPP en produccion (GAP-005).
- **Decision:** Migrar los servicios a **.NET 8** contenerizado (SBB-006) y retirar Wordpress/XAMPP del canal B2C.
- **Consecuencias:** Cierra brechas de soporte y licenciamiento; implica esfuerzo de migracion por ola. Liga a DRV-005/DRV-004.

### ADR-004: WSO2 como plataforma de API Management frente a alternativas

- **Estado:** Aceptada.
- **Contexto:** El assessment analiza el ecosistema actual y recomienda una capa unica de gestion de APIs; existen alternativas (Kong, AWS API Gateway/MuleSoft, Apigee) [DOC-ASSUMPTION].
- **Decision:** Adoptar **WSO2 API Platform + Integration Platform** (SBB-001) por continuidad con la recomendacion del assessment y por cubrir API Management + integracion + Data Services en una sola plataforma; se mantiene la decision recalibrable si el cliente prefiere una alternativa cloud-native.
- **Consecuencias:** Minimiza fragmentacion de herramientas; crea dependencia de una plataforma que debe operarse y licenciarse. Liga a DRV-004.

### ADR-005: Fuente unica de verdad por dominio (consolidar +200 BDs)

- **Estado:** Aceptada.
- **Contexto:** Existen +200 bases de datos duplicadas/inconsistentes a nivel grupo con logica repetida y controles manuales en Excel (GAP-003).
- **Decision:** Establecer una **fuente unica de verdad por dominio** (SBB-007), con dominios de datos con duenio claro y los demas sistemas consumiendo via API/eventos en lugar de replicar BDs.
- **Consecuencias:** Reduce inconsistencia y reconciliacion manual; requiere migracion/consolidacion de datos y gobierno de dominios. Liga a DRV-002.

### ADR-006: Estrategia cloud en AWS para el TO-BE

- **Estado:** Aceptada.
- **Contexto:** La infraestructura AS-IS usa AWS (VPC, EC2, ALB/WAF segun los diagramas), con EC2 estaticos y un WS lento como cuello de botella (GAP-002).
- **Decision:** Desplegar los servicios de dominio .NET 8 contenerizados en **AWS** (VPC, ALB, WAF, orquestacion de contenedores) con escalamiento elastico y observabilidad (SBB-008, SBB-005), manteniendo el costo de infraestructura controlado (DRV-003).
- **Consecuencias:** Habilita escalamiento y resiliencia; exige IaC y disciplina de FinOps para no degradar costo. Liga a DRV-003/DRV-004.


### NFRs TO-BE

| NFR TO-BE | Objetivo | SBB que lo habilita | Driver |
| --- | --- | --- | --- |
| Disponibilidad | 90% -> 99% | SBB-001, SBB-005 | DRV-001 |
| Eficiencia de recursos | 60% -> 80% (latencia base sin instrumentar hoy [EPISTEMIC-VOID]) | SBB-002, SBB-003 | DRV-002 |
| Costo de infraestructura | 80% -> 80% (sin degradar) | SBB-004 | DRV-003 |
| Evolucion/escalamiento | 50% -> 100% | SBB-004, SBB-006 | DRV-004 |
| Licenciamiento | 70% -> 100% | SBB-006 | DRV-005 |

## E4.2 - Modelo de Datos (ERD/DDD), Contratos y Migracion

Un **ERD por bounded context** (DDD), complementando el modelo Recaudo/Pagos. Son artefactos de especificacion embebidos (documentacion para la siguiente etapa), no esquemas ejecutables.

### Modelo de datos - contexto Originacion / Estudio de Credito

```mermaid
erDiagram
    CLIENTE ||--o{ SOLICITUD : origina
    SOLICITUD ||--|| ESTUDIO_CREDITO : evalua
    ESTUDIO_CREDITO ||--o{ CONSULTA_BURO : encadena
    SOLICITUD ||--o{ SOPORTE_FOTO : adjunta
    CLIENTE {
        string documento PK
        string nombre
    }
    SOLICITUD {
        string id_solicitud PK
        string documento FK
        string estado
    }
    ESTUDIO_CREDITO {
        string id_estudio PK
        string id_solicitud FK
        string decision
        int score
    }
    CONSULTA_BURO {
        string id_consulta PK
        string id_estudio FK
        string buro
        string resultado
    }
    SOPORTE_FOTO {
        string id_soporte PK
        string id_solicitud FK
        string uri
    }
```


### Modelo de datos - contexto Recaudo / Pagos

```mermaid
erDiagram
    CLIENTE ||--o{ SOLICITUD : origina
    SOLICITUD ||--|| ESTUDIO_CREDITO : evalua
    SOLICITUD ||--o{ OBLIGACION : genera
    OBLIGACION ||--o{ LINK_RECAUDO : cobra
    LINK_RECAUDO ||--o{ PAGO : concilia
    CLIENTE {
        string documento PK
        string nombre
    }
    SOLICITUD {
        string id_solicitud PK
        string documento FK
        string estado
    }
    ESTUDIO_CREDITO {
        string id_estudio PK
        string id_solicitud FK
        string decision
        int score
    }
    OBLIGACION {
        string id_obligacion PK
        decimal saldo
    }
    LINK_RECAUDO {
        string id_link PK
        string id_obligacion FK
        decimal monto
        string estado
    }
    PAGO {
        string id_pago PK
        string id_link FK
        string referencia_payu
    }
```


### Modelo de datos - contexto Corte / Cartera

```mermaid
erDiagram
    OBLIGACION ||--o{ CORTE_CARTERA : consolida
    CORTE_CARTERA ||--o{ ESTADO_MORA : clasifica
    OBLIGACION {
        string id_obligacion PK
        string documento FK
        decimal saldo
    }
    CORTE_CARTERA {
        string id_corte PK
        string periodo
        decimal saldo_total
    }
    ESTADO_MORA {
        string id_obligacion FK
        string id_corte FK
        int dias_mora
        string tramo
    }
```


### Modelo de datos - contexto Cobranza

```mermaid
erDiagram
    OBLIGACION ||--o{ CAMPANA_COBRANZA : incluye
    CAMPANA_COBRANZA ||--o{ CONTACTO : ejecuta
    CONTACTO ||--o{ PROMESA_PAGO : genera
    CAMPANA_COBRANZA {
        string id_campana PK
        string canal
        string segmento
    }
    CONTACTO {
        string id_contacto PK
        string id_campana FK
        string id_obligacion FK
        string resultado
    }
    PROMESA_PAGO {
        string id_promesa PK
        string id_contacto FK
        decimal monto
        string fecha
    }
```


### Modelo de datos - contexto Cliente / B2C

```mermaid
erDiagram
    CLIENTE ||--o{ SESION_PORTAL : accede
    CLIENTE ||--o{ OBLIGACION : posee
    CLIENTE ||--o{ PEDIDO_ECOMMERCE : compra
    SESION_PORTAL {
        string id_sesion PK
        string documento FK
        string canal
    }
    PEDIDO_ECOMMERCE {
        string id_pedido PK
        string documento FK
        decimal monto
        string estado
    }
    OBLIGACION {
        string id_obligacion PK
        string documento FK
        decimal saldo
    }
```


### Contratos de API (indice)

Contratos **OpenAPI (REST)** y **AsyncAPI (eventos)** esbozados para las integraciones clave. Son **artefactos de especificacion** embebidos como snippets en este informe (specs de diseno para la siguiente etapa), NO codigo ejecutable ni archivos de API independientes.

| Contrato | Tipo | Integracion | SBB |
| --- | --- | --- | --- |
| POST /estudio-credito | OpenAPI (REST) | CrossCore/Inspektor/Datacredito | SBB-001, SBB-004 |
| GET /siesa/obligaciones/{id} | OpenAPI (REST) | Data Services Siesa/UnoEE | SBB-002 |
| recaudo/pago-aplicado | AsyncAPI (eventos) | PayU -> recaudo | SBB-003 |
| cobranza/contacto-realizado | AsyncAPI (eventos) | Cobranza multicanal | SBB-003 |

### Contrato OpenAPI - POST /estudio-credito (CrossCore/Inspektor/Datacredito)

```yaml
openapi: 3.0.3
info:
  title: Credi10 2.0 - Estudio de Credito
  version: 1.0.0
paths:
  /estudio-credito:
    post:
      summary: Inicia el estudio de credito (CrossCore -> Inspektor -> Datacredito)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [documento, idSolicitud]
              properties:
                documento: { type: string }
                idSolicitud: { type: string }
      responses:
        '200':
          description: Decision del estudio
          content:
            application/json:
              schema:
                type: object
                properties:
                  idEstudio: { type: string }
                  decision: { type: string, enum: [APROBADO, RECHAZADO, REVISION] }
                  score: { type: integer }
        '424':
          description: Buro no disponible (CrossCore/Inspektor/Datacredito)
```


### Contrato OpenAPI - Data Services sobre Siesa/UnoEE

```yaml
openapi: 3.0.3
info:
  title: Credi10 2.0 - Data Services sobre Siesa/UnoEE (SBB-002)
  version: 1.0.0
paths:
  /siesa/obligaciones/{idObligacion}:
    get:
      summary: Lee una obligacion via Data Service gobernado (NO acceso directo a BD)
      parameters:
        - name: idObligacion
          in: path
          required: true
          schema: { type: string }
      responses:
        '200':
          description: Obligacion
          content:
            application/json:
              schema:
                type: object
                properties:
                  idObligacion: { type: string }
                  saldo: { type: number }
        '503':
          description: Data Service de Siesa no disponible (reintentar via eventos)
```


### Contrato AsyncAPI - evento de recaudo (PayU)

```yaml
asyncapi: 2.6.0
info:
  title: Credi10 2.0 - Eventos de integracion Siesa
  version: 1.0.0
channels:
  recaudo/pago-aplicado:
    subscribe:
      message:
        name: PagoAplicado
        payload:
          type: object
          properties:
            idPago: { type: string }
            idObligacion: { type: string }
            referenciaPayU: { type: string }
            monto: { type: number }
```


### Contrato AsyncAPI - eventos de cobranza multicanal

```yaml
asyncapi: 2.6.0
info:
  title: Credi10 2.0 - Eventos de Cobranza multicanal
  version: 1.0.0
channels:
  cobranza/contacto-realizado:
    subscribe:
      message:
        name: ContactoRealizado
        payload:
          type: object
          properties:
            idObligacion: { type: string }
            canal: { type: string, enum: [SMS, WhatsApp, Email, Llamada] }
            resultado: { type: string }
            idCampana: { type: string }
```


### Estrategia de migracion

| Elemento legado | Estrategia de migracion | SBB destino |
| --- | --- | --- |
| WS unico + archivos planos de Siesa | Strangler Fig: desviar por Data Services + eventos de forma incremental | SBB-002, SBB-003 |
| Lectura directa a la BD del ERP Siesa | Prohibir y reemplazar por Data Services; CDC donde aplique | SBB-002 |
| .NET Framework 4.8 / .NET Core 3.1 | Migracion por dominio a .NET 8 contenerizado | SBB-006, SBB-004 |
| Integraciones Windows/cronjobs | Reencaminar por API Gateway + bus de eventos | SBB-001, SBB-003 |

## E4.3 - Procesos BPMN To-Be, Service Blueprint y UX

### BPMN To-Be (estudio de credito -> recaudo)

```mermaid
flowchart LR
    A([Cliente solicita credito]) --> B[UX: Formulario de solicitud]
    B --> C[API Gateway SBB-001]
    C --> D[Servicio Estudio de Credito]
    D --> E{Decision}
    E -- Aprobado --> F[Desembolso + RCL/RCR via Data Services Siesa]
    E -- Revision --> R[Cola de revision manual]
    E -- Rechazado --> X([Fin])
    F --> G[Recaudo: Link de Recaudo -> PayU]
    G --> H[Evento PagoAplicado al bus]
    H --> X
    R --> X
```


### BPMN To-Be (recaudo -> cobranza multicanal)

```mermaid
flowchart LR
    A([Corte de cartera]) --> B{Obligacion en mora?}
    B -- No --> Z([Fin])
    B -- Si --> C[Segmentar y priorizar cartera]
    C --> D[Scheduler de cobranza multicanal]
    D --> E[SMS / WhatsApp / Email]
    D --> F[Llamada predictiva WOLKVOX]
    E --> G[Evento ContactoRealizado al bus SBB-003]
    F --> G
    G --> H{Promesa de pago?}
    H -- Si --> I[Link de Recaudo -> PayU]
    H -- No --> C
    I --> Z
```


### BPMN To-Be (desembolso -> facturacion RCL/RCR)

```mermaid
flowchart LR
    A([Estudio APROBADO]) --> B[Desembolso]
    B --> C[Generar RCL/RCR en UnoEE]
    C --> D[Timbrado Numrot]
    D --> E{Timbrado OK?}
    E -- Si --> F[Enviar a cliente y DIAN]
    E -- No --> G[Reintentar via eventos - nunca BD directa ADR-002]
    G --> D
    F --> H([Fin])
```


### Service Blueprint

| Capa del Service Blueprint | Actividad (flujo estudio -> recaudo) |
| --- | --- |
| Evidencia fisica | Formulario web, confirmacion de aprobacion, link de pago |
| Acciones del cliente | Enviar solicitud, aceptar oferta, pagar en PayU |
| Frontstage (UX) | Pantalla de solicitud, pantalla de decision, pantalla de pago |
| Backstage | Orquestacion de buros, motor de reglas, generacion de RCL/RCR |
| Procesos de soporte | Data Services Siesa, bus de eventos, observabilidad |

> **Prototipos UX/UI:** pantalla de solicitud (captura de documento), pantalla de decision (APROBADO/RECHAZADO/REVISION con score) y pantalla de pago (redireccion a PayU). Disenadas por UX para minimizar pasos manuales (DRV-002).

## E4.4 - Paquete Spec-Driven (Historias BDD / Gherkin)

Historia representativa en Gherkin espanol (Dado/Cuando/Entonces) que cubre el happy path y los casos borde del Exception Storming (EX-01, EX-04). El **catalogo EXHAUSTIVO** con una historia (happy + borde) para CADA modulo del universo Credi10 esta en [`04b-catalogo-historias.md`](04b-catalogo-historias.md):

```gherkin
# language: es
Caracteristica: Estudio de credito en Credi10 2.0

  Escenario: Aprobacion con buros disponibles (happy path)
    Dado un cliente con documento "CC123" y una solicitud "SOL-1"
    Cuando se invoca POST /estudio-credito con el documento y la solicitud
    Y CrossCore, Inspektor y Datacredito responden correctamente
    Entonces la decision es "APROBADO"
    Y se publica el evento de estudio en el bus

  Escenario: Buro no disponible (caso borde EX-01)
    Dado un cliente con documento "CC124" y una solicitud "SOL-2"
    Cuando se invoca POST /estudio-credito
    Y CrossCore agota el tiempo de espera
    Entonces el servicio responde con estado 424
    Y la solicitud queda encolada sin perderse

  Escenario: Escritura a Siesa falla (caso borde EX-04)
    Dado una solicitud "SOL-3" aprobada
    Cuando falla la escritura al ERP Siesa
    Entonces nunca se escribe directo a la base de datos del ERP
    Y se publica un evento para reintentar via Data Services
```


## E4.6 - Catalogo de Oportunidades de IA (skill declarativo)

Las oportunidades de IA se modelan como **skill declarativo** (`.kiro/skills/ai-opportunities-catalog`) y se renderizan aqui consumiendo `engine.skills.load_ai_catalog()` (NO hardcodeadas). Dos pistas: **IA-como-producto** e **IA-como-acelerador-de-construccion**. Las viabilidades/beneficios especulativos van [DOC-ASSUMPTION]; donde el corpus no da base se marca [EPISTEMIC-VOID].

### IA-como-producto

| ID | Caso de uso | Modulo | Datos requeridos | Viabilidad | Gancho al roadmap |
| --- | --- | --- | --- | --- | --- |
| AIP-001 | Credit/Risk Scoring en Originacion: Modelo de scoring de credito y riesgo que complementa las reglas de CrossCore/DICTUM para decidir y priorizar solicitudes de originacion. | Originacion (CrossCore / Inspektor / Datacredito / Aplicacion ADMIN) | Historico de solicitudes y decisiones, bureau (Datacredito), variables de Inspektor, resultado de mora posterior. | Alta si existe historico etiquetado; [DOC-ASSUMPTION] sobre volumen y calidad de datos a confirmar con el cliente. | Ola 2 - capacidades de decision inteligente sobre originacion. |
| AIP-002 | Antifraude en CrossCore / Inspektor: Deteccion de fraude y anomalias en solicitudes usando senales de CrossCore e Inspektor para reducir perdidas por fraude. | Originacion (CrossCore, Inspektor) | Casos historicos de fraude confirmado, features de dispositivo/identidad, senales de CrossCore/Inspektor. | Media-alta; requiere etiquetas de fraude confiables. [DOC-ASSUMPTION] sobre disponibilidad de ground-truth. | Ola 2 - control de riesgo y fraude. |
| AIP-003 | Cobranza Predictiva y Priorizada: Priorizacion de cartera y seleccion de canal/mensaje optimo por cliente para maximizar recaudo con menor costo de contacto. | Cobranza (SMS/WhatsApp/Email/Scheduler, Llamada Predictiva) | Historico de pagos y promesas, resultados por canal, estados de mora, respuesta a campanas previas. | Alta; datos operativos de cobranza suelen existir. [DOC-ASSUMPTION] sobre granularidad de resultados por canal. | Ola 3 - optimizacion de recaudo. |
| AIP-004 | OCR / Vision en Captura de Documentos: Extraccion automatica de datos de documentos de identidad y soportes fotograficos para acelerar y validar la originacion. | Captura Foto | Imagenes de documentos capturados, ground-truth de campos extraidos, plantillas de documentos. | Alta para documentos estandar; [DOC-ASSUMPTION] sobre calidad/variedad de capturas. Nota: el motor no hace OCR en runtime (stdlib). | Ola 2 - automatizacion de captura. |
| AIP-005 | NLP / Chatbot en Atencion al Cliente: Asistente conversacional y clasificacion/ruteo de intenciones para atencion omnicanal integrada con Wolkvox y B2Chat. | Atencion al Cliente (Wolkvox, B2Chat, API Integrador) | Transcripciones y chats historicos, taxonomia de intenciones, base de conocimiento de respuestas. | Media-alta; depende de calidad de transcripciones. [DOC-ASSUMPTION] sobre volumen de conversaciones. | Ola 3 - experiencia de atencion. |
| AIP-006 | Pronostico de Cartera (Portfolio Forecasting): Pronostico de comportamiento de cartera (mora, prepago, roll-rates) para planeacion financiera y provisiones. | Cartera (Proceso Corte de Cartera, BI Pentaho) | Series historicas de cartera, cortes mensuales, variables macro, resultados de cobranza. | Media; requiere series suficientes. [DOC-ASSUMPTION] sobre profundidad historica disponible. | Ola 3 - inteligencia financiera. |

### IA-como-acelerador-de-construccion (rol AIA)

| ID | Caso de uso | Modulo | Datos requeridos | Viabilidad | Gancho al roadmap |
| --- | --- | --- | --- | --- | --- |
| AIB-001 | Spec-to-Code: Generar scaffolding y codigo a partir de specs/HU estructuradas para acelerar la construccion de los modulos del roadmap. | Fabrica de software (rol AIA) | HU y specs AI-ready con criterios Gherkin, contratos OpenAPI/AsyncAPI, convenciones del repositorio. | Alta como acelerador; requiere specs de calidad (ver AIB-002). [DOC-ASSUMPTION] sobre adopcion del equipo. | Ola 1 - habilitadores de entrega. |
| AIB-002 | Specs AI-Ready: Estandarizar HU/specs en formato estructurado y trazable (AI-ready) para que spec-to-code y la generacion de pruebas sean fiables. | Fabrica de software (roles BA + AIA) | Plantillas de HU/Gherkin, catalogo de modulos, Hilo Dorado de trazabilidad. | Alta; es practica de proceso, bajo riesgo tecnico. | Ola 1 - habilitadores de entrega. |
| AIB-003 | Generacion Automatica de Pruebas: Derivar casos de prueba (unitarios/aceptacion) desde los criterios Gherkin de las HU para aumentar cobertura y reducir regresion. | Fabrica de software (rol AIA) | Criterios de aceptacion Gherkin, contratos de API, datos de ejemplo. | Alta cuando las specs son AI-ready (depende de AIB-002). | Ola 2 - calidad y automatizacion de pruebas. |

> Total de oportunidades catalogadas: **9** (skill declarativo versionado, recalibrable sin tocar el motor).

## E4.5 - Acta de Certificacion Dry-Run y Threat Modeling

### Cadena de validacion (Dry-Run / Tabletop del AM)

El AM recorre la cadena completa Evento -> Pantalla UX -> Regla Gherkin -> Contrato API (payload JSON) -> Componente C4 -> Tabla/Entidad BD -> Respuesta al usuario:

| Eslabon de la cadena de validacion | Artefacto concreto |
| --- | --- |
| Evento | Cliente envia solicitud de credito |
| Pantalla UX | Formulario de solicitud -> pantalla de decision |
| Regla Gherkin | Escenario "Aprobacion con buros disponibles" (Dado/Cuando/Entonces) |
| Contrato API (payload JSON) | `POST /estudio-credito` `{ "documento": "CC123", "idSolicitud": "SOL-1" }` |
| Componente C4 | Servicio Estudio de Credito (.NET 8, SBB-004) + API Gateway (SBB-001) |
| Tabla/Entidad BD | ESTUDIO_CREDITO (id_estudio, id_solicitud, decision, score) |
| Respuesta al usuario | Decision APROBADO/RECHAZADO/REVISION con score (umbral de score [DOC-ASSUMPTION], a confirmar con negocio) |

### Matriz de Threat Modeling (SEC, STRIDE)

| Amenaza (STRIDE) | Vector | Mitigacion | SBB |
| --- | --- | --- | --- |
| Spoofing | Suplantacion de cliente o asesor | Autenticacion fuerte en el API Gateway | SBB-001 |
| Tampering | Manipulacion directa de la BD del ERP Siesa | Prohibir acceso directo; solo Data Services | SBB-002 |
| Repudiation | Falta de trazabilidad de operaciones | Logging y auditoria centralizada | SBB-005 |
| Information disclosure | Fuga de datos de buros | Cifrado extremo a extremo y minimizacion | SBB-001 |
| Denial of service | Saturacion del WS unico de Siesa | Bus de eventos + rate limiting en el gateway | SBB-003, SBB-001 |
| Elevation of privilege | Escalamiento via integraciones dispersas | Zero-trust y segmentacion por dominio | SBB-004 |

### Acta de certificacion

| Criterio de Dry-Run / Tabletop (AM) | Resultado |
| --- | --- |
| Cada SBB mapea a un ABB trazable | OK |
| Cada historia Gherkin cubre happy path + casos borde | OK |
| Contratos API/eventos definidos (OpenAPI/AsyncAPI) | OK |
| Cadena Evento -> UX -> Gherkin -> API -> C4 -> BD -> respuesta completa | OK |
| Reglas de negocio preservadas (requisito RFP) | OK |

> El Dry-Run certifica que cada SBB es trazable a un ABB y que la cadena Evento -> respuesta esta completa, preservando las reglas de negocio; se habilita el build.

## Stage-Gate QG-4 - Diseno TO-BE (Dry-Run)

| Criterio de salida QG-4 | Estado |
| --- | --- |
| Arquitectura TO-BE y SBBs definidos. | Satisfecho |
| Specs e historias trazables a gaps. | Satisfecho |
| Dry-Run / Tabletop ejecutado por AM antes del build. | Satisfecho |

**No-Go si:** El Dry-Run revela SBBs sin spec o specs sin historia trazable.

> **Veredicto QG-4:** QG-4 :: GO - Criterios de salida satisfechos.


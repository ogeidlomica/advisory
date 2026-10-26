# 02 - Arquitectura TO-BE multinivel (Credi10 2.0)

> Capitulo de **arquitectura** del dossier TO-BE. Presenta vistas por nivel arquitectonico (negocio, aplicacion con C4 N1-3, datos con ERD por bounded context, integracion con desacople de Siesa, infraestructura AWS objetivo y seguridad). **Reutiliza y enlaza** la Fase 4 (`../../04-diseno-to-be.md`: C4, ADR-001..006, ERD, OpenAPI/AsyncAPI) sin contradecirla; aqui se consolidan las vistas por nivel.

> Etiquetas epistemicas: **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto a validar; **[DOC-CONFLICT]** contradiccion entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

Niveles arquitectonicos cubiertos: **negocio**, **aplicacion**, **datos**, **integracion**, **infraestructura**, **seguridad**.

## Resumen por nivel arquitectonico

| Nivel arquitectonico | Vista TO-BE | Elementos clave | SBB / ADR |
| --- | --- | --- | --- |
| Negocio | Cadena de valor credito | Originacion -> Estudio -> Desembolso -> Recaudo -> Cartera -> Cobranza | - |
| Aplicacion (C4 N1-3) | Servicios de dominio tras API Gateway | WSO2 + .NET 8 por bounded context | SBB-001, SBB-004 |
| Datos | ERD por bounded context + fuente unica de verdad | Consolidar +200 BDs | SBB-007, ADR-005 |
| Integracion | APIs + eventos, desacople de Siesa | Data Services + bus de eventos | SBB-002, SBB-003, ADR-002 |
| Infraestructura | AWS objetivo | VPC/ALB/WAF, contenedores, VPN Telmex, SQL Server | SBB-008, ADR-006 |
| Seguridad | Zero-trust transversal | authn/authz, cifrado, trazabilidad STRIDE | SBB-001, SBB-005 |

## Nivel negocio

```mermaid
flowchart LR
    CL(["Cliente / Asesor"]) --> ORIG[Originacion]
    ORIG --> EC[Estudio de Credito]
    EC --> DES[Desembolso + RCL/RCR]
    DES --> REC[Recaudo PayU]
    REC --> CAR[Corte de Cartera]
    CAR --> COB[Cobranza multicanal]
    COB --> REC
```


## Nivel aplicacion (C4 contenedores)

Vista de contenedores coherente con los diagramas C4 N1-3 de la Fase 4 (no se duplican; se enlazan en `../../04-diseno-to-be.md`):

```mermaid
flowchart LR
    GW{{API Gateway / WSO2<br/>SBB-001}}
    subgraph DOM["Servicios de dominio .NET 8 - SBB-004"]
        ORIG[Originacion]
        EC[Estudio de Credito]
        PAG[Pagos]
        REC[Recaudo]
        COB[Cobranza]
    end
    BUS[(Bus de eventos<br/>SBB-003)]
    DS[Data Services Siesa<br/>SBB-002]
    GW --> ORIG & EC & PAG & REC & COB
    EC --> BUS
    REC --> BUS
    BUS --> DS
    DS --> SIESA[(ERP Siesa/UnoEE)]
```


## Nivel datos (ERD por bounded context)

```mermaid
erDiagram
    CLIENTE ||--o{ SOLICITUD : origina
    SOLICITUD ||--|| ESTUDIO_CREDITO : evalua
    SOLICITUD ||--o{ OBLIGACION : genera
    OBLIGACION ||--o{ LINK_RECAUDO : cobra
    LINK_RECAUDO ||--o{ PAGO : concilia
    OBLIGACION ||--o{ CORTE_CARTERA : consolida
    CLIENTE {
        string documento PK
    }
    ESTUDIO_CREDITO {
        string id_estudio PK
        string decision
    }
    PAGO {
        string id_pago PK
        string referencia_payu
    }
```


## Nivel integracion (desacople de Siesa)

El cuello de botella AS-IS (WS unico + archivos planos, GAP-001) se reemplaza por Data Services gobernados (SBB-002) y un bus de eventos (SBB-003); nunca acceso directo a la BD del ERP (ADR-002):

```mermaid
flowchart LR
    subgraph ASIS["AS-IS (a desacoplar)"]
        WS[WS unico Siesa]
        FLAT[Archivos planos batch]
    end
    subgraph TOBE["TO-BE gobernado"]
        GW{{API Gateway SBB-001}}
        BUS[(Bus de eventos SBB-003)]
        DS[Data Services Siesa SBB-002]
    end
    WS -. reemplaza .-> DS
    FLAT -. reemplaza .-> BUS
    GW --> BUS --> DS --> SIESA[(ERP Siesa/UnoEE)]
```


## Nivel infraestructura (AWS objetivo)

```mermaid
flowchart TB
    subgraph AWS["AWS (VPC)"]
        WAF[WAF] --> ALB[ALB]
        ALB --> ECS[Contenedores .NET 8<br/>ECS/EKS - SBB-008]
        ECS --> SQL[(SQL Server)]
        ECS --> OBS[Observabilidad CloudWatch<br/>SBB-005]
    end
    TELMEX[VPN IPSec Telmex] --> AWS
    ECS --> SIESA[(ERP Siesa/UnoEE)]
```


## Nivel seguridad

```mermaid
flowchart LR
    USER([Cliente / Asesor]) --> GW{{API Gateway<br/>authn/authz SBB-001}}
    GW --> SVC[Servicios de dominio .NET 8]
    SVC --> OBS[Logging/auditoria SBB-005]
    SVC --> ENC[Cifrado de datos sensibles]
    ENC --> SQL[(SQL Server)]
```


> **Veredicto de cobertura:** seis niveles arquitectonicos con vista TO-BE, trazados a SBB-001..008 y ADR-001..006 de la Fase 4.


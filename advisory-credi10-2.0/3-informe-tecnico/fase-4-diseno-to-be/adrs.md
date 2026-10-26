# Decisiones de arquitectura (ADRs)

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 4 - Diseno TO-BE**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../04-diseno-to-be.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

Los **ADR** (Architecture Decision Records) documentan las seis decisiones estructurales del TO-BE con su contexto, decision y consecuencias. Son el corazon de la trazabilidad arquitectonica: explican **por que** se eligio cada camino, lo que permite recalibrar con fundamento si el cliente prefiere una alternativa.

Para la estimacion, los ADR acotan el espacio de solucion y, por tanto, la varianza del esfuerzo: fijar WSO2, .NET 8, AWS y la prohibicion de acceso directo a la BD elimina ramas de incertidumbre que, de quedar abiertas, inflarian el rango de la estimacion.

## Resumen de decisiones (ADR)

| ADR | Decision | Gap que ataca | Impacto en esfuerzo/riesgo |
| --- | --- | --- | --- |
| ADR-001 | API Management centralizado (WSO2) | GAP-004 | Alto (plataforma transversal) |
| ADR-002 | Data Services + eventos sobre Siesa (sin BD directa) | GAP-001, GAP-002 | Muy alto (nucleo del acoplamiento) |
| ADR-003 | Migrar runtime a .NET 8 | GAP-005 | Alto (extension: muchos componentes) |
| ADR-004 | WSO2 vs. alternativas (recalibrable) | GAP-004 | Medio (fuente de varianza si cambia) |
| ADR-005 | Fuente unica de verdad por dominio | GAP-003 | Alto (consolidar +200 BDs) |
| ADR-006 | Estrategia cloud AWS | GAP-002 | Medio (IaC + FinOps) |

## Registro detallado de decisiones

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


### Como leer los ADR para estimar

ADR-002 (reemplazar el WS unico y la BD directa por Data Services + eventos) es el de mayor impacto en esfuerzo y riesgo, porque toca el punto mas acoplado del sistema. ADR-003 (migrar a .NET 8) es el de mayor extension. ADR-004 (elegir WSO2) es recalibrable y su cambio afectaria la estimacion de la plataforma de integracion. Leer los ADR en clave de esfuerzo/riesgo es parte del trabajo de estimacion.
## Implicaciones para la estimacion

Las decisiones fijan el stack y, con el, los factores de la tabla parametrica. Un cambio de ADR (p. ej. otra plataforma de API) obligaria a recalibrar la estimacion de los SBB afectados; por eso los ADR marcados recalibrables se vigilan como fuente de varianza.

## Implicaciones para la estrategia de implementacion

Las consecuencias de cada ADR definen prerrequisitos de implementacion (IaC y FinOps para AWS, contratos AsyncAPI para el desacople) que entran al roadmap como trabajo habilitador.

## Riesgos e incertidumbre

El riesgo es tratar un ADR aceptado como inmutable cuando el contexto cambia. El formato ADR mantiene la decision revisable y trazable, conteniendo ese riesgo. [DOC-ASSUMPTION]


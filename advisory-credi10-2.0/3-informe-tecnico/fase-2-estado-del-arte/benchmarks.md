# Benchmarks de industria y comparativo AS-IS

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 2 - Estado del Arte**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../02-estado-del-arte.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

El estado del arte conecta la realidad de Credi10 con los **patrones de referencia** del credito de consumo y fintech: integracion API-led con gestion centralizada de APIs (eco directo de la recomendacion del assessment WSO2), arquitectura event-driven, cloud-native, observabilidad/SRE, zero-trust y automatizacion/IA. El valor de esta fase es que **evita reinventar la rueda**: cada gap se medira contra una practica reconocida, lo que da credibilidad y reduce la incertidumbre de la estimacion.

La narrativa es de brecha: el comparativo AS-IS vs. estado del arte muestra que Credi10 esta lejos del patron en integracion y datos, y mas cerca en seguridad perimetral. Esa distancia es, en esencia, el trabajo por hacer, y ordenarla por tamanio de brecha ayuda a priorizar.

## Benchmarks ligados al Hilo Dorado

| Hilo Dorado | Benchmark / patron de industria | Capacidad / Driver | Relevancia para Credi10 |
| --- | --- | --- | --- |
| BMK-001 | Integracion API-led (API gateway + management) | CAP-007 / DRV-004 | Gestionar todas las APIs de forma centralizada (eco directo de la recomendacion 5.2 del assessment: WSO2 API Platform + Integration Platform) frente a integraciones dispersas en Windows Services. |
| BMK-002 | Arquitectura event-driven / mensajeria | CAP-002 / DRV-002 | Reemplazar batch por archivos planos del ERP Siesa con eventos/colas para sincronizacion casi en tiempo real. |
| BMK-003 | Cloud-native / contenedores y escalamiento elastico | CAP-006 / DRV-004 | Contenerizar workloads y escalar en AWS (us-east-2) con autoscaling en lugar de EC2 estaticos Coatlanta/Codallas/Comumbai. |
| BMK-004 | Observabilidad y alta disponibilidad (SRE) | CAP-003 / DRV-001 | Instrumentar disponibilidad y SLOs para sustentar el salto 90% -> 99%. |
| BMK-005 | Zero-trust y seguridad por diseno | CAP-007 / DRV-005 | Fortalecer WAF/ALB/VPN IPSec con identidad, segmentacion y cifrado extremo a extremo. |
| BMK-006 | Automatizacion / IA en originacion y cobranza | CAP-001 / DRV-002 | Scoring asistido y cobranza omnicanal inteligente sobre el flujo CrossCore/Inspektor/Datacredito y WOLKVOX. |

## Comparativo AS-IS vs. estado del arte

| Dimension | Credi10 AS-IS | Patron de industria (estado del arte) | Brecha |
| --- | --- | --- | --- |
| Integracion | WS unico + archivos planos + lectura directa a BD del ERP | API-led connectivity con API gateway/management (WSO2) | Alta |
| Datos | +200 BDs duplicadas, controles en Excel (nivel grupo) | Fuente unica de verdad, data products, CDC | Alta |
| Despliegue | .NET Framework 4.8 / .NET Core 3.1 sobre IIS y EC2 estaticos | Cloud-native, contenedores, autoscaling | Media-Alta |
| Disponibilidad | 90% sin instrumentacion formal | SRE con SLOs/error budgets (99%+) | Alta |
| Seguridad | WAF + ALB + VPN IPSec perimetral | Zero-trust, identidad y microsegmentacion | Media |
| Canales | Portal B2C Wordpress/XAMPP + VTEX + B2CHAT | Experiencia digital componible (MACH) | Media |

### Donde esta la brecha mas grande

Las brechas 'Alta' se concentran en **integracion** y **datos**, que son justamente los frentes que la Fase 3 convierte en los gaps de mayor costo de inaccion. La brecha en disponibilidad es alta por falta de instrumentacion, no necesariamente por mala arquitectura: se cierra con observabilidad antes que con grandes rediseños.
## Implicaciones para la estimacion

Anclar cada frente a un benchmark conocido permite usar **referencias de industria** para calibrar el esfuerzo, reduciendo la incertidumbre frente a estimar en el vacio. Los frentes con brecha 'Alta' concentran el grueso de los story points.

## Implicaciones para la estrategia de implementacion

La estrategia adopta API-led connectivity como columna vertebral: primero la plataforma de gestion de APIs, luego los dominios. El comparativo justifica por que ese orden maximiza el cierre de brechas por unidad de esfuerzo.

## Riesgos e incertidumbre

El riesgo es adoptar patrones por moda y no por ajuste al problema. El posicionamiento Hype Cycle (abajo) mitiga esto marcando que adoptar ya y que solo pilotar. [DOC-ASSUMPTION]


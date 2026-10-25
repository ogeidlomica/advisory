# Matriz RAID (supuestos, restricciones, dependencias, prerrequisitos)

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 5 - Roadmap, Estimacion y RAID**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../05-roadmap-estimacion-raid.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

La matriz **RAID** consolida los supuestos, restricciones, dependencias y prerrequisitos que condicionan la ejecucion. Es el contrato de realidad del proyecto: enumera lo que debe ser cierto, lo que no puede cambiar, lo que depende de que, y lo que debe existir antes de arrancar cada frente. Sin RAID, una estimacion es una promesa sin condiciones.

Las restricciones son reales y vienen del RFP: preservar reglas de negocio, compatibilidad con proveedores actuales, continuidad operativa, dependencia del ERP Siesa y facturacion por entregables a 60 dias. Cada una moldea el roadmap y, por tanto, la estimacion de tiempos.

## Supuestos

| ID | Supuesto (Assumption) | Impacto si no se cumple | Dueno |
| --- | --- | --- | --- |
| A-01 | El equipo actual preserva el conocimiento de las reglas de negocio existentes | Reprocesos y regresiones funcionales | ORG |
| A-02 | Las cifras de tamanio (CFP/SP) se reconcilian en taller antes de comprometer olas [DOC-ASSUMPTION] | Desviacion de cronograma y costo | PM |
| A-03 | Los proveedores actuales (Siesa/UnoEE, PayU, buros) exponen contratos estables durante la transicion | Bloqueo del desacople | SA |

## Restricciones (del RFP)

| ID | Restriccion (Constraint) - fuente RFP | Implicacion en el roadmap |
| --- | --- | --- |
| R-01 | **Preservar las reglas de negocio existentes** (requisito RFP) | Toda ola migra comportamiento 1:1 antes de optimizar; se prohibe reescribir reglas sin equivalencia verificada |
| R-02 | **Flexibilidad / compatibilidad con los proveedores actuales** (RFP) | Los contratos de integracion deben convivir con Siesa/UnoEE, PayU y los buros durante la transicion |
| R-03 | **Garantizar continuidad funcional y operativa durante la transicion** (RFP) | Se adopta Strangler Fig por ola; sin big-bang; rollback por ola |
| R-04 | **Dependencia fuerte del ERP Siesa/UnoEE** | Ola 1 debe entregar Data Services + eventos antes de retirar el WS unico / la lectura directa a BD |
| R-05 | **Facturacion por entregables y pago a 60 dias** (RFP) | El flujo de caja del proveedor condiciona el tamanio de cada ola/entregable |

## Dependencias

| ID | Dependencia (Dependency) | Depende de | Habilita | Ola |
| --- | --- | --- | --- | --- |
| D-01 | Observabilidad y HA (SBB-005) | - (base) | Medicion de SLOs para el resto de olas | WAV-000 |
| D-02 | API Management (SBB-001) | WAV-000 | Exposicion gobernada de Data Services y dominios | WAV-001 |
| D-03 | Data Services + eventos sobre Siesa (SBB-002, SBB-003, MOD-16) | WAV-001 (API Management) | Retiro del WS unico y de la lectura directa a BD; habilita los modulos transaccionales | WAV-001 |
| D-04 | Migracion a .NET 8 y plataforma de datos (SBB-006, SBB-004) | WAV-001 (integracion gobernada) | Escalamiento y canal B2C | WAV-002 |
| D-05 | Canal B2C y escalamiento (SBB-004) | WAV-002 | Cierre del alcance | WAV-003 |

## Prerrequisitos

| ID | Prerrequisito (Issue / Prerequisite) | Estado | Ola que lo exige |
| --- | --- | --- | --- |
| P-01 | Inventario funcional de reglas de negocio a preservar | Pendiente [DOC-ASSUMPTION] | WAV-000 |
| P-02 | Linea base de disponibilidad medida (hoy sin instrumentar) [EPISTEMIC-VOID] | Pendiente | WAV-000 |
| P-03 | Catalogo de contratos de Siesa/UnoEE, PayU y buros | Pendiente | WAV-001 |
| P-04 | Pipeline CI/CD y contenedores para .NET 8 | Pendiente | WAV-002 |

### Como el RAID disciplina la estimacion

Cada prerrequisito no cumplido es un bloqueo de ola; cada dependencia define un orden obligatorio; cada restriccion acota el espacio de solucion. El RAID es, en la practica, la lista de condiciones bajo las cuales la estimacion es valida.
## Implicaciones para la estimacion

Los supuestos de estimacion (reconciliar tallas en taller, estabilidad de contratos de proveedores) condicionan la validez de las cifras. La facturacion por entregables a 60 dias condiciona el tamanio de cada ola. [DOC-ASSUMPTION]

## Implicaciones para la estrategia de implementacion

La estrategia respeta las restricciones duras del RFP: Strangler Fig y rollback por ola para continuidad, preservacion de reglas, convivencia con Siesa/UnoEE y proveedores durante la transicion.

## Riesgos e incertidumbre

El riesgo es arrancar una ola con prerrequisitos abiertos (p. ej. sin el catalogo de contratos de Siesa). El RAID hace ese riesgo visible y asignable. [EPISTEMIC-VOID] en la linea base de disponibilidad (P-02).


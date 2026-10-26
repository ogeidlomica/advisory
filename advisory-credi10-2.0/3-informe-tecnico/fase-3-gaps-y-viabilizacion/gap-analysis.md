# Matriz de dolores, causas raiz y gap analysis

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 3 + 3.5 - Gaps y Viabilizacion**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../03-gaps-y-viabilizacion.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

Aqui el advisory pasa del diagnostico al **caso de cambio**. Los dolores del assessment WSO2/Studio F se convierten en gaps cuantificables (GAP-001..005), cada uno con su causa raiz y su costo de inaccion, y se ligan a un indicador del RFP. Este es el pivote narrativo del informe: todo lo que vimos en el AS-IS cristaliza en una lista acotada de problemas que el proyecto debe resolver, y esa lista es la base del alcance y de la estimacion.

Importa porque **un gap bien definido es un trozo de alcance estimable**. El gap analysis multidominio (TOGAF B/C/D) asegura que no se nos escape ninguna dimension (negocio, datos, aplicacion, tecnologia), de modo que la estimacion sea completa y no solo tecnica.

## Matriz cuantificada de dolores y costo de inaccion

| Hilo Dorado | Dolor (assessment WSO2/Studio F) | Causa raiz | Costo de Inaccion (COI) | Driver | Benchmark |
| --- | --- | --- | --- | --- | --- |
| GAP-001 | Integracion rigida con Siesa (archivos planos + WS unico, batch, errores con intervencion manual) | WS unico como cuello de botella; acoplamiento punto a punto | Sobrecosto operativo por reprocesos manuales y demoras batch [DOC-ASSUMPTION] | DRV-002 | BMK-001 |
| GAP-002 | Lectura/escritura directa a la BD del ERP Siesa (practica de ALTO RIESGO) | El WS unico no soporta la carga; se evade el contrato | Riesgo de corrupcion de datos del ERP e indisponibilidad [DOC-ASSUMPTION] | DRV-001 | BMK-002 |
| GAP-003 | +200 BDs duplicadas/inconsistentes, logica repetida y controles manuales en Excel | Ausencia de fuente unica de verdad y de dominios de datos | Horas-hombre en conciliacion manual y errores de datos [DOC-ASSUMPTION] | DRV-002 | BMK-002 |
| GAP-004 | Apps .NET desordenadas, integraciones dispersas en Windows Services/cronjobs sin gestion centralizada ni trazabilidad | Falta de plataforma de API Management y observabilidad | Incidentes sin trazabilidad y MTTR elevado [DOC-ASSUMPTION] | DRV-004 | BMK-001 |
| GAP-005 | Obsolescencia .NET Framework 4.8 / .NET Core 3.1 (EOL) y Wordpress/XAMPP en produccion | Falta de ciclo de modernizacion y de cumplimiento de licenciamiento | Riesgo de soporte, seguridad y multas de licenciamiento [DOC-ASSUMPTION] | DRV-005 | BMK-003 |

### Lectura de la matriz

Los dos gaps de **integracion con Siesa** (GAP-001 integracion rigida y GAP-002 lectura directa a la BD) tienen el mayor costo de inaccion porque bloquean el proceso completo y arriesgan la integridad de los datos. GAP-003 (datos inconsistentes) y GAP-004 (falta de gobierno) erosionan la confianza y la eficiencia. GAP-005 (obsolescencia) es riesgo latente de soporte y seguridad. Esta jerarquia de dolor es la que ordena las primeras olas.

## Gap analysis multidominio (TOGAF B/C/D)

### Dominio B - Negocio

| Gap | Dominio B (Negocio) | AS-IS -> TO-BE | Indicador RFP |
| --- | --- | --- | --- |
| GAP-003 | Desconfianza del usuario y controles manuales en Excel | Procesos con fuente unica de verdad | DRV-002 (60% -> 80%) |
| GAP-001 | Procesos batch con intervencion manual (Siesa) | Procesos sincronizados y automatizados | DRV-002 (60% -> 80%) |
| GAP-004 | Reglas de negocio duplicadas y dispersas | Reglas centralizadas y preservadas (requisito RFP) | DRV-004 (50% -> 100%) |

### Dominio C - Datos y Aplicacion

| Gap | Dominio C (Datos) | AS-IS -> TO-BE | Indicador RFP |
| --- | --- | --- | --- |
| GAP-003 | +200 BDs duplicadas/inconsistentes | Dominios de datos con fuente unica de verdad | DRV-002 (60% -> 80%) |
| GAP-002 | Acceso directo a la BD del ERP Siesa | Data Services gobernados sobre el ERP | DRV-001 (90% -> 99%) |

| Gap | Dominio C (Aplicacion) | AS-IS -> TO-BE | Indicador RFP |
| --- | --- | --- | --- |
| GAP-004 | Apps .NET desordenadas con funciones duplicadas | Servicios de dominio desacoplados tras un API Gateway | DRV-004 (50% -> 100%) |
| GAP-001 | WS unico monolitico para todas las operaciones | APIs estandarizadas por dominio + bus de eventos | DRV-002 (60% -> 80%) |

### Dominio D - Tecnologia

| Gap | Dominio D (Tecnologia) | AS-IS -> TO-BE | Indicador RFP |
| --- | --- | --- | --- |
| GAP-005 | .NET Framework 4.8 / .NET Core 3.1 (EOL) | Runtime .NET 8 contenerizado | DRV-005 (70% -> 100%) |
| GAP-005 | Wordpress/XAMPP en produccion | Canal B2C modernizado y hardenizado | DRV-004 (50% -> 100%) |
| GAP-002 | EC2 estaticos y WS lento | Cloud-native con escalamiento y costo controlado | DRV-003 (80% -> 80%) |
## Implicaciones para la estimacion

Cada gap es una unidad de alcance con un indicador asociado; estimar el proyecto es, en primera aproximacion, estimar el cierre de GAP-001..005. El costo de inaccion (aunque marcado [DOC-ASSUMPTION] por falta de cifras reales) permite priorizar por valor, no solo por esfuerzo.

## Implicaciones para la estrategia de implementacion

La estrategia secuencia el cierre de gaps por dependencia tecnica: no se puede cerrar GAP-002 (BD directa) sin antes habilitar la capa de integracion gobernada que resuelve GAP-001/004. Esa logica define el orden de las olas.

## Riesgos e incertidumbre

El riesgo es cerrar un gap y abrir otro (p. ej. desacoplar Siesa sin preservar las reglas de negocio). La matriz de excepciones y los relievers trazables contienen ese riesgo.


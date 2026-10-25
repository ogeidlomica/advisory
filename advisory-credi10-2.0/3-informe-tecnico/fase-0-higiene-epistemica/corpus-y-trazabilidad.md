# Corpus, trazabilidad y cobertura de evidencia

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 0 - Higiene Epistemica**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../00-higiene-epistemica.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

Antes de analizar nada, el advisory establece la **higiene epistemica**: que sabemos, con que evidencia y con que grado de confianza. Se ingirio **18** documentos (RFP, assessment WSO2/Studio F y los tres diagramas de arquitectura) de forma COMPLETA y sin muestreo, y cada afirmacion que entra al analisis queda anclada a su documento fuente con su huella `sha256`. Esta disciplina no es burocracia: es el cimiento de una estimacion defendible. Un advisory que no distingue hecho de supuesto termina estimando sobre arena, y es exactamente ese riesgo el que esta fase elimina antes de que cueste caro.

La consecuencia practica es que **la calidad de la evidencia se convierte en un parametro de la estimacion**: los frentes sustentados por evidencia fuerte se pueden tallar con confianza, mientras que los frentes sustentados por PDFs de proceso que son mayormente imagen arrastran una contingencia explicita. Mirar el corpus con honestidad es, por tanto, el primer acto de gestion de riesgo del proyecto.

## Inventario y clasificacion epistemica

El inventario de evidencia y la clasificacion de afirmaciones con las cuatro etiquetas (verificado / supuesto / conflicto / vacio) es la foto cruda de lo que el corpus permite afirmar:

| ID | Afirmacion del corpus | Fuente primaria | Etiqueta |
| --- | --- | --- | --- |
| HE-01 | Credi10 corre sobre .NET Framework 4.8 en IIS 10; integradores (CrossCore, Inspektor, Datacredito, Servicios) en .NET y Windows Services en .NET Core 8 / .NET 4.8. | Diagrama de Despliegue (PNG) | [VERIFIED-FACT] |
| HE-02 | Bases de datos SQL Server 2019 Enterprise: C10_Credi10NET (principal), C10_Inspektor, C10_Datacredito, C10_Database (Link de Recaudo); UnoEE_studiof (principal + espejo), Siesa Unoee. | Diagrama de Despliegue (PNG) | [VERIFIED-FACT] |
| HE-03 | Portal B2C: API en Node.js + React y Wordpress sobre Apache (XAMPP) con BDs MariaDB 10.4.32 (C10_B2C_Wordpress, C10_B2C); Link de Recaudo en .NET Core 3.1. | Diagrama de Despliegue (PNG) | [VERIFIED-FACT] |
| HE-04 | Integraciones de contexto: UNOEE/Siesa (ERP), PENTAHO, CROSSCORE -> INSPEKTOR -> DICTUM/Datacredito, Numrot, Link de Recaudo -> PayU, VTEX, WOLKVOX, ICOMMARKETING, B2CHAT (mayoria JSON/HTTP). | Diagrama de Contexto C4 (PNG) | [VERIFIED-FACT] |
| HE-05 | Infraestructura AWS en us-east-2, VPC STUDIO F, flujo Internet Gateway -> WAF -> ALB -> EC2 privados (Coatlanta/Codallas/Comumbai), S3, CloudWatch, NAT, Bastion y VPN IPSec (Telmex) a on-prem Cokioto. | Diagrama de Infraestructura AWS (PNG) | [VERIFIED-FACT] |
| HE-06 | El RFP 'Proyecto Credi10 2.0' (STF Group S.A., Cali/Yumbo, emitido 20-ago-2026) fija indicadores de retorno: disponibilidad 90%->99%, eficiencia de recursos 60%->80%, costo infraestructura 80%->80%, evolucion/escalamiento 50%->100%, licenciamiento 70%->100%. | RFP_CREDI10_2_0.pdf | [VERIFIED-FACT] |
| HE-07 | El assessment WSO2/Studio F describe arquitectura fragmentada con +150 aplicaciones .NET y +200 bases de datos con informacion duplicada e inconsistente. | WSO2 y Studio F - Assessment Mayo2026 | [VERIFIED-FACT] |
| HE-08 | Pain de integracion con ERP Siesa: integraciones rigidas por archivos planos, un unico Web Service para todas las operaciones, mayoria batch, y lectura/escritura directa a la BD del ERP por lentitud del WS (practica de alto riesgo). | WSO2 y Studio F - Assessment | [VERIFIED-FACT] |
| HE-09 | El universo '+150 apps .NET / +200 BDs' del assessment es a nivel Studio F / grupo completo, mientras que los diagramas acotan Credi10 a ~20 componentes. Diferencia de ALCANCE que debe resolverse antes de dimensionar. | WSO2 Assessment vs. Diagramas Credi10 | [DOC-CONFLICT] |
| HE-10 | El numero objetivo de disponibilidad (99%) presupone un baseline del 90%, pero el corpus no aporta una medicion real (instrumentacion, ventana, SLA) que lo sustente. | RFP_CREDI10_2_0.pdf | [EPISTEMIC-VOID] |
| HE-11 | No hay cifras reales de costo de infraestructura ni de gasto de licenciamiento actual en el corpus; los indicadores 80%->80% y 70%->100% carecen de linea base cuantificada. | RFP_CREDI10_2_0.pdf | [EPISTEMIC-VOID] |
| HE-12 | La mayoria de las integraciones de contexto se marcan 'JSON/HTTP', pero el corpus no detalla contratos, versiones de API ni volumetria/transaccionalidad por integracion. | Diagrama de Contexto | [EPISTEMIC-VOID] |
| HE-13 | Se asume que las reglas de negocio existentes (originacion, corte de cartera, cobranza) deben preservarse 1:1 en Credi10 2.0, segun el requisito funcional del RFP, pero su especificacion detallada no esta en el corpus. | RFP_CREDI10_2_0.pdf | [DOC-ASSUMPTION] |
| HE-14 | Se asume que los 13 PDFs de proceso (Originacion, GenerarPagos FT-SL-003, ProcesoCorteCartera FT-SL-004, LinkDePagos FT-SL-011, B2C, etc.) reflejan el AS-IS vigente; son imagen-pesados y su texto es evidencia secundaria de soporte. | PDFs de proceso | [DOC-ASSUMPTION] |

### Lectura analitica de la clasificacion

La tabla cuenta una historia: el **stack tecnologico y la topologia** (componentes .NET, bases SQL Server, infraestructura AWS, integraciones de contexto) estan bien soportados por los diagramas y se etiquetan [VERIFIED-FACT], mientras que casi todo lo **cuantitativo de negocio** (lineas base de disponibilidad, costos, volumetria de integraciones) cae en [EPISTEMIC-VOID]. Esa asimetria es decisiva: podemos estimar el **esfuerzo de construccion** con relativa confianza, pero NO podemos todavia comprometer el **retorno economico** sin cerrar los vacios. La estimacion honesta separa esas dos cosas.

## Supuestos y vacios que marcan el ritmo del proyecto

Los vacios y supuestos no se ocultan: se vuelven una **agenda de elicitacion** con responsable asignado. Cada pregunta abierta que no se cierra a tiempo es una fuente potencial de retrabajo y, por tanto, de desfase de cronograma.

| ID | Pregunta abierta (delta) | Vacio/Conflicto que cierra | Responsable |
| --- | --- | --- | --- |
| DEL-01 | Cual es la medicion real de disponibilidad actual y bajo que SLA/ventana se calculo el 90%? | HE-10 [EPISTEMIC-VOID] | Cliente / EM |
| DEL-02 | Cuales son los costos reales de infraestructura AWS/on-prem y el gasto de licenciamiento vigente? | HE-11 [EPISTEMIC-VOID] | FIN / Cliente |
| DEL-03 | Que subconjunto exacto de los +150 apps y +200 BDs pertenece al perimetro Credi10 vs. al grupo Studio F? | HE-09 [DOC-CONFLICT] | EA / TDA |
| DEL-04 | Que contratos, versiones y volumetria tiene cada integracion JSON/HTTP de contexto? | HE-12 [EPISTEMIC-VOID] | DA / TDA |
| DEL-05 | Donde esta la especificacion detallada de las reglas de negocio a preservar (originacion, corte, cobranza)? | HE-13 [DOC-ASSUMPTION] | BA / DRE |
| DEL-06 | Que operaciones usan hoy lectura/escritura directa a la BD del ERP y cual es su criticidad? | HE-08 [VERIFIED-FACT] | DA / SEC |
## Implicaciones para la estimacion

La higiene epistemica fija el **nivel de confianza** de cada cifra aguas abajo. Donde la evidencia es fuerte, la talla T-Shirt se puede comprometer; donde hay [EPISTEMIC-VOID] (p. ej. la linea base del 90% de disponibilidad o el contrato real del Web Service de Siesa), la estimacion carga una **contingencia explicita** y se marca [DOC-ASSUMPTION]. Sin esta fase la estimacion pareceria mas precisa de lo que realmente es, que es el peor error posible.

## Implicaciones para la estrategia de implementacion

La estrategia de implementacion arranca por **cerrar deltas**: las preguntas de la agenda de elicitacion (DEL-01..DEL-06) deben resolverse en el arranque, porque condicionan el alcance real. En particular, el conflicto de alcance Studio F vs. Credi10 (DEL-03) define cuanto del universo entra en el proyecto y, por tanto, el tamanio de todas las olas.

## Riesgos e incertidumbre

El riesgo dominante de esta fase es el **riesgo de alcance**: si el conflicto +150 apps / +200 BDs (nivel grupo) vs. ~20 componentes (Credi10) no se resuelve, cualquier estimacion puede desviarse por un factor grande. Se mitiga tratando el delta como prerrequisito duro antes de comprometer fechas. [DOC-CONFLICT]


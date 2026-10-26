# Deuda tecnica y riesgos del AS-IS

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 1 - Contexto AS-IS**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../01-contexto-as-is.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

La deuda tecnica del AS-IS no es una lista de quejas: es el **motor del caso de negocio**. Cada item de deuda (runtime obsoleto, lectura directa a la BD del ERP, Wordpress en produccion, integraciones dispersas, +200 BDs duplicadas) se traduce mas adelante en un gap, un reliever y un bloque de solucion. Interpretar la deuda es, en realidad, dimensionar el trabajo de modernizacion.

El hilo narrativo con la fase anterior es directo: la higiene epistemica verifico estas practicas de alto riesgo como hechos [VERIFIED-FACT]; aqui las ordenamos por impacto en los drivers para que la priorizacion sea defendible.

## Catalogo de deuda tecnica

| ID | Deuda / obsolescencia tecnica | Riesgo | Driver impactado |
| --- | --- | --- | --- |
| DT-01 | .NET Framework 4.8 en plataforma e integradores | Marco legado, sin evolucion de features; riesgo de soporte | DRV-004, DRV-005 |
| DT-02 | .NET Core 3.1 en Link de Recaudo | Fuera de soporte (end-of-life) | DRV-004, DRV-005 |
| DT-03 | Wordpress + XAMPP/Apache en produccion | Superficie de ataque y operacion fragil para un canal B2C | DRV-001, DRV-004 |
| DT-04 | Lectura/escritura directa a la BD del ERP Siesa | Acoplamiento fuerte y riesgo de integridad de datos | DRV-002 |
| DT-05 | Integraciones dispersas en Windows Services/cronjobs sin gestion centralizada ni trazabilidad de errores | Baja gobernanza, intervencion manual | DRV-002, DRV-004 |
| DT-06 | +200 bases de datos duplicadas con controles manuales en Excel (nivel grupo) | Inconsistencia de datos | DRV-002 |

### De la deuda a la decision

La deuda de **acceso directo a la BD del ERP Siesa** (DT-04) es la mas peligrosa porque combina alto riesgo de integridad con alto acoplamiento; por eso el TO-BE la prohibe explicitamente (ADR-002). La obsolescencia de runtime (DT-01, DT-02) es la mas extensa en esfuerzo porque toca muchos componentes. Esta distincion riesgo vs. esfuerzo es la que permite secuenciar: primero lo peligroso, luego lo extenso.
## Implicaciones para la estimacion

Cada item de deuda se convierte en un multiplicador de esfuerzo en la estimacion por modulo (factor de acople legado = 1,20 en la tabla parametrica de la Fase 5). La deuda es, literalmente, un parametro de la ecuacion de estimacion.

## Implicaciones para la estrategia de implementacion

La estrategia prioriza por **riesgo x impacto en drivers**: las practicas de alto riesgo (BD directa, Wordpress en produccion) se atacan en las primeras olas aunque su esfuerzo sea moderado, porque su costo de inaccion es alto.

## Riesgos e incertidumbre

El meta-riesgo es que la deuda tecnica crezca mas rapido de lo que se paga. Por eso el roadmap intercala modernizacion con entrega de valor y no la pospone al final.


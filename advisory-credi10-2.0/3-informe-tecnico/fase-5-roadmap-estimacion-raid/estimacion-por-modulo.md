# Estimacion por modulo y modelo parametrico

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 5 - Roadmap, Estimacion y RAID**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../05-roadmap-estimacion-raid.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

Esta es la fase que da sentido a todo el advisory: una **estimacion por modulo** derivada de un modelo parametrico recalibrable, con cobertura COMPLETA de los modulos declarados (**17** modulos, sin muestreo). Cada modulo recibe una talla T-Shirt, story points ajustados, person-months y un WSJF, todo calculado de forma determinista a partir de parametros explicitos. La clave es la honestidad: **todas las cifras de esfuerzo son [DOC-ASSUMPTION]**, esfuerzo relativo para dimensionar, no un compromiso de fechas.

El objetivo declarado del engagement es 'estimar lo mas acertado posible'. Este modelo lo logra no inventando precision falsa, sino haciendo explicitos los supuestos: cambiar un parametro recalcula toda la estimacion, lo que permite hacer sensibilidad y converger con el equipo tecnico en un taller.

## Tabla parametrica recalibrable

| Parametro | Simbolo | Valor asumido [DOC-ASSUMPTION] | Que recalibra |
| --- | --- | --- | --- |
| Productividad (velocidad del squad) | v | 20 SP / person-month | Convierte story points en person-months |
| Factor de complejidad tecnica | fc | 1.15 | Sube/baja el esfuerzo por complejidad intrinseca |
| Factor de acople con legado | fl | 1.20 | Penaliza el acople con Siesa/.NET 4.8/Wordpress |
| Factor de riesgo de integracion | fi | 1.25 | Penaliza integracion con terceros (buros, PayU, WOLKVOX, VTEX) |

| Talla T-Shirt | Story points base (SP_base) [DOC-ASSUMPTION] |
| --- | --- |
| XS | 5 |
| S | 13 |
| M | 21 |
| L | 40 |
| XL | 80 |

> **Como se derivan las cifras (recalibrable).** Para cada modulo:
>
> `SP_ajustado = round(SP_base x fc x fl x fi)`
>
> `person_months = SP_ajustado / v`
>
> Con los valores asumidos [DOC-ASSUMPTION] el multiplicador compuesto es `fc x fl x fi = 1.15 x 1.20 x 1.25 = 1.725` y la velocidad `v = 20 SP/person-month`. Cambiar cualquier celda de la tabla parametrica o de los story points base recalcula TODA la estimacion por modulo de forma determinista. Las cifras son esfuerzo **relativo** [DOC-ASSUMPTION], no una oferta ni un compromiso de fechas absolutas.

## Estimacion detallada por modulo

| Modulo | Nombre | Bounded Context | Talla | SP base | SP ajustado [DOC-ASSUMPTION] | Person-months [DOC-ASSUMPTION] | CoD | Job Size | WSJF |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MOD-01 | Plataforma Credi10 / Administracion de creditos | Plataforma / Core | L | 40 | 69 | 3,45 | 23 | 8 | 2.88 |
| MOD-02 | Originacion - CrossCore | Estudio de Credito | M | 21 | 36 | 1,80 | 24 | 5 | 4.8 |
| MOD-03 | Originacion - Inspektor | Estudio de Credito | M | 21 | 36 | 1,80 | 21 | 5 | 4.2 |
| MOD-04 | Originacion - Datacredito | Estudio de Credito | M | 21 | 36 | 1,80 | 24 | 5 | 4.8 |
| MOD-05 | Originacion - Aplicacion ADMIN | Originacion | M | 21 | 36 | 1,80 | 17 | 5 | 3.4 |
| MOD-06 | Pagos / GenerarPagos | Pagos | S | 13 | 22 | 1,10 | 19 | 3 | 6.33 |
| MOD-07 | Corte de Cartera | Corte / Cartera | M | 21 | 36 | 1,80 | 20 | 5 | 4.0 |
| MOD-08 | Link de Recaudo / APIs de recaudo | Recaudo | M | 21 | 36 | 1,80 | 25 | 5 | 5.0 |
| MOD-09 | B2C / Portal de clientes | B2C / E-commerce | L | 40 | 69 | 3,45 | 19 | 8 | 2.38 |
| MOD-10 | Boton E-commerce | B2C / E-commerce | S | 13 | 22 | 1,10 | 16 | 3 | 5.33 |
| MOD-11 | Captura Foto | Originacion | S | 13 | 22 | 1,10 | 14 | 3 | 4.67 |
| MOD-12 | API Integrador Atencion al Cliente | Atencion al Cliente | M | 21 | 36 | 1,80 | 19 | 5 | 3.8 |
| MOD-13 | Llamada Predictiva | Cobranza | S | 13 | 22 | 1,10 | 17 | 3 | 5.67 |
| MOD-14 | Cobranza (SMS / WhatsApp / Email / Scheduler) | Cobranza | M | 21 | 36 | 1,80 | 20 | 5 | 4.0 |
| MOD-15 | Envio RCL y RCR | Integracion ERP | M | 21 | 36 | 1,80 | 21 | 5 | 4.2 |
| MOD-16 | Integracion UnoEE / Siesa | Integracion ERP | XL | 80 | 138 | 6,90 | 29 | 13 | 2.23 |
| MOD-17 | Fidelizacion / Pentaho (BI) | Cartera | S | 13 | 22 | 1,10 | 13 | 3 | 4.33 |

> **Totales agregados [DOC-ASSUMPTION].** Sumando los **17** modulos (cobertura COMPLETA, sin muestreo): **710 story points ajustados** y **~35,50 person-months**. Es esfuerzo relativo para dimensionar olas y squads, no un compromiso de fechas: debe reconciliarse en taller antes de comprometer el cronograma.

## Descomposicion del esfuerzo por frente

| Modulo | Person-months | Dev | Data | Integracion | QA | DevOps | Gestion del cambio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MOD-01 | 3,45 | 1,38 | 0,52 | 0,69 | 0,41 | 0,28 | 0,17 |
| MOD-02 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-03 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-04 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-05 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-06 | 1,10 | 0,44 | 0,17 | 0,22 | 0,13 | 0,09 | 0,06 |
| MOD-07 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-08 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-09 | 3,45 | 1,38 | 0,52 | 0,69 | 0,41 | 0,28 | 0,17 |
| MOD-10 | 1,10 | 0,44 | 0,17 | 0,22 | 0,13 | 0,09 | 0,06 |
| MOD-11 | 1,10 | 0,44 | 0,17 | 0,22 | 0,13 | 0,09 | 0,06 |
| MOD-12 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-13 | 1,10 | 0,44 | 0,17 | 0,22 | 0,13 | 0,09 | 0,06 |
| MOD-14 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-15 | 1,80 | 0,72 | 0,27 | 0,36 | 0,22 | 0,14 | 0,09 |
| MOD-16 | 6,90 | 2,76 | 1,03 | 1,38 | 0,83 | 0,55 | 0,34 |
| MOD-17 | 1,10 | 0,44 | 0,17 | 0,22 | 0,13 | 0,09 | 0,06 |
| **Total [DOC-ASSUMPTION]** | **35,50** | **14,20** | **5,33** | **7,10** | **4,26** | **2,84** | **1,77** |

> **Descomposicion por frente [DOC-ASSUMPTION].** Cada modulo reparte sus person-months segun un perfil fijo recalibrable: Dev 40%, Data 15%, Integracion 20%, QA 12%, DevOps 8%, Gestion del cambio 5% (suma 100%). El perfil representa el mix tipico de un equipo stream-aligned con soporte de la plataforma de integracion; se ajusta en el taller de estimacion por modulo.

### Como leer la estimacion

Los modulos de integracion (MOD-16 Siesa, talla XL) y de plataforma (MOD-01, MOD-09) concentran el esfuerzo. La descomposicion por frente revela que Dev no es el unico costo: integracion, QA y gestion del cambio suman una porcion significativa, algo que las estimaciones ingenuas suelen olvidar.
## Implicaciones para la estimacion

Esta seccion ES la estimacion. Su valor esta en ser **parametrica y auditable**: cada cifra se deriva de la talla y los factores, de modo que una recalibracion (nueva productividad, nuevos factores) actualiza todo el modelo sin reescribir a mano. Las cifras son relativas [DOC-ASSUMPTION] y deben reconciliarse en taller.

## Implicaciones para la estrategia de implementacion

La estimacion por frente informa la composicion de los squads (Team Topologies): cuanto Dev, Data, Integracion y QA necesita cada ola. Es insumo directo del dimensionamiento de equipos.

## Riesgos e incertidumbre

El riesgo es tomar las cifras como compromiso de fechas. Se mitiga marcando todo [DOC-ASSUMPTION] y atando la incertidumbre a la cobertura del corpus (ver riesgo de desfase).


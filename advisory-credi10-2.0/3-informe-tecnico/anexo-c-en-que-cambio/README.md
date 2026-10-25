# Anexo C - En que cambio: evidencia ANTES vs AHORA y suficiencia para definir el proyecto

> **Anexo del informe tecnico** de Credi10 2.0. Responde, con cifras leidas de la Base de Conocimiento del run, la pregunta del negocio: tras recuperar la capa de texto nativa de los documentos que antes eran **vacios epistemicos**, ¿con esta informacion podemos definir el proyecto con tranquilidad y, si no, que % exige todavia una **conceptualizacion / etapa de especificacion** adicional? Es un artefacto **generado** y **determinista** (se recomputa si el corpus cambia); no se escribe a mano.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** texto nativo util recuperado (incluida la decodificacion de fuentes) o transcripcion humana; **[EPISTEMIC-VOID]** no recuperable / ausente (no se fabrica); **[DOC-ASSUMPTION]** supuesto a validar.

## 1. Que cambio en una frase

La recuperacion de texto nativo (L1: `/ToUnicode` por fuente + reconstruccion lexica) movio a **5 de 5** documentos desde el **vacio epistemico** ([EPISTEMIC-VOID]) hacia **evidencia verificada** ([VERIFIED-FACT]). En concreto, el Assessment WSO2/Studio F paso de **1.60%** de texto util (vacio epistemico) a **74.90%** ([VERIFIED-FACT]). El corpus paso de **5 documentos en vacio** a **0 en vacio** hoy, y esos cinco documentos, que antes aportaban **~0** hechos clave trazables, hoy aportan **60** (de un total de **193** hechos clave en todo el corpus). El diagnostico, la arquitectura y la estimacion de los frentes que dependian de esos documentos dejan de apoyarse en supuestos y pasan a citar evidencia real.

## 2. ANTES vs AHORA de los documentos recuperados

Las cifras 'antes' son la linea base declarativa previa a la decodificacion de fuentes (`knowledge.USEFUL_TEXT_BASELINE_PCT`); las 'ahora', la banda, el flag y el conteo de hechos se leen de la Base de Conocimiento viva. No hay cifras hardcodeadas en esta tabla.

| # | Documento (antes [EPISTEMIC-VOID]) | Texto util antes | Texto util ahora | Delta | Banda ahora | Flag ahora | Hechos clave |
| --- | --- | ---: | ---: | ---: | --- | --- | ---: |
| 1 | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | 1.60% | 74.90% | +73.30 pp | alta | [VERIFIED-FACT] | 12 |
| 2 | Api Integrador Atencion al cliente.pdf | 0.70% | 69.65% | +68.95 pp | alta | [VERIFIED-FACT] | 12 |
| 3 | Originacion_API_Inspektor.pdf | 0.99% | 69.31% | +68.32 pp | alta | [VERIFIED-FACT] | 12 |
| 4 | ProcesoCorteCartera.pdf | 1.09% | 54.15% | +53.06 pp | alta | [VERIFIED-FACT] | 12 |
| 5 | B2C.pdf | 2.55% | 55.54% | +52.99 pp | alta | [VERIFIED-FACT] | 12 |

## 3. Balance epistemico del corpus (18 documentos)

| Metrica | Antes (linea base) | Ahora (KB viva) |
| --- | ---: | ---: |
| Documentos en [EPISTEMIC-VOID] | 5 | 0 |
| Documentos recuperados a [VERIFIED-FACT] | 0 | 5 |
| Hechos clave aportados por esos 5 documentos | ~0 | 60 |
| Hechos clave trazables en todo el corpus | - | 193 |

> El salto de **5 -> 0** vacios epistemicos es el cambio estructural: ya no hay modulos cuyo soporte documental sea 'solo imagen' / sin capa de texto. Lo que resta en vacio no son documentos sino **mediciones** que el corpus nunca contuvo (SLA/latencia instrumentada, linea base de costos), que se levantan en el sprint 0, no por mas OCR.

## 4. Que secciones del advisory ganaron fundamento

Cada documento recuperado aterriza en secciones concretas del advisory, que pasan de [DOC-ASSUMPTION] a [VERIFIED-FACT]:

| Documento recuperado | Secciones del advisory que ganan evidencia |
| --- | --- |
| `WSO2 y Studio F - Assessment Mayo2026-Final.pdf` | Integracion / gobierno de APIs (MOD-16, desacople Siesa/UnoEE): diagnostico AS-IS fase 1, gaps fase 3, ruta critica de la estimacion fase 5 |
| `Originacion_API_Inspektor.pdf` | Originacion - estudio de credito Inspektor (MOD-03): specs de modulo e historias fase 4 |
| `ProcesoCorteCartera.pdf` | Corte y gestion de cartera (MOD-07): specs de modulo e historias fase 4 |
| `B2C.pdf` | Canales digitales / portal B2C (MOD-09): specs de modulo fase 4 |
| `Api Integrador Atencion al cliente.pdf` | Integrador de atencion al cliente (MOD-12): specs de modulo fase 4 |

## 5. Evidencia concreta recuperada (muestra trazable)

Muestra de hechos clave recuperados (leidos de la KB; cada uno trazable a su documento fuente), que antes eran inaccesibles:

### WSO2 y Studio F - Assessment Mayo2026-Final.pdf

Evidencia recuperada de `WSO2 y Studio F - Assessment Mayo2026-Final.pdf` (banda **alta**, **[VERIFIED-FACT]**):

| Hecho recuperado [VERIFIED-FACT] | Tokens | Fuente |
| --- | --- | --- |
| Gestionar todas las APIs de manera Centralizada 19 5.3. | API | WSO2 y Studio F - Assessment Mayo2026-Final.pdf |
| Objetivo del Documento Evaluar el contexto actual de Studio F para analizar las oportunidades de mejora y en su arquitectura, donde las soluciones WSO2 API Plat... | WSO2, Studio F, API | WSO2 y Studio F - Assessment Mayo2026-Final.pdf |
| Contexto de Negócio Studio F cuenta con una arquitectura fragmentada y un ecosistema de sistemas y aplicaciones desactualizados, compuestos por más de 150 aplic... | .NET, Studio F | WSO2 y Studio F - Assessment Mayo2026-Final.pdf |
| Actualmente, el ecosistema depende de integraciones "punto a punto" y procesos batch (archivos planos) hacia su ERP Siesa. | Siesa | WSO2 y Studio F - Assessment Mayo2026-Final.pdf |

### Originacion_API_Inspektor.pdf

Evidencia recuperada de `Originacion_API_Inspektor.pdf` (banda **alta**, **[VERIFIED-FACT]**):

| Hecho recuperado [VERIFIED-FACT] | Tokens | Fuente |
| --- | --- | --- |
| ORI - API - 00 1 Versión:001 Fecha: | API | Originacion_API_Inspektor.pdf |
| 08/ 11 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES API IN SPEKTOR STF GROUP S.A. | API | Originacion_API_Inspektor.pdf |
| CREDI10 SOFTWARE PROPIO Cali , martes, 15 de septiembre de 2026 Código: | Credi10 | Originacion_API_Inspektor.pdf |
| En el presente documento se describe técnicamente como fue desarrollada la API que interviene en el proceso de o riginaci ó n de cupo para Credi 10. | API | Originacion_API_Inspektor.pdf |

### ProcesoCorteCartera.pdf

Evidencia recuperada de `ProcesoCorteCartera.pdf` (banda **alta**, **[VERIFIED-FACT]**):

| Hecho recuperado [VERIFIED-FACT] | Tokens | Fuente |
| --- | --- | --- |
| 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 004 - Módulo_Cartera STF GROUP S.A. | Cartera | ProcesoCorteCartera.pdf |
| CREDI10 SOFTWARE PROPIO C ali , lunes 12 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 | ProcesoCorteCartera.pdf |
| 1.1.1 Requerimiento Realizar los procesos saldos al corte, presupuesto, facturación , estados de cuenta y creación del reporte de facturas en las fechas adecuad... | Credi10 | ProcesoCorteCartera.pdf |
| 08/06/2021 1.2 Detallar componentes existentes SOLUCION CarteraWindowsServices Proyecto de tipo servicio de Windows que se ejecuta automáticamente en fechas est... | Credi10, Cartera | ProcesoCorteCartera.pdf |

### B2C.pdf

Evidencia recuperada de `B2C.pdf` (banda **alta**, **[VERIFIED-FACT]**):

| Hecho recuperado [VERIFIED-FACT] | Tokens | Fuente |
| --- | --- | --- |
| 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Portal clientes B2C STF GROUP S.A. | Portal, B2C, API | B2C.pdf |
| CREDI10 SOFTWARE PROPIO Cali , jueves 19 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 | B2C.pdf |
| 1.1.1 Requerimiento Disponer API para suministrar diferente información al portal de clientes credi10 (B2C) . | Credi10, Portal, B2C, API | B2C.pdf |
| 1.2 Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con 1 solución desarrollada en .NET Framework 4.8 llamada “Créditos”. | .NET | B2C.pdf |

### Api Integrador Atencion al cliente.pdf

Evidencia recuperada de `Api Integrador Atencion al cliente.pdf` (banda **alta**, **[VERIFIED-FACT]**):

| Hecho recuperado [VERIFIED-FACT] | Tokens | Fuente |
| --- | --- | --- |
| 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES API Integrador Atención Al Cliente STF GROUP S.A. | integrador, API | Api Integrador Atencion al cliente.pdf |
| CREDI10 SOFTWARE PROPIO Cali , viernes 26 de diciembre del 202 5 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 | Api Integrador Atencion al cliente.pdf |
| DETALLE TECNICO Requerimiento Disponer API para suministrar información de los clientes de C redi10 y generación de certificados PDF . | API | Api Integrador Atencion al cliente.pdf |
| Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con una solución desarrollada en .NET Framework 4.8 . | .NET | Api Integrador Atencion al cliente.pdf |

## 6. ¿Podemos definir el proyecto con tranquilidad? Veredicto de suficiencia

**Cobertura de evidencia documental del corpus: ~100%** (100% de los 18 documentos con [VERIFIED-FACT]). Este porcentaje mide cuanta **evidencia leible** respalda hoy el advisory, y **no** la preparacion total para **comprometer** alcance, fechas y presupuesto. La distincion es decisiva para responder la pregunta del negocio:

- **Lo que SI habilita la evidencia recuperada (suficiente para arrancar).** El diagnostico AS-IS, el catalogo de modulos/historias y la estimacion por olas ya se apoyan en texto verificado; se puede **iniciar la construccion por olas** (enablers WAV-000/WAV-001) con confianza razonable. Esto es coherente con el veredicto **GO CONDICIONADO** de la Fase 5.
- **Lo que AUN exige una etapa de conceptualizacion / especificacion.** Que la evidencia **documental** este al ~100% NO significa que la **especificacion de la solucion objetivo** lo este: la evidencia recuperada es **documentacion tecnica del AS-IS existente**, no un diseno comprometible. Persisten vacios que ningun OCR cierra porque **no estan en ningun documento**: (1) **mediciones ausentes** (SLA/latencia hoy sin instrumentar [EPISTEMIC-VOID]) y (2) **linea base de costos** para el caso de negocio [EPISTEMIC-VOID]; y las specs recuperadas de los modulos deben **ratificarse 1:1 con el cliente** (riesgo RS-03).

> **Lectura honesta (porcentajes).** La base **documental** para encuadrar el proyecto esta cubierta al **~100%**. Pero para pasar de 'arrancar' a 'comprometer alcance, fechas y presupuesto con tranquilidad' se requiere todavia una **etapa de conceptualizacion / especificacion** acotada (sprint 0 / descubrimiento), estimada en **~15-20% de esfuerzo adicional de advisory [DOC-ASSUMPTION]**, que cierre lo que el corpus no contiene: (a) **~10-15%** levantar la **linea base de medicion** (disponibilidad/latencia reales) y de **costos** para el caso de negocio; (b) **~5%** **ratificar las specs recuperadas** de originacion, cartera, pagos e integracion WSO2 en talleres con el cliente; y (c) **recalibrar la estimacion** con conteo funcional historico. Estos porcentajes son una **guia de advisory [DOC-ASSUMPTION]**, no una medicion; se afinan en el sprint 0. Sin ese cierre, comprometer fechas absolutas de las olas 2 y 3 incurre en alto riesgo de desfase (ver Fase 5, RS-01..RS-06).

## 7. Trazabilidad

Este anexo se deriva de la Base de Conocimiento (`knowledge-base/`) y de las constantes declarativas `engine.knowledge.USEFUL_TEXT_BASELINE_PCT` y `BASELINE_NULA_PDFS`. Complementa el **Anexo B** (arquitectura de extraccion, delta de texto util por documento) con la **lectura de consecuencia** para el negocio. Para volver al indice maestro del informe tecnico ver [`../README.md`](../README.md).


# Catalogo de oportunidades de IA

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 4 - Diseno TO-BE**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../04-diseno-to-be.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

El catalogo de IA se modela como **skill declarativo** (no hardcodeado) y distingue dos pistas: IA-como-producto (casos de uso que agregan valor al negocio) e IA-como-acelerador-de-construccion (IA que acelera el propio desarrollo). Presentarlo aqui, dentro del informe tecnico, permite evaluar su viabilidad con los datos disponibles y evitar promesas sin sustento.

Para la estimacion, la IA se trata con prudencia: la mayoria de los casos son **spikes/experimentos** acotados, no alcance firme, porque su viabilidad depende de datos cuya calidad aun no esta garantizada.

## IA como producto

| ID | Caso de uso | Modulo | Datos requeridos | Viabilidad | Gancho al roadmap |
| --- | --- | --- | --- | --- | --- |
| AIP-001 | Credit/Risk Scoring en Originacion: Modelo de scoring de credito y riesgo que complementa las reglas de CrossCore/DICTUM para decidir y priorizar solicitudes de originacion. | Originacion (CrossCore / Inspektor / Datacredito / Aplicacion ADMIN) | Historico de solicitudes y decisiones, bureau (Datacredito), variables de Inspektor, resultado de mora posterior. | Alta si existe historico etiquetado; [DOC-ASSUMPTION] sobre volumen y calidad de datos a confirmar con el cliente. | Ola 2 - capacidades de decision inteligente sobre originacion. |
| AIP-002 | Antifraude en CrossCore / Inspektor: Deteccion de fraude y anomalias en solicitudes usando senales de CrossCore e Inspektor para reducir perdidas por fraude. | Originacion (CrossCore, Inspektor) | Casos historicos de fraude confirmado, features de dispositivo/identidad, senales de CrossCore/Inspektor. | Media-alta; requiere etiquetas de fraude confiables. [DOC-ASSUMPTION] sobre disponibilidad de ground-truth. | Ola 2 - control de riesgo y fraude. |
| AIP-003 | Cobranza Predictiva y Priorizada: Priorizacion de cartera y seleccion de canal/mensaje optimo por cliente para maximizar recaudo con menor costo de contacto. | Cobranza (SMS/WhatsApp/Email/Scheduler, Llamada Predictiva) | Historico de pagos y promesas, resultados por canal, estados de mora, respuesta a campanas previas. | Alta; datos operativos de cobranza suelen existir. [DOC-ASSUMPTION] sobre granularidad de resultados por canal. | Ola 3 - optimizacion de recaudo. |
| AIP-004 | OCR / Vision en Captura de Documentos: Extraccion automatica de datos de documentos de identidad y soportes fotograficos para acelerar y validar la originacion. | Captura Foto | Imagenes de documentos capturados, ground-truth de campos extraidos, plantillas de documentos. | Alta para documentos estandar; [DOC-ASSUMPTION] sobre calidad/variedad de capturas. Nota: el motor no hace OCR en runtime (stdlib). | Ola 2 - automatizacion de captura. |
| AIP-005 | NLP / Chatbot en Atencion al Cliente: Asistente conversacional y clasificacion/ruteo de intenciones para atencion omnicanal integrada con Wolkvox y B2Chat. | Atencion al Cliente (Wolkvox, B2Chat, API Integrador) | Transcripciones y chats historicos, taxonomia de intenciones, base de conocimiento de respuestas. | Media-alta; depende de calidad de transcripciones. [DOC-ASSUMPTION] sobre volumen de conversaciones. | Ola 3 - experiencia de atencion. |
| AIP-006 | Pronostico de Cartera (Portfolio Forecasting): Pronostico de comportamiento de cartera (mora, prepago, roll-rates) para planeacion financiera y provisiones. | Cartera (Proceso Corte de Cartera, BI Pentaho) | Series historicas de cartera, cortes mensuales, variables macro, resultados de cobranza. | Media; requiere series suficientes. [DOC-ASSUMPTION] sobre profundidad historica disponible. | Ola 3 - inteligencia financiera. |

## IA como acelerador de construccion

| ID | Caso de uso | Modulo | Datos requeridos | Viabilidad | Gancho al roadmap |
| --- | --- | --- | --- | --- | --- |
| AIB-001 | Spec-to-Code: Generar scaffolding y codigo a partir de specs/HU estructuradas para acelerar la construccion de los modulos del roadmap. | Fabrica de software (rol AIA) | HU y specs AI-ready con criterios Gherkin, contratos OpenAPI/AsyncAPI, convenciones del repositorio. | Alta como acelerador; requiere specs de calidad (ver AIB-002). [DOC-ASSUMPTION] sobre adopcion del equipo. | Ola 1 - habilitadores de entrega. |
| AIB-002 | Specs AI-Ready: Estandarizar HU/specs en formato estructurado y trazable (AI-ready) para que spec-to-code y la generacion de pruebas sean fiables. | Fabrica de software (roles BA + AIA) | Plantillas de HU/Gherkin, catalogo de modulos, Hilo Dorado de trazabilidad. | Alta; es practica de proceso, bajo riesgo tecnico. | Ola 1 - habilitadores de entrega. |
| AIB-003 | Generacion Automatica de Pruebas: Derivar casos de prueba (unitarios/aceptacion) desde los criterios Gherkin de las HU para aumentar cobertura y reducir regresion. | Fabrica de software (rol AIA) | Criterios de aceptacion Gherkin, contratos de API, datos de ejemplo. | Alta cuando las specs son AI-ready (depende de AIB-002). | Ola 2 - calidad y automatizacion de pruebas. |

### Como se incorpora la IA sin inflar el alcance

Cada oportunidad lleva un gancho al roadmap y una nota de viabilidad. Las de viabilidad alta con datos disponibles pueden entrar como incremento; las demas se exploran en spikes de tiempo acotado. Asi la IA aporta valor sin convertirse en un riesgo de cronograma.
## Implicaciones para la estimacion

Las oportunidades de IA se estiman como spikes acotados salvo cuando la viabilidad es alta y los datos existen. Esto evita comprometer esfuerzo sobre casos cuya factibilidad aun es [DOC-ASSUMPTION].

## Implicaciones para la estrategia de implementacion

La estrategia prioriza primero la IA-como-acelerador (mejora la productividad del equipo desde el inicio) y difiere la IA-como-producto a cuando la plataforma de datos este consolidada.

## Riesgos e incertidumbre

El riesgo es sobreprometer capacidades de IA sin datos de calidad. El tratamiento por spikes y la nota de viabilidad por caso contienen ese riesgo. [DOC-ASSUMPTION]


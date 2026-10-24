---
name: ai-opportunities-catalog
description: Usar en la Fase 4 (diseno TO-BE) para enumerar oportunidades de IA; catalogo DECLARATIVO y legible por maquina (bloque estable que el motor parsea de forma determinista) con dos pistas, IA-como-producto e IA-como-acelerador-de-construccion, cada entrada con caso de uso, datos requeridos, viabilidad y gancho al roadmap.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: Fase 4 TO-BE, rol AIA, cualquier cliente
---

# Catalogo de oportunidades de IA (ai-opportunities-catalog)

Politica **declarativa y reutilizable**: las oportunidades de IA se modelan como
DATOS, no como codigo hardcodeado. El builder de la Fase 4 (`phases/phase4.py`,
FEAT-003) parsea el bloque `ai-catalog` de abajo con un parser stdlib
determinista y renderiza la vista de oportunidades. Credi10 2.0 aparece solo
como ejemplo; manten las entradas genericas para reutilizarlas con otros
clientes.

## Formato legible por maquina

Las entradas viven dentro de un unico bloque cercado con la etiqueta
`ai-catalog`. Cada entrada es un grupo de lineas `clave: valor` separado del
siguiente por una linea en blanco. Campos por entrada:

- `id`: identificador estable (p. ej. `AIP-001`, `AIB-001`).
- `track`: `ai-as-product` o `ai-as-build-accelerator`.
- `name`: nombre corto del caso de uso.
- `module`: modulo/contexto de aplicacion (ejemplo Credi10, generico reutilizable).
- `use_case`: descripcion del caso de uso.
- `required_data`: datos/insumos necesarios.
- `viability`: nota de viabilidad (incluye flag epistemico cuando aplique).
- `roadmap_hook`: gancho al roadmap (ola/fase sugerida).

El parser ignora cualquier texto fuera del bloque, por lo que esta prosa es
segura. El orden de las entradas en el bloque es el orden de render.

```ai-catalog
id: AIP-001
track: ai-as-product
name: Credit/Risk Scoring en Originacion
module: Originacion (CrossCore / Inspektor / Datacredito / Aplicacion ADMIN)
use_case: Modelo de scoring de credito y riesgo que complementa las reglas de CrossCore/DICTUM para decidir y priorizar solicitudes de originacion.
required_data: Historico de solicitudes y decisiones, bureau (Datacredito), variables de Inspektor, resultado de mora posterior.
viability: Alta si existe historico etiquetado; [DOC-ASSUMPTION] sobre volumen y calidad de datos a confirmar con el cliente.
roadmap_hook: Ola 2 - capacidades de decision inteligente sobre originacion.

id: AIP-002
track: ai-as-product
name: Antifraude en CrossCore / Inspektor
module: Originacion (CrossCore, Inspektor)
use_case: Deteccion de fraude y anomalias en solicitudes usando senales de CrossCore e Inspektor para reducir perdidas por fraude.
required_data: Casos historicos de fraude confirmado, features de dispositivo/identidad, senales de CrossCore/Inspektor.
viability: Media-alta; requiere etiquetas de fraude confiables. [DOC-ASSUMPTION] sobre disponibilidad de ground-truth.
roadmap_hook: Ola 2 - control de riesgo y fraude.

id: AIP-003
track: ai-as-product
name: Cobranza Predictiva y Priorizada
module: Cobranza (SMS/WhatsApp/Email/Scheduler, Llamada Predictiva)
use_case: Priorizacion de cartera y seleccion de canal/mensaje optimo por cliente para maximizar recaudo con menor costo de contacto.
required_data: Historico de pagos y promesas, resultados por canal, estados de mora, respuesta a campanas previas.
viability: Alta; datos operativos de cobranza suelen existir. [DOC-ASSUMPTION] sobre granularidad de resultados por canal.
roadmap_hook: Ola 3 - optimizacion de recaudo.

id: AIP-004
track: ai-as-product
name: OCR / Vision en Captura de Documentos
module: Captura Foto
use_case: Extraccion automatica de datos de documentos de identidad y soportes fotograficos para acelerar y validar la originacion.
required_data: Imagenes de documentos capturados, ground-truth de campos extraidos, plantillas de documentos.
viability: Alta para documentos estandar; [DOC-ASSUMPTION] sobre calidad/variedad de capturas. Nota: el motor no hace OCR en runtime (stdlib).
roadmap_hook: Ola 2 - automatizacion de captura.

id: AIP-005
track: ai-as-product
name: NLP / Chatbot en Atencion al Cliente
module: Atencion al Cliente (Wolkvox, B2Chat, API Integrador)
use_case: Asistente conversacional y clasificacion/ruteo de intenciones para atencion omnicanal integrada con Wolkvox y B2Chat.
required_data: Transcripciones y chats historicos, taxonomia de intenciones, base de conocimiento de respuestas.
viability: Media-alta; depende de calidad de transcripciones. [DOC-ASSUMPTION] sobre volumen de conversaciones.
roadmap_hook: Ola 3 - experiencia de atencion.

id: AIP-006
track: ai-as-product
name: Pronostico de Cartera (Portfolio Forecasting)
module: Cartera (Proceso Corte de Cartera, BI Pentaho)
use_case: Pronostico de comportamiento de cartera (mora, prepago, roll-rates) para planeacion financiera y provisiones.
required_data: Series historicas de cartera, cortes mensuales, variables macro, resultados de cobranza.
viability: Media; requiere series suficientes. [DOC-ASSUMPTION] sobre profundidad historica disponible.
roadmap_hook: Ola 3 - inteligencia financiera.

id: AIB-001
track: ai-as-build-accelerator
name: Spec-to-Code
module: Fabrica de software (rol AIA)
use_case: Generar scaffolding y codigo a partir de specs/HU estructuradas para acelerar la construccion de los modulos del roadmap.
required_data: HU y specs AI-ready con criterios Gherkin, contratos OpenAPI/AsyncAPI, convenciones del repositorio.
viability: Alta como acelerador; requiere specs de calidad (ver AIB-002). [DOC-ASSUMPTION] sobre adopcion del equipo.
roadmap_hook: Ola 1 - habilitadores de entrega.

id: AIB-002
track: ai-as-build-accelerator
name: Specs AI-Ready
module: Fabrica de software (roles BA + AIA)
use_case: Estandarizar HU/specs en formato estructurado y trazable (AI-ready) para que spec-to-code y la generacion de pruebas sean fiables.
required_data: Plantillas de HU/Gherkin, catalogo de modulos, Hilo Dorado de trazabilidad.
viability: Alta; es practica de proceso, bajo riesgo tecnico.
roadmap_hook: Ola 1 - habilitadores de entrega.

id: AIB-003
track: ai-as-build-accelerator
name: Generacion Automatica de Pruebas
module: Fabrica de software (rol AIA)
use_case: Derivar casos de prueba (unitarios/aceptacion) desde los criterios Gherkin de las HU para aumentar cobertura y reducir regresion.
required_data: Criterios de aceptacion Gherkin, contratos de API, datos de ejemplo.
viability: Alta cuando las specs son AI-ready (depende de AIB-002).
roadmap_hook: Ola 2 - calidad y automatizacion de pruebas.
```

## Garantias de parseo

- Bloque cercado con etiqueta `ai-catalog`; entradas separadas por linea en blanco.
- Claves en minuscula, formato `clave: valor`; sin dependencias de PyYAML.
- Orden estable = orden de render; parser determinista (ver `engine/skills.py`).
- Si el skill falta, el motor degrada con gracia (catalogo vacio) y sigue corriendo.

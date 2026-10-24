---
name: complete-corpus-ingestion
description: Usar al iniciar cualquier engagement de advisory o analisis sobre un corpus documental; obliga a ingerir y validar TODA la documentacion (sin muestreo parcial) y define como probar que cada documento fue procesado y entendido.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los engagements, cualquier cliente, cualquier corpus
---

# Politica: Ingesta completa del corpus (complete-corpus-ingestion)

Politica **permanente y reutilizable** de la organizacion. No es especifica de
ningun cliente. Credi10 2.0 se cita solo como *ejemplo de aplicacion*, nunca
como el sujeto de la politica.

## 1. Principio (no negociable)

> **SIEMPRE tomar y validar la informacion y el contexto de TODA la
> documentacion disponible.** Esta prohibido el muestreo parcial: no se decide
> alcance, arquitectura, estimacion ni riesgo a partir de "algunos" documentos.

La clasificacion `primary` / `secondary` es **PRIORIDAD de esfuerzo y orden de
lectura**, nunca un criterio de **exclusion**. Un documento secundario se lee
mas tarde o con menor profundidad inicial, pero se ingiere, se resume y se
registra igual que uno primario.

## 2. Inventario exhaustivo (paso obligatorio)

1. Enumerar **todos** los artefactos del corpus (PDF, PNG/diagramas, hojas de
   calculo, texto, correos, transcripciones, etc.).
2. Registrar por documento: `filename`, `tipo`, `tamano (bytes)`, `sha256`.
3. No continuar a ninguna fase de analisis hasta que el inventario cubra el
   100% de los artefactos descubiertos en la raiz del corpus.

## 3. Clasificacion por documento

Cada documento recibe:

- **tipo**: formato/medio (pdf, png, ...).
- **rol de prioridad**: `primary` (evidencia decisoria densa: RFP, assessments,
  contratos) o `secondary` (soporte, diagramas, anexos). PRIORIDAD, no exclusion.
- **metodo de ingesta**: como se extrajo el contenido (p. ej. `zlib+regex` para
  la capa de texto PDF, `transcripcion estatica` para imagenes sin OCR).

## 4. Validacion de cobertura

Para cada documento se calcula y registra:

- **longitud raw** y **longitud limpia** del texto recuperado.
- **ratio de cobertura** = longitud_limpia / tamano, acotado a [0, 1].
- **banda de cobertura**: `alta` / `media` / `baja` / `nula` (umbrales
  parametricos y recalibrables).
- **flag epistemico honesto**: `[VERIFIED-FACT]` cuando hay capa de texto util;
  `[EPISTEMIC-VOID]` cuando el documento no aporta texto explotable (p. ej. PDF
  solo-imagen). **Nunca se fabrica contenido** para rellenar un vacio.

## 5. Definicion de DONE (prueba de procesamiento y entendimiento)

Un documento esta "ingerido y entendido" solo si existe, de forma trazable:

- [ ] un **registro** con `sha256`, `tipo` y `tamano`;
- [ ] un **resumen jerarquico** (linea de documento + encabezados de seccion);
- [ ] **hechos clave extraidos con trazabilidad** a su documento fuente;
- [ ] una **banda de cobertura** calculada;
- [ ] un **flag epistemico** honesto (`[VERIFIED-FACT]` / `[EPISTEMIC-VOID]`).

El engagement entero esta DONE en ingesta solo cuando **N de N** documentos
cumplen lo anterior (p. ej. 18/18). Cualquier numero menor es INCOMPLETO.

## 6. Checklist de cobertura (declarativo, lo ejecuta el motor)

Esta es la lista de verificaciones que alimenta la base de conocimiento. El
motor determinista la ejecuta y publica su resultado (ver
`knowledge-base/coverage-checklist.md`).

```checklist
- id: inventory-complete
  check: Todos los artefactos de la raiz del corpus estan inventariados (N/N).
- id: per-doc-record
  check: Cada documento tiene sha256 + tipo + tamano.
- id: per-doc-classification
  check: Cada documento tiene rol de prioridad (primary/secondary).
- id: per-doc-method
  check: Cada documento registra su metodo de ingesta.
- id: per-doc-summary
  check: Cada documento tiene un resumen jerarquico.
- id: per-doc-keyfacts
  check: Cada documento tiene hechos clave trazables (o se declara EPISTEMIC-VOID honesto).
- id: per-doc-coverage-band
  check: Cada documento tiene una banda de cobertura calculada.
- id: per-doc-epistemic-flag
  check: Cada documento tiene un flag epistemico honesto.
- id: no-sampling
  check: Ningun documento fue omitido; cobertura total sin muestreo (N de N).
- id: no-fabrication
  check: Los vacios se marcan EPISTEMIC-VOID; no se fabrica contenido.
```

## 7. Implementacion de referencia

El motor stdlib en `advisory-system/engine/knowledge.py` implementa esta
politica: enriquece los 18 documentos del corpus, calcula cobertura/flag,
extrae hechos clave trazables y publica `knowledge-base/` con el checklist.
Determinista, sin red ni LLM. Recalibrable via las perillas de politica
(`COVERAGE_BANDS`, `MIN_CLEAN_CHARS_FOR_VERIFIED`, ...).

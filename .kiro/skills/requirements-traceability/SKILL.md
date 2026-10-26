---
name: requirements-traceability
description: Usar cuando un engagement debe demostrar que CADA solicitud del cliente fue entendida y respondida; define como derivar DINAMICAMENTE las solicitudes del corpus (numerales, vinetas y secciones de requisitos/alcance/informes/objetivos/evaluacion), como citarlas a su documento fuente y como producir un anexo de trazabilidad con DOS artefactos: un checklist marcable de que desarrollar y una tabla punto a punto con estado Cubierto/Parcial/Pendiente.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los engagements, cualquier cliente, cualquier corpus con solicitudes/requisitos
---

# Politica: Trazabilidad de requisitos del cliente (requirements-traceability)

Politica **permanente y reutilizable** de la organizacion. No es especifica de
ningun cliente. Credi10 2.0 se cita solo como *ejemplo de aplicacion*, nunca
como el sujeto de la politica.

## 1. Principio (no negociable)

> **Toda solicitud del cliente presente en el corpus se responde punto a punto,
> con cita al documento fuente.** Ninguna solicitud se omite, y ninguna
> respuesta se fabrica: si el corpus no permite responder una solicitud, se
> marca honestamente como **Pendiente** con la etiqueta epistemica
> correspondiente (`[EPISTEMIC-VOID]` / OCR pendiente), no se inventa cobertura.

Esta politica es complementaria de `complete-corpus-ingestion` (ingerir TODO el
corpus) y de `ocr-image-extraction` (recuperar texto de forma honesta): aqui se
usa el corpus ya ingerido para **demostrar cobertura de las solicitudes**.

## 2. Derivacion DINAMICA de las solicitudes (no hardcodeo)

Las solicitudes NO se escriben a mano para un cliente concreto: se **extraen del
corpus** con heuristicas deterministas sobre la capa de texto limpia. Si cambia
el corpus, el anexo se regenera con las solicitudes de ese nuevo cliente.

1. **Priorizacion de fuentes.** Se prioriza el documento con rol `primary` cuyo
   nombre o contenido lo identifica como la solicitud de oferta (p. ej. un RFP);
   se complementa con el resto del corpus. La priorizacion es por **heuristica
   de rol/nombre**, nunca una lista fija de documentos de un cliente.
2. **Anclas de seccion portadoras de requisitos.** Se detectan encabezados y
   numerales cuyo texto (normalizado, insensible a acentos y a la fragmentacion
   del PDF) corresponde a secciones que tipicamente contienen solicitudes:
   `objetivos` (general / especificos), `alcance`, `requisitos`/`requerimientos`
   (funcionales / de la operacion / tecnicos / de arquitectura objetivo),
   `informes requeridos` / `entregables`, `evaluacion` (tecnologica / de bases
   de datos / de integraciones), `indicadores de retorno` y
   `criterios de evaluacion`.
3. **Items dentro de cada seccion.** Dentro de cada ancla se detectan items por
   numerales (`1.`, `1.1`, `2.3`), vinetas y enumeraciones, acotando el texto a
   una longitud fija para una cita fiel y legible.
4. **Robustez a PDF fragmentado.** La capa de texto de PDFs escaneados aparece
   defragmentada (p. ej. `E va lu ac ión`); la deteccion trabaja sobre una
   version **sin espacios y sin acentos** del texto para localizar las anclas, y
   luego recupera la ventana original correspondiente.
5. **Semillas curadas (opcionales).** Se permite un conjunto de **anclas
   semilla** (nombres de secciones estandar de RFP) SOLO para robustez; si el
   corpus es de otro cliente sin esas secciones, la extraccion **degrada a la
   deteccion generica** de numerales/vinetas. Las semillas nunca introducen
   solicitudes que no esten en el texto del corpus.

## 3. Identificadores y cita a la fuente

- Cada solicitud recibe un **ID estable** `REQ-NNN` asignado en **orden de
  documento** (orden de aparicion), de modo que dos corridas producen los
  mismos IDs (determinismo).
- La **cita al documento fuente** es, como minimo, el `filename` del documento;
  cuando es recuperable, se agrega la **seccion/numeral** del que proviene la
  solicitud.

## 4. Mapeo "donde se responde" (punto a punto)

Cada solicitud se mapea de forma determinista a **donde la responde el advisory**
(fase / seccion / entregable), mediante una tabla declarativa
`palabra-clave -> punto de entrada`. Ejemplos de mapeo (recalibrables):

| Tipo de solicitud | Donde se responde (entregable del advisory) |
| --- | --- |
| objetivos / vision | Fase 1 contexto + Fase 6 caso de negocio |
| alcance / assessment | Fase 0 higiene + Fase 1 AS-IS |
| arquitectura objetivo / TO-BE | Fase 4 diseno TO-BE (C4, ADRs, contratos) |
| integraciones | Fase 1 ecosistema + Fase 4 contratos |
| bases de datos / tecnologia | Fase 1 deuda tecnica + Fase 2 estado del arte |
| informes requeridos / entregables | los 3 informes + dossier TO-BE |
| indicadores de retorno / ROI | Fase 6 value-driver-tree / modelo financiero |
| roadmap / estimacion / riesgos | Fase 5 roadmap, estimacion y RAID |

## 5. Estado de cobertura (honesto)

Cada solicitud recibe un **Estado**:

- **Cubierto**: existe un punto de entrada claro del advisory Y el documento
  fuente aporto texto util (banda de cobertura por texto util real > nula).
- **Parcial**: la solicitud es parcialmente abordable (punto de entrada existe
  pero la evidencia es limitada), o depende de deltas aun por cerrar.
- **Pendiente**: el corpus NO permite responder (el documento fuente no tiene
  texto util real / OCR pendiente). Se marca `[EPISTEMIC-VOID]` y una nota
  honesta; no se fabrica cobertura.

La decision usa las senales de texto util / flag epistemico de
`complete-corpus-ingestion` y `ocr-image-extraction` (campos `useful_ratio`,
`coverage_band`, `epistemic_flag`, `ingestion_method` del documento).

## 6. Artefactos obligatorios (AMBOS)

El anexo de trazabilidad contiene SIEMPRE los dos artefactos:

1. **Checklist marcable** de "que desarrollar / que pide el cliente":
   - `- [x]` Cubierto
   - `- [~]` Parcial
   - `- [ ]` Pendiente
2. **Tabla de trazabilidad punto a punto** con columnas EXACTAS:

   `ID | Solicitud del cliente | Cita al documento fuente | Donde se responde (fase/seccion/entregable) | Estado | Evidencia/Nota`

Ademas: una introduccion que declara que es **generado de forma determinista** y
**dinamico** (se regenera con el corpus de otro cliente), la nota de etiquetas
epistemicas y, opcionalmente, un resumen Mermaid de cobertura por estado.

## 7. Etiquetas epistemicas

| Etiqueta | Significado |
| --- | --- |
| `[VERIFIED-FACT]` | La solicitud proviene de capa de texto util verificada. |
| `[OCR-EXTRACTED]` | La solicitud proviene de texto recuperado via OCR. |
| `[DOC-ASSUMPTION]` | Supuesto razonable sobre la solicitud, a validar. |
| `[DOC-CONFLICT]` | Tension entre fuentes del corpus. |
| `[EPISTEMIC-VOID]` | El corpus no permite derivar/responder (OCR pendiente). |

## 8. Checklist de aplicacion (declarativo, lo ejecuta el motor)

```checklist
- id: dynamic-extraction
  check: Las solicitudes se extraen del corpus (numerales/secciones), no se hardcodean.
- id: source-priority
  check: Se prioriza el documento primary tipo RFP y se complementa con el resto.
- id: stable-ids
  check: Cada solicitud tiene un ID REQ-NNN estable en orden de documento.
- id: source-citation
  check: Cada solicitud cita su documento fuente (y seccion/numeral si se recupera).
- id: where-answered
  check: Cada solicitud se mapea a una fase/seccion/entregable del advisory.
- id: honest-status
  check: Estado Cubierto/Parcial/Pendiente usando texto util real; Pendiente -> [EPISTEMIC-VOID].
- id: both-artifacts
  check: El anexo incluye checklist marcable Y tabla de trazabilidad con las columnas exactas.
- id: deterministic
  check: Dos corridas producen el mismo anexo byte-identico (sin azar ni timestamps).
- id: corpus-agnostic
  check: Con otro corpus el anexo se regenera con las solicitudes de ese cliente.
```

## 9. Implementacion de referencia

El generador stdlib en `advisory-system/phases/requirements_traceability.py`
implementa esta politica: recibe una `KnowledgeBase` o una lista de `Document`,
prioriza el RFP por heuristica de rol/nombre, extrae solicitudes con las anclas
de seccion y la deteccion de numerales (robusta a la fragmentacion del PDF via
normalizacion sin espacios/acentos), asigna IDs `REQ-NNN` en orden de documento,
mapea cada solicitud a su punto de entrada del advisory y fija el Estado con las
senales de texto util / flag epistemico. Renderiza el anexo bajo
`3-informe-tecnico/anexo-a-trazabilidad-requisitos/` con el checklist marcable y
la tabla de trazabilidad, y se enlaza desde el README maestro del informe
tecnico. Determinista, sin red ni LLM, y recalibrable via sus perillas de
politica (`SECTION_ANCHORS`, `KEYWORD_ENTRY_POINTS`, `MAX_REQUEST_CHARS`).

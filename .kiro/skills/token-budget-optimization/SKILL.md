---
name: token-budget-optimization
description: Usar cuando el corpus o el contexto excede el presupuesto de tokens/ventana; define tecnicas para optimizar el consumo GARANTIZANDO comprension completa, con un safeguard por cada tecnica y la regla de que la priorizacion cambia el orden/esfuerzo, nunca excluye un documento.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los engagements, cualquier cliente, cualquier corpus
---

# Politica: Optimizacion del presupuesto de tokens (token-budget-optimization)

Politica **permanente y reutilizable** de la organizacion. Credi10 2.0 se cita
solo como *ejemplo de aplicacion*.

## 1. Principio (no negociable)

> Optimizar el consumo de tokens/contexto es **obligatorio**, pero **jamas** a
> costa de la comprension. Toda tecnica de ahorro va **emparejada con un
> safeguard** que garantiza que el documento sigue procesado y entendido.
>
> **La priorizacion cambia el ORDEN y el ESFUERZO, nunca EXCLUYE un documento.**

Esta politica trabaja en conjunto con `complete-corpus-ingestion`: primero se
garantiza la cobertura 100% (N de N), luego se optimiza como se consume.

## 2. Estrategias y sus safeguards

| Estrategia | Que hace | Safeguard de comprension |
| --- | --- | --- |
| Resumenes jerarquicos por documento | Reemplaza texto crudo por un resumen multinivel (documento -> secciones). | El resumen se deriva del texto completo; el checklist exige un resumen por CADA documento. |
| Chunking | Parte documentos largos en fragmentos acotados y estables. | Chunking determinista por offset: ningun fragmento se descarta, todos quedan direccionables. |
| Map-reduce para documentos largos | Resume por chunk (map) y consolida (reduce). | El reduce debe cubrir todos los chunks del map; se verifica que no queden chunks sin consolidar. |
| Retrieval selectivo por fase/rol | Cada fase/rol recupera solo los hechos que necesita. | El indice completo permanece disponible; la seleccion es una VISTA, no un recorte del corpus. |
| Deduplicacion | Elimina segmentos/hechos repetidos. | Se deduplica por contenido normalizado; se conserva la trazabilidad a la fuente original. |
| Caching de extraccion | Reutiliza la extraccion ya calculada (idempotente). | La extraccion es determinista; el cache produce exactamente el mismo resultado que recomputar. |
| Priorizacion primary vs secondary | Lee primero y mas a fondo lo primario. | Lo secundario se ingiere igual (resumen + registro + cobertura); PRIORIDAD != exclusion. |

## 3. Reglas de verificacion (safeguards transversales)

1. **Cobertura total primero**: ninguna optimizacion se aplica antes de
   garantizar el inventario N de N de `complete-corpus-ingestion`.
2. **Todo documento conserva**: resumen + indice/registro + trazabilidad. Si
   una optimizacion rompe cualquiera de los tres, se revierte.
3. **Determinismo**: las tecnicas no introducen aleatoriedad; el mismo corpus
   produce el mismo resultado (reproducible, auditable).
4. **Honestidad epistemica**: optimizar no puede convertir un
   `[EPISTEMIC-VOID]` en contenido fabricado.

## 4. Presupuesto parametrico (recalibrable)

Los limites viven como perillas declarativas y recalibrables en el motor
(`MAX_KEY_FACTS_PER_DOC`, `MAX_SUMMARY_CHUNKS`, `MAX_FACT_CHARS`,
`SUMMARY_CHUNK_CHARS` en `advisory-system/engine/knowledge.py`). Ajustar el
presupuesto se hace ahi, sin tocar la logica ni violar los safeguards.

## 5. Implementacion de referencia

`engine/knowledge.py` aplica resumenes jerarquicos acotados, chunking por
offset, deduplicacion de hechos y caching implicito (idempotencia), siempre
registrando CADA documento. El checklist de cobertura es el safeguard que prueba
que la optimizacion no perdio ningun documento.

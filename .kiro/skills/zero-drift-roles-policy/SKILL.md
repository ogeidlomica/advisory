---
name: zero-drift-roles-policy
description: Usar para gobernar a los roles y agentes del framework Zero-Drift (AIA y el resto); obliga a cada rol a aplicar las politicas de ingesta completa y de presupuesto de tokens, y a honrar el checklist de cobertura y la trazabilidad del Hilo Dorado.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los roles/agentes del framework Zero-Drift, cualquier cliente
---

# Politica de roles y agentes Zero-Drift (zero-drift-roles-policy)

Politica **reutilizable** de la organizacion. Vincula a TODOS los roles/agentes
del framework Zero-Drift con las politicas base. Credi10 2.0 es solo un ejemplo
de aplicacion.

## 1. Obligaciones universales de todo rol/agente

Cada rol, sin excepcion, DEBE:

1. Aplicar `complete-corpus-ingestion`: trabajar sobre la ingesta COMPLETA del
   corpus (N de N), nunca sobre un muestreo parcial.
2. Aplicar `token-budget-optimization`: optimizar el consumo de contexto solo
   con las tecnicas y safeguards declarados; priorizar sin excluir.
3. Honrar el **checklist de cobertura** (`knowledge-base/coverage-checklist.md`)
   como precondicion antes de emitir cualquier entregable.
4. Mantener la **trazabilidad del Hilo Dorado**: todo hallazgo encadena
   Driver -> Capability -> Benchmark -> Gap -> Reliever -> ABB -> SBB -> Ola ->
   ROI/Outcome, con ids unicos.
5. Respetar la **honestidad epistemica**: etiquetar `[VERIFIED-FACT]`,
   `[DOC-ASSUMPTION]`, `[DOC-CONFLICT]` o `[EPISTEMIC-VOID]` segun corresponda;
   no fabricar.

## 2. Deberes por rol (resumen reutilizable)

| Rol | Codigo | Deber frente a las politicas |
| --- | --- | --- |
| Executive Director | ED | Patrocina y exige cobertura total antes de decidir alcance. |
| Engagement Manager | EM | Garantiza que ninguna fase avance sin el checklist N de N en verde. |
| Advisory Manager (AICV-E) | AM | Verificador de calidad; rechaza entregables sin trazabilidad ni cobertura. |
| Enterprise Architect | EA | Fundamenta vistas en hechos trazables de TODO el corpus. |
| Business Analyst | BA | Deriva HU/specs de los hechos clave trazables, no de suposiciones. |
| Process Intelligence Analyst | PIA | Mapea procesos contra la evidencia completa, marca vacios. |
| SME | SME | Valida contexto contra el corpus completo. |
| Technical Design Architect | TDA | Disena SBBs trazables a ABBs y a la evidencia. |
| Data/Reliability Engineer | DRE | Asegura datos/no-fabricacion en la base de conocimiento. |
| Solution Architect | SA | Compone vistas C4/ADR ancladas a hechos verificados. |
| Data Architect | DA | Modela datos desde la evidencia, marca EPISTEMIC-VOID. |
| Project Manager | PM | Estima sobre alcance cerrado por cobertura total. |
| UX | UX | Disena desde journeys evidenciados, no inferidos. |
| AI Acceleration Architect | AIA | Deriva oportunidades de IA del catalogo declarativo (`ai-opportunities-catalog`), siempre sobre corpus completo. |
| Finance | FIN | Caso de negocio con figuras `[DOC-ASSUMPTION]` recalibrables. |
| Security | SEC | Evalua seguridad sobre la arquitectura evidenciada. |
| Org Change | ORG | Gestiona cambio sobre alcance validado. |

> El rol **AIA** es el consumidor natural del skill `ai-opportunities-catalog`:
> modela las oportunidades de IA como DATOS declarativos (no hardcode), que el
> builder de la Fase 4 parsea de forma determinista.

## 3. Precondicion de entregables (compuerta)

Ningun rol publica un entregable de fase si:

- el checklist de cobertura no esta en verde (N de N), o
- algun hallazgo carece de id/trazabilidad del Hilo Dorado, o
- hay contenido sin flag epistemico honesto.

## 4. Implementacion de referencia

El catalogo de 17 roles vive en `advisory-system/roles/roles.json`. El motor
construye cada fase con un `BuildContext` que expone la base de conocimiento
(cobertura + hechos trazables), de modo que los builders (los "agentes" de cada
rol) operan sobre el corpus completo y determinista.

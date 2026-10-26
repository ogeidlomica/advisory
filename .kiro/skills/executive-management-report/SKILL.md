---
name: executive-management-report
description: Usar al generar el REPORTE GERENCIAL ejecutivo que da soporte a la propuesta comercial; obliga a producir un documento ejecutivo/comercial con alcance del proyecto, fases, diagnostico de alto nivel del proceso realizado, estrategia, riesgos, consideraciones y prerrequisitos, en tono narrativo, con diagramas Mermaid de alto nivel y tablas resumen, coherente con y referenciando el informe tecnico, generado de forma determinista desde el analisis del corpus.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los engagements, cualquier cliente, soporte ejecutivo/comercial de la propuesta
---

# Politica: Reporte Gerencial ejecutivo (executive-management-report)

Politica **permanente y reutilizable** de la organizacion. No es especifica de
ningun cliente. Credi10 2.0 se cita solo como *ejemplo de aplicacion*, nunca
como el sujeto de la politica.

## 1. Principio (no negociable)

> El **reporte gerencial** es el **soporte ejecutivo/comercial** de la propuesta:
> describe comercialmente el **alcance del proyecto**, sus **fases** y un
> **diagnostico de alto nivel** del proceso de advisory ya realizado, y habilita
> la decision de la gerencia. Su contenido se **deriva deterministamente** del
> analisis del corpus y del trabajo por fases; nunca se fabrica evidencia.

El reporte gerencial es un **informe hermano** de la propuesta comercial y del
informe tecnico narrativo: se publica por separado y se enlaza desde el indice
maestro. Es un **resumen ejecutivo** del diagnostico, no un sustituto del
informe tecnico: debe **exigir coherencia con** y **referenciar** al informe
tecnico para el detalle.

## 2. Audiencia y tono

- Audiencia: **gerencia/direccion** (negocio), no equipos de implementacion.
- Tono: **narrativo y ejecutivo**; prosa clara que cuente el hilo del
  diagnostico, evitando jerga tecnica profunda (que vive en el informe tecnico).
- Extension: condensado; prioriza sintesis sobre exhaustividad.

## 3. Secciones obligatorias

El reporte DEBE contener, en orden estable:

| # | Clave | Seccion | Contenido minimo |
| --- | --- | --- | --- |
| 1 | `resumen-ejecutivo` | Resumen ejecutivo | Sintesis del engagement y de la recomendacion. |
| 2 | `alcance-proyecto` | Alcance del proyecto | Alcance comercial del proyecto (que entra / que no). |
| 3 | `fases` | Fases | Las fases del advisory (las mismas del framework), con su proposito. |
| 4 | `diagnostico` | Diagnostico de alto nivel | Resumen ejecutivo de hallazgos del proceso realizado (AS-IS, gaps, oportunidades). |
| 5 | `estrategia` | Estrategia | Enfoque de implementacion propuesto y olas/roadmap de alto nivel. |
| 6 | `riesgos` | Riesgos | Riesgos clave del proyecto (resumen del RAID), con impacto/mitigacion. |
| 7 | `consideraciones` | Consideraciones | Consideraciones de negocio, organizacionales y de cambio. |
| 8 | `prerrequisitos` | Prerrequisitos | Condiciones previas para iniciar/ejecutar con exito. |

## 4. Contrato de contenido

El reporte, como documento completo, DEBE incluir:

- [ ] al menos **un diagrama Mermaid de alto nivel** (fases, olas o contexto);
- [ ] al menos **una tabla resumen** (p. ej. riesgos, fases o diagnostico);
- [ ] al menos **una etiqueta epistemica** honesta
  (`[VERIFIED-FACT]` / `[DOC-ASSUMPTION]` / `[DOC-CONFLICT]` /
  `[EPISTEMIC-VOID]`);
- [ ] una **referencia explicita al informe tecnico** como fuente de detalle;
- [ ] trazabilidad al corpus y a los artefactos del Hilo Dorado (no se duplican
  datos: se reutilizan y se citan).

## 5. Coherencia con el informe tecnico (regla dura)

El reporte gerencial **no puede contradecir** al informe tecnico ni a la
propuesta comercial. Alcance, fases, riesgos y estrategia deben derivarse de las
**mismas fuentes de verdad** (Base de Conocimiento, roadmap/RAID, gaps). Si un
dato aparece en varios informes, debe ser **congruente** (mismo valor, misma
etiqueta epistemica).

## 6. Determinismo (hard requirement)

El reporte lo **genera el motor** del advisory, no se escribe a mano:

- orden estable de secciones, sin aleatoriedad y sin timestamps;
- regeneracion idempotente: una segunda corrida deja el control de versiones
  limpio (sin drift);
- contenido estatico ordenado derivado de la Base de Conocimiento.

## 7. Definicion de DONE

El reporte esta DONE solo si:

- [ ] existen las ocho secciones (resumen, alcance, fases, diagnostico,
  estrategia, riesgos, consideraciones, prerrequisitos);
- [ ] se cumple el contrato de contenido (diagrama + tabla resumen + etiqueta
  epistemica + referencia al informe tecnico);
- [ ] el reporte es coherente con la propuesta y con el informe tecnico;
- [ ] esta enlazado desde el indice maestro del engagement;
- [ ] la regeneracion es determinista (segunda corrida sin cambios).

## 8. Implementacion de referencia

El motor stdlib (en `advisory-system/phases/`) implementa esta politica como un
builder determinista que reutiliza la Base de Conocimiento, el roadmap/RAID
(Fase 5) y los gaps (Fase 3). Los roles productores naturales son el **Comite de
Gobierno** (Engagement Director y Engagement Manager). Para Credi10 2.0 el
reporte gerencial se publica bajo `advisory-credi10-2.0/`.

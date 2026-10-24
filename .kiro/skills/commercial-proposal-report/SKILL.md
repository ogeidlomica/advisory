---
name: commercial-proposal-report
description: Usar al generar la PROPUESTA COMERCIAL de un engagement de advisory; obliga a producir un documento de venta emitido por la consultora (marca configurable, por defecto Kulgops) con 11 secciones obligatorias a-k (quienes somos, alcance del servicio, contexto de negocio con diagrama, metodologia, entregables, estrategia de consultoria, equipo, cronograma, supuestos y restricciones, inversion y terminos), generado de forma determinista desde el analisis del corpus, con perfil corporativo e inversion marcados [DOC-ASSUMPTION].
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los engagements, cualquier cliente, fase de propuesta/venta consultiva
---

# Politica: Propuesta Comercial del engagement (commercial-proposal-report)

Politica **permanente y reutilizable** de la organizacion. No es especifica de
ningun cliente ni de ninguna consultora concreta: la **marca emisora** es un
parametro configurable (por defecto `Kulgops`). Credi10 2.0 se cita solo como
*ejemplo de aplicacion*, nunca como el sujeto de la politica.

## 1. Principio (no negociable)

> La **propuesta comercial** es el documento de **venta** del servicio de
> consultoria: lo emite la **consultora** hacia el prospecto/cliente y describe
> el valor, el alcance, el equipo, el cronograma y la inversion del engagement.
> Su contenido se **deriva deterministamente** del analisis del corpus (contexto
> de negocio) y de las politicas de la organizacion (metodologia, framework,
> entregables); nunca se fabrica evidencia ni se presentan datos corporativos
> como verificados cuando son de referencia.

La propuesta es un **informe hermano** del reporte gerencial ejecutivo y del
informe tecnico narrativo: los tres se publican por separado y se enlazan desde
el indice maestro del engagement. La propuesta **no** reemplaza al informe
tecnico; lo **referencia** como soporte del alcance ofertado.

## 2. Marca emisora (parametro configurable)

- La consultora emisora es **configurable**; valor por defecto: `Kulgops`.
- El **perfil corporativo** de la consultora (historia, tamano, clientes,
  certificaciones, etc.) se construye de forma **generica y plausible** y se
  marca `[DOC-ASSUMPTION]`. Esta **prohibido** presentar datos reales de una
  empresa como `[VERIFIED-FACT]` sin fuente en el corpus.
- La propuesta debe ser **reutilizable**: cambiar la marca emisora o el cliente
  no debe requerir reescribir la politica, solo recalibrar parametros.

## 3. Secciones obligatorias (a-k)

La propuesta DEBE contener, en orden estable, las **11 secciones**:

| # | Clave | Seccion | Contenido minimo |
| --- | --- | --- | --- |
| a | `quienes-somos` | Quienes somos | Introduccion breve de la consultora emisora; propuesta de valor. Perfil marcado `[DOC-ASSUMPTION]`. |
| b | `alcance-servicio` | Alcance del servicio | Descripcion del servicio de consultoria y especificacion de requisitos para desarrollo de software. |
| c | `contexto-negocio` | Contexto de negocio | Resumen del contexto procesado desde los documentos del corpus; incluye **diagrama de contexto de alto nivel** (bloque ```mermaid```). |
| d | `metodologia` | Metodologia de consultoria | Como trabajamos: fases, gates y gobierno. |
| e | `entregables` | Entregables | Los outputs que el engagement produce (los 3 informes + dossier + base de conocimiento). |
| f | `estrategia-consultoria` | Estrategia de consultoria | Nuestro **framework** (Zero-Drift): principios, Hilo Dorado, honestidad epistemica. |
| g | `equipo-trabajo` | Equipo de trabajo | Comite de Gobierno + celulas; roles clave del `roles.json`. |
| h | `cronograma` | Cronograma de trabajo | Plan por fases; **diagrama Gantt** (bloque ```mermaid gantt```). |
| i | `supuestos-restricciones` | Supuestos y restricciones | Supuestos y limites del engagement; etiquetas epistemicas. |
| j | `inversion` | Inversion | **Rangos de referencia** recalibrables, marcados `[DOC-ASSUMPTION]`; nunca compromisos. |
| k | `terminos-condiciones` | Terminos y condiciones | Validez de la oferta, propiedad intelectual, confidencialidad, exclusiones. |

## 4. Contrato de contenido

La propuesta, como documento completo, DEBE incluir:

- [ ] al menos **un diagrama de contexto** de alto nivel (```mermaid```) en la
  seccion de contexto de negocio;
- [ ] al menos **un cronograma Gantt** (```mermaid gantt```) en la seccion de
  cronograma;
- [ ] al menos **una tabla** que estructure informacion (p. ej. entregables,
  equipo o inversion);
- [ ] al menos **una etiqueta epistemica** honesta
  (`[VERIFIED-FACT]` / `[DOC-ASSUMPTION]` / `[DOC-CONFLICT]` /
  `[EPISTEMIC-VOID]`), con el **perfil corporativo** y la **inversion**
  marcados `[DOC-ASSUMPTION]`;
- [ ] trazabilidad al corpus para el contexto de negocio (no se inventan datos
  del cliente).

## 5. Inversion (regla dura)

Las cifras de inversion **siempre** se expresan como **rangos de referencia**
`[DOC-ASSUMPTION]` recalibrables y **nunca** como precios firmes o compromisos.
Deben poder ajustarse cambiando parametros del builder, sin reescribir prosa.

## 6. Determinismo (hard requirement)

La propuesta la **genera el motor** del advisory, no se escribe a mano:

- orden estable de secciones a-k, sin aleatoriedad y sin timestamps;
- regeneracion idempotente: una segunda corrida deja el control de versiones
  limpio (sin drift);
- contenido estatico ordenado; marca emisora e inversion desde parametros.

## 7. Definicion de DONE

La propuesta esta DONE solo si:

- [ ] existen las **11 secciones** a-k en orden;
- [ ] se cumple el contrato de contenido (diagrama de contexto + Gantt + tabla +
  etiqueta epistemica);
- [ ] el perfil corporativo y la inversion estan marcados `[DOC-ASSUMPTION]`;
- [ ] la propuesta esta enlazada desde el indice maestro del engagement y
  referencia el informe tecnico como soporte del alcance;
- [ ] la regeneracion es determinista (segunda corrida sin cambios).

## 8. Implementacion de referencia

El motor stdlib (en `advisory-system/phases/`) implementa esta politica como un
builder determinista que reutiliza la Base de Conocimiento (contexto de
negocio), `roles.json` (equipo) y los parametros de marca/inversion. Los roles
productores naturales son el **Comite de Gobierno** (Engagement Director y
Engagement Manager). Para Credi10 2.0 la propuesta se publica bajo
`advisory-credi10-2.0/`.

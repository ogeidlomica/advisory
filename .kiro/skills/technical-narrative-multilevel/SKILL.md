---
name: technical-narrative-multilevel
description: Usar al construir el INFORME TECNICO del engagement; obliga a una estructura desagregada multinivel (>=3 niveles fase->tema->subtema, una subcarpeta por fase, varios archivos por tema), jerarquia interna H1-H2-H3, un README indice con hilo narrativo/storytelling, y la regla de calidad clave de NARRATIVA/ANALISIS sustancial en prosa (no solo tablas y Mermaid) que interprete hallazgos y explique implicaciones para la estimacion, la estrategia de implementacion y los riesgos, aplicando mejores practicas actuales del SDLC, generado de forma determinista desde el analisis del corpus.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los engagements, cualquier cliente, informe tecnico del advisory
---

# Politica: Informe Tecnico narrativo multinivel (technical-narrative-multilevel)

Politica **permanente y reutilizable** de la organizacion. No es especifica de
ningun cliente. Credi10 2.0 se cita solo como *ejemplo de aplicacion*, nunca
como el sujeto de la politica.

## 1. Principio (no negociable)

> El **informe tecnico** es el entregable de advisory que sostiene una
> **estimacion lo mas acertada posible**. Debe presentarse como una estructura
> **desagregada y multinivel** facil de leer, con **hilo narrativo/storytelling**
> y **analisis sustancial en prosa** que interprete los hallazgos y explique sus
> implicaciones para la **estimacion**, la **estrategia de implementacion** y los
> **riesgos**. Su contenido se **deriva deterministamente** del analisis del
> corpus; nunca se fabrica evidencia.

El informe tecnico es el **informe hermano** detallado de la propuesta comercial
y del reporte gerencial: es la **fuente de verdad del detalle** que ambos
referencian. El **dossier TO-BE** (politica `sdlc-project-dossier`) se **integra
dentro** del informe tecnico como su vista orientada a ejecucion.

## 2. Estructura multinivel (obligatoria, >=3 niveles)

- **Nivel 1 = Fase.** Una **subcarpeta por fase** del framework (las mismas
  fases nombradas por el engagement: higiene epistemica, contexto AS-IS, estado
  del arte, gaps y viabilizacion, diseno TO-BE, roadmap/estimacion/RAID, caso de
  negocio). Numeracion estable para orden determinista.
- **Nivel 2 = Tema.** Dentro de cada fase, **varios archivos**, uno por tema
  (no un unico archivo monolitico por fase).
- **Nivel 3 = Subtema.** Dentro de cada archivo, **secciones de subtema** con
  jerarquia interna.

La **jerarquia interna** de cada archivo usa `H1 -> H2 -> H3` (un solo `H1` por
archivo = el tema; `H2` por subtema; `H3` para detalle).

## 3. README indice con hilo narrativo (obligatorio)

El informe tecnico DEBE tener un `README.md` indice que:

- presente el **hilo narrativo/storytelling** que conecta las fases (de donde
  partimos, que encontramos, a donde vamos y por que);
- enlace cada fase y cada tema (navegacion multinivel);
- explique como leer el informe y como se integra el dossier TO-BE.

## 4. Regla de calidad clave: NARRATIVA sustancial (regla dura)

> Cada seccion/archivo debe contener **narrativa/analisis sustancial en prosa**,
> **ademas** de las tablas y los diagramas Mermaid. Esta **prohibido** entregar
> secciones que sean solo tablas y graficos sin interpretacion.

Cada tema/archivo debe, como minimo:

- **interpretar** los hallazgos (que significan, no solo cuales son);
- explicar sus **implicaciones para la estimacion** (que lo hace mas facil o mas
  dificil de estimar, que impulsa el esfuerzo);
- conectar con la **estrategia de implementacion** (secuencia, dependencias,
  olas) y con los **riesgos** (que puede salir mal y como se mitiga);
- mantener el **hilo narrativo** con la fase anterior y la siguiente.

## 5. Mejores practicas del SDLC (aplicar)

El informe tecnico aplica las practicas actuales del ciclo de vida de desarrollo
de software, trazables al detalle que corresponda:

- **Requisitos** (funcionales + NFR, p. ej. ISO/IEC 25010) y reglas de negocio;
- **Arquitectura** con vistas **C4** y **ADRs** (decisiones y su justificacion);
- **Specs/contratos** (APIs, eventos, esquemas de datos);
- **UX** (customer journeys, service blueprints, wireflows);
- **Pruebas** (estrategia, matriz de cobertura, criterios de aceptacion);
- **DevOps/CI-CD** (entrega continua, calidad, observabilidad);
- **Estimacion** (descomposicion por modulo, tabla parametrica recalibrable);
- **Roadmap** (olas, dependencias, RAID).

## 6. Contrato de contenido por archivo

Cada archivo de tema DEBE incluir:

- [ ] **narrativa/analisis en prosa** (regla dura de la seccion 4);
- [ ] al menos **un diagrama** cuando aporte (```mermaid```);
- [ ] al menos **una tabla** cuando estructure datos;
- [ ] al menos **una etiqueta epistemica** honesta
  (`[VERIFIED-FACT]` / `[DOC-ASSUMPTION]` / `[DOC-CONFLICT]` /
  `[EPISTEMIC-VOID]`);
- [ ] **trazabilidad** al corpus y al Hilo Dorado (Driver -> Capability ->
  Benchmark -> Gap -> Reliever -> ABB -> SBB -> Ola -> ROI/Outcome).

## 7. Determinismo (hard requirement)

El informe tecnico lo **genera el motor** del advisory, no se escribe a mano:

- orden estable de fases/temas/subtemas, sin aleatoriedad y sin timestamps;
- creacion de subcarpetas con `exist_ok` y escritura de contenido estatico
  ordenado;
- regeneracion idempotente: una segunda corrida deja el control de versiones
  limpio (sin drift).

## 8. Definicion de DONE

El informe tecnico esta DONE solo si:

- [ ] existe una **subcarpeta por fase** (nivel 1) con **varios archivos de
  tema** (nivel 2) y **subtemas** internos (nivel 3);
- [ ] cada archivo usa jerarquia `H1 -> H2 -> H3` y cumple el contrato de
  contenido, con **narrativa sustancial** (no solo tablas/Mermaid);
- [ ] existe un `README.md` indice con hilo narrativo/storytelling que enlaza la
  estructura multinivel;
- [ ] el dossier TO-BE queda integrado dentro del informe tecnico;
- [ ] la propuesta y el reporte gerencial referencian este informe como detalle;
- [ ] la regeneracion es determinista (segunda corrida sin cambios).

## 9. Implementacion de referencia

El motor stdlib (en `advisory-system/phases/`) implementa esta politica
reescribiendo la presentacion del informe tecnico a la estructura multinivel y
reutilizando los builders por fase, el catalogo de modulos/historias
(`phases/modules.py`), el dossier (`phases/dossier.py`) y la Base de
Conocimiento. Las celulas (Discovery, Diseno, Valor y Habilitacion) son los
roles productores naturales del informe tecnico, con AM como verificador de
calidad. Para Credi10 2.0 el informe tecnico se publica bajo
`advisory-credi10-2.0/`.

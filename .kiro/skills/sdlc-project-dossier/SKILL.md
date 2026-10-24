---
name: sdlc-project-dossier
description: Usar al construir el entregable TO-BE de un engagement de advisory; obliga a producir un dossier de proyecto organizado con una subcarpeta por etapa/practica del SDLC (requisitos, arquitectura, specs, UX, pruebas, insumos de estimacion) mas registros transversales (ambiguedades, riesgos, consideraciones, restricciones, prerrequisitos) en TODOS los niveles arquitectonicos, generado de forma determinista desde el analisis del corpus.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los engagements, cualquier cliente, fase de diseno TO-BE
---

# Politica: Dossier de proyecto TO-BE por etapa del SDLC (sdlc-project-dossier)

Politica **permanente y reutilizable** de la organizacion. No es especifica de
ningun cliente. Credi10 2.0 se cita solo como *ejemplo de aplicacion*, nunca
como el sujeto de la politica.

## 1. Principio (no negociable)

> El entregable TO-BE de un proyecto se materializa como un **dossier** con
> **una subcarpeta por etapa/practica del SDLC** y un conjunto de **registros
> transversales** del proyecto que cubren **todos los niveles arquitectonicos**.
> Todo el contenido se **deriva deterministamente** del analisis del corpus;
> nunca se fabrica evidencia para rellenar vacios.

El dossier no reemplaza los informes por fase: los **consolida** en una vista
orientada a ejecutar el proyecto, enlazando al detalle por fase.

## 2. Estructura por etapa del SDLC (obligatoria)

Una subcarpeta por etapa, con numeracion estable para orden determinista:

- `01-requisitos/`         requisitos funcionales + NFR (p. ej. ISO/IEC 25010)
  + reglas de negocio + trazabilidad.
- `02-arquitectura/`       vistas TO-BE por nivel (negocio, aplicacion,
  datos, integracion, infraestructura, seguridad).
- `03-specs/`              contratos de API/eventos, esquemas de datos y specs
  por componente/modulo.
- `04-ux/`                 service blueprints, customer journeys, wireflows / IA.
- `05-pruebas/`            estrategia, matriz de cobertura, casos derivados de
  las historias, plan de Dry-Run/Tabletop y criterios de aceptacion.
- `06-insumos-estimacion/` descomposicion por modulo, tabla parametrica
  recalibrable, supuestos y dependencias.

## 3. Registros transversales (todos los niveles arquitectonicos)

En `00-registros/`, cinco registros, cada entrada con **ID**, **nivel
arquitectonico**, **severidad/impacto**, **estado** y **etiqueta epistemica**
donde aplique:

- `ambiguedades.md`     (prefijo `AMB-`)
- `riesgos.md`          (prefijo `RSK-`)
- `consideraciones.md`  (prefijo `CON-`)
- `restricciones.md`    (prefijo `RST-`)
- `prerrequisitos.md`   (prefijo `PRE-`)

Niveles arquitectonicos de referencia: `negocio`, `aplicacion`, `datos`,
`integracion`, `infraestructura`, `seguridad`.

## 4. Contrato de contenido por capitulo

Cada capitulo del dossier debe contener, como minimo:

- [ ] al menos un **diagrama** (p. ej. bloque ```mermaid```);
- [ ] al menos una **tabla** que estructure la informacion;
- [ ] al menos una **etiqueta epistemica** honesta
  (`[VERIFIED-FACT]` / `[DOC-ASSUMPTION]` / `[DOC-CONFLICT]` /
  `[EPISTEMIC-VOID]`);
- [ ] **trazabilidad** a las fuentes del corpus y a los artefactos del Hilo
  Dorado existentes (no se duplican datos: se reutilizan y se citan).

Las cifras de esfuerzo/estimacion **siempre** se marcan `[DOC-ASSUMPTION]` y
viven en una **tabla parametrica recalibrable**; no son compromisos.

## 5. Reutilizar la fuente unica de verdad (no duplicar)

El dossier debe **reutilizar** las fuentes de verdad ya definidas (catalogo de
modulos/historias, building blocks de solucion, gaps, indicadores del cliente)
y **enlazar** los informes por fase para el detalle. Esta prohibido re-inventar
o contradecir esos datos.

## 6. Determinismo (hard requirement)

El dossier lo **genera el motor** del advisory, no se escribe a mano:

- orden estable, sin aleatoriedad y sin timestamps;
- regeneracion idempotente: una segunda corrida deja el control de versiones
  limpio (sin drift);
- creacion de carpetas con `exist_ok` y escritura de contenido estatico
  ordenado.

## 7. Definicion de DONE

El dossier esta DONE solo si:

- [ ] existen las seis subcarpetas de etapa del SDLC + `00-registros/` + un
  `README.md` indice;
- [ ] cada capitulo cumple el contrato de contenido (diagrama + tabla +
  etiqueta epistemica);
- [ ] cada registro transversal tiene entradas con ID + nivel + severidad +
  estado (+ etiqueta donde aplique) y cubre los niveles relevantes;
- [ ] el dossier esta enlazado desde el indice del engagement;
- [ ] la regeneracion es determinista (segunda corrida sin cambios).

## 8. Implementacion de referencia

El motor stdlib en `advisory-system/phases/dossier.py` implementa esta politica:
reutiliza `phases/modules.py`, `phases/phase4.py` (SBBs) y `phases/phase3.py`
(gaps/relievers/ABBs) y la Base de Conocimiento, y escribe el arbol
`to-be/` de forma determinista durante `--phase all`. Para Credi10 2.0 el
dossier se publica bajo `advisory-credi10-2.0/to-be/`.

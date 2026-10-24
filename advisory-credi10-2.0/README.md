# Advisory Credi10 2.0 - Framework Zero-Drift

Este directorio contiene los **informes del advisory Credi10 2.0**, generados automaticamente por el motor `advisory-system/` a partir del corpus de evidencia (RFP, assessment WSO2/Studio F y diagramas de arquitectura). Cada informe corresponde a una fase del framework **Zero-Drift** y es 100% reproducible re-ejecutando el quickstart.

> **Regenerar todos los informes:**
>
> ```bash
> python3 advisory-system/quickstart.py --phase all
> ```

## El framework Zero-Drift

Zero-Drift organiza el advisory como un **Comite de Gobierno** mas **3 Celulas** de trabajo, con **17 roles** declarativos, **7 fases** con stage-gates **QG-0..QG-6**, separacion productor/verificador (**RACI-V**), gobierno de calidad **AICV-E** (a cargo del AM) y un **Hilo Dorado** de trazabilidad que conecta cada driver del RFP con un outcome de negocio.

- **Comite de Gobierno:** ED (Engagement Director), EM (Engagement Manager), AM (Advisory Manager).
- **Celula 1 - Discovery:** EA, BA, PIA, SME, TDA, DRE.
- **Celula 2 - Diseno:** SA, DA, PM, UX, AIA.
- **Celula 3 - Valor y Habilitacion:** FIN, SEC, ORG.
- **Roles totales:** 17 (catalogo declarativo en `advisory-system/roles/roles.json`).

## Corpus de evidencia

- Documentos PDF analizados: **15**
- Diagramas PNG (evidencia binaria transcrita): **3**
- Total ingerido (cobertura COMPLETA, sin muestreo): **18** documentos.

## Base de Conocimiento y capa de politicas (skills)

La ingesta del corpus es **completa y verificable** (nada de muestreo parcial) y esta gobernada por una **capa declarativa de politicas reutilizables** (skills), pensada como politica de la organizacion y aplicable a otros corpus/clientes:

- **Base de Conocimiento generada** en [`../knowledge-base/`](../knowledge-base/): indice por documento (sha256, tipo, rol primario/secundario, tamanio), resumenes jerarquicos, extraccion de hechos clave con trazabilidad a su documento fuente y una [`coverage-checklist.md`](../knowledge-base/coverage-checklist.md) que marca honestamente los documentos de baja cobertura / [EPISTEMIC-VOID] (sin fabricar evidencia). La consume el advisory para trazar cada decision a su fuente.
- **Capa de skills declarativos** en `.kiro/skills/` (politicas versionadas, agnosticas del cliente): `complete-corpus-ingestion` (ingesta y validacion COMPLETA del corpus), `token-budget-optimization` (optimizar tokens GARANTIZANDO procesamiento y entendimiento completos), `zero-drift-roles-policy` (politica permanente de tomar y validar TODO el contexto documental) y `ai-opportunities-catalog` (oportunidades de IA modeladas como skills, no hardcodeadas). El motor las carga via `advisory-system/engine/skills.py`.

## Informes por fase

| Fase | Informe | Entregables | Lider(es) | Verificador | Gate |
| --- | --- | --- | --- | --- | --- |
| Fase 0 - Higiene Epistemica | [00-higiene-epistemica.md](00-higiene-epistemica.md) | E0.1, E0.2, E0.3 | AM, TDA, DRE | EM | QG-0 |
| Fase 1 - Contexto AS-IS | [01-contexto-as-is.md](01-contexto-as-is.md) | E1.1, E1.2, E1.3 | EA, BA, PIA, TDA | AM | QG-1 |
| Fase 2 - Estado del Arte | [02-estado-del-arte.md](02-estado-del-arte.md) | E2.1, E2.2 | EA, SME, BA | AM | QG-2 |
| Fase 3 + 3.5 - Gaps y Viabilizacion | [03-gaps-y-viabilizacion.md](03-gaps-y-viabilizacion.md) | E3.1, E3.2, E3.5 | EA, DRE, PIA | AM | QG-3 |
| Fase 4 - Diseno TO-BE | [04-diseno-to-be.md](04-diseno-to-be.md) | E4.1, E4.2, E4.3 | SA, DA, PM, UX | AM | QG-4 |
| Fase 5 - Roadmap, Estimacion y RAID | [05-roadmap-estimacion-raid.md](05-roadmap-estimacion-raid.md) | E5.1, E5.2, E5.3 | EM, SA, PM, ORG | AM | QG-5 |
| Fase 6 - Caso de Negocio | [06-caso-de-negocio.md](06-caso-de-negocio.md) | E6.1, E6.2, E6.3 | ED, FIN, EA | AM | QG-6 |

## Informes del engagement (familia de 3)

Ademas de los informes por fase, el motor genera un conjunto de **informes del engagement** orientados a distintas audiencias, enlazados desde este indice maestro:

- [`1-propuesta-comercial.md`](1-propuesta-comercial.md): **Propuesta comercial** emitida por Kulgops (documento de venta con las 11 secciones a-k; perfil corporativo e inversion marcados [DOC-ASSUMPTION]).
- [`2-reporte-gerencial.md`](2-reporte-gerencial.md): **Reporte gerencial** (soporte ejecutivo de la propuesta: alcance, fases, diagnostico de alto nivel, estrategia, riesgos, consideraciones y prerrequisitos; tono gerencial, no tecnico).

## Dossier de proyecto TO-BE (por etapa del SDLC)

Ademas de los informes por fase, el motor genera de forma **determinista** un **dossier de proyecto TO-BE** en [`to-be/`](to-be/README.md), organizado con **una subcarpeta por etapa/practica del SDLC** mas **registros transversales** del proyecto en todos los niveles arquitectonicos (negocio, aplicacion, datos, integracion, infraestructura, seguridad):

- [`to-be/01-requisitos/`](to-be/01-requisitos/requisitos.md): requisitos funcionales por modulo + NFR ISO 25010 + reglas de negocio.
- [`to-be/02-arquitectura/`](to-be/02-arquitectura/arquitectura.md): vistas TO-BE por nivel arquitectonico (reutiliza la Fase 4).
- [`to-be/03-specs/`](to-be/03-specs/specs.md): contratos API/eventos, esquemas de datos y specs por modulo (enlaza el catalogo 04b).
- [`to-be/04-ux/`](to-be/04-ux/ux.md): service blueprints, journeys y wireflows de originacion, pagos, B2C y cobranza.
- [`to-be/05-pruebas/`](to-be/05-pruebas/pruebas.md): estrategia, matriz de cobertura, Dry-Run/Tabletop y criterios de aceptacion.
- [`to-be/06-insumos-estimacion/`](to-be/06-insumos-estimacion/insumos-estimacion.md): descomposicion por modulo + tabla parametrica recalibrable (cifras [DOC-ASSUMPTION]).
- [`to-be/00-registros/`](to-be/README.md): ambiguedades, riesgos, consideraciones, restricciones y prerrequisitos, cada entrada con ID + nivel arquitectonico + severidad/impacto + estado + etiqueta epistemica.

> El dossier se regenera con `python3 advisory-system/quickstart.py --phase all` (es idempotente: una segunda corrida deja git limpio).

## Catalogo complementario

Ademas de los 7 informes por fase, el motor genera un catalogo **exhaustivo de Historias de Usuario + BDD/Gherkin** que cubre TODO el universo de modulos de Credi10 (sin muestreo), complemento de la Fase 4:

- [`04b-catalogo-historias.md`](04b-catalogo-historias.md): HU + criterios Gherkin (happy path + casos borde) por modulo, desde la fuente unica de verdad `advisory-system/phases/modules.py` (reutilizada por la estimacion por modulo de la Fase 5).

## Secciones profundizadas (iteracion de detalle)

Esta iteracion lleva el advisory al nivel de detalle necesario para **definir el alcance y estimar**:

- **Arquitectura de solucion (Fase 4):** vistas C4 N1-3 TO-BE, ADR-001..006, ERD por bounded context, contratos OpenAPI/AsyncAPI y BPMN.
- **Catalogo de HU/Gherkin exhaustivo (04b):** cobertura COMPLETA de todos los modulos declarados (sin muestreo).
- **Catalogo de oportunidades de IA (Fase 4):** IA-como-producto e IA-como-acelerador-de-construccion, renderizado desde el skill declarativo `ai-opportunities-catalog`.
- **Estimacion detallada por modulo (Fase 5):** T-Shirt + WSJF + story points / person-months con una **tabla parametrica recalibrable** y descomposicion por frente (Dev/Data/Integracion/QA/DevOps/gestion del cambio). Todas las cifras de esfuerzo son [DOC-ASSUMPTION].
- **Roadmap por olas (Fase 5):** gantt Mermaid con dependencias tecnicas explicitas (aciclicas) y ruta critica.
- **Evaluacion del dueno de negocio + riesgo de desfase (Fase 5):** scorecard de suficiencia para crear el proyecto y analisis de **schedule-slip** atado a la cobertura de la Base de Conocimiento, con veredicto Go/No-Go.

## Hilo Dorado (F1 -> F6)

La trazabilidad end-to-end encadena: Driver (F1) -> Capability (F1) -> Benchmark (F2) -> Gap (F3) -> Reliever (F3) -> ABB (F3.5) -> SBB (F4) -> Ola/WAV (F5) -> ROI/Outcome (F6).

```mermaid
flowchart LR
    DRV["DRV<br/>Drivers RFP (F1)"] --> CAP["CAP<br/>Capabilities (F1)"]
    CAP --> BMK["BMK<br/>Benchmarks (F2)"]
    BMK --> GAP["GAP<br/>Gaps (F3)"]
    GAP --> REL["REL<br/>Relievers (F3)"]
    REL --> ABB["ABB<br/>ABBs (F3.5)"]
    ABB --> SBB["SBB<br/>SBBs (F4)"]
    SBB --> WAV["WAV<br/>Olas (F5)"]
    WAV --> ROI["ROI<br/>Outcomes (F6)"]
```

## Flujo de fases y stage-gates

```mermaid
flowchart LR
    F0["Fase 0<br/>Higiene (QG-0)"] --> F1["Fase 1<br/>AS-IS (QG-1)"]
    F1 --> F2["Fase 2<br/>Estado del Arte (QG-2)"]
    F2 --> F3["Fase 3+3.5<br/>Gaps (QG-3)"]
    F3 --> F4["Fase 4<br/>TO-BE (QG-4)"]
    F4 --> F5["Fase 5<br/>Roadmap/RAID (QG-5)"]
    F5 --> F6["Fase 6<br/>Caso de Negocio (QG-6)"]
```

## Como regenerar

- Todo el pipeline (7 informes + este indice): `python3 advisory-system/quickstart.py --phase all`
- Una sola fase (ej. Fase 3): `python3 advisory-system/quickstart.py --phase 3`
- Opciones: `--corpus <ruta>` para otro corpus, `--out <ruta>` para otra carpeta de salida.

La documentacion del motor (estrategia, arquitectura y pruebas) esta en [`advisory-system/README.md`](../advisory-system/README.md).


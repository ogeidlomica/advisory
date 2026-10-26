# Fase 5 - Roadmap, Estimacion y RAID - Vista narrativa multinivel

> Nivel 1 del **informe tecnico multinivel** de Credi10 2.0. Esta fase se desagrega en **4 temas** (nivel 2), cada uno con jerarquia interna H1->H2->H3 (nivel 3) y narrativa de analisis sustancial, ademas de las tablas y diagramas reutilizados del motor.

> **Hilo narrativo de la fase.** Convertimos el diseño en numeros y en un plan: estimacion por modulo, priorizacion WSJF, roadmap por olas, RAID y riesgo de desfase. Es el corazon de 'estimar lo mas acertado posible'.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

## Temas de esta fase

| # | Tema | Archivo |
| --- | --- | --- |
| 1 | Estimacion por modulo y modelo parametrico | [`estimacion-por-modulo.md`](estimacion-por-modulo.md) |
| 2 | Roadmap por olas, WSJF y ruta critica | [`roadmap-olas.md`](roadmap-olas.md) |
| 3 | Matriz RAID (supuestos, restricciones, dependencias, prerrequisitos) | [`raid.md`](raid.md) |
| 4 | Evaluacion de suficiencia y riesgo de desfase | [`riesgo-de-desfase.md`](riesgo-de-desfase.md) |

## Como se conecta con el resto del informe

```mermaid
flowchart LR
    PREV["Fase anterior"] --> THIS["Fase 5 - Roadmap, Estimacion y RAID"]
    THIS --> NEXT["Fase siguiente"]
```

Para la **vista compacta** de esta fase (un solo archivo, misma evidencia, gobernada por el gate de calidad) ver [el informe plano de la fase](../../05-roadmap-estimacion-raid.md). Para volver al indice maestro del informe tecnico, ver [`../README.md`](../README.md).


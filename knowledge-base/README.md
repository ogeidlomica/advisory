# Base de Conocimiento - Advisory Credi10 2.0

Artefacto **generado** por el motor `advisory-system/` a partir de la ingesta COMPLETA del corpus de evidencia. Politica aplicada: **ingesta y validacion de los 18 documentos (sin muestreo)**; la clasificacion primary/secondary es PRIORIDAD, nunca exclusion. 100% reproducible re-ejecutando el quickstart.

> **Regenerar:** `python3 advisory-system/quickstart.py --phase all`

- Documentos totales ingeridos: **18** (15 PDF + 3 PNG)
- Metodo PDF: `zlib+regex` (capa de texto). Metodo PNG: transcripcion estatica (sin OCR).
- Honestidad epistemica: los PDF basados en imagen (sin texto extraible) se marcan `[EPISTEMIC-VOID]`, nunca se fabrican.

## Indice de documentos

| # | Documento | Tipo | Rol | Tamano (bytes) | Raw | Limpio | Cobertura | Flag | sha256 (12) |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| 1 | Api Integrador Atencion al cliente.pdf | pdf | secondary | 910137 | 3605911 | 3595967 | alta | [VERIFIED-FACT] | `230c3c9a38f8` |
| 2 | Arquitectura_Aplicacion_Despliegue_Credi10.png | png | primary | 1562032 | 427 | 427 | baja | [VERIFIED-FACT] | `825cd6260b5f` |
| 3 | Arquitectura_Infraestructura_AWS_Credi10.png | png | primary | 120983 | 276 | 276 | baja | [VERIFIED-FACT] | `f4491865fe1a` |
| 4 | B2C.pdf | pdf | secondary | 2256650 | 3879867 | 2130043 | alta | [VERIFIED-FACT] | `cde25f1342db` |
| 5 | BotonEcommerce.pdf | pdf | secondary | 2109944 | 3060169 | 1367492 | alta | [VERIFIED-FACT] | `7022aa5fb6e8` |
| 6 | Captura Foto.pdf | pdf | secondary | 846421 | 962629 | 242045 | alta | [VERIFIED-FACT] | `694c1d200196` |
| 7 | Diagrama_Contexto_Credi10.png | png | primary | 440843 | 444 | 444 | baja | [VERIFIED-FACT] | `ee8676200cd6` |
| 8 | Envio de RCL y RCR.pdf | pdf | secondary | 330050 | 175952 | 161351 | alta | [VERIFIED-FACT] | `8a5b0becf5b4` |
| 9 | GenerarPagos.pdf | pdf | secondary | 4933401 | 14994910 | 2349952 | alta | [VERIFIED-FACT] | `77dac0283c54` |
| 10 | LinkDePagos.pdf | pdf | secondary | 1542583 | 2309143 | 650504 | alta | [VERIFIED-FACT] | `b7217bd96e21` |
| 11 | Llamada predictiva.pdf | pdf | secondary | 180654 | 73018 | 69197 | alta | [VERIFIED-FACT] | `75de074b46da` |
| 12 | Originacion_API_Datacredito.pdf | pdf | secondary | 1070575 | 810463 | 357232 | alta | [VERIFIED-FACT] | `d3e307f9ec74` |
| 13 | Originacion_API_Inspektor.pdf | pdf | secondary | 831033 | 4504795 | 3899544 | alta | [VERIFIED-FACT] | `5699645db159` |
| 14 | Originacion_Aplicacion_ADMIN.pdf | pdf | secondary | 874196 | 806310 | 286223 | alta | [VERIFIED-FACT] | `1e1e01d8565d` |
| 15 | Originacion_CrossCore.pdf | pdf | secondary | 1335963 | 2937403 | 466349 | alta | [VERIFIED-FACT] | `44384189e295` |
| 16 | ProcesoCorteCartera.pdf | pdf | secondary | 4672023 | 6573062 | 5046503 | alta | [VERIFIED-FACT] | `c5058d4fb7ba` |
| 17 | RFP_CREDI10_2_0.pdf | pdf | primary | 398028 | 175086 | 161503 | alta | [VERIFIED-FACT] | `9ea0d58a40e2` |
| 18 | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | pdf | primary | 1490004 | 1695397 | 1673322 | alta | [VERIFIED-FACT] | `a8f03b42fa08` |

## Resumen de cobertura

| Banda | Documentos |
| --- | ---: |
| alta | 15 |
| media | 0 |
| baja | 3 |
| nula | 0 |
| **total** | **18** |

## Artefactos

- [`coverage-checklist.md`](coverage-checklist.md): checklist de cobertura 18/18 (metodo + banda + flag epistemico).
- [`key-facts.md`](key-facts.md): hechos clave consolidados con trazabilidad a su documento fuente.
- [`documents/`](documents/): un resumen jerarquico por documento.


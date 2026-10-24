# Checklist de cobertura del corpus (18/18)

Politica **complete-corpus-ingestion**: se verifica que CADA documento del corpus fue procesado (sin muestreo). Para cada documento se registra el metodo de procesamiento, la banda de cobertura textual y un flag epistemico honesto.

## Veredicto de ingesta: 18/18 documentos procesados (sin muestreo)

- PDF procesados (zlib+regex): **15**
- PNG transcritos (sin OCR): **3**
- Documentos marcados `[EPISTEMIC-VOID]` (sin texto util, registrados honestamente): **0**

| # | Documento | Procesado | Metodo | Banda | Flag |
| --- | --- | --- | --- | --- | --- |
| 1 | Api Integrador Atencion al cliente.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 2 | Arquitectura_Aplicacion_Despliegue_Credi10.png | si | transcripcion estatica PNG (sin OCR) | baja | [VERIFIED-FACT] |
| 3 | Arquitectura_Infraestructura_AWS_Credi10.png | si | transcripcion estatica PNG (sin OCR) | baja | [VERIFIED-FACT] |
| 4 | B2C.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 5 | BotonEcommerce.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 6 | Captura Foto.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 7 | Diagrama_Contexto_Credi10.png | si | transcripcion estatica PNG (sin OCR) | baja | [VERIFIED-FACT] |
| 8 | Envio de RCL y RCR.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 9 | GenerarPagos.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 10 | LinkDePagos.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 11 | Llamada predictiva.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 12 | Originacion_API_Datacredito.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 13 | Originacion_API_Inspektor.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 14 | Originacion_Aplicacion_ADMIN.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 15 | Originacion_CrossCore.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 16 | ProcesoCorteCartera.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 17 | RFP_CREDI10_2_0.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |
| 18 | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | si | zlib+regex (capa de texto PDF) | alta | [VERIFIED-FACT] |

## Resumen de cobertura

| Banda | Documentos |
| --- | ---: |
| alta | 15 |
| media | 0 |
| baja | 3 |
| nula | 0 |

**Aserto:** 18 de 18 documentos procesados (OK). No se omitio ningun documento (cobertura total, sin muestreo).


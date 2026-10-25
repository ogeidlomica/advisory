# Checklist de cobertura del corpus (18/18)

Politica **complete-corpus-ingestion**: se verifica que CADA documento del corpus fue procesado (sin muestreo). Para cada documento se registra el metodo de procesamiento, el porcentaje de **texto util real**, la banda de cobertura y un flag epistemico honesto.

> **Nota de metodo (honestidad epistemica):** la banda de cobertura ahora se calcula a partir del **texto util real** = caracteres en palabras reales (>= 3 letras, con acentos) / bytes de texto extraido, **no** a partir del tamano crudo del texto extraido. El metodo anterior (texto_limpio/tamano) SOBRESTIMABA la cobertura de los PDF basados en imagen.

> **OCR en este entorno:** NO hay motor OCR disponible (ni pytesseract/PIL/fitz ni tesseract/ocrmypdf/pdfimages/pdftoppm, y sin red para instalarlos). Degradacion honesta: los PDF basados en imagen quedan como **pendiente-OCR** y `[EPISTEMIC-VOID]`; **no se fabrica texto**.

## Veredicto de ingesta: 18/18 documentos procesados (sin muestreo)

- PDF procesados (zlib+regex): **15**
- PNG transcritos (sin OCR): **3**
- Documentos recuperados via OCR `[OCR-EXTRACTED]`: **0**
- Documentos **pendiente-OCR** (PDF basado en imagen, texto util insuficiente): **5**
- Documentos marcados `[EPISTEMIC-VOID]` (sin texto util real, registrados honestamente): **5**

| # | Documento | Procesado | Metodo | Texto util real | Banda | Flag |
| --- | --- | --- | --- | ---: | --- | --- |
| 1 | Api Integrador Atencion al cliente.pdf | si | pendiente-OCR | 0.70% | nula | [EPISTEMIC-VOID] |
| 2 | Arquitectura_Aplicacion_Despliegue_Credi10.png | si | transcripcion estatica PNG (sin OCR) | 64.87% | alta | [VERIFIED-FACT] |
| 3 | Arquitectura_Infraestructura_AWS_Credi10.png | si | transcripcion estatica PNG (sin OCR) | 70.29% | alta | [VERIFIED-FACT] |
| 4 | B2C.pdf | si | pendiente-OCR | 2.55% | nula | [EPISTEMIC-VOID] |
| 5 | BotonEcommerce.pdf | si | texto nativo (zlib+regex) | 3.29% | baja | [VERIFIED-FACT] |
| 6 | Captura Foto.pdf | si | texto nativo (zlib+regex) | 6.48% | baja | [VERIFIED-FACT] |
| 7 | Diagrama_Contexto_Credi10.png | si | transcripcion estatica PNG (sin OCR) | 70.95% | alta | [VERIFIED-FACT] |
| 8 | Envio de RCL y RCR.pdf | si | texto nativo (zlib+regex) | 4.13% | baja | [VERIFIED-FACT] |
| 9 | GenerarPagos.pdf | si | texto nativo (zlib+regex) | 6.86% | baja | [VERIFIED-FACT] |
| 10 | LinkDePagos.pdf | si | texto nativo (zlib+regex) | 3.43% | baja | [VERIFIED-FACT] |
| 11 | Llamada predictiva.pdf | si | texto nativo (zlib+regex) | 7.15% | baja | [VERIFIED-FACT] |
| 12 | Originacion_API_Datacredito.pdf | si | texto nativo (zlib+regex) | 4.35% | baja | [VERIFIED-FACT] |
| 13 | Originacion_API_Inspektor.pdf | si | pendiente-OCR | 0.99% | nula | [EPISTEMIC-VOID] |
| 14 | Originacion_Aplicacion_ADMIN.pdf | si | texto nativo (zlib+regex) | 5.75% | baja | [VERIFIED-FACT] |
| 15 | Originacion_CrossCore.pdf | si | texto nativo (zlib+regex) | 13.37% | baja | [VERIFIED-FACT] |
| 16 | ProcesoCorteCartera.pdf | si | pendiente-OCR | 1.09% | nula | [EPISTEMIC-VOID] |
| 17 | RFP_CREDI10_2_0.pdf | si | texto nativo (zlib+regex) | 5.92% | baja | [VERIFIED-FACT] |
| 18 | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | si | pendiente-OCR | 1.60% | nula | [EPISTEMIC-VOID] |

## Resumen de cobertura (por texto util real)

| Banda | Documentos |
| --- | ---: |
| alta | 3 |
| media | 0 |
| baja | 10 |
| nula | 5 |

**Aserto:** 18 de 18 documentos procesados (OK). No se omitio ningun documento (cobertura total, sin muestreo). Las bandas reflejan **texto util real**: un PDF basado en imagen ya no se reporta como 'alta'; queda 'baja'/'nula' con nota 'OCR pendiente'.


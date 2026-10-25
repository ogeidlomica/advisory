# Checklist de cobertura del corpus (18/18)

Politica **complete-corpus-ingestion**: se verifica que CADA documento del corpus fue procesado (sin muestreo). Para cada documento se registra el metodo de procesamiento, el porcentaje de **texto util real**, la banda de cobertura y un flag epistemico honesto.

> **Nota de metodo (honestidad epistemica):** la banda de cobertura ahora se calcula a partir del **texto util real** = caracteres en palabras reales (>= 3 letras, con acentos) / bytes de texto extraido, **no** a partir del tamano crudo del texto extraido. El metodo anterior (texto_limpio/tamano) SOBRESTIMABA la cobertura de los PDF basados en imagen.

> **OCR en este entorno:** NO hay motor OCR disponible (ni pytesseract/PIL/fitz ni tesseract/ocrmypdf/pdfimages/pdftoppm, y sin red para instalarlos). Degradacion honesta: los PDF basados en imagen quedan como **pendiente-OCR** y `[EPISTEMIC-VOID]`; **no se fabrica texto**.

## Veredicto de ingesta: 18/18 documentos procesados (sin muestreo)

- PDF procesados (zlib + /ToUnicode por fuente): **15**
- PNG transcritos (sin OCR): **3**
- Documentos recuperados via OCR `[OCR-EXTRACTED]`: **0**
- Documentos **pendiente-OCR** (PDF basado en imagen, texto util insuficiente): **0**
- Documentos marcados `[EPISTEMIC-VOID]` (sin texto util real, registrados honestamente): **0**

| # | Documento | Procesado | Metodo | Texto util real | Banda | Flag |
| --- | --- | --- | --- | ---: | --- | --- |
| 1 | Api Integrador Atencion al cliente.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 64.31% | alta | [VERIFIED-FACT] |
| 2 | Arquitectura_Aplicacion_Despliegue_Credi10.png | si | transcripcion estatica PNG (sin OCR) | 64.87% | alta | [VERIFIED-FACT] |
| 3 | Arquitectura_Infraestructura_AWS_Credi10.png | si | transcripcion estatica PNG (sin OCR) | 70.29% | alta | [VERIFIED-FACT] |
| 4 | B2C.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 54.60% | alta | [VERIFIED-FACT] |
| 5 | BotonEcommerce.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 50.10% | alta | [VERIFIED-FACT] |
| 6 | Captura Foto.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 66.06% | alta | [VERIFIED-FACT] |
| 7 | Diagrama_Contexto_Credi10.png | si | transcripcion estatica PNG (sin OCR) | 70.95% | alta | [VERIFIED-FACT] |
| 8 | Envio de RCL y RCR.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 66.43% | alta | [VERIFIED-FACT] |
| 9 | GenerarPagos.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 60.38% | alta | [VERIFIED-FACT] |
| 10 | LinkDePagos.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 65.91% | alta | [VERIFIED-FACT] |
| 11 | Llamada predictiva.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 75.66% | alta | [VERIFIED-FACT] |
| 12 | Originacion_API_Datacredito.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 68.03% | alta | [VERIFIED-FACT] |
| 13 | Originacion_API_Inspektor.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 68.27% | alta | [VERIFIED-FACT] |
| 14 | Originacion_Aplicacion_ADMIN.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 69.63% | alta | [VERIFIED-FACT] |
| 15 | Originacion_CrossCore.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 64.28% | alta | [VERIFIED-FACT] |
| 16 | ProcesoCorteCartera.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 53.85% | alta | [VERIFIED-FACT] |
| 17 | RFP_CREDI10_2_0.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 73.05% | alta | [VERIFIED-FACT] |
| 18 | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | si | texto nativo (zlib + /ToUnicode por fuente) | 69.74% | alta | [VERIFIED-FACT] |

## Resumen de cobertura (por texto util real)

| Banda | Documentos |
| --- | ---: |
| alta | 18 |
| media | 0 |
| baja | 0 |
| nula | 0 |

**Aserto:** 18 de 18 documentos procesados (OK). No se omitio ningun documento (cobertura total, sin muestreo). Las bandas reflejan **texto util real**: el texto nativo recuperado mediante decodificacion por fuente (CMap /ToUnicode) es capa de texto REAL, no OCR, por lo que conserva su flag [VERIFIED-FACT].

## Comparacion antes/despues: recuperacion de texto util

Esta seccion compara el **texto util real %** de cada documento ANTES de la decodificacion por fuente (linea base FEAT-001, metodo `zlib+regex` ingenuo que ademas arrastraba ruido binario de imagenes/fuentes) contra el valor ACTUAL, obtenido con el extractor consciente de la fuente (`engine/pdf_text.py`): rastreo de la fuente activa (`Tf`), decodificacion de literales `( ... )` y cadenas hex `< ... >` en `Tj`/`TJ`, y mapeo de los codigos de glifo a traves del CMap `/ToUnicode` de cada fuente embebida, leyendo SOLO dentro de objetos de texto `BT ... ET`.

> **Honestidad epistemica:** la recuperacion es de **texto nativo** (capa de texto del PDF decodificada correctamente), NO es OCR. No se fabrica contenido; el texto recuperado conserva el flag `[VERIFIED-FACT]`. El adaptador OCR sigue degradando honestamente (0 OCR en este entorno).

| # | Documento | Tipo | Texto util antes | Texto util ahora | Delta | Banda ahora | Flag |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | Api Integrador Atencion al cliente.pdf | pdf | 0.70% | 64.31% | +63.61 pp | alta | [VERIFIED-FACT] |
| 2 | Arquitectura_Aplicacion_Despliegue_Credi10.png | png | 64.87% | 64.87% | +0.00 pp | alta | [VERIFIED-FACT] |
| 3 | Arquitectura_Infraestructura_AWS_Credi10.png | png | 70.29% | 70.29% | +0.00 pp | alta | [VERIFIED-FACT] |
| 4 | B2C.pdf | pdf | 2.55% | 54.60% | +52.05 pp | alta | [VERIFIED-FACT] |
| 5 | BotonEcommerce.pdf | pdf | 3.29% | 50.10% | +46.81 pp | alta | [VERIFIED-FACT] |
| 6 | Captura Foto.pdf | pdf | 6.48% | 66.06% | +59.58 pp | alta | [VERIFIED-FACT] |
| 7 | Diagrama_Contexto_Credi10.png | png | 70.95% | 70.95% | +0.00 pp | alta | [VERIFIED-FACT] |
| 8 | Envio de RCL y RCR.pdf | pdf | 4.13% | 66.43% | +62.30 pp | alta | [VERIFIED-FACT] |
| 9 | GenerarPagos.pdf | pdf | 6.86% | 60.38% | +53.52 pp | alta | [VERIFIED-FACT] |
| 10 | LinkDePagos.pdf | pdf | 3.43% | 65.91% | +62.48 pp | alta | [VERIFIED-FACT] |
| 11 | Llamada predictiva.pdf | pdf | 7.15% | 75.66% | +68.51 pp | alta | [VERIFIED-FACT] |
| 12 | Originacion_API_Datacredito.pdf | pdf | 4.35% | 68.03% | +63.68 pp | alta | [VERIFIED-FACT] |
| 13 | Originacion_API_Inspektor.pdf | pdf | 0.99% | 68.27% | +67.28 pp | alta | [VERIFIED-FACT] |
| 14 | Originacion_Aplicacion_ADMIN.pdf | pdf | 5.75% | 69.63% | +63.88 pp | alta | [VERIFIED-FACT] |
| 15 | Originacion_CrossCore.pdf | pdf | 13.37% | 64.28% | +50.91 pp | alta | [VERIFIED-FACT] |
| 16 | ProcesoCorteCartera.pdf | pdf | 1.09% | 53.85% | +52.76 pp | alta | [VERIFIED-FACT] |
| 17 | RFP_CREDI10_2_0.pdf | pdf | 5.92% | 73.05% | +67.13 pp | alta | [VERIFIED-FACT] |
| 18 | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | pdf | 1.60% | 69.74% | +68.14 pp | alta | [VERIFIED-FACT] |

### Lectura honesta de los resultados

- **Documentos que subieron:** 15 de 18 (comparables con linea base).
- **PDFs recuperados del vacio epistemico:** 5 de 5 PDFs que estaban en banda 'nula' / `[EPISTEMIC-VOID]` cruzaron el umbral de texto util (3%) y hoy son texto nativo `[VERIFIED-FACT]`: Api Integrador Atencion al cliente.pdf, B2C.pdf, Originacion_API_Inspektor.pdf, ProcesoCorteCartera.pdf, WSO2 y Studio F - Assessment Mayo2026-Final.pdf.
- **Por que subieron:** su capa de texto SI existia, pero usaba fuentes embebidas con codificacion personalizada (CMap `/ToUnicode`, p. ej. `Type0`/`Identity-H`). El extractor anterior no aplicaba el mapeo por fuente y ademas inyectaba bytes binarios de imagenes como si fueran texto, hundiendo el ratio de texto util. El nuevo extractor decodifica cada fuente y lee solo objetos de texto, recuperando el espanol legible (p. ej. 'aplicacion'/'arquitectura'/'integracion').
- **Limites honestos (lo que NO resuelve este nivel):** las paginas que son imagenes reales (JPEG `DCTDecode` sin capa de texto) siguen necesitando OCR real (nivel 2); las fuentes sin `/ToUnicode` ni `/Differences` reconocible degradan al heuristico latin-1. Nada de esto fabrica texto: lo no recuperable permanece marcado honestamente.


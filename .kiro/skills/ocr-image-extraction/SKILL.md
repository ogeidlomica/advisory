---
name: ocr-image-extraction
description: Usar cuando un PDF o imagen del corpus tiene baja proporcion de texto util real (paginas escaneadas / solo-imagen); define cuando aplicar OCR, los motores soportados en orden de preferencia, el umbral de confianza, la etiqueta epistemica [OCR-EXTRACTED] y la regla de DEGRADACION HONESTA cuando no hay motor OCR disponible.
version: 1.0.0
owner: Zero-Drift Advisory - Organizacion
applies_to: todos los engagements, cualquier cliente, cualquier corpus con PDF/imagenes escaneadas
---

# Politica: Extraccion OCR de documentos basados en imagen (ocr-image-extraction)

Politica **permanente y reutilizable** de la organizacion. No es especifica de
ningun cliente. Credi10 2.0 se cita solo como *ejemplo de aplicacion*, nunca
como el sujeto de la politica.

## 1. Principio (no negociable)

> Un PDF o imagen **sin capa de texto util** (escaneado / solo-imagen) **no se
> abandona ni se inventa**. Se intenta recuperar su contenido mediante **OCR**
> cuando el entorno de ejecucion dispone de un motor OCR. Cuando **no** lo
> dispone, el documento se marca honestamente como **pendiente de OCR** con su
> cobertura **real**; esta prohibido fabricar texto para rellenar el vacio.

Esta politica es complementaria de `complete-corpus-ingestion`: alli se obliga a
ingerir TODO el corpus; aqui se define como recuperar, de forma honesta, el
contenido de los artefactos que NO tienen una capa de texto nativa explotable.

## 2. Cuando aplicar OCR (condicion de disparo)

Se evalua el **texto util real** del documento:

```
texto_util_real = caracteres_en_palabras_reales / bytes_de_texto_extraido
```

donde "palabra real" es una secuencia de **>= 3 letras** (incluidas vocales
acentuadas y ñ del espanol). Se aplica OCR cuando:

- el documento es un **PDF basado en imagen** o tiene paginas escaneadas; y
- su `texto_util_real` esta por **debajo del umbral** de texto util
  (`MIN_USEFUL_RATIO_FOR_TEXT`, p. ej. 3%), es decir, lo que la capa de texto
  nativa aporta es ruido/fragmentos, no contenido explotable.

Los diagramas registrados por **transcripcion humana estatica** (PNG) NO
requieren OCR: ya tienen una transcripcion verificada `[VERIFIED-FACT]`.

## 3. Motores OCR soportados (orden de preferencia)

El adaptador prueba el entorno y usa el **primer** motor completamente
disponible, en este orden:

1. **pytesseract / Tesseract** (modulo `pytesseract` + binario `tesseract`).
2. **ocrmypdf** (binario `ocrmypdf`; agrega capa de texto y se re-extrae).
3. **pdfimages + tesseract** (rasteriza imagenes del PDF y las pasa a OCR).
4. **pdftoppm + tesseract** (rasteriza paginas a imagen y las pasa a OCR).

La deteccion es en **tiempo de ejecucion**: binarios via `shutil.which` y
modulos via `try/except ImportError`, sin que la ausencia de ninguno provoque un
error. El orden y la lista son perillas declarativas recalibrables. Los imports
de terceros (`pytesseract`, `PIL`, `fitz`) son **perezosos**: ocurren SOLO
dentro de la funcion del motor cuando este fue detectado, nunca a nivel de
modulo, para que `engine/ocr.py` importe con **stdlib pura** en cualquier
entorno.

Cada motor tolera la ausencia de su rasterizador preferido:

- **pytesseract** prefiere **PyMuPDF (`fitz`)** para rasterizar cada pagina del
  PDF a imagen en proceso; si `fitz` no esta, cae a los rasterizadores CLI
  **`pdftoppm`/`pdfimages`** + `PIL`, de modo que una instalacion simple
  `pytesseract`+`tesseract` sigue sirviendo sobre PDFs crudos.
- La capacidad tambien puede **OCR-ear una imagen suelta** (PNG/JPG/TIFF/...)
  pasada directamente (util para los diagramas de arquitectura en futuros
  corpus), no solo PDFs: `_ocr_image_file` usa pytesseract+PIL y, si falta
  pytesseract pero existe el binario `tesseract`, invoca el CLI.
- Toda invocacion de subproceso (ocrmypdf/tesseract/rasterizadores) corre bajo
  un **timeout** duro (`OCR_SUBPROCESS_TIMEOUT`, p. ej. 300 s). Un motor colgado
  o que falla **degrada a "sin texto"** en vez de abortar el pipeline.

## 4. Umbral de confianza

Cuando un motor OCR produce texto con confianza por palabra/pagina, se
**descarta** el texto cuya confianza este por debajo de
`OCR_CONFIDENCE_THRESHOLD` (0..100, p. ej. 60). La ruta pytesseract usa
`image_to_data` para obtener la confianza por palabra y **filtra** las palabras
bajo el umbral (y descarta los bloques `conf == -1` de no-texto); si esa llamada
estructurada no esta disponible, cae a `image_to_string`. Es una perilla
declarativa; solo se consulta cuando un motor real corre.

## 5. Etiquetas epistemicas (honestidad)

| Etiqueta | Significado |
| --- | --- |
| `[VERIFIED-FACT]` | Capa de texto **nativa** util, o transcripcion humana estatica de un diagrama. |
| `[OCR-EXTRACTED]` | Texto **recuperado via OCR** desde una imagen/escaneo. Distinto de un hecho nativo verificado. |
| `[EPISTEMIC-VOID]` | Contenido **no recuperable** en este entorno (OCR pendiente / no disponible). No se fabrica. |

`[OCR-EXTRACTED]` es texto recuperado, no texto nativo: se trata con la cautela
de una recuperacion automatica (puede contener errores de OCR) y se cita como
tal en la trazabilidad.

## 6. Regla de DEGRADACION HONESTA (sin motor OCR)

Cuando el entorno **no** tiene ningun motor OCR disponible (p. ej. sin
`tesseract`/`ocrmypdf`/`pdfimages`/`pdftoppm` ni `pytesseract`/`PIL`/`fitz`, y
sin red para instalarlos):

- [ ] **No se fabrica texto.** El contenido ausente permanece ausente.
- [ ] El documento conserva su texto nativo (posiblemente vacio/bajo) **sin
      alterarlo**, para que la salida siga siendo **determinista y byte-identica**
      al re-ejecutar.
- [ ] Se registra el metodo de ingesta honesto:
      `OCR pendiente (motor no disponible en este entorno)`.
- [ ] Se reporta la **cobertura real** por texto util; el documento no puede
      clasificarse como banda `alta`.
- [ ] Si no hay texto util real, se marca `[EPISTEMIC-VOID]` (OCR pendiente).

La capacidad OCR queda **lista y probada**: cuando el mismo corpus se procese en
un entorno con motor OCR, el adaptador recuperara el texto y lo marcara
`[OCR-EXTRACTED]` sin cambios de codigo.

## 7. Checklist de aplicacion (declarativo, lo ejecuta el motor)

```checklist
- id: ocr-capability-probe
  check: Se detecto en runtime si hay motor OCR (binarios + modulos), sin crashear.
- id: ocr-trigger-by-useful-text
  check: Se evaluo el texto util real de cada PDF y se disparo OCR bajo el umbral.
- id: ocr-engine-preference
  check: Si hay motor, se uso el primero disponible en el orden de preferencia.
- id: ocr-extracted-tag
  check: El texto recuperado via OCR se etiqueta [OCR-EXTRACTED].
- id: honest-degradation
  check: Sin motor OCR, se marca 'OCR pendiente' y cobertura real; no se fabrica texto.
- id: determinism
  check: Sin motor OCR el resultado es un estado 'pendiente' fijo y byte-estable.
- id: no-fabrication
  check: Los vacios no recuperables se marcan [EPISTEMIC-VOID]; nunca se inventan.
```

## 8. Politica de merge (fusion con el texto nativo)

El OCR es un **fallback**, no un reemplazo ciego. El adaptador se consulta
**solo** para los documentos cuyo **texto util nativo** quedo por debajo del
umbral de utilidad (`MIN_USEFUL_RATIO_FOR_TEXT`). Para un PDF cuya capa de texto
nativa ya es suficiente, el OCR **nunca se invoca**, de modo que no se duplica
texto que ya salio nativo. Cuando el OCR si corre y recupera texto de confianza,
este **sustituye** la pobre capa nativa de ese documento (no se concatenan ambas
versiones del mismo contenido) y el documento se re-mide por texto util. La
politica es determinista: dada la misma entrada y el mismo entorno, el resultado
es byte-identico.

## 9. Activacion en un entorno productivo

La capacidad ya esta **implementada**; en produccion solo hace falta instalar un
motor (sin cambios de codigo). Opciones tipicas:

```bash
# Opcion A: Tesseract + pytesseract (+ un rasterizador de PDF)
apt install tesseract-ocr poppler-utils         # tesseract + pdftoppm/pdfimages
pip install pytesseract pdf2image Pillow         # o 'pip install PyMuPDF' (fitz)

# Opcion B: ocrmypdf (agrega capa de texto y se re-extrae)
apt install ocrmypdf
```

Al detectar el motor, `enrich_document` enviara a OCR los documentos
`pendiente-OCR`, incorporara el texto marcado `[OCR-EXTRACTED]` y actualizara su
% de texto util y su banda en el `coverage-checklist.md`, automaticamente.

## 10. Implementacion de referencia

El adaptador stdlib en `advisory-system/engine/ocr.py` implementa esta politica:
`detect_ocr_capability()` sondea el entorno (binarios via `shutil.which`,
modulos via `try/except ImportError`) y devuelve un `OCRCapability`
{`available`, `engine`, `reason`, `probed`}; `extract_text_via_ocr(path, cap)`
ejecuta el motor disponible (PDF o imagen suelta) y devuelve
`(texto, "[OCR-EXTRACTED]")`, o degrada honestamente a `("", "[EPISTEMIC-VOID]")`
sin fabricar. Los motores reales (`_ocr_pytesseract` con fallback CLI,
`_ocr_ocrmypdf`, `_ocr_rasterize_then_tesseract`, `_ocr_image_file`) hacen
imports **perezosos**, aplican el **filtro de confianza** por palabra
(`_pytesseract_text_above_confidence`) y corren bajo **timeout**; cualquier
fallo degrada a "sin texto" sin abortar. La integracion vive en
`engine/knowledge.py` (`enrich_document`): se calcula el **texto util real**, y
si esta bajo `MIN_USEFUL_RATIO_FOR_TEXT` se consulta el adaptador; la banda de
cobertura y el flag epistemico se derivan del texto util real (perilla
`USEFUL_TEXT_BANDS`), no del tamano crudo. Esta es la **capa L2** de la
arquitectura `document-extraction-architecture` (L1 texto nativo + `/ToUnicode`;
L2 OCR; L3 vision/LLM; L4 NLP/LLM). Determinista, sin red ni LLM, y recalibrable
via las perillas de politica (`OCR_ENGINE_PREFERENCE`,
`OCR_CONFIDENCE_THRESHOLD`, `OCR_SUBPROCESS_TIMEOUT`, `USEFUL_TEXT_BANDS`,
`MIN_USEFUL_RATIO_FOR_TEXT`).

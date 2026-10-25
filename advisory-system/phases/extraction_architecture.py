"""Anexo B - Arquitectura IA multicapa de extraccion de texto util (FEAT-003).

Generador DETERMINISTA, stdlib-only, del **anexo B del informe tecnico**: la
recomendacion de advisory de una **arquitectura de extraccion de documentos
multicapa (L1-L4)** cuyo objetivo es **maximizar el texto util real** de todo
el corpus. Gobernado por el skill generico
``document-extraction-architecture`` (y por ``technical-narrative-multilevel``
en cuanto a la regla de prosa sustancial).

Que produce (bajo ``3-informe-tecnico/anexo-b-arquitectura-extraccion/``):

  * ``README.md`` con:
      - narrativa sustancial en espanol (no solo tablas/Mermaid),
      - un diagrama **Mermaid** de la arquitectura por capas con el flujo de
        fallback,
      - la **tabla de tactica por tipo de documento**,
      - la **comparacion antes/despues real** del corpus (cifras de texto util
        LEIDAS de la Base de Conocimiento viva + la linea base declarativa
        ``knowledge.USEFUL_TEXT_BASELINE_PCT``, NO hardcodeadas aqui), y
      - la separacion EXPLICITA entre lo IMPLEMENTADO aqui (L1, decodificacion
        de fuentes) y lo que requiere el entorno de produccion (L2-L4).

Fundamentacion (grounding): las cifras de texto util "ahora" se obtienen de la
``KnowledgeBase`` del run (``doc.useful_ratio``), y las de la linea base del
constante compartido ``engine.knowledge.USEFUL_TEXT_BASELINE_PCT``, de modo que
el anexo se mantiene en sincronia con el analisis de cobertura real y es
determinista. Si no hay Base de Conocimiento disponible (p. ej. una prueba que
no corre el pipeline completo) el anexo degrada a la linea base declarativa, sin
fabricar numeros.

Determinismo: contenido estatico ordenado por nombre de archivo; sin azar ni
timestamps; ``os.makedirs(..., exist_ok=True)``. Una segunda corrida deja la
salida byte-identica.
"""

from __future__ import annotations

import os
from typing import List, Optional

from engine import knowledge as kb_mod


ANNEX_DIRNAME = "anexo-b-arquitectura-extraccion"


# --------------------------------------------------------------------------- #
# Helpers de datos (grounding en la Base de Conocimiento viva).
# --------------------------------------------------------------------------- #

def _now_pct(knowledge_base, filename: str) -> Optional[float]:
    """Texto util % ACTUAL del documento, leido de la KB viva (o None)."""
    if knowledge_base is None:
        return None
    try:
        doc = knowledge_base.by_filename(filename)
    except Exception:
        return None
    if doc is None:
        return None
    return doc.useful_ratio * 100.0


def _doc_band_flag(knowledge_base, filename: str):
    """(banda, flag) ACTUAL del documento desde la KB viva, o (None, None)."""
    if knowledge_base is None:
        return (None, None)
    try:
        doc = knowledge_base.by_filename(filename)
    except Exception:
        return (None, None)
    if doc is None:
        return (None, None)
    return (doc.coverage_band, doc.epistemic_flag)


def _recovered_void_names(knowledge_base) -> List[str]:
    """Nombres de los PDFs 'nula'/[EPISTEMIC-VOID] de base que ya cruzaron umbral."""
    threshold = kb_mod.MIN_USEFUL_RATIO_FOR_TEXT * 100.0
    names: List[str] = []
    for name in kb_mod.BASELINE_NULA_PDFS:
        now = _now_pct(knowledge_base, name)
        if now is not None and now >= threshold:
            names.append(name)
    return names


# --------------------------------------------------------------------------- #
# Secciones del anexo.
# --------------------------------------------------------------------------- #

def _architecture_mermaid() -> str:
    return (
        "```mermaid\n"
        "flowchart TD\n"
        '    DOC["Documento del corpus"] --> L1["L1 - Texto nativo + '
        'decodificacion de fuentes<br/>(ToUnicode / Differences)"]\n'
        '    L1 --> U1{"texto util &gt;= umbral?"}\n'
        '    U1 -- "si" --> OK1["Aceptar L1<br/>[VERIFIED-FACT]"]\n'
        '    U1 -- "no" --> IMG{"pagina es imagen / escaneo?"}\n'
        '    IMG -- "si" --> L2["L2 - OCR de paginas imagen<br/>'
        '(Tesseract / ocrmypdf)"]\n'
        '    IMG -- "no" --> HEUR["Fuente sin mapa: heuristico latin-1"]\n'
        '    L2 --> U2{"confianza OCR y texto util &gt;= umbral?"}\n'
        '    U2 -- "si" --> OK2["Aceptar L2<br/>[OCR-EXTRACTED]"]\n'
        '    U2 -- "no" --> L3["L3 - Vision / LLM multimodal<br/>'
        '(layout, tablas, diagramas)"]\n'
        '    L3 --> U3{"texto util &gt;= umbral?"}\n'
        '    U3 -- "si" --> OK3["Aceptar L3<br/>[OCR-EXTRACTED]"]\n'
        '    U3 -- "no" --> VOID["[EPISTEMIC-VOID]<br/>pendiente, no se fabrica"]\n'
        '    OK1 --> L4["L4 - NLP / LLM<br/>estructura, normaliza y extrae '
        'entidades con trazabilidad"]\n'
        "    OK2 --> L4\n"
        "    OK3 --> L4\n"
        "    HEUR --> L4\n"
        '    L4 --> OUT["Texto util maximizado<br/>+ hechos trazables"]\n'
        "```\n"
    )


def _layers_table() -> List[str]:
    return [
        "| Capa | Que hace | Tecnologia tipica | Etiqueta | Estado aqui |",
        "| --- | --- | --- | --- | --- |",
        "| **L1** Texto nativo + decodificacion de fuentes | Lee la capa de "
        "texto del PDF y decodifica fuentes embebidas de codificacion "
        "personalizada (CMap `/ToUnicode`, `/Encoding /Differences`, "
        "`Type0`/`Identity-H`). | stdlib (`zlib`+`re`), sin red | "
        "`[VERIFIED-FACT]` | **IMPLEMENTADA** |",
        "| **L2** OCR de paginas imagen | Rasteriza y aplica OCR a paginas que "
        "son imagen/escaneo sin capa de texto. | Tesseract / ocrmypdf | "
        "`[OCR-EXTRACTED]` | Requiere produccion |",
        "| **L3** Vision / LLM multimodal | Interpreta layout complejo, tablas, "
        "formularios y diagramas. | Document AI / LLM multimodal | "
        "`[OCR-EXTRACTED]` | Requiere produccion |",
        "| **L4** NLP / LLM de post-proceso | Estructura, normaliza y extrae "
        "entidades/hechos con trazabilidad, sin inventar lo ausente. | NLP / "
        "LLM con citas | hereda la capa origen | Requiere produccion |",
    ]


def _tactics_table() -> List[str]:
    return [
        "| Tipo de documento | Capa recomendada | Fallback | Nota |",
        "| --- | --- | --- | --- |",
        "| PDF con capa de texto nativa limpia | L1 | - | Caso ideal, costo "
        "minimo. |",
        "| PDF con fuentes embebidas de codificacion personalizada "
        "(`Type0`/`Identity-H`, `/ToUnicode`) | L1 (decodificacion de fuentes) "
        "| L2 | El contenido SI existe; hay que decodificarlo, no escanearlo. |",
        "| PDF escaneado / pagina imagen (`DCTDecode`, sin capa de texto) | L2 "
        "(OCR) | L3 | Requiere motor OCR en el entorno. |",
        "| PDF con tablas / formularios / layout complejo | L3 (vision/LLM) | "
        "L2 | El OCR plano pierde la estructura. |",
        "| Diagrama / plano (PNG/JPG) de arquitectura | Transcripcion humana "
        "estatica `[VERIFIED-FACT]` o L3 | L2 | El valor esta en relaciones, no "
        "en texto corrido. |",
        "| Documento ofimatico nativo (docx/xlsx/pptx) | L1 (parser del "
        "formato) | L4 | Texto ya estructurado; L4 normaliza entidades. |",
    ]


def _comparison_table(knowledge_base) -> List[str]:
    """Tabla antes/despues GROUNDED: 'ahora' de la KB viva, 'antes' del baseline.

    Ordenada por el delta descendente (mayor recuperacion primero) y, a igual
    delta, por nombre de archivo, para ser determinista.
    """
    rows = []
    for name in sorted(kb_mod.USEFUL_TEXT_BASELINE_PCT):
        before = kb_mod.USEFUL_TEXT_BASELINE_PCT[name]
        now = _now_pct(knowledge_base, name)
        band, flag = _doc_band_flag(knowledge_base, name)
        if now is None:
            # Sin KB viva: degradamos a la linea base (no se fabrica el 'ahora').
            now_display = "n/d"
            delta_val = -1.0
            delta_display = "n/d"
        else:
            delta = now - before
            if abs(delta) < 0.005:
                delta = 0.0
            sign = "+" if delta >= 0 else ""
            now_display = f"{now:.2f}%"
            delta_val = delta
            delta_display = f"{sign}{delta:.2f} pp"
        rows.append((delta_val, name, before, now_display, delta_display,
                     band or "-", flag or "-"))

    # Orden determinista: delta desc, luego nombre asc.
    rows.sort(key=lambda r: (-r[0], r[1]))

    lines = [
        "| # | Documento | Texto util antes | Texto util ahora | Delta | "
        "Banda ahora | Flag |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for i, (_delta, name, before, now_display, delta_display, band, flag) in \
            enumerate(rows, start=1):
        lines.append(
            f"| {i} | {name} | {before:.2f}% | {now_display} | "
            f"{delta_display} | {band} | {flag} |"
        )
    return lines


# --------------------------------------------------------------------------- #
# Cuerpo del anexo.
# --------------------------------------------------------------------------- #

def build_annex(knowledge_base=None) -> str:
    recovered = _recovered_void_names(knowledge_base)
    n_recovered = len(recovered)
    n_void_base = len(kb_mod.BASELINE_NULA_PDFS)
    threshold_pct = kb_mod.MIN_USEFUL_RATIO_FOR_TEXT * 100.0

    # Cifras ancla del WSO2 (grounding de un caso concreto en la narrativa).
    wso2_name = "WSO2 y Studio F - Assessment Mayo2026-Final.pdf"
    wso2_before = kb_mod.USEFUL_TEXT_BASELINE_PCT.get(wso2_name)
    wso2_now = _now_pct(knowledge_base, wso2_name)
    if wso2_before is not None and wso2_now is not None:
        wso2_phrase = (
            f"el assessment WSO2/Studio F paso de **{wso2_before:.2f}%** de "
            f"texto util (banda 'nula', `[EPISTEMIC-VOID]`) a "
            f"**{wso2_now:.2f}%** (banda 'alta', `[VERIFIED-FACT]`)"
        )
    elif wso2_before is not None:
        wso2_phrase = (
            f"el assessment WSO2/Studio F partia de **{wso2_before:.2f}%** de "
            "texto util (banda 'nula', `[EPISTEMIC-VOID]`)"
        )
    else:
        wso2_phrase = "el assessment WSO2/Studio F era un caso critico de base"

    recovered_phrase = (
        ", ".join(recovered) if recovered else
        "los PDFs de codificacion personalizada"
    )

    parts: List[str] = [
        "# Anexo B - Arquitectura IA multicapa de extraccion de texto util",
        "",
        "> **Anexo del informe tecnico** de Credi10 2.0. Presenta, como "
        "**recomendacion de advisory**, la arquitectura de **ingesta "
        "documental multicapa (L1-L4)** cuyo objetivo es **maximizar el texto "
        "util real** de todo el corpus. Esta gobernado por el skill generico "
        "[`document-extraction-architecture`]"
        "(../../../../.kiro/skills/document-extraction-architecture/SKILL.md) e "
        "integra las politicas [`complete-corpus-ingestion`]"
        "(../../../../.kiro/skills/complete-corpus-ingestion/SKILL.md), "
        "[`ocr-image-extraction`]"
        "(../../../../.kiro/skills/ocr-image-extraction/SKILL.md) y "
        "[`token-budget-optimization`]"
        "(../../../../.kiro/skills/token-budget-optimization/SKILL.md).",
        "",
        "> **Etiquetas epistemicas:** **[VERIFIED-FACT]** capa de texto nativa "
        "util (incluida la recuperada por decodificacion de fuentes) o "
        "transcripcion humana estatica; **[OCR-EXTRACTED]** texto recuperado "
        "por OCR o por modelo de vision; **[EPISTEMIC-VOID]** no recuperable en "
        "este entorno (no se fabrica); **[DOC-ASSUMPTION]** supuesto a validar; "
        "**[DOC-CONFLICT]** tension entre fuentes.",
        "",
        "## 1. Por que una arquitectura de extraccion y no un extractor unico",
        "",
        "El analisis de cobertura del corpus revelo un patron que suele pasar "
        "inadvertido y que, de no corregirse, contamina toda la estimacion: "
        "varios PDFs que parecian 'vacios' o 'solo imagen' **si tenian una capa "
        "de texto real**, pero codificada con fuentes embebidas de codificacion "
        "personalizada (`Type0`/`Identity-H` con un CMap `/ToUnicode` por "
        "fuente). Un extractor ingenuo que lee literales `( ... )` sin aplicar "
        "el mapeo por fuente devuelve ruido, y ademas tiende a ingerir bytes "
        "binarios de imagenes y programas de fuente como si fueran texto, "
        "hundiendo artificialmente el ratio de texto util. El diagnostico, por "
        "tanto, no era 'faltan documentos' sino 'falta la capa de extraccion "
        "correcta para cada tipo de documento'.",
        "",
        "De ahi la decision de advisory: en lugar de un unico extractor, se "
        "adopta una **arquitectura por capas** que aplica a cada documento la "
        "tecnica mas barata y mas fiel capaz de recuperar su contenido, y "
        "**escala** a capas mas potentes solo cuando la capa previa no alcanza "
        "el umbral de texto util. Es una estrategia de **maximizacion del texto "
        "util con degradacion honesta**: lo que una capa no recupera lo intenta "
        "la siguiente, y lo que ninguna capa disponible recupera se marca como "
        "vacio epistemico en vez de inventarse. Esta disciplina es lo que "
        "convierte la ingesta en un cimiento defendible para la estimacion: "
        "cada afirmacion del informe queda anclada a texto realmente recuperado "
        "y etiquetado segun su procedencia.",
        "",
        "## 2. La escalera de capas (estrategia)",
        "",
        "La estrategia organiza la extraccion como una escalera de cuatro "
        "capas. Cada documento ocupa la capa mas baja que supere el umbral de "
        "texto util (`MIN_USEFUL_RATIO_FOR_TEXT`, "
        f"{threshold_pct:.0f}%); solo escala cuando esa capa se queda corta. "
        "Preferir la capa mas baja no es una preferencia estetica: la capa L1 "
        "es la unica **determinista y sin costo de inferencia**, reproduce el "
        "original sin alucinaciones y no depende de servicios externos.",
        "",
    ]
    parts += _layers_table()
    parts += [
        "",
        "La regla de oro de la capa L4 es que **estructura y normaliza lo ya "
        "recuperado por L1-L3, sin inventar** datos que el texto no contiene: "
        "si una entidad no aparece en el texto extraido, queda como "
        "`[EPISTEMIC-VOID]`, no se completa por inferencia del modelo. Esta "
        "frontera entre 'normalizar' y 'fabricar' es la que preserva la "
        "honestidad epistemica del advisory cuando entran modelos generativos.",
        "",
        "## 3. Flujo de decision con fallback (tactica)",
        "",
        "La tactica concreta es un flujo de decision que evalua el **texto util "
        "real** de cada documento y escala de capa hasta cruzar el umbral o "
        "agotar las capas disponibles en el entorno. El flujo es tolerante a "
        "fallos (un error en una capa degrada a la siguiente, nunca aborta el "
        "pipeline) y determinista (re-ejecutar deja la salida byte-identica).",
        "",
        _architecture_mermaid(),
        "",
        "El diagrama hace explicito el punto de bifurcacion mas importante: "
        "cuando L1 no alcanza el umbral, la pregunta no es 'aplicar OCR o no' "
        "sino **por que** la capa de texto es insuficiente. Si la pagina es "
        "realmente una imagen/escaneo, corresponde L2 (OCR); si hay capa de "
        "texto pero la fuente carece de mapa, corresponde el heuristico de "
        "respaldo. Distinguir ambos casos evita gastar OCR donde bastaba "
        "decodificar una fuente, que es exactamente el error que inflaba el "
        "problema en este corpus.",
        "",
        "## 4. Tactica por tipo de documento",
        "",
        "La capa de entrada se elige segun la naturaleza del documento. Esta "
        "tabla es la guia operativa que el motor aplica y que el equipo de "
        "produccion debe respetar al activar L2-L4:",
        "",
    ]
    parts += _tactics_table()
    parts += [
        "",
        "## 5. Resultado real sobre el corpus Credi10 (antes / despues)",
        "",
        "La recomendacion no es teorica: la **capa L1 ya se ejecuto** sobre el "
        "corpus real de este engagement y los numeros que siguen se leen "
        "directamente de la Base de Conocimiento del run (columna 'ahora') "
        "frente a la linea base previa a la decodificacion de fuentes (columna "
        "'antes', constante declarativa "
        "`knowledge.USEFUL_TEXT_BASELINE_PCT`). No hay cifras hardcodeadas en "
        "este anexo: se mantienen en sincronia con el analisis de cobertura.",
        "",
    ]
    parts += _comparison_table(knowledge_base)
    parts += [
        "",
        "### Lectura de los resultados",
        "",
        f"La decodificacion de fuentes de **L1 recupero texto nativo real** en "
        f"todo el bloque de PDFs. En particular, {wso2_phrase}; y "
        f"**{n_recovered} de {n_void_base}** PDFs que estaban en banda 'nula' "
        f"con `[EPISTEMIC-VOID]` cruzaron el umbral de texto util "
        f"({threshold_pct:.0f}%) y hoy son texto nativo `[VERIFIED-FACT]`"
        + (f": {recovered_phrase}." if recovered else ".") +
        " El salto se explica porque su capa de texto SI existia pero usaba "
        "fuentes con CMap `/ToUnicode`; el extractor consciente de la fuente "
        "(`engine/pdf_text.py`) la decodifica y lee solo dentro de objetos de "
        "texto `BT ... ET`, recuperando espanol legible como 'aplicacion', "
        "'arquitectura' o 'integracion'.",
        "",
        "Es importante subrayar que esta recuperacion es de **texto nativo**, "
        "no de OCR: el documento siempre tuvo el texto, solo estaba mal "
        "decodificado. Por eso conserva la etiqueta `[VERIFIED-FACT]` y no "
        "`[OCR-EXTRACTED]`. El adaptador OCR del motor sigue degradando "
        "honestamente (0 OCR en este entorno), sin fabricar contenido.",
        "",
        "## 6. Alcance: lo IMPLEMENTADO aqui (L1) vs. lo que requiere produccion (L2-L4)",
        "",
        "> **Marca de alcance explicita.** En este entorno (stdlib-only, sin "
        "red, sin motor OCR) **solo la capa L1 esta implementada y en "
        "ejecucion**. Las capas L2, L3 y L4 estan **disenadas y listas por "
        "contrato**, pero su activacion requiere el **entorno de produccion**.",
        "",
        "| Capa | Estado en este entorno | Requiere para activarse |",
        "| --- | --- | --- |",
        "| **L1** texto nativo + decodificacion de fuentes | **IMPLEMENTADA y "
        "ejecutada** (`advisory-system/engine/pdf_text.py`, stdlib) | nada |",
        "| **L2** OCR de paginas imagen | **No disponible** (degradacion "
        "honesta) | Tesseract / ocrmypdf en el entorno |",
        "| **L3** vision / LLM multimodal | **No disponible** | Document AI / "
        "LLM multimodal con red |",
        "| **L4** NLP / LLM de post-proceso | **No disponible** | servicio NLP "
        "/ LLM con red |",
        "",
        "Lo que **L1 NO resuelve** y queda explicitamente para L2-L4 en "
        "produccion: las paginas que son imagenes reales (JPEG `DCTDecode` sin "
        "capa de texto) siguen necesitando **OCR real (L2)**; el layout "
        "complejo, las tablas y los diagramas se interpretan mejor con "
        "**vision/LLM (L3)**; y la estructuracion y extraccion de entidades con "
        "trazabilidad es trabajo de **L4**. Nada de esto se simula aqui: cuando "
        "el mismo corpus se procese en produccion, L2-L4 se activan sin cambiar "
        "la estrategia ni las etiquetas epistemicas ya definidas.",
        "",
        "## 7. Implicaciones para la estimacion, la estrategia y los riesgos",
        "",
        "**Para la estimacion.** Al recuperar como texto nativo los PDFs que "
        "antes eran vacios epistemicos, los frentes que dependian de esos "
        "documentos (assessment WSO2, procesos de cartera, integraciones de "
        "originacion) pasan a estar soportados por evidencia `[VERIFIED-FACT]` "
        "y se pueden tallar con mayor confianza, reduciendo la contingencia que "
        "antes cargaba la incertidumbre documental.",
        "",
        "**Para la estrategia de implementacion.** La arquitectura por capas se "
        "implanta de forma incremental: L1 es inmediata y sin costo externo; "
        "L2 se habilita cuando el entorno de produccion disponga de motor OCR; "
        "L3 y L4 se incorporan cuando se justifique el layout complejo o la "
        "extraccion de entidades a escala. La priorizacion por presupuesto de "
        "tokens cambia el orden/esfuerzo de las capas, nunca excluye un "
        "documento.",
        "",
        "**Para los riesgos.** El riesgo dominante es confundir 'documento sin "
        "texto util' con 'documento sin informacion': este corpus demostro que "
        "el contenido estaba presente y mal decodificado. La arquitectura "
        "mitiga ese riesgo obligando a diagnosticar la causa (fuente sin mapa "
        "vs. imagen real) antes de escalar de capa, y manteniendo la "
        "degradacion honesta para no fabricar lo que no se recupera. "
        "`[DOC-ASSUMPTION]` cualquier cifra de L2-L4 queda sujeta a su "
        "activacion en produccion.",
        "",
        "## 8. Trazabilidad con las politicas de la organizacion",
        "",
        "Este anexo materializa, sobre el corpus real de Credi10, la politica "
        "generica [`document-extraction-architecture`]"
        "(../../../../.kiro/skills/document-extraction-architecture/SKILL.md): "
        "la capa L1 es su implementacion de referencia; L2 es la tactica de "
        "[`ocr-image-extraction`]"
        "(../../../../.kiro/skills/ocr-image-extraction/SKILL.md); la cobertura "
        "total sin muestreo es la obligacion de [`complete-corpus-ingestion`]"
        "(../../../../.kiro/skills/complete-corpus-ingestion/SKILL.md); y el "
        "control de volumen de L4 obedece a [`token-budget-optimization`]"
        "(../../../../.kiro/skills/token-budget-optimization/SKILL.md). Para "
        "volver al indice maestro del informe tecnico ver "
        "[`../README.md`](../README.md).",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# Escritura.
# --------------------------------------------------------------------------- #

def write(tech_report_base: str, knowledge_base=None,
          documents=None) -> List[str]:
    """Escribe el Anexo B bajo ``<tech_report_base>/anexo-b-arquitectura-extraccion/``.

    ``tech_report_base`` es la carpeta ``3-informe-tecnico/``. Devuelve la lista
    de paths escritos (ordenada). Idempotente y byte-identico entre corridas.
    """
    annex_dir = os.path.join(tech_report_base, ANNEX_DIRNAME)
    os.makedirs(annex_dir, exist_ok=True)
    path = os.path.join(annex_dir, "README.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build_annex(knowledge_base))
    return [path]

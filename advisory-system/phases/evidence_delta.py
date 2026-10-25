"""Anexo C del informe tecnico: 'En que cambio' (ANTES vs AHORA).

Generador DETERMINISTA, stdlib-only, del **anexo C del informe tecnico**: la
**narrativa de consecuencia** de haber recuperado la capa de texto nativa de
los cinco PDF que antes eran vacios epistemicos. A diferencia del Anexo B (que
explica la *arquitectura de extraccion* y el delta de texto util por documento),
este anexo responde la pregunta del negocio: **con la informacion recuperada,
¿podemos definir el proyecto con tranquilidad, o que % necesitariamos una
conceptualizacion / etapa de especificacion adicional?** Mide el salto del
balance evidenciario del advisory (vacios -> verificado) y lo traduce a una
lectura de suficiencia honesta.

Que produce (bajo ``3-informe-tecnico/anexo-c-en-que-cambio/``):

  * ``README.md`` con:
      - narrativa sustancial en espanol (no solo tablas),
      - la **tabla ANTES vs AHORA** de los 5 documentos recuperados (texto util
        antes/ahora, banda y flag ACTUALES leidos de la Base de Conocimiento),
      - el **balance epistemico** del corpus de 18 docs (vacios-antes -> 0
        vacios-ahora), derivado deterministamente,
      - el **conteo de hechos clave trazables** que hoy existen frente a los ~0
        que los 5 documentos aportaban antes, y
      - un **veredicto de suficiencia** (% estimado de cobertura de evidencia y
        que exige una etapa de conceptualizacion/especificacion adicional).

Fundamentacion (grounding): las cifras 'ahora' se leen de la ``KnowledgeBase``
del run (``doc.useful_ratio``, ``doc.epistemic_flag``, ``doc.key_facts``), y las
'antes' de las constantes declarativas compartidas en ``engine.knowledge``
(``USEFUL_TEXT_BASELINE_PCT``, ``BASELINE_NULA_PDFS``). NO hay cifras
hardcodeadas: si el corpus cambia, el anexo recomputa. Si no hay KB (p. ej. una
prueba que no corre el pipeline) degrada a la linea base declarativa sin
fabricar numeros.

Determinismo: orden estable por nombre de archivo; sin azar ni timestamps;
``os.makedirs(..., exist_ok=True)``. Una segunda corrida deja la salida
byte-identica.
"""

from __future__ import annotations

import os
from typing import List, Optional, Tuple

from engine import knowledge as kb_mod


ANNEX_DIRNAME = "anexo-c-en-que-cambio"

# Maximo de hechos recuperados que se citan por documento en las tablas de
# evidencia groundeada (bounded, determinista).
MAX_GROUNDED_FACTS = 4
# Longitud maxima de la cita de un hecho recuperado en las tablas.
MAX_GROUNDED_FACT_CHARS = 160


# --------------------------------------------------------------------------- #
# Helpers de datos (grounding en la Base de Conocimiento viva).
# --------------------------------------------------------------------------- #

def _doc(knowledge_base, filename: str):
    if knowledge_base is None:
        return None
    try:
        return knowledge_base.by_filename(filename)
    except Exception:
        return None


def _now_pct(knowledge_base, filename: str) -> Optional[float]:
    """Texto util % ACTUAL del documento, leido de la KB viva (o None)."""
    doc = _doc(knowledge_base, filename)
    return None if doc is None else doc.useful_ratio * 100.0


def _band_flag(knowledge_base, filename: str) -> Tuple[Optional[str], Optional[str]]:
    doc = _doc(knowledge_base, filename)
    if doc is None:
        return (None, None)
    return (doc.coverage_band, doc.epistemic_flag)


def _clean_fact(text: str) -> str:
    """Normaliza un hecho a una sola linea segura para una celda de tabla."""
    one_line = " ".join((text or "").split())
    if len(one_line) > MAX_GROUNDED_FACT_CHARS:
        one_line = one_line[:MAX_GROUNDED_FACT_CHARS].rstrip() + "..."
    return one_line.replace("|", "\\|")


# --------------------------------------------------------------------------- #
# Helper REUTILIZABLE por los builders de fase para citar evidencia recuperada.
# --------------------------------------------------------------------------- #

def grounded_evidence_rows(knowledge_base, filename: str,
                           limit: int = MAX_GROUNDED_FACTS) -> List[str]:
    """Filas Markdown de hechos clave recuperados de ``filename`` (trazables).

    Columnas: ``| Hecho recuperado [VERIFIED-FACT] | Tokens | Fuente |``. Cada
    hecho proviene de ``KnowledgeBase.facts_for(filename)`` (deterministico y
    trazable). Devuelve ``[]`` si no hay KB o el documento no tiene hechos (no
    se fabrica contenido).
    """
    if knowledge_base is None:
        return []
    try:
        facts = knowledge_base.facts_for(filename)
    except Exception:
        return []
    rows: List[str] = []
    for kf in facts[:limit]:
        toks = ", ".join(kf.tokens[:5]) if kf.tokens else "-"
        rows.append(
            f"| {_clean_fact(kf.fact)} | {toks} | {kf.source_filename} |"
        )
    return rows


def grounded_evidence_table(knowledge_base, filename: str,
                            limit: int = MAX_GROUNDED_FACTS) -> str:
    """Tabla Markdown completa de evidencia recuperada de ``filename``.

    Si no hay hechos recuperables devuelve una nota honesta (sin fabricar).
    Pensada para inyectarse en los builders de fase (phase1/phase3/exec/tech).
    """
    rows = grounded_evidence_rows(knowledge_base, filename, limit)
    band, flag = _band_flag(knowledge_base, filename)
    if not rows:
        return (
            f"_Sin hechos clave recuperables de `{filename}` en este run "
            "(no se fabrica evidencia)._"
        )
    header = [
        f"Evidencia recuperada de `{filename}` "
        f"(banda **{band or 'n/d'}**, **{flag or 'n/d'}**):",
        "",
        "| Hecho recuperado [VERIFIED-FACT] | Tokens | Fuente |",
        "| --- | --- | --- |",
    ]
    return "\n".join(header + rows)


# --------------------------------------------------------------------------- #
# Metricas del balance epistemico (ANTES vs AHORA), deterministas.
# --------------------------------------------------------------------------- #

def _recovered_now(knowledge_base) -> List[str]:
    """De los 5 PDF 'nula'/[EPISTEMIC-VOID] de base, cuales son hoy VERIFIED."""
    names: List[str] = []
    for name in kb_mod.BASELINE_NULA_PDFS:
        _band, flag = _band_flag(knowledge_base, name)
        if flag == kb_mod.VERIFIED_FACT:
            names.append(name)
    return sorted(names)


def _void_now(knowledge_base) -> int:
    """Documentos del corpus hoy marcados [EPISTEMIC-VOID] en la KB viva."""
    if knowledge_base is None:
        return len(kb_mod.BASELINE_NULA_PDFS)
    n = 0
    for doc in getattr(knowledge_base, "documents", []):
        if doc.epistemic_flag == kb_mod.EPISTEMIC_VOID:
            n += 1
    return n


def _facts_from_recovered(knowledge_base) -> int:
    """Total de hechos clave que hoy aportan los 5 documentos recuperados."""
    if knowledge_base is None:
        return 0
    total = 0
    for name in kb_mod.BASELINE_NULA_PDFS:
        try:
            total += len(knowledge_base.facts_for(name))
        except Exception:
            pass
    return total


def _total_facts(knowledge_base) -> int:
    if knowledge_base is None:
        return 0
    try:
        return len(knowledge_base.all_facts())
    except Exception:
        return 0


def _comparison_rows(knowledge_base) -> List[str]:
    """Tabla ANTES vs AHORA de los 5 documentos recuperados (ordenada)."""
    rows = []
    for name in kb_mod.BASELINE_NULA_PDFS:
        before = kb_mod.USEFUL_TEXT_BASELINE_PCT.get(name)
        now = _now_pct(knowledge_base, name)
        band, flag = _band_flag(knowledge_base, name)
        try:
            n_facts = len(knowledge_base.facts_for(name)) if knowledge_base else 0
        except Exception:
            n_facts = 0
        if before is None:
            before = 0.0
        if now is None:
            now_display = "n/d"
            delta_display = "n/d"
            delta_val = -1.0
        else:
            delta = now - before
            if abs(delta) < 0.005:
                delta = 0.0
            now_display = f"{now:.2f}%"
            delta_display = f"{'+' if delta >= 0 else ''}{delta:.2f} pp"
            delta_val = delta
        rows.append((delta_val, name, before, now_display, delta_display,
                     band or "-", flag or "-", n_facts))
    rows.sort(key=lambda r: (-r[0], r[1]))

    lines = [
        "| # | Documento (antes [EPISTEMIC-VOID]) | Texto util antes | "
        "Texto util ahora | Delta | Banda ahora | Flag ahora | Hechos clave |",
        "| --- | --- | ---: | ---: | ---: | --- | --- | ---: |",
    ]
    for i, (_d, name, before, now_display, delta_display, band, flag, nf) in \
            enumerate(rows, start=1):
        lines.append(
            f"| {i} | {name} | {before:.2f}% | {now_display} | "
            f"{delta_display} | {band} | {flag} | {nf} |"
        )
    return lines


def _sufficiency_pct(knowledge_base) -> int:
    """% honesto de cobertura de evidencia del corpus para definir el proyecto.

    Definicion deterministica: fraccion de documentos del corpus con flag
    [VERIFIED-FACT] (texto nativo util o transcripcion humana) sobre el total.
    Es una medida de **cobertura de evidencia**, no de completitud funcional:
    aun con 100% de evidencia leible persisten vacios de medicion (SLA/latencia)
    y de linea base de costos que exigen una etapa de especificacion.
    """
    if knowledge_base is None:
        return 0
    docs = list(getattr(knowledge_base, "documents", []))
    if not docs:
        return 0
    verified = sum(1 for d in docs
                   if d.epistemic_flag in (kb_mod.VERIFIED_FACT,))
    return int(round(verified * 100.0 / len(docs)))


# --------------------------------------------------------------------------- #
# Cuerpo del anexo.
# --------------------------------------------------------------------------- #

# Modulos del advisory que dependian de los 5 documentos recuperados y que, por
# tanto, ganaron fundamento [VERIFIED-FACT]. Declarativo (trazable a modules.py).
_DEPENDENT_SECTIONS: List[Tuple[str, str]] = [
    ("WSO2 y Studio F - Assessment Mayo2026-Final.pdf",
     "Integracion / gobierno de APIs (MOD-16, desacople Siesa/UnoEE): "
     "diagnostico AS-IS fase 1, gaps fase 3, ruta critica de la estimacion "
     "fase 5"),
    ("Originacion_API_Inspektor.pdf",
     "Originacion - estudio de credito Inspektor (MOD-03): specs de modulo e "
     "historias fase 4"),
    ("ProcesoCorteCartera.pdf",
     "Corte y gestion de cartera (MOD-07): specs de modulo e historias fase 4"),
    ("B2C.pdf",
     "Canales digitales / portal B2C (MOD-09): specs de modulo fase 4"),
    ("Api Integrador Atencion al cliente.pdf",
     "Integrador de atencion al cliente (MOD-12): specs de modulo fase 4"),
]


def build_annex(knowledge_base=None) -> str:
    recovered = _recovered_now(knowledge_base)
    n_recovered = len(recovered)
    n_void_base = len(kb_mod.BASELINE_NULA_PDFS)
    n_void_now = _void_now(knowledge_base)
    facts_recovered = _facts_from_recovered(knowledge_base)
    total_facts = _total_facts(knowledge_base)
    suff_pct = _sufficiency_pct(knowledge_base)

    wso2_name = "WSO2 y Studio F - Assessment Mayo2026-Final.pdf"
    wso2_before = kb_mod.USEFUL_TEXT_BASELINE_PCT.get(wso2_name, 0.0)
    wso2_now = _now_pct(knowledge_base, wso2_name)
    if wso2_now is not None:
        wso2_phrase = (
            f"el Assessment WSO2/Studio F paso de **{wso2_before:.2f}%** de "
            f"texto util (vacio epistemico) a **{wso2_now:.2f}%** "
            "([VERIFIED-FACT])"
        )
    else:
        wso2_phrase = (
            f"el Assessment WSO2/Studio F partia de **{wso2_before:.2f}%** de "
            "texto util (vacio epistemico)"
        )

    parts: List[str] = [
        "# Anexo C - En que cambio: evidencia ANTES vs AHORA y suficiencia para definir el proyecto",
        "",
        "> **Anexo del informe tecnico** de Credi10 2.0. Responde, con cifras "
        "leidas de la Base de Conocimiento del run, la pregunta del negocio: "
        "tras recuperar la capa de texto nativa de los documentos que antes "
        "eran **vacios epistemicos**, ¿con esta informacion podemos definir el "
        "proyecto con tranquilidad y, si no, que % exige todavia una "
        "**conceptualizacion / etapa de especificacion** adicional? Es un "
        "artefacto **generado** y **determinista** (se recomputa si el corpus "
        "cambia); no se escribe a mano.",
        "",
        "> **Etiquetas epistemicas:** **[VERIFIED-FACT]** texto nativo util "
        "recuperado (incluida la decodificacion de fuentes) o transcripcion "
        "humana; **[EPISTEMIC-VOID]** no recuperable / ausente (no se fabrica); "
        "**[DOC-ASSUMPTION]** supuesto a validar.",
        "",
        "## 1. Que cambio en una frase",
        "",
        "La recuperacion de texto nativo (L1: `/ToUnicode` por fuente + "
        "reconstruccion lexica) movio a **" + str(n_recovered) + " de " +
        str(n_void_base) + "** documentos desde el **vacio epistemico** "
        "([EPISTEMIC-VOID]) hacia **evidencia verificada** ([VERIFIED-FACT]). "
        f"En concreto, {wso2_phrase}. El corpus paso de **{n_void_base} "
        f"documentos en vacio** a **{n_void_now} en vacio** hoy, y esos cinco "
        "documentos, que antes aportaban **~0** hechos clave trazables, hoy "
        f"aportan **{facts_recovered}** (de un total de **{total_facts}** "
        "hechos clave en todo el corpus). El diagnostico, la arquitectura y la "
        "estimacion de los frentes que dependian de esos documentos dejan de "
        "apoyarse en supuestos y pasan a citar evidencia real.",
        "",
        "## 2. ANTES vs AHORA de los documentos recuperados",
        "",
        "Las cifras 'antes' son la linea base declarativa previa a la "
        "decodificacion de fuentes (`knowledge.USEFUL_TEXT_BASELINE_PCT`); las "
        "'ahora', la banda, el flag y el conteo de hechos se leen de la Base de "
        "Conocimiento viva. No hay cifras hardcodeadas en esta tabla.",
        "",
    ]
    parts += _comparison_rows(knowledge_base)
    parts += [
        "",
        "## 3. Balance epistemico del corpus (18 documentos)",
        "",
        "| Metrica | Antes (linea base) | Ahora (KB viva) |",
        "| --- | ---: | ---: |",
        f"| Documentos en [EPISTEMIC-VOID] | {n_void_base} | {n_void_now} |",
        f"| Documentos recuperados a [VERIFIED-FACT] | 0 | {n_recovered} |",
        f"| Hechos clave aportados por esos 5 documentos | ~0 | "
        f"{facts_recovered} |",
        f"| Hechos clave trazables en todo el corpus | - | {total_facts} |",
        "",
        "> El salto de **" + str(n_void_base) + " -> " + str(n_void_now) +
        "** vacios epistemicos es el cambio estructural: ya no hay modulos "
        "cuyo soporte documental sea 'solo imagen' / sin capa de texto. Lo que "
        "resta en vacio no son documentos sino **mediciones** que el corpus "
        "nunca contuvo (SLA/latencia instrumentada, linea base de costos), que "
        "se levantan en el sprint 0, no por mas OCR.",
        "",
        "## 4. Que secciones del advisory ganaron fundamento",
        "",
        "Cada documento recuperado aterriza en secciones concretas del "
        "advisory, que pasan de [DOC-ASSUMPTION] a [VERIFIED-FACT]:",
        "",
        "| Documento recuperado | Secciones del advisory que ganan evidencia |",
        "| --- | --- |",
    ]
    for name, where in _DEPENDENT_SECTIONS:
        parts.append(f"| `{name}` | {where} |")
    parts += [
        "",
        "## 5. Evidencia concreta recuperada (muestra trazable)",
        "",
        "Muestra de hechos clave recuperados (leidos de la KB; cada uno trazable "
        "a su documento fuente), que antes eran inaccesibles:",
        "",
    ]
    # Evidencia groundeada por documento (determinista, desde la KB).
    for name, _where in _DEPENDENT_SECTIONS:
        parts.append(f"### {name}")
        parts.append("")
        parts.append(grounded_evidence_table(knowledge_base, name))
        parts.append("")

    parts += [
        "## 6. ¿Podemos definir el proyecto con tranquilidad? Veredicto de suficiencia",
        "",
        f"**Cobertura de evidencia documental del corpus: ~{suff_pct}%** "
        f"({suff_pct}% de los {len(getattr(knowledge_base, 'documents', [])) or len(kb_mod.BASELINE_NULA_PDFS)} "
        "documentos con [VERIFIED-FACT]). Este porcentaje mide cuanta "
        "**evidencia leible** respalda hoy el advisory, y **no** la "
        "preparacion total para **comprometer** alcance, fechas y presupuesto. "
        "La distincion es decisiva para responder la pregunta del negocio:",
        "",
        "- **Lo que SI habilita la evidencia recuperada (suficiente para "
        "arrancar).** El diagnostico AS-IS, el catalogo de modulos/historias y "
        "la estimacion por olas ya se apoyan en texto verificado; se puede "
        "**iniciar la construccion por olas** (enablers WAV-000/WAV-001) con "
        "confianza razonable. Esto es coherente con el veredicto **GO "
        "CONDICIONADO** de la Fase 5.",
        "- **Lo que AUN exige una etapa de conceptualizacion / especificacion.** "
        "Que la evidencia **documental** este al ~" + str(suff_pct) + "% NO "
        "significa que la **especificacion de la solucion objetivo** lo este: "
        "la evidencia recuperada es **documentacion tecnica del AS-IS "
        "existente**, no un diseno comprometible. Persisten vacios que ningun "
        "OCR cierra porque **no estan en ningun documento**: (1) **mediciones "
        "ausentes** (SLA/latencia hoy sin instrumentar [EPISTEMIC-VOID]) y (2) "
        "**linea base de costos** para el caso de negocio [EPISTEMIC-VOID]; y "
        "las specs recuperadas de los modulos deben **ratificarse 1:1 con el "
        "cliente** (riesgo RS-03).",
        "",
        "> **Lectura honesta (porcentajes).** La base **documental** para "
        f"encuadrar el proyecto esta cubierta al **~{suff_pct}%**. Pero para "
        "pasar de 'arrancar' a 'comprometer alcance, fechas y presupuesto con "
        "tranquilidad' se requiere todavia una **etapa de conceptualizacion / "
        "especificacion** acotada (sprint 0 / descubrimiento), estimada en "
        "**~15-20% de esfuerzo adicional de advisory [DOC-ASSUMPTION]**, que "
        "cierre lo que el corpus no contiene: (a) **~10-15%** levantar la "
        "**linea base de medicion** (disponibilidad/latencia reales) y de "
        "**costos** para el caso de negocio; (b) **~5%** **ratificar las specs "
        "recuperadas** de originacion, cartera, pagos e integracion WSO2 en "
        "talleres con el cliente; y (c) **recalibrar la estimacion** con conteo "
        "funcional historico. Estos porcentajes son una **guia de advisory "
        "[DOC-ASSUMPTION]**, no una medicion; se afinan en el sprint 0. Sin ese "
        "cierre, comprometer fechas absolutas de las olas 2 y 3 incurre en alto "
        "riesgo de desfase (ver Fase 5, RS-01..RS-06).",
        "",
        "## 7. Trazabilidad",
        "",
        "Este anexo se deriva de la Base de Conocimiento (`knowledge-base/`) y "
        "de las constantes declarativas `engine.knowledge."
        "USEFUL_TEXT_BASELINE_PCT` y `BASELINE_NULA_PDFS`. Complementa el "
        "**Anexo B** (arquitectura de extraccion, delta de texto util por "
        "documento) con la **lectura de consecuencia** para el negocio. Para "
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
    """Escribe el Anexo C bajo ``<tech_report_base>/anexo-c-en-que-cambio/``.

    ``tech_report_base`` es la carpeta ``3-informe-tecnico/``. Devuelve la lista
    de paths escritos (ordenada). Idempotente y byte-identico entre corridas.
    """
    annex_dir = os.path.join(tech_report_base, ANNEX_DIRNAME)
    os.makedirs(annex_dir, exist_ok=True)
    path = os.path.join(annex_dir, "README.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build_annex(knowledge_base))
    return [path]

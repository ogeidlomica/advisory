"""Anexo A - Trazabilidad de requisitos del cliente (FEAT-002).

Generador DETERMINISTA, stdlib-only, del **anexo de trazabilidad de requisitos**
del informe tecnico. Gobernado por el skill generico ``requirements-traceability``.

Que produce (bajo ``3-informe-tecnico/anexo-a-trazabilidad-requisitos/``):

  * un **checklist marcable** de "que desarrollar / que pide el cliente"
    (``- [x]`` Cubierto / ``- [~]`` Parcial / ``- [ ]`` Pendiente), y
  * una **tabla de trazabilidad punto a punto** con columnas EXACTAS:
    ``ID | Solicitud del cliente | Cita al documento fuente |
    Donde se responde (fase/seccion/entregable) | Estado | Evidencia/Nota``.

Principio (ver skill): **toda solicitud del cliente presente en el corpus se
responde punto a punto, con cita al documento fuente**; si el corpus no permite
responder una solicitud (documento sin texto util / OCR pendiente) se marca
**Pendiente** con ``[EPISTEMIC-VOID]`` y una nota honesta. Nada se fabrica.

DINAMISMO (no hardcodeo para Credi10): las solicitudes se **extraen del corpus**
con heuristicas deterministas. Se prioriza el documento ``primary`` tipo RFP por
heuristica de rol/nombre y se complementa con el resto. Dentro de cada documento
se localizan **anclas de seccion** portadoras de requisitos (objetivos, alcance,
requisitos, informes, evaluacion, indicadores de retorno) y, como respaldo
generico, numerales/vinetas. Si el corpus es de otro cliente sin esas secciones,
la extraccion degrada a la deteccion generica. El modulo es llamable
directamente con una ``KnowledgeBase`` o una lista de ``Document`` para habilitar
pruebas sobre un corpus sintetico.

Determinismo: orden estable por documento y por posicion; sin azar ni
timestamps; una segunda corrida deja la salida byte-identica.
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple


# --------------------------------------------------------------------------- #
# Perillas de politica (declarativas, recalibrables)
# --------------------------------------------------------------------------- #

ANNEX_DIRNAME = "anexo-a-trazabilidad-requisitos"

# Longitud maxima (caracteres) de la cita fiel de una solicitud.
MAX_REQUEST_CHARS = 220
# Ventana de texto original (caracteres) que se inspecciona tras un ancla.
_ANCHOR_WINDOW = 320

# Anclas de seccion portadoras de requisitos. Cada ancla define:
#   key      -> forma NORMALIZADA (sin espacios, sin acentos, minuscula) que se
#               busca en el texto defragmentado del documento,
#   label    -> etiqueta legible de la seccion para la cita,
#   kind     -> tipo de solicitud (dirige el mapeo keyword -> entry point).
# Son SEMILLAS para robustez sobre RFPs estandar; si no aparecen en el corpus de
# otro cliente, la extraccion usa la deteccion generica de numerales/vinetas.
SECTION_ANCHORS: List[Tuple[str, str, str]] = [
    ("objetivogeneral", "Objetivo general", "objetivos"),
    ("objetivosespecificos", "Objetivos especificos", "objetivos"),
    ("alcancedelproyecto", "Alcance del proyecto", "alcance"),
    ("alcance", "Alcance", "alcance"),
    ("assessmentdearquitectura", "Assessment de arquitectura actual",
     "alcance"),
    ("evaluaciontecnologica", "Evaluacion tecnologica", "tecnologia"),
    ("evaluaciondebasesdedatos", "Evaluacion de bases de datos", "datos"),
    ("evaluaciondeintegraciones", "Evaluacion de integraciones",
     "integraciones"),
    ("arquitecturaobjetivo", "Arquitectura objetivo", "arquitectura"),
    ("requerimientosfuncionales", "Requerimientos funcionales", "funcional"),
    ("requerimientosdelaoperacion", "Requerimientos de la operacion",
     "operacion"),
    ("requerimientostecnicos", "Requerimientos tecnicos", "tecnico"),
    ("metodosdeintegracion", "Metodos de integracion", "integraciones"),
    ("informesrequeridos", "Informes requeridos", "informes"),
    ("indicadorderetorno", "Indicadores de retorno", "indicadores"),
    ("indicadoresderetorno", "Indicadores de retorno", "indicadores"),
    ("evaluaciondelaspropuestas", "Evaluacion de las propuestas",
     "evaluacion"),
    ("criteriosdeevaluacion", "Criterios de evaluacion", "evaluacion"),
]

# Mapeo determinista tipo-de-solicitud -> donde la responde el advisory. La
# primera columna es el ``kind`` del ancla (o inferido de palabras clave); la
# segunda es el texto de "Donde se responde".
KEYWORD_ENTRY_POINTS: Dict[str, str] = {
    "objetivos": "Fase 1 contexto-negocio + Fase 6 caso de negocio "
                 "(01-contexto-as-is.md, 06-caso-de-negocio.md)",
    "alcance": "Fase 0 higiene epistemica + Fase 1 AS-IS "
               "(00-higiene-epistemica.md, 01-contexto-as-is.md)",
    "tecnologia": "Fase 1 deuda tecnica + Fase 2 estado del arte "
                  "(01-contexto-as-is.md, 02-estado-del-arte.md)",
    "datos": "Fase 1 ecosistema (datos) + Fase 4 modelo de datos y contratos "
             "(01-contexto-as-is.md, 04-diseno-to-be.md)",
    "integraciones": "Fase 1 ecosistema + Fase 4 contratos (OpenAPI/AsyncAPI) "
                     "(01-contexto-as-is.md, 04-diseno-to-be.md)",
    "arquitectura": "Fase 4 diseno TO-BE: C4 + ADRs "
                    "(04-diseno-to-be.md, to-be/)",
    "funcional": "Fase 4 catalogo de historias + modelo de datos "
                 "(04b-catalogo-historias.md, 04-diseno-to-be.md)",
    "operacion": "Fase 4 UX y pruebas + Fase 5 RAID "
                 "(04-diseno-to-be.md, 05-roadmap-estimacion-raid.md)",
    "tecnico": "Fase 4 diseno TO-BE + ADRs "
               "(04-diseno-to-be.md, to-be/)",
    "informes": "Los 3 informes del engagement + dossier TO-BE "
                "(1-propuesta-comercial.md, 2-reporte-gerencial.md, "
                "3-informe-tecnico/, to-be/)",
    "indicadores": "Fase 6 value-driver-tree + modelo financiero "
                   "(06-caso-de-negocio.md)",
    "evaluacion": "Fase 5 roadmap/estimacion + Fase 6 caso de negocio "
                  "(05-roadmap-estimacion-raid.md, 06-caso-de-negocio.md)",
    "roadmap": "Fase 5 roadmap, estimacion y RAID "
               "(05-roadmap-estimacion-raid.md)",
    "generico": "Fase 1 AS-IS + Fase 4 diseno TO-BE "
                "(01-contexto-as-is.md, 04-diseno-to-be.md)",
}

# Palabras clave (normalizadas) -> kind, para inferir el mapeo cuando una
# solicitud se extrae por deteccion generica (sin ancla de seccion explicita).
_GENERIC_KEYWORDS: List[Tuple[str, str]] = [
    ("objetivo", "objetivos"),
    ("alcance", "alcance"),
    ("integracion", "integraciones"),
    ("basesdedatos", "datos"),
    ("basededatos", "datos"),
    ("arquitectura", "arquitectura"),
    ("informe", "informes"),
    ("entregable", "informes"),
    ("indicador", "indicadores"),
    ("roadmap", "roadmap"),
    ("estimacion", "roadmap"),
    ("riesgo", "roadmap"),
    ("evaluacion", "evaluacion"),
    ("funcional", "funcional"),
    ("operacion", "operacion"),
    ("tecnolog", "tecnologia"),
    ("seguridad", "tecnico"),
    ("requisito", "tecnico"),
    ("requerimiento", "tecnico"),
]

# Heuristica de documento tipo RFP (solicitud de oferta) por nombre.
_RFP_NAME_HINTS = ("rfp", "solicitud", "oferta", "pliego", "terminos",
                   "request for proposal", "tdr")

# Etiquetas epistemicas.
VERIFIED_FACT = "[VERIFIED-FACT]"
OCR_EXTRACTED = "[OCR-EXTRACTED]"
EPISTEMIC_VOID = "[EPISTEMIC-VOID]"


# --------------------------------------------------------------------------- #
# Modelo de una solicitud extraida
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Requirement:
    """Una solicitud del cliente extraida del corpus (determinista)."""

    req_id: str                 # REQ-NNN, estable en orden de documento
    request: str                # cita fiel acotada
    source_filename: str        # documento fuente
    source_section: str         # seccion/numeral cuando se recupera, o ""
    kind: str                   # tipo de solicitud (dirige el mapeo)
    where: str                  # donde se responde (fase/seccion/entregable)
    status: str                 # 'Cubierto' | 'Parcial' | 'Pendiente'
    epistemic_tag: str          # etiqueta epistemica honesta
    note: str                   # evidencia / nota

    @property
    def citation(self) -> str:
        if self.source_section:
            return f"{self.source_filename} - {self.source_section}"
        return self.source_filename


# --------------------------------------------------------------------------- #
# Normalizacion robusta a la fragmentacion del PDF
# --------------------------------------------------------------------------- #

def _strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def _normalize_name(name: str) -> str:
    return _strip_accents(name).lower()


def _despace(text: str) -> Tuple[str, List[int]]:
    """Return (despaced-normalized text, index map to the original text).

    The despaced text lowercases, drops whitespace and strips accents so that
    heavily fragmented PDF layers (``E va lu ac ión``) still match the anchors.
    The index map ties each despaced char back to its original position.
    """
    chars: List[str] = []
    idxmap: List[int] = []
    for i, ch in enumerate(text):
        if ch.isspace():
            continue
        chars.append(ch.lower())
        idxmap.append(i)
    despaced = _strip_accents("".join(chars))
    # NFD may change length; guard by rebuilding a 1:1 map defensively.
    if len(despaced) != len(idxmap):
        # Fallback: rebuild char-by-char preserving a stable, bounded mapping.
        chars2: List[str] = []
        idx2: List[int] = []
        for i, ch in enumerate(text):
            if ch.isspace():
                continue
            norm = _strip_accents(ch.lower())
            for c in norm:
                chars2.append(c)
                idx2.append(i)
        return "".join(chars2), idx2
    return despaced, idxmap


def _clean_excerpt(text: str, limit: int = MAX_REQUEST_CHARS) -> str:
    """Collapse whitespace and bound an excerpt to a faithful, legible length."""
    collapsed = re.sub(r"\s+", " ", text).strip()
    if len(collapsed) > limit:
        collapsed = collapsed[:limit].rstrip() + "..."
    # Escape pipes so table cells stay well-formed.
    return collapsed.replace("|", "\\|")


# --------------------------------------------------------------------------- #
# Extraccion de solicitudes por documento
# --------------------------------------------------------------------------- #

def _document_text(doc) -> str:
    kind = getattr(doc, "kind", "pdf")
    if kind == "png":
        return getattr(doc, "description", "") or ""
    return getattr(doc, "extracted_text", "") or ""


def _looks_like_rfp(doc) -> bool:
    name = _normalize_name(getattr(doc, "filename", ""))
    return any(h in name for h in _RFP_NAME_HINTS)


def _doc_sort_key(doc) -> Tuple[int, str]:
    """Order: RFP-like primary first, then other primary, then the rest.

    Within each bucket, stable by lowercased filename. Deterministic.
    """
    name = _normalize_name(getattr(doc, "filename", ""))
    is_rfp = _looks_like_rfp(doc)
    role = getattr(doc, "role", "secondary")
    if is_rfp:
        bucket = 0
    elif role == "primary":
        bucket = 1
    else:
        bucket = 2
    return (bucket, name)


def _has_useful_text(doc) -> bool:
    """True when the document carries usable text per FEAT-001 signals."""
    flag = getattr(doc, "epistemic_flag", "")
    if flag in (VERIFIED_FACT, OCR_EXTRACTED):
        return True
    if flag == EPISTEMIC_VOID:
        return False
    # Fallback for plain Document lists not enriched: use useful_ratio.
    return getattr(doc, "useful_ratio", 0.0) > 0.0


def _infer_kind(snippet_despaced: str) -> str:
    for kw, kind in _GENERIC_KEYWORDS:
        if kw in snippet_despaced:
            return kind
    return "generico"


def _status_for(doc, kind: str) -> Tuple[str, str, str]:
    """Return (status, epistemic_tag, note) honestly from FEAT-001 signals."""
    flag = getattr(doc, "epistemic_flag", "")
    method = getattr(doc, "ingestion_method", "") or ""
    if flag == OCR_EXTRACTED:
        return ("Parcial", OCR_EXTRACTED,
                "Solicitud derivada de texto recuperado via OCR; validar la "
                "transcripcion antes de comprometer alcance.")
    if not _has_useful_text(doc):
        pending = ("OCR pendiente" in method)
        reason = ("documento basado en imagen, OCR pendiente en este entorno"
                  if pending else "sin texto util real en el corpus")
        return ("Pendiente", EPISTEMIC_VOID,
                f"El documento fuente no aporta texto util ({reason}); la "
                "solicitud no puede responderse sin recuperar su contenido. No "
                "se fabrica cobertura.")
    where = KEYWORD_ENTRY_POINTS.get(kind, KEYWORD_ENTRY_POINTS["generico"])
    # A clear entry point + useful text => Cubierto; generic mapping => Parcial.
    if kind in ("generico",):
        return ("Parcial", VERIFIED_FACT,
                "Solicitud abordable por el advisory; el mapeo es generico y se "
                "afina al cerrar los deltas de elicitacion.")
    return ("Cubierto", VERIFIED_FACT,
            f"Respondida por {where}.")


def _extract_from_anchors(doc, text: str) -> List[Tuple[str, str, str]]:
    """Return [(request_excerpt, section_label, kind)] for matched anchors.

    Deterministic: anchors are scanned in document (text) order of their first
    occurrence, de-duplicated by label.
    """
    despaced, idxmap = _despace(text)
    if not despaced:
        return []
    found: List[Tuple[int, str, str, str]] = []
    seen_labels: set = set()
    for key, label, kind in SECTION_ANCHORS:
        pos = despaced.find(key)
        if pos < 0 or label in seen_labels:
            continue
        seen_labels.add(label)
        orig = idxmap[pos] if pos < len(idxmap) else 0
        window = text[orig:orig + _ANCHOR_WINDOW]
        excerpt = _clean_excerpt(window)
        if excerpt:
            found.append((orig, excerpt, label, kind))
    found.sort(key=lambda t: t[0])
    return [(e, lbl, kind) for _o, e, lbl, kind in found]


def _extract_generic(doc, text: str,
                     limit: int = 12) -> List[Tuple[str, str, str]]:
    """Fallback: detect numbered items as requests (corpus-agnostic).

    Used when no section anchors match (another client's corpus). Picks numbered
    markers like ``1.`` / ``1.1`` / ``2.3`` in text order, bounded by ``limit``.
    """
    results: List[Tuple[str, str, str]] = []
    # Numerals possibly fragmented by spaces: ``1 . 1`` -> normalize first.
    collapsed = re.sub(r"\s+", " ", text)
    for m in re.finditer(r"(?<![\d.])(\d{1,2}(?:\.\d{1,2}){0,2})\.?\s+(\S.{20,})",
                         collapsed):
        numeral = m.group(1)
        body = m.group(2)
        excerpt = _clean_excerpt(body)
        despaced = _strip_accents(re.sub(r"\s+", "", body).lower())
        kind = _infer_kind(despaced)
        results.append((excerpt, f"Numeral {numeral}", kind))
        if len(results) >= limit:
            break
    return results


def extract_requirements(documents: Sequence) -> List[Requirement]:
    """Extract client requests from the corpus. Deterministic and dynamic.

    Accepts a list of enriched ``Document`` objects (or anything exposing
    ``filename``, ``extracted_text``/``description``, ``epistemic_flag``,
    ``ingestion_method``, ``role``, ``kind``). Prioritises RFP-like primary docs
    and complements with the rest. Returns a list of :class:`Requirement` with
    stable ``REQ-NNN`` IDs in document order.
    """
    ordered = sorted(documents, key=_doc_sort_key)
    reqs: List[Requirement] = []
    counter = 0
    for doc in ordered:
        text = _document_text(doc)
        pairs = _extract_from_anchors(doc, text)
        if not pairs:
            pairs = _extract_generic(doc, text)
        if not pairs and not _has_useful_text(doc):
            # Honest: a document with no useful text and no detectable requests
            # is still recorded as a Pendiente entry so coverage stays truthful.
            counter += 1
            status, tag, note = _status_for(doc, "generico")
            reqs.append(Requirement(
                req_id=f"REQ-{counter:03d}",
                request="(Documento sin texto util: solicitudes no recuperables "
                        "en este entorno)",
                source_filename=getattr(doc, "filename", "?"),
                source_section="",
                kind="generico",
                where=KEYWORD_ENTRY_POINTS["generico"],
                status=status, epistemic_tag=tag, note=note,
            ))
            continue
        for excerpt, label, kind in pairs:
            counter += 1
            status, tag, note = _status_for(doc, kind)
            where = KEYWORD_ENTRY_POINTS.get(
                kind, KEYWORD_ENTRY_POINTS["generico"])
            reqs.append(Requirement(
                req_id=f"REQ-{counter:03d}",
                request=excerpt,
                source_filename=getattr(doc, "filename", "?"),
                source_section=label,
                kind=kind,
                where=where,
                status=status,
                epistemic_tag=tag,
                note=note,
            ))
    return reqs


# --------------------------------------------------------------------------- #
# Render del anexo
# --------------------------------------------------------------------------- #

_CHECK_SYMBOL = {"Cubierto": "x", "Parcial": "~", "Pendiente": " "}


def _status_counts(reqs: Sequence[Requirement]) -> Dict[str, int]:
    counts = {"Cubierto": 0, "Parcial": 0, "Pendiente": 0}
    for r in reqs:
        counts[r.status] = counts.get(r.status, 0) + 1
    return counts


def _epistemic_note() -> str:
    return (
        "> **Etiquetas epistemicas:** **[VERIFIED-FACT]** solicitud derivada de "
        "capa de texto util verificada; **[OCR-EXTRACTED]** derivada de texto "
        "recuperado via OCR; **[DOC-ASSUMPTION]** supuesto a validar; "
        "**[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** el "
        "corpus no permite derivar/responder (OCR pendiente). No se fabrica "
        "cobertura."
    )


def _status_mermaid(counts: Dict[str, int]) -> str:
    return (
        "```mermaid\n"
        "pie showData\n"
        '    title Cobertura de solicitudes por estado\n'
        f'    "Cubierto" : {counts["Cubierto"]}\n'
        f'    "Parcial" : {counts["Parcial"]}\n'
        f'    "Pendiente" : {counts["Pendiente"]}\n'
        "```\n"
    )


def build_annex_readme(reqs: Sequence[Requirement],
                       total_docs: Optional[int] = None) -> str:
    """Render the annex README with BOTH the checklist and the table."""
    counts = _status_counts(reqs)
    n = len(reqs)
    docs_line = (f" sobre un corpus de **{total_docs}** documentos"
                 if total_docs is not None else "")
    parts: List[str] = [
        "# Anexo A - Trazabilidad de requisitos del cliente",
        "",
        "> Anexo del **informe tecnico** que responde **punto a punto** cada "
        "solicitud del cliente presente en el corpus, con **cita al documento "
        "fuente**. Es documentacion **generada de forma determinista** por el "
        "motor (`advisory-system/phases/requirements_traceability.py`) y es "
        "**dinamica**: las solicitudes se **extraen del corpus** (no estan "
        "hardcodeadas para ningun cliente), de modo que si cambian los "
        "documentos de contexto el anexo se **regenera** con las solicitudes de "
        "ese nuevo cliente. Gobernado por el skill "
        "`requirements-traceability`.",
        "",
        f"Se derivaron **{n} solicitudes**{docs_line}: "
        f"**{counts['Cubierto']} Cubierto**, **{counts['Parcial']} Parcial**, "
        f"**{counts['Pendiente']} Pendiente**.",
        "",
        _epistemic_note(),
        "",
        "> **Regenerar (parte de `--phase all`):**",
        ">",
        "> ```bash",
        "> python3 advisory-system/quickstart.py --phase all",
        "> ```",
        "",
        "## Resumen de cobertura",
        "",
        _status_mermaid(counts),
        "",
        "## 1. Checklist marcable (que desarrollar / que pide el cliente)",
        "",
        "Leyenda: `- [x]` Cubierto - `- [~]` Parcial - `- [ ]` Pendiente.",
        "",
    ]
    if reqs:
        for r in reqs:
            sym = _CHECK_SYMBOL.get(r.status, " ")
            parts.append(
                f"- [{sym}] **{r.req_id}** ({r.status}) {r.request} "
                f"_[fuente: {r.citation}]_ {r.epistemic_tag}"
            )
    else:
        parts.append("- [ ] (El corpus no permitio derivar solicitudes).")
    parts += [
        "",
        "## 2. Tabla de trazabilidad punto a punto",
        "",
        "| ID | Solicitud del cliente | Cita al documento fuente | Donde se "
        "responde (fase/seccion/entregable) | Estado | Evidencia/Nota |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    if reqs:
        for r in reqs:
            note = f"{r.epistemic_tag} {r.note}".replace("|", "\\|")
            where = r.where.replace("|", "\\|")
            cite = r.citation.replace("|", "\\|")
            parts.append(
                f"| {r.req_id} | {r.request} | {cite} | {where} | "
                f"{r.status} | {note} |"
            )
    else:
        parts.append("| - | (sin solicitudes derivables del corpus) | - | - | "
                     "- | - |")
    parts += [
        "",
        "## Metodo de derivacion (determinista y dinamico)",
        "",
        "Las solicitudes se extraen priorizando el documento `primary` tipo RFP "
        "(heuristica de rol/nombre) y complementando con el resto del corpus. "
        "En cada documento se localizan **anclas de seccion** portadoras de "
        "requisitos (objetivos, alcance, requisitos, informes requeridos, "
        "evaluacion, indicadores de retorno) mediante una normalizacion **sin "
        "espacios y sin acentos** robusta a la fragmentacion del PDF escaneado; "
        "como respaldo generico se detectan numerales/vinetas. Cada solicitud "
        "recibe un **ID estable** `REQ-NNN` en orden de documento, una **cita** "
        "a su documento (y seccion cuando es recuperable) y un **Estado** "
        "honesto derivado del **texto util real** y el flag epistemico de la "
        "Base de Conocimiento: **Pendiente + [EPISTEMIC-VOID]** cuando el "
        "documento fuente no tiene texto util (OCR pendiente).",
        "",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- #
# Escritura del anexo
# --------------------------------------------------------------------------- #

def write(tech_report_base: str, knowledge_base=None,
          documents: Optional[Sequence] = None) -> List[str]:
    """Write the traceability annex under ``<tech_report_base>/<ANNEX_DIRNAME>/``.

    Accepts either a ``KnowledgeBase`` (``.documents`` / ``.total``) or a plain
    list of ``Document`` objects via ``documents``. Deterministic and
    byte-identical between runs. Returns the sorted list of written paths.
    """
    docs: Sequence = []
    total: Optional[int] = None
    if knowledge_base is not None:
        docs = list(getattr(knowledge_base, "documents", []) or [])
        try:
            total = knowledge_base.total
        except Exception:
            total = len(docs)
    elif documents is not None:
        docs = list(documents)
        total = len(docs)

    reqs = extract_requirements(docs)

    annex_dir = os.path.join(tech_report_base, ANNEX_DIRNAME)
    os.makedirs(annex_dir, exist_ok=True)
    written: List[str] = []
    path = os.path.join(annex_dir, "README.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build_annex_readme(reqs, total_docs=total))
    written.append(path)
    return sorted(written)

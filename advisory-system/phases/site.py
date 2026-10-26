"""Self-contained HTML viewer builder for the Credi10 2.0 advisory.

Generates ONE standalone ``.html`` file that embeds the Markdown of the three
reports (commercial proposal, executive report, multi-level technical report)
so the user can download it and open it locally with a double click
(``file://``) -- WITHOUT a server and WITHOUT ``fetch()``.

Hard constraints (consistent with the rest of the engine):
  * Standard library ONLY.
  * Deterministic: regenerating produces a byte-identical file (documents are
    discovered in a stable, sorted order; no timestamps, no absolute paths).
  * The Markdown is embedded inside ``<script type="text/plain">`` blocks; the
    only external dependencies (marked.js + mermaid.js) load from CDN at runtime
    in the user's browser, and the page degrades to readable raw Markdown if
    those fail to load.
"""

from __future__ import annotations

import html
import json
import os
from typing import Dict, List, Tuple

REPORT_DIRNAME = "advisory-credi10-2.0"
OUTPUT_FILENAME = "advisory-credi10-2.0.html"

TECH_DIR = "3-informe-tecnico"

# Stable ordering of the technical-report phase folders.
PHASE_ORDER = [
    "fase-0-higiene-epistemica",
    "fase-1-contexto-as-is",
    "fase-2-estado-del-arte",
    "fase-3-gaps-y-viabilizacion",
    "fase-4-diseno-to-be",
    "fase-5-roadmap-estimacion-raid",
    "fase-6-caso-de-negocio",
]
ANNEX_ORDER = [
    "anexo-a-trazabilidad-requisitos",
    "anexo-b-arquitectura-extraccion",
    "anexo-c-en-que-cambio",
]


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _first_heading(md: str, fallback: str) -> str:
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()
    return fallback


def _safe_embed(md: str) -> str:
    """Escape so the Markdown can live inside a <script type=text/plain>.

    The only sequence that can break out is ``</script``; we neutralise it and
    revert it in JS (textContent.replace) before rendering.
    """
    return md.replace("</script", "<\\/script")


def _titleize(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").capitalize()


def _collect_documents(report_root: str) -> Tuple[List[Dict], List[Dict]]:
    """Return (documents, nav_tree).

    documents: list of {id, markdown} in stable order.
    nav_tree:  list of nav nodes describing the 3 reports (the technical one
               carries nested children for phases/themes/annexes).
    """
    documents: List[Dict] = []
    nav: List[Dict] = []

    def add_doc(doc_id: str, md: str) -> None:
        documents.append({"id": doc_id, "markdown": md})

    # --- Commercial / offer: the two separate commercial outcomes --------
    # Governed by the commercial-opportunity-analysis skill. Embedded as a
    # top-level nav group with the two outcomes as leaves, in stable order.
    commercial_children: List[Dict] = []
    for cid, fname, fallback in (
        ("c-opp", "0-analisis-oportunidad-comercial.md",
         "Analisis de oportunidad comercial"),
        ("c-corr", "0b-checklist-oferta-y-correlacion.md",
         "Checklist de oferta y correlacion"),
    ):
        fpath = os.path.join(report_root, fname)
        if not os.path.exists(fpath):
            continue
        md = _read(fpath)
        add_doc(cid, md)
        commercial_children.append(
            {"id": cid, "title": _first_heading(md, fallback),
             "kind": "leaf", "children": []})
    if commercial_children:
        nav.append({"id": "c0", "title": "Comercial / Oferta",
                    "kind": "report", "children": commercial_children})

    # --- Report 1: commercial proposal -----------------------------------
    p1 = os.path.join(report_root, "1-propuesta-comercial.md")
    md1 = _read(p1)
    add_doc("r1", md1)
    nav.append({"id": "r1", "title": _first_heading(md1, "Propuesta Comercial"),
                "kind": "report", "children": []})

    # --- Report 2: executive / management report -------------------------
    p2 = os.path.join(report_root, "2-reporte-gerencial.md")
    md2 = _read(p2)
    add_doc("r2", md2)
    nav.append({"id": "r2", "title": _first_heading(md2, "Reporte Gerencial"),
                "kind": "report", "children": []})

    # --- Report 3: multi-level technical report --------------------------
    tech_root = os.path.join(report_root, TECH_DIR)
    tech_children: List[Dict] = []

    readme = os.path.join(tech_root, "README.md")
    md_tr = _read(readme)
    add_doc("r3-root", md_tr)
    tech_children.append({"id": "r3-root",
                          "title": "Indice del informe tecnico",
                          "kind": "leaf", "children": []})

    # Phases, each with its README first then the remaining themes sorted.
    for phase in PHASE_ORDER:
        phase_dir = os.path.join(tech_root, phase)
        if not os.path.isdir(phase_dir):
            continue
        phase_readme = os.path.join(phase_dir, "README.md")
        phase_title = _first_heading(_read(phase_readme), _titleize(phase)) \
            if os.path.exists(phase_readme) else _titleize(phase)
        phase_node = {"id": "nav-" + phase, "title": phase_title,
                      "kind": "group", "children": []}
        # README first
        if os.path.exists(phase_readme):
            did = "d-%s-readme" % phase
            add_doc(did, _read(phase_readme))
            phase_node["children"].append(
                {"id": did, "title": "Resumen de fase", "kind": "leaf",
                 "children": []})
        # themes (everything except README), sorted for determinism
        for fname in sorted(os.listdir(phase_dir)):
            if fname == "README.md" or not fname.endswith(".md"):
                continue
            fpath = os.path.join(phase_dir, fname)
            md = _read(fpath)
            did = "d-%s-%s" % (phase, fname[:-3])
            add_doc(did, md)
            phase_node["children"].append(
                {"id": did, "title": _first_heading(md, _titleize(fname[:-3])),
                 "kind": "leaf", "children": []})
        tech_children.append(phase_node)

    # Annexes
    for annex in ANNEX_ORDER:
        apath = os.path.join(tech_root, annex, "README.md")
        if not os.path.exists(apath):
            continue
        md = _read(apath)
        did = "d-%s" % annex
        add_doc(did, md)
        tech_children.append({"id": did,
                              "title": _first_heading(md, _titleize(annex)),
                              "kind": "leaf", "children": []})

    nav.append({"id": "r3", "title": _first_heading(md_tr, "Informe Tecnico"),
                "kind": "report", "children": tech_children})

    return documents, nav


def _render_html(documents: List[Dict], nav: List[Dict]) -> str:
    # Embedded documents as individual plain-text script blocks.
    doc_blocks = []
    for doc in documents:
        doc_blocks.append(
            '<script type="text/plain" class="md-doc" data-doc-id="%s">%s</script>'
            % (html.escape(doc["id"], quote=True), _safe_embed(doc["markdown"]))
        )
    docs_html = "\n".join(doc_blocks)
    nav_json = json.dumps(nav, ensure_ascii=False, sort_keys=False)

    return _TEMPLATE.replace("/*__NAV__*/", nav_json).replace(
        "<!--__DOCS__-->", docs_html)


def build_site(repo_root: str) -> str:
    """Build the standalone HTML. Returns the output path."""
    report_root = os.path.join(repo_root, REPORT_DIRNAME)
    documents, nav = _collect_documents(report_root)
    out_path = os.path.join(report_root, OUTPUT_FILENAME)
    htmltext = _render_html(documents, nav)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(htmltext)
    return out_path


_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Advisory Credi10 2.0 - Kulgops</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<style>
:root{
  --brand:#1f6feb; --brand-dark:#0b3d91; --bg:#f6f8fb; --panel:#ffffff;
  --text:#1b2330; --muted:#5b6673; --border:#e3e8ef; --code:#0d1117;
  --sidebar:#0e1b33; --sidebar-text:#cdd7e6; --sidebar-active:#1f6feb;
}
html[data-theme="dark"]{
  --bg:#0d1117; --panel:#161b22; --text:#e6edf3; --muted:#9aa7b4;
  --border:#2b333d; --sidebar:#060a12;
}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.6}
header.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;
  gap:16px;padding:12px 22px;background:linear-gradient(90deg,var(--brand-dark),var(--brand));
  color:#fff;box-shadow:0 2px 12px rgba(0,0,0,.18)}
.logo{font-weight:800;letter-spacing:.5px;font-size:20px}
.logo span{opacity:.85;font-weight:400;font-size:13px;margin-left:8px}
.topbar .spacer{flex:1}
.btn{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);
  color:#fff;border-radius:8px;padding:7px 12px;cursor:pointer;font-size:13px;
  transition:.2s}
.btn:hover{background:rgba(255,255,255,.3)}
.layout{display:flex;min-height:calc(100vh - 56px)}
aside{width:320px;background:var(--sidebar);color:var(--sidebar-text);
  overflow-y:auto;max-height:calc(100vh - 56px);position:sticky;top:56px;
  transition:margin-left .25s ease;padding:10px 0}
aside.hidden{margin-left:-320px}
.navitem{padding:9px 18px;cursor:pointer;font-size:14px;border-left:3px solid transparent;
  transition:.15s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.navitem:hover{background:rgba(255,255,255,.06)}
.navitem.report{font-weight:700;color:#fff;margin-top:6px}
.navitem.group{font-weight:600;color:#9db7e8}
.navitem.leaf{padding-left:34px;font-size:13px;color:var(--sidebar-text)}
.navitem.active{border-left-color:var(--sidebar-active);background:rgba(31,111,235,.18);color:#fff}
.navchildren{overflow:hidden;max-height:0;transition:max-height .3s ease}
.navchildren.open{max-height:4000px}
main{flex:1;overflow-x:auto;padding:0}
.content-wrap{max-width:980px;margin:0 auto;padding:30px 40px 80px}
.breadcrumb{color:var(--muted);font-size:13px;margin-bottom:10px}
article{background:var(--panel);border:1px solid var(--border);border-radius:14px;
  padding:34px 40px;box-shadow:0 1px 3px rgba(0,0,0,.05);animation:fade .35s ease}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
article h1{font-size:28px;border-bottom:2px solid var(--brand);padding-bottom:10px;margin-top:0}
article h2{font-size:22px;margin-top:34px;color:var(--brand-dark)}
html[data-theme="dark"] article h2{color:#6ea8ff}
article h3{font-size:17px;margin-top:24px}
article table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14px;display:block;overflow-x:auto}
article th,article td{border:1px solid var(--border);padding:8px 11px;text-align:left}
article th{background:rgba(31,111,235,.1)}
article tr:nth-child(even) td{background:rgba(127,127,127,.05)}
article code{background:rgba(127,127,127,.14);padding:2px 6px;border-radius:5px;font-size:.9em}
article pre{background:var(--code);color:#e6edf3;padding:16px;border-radius:10px;overflow-x:auto}
article pre code{background:none;color:inherit}
article blockquote{border-left:4px solid var(--brand);margin:16px 0;padding:6px 16px;
  background:rgba(31,111,235,.06);color:var(--muted)}
.mermaid{background:var(--panel);text-align:center;margin:18px 0}
.landing{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px;margin-top:10px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:26px;
  cursor:pointer;transition:.25s;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.card:hover{transform:translateY(-6px);box-shadow:0 12px 28px rgba(31,111,235,.18);border-color:var(--brand)}
.card .badge{display:inline-block;background:var(--brand);color:#fff;border-radius:20px;
  padding:3px 12px;font-size:12px;margin-bottom:12px}
.card h3{margin:0 0 8px;font-size:19px}
.card p{margin:0;color:var(--muted);font-size:14px}
.hero{padding:26px 0 8px}
.hero h1{font-size:30px;margin:0 0 6px}
.hero p{color:var(--muted);margin:0}
.toggle-side{display:none}
@media(max-width:820px){aside{position:fixed;z-index:30;height:100%}.content-wrap{padding:20px}}
footer{color:var(--muted);text-align:center;font-size:12px;padding:24px}
</style>
</head>
<body>
<header class="topbar">
  <button class="btn toggle-side" id="toggleSide" title="Menu">&#9776;</button>
  <div class="logo">KULGOPS<span>Advisory &middot; Credi10 2.0</span></div>
  <div class="spacer"></div>
  <button class="btn" id="homeBtn">Inicio</button>
  <button class="btn" id="themeBtn">Modo oscuro</button>
</header>
<div class="layout">
  <aside id="sidebar"></aside>
  <main>
    <div class="content-wrap">
      <div class="breadcrumb" id="breadcrumb"></div>
      <div id="view"></div>
      <footer>Generado por el motor Zero-Drift &middot; Kulgops Advisory &middot; vista de los 3 informes (no es fuente de verdad; los .md lo son)</footer>
    </div>
  </main>
</div>

<!--__DOCS__-->

<script type="application/json" id="navdata">/*__NAV__*/</script>

<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
(function(){
  "use strict";
  var NAV = JSON.parse(document.getElementById("navdata").textContent);
  // Build an id -> markdown map from the embedded plain-text blocks.
  var DOCS = {};
  Array.prototype.forEach.call(document.querySelectorAll("script.md-doc"), function(s){
    DOCS[s.getAttribute("data-doc-id")] = s.textContent.replace(/<\\\/script/g, "</script");
  });
  var titleById = {};
  (function idx(nodes){nodes.forEach(function(n){titleById[n.id]=n.title; if(n.children) idx(n.children);});})(NAV);

  var hasMarked = typeof window.marked !== "undefined";
  var hasMermaid = typeof window.mermaid !== "undefined";
  if(hasMermaid){ try{ mermaid.initialize({startOnLoad:false, theme:"default", securityLevel:"loose"}); }catch(e){ hasMermaid=false; } }

  var view = document.getElementById("view");
  var breadcrumb = document.getElementById("breadcrumb");
  var sidebar = document.getElementById("sidebar");

  function renderMarkdown(md){
    if(!hasMarked){ var pre=document.createElement("pre"); pre.textContent=md; return pre.outerHTML; }
    // Protect mermaid code fences so marked doesn't turn them into <code>.
    var blocks=[]; 
    md = md.replace(/```mermaid\s*([\s\S]*?)```/g, function(_,code){ blocks.push(code); return "@@MERMAID"+(blocks.length-1)+"@@"; });
    var htmlStr = marked.parse(md);
    htmlStr = htmlStr.replace(/@@MERMAID(\d+)@@/g, function(_,i){ return '<div class="mermaid">'+blocks[+i].trim()+'</div>'; });
    return htmlStr;
  }

  function showDoc(id){
    var md = DOCS[id]; if(md===undefined){ return; }
    breadcrumb.textContent = titleById[id] || "";
    view.innerHTML = '<article>'+renderMarkdown(md)+'</article>';
    if(hasMermaid){ try{ mermaid.run({nodes: view.querySelectorAll(".mermaid")}); }catch(e){} }
    markActive(id);
    window.scrollTo({top:0, behavior:"smooth"});
  }

  function showHome(){
    breadcrumb.textContent="";
    var cards = NAV.map(function(r){
      return '<div class="card" data-go="'+r.id+'"><span class="badge">Informe</span>'+
             '<h3>'+r.title+'</h3><p>'+(r.kind==="report"&&r.children&&r.children.length?
             (r.children.length+" secciones navegables"):"Documento completo")+'</p></div>';
    }).join("");
    view.innerHTML='<div class="hero"><h1>Advisory Credi10 2.0</h1>'+
      '<p>Vista interactiva de los tres informes. Selecciona uno para comenzar.</p></div>'+
      '<div class="landing">'+cards+'</div>';
    Array.prototype.forEach.call(view.querySelectorAll(".card"), function(c){
      c.addEventListener("click", function(){ var r=NAV.filter(function(x){return x.id===c.getAttribute("data-go");})[0];
        if(r.children && r.children.length){ openFirstLeaf(r); } else { showDoc(r.id); } });
    });
  }
  function openFirstLeaf(node){
    if(DOCS[node.id]!==undefined){ showDoc(node.id); return true; }
    if(node.children){ for(var i=0;i<node.children.length;i++){ if(openFirstLeaf(node.children[i])) return true; } }
    return false;
  }

  function buildNav(){
    sidebar.innerHTML="";
    NAV.forEach(function(r){
      var el=document.createElement("div"); el.className="navitem report"; el.textContent=r.title;
      el.addEventListener("click", function(){ if(r.children&&r.children.length){ toggleChildren(r.id); } else { showDoc(r.id); } });
      sidebar.appendChild(el);
      if(r.children && r.children.length){
        var wrap=document.createElement("div"); wrap.className="navchildren open"; wrap.id="nc-"+r.id;
        r.children.forEach(function(c){ renderNode(c, wrap, 0); });
        sidebar.appendChild(wrap);
      }
    });
  }
  function renderNode(node, parent, depth){
    var el=document.createElement("div");
    el.className="navitem "+(node.kind==="group"?"group":"leaf");
    el.textContent=node.title; el.setAttribute("data-id", node.id);
    parent.appendChild(el);
    if(node.kind==="group" && node.children && node.children.length){
      var wrap=document.createElement("div"); wrap.className="navchildren open";
      node.children.forEach(function(c){ renderNode(c, wrap, depth+1); });
      parent.appendChild(wrap);
      el.addEventListener("click", function(){ wrap.classList.toggle("open"); });
    } else {
      el.addEventListener("click", function(){ showDoc(node.id); });
    }
  }
  function toggleChildren(id){ var w=document.getElementById("nc-"+id); if(w){ w.classList.toggle("open"); } }
  function markActive(id){
    Array.prototype.forEach.call(sidebar.querySelectorAll(".navitem"), function(n){
      n.classList.toggle("active", n.getAttribute("data-id")===id); });
  }

  document.getElementById("homeBtn").addEventListener("click", showHome);
  document.getElementById("toggleSide").addEventListener("click", function(){ sidebar.classList.toggle("hidden"); });
  document.getElementById("themeBtn").addEventListener("click", function(){
    var h=document.documentElement; var dark=h.getAttribute("data-theme")==="dark";
    h.setAttribute("data-theme", dark?"light":"dark"); this.textContent=dark?"Modo oscuro":"Modo claro";
    if(hasMermaid){ try{ mermaid.initialize({startOnLoad:false, theme: dark?"default":"dark", securityLevel:"loose"}); }catch(e){} }
  });

  buildNav();
  showHome();
})();
</script>
</body>
</html>
"""

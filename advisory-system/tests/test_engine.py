"""Unit tests for the Zero-Drift advisory engine core (FEAT-001).

Run with:
    python3 -m unittest discover -s advisory-system/tests -v
"""

import os
import sys
import unittest

# Make advisory-system/ importable regardless of the discovery CWD.
_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
_SYSTEM_DIR = os.path.dirname(_TESTS_DIR)
_REPO_ROOT = os.path.dirname(_SYSTEM_DIR)
if _SYSTEM_DIR not in sys.path:
    sys.path.insert(0, _SYSTEM_DIR)

from engine.corpus import CorpusLoader, clean_text, defragment  # noqa: E402
from engine.phases import REPORT_FILENAMES, load_phases, PHASE_ORDER  # noqa: E402
import roles as roles_pkg  # noqa: E402


EXPECTED_FILENAMES = {
    "0": "00-higiene-epistemica.md",
    "1": "01-contexto-as-is.md",
    "2": "02-estado-del-arte.md",
    "3": "03-gaps-y-viabilizacion.md",
    "4": "04-diseno-to-be.md",
    "5": "05-roadmap-estimacion-raid.md",
    "6": "06-caso-de-negocio.md",
}


class TestCorpusLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = CorpusLoader(_REPO_ROOT)
        cls.docs = cls.loader.load()

    def test_discovers_pdfs_and_pngs(self):
        pdfs = [d for d in self.docs if d.kind == "pdf"]
        pngs = [d for d in self.docs if d.kind == "png"]
        self.assertGreaterEqual(len(pdfs), 1, "debe descubrir al menos un PDF")
        self.assertEqual(len(pngs), 3, "deben existir 3 diagramas PNG")

    def test_rfp_text_extraction(self):
        rfp = self.loader.find("RFP_CREDI10_2_0")
        self.assertIsNotNone(rfp, "RFP_CREDI10_2_0.pdf debe descubrirse")
        self.assertEqual(rfp.kind, "pdf")
        self.assertEqual(rfp.role, "primary")
        self.assertTrue(rfp.extracted_text, "el texto extraido del RFP no debe estar vacio")
        low = rfp.extracted_text.lower()
        self.assertTrue(
            ("credi10" in low) or ("assessment" in low) or ("credi 10" in low),
            "el texto del RFP debe contener un token conocido",
        )

    def test_png_registered_as_binary_evidence(self):
        for png in [d for d in self.docs if d.kind == "png"]:
            self.assertTrue(png.sha256, "el PNG debe tener sha256")
            self.assertGreater(png.size, 0)
            self.assertTrue(png.description, "el PNG debe tener descripcion transcrita")
            self.assertEqual(png.extracted_text, "", "no se debe OCR-izar el PNG")

    def test_classification_primary_secondary(self):
        primary = self.loader.primary()
        prim_names = {d.filename for d in primary}
        self.assertIn("RFP_CREDI10_2_0.pdf", prim_names)
        self.assertIn("WSO2 y Studio F - Assessment Mayo2026-Final.pdf", prim_names)
        # 3 PNGs are primary too -> at least 5 primary artifacts.
        self.assertGreaterEqual(len(primary), 5)


class TestCleanupHelpers(unittest.TestCase):
    def test_defragment_single_letters(self):
        self.assertEqual(defragment("C r e d i 10"), "Credi 10")
        self.assertEqual(defragment("P R O Y E C T O"), "PROYECTO")

    def test_clean_text_strips_language_tags(self):
        raw = "es-CO   es-ES P R O Y E C T O pt-BR D E pt-BR C R E D I 10"
        cleaned = clean_text(raw)
        self.assertNotIn("es-CO", cleaned)
        self.assertNotIn("pt-BR", cleaned)
        self.assertIn("PROYECTO", cleaned)
        self.assertIn("CREDI 10", cleaned)

    def test_clean_text_collapses_whitespace(self):
        self.assertEqual(clean_text("a    b\n\tc"), "a b c")


class TestRoles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roles = roles_pkg.load_roles()

    def test_seventeen_roles(self):
        expected = {
            "ED", "EM", "AM", "EA", "BA", "PIA", "SME", "TDA", "DRE",
            "SA", "DA", "PM", "UX", "AIA", "FIN", "SEC", "ORG",
        }
        self.assertEqual(set(self.roles.keys()), expected)
        self.assertEqual(len(self.roles), 17)

    def test_roles_have_non_empty_fields(self):
        for code, role in self.roles.items():
            self.assertTrue(role.scope, f"{code} debe tener scope")
            self.assertTrue(role.income, f"{code} debe tener income")
            self.assertTrue(role.outcome, f"{code} debe tener outcome")
            self.assertTrue(role.cell, f"{code} debe pertenecer a una celula/comite")

    def test_am_is_main_verifier(self):
        am = self.roles["AM"]
        # AM verifies phases 1..6.
        self.assertEqual(set(am.verifies), {"1", "2", "3", "4", "5", "6"})

    def test_committee_and_cells(self):
        self.assertEqual(set(roles_pkg.committee()), {"ED", "EM", "AM"})
        cells = roles_pkg.cells()
        self.assertIn("EA", cells["Celula 1 - Discovery"])
        self.assertIn("SA", cells["Celula 2 - Diseno"])
        self.assertIn("FIN", cells["Celula 3 - Valor y Habilitacion"])

    def test_verifier_relationships_consistent(self):
        # Every phase verifier must be a defined role.
        phases = load_phases()
        for ph in phases.values():
            self.assertIn(ph.verifier, self.roles, f"verificador {ph.verifier} debe existir")


class TestPhases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.phases = load_phases()

    def test_seven_phases(self):
        self.assertEqual(set(self.phases.keys()), set(PHASE_ORDER))
        self.assertEqual(len(self.phases), 7)

    def test_phases_map_to_expected_filenames(self):
        self.assertEqual(REPORT_FILENAMES, EXPECTED_FILENAMES)
        for pid, fname in EXPECTED_FILENAMES.items():
            self.assertEqual(self.phases[pid].filename, fname)

    def test_each_phase_has_gate_and_leaders(self):
        for pid, ph in self.phases.items():
            self.assertTrue(ph.gate, f"fase {pid} debe tener gate")
            self.assertEqual(ph.gate.id, f"QG-{pid}")
            self.assertTrue(ph.gate.criteria, f"gate {ph.gate.id} debe tener criterios")
            self.assertTrue(ph.gate.nogo_condition, f"gate {ph.gate.id} debe tener No-Go")
            self.assertTrue(ph.leaders, f"fase {pid} debe tener lideres")
            self.assertTrue(ph.builder, f"fase {pid} debe tener builder")

    def test_builders_produce_structural_contract(self):
        from engine.corpus import CorpusLoader
        from engine.model import GoldenThread
        from phases.builders import BuildContext

        roles = roles_pkg.load_roles()
        loader = CorpusLoader(_REPO_ROOT)
        docs = loader.load()
        for pid, ph in self.phases.items():
            ctx = BuildContext(ph, roles, docs, GoldenThread())
            body = ph.builder(ctx)
            self.assertIn("```mermaid", body, f"fase {pid} debe incluir mermaid")
            self.assertIn("| ", body, f"fase {pid} debe incluir una tabla markdown")
            self.assertIn("Veredicto", body, f"fase {pid} debe incluir veredicto de gate")


class TestPhaseReportsContent(unittest.TestCase):
    """FEAT-002: corpus-grounded content for phases 0, 1 and 2."""

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.model import GoldenThread
        from phases.builders import BuildContext

        cls.phases = load_phases()
        roles = roles_pkg.load_roles()
        loader = CorpusLoader(_REPO_ROOT)
        docs = loader.load()
        cls.bodies = {}
        for pid in ("0", "1", "2"):
            ph = cls.phases[pid]
            ctx = BuildContext(ph, roles, docs, GoldenThread())
            cls.bodies[pid] = ph.builder(ctx)

    def _assert_structural_contract(self, pid, verdict_id):
        body = self.bodies[pid]
        self.assertIn("```mermaid", body, f"fase {pid} debe incluir mermaid")
        self.assertTrue(
            any(line.startswith("|") for line in body.splitlines()),
            f"fase {pid} debe incluir una tabla markdown (linea con '|')",
        )
        self.assertTrue(
            any(tag in body for tag in (
                "[VERIFIED-FACT]", "[DOC-ASSUMPTION]",
                "[DOC-CONFLICT]", "[EPISTEMIC-VOID]")),
            f"fase {pid} debe incluir al menos una etiqueta epistemica",
        )
        self.assertIn(f"Veredicto {verdict_id}", body,
                      f"fase {pid} debe incluir veredicto {verdict_id}")

    def test_phase0_contract_and_tokens(self):
        self._assert_structural_contract("0", "QG-0")
        body = self.bodies["0"]
        # El conflicto real de alcance (+150 apps / +200 BDs vs ~20 componentes).
        self.assertIn("[DOC-CONFLICT]", body)
        self.assertIn("+150", body)
        self.assertIn("+200", body)
        self.assertIn("Studio F", body)
        self.assertIn("[EPISTEMIC-VOID]", body)
        for token in ("CrossCore", "Inspektor", "C10_Credi10NET", "WOLKVOX"):
            self.assertIn(token, body, f"fase 0 debe mencionar {token}")

    def test_phase1_contract_and_tokens(self):
        self._assert_structural_contract("1", "QG-1")
        body = self.bodies["1"]
        for token in ("CrossCore", "Inspektor", "Datacredito",
                      "C10_Credi10NET", ".NET Framework 4.8",
                      ".NET Core 3.1", "WOLKVOX"):
            self.assertIn(token, body, f"fase 1 debe mencionar {token}")
        # Indicador de disponibilidad 90 -> 99 del RFP.
        self.assertIn("90%", body)
        self.assertIn("99%", body)
        # Hilo Dorado DRV/CAP.
        self.assertIn("DRV-001", body)
        self.assertIn("CAP-001", body)

    def test_phase2_contract_and_tokens(self):
        self._assert_structural_contract("2", "QG-2")
        body = self.bodies["2"]
        for token in ("WSO2", "API", "BIAN", "BMK-001"):
            self.assertIn(token, body, f"fase 2 debe mencionar {token}")
        # Los benchmarks enlazan al Hilo Dorado de la Fase 1.
        self.assertIn("CAP-", body)
        self.assertIn("DRV-", body)
        self.assertIn("[DOC-ASSUMPTION]", body)

    def test_generated_files_on_disk(self):
        """Tras regenerar, los 3 .md existen y cumplen el contrato."""
        import subprocess

        out_dir = os.path.join(_REPO_ROOT, "advisory-credi10-2.0")
        for pid in ("0", "1", "2", "3", "4"):
            subprocess.run(
                [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
                 "--phase", pid],
                cwd=_REPO_ROOT, check=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        for pid, fname in (("0", "00-higiene-epistemica.md"),
                           ("1", "01-contexto-as-is.md"),
                           ("2", "02-estado-del-arte.md"),
                           ("3", "03-gaps-y-viabilizacion.md"),
                           ("4", "04-diseno-to-be.md")):
            path = os.path.join(out_dir, fname)
            self.assertTrue(os.path.isfile(path), f"{fname} debe existir")
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            self.assertIn("```mermaid", content)
            self.assertIn("Veredicto QG-", content)


class TestPhase34ReportsContent(unittest.TestCase):
    """FEAT-003: corpus-grounded content for phases 3 and 4."""

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.model import GoldenThread
        from phases.builders import BuildContext

        cls.phases = load_phases()
        roles = roles_pkg.load_roles()
        loader = CorpusLoader(_REPO_ROOT)
        docs = loader.load()
        cls.bodies = {}
        for pid in ("3", "4"):
            ph = cls.phases[pid]
            ctx = BuildContext(ph, roles, docs, GoldenThread())
            cls.bodies[pid] = ph.builder(ctx)

    def _assert_structural_contract(self, pid, verdict_id):
        body = self.bodies[pid]
        self.assertIn("```mermaid", body, f"fase {pid} debe incluir mermaid")
        self.assertTrue(
            any(line.startswith("|") for line in body.splitlines()),
            f"fase {pid} debe incluir una tabla markdown",
        )
        self.assertTrue(
            any(tag in body for tag in (
                "[VERIFIED-FACT]", "[DOC-ASSUMPTION]",
                "[DOC-CONFLICT]", "[EPISTEMIC-VOID]")),
            f"fase {pid} debe incluir al menos una etiqueta epistemica",
        )
        self.assertIn(f"Veredicto {verdict_id}", body,
                      f"fase {pid} debe incluir veredicto {verdict_id}")

    def test_phase3_contract_and_tokens(self):
        self._assert_structural_contract("3", "QG-3")
        body = self.bodies["3"]
        # Dolor real de integracion con Siesa + gobernanza + obsolescencia.
        for token in ("Siesa", "archivos planos", "Data Services",
                      "CrossCore", "Inspektor", "Datacredito",
                      ".NET Framework 4.8", ".NET Core 3.1"):
            self.assertIn(token, body, f"fase 3 debe mencionar {token}")
        # Gap Analysis TOGAF B/C/D ligado a indicadores RFP.
        self.assertIn("TOGAF", body)
        self.assertIn("90% -> 99%", body)
        # Hilo Dorado GAP/REL/ABB referenciando DRV/BMK.
        for prefix in ("GAP-001", "REL-001", "ABB-001", "DRV-", "BMK-"):
            self.assertIn(prefix, body, f"fase 3 debe incluir {prefix}")
        # Reverse Briefing (handoff Celula 1 -> Celula 2).
        self.assertIn("Reverse Briefing", body)

    def test_phase4_contract_and_tokens(self):
        self._assert_structural_contract("4", "QG-4")
        body = self.bodies["4"]
        for token in ("Siesa", "Data Services", ".NET 8", "PayU",
                      "API Gateway", "CrossCore"):
            self.assertIn(token, body, f"fase 4 debe mencionar {token}")
        # Mermaid ER/C4/flowchart.
        self.assertIn("erDiagram", body, "fase 4 debe incluir un erDiagram")
        self.assertIn("flowchart", body, "fase 4 debe incluir un flowchart (C4)")
        # Al menos 3 ADRs.
        for adr in ("ADR-001", "ADR-002", "ADR-003"):
            self.assertIn(adr, body, f"fase 4 debe incluir {adr}")
        # Gherkin BDD en espanol.
        for kw in ("Dado", "Cuando", "Entonces"):
            self.assertIn(kw, body, f"fase 4 debe incluir Gherkin '{kw}'")
        # Hilo Dorado SBB referenciando ABB.
        self.assertIn("SBB-001", body)
        self.assertIn("ABB-001", body)
        # Dry-Run y cadena de validacion.
        self.assertIn("Dry-Run", body)
        self.assertIn("STRIDE", body)


class TestPhase56ReportsContent(unittest.TestCase):
    """FEAT-004: corpus-grounded content for phases 5 and 6."""

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.model import GoldenThread
        from phases.builders import BuildContext

        cls.phases = load_phases()
        roles = roles_pkg.load_roles()
        loader = CorpusLoader(_REPO_ROOT)
        docs = loader.load()
        cls.bodies = {}
        for pid in ("5", "6"):
            ph = cls.phases[pid]
            ctx = BuildContext(ph, roles, docs, GoldenThread())
            cls.bodies[pid] = ph.builder(ctx)

    def _assert_structural_contract(self, pid, verdict_id):
        body = self.bodies[pid]
        self.assertIn("```mermaid", body, f"fase {pid} debe incluir mermaid")
        self.assertTrue(
            any(line.startswith("|") for line in body.splitlines()),
            f"fase {pid} debe incluir una tabla markdown",
        )
        self.assertTrue(
            any(tag in body for tag in (
                "[VERIFIED-FACT]", "[DOC-ASSUMPTION]",
                "[DOC-CONFLICT]", "[EPISTEMIC-VOID]")),
            f"fase {pid} debe incluir al menos una etiqueta epistemica",
        )
        self.assertIn(f"Veredicto {verdict_id}", body,
                      f"fase {pid} debe incluir veredicto {verdict_id}")

    def test_phase5_contract_and_tokens(self):
        self._assert_structural_contract("5", "QG-5")
        body = self.bodies["5"]
        # Roadmap por olas como gantt Mermaid.
        self.assertIn("gantt", body, "fase 5 debe incluir un gantt Mermaid")
        # Matriz RAID con las 4 secciones.
        self.assertIn("RAID", body)
        for section in ("Supuesto", "Restriccion", "Dependencia", "Prerrequisito"):
            self.assertIn(section, body, f"fase 5 debe incluir la seccion {section}")
        # WSJF y Team Topologies.
        self.assertIn("WSJF", body)
        self.assertIn("Team Topologies", body)
        self.assertIn("stream-aligned", body)
        # Restricciones reales del RFP.
        for token in ("preservar", "Siesa", "continuidad", "60 dias"):
            self.assertIn(token, body, f"fase 5 debe mencionar {token}")
        # Hilo Dorado WAV referenciando SBB y DRV.
        self.assertIn("WAV-000", body)
        self.assertIn("WAV-001", body)
        self.assertIn("SBB-", body)
        self.assertIn("DRV-", body)

    def test_phase6_contract_and_tokens(self):
        self._assert_structural_contract("6", "QG-6")
        body = self.bodies["6"]
        # Value Driver Tree (grafo Mermaid con outcomes tecnicos -> negocio).
        self.assertIn("Technical Outcomes", body)
        self.assertIn("Business Outcomes", body)
        self.assertIn("flowchart", body, "fase 6 debe incluir un grafo flowchart")
        # Linea base de costos ausente marcada como vacio epistemico.
        self.assertIn("[EPISTEMIC-VOID]", body)
        # Toda cifra monetaria debe llevar [DOC-ASSUMPTION]: las tablas
        # financieras (CAPEX/OPEX, TCO, escenarios) deben portar la etiqueta.
        for term in ("CAPEX", "OPEX", "TCO", "VAN/NPV", "TIR/IRR", "Payback"):
            self.assertIn(term, body, f"fase 6 debe incluir {term}")
        self.assertIn("[DOC-ASSUMPTION]", body)
        # Las filas de escenarios financieros deben estar en una tabla con
        # DOC-ASSUMPTION en su cabecera.
        self.assertTrue(
            any("Conservador" in l and "|" in l for l in body.splitlines()),
            "fase 6 debe incluir el escenario Conservador en una tabla",
        )
        # Hilo Dorado ROI referenciando DRV y completando F1->F6.
        self.assertIn("ROI-001", body)
        self.assertIn("DRV-001", body)
        self.assertIn("WAV-", body)
        self.assertIn("SBB-", body)
        # Criterios de evaluacion de la oferta 15/30/10/30/15.
        for pts in ("15", "30", "10"):
            self.assertIn(pts, body)
        self.assertIn("Experiencia", body)
        self.assertIn("Metodologia", body)


class TestReadmeIndexAndPipeline(unittest.TestCase):
    """FEAT-004: the generated README indexes and links all 7 reports."""

    @classmethod
    def setUpClass(cls):
        import subprocess

        cls.out_dir = os.path.join(_REPO_ROOT, "advisory-credi10-2.0")
        # Una sola corrida de `--phase all` deja en disco README + 7 informes.
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        with open(os.path.join(cls.out_dir, "README.md"), encoding="utf-8") as fh:
            cls.readme = fh.read()

    def test_readme_exists_and_links_all_reports(self):
        self.assertTrue(self.readme, "README.md debe existir y no estar vacio")
        for fname in EXPECTED_FILENAMES.values():
            # Enlace markdown [fname](fname).
            self.assertIn(f"[{fname}]({fname})", self.readme,
                          f"README debe enlazar {fname}")
            # Y el archivo debe existir en disco.
            self.assertTrue(
                os.path.isfile(os.path.join(self.out_dir, fname)),
                f"{fname} debe existir en disco tras --phase all",
            )

    def test_readme_shows_hilo_dorado(self):
        self.assertIn("```mermaid", self.readme)
        self.assertIn("Hilo Dorado", self.readme)
        # El grafo encadena DRV..ROI.
        for stage in ("DRV", "CAP", "BMK", "GAP", "REL", "ABB", "SBB", "WAV", "ROI"):
            self.assertIn(stage, self.readme, f"el Hilo Dorado debe incluir {stage}")

    def test_readme_has_framework_and_regen_command(self):
        self.assertIn("Zero-Drift", self.readme)
        self.assertIn("python3 advisory-system/quickstart.py --phase all",
                      self.readme)

    def test_generated_phase56_on_disk(self):
        with open(os.path.join(self.out_dir, "05-roadmap-estimacion-raid.md"),
                  encoding="utf-8") as fh:
            p5 = fh.read()
        self.assertIn("gantt", p5)
        self.assertIn("RAID", p5)
        with open(os.path.join(self.out_dir, "06-caso-de-negocio.md"),
                  encoding="utf-8") as fh:
            p6 = fh.read()
        self.assertIn("[DOC-ASSUMPTION]", p6)
        self.assertIn("[EPISTEMIC-VOID]", p6)


class TestGateEvaluation(unittest.TestCase):
    """Review follow-up: the stage-gate verdict must be COMPUTED, not hardcoded.

    Exercises both paths: the real report bodies evaluate to GO, and a
    deliberately-incomplete body / a broken Hilo Dorado evaluate to NO-GO with
    concrete reasons (so the No-Go branch is no longer dead/untested).
    """

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.model import GoldenThread
        from phases.builders import BuildContext

        cls.phases = load_phases()
        roles = roles_pkg.load_roles()
        loader = CorpusLoader(_REPO_ROOT)
        docs = loader.load()
        cls.bodies = {}
        for pid in PHASE_ORDER:
            ph = cls.phases[pid]
            ctx = BuildContext(ph, roles, docs, GoldenThread())
            cls.bodies[pid] = ph.builder(ctx)

    def test_all_real_reports_evaluate_go(self):
        from engine.gating import evaluate_gate
        for pid in PHASE_ORDER:
            ph = self.phases[pid]
            satisfied, reasons = evaluate_gate(ph, self.bodies[pid])
            self.assertTrue(
                satisfied,
                f"fase {pid} debe evaluar GO con el corpus real; reasons={reasons}",
            )
            self.assertEqual(reasons, [], f"fase {pid} no debe tener reasons en GO")

    def test_empty_body_is_nogo_with_reasons(self):
        from engine.gating import evaluate_gate
        ph = self.phases["0"]
        satisfied, reasons = evaluate_gate(ph, "# Fase vacia\n\n(sin contenido)\n")
        self.assertFalse(satisfied, "un cuerpo vacio debe evaluar NO-GO")
        self.assertTrue(reasons, "NO-GO debe enumerar motivos")
        joined = " ".join(reasons)
        self.assertIn("mermaid", joined)
        self.assertIn("tabla", joined)
        self.assertIn("epistemica", joined)
        self.assertIn("Veredicto QG-0", joined)

    def test_missing_mermaid_is_nogo(self):
        from engine.gating import evaluate_gate
        ph = self.phases["1"]
        body = self.bodies["1"].replace("```mermaid", "```text")
        satisfied, reasons = evaluate_gate(ph, body)
        self.assertFalse(satisfied)
        self.assertTrue(any("mermaid" in r for r in reasons))

    def test_qg6_broken_golden_thread_is_nogo(self):
        """QG-6 fails if an ROI link lacks a DRV ancestor on its line."""
        from engine.gating import evaluate_gate
        ph = self.phases["6"]
        # Strip every DRV id so no ROI can trace to a driver.
        import re as _re
        broken = _re.sub(r"DRV-\d+", "XXX-000", self.bodies["6"])
        satisfied, reasons = evaluate_gate(ph, broken)
        self.assertFalse(satisfied, "QG-6 debe ser NO-GO si el Hilo Dorado se rompe")
        self.assertTrue(
            any("ROI" in r and "driver" in r.lower() for r in reasons),
            f"la razon debe citar ROI sin ancestro driver; reasons={reasons}",
        )

    def test_qg3_gap_without_reliever_is_nogo(self):
        """QG-3 fails if a gap/reliever lacks traceability."""
        from engine.gating import evaluate_gate
        ph = self.phases["3"]
        # Remove every REL id so gaps become orphaned and relievers vanish.
        import re as _re
        broken = _re.sub(r"REL-\d+", "", self.bodies["3"])
        satisfied, reasons = evaluate_gate(ph, broken)
        self.assertFalse(satisfied, "QG-3 debe ser NO-GO si hay gaps sin reliever")
        self.assertTrue(
            any("reliever" in r.lower() for r in reasons),
            f"la razon debe citar gaps sin reliever; reasons={reasons}",
        )

    def test_nogo_verdict_line_is_patched_on_disk(self):
        """A computed NO-GO rewrites the printed 'Veredicto QG-x' line."""
        from engine.gating import evaluate_gate
        from engine.orchestrator import AdvisoryOrchestrator
        ph = self.phases["6"]
        import re as _re
        broken = _re.sub(r"DRV-\d+", "XXX-000", self.bodies["6"])
        satisfied, reasons = evaluate_gate(ph, broken)
        verdict = ph.gate.verdict(satisfied, reasons)
        patched = AdvisoryOrchestrator._patch_verdict(broken, ph, verdict)
        self.assertIn("NO-GO", patched)
        self.assertIn(f"> **Veredicto {ph.gate.id}:** {ph.gate.id} :: NO-GO", patched)
        # The GO line must be gone.
        self.assertNotIn(
            f"**Veredicto {ph.gate.id}:** {ph.gate.id} :: GO", patched
        )


class TestKnowledgeBase(unittest.TestCase):
    """FEAT-001: full 18-doc ingestion + generated knowledge base + checklist."""

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.knowledge import KnowledgeBase
        loader = CorpusLoader(_REPO_ROOT)
        docs = loader.load()
        cls.docs = docs
        cls.kb = KnowledgeBase.from_documents(docs)

    def test_all_18_documents_ingested(self):
        self.assertEqual(self.kb.total, 18, "deben ingerirse los 18 documentos")
        n_pdf = sum(1 for d in self.kb.documents if d.kind == "pdf")
        n_png = sum(1 for d in self.kb.documents if d.kind == "png")
        self.assertEqual(n_pdf, 15)
        self.assertEqual(n_png, 3)

    def test_documents_sorted_by_filename(self):
        names = [d.filename.lower() for d in self.kb.documents]
        self.assertEqual(names, sorted(names), "orden determinista por filename")

    def test_every_doc_has_coverage_band_and_flag(self):
        valid_bands = {"alta", "media", "baja", "nula"}
        valid_flags = {"[VERIFIED-FACT]", "[EPISTEMIC-VOID]"}
        for d in self.kb.documents:
            self.assertIn(d.coverage_band, valid_bands, d.filename)
            self.assertIn(d.epistemic_flag, valid_flags, d.filename)
            self.assertTrue(d.hierarchical_summary, d.filename)
            self.assertTrue(d.sha256)

    def test_primary_secondary_is_priority_not_exclusion(self):
        # ALL docs ingested regardless of role; both roles present.
        roles = {d.role for d in self.kb.documents}
        self.assertEqual(roles, {"primary", "secondary"})
        self.assertEqual(len(self.kb.documents), 18)

    def test_key_facts_are_traceable_to_source(self):
        for kf in self.kb.all_facts():
            self.assertTrue(kf.source_filename)
            self.assertTrue(
                self.kb.by_filename(kf.source_filename) is not None,
                f"la fuente {kf.source_filename} debe existir en el corpus",
            )

    def test_image_only_pdf_flagged_void_not_fabricated(self):
        # Honest epistemic policy: any PDF without a usable text layer must be
        # [EPISTEMIC-VOID] (never fabricated). Assert the rule, not a specific
        # count, since extraction quality can vary.
        from engine.knowledge import (
            MIN_CLEAN_CHARS_FOR_VERIFIED, EPISTEMIC_VOID, VERIFIED_FACT,
        )
        for d in self.kb.documents:
            if d.kind == "pdf" and d.clean_length < MIN_CLEAN_CHARS_FOR_VERIFIED:
                self.assertEqual(d.epistemic_flag, EPISTEMIC_VOID, d.filename)
            elif d.kind == "pdf":
                self.assertEqual(d.epistemic_flag, VERIFIED_FACT, d.filename)

    def test_write_is_deterministic_and_complete(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            kb_dir = os.path.join(tmp, "knowledge-base")
            first = self.kb.write(kb_dir)
            with open(os.path.join(kb_dir, "coverage-checklist.md"),
                      encoding="utf-8") as fh:
                checklist = fh.read()
            with open(os.path.join(kb_dir, "README.md"), encoding="utf-8") as fh:
                index = fh.read()
            # README + checklist + key-facts + 18 doc summaries = 21 files.
            self.assertEqual(len(first), 21)
            self.assertIn("18/18 documentos procesados", checklist)
            self.assertIn("sin muestreo", checklist)
            self.assertIn("| 18 |", index)
            # Second write must be byte-identical (determinism).
            before = {p: open(p, encoding="utf-8").read() for p in first}
            self.kb.write(kb_dir)
            after = {p: open(p, encoding="utf-8").read() for p in first}
            self.assertEqual(before, after, "la base de conocimiento debe ser determinista")

    def test_buildcontext_exposes_knowledge_base(self):
        from phases.builders import BuildContext
        from engine.model import GoldenThread
        phases = load_phases()
        roles = roles_pkg.load_roles()
        ctx = BuildContext(phases["0"], roles, self.docs, GoldenThread(),
                           knowledge_base=self.kb)
        self.assertIs(ctx.knowledge_base, self.kb)

    def test_orchestrator_writes_knowledge_base_folder(self):
        import subprocess
        kb_dir = os.path.join(_REPO_ROOT, "knowledge-base")
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        self.assertTrue(os.path.isdir(kb_dir))
        self.assertTrue(os.path.isfile(os.path.join(kb_dir, "README.md")))
        self.assertTrue(os.path.isfile(os.path.join(kb_dir, "coverage-checklist.md")))
        self.assertTrue(os.path.isfile(os.path.join(kb_dir, "key-facts.md")))
        self.assertTrue(os.path.isdir(os.path.join(kb_dir, "documents")))
        docs = [f for f in os.listdir(os.path.join(kb_dir, "documents"))
                if f.endswith(".md")]
        self.assertEqual(len(docs), 18)


class TestSkillsLoader(unittest.TestCase):
    """FEAT-002: declarative .kiro/skills policy layer + engine loader.

    These tests assert that the hand-authored SKILL.md policy documents are
    discoverable and that the ai-opportunities catalog is parseable by the
    stdlib loader. No solution/application code is involved: the SKILL.md files
    are advisory policy documentation and the loader is report-generator
    tooling that consumes that documentation.
    """

    @classmethod
    def setUpClass(cls):
        from engine.skills import SkillsLoader, default_skills_dir
        cls.skills_dir = default_skills_dir(_REPO_ROOT)
        cls.loader = SkillsLoader(root=_REPO_ROOT)
        cls.skills = cls.loader.load()

    def test_skills_dir_resolves_under_repo_root(self):
        self.assertEqual(
            self.skills_dir,
            os.path.join(_REPO_ROOT, ".kiro", "skills"),
        )
        self.assertTrue(os.path.isdir(self.skills_dir))

    def test_discovers_the_four_policy_skills(self):
        names = {s.name for s in self.skills}
        for expected in {
            "complete-corpus-ingestion",
            "token-budget-optimization",
            "zero-drift-roles-policy",
            "ai-opportunities-catalog",
        }:
            self.assertIn(expected, names)

    def test_skills_sorted_and_have_frontmatter(self):
        names = [s.name for s in self.skills]
        self.assertEqual(names, sorted(names), "orden determinista por nombre")
        for s in self.skills:
            self.assertTrue(s.description, f"{s.name} debe tener description")
            self.assertEqual(s.version, "1.0.0", s.name)

    def test_ai_catalog_parses_both_tracks(self):
        entries = self.loader.ai_opportunities()
        self.assertTrue(entries, "el catalogo de IA debe parsearse")
        tracks = {e.track for e in entries}
        self.assertEqual(tracks, {"ai-as-product", "ai-as-build-accelerator"})
        # Every entry carries the fields the Phase 4 builder will render.
        for e in entries:
            self.assertTrue(e.id)
            self.assertTrue(e.name)
            self.assertTrue(e.use_case)
            self.assertTrue(e.required_data)
            self.assertTrue(e.viability)
            self.assertTrue(e.roadmap_hook)

    def test_ai_catalog_order_is_stable(self):
        ids1 = [e.id for e in self.loader.ai_opportunities()]
        ids2 = [e.id for e in self.loader.ai_opportunities()]
        self.assertEqual(ids1, ids2, "orden de catalogo determinista")

    def test_graceful_degradation_when_skills_absent(self):
        from engine.skills import SkillsLoader
        missing = SkillsLoader(skills_dir=os.path.join(_REPO_ROOT, "__no_skills__"))
        self.assertEqual(missing.load(), [])
        self.assertEqual(missing.ai_opportunities(), [])


if __name__ == "__main__":
    unittest.main()

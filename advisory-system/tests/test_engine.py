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


class TestCommercialProposal(unittest.TestCase):
    """task three-reports / FEAT-002: the engine writes the commercial proposal.

    After `--phase all` the proposal must exist on disk and satisfy its content
    contract: Kulgops brand marked [DOC-ASSUMPTION], the 11 sections a-k, a
    high-level context Mermaid diagram, a Gantt, a table, and the investment
    marked [DOC-ASSUMPTION].
    """

    PROPOSAL_FILENAME = "1-propuesta-comercial.md"

    @classmethod
    def setUpClass(cls):
        import subprocess

        cls.out_dir = os.path.join(_REPO_ROOT, "advisory-credi10-2.0")
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        cls.path = os.path.join(cls.out_dir, cls.PROPOSAL_FILENAME)
        with open(cls.path, encoding="utf-8") as fh:
            cls.body = fh.read()

    def test_proposal_file_exists(self):
        self.assertTrue(os.path.isfile(self.path),
                        "la propuesta comercial debe existir tras --phase all")
        self.assertTrue(self.body.strip(), "la propuesta no puede estar vacia")

    def test_brand_kulgops_present_and_doc_assumption(self):
        self.assertIn("Kulgops", self.body)
        # El perfil corporativo de Kulgops debe marcarse como referencia.
        self.assertIn("Perfil corporativo de referencia [DOC-ASSUMPTION]",
                      self.body)

    def test_eleven_sections_a_to_k(self):
        expected = [
            "## a. Quienes somos",
            "## b. Alcance del servicio",
            "## c. Contexto de negocio",
            "## d. Metodologia de consultoria",
            "## e. Entregables",
            "## f. Estrategia de consultoria",
            "## g. Equipo de trabajo",
            "## h. Cronograma de trabajo",
            "## i. Supuestos y restricciones",
            "## j. Inversion",
            "## k. Terminos y condiciones",
        ]
        for heading in expected:
            self.assertIn(heading, self.body,
                          f"la propuesta debe incluir la seccion '{heading}'")

    def test_has_context_diagram_and_gantt(self):
        # >= 1 bloque mermaid (diagrama de contexto de alto nivel).
        self.assertGreaterEqual(self.body.count("```mermaid"), 1,
                                "debe haber al menos un diagrama Mermaid")
        # >= 1 Gantt en el cronograma.
        self.assertIn("gantt", self.body)
        # El diagrama de contexto vive en la seccion de contexto de negocio.
        ctx_idx = self.body.index("## c. Contexto de negocio")
        met_idx = self.body.index("## d. Metodologia de consultoria")
        self.assertIn("```mermaid", self.body[ctx_idx:met_idx],
                      "el diagrama de contexto debe estar en la seccion c")

    def test_has_markdown_table(self):
        self.assertIn("| --- |", self.body,
                      "la propuesta debe incluir al menos una tabla markdown")

    def test_investment_marked_doc_assumption(self):
        inv_idx = self.body.index("## j. Inversion")
        terms_idx = self.body.index("## k. Terminos y condiciones")
        investment = self.body[inv_idx:terms_idx]
        self.assertIn("[DOC-ASSUMPTION]", investment,
                      "la inversion debe estar marcada [DOC-ASSUMPTION]")

    def test_readme_links_proposal(self):
        with open(os.path.join(self.out_dir, "README.md"),
                  encoding="utf-8") as fh:
            readme = fh.read()
        self.assertIn(
            f"[`{self.PROPOSAL_FILENAME}`]({self.PROPOSAL_FILENAME})", readme,
            "el README maestro debe enlazar la propuesta comercial",
        )


class TestExecutiveReport(unittest.TestCase):
    """task three-reports / FEAT-003: the engine writes the management report.

    After `--phase all` the executive/management report must exist on disk and
    satisfy its content contract: executive sections (scope, phases, high-level
    diagnosis, strategy, risks, considerations, prerequisites), >= 1 Mermaid and
    >= 1 table, a reference to the technical report, and the real Credi10
    findings (Siesa/UnoEE and .NET). Figures marked [DOC-ASSUMPTION].
    """

    EXEC_REPORT_FILENAME = "2-reporte-gerencial.md"
    TECH_REPORT_REF = "3-informe-tecnico/README.md"

    @classmethod
    def setUpClass(cls):
        import subprocess

        cls.out_dir = os.path.join(_REPO_ROOT, "advisory-credi10-2.0")
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        cls.path = os.path.join(cls.out_dir, cls.EXEC_REPORT_FILENAME)
        with open(cls.path, encoding="utf-8") as fh:
            cls.body = fh.read()

    def test_report_file_exists(self):
        self.assertTrue(os.path.isfile(self.path),
                        "el reporte gerencial debe existir tras --phase all")
        self.assertTrue(self.body.strip(), "el reporte no puede estar vacio")

    def test_executive_sections_present(self):
        expected = [
            "## 1. Resumen ejecutivo",
            "## 2. Alcance comercial del proyecto",
            "## 3. Fases del proyecto (Zero-Drift)",
            "## 4. Diagnostico de alto nivel",
            "## 5. Estrategia de implementacion",
            "## 6. Riesgos",
            "## 7. Consideraciones",
            "## 8. Prerrequisitos",
        ]
        for heading in expected:
            self.assertIn(heading, self.body,
                          f"el reporte debe incluir la seccion '{heading}'")

    def test_has_mermaid_and_table(self):
        self.assertGreaterEqual(self.body.count("```mermaid"), 1,
                                "debe haber al menos un diagrama Mermaid")
        self.assertIn("| --- |", self.body,
                      "el reporte debe incluir al menos una tabla markdown")
        # El Mermaid de alto nivel vive en el diagnostico.
        diag_idx = self.body.index("## 4. Diagnostico de alto nivel")
        est_idx = self.body.index("## 5. Estrategia de implementacion")
        self.assertIn("```mermaid", self.body[diag_idx:est_idx],
                      "el diagnostico debe incluir un Mermaid de alto nivel")

    def test_references_technical_report(self):
        self.assertIn(self.TECH_REPORT_REF, self.body,
                      "el reporte debe referenciar el informe tecnico")

    def test_references_commercial_proposal(self):
        self.assertIn("1-propuesta-comercial.md", self.body,
                      "el reporte debe referenciar la propuesta comercial")

    def test_reflects_real_findings(self):
        # Hallazgos reales de Credi10: acople al ERP y obsolescencia .NET.
        self.assertTrue(
            ("Siesa" in self.body) or ("UnoEE" in self.body),
            "el diagnostico debe reflejar el acople a Siesa/UnoEE",
        )
        self.assertIn(".NET", self.body,
                      "el diagnostico debe reflejar la obsolescencia .NET")
        # Los 5 indicadores de retorno del RFP.
        for delta in ("90% -> 99%", "60% -> 80%", "80% -> 80%",
                      "50% -> 100%", "70% -> 100%"):
            self.assertIn(delta, self.body,
                          f"el reporte debe incluir el indicador {delta}")

    def test_figures_marked_doc_assumption(self):
        self.assertIn("[DOC-ASSUMPTION]", self.body,
                      "las cifras del reporte deben marcarse [DOC-ASSUMPTION]")

    def test_readme_links_report(self):
        with open(os.path.join(self.out_dir, "README.md"),
                  encoding="utf-8") as fh:
            readme = fh.read()
        self.assertIn(
            f"[`{self.EXEC_REPORT_FILENAME}`]({self.EXEC_REPORT_FILENAME})",
            readme,
            "el README maestro debe enlazar el reporte gerencial",
        )


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
        # Honest epistemic policy (recalibrated): the flag is driven by the REAL
        # useful-text ratio (real words / extracted-text bytes), NOT by raw
        # extracted size. A PDF whose useful text is below the threshold (an
        # image/scan, OCR pending in this environment) must be [EPISTEMIC-VOID];
        # above it, [VERIFIED-FACT]. Text is never fabricated. OCR-recovered
        # text (not reachable without an OCR engine) would be [OCR-EXTRACTED].
        from engine.knowledge import (
            MIN_USEFUL_RATIO_FOR_TEXT, EPISTEMIC_VOID, VERIFIED_FACT,
            OCR_EXTRACTED,
        )
        for d in self.kb.documents:
            if d.kind != "pdf":
                continue
            if d.epistemic_flag == OCR_EXTRACTED:
                # Only possible when a real OCR engine is present.
                continue
            if d.useful_ratio < MIN_USEFUL_RATIO_FOR_TEXT:
                self.assertEqual(d.epistemic_flag, EPISTEMIC_VOID, d.filename)
            else:
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


class TestModulesSourceOfTruth(unittest.TestCase):
    """FEAT-003: the declarative module universe is the single source of truth."""

    def test_full_module_universe_declared(self):
        from phases import modules as mods
        # The full Credi10 universe must be declared (no sampling).
        self.assertGreaterEqual(mods.module_count(), 17)
        self.assertEqual(mods.module_count(), len(mods.MODULES))

    def test_every_module_has_story_with_happy_and_edge(self):
        from phases.modules import MODULES
        for m in MODULES:
            self.assertGreaterEqual(
                len(m.stories), 1, f"{m.id} debe tener >= 1 historia")
            for s in m.stories:
                self.assertIsNotNone(s.happy, f"{s.id} debe tener happy path")
                self.assertIsNotNone(s.edge, f"{s.id} debe tener caso borde")
                self.assertEqual(s.happy.tipo, "happy")
                self.assertEqual(s.edge.tipo, "edge")
                # Gherkin steps present.
                self.assertTrue(s.happy.dado and s.happy.cuando and s.happy.entonces)
                self.assertTrue(s.edge.dado and s.edge.cuando and s.edge.entonces)

    def test_story_ids_unique_and_traceable(self):
        from phases.modules import all_story_ids, all_module_ids
        sids = all_story_ids()
        self.assertEqual(len(sids), len(set(sids)), "HU ids unicos")
        mids = all_module_ids()
        self.assertEqual(len(mids), len(set(mids)), "MOD ids unicos")

    def test_key_modules_present(self):
        from phases.modules import MODULES
        names = " | ".join(m.name for m in MODULES)
        for token in ("Plataforma Credi10", "CrossCore", "Inspektor",
                      "Datacredito", "Aplicacion ADMIN", "GenerarPagos",
                      "Corte de Cartera", "Link de Recaudo", "Portal",
                      "Boton E-commerce", "Captura Foto",
                      "Atencion al Cliente", "Llamada Predictiva",
                      "SMS / WhatsApp", "RCL y RCR", "UnoEE / Siesa",
                      "Fidelizacion"):
            self.assertIn(token, names, f"debe declararse el modulo {token}")


class TestCatalogReport(unittest.TestCase):
    """FEAT-003: exhaustive HU/Gherkin catalog render (04b)."""

    @classmethod
    def setUpClass(cls):
        from phases import catalog
        cls.body = catalog.build(knowledge_base=None)

    def test_structural_contract(self):
        self.assertIn("```mermaid", self.body)
        self.assertTrue(
            any(line.startswith("|") for line in self.body.splitlines()))
        self.assertTrue(any(tag in self.body for tag in (
            "[VERIFIED-FACT]", "[DOC-ASSUMPTION]",
            "[DOC-CONFLICT]", "[EPISTEMIC-VOID]")))
        self.assertIn("Veredicto QG-4b", self.body)

    def test_coverage_equals_declared_count(self):
        from phases.modules import module_count
        rendered = self.body.count("\n### MOD-")
        self.assertEqual(rendered, module_count(),
                         "el catalogo debe renderizar todos los modulos declarados")

    def test_every_module_has_gherkin_steps(self):
        # 17 modulos x 2 escenarios -> 34 de cada palabra clave Gherkin.
        from phases.modules import story_count
        expected = story_count() * 2
        for kw in ("Dado ", "Cuando ", "Entonces "):
            self.assertGreaterEqual(self.body.count(kw), expected,
                                    f"faltan pasos Gherkin '{kw.strip()}'")

    def test_verdict_is_go(self):
        self.assertIn("Veredicto QG-4b:** GO", self.body)


class TestPhase4Deepening(unittest.TestCase):
    """FEAT-003: deeper TO-BE architecture + AI catalog render in Phase 4."""

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.knowledge import KnowledgeBase
        from engine.model import GoldenThread
        from phases.builders import BuildContext
        phases = load_phases()
        roles = roles_pkg.load_roles()
        docs = CorpusLoader(_REPO_ROOT).load()
        kb = KnowledgeBase.from_documents(docs)
        ctx = BuildContext(phases["4"], roles, docs, GoldenThread(),
                           knowledge_base=kb)
        cls.body = phases["4"].builder(ctx)

    def test_c4_three_levels_tobe(self):
        for lvl in ("C4 Nivel 1 (TO-BE)", "C4 Nivel 2 (TO-BE)",
                    "C4 Nivel 3 (TO-BE)"):
            self.assertIn(lvl, self.body)

    def test_at_least_six_adrs(self):
        for adr in ("ADR-001", "ADR-002", "ADR-003", "ADR-004", "ADR-005",
                    "ADR-006"):
            self.assertIn(adr, self.body)

    def test_multiple_erds_per_bounded_context(self):
        self.assertGreaterEqual(self.body.count("erDiagram"), 5,
                                "debe haber un ERD por bounded context")

    def test_openapi_and_asyncapi_contracts(self):
        self.assertIn("openapi: 3.0.3", self.body)
        self.assertIn("asyncapi: 2.6.0", self.body)
        # Siesa Data Services + cobranza channels sketched.
        self.assertIn("Data Services sobre Siesa", self.body)
        self.assertIn("cobranza/contacto-realizado", self.body)

    def test_ai_catalog_rendered_from_skill(self):
        # Both tracks with entries from the declarative skill (FEAT-002).
        self.assertIn("IA-como-producto", self.body)
        self.assertIn("IA-como-acelerador-de-construccion", self.body)
        for aid in ("AIP-001", "AIP-006", "AIB-001", "AIB-003"):
            self.assertIn(aid, self.body)

    def test_kb_citation_present(self):
        self.assertIn("Base de Conocimiento", self.body)
        self.assertIn("RFP_CREDI10_2_0.pdf", self.body)

    def test_catalog_crossreference(self):
        self.assertIn("04b-catalogo-historias.md", self.body)


class TestPhase5Deepening(unittest.TestCase):
    """FEAT-004: per-module estimation + parametric model + roadmap +
    business-owner evaluation + schedule-slip risk analysis in Phase 5.

    These tests exercise the deepened estimation code paths and derive the
    expected coverage from len(MODULES) so adding/removing a module keeps the
    assertions honest (no sampling, no hardcoded counts)."""

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.knowledge import KnowledgeBase
        from engine.model import GoldenThread
        from phases.builders import BuildContext
        phases = load_phases()
        roles = roles_pkg.load_roles()
        docs = CorpusLoader(_REPO_ROOT).load()
        kb = KnowledgeBase.from_documents(docs)
        ctx = BuildContext(phases["5"], roles, docs, GoldenThread(),
                           knowledge_base=kb)
        cls.body = phases["5"].builder(ctx)

    def test_per_module_estimation_row_for_every_module(self):
        """Full coverage: every declared module has an estimation row with its
        T-shirt size, adjusted SP, person-months and WSJF (no sampling)."""
        from phases.modules import MODULES
        from phases.phase5 import (_module_profile, _derive_estimate, _wsjf,
                                   _fmt_pm)
        self.assertIn("Estimacion Detallada por Modulo", self.body)
        for mod in MODULES:
            tshirt, valor, crit, red, job = _module_profile(mod)
            _base, adj_sp, pm = _derive_estimate(tshirt)
            cod, wsjf = _wsjf(valor, crit, red, job)
            # A table row that begins with the module id must carry its name,
            # the derived adjusted SP, the formatted person-months and WSJF.
            row = next(
                (l for l in self.body.splitlines()
                 if l.startswith(f"| {mod.id} |") and mod.name in l
                 and _fmt_pm(pm) in l),
                None,
            )
            self.assertIsNotNone(
                row, f"falta la fila de estimacion de {mod.id} con sus cifras")
            self.assertIn(str(adj_sp), row,
                          f"{mod.id} debe mostrar su SP ajustado derivado")
            self.assertIn(str(wsjf), row, f"{mod.id} debe mostrar su WSJF")

    def test_estimation_count_equals_module_count(self):
        """Number of estimation rows == len(MODULES) (completeness, no sampling)."""
        from phases.modules import MODULES
        rows = [l for l in self.body.splitlines()
                if any(l.startswith(f"| {m.id} |") for m in MODULES)]
        # Every module appears in several tables (estimation, WSJF order,
        # front breakdown, scheduling, uncertainty). At minimum each module has
        # one estimation row; ensure all module ids are present.
        present = {m.id for m in MODULES
                   if any(l.startswith(f"| {m.id} |") for l in self.body.splitlines())}
        self.assertEqual(present, {m.id for m in MODULES},
                         "todos los modulos declarados deben estimarse")
        self.assertTrue(rows)

    def test_parametric_table_is_recalibratable(self):
        """The parametric table must surface the live PARAM/TSHIRT values, so a
        recalibration would change the rendered numbers (not a static string)."""
        from phases.phase5 import PARAM, TSHIRT_BASE_SP
        self.assertIn("Tabla parametrica recalibrable", self.body)
        self.assertIn(f"{PARAM['productividad_sp_por_pm']:.0f} SP / person-month",
                      self.body)
        self.assertIn(f"{PARAM['complejidad']:.2f}", self.body)
        self.assertIn(f"{PARAM['acople_legado']:.2f}", self.body)
        self.assertIn(f"{PARAM['riesgo_integracion']:.2f}", self.body)
        # Story-point base per size rendered from the live dict.
        for size, sp in TSHIRT_BASE_SP.items():
            self.assertTrue(
                any(l.strip() == f"| {size} | {sp} |"
                    for l in self.body.splitlines()),
                f"la talla {size} debe mostrar SP base {sp}")

    def test_front_decomposition_present(self):
        """Per-front breakdown (Dev/Data/Integracion/QA/DevOps/cambio)."""
        from phases.phase5 import FRONT_SPLIT
        self.assertEqual(sum(p for _, p in FRONT_SPLIT), 100,
                         "el perfil por frente debe sumar 100%")
        for front, _pct in FRONT_SPLIT:
            self.assertIn(front, self.body, f"falta el frente {front}")
        self.assertIn("Descomposicion del esfuerzo por frente", self.body)

    def test_roadmap_gantt_critical_path_and_dependencies(self):
        self.assertIn("gantt", self.body, "debe incluir un gantt Mermaid")
        self.assertIn("Ruta critica", self.body)
        # Explicit, acyclic technical dependency graph.
        self.assertIn("flowchart LR", self.body)
        self.assertIn("-->", self.body)

    def test_dependency_graph_is_acyclic(self):
        """Parse the dependency flowchart edges and assert no cycle exists."""
        from phases.phase5 import _dependency_diagram
        import re as _re
        diagram = _dependency_diagram()
        edges = _re.findall(r"(\w+)\s*-->\s*(\w+)", diagram)
        self.assertTrue(edges, "debe haber aristas de dependencia")
        graph = {}
        for a, b in edges:
            graph.setdefault(a, []).append(b)

        state = {}

        def has_cycle(node):
            state[node] = "grey"
            for nxt in graph.get(node, []):
                if state.get(nxt) == "grey":
                    return True
                if state.get(nxt) != "black" and has_cycle(nxt):
                    return True
            state[node] = "black"
            return False

        self.assertFalse(any(has_cycle(n) for n in list(graph)),
                         "el grafo de dependencias debe ser aciclico")

    def test_business_owner_evaluation_present(self):
        self.assertIn("Evaluacion critica del Dueno de Negocio", self.body)
        self.assertIn("Evaluacion del dueno de negocio", self.body)
        # The verdict must speak to sufficiency for creating the project.
        self.assertIn("suficiente para CREAR y ARRANCAR el proyecto", self.body)

    def test_schedule_slip_risk_with_go_nogo(self):
        self.assertIn("Riesgo de Desfase de Tiempos", self.body)
        self.assertIn("schedule-slip", self.body)
        # Probability / impact matrix with concrete risk ids.
        for rs in ("RS-01", "RS-02", "RS-03", "RS-04", "RS-05", "RS-06"):
            self.assertIn(rs, self.body)
        self.assertIn("Probabilidad", self.body)
        self.assertIn("Impacto", self.body)
        # Explicit Go/No-Go verdict to start construction.
        self.assertIn("Veredicto Go/No-Go", self.body)
        self.assertIn("GO CONDICIONADO", self.body)

    def test_schedule_risk_tied_to_kb_coverage(self):
        """The uncertainty table must be derived from KB coverage bands/flags,
        not hardcoded: it must list every module and a per-module uncertainty."""
        from phases.modules import MODULES
        self.assertIn("Incertidumbre de estimacion por cobertura del corpus",
                      self.body)
        for mod in MODULES:
            self.assertTrue(
                any(l.startswith(f"| {mod.id} |") and mod.source in l
                    for l in self.body.splitlines()),
                f"{mod.id} debe aparecer en la tabla de incertidumbre con su fuente")

    def test_effort_and_money_figures_carry_doc_assumption(self):
        """Every effort figure region must be marked [DOC-ASSUMPTION]."""
        self.assertIn("[DOC-ASSUMPTION]", self.body)
        # The per-module estimation header (SP ajustado / person-months) is the
        # region that must carry the tag.
        est_header = next(
            (l for l in self.body.splitlines()
             if l.startswith("| Modulo |") and "SP ajustado" in l), None)
        self.assertIsNotNone(est_header, "debe existir la cabecera de estimacion")
        self.assertIn("[DOC-ASSUMPTION]", est_header,
                      "la estimacion por modulo debe marcarse [DOC-ASSUMPTION]")

    def test_recalibration_changes_numbers(self):
        """Smoke check that the model is parametric: bumping productivity lowers
        derived person-months (would be impossible for a hardcoded table)."""
        from phases import phase5
        base_pm = phase5._derive_estimate("L")[2]
        original = phase5.PARAM["productividad_sp_por_pm"]
        try:
            phase5.PARAM["productividad_sp_por_pm"] = original * 2
            faster_pm = phase5._derive_estimate("L")[2]
        finally:
            phase5.PARAM["productividad_sp_por_pm"] = original
        self.assertLess(faster_pm, base_pm,
                        "mas velocidad => menos person-months (modelo parametrico)")


class TestCatalogGating(unittest.TestCase):
    """FEAT-005 step 5: the HU/Gherkin catalog (QG-4b) must evaluate GO for the
    real module universe and NO-GO if a module loses its edge scenario, so the
    gate is computed (not a hardcoded GO string)."""

    def test_real_catalog_is_go(self):
        from phases import catalog
        body = catalog.build(knowledge_base=None)
        self.assertIn("Veredicto QG-4b:** GO", body)

    def test_catalog_nogo_when_a_module_has_no_story(self):
        """Temporarily strip a module's stories and confirm the catalog verdict
        flips to NO-GO (revert-sensitive, not a static string)."""
        import dataclasses
        from phases import catalog, modules as mods
        original = list(mods.MODULES)
        try:
            # Rebuild the first module with an empty story list; the verdict
            # logic requires every module to carry >= 1 story.
            broken_module = dataclasses.replace(original[0], stories=[])
            mods.MODULES[0] = broken_module
            # catalog imported MODULES by reference at module load; patch both.
            catalog.MODULES[0] = broken_module
            body = catalog.build(knowledge_base=None)
            self.assertIn("Veredicto QG-4b:** NO-GO", body)
        finally:
            mods.MODULES[:] = original
            catalog.MODULES[:] = original


class TestAllPhasesAndCatalogGateGo(unittest.TestCase):
    """FEAT-005 step 5: evaluate EVERY phase body (0..6) plus the catalog and
    confirm all quality gates are GO, reusing in-memory bodies (fast)."""

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.knowledge import KnowledgeBase
        from engine.model import GoldenThread
        from phases.builders import BuildContext
        cls.phases = load_phases()
        roles = roles_pkg.load_roles()
        docs = CorpusLoader(_REPO_ROOT).load()
        kb = KnowledgeBase.from_documents(docs)
        cls.bodies = {}
        for pid in PHASE_ORDER:
            ph = cls.phases[pid]
            ctx = BuildContext(ph, roles, docs, GoldenThread(),
                               knowledge_base=kb)
            cls.bodies[pid] = ph.builder(ctx)

    def test_every_phase_gate_go(self):
        from engine.gating import evaluate_gate
        for pid in PHASE_ORDER:
            satisfied, reasons = evaluate_gate(self.phases[pid], self.bodies[pid])
            self.assertTrue(satisfied,
                            f"QG-{pid} debe ser GO; reasons={reasons}")
            self.assertEqual(reasons, [])

    def test_catalog_gate_go(self):
        from phases import catalog
        body = catalog.build(knowledge_base=None)
        self.assertIn("Veredicto QG-4b:** GO", body)


class TestPipelineProducesCatalog(unittest.TestCase):
    """FEAT-003: the full pipeline writes the catalog file deterministically."""

    def test_quickstart_writes_catalog(self):
        import subprocess
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        from engine.phases import CATALOG_FILENAME
        path = os.path.join(_REPO_ROOT, "advisory-credi10-2.0", CATALOG_FILENAME)
        self.assertTrue(os.path.isfile(path), "el catalogo debe existir")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        self.assertIn("Veredicto QG-4b", content)
        self.assertIn("```gherkin", content)


_EPISTEMIC_TAGS = (
    "[VERIFIED-FACT]", "[DOC-ASSUMPTION]", "[DOC-CONFLICT]", "[EPISTEMIC-VOID]",
)


class TestToBeDossier(unittest.TestCase):
    """TO-BE dossier task: lock in the deterministic SDLC-stage dossier tree.

    Mirrors ``TestReadmeIndexAndPipeline``: a single ``--phase all`` run in
    ``setUpClass`` materializes the dossier on disk, then the tests read the
    generated files. Assertions exercise the REAL generated content, so they
    would fail if the dossier generator (``phases/dossier.py``) were reverted.
    """

    @classmethod
    def setUpClass(cls):
        import subprocess
        from phases import dossier as dossier_mod

        cls.dossier_mod = dossier_mod
        cls.out_dir = os.path.join(_REPO_ROOT, "advisory-credi10-2.0")
        cls.base = os.path.join(cls.out_dir, dossier_mod.DOSSIER_DIRNAME)
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        def _read(relpath):
            with open(os.path.join(cls.base, relpath), encoding="utf-8") as fh:
                return fh.read()

        cls._read = staticmethod(_read)
        cls.stage_files = {
            "requisitos": os.path.join("01-requisitos", "requisitos.md"),
            "arquitectura": os.path.join("02-arquitectura", "arquitectura.md"),
            "specs": os.path.join("03-specs", "specs.md"),
            "ux": os.path.join("04-ux", "ux.md"),
            "pruebas": os.path.join("05-pruebas", "pruebas.md"),
            "estimacion": os.path.join("06-insumos-estimacion",
                                       "insumos-estimacion.md"),
        }
        cls.stage_content = {k: _read(v) for k, v in cls.stage_files.items()}
        cls.registry_slugs = [
            "ambiguedades", "riesgos", "consideraciones",
            "restricciones", "prerrequisitos",
        ]
        cls.registry_content = {
            slug: _read(os.path.join("00-registros", f"{slug}.md"))
            for slug in cls.registry_slugs
        }

    # -- 1. tree structure --------------------------------------------------- #
    def test_dossier_tree_structure(self):
        self.assertTrue(os.path.isdir(self.base),
                        "la carpeta base to-be/ debe existir")
        self.assertTrue(os.path.isfile(os.path.join(self.base, "README.md")),
                        "el dossier debe tener un README.md")
        self.assertTrue(os.path.isdir(os.path.join(self.base, "00-registros")),
                        "debe existir 00-registros/")
        for sub in ("01-requisitos", "02-arquitectura", "03-specs", "04-ux",
                    "05-pruebas", "06-insumos-estimacion"):
            self.assertTrue(
                os.path.isdir(os.path.join(self.base, sub)),
                f"debe existir la subcarpeta {sub}/",
            )
            # Y cada etapa tiene al menos un capitulo .md en disco.
            mds = [f for f in os.listdir(os.path.join(self.base, sub))
                   if f.endswith(".md")]
            self.assertTrue(mds, f"{sub}/ debe contener al menos un capitulo .md")

    # -- 2. structural contract per SDLC chapter ----------------------------- #
    def test_each_chapter_honors_structural_contract(self):
        for stage, content in self.stage_content.items():
            self.assertIn("```mermaid", content,
                          f"{stage} debe tener al menos un bloque mermaid")
            table_lines = [ln for ln in content.splitlines()
                           if ln.lstrip().startswith("|")]
            self.assertTrue(
                table_lines,
                f"{stage} debe tener al menos una tabla markdown",
            )
            self.assertTrue(
                any(tag in content for tag in _EPISTEMIC_TAGS),
                f"{stage} debe tener al menos una etiqueta epistemica",
            )

    # -- 3. cross-cutting registries ----------------------------------------- #
    def test_registries_exist_with_ids_levels_and_columns(self):
        prefixes = {
            "ambiguedades": "AMB-",
            "riesgos": "RSK-",
            "consideraciones": "CON-",
            "restricciones": "RST-",
            "prerrequisitos": "PRE-",
        }
        niveles = ["negocio", "aplicacion", "datos", "integracion",
                   "infraestructura", "seguridad"]
        # Sanity: our expected levels match the generator's NIVELES.
        self.assertEqual(sorted(niveles), sorted(self.dossier_mod.NIVELES))

        levels_seen = set()
        for slug in self.registry_slugs:
            content = self.registry_content[slug]
            self.assertIn(prefixes[slug], content,
                          f"{slug}.md debe contener el prefijo {prefixes[slug]}")
            # Cada registro declara un ID concreto (p. ej. AMB-001).
            self.assertRegex(
                content, prefixes[slug] + r"\d{3}",
                f"{slug}.md debe tener al menos un ID {prefixes[slug]}xxx",
            )
            self.assertIn("Estado", content,
                          f"{slug}.md debe tener columna Estado")
            self.assertTrue(
                ("Severidad" in content) or ("Impacto" in content)
                or ("Prioridad" in content),
                f"{slug}.md debe tener severidad/impacto/prioridad",
            )
            for nivel in niveles:
                if nivel in content:
                    levels_seen.add(nivel)
        # Los seis niveles arquitectonicos aparecen en el conjunto de registros.
        self.assertEqual(
            levels_seen, set(niveles),
            "los registros deben cubrir los seis niveles arquitectonicos",
        )

    def test_registries_carry_key_epistemic_and_corpus_items(self):
        amb = self.registry_content["ambiguedades"]
        rsk = self.registry_content["riesgos"]
        self.assertIn("[EPISTEMIC-VOID]", amb,
                      "ambiguedades debe tener al menos un [EPISTEMIC-VOID]")
        # Tension de alcance +150 aplicaciones / +200 bases de datos.
        self.assertIn("+150", amb)
        self.assertIn("+200", amb)
        # Riesgo de lectura directa a la BD del ERP Siesa.
        low_rsk = rsk.lower()
        self.assertIn("siesa", low_rsk)
        self.assertTrue(
            ("directo a la base de datos" in low_rsk)
            or ("directa a la bd" in low_rsk),
            "riesgos debe registrar la lectura directa a la BD del ERP Siesa",
        )

    # -- 4. corpus grounding ------------------------------------------------- #
    def test_corpus_grounding_real_tokens(self):
        req = self.stage_content["requisitos"]
        arch = self.stage_content["arquitectura"]
        specs = self.stage_content["specs"]
        est = self.stage_content["estimacion"]

        for token in ("CrossCore", "Inspektor", "Datacredito"):
            self.assertIn(token, req, f"requisitos debe mencionar {token}")
        for token in ("Siesa", "WSO2", "AWS", ".NET 8"):
            self.assertIn(token, arch, f"arquitectura debe mencionar {token}")
        for token in ("Siesa", "PayU"):
            self.assertIn(token, specs, f"specs debe mencionar {token}")
        self.assertIn("[DOC-ASSUMPTION]", est,
                      "el capitulo de estimacion debe llevar [DOC-ASSUMPTION]")

    # -- 5. determinism of the dossier writer ------------------------------- #
    def test_write_is_deterministic(self):
        import tempfile
        from engine.corpus import CorpusLoader
        from engine.knowledge import KnowledgeBase
        docs = CorpusLoader(_REPO_ROOT).load()
        kb = KnowledgeBase.from_documents(docs)
        with tempfile.TemporaryDirectory() as tmp:
            first = self.dossier_mod.write(tmp, kb)
            self.assertTrue(first, "write debe devolver paths escritos")
            # 1 README + 5 registros + 6 capitulos = 12 archivos.
            self.assertEqual(len(first), 12)
            # Debe devolver una lista ordenada de paths.
            self.assertEqual(first, sorted(first))
            before = {p: open(p, encoding="utf-8").read() for p in first}
            second = self.dossier_mod.write(tmp, kb)
            self.assertEqual(first, second,
                             "los paths deben ser estables entre corridas")
            after = {p: open(p, encoding="utf-8").read() for p in second}
            self.assertEqual(before, after,
                             "el dossier debe ser byte-identico entre corridas")

    # -- 6. README of the report set links the dossier ---------------------- #
    def test_report_readme_links_dossier(self):
        with open(os.path.join(self.out_dir, "README.md"),
                  encoding="utf-8") as fh:
            readme = fh.read()
        self.assertIn("to-be/README.md", readme,
                      "el README debe enlazar el dossier (to-be/README.md)")


def _count_headings(content):
    """Count H1/H2/H3 lines, ignoring fenced code blocks (``` ... ```)."""
    in_fence = False
    h1 = h2 = h3 = 0
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("### "):
            h3 += 1
        elif line.startswith("## "):
            h2 += 1
        elif line.startswith("# "):
            h1 += 1
    return h1, h2, h3


def _prose_word_count(content):
    """Count words that live in prose paragraphs (not tables/code/headings)."""
    in_fence = False
    words = 0
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if (not stripped or stripped.startswith("|")
                or stripped.startswith("#")):
            continue
        words += len(stripped.split())
    return words


class TestTechnicalReport(unittest.TestCase):
    """task three-reports / FEAT-004: multilevel narrative technical report.

    After `--phase all` the technical report must exist on disk as a tree under
    advisory-credi10-2.0/3-informe-tecnico/ with one subfolder per Zero-Drift
    phase, several theme files per phase, each with H1/H2/H3 hierarchy and
    substantial prose narrative in addition to tables/Mermaid. The TO-BE dossier
    must be integrated/linked coherently and the master index must link the 3
    engagement reports.
    """

    TECH_DIRNAME = "3-informe-tecnico"
    PHASE_SLUGS = [
        "fase-0-higiene-epistemica",
        "fase-1-contexto-as-is",
        "fase-2-estado-del-arte",
        "fase-3-gaps-y-viabilizacion",
        "fase-4-diseno-to-be",
        "fase-5-roadmap-estimacion-raid",
        "fase-6-caso-de-negocio",
    ]

    @classmethod
    def setUpClass(cls):
        import subprocess

        cls.out_dir = os.path.join(_REPO_ROOT, "advisory-credi10-2.0")
        cls.base = os.path.join(cls.out_dir, cls.TECH_DIRNAME)
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        with open(os.path.join(cls.base, "README.md"), encoding="utf-8") as fh:
            cls.master_readme = fh.read()

    # -- 1. tree: subfolder per phase + master README ----------------------- #
    def test_tree_has_readme_and_seven_phase_subfolders(self):
        self.assertTrue(os.path.isdir(self.base),
                        "la carpeta 3-informe-tecnico/ debe existir")
        self.assertTrue(
            os.path.isfile(os.path.join(self.base, "README.md")),
            "el informe tecnico debe tener un README.md maestro")
        for slug in self.PHASE_SLUGS:
            sub = os.path.join(self.base, slug)
            self.assertTrue(os.path.isdir(sub),
                            f"debe existir la subcarpeta de fase {slug}/")

    # -- 2. several theme files per phase ----------------------------------- #
    def test_each_phase_has_multiple_theme_files(self):
        for slug in self.PHASE_SLUGS:
            sub = os.path.join(self.base, slug)
            mds = sorted(f for f in os.listdir(sub) if f.endswith(".md"))
            # README.md + at least 2 theme files => >= 3 markdown files, and at
            # least 2 non-README theme files per phase (nivel 2).
            themes = [f for f in mds if f != "README.md"]
            self.assertGreaterEqual(
                len(themes), 2,
                f"{slug}/ debe tener varios archivos de tema (nivel 2)")

    # -- 3. H1/H2/H3 hierarchy + table + epistemic tag per theme ------------ #
    def test_theme_files_have_three_level_hierarchy(self):
        for slug in self.PHASE_SLUGS:
            sub = os.path.join(self.base, slug)
            for fname in os.listdir(sub):
                if not fname.endswith(".md") or fname == "README.md":
                    continue
                with open(os.path.join(sub, fname), encoding="utf-8") as fh:
                    content = fh.read()
                h1, h2, h3 = _count_headings(content)
                where = f"{slug}/{fname}"
                self.assertGreaterEqual(h1, 1, f"{where} debe tener un H1")
                self.assertGreaterEqual(h2, 1, f"{where} debe tener H2")
                self.assertGreaterEqual(
                    h3, 1, f"{where} debe tener H3 (>=3 niveles)")
                self.assertTrue(
                    any(l.lstrip().startswith("|")
                        for l in content.splitlines()),
                    f"{where} debe incluir al menos una tabla markdown")
                self.assertTrue(
                    any(tag in content for tag in _EPISTEMIC_TAGS),
                    f"{where} debe incluir al menos una etiqueta epistemica")

    # -- 4. substantial narrative prose, not just tables/Mermaid ------------ #
    def test_theme_files_have_substantial_prose(self):
        for slug in self.PHASE_SLUGS:
            sub = os.path.join(self.base, slug)
            for fname in os.listdir(sub):
                if not fname.endswith(".md") or fname == "README.md":
                    continue
                with open(os.path.join(sub, fname), encoding="utf-8") as fh:
                    content = fh.read()
                words = _prose_word_count(content)
                self.assertGreaterEqual(
                    words, 200,
                    f"{slug}/{fname} debe tener narrativa sustancial en prosa "
                    f"(>=200 palabras fuera de tablas/codigo), tiene {words}")
                # The mandatory analysis sections must be present.
                for section in ("Implicaciones para la estimacion",
                                "Implicaciones para la estrategia de "
                                "implementacion",
                                "Riesgos e incertidumbre"):
                    self.assertIn(
                        section, content,
                        f"{slug}/{fname} debe incluir la seccion '{section}'")

    # -- 5. master README: storytelling + Mermaid + phase links ------------- #
    def test_master_readme_has_storytelling_and_structure(self):
        self.assertTrue(self.master_readme.strip())
        self.assertIn("```mermaid", self.master_readme,
                      "el README maestro debe incluir Mermaid")
        self.assertTrue(
            ("storytelling" in self.master_readme.lower())
            or ("hilo narrativo" in self.master_readme.lower()),
            "el README maestro debe incluir el hilo narrativo/storytelling")
        for slug in self.PHASE_SLUGS:
            self.assertIn(f"{slug}/README.md", self.master_readme,
                          f"el README maestro debe enlazar la fase {slug}")

    # -- 6. the TO-BE dossier is integrated/linked coherently --------------- #
    def test_master_readme_integrates_dossier(self):
        self.assertIn("../to-be/README.md", self.master_readme,
                      "el informe tecnico debe integrar/enlazar el dossier "
                      "TO-BE de forma inequivoca")

    # -- 7. phase index READMEs link their themes --------------------------- #
    def test_phase_readmes_link_themes(self):
        for slug in self.PHASE_SLUGS:
            path = os.path.join(self.base, slug, "README.md")
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            sub = os.path.join(self.base, slug)
            themes = [f for f in os.listdir(sub)
                      if f.endswith(".md") and f != "README.md"]
            for t in themes:
                self.assertIn(f"]({t})", content,
                              f"{slug}/README.md debe enlazar el tema {t}")

    # -- 8. determinism: a second write is byte-identical ------------------- #
    def test_technical_report_write_is_deterministic(self):
        import tempfile
        from engine.corpus import CorpusLoader
        from engine.knowledge import KnowledgeBase
        from phases import technical_report as tr
        docs = CorpusLoader(_REPO_ROOT).load()
        kb = KnowledgeBase.from_documents(docs)
        with tempfile.TemporaryDirectory() as tmp:
            first = tr.write(tmp, knowledge_base=kb)
            self.assertTrue(first, "write debe devolver paths escritos")
            self.assertEqual(first, sorted(first),
                             "los paths deben estar ordenados")
            # README maestro + por fase: 7 README de fase + 1 maestro + temas.
            self.assertGreaterEqual(len(first), 7 + 1 + 14)
            before = {p: open(p, encoding="utf-8").read() for p in first}
            second = tr.write(tmp, knowledge_base=kb)
            self.assertEqual(first, second,
                             "los paths deben ser estables entre corridas")
            after = {p: open(p, encoding="utf-8").read() for p in second}
            self.assertEqual(before, after,
                             "el informe tecnico debe ser byte-identico")


class TestMasterReadmeLinksThreeReports(unittest.TestCase):
    """FEAT-004: the master index links the three separate engagement reports
    (commercial proposal, executive report, technical report) and still links
    the per-phase reports and the Hilo Dorado (regression of the earlier
    README contract)."""

    @classmethod
    def setUpClass(cls):
        import subprocess

        cls.out_dir = os.path.join(_REPO_ROOT, "advisory-credi10-2.0")
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        with open(os.path.join(cls.out_dir, "README.md"),
                  encoding="utf-8") as fh:
            cls.readme = fh.read()

    def test_links_the_three_engagement_reports(self):
        self.assertIn("[`1-propuesta-comercial.md`](1-propuesta-comercial.md)",
                      self.readme)
        self.assertIn("[`2-reporte-gerencial.md`](2-reporte-gerencial.md)",
                      self.readme)
        self.assertIn(
            "[`3-informe-tecnico/README.md`](3-informe-tecnico/README.md)",
            self.readme,
            "el README maestro debe enlazar el informe tecnico (report 3)")

    def test_describes_multilevel_and_dossier_integration(self):
        low = self.readme.lower()
        self.assertIn("multinivel", low,
                      "el README debe describir la estructura multinivel")
        self.assertIn("to-be/README.md", self.readme,
                      "el README debe enlazar el dossier TO-BE")

    def test_documents_the_three_skills(self):
        for skill in ("commercial-proposal-report",
                      "executive-management-report",
                      "technical-narrative-multilevel"):
            self.assertIn(skill, self.readme,
                          f"el README debe documentar el skill {skill}")

    def test_still_links_per_phase_reports_and_hilo_dorado(self):
        for fname in EXPECTED_FILENAMES.values():
            self.assertIn(f"[{fname}]({fname})", self.readme,
                          f"el README debe seguir enlazando {fname}")
        self.assertIn("Hilo Dorado", self.readme)
        for stage in ("DRV", "CAP", "BMK", "GAP", "REL", "ABB", "SBB", "WAV",
                      "ROI"):
            self.assertIn(stage, self.readme)

    def test_documents_regeneration_and_reuse(self):
        self.assertIn("python3 advisory-system/quickstart.py --phase all",
                      self.readme)
        self.assertIn("--corpus", self.readme,
                      "el README debe explicar la reutilizacion con --corpus")


class TestOCRAdapter(unittest.TestCase):
    """FEAT-001/003: OCR capability probe + honest degradation + stub 'with
    engine' path. Proves [OCR-EXTRACTED] tagging WITHOUT depending on a real
    binary (this environment has no OCR engine)."""

    def test_detect_capability_unavailable_without_raising(self):
        from engine.ocr import detect_ocr_capability, OCRCapability
        cap = detect_ocr_capability()
        self.assertIsInstance(cap, OCRCapability)
        # No OCR engine is present in this environment.
        self.assertFalse(cap.available, "no debe haber motor OCR en este entorno")
        self.assertIsNone(cap.engine)
        self.assertTrue(cap.reason, "debe reportar una razon honesta")
        # The probe reports what was looked for (modules and binaries).
        self.assertTrue(cap.probed, "debe reportar lo sondeado")
        self.assertIn("binary:tesseract", cap.probed)
        self.assertIn("module:pytesseract", cap.probed)
        # In this environment everything is missing.
        self.assertFalse(cap.probed["binary:tesseract"])
        self.assertFalse(cap.probed["module:pytesseract"])

    def test_extract_degrades_to_epistemic_void_without_engine(self):
        from engine.ocr import extract_text_via_ocr, EPISTEMIC_VOID
        text, tag = extract_text_via_ocr("/nonexistent/scan.pdf")
        self.assertEqual(text, "", "sin motor no se recupera (ni fabrica) texto")
        self.assertEqual(tag, EPISTEMIC_VOID)

    def test_extract_with_stub_engine_tags_ocr_extracted(self):
        # Inject a fake capability (available=True) and monkeypatch the engine
        # dispatcher to return fake text, proving the [OCR-EXTRACTED] path works
        # without any real binary.
        from engine import ocr
        from engine.ocr import (
            extract_text_via_ocr, OCRCapability, OCR_EXTRACTED,
        )
        fake_text = "Texto recuperado por OCR falso para la prueba."
        original_run = ocr._run_engine
        try:
            ocr._run_engine = lambda engine, path: fake_text  # type: ignore
            cap = OCRCapability(available=True, engine="pytesseract",
                                reason="stub", probed={})
            text, tag = extract_text_via_ocr("/any/scan.pdf", cap)
            self.assertEqual(text, fake_text)
            self.assertEqual(tag, OCR_EXTRACTED)
        finally:
            ocr._run_engine = original_run  # type: ignore

    def test_enrich_document_tags_ocr_extracted_with_stub(self):
        # A low-useful-text PDF enriched WITH a stub OCR engine must be tagged
        # [OCR-EXTRACTED] and carry an OCR ingestion method.
        from engine import ocr
        from engine.corpus import Document
        from engine.knowledge import enrich_document, OCR_EXTRACTED
        from engine.ocr import OCRCapability
        fake_text = (
            "Credi10 requiere integrar Siesa con CrossCore y Datacredito "
            "mediante APIs REST, con observabilidad y trazabilidad completas "
            "para la originacion, el recaudo y la cobranza del negocio."
        )
        doc = Document(
            id="scan_doc", filename="scan_doc.pdf", kind="pdf",
            role="secondary", path="/any/scan_doc.pdf",
            size=100000, sha256="deadbeef",
            extracted_text="a b c d e",  # garbage, ~0 useful text -> triggers OCR
        )
        original_run = ocr._run_engine
        try:
            ocr._run_engine = lambda engine, path: fake_text  # type: ignore
            cap = OCRCapability(available=True, engine="pytesseract",
                                reason="stub", probed={})
            enrich_document(doc, cap)
            self.assertEqual(doc.epistemic_flag, OCR_EXTRACTED,
                             "el PDF de baja cobertura con motor OCR debe "
                             "quedar [OCR-EXTRACTED]")
            self.assertIn("OCR", doc.ingestion_method)
            self.assertEqual(doc.extracted_text, fake_text,
                             "el texto OCR debe reemplazar la capa pobre")
        finally:
            ocr._run_engine = original_run  # type: ignore

    def test_enrich_document_without_engine_keeps_native_text(self):
        # Honest degradation: no engine -> native (poor) text is kept unchanged
        # and the method becomes 'OCR pendiente'; nothing is fabricated.
        from engine.corpus import Document
        from engine.knowledge import enrich_document, EPISTEMIC_VOID
        from engine.ocr import detect_ocr_capability
        doc = Document(
            id="scan2", filename="scan2.pdf", kind="pdf", role="secondary",
            path="/any/scan2.pdf", size=100000, sha256="cafebabe",
            extracted_text="a b c d e",
        )
        enrich_document(doc, detect_ocr_capability())
        self.assertEqual(doc.extracted_text, "a b c d e",
                         "sin motor OCR el texto nativo no cambia")
        self.assertEqual(doc.epistemic_flag, EPISTEMIC_VOID)
        self.assertIn("OCR pendiente", doc.ingestion_method)


class TestUsefulTextMetric(unittest.TestCase):
    """FEAT-001/003: coverage reclassification by REAL useful text."""

    def test_useful_text_helpers_behaviour(self):
        from engine.knowledge import (
            count_useful_chars, useful_text_ratio, useful_text_band,
        )
        prose = ("La arquitectura objetivo propone microservicios desacoplados "
                 "con contratos OpenAPI para las integraciones del negocio.")
        garbage = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
        prose_useful = count_useful_chars(prose)
        garbage_useful = count_useful_chars(garbage)
        self.assertGreater(prose_useful, 0)
        self.assertEqual(garbage_useful, 0,
                         "fragmentos de una sola letra no cuentan como texto util")
        # Ratio: high for prose, ~0 for garbage.
        prose_ratio = useful_text_ratio(prose_useful, len(prose))
        garbage_ratio = useful_text_ratio(garbage_useful, len(garbage))
        self.assertGreater(prose_ratio, 0.6)
        self.assertEqual(garbage_ratio, 0.0)
        # Band: prose high band, garbage nula.
        self.assertEqual(useful_text_band(prose_ratio, prose_useful), "alta")
        self.assertEqual(useful_text_band(garbage_ratio, garbage_useful), "nula")

    def test_formerly_void_pdfs_recovered_to_native_text(self):
        """FEAT-002: the PDFs once flagged [EPISTEMIC-VOID] are NOT image-only.

        The verified root cause is that these PDFs carry a real native text
        layer behind custom-encoded embedded fonts (``/ToUnicode`` CMaps). With
        the font-aware extractor their text is recovered as genuine native text,
        so they legitimately cross the useful-text threshold and become
        ``[VERIFIED-FACT]``. Nothing is fabricated: this is native-text recovery,
        not OCR. (Supersedes the earlier assumption that they were image/scan
        PDFs that could never be banded 'alta'.)
        """
        from engine.corpus import CorpusLoader
        from engine.knowledge import (
            KnowledgeBase, VERIFIED_FACT, MIN_USEFUL_RATIO_FOR_TEXT)
        kb = KnowledgeBase.from_documents(CorpusLoader(_REPO_ROOT).load())
        formerly_void = [
            "WSO2 y Studio F - Assessment Mayo2026-Final.pdf",
            "Api Integrador Atencion al cliente.pdf",
            "Originacion_API_Inspektor.pdf",
            "ProcesoCorteCartera.pdf",
            "B2C.pdf",
        ]
        for name in formerly_void:
            doc = kb.by_filename(name)
            self.assertIsNotNone(doc, f"{name} debe existir en el corpus")
            self.assertGreaterEqual(
                doc.useful_ratio, MIN_USEFUL_RATIO_FOR_TEXT,
                f"{name}: texto nativo recuperado debe superar el umbral util")
            self.assertEqual(
                doc.epistemic_flag, VERIFIED_FACT,
                f"{name}: texto nativo recuperado debe ser [VERIFIED-FACT]")
            # The recovered text must contain real Spanish words, not noise.
            self.assertTrue(
                any(tok in doc.extracted_text.lower()
                    for tok in ("arquitectura", "aplicaci", "integraci",
                                "tecnico", "componentes", "detalle")),
                f"{name}: el texto recuperado debe ser espanol legible")


class TestRequirementsTraceabilityAnnex(unittest.TestCase):
    """FEAT-002/003: annex structure on disk + dynamic (non-Credi10) extraction."""

    @classmethod
    def setUpClass(cls):
        import subprocess
        cls.out_dir = os.path.join(_REPO_ROOT, "advisory-credi10-2.0")
        cls.annex = os.path.join(
            cls.out_dir, "3-informe-tecnico",
            "anexo-a-trazabilidad-requisitos", "README.md")
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        with open(cls.annex, encoding="utf-8") as fh:
            cls.content = fh.read()
        with open(os.path.join(cls.out_dir, "3-informe-tecnico", "README.md"),
                  encoding="utf-8") as fh:
            cls.tech_readme = fh.read()

    def test_annex_file_exists(self):
        self.assertTrue(os.path.isfile(self.annex),
                        "el anexo de trazabilidad debe existir tras --phase all")

    def test_annex_has_markable_checklist_symbols(self):
        # At least one checklist symbol must be present; all three symbols are
        # legal markable states.
        has_any = any(sym in self.content
                      for sym in ("- [x]", "- [~]", "- [ ]"))
        self.assertTrue(has_any, "el anexo debe tener un checklist marcable")

    def test_annex_has_traceability_table_exact_columns(self):
        header = ("| ID | Solicitud del cliente | Cita al documento fuente | "
                  "Donde se responde (fase/seccion/entregable) | Estado | "
                  "Evidencia/Nota |")
        self.assertIn(header, self.content,
                      "la tabla debe tener las columnas exactas requeridas")
        # Explicit column-presence assertions (per acceptance criteria).
        for col in ("Cita al documento fuente",
                    "Donde se responde (fase/seccion/entregable)",
                    "Estado", "Evidencia/Nota"):
            self.assertIn(col, self.content, col)

    def test_tech_report_readme_links_annex(self):
        self.assertIn(
            "anexo-a-trazabilidad-requisitos/README.md", self.tech_readme,
            "el README del informe tecnico debe enlazar el anexo")

    def test_extraction_is_dynamic_over_synthetic_corpus(self):
        # Build a SMALL synthetic corpus distinct from Credi10 and assert the
        # generator yields THAT corpus's requests (proves not hardcoded).
        from engine.corpus import Document
        from engine.knowledge import enrich_corpus
        from phases import requirements_traceability as rt
        distinctive = (
            "1. El sistema de la Biblioteca Municipal Zunflandia debe permitir "
            "el prestamo de libros con reserva en linea y notificaciones. "
            "2. El catalogo debe integrarse con el portal ciudadano de "
            "Zunflandia mediante un API de consulta."
        )
        synth = [
            Document(
                id="rfp_zunflandia", filename="RFP_Zunflandia.pdf", kind="pdf",
                role="primary", path="/synthetic/RFP_Zunflandia.pdf",
                size=len(distinctive) * 4, sha256="0" * 64,
                extracted_text=distinctive,
            ),
        ]
        enriched = enrich_corpus(synth)
        reqs = rt.extract_requirements(enriched)
        self.assertTrue(reqs, "debe derivar solicitudes del corpus sintetico")
        blob = " ".join(r.request for r in reqs).lower()
        self.assertIn("zunflandia", blob,
                      "las solicitudes deben ser las del corpus sintetico")
        # And must NOT be the Credi10 ones.
        self.assertNotIn("credi10", blob)
        # Every request cites the synthetic source document.
        for r in reqs:
            self.assertEqual(r.source_filename, "RFP_Zunflandia.pdf")
        # The rendered annex over the synthetic corpus carries both artifacts
        # and the exact table header.
        readme = rt.build_annex_readme(reqs, total_docs=len(enriched))
        self.assertIn("| ID | Solicitud del cliente | Cita al documento fuente",
                      readme)
        self.assertTrue(
            any(sym in readme for sym in ("- [x]", "- [~]", "- [ ]")))


class TestFontAwareExtraction(unittest.TestCase):
    """Per-font ToUnicode-aware PDF extractor (FEAT-002).

    Verifies that the custom-encoded embedded fonts in the formerly-'nula' PDFs
    are decoded into legible Spanish, that the useful-text % rises strictly over
    the recorded FEAT-001 baseline, that the CMap parser maps codes correctly,
    and that extraction degrades gracefully when a font has no /ToUnicode.
    """

    @classmethod
    def setUpClass(cls):
        from engine.corpus import CorpusLoader
        from engine.knowledge import enrich_corpus
        cls.loader = CorpusLoader(_REPO_ROOT)
        cls.enriched = enrich_corpus(cls.loader.load())

    def _doc(self, needle):
        for d in self.enriched:
            if needle.lower() in d.filename.lower():
                return d
        return None

    def test_wso2_recovers_spanish_words(self):
        """The WSO2 assessment now yields legible Spanish, not font noise."""
        wso2 = self._doc("WSO2 y Studio F")
        self.assertIsNotNone(wso2, "debe descubrirse el PDF WSO2")
        low = wso2.extracted_text.lower()
        self.assertTrue(
            any(tok in low for tok in ("aplicaci", "arquitectura", "integraci")),
            "el texto recuperado de WSO2 debe contener espanol legible "
            "(aplicaci/arquitectura/integraci), ausente con el extractor viejo",
        )

    def test_second_nula_doc_recovers_spanish(self):
        """At least one other formerly-'nula' PDF also recovers Spanish."""
        found = False
        for needle in ("ProcesoCorteCartera", "B2C", "Originacion_API_Inspektor",
                       "Api Integrador"):
            d = self._doc(needle)
            if d is None:
                continue
            low = d.extracted_text.lower()
            if any(tok in low for tok in (
                    "detalle", "tecnico", "componentes", "arquitectura",
                    "funcionalidad", "proceso")):
                found = True
                break
        self.assertTrue(
            found, "al menos otro PDF antes 'nula' debe recuperar espanol real")

    def test_useful_text_strictly_above_baseline(self):
        """WSO2 and ProcesoCorteCartera useful-text % beats the FEAT-001 baseline."""
        from engine.knowledge import USEFUL_TEXT_BASELINE_PCT
        for fname in ("WSO2 y Studio F - Assessment Mayo2026-Final.pdf",
                      "ProcesoCorteCartera.pdf"):
            d = self._doc(fname.split(" - ")[0] if " - " in fname else fname)
            self.assertIsNotNone(d, f"debe descubrirse {fname}")
            before = USEFUL_TEXT_BASELINE_PCT[fname]
            now = d.useful_ratio * 100.0
            self.assertGreater(
                now, before,
                f"{fname}: texto util ahora ({now:.2f}%) debe superar "
                f"estrictamente la linea base ({before:.2f}%)")

    def test_formerly_nula_now_verified_fact(self):
        """The 5 formerly-'nula' PDFs cross the threshold -> [VERIFIED-FACT]."""
        from engine.knowledge import (
            BASELINE_NULA_PDFS, MIN_USEFUL_RATIO_FOR_TEXT, VERIFIED_FACT)
        for fname in BASELINE_NULA_PDFS:
            d = self._doc(fname.split(" - ")[0] if " - " in fname else fname)
            self.assertIsNotNone(d, f"debe descubrirse {fname}")
            self.assertGreaterEqual(d.useful_ratio, MIN_USEFUL_RATIO_FOR_TEXT,
                                    f"{fname} debe superar el umbral de texto util")
            self.assertEqual(d.epistemic_flag, VERIFIED_FACT,
                             f"{fname} debe ser texto nativo [VERIFIED-FACT]")

    def test_cmap_parser_bfchar_and_bfrange(self):
        """A tiny CMap block maps codes to unicode correctly (both forms)."""
        from engine.pdf_text import parse_tounicode_cmap
        cmap = (
            b"1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n"
            b"2 beginbfchar\n<0044> <0061>\n<0069> <00E1>\nendbfchar\n"
            b"1 beginbfrange\n<0046> <0049> <0063>\nendbfrange\n"
            b"1 beginbfrange\n<00B2> <00B2> [<2014>]\nendbfrange\n"
        )
        m = parse_tounicode_cmap(cmap)
        self.assertEqual(m.code_bytes, 2, "codespacerange <0000><FFFF> => 2 bytes")
        # bfchar pairs
        self.assertEqual(m.mapping[0x0044], "a")   # <0044> -> U+0061
        self.assertEqual(m.mapping[0x0069], "\u00E1")  # -> 'á'
        # bfrange triple: 0x46->0x63('c'), 0x47->'d', 0x48->'e', 0x49->'f'
        self.assertEqual(m.mapping[0x0046], "c")
        self.assertEqual(m.mapping[0x0047], "d")
        self.assertEqual(m.mapping[0x0049], "f")
        # bfrange array form
        self.assertEqual(m.mapping[0x00B2], "\u2014")  # em dash

    def test_two_byte_code_decoding(self):
        """2-byte codes are grouped and mapped through the font table."""
        from engine.pdf_text import (
            parse_tounicode_cmap, FontInfo, _decode_codes)
        cmap = (
            b"1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n"
            b"2 beginbfchar\n<0003> <0041>\n<0004> <0042>\nendbfchar\n"
        )
        font = FontInfo(parse_tounicode_cmap(cmap), None)
        # bytes 00 03 00 04 -> codes 0x0003, 0x0004 -> 'A','B'
        self.assertEqual(_decode_codes(b"\x00\x03\x00\x04", font), "AB")
        # Unknown 2-byte code is skipped, not emitted as noise.
        self.assertEqual(_decode_codes(b"\x00\xFF", font), "")

    def test_tolerant_no_tounicode(self):
        """A font/stream without /ToUnicode never crashes extraction."""
        from engine.pdf_text import (
            extract_pdf_text_font_aware, FontInfo, _decode_codes)
        # No mapping at all -> latin-1 clear-char fallback (no crash).
        self.assertEqual(_decode_codes(b"Hola", None), "Hola")
        self.assertEqual(_decode_codes(b"Hola", FontInfo(None, None)), "Hola")
        # A minimal PDF-ish blob with a font lacking /ToUnicode must not raise
        # and must return a (possibly empty) string.
        blob = (
            b"%PDF-1.4\n"
            b"1 0 obj<</Type/Page/Resources<</Font<</F1 2 0 R>>>>>>endobj\n"
            b"2 0 obj<</Type/Font/Subtype/TrueType/Encoding/WinAnsiEncoding>>"
            b"endobj\n"
        )
        out = extract_pdf_text_font_aware(blob)
        self.assertIsInstance(out, str)

    def test_tj_array_word_spacing(self):
        """Large negative kerning in a TJ array separates words."""
        from engine.pdf_text import _decode_tj_array
        token = b"[(Hola)-400(mundo)] TJ"
        out = _decode_tj_array(token, None)
        self.assertIn("Hola", out)
        self.assertIn("mundo", out)
        self.assertIn(" ", out, "un kerning negativo grande debe insertar espacio")


class TestBeforeAfterComparison(unittest.TestCase):
    """The regenerated coverage checklist carries the before/after comparison."""

    @classmethod
    def setUpClass(cls):
        import subprocess
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True, capture_output=True, text=True,
            timeout=600,
        )
        cls.checklist = os.path.join(_REPO_ROOT, "knowledge-base",
                                     "coverage-checklist.md")

    def test_comparison_section_present(self):
        with open(self.checklist, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("Comparacion antes/despues", text)
        self.assertIn("Texto util antes", text)
        self.assertIn("Texto util ahora", text)
        self.assertIn("pp", text, "debe haber una columna de delta en pp")
        # Honest prose on recovery and limits.
        self.assertIn("recuperados del vacio epistemico", text)
        self.assertIn("DCTDecode", text)

    def test_comparison_shows_wso2_rise(self):
        with open(self.checklist, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("WSO2 y Studio F - Assessment Mayo2026-Final.pdf", text)
        self.assertIn("1.60%", text, "la linea base de WSO2 debe aparecer")


class TestExtractionArchitecture(unittest.TestCase):
    """FEAT-003: multilayer (L1-L4) document-extraction architecture.

    Covers the generic policy skill ``document-extraction-architecture`` and
    the GENERATED advisory annex (Anexo B) under the technical report. The
    annex must be grounded in the REAL corpus coverage numbers (not abstract)
    and must separate what is implemented here (L1) from what requires the
    production environment (L2-L4).
    """

    SKILL_REL = os.path.join(
        ".kiro", "skills", "document-extraction-architecture", "SKILL.md")
    ANNEX_REL = os.path.join(
        "advisory-credi10-2.0", "3-informe-tecnico",
        "anexo-b-arquitectura-extraccion", "README.md")

    @classmethod
    def setUpClass(cls):
        import subprocess
        subprocess.run(
            [sys.executable, os.path.join(_SYSTEM_DIR, "quickstart.py"),
             "--phase", "all"],
            cwd=_REPO_ROOT, check=True, capture_output=True, text=True,
            timeout=600,
        )
        with open(os.path.join(_REPO_ROOT, cls.SKILL_REL),
                  encoding="utf-8") as fh:
            cls.skill = fh.read()
        with open(os.path.join(_REPO_ROOT, cls.ANNEX_REL),
                  encoding="utf-8") as fh:
            cls.annex = fh.read()
        master = os.path.join(_REPO_ROOT, "advisory-credi10-2.0",
                              "3-informe-tecnico", "README.md")
        with open(master, encoding="utf-8") as fh:
            cls.master_readme = fh.read()

    # -- 1. the generic skill exists with the required sections ------------- #
    def test_skill_exists_and_is_generic_policy(self):
        self.assertTrue(os.path.isfile(os.path.join(_REPO_ROOT, self.SKILL_REL)),
                        "debe existir el SKILL.md de la arquitectura de extraccion")
        self.assertIn("name: document-extraction-architecture", self.skill)
        self.assertIn("version: 1.0.0", self.skill)
        self.assertIn("owner:", self.skill)
        self.assertIn("applies_to:", self.skill)
        # Client-agnostic: Credi10 only as an EXAMPLE, never the subject.
        low = self.skill.lower()
        self.assertIn("ejemplo", low,
                      "la politica debe citar Credi10 solo como ejemplo")

    def test_skill_defines_four_layers(self):
        for layer in ("**L1**", "**L2**", "**L3**", "**L4**"):
            self.assertIn(layer, self.skill,
                          f"la politica debe definir la capa {layer}")
        self.assertIn("ToUnicode", self.skill)
        self.assertIn("OCR", self.skill)

    def test_skill_has_mermaid_tactics_table_and_epistemic_tags(self):
        self.assertIn("```mermaid", self.skill,
                      "la politica debe incluir un diagrama Mermaid")
        self.assertIn("Tipo de documento", self.skill,
                      "la politica debe incluir la tabla tactica por tipo")
        for tag in ("[VERIFIED-FACT]", "[OCR-EXTRACTED]", "[EPISTEMIC-VOID]",
                    "[DOC-ASSUMPTION]", "[DOC-CONFLICT]"):
            self.assertIn(tag, self.skill,
                          f"la politica debe gobernar la etiqueta {tag}")

    def test_skill_integrates_sibling_policies(self):
        self.assertIn("complete-corpus-ingestion", self.skill)
        self.assertIn("token-budget-optimization", self.skill)
        self.assertIn("ocr-image-extraction", self.skill)

    def test_skill_is_discovered_by_loader(self):
        from engine.skills import SkillsLoader
        names = {s.name for s in SkillsLoader(root=_REPO_ROOT).load()}
        self.assertIn("document-extraction-architecture", names)

    # -- 2. the generated annex exists, Mermaid + narrative + real figures -- #
    def test_annex_exists_with_mermaid_and_tactics_table(self):
        self.assertTrue(os.path.isfile(os.path.join(_REPO_ROOT, self.ANNEX_REL)),
                        "debe generarse el Anexo B bajo 3-informe-tecnico/")
        self.assertIn("```mermaid", self.annex,
                      "el anexo debe incluir un diagrama Mermaid")
        self.assertIn("Tipo de documento", self.annex,
                      "el anexo debe incluir la tabla tactica por tipo")

    def test_annex_has_substantial_narrative(self):
        words = _prose_word_count(self.annex)
        self.assertGreaterEqual(
            words, 400,
            f"el anexo debe tener narrativa sustancial en prosa, tiene {words}")

    def test_annex_is_grounded_in_real_before_after_figures(self):
        # Real FEAT-002 numbers, not abstract placeholders. These come from the
        # live knowledge base + the declarative baseline, so they stay in sync.
        self.assertIn("WSO2 y Studio F - Assessment Mayo2026-Final.pdf",
                      self.annex)
        self.assertIn("1.60%", self.annex,
                      "la linea base real de WSO2 debe aparecer")
        self.assertIn("69.74%", self.annex,
                      "el valor recuperado real de WSO2 debe aparecer")
        self.assertIn("pp", self.annex, "debe mostrar el delta en pp")
        # Grounded, not hardcoded: the figures match the knowledge base.
        from engine.corpus import CorpusLoader
        from engine.knowledge import KnowledgeBase
        kb = KnowledgeBase.from_documents(CorpusLoader(_REPO_ROOT).load())
        wso2 = kb.by_filename(
            "WSO2 y Studio F - Assessment Mayo2026-Final.pdf")
        self.assertIsNotNone(wso2)
        self.assertIn(f"{wso2.useful_ratio * 100.0:.2f}%", self.annex)

    def test_annex_distinguishes_implemented_l1_vs_production_l2_l4(self):
        self.assertIn("IMPLEMENTADA", self.annex,
                      "el anexo debe marcar lo implementado (L1)")
        low = self.annex.lower()
        self.assertIn("produccion", low,
                      "el anexo debe marcar lo que requiere produccion (L2-L4)")
        self.assertIn("DCTDecode", self.annex,
                      "el anexo debe nombrar el limite honesto de L1 (imagenes "
                      "DCTDecode que aun necesitan OCR real)")
        # The skill link is present.
        self.assertIn("document-extraction-architecture", self.annex)

    def test_annex_registered_in_master_index(self):
        self.assertIn("anexo-b-arquitectura-extraccion/README.md",
                      self.master_readme,
                      "el README maestro del informe tecnico debe enlazar el "
                      "Anexo B")

    # -- 3. determinism: a second annex write is byte-identical ------------- #
    def test_annex_write_is_deterministic(self):
        import tempfile
        from engine.corpus import CorpusLoader
        from engine.knowledge import KnowledgeBase
        from phases import extraction_architecture as ea
        kb = KnowledgeBase.from_documents(CorpusLoader(_REPO_ROOT).load())
        with tempfile.TemporaryDirectory() as tmp:
            first = ea.write(tmp, knowledge_base=kb)
            self.assertEqual(first, sorted(first))
            before = {p: open(p, encoding="utf-8").read() for p in first}
            second = ea.write(tmp, knowledge_base=kb)
            self.assertEqual(first, second)
            after = {p: open(p, encoding="utf-8").read() for p in second}
            self.assertEqual(before, after,
                             "el anexo debe ser byte-identico entre corridas")

    def test_annex_degrades_without_knowledge_base(self):
        # With no KB the annex still renders (baseline only), without crashing
        # and without fabricating 'now' numbers.
        from phases import extraction_architecture as ea
        body = ea.build_annex(knowledge_base=None)
        self.assertIn("```mermaid", body)
        self.assertIn("n/d", body,
                      "sin KB viva el 'ahora' se marca n/d, no se fabrica")


if __name__ == "__main__":
    unittest.main()

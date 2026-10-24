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


if __name__ == "__main__":
    unittest.main()

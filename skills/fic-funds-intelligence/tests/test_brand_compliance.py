from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class BrandComplianceTests(unittest.TestCase):
    def test_design_tokens_match_light_reference(self):
        tokens = json.loads((ROOT / "references/design-tokens.json").read_text())
        self.assertEqual(tokens["theme"], "frontera-funds")
        self.assertTrue(tokens["configurable"])
        self.assertEqual(tokens["colors"]["page"], "#FFFFFF")
        self.assertEqual(tokens["colors"]["surface"], "#F9FAFB")
        self.assertEqual(tokens["colors"]["text_primary"], "#1F2937")
        self.assertEqual(tokens["colors"]["brand_accent"], "#0BDA46")

    def test_reference_mark_is_the_outline_mark(self):
        svg = (ROOT / "assets/frontera-funds-mark.svg").read_text()
        self.assertIn('viewBox="0 0 24 24"', svg)
        self.assertIn('stroke="currentColor"', svg)
        self.assertIn('fill-opacity="0.1"', svg)
        self.assertNotIn('fill="#FFFFFF"', svg)

    def test_templates_use_light_theme_and_print_layout(self):
        for name in ("factsheet.html", "comparative.html"):
            html = (ROOT / "templates" / name).read_text()
            self.assertIn("{{THEME_CSS_VARIABLES}}", html)
            self.assertIn("{{PRINT_PAGE_SIZE}}", html)
            self.assertIn("{{BRAND_WORDMARK}}", html)
            self.assertIn("--surface", html)
            self.assertIn("@media print", html)
            self.assertIn("@media(max-width:760px)", html)
            self.assertIn('lang="es-CO"', html)

    def test_public_skill_has_no_provider_specific_mcp_wiring(self):
        skill = (ROOT / "SKILL.md").read_text().lower()
        methodology = (ROOT / "references/source-and-methodology.md").read_text().lower()
        manifest = json.loads((ROOT / "manifest.json").read_text())
        for text in (skill, methodology):
            self.assertNotIn("mcp-sfc-fics-colombia", text)
            self.assertNotIn("obtener_estado_dataset", text)
            self.assertNotIn("radiografia_fondo", text)
            self.assertNotIn("vercel.app/api/mcp", text)
        self.assertNotIn("reference_products", manifest)
        self.assertTrue(manifest["service_profile"]["commercialization"]["commercially_licensable"])
        self.assertEqual(manifest["service_profile"]["quality_gates_ref"], "standards/quality-gates.yaml")
        self.assertEqual(manifest["version"], "0.3.0")
        self.assertEqual(manifest["branding"]["default_theme"], "frontera-funds")
        self.assertTrue(manifest["branding"]["configurable"])
        self.assertEqual(manifest["report_profiles"], ["factsheet", "comparative"])

if __name__ == "__main__":
    unittest.main()

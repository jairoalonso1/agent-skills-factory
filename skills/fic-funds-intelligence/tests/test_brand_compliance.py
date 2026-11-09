from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BrandComplianceTests(unittest.TestCase):
    def test_design_tokens_match_light_reference(self):
        tokens = json.loads((ROOT / "references/design-tokens.json").read_text())
        self.assertEqual(tokens["theme"], "light-institutional")
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
            self.assertIn("--surface:#F9FAFB", html)
            self.assertIn("--green:#0BDA46", html)
            self.assertIn("@media print", html)
            self.assertIn("@media(max-width:760px)", html)
            self.assertIn('lang="es-CO"', html)


if __name__ == "__main__":
    unittest.main()

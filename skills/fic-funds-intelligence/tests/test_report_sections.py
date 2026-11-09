from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReportTemplateTests(unittest.TestCase):
    def test_factsheet_has_required_sections(self):
        html = (ROOT / "templates/factsheet.html").read_text()
        for section in (
            "Identificación del fondo", "Resumen ejecutivo",
            "Indicadores principales", "Riesgo y comportamiento",
            "Historia y distribución", "Categoría y contexto",
            "Diagnósticos y calidad de datos", "Fuentes y metodología",
        ):
            self.assertIn(section, html)

    def test_comparative_has_required_sections(self):
        html = (ROOT / "templates/comparative.html").read_text()
        for section in (
            "Resumen ejecutivo", "Alcance de la comparación",
            "Matriz comparativa", "Escala y características de los fondos",
            "Comparación de desempeño", "Comparación de riesgo",
            "Flujos y liquidez", "Conclusiones y puntos de vigilancia",
            "Fuentes y metodología",
        ):
            self.assertIn(section, html)

    def test_templates_identify_profile_and_provenance(self):
        factsheet = (ROOT / "templates/factsheet.html").read_text()
        comparative = (ROOT / "templates/comparative.html").read_text()
        self.assertIn('data-report-profile="factsheet"', factsheet)
        self.assertIn('data-report-profile="comparative"', comparative)
        for html in (factsheet, comparative):
            self.assertIn('data-provenance="frontera_skaas_generated"', html)
            self.assertIn("{{BRAND_MARK_DATA_URI}}", html)
            self.assertIn("{{CUTOFF_DATE}}", html)


if __name__ == "__main__":
    unittest.main()

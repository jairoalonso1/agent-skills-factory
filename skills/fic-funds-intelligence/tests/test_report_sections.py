from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReportTemplateTests(unittest.TestCase):
    def test_factsheet_has_required_sections_and_diagnostic_charts(self):
        html = (ROOT / "templates/factsheet.html").read_text()
        for section in ("Identificación del fondo", "Resumen ejecutivo", "Indicadores principales", "Riesgo y comportamiento", "Historia y distribución", "Historial de drawdown", "Volatilidad anualizada móvil (30 observaciones)", "Categoría y contexto", "Diagnósticos y calidad de datos", "Fuentes y metodología"):
            self.assertIn(section, html)
        self.assertIn("{{DRAWDOWN_CHART_SVG}}", html)
        self.assertIn("{{ROLLING_VOLATILITY_30_OBSERVATIONS_CHART_SVG}}", html)

    def test_comparative_has_required_sections_and_aligned_diagnostics(self):
        html = (ROOT / "templates/comparative.html").read_text()
        for section in ("Resumen ejecutivo", "Alcance de la comparación", "Matriz comparativa", "Escala y características de los fondos", "Comparación de desempeño", "Comparación de riesgo", "Comparación de drawdown", "Volatilidad anualizada móvil (30 observaciones)", "Flujos y liquidez", "Conclusiones y puntos de vigilancia", "Fuentes y metodología"):
            self.assertIn(section, html)
        self.assertIn("{{ALIGNED_DRAWDOWN_CHART_SVG}}", html)
        self.assertIn("{{ALIGNED_ROLLING_VOLATILITY_30_OBSERVATIONS_CHART_SVG}}", html)

    def test_templates_identify_profile_provenance_and_source_line(self):
        for profile in ("factsheet", "comparative"):
            html = (ROOT / "templates" / f"{profile}.html").read_text()
            self.assertIn(f'data-report-profile=\"{profile}\"', html)
            self.assertIn('data-provenance=\"frontera_skaas_generated\"', html)
            self.assertIn("{{BRAND_MARK_DATA_URI}}", html)
            self.assertIn("{{CUTOFF_DATE}}", html)
            self.assertIn("{{SOURCE_ATTRIBUTION}}", html)

if __name__ == "__main__":
    unittest.main()

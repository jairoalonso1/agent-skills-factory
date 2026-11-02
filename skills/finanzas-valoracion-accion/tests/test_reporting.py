import json
from pathlib import Path
from zipfile import ZipFile
from openpyxl import load_workbook
from docx import Document
from pptx import Presentation
from scripts.reporting import generate_research_deliverables


def test_all_standard_deliverables_are_created_and_readable(tmp_path):
    package={"issuer":"Example plc","ticker":"EXM","exchange":"LSE","valuation_date":"2026-10-31",
      "current_price":42.5,"reporting_currency":"USD","rating":"NOT RATED",
      "investment_thesis":{"summary":"Illustrative only"},"financials":{"revenue":100},
      "industry":{"peers":["A","B"]},"valuation":{"method":"DCF"},
      "scenarios":{"bear":{"target_price":8},"base":{"target_price":10},"bull":{"target_price":12}},
      "risks":["Illustrative risk"],"sources":[{"source_id":"S1","title":"Example source"}]}
    paths=generate_research_deliverables(package,tmp_path,"example")
    assert set(paths)=={"html","xlsx","docx","pptx"}
    for path in paths.values(): assert Path(path).is_file() and Path(path).stat().st_size > 500
    html=Path(paths["html"]).read_text(encoding="utf-8")
    assert "Desempeño financiero y calidad de resultados" in html and "Created by Jairo Alonso González" in html
    wb=load_workbook(paths["xlsx"],read_only=True)
    assert "Executive Summary" in wb.sheetnames and "Valuation" in wb.sheetnames
    assert wb["Executive Summary"]["A1"].value.startswith("Institutional Equity Research")
    doc=Document(paths["docx"])
    assert any("Tesis de inversión" in p.text for p in doc.paragraphs)
    prs=Presentation(paths["pptx"])
    assert len(prs.slides) >= 8
    assert "Example plc" in prs.slides[0].shapes.title.text


def test_html_uses_institutional_layout_and_semantic_values(tmp_path):
    from scripts.reporting import build_html_report
    package = {
        "issuer": "Example plc", "ticker": "EXM", "exchange": "LSE",
        "valuation_date": "2026-10-31", "current_price": 42.5,
        "reporting_currency": "USD", "rating": "HOLD / NEUTRAL",
        "expected_total_return": 0.075,
        "investment_thesis": {"summary": "A sourced thesis with <caution> material risks."},
        "financials": {"revenue": 1000, "revenue_growth": 0.12, "roic": 0.14},
        "valuation": {"method": "DCF", "wacc": 0.09, "intrinsic_value_per_share": 48.0},
        "scenarios": {
            "bear": {"target_price": 30.0, "probability": 0.25, "drivers": ["Lower growth"]},
            "base": {"target_price": 48.0, "probability": 0.5, "drivers": ["Central case"]},
            "bull": {"target_price": 60.0, "probability": 0.25, "drivers": ["Higher growth"]},
        },
        "sources": [{"source_id": "S1", "publisher": "Issuer", "title": "Annual report", "url": "https://example.com/report"}],
    }
    out = Path(build_html_report(package, tmp_path / "report.html"))
    rendered = out.read_text(encoding="utf-8")
    assert '<html lang="es">' in rendered
    assert 'class="hero"' in rendered and 'class="decision neutral"' in rendered
    assert 'class="kpi-grid"' in rendered and 'Precio actual' in rendered
    assert '14.00%' in rendered and '9.00%' in rendered and '12.00%' in rendered
    assert 'Escenarios de inversión' in rendered and 'Escenario base' in rendered
    assert 'Desempeño financiero y calidad de resultados' in rendered
    assert '&lt;caution&gt;' in rendered and '<caution>' not in rendered
    assert 'application/json' not in rendered and '<pre>' not in rendered
    assert 'Created by Jairo Alonso González' in rendered
    assert '@media(max-width:700px)' in rendered and '@media print' in rendered


def test_pptx_brand_is_visible_on_slides(tmp_path):
    from scripts.reporting import build_pptx_briefing
    package = {"issuer": "Example plc", "ticker": "EXM", "investment_thesis": {"summary": "Synthetic"}}
    path = build_pptx_briefing(package, tmp_path / "brand.pptx")
    prs = Presentation(path)
    visible = [shape.text for slide in prs.slides for shape in slide.shapes if getattr(shape, "has_text_frame", False)]
    assert any("Created by Jairo Alonso González" in text for text in visible)



def test_chart_assets_are_embedded_in_all_four_deliverables(tmp_path):
    package = {
        "issuer": "Chart Test plc", "ticker": "CHT", "exchange": "LSE",
        "valuation_date": "2026-10-31", "current_price": 42.5,
        "security_currency": "GBP", "reporting_currency": "USD", "rating": "HOLD / NEUTRAL",
        "financials": {"revenue": 1000, "ebitda": 180},
        "valuation": {"method": "DCF"},
        "scenarios": {
            "bear": {"target_price": 30, "drivers": ["Lower growth"]},
            "base": {"target_price": 45, "drivers": ["Central case"]},
            "bull": {"target_price": 60, "drivers": ["Higher growth"]},
        },
        "risks": ["Execution"], "sources": [],
        "chart_data": {
            "valuation_ranges": {"DCF": {"Bear": 30, "Base": 45, "Bull": 60}},
            "dcf_sensitivity": {
                "wacc_values": [0.08, 0.09], "terminal_growth_values": [0.02, 0.025],
                "grid_per_share": {"0.08": {"0.02": 48, "0.025": 52}, "0.09": {"0.02": 42, "0.025": 45}},
            },
            "price_history": [
                {"Date": "2026-10-28", "Close": 40, "SMA_50": 38},
                {"Date": "2026-10-29", "Close": 41, "SMA_50": 38.5},
                {"Date": "2026-10-30", "Close": 42.5, "SMA_50": 39},
            ],
        },
    }
    paths = generate_research_deliverables(package, tmp_path, "charts")
    html = Path(paths["html"]).read_text(encoding="utf-8")
    assert html.count("data:image/png;base64,") == 3
    wb = load_workbook(paths["xlsx"])
    assert "Charts" in wb.sheetnames and len(wb["Charts"]._images) == 3
    assert len(wb["Financials"]._cells) > 0
    doc = Document(paths["docx"])
    assert len(doc.inline_shapes) == 3
    prs = Presentation(paths["pptx"])
    picture_count = sum(1 for slide in prs.slides for shape in slide.shapes if shape.shape_type == 13)
    assert picture_count == 3
    assert "Moneda del título: GBP" in html and "Moneda de reporte: USD" in html


def test_xlsx_preserves_financial_values_as_numeric_cells(tmp_path):
    from scripts.reporting import build_xlsx_workbook
    package = {"issuer": "Numeric plc", "reporting_currency": "USD", "financials": {"revenue": 1234.5, "margin": 0.2}}
    path = build_xlsx_workbook(package, tmp_path / "numeric.xlsx")
    wb = load_workbook(path, data_only=False)
    sheet = wb["Financials"]
    assert sheet["A4"].value == "revenue"
    assert sheet["B4"].value == 1234.5
    assert isinstance(sheet["B4"].value, (int, float))


def test_non_estimated_scenario_is_rendered_without_fabricated_target(tmp_path):
    from scripts.reporting import build_html_report
    from scripts.research_quality import validate_research_package
    package = {
        "issuer": "Insufficient plc", "valuation_date": "2026-10-31", "reporting_currency": "USD",
        "financials": {"revenue": 100}, "valuation": {"method": "Not estimated", "reason": "Insufficient evidence to support a defensible valuation."},
        "scenarios": {
            "bear": {"status": "not_estimated"},
            "base": {"status": "not_estimated"},
            "bull": {"status": "not_estimated"},
        },
        "risks": ["Insufficient operating history"],
        "sources": [{"source_id": "S1", "publisher": "Issuer", "title": "Filing", "url": "https://example.com/filing", "published_at": "2026-10-30", "retrieved_at": "2026-10-31T12:00:00Z", "evidence_type": "reported"}],
    }
    quality = validate_research_package(package)
    assert quality["passed"] is True
    html = Path(build_html_report(package, tmp_path / "not-estimated.html")).read_text(encoding="utf-8")
    assert "No estimado" in html
    assert "Precio objetivo" in html

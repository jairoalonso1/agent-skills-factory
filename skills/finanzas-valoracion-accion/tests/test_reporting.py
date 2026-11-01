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

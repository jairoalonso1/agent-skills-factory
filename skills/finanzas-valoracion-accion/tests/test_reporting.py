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
    assert "Financial performance and quality" in html and "Created by Jairo Alonso González" in html
    wb=load_workbook(paths["xlsx"],read_only=True)
    assert "Executive Summary" in wb.sheetnames and "Valuation" in wb.sheetnames
    assert wb["Executive Summary"]["A1"].value.startswith("Institutional Equity Research")
    doc=Document(paths["docx"])
    assert any("Investment thesis" in p.text for p in doc.paragraphs)
    prs=Presentation(paths["pptx"])
    assert len(prs.slides) >= 8
    assert "Example plc" in prs.slides[0].shapes.title.text

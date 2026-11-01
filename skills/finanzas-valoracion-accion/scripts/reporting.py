"""Generate consistent institutional equity-research deliverables.

Input is a structured, analyst-reviewed research package. This module formats
provided information; it never fetches data or invents financial conclusions.
"""
from __future__ import annotations
import html
import json
from pathlib import Path
from typing import Any

AUTHOR_SIGNATURE = "Created by Jairo Alonso González"
SECTIONS = (
    ("investment_thesis", "Investment thesis"),
    ("industry", "Business, industry and peers"),
    ("financials", "Financial performance and quality"),
    ("valuation", "Valuation methodology and results"),
    ("scenarios", "Bear / Base / Bull scenarios"),
    ("risks", "Risks and thesis invalidation"),
    ("assumptions", "Key assumptions and limitations"),
    ("data_gaps", "Data gaps"),
    ("sources", "Sources and evidence"),
)


def _summary_lines(package: dict[str, Any]) -> list[str]:
    return [
        f"Ticker: {package.get('ticker', 'Not provided')} | Exchange: {package.get('exchange', 'Not provided')}",
        f"Valuation date: {package.get('valuation_date', 'Not provided')} | Currency: {package.get('reporting_currency', 'Not provided')}",
        f"Current price: {package.get('current_price', 'Not provided')} | Rating: {package.get('rating', 'NOT RATED')}",
    ]


def _display(value: Any) -> str:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, indent=2, default=str)
    if value is None:
        return "Not provided"
    return str(value)


def _rows(value: Any) -> list[tuple[str, Any]]:
    if isinstance(value, dict):
        return [(str(k), v) for k, v in value.items()]
    if isinstance(value, list):
        return [(f"{i + 1}", item) for i, item in enumerate(value)]
    return [("Value", value)]


def _html_section(title: str, value: Any) -> str:
    rows = _rows(value)
    if not rows:
        return f"<section><h2>{html.escape(title)}</h2><p>Not provided</p></section>"
    body = "".join(
        "<tr><th>" + html.escape(k) + "</th><td><pre>" + html.escape(_display(v)) + "</pre></td></tr>"
        for k, v in rows
    )
    return f"<section><h2>{html.escape(title)}</h2><table>{body}</table></section>"


def build_html_report(package: dict[str, Any], output_path: str | Path) -> str:
    issuer = html.escape(str(package.get("issuer", "Issuer not provided")))
    summary = "".join(f"<li>{html.escape(x)}</li>" for x in _summary_lines(package))
    sections = "".join(_html_section(title, package.get(key, {})) for key, title in SECTIONS)
    thesis = package.get("investment_thesis", {})
    thesis_summary = thesis.get("summary", "Thesis summary not provided") if isinstance(thesis, dict) else "Thesis summary not provided"
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Institutional Equity Research — {issuer}</title><style>
:root{{font-family:Arial,sans-serif;color:#172033;background:#f6f8fb}}body{{max-width:1120px;margin:36px auto;padding:0 24px;line-height:1.5}}header,.panel{{background:white;border:1px solid #dce3eb;border-radius:10px;padding:22px;margin:16px 0}}h1,h2{{color:#173b5e}}h2{{border-bottom:1px solid #dce3eb;padding-bottom:8px}}table{{border-collapse:collapse;width:100%}}th,td{{border-bottom:1px solid #e6ebf0;padding:10px;text-align:left;vertical-align:top}}th{{width:24%;color:#344b63}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.45 Consolas,monospace;margin:0}}.brand{{color:#64748b;border-top:1px solid #dce3eb;padding-top:12px;margin-top:28px}}
</style></head><body><header><h1>Institutional Equity Research — {issuer}</h1><ul>{summary}</ul><p>{html.escape(str(thesis_summary))}</p></header>{sections}<p class="brand">{AUTHOR_SIGNATURE}</p></body></html>"""
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(doc, encoding="utf-8")
    return str(path)


def build_xlsx_workbook(package: dict[str, Any], output_path: str | Path) -> str:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = Workbook(); summary = wb.active; summary.title = "Executive Summary"
    summary.append([f"Institutional Equity Research — {package.get('issuer', 'Issuer not provided')}"])
    summary.append([AUTHOR_SIGNATURE]); summary.append(["Field", "Value"])
    for key, value in (("Ticker", package.get("ticker")), ("Exchange", package.get("exchange")),
                       ("Valuation date", package.get("valuation_date")), ("Currency", package.get("reporting_currency")),
                       ("Current price", package.get("current_price")), ("Rating", package.get("rating", "NOT RATED")),
                       ("Investment thesis", package.get("investment_thesis", {}).get("summary") if isinstance(package.get("investment_thesis"), dict) else None)):
        summary.append([key, _display(value)])
    sheet_names = {"investment_thesis": "Thesis", "industry": "Industry & Peers", "financials": "Financials",
                   "valuation": "Valuation", "scenarios": "Scenarios", "risks": "Risks",
                   "assumptions": "Assumptions", "data_gaps": "Data Gaps", "sources": "Sources"}
    for key, title in SECTIONS:
        sheet = wb.create_sheet(sheet_names[key])
        sheet.append([title]); sheet.append([AUTHOR_SIGNATURE]); sheet.append(["Field", "Value"])
        for field, value in _rows(package.get(key, {})):
            sheet.append([field, _display(value)])
    for sheet in wb.worksheets:
        sheet.freeze_panes = "A4"
        sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=2)
        sheet.cell(1,1).font = Font(bold=True, size=14, color="FFFFFF")
        sheet.cell(1,1).fill = PatternFill("solid", fgColor="173B5E")
        sheet.cell(2,1).font = Font(italic=True, color="526579")
        for cell in sheet[3]:
            cell.font = Font(bold=True, color="173B5E")
            cell.fill = PatternFill("solid", fgColor="DCE6F1")
        for row in sheet.iter_rows():
            for cell in row: cell.alignment = Alignment(vertical="top", wrap_text=True)
        for col in sheet.columns:
            width = min(max(max(len(str(c.value or "")) for c in col) + 2, 14), 65)
            sheet.column_dimensions[get_column_letter(col[0].column)].width = width
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True); wb.save(path)
    return str(path)


def build_docx_report(package: dict[str, Any], output_path: str | Path) -> str:
    from docx import Document
    from docx.shared import Inches, Pt
    doc = Document(); section = doc.sections[0]
    section.top_margin = Inches(.65); section.bottom_margin = Inches(.65)
    doc.add_heading(f"Institutional Equity Research — {package.get('issuer', 'Issuer not provided')}", 0)
    p = doc.add_paragraph(AUTHOR_SIGNATURE); p.runs[0].italic = True
    for line in _summary_lines(package): doc.add_paragraph(line)
    thesis = package.get("investment_thesis", {})
    if isinstance(thesis, dict) and thesis.get("summary"):
        doc.add_heading("Investment overview", level=1); doc.add_paragraph(str(thesis["summary"]))
    for key, title in SECTIONS:
        value = package.get(key, {})
        doc.add_heading(title, level=1)
        rows = _rows(value)
        if not rows:
            doc.add_paragraph("Not provided")
        elif isinstance(value, list):
            for _, item in rows: doc.add_paragraph(_display(item), style="List Bullet")
        else:
            table = doc.add_table(rows=0, cols=2); table.style = "Light Shading Accent 1"
            for field, item in rows:
                cells = table.add_row().cells; cells[0].text = field; cells[1].text = _display(item)
    for style in doc.styles:
        if style.type == 1: style.font.name = "Aptos"; style.font.size = Pt(9)
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True); doc.save(path)
    return str(path)


def build_pptx_briefing(package: dict[str, Any], output_path: str | Path) -> str:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    def add_slide(title: str, lines: list[str]):
        slide = prs.slides.add_slide(prs.slide_layouts[1]); slide.shapes.title.text = title
        frame = slide.placeholders[1].text_frame; frame.clear()
        for i, line in enumerate(lines[:8]):
            para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
            para.text = line; para.font.size = Pt(18)
        slide.notes_slide.notes_text_frame.text = AUTHOR_SIGNATURE
    add_slide(f"Equity Research — {package.get('issuer', 'Issuer not provided')}", _summary_lines(package))
    for key, title in SECTIONS:
        value = package.get(key, {})
        lines = [f"{field}: {_display(item).replace(chr(10), ' ')[:220]}" for field, item in _rows(value)]
        add_slide(title, lines or ["Not provided"])
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True); prs.save(path)
    return str(path)


def generate_research_deliverables(package: dict[str, Any], output_dir: str | Path,
                                   basename: str | None = None) -> dict[str, str]:
    """Generate all four standard formats from one structured package."""
    safe_name = basename or "equity-research"
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    return {
        "html": build_html_report(package, out / f"{safe_name}.html"),
        "xlsx": build_xlsx_workbook(package, out / f"{safe_name}.xlsx"),
        "docx": build_docx_report(package, out / f"{safe_name}.docx"),
        "pptx": build_pptx_briefing(package, out / f"{safe_name}.pptx"),
    }

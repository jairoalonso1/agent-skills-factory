"""Generate consistent institutional equity-research deliverables.

Input is a structured, analyst-reviewed research package. This module formats
provided information; it never fetches data or invents financial conclusions.
"""
from __future__ import annotations
import base64
import html
import json
from pathlib import Path
from typing import Any

AUTHOR_SIGNATURE = "Created by Jairo Alonso González"
SECTIONS = (
    ("investment_thesis", "Tesis de inversión"),
    ("industry", "Negocio, industria y empresas comparables"),
    ("financials", "Desempeño financiero y calidad de resultados"),
    ("valuation", "Metodología y resultados de valoración"),
    ("scenarios", "Escenarios bajista, base y alcista"),
    ("risks", "Riesgos y condiciones que invalidan la tesis"),
    ("assumptions", "Supuestos y limitaciones"),
    ("data_gaps", "Vacíos de información"),
    ("sources", "Fuentes y evidencia"),
)


def _summary_lines(package: dict[str, Any]) -> list[str]:
    return [
        f"Ticker: {package.get('ticker', 'No disponible')} | Bolsa: {package.get('exchange', 'No disponible')}",
        f"Fecha de valoración: {package.get('valuation_date', 'No disponible')} | Moneda de reporte: {package.get('reporting_currency', 'No disponible')}",
        f"Moneda del título: {package.get('security_currency', package.get('valuation_currency', package.get('reporting_currency', 'No disponible')))} | Precio actual: {package.get('current_price', 'No disponible')} | Recomendación: {package.get('rating', 'NOT RATED')}",
    ]


_LABELS = {
    "summary": "Resumen ejecutivo", "catalysts": "Catalizadores", "invalidation_conditions": "Condiciones que invalidan la tesis",
    "sector": "Sector", "business": "Modelo de negocio", "peer_selection_basis": "Criterios de selección de comparables",
    "peers": "Empresas comparables", "revenue": "Ingresos", "revenue_growth": "Crecimiento de ingresos",
    "gross_margin": "Margen bruto", "ebit_margin": "Margen EBIT", "ebitda_margin": "Margen EBITDA",
    "net_income": "Utilidad neta", "free_cash_flow": "Flujo de caja libre", "roic": "ROIC", "roe": "ROE",
    "wacc": "WACC", "cost_of_equity": "Costo del patrimonio", "terminal_growth": "Crecimiento terminal",
    "current_price": "Precio actual", "target_price": "Precio objetivo", "intrinsic_value_per_share": "Valor intrínseco por acción",
    "expected_total_return": "Retorno total esperado", "probability_weighted_target": "Precio objetivo ponderado por probabilidad",
    "method": "Metodología", "methods_used": "Métodos utilizados", "methods_excluded": "Métodos excluidos",
    "assumptions": "Supuestos", "drivers": "Factores determinantes", "probability": "Probabilidad",
    "bear": "Escenario bajista", "base": "Escenario base", "bull": "Escenario alcista",
    "risks": "Riesgos", "data_gaps": "Vacíos de información", "sources": "Fuentes y evidencia",
    "publisher": "Editor / entidad", "title": "Título", "url": "Enlace", "published_at": "Fecha de publicación",
    "retrieved_at": "Fecha de consulta", "evidence_type": "Tipo de evidencia", "period": "Periodo",
    "notes": "Notas", "source_id": "ID de fuente", "rating": "Recomendación", "valuation_date": "Fecha de valoración",
    "reporting_currency": "Moneda de reporte", "exchange": "Bolsa", "ticker": "Ticker", "issuer": "Emisor",
    "current_price": "Precio actual", "financials": "Información financiera", "valuation": "Valoración",
    "industry": "Negocio, industria y comparables", "investment_thesis": "Tesis de inversión",
    "scenarios": "Escenarios de valoración", "assumptions": "Supuestos y limitaciones",
    "not_estimated": "No estimado", "not_available": "No disponible", "not_applicable": "No aplica",
}


def _label(value: Any) -> str:
    raw = str(value).replace("_", " ").strip()
    return _LABELS.get(str(value), raw[:1].upper() + raw[1:])


def _fmt(value: Any, key: str = "") -> str:
    if value is None:
        return "No disponible"
    if isinstance(value, bool):
        return "Sí" if value else "No"
    if isinstance(value, float):
        pct_keys = ("margin", "growth", "return", "yield", "wacc", "rate", "probability", "roic", "roe", "irr", "upside", "downside")
        if any(token in key.lower() for token in pct_keys) and -1.5 <= value <= 2:
            return f"{value:.2%}"
        return f"{value:,.2f}" if abs(value) < 1000 else f"{value:,.1f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def _render_value(value: Any, key: str = "") -> str:
    if value is None:
        return '<span class="muted">No disponible</span>'
    if isinstance(value, dict):
        if not value:
            return '<span class="muted">No disponible</span>'
        rows = "".join(f'<tr><th>{html.escape(_label(k))}</th><td>{_render_value(v, str(k))}</td></tr>' for k, v in value.items())
        return f'<table class="detail-table"><tbody>{rows}</tbody></table>'
    if isinstance(value, (list, tuple)):
        if not value:
            return '<span class="muted">No disponible</span>'
        if all(not isinstance(x, (dict, list, tuple)) for x in value):
            return '<ul class="clean-list">' + ''.join(f'<li>{html.escape(_fmt(x, key))}</li>' for x in value) + '</ul>'
        if all(isinstance(x, dict) for x in value):
            keys = list(dict.fromkeys(k for item in value for k in item.keys()))
            head = ''.join(f'<th>{html.escape(_label(k))}</th>' for k in keys)
            body = ''.join('<tr>' + ''.join(f'<td>{_render_value(item.get(k), str(k))}</td>' for k in keys) + '</tr>' for item in value)
            return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
        return '<ul class="clean-list">' + ''.join(f'<li>{_render_value(x, key)}</li>' for x in value) + '</ul>'
    if isinstance(value, str) and value.startswith(('https://', 'http://')):
        safe = html.escape(value, quote=True)
        return f'<a href="{safe}" target="_blank" rel="noopener noreferrer">Consultar fuente ↗</a>'
    return html.escape(_fmt(value, key))


def _section_card(title: str, value: Any, key: str) -> str:
    if value in (None, {}, []):
        return ""
    content = _render_value(value, key)
    return f'<section class="card"><h2>{html.escape(title)}</h2>{content}</section>'


def _metric_cards(package: dict[str, Any]) -> str:
    financials = package.get("financials") if isinstance(package.get("financials"), dict) else {}
    valuation = package.get("valuation") if isinstance(package.get("valuation"), dict) else {}
    thesis = package.get("investment_thesis") if isinstance(package.get("investment_thesis"), dict) else {}
    target = package.get("target_price") or package.get("probability_weighted_target") or valuation.get("target_price") or valuation.get("probability_weighted_target")
    expected_return = package.get("expected_total_return") if package.get("expected_total_return") is not None else thesis.get("expected_total_return")
    wacc = package.get("wacc") if package.get("wacc") is not None else valuation.get("wacc")
    if isinstance(wacc, dict):
        wacc = wacc.get("value")
    candidates = [
        ("Precio actual", package.get("current_price"), package.get("security_currency", package.get("valuation_currency", package.get("reporting_currency", ""))), "price"),
        ("Precio objetivo", target, package.get("security_currency", package.get("valuation_currency", package.get("reporting_currency", ""))), "price"),
        ("Retorno total esperado", expected_return, "", "return"),
        ("ROIC", package.get("roic") if package.get("roic") is not None else financials.get("roic"), "", "roic"),
        ("WACC", wacc, "", "wacc"),
        ("Crecimiento de ingresos", financials.get("revenue_growth"), "", "growth"),
    ]
    cards = []
    for label, value, unit, fmt_key in candidates:
        if value is None:
            continue
        shown = _fmt(value, fmt_key)
        if unit and fmt_key == "price":
            shown = f"{unit} {shown}"
        cards.append(f'<div class="kpi"><div class="kpi-label">{html.escape(label)}</div><div class="kpi-value">{html.escape(shown)}</div></div>')
    return '<div class="kpi-grid">' + ''.join(cards) + '</div>' if cards else ''


def _scenario_matrix(scenarios: Any, currency: str) -> str:
    if not isinstance(scenarios, dict) or not any(k in scenarios for k in ("bear", "base", "bull")):
        return ""
    rows = []
    for key in ("bear", "base", "bull"):
        item = scenarios.get(key)
        if not isinstance(item, dict):
            continue
        price = item.get("target_price", item.get("price_target", item.get("value_per_share")))
        prob = item.get("probability")
        status = item.get("status", "not_available" if price is None else "estimated")
        drivers = item.get("drivers", [])
        price_text = f"{currency} {_fmt(price)}" if price is not None else _label(status)
        rows.append(f'<tr><th>{html.escape(_label(key))}</th><td class="numeric">{html.escape(price_text)}</td><td class="numeric">{html.escape(_fmt(prob, "probability")) if prob is not None else "No disponible"}</td><td>{_render_value(drivers, "drivers")}</td></tr>')
    if not rows:
        return ""
    return '<section class="card"><h2>Escenarios de inversión</h2><div class="table-wrap"><table><thead><tr><th>Escenario</th><th class="numeric">Precio objetivo</th><th class="numeric">Probabilidad</th><th>Factores determinantes</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div></section>'


def _flatten_rows(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    """Flatten nested package data into typed spreadsheet cells, not JSON text."""
    rows: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            label = f"{prefix}.{key}" if prefix else str(key)
            rows.extend(_flatten_rows(item, label))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value, 1):
            label = f"{prefix}[{index}]" if prefix else str(index)
            rows.extend(_flatten_rows(item, label))
    else:
        rows.append((prefix or "Value", value))
    return rows


def _build_chart_assets(package: dict[str, Any], output_dir: Path) -> dict[str, str]:
    """Create only charts backed by explicit chart_data in the canonical package."""
    data = package.get("chart_data")
    if not isinstance(data, dict) or not data:
        return {}
    from .charts import football_field, dcf_sensitivity_heatmap, price_technical_chart
    chart_dir = output_dir / "charts"
    assets: dict[str, str] = {}
    ranges = data.get("valuation_ranges")
    if ranges:
        if not isinstance(ranges, dict) or not package.get("current_price"):
            raise ValueError("chart_data.valuation_ranges requires ranges and a positive current_price")
        assets["valuation_ranges"] = football_field(ranges, float(package["current_price"]), str(chart_dir / "valuation-football-field.png"))
    sensitivity = data.get("dcf_sensitivity")
    if sensitivity:
        assets["dcf_sensitivity"] = dcf_sensitivity_heatmap(sensitivity, str(chart_dir / "dcf-sensitivity.png"))
    history = data.get("price_history")
    if history:
        if not isinstance(history, list) or not all(isinstance(row, dict) for row in history):
            raise ValueError("chart_data.price_history must be a list of row objects")
        import pandas as pd
        frame = pd.DataFrame(history)
        if not {"Date", "Close"}.issubset(frame.columns):
            raise ValueError("chart_data.price_history requires Date and Close columns")
        assets["price_history"] = price_technical_chart(frame, str(package.get("ticker", "Security")), str(chart_dir / "price-technical-context.png"))
    return assets


def _chart_relative_path(path: str, output_dir: Path) -> str:
    return Path(path).relative_to(output_dir).as_posix()


def build_html_report(package: dict[str, Any], output_path: str | Path, chart_paths: dict[str, str] | None = None) -> str:
    issuer = html.escape(str(package.get("issuer", "Emisor no identificado")))
    ticker = html.escape(str(package.get("ticker", "—")))
    exchange = html.escape(str(package.get("exchange", "—")))
    date = html.escape(str(package.get("valuation_date", "—")))
    currency = str(package.get("security_currency", package.get("valuation_currency", package.get("reporting_currency", ""))))
    chart_paths = chart_paths or {}
    rating = str(package.get("rating", "NOT RATED")).upper()
    thesis = package.get("investment_thesis", {})
    thesis_summary = thesis.get("summary") if isinstance(thesis, dict) else None
    if not thesis_summary:
        thesis_summary = "El informe presenta la evidencia, los supuestos y los resultados disponibles a la fecha de valoración."
    rating_class = "positive" if any(x in rating for x in ("BUY", "COMPRA")) else "negative" if any(x in rating for x in ("SELL", "VENTA")) else "neutral"
    summary_metrics = _metric_cards(package)
    sections = []
    if chart_paths:
        chart_titles = {"valuation_ranges": "Rango de valoración", "dcf_sensitivity": "Sensibilidad del DCF", "price_history": "Precio y contexto técnico"}
        for chart_key, chart_path in chart_paths.items():
            encoded = base64.b64encode(Path(chart_path).read_bytes()).decode("ascii")
            sections.append(f'<section class="card chart-card"><h2>{html.escape(chart_titles.get(chart_key, chart_key))}</h2><img src="data:image/png;base64,{encoded}" alt="{html.escape(chart_titles.get(chart_key, chart_key), quote=True)}" style="display:block;width:100%;height:auto;max-height:620px;object-fit:contain"></section>')
    for key, title in SECTIONS:
        if key == "scenarios":
            matrix = _scenario_matrix(package.get(key), currency)
            if matrix:
                sections.append(matrix)
                continue
        sections.append(_section_card(title, package.get(key), key))
    source_note = "Los resultados dependen de la calidad, cobertura y fecha de corte de las fuentes y de los supuestos declarados."
    doc = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Informe institucional de análisis fundamental y valoración de acciones.">
<title>{ticker} | Investigación de renta variable — {issuer}</title>
<style>
:root{{--navy:#102a43;--blue:#176b87;--gold:#c28b2c;--bg:#f2f5f8;--card:#fff;--border:#d9e2ec;--text:#243b53;--muted:#627d98;--soft:#eaf1f6;--green:#237a57;--red:#a33a3a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}.container{{max-width:1380px;margin:0 auto;padding:28px 30px 40px}}
.hero{{background:linear-gradient(120deg,#102a43 0%,#176b87 100%);color:#fff;border-radius:14px;padding:28px 32px;display:flex;justify-content:space-between;align-items:center;gap:24px;box-shadow:0 8px 24px rgba(16,42,67,.16)}}.eyebrow{{font-size:11px;text-transform:uppercase;letter-spacing:1.4px;color:#c8dce8;font-weight:700}}h1{{font-size:25px;line-height:1.25;margin:7px 0 5px;color:#fff}}.meta{{color:#d8e6ee;font-size:13px}}.decision{{min-width:250px;text-align:right;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);padding:15px 18px;border-radius:10px}}.decision .rating{{font-size:18px;font-weight:800;letter-spacing:.3px}}.decision .sub{{font-size:12px;color:#e1edf3;margin-top:4px}}.decision.positive{{border-left:5px solid #5cc69a}}.decision.negative{{border-left:5px solid #e58c8c}}.decision.neutral{{border-left:5px solid #e1b85b}}
.lead{{font-size:15px;margin:18px 2px 20px;max-width:1100px}}.kpi-grid{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:18px 0 22px}}.kpi{{background:var(--card);border:1px solid var(--border);border-top:4px solid var(--blue);border-radius:9px;padding:13px 15px;min-width:0;box-shadow:0 2px 7px rgba(16,42,67,.035)}}.kpi-label{{font-size:10px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted);font-weight:700}}.kpi-value{{font-size:20px;font-weight:750;color:var(--navy);margin-top:4px;overflow-wrap:anywhere;font-variant-numeric:tabular-nums}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px 22px;margin:0 0 17px;box-shadow:0 2px 8px rgba(16,42,67,.035);break-inside:avoid}}h2{{font-size:14px;color:var(--navy);text-transform:uppercase;letter-spacing:.55px;border-bottom:2px solid var(--blue);padding-bottom:9px;margin:0 0 14px}}.detail-table,table{{width:100%;border-collapse:collapse;font-size:12.5px}}th{{background:#edf3f7;color:var(--navy);font-weight:700;text-align:left;width:25%}}th,td{{padding:9px 11px;border-bottom:1px solid var(--border);vertical-align:top}}tr:nth-child(even) td{{background:#fafcfd}}.detail-table th{{background:#f3f7fa}}.numeric{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}.clean-list{{margin:0;padding-left:20px}}.clean-list li{{margin:3px 0}}.muted{{color:var(--muted);font-style:italic}}a{{color:var(--blue);text-decoration:none}}a:hover{{text-decoration:underline}}.table-wrap{{overflow-x:auto}}.disclosure{{background:#eaf1f6;border-left:4px solid var(--gold);padding:13px 16px;border-radius:5px;color:#486581;font-size:12px;margin:20px 0}}footer{{display:flex;justify-content:space-between;gap:15px;flex-wrap:wrap;border-top:1px solid var(--border);padding:18px 3px;color:var(--muted);font-size:11px}}
@media(max-width:1050px){{.kpi-grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}@media(max-width:700px){{.container{{padding:14px}}.hero{{display:block;padding:22px}}.decision{{margin-top:18px;text-align:left;min-width:0}}h1{{font-size:21px}}.kpi-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.card{{padding:16px}}th,td{{padding:7px}}}}@media print{{body{{background:#fff}}.container{{max-width:none;padding:0}}.hero{{box-shadow:none;print-color-adjust:exact;-webkit-print-color-adjust:exact}}.card,.kpi{{box-shadow:none}}a{{color:inherit}}}}
</style></head><body><main class="container">
<header class="hero"><div><div class="eyebrow">Equity research · Informe institucional</div><h1>{issuer}</h1><div class="meta">{ticker} · {exchange} · Fecha de valoración: {date} · Moneda del título: {html.escape(currency or 'No especificada')} · Moneda de reporte: {html.escape(str(package.get("reporting_currency", "No especificada")))}</div></div><div class="decision {rating_class}"><div class="eyebrow">Recomendación</div><div class="rating">{html.escape(rating)}</div><div class="sub">Horizonte y retorno según los datos suministrados</div></div></header>
<p class="lead">{html.escape(str(thesis_summary))}</p>{summary_metrics}
{''.join(sections)}
<div class="disclosure"><strong>Alcance y advertencia.</strong> {html.escape(source_note)} La generación y validación estructural de este documento no certifican la exactitud financiera, la idoneidad de una inversión ni constituyen asesoría personalizada. Las estimaciones y juicios requieren revisión de un analista.</div>
<footer><span><strong>{AUTHOR_SIGNATURE}</strong> · finanzas-valoracion-accion</span><span>Documento generado a partir del paquete de investigación proporcionado · {date}</span></footer>
</main></body></html>'''
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(doc, encoding="utf-8")
    return str(path)


def _display(value: Any) -> str:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, indent=2, default=str)
    return "No disponible" if value is None else str(value)


def _rows(value: Any) -> list[tuple[str, Any]]:
    if isinstance(value, dict):
        return [(str(k), v) for k, v in value.items()]
    if isinstance(value, list):
        return [(f"{i + 1}", item) for i, item in enumerate(value)]
    return [("Valor", value)]

def build_xlsx_workbook(package: dict[str, Any], output_path: str | Path, chart_paths: dict[str, str] | None = None) -> str:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = Workbook(); summary = wb.active; summary.title = "Executive Summary"
    summary.append([f"Institutional Equity Research — {package.get('issuer', 'Issuer not provided')}"])
    summary.append([AUTHOR_SIGNATURE]); summary.append(["Field", "Value"])
    for key, value in (("Ticker", package.get("ticker")), ("Exchange", package.get("exchange")),
                       ("Valuation date", package.get("valuation_date")), ("Security currency", package.get("security_currency", package.get("valuation_currency", package.get("reporting_currency")))), ("Reporting currency", package.get("reporting_currency")),
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
            for flat_field, flat_value in _flatten_rows(value, field):
                sheet.append([flat_field, flat_value])
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
    chart_paths = chart_paths or {}
    if chart_paths:
        from openpyxl.drawing.image import Image as SpreadsheetImage
        charts_sheet = wb.create_sheet("Charts")
        charts_sheet.append(["Research charts — sourced from canonical chart_data"])
        for index, (chart_key, chart_path) in enumerate(chart_paths.items()):
            title_row = 3 + index * 32
            charts_sheet.cell(title_row, 1, chart_key)
            image = SpreadsheetImage(chart_path)
            scale = min(1.0, 900 / image.width, 520 / image.height)
            image.width = int(image.width * scale)
            image.height = int(image.height * scale)
            charts_sheet.add_image(image, f"A{title_row + 1}")
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True); wb.save(path)
    return str(path)


def build_docx_report(package: dict[str, Any], output_path: str | Path, chart_paths: dict[str, str] | None = None) -> str:
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
    chart_paths = chart_paths or {}
    if chart_paths:
        doc.add_heading("Gráficas de análisis", level=1)
        for chart_key, chart_path in chart_paths.items():
            doc.add_paragraph(_label(chart_key))
            doc.add_picture(chart_path, width=Inches(6.3))
    for key, title in SECTIONS:
        value = package.get(key, {})
        doc.add_heading(title, level=1)
        rows = _flatten_rows(value)
        if not rows:
            doc.add_paragraph("No disponible")
        else:
            table = doc.add_table(rows=0, cols=2); table.style = "Light Shading Accent 1"
            for field, item in rows:
                cells = table.add_row().cells; cells[0].text = field; cells[1].text = _display(item)
    for style in doc.styles:
        if style.type == 1: style.font.name = "Aptos"; style.font.size = Pt(9)
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True); doc.save(path)
    return str(path)


def build_pptx_briefing(package: dict[str, Any], output_path: str | Path, chart_paths: dict[str, str] | None = None) -> str:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    def add_slide(title: str, lines: list[str]):
        slide = prs.slides.add_slide(prs.slide_layouts[1]); slide.shapes.title.text = title
        frame = slide.placeholders[1].text_frame; frame.clear()
        for i, line in enumerate(lines[:8]):
            para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
            para.text = line; para.font.size = Pt(18)
        footer = slide.shapes.add_textbox(Inches(0.55), Inches(7.12), Inches(12.2), Inches(0.22))
        footer.text_frame.text = AUTHOR_SIGNATURE
        footer.text_frame.paragraphs[0].font.size = Pt(9)
        footer.text_frame.paragraphs[0].font.italic = True
        slide.notes_slide.notes_text_frame.text = AUTHOR_SIGNATURE
    add_slide(f"Equity Research — {package.get('issuer', 'Issuer not provided')}", _summary_lines(package))
    chart_paths = chart_paths or {}
    for chart_key, chart_path in chart_paths.items():
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.title.text = _label(chart_key)
        slide.shapes.add_picture(chart_path, Inches(.65), Inches(1.25), width=Inches(12.0))
        footer = slide.shapes.add_textbox(Inches(.55), Inches(7.12), Inches(12.2), Inches(.22))
        footer.text_frame.text = AUTHOR_SIGNATURE
        footer.text_frame.paragraphs[0].font.size = Pt(9)
        footer.text_frame.paragraphs[0].font.italic = True
        slide.notes_slide.notes_text_frame.text = AUTHOR_SIGNATURE
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
    chart_paths = _build_chart_assets(package, out)
    return {
        "html": build_html_report(package, out / f"{safe_name}.html", chart_paths),
        "xlsx": build_xlsx_workbook(package, out / f"{safe_name}.xlsx", chart_paths),
        "docx": build_docx_report(package, out / f"{safe_name}.docx", chart_paths),
        "pptx": build_pptx_briefing(package, out / f"{safe_name}.pptx", chart_paths),
    }

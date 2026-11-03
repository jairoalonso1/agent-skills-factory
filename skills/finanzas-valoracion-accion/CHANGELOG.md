# Changelog — finanzas-valoracion-accion

## 0.2.2 — Final four-deliverable pipeline

- Integrated valuation football-field, DCF sensitivity and price/technical charts from explicit canonical `chart_data` into HTML, XLSX, DOCX and PPTX; HTML embeds chart images to remain portable.
- Reworked XLSX workpaper sections to flatten nested research data into typed, usable cells instead of serializing entire structures as JSON text.
- Distinguished security quote currency, issuer financial-reporting currency, valuation currency and report currency in the package contract and report metadata.
- Allowed bear/base/bull cases to carry explicit `not_available`, `not_estimated` or `not_applicable` states without inventing numeric target prices.
- Added end-to-end synthetic profile tests for Intel, JPMorgan Chase, NVIDIA and an insufficient-data issuer. These tests validate the workflow and deliverables, not factual issuer research or investment conclusions.
- Expanded the automated suite to 40 passing tests in the development runtime.

# Changelog — finanzas-valoracion-accion

## 0.2.1 — Candidate

- Replaced the HTML JSON-dump layout with a responsive institutional equity-research tear sheet.
- Added an executive banner, recommendation panel, data-driven KPI cards, structured section cards, and a Bear/Base/Bull scenario matrix.
- Added readable nested tables/lists, source links, mobile layout, print styling, and an explicit scope/disclaimer block.
- Escaped report content and rendered unavailable values explicitly instead of inventing values.
- Made the author signature visible in PowerPoint slide footers as well as speaker notes.
- Added regression tests for semantic HTML structure, HTML escaping, scenario presentation, responsive/print styles, and visible PPTX branding.

This remains a candidate release. These presentation tests do not certify financial data, valuation methodology, or investment conclusions.


## 0.3.0 — Reproducibility and release hardening

- Fixed chart module syntax and retained reproducible chart generation.
- Made Matplotlib optional; core report generation does not require charting libraries.
- Added optional structured observation ledger with source and calculation-lineage validation.
- Added ROIC methodology disclosure and warning without imposing a universal invested-capital formula.
- Removed stale evaluation claims; manifest metrics are populated only from the actual 0.3.0 verification run.

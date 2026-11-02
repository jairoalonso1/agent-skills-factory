# Changelog — finanzas-valoracion-accion

## 0.2.2 — Candidate

- Introduced a versioned, model-independent canonical output contract (equity-research-report 1.0.0).
- Preserved every mandatory report section across HTML, XLSX, DOCX and PPTX, including explicit missing-data placeholders.
- Standardized all deliverables and workbook/slide labels to Spanish (es-CO).
- Separated issuer reporting currency, security quote currency and valuation currency to avoid ADR/cross-listing mislabeling.
- Allowed target prices to be explicitly not estimated or not applicable, with a required reason, instead of substituting spot prices.
- Added cross-format output-contract regression tests.
- Cross-model host compatibility remains not tested; no model-specific compatibility claim is made.


## 0.2.1 — Candidate

- Replaced the HTML JSON-dump layout with a responsive institutional equity-research tear sheet.
- Added an executive banner, recommendation panel, data-driven KPI cards, structured section cards, and a Bear/Base/Bull scenario matrix.
- Added readable nested tables/lists, source links, mobile layout, print styling, and an explicit scope/disclaimer block.
- Escaped report content and rendered unavailable values explicitly instead of inventing values.
- Made the author signature visible in PowerPoint slide footers as well as speaker notes.
- Added regression tests for semantic HTML structure, HTML escaping, scenario presentation, responsive/print styles, and visible PPTX branding.

This remains a candidate release. These presentation tests do not certify financial data, valuation methodology, or investment conclusions.

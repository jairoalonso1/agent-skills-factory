# HTML Rendering Contract

## Purpose and precedence
This contract is normative for every generated HTML artifact. It operationalizes the user-supplied SaaS factsheet reference. If a model default conflicts with this contract, this contract wins. Analytical content remains governed by `report-profiles.md`.

## Mandatory template use
1. Select `templates/factsheet.html` for one fund and `templates/comparative.html` for two or more funds.
2. Treat the selected template as the canonical DOM/CSS scaffold. Populate its semantic sections and data slots; do not start from a generic dashboard.
3. Preserve the light institutional palette, header, section hierarchy, KPI cards, tables, chart containers and footer.
4. Keep output portable: inline CSS and SVG charts/logo where practical. No Tailwind CDN, remote chart library, external JavaScript dependency or network font fetch is required.
5. Financial content and metric definitions remain governed by `report-profiles.md`; templates must not invent data or calculations.

## Required document semantics
- `<!doctype html>`, `<html lang="es-CO">`, UTF-8 and responsive viewport.
- Meaningful document title and one primary `h1`.
- Header metadata: generation date, cutoff and analysis period.
- Brand lockup: reference mark plus “Frontera Funds”; if the host cannot package the asset, use text-only fallback and report a warning.
- All required profile sections, including historical drawdown and rolling volatility (30 valid observations) diagnostics. If a section cannot be populated, retain it and show “No disponible con la información consultada” plus the reason.
- Footer: source attribution, methodology, limitations, Frontera Funds SKaaS identity and provenance. For SFC-sourced FIC data, the source-attribution slot must read exactly “Fuente: SFC. Procesado por Frontera Funds.” Do not claim SFC as a source when the report uses other data.
- Do not expose provider-specific tool names, endpoint URLs, credentials, internal query strings or implementation details in client-facing HTML. Keep technical traceability in internal execution metadata.
- Accessible table headers and chart descriptions; color is never the only carrier of meaning.

## Template data slots
Replace every `{{PLACEHOLDER}}` token before delivery. Escape all untrusted text for HTML. For optional values, render an explicit missing-data state; never leave raw placeholders. Repeatable rows/sections must be populated from structured records, not untrusted HTML strings. Do not insert source HTML as markup.

## Visual acceptance
- White page, `#F9FAFB` soft surfaces, `#1F2937` primary text, `#4B5563` secondary text, `#E5E7EB` borders and restrained `#0BDA46` accent.
- Roboto/system sans-serif, consistent spacing, centered page, restrained rounded cards.
- Responsive mobile layout and A4 print stylesheet.
- No dark-first dashboard, gradients, neon effects, emoji charts or fabricated logo.
- Charts/tables show units, periods, labels and source context.

## Preflight checks
Confirm correct template/profile, required sections, brand asset or fallback warning, no remote runtime dependency, no unresolved placeholders, responsive and print CSS, non-empty HTML and reconciliation with structured output. Open/render the artifact when browser preview is available. If not, state that visual rendering was not executed; do not claim pixel-perfect validation.

## Provenance
Generated reports use `frontera_skaas_generated`. The user-supplied reference HTML is a design reference only; never label generated output as an original SaaS export.

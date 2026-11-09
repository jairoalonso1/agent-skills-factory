# HTML Rendering Contract

## Purpose and precedence
This contract is normative for every generated HTML artifact. Analytical content is governed by the selected versioned profile and `standards/metric-definitions.yaml`. Presentation is governed by the effective theme and validated client overrides.

## Mandatory template use
1. Select `templates/factsheet.html` for one fund and `templates/comparative.html` for two to eight funds.
2. Treat the selected template as the canonical DOM/CSS scaffold. Populate semantic sections and data slots; do not start from a generic dashboard.
3. Resolve the effective theme from `themes/` and `configuration/`; substitute `{{THEME_CSS_VARIABLES}}`, `{{PRINT_PAGE_SIZE}}`, brand identity and standard metadata placeholders.
4. Preserve the selected profile's required sections even when values are unavailable.
5. Keep output portable: inline CSS and SVG charts/logo where practical. No Tailwind CDN, remote chart library, external JavaScript dependency or network font fetch is required.

## Required document semantics
- `<!doctype html>`, `<html lang="es-CO">`, UTF-8 and responsive viewport.
- Meaningful document title and one primary `h1`.
- Header metadata: generation date, cutoff and analysis period.
- Brand lockup uses the effective theme's authorized mark/wordmark. If no authorized logo is available, use a text-only wordmark and record `brand_mark_unavailable`.
- Include the selected profile's required sections; if a section cannot be populated, retain it and show “No disponible con la información consultada” plus the reason.
- Footer identifies the effective brand/product identity, source attribution, methodology, limitations and provenance. For SFC-sourced FIC data under the default Frontera theme, the exact attribution is “Fuente: SFC. Procesado por Frontera Funds.” For another brand, attribution must reflect the actual source and configured processor identity; never falsely attribute processing to Frontera.
- Do not expose provider-specific tool names, endpoint URLs, credentials, internal query strings or implementation details in client-facing HTML. Keep technical traceability in internal execution metadata.
- Accessible table headers and chart descriptions; color is never the only carrier of meaning.

## Template data slots
Replace every `{{PLACEHOLDER}}` token before delivery. Theme placeholders are resolved from validated theme tokens; identity placeholders are escaped as text. `{{BRAND_MARK_ELEMENT}}` may contain only renderer-generated markup derived from a bundled or host-authorized asset, never raw user HTML. Escape all untrusted text. For optional values, render an explicit missing-data state; never leave raw placeholders. Repeatable rows/sections must be populated from structured records, not untrusted HTML strings.

## Theme variables
At minimum resolve these variables from the effective theme:

| CSS variable | Theme field |
|---|---|
| `--page` | `colors.page` |
| `--outer-canvas` | `colors.outer_canvas` |
| `--surface` | `colors.surface` |
| `--text` | `colors.text_primary` |
| `--muted` | `colors.text_secondary` |
| `--border` | `colors.border` |
| `--green` | `colors.accent` |
| `--positive` / `--negative` | `colors.positive` / `colors.negative` |
| `--font-family` | `typography.family` |
| `--base-font-size` | `typography.base_px` converted to px |
| `--line-height` | `typography.line_height` |

The effective theme must be recorded in the report metadata. `{{REPORT_TITLE}}` is populated from the validated report-title override or the profile default. `{{PRINT_PAGE_SIZE}}` is selected from the profile page specification.

## Visual acceptance
- Validate contrast and preserve semantic status distinctions.
- Use consistent typography, spacing, page sizing and numeric alignment.
- Provide responsive mobile layout and print CSS.
- Charts/tables show units, periods, labels and source context.
- No unapproved logo, gradients or styling that harms readability.

## Preflight checks
Confirm correct template/profile, required sections, effective theme, authorized brand assets or fallback warning, no remote runtime dependency, no unresolved placeholders, escaped text, responsive and print CSS, non-empty HTML and reconciliation with structured output. Open/render the artifact when browser preview is available. If not, state that visual rendering was not executed; do not claim pixel-perfect validation.

## Provenance
Generated reports use `frontera_skaas_generated` as artifact provenance regardless of selected visual theme. This records the producing service, not the brand owner or data source. The user-supplied Frontera reference HTML is a design reference only; never label generated output as an original SaaS export.

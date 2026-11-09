# Frontera Funds SKaaS — Brand Identity

## Product relationship

FIC Funds Intelligence is an official SKaaS product in the Frontera Funds ecosystem. It inherits the Frontera Funds brand, visual identity and institutional report-quality standard. It is not a separate or competing brand.

## Official logo

Use the official Frontera Funds brand mark stored at `assets/frontera-funds-mark.svg`, paired with the text wordmark `Frontera Funds`. This approved vector mark is the same shield/financial-column symbol embedded in the SaaS favicon. The host may replace or supplement it only with a newer approved brand asset. The Skill package must not scrape, reconstruct, redraw, approximate or guess the logo from private application source.

Preferred delivery order:
1. Official SVG mark at `assets/frontera-funds-mark.svg` paired with the Frontera Funds text wordmark.
2. Newer official vector or transparent PNG asset supplied by the brand owner.
3. Text wordmark fallback, exactly "Frontera Funds", only if the SVG cannot be loaded.

The runtime should place the logo in the report header and, where appropriate, the footer. Preserve original proportions, clear space, approved color variants and contrast. Do not recolor or distort the logo.

If the SVG asset cannot be loaded and no replacement is available, render the text wordmark and add a warning to the structured result: `official_brand_logo_unavailable`. Never fabricate a substitute graphic.

## Visual system and quality parity

Reports must meet the institutional presentation quality expected from Frontera Funds SaaS:
- consistent typography, hierarchy, spacing and restrained color use;
- clear report title, fund identity, cutoff and period;
- well-defined KPI cards and analytical sections;
- charts with legible axes, units, legends and source context;
- tables with consistent alignment, numeric formatting and clear missing-value treatment;
- responsive desktop/mobile layout and print CSS;
- consistent header/footer, page metadata and source disclosures.

Use the approved palette below. Maintain accessible contrast and use the green accent selectively; do not turn every KPI or chart into a neon sign.

| Token | Value | Use |
|---|---|---|
| Frontera green | `#0BDA46` | Primary accent, positive highlights, brand mark |
| App background | `#131614` | Dark-mode report background |
| Surface | `#2D3430` | Cards and elevated sections |
| Divider | `#424C47` | Borders and separators |
| Secondary text | `#A5B1AB` | Supporting labels and metadata |
| Alert red | `#FA5538` | Negative or warning states |
| Primary text | `#FFFFFF` | High-contrast text on dark surfaces |

A light report theme may be used when the report medium requires it, but preserve the same accent and semantic color roles. Avoid low-contrast gray-on-gray combinations.

## Implementation and confidentiality boundary

Brand consistency does not require shared implementation. The SKaaS renderer must not import, copy or depend on private Frontera SaaS source code, internal APIs, infrastructure, credentials, deployment configuration or proprietary runtime services.

Approved brand assets and product-level design specifications may be supplied to the SKaaS runtime independently. Keep secrets and private implementation details out of the Skill package and generated reports.

## Report identity and provenance

Every generated report must identify itself as a **Frontera Funds SKaaS** deliverable and use artifact provenance `frontera_skaas_generated`. User-supplied artifacts retain `user_supplied` provenance. Do not describe a SKaaS-generated report as an export from the Frontera SaaS application.

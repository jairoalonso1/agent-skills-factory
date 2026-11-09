# Frontera Funds SKaaS — Brand Identity

## Product relationship

FIC Funds Intelligence is an official SKaaS product in the Frontera Funds ecosystem. It inherits the Frontera Funds brand, visual identity and institutional report-quality standard. It is not a separate or competing brand.

## Official logo

Use the official Frontera Funds logo supplied through an authorized brand asset package or host-managed asset binding. The Skill package must not scrape, reconstruct, redraw, approximate or guess the logo from private application source.

Preferred delivery order:
1. Official vector logo (SVG) from the approved brand package.
2. Official transparent PNG at adequate resolution.
3. Approved text wordmark fallback, exactly "Frontera Funds".

The runtime should place the logo in the report header and, where appropriate, the footer. Preserve original proportions, clear space, approved color variants and contrast. Do not recolor or distort the logo.

If no authorized logo asset is available, render the text wordmark and add a warning to the structured result: `official_brand_logo_unavailable`. Never fabricate a substitute graphic.

## Visual system and quality parity

Reports must meet the institutional presentation quality expected from Frontera Funds SaaS:
- consistent typography, hierarchy, spacing and restrained color use;
- clear report title, fund identity, cutoff and period;
- well-defined KPI cards and analytical sections;
- charts with legible axes, units, legends and source context;
- tables with consistent alignment, numeric formatting and clear missing-value treatment;
- responsive desktop/mobile layout and print CSS;
- consistent header/footer, page metadata and source disclosures.

Use only approved brand tokens and visual assets supplied to the runtime. If tokens are not available, choose a restrained, accessible neutral presentation rather than inventing brand colors.

## Implementation and confidentiality boundary

Brand consistency does not require shared implementation. The SKaaS renderer must not import, copy or depend on private Frontera SaaS source code, internal APIs, infrastructure, credentials, deployment configuration or proprietary runtime services.

Approved brand assets and product-level design specifications may be supplied to the SKaaS runtime independently. Keep secrets and private implementation details out of the Skill package and generated reports.

## Report identity and provenance

Every generated report must identify itself as a **Frontera Funds SKaaS** deliverable and use artifact provenance `frontera_skaas_generated`. User-supplied artifacts retain `user_supplied` provenance. Do not describe a SKaaS-generated report as an export from the Frontera SaaS application.

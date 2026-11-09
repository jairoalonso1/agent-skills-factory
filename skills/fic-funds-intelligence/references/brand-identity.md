# Brand Identity and Theme Configuration

## Separation of brand and analytical standard

The reporting standard is brand-independent. A theme controls presentation and authorized identity fields; it cannot change metric definitions, data provenance, required sections, entity identity, comparability rules or quality gates. The default theme is `frontera-funds`, defined in `themes/frontera-funds.yaml`.

## Default Frontera theme

The default visual reference is the light institutional style supplied in the Frontera Funds factsheet: white page, soft gray surfaces, dark slate text, subtle neutral borders, restrained green accent, Roboto/Arial sans-serif, centered header, KPI cards, analytical sections, legible tables and institutional footer. Exact design tokens are maintained in `themes/frontera-funds.yaml` and `references/design-tokens.json`.

## Configurable themes and authorized assets

A host may select `frontera-funds`, `neutral-institutional` or a validated custom theme. Brand name, wordmark, logo, palette and typography may be overridden only with authorization to use those assets and identities. The host must record the effective theme ID/version and applied overrides.

The bundled SVG at `assets/frontera-funds-mark.svg` is the **reference mark extracted from the user-supplied Frontera Funds factsheet HTML**. Its provenance is `user_supplied_reference`; it is not independently trademark-verified. It is excluded from the package MIT code license and may be used only for authorized Frontera Funds distribution. Preserve its paths, proportions and viewBox. Never redraw, approximate or invent a logo. If no authorized logo is available, use the configured text wordmark and emit `brand_mark_unavailable`.

## Accessibility and visual quality

Every theme must preserve readable contrast, hierarchy, legible numeric values and chart labels. Color cannot be the sole carrier of positive/negative/neutral meaning. Green is an accent in the default Frontera theme, not a universal page background or chart color. Validate color contrast after overrides.

## Layout and print

Use an A4 portrait page for factsheets and A4 landscape for comparative reports by default. Keep whitespace disciplined, tables legible and chart axes/units explicit. On narrow screens, stack cards and allow wide tables to scroll. Print on white background, remove shadows and nonessential controls, and avoid splitting important cards or sections.

## Prohibited deviations

Do not use an invented mark, unauthorized third-party identity, illegible dense tables, low-contrast palette, emoji as data visualization or styling that obscures financial meaning. A custom theme may differ visually from Frontera, but it must meet the same accessibility and institutional quality requirements.

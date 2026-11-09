# Frontera Funds SKaaS — Brand Identity

## Product relationship
FIC Funds Intelligence is a Frontera Funds SKaaS service. Reports use the visual language of the supplied Frontera Funds SaaS factsheet reference while remaining independently implemented. This is a product-level presentation specification, not a dependency on private application code.

## Approved reference mark and provenance
The bundled SVG at `assets/frontera-funds-mark.svg` is the **reference mark extracted from the user-supplied Frontera Funds factsheet HTML**. Its provenance is `user_supplied_reference`; do not describe it as independently trademark-verified. Use it with the text wordmark “Frontera Funds”. Preserve its paths, proportions and viewBox. Do not redraw, approximate, recolor the paths or replace it with an invented shield. If unavailable, use the text wordmark and emit `reference_mark_unavailable`.

## Canonical report appearance
The default factsheet and comparative theme is the **light institutional theme** shown in the supplied SaaS factsheet. A dark theme is not the default and must not be substituted because a model prefers it.

| Token | Value | Use |
|---|---|---|
| Page | `#FFFFFF` | Main report canvas |
| Soft surface | `#F9FAFB` | KPI cards, table headers, subtle panels |
| Primary text | `#1F2937` | Titles and body |
| Secondary text | `#4B5563` | Labels, descriptions and metadata |
| Border | `#E5E7EB` | Dividers and card outlines |
| Brand green | `#0BDA46` | Brand accent, selected highlights |
| Positive | `#16A34A` | Positive change |
| Negative | `#DC2626` | Negative change and adverse values |
| Neutral | `#6B7280` | Neutral states |

Use Roboto with a system sans-serif fallback. For portable output, use `Roboto, Arial, sans-serif`; do not require a network font fetch. Green is an accent, not a page background or a universal chart color.

## Layout and components
- White A4-like report canvas, centered and readable on screen.
- Header with mark/wordmark, centered report title, generation date and analyzed period/cutoff.
- Generous but disciplined whitespace; thin neutral dividers; restrained rounded cards.
- KPI cards use soft gray surfaces, clear labels, prominent values, units and comparison context.
- Analytical sections have consistent heading hierarchy and spacing.
- Charts have legible axes, legends, units, dates and source notes.
- Tables use clear headers, aligned numeric values, subtle row separators and explicit missing-value labels.
- Footer identifies Frontera Funds SKaaS, report provenance and limitations/disclaimer.

## Responsive and print
At desktop widths, center the report on a neutral outer canvas with a maximum page width. On narrow screens, remove outer margins, stack cards and make wide tables horizontally scrollable. Print with white background, no shadows, visible text, sensible page breaks and A4 page sizing. Hide nonessential interactive controls.

## Prohibited deviations
Do not use a dark-first dashboard, neon/glowing effects, gradients, oversized colored backgrounds, generic admin-dashboard styling, emoji as data visualization, illegible dense tables, or a logo substitute. Do not omit the title/date/cutoff header or source/methodology footer. The supplied factsheet reference takes precedence over model defaults.

## Brand ownership
The Frontera Funds name and brand assets remain the property of their owner. Repository inclusion of the user-supplied reference mark does not grant a trademark license beyond authorized Frontera Funds SKaaS use. The package's software license does not relicense the mark.

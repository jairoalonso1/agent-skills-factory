# HTML Report Profiles

These profiles define the two standard outputs for FIC Funds Intelligence. They are inspired by the factsheet and comparative-table report patterns reviewed in Frontera Funds. They are portable specifications, not copied React components or a Frontera runtime dependency.

## Shared publication standard

- Language: Spanish (Colombia); use consistent COP formatting and decimal conventions.
- Delivery: one HTML file, preferably self-contained, with embedded CSS and chart assets where feasible.
- Responsive: readable on desktop and mobile; tables must scroll or reflow without hiding material information.
- Print: provide a print stylesheet and sensible page breaks.
- Header: report title, profile, generation timestamp, cutoff date, date range, service version and data freshness.
- Identity: fund name, `codigo_negocio`, manager, SFC subtype and participation class where relevant.
- Evidence: source name, locator/URL, retrieval time and date of data cutoff.
- Interpretation: distinguish source data, calculations and model interpretation.
- Gaps: visibly mark N/A, missing observations, stale records and assumptions; do not silently impute.
- Footer: methodology, limitations, report provenance and informational-use disclosure.

## Profile A — Fund factsheet (`factsheet`)

Use for one fund. Required sections:

1. **Fund identification** — name, business code, manager, subtype/nature, representative participation class and reporting cutoff.
2. **Executive overview** — short evidence-led summary, not a recommendation.
3. **Fund scale** — AUM, investors, average investor ticket and unit value where available.
4. **Performance** — reported EA returns for daily, 30-day, 180-day and 365-day horizons; cumulative return and CAGR only when their source series/definitions are available.
5. **Risk and behavior** — volatility, maximum drawdown, drawdown duration/recovery, Sharpe/Sortino and VaR/CVaR only if supplied or reproducibly calculated with assumptions.
6. **History and distribution** — NAV or return evolution, monthly return heatmap/table and worst drawdown episodes where observations exist.
7. **Category context** — statistical volatility category or nature-based category with dimension, snapshot cutoff and reason/status.
8. **Diagnostics** — data coverage, missing or extreme observations, concentration/class caveats and liquidity/flow flags when relevant.
9. **Evidence and methodology** — sources, dates, metric definitions, assumptions and limitations.

Optional sections may include peer percentile, category distribution, manager context or AI-generated narrative. Optional content must not displace required sections or imply unsupported precision.

## Profile B — Comparative report (`comparative`)

Use for at least two funds. Required sections:

1. **Comparison scope** — selected funds, their business codes, manager, subtype, participation class, common cutoff and overlapping period.
2. **Executive comparison** — key similarities, differences and caveats; do not merely declare a winner.
3. **Summary matrix** — AUM, investors, ticket, reported EA returns (daily/30d/180d/365d), volatility, drawdown and applicable risk ratios.
4. **Performance comparison** — aligned time-series chart where common history exists, with clear axes and period.
5. **Risk comparison** — comparable risk metrics, observation counts and assumptions.
6. **Category/peer context** — category dimension and snapshot date; explain when funds are not statistically comparable (for example, different nature-based categories).
7. **Flows and liquidity** — optional, with explicit window and definition.
8. **Conclusions and watchpoints** — counterpoints, data gaps, measurement limitations and reasons a ranking may be misleading.
9. **Evidence and methodology** — source ledger, cutoff, metric definitions and disclaimers.

## Metric conventions

- Always state whether an annual effective return is an SFC-reported figure or calculated from NAV.
- Never combine return series with different sampling frequency or date ranges without labeling the adjustment.
- Volatility annualization must state the observation frequency and annualization factor. If using the FIC classification methodology, record the 365-calendar-day window and √365 factor.
- Sharpe/Sortino must identify the risk-free rate, its effective annual basis, conversion method, target/downside definition and observation frequency.
- For peer comparisons, use the same cutoff and comparable participation class. If the MCP selects the largest-AUM class by default, disclose that selection.
- No metric should appear without value, unit, period, source/definition and status when applicable.

## Design inspiration and provenance

Frontera Funds' reviewed report components show two distinct templates: a customized factsheet with KPI sections, cumulative-return/drawdown/period-return charts, monthly-return heatmap and worst-drawdown table; and a comparative table report with selectable columns. Use these as inspiration for information hierarchy and analytical richness, but implement the layout in the host's available renderer or model-generated HTML. Do not copy the Frontera application or assume its login, premium entitlement, local storage or React app are available.

When actual original Frontera HTML is supplied or exported through an authorized session, label and retain it as `frontera_original`. A newly produced report is `skill_generated`, even when it follows the same profile.
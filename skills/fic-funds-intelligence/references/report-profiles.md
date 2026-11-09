# HTML Report Profiles

These profiles define the two standard outputs for Frontera Funds SKaaS — FIC Funds Intelligence. They are official product report standards, carrying the Frontera Funds information hierarchy and institutional quality bar while remaining independently implemented from the private SaaS codebase.

## Shared publication standard

- Language: Spanish (Colombia); use consistent COP formatting and decimal conventions.
- Delivery: one HTML file, preferably self-contained, with embedded CSS and chart assets where feasible.
- Responsive: readable on desktop and mobile; tables must scroll or reflow without hiding material information.
- Print: provide a print stylesheet and sensible page breaks.
- Header: report title, profile, generation timestamp, cutoff date, date range, service version and data freshness.
- Identity: fund name, `codigo_negocio`, manager, SFC subtype and participation class where relevant.
- Evidence: source name and date of data cutoff. Keep technical locators, queries and retrieval identifiers in internal execution metadata, not in the client-facing report.
- Interpretation: distinguish source data, calculations and model interpretation.
- Gaps: visibly mark N/A, missing observations, stale records and assumptions; do not silently impute.
- Footer: methodology, limitations, report provenance and informational-use disclosure. Populate the source-attribution slot from the actual sources used; for SFC-sourced FIC data the exact line is “Fuente: SFC. Procesado por Frontera Funds.”

## Profile A — Fund factsheet (`factsheet`)

Use for one fund. Required sections:

1. **Fund identification** — name, business code, manager, subtype/nature, representative participation class and reporting cutoff.
2. **Executive overview** — short evidence-led summary, not a recommendation.
3. **Fund scale** — AUM, investors, average investor ticket and unit value where available.
4. **Performance** — reported EA returns for daily, 30-day, 180-day and 365-day horizons; cumulative return and CAGR only when their source series/definitions are available.
5. **Risk and behavior** — volatility, maximum drawdown, drawdown duration/recovery, Sharpe/Sortino and VaR/CVaR only if supplied or reproducibly calculated with assumptions.
6. **History and distribution** — NAV or return evolution, monthly return heatmap/table, historical drawdown series and worst drawdown episodes where observations exist. Include a drawdown chart calculated as `NAV / running_max(NAV) - 1`.
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
5. **Risk comparison** — comparable risk metrics, observation counts and assumptions. Include aligned drawdown series and 30-observation rolling annualized volatility when common daily NAV histories support them.
6. **Category/peer context** — category dimension and snapshot date; explain when funds are not statistically comparable (for example, different nature-based categories).
7. **Flows and liquidity** — optional, with explicit window and definition.
8. **Conclusions and watchpoints** — counterpoints, data gaps, measurement limitations and reasons a ranking may be misleading.
9. **Evidence and methodology** — source ledger, cutoff, metric definitions and disclaimers.

## Required analytical charts

- **Historical drawdown:** derive from the NAV/unit-value series as `NAV_t / max(NAV_0…NAV_t) - 1`. Show the full available period, a zero reference line, date axis, percentage axis and explicit missing-data treatment. Do not infer drawdown from a single reported maximum-drawdown statistic.
- **Rolling volatility (30 observations):** calculate from 30 valid consecutive daily NAV-derived logarithmic returns, using sample standard deviation (`ddof=1`) multiplied by `√365`, expressed as an annualized percentage. Label it “Volatilidad anualizada móvil (30 observaciones)”. Do not confuse 30 observations with 30 calendar days. If fewer than 30 valid returns exist, retain the chart section and state why it cannot be calculated.
- **Comparative reports:** align funds to the same dates and frequency before plotting drawdown or rolling volatility. Do not interpolate missing observations silently. If histories are not comparable, show the limitation rather than a misleading overlay.
- All charts must have descriptive titles, units, period, legible axes and accessible text alternatives. SVG or another portable inline representation is preferred.

## Metric conventions

- Always state whether an annual effective return is an SFC-reported figure or calculated from NAV.
- Never combine return series with different sampling frequency or date ranges without labeling the adjustment.
- Volatility annualization must state the observation frequency and annualization factor. If using the FIC classification methodology, record the 365-calendar-day window and √365 factor.
- Sharpe/Sortino must identify the risk-free rate, its effective annual basis, conversion method, target/downside definition and observation frequency.
- For peer comparisons, use the same cutoff and comparable participation class. If the MCP selects the largest-AUM class by default, disclose that selection.
- No metric should appear without value, unit, period, source/definition and status when applicable.

## Frontera Funds brand and quality standard

All reports generated from these profiles are official **Frontera Funds SKaaS** deliverables. Apply the approved identity and logo rules in `brand-identity.md`.

The report experience must meet the same institutional quality bar as Frontera Funds SaaS: coherent typography, restrained use of color, consistent spacing, clear KPI hierarchy, readable data tables, meaningful chart annotations, responsive layouts and print-ready output. The SKaaS implementation may use a different renderer and codebase; visual and analytical consistency is the requirement, not shared application components.

Use the bundled reference mark at `assets/frontera-funds-mark.svg`, extracted from the user-supplied factsheet HTML, paired with the Frontera Funds text wordmark. Its provenance is `user_supplied_reference`; it is not independently trademark-verified. Do not redraw, reconstruct or guess a logo. If it cannot be loaded, use the text wordmark fallback and emit a warning. The canonical HTML structure and appearance are mandatory as specified in `html-rendering-contract.md` and `design-tokens.json`.

Generated HTML must carry the Frontera Funds SKaaS identity and use provenance `frontera_skaas_generated`. User-provided files retain `user_supplied` provenance. Never label a newly generated report as a SaaS export.

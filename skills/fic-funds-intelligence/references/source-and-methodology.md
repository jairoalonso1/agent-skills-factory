# Sources and Methodology

## SFC data source

The primary regulatory source is the SFC FIC open-data dataset `qhpu-8ixx` published through datos.gov.co. Use the current source endpoint and actual latest cutoff returned by the authorized source. Record retrieval time, selected period, relevant query and returned observation coverage in the evidence ledger. Historical cutoff is not synonymous with the latest cutoff.

Resolve fund identity using `codigo_negocio`; retain `tipo_participacion` for participation-level observations. Manager and subtype must come from regulator fields, not be inferred from fund branding alone.

## Data access and host integration

This Skill defines analytical data requirements, not a concrete integration. It does not contain or require an MCP server, endpoint, connector, API vendor, credential, tool name or private service implementation. The agent host is responsible for connecting authorized data services and exposing the capabilities available in that environment.

Conceptual capabilities may include dataset freshness, fund discovery, fund snapshots, historical NAV/returns, risk metrics, peer comparisons, rankings, AUM, investors, flows, liquidity indicators and dated categorization snapshots. Discover actual capabilities at invocation time; do not assume every host exposes all of them. Verify permissions and entitlements before retrieval. If a required capability is unavailable, disclose the limitation and do not fabricate data.

## Classification snapshot (optional)

A dated FIC categorization snapshot may be supplied by an authorized host capability or by the user. Inspect its actual schema and metadata before use. Join on `codigo_negocio`; do not join on fund name. Retain category dimension, commercial label, classification status, reason, cutoff and model version where supplied. Do not assume a fixed repository, path, file name or provider.

### Methodology reference

When the supplied snapshot follows the reviewed FIC categorization methodology, its documented conventions are:

- Universe: SFC subtypes 1, 2, 3, 6 and 7.
- Subtypes 1 and 2: traditional FICs, clustered jointly by log annualized volatility.
- Subtypes 3, 6 and 7: assigned nature-based categories — Inmobiliarios, Bursátiles and Fondos de Capital Privado — and excluded from volatility clustering.
- Window: 365 calendar days.
- Returns: daily logarithmic returns on unit value, `r_t = ln(V_t / V_(t-1))`.
- Annualized volatility: sample standard deviation (`ddof=1`) times `√365`, expressed as a percentage.
- Eligibility: strictly more than 180 valid daily returns for subtypes 1 and 2; 180 or fewer become `Sin Clasificar`.
- Clustering: one-dimensional K-means on log annualized volatility, K=12, random seed 42 and 50 initializations.
- Cluster labels are ordered by centroid, lowest to highest volatility, and named from `Estabilidad excepcional` through `Volatilidad extrema`.
- `Sin Clasificar` is a residual status, not a nature class, statistical cluster or risk category.

Always inspect the methodology version accompanying the retrieved snapshot and follow it if different. This Skill does not reimplement K-means or publish a new category assignment.

### Interpretation limits

Volatility is only one dimension of investment risk. It does not fully represent credit quality, liquidity, concentration, duration, leverage, valuation smoothing or operational risk. A low-volatility fund is not automatically low-risk in every relevant sense. A higher return is not automatically superior. Use category as a peer-grouping aid, not as an investment recommendation or substitute for due diligence.

## Source hierarchy and conflict handling

Prefer regulator-reported data for official fund observations. Use classification artifacts only for their declared classification purpose. If category and current SFC subtype conflict, disclose the conflict and do not silently override the regulator field. If a third-party source conflicts with regulator data, show the conflict and explain the source hierarchy.

## Evidence ledger and client attribution

Capture internally where available: source name and owner; dataset/API/tool locator; retrieval timestamp; cutoff and period; record/observation count; source version or snapshot identifier; metric definition, units and transformation; limitations, stale status and warnings. Keep technical identifiers in execution metadata, not in the client-facing report.

For SFC-sourced reports under the default Frontera theme, use the exact attribution: **“Fuente: SFC. Procesado por Frontera Funds.”** For another authorized brand, preserve the source name and use the configured processor identity. Add another source only when it materially contributes to a displayed result.

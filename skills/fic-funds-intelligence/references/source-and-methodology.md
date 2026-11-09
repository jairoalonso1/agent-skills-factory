# Sources and Methodology

## SFC data source

The SFC FIC open dataset is `qhpu-8ixx` on datos.gov.co. Use the current source endpoint and actual latest cutoff returned by the tool/source. Record retrieval time, selected period, relevant query and returned observation coverage. Historical cutoff is not synonymous with the latest cutoff.

Fund identity must be resolved using `codigo_negocio`; participation-level observations should retain `tipo_participacion`. Manager and subtype should be sourced from regulator fields, not inferred from fund branding alone.

## MCP adapter (optional)

The optional server `mcp-sfc-fics-colombia` exposes twelve tools over the SFC dataset. The exact names and required arguments are listed in `../SKILL.md`.

Recommended call sequence:

1. `obtener_estado_dataset` to establish latest cutoff and dataset freshness.
2. `buscar_fondos_fic` to resolve user-provided fund names or managers.
3. `radiografia_fondo` for a full single-fund snapshot or `comparar_peer_group_fics` for a 2–8 fund comparison.
4. `serie_historica_nav_y_tasas` when a history chart or custom calculation is needed.
5. `metricas_riesgo_cuantitativo` only when date range and inputs support its calculations.
6. Supplement with `ranking_rentabilidades_fics`, `cuota_mercado_aum_entidades`, `flujos_netos_captacion` and `radar_corridas_y_alertas_liquidez` where relevant.
7. Use `ejecutar_soql_avanzado` only for a specific missing query; record the SoQL clauses used.

The MCP is optional. If unavailable, use other authorized sources or user-supplied files and label the limitation.

## Classification provider (optional)

The external project `jairoalonso1/categorizacion-fic-colombia` creates quarterly classification output. The current documented output files are:

- `outputs/latest/fondos_clasificados.csv` — fund-level records and category fields.
- `outputs/latest/resumen_clasificacion.json` — source, cutoff, window, universe, model parameters, category counts and coverage.
- `outputs/latest/clasificacion_fic.xlsx` — workbook output.

Use `codigo_negocio` as join key. Read the actual file's column names and metadata before joining; do not assume future versions preserve all fields. Retain category dimension, commercial label, classification status, reason, cutoff and model version where the source supplies them.

### Current methodology reference

The currently reviewed methodology document describes:

- Universe: SFC subtypes 1, 2, 3, 6 and 7.
- Subtypes 1 and 2: traditional FICs, clustered jointly by log annualized volatility.
- Subtypes 3, 6 and 7: assigned their own nature-based categories — Inmobiliarios, Bursátiles and Fondos de Capital Privado — and excluded from volatility clustering.
- Window: 365 calendar days.
- Returns: daily logarithmic returns on unit value, `r_t = ln(V_t / V_(t-1))`.
- Annualized volatility: sample standard deviation (`ddof=1`) times `√365`, expressed as a percentage.
- Eligibility: strictly more than 180 valid daily returns for subtypes 1 and 2; 180 or fewer become `Sin Clasificar`.
- Clustering: one-dimensional K-means on log annualized volatility, K=12, random seed 42 and 50 initializations.
- Cluster labels are ordered by centroid, lowest to highest volatility, and named from `Estabilidad excepcional` through `Volatilidad extrema`.
- `Sin Clasificar` is a residual status, not a nature class, statistical cluster or risk category.

Always inspect the methodology version that accompanies the retrieved output and follow it if different. This Skill does not reimplement K-means or publish a new category assignment.

### Interpretation limits

Volatility is only one dimension of investment risk. It does not fully represent credit quality, liquidity, concentration, duration, leverage, valuation smoothing or operational risk. A low-volatility fund is not automatically low-risk in every relevant sense. A higher return is not automatically superior. Use category as a peer grouping aid, not as an investment recommendation or a substitute for due diligence.

## Source hierarchy and conflict handling

Prefer regulator-reported data for official fund observations. Use classification artifacts only for their declared classification purpose. If category and current SFC subtype conflict, disclose the conflict and do not silently override the regulator field. If a third-party source conflicts with regulator data, show the conflict and explain the source hierarchy.

## Evidence ledger fields

Capture where available:

- source name and owner;
- dataset/API/tool name;
- source URL or query locator;
- retrieval timestamp;
- cutoff and period covered;
- record count or observation count;
- source/version or repository commit;
- metric definition, units and transformation;
- limitations, stale status and warnings.
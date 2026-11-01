# Valuation Framework and Method Selection

This guide selects methods by issuer economics. It is not a mandate to calculate every model.

| Issuer profile | Primary methods to consider | Common cautions |
|---|---|---|
| Mature operating company | FCFF DCF, EV/EBITDA, EV/EBIT, P/E, P/FCF | Normalize cycle and capex; DDM only if dividends are representative |
| High-growth / currently unprofitable | Long-horizon scenario DCF, EV/Sales, unit economics | Wide uncertainty; near-term P/E and EBITDA may be meaningless |
| Bank / insurer | P/B, P/E, dividend/residual-income/excess-return models | Industrial EV/EBITDA and conventional FCFF often unsuitable |
| REIT / property | NAV, FFO/AFFO multiples, dividend model | Reconcile property values, debt and recurring capex |
| Holding company / conglomerate | SOTP, NAV, holding-company discount | Include corporate costs, debt and minority interests |
| Cyclical company | Mid-cycle earnings/FCF, normalized multiples, scenario DCF | Peak/trough earnings are not sustainable by default |
| Distressed / restructuring | Liquidity runway, recovery waterfall, asset value, survival scenarios | Perpetuity DCF may be meaningless |
| Asset-heavy / commodity | NAV/replacement cost, normalized cash flows, cycle scenarios | Commodity price and reserve assumptions dominate value |

## FCFF DCF

FCFF = EBIT × (1 − normalized cash tax rate) + D&A − capital expenditure − change in operating net working capital.

Discount explicit FCFF and terminal value at WACC. Enterprise value is converted to equity value by subtracting net debt and other senior claims, adding supportable non-operating assets, and dividing by diluted shares. State whether mid-year convention is used. Nominal cash flows require nominal discount rates in the same currency.

## FCFE DCF

FCFE = Net income + D&A − capex − change in operating NWC + net borrowing.

Discount at cost of equity. The result is equity value; do not subtract net debt again. Ensure financing assumptions and net borrowing are consistent with projected leverage.

## Terminal value

Perpetuity growth: TV = FCF_(n+1) / (discount rate − perpetual growth). Discount rate must exceed terminal growth. Show sensitivity and implied terminal multiple. Do not silently cap invalid inputs.

Exit multiple: use a justified normalized metric and comparable multiple. Explain peer selection and why the terminal multiple is appropriate for the forecast horizon.

## Dividend and total payout models

DDM is appropriate only when dividends are meaningful and forecastable. Gordon growth is invalid when cost of equity is not greater than perpetual dividend growth. Multistage models disclose transition period and terminal assumptions. In `ddm_multistage`, `transition_growth` is the first transition-year rate; later transition years converge linearly to terminal growth.

Total payout includes dividends and net repurchases (repurchases less equity issuance). Use aggregate cash returned to equity holders, not gross repurchases if material issuance exists. Do not double count buybacks through both share-count reduction and separately added payout value.

## Comparable-company analysis

Use a consistent trailing or forward basis. Verify EV definitions, net debt, minority interests, leases where material, diluted shares and reporting periods. Show peer set, median, range and dispersion. Explain exclusions and outliers. P/E requires positive, meaningful earnings; EV/EBITDA requires positive, comparable EBITDA; P/B is most meaningful for certain financial and asset-based businesses.

## SOTP

Value each material segment with a method suited to its economics. Add supportable non-operating assets, subtract corporate costs (capitalized or explicitly valued), debt, minority interests and other senior claims. Disclose holding-company discount and its rationale; do not use a default discount.

## Financial-sector caution

Banks and insurers have distinct balance-sheet economics, regulatory capital, credit quality, reserves and solvency constraints. Prefer P/B, P/E, dividend/residual-income/excess-return approaches where appropriate. Explain capital adequacy and asset-quality assumptions.

## Technical context

Moving averages, RSI, MACD, Bollinger Bands, support/resistance and Fibonacci describe price behavior. They are not intrinsic valuation methods and should not be assigned weights in a fundamental valuation blend. State lookback, frequency, price adjustment and swing-point definitions.

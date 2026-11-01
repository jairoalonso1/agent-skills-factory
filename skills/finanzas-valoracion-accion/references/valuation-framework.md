# Valuation framework reference

This is a decision guide, not a requirement to calculate every model.

## Method selection

| Company profile | Primary methods to consider | Cautions |
|---|---|---|
| Mature operating company | FCFF DCF, EV/EBITDA, P/E, P/FCF | DDM if dividends are irregular |
| High-growth / unprofitable | Revenue or unit economics, EV/Sales, long-horizon DCF with wide sensitivity | P/E, near-term EBITDA multiples |
| Bank / insurer | Dividend or residual-income models, P/B, P/E, excess-return models | Enterprise value, EV/EBITDA, industrial FCFF |
| REIT / property company | NAV, FFO/AFFO multiples, dividend model | Unadjusted EBITDA |
| Holding company / conglomerate | Sum-of-the-parts, NAV, holding-company discount | Single consolidated multiple |
| Cyclical company | Mid-cycle earnings/FCF, normalized multiples, scenario DCF | Peak/trough earnings as sustainable |
| Distressed / restructuring | Asset value, recovery analysis, liquidity runway, scenarios | Perpetuity growth on unstable cash flows |

## DCF FCFF

A common unlevered free cash flow definition:

FCFF = EBIT × (1 − tax rate) + D&A − capital expenditure − change in net working capital.

Enterprise value is the present value of explicit FCFF plus terminal value, discounted at WACC. The equity bridge typically subtracts net debt and other senior claims, adds justified non-operating assets, and divides by diluted shares.

Do not mix nominal cash flows with real discount rates, currencies or inconsistent fiscal periods. Disclose mid-year convention if used.

## DCF FCFE

A common FCFE definition:

FCFE = Net income + D&A − capital expenditure − change in net working capital + net borrowing.

Discount FCFE at cost of equity. Do not subtract net debt again after deriving equity value from FCFE.

## Terminal value

Perpetuity growth:

TV = FCF_(n+1) / (discount rate − perpetual growth).

Discount rate must exceed perpetual growth. Otherwise the model is invalid; do not silently cap or conceal the issue. Test a reasonable range of both inputs.

Exit-multiple terminal value should use a justified normalized metric and peer multiple. Explain why it is consistent with the forecast horizon.

## Comparable-company analysis

Use comparable fiscal periods, forward/trailing basis consistently, enterprise-value definitions and diluted share counts. Explain outliers and adjust for differences only transparently. Show median and range rather than cherry-picking the most favorable peer.

## Dividend and payout models

DDM is appropriate only when dividends are meaningful and reasonably forecastable. A Gordon growth model is invalid when cost of equity is not greater than perpetual dividend growth. Multi-stage models should disclose transition period and terminal assumptions.

Total payout models can include dividends and repurchases. Avoid double counting repurchases through both share-count reduction and separately added payout value.

## Financial-sector caution

Banks and insurers have distinct balance-sheet economics and regulatory capital requirements. Enterprise-value metrics such as EV/EBITDA are often not meaningful. Prefer sector-appropriate approaches and explain capital, credit quality, reserves, solvency and regulatory constraints.

## Technical context

Moving averages, RSI, MACD, Bollinger Bands, support/resistance and Fibonacci levels describe price behavior. They do not independently establish intrinsic value. State lookback window, data frequency and calculation convention.

## Expected total return

Keep price-return and income components on the same horizon. Use expected distributions over the forecast horizon, not an undisclosed trailing yield. Consider buybacks separately and avoid double counting.

## Required audit trail

For each method record input data and source/date, forecast period and units, core assumptions, formulas, bear/base/bull results, sensitivities and reasons for excluding other methods.

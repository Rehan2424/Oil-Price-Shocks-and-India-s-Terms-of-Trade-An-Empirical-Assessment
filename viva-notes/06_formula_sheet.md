# 06 · Formula sheet

Everything on one page. y = ln ToT, x = ln real oil price, z = ln real non-energy commodity price.

## Trade measures

| Measure | Formula | Lecture |
|---|---|---|
| Net barter terms of trade | NTT = (UVI_X / UVI_M) × 100 | L21 |
| Income terms of trade | ITT = NTT × QI_X / 100 | – |
| Gross barter terms of trade | GBT = (QI_M / QI_X) × 100 | – |
| Revealed comparative advantage (Balassa) | RCA_ij = (X_ij / X_i) / (X_wj / X_w); RCA > 1 = advantage | L08 |
| Grubel–Lloyd index | GL = 1 − \|X − M\| / (X + M); 0 = one-way, 1 = fully two-way | L19 |
| Horizontal vs vertical IIT | Horizontal if 1/1.15 ≤ UV_X / UV_M ≤ 1.15; otherwise vertical | L20 |
| Monopoly markup (Lerner) | MR = p(1 − 1/e) = MC, so (p − MC)/p = 1/e | L16 |
| Average cost with scale economies | AC = F/Q + c | L16 |
| Real oil price | P_oil / MUV × 100 | – |
| Fiscal-year MUV | 0.75 × MUV_CY t + 0.25 × MUV_CY t+1 | – |

## The theory benchmark

> d ln NTT ≈ (s_x − s_m) · d ln P_oil

s_x = oil exports / total exports; s_m = oil imports / total imports. Benchmark −0.25 (FY1999) → −0.10 (FY2025).

## ARDL(1,1,1) in error-correction form (H1)

> Δy_t = c + α y_{t−1} + β₁ x_{t−1} + β₂ z_{t−1} + γ₁ Δx_t + γ₂ Δz_t + ε_t

| Quantity | Formula | Our value |
|---|---|---|
| Short-run elasticity | γ₁ | −0.241 |
| Long-run elasticity | −β₁ / α | −0.092 |
| Speed of adjustment | α (must be between −1 and 0) | −0.308 |
| Half-life of a deviation | ln 0.5 / ln(1 + α) | ≈ 1.9 years |
| Bounds test | F-test of α = β₁ = β₂ = 0 (case 3) | F = 4.74 |
| Delta-method variance of −β₁/α | g′ V g, with g = (−1/α, β₁/α²) | s.e. 0.059 |

Finite-sample bounds (N = 54, k = 2): 10% 3.32 / 4.32; 5% 4.02 / 5.13; 1% 5.69 / 7.03.

## NARDL (H2)

> x⁺_t = Σ_{j≤t} max(Δx_j, 0),  x⁻_t = Σ_{j≤t} min(Δx_j, 0)

> Δy_t = c + α y_{t−1} + θ⁺ x⁺_{t−1} + θ⁻ x⁻_{t−1} + π⁺ Δx⁺_t + π⁻ Δx⁻_t + controls + ε_t

Long run L± = −θ±/α. Wald tests: L⁺ = L⁻ (long run), π⁺ = π⁻ (short run).

## Benchmark test

> Δln NTT_t = a + b [(s_x − s_m)_{t−1} Δln P_oil,t] + c Δln P_nonoil,t + e_t,  H₀: b = 1

Result: b = 1.70 (s.e. 0.38), p(b = 1) = 0.07, N = 30.

## Local projections (Jordà 2005)

> y_{t+h} − y_{t−1} = a_h + β_h Δln Brent_t + φ_h Δln Brent_{t−1} + ψ_h Δy_{t−1} + u_{t+h},  h = 0…6

HAC (Newey–West) standard errors with h + 1 lags. β₂ = −0.39.

## Supply vs demand split (H3)

Step 1: Δln P_oil,t = c + Σ_k Σ_{j=0}^{2} b_kj ε_k,t−j + u_t, with k ∈ {supply, activity, consumption demand,
inventory demand}. R² = 0.80, 612 months.

- Supply part_t = Σ_j b_supply,j ε_supply,t−j
- Demand part_t = the same sum over the other three shocks

Step 2: ΔToT_t = a + b_S · supply part_t + b_D · demand part_t + e_t,  H₀: b_S = b_D.

## Tests and what their null hypothesis is

| Test | Null | Our p |
|---|---|---|
| ADF, Phillips–Perron | Unit root | levels 0.05–0.95 (ToT and oil ≈ 0.05), differences ≤ 0.001 |
| KPSS | Stationary | levels 0.01–0.10 |
| Zivot–Andrews | Unit root with one break | 0.39 (ToT), 0.53 (oil) |
| Breusch–Godfrey | No serial correlation | 0.90 |
| Breusch–Pagan | Homoskedastic errors | 0.019 |
| Jarque–Bera | Normal errors | 0.25 |
| Ramsey RESET | Correct functional form | 0.84 |
| CUSUM / CUSUMSQ | Stable coefficients | inside 5% bands |

## Standard errors

| Type | Robust to | Used in |
|---|---|---|
| HC1 (White) | Heteroskedasticity; small-sample factor n/(n − k) | ARDL robust table, rolling regressions |
| HAC (Newey–West) | Heteroskedasticity and autocorrelation | Benchmark test, local projections, H3 |

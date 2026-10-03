# Methodology

The code for each step is in the notebooks in [`../code/`](../code/). Open them on GitHub to see every output.

## Step 0: Measure the terms of trade correctly
- **Net barter ToT** = export unit value index / import unit value index × 100 (L21's definition). We recompute it from the published UVIs.
- **Two measures:**
  - Merchandise ToT (DGCI&S/RBI).
  - Goods-and-services ToT (export deflator / import deflator, national accounts).

  Using both shows the result does not depend on one statistical source.
- **Real oil price** = crude price / MUV index: the price of oil in terms of manufactures, the relative price on the offer-curve axes (L22).
- **Logs throughout**, so coefficients are **elasticities**: the % change in ToT for a 1% change in the oil price.

## Step 1: Order of integration (notebook 03)
- **Tests:**
  - ADF and Phillips–Perron (null: unit root).
  - KPSS (null: stationary).
  - Zivot–Andrews (unit root allowing one structural break).
- **Why:** regressing one trending series on another can give **spurious** results. ARDL is valid if variables are I(0) or I(1), **but not I(2)**.
- **Result:** every series is stationary in first differences, and levels are borderline. That is the ideal case for ARDL.

## Step 2: H1, long and short run (ARDL bounds test; notebook 03)
- **Model:** ARDL in error-correction form, with lags chosen by AIC (max 2):
  - Short-run elasticity = coefficient on Δln P_oil.
  - Long-run elasticity = −(coefficient on ln P_oil,t−1) / α.
  - α = speed of adjustment; it must be between −1 and 0 and significant.
- **Bounds test (Pesaran, Shin & Smith 2001):** F-test that all lagged levels are jointly zero.
  - F above the upper I(1) bound: a long-run relationship exists.
  - F below the lower I(0) bound: no long-run relationship.
  - In between: inconclusive.
  - We use **finite-sample** critical values and p-values (Kripfganz & Schneider 2020), because N = 54.
- **Control:** real non-energy commodity prices. This separates oil from a general commodity boom (L21: in general equilibrium, other markets matter).
- **Diagnostics:**
  - Breusch–Godfrey (serial correlation)
  - Breusch–Pagan (heteroskedasticity; detected, so we report HC1 robust s.e.)
  - Jarque–Bera (normality)
  - Ramsey RESET (functional form)
  - CUSUM / CUSUMSQ (stability)
- **Robustness checks:**
  - Oil only
  - Adding gold
  - Brent instead of the average crude price
  - Post-1980 sample
  - Merchandise ToT

## Step 3: H2, asymmetry (NARDL; notebook 04)
- Split ln P_oil into the cumulative sum of increases (P⁺) and of decreases (P⁻) (Shin, Yu & Greenwood-Nimmo 2014).
- **Wald tests:**
  - Long-run symmetry: θ⁺ = θ⁻.
  - Short-run symmetry: π⁺ = π⁻.
- Dynamic multipliers show the path after a permanent 1% rise vs a 1% fall.
- Robustness across samples and controls.

## Step 4: How big, and changing over time (notebook 05)
- **Benchmark test:** regress Δln NTT on (s_x − s_m)_{t−1} × Δln P_oil (plus non-oil control). Theory predicts a coefficient of 1. HAC (Newey–West) standard errors.
- **Rolling 20-year regressions** of Δln ToT on Δln P_oil: has exposure changed?
- **Monthly local projections (Jordà 2005):** ln ToT_{t+h} − ln ToT_{t−1} on Δln Brent_t, for h = 0…6 months, with HAC standard errors. Each horizon is its own regression, which is robust to misspecified dynamics in short samples.

## Step 5: H3, supply- vs demand-driven oil prices (notebook 06)
1. Regress the monthly oil price change (1975–2026, 612 months) on Baumeister–Hamilton (2019) structural shocks (supply, economic activity, consumption demand, inventory demand; current + 2 lags; R² = 0.80). Split the fitted oil price change into a **supply part** and a **demand part**.
2. Regress ToT changes (annual and monthly) on the two parts and test whether their coefficients are equal.
3. **Cross-check:** effect of Känzig (2021) OPEC supply-news shocks, which are exogenous to India (answers the "India is not a price-taker" critique, L11).

## Why these methods (short answers for the viva)
- **ARDL, not Johansen:**
  - It works with a mix of I(0) and I(1) variables.
  - It is reliable in small samples (N ≈ 54).
  - It has a single equation with a clear dependent variable (ToT).
- **NARDL:** the standard way to test for rise/fall asymmetry inside the same cointegration framework.
- **Local projections, not a VAR:** they need fewer assumptions about dynamics and are more robust with 80–85 monthly observations.
- **Identified shocks:** a raw oil price change mixes causes. Baumeister–Hamilton and Känzig separate *why* oil moved, which is needed for H3 and for exogeneity.

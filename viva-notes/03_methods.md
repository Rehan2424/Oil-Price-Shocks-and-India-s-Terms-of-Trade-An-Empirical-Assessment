# 03 · Methods: what each one does, why we chose it, and the traps

For each method you need to know four things: what it does, why we used it rather than the alternative, what
it assumes, and how to read our output. The questions examiners like most are marked **Trap**.

Notation: y = ln ToT, x = ln real oil price, z = ln real non-energy commodity price. Δ is the first difference.

---

## Logs and elasticities

Every variable is in logs, so each coefficient is an **elasticity**: the percentage change in ToT for a 1% change
in the oil price. "−0.24" means a 10% oil rise lowers the ToT by 2.4%.
- In the monthly models we use 100 × ln, so the coefficients read directly as percentages.

---

## Step 1. Unit-root tests (notebook 03, backup slide)

**Why.** If two series both trend, regressing one on the other can give a high R² and "significant" coefficients
even when they are unrelated (a **spurious regression**). We need to know each series' order of integration.

| Test | Null hypothesis | Reject the null means |
|---|---|---|
| ADF (augmented Dickey–Fuller) | Unit root | Stationary |
| Phillips–Perron | Unit root (robust to serial correlation and heteroskedasticity) | Stationary |
| KPSS | **Stationary** | Unit root |
| Zivot–Andrews | Unit root, allowing one structural break | Stationary with a break |

**Our results (p-values).**

| Series | ADF level | ADF diff | KPSS level |
|---|---|---|---|
| ln ToT goods and services | 0.057 | 0.000 | 0.10 |
| ln ToT merchandise | 0.27 | 0.001 | 0.01 |
| ln real oil price | 0.053 | 0.000 | 0.013 |
| ln real non-energy prices | 0.36 | 0.000 | 0.10 |

- **Reading:** levels are borderline between I(0) and I(1); every first difference is clearly stationary.
  **Nothing is I(2).**
- **Why that suits ARDL:** the bounds test is valid whether each regressor is I(0) or I(1), so we do not have to
  take a stand on the borderline cases.
- **Zivot–Andrews** does not reject a unit root in levels even with a break (break years: ToT 1985, oil 1999), so
  a single break is not driving the results.

**Trap.** "Why run both ADF and KPSS?" Because they have opposite nulls. ADF has low power in short samples, so
failing to reject a unit root is weak evidence. KPSS is the confirmation from the other side.

---

## Step 2. ARDL and the bounds test, for H1 (notebook 03)

**The model.** Lag lengths were chosen by AIC with a maximum of 2, which gave ARDL(1,1,1). In error-correction
form (UECM):

> Δy_t = c + α·y_{t−1} + β₁·x_{t−1} + β₂·z_{t−1} + γ₁·Δx_t + γ₂·Δz_t + ε_t

- **Short-run elasticity:** γ₁, the effect of this year's oil change on this year's ToT change.
- **Long-run elasticity:** −β₁/α. Its standard error comes from the delta method, because it is a ratio of
  two estimates.
- **Speed of adjustment:** α. It must be negative and between −1 and 0. α = −0.31 means 31% of any gap from the
  long-run relationship closes in a year (a half-life of about two years).

**The bounds test (Pesaran, Shin and Smith 2001).** An F-test of α = β₁ = β₂ = 0, "no long-run relationship".
The critical values come in two bounds:
- the **lower bound** assumes all regressors are I(0);
- the **upper bound** assumes all are I(1).

| F compared with | Conclusion |
|---|---|
| Above the upper bound | A long-run relationship exists |
| Below the lower bound | No long-run relationship |
| Between the bounds | Inconclusive |

We use **case 3** (unrestricted intercept, no trend) and **finite-sample** critical values (Kripfganz and
Schneider 2020), because 54 observations is small and the asymptotic tables are too lenient.

**Our result.** F = 4.74.

| Significance | Lower bound | Upper bound |
|---|---|---|
| 10% | 3.32 | 4.32 |
| 5% | 4.02 | 5.13 |
| 1% | 5.69 | 7.03 |

- F is above the 10% upper bound, so there is a long-run relationship at 10% (p = 0.070 against the I(1) bound).
- F lies between the bounds at 5%, so the 5% test is inconclusive (p = 0.025 against the I(0) bound).
- The error-correction coefficient is strongly significant (t = −3.60), which also points to adjustment towards
  a long-run level.

**Diagnostics.**

| Test | p-value | Reading |
|---|---|---|
| Breusch–Godfrey (2 lags) | 0.90 | No serial correlation |
| Breusch–Pagan | 0.019 | **Heteroskedasticity**, so we also report HC1 robust s.e. |
| Jarque–Bera | 0.25 | Residuals are normal |
| Ramsey RESET | 0.84 | Functional form is fine |
| CUSUM and CUSUMSQ | inside 5% bands | Coefficients are stable over time |

- With HC1 robust standard errors the short-run s.e. is 0.040 instead of 0.049. The conclusion does not change.
- HC1 is White's robust covariance with a small-sample correction, n/(n − k).

**Robustness (six specifications).** The baseline, oil only, adding gold, Brent instead of the average crude,
post-1980 only, and merchandise ToT. The short-run elasticity stays between −0.19 and −0.28 and is
significant in every one.

**Why ARDL and not Johansen or Engle–Granger?**
- It works with a mix of I(0) and I(1) variables. Johansen needs everything to be I(1).
- It behaves better in small samples (N = 54).
- It is a single equation with an obvious dependent variable (ToT). We are not interested in modelling the
  oil price as a function of India's ToT.
- It gives short-run and long-run effects in one regression.

**Traps.**
- "Your bounds test isn't significant at 5%, so where is your long-run relationship?" Agree: the long run is
  weak, the long-run elasticity (−0.09) is not significant, and our headline is the **short-run** effect. It is
  significant in every specification and does not depend on cointegration.
- "Is the oil price exogenous?" Mostly yes for annual data, because India's own demand moves world prices only
  slowly. We address it directly in H3 with shocks India cannot cause.
- "Why no trend?" The ToT has no significant linear trend over 1970–2025: it is 110 in FY1970 and 98 in
  FY2025, and a trend term has p = 0.12. Adding one would use up a degree of freedom we cannot spare.

---

## Step 3. Nonlinear ARDL, for H2 (notebook 04)

**Idea (Shin, Yu and Greenwood-Nimmo 2014).** Split the oil price into two running totals, one of all the
increases and one of all the decreases:

> x⁺_t = Σ max(Δx_j, 0)  and  x⁻_t = Σ min(Δx_j, 0)

Then estimate an ARDL with both:

> Δy_t = c + α·y_{t−1} + θ⁺·x⁺_{t−1} + θ⁻·x⁻_{t−1} + π⁺·Δx⁺_t + π⁻·Δx⁻_t + controls + ε_t

- Long-run effects are L⁺ = −θ⁺/α and L⁻ = −θ⁻/α.
- **Wald tests:** long-run symmetry L⁺ = L⁻, short-run symmetry π⁺ = π⁻.

**Reading the signs.** x⁻ only ever goes down. So a **negative** coefficient on x⁻ means an oil price *fall*
**raises** the ToT. Both coefficients negative means "rises hurt and falls help". Asymmetry is about whether the
two have the same size.

**Our result (baseline, N = 54).**
- Short run: rise −0.27, fall −0.22, symmetry p = 0.62.
- Long run: rise −0.16, fall −0.23, symmetry p = 0.035.

**Is the long-run asymmetry real? No, it is fragile:**
- p = 0.05 with an extra lag;
- p = 0.08 from FY1975;
- p = 0.28 from FY1980;
- reversed and not significant for merchandise ToT.

Short-run symmetry is never rejected in any specification. So we conclude the effects are **symmetric**, and H2 is
not supported. Notice that the baseline's long-run asymmetry goes the *opposite* way to Mork (1989): falls help
more than rises hurt. It comes from the 1970s.

---

## Step 4a. Benchmark test (notebook 05)

> Δln NTT_t = a + b·[(s_x − s_m)_{t−1} · Δln P_oil,t] + c·Δln P_nonoil,t + e_t

- Theory says **b = 1**: the ToT moves exactly by the oil share gap times the oil price change.
- Shares are lagged one year, so they are not affected by this year's oil price.
- Data: merchandise NTT, FY1995–FY2024, N = 30, HAC (Newey–West) standard errors.

**Result.** b = 1.70 (s.e. 0.38).
- It is significantly different from 0 (p < 0.001).
- It is not significantly different from 1 at 5% (p = 0.07).
- The theory gets the sign and the order of magnitude right. The extra effect is the indirect channels:
  fertiliser, petrochemicals, plastics and freight.

## Step 4b. Rolling 20-year elasticity (notebook 05)

Δln ToT on Δln P_oil and Δln P_non-energy, re-estimated on every 20-year window, with HC1 standard errors.

- **Result:** −0.30 for the window ending FY1989; about −0.25 to −0.27 through the 2000s; −0.16 by FY2015;
  −0.11 for the window ending FY2024.
- From about 2013 it runs close to the theory benchmark.
- **Why 20 years?** Long enough to include several oil cycles in each window, short enough to show change.

## Step 4c. Local projections, monthly timing (notebook 05)

**Jordà (2005).** Instead of one model that is iterated forward (like a VAR), run one regression per horizon h:

> ln NTT_{t+h} − ln NTT_{t−1} = a_h + β_h·Δln Brent_t + φ_h·Δln Brent_{t−1} + ψ_h·Δln NTT_{t−1} + u_{t+h}

- β_h is the cumulative response of the ToT h months after a 1% oil price change.
- h = 0, 1, …, 6. HAC standard errors with h + 1 lags, because overlapping horizons create serial correlation.
- 79 to 85 monthly observations (April 2019 to June 2026).

**Result.**

| h (months) | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| β_h | −0.02 | −0.23 | **−0.39** | −0.37 | −0.28 | −0.30 | −0.37 |

Nothing happens in month 0. The effect builds in one to three months and stays.

**Why local projections and not a VAR?** With only about 85 months, a VAR's impulse responses depend heavily on
getting the whole lag structure right. Local projections estimate each horizon directly, so a mistake at one
horizon does not carry over to the others. The cost is wider confidence bands, which we accept.

---

## Step 5. Supply-driven vs demand-driven oil prices, for H3 (notebook 06)

**Step 1, split each oil price change.** Regress the monthly oil price change (February 1975 to March 2026,
612 months) on Baumeister and Hamilton's four structural shocks, each with two lags:
- oil supply;
- economic activity;
- oil consumption demand;
- oil inventory demand.

R² = 0.80, so the four shocks explain most oil price movements.
- **Supply part:** the fitted contribution of the supply shocks.
- **Demand part:** the fitted contribution of the other three shocks.

**Step 2, compare.** Regress ToT changes on the two parts and test whether their coefficients are equal. This is
done in three samples:
- annual goods-and-services ToT (fiscal-year sums of the monthly parts);
- annual merchandise ToT;
- monthly merchandise ToT, as three-month cumulative effects.

**Result.** Demand-driven rises hurt at least as much in all three. Equality is never rejected (p = 0.53 to 0.71).

| Sample | Supply-driven | Demand-driven | p (equal) |
|---|---|---|---|
| Annual G&S, FY1975–2025 | −0.07 (0.07) | −0.11 (0.05) | 0.71 |
| Annual merchandise, FY1995–2024 | −0.03 (0.10) | −0.13 (0.09) | 0.55 |
| Monthly, 3-month cumulative, 2019–26 | −0.24 (0.17) | −0.37 (0.09) | 0.53 |

**Cross-check with Känzig (2021).** These are oil supply *news* shocks, measured from oil futures prices in a
narrow window around OPEC announcements. India cannot cause them, so they settle the endogeneity worry. One
shock raises oil prices about 10% on impact.
- **Annual:** ToT falls 0.95% per shock (s.e. 0.49), an elasticity of about −0.1.
- **Monthly:** ToT falls 4.2% at two months and 4.7% at three months, an elasticity of about −0.4 to −0.5.

Pure supply shocks clearly hurt India, but not more than demand shocks.

**Why Baumeister–Hamilton and not Kilian (2009)?** Kilian assumes the oil supply curve is completely vertical
within a month. Baumeister and Hamilton replace that strict assumption with Bayesian priors on the elasticities.
They find supply shocks matter more than Kilian's method suggests, which made them the tougher test for H3.

**Traps.**
- "Your supply and demand parts are estimated, so aren't your second-step standard errors too small?" Yes, in
  principle. That is the generated-regressor problem. But the first stage is very precise (612 months, R² = 0.80),
  and our conclusion is that the two effects are *not* different. Larger standard errors would only make that
  conclusion stronger.
- "The BH shocks are about the US/world economy. Why do they apply to India?" They identify why the *world* oil
  price moved. India takes that price from the world market, so the source of the world price move is exactly
  what we need.

---

## What we deliberately did not do

- **No VAR for the annual data.** With 54 years, a VAR with three or four variables and two lags uses up too many
  degrees of freedom. ARDL is more economical.
- **No GARCH or volatility models.** Our question is about the level of the terms of trade, not its volatility.
- **No quantum-index measures** (income or gross ToT), because the DGCI&S export quantum index is unreliable.
- **No trade-balance regression.** The trade balance mixes prices and volumes and depends on income and the rupee.
  The terms of trade is the pure price channel that trade theory is about.

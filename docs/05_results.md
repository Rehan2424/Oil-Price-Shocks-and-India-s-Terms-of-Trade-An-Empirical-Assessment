# Results

All numbers come from [`../output/tables/`](../output/tables/), produced by the notebooks in [`../code/`](../code/).

## Headline findings

| | Finding | Key numbers |
|---|---|---|
| **H1** | Oil price rises **worsen** India's terms of trade. | Short-run elasticity **−0.24** (goods & services, s.e. 0.04 robust) and **−0.28 to −0.30** (merchandise). Monthly: **−0.39** after 2 months. |
| **H2** | Rises and falls have **roughly symmetric** effects. **Not supported.** | Short-run symmetry never rejected (p = 0.54–0.91). Long-run asymmetry only when the 1970s are included; disappears for FY1980–2024 (p = 0.28). |
| **H3** | Supply-driven increases do **not** hurt more than demand-driven ones. **Not supported.** | Annual: supply −0.07 vs demand −0.11 (p equal = 0.71). Monthly 3-month: −0.24 vs −0.37 (p = 0.54). |
| **Exposure** | India's sensitivity has **roughly halved**, in line with its rising refined-product exports. | Rolling elasticity −0.30 (window to FY1989-90) → −0.11 (to FY2024-25). Benchmark s_x − s_m: −0.25 (1999-00) → −0.10 (2025-26). |
| **Theory test** | The trade-share benchmark explains direction and magnitude. | Coefficient 1.70 (s.e. 0.38); cannot reject = 1 at 5% (p = 0.07). |

## 1. Stylized facts (notebook 01)

ToT changes in oil episodes (fiscal-year averages):

| Episode | Real oil price | ToT goods & services | ToT merchandise |
|---|---|---|---|
| 1973 OPEC embargo (FY72→74) | +284% | −38.6% | – |
| 1979 Iranian revolution (FY78→80) | +110% | −19.2% | – |
| 1990 Gulf war (FY89→90) | +21% | −9.8% | – |
| 2014-16 collapse (FY13→15) | −50% | −1.0% | **+19.4%** |
| 2022 Russia–Ukraine (FY20→22) | +83% | −14.4% | **−23.7%** |

**Monthly episodes:**
- **2022:** Feb→Jun 2022, merchandise ToT **−16.1%** while Brent rose 25%.
- **2026 Hormuz crisis:** Feb→Jun 2026, ToT **−13.1%**. In Feb→Apr 2026, export unit values rose **+18.1%** against **+15.7%** for imports, so the fall came with a lag. The refining hedge delayed it.

## 2. H1: ARDL (notebook 03, FY1970-71 to FY2024-25, N = 54)

| | Estimate | s.e. | p |
|---|---|---|---|
| Short-run oil elasticity | **−0.241** | 0.049 (HC1: 0.040) | 0.000 |
| Long-run oil elasticity | −0.092 | 0.059 | 0.12 |
| Error-correction speed α | **−0.308** | 0.086 | 0.001 |
| Bounds F | 4.74 | p vs I(0) = 0.025, vs I(1) = **0.070** | |

- **Diagnostics:**
  - No serial correlation (BG p = 0.90), normal errors (JB p = 0.26), correct functional form (RESET p = 0.84).
  - Heteroskedasticity detected (BP p = 0.02), so HC1 robust s.e. are reported; the conclusions are unchanged.
  - CUSUM and CUSUMSQ stay inside the 5% bands.
- **Robustness:** short-run elasticity of −0.20 to −0.28, significant in all six specifications.
- **Interpretation:** oil shocks hit India's ToT **hard and fast but temporarily**. About 31% of the deviation closes each year, and the long-run effect is small. This matches the L13 time-horizon logic: short-run fixity, long-run adjustment.

## 3. H2: NARDL (notebook 04)

- **Baseline:** long-run effect of a rise **−0.16** vs a fall **−0.23** (p = 0.035).
- **Not robust:**
  - p = 0.05 with an extra lag.
  - p = 0.08 for FY1975–2024.
  - p = 0.28 for FY1980–2024.
  - Reversed (not significant) for merchandise.
- **Short-run symmetry is never rejected.**
- **Conclusion:** effectively symmetric. India gains from oil price falls about as much as it loses from rises.

## 4. Size, exposure, dynamics (notebook 05)

- **Benchmark test:** coefficient 1.70 (HAC s.e. 0.38); p(coef = 0) < 0.001; p(coef = 1) = 0.07. The plain merchandise elasticity is −0.30 (s.e. 0.06), against an average benchmark of −0.16 over the same years. The extra comes from indirect channels: fertiliser, petrochemicals, freight (CIF).
- **Rolling elasticity:** −0.30 → −0.25 (2005) → −0.16 (2015) → −0.11 (2024). The estimate converges to the theory benchmark after about 2013.
- **Monthly local projections:**

  | Months after the change | 0 | 1 | 2 | 3 | 6 |
  |---|---|---|---|---|---|
  | Elasticity | −0.02 | −0.23 | **−0.39** | −0.37 | −0.37 |

  The effect builds over 1–3 months: contract pricing and shipping lags.

## 5. H3: why oil got expensive (notebook 06)

| Sample | Supply-driven | Demand-driven | p (equal) |
|---|---|---|---|
| Annual G&S ToT, FY1975–2025 | −0.07 (0.07) | **−0.11 (0.05)** | 0.71 |
| Annual merchandise, FY1995–2024 | −0.03 (0.10) | −0.13 (0.09) | 0.55 |
| Monthly, 3-month cumulative | −0.24 (0.17) | **−0.37 (0.09)** | 0.54 |

- **Känzig OPEC supply-news shocks:**
  - Annual: −0.95% per shock (≈ −0.1 elasticity; s.e. 0.49).
  - Monthly: −4.2% and −4.7% at 2–3 months (≈ −0.4 to −0.5).
- **Interpretation:** a global demand boom raises *all* the commodity prices India imports (gold, coal, fertiliser, edible oils, metals), not just oil. Offer-curve "case B" softening does not appear for India; the import-commodity channel dominates.

## 6. Theory applications (notebook 02)

- **RCA in refined petroleum (SITC 334):** 0.06 (1999) → 1.26 (2000) → 4.37 (2025). RCA in crude ≈ 0.
- **Grubel–Lloyd for oil:**
  - 0.55 (2025) when crude and products are treated as one industry.
  - 0.10 when they are measured separately.

  The aggregation effect warned about in L17.
- **Refined-export unit value ÷ crude-import unit value:** 1.23–1.41, i.e. vertical, value-adding trade (L20).
- **India's oil demand:** 5.4% of world consumption, 3rd largest (EIA 2024). India is not a pure price-taker, which is why we use exogenous shocks.
- **Import bill vs volume:** the bill moves with the oil price (correlation of annual changes 0.96); volume does not fall when prices rise. Partial-equilibrium inelastic demand.

## 7. Limitations (say these before the examiner does)

1. Unit value indices are not true price indices: they mix composition and quality changes. The 2012-13-base export *quantum* index is erratic, so we do not use it.
2. Monthly DGCI&S data exist only from April 2019 (87 months), so monthly estimates have wide bands.
3. The goods-and-services ToT includes services (software), which dilutes the oil effect. The merchandise series is shorter.
4. Imports are valued CIF and exports FOB, so freight and insurance spikes also move measured ToT (L14).
5. The 2026 Hormuz shock is still unfolding: data run to June 2026 (ToT) and March 2026 (BH shocks).
6. Official series contained errors that we corrected (see `docs/03_data.md`). Results could change if RBI revises them.

## 8. Policy implications

- **Buffers matter more than direction:** with symmetric effects, India needs tools that smooth both rises and falls:
  - Strategic petroleum reserves.
  - A fuel-tax buffer (cut excise in spikes, rebuild in slumps).
  - Hedging.
- **Refining is a natural hedge:** keep building the acquired comparative advantage. More refined and petrochemical exports raise s_x and shrink the net exposure.
- **Diversify suppliers:** this is L16's pro-competitive effect. More sources (e.g., the shift towards Russian crude after 2022) mean less exposure to any one supplier's market power and a lower effective import price.
- **Demand-driven booms hurt too:** diversify beyond oil (energy transition, ethanol blending, renewables) to cut broad commodity-import exposure.

# Applied Theory Framework

**Rule for the presentation:** no theory slide stands alone. Every concept appears only as **(1)** how it works in India's oil case, plus **(2)** a number or chart from our data. Plain definitions go in the viva notes, not on slides.

Lecture numbers refer to [`course-material/lectures/`](../course-material/lectures/).

---

## 1. The setting

Treat the world as two "countries", as in L21–L22:
- **India (A)** exports a composite good **X**: manufactures, services-linked goods, and refined petroleum products. It imports **Y**: crude oil.
- **Rest of world incl. OPEC+ (B)** exports oil and imports X.

India's terms of trade is **P_X / P_Y**. With many goods, this is the **net barter terms of trade** = export unit value index / import unit value index × 100 (L21's own definition). It is exactly the series published by DGCI&S and the RBI, which we use as our dependent variable.

---

## 2. Core application: offer curves (L22, L21)

**The diagram (drawn for India, not generic):**
- Horizontal axis: India's exports X. Vertical axis: oil Y.
- India's offer curve OC_IN bows toward the oil axis. The rest of world's curve OC_W bows toward the X axis.
- India's ToT is the slope of the ray from the origin through the point where the curves cross. A **steeper ray means better ToT** for India.

| Case | What happens in the diagram (L22 rule applied) | Prediction for India's ToT | Real episode |
|---|---|---|---|
| **A. Oil supply shock** (OPEC+ cut, war, sanctions) | Rest of world offers less oil for every unit of X. OC_W shifts toward the X axis. This is the L22 "tariff" logic with the oil exporter as the one restricting trade: its ToT improves and India's worsens. | **ToT falls sharply.** Trade volume falls. | 1990 Gulf War (India's 1991 BoP crisis); 2022 Russia–Ukraine |
| **B. World demand boom** | The rest of world also wants more of India's exports, so OC_W shifts *up* (L22: "increased demand for imports by B, so A's ToT improves"). At the same time, oil is scarcer. The two effects partly cancel. | **ToT falls less** than in case A | 2003–08 commodity boom |
| **C. India's own demand growth** | India demands more oil imports, so OC_IN shifts out. L22: "volume of trade increases, but A's terms of trade go down". | **ToT falls**: India is not a pure price-taker | 2000s–2010s rising Indian oil demand |
| **D. Oil glut** (supply surge, demand collapse) | The reverse of case A | **ToT improves** | 2014–16 collapse; 2020 COVID crash |

**Elasticity point:** India's short-run oil demand is price-inelastic. When OC_W shifts, most of the adjustment shows up in **price (ToT)** rather than **volume**.
- *Data check:* crude import volumes (RBI Table 32, UN Comtrade) barely respond to price: an elasticity of 0.16, while the import bill moves almost one-for-one with the oil price (correlation 0.96). See notebook 02.

**These cases are our hypotheses:**
- **H1 (case A):** an oil price rise worsens India's ToT.
- **H3 (case A vs B):** supply-driven shocks hurt more than demand-driven ones.

---

## 3. How big should the effect be? A benchmark from the definition of ToT

From NTT = UV_X / UV_M, taking logs and differentiating for oil-linked items:

> **d ln(NTT) ≈ (s_x − s_m) · d ln(P_oil)**

where s_x and s_m are oil's shares in India's export and import baskets.
- Since s_m > s_x, the sign is negative (H1). The **size is predicted by the data before any regression**.
- We compare the regression elasticity with this benchmark.
- Possible gaps and their causes:
  - **Estimate more negative than the benchmark:** indirect effects such as petrochemicals, fertiliser and freight.
  - **Estimate less negative:** India's other export prices rise with world demand (case B).

*Data:* oil shares from the RBI Handbook / DGCI&S principal-commodity trade tables, year by year. The benchmark changes as India's refined-product exports grew.

---

## 4. Why India is partly hedged: acquired comparative advantage in refining (L08, L16, L19–L20)

| Concept | Application | What we compute |
|---|---|---|
| **Balassa RCA** (L08) | India has little crude but large refining capacity, so it may have an *acquired* comparative advantage (L19: Lancaster) in refined products | RCA for refined petroleum (HS 2710 / SITC 334) over time. Primary source UNCTADstat (cited in L08); cross-check UN Comtrade |
| **Internal economies of scale** (L16–L17) | Large refineries cut average cost (AC = F/Q + c), which is the source of that advantage | Viva point |
| **Grubel–Lloyd index and aggregation** (L17, L19) | India both imports and exports "mineral fuels" (HS 27), so it looks intra-industry at HS-2. At HS-4 (2709 crude vs 2710 products) it is inter-industry. L17: "the more broadly an industry is defined, the more trade appears to be intra-industry" | GL at HS-2 vs HS-4 (backup slide) |
| **Vertical differentiation / unit values** (L20) | India imports a lower-value input (crude) and exports a higher-value product (refined fuels). The unit-value gap is value addition: the "refining margin" hedge | Export unit value of 2710 vs import unit value of 2709 |

**Link to the benchmark (section 3):** this refining advantage is exactly why s_x > 0, which shrinks India's net exposure (s_m − s_x).

---

## 5. Oil market: partial equilibrium and monopoly power (L21, L16)

| Concept | Application | What we show |
|---|---|---|
| **Partial equilibrium import market** (L21) | India's crude import demand (inelastic) meets world export supply. A supply shock shifts supply up: the price rises a lot, volume falls a little, so the **import bill jumps** | Crude import volume vs value in shock years |
| **PE vs GE** (L21) | PE explains the oil bill. GE (offer curves) explains ToT. Our regression adds controls (REER, world demand, non-oil commodity prices) because "changes in one market affect other markets" | Justifies our control variables |
| **Aggregation bias** (L21) | Aggregate trade hides that oil behaves differently from everything else | Why we split oil and non-oil |
| **Monopoly markup** (L16): p(1 − 1/e) = MC | OPEC+ acts as a dominant supplier. Inelastic world demand gives a high markup and makes supply cuts very effective. Cartels defend price floors, so falls may be shorter than rises (H2: asymmetry) | Our supply-shock series is built from OPEC announcements (Känzig 2021) |
| **Pro-competitive effect** (L16) | More suppliers means a lower markup. India's diversification of crude sources (e.g., Russian crude since 2022) lowers its effective import price | Indian basket (PPAC) vs Brent (World Bank) spread |

---

## 6. Welfare and who gains or loses (L11, L13, L12, L14)

| Concept | Application | What we show |
|---|---|---|
| **Trade line and indifference curves** (L11) | A worse ToT rotates India's trade line inward, putting it on a lower indifference curve. That is a real-income loss even if production is unchanged | **ToT income loss ≈ change in net oil import bill as % of GDP** for 2008, 2011–13 and 2022 |
| **Small vs large country** (L11) | India is a top oil consumer, so it is not a pure price-taker (case C). We use shocks that are exogenous to India (OPEC announcements) | Viva point and identification argument |
| **Ricardo–Viner / Stolper–Samuelson** (L13) | Oil price rise raises returns to factors specific to refining and hurts oil-using sectors | Viva point |
| **Time horizons** (L13): very short / medium / long run | Short run vs long run maps directly onto our **error-correction model** (short-run vs long-run elasticity) | Methods slide |
| **H-O endowments** (L12, L14 "skills and land") | Oil is a scarce natural-resource factor in India, so imports are structural. Policy can manage the exposure, not remove it | Viva point |
| **Transport costs** (L14) | Imports are valued CIF, exports FOB. Freight and insurance spikes (war-risk premiums) also lower measured ToT | Limitation slide / viva |
| **Mercantilism** (L06) | Oil shocks widen the trade deficit. The real welfare loss is the ToT effect, not the deficit itself. Gold (a bullion import) moves the import price index, so we control for the gold price | Viva point + control variable |
| **Immiserizing growth** (L18 mention) | If India's growth pushes up oil import demand enough to worsen its ToT, part of the growth gain leaks abroad | Viva point |

---

## 7. Where theory appears in the presentation

There are no standalone theory slides. Each concept turns up where it does some work:

| Slide | Concept | What the audience sees |
|---|---|---|
| 2 Question and hypotheses | Net barter ToT (L21); monopoly power (L16); offer curves (L22) | The definition we measure; where each hypothesis comes from |
| 3 Offer curves for India | Offer curves, tariff case, large country (L22, L11) | Cases A and C drawn for India; ToT ray 1.00 → 0.86; −16% (2022) and −13% (2026) |
| 4 How big should the hit be? | ToT definition (L21); RCA (L08); Grubel–Lloyd (L17, L19) | Benchmark −0.25 → −0.10; RCA 0.06 → 4.37; GL 0.55 vs 0.10 |
| 7 Method | Time horizons (L13) | Short run vs long run, the reason for the error-correction model |
| 10 Symmetric, and half as large | RCA as a hedge (L08, L16) | Rolling elasticity tracking the benchmark |
| 11 H3 | Offer curves, case B (L22) | Why the world-boom softening does not show up for India |
| 12 What it means for India | Pro-competitive effect (L16); refining scale (L08, L16) | Policy: diversify suppliers, grow the refining hedge |
| Backup: refining hedge | Vertical IIT and the unit-value rule (L20) | Refined exports worth 1.2–1.4 times crude imports per tonne |

The rest (partial equilibrium, Ricardo–Viner, H-O, CIF/FOB, mercantilism, immiserizing growth) is in the viva notes,
`viva-notes/01_theory.md`, in definition-plus-application form.

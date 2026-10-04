# 01 · Theory, applied to India

Each concept follows the same pattern: what the lecture says, how it applies to India's oil case, and the number
from our data that goes with it. Lecture numbers (L05 to L22) refer to `course-material/lectures/`.

---

## 1. Terms of trade (L21)

**What it is.** With many goods, the terms of trade is the ratio of the export price index to the import price
index. L21 calls it the commodity or net barter terms of trade:

> NTT = (P_X / P_M) × 100

In Indian data, the price indices are DGCI&S **unit value indices** (UVI): value divided by quantity, for a fixed
basket of commodities. A rise in NTT is an improvement, because each unit of exports buys more imports.

**Related measures, and why we don't use them.**
- *Income terms of trade* = NTT × export volume index. It measures the import capacity of exports.
- *Gross barter terms of trade* = import volume / export volume.

Both need the DGCI&S **quantum** indices. The export quantum index on the 2012-13 base is erratic (monthly
values from 54 to 2001), so we use price indices only.

**Our two measures.**
- **Merchandise NTT** (DGCI&S and RBI): goods only, the textbook definition.
- **Goods-and-services ToT** from the national accounts: the export deflator divided by the import deflator
  (World Bank WDI). It covers 1970 onwards and includes services such as software, which makes it a broader
  measure of India's purchasing power over imports.

---

## 2. Offer curves (L22): the core framework

**What the lecture says.**
- An offer curve shows how much of its export good a country is willing to give for different amounts of its
  import good. It is built from the trade triangles at each relative price, so it carries the country's
  production and preference information.
- Each offer curve bends towards the axis of the country's import good.
- Equilibrium is where the two curves cross. The terms of trade is the slope of the ray from the origin through
  that point.
- Shifts in the curves:
  - **Higher import demand by A:** trade volume rises and A's terms of trade fall.
  - **Higher import demand by B:** A's terms of trade improve.
  - **A tariff:** the tariff country's curve rotates towards its import axis. Trade volume falls and its terms
    of trade improve (if it is large).

**Applied to India.** Two "countries":
- India exports a composite good X (manufactures, services-linked goods, refined fuels) and imports oil Y.
- The rest of the world, including OPEC+, exports oil and imports X.
- With X on the horizontal axis and Y on the vertical axis, the ray's slope is Y/X: oil received per unit of
  exports, which is P_X/P_Y, India's terms of trade. A **flatter ray is worse** for India.

| Case | What shifts | Prediction | When it happened |
|---|---|---|---|
| **A. Supply cut** (OPEC+ cut, war, sanctions) | The rest of the world offers less oil for each unit of X; its curve rotates towards the X axis. It is the L22 tariff case with the oil exporter doing the restricting. | India's ToT falls, a lot | 1973, 1979, 1990, 2022, 2026 |
| **B. World demand boom** | The rest of the world wants more oil *and* more of India's exports, so both effects work at once | Ambiguous in theory; this is our H3 | 2003–08 |
| **C. India's own demand grows** | India offers more X for oil; India's curve shifts out | India's ToT falls (India is not a price-taker) | 2000s and 2010s |
| **D. Oil glut** | The reverse of A | India's ToT improves | 2014–16, 2020 |

**Numbers.**
- In our stylised diagram (slide 3), India's terms of trade fall from 1.00 to 0.86 in case A.
- The data: after the 2022 shock, India's merchandise ToT fell 23.7% (FY2020-21 to FY2022-23).
- In 2014–16 (case D), the merchandise ToT rose 19.4%.

**The elasticity point.** India's short-run oil demand is very inelastic. When the rest of the world's curve
shifts, almost all of the adjustment shows up in the price (ToT), not the volume.
- Our data: the elasticity of crude import volume to the oil price is only 0.16 (s.e. 0.09).
- The correlation between changes in the oil import bill and changes in the oil price is 0.96.

---

## 3. How big should the effect be? A benchmark from the definition

Start from NTT = P_X / P_M and split both indices into oil and non-oil parts with value shares s_x (oil in
exports) and s_m (oil in imports). Take logs and differentiate, holding non-oil prices fixed:

> d ln NTT ≈ s_x · d ln P_oil − s_m · d ln P_oil = **(s_x − s_m) · d ln P_oil**

- **The sign:** India's oil share of imports (about 26% on average) is larger than of exports (about 10%),
  so the effect is negative. That is H1.
- **The size:** the benchmark gives the elasticity before any regression. It was −0.25 in FY1999 and is
  about −0.10 in FY2025.
- **Why it shrank:** s_x rose from about 3% in FY1990 to between 9% and 22% since FY2008 (22% in FY2022). The big private refineries at
  Jamnagar (1999, expanded in 2008) turned India into a large exporter of refined fuels.

**What the regression adds.** We test whether the actual effect matches the benchmark (coefficient 1.70; we
cannot reject 1). Being a bit bigger makes sense, because oil also raises the prices of fertiliser,
petrochemicals, plastics and freight, which the direct-share formula ignores.

---

## 4. Trade line, welfare and the small-country assumption (L11)

**Welfare.** With trade, a country consumes on its trade line, whose slope is the terms of trade. A worse ToT
rotates the trade line inwards: the country reaches a lower community indifference curve even if production
does not change. So a ToT loss is a **real-income loss**, not just a bookkeeping change.
- A rough size: net oil imports were 3.0% of GDP in FY2025 and 5.6% at the FY2012 peak. A 10% rise in oil
  prices costs roughly 0.3% of GDP in purchasing power at today's shares.

**Small vs large country.** A small country takes world prices as given. India is not small in oil: it uses
5.4% of world oil (EIA, 2024), third after the US and China.
- That is case C: India's own demand growth can push up the oil price and worsen its own terms of trade.
- For the regressions this means **endogeneity**: part of the oil price movement may be caused by India.
  That is why H3 uses shocks India cannot cause (Baumeister–Hamilton supply shocks; Känzig's OPEC news shocks).

---

## 5. Comparative advantage and RCA (L08)

**Balassa's revealed comparative advantage:**

> RCA_ij = (X_ij / X_i) / (X_wj / X_w)

India's share of product j in its exports, divided by the world's share of j in world exports. RCA above 1
means India exports relatively more of j than the world does.

**Applied.**
- **Refined petroleum (SITC 334):** 0.06 in 1999, 1.26 in 2000, **4.37** in 2025.
- **Crude (SITC 333):** about 0.

India has almost no oil but a strong *acquired* comparative advantage in refining it. L05 even lists "fuels" among the
goods in which India has a comparative advantage in the world market. This is the main reason India's exposure to oil prices has fallen.

---

## 6. Economies of scale and monopoly power (L16)

**Scale.** Average cost AC = F/Q + c falls with output when fixed costs are large. Refineries are a textbook
case: Jamnagar is the world's largest refining complex. Scale is the source of the acquired advantage in §5.

**Monopoly markup.** MR = p(1 − 1/e) = MC, so the markup (p − MC)/p = 1/e. The less elastic the demand, the
bigger the markup.
- OPEC+ behaves like a dominant supplier. Short-run world oil demand is inelastic, so supply cuts raise the
  price sharply. This is case A in the offer-curve diagram.
- It also motivated H2: a cartel defends price floors by cutting output, so falls might be smaller than rises.
  The data do not show that.

**Pro-competitive effect.** More sellers mean a smaller markup. When India diversifies its crude suppliers
(for example, buying more Russian crude after 2022), no single seller has as much market power over it.

---

## 7. Intra-industry trade: Grubel–Lloyd and the aggregation trap (L17, L19, L20)

**Grubel–Lloyd index (L19):**

> GL = 1 − |X − M| / (X + M)

GL is 0 when trade is one-way (pure inter-industry) and 1 when exports equal imports (pure intra-industry).

**The aggregation trap (L17):** "the more broadly an industry is defined, the more trade appears to be
intra-industry". India both imports and exports "mineral fuels" (HS chapter 27).
- Treat crude and products as one industry and GL is **0.55**: it looks like intra-industry trade.
- Measure crude (HS 2709) and products (HS 2710) separately and GL is **0.10**: it is really inter-industry.

**Horizontal vs vertical (L20).** Unit values separate the two. If export and import unit values are within
±15% of each other, the goods are horizontally differentiated (similar quality). Otherwise the trade is vertical.
- India's refined-export unit value is **1.13 to 1.41 times** its crude-import unit value per tonne
  (2000–2025), outside ±15% in every year except 2011 and 2012.
- So this is vertical, value-adding trade: India imports a raw input and exports a processed product. The
  refining margin is the hedge.

---

## 8. Partial and general equilibrium (L21)

**Partial equilibrium** looks at one market at a time. India's crude import demand is inelastic and the world
supply curve shifts with OPEC+ decisions.
- A supply cut raises the price a lot and lowers the volume a little, so the **import bill jumps**.
- Our data: bill and price move together (correlation 0.96); volume barely responds (elasticity 0.16).

**General equilibrium.** Offer curves are general equilibrium: they bring in what happens in the other market
too. In our regressions this is why we control for non-oil commodity prices: "changes in one market affect other
markets".

**Aggregation bias.** L21's apples-and-oranges warning is why we split oil from non-oil trade and do not treat
India's trade as one good.

---

## 9. Time horizons, distribution and endowments (L12, L13)

**Time horizons (L13).**
- **Very short run:** all factors fixed.
- **Medium run:** some factors specific (Ricardo–Viner).
- **Long run:** everything mobile (Heckscher–Ohlin–Samuelson).

Our error-correction model has exactly this structure. The short-run elasticity (−0.24) is the effect before
anything adjusts; α = −0.31 is how fast the economy adjusts; the long-run elasticity (−0.09) is what is left
after adjustment.

**Who gains and who loses (L13).** In the Ricardo–Viner model, a higher oil price raises the return to factors
specific to refining and hurts oil-using sectors (transport, fertiliser, airlines). Stolper–Samuelson: a change in
relative prices helps the factor used intensively in the good whose price rose.

**Endowments (L12).** India is poorly endowed with oil, a natural-resource factor. So crude imports are
structural, and policy can manage the exposure but cannot remove it.

---

## 10. Transport costs, CIF and FOB (L14)

- Imports are valued **CIF** (cost, insurance and freight).
- Exports are valued **FOB** (free on board).

So a jump in freight or war-risk insurance (Red Sea in 2024, Hormuz in 2026) raises measured import prices and
lowers the measured ToT, even if the oil price itself did not change. We list this as a limitation.

---

## 11. Mercantilism and immiserizing growth (L06, L18)

**Mercantilism (L06).** A mercantilist would say the loss from an oil shock is the bigger trade deficit. Modern
theory says the real loss is the fall in purchasing power, which is the ToT effect. The deficit is the financing
side. Gold, a bullion import that India buys in large amounts, also moves India's import prices. That is why one
robustness check controls for the gold price.

**Immiserizing growth (L18, Bhagwati 1958).** If India's growth raises its oil import demand enough to worsen
its terms of trade (case C), part of the gain from growth leaks abroad. It needs very inelastic foreign supply,
so it is a warning rather than India's actual situation.

---

## 12. Ideas outside our lecture set that examiners like to ask about

These are standard international economics. They are not in the 16 lectures we used, so keep the answers short.

- **Harberger–Laursen–Metzler effect.**
  - A worse ToT lowers real income; households smooth consumption, so saving falls and the current account worsens.
  - This links our ToT result to India's balance-of-payments stress in 1990-91, 2013 and 2022.
- **Prebisch–Singer hypothesis.**
  - Primary-commodity exporters face a long-run decline in their terms of trade against manufactures.
  - India is the opposite case: it *imports* the commodity. A long-run fall in commodity prices would help India,
    which is consistent with the merchandise ToT gains when oil collapsed in 2014–16.
- **Marshall–Lerner condition and J-curve.**
  - A depreciation improves the trade balance only if the export and import demand elasticities sum to more than one.
  - Oil demand is inelastic, which is why a weaker rupee does little for India's oil bill in the short run.
  - That is also why we model the terms of trade, not the trade balance.
- **Dutch disease.** A resource boom raises the real exchange rate and hurts other tradables. It applies to oil
  *exporters*. For India the mirror image is the rupee weakening in oil shocks (Ghosh 2011).
- **Real effective exchange rate (REER).** The trade-weighted relative price of Indian goods. We collected the BIS
  and RBI series but kept them out of the main models. The terms of trade is already a relative price, and the
  REER itself reacts to oil shocks, so controlling for it would absorb part of the effect we want to measure
  (a "bad control").

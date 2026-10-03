# Project Plan

**Oil Price Shocks and India's Terms of Trade: An Empirical Assessment**
International Economics, group assignment (4 members). Deliverable: a 15-minute presentation followed by a 15-minute viva.

---

## 1. Research question

How do oil price shocks affect India's terms of trade (ToT)? Does the effect depend on **whether oil prices rise or fall** and on **what caused the shock** (supply disruption vs. a global demand boom)?

## 2. Core idea and mechanism

India imports most of the crude oil it uses but also exports refined petroleum products. The net barter terms of trade is

> NTT = (Export unit value index / Import unit value index) × 100

To a first approximation, the change in NTT caused by an oil price change is

> d ln(NTT) ≈ (s_x − s_m) · d ln(P_oil)

where `s_x` and `s_m` are oil's shares in the export and import baskets. Because `s_m > s_x` for India, theory predicts that higher oil prices **worsen** India's ToT. It also gives a **predicted magnitude**, which we compare with our estimated elasticity.

Other channels to discuss:
- Global demand: when an oil rise is driven by a world boom, India's export prices also rise.
- Exchange-rate / BoP: wider CAD, so rupee pressure.
- Dollar invoicing (dominant-currency pricing).

## 3. Hypotheses

| | Hypothesis | Method |
|---|---|---|
| **H1** | Higher oil prices worsen India's net barter ToT, with a size close to the net oil-share benchmark | ARDL (long run + error correction) |
| **H2** | ToT responds asymmetrically to oil price increases vs. decreases | NARDL |
| **H3** | Supply-driven oil shocks hurt ToT more than demand-driven ones | Local projections with identified oil shocks |

## 4. Course theory, applied rather than explained alone

**Rule:** no theory slide stands alone. Each concept appears as *how it works in India's oil case* plus *a number or chart from our data*. Full mapping: [`01_theory_framework.md`](01_theory_framework.md). Per-lecture notes: [`../theory/lecture_digest.md`](../theory/lecture_digest.md).

| Concept (lecture) | How we apply it |
|---|---|
| **Offer curves** (L22, L21) | India vs rest-of-world (incl. OPEC+) offer curves. Oil supply shock, world demand boom and India's demand growth each shift a curve and rotate India's ToT ray. This gives H1 and H3 |
| **Net barter ToT definition** (L21) | Export unit value index / import unit value index: exactly our DGCI&S/RBI series |
| **Comparative advantage, Balassa RCA** (L08) | RCA of India's refined petroleum exports: an acquired advantage that partly hedges oil shocks |
| **Grubel–Lloyd, vertical IIT** (L19, L20, L17) | India imports crude and exports refined fuels. GL at HS-2 vs HS-4 shows the aggregation effect; the unit-value gap shows value addition |
| **Partial equilibrium** (L21) | India's inelastic crude import demand: price spikes raise the import bill with little volume change |
| **Monopoly markup, scale economies** (L16, L17) | OPEC+ markup p(1 − 1/e); cuts are effective because demand is inelastic. Diversifying crude suppliers is a pro-competitive gain. Refining scale is the source of India's RCA |
| **Standard trade model, small vs large country** (L11) | A worse ToT rotates India's trade line, giving a real income loss (net oil import bill as % of GDP). Is India a price-taker? |
| **Ricardo–Viner, time horizons** (L13) | Winners and losers of oil shocks; short run vs long run maps onto our error-correction model |
| **H-O endowments, transport costs** (L12, L14) | Oil-scarce endowment makes the exposure structural. The CIF/FOB wedge is a limitation of the ToT measure |
| **Mercantilism, immiserizing growth** (L06, L18) | Viva points: trade deficit vs ToT welfare loss; growth-driven oil demand worsening ToT |

Historical hooks: 1990–91 Gulf War and India's BoP crisis; 2008 spike; 2014–16 collapse; 2020 COVID crash; 2022 Russia–Ukraine shock and discounted Russian crude.

## 5. Literature review (short: about 12–15 references in 4 strands)

Every reference is verified against its journal page or DOI before it is used.

1. **Why ToT matter:**
   - Prebisch (1950); Singer (1950)
   - Harberger (1950); Laursen & Metzler (1950)
   - Mendoza (1995); Schmitt-Grohé & Uribe (2018)
2. **Oil and ToT / external balances:**
   - Backus & Crucini (2000), *Oil prices and the terms of trade* (our anchor paper)
   - Kilian, Rebucci & Spatafora (2009)
3. **Defining and identifying oil shocks:**
   - Hamilton (1983, 2003); Mork (1989)
   - Kilian (2009); Baumeister & Hamilton (2019); Känzig (2021)
4. **India evidence:**
   - Tiwari & Olayeni (2013)
   - Bhanumurthy, Das & Bose (2012)
   - Deheri & Sahu (2024)
   - Selected RBI studies
5. **Gap (to be confirmed):** Indian studies mostly look at the trade balance, inflation or the exchange rate. Few model the ToT directly, test for asymmetry, separate supply shocks from demand shocks, or cover 2022–25.

## 6. Data (official sources only)

| Variable | Primary source | Cross-check |
|---|---|---|
| Net barter ToT, export and import unit value indices, income ToT (annual, FY 1980-81 onward) | RBI *Handbook of Statistics on the Indian Economy*, Table 127 (DGCI&S data) | World Bank WDI `TT.PRI.MRCH.XD.WD` |
| Monthly export and import unit value indices (2012-13 = 100; new 2022-23 = 100 series) | DGCI&S Foreign Trade Indices | Recompute NTT = UVx / UVm × 100 |
| Crude oil prices: Brent, Dubai, average (monthly) | World Bank Pink Sheet | FRED (Brent) |
| Indian crude basket | PPAC (Ministry of Petroleum) | World Bank Dubai/Brent (basket is a weighted mix) |
| Crude import volume and value; import dependence | PPAC | RBI Handbook trade tables |
| Real oil price deflator | World Bank MUV index | US CPI |
| Real effective exchange rate | RBI 40-currency REER | BIS REER |
| Non-fuel commodity prices; gold price | World Bank Pink Sheet | — |
| Oil shares of exports and imports | RBI Handbook / Commerce Ministry TradeStat | DGCI&S |
| RCA of refined petroleum; HS 27/2709/2710 trade (for GL index and unit values) | UNCTADstat (cited in L08) | UN Comtrade |
| India's share of world oil consumption | Energy Institute *Statistical Review of World Energy* | US EIA |
| GDP (for ToT income loss as % of GDP) | MoSPI / RBI Handbook | World Bank WDI |
| Identified oil shocks (monthly) | Känzig (2021) oil supply news shocks; Baumeister & Hamilton (2019) | — |

**Data-quality rules:** see [`../data/SOURCE_POLICY.md`](../data/SOURCE_POLICY.md). The short version:
- Only official agencies, international organisations, or peer-reviewed replication data. No Kaggle, Statista, news sites or blogs.
- Raw files are never edited.
- Every file is logged with its URL, table, date, units, base year and checksum.
- Every key series is cross-checked against a second source.
- Fiscal years (April–March) are aligned in code.
- One teammate hand-checks 10 random values against the original publications.

## 7. Analysis

**Tier 1: Annual, long run (FY 1980-81 to 2024-25)**
1. Stylized facts: oil price vs ToT chart with episodes marked; oil shares over time; the theory-benchmark elasticity.
2. Unit root tests: ADF, PP, KPSS; Zivot–Andrews structural-break test.
3. **ARDL bounds test:** long-run oil elasticity of ToT plus the error-correction speed. Controls: REER, non-fuel commodity prices, gold price, world demand.
4. Diagnostics: serial correlation, heteroskedasticity, normality, RESET, CUSUM/CUSUMSQ.
5. **NARDL:** separate effects of oil price rises and falls (asymmetry tests, dynamic multipliers).
6. Rolling-window elasticity: has India's exposure changed since refined-product exports surged around 2008?

**Tier 2: Monthly, causal (2012 onward)**
- **Local projections** of ToT on identified oil supply shocks and demand shocks, showing impulse responses over 0–12 months.

**Robustness (backup slides):**
- Alternative ToT measures and oil price measures
- Hamilton net oil price increase
- Sub-samples
- Small VAR

Software: Python notebooks committed with outputs, so they display directly on GitHub. An Excel copy of the final dataset is also provided.

## 8. Deliverables

### Presentation
15 minutes, about 13 slides plus backup slides for Q&A, with speaker notes. Presenter split:

| Presenter | Section | Time |
|---|---|---|
| P1 | Hook → motivation → theory in action (India vs world offer curves; the ToT benchmark) → hypotheses | ~4 min |
| P2 | Literature and gap → data and stylized facts | ~3.5 min |
| P3 | Methodology → long-run and asymmetry results (H1, H2) | ~4 min |
| P4 | Shock-source results (H3) → robustness → policy → conclusion and limitations | ~3.5 min |

### Viva notes (`viva-notes/`)
Everyone reads the core files; each presenter deep-dives their own section.
- One-page summary: the 60-second pitch and the key numbers.
- Theory notes: every concept used, with a definition, formula and how it applies to India.
- Data notes: every variable, its source, base year and limitations.
- Methods notes: why each method, its assumptions, how to read the output, and common examiner traps.
- Results notes: every coefficient in plain language.
- **Q&A bank of 100+ likely questions with model answers**, tagged by who leads the answer.
- Formula sheet.

## 9. Workflow and checkpoints

| Phase | Output | Checkpoint |
|---|---|---|
| 0. Lectures | `theory/lecture_digest.md`, `docs/01_theory_framework.md` | Team confirms theory emphasis |
| 1. Literature | `docs/02_literature_review.md` | — |
| 2. Data | `data/`, validation log | Team approves dataset |
| 3. Analysis | `code/` notebooks, `output/` | Team agrees on the story |
| 4. Slides + viva notes | `presentation/`, `viva-notes/` | Draft review and rehearsal |

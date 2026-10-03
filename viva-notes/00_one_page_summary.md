# 00 · One-page summary

Everyone should know this page cold. If you only have ten minutes before the viva, read this.

## The 60-second version

India buys about 90% of the crude it refines from abroad, so every oil spike raises the price of what India
imports relative to what it exports, the **net barter terms of trade** from lecture 21. We ask three things.
Does an oil price rise worsen India's terms of trade, and by how much (H1)? Do rises and falls have the same
effect (H2)? Does it matter *why* oil became expensive, supply or demand (H3)?

We use official data only (RBI, DGCI&S, PPAC, World Bank, UNCTAD, UN Comtrade, EIA, BIS) and the published
shock series of Baumeister and Hamilton (2019) and Känzig (2021). Annual data run from FY1970-71 to FY2025-26,
and monthly data from April 2019 to June 2026.

**Answers.**
- **H1, yes.** A 10% rise in the real oil price cuts the terms of trade by about 2.4% in the same year. The
  effect is fast (two to three months) but temporary: about 31% of the gap closes every year.
- **H2, no.** Rises and falls have about the same effect.
- **H3, no.** Demand-driven rises hurt at least as much as supply-driven ones, because a world boom also
  raises the prices of gold, coal, fertiliser and metals that India imports.
- **Exposure has roughly halved since the 1990s**, from −0.30 to −0.11. This tracks the trade-share benchmark
  (s_x − s_m), because India became a big exporter of refined fuels (RCA of 4.37). Refining is India's hedge.

## Numbers to know by heart

| What | Number | Where it comes from |
|---|---|---|
| Short-run oil elasticity of ToT (annual, goods and services) | **−0.24** (s.e. 0.049; robust 0.040) | `t03`, ARDL, N = 54 |
| Speed of adjustment α | **−0.31** (31% of the gap closes each year) | `t03` |
| Long-run elasticity | −0.09, not significant (p = 0.12) | `t03` |
| Bounds test | F = 4.74; p = 0.025 vs the I(0) bound, 0.070 vs the I(1) bound | notebook 03 |
| Short-run effect across six specifications | −0.20 to −0.28, all significant | `t04` |
| Monthly elasticity two months after a rise | **−0.39** (almost zero in month 0) | `t08` |
| Benchmark test coefficient (theory says 1) | **1.70**, cannot reject 1 at 5% (p = 0.07) | `t07` |
| Rolling elasticity, window ending FY1989 → FY2024 | **−0.30 → −0.11** | `t08b` |
| Theory benchmark s_x − s_m, FY1999 → FY2025 | **−0.25 → −0.10** | RBI Table 111 |
| NARDL short-run, rise vs fall | −0.27 vs −0.22, symmetry p = 0.62 | `t06` |
| H3, supply vs demand (annual G&S) | −0.07 vs −0.11, equality p = 0.71 | `t09` |
| RCA of refined petroleum, 1999 → 2025 | **0.06 → 4.37** | UNCTADstat |
| Grubel–Lloyd for oil, one industry vs crude and products separately | **0.55 vs 0.10** | UN Comtrade |
| India's share of world oil demand (2024) | 5.4%, third after the US and China | EIA |
| Merchandise ToT, Feb → Jun 2022 and Feb → Jun 2026 | −16.1% and −13.1% | DGCI&S monthly |

Fiscal years are labelled by the year they start: "FY2024" means 2024-25.

## If they ask "what is new in your project?"

1. Indian studies look at the trade balance, inflation or the rupee. We model the **terms of trade itself**,
   which is the price ratio at the heart of the course's trade theory.
2. We test a **theory benchmark** built from the definition of the terms of trade, instead of only reporting
   a regression coefficient.
3. We separate **supply-driven and demand-driven** oil price changes with identified shocks that India cannot cause.
4. We show **exposure has halved** and explain it with RCA and Grubel–Lloyd, two measures from the lectures.
5. We **cleaned the official data**: four errors in RBI and DGCI&S tables were found and fixed.

## Who takes which questions

| Presenter | Leads on | Backs up |
|---|---|---|
| P1 | Motivation, theory (offer curves, terms of trade, small vs large country), hypotheses | Policy |
| P2 | Benchmark, RCA and Grubel–Lloyd, literature, data and the data problems | Theory |
| P3 | Unit roots, ARDL, bounds test, diagnostics, local projections, benchmark test | Data |
| P4 | NARDL (H2), supply vs demand (H3), rolling elasticity, policy, limitations | Methods |

Anyone can take a question, but let the lead answer first and add one sentence at most. Two people giving
long answers to the same question looks unprepared.

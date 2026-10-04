# 02 · Data: what we used, why, and what we fixed

Every raw file is listed with its web address and a checksum in `data/SOURCES.md`. The automatic checks are in
`data/validation_report.md`. This page is the version to remember for the viva.

## Our rule for sources

We used only **official statistical agencies** and the **published replication data of peer-reviewed papers**.
No news sites, no blogs, no Kaggle or data aggregators. FRED was used only to cross-check the World Bank's Brent series.

## The four datasets

| Dataset | Period | Terms-of-trade measure | Used for |
|---|---|---|---|
| Monthly | Apr 2019 – Jun 2026 (87 months) | DGCI&S merchandise NTT, base 2012-13 | Timing (local projections), 2022 and 2026 episodes, H3 monthly |
| Annual, long run | FY1970-71 – FY2025-26 | Goods-and-services ToT, national accounts (WDI) | Main ARDL (H1), NARDL (H2), rolling elasticity, H3 annual |
| Annual, merchandise | FY1994-95 – FY2025-26 | RBI/DGCI&S NTT, chain-linked across three bases | Robustness, benchmark test |
| Calendar-year theory data | 1995/2000 – 2025 | – | RCA, Grubel–Lloyd, unit values, India's share of world oil demand |

**Fiscal years.** All Indian annual data are April to March and labelled by the starting year: FY2024 = 2024-25.
Monthly world prices are averaged over April to March in our code, never mixed with calendar-year averages.
- We checked WDI's labelling: WDI's India "2024" equals RBI's FY2024-25 GDP, so WDI year t is FY t/t+1.
- The MUV index is calendar-year only, so the fiscal-year value is 0.75 × CY t + 0.25 × CY t+1 (nine months
  of the fiscal year fall in t, three in t+1).

## Variables and where they come from

| Variable | Definition | Source |
|---|---|---|
| Merchandise NTT, monthly | Export UVI / import UVI × 100, recomputed from the published indices | DGCI&S Terms of Trade files, base 2012-13 |
| Merchandise NTT, annual | Same, fiscal-year indices, three bases chain-linked | RBI Handbook of Statistics 2025-26, Table 121 |
| Goods-and-services ToT | Export deflator / import deflator (national accounts) | World Bank WDI |
| Oil price | Brent and Dubai; main series = average of Brent, Dubai and WTI | World Bank Pink Sheet (monthly since 1960) |
| Real oil price | Oil price / MUV index (price of manufactured exports), in 2010 prices | Pink Sheet and World Bank MUV |
| Indian crude basket | Weighted sour (Dubai/Oman) and sweet (Brent) grades India buys | PPAC (cross-check and the March 2026 hook) |
| Oil shares s_x, s_m | Oil exports / total exports; oil imports / total imports | RBI Table 111 (from FY1987) |
| Crude production and imports | Million tonnes | RBI Table 32 |
| Rupee per dollar | Annual average and end of March | RBI Table 133 |
| Non-energy commodity prices (control) | World Bank non-energy index / MUV | Pink Sheet |
| Gold price (robustness control) | US$ per troy ounce, real | Pink Sheet |
| REER | Real effective exchange rate | BIS broad index; RBI Table 135 |
| Structural oil shocks | Supply, economic activity, consumption demand, inventory demand | Baumeister & Hamilton (2019), updated series to Mar 2026 |
| Oil supply news shock | Surprise in oil futures around OPEC announcements | Känzig (2021, AER), updated to Dec 2025 |
| RCA, refined and crude | Balassa index, SITC 334 and 333 | UNCTADstat |
| Fuel trade by HS code | Values and tonnes, HS 2709 (crude) and 2710 (products) | UN Comtrade public API |
| Oil consumption by country | Thousand barrels a day | US EIA International Energy Data |

**About unit value indices.** The current DGCI&S indices (bases 2012-13 and 2022-23) are fixed-base Laspeyres
indices: the unit value (value / quantity) of each commodity, weighted by base-year trade shares. The older
1999-2000 series was a Fisher index (RBI Table 121, notes). They are not pure prices,
because a change in the quality or mix within a commodity code also changes the unit value. That is a known
limitation, and it applies to every study of India's terms of trade: the official long-run series published by
DGCI&S and the RBI are built from unit values.

## Why these choices (short answers)

- **Why the national-accounts ToT for the long run?** It is the only Indian ToT series that goes back to 1970
  on one consistent method, so it covers the 1973, 1979 and 1990 shocks. The merchandise series only links
  cleanly from FY1994.
- **Why deflate oil by MUV, not US CPI?** P_oil / MUV is the price of oil in terms of manufactures, which is the
  relative price on the axes of the offer-curve diagram. It is also the World Bank's standard deflator for
  commodity prices.
- **Why the average of Brent, Dubai and WTI, not the Indian basket?** The Indian basket is only published from
  2020 in usable form, and PPAC's site does not even have FY2022-23. The average is available from 1960, and
  the results are the same with Brent alone.
- **Why not a quantum or volume index?** DGCI&S's 2012-13-base export quantum index is erratic (monthly
  values between 54 and 2001), which also makes RBI's published gross and income ToT for 2025-26 meaningless.
- **Why monthly data only from 2019?** DGCI&S's online archive of the 2012-13 base starts in FY2019-20, and the
  1999-2000 base monthly page says "No Data Found". The long annual series carry the history.

## How the merchandise series is chain-linked

RBI publishes NTT on three bases: 1978-79, 1999-2000 and 2012-13. They overlap but do not agree. We use the
**newest base available for each year** and link the older bases at the overlap year with a ratio:

- 1999-2000 base for FY1999 to FY2011.
- 1978-79 base before FY1999, scaled so it equals the 1999 base in FY1999.
- 2012-13 base from FY2012 on, with the earlier segment scaled so the two meet in FY2012 (= 100).

This is the standard overlap-ratio method. It keeps the year-to-year growth rates of each base and only
rescales the levels.

## Problems we found in official data

This is a strong viva point: the data were checked, not just downloaded.

1. **RBI's base-year series contradict each other.** From FY1999-00 to 2007-08 the 1978-79-base NTT rises 21.7%,
   while the 1999-2000-base NTT falls 21.0%. The old base uses 1978-79 weights, from before India imported much
   oil or exported any refined fuel, so it misweights exactly the goods we study. We use the newest base for each
   period.
2. **Three published RBI NTT values disagree with RBI's own unit value indices** by more than rounding
   (FY2002-03, 2015-16, 2018-19). We recompute NTT from the indices, which is the textbook definition.
3. **The DGCI&S export quantum index is erratic** (see above). We never use quantum, gross or income ToT.
4. **WDI's 1960s deflators are a back-cast.** The export/import deflator ratio is frozen at one value through
   the 1960s, so the national-accounts ToT starts in FY1970.
5. **PPAC's website serves the wrong file for FY2022-23.** It is a provisional April 2023 table. We kept it,
   renamed it, and left that year of the Indian basket out.
6. **RBI Table 32 has a copy-paste error.** The rows for FY1990-91 to FY1997-98 are an exact copy of FY2000-01
   to FY2007-08 in all four columns. We set those eight years to missing. Our validation script now looks for
   any repeated block of four or more rows in every table.
7. **No monthly DGCI&S data before April 2019** are online. That limits the monthly sample to 87 months.
8. **DGCI&S's two current monthly series disagree month to month.** DGCI&S now publishes a 2022-23 base alongside
   the 2012-13 base. Over April 2023 to June 2026 the correlation of their monthly changes is about zero, and for
   February to June 2026 one shows the terms of trade 13% lower while the other shows it 8% higher. Single months
   are dominated by changes in the mix of goods, so we never judge an episode on one month: we use fiscal-year
   averages and regressions over many months. We use the 2012-13 base for the monthly models because the new base
   only starts in April 2023.

## Checks that pass

- NTT recomputed from the unit value indices equals the published DGCI&S NTT in every month, on both bases.
- DGCI&S fiscal-year indices equal RBI Table 121 for FY2019-20 to FY2025-26.
- World Bank Brent vs FRED/EIA Brent: correlation 0.9998, mean difference $0.33 a barrel over 441 months.
- The PPAC Indian basket lies between Dubai and Brent in 95% of normal months (it diverged in March 2026,
  when Gulf sour grades spiked).
- WDI and UNCTAD terms of trade are identical where both exist.
- RBI oil imports: Table 111 equals Table 115.
- Crude import tonnes: UN Comtrade and RBI Table 32 agree within ±9%.

## Quick facts from the data

| | Value |
|---|---|
| Oil share of India's imports, FY1987–2025 | mean 26%, range 15–37% |
| Oil share of India's exports, FY1987–2025 | mean 10%, range 0.1–22% (22% in FY2022) |
| Crude imports as share of crude refined, FY2025-26 | 90% (246 of 272 million tonnes) |
| Net oil imports, % of GDP | 5.6% at the FY2012 peak, 3.0% in FY2025 |
| Monthly merchandise NTT, Apr 2019–Jun 2026 | mean 111.9; high 163.2 (May 2020, oil crash); low 89.4 (Jun 2022) |
| Brent, Apr 2019–Jun 2026 | mean $74; low $23 (Apr 2020); high $120 (Apr 2026) |
| March 2026 | Brent $104, Indian basket $113, rupee 94.65 per dollar at end-March |

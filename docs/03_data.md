# Data

Related files:
- Policy: [`../data/SOURCE_POLICY.md`](../data/SOURCE_POLICY.md)
- Every file with URL and checksum: [`../data/SOURCES.md`](../data/SOURCES.md)
- Automatic checks: [`../data/validation_report.md`](../data/validation_report.md)
- Variable definitions: [`../data/variable_dictionary.csv`](../data/variable_dictionary.csv)
- Excel copy: [`../data/processed/final_dataset.xlsx`](../data/processed/final_dataset.xlsx)

## 1. Four datasets, each with a clear job

| Dataset | Period | Terms-of-trade measure | Used for |
|---|---|---|---|
| **Monthly** | Apr 2019 – Jun 2026 (87 months) | DGCI&S merchandise NTT = export UVI / import UVI (base 2012-13), recomputed from the published indices | Short-run dynamics, the 2020, 2022 and 2026 shocks, supply vs demand shocks (H3) |
| **Annual long run** | FY1970-71 – FY2025-26 | National-accounts terms of trade = export deflator / import deflator (goods & services, World Bank WDI) | Long-run elasticity (H1), asymmetry (H2); covers the 1973, 1979, 1990, 2008, 2022 shocks |
| **Annual merchandise** | FY1994-95 – FY2025-26 | DGCI&S/RBI merchandise NTT, chain-linked across the 1978-79, 1999-2000 and 2012-13 bases | Robustness for H1 and H2 |
| **Calendar-year theory data** | 1995/2000 – 2025 | UNCTAD/WDI merchandise NTT | RCA (L08), Grubel–Lloyd (L19), unit values (L20), India's share of world oil demand |

All annual Indian data are on the **fiscal year (April–March)**, labelled by the starting year (2024 = 2024-25). Monthly world prices are averaged over April–March in code.

**WDI's labelling was verified:** WDI's India "2024" equals RBI's FY2024-25 GDP to the rupee crore.

## 2. Main variables

- **Oil price:** Brent and Dubai (World Bank Pink Sheet, monthly since 1960).
  - Annual models use the **real** oil price = oil price / MUV index.
  - MUV is the price of manufactured exports, so P_oil/MUV is the relative price of oil in terms of manufactures. That is the axis of the offer-curve diagram (L22).
- **Indian crude basket:** PPAC, Apr 2020 onward. A cross-check only: PPAC's own site has no FY2022-23 file.
- **Oil shares of trade:** RBI Handbook Table 111 (oil and non-oil exports/imports, FY1987-88 onward). These give the theory benchmark elasticity s_x − s_m.
- **Identified shocks:**
  - Känzig (2021) oil supply news shocks (to Dec 2025)
  - Baumeister & Hamilton (2019) oil supply, economic activity and oil demand shocks (to Mar 2026)
- **Controls used in the models:**
  - World Bank non-energy commodity price index (deflated by MUV), in every annual model
  - Gold price (deflated by MUV), as a robustness check
- **Collected but kept out of the main models:** the BIS and RBI real effective exchange rates and world industrial
  production. The exchange rate reacts to oil shocks itself, so controlling for it would absorb part of the effect
  we are measuring, and world activity is already part of the Baumeister–Hamilton shocks used for H3.

## 3. Problems found in official data, and what we did

These are worth knowing for the viva: they show the data were checked, not just downloaded.

1. **RBI's three base-year merchandise ToT series contradict each other.**
   - Over FY1999-00 to 2007-08, the 1978-79-base series rises 21.7% while the 1999-2000-base series falls 21.0%.
   - The old base uses outdated 1978-79 weights (before India's large oil imports and refined exports), so we use the **newest base for each period** and link at the overlap years.
2. **Three RBI-published NTT values are inconsistent with RBI's own unit value indices** beyond rounding (FY2002-03, 2015-16, 2018-19). We **recompute NTT from the UVIs**, which is the textbook definition (L21).
3. **DGCI&S's export quantum index (base 2012-13) is erratic.**
   - Monthly values range from 54 to 2001, which produces RBI's implausible export QI = 473.6 and gross ToT = 38.2 for 2025-26.
   - We use **only unit value indices and NTT**, never QI, GTT or ITT.
4. **WDI's 1960s deflators are a back-cast artefact:** the export/import deflator ratio is constant at its 1999 value. The national-accounts ToT starts in FY1970-71.
5. **PPAC's website serves the wrong file for FY2022-23** (a provisional April 2023 table). Indian basket data for that year are missing; the file is kept, renamed, and not used.
6. **RBI Handbook Table 32 (crude production and imports) has a copy-paste error.**
   - The rows for FY1990-91 to FY1997-98 are an exact duplicate of FY2000-01 to FY2007-08 in all four columns. The validation script detects any repeated block of 4+ rows automatically.
   - Those eight years are set to missing. Volume data are used from FY1998-99 on, where they match UN Comtrade within ±9%.
7. **Monthly DGCI&S data before April 2019 are not published online.**
   - The 1999-2000-base monthly page says "No Data Found"; the 2012-13 archive starts in FY2019-20.
   - The monthly sample is therefore 87 months. The long annual series carry the history.

## 4. Cross-checks passed (see validation report)

- DGCI&S NTT recomputed from UVIs equals the published NTT (all 87 + 39 months).
- DGCI&S fiscal-year UVIs equal RBI Table 121 (FY2019-20 to 2025-26).
- World Bank Brent equals FRED/EIA Brent: correlation 0.9998, mean difference $0.33/bbl over 441 months.
- PPAC basket lies between Dubai and Brent in 95% of normal months (it diverges in March 2026, when Gulf sour grades spiked).
- WDI and UNCTAD terms of trade are identical.
- RBI oil imports: Table 111 = Table 115.
- Crude import tonnes: UN Comtrade vs RBI Table 32 within ±9%.

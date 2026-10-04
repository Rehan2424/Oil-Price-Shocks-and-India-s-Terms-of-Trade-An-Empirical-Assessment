# Number check

Every number we quote in the slides, the speaker notes and the viva notes, recomputed from the raw files.

`src/check_numbers.py` does this without using our own pipeline: it parses `data/raw/` again, rebuilds
the series, re-estimates every model with plain OLS and compares each result with the number as we write it
(so "−0.24" passes if the recomputed value rounds to −0.24). Run it again after any change.

**223 of 223 checks pass.**

Facts that come from outside our dataset (events, institutions, papers) are checked by hand at the end of
this page, with links to the original sources.


## Slide 1: March 2026

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Slide 1 | Brent, February 2026 (US$/bbl) | $71 | 71.10 | Pink Sheet, monthly |
| ✓ | Slide 1 | Brent, March 2026 (US$/bbl) | $104 | 103.70 | Pink Sheet, monthly |
| ✓ | Slide 1 | Brent rise, Feb to Mar 2026 | +46% | 45.85 | Pink Sheet |
| ✓ | Slide 1 | Indian crude basket, February 2026 | $69 | 69.01 | PPAC FY2025-26 file |
| ✓ | Slide 1 | Indian crude basket, March 2026 | $113 | 113.49 | PPAC FY2025-26 file |
| ✓ | Slide 1 | Rupee per US$, end-March 2026 | 94.65 | 94.6543 | RBI Table 133, end-year |
| ✓ | Slide 1 | End-March 2026 is the weakest year-end rupee rate in the table | weakest year-end rate on record | highest end-year value: 94.6543 in FY2025 (table starts FY1986) | RBI Table 133 |
| ✓ | Slide 1 | Merchandise ToT after the last shock, FY2020-21 to FY2022-23 | −24% | -23.70 | RBI Table 121, chain-linked |
| ✓ | Viva notes | 2026, base 2012-13: Apr-Jun vs Nov-Jan, three-month averages | +5.5% | 5.488 | DGCI&S |
| ✓ | Viva notes | 2026, base 2022-23: Apr-Jun vs Nov-Jan, three-month averages | +3.4% | 3.391 | DGCI&S |
| ✓ | Viva notes | Feb to Jun 2026, single months, base 2012-13 | −13% | -13.08 | DGCI&S |
| ✓ | Viva notes | Feb to Jun 2026, single months, base 2022-23 | +8% | 8.10 | DGCI&S |
| ✓ | Viva notes | The two DGCI&S bases barely agree month to month | correlation about zero | correlation of monthly changes -0.04, 38 months | DGCI&S, both bases |

## Slides 2-4: exposure, benchmark, RCA, Grubel-Lloyd

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Slide 2 | Crude imports as % of crude refined (imports / (imports + output)), FY2025-26 | 90% | 90.44 | RBI Table 32 (2025-26 provisional) |
| ✓ | Slide 2 | India's share of world oil consumption, 2024 | 5.4% | 5.430 | EIA International Energy Data |
| ✓ | Slide 2 | India is the 3rd-largest oil consumer | 3rd, after the US and China | top three: USA, CHN, IND | EIA |
| ✓ | Slide 3 | Offer-curve diagram, case A: ToT ray after the supply cut (h = 0.55) | 0.86 | 0.8612 | Model in src/slide_figures.py (elasticities 1.5) |
| ✓ | Slide 3 | Offer-curve diagram, case C: ToT ray after India's demand grows (k = 1.8) | 0.86 | 0.8633 | Model in src/slide_figures.py |
| ✓ | Slide 3 | Merchandise ToT, FY2020-21 to FY2022-23 | −24% | -23.70 | RBI Table 121 |
| ✓ | Viva notes | Same, one decimal | −23.7% | -23.704 | RBI Table 121 |
| ✓ | Notes | Brent, Feb to Jun 2022 | +25% | 25.37 | Pink Sheet |
| ✓ | Slide 4 | Benchmark s_x − s_m, FY1999-00 | −0.25 | -0.2528 | RBI Table 111 |
| ✓ | Slide 4 | Benchmark s_x − s_m, FY2025-26 | −0.10 | -0.1026 | RBI Table 111 |
| ✓ | Viva notes | Oil share of exports, FY1990-91 | 3% | 2.88 | RBI Table 111 |
| ✓ | Slide 4 notes | Lowest oil share of exports since FY2008 | 9% | 8.8% (FY2020) | RBI Table 111 |
| ✓ | Viva notes / notes | Highest oil share of exports since FY2008 | 22% | 21.6% (FY2022) | RBI Table 111 |
| ✓ | Viva notes | Oil share of imports, FY1987-2025: mean | 26% | 26.02 | RBI Table 111 |
| ✓ | Viva notes | Oil share of imports: lowest | 15% | 15.10 | RBI Table 111 |
| ✓ | Viva notes | Oil share of imports: highest | 37% | 36.60 | RBI Table 111 |
| ✓ | Viva notes | Oil share of exports, FY1987-2025: mean | 10% | 9.57 | RBI Table 111 |
| ✓ | Viva notes | Oil share of exports: lowest | 0.1% | 0.106 | RBI Table 111 |
| ✓ | Slide 4 | RCA, refined petroleum (SITC 334), 1999 | 0.06 | 0.0570 | UNCTADstat |
| ✓ | Notes | RCA, refined petroleum, 2000 | 1.26 | 1.2644 | UNCTADstat |
| ✓ | Slide 4 | RCA, refined petroleum, 2025 | 4.37 | 4.3680 | UNCTADstat |
| ✓ | Viva notes | RCA in crude (SITC 333) is about zero | about 0 | max 0.0084 over 1995-2025 | UNCTADstat |
| ✓ | Slide 4 | Grubel-Lloyd, oil as one industry, 2025 | 0.55 | 0.5452 | UN Comtrade, HS 2709 + 2710 |
| ✓ | Slide 4 | Grubel-Lloyd, crude and products separately, 2025 | 0.10 | 0.0957 | UN Comtrade |
| ✓ | Backup: refining hedge | Refined-export / crude-import unit value, 2005 | 1.28 | 1.2810 | UN Comtrade |
| ✓ | Backup: refining hedge | Refined-export / crude-import unit value, 2015 | 1.41 | 1.4108 | UN Comtrade |
| ✓ | Backup: refining hedge | Refined-export / crude-import unit value, 2022 | 1.40 | 1.3970 | UN Comtrade |
| ✓ | Backup: refining hedge | Refined-export / crude-import unit value, 2024 | 1.23 | 1.2320 | UN Comtrade |
| ✓ | Backup: refining hedge | Refined-export / crude-import unit value, 2025 | 1.27 | 1.2743 | UN Comtrade |
| ✓ | Backup: refining hedge | Unit value ratio, lowest year 2000-2025 | 1.13 | 1.128 (2012) | UN Comtrade |
| ✓ | Backup: refining hedge | Unit value ratio, highest year 2000-2025 | 1.41 | 1.411 (2015) | UN Comtrade |
| ✓ | Backup: refining hedge | Inside the ±15% band only in 2011 and 2012 | every year except 2011 and 2012 | years at or below 1.15: [2011, 2012]; 23 years with data | UN Comtrade |
| ✓ | Notebook 02 | GL as one industry since 2010: lowest | 0.5 | 0.511 | UN Comtrade |
| ✓ | Notebook 02 | GL as one industry since 2010: highest | 0.7 | 0.717 | UN Comtrade |
| ✓ | Notebook 02 | GL separately since 2010: lowest | 0.04 | 0.0403 | UN Comtrade |
| ✓ | Notebook 02 | GL separately since 2010: highest | 0.12 | 0.1217 | UN Comtrade |

## Slide 6: data and the problems we found

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Slide 6 | 1978-79 base NTT, FY1999-00 to FY2007-08 | +21.7% | 21.667 | RBI Table 121 |
| ✓ | Slide 6 | 1999-2000 base NTT, same years | −21.0% | -20.952 | RBI Table 121 |
| ✓ | Slide 6 | Table 32 rows FY1990-97 repeat FY2000-07 | exact copy | all 8 rows x 4 columns identical | RBI Table 32 |
| ✓ | Slide 6 | DGCI&S export quantum index (base 2012-13), monthly minimum | 54 | 53.74 | DGCI&S |
| ✓ | Slide 6 | DGCI&S export quantum index, monthly maximum | 2001 | 2001.27 | DGCI&S |
| ✓ | Slide 6 | Published RBI NTT values that disagree with RBI's own indices beyond rounding | three | FY2002 (1978 base); FY2015 (1999 base); FY2018 (1999 base) | RBI Table 121 |
| ✓ | Slide 6 | Monthly sample length (months with DGCI&S base 2012-13 data) | 87 | 87 months, Apr 2019 to Jun 2026 | DGCI&S |

## Slides 7-8 and backup: H1 (ARDL)

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Slide 8 | Lag order chosen by AIC (max 2) | ARDL(1,1,1) | (1, {'real_avg': 1, 'real_nonenergy': 1}) | re-estimated |
| ✓ | Slide 8 | Observations | 54 | 54.00 | FY1970-71 to FY2024-25 |
| ✓ | Slide 8 | Short-run oil elasticity | −0.24 | -0.2411 | OLS on raw-built series |
| ✓ | Backup: ARDL | Short-run oil elasticity (3 decimals) | −0.241 | -0.24108 | re-estimated |
| ✓ | Backup: ARDL | Its standard error | 0.049 | 0.04889 | re-estimated |
| ✓ | Backup: ARDL | Its HC1 robust standard error | 0.040 | 0.04012 | re-estimated |
| ✓ | Slide 8 | p < 0.001 with robust s.e. | p < 0.001 | p = 1.87e-09 | re-estimated |
| ✓ | Slide 8 | Error-correction coefficient α | −0.31 | -0.3079 | re-estimated |
| ✓ | Backup: ARDL | α (3 decimals) and its s.e. | −0.308 | -0.30789 | re-estimated |
| ✓ | Backup: ARDL | s.e. of α | 0.086 | 0.08555 | re-estimated |
| ✓ | Viva notes | t-statistic of α | −3.60 | -3.5989 | re-estimated |
| ✓ | Slide 8 | Long-run oil elasticity | −0.09 | -0.0918 | re-estimated |
| ✓ | Backup: ARDL | Long-run elasticity and delta-method s.e. | 0.059 | 0.05888 | re-estimated |
| ✓ | Backup: ARDL | p-value of the long-run elasticity (normal approximation) | 0.119 | 0.11880 | re-estimated |
| ✓ | Backup: ARDL | Long-run non-energy commodity elasticity | −0.249 | -0.24866 | re-estimated |
| ✓ | Slide 8 | Bounds F-statistic | 4.74 | 4.7432 | re-estimated |
| ✓ | Slide 8 | Bounds p-value against the I(1) bound (simulated, seed 2026) | 0.07 | 0.0697 | statsmodels |
| ✓ | Backup: ARDL | Bounds p-value against the I(0) bound | 0.025 | 0.02494 | statsmodels |
| ✓ | Viva notes | 10% upper bound | 4.32 | 4.3164 | statsmodels finite-sample |
| ✓ | Viva notes | 5% lower bound | 4.02 | 4.0231 | statsmodels finite-sample |
| ✓ | Viva notes | 5% upper bound | 5.13 | 5.1343 | statsmodels finite-sample |
| ✓ | Backup: ARDL | Breusch-Godfrey (2 lags) p | 0.90 | 0.9014 | re-estimated |
| ✓ | Backup: ARDL | Breusch-Pagan p | 0.019 | 0.01878 | re-estimated |
| ✓ | Backup: ARDL | Jarque-Bera p | 0.25 | 0.2546 | re-estimated |
| ✓ | Backup: ARDL | Ramsey RESET p | 0.84 | 0.8434 | re-estimated |
| ✓ | Viva notes | R-squared | 0.51 | 0.5059 | re-estimated |
| ✓ | Viva notes | Adjusted R-squared | 0.45 | 0.4545 | re-estimated |
| ✓ | Viva notes | Half-life of a deviation (years) | 1.9 | 1.884 | derived |
| ✓ | Backup: robustness | Oil only: short-run elasticity | −0.195 | -0.19470 | re-estimated |
| ✓ | Backup: robustness | Oil + non-oil + gold: short-run elasticity | −0.217 | -0.21694 | re-estimated |
| ✓ | Backup: robustness | Brent instead of average crude: short-run elasticity | −0.236 | -0.23632 | re-estimated |
| ✓ | Backup: robustness | Post-1980 sample: short-run elasticity | −0.211 | -0.21099 | re-estimated |
| ✓ | Backup: robustness | Merchandise ToT, FY1994-2024: short-run elasticity | −0.277 | -0.27685 | re-estimated |
| ✓ | Slide 8 | Short-run range across the six specifications: smallest (corrected from −0.20) | −0.19 | -0.1947 | re-estimated |
| ✓ | Slide 8 | Short-run range across the six specifications: largest | −0.28 | -0.2768 | re-estimated |
| ✓ | Slide 8 | Significant in every specification | all six | t from -4.97 to -3.46 | re-estimated |
| ✓ | Viva notes | ToT (goods and services), FY1970-71 | 110 | 110.02 | WDI |
| ✓ | Viva notes | ToT (goods and services), FY2025-26 | 98 | 97.75 | WDI |
| ✓ | Viva notes | p-value of a linear trend in ln ToT | 0.12 | 0.1213 | WDI |
| ✓ | Viva notes | Correlation of annual oil and non-energy price changes | 0.47 | 0.4677 | Pink Sheet |

## Slide 9: timing (local projections) and the benchmark test

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Slide 9 | Response at 2 months | −0.39 | -0.3860 | re-estimated |
| ✓ | Viva notes | Response at 0 months | −0.02 | -0.0153 | re-estimated |
| ✓ | Viva notes | Response at 1 month | −0.23 | -0.2255 | re-estimated |
| ✓ | Viva notes | Response at 3 months | −0.37 | -0.3688 | re-estimated |
| ✓ | Viva notes | Response at 6 months | −0.37 | -0.3693 | re-estimated |
| ✓ | Viva notes | s.e. at 2 months | 0.13 | 0.1275 | re-estimated |
| ✓ | Viva notes | s.e. at 3 months | 0.08 | 0.0817 | re-estimated |
| ✓ | Viva notes | Significant (90%) at every horizon from 1 to 6 months | 1 to 6 months | t: -2.2, -3.0, -4.5, -2.9, -4.6, -5.3 | re-estimated |
| ✓ | Viva notes | Observations at horizon 0 | 85 | 85.00 | re-estimated |
| ✓ | Slide 9 | Benchmark-test coefficient (theory: 1) | 1.70 | 1.6958 | re-estimated |
| ✓ | Viva notes | Its HAC s.e. | 0.38 | 0.3838 | re-estimated |
| ✓ | Slide 9 | p-value for coefficient = 1 | 0.07 | 0.0699 | re-estimated |
| ✓ | Viva notes | Observations | 30 | 30.00 | FY1995-96 to FY2024-25 |
| ✓ | Viva notes | Plain merchandise oil elasticity, same years | −0.30 | -0.3024 | re-estimated |
| ✓ | Viva notes | Average benchmark over the same years | −0.16 | -0.1593 | RBI Table 111 |
| ✓ | Slide 9 | Export unit values, Feb to Apr 2026 | +18% | 18.09 | DGCI&S |
| ✓ | Viva notes | Export unit values, Feb to Apr 2026 (one decimal) | +18.1% | 18.086 | DGCI&S |
| ✓ | Slide 9 | Import unit values, Feb to Apr 2026 | +16% | 15.74 | DGCI&S |
| ✓ | Viva notes | Import unit values, Feb to Apr 2026 (one decimal) | +15.7% | 15.741 | DGCI&S |
| ✓ | Viva notes | Import unit values, Feb to Jun 2026 | +20% | 20.39 | DGCI&S |

## Slide 10 and backup: H2 (NARDL) and the rolling elasticity

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Slide 10 | Short-run effect of a rise | −0.27 | -0.2708 | re-estimated |
| ✓ | Slide 10 | Short-run effect of a fall | −0.22 | -0.2150 | re-estimated |
| ✓ | Viva notes | Short-run symmetry p (baseline) | 0.62 | 0.6200 | re-estimated |
| ✓ | Viva notes | Long-run effect of a rise (baseline) | −0.16 | -0.1616 | re-estimated |
| ✓ | Viva notes | Long-run effect of a fall (baseline) | −0.23 | -0.2277 | re-estimated |
| ✓ | Viva notes | Long-run symmetry p (baseline) | 0.035 | 0.03538 | re-estimated |
| ✓ | Slide 10 | Short-run symmetry p, smallest of seven specifications | 0.54 | 0.5367 | re-estimated |
| ✓ | Slide 10 | Short-run symmetry p, largest | 0.91 | 0.9132 | re-estimated |
| ✓ | Slide 10 | Long-run symmetry p from FY1980 | 0.28 | 0.2754 | re-estimated |
| ✓ | Viva notes | Long-run symmetry p with an extra lag | 0.05 | 0.0513 | re-estimated |
| ✓ | Viva notes | Long-run symmetry p from FY1975 | 0.08 | 0.0766 | re-estimated |
| ✓ | Viva notes | Merchandise: long-run asymmetry reversed, not significant | reversed | rise -0.187, fall -0.075, p = 0.13 | re-estimated |
| ✓ | Slide 10 | Rolling elasticity, window ending FY1989 | −0.30 | -0.2992 | re-estimated |
| ✓ | Slide 10 | Rolling elasticity, window ending FY2024 | −0.11 | -0.1106 | re-estimated |
| ✓ | Viva notes | Its s.e., first window | 0.09 | 0.0927 | re-estimated |
| ✓ | Viva notes | Its s.e., last window | 0.06 | 0.0617 | re-estimated |
| ✓ | Viva notes | Rolling elasticity, window ending FY2015 | −0.16 | -0.1618 | re-estimated |
| ✓ | Notebook 05 | Most recent windows (ending FY2019-24): smallest effect | −0.10 | -0.0985 | re-estimated |
| ✓ | Notebook 05 | Most recent windows: largest effect | −0.15 | -0.1498 | re-estimated |

## Slide 11 and backup: H3 (supply- vs demand-driven oil prices)

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Viva notes | First step: R-squared | 0.80 | 0.7992 | re-estimated |
| ✓ | Viva notes | First step: months | 612 | 612.00 | Feb 1975 to Mar 2026, less two lags |
| ✓ | Backup: H3 | Annual G&S: supply-driven effect | −0.068 | -0.06845 | re-estimated |
| ✓ | Backup: H3 | Annual G&S: demand-driven effect | −0.106 | -0.10645 | re-estimated |
| ✓ | Backup: H3 | Annual G&S: p (equal) | 0.707 | 0.70738 | re-estimated |
| ✓ | Backup: H3 | Annual merchandise: supply-driven | −0.027 | -0.02654 | re-estimated |
| ✓ | Backup: H3 | Annual merchandise: demand-driven | −0.130 | -0.13040 | re-estimated |
| ✓ | Backup: H3 | Annual merchandise: p (equal) | 0.547 | 0.54729 | re-estimated |
| ✓ | Backup: H3 | Monthly, 3-month cumulative: supply-driven | −0.242 | -0.24242 | re-estimated |
| ✓ | Backup: H3 | Monthly, 3-month cumulative: demand-driven | −0.373 | -0.37293 | re-estimated |
| ✓ | Backup: H3 | Monthly: p (equal) | 0.535 | 0.53485 | re-estimated |
| ✓ | Slide 11 | p (supply = demand), smallest of three samples (corrected from 0.54) | 0.53 | 0.5348 | re-estimated |
| ✓ | Slide 11 | p (supply = demand), largest | 0.71 | 0.7074 | re-estimated |
| ✓ | Slide 11 | Oil price response to one Känzig news shock, same month (%) | +10% | 9.80 | Känzig series, Pink Sheet |
| ✓ | Backup: H3 | Annual ToT response per Känzig shock (%) | −0.95 | -0.9521 | re-estimated |
| ✓ | Backup: H3 | Its s.e. | 0.49 | 0.4890 | re-estimated |
| ✓ | Backup: H3 | Monthly ToT response to a Känzig shock, 2 months (%) | −4.2 | -4.155 | re-estimated |
| ✓ | Backup: H3 | Monthly ToT response to a Känzig shock, 3 months (%) | −4.7 | -4.668 | re-estimated |
| ✓ | Notebook 06 | Its t-statistic at 2 months | −2.0 | -1.958 | re-estimated |
| ✓ | Notebook 06 | Its t-statistic at 3 months | −2.7 | -2.728 | re-estimated |
| ✓ | Notebook 06 | March 2026 oil price change (100 x log) | 34 | 34.07 | Pink Sheet |
| ✓ | Notebook 06 | March 2026: supply-driven part | 36 | 36.44 | re-estimated |
| ✓ | Notebook 06 | Feb 2022 rise mainly demand-driven; March 2022 has a supply part | mainly demand | Feb: demand 11.8, supply -0.2; Mar: demand 9.0, supply 4.5 | re-estimated |

## Backup: oil episodes (fiscal-year averages)

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Backup: episodes | 1973 OPEC embargo: real oil price | +284.1% | 284.059 | Pink Sheet / MUV |
| ✓ | Backup: episodes | 1973 OPEC embargo: ToT goods and services | −38.6% | -38.648 | WDI |
| ✓ | Backup: episodes | 1979 Iranian revolution: real oil price | +110.2% | 110.228 | Pink Sheet / MUV |
| ✓ | Backup: episodes | 1979 Iranian revolution: ToT goods and services | −19.2% | -19.182 | WDI |
| ✓ | Backup: episodes | 1990 Gulf war: real oil price | +21.1% | 21.088 | Pink Sheet / MUV |
| ✓ | Backup: episodes | 1990 Gulf war: ToT goods and services | −9.8% | -9.801 | WDI |
| ✓ | Backup: episodes | 2008 price spike: real oil price | +19.9% | 19.852 | Pink Sheet / MUV |
| ✓ | Backup: episodes | 2008 price spike: ToT goods and services | +4.9% | 4.892 | WDI |
| ✓ | Backup: episodes | 2008 price spike: ToT merchandise | +5.8% | 5.831 | RBI Table 121 |
| ✓ | Backup: episodes | 2014-16 collapse: real oil price | −49.9% | -49.896 | Pink Sheet / MUV |
| ✓ | Backup: episodes | 2014-16 collapse: ToT goods and services | −1.0% | -0.983 | WDI |
| ✓ | Backup: episodes | 2014-16 collapse: ToT merchandise | +19.4% | 19.438 | RBI Table 121 |
| ✓ | Backup: episodes | 2020 COVID crash: real oil price | −26.4% | -26.408 | Pink Sheet / MUV |
| ✓ | Backup: episodes | 2020 COVID crash: ToT goods and services | +4.7% | 4.673 | WDI |
| ✓ | Backup: episodes | 2020 COVID crash: ToT merchandise | +9.6% | 9.649 | RBI Table 121 |
| ✓ | Backup: episodes | 2022 Russia-Ukraine: real oil price | +82.8% | 82.804 | Pink Sheet / MUV |
| ✓ | Backup: episodes | 2022 Russia-Ukraine: ToT goods and services | −14.4% | -14.355 | WDI |
| ✓ | Backup: episodes | 2022 Russia-Ukraine: ToT merchandise | −23.7% | -23.704 | RBI Table 121 |
| ✓ | Viva notes | 2008: oil peaked in July and collapsed by December | July peak, December low | peak 133.9 (Jul), December 41.6 | Pink Sheet |

## Backup: unit-root tests (p-values)

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Backup: unit roots | ln ToT goods & services: ADF level p | 0.057 | 0.05709 | re-tested |
| ✓ | Backup: unit roots | ln ToT goods & services: Phillips-Perron level p | 0.050 | 0.04966 | re-tested |
| ✓ | Backup: unit roots | ln ToT goods & services: KPSS level p | 0.100 | 0.10000 | re-tested |
| ✓ | Backup: unit roots | ln ToT goods & services: Zivot-Andrews p | 0.391 | 0.39117 | re-tested |
| ✓ | Backup: unit roots | ln ToT goods & services: stationary in first differences (ADF) | p ≈ 0.000 | p = 0.0000 | re-tested |
| ✓ | Backup: unit roots | ln ToT merchandise: ADF level p | 0.271 | 0.27138 | re-tested |
| ✓ | Backup: unit roots | ln ToT merchandise: Phillips-Perron level p | 0.392 | 0.39241 | re-tested |
| ✓ | Backup: unit roots | ln ToT merchandise: KPSS level p | 0.010 | 0.01000 | re-tested |
| ✓ | Backup: unit roots | ln ToT merchandise: Zivot-Andrews p | 0.062 | 0.06182 | re-tested |
| ✓ | Backup: unit roots | ln ToT merchandise: stationary in first differences (ADF) | p ≈ 0.000 | p = 0.0007 | re-tested |
| ✓ | Backup: unit roots | ln real oil price: ADF level p | 0.053 | 0.05282 | re-tested |
| ✓ | Backup: unit roots | ln real oil price: Phillips-Perron level p | 0.050 | 0.05019 | re-tested |
| ✓ | Backup: unit roots | ln real oil price: KPSS level p | 0.013 | 0.01262 | re-tested |
| ✓ | Backup: unit roots | ln real oil price: Zivot-Andrews p | 0.533 | 0.53262 | re-tested |
| ✓ | Backup: unit roots | ln real oil price: stationary in first differences (ADF) | p ≈ 0.000 | p = 0.0000 | re-tested |
| ✓ | Backup: unit roots | ln real non-energy prices: ADF level p | 0.355 | 0.35539 | re-tested |
| ✓ | Backup: unit roots | ln real non-energy prices: Phillips-Perron level p | 0.395 | 0.39545 | re-tested |
| ✓ | Backup: unit roots | ln real non-energy prices: KPSS level p | 0.100 | 0.10000 | re-tested |
| ✓ | Backup: unit roots | ln real non-energy prices: Zivot-Andrews p | 0.911 | 0.91094 | re-tested |
| ✓ | Backup: unit roots | ln real non-energy prices: stationary in first differences (ADF) | p ≈ 0.000 | p = 0.0000 | re-tested |
| ✓ | Backup: unit roots | ln real gold price: ADF level p | 0.945 | 0.94524 | re-tested |
| ✓ | Backup: unit roots | ln real gold price: Phillips-Perron level p | 0.582 | 0.58165 | re-tested |
| ✓ | Backup: unit roots | ln real gold price: KPSS level p | 0.010 | 0.01000 | re-tested |
| ✓ | Backup: unit roots | ln real gold price: Zivot-Andrews p | 0.942 | 0.94154 | re-tested |
| ✓ | Backup: unit roots | ln real gold price: stationary in first differences (ADF) | p ≈ 0.000 | p = 0.0002 | re-tested |

## Other numbers in the speaker notes and viva notes

| | Where | What | We say | Recomputed | Source |
|---|---|---|---|---|---|
| ✓ | Viva notes | Crude import volume elasticity to the oil price | 0.16 | 0.1576 | RBI Tables 32, 111 |
| ✓ | Viva notes | Its s.e. | 0.09 | 0.0939 | re-estimated |
| ✓ | Viva notes | Correlation of oil import bill and oil price changes | 0.96 | 0.9577 | RBI Table 111, Pink Sheet |
| ✓ | Viva notes | Net oil imports, % of GDP, FY2025-26 | 3.0% | 3.036 | RBI Table 111, WDI |
| ✓ | Viva notes | Net oil imports, % of GDP, peak | 5.6% | 5.65% (FY2012) | RBI Table 111, WDI |
| ✓ | Viva notes | The peak year is FY2012-13 | FY2012 | FY2012 | RBI Table 111, WDI |
| ✓ | Viva notes | Monthly merchandise NTT: mean | 111.9 | 111.880 | DGCI&S |
| ✓ | Viva notes | Monthly merchandise NTT: high (May 2020) | 163.2 | 163.229 (May 2020) | DGCI&S |
| ✓ | Viva notes | Monthly merchandise NTT: low (Jun 2022) | 89.4 | 89.450 (Jun 2022) | DGCI&S |
| ✓ | Viva notes | Brent Apr 2019-Jun 2026: mean | $74 | 74.40 | Pink Sheet |
| ✓ | Viva notes | Brent: low (Apr 2020) | $23 | 23.3 (Apr 2020) | Pink Sheet |
| ✓ | Viva notes | Brent: high (Apr 2026) | $120 | 120.4 (Apr 2026) | Pink Sheet |
| ✓ | Viva notes | World Bank vs FRED Brent: correlation (logs) | 0.9998 | 0.999769 | Pink Sheet, FRED |
| ✓ | Viva notes | Mean absolute difference (US$/bbl) | 0.33 | 0.3271 | Pink Sheet, FRED |
| ✓ | Viva notes | Months compared | 441 | 441.00 | Pink Sheet, FRED |
| ✓ | Viva notes | PPAC basket within the Dubai-Brent range (±$1.5), Apr 2020-Feb 2026 | 95% | 94.92 | PPAC, Pink Sheet |
| ✓ | Viva notes | Comtrade (calendar year) vs RBI (fiscal year) crude import tonnes | within ±9% | ratio 0.907 to 1.089 over 26 years | UN Comtrade, RBI Table 32 |
| ✓ | Q&A G12 | Oil share of imports, FY2025-26 | 22% | 22.44 | RBI Table 111 |
| ✓ | Q&A D4 | Services share of India's exports, 1990 | 20% | 20.19 | WDI (BoP) |
| ✓ | Q&A D4 | Services share of India's exports, 2024 ("almost half") | 46% | 45.60 | WDI (BoP) |
| ✓ | Speaker notes | Oil is the largest single item in India's import bill | largest item | FY2025-26: Petroleum, Crude & products US$173.9 bn; next Electronic goods 116.2, Gold 72.0 | RBI Table 115 |

## Our raw files match the publishers' current files

On 4 October 2026 we downloaded the main sources again and compared them with the copies in `data/raw/`.

| Source | What was compared | Result |
|---|---|---|
| RBI Handbook 2025-26, Tables 32, 111, 115, 121, 133 (live pages, links in `data/SOURCES.md`) | 1,416 published numbers | identical |
| World Bank Pink Sheet, monthly (Brent, Dubai, average crude, gold) | 801 months × 4 series | identical |
| World Bank WDI: export and import values at current and constant prices, GDP in US$ | 66 years × 5 series | identical |
| FRED Brent (cross-check series) | 9,097 days | identical |
| Känzig (2021) oil supply news shocks, author's GitHub | 612 months | identical |

## Facts from outside our dataset

Checked against the original source or a report of it.

| Claim (where we use it) | What the source says | Source |
|---|---|---|
| The IEA called the 2026 Hormuz disruption the largest oil supply disruption on record (slide 1 notes, Q&A A9) | IEA Oil Market Report, March 2026: "the biggest oil supply disruption in history"; flows through Hormuz fell from about 20 mb/d to a trickle; strikes on Iran began on 28 February | [BNN Bloomberg, 12 Mar 2026](https://www.bnnbloomberg.ca/business/2026/03/12/world-faces-largest-ever-oil-supply-disruption-on-middle-east-war-iea-says/); [Business Today, 12 Mar 2026](https://www.businesstoday.in/amp/world/story/from-20-mn-barrels-a-day-to-a-trickle-iea-says-hormuz-closure-is-biggest-oil-supply-disruption-ever-520370-2026-03-12) |
| Jamnagar is the world's largest refining complex; first refinery 1999, export refinery 2008 (viva notes 01, Q&A B11) | Commissioned 1999; SEZ export refinery added 2008; 1.24 million barrels a day | [NS Energy](https://www.nsenergybusiness.com/projects/reliance-industries-jamnagar-refinery-india) |
| Strategic reserves of about 5.3 million tonnes at Visakhapatnam, Mangaluru and Padur, roughly 9–10 days (Q&A G3) | 1.33 + 1.50 + 2.50 = 5.33 million tonnes; about 9.5 days at full capacity | [Business Today, 24 Mar 2026](https://www.businesstoday.in/latest/economy/story/exclusive-indias-strategic-oil-reserves-cover-just-less-than-10-days-522058-2026-03-24); [Lok Sabha answer](https://eparlib.nic.in/bitstream/123456789/2974287/1/AU1056.pdf) |
| Excise duties raised in 2020, cut in November 2021 and May 2022 (Q&A G2) | Raised by ₹13 (petrol) and ₹16 (diesel) in March–May 2020; cut ₹5/₹10 on 4 Nov 2021 and ₹8/₹6 in May 2022 | [Autocar Pro](https://autocarpro.in/news-national/government-slashes-excise-duty-on-petrol-by-rs-5--diesel-by-rs-10-80387); [Outlook Business](https://www.outlookbusiness.com/amp/story/news/excise-duty-cut-petrol-price-slashed-by-rs-8-69-ltr-diesel-by-rs-7-05-ltr-news-197902) |
| Special duties on fuel exports and domestic crude from July 2022 (Q&A G6) | Imposed 1 July 2022 on domestic crude and on exports of petrol, diesel and ATF | [Drishti IAS, 22 Jul 2022](https://www.drishtiias.com/daily-updates/daily-news-analysis/windfall-tax/print_manually) |
| India shifted a large share of its crude purchases to Russia after 2022 (Q&A B17) | About 35% of India's crude imports in 2023 and FY2023-24, up from about 2% before the war | [S&P Global](https://spglobal.com/commodityinsights/en/market-insights/latest-news/oil/010824-red-sea-woes-unlikely-to-dent-russias-position-as-indias-top-crude-supplier); [Business Standard](https://www.business-standard.com/amp/economy/news/import-of-russian-crude-up-25-at-14-7-billion-in-q1-shows-data-124082500392_1.html) |
| Schmitt-Grohé and Uribe find terms-of-trade shocks explain under 10% of output movements, in 38 countries (literature slide, Q&A C9) | Country-specific SVARs for 38 countries; terms-of-trade shocks explain less than 10% of movements in aggregate activity | [RePEc](https://ideas.repec.org/a/wly/iecrev/v59y2018i1p85-111.html); [NBER WP 21253](https://www.nber.org/system/files/working_papers/w21253/w21253.pdf) |
| Backus and Crucini: oil explains much of the variation in the terms of trade (literature slide) | "Oil accounts for much of the variation in the terms of trade over the last twenty-five years" | [RePEc](https://ideas.repec.org/a/eee/inecon/v50y2000i1p185-213.html) |
| Deheri and Sahu: only oil-specific demand shocks significantly affect India's trade balances (literature slide, Q&A C8) | "Among oil market shocks, only oil-specific demand shocks have a significant impact on India's merchandise trade balances" | [Energy Research Letters](https://erl.scholasticahq.com/article/77528.pdf) |
| Lecture quotes (L17 "the more broadly an industry is defined…", L21 definition of the net barter terms of trade, L20 ±15% rule, L16 MR = p(1 − 1/e), L13 time horizons, L05 "fuels") | Found word for word in the lecture PDFs | `course-material/lectures/` |

## Corrections made after this check

Running the check found these mistakes in our own text, all now fixed in the slides, notes and docs:

1. **2026 terms of trade.** We had said India's merchandise terms of trade fell 13% from February to June 2026. That
   is true of those two months on DGCI&S's 2012-13 base, but February was an unusually high month, the new 2022-23
   base shows +8% for the same months, and in three-month averages neither base shows a fall. The slides now use
   the robust number from the last shock (−24%, FY2020-21 to FY2022-23) and say that 2026 shows no clear fall yet.
2. **Short-run range across the six ARDL specifications:** −0.19 to −0.28 (we had written −0.20).
3. **Jarque–Bera p-value:** 0.25 (we had written 0.26 by rounding 0.255 twice).
4. **H3, smallest p-value:** 0.53 (we had written 0.54).
5. **Refined/crude unit-value ratio:** 1.13–1.41 over 2000–2025, outside the ±15% band in every year except 2011 and
   2012 (we had quoted 1.2–1.4 from the five years in our table).
6. **Oil share of exports since FY2008:** 9–22% (we had written 12–22%; FY2020-21 was 8.8%).
7. **Services share of India's exports:** almost half today (46% in 2024), not "about a third".
8. **Monthly response after one to three months:** about 0.2–0.4% per 1% oil rise (we had written 0.3–0.45%).
9. **Rupee:** 94.65 is the weakest *year-end* rate on record (the table holds year-end rates, not daily lows).
10. **DGCI&S index formula:** the 1999-2000 series was a Fisher index; only the 2012-13 and 2022-23 bases are
    Laspeyres.
11. **Lecture 5:** it lists fuels among goods where India has a comparative advantage in the world market; we had
    paraphrased it as an advantage "over China".


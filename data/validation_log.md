# Human Validation Log

The automatic checks are in [`validation_report.md`](validation_report.md). This page is the **human check**: one teammate opens each original publication and confirms that the value in our dataset matches it exactly.

**How to do it:**
1. Open the source link.
2. Find the cell described in the "Where to look" column.
3. Write ✅ or ❌, your name and the date.

If anything is ❌, tell the group before using the data.

| # | Our value | Variable (file) | Where to look in the original source | OK? | Checked by / date |
|---|---|---|---|---|---|
| 1 | 159.6 | `uvi_x_rbi_2012`, FY2022-23 (annual_fy) | RBI Handbook 2025-26, **Table 121** "Index Numbers and Terms of Foreign Trade", base 2012-13, row 2022-23, column "Unit Value Index – Exports" | | |
| 2 | 6028.1 | `m_oil_usdm`, FY1990-91 (annual_fy) | RBI Handbook 2025-26, **Table 111** "India's Foreign Trade – US Dollar", row 1990-91, column "Imports – Oil" (US$ million) | | |
| 3 | 53828.1 | `x_oil_usdm`, FY2025-26 (annual_fy) | RBI Handbook 2025-26, **Table 111**, row 2025-26, "Exports – Oil" | | |
| 4 | 89.45 | `ntt_b12`, June 2022 (monthly) | DGCI&S, Terms of Trade archive (base 2012-13), file **Terms_of_Trade_FY_22_23.xlsx**, "Net terms of trade", column Jun-2022 (shows 89.45…) | | |
| 5 | 181.73 | `uvi_x_b12`, March 2026 (monthly) | DGCI&S file **TermsofTradeFY202526.xlsx**, "Export Grand Total Index", UVI column for Mar-2026 | | |
| 6 | 103.7 | `brent`, March 2026 (monthly) | World Bank Pink Sheet, **CMO-Historical-Data-Monthly.xlsx**, sheet "Monthly Prices", row 2026M03, column "Crude oil, Brent" | | |
| 7 | 115.7 | `dubai`, June 2022 (monthly) | Same file, row 2022M06, column "Crude oil, Dubai" | | |
| 8 | 113.49 | `icb_ppac`, March 2026 (monthly) | PPAC website → Prices → International Prices of Crude Oil, FY 2025-26, March | | |
| 9 | 90.14 | `reer_bis`, August 2026 (monthly) | BIS data portal → Effective exchange rates → India, real, broad, monthly, 2026-08 | | |
| 10 | 1.2644 | `rca_refined_334`, 2000 (annual_cy) | UNCTADstat → "Revealed comparative advantage index" → India, product 334, year 2000 | | |
| 11 | 5598.89 | `oilcons_ind_kbd`, 2024 (annual_cy) | US EIA International Energy Data → Petroleum and other liquids → Consumption → India, 2024 (thousand barrels per day) | | |

Values were chosen to cover every main source (RBI, DGCI&S, World Bank, PPAC, BIS, UNCTAD, EIA) and both old and recent years.

# Data Source Policy

Every number in this project must come from an **official statistical agency, an international organisation, or the published replication data of a peer-reviewed paper**. No exceptions.

## Allowed sources

| Tier | Source | What we take from it |
|---|---|---|
| **A1: Indian official** | **RBI** *Handbook of Statistics on the Indian Economy*; RBI DBIE | Unit value and quantum indices, ToT (Table 121 in the 2025-26 edition), REER, BoP, GDP, trade by commodity |
| | **DGCI&S** (Ministry of Commerce), Foreign Trade Indices | Monthly/annual export and import unit value indices, ToT |
| | **Ministry of Commerce TradeStat** | Commodity-level trade values (HS 27, 2709, 2710) |
| | **PPAC** (Ministry of Petroleum & Natural Gas) | Indian crude basket price, crude import volume/value, import dependence |
| | **MoSPI** | GDP (national accounts) |
| **A2: International official** | **World Bank**: Commodity Price Data ("Pink Sheet"), WDI | Brent/Dubai/average crude, non-energy index, gold, MUV index; WDI ToT (cross-check) |
| | **IMF** | Commodity prices, cross-checks |
| | **BIS** | REER (cross-check) |
| | **UNCTADstat / UN Comtrade** | RCA, world trade in HS 2709/2710 (for RCA and GL indices) |
| | **US EIA**; **Energy Institute** *Statistical Review of World Energy* | World oil consumption and India's share |
| **A3: Peer-reviewed replication data** | Känzig (2021, *American Economic Review*), the author's official data | Oil supply news shocks |
| | Baumeister & Hamilton (2019, *American Economic Review*), the authors' official data | Oil supply and demand shocks |
| **Cross-check only** | FRED (St. Louis Fed), which redistributes official series | Brent cross-check; never the primary source |

## Never used

Kaggle, Statista, Investing.com, Macrotrends, Trading Economics, Wikipedia, news websites, blogs, ChatGPT/AI-generated numbers, or any number typed by hand from memory.

## Rules

1. **Raw files are never edited.** They are saved as downloaded in `data/raw/`. All cleaning, splicing and conversion happens in code.
2. **Every file is logged** in `data/SOURCES.md` with:
   - publisher, table/series ID and exact URL
   - download date
   - units, base year and frequency
   - fiscal year (April–March) or calendar year
   - SHA-256 checksum
3. **Every key series is cross-checked** against a second independent source, or recomputed from its components. For example, NTT = UV_X / UV_M × 100 is recomputed and compared with the published NTT.
4. **Fiscal year alignment:** Indian data run April–March. Monthly world prices are averaged to the Indian fiscal year in code, never mixed with calendar years.
5. **Base-year changes** (1978-79, 1999-2000, 2012-13, 2022-23) are linked using overlap ratios. The method and the overlap values are reported.
6. **Every number on a slide** carries a source line and must trace back to a file in `output/tables/`.
7. **Human check:** one teammate checks 10 random values against the original publication and records them in `data/validation_log.md`.

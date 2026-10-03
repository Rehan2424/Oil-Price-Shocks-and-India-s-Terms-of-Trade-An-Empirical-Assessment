"""Writes data/SOURCES.md: one row per raw file with publisher, URL, retrieval date and SHA-256."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RETRIEVED = "2026-10-03/04 (UTC)"

# folder or file prefix -> (publisher / dataset, URL, notes)
META = [
    ("worldbank/CMO-Historical-Data-Monthly", "World Bank, Commodity Price Data (Pink Sheet), monthly",
     "https://www.worldbank.org/en/research/commodity-markets", "Updated 2 Oct 2026; data to 2026M09"),
    ("worldbank/CMO-Historical-Data-Annual", "World Bank, Commodity Price Data (Pink Sheet), annual (MUV index)",
     "https://www.worldbank.org/en/research/commodity-markets", "Updated 2 Sep 2026"),
    ("worldbank/WDI_", "World Bank, World Development Indicators API",
     "https://api.worldbank.org/v2/country/IND/indicator/<ID>?format=json", "WDI last updated 2026-07-13"),
    ("ppac/", "PPAC (Ministry of Petroleum & Natural Gas), Crude Oil FOB Price (Indian Basket)",
     "https://ppac.gov.in/prices/international-prices-of-crude-oil", "One xlsx per fiscal year via the page's data service"),
    ("rbi/HBS2026_", "Reserve Bank of India, Handbook of Statistics on the Indian Economy 2025-26 (HTML table view)",
     "https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=Handbook%20of%20Statistics%20on%20Indian%20Economy",
     "Table number in file name; page = Scripts/PublicationsView.aspx?id=<id>"),
    ("dgcis/base2012-13/", "DGCI&S (Ministry of Commerce), Terms of Trade, Laspeyres base 2012-13",
     "https://dgciskol.gov.in/TermTradeArchive_New.aspx", "Monthly UVI, QI, NTT"),
    ("dgcis/base2022-23/", "DGCI&S, Terms of Trade, Laspeyres base 2022-23",
     "https://dgciskol.gov.in/TermTradeArchive_202223.aspx", "Monthly UVI, QI, NTT from Apr 2023"),
    ("dgcis/reports/", "DGCI&S, Summary Statistics of Foreign Trade Indices / methodology note",
     "https://dgciskol.gov.in/writereaddata/Downloads/", "Reference documents"),
    ("unctad/", "UNCTADstat bulk download (US.TermsOfTrade, US.RCA)",
     "https://unctadstat-api.unctad.org/bulkdownload/<dataset>/<file>", "Archives not committed; India extracts committed"),
    ("comtrade/", "UN Comtrade public API (India = 699, partner World, HS 2709/2710/27/TOTAL)",
     "https://comtradeapi.un.org/public/v1/preview/C/A/HS", "One JSON per year"),
    ("eia/", "U.S. Energy Information Administration, International Energy Data bulk file",
     "https://api.eia.gov/bulk/INTL.zip", "Archive not committed; consumption extract committed"),
    ("bis/", "Bank for International Settlements, effective exchange rates (WS_EER, M.R.B.IN)",
     "https://stats.bis.org/api/v1/data/WS_EER/M.R.B.IN/all?format=csv", "Real, broad basket, monthly"),
    ("fred/", "FRED (St. Louis Fed), Brent spot DCOILBRENTEU (source: EIA)",
     "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILBRENTEU", "Cross-check only"),
    ("shocks/oilSupplyNewsShocks", "Kanzig (2021, AER) oil supply news shocks, author's official data, vintage 2025M12",
     "https://github.com/dkaenzig/oilsupplynews", "CC BY 4.0"),
    ("shocks/VARdata", "Kanzig (2021, AER) VAR dataset", "https://github.com/dkaenzig/oilsupplynews", ""),
    ("shocks/BH2_", "Baumeister & Hamilton (2019, AER) structural oil supply/demand shocks, author's official data",
     "https://sites.google.com/site/cjsbaumeister/datasets", "Posterior medians"),
    ("shocks/OECD_plus6", "Baumeister & Hamilton (2019, AER) world industrial production index",
     "https://sites.google.com/site/cjsbaumeister/datasets", ""),
    ("shocks/GECON", "Baumeister, Korobilis & Lee (2022, REStat) Global Economic Conditions indicator",
     "https://sites.google.com/site/cjsbaumeister/datasets", ""),
]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


rows = []
for p in sorted(RAW.rglob("*")):
    if p.is_dir() or "extracted" in p.parts:
        continue
    rel = p.relative_to(RAW).as_posix()
    meta = next((m for m in META if rel.startswith(m[0])), ("(see folder)", "", ""))
    rows.append(f"| `{rel}` | {meta[1]} | {meta[2]} | {meta[3]} | `{sha(p)[:16]}…` |")

text = f"""# Data Sources

Every raw file in `data/raw/` is listed below, as downloaded (never edited).
Retrieved: {RETRIEVED}. SHA-256 is shown truncated to 16 hex characters (full hashes: run `sha256sum` on the file).
Policy: [`SOURCE_POLICY.md`](SOURCE_POLICY.md). Automatic checks: [`validation_report.md`](validation_report.md).

| File | Publisher / dataset | URL | Notes | SHA-256 |
|---|---|---|---|---|
""" + "\n".join(rows) + "\n"
(ROOT / "data" / "SOURCES.md").write_text(text)
print(len(rows), "files listed")

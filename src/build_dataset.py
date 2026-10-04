"""
Build the project datasets from the untouched raw files in data/raw/.

Outputs (data/processed/):
  monthly.csv     - monthly series (DGCI&S ToT, oil prices, shocks, REER, ...)
  annual_fy.csv   - Indian fiscal-year series (FY label = starting year: 2024 -> 2024-25)
  annual_cy.csv   - calendar-year series (UNCTAD/WDI ToT, RCA, Grubel-Lloyd, EIA)
  final_dataset.xlsx - all three tables + a variable dictionary

No number is typed by hand: every value is read from a raw file listed in data/SOURCES.md.
Run from the repository root:  python src/build_dataset.py
"""
from pathlib import Path
import glob
import json
import re
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

MONTHS_FY = ["april", "may", "june", "july", "august", "september",
             "october", "november", "december", "january", "february", "march"]


def to_num(s):
    return pd.to_numeric(pd.Series(s).replace({"…": np.nan, "..": np.nan, "-": np.nan}), errors="coerce")


def fy_of(ts):
    """Indian fiscal year (April-March) labelled by its starting year."""
    return ts.year if ts.month >= 4 else ts.year - 1


def fy_label(y):
    return f"{y}-{str(y + 1)[-2:]}"


# ----------------------------------------------------------------------------- World Bank Pink Sheet
def pink_sheet_monthly():
    f = RAW / "worldbank" / "CMO-Historical-Data-Monthly.xlsx"
    p = pd.read_excel(f, "Monthly Prices", header=None)
    names = p.iloc[4].tolist()
    want = {"Crude oil, average": "oil_avg", "Crude oil, Brent": "brent",
            "Crude oil, Dubai": "dubai", "Crude oil, WTI": "wti", "Gold": "gold"}
    data = p.iloc[6:].copy()
    out = pd.DataFrame({"date": pd.to_datetime(data[0].astype(str).str.replace("M", "-"), format="%Y-%m")})
    for i, n in enumerate(names):
        if n in want:
            out[want[n]] = to_num(data[i]).values
    ix = pd.read_excel(f, "Monthly Indices", header=None)
    hdr = ix.iloc[5].tolist()
    col_energy = [i for i, h in enumerate(hdr) if isinstance(h, str) and h.strip() == "Energy"][0]
    col_nonen = [i for i, h in enumerate(hdr) if isinstance(h, str) and h.strip().startswith("Non-energy")][0]
    d2 = ix.iloc[9:].copy()
    d2 = d2[d2[0].astype(str).str.match(r"^\d{4}M\d{2}$")]
    idx = pd.DataFrame({"date": pd.to_datetime(d2[0].str.replace("M", "-"), format="%Y-%m"),
                        "wb_energy_idx": to_num(d2[col_energy]).values,
                        "wb_nonenergy_idx": to_num(d2[col_nonen]).values})
    return out.merge(idx, on="date", how="left")


def pink_sheet_muv():
    """Manufactures Unit Value index (2010=100), calendar years."""
    f = RAW / "worldbank" / "CMO-Historical-Data-Annual.xlsx"
    a = pd.read_excel(f, "Annual Indices (Real)", header=None)
    col = None
    for r in range(4, 9):
        for c, v in enumerate(a.iloc[r].tolist()):
            if isinstance(v, str) and "MUV" in v:
                col = c
    rows = a[a[0].astype(str).str.match(r"^\d{4}$")]
    return pd.DataFrame({"year": rows[0].astype(int).values, "muv": to_num(rows[col]).values})


# ----------------------------------------------------------------------------- PPAC Indian basket
def ppac_icb():
    # One file per fiscal year; each row is a year ("2025-26") followed by April ... March prices.
    recs = []
    for f in sorted(glob.glob(str(RAW / "ppac" / "PPAC_crude-price_*.xlsx"))):
        df = pd.read_excel(f, sheet_name=0, header=None)
        rows = df[df[0].astype(str).str.match(r"^\d{4}-\d{2}$")]
        for _, r in rows.iterrows():
            fy = int(str(r[0])[:4])
            for k in range(12):
                v = pd.to_numeric(r[k + 1], errors="coerce")
                if pd.notna(v):
                    y = fy if k < 9 else fy + 1
                    m = k + 4 if k < 9 else k - 8
                    recs.append({"date": pd.Timestamp(y, m, 1), "icb_ppac": float(v), "ppac_file": Path(f).name})
    out = pd.DataFrame(recs).sort_values("date")
    assert not out["date"].duplicated().any(), "duplicate PPAC months"
    return out.drop(columns="ppac_file")


# ----------------------------------------------------------------------------- DGCI&S monthly indices
def _norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def dgcis_monthly(folder, suffix):
    # DGCI&S sheets are laid out by row label ("Export Grand Total", "Net terms of trade", ...), with
    # each month taking two columns: unit value index, then quantum index. Rows are found by label,
    # not position, because the layout shifts slightly between years.
    recs = {}
    files = sorted(glob.glob(str(RAW / "dgcis" / folder / "*.xlsx")))
    for f in files:
        df = pd.read_excel(f, header=None)
        lab = df[1].map(_norm)
        r_hdr = lab[lab.str.startswith("grand total indices")].index[0]
        r_x = lab[lab.str.startswith("export grand total")].index[0]
        r_m = lab[lab.str.startswith("import grand total")].index[0]
        r_ntt = lab[lab.str.startswith("net terms of trade")].index[0]
        for c in range(df.shape[1]):
            h = df.iat[r_hdr, c]
            if isinstance(h, (pd.Timestamp, np.datetime64)) or hasattr(h, "year"):
                d = pd.Timestamp(h).to_period("M").to_timestamp()
                recs[d] = {"date": d,
                           f"uvi_x_{suffix}": float(df.iat[r_x, c]),
                           f"uvi_m_{suffix}": float(df.iat[r_m, c]),
                           f"ntt_pub_{suffix}": float(df.iat[r_ntt, c]),
                           f"qi_x_{suffix}": float(df.iat[r_x, c + 1]),
                           f"qi_m_{suffix}": float(df.iat[r_m, c + 1])}
    return pd.DataFrame(list(recs.values())).sort_values("date").reset_index(drop=True)


# ----------------------------------------------------------------------------- RBI Handbook (HTML tables)
def _rbi_table(name):
    # The saved Handbook pages contain several small layout tables; the data table is the largest one.
    t = pd.read_html(RAW / "rbi" / name)
    return max(t, key=lambda x: x.size)


def rbi_t121():
    # Table 121 stacks three base periods (1978-79, 1999-2000, 2012-13), each block introduced by a
    # "Base: ..." row, so we carry the current base down as we read.
    t = _rbi_table("HBS2026_T121_Index_Numbers_Terms_of_Trade.html")
    base, recs = None, []
    for _, r in t.iterrows():
        c0 = str(r[0])
        m = re.search(r"Base:\s*(\d{4})", c0)
        if m:
            base = m.group(1)
            continue
        if re.match(r"^\d{4}-\d{2}$", c0) and base:
            v = to_num(r.tolist()[1:8]).tolist()
            recs.append({"fy": int(c0[:4]), "base": base, "uvi_x": v[0], "uvi_m": v[1], "qi_x": v[2],
                         "qi_m": v[3], "gtt": v[4], "ntt": v[5], "itt": v[6]})
    return pd.DataFrame(recs)


def rbi_t111():
    t = _rbi_table("HBS2026_T111_Foreign_Trade_USD.html")
    rows = t[t[0].astype(str).str.match(r"^\d{4}-\d{2}$")]
    cols = ["x_oil", "x_nonoil", "x_total", "m_oil", "m_nonoil", "m_total", "tb_oil", "tb_nonoil", "tb_total"]
    out = pd.DataFrame({"fy": rows[0].str[:4].astype(int).values})
    for i, c in enumerate(cols):
        out[c + "_usdm"] = to_num(rows[i + 1]).values
    return out


def rbi_t32():
    t = _rbi_table("HBS2026_T32_Crude_Production_Imports.html")
    rows = t[t[0].astype(str).str.match(r"^\d{4}-\d{2}$")]
    out = pd.DataFrame({"fy": rows[0].str[:4].astype(int).values,
                        "crude_prod_mmt": to_num(rows[1]).values, "pol_prod_mmt": to_num(rows[2]).values,
                        "crude_imp_mmt": to_num(rows[3]).values, "pol_imp_mmt": to_num(rows[4]).values})
    # The published rows for FY1990-91..1997-98 are an exact copy of FY2000-01..2007-08 (all four columns),
    # a transcription error in the Handbook (see validation report), so they are set to missing.
    out.loc[out["fy"].between(1990, 1997), ["crude_prod_mmt", "pol_prod_mmt", "crude_imp_mmt", "pol_imp_mmt"]] = np.nan
    return out


def rbi_t133():
    t = _rbi_table("HBS2026_T133_Exchange_Rate_FY.html")
    rows = t[t[0].astype(str).str.match(r"^\d{4}-\d{2}$")]
    return pd.DataFrame({"fy": rows[0].str[:4].astype(int).values, "inr_usd_avg": to_num(rows[3]).values,
                         "inr_usd_end": to_num(rows[4]).values})


def rbi_t135():
    t = _rbi_table("HBS2026_T135_NEER_REER_40_FY.html")
    rows = t[t[0].astype(str).str.match(r"^\d{4}-\d{2}$")]
    return pd.DataFrame({"fy": rows[0].str[:4].astype(int).values, "reer40_rbi_fy": to_num(rows[2]).values})


# ----------------------------------------------------------------------------- WDI / UNCTAD / EIA / Comtrade / BIS
def wdi(ind, ctry="IND"):
    d = json.load(open(RAW / "worldbank" / f"WDI_{ind}_{ctry}.json"))
    s = {int(r["date"]): r["value"] for r in d[1] if r["value"] is not None}
    return pd.Series(s, name=ind).sort_index()


def unctad_tot():
    ind = pd.read_csv(RAW / "unctad" / "UNCTAD_US_TermsOfTrade_India_extract.csv")
    ind["Index Base 2015"] = pd.to_numeric(ind["Index Base 2015"])
    piv = ind.pivot(index="Year", columns="Index", values="Index Base 2015")
    return pd.DataFrame({"year": piv.index, "uvi_x_unctad": piv[5].values, "uvi_m_unctad": piv[6].values,
                         "ntt_unctad": piv[7].values})


def unctad_rca():
    df = pd.read_csv(RAW / "unctad" / "UNCTAD_US_RCA_India_extract.csv", dtype=str)
    df["Index"] = df["Index"].astype(float)
    piv = df[df["Product"].isin(["333", "334", "335"])].pivot(index="Year", columns="Product", values="Index")
    piv.index = piv.index.astype(int)
    return pd.DataFrame({"year": piv.index, "rca_crude_333": piv.get("333").values,
                         "rca_refined_334": piv["334"].values, "rca_residual_335": piv["335"].values})


def eia_consumption():
    recs = {}
    for line in open(RAW / "eia" / "EIA_INTL_petroleum_consumption_all_countries_TBPD_A.jsonl"):
        d = json.loads(line)
        code = d["series_id"].split("-")[2]
        if code in ("IND", "WORL", "CHN", "USA"):
            for y, v in d["data"]:
                if isinstance(v, (int, float)):
                    recs.setdefault(int(y), {})[f"oilcons_{code.lower()}_kbd"] = v
    out = pd.DataFrame.from_dict(recs, orient="index").sort_index()
    out.index.name = "year"
    out["india_share_world_oil_cons"] = out["oilcons_ind_kbd"] / out["oilcons_worl_kbd"]
    return out.reset_index()


def comtrade():
    recs = {}
    for f in sorted(glob.glob(str(RAW / "comtrade" / "Comtrade_India_*.json"))):
        d = json.load(open(f))
        for r in d.get("data", []):
            y = int(r["period"])
            k = f"{r['flowCode'].lower()}_{r['cmdCode'].lower()}"
            recs.setdefault(y, {})[k + "_usd"] = r["primaryValue"]
            if r["cmdCode"] in ("2709", "2710") and r.get("netWgt"):
                recs[y][k + "_kg"] = r["netWgt"]
    out = pd.DataFrame.from_dict(recs, orient="index").sort_index()
    out.index.name = "year"
    return out.reset_index()


def bis_reer():
    df = pd.read_csv(RAW / "bis" / "BIS_WS_EER_M_R_B_IN.csv")
    return pd.DataFrame({"date": pd.to_datetime(df["TIME_PERIOD"] + "-01"), "reer_bis": df["OBS_VALUE"].astype(float)})


# ----------------------------------------------------------------------------- Oil shocks / global activity
def shocks_monthly():
    k = pd.read_excel(RAW / "shocks" / "oilSupplyNewsShocks_2025M12.xlsx", "Monthly")
    k = pd.DataFrame({"date": pd.to_datetime(k["Date"].str.replace("M", "-"), format="%Y-%m"),
                      "kanzig_news_shock": k["Oil supply news shock"].values,
                      "kanzig_surprise": k["Oil supply surprise series"].values})
    s = pd.read_excel(RAW / "shocks" / "BH2_supply_shocks.xlsx", header=None).iloc[2:, :2]
    s = pd.DataFrame({"date": pd.to_datetime(s[0]), "bh_supply": pd.to_numeric(s[1])})
    d = pd.read_excel(RAW / "shocks" / "BH2_demand_shocks.xlsx", header=None).iloc[2:, :4]
    d = pd.DataFrame({"date": pd.to_datetime(d[0]), "bh_activity": pd.to_numeric(d[1]),
                      "bh_consumption_demand": pd.to_numeric(d[2]), "bh_inventory_demand": pd.to_numeric(d[3])})
    w = pd.read_excel(RAW / "shocks" / "OECD_plus6_industrial_production.xlsx", header=None).iloc[1:, :2]
    w = pd.DataFrame({"date": pd.to_datetime(w[0]), "world_ip": pd.to_numeric(w[1])})
    g = pd.read_excel(RAW / "shocks" / "GECON_indicator.xlsx", header=None).iloc[1:, :2]
    g = pd.DataFrame({"date": pd.to_datetime(g[0].astype(str).str.replace("M", "-"), format="%Y-%m"),
                      "gecon": pd.to_numeric(g[1])})
    out = k
    for x in (s, d, w, g):
        out = out.merge(x.dropna(subset=["date"]), on="date", how="outer")
    return out.sort_values("date")


# ----------------------------------------------------------------------------- assemble
def fy_average(df, cols, how="mean", min_months=12):
    """Average (or sum) monthly series over Indian fiscal years; incomplete years are left missing."""
    x = df.copy()
    x["fy"] = x["date"].map(fy_of)
    g = x.groupby("fy")
    agg = g[cols].agg(how)
    cnt = g[cols].count()
    agg[cnt < min_months] = np.nan
    return agg.reset_index()


def main():
    # ---------------- monthly
    pink = pink_sheet_monthly()
    icb = ppac_icb()
    d12 = dgcis_monthly("base2012-13", "b12")
    d22 = dgcis_monthly("base2022-23", "b22")
    reer = bis_reer()
    sh = shocks_monthly()
    m = pink.merge(icb, on="date", how="left").merge(d12, on="date", how="left").merge(d22, on="date", how="left")
    m = m.merge(reer, on="date", how="left").merge(sh, on="date", how="left")
    m = m[m["date"] >= "1960-01-01"].sort_values("date").reset_index(drop=True)
    m["ntt_b12"] = 100 * m["uvi_x_b12"] / m["uvi_m_b12"]          # recomputed from components
    m["ntt_b22"] = 100 * m["uvi_x_b22"] / m["uvi_m_b22"]
    m["fy"] = m["date"].map(fy_of)
    m.to_csv(OUT / "monthly.csv", index=False, float_format="%.6g")

    # ---------------- annual, Indian fiscal year
    oilfy = fy_average(m, ["brent", "dubai", "oil_avg", "gold", "wb_nonenergy_idx", "reer_bis", "world_ip"])
    shk = fy_average(m, ["kanzig_news_shock", "bh_supply", "bh_activity", "bh_consumption_demand",
                         "bh_inventory_demand"], how="sum")
    shk.columns = ["fy"] + [c + "_fysum" for c in shk.columns[1:]]
    icbfy = fy_average(m, ["icb_ppac"])
    muv = pink_sheet_muv().set_index("year")["muv"]
    # FY t covers Apr t - Mar t+1: 9 months of CY t and 3 months of CY t+1
    muv_fy = pd.Series({y: 0.75 * muv.get(y, np.nan) + 0.25 * muv.get(y + 1, np.nan) for y in muv.index},
                       name="muv_fy")
    a = pd.DataFrame({"fy": range(1960, int(m["fy"].max()) + 1)})
    a["fy_label"] = a["fy"].map(fy_label)
    # national-accounts ToT (goods & services), WDI, FY-based (WDI label t = FY t/t+1, verified vs RBI T4)
    px = wdi("NE.EXP.GNFS.CN") / wdi("NE.EXP.GNFS.KN")
    pm = wdi("NE.IMP.GNFS.CN") / wdi("NE.IMP.GNFS.KN")
    tot_na = (px / pm)
    tot_na = 100 * tot_na / tot_na.loc[2015]
    # WDI back-casts 1960-69 constant-price exports and imports with one common deflator, so the
    # export/import deflator ratio is frozen at its 1999 value in those years (see validation report).
    tot_na[tot_na.index < 1970] = np.nan
    a = a.merge(pd.DataFrame({"fy": tot_na.index, "tot_gs_na": tot_na.values,
                              "px_gs_defl": (px / px.loc[2015] * 100).values,
                              "pm_gs_defl": (pm / pm.loc[2015] * 100).values}), on="fy", how="left")
    gdp_usd = wdi("NY.GDP.MKTP.CD")
    a = a.merge(pd.DataFrame({"fy": gdp_usd.index, "gdp_usd": gdp_usd.values}), on="fy", how="left")
    gdp_g = wdi("NY.GDP.MKTP.KD.ZG")
    a = a.merge(pd.DataFrame({"fy": gdp_g.index, "india_gdp_growth": gdp_g.values}), on="fy", how="left")
    # RBI/DGCI&S merchandise ToT by base, plus chain-linked series
    t121 = rbi_t121()
    for b in ("1978", "1999", "2012"):
        sub = t121[t121["base"] == b][["fy", "uvi_x", "uvi_m", "ntt"]].copy()
        # NTT is recomputed from the published unit value indices (three published NTT values are
        # inconsistent with their own UVIs beyond rounding; see validation report)
        sub["ntt_calc"] = 100 * sub["uvi_x"] / sub["uvi_m"]
        sub = sub[["fy", "uvi_x", "uvi_m", "ntt_calc", "ntt"]]
        sub.columns = ["fy", f"uvi_x_rbi_{b}", f"uvi_m_rbi_{b}", f"ntt_rbi_{b}", f"ntt_rbi_pub_{b}"]
        a = a.merge(sub, on="fy", how="left")
    # chain: 1999-base for 1999..2012, link 1978-base backwards at 1999, 2012-base forward at 2012 (=100)
    chain = pd.Series(np.nan, index=a["fy"].values)
    s99 = a.set_index("fy")["ntt_rbi_1999"]
    s78 = a.set_index("fy")["ntt_rbi_1978"]
    s12 = a.set_index("fy")["ntt_rbi_2012"].copy()
    s12.loc[2012] = 100.0                     # base year of the 2012-13 series is 100 by definition
    for y in range(1999, 2013):
        chain[y] = s99.get(y)
    for y in range(1994, 1999):
        chain[y] = s78[y] * s99[1999] / s78[1999]
    for y in range(2013, 2026):
        chain[y] = s12[y] * s99[2012] / 100.0
    a["ntt_rbi_chained"] = a["fy"].map(chain)
    a = a.merge(rbi_t111(), on="fy", how="left").merge(rbi_t32(), on="fy", how="left")
    a = a.merge(rbi_t133(), on="fy", how="left").merge(rbi_t135(), on="fy", how="left")
    a["s_x_oil"] = a["x_oil_usdm"] / a["x_total_usdm"]
    a["s_m_oil"] = a["m_oil_usdm"] / a["m_total_usdm"]
    a["benchmark_elasticity"] = a["s_x_oil"] - a["s_m_oil"]
    a["net_oil_imports_pct_gdp"] = 100 * (a["m_oil_usdm"] - a["x_oil_usdm"]) * 1e6 / a["gdp_usd"]
    a = a.merge(oilfy, on="fy", how="left").merge(shk, on="fy", how="left").merge(icbfy, on="fy", how="left")
    a = a.merge(pd.DataFrame({"fy": muv_fy.index, "muv_fy": muv_fy.values}), on="fy", how="left")
    a["real_brent"] = 100 * a["brent"] / a["muv_fy"]
    a["real_oil_avg"] = 100 * a["oil_avg"] / a["muv_fy"]
    a["real_nonenergy"] = 100 * a["wb_nonenergy_idx"] / a["muv_fy"]
    a["real_gold"] = 100 * a["gold"] / a["muv_fy"]
    a.to_csv(OUT / "annual_fy.csv", index=False, float_format="%.6g")

    # ---------------- annual, calendar year
    c = pd.DataFrame({"year": range(1960, 2027)})
    nbtt = wdi("TT.PRI.MRCH.XD.WD")
    c = c.merge(pd.DataFrame({"year": nbtt.index, "ntt_wdi": nbtt.values}), on="year", how="left")
    c = c.merge(unctad_tot(), on="year", how="left").merge(unctad_rca(), on="year", how="left")
    c = c.merge(eia_consumption(), on="year", how="left").merge(comtrade(), on="year", how="left")
    c["muv"] = c["year"].map(muv)
    wg = wdi("NY.GDP.MKTP.KD.ZG", "WLD")
    c = c.merge(pd.DataFrame({"year": wg.index, "world_gdp_growth": wg.values}), on="year", how="left")
    oilcy = m.assign(year=m["date"].dt.year).groupby("year")[["brent", "dubai", "oil_avg"]].mean().reset_index()
    c = c.merge(oilcy, on="year", how="left")
    # Grubel-Lloyd index (L19): GL = 1 - |X - M| / (X + M)
    for code in ("27", "2709", "2710"):
        X, M = c.get(f"x_{code}_usd"), c.get(f"m_{code}_usd")
        X = X.fillna(0) if X is not None else 0
        c[f"gl_{code}"] = 1 - (X - M).abs() / (X + M)
    # GL at the HS-4 level for oil (crude + refined), the weighted average of the two lines
    x4 = c["x_2709_usd"].fillna(0) + c["x_2710_usd"].fillna(0)
    m4 = c["m_2709_usd"].fillna(0) + c["m_2710_usd"].fillna(0)
    c["gl_oil_hs4_weighted"] = 1 - ((c["x_2709_usd"].fillna(0) - c["m_2709_usd"]).abs()
                                    + (c["x_2710_usd"].fillna(0) - c["m_2710_usd"]).abs()) / (x4 + m4)
    c["gl_oil_hs2_like"] = 1 - (x4 - m4).abs() / (x4 + m4)
    # unit values (US$ per tonne) and the export/import unit-value ratio used in L20
    c["uv_imp_crude_usd_t"] = c["m_2709_usd"] / (c["m_2709_kg"] / 1000)
    c["uv_exp_refined_usd_t"] = c["x_2710_usd"] / (c["x_2710_kg"] / 1000)
    c["uv_ratio_refined_x_over_crude_m"] = c["uv_exp_refined_usd_t"] / c["uv_imp_crude_usd_t"]
    c.to_csv(OUT / "annual_cy.csv", index=False, float_format="%.6g")

    # ---------------- Excel copy with dictionary
    dictionary = pd.read_csv(ROOT / "data" / "variable_dictionary.csv")
    with pd.ExcelWriter(OUT / "final_dataset.xlsx") as xw:
        dictionary.to_excel(xw, sheet_name="README_variables", index=False)
        m[m["date"] >= "2000-01-01"].to_excel(xw, sheet_name="monthly_2000on", index=False)
        a.to_excel(xw, sheet_name="annual_fiscal_year", index=False)
        c.to_excel(xw, sheet_name="annual_calendar_year", index=False)
    print("monthly", m.shape, "annual_fy", a.shape, "annual_cy", c.shape)


if __name__ == "__main__":
    main()

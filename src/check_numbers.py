"""
Independent re-check of the numbers we quote in the slides, the speaker notes and the viva notes.

It does not reuse build_dataset.py or econ.py: the raw files in data/raw/ are parsed again here, the
annual series are rebuilt, and every model is re-estimated with plain OLS. Each result is compared
with the value we quote, rounded the way we quote it. The report is written to docs/number_check.md; the
hand-checked part (outside facts, live re-downloads) is kept in docs/number_check_external.md and appended.

Run from the repository root:  python src/check_numbers.py
"""
from pathlib import Path
import glob
import json
import re
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from arch.unitroot import PhillipsPerron, ZivotAndrews
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan, linear_reset
from statsmodels.stats.stattools import jarque_bera
from statsmodels.tsa.ardl import UECM, ardl_select_order
from statsmodels.tsa.stattools import adfuller, kpss

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


# ============================================================================ raw files, parsed afresh
def first_row_containing(df, text, col=None):
    cells = df.astype(str) if col is None else df[[col]].astype(str)
    hits = cells.apply(lambda c: c.str.contains(text, regex=False)).any(axis=1)
    return hits[hits].index[0]


def pink_monthly():
    f = RAW / "worldbank" / "CMO-Historical-Data-Monthly.xlsx"
    p = pd.read_excel(f, "Monthly Prices", header=None)
    h = first_row_containing(p, "Crude oil, Brent")
    names = {v: i for i, v in enumerate(p.loc[h]) if isinstance(v, str)}
    rows = p[p[0].astype(str).str.fullmatch(r"\d{4}M\d{2}")]
    out = pd.DataFrame(index=pd.to_datetime(rows[0].str.replace("M", "-"), format="%Y-%m"))
    for key, name in [("brent", "Crude oil, Brent"), ("dubai", "Crude oil, Dubai"),
                      ("avg", "Crude oil, average"), ("gold", "Gold")]:
        out[key] = pd.to_numeric(rows[names[name]], errors="coerce").values
    ix = pd.read_excel(f, "Monthly Indices", header=None)
    h = first_row_containing(ix, "Non-energy")
    col = [i for i, v in enumerate(ix.loc[h]) if isinstance(v, str) and v.strip().startswith("Non-energy")][0]
    r2 = ix[ix[0].astype(str).str.fullmatch(r"\d{4}M\d{2}")]
    nonen = pd.Series(pd.to_numeric(r2[col], errors="coerce").values,
                      index=pd.to_datetime(r2[0].str.replace("M", "-"), format="%Y-%m"))
    out["nonenergy"] = nonen.reindex(out.index)
    return out


def muv_calendar():
    a = pd.read_excel(RAW / "worldbank" / "CMO-Historical-Data-Annual.xlsx", "Annual Indices (Real)", header=None)
    h = first_row_containing(a, "MUV")
    col = [i for i, v in enumerate(a.loc[h]) if isinstance(v, str) and "MUV" in v][0]
    rows = a[a[0].astype(str).str.fullmatch(r"\d{4}")]
    return pd.Series(pd.to_numeric(rows[col], errors="coerce").values, index=rows[0].astype(int).values)


def wdi(code, country="IND"):
    d = json.load(open(RAW / "worldbank" / f"WDI_{code}_{country}.json"))
    return pd.Series({int(r["date"]): r["value"] for r in d[1] if r["value"] is not None}).sort_index()


def dgcis(folder):
    recs = {}
    for f in sorted(glob.glob(str(RAW / "dgcis" / folder / "*.xlsx"))):
        df = pd.read_excel(f, header=None)
        lab = df[1].astype(str).str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
        hdr = lab[lab.str.startswith("grand total indices")].index[0]
        rx = lab[lab.str.startswith("export grand total")].index[0]
        rm = lab[lab.str.startswith("import grand total")].index[0]
        rn = lab[lab.str.startswith("net terms of trade")].index[0]
        for c in range(df.shape[1]):
            v = df.iat[hdr, c]
            if hasattr(v, "year"):
                d = pd.Timestamp(v.year, v.month, 1)
                recs[d] = (float(df.iat[rx, c]), float(df.iat[rm, c]), float(df.iat[rn, c]), float(df.iat[rx, c + 1]))
    return pd.DataFrame.from_dict(recs, orient="index", columns=["uvi_x", "uvi_m", "ntt_pub", "qi_x"]).sort_index()


def rbi(name):
    t = max(pd.read_html(RAW / "rbi" / name), key=lambda x: x.size)
    return t


def rbi_rows(name):
    t = rbi(name)
    rows = t[t[0].astype(str).str.fullmatch(r"\d{4}-\d{2}")].copy()
    rows.index = rows[0].str[:4].astype(int)
    return rows.drop(columns=0).apply(pd.to_numeric, errors="coerce")


def t121_by_base():
    t = rbi("HBS2026_T121_Index_Numbers_Terms_of_Trade.html")
    blocks, base = {}, None
    for _, r in t.iterrows():
        m = re.search(r"Base:\s*(\d{4})", str(r[0]))
        if m:
            base = m.group(1); blocks[base] = {}
        elif base and re.fullmatch(r"\d{4}-\d{2}", str(r[0])):
            v = pd.to_numeric(pd.Series(r.tolist()[1:]), errors="coerce").tolist()
            blocks[base][int(str(r[0])[:4])] = {"ux": v[0], "um": v[1], "ntt_pub": v[5]}
    return {b: pd.DataFrame.from_dict(d, orient="index") for b, d in blocks.items()}


def ppac():
    recs = {}
    for f in glob.glob(str(RAW / "ppac" / "PPAC_crude-price_*.xlsx")):
        df = pd.read_excel(f, header=None)
        for _, r in df[df[0].astype(str).str.fullmatch(r"\d{4}-\d{2}")].iterrows():
            y0 = int(str(r[0])[:4])
            for k in range(12):
                v = pd.to_numeric(r[k + 1], errors="coerce")
                if pd.notna(v):
                    recs[pd.Timestamp(y0 + (k >= 9), (k + 3) % 12 + 1, 1)] = float(v)
    return pd.Series(recs).sort_index()


def comtrade():
    recs = {}
    for f in glob.glob(str(RAW / "comtrade" / "Comtrade_India_*.json")):
        for r in json.load(open(f)).get("data", []):
            k = f"{r['flowCode']}_{r['cmdCode']}"
            recs.setdefault(int(r["period"]), {})[k] = r["primaryValue"]
            if r.get("netWgt"):
                recs[int(r["period"])][k + "_kg"] = r["netWgt"]
    return pd.DataFrame.from_dict(recs, orient="index").sort_index()


def eia():
    out = {}
    for line in open(RAW / "eia" / "EIA_INTL_petroleum_consumption_all_countries_TBPD_A.jsonl"):
        d = json.loads(line)
        out[d["series_id"].split("-")[2]] = {int(y): v for y, v in d["data"] if isinstance(v, (int, float))}
    return out


def shocks():
    k = pd.read_excel(RAW / "shocks" / "oilSupplyNewsShocks_2025M12.xlsx", "Monthly")
    k = pd.Series(k["Oil supply news shock"].values, index=pd.to_datetime(k["Date"].str.replace("M", "-")))
    s = pd.read_excel(RAW / "shocks" / "BH2_supply_shocks.xlsx", header=None).iloc[2:, :2].dropna()
    d = pd.read_excel(RAW / "shocks" / "BH2_demand_shocks.xlsx", header=None).iloc[2:, :4].dropna()
    bh = pd.DataFrame({"supply": pd.to_numeric(s[1]).values}, index=pd.to_datetime(s[0]).values)
    dd = pd.DataFrame(d.iloc[:, 1:].apply(pd.to_numeric).values, index=pd.to_datetime(d[0]).values,
                      columns=["activity", "consumption", "inventory"])
    return k, bh.join(dd, how="outer")


# ============================================================================ series built from the raw files
pk = pink_monthly()
muv = muv_calendar()
d12, d22 = dgcis("base2012-13"), dgcis("base2022-23")
d12["ntt"] = 100 * d12.uvi_x / d12.uvi_m
icb = ppac()
kanzig, bh = shocks()


def fy_of(ts):
    return ts.year if ts.month >= 4 else ts.year - 1


def fy_mean(s, how="mean"):
    g = s.groupby(s.index.map(fy_of))
    v = g.agg(how)
    return v[g.count() == 12]


A = pd.DataFrame(index=range(1960, 2027))
for k in ("brent", "avg", "nonenergy", "gold"):
    A[k] = fy_mean(pk[k])
A["muv"] = [0.75 * muv.get(y, np.nan) + 0.25 * muv.get(y + 1, np.nan) for y in A.index]
for k in ("brent", "avg", "nonenergy", "gold"):
    A["real_" + k] = 100 * A[k] / A["muv"]
px = wdi("NE.EXP.GNFS.CN") / wdi("NE.EXP.GNFS.KN")
pm = wdi("NE.IMP.GNFS.CN") / wdi("NE.IMP.GNFS.KN")
tot = (px / pm) / (px / pm)[2015] * 100
A["tot"] = tot[tot.index >= 1970]
A["gdp_usd"] = wdi("NY.GDP.MKTP.CD")

# merchandise NTT: newest base for each year, older bases linked at the overlap (1999 and 2012)
T121 = t121_by_base()
n = {b: 100 * T121[b].ux / T121[b].um for b in T121}
n["2012"][2012] = 100.0
chain = pd.Series(dtype=float)
for y in range(1999, 2013):
    chain[y] = n["1999"][y]
for y in range(1994, 1999):
    chain[y] = n["1978"][y] * n["1999"][1999] / n["1978"][1999]
for y in range(2013, 2026):
    chain[y] = n["2012"][y] * n["1999"][2012] / 100
A["ntt"] = chain

t111 = rbi_rows("HBS2026_T111_Foreign_Trade_USD.html")       # columns 1-9: X oil, non-oil, total, M oil, ...
A["x_oil"], A["x_tot"], A["m_oil"], A["m_tot"] = t111[1], t111[3], t111[4], t111[6]
A["s_x"], A["s_m"] = A.x_oil / A.x_tot, A.m_oil / A.m_tot
A["bench"] = A.s_x - A.s_m
t32 = rbi_rows("HBS2026_T32_Crude_Production_Imports.html")   # crude prod, POL prod, crude imp, POL imp
t133 = rbi_rows("HBS2026_T133_Exchange_Rate_FY.html")         # column 4 = US dollar, end-year
C = comtrade()
E = eia()

# ============================================================================ the claims
CLAIMS = []
SECTION = [""]


def section(title):
    SECTION[0] = title


def parse(q):
    s = q.replace("−", "-").replace("–", "-")
    s = re.sub(r"[^\d.\-]", "", s)
    dec = len(s.split(".")[1]) if "." in s else 0
    return float(s), dec


def claim(where, what, quoted, value, source, tol=None, shown=None):
    """quoted: the number exactly as we write it; value: what the raw data give."""
    q, dec = parse(quoted)
    ok = abs(value - q) <= (tol if tol is not None else 0.5 * 10 ** -dec + 1e-9)
    CLAIMS.append((SECTION[0], where, what, quoted, shown or f"{value:.{dec + 2}f}", source, ok))


def fact(where, what, quoted, ok, shown, source):
    CLAIMS.append((SECTION[0], where, what, quoted, shown, source, bool(ok)))


def pct(a, b):
    return 100 * (b / a - 1)


def ols(y, X, cov="nonrobust", **kw):
    return sm.OLS(y, sm.add_constant(X), missing="drop").fit(cov_type=cov, cov_kwds=kw or None)


# ---------------------------------------------------------------------------- slide 1: the hook
section("Slide 1: March 2026")
m26 = lambda s, d: s.loc[pd.Timestamp(d)]
claim("Slide 1", "Brent, February 2026 (US$/bbl)", "$71", m26(pk.brent, "2026-02"), "Pink Sheet, monthly")
claim("Slide 1", "Brent, March 2026 (US$/bbl)", "$104", m26(pk.brent, "2026-03"), "Pink Sheet, monthly")
claim("Slide 1", "Brent rise, Feb to Mar 2026", "+46%", pct(m26(pk.brent, "2026-02"), m26(pk.brent, "2026-03")), "Pink Sheet")
claim("Slide 1", "Indian crude basket, February 2026", "$69", m26(icb, "2026-02"), "PPAC FY2025-26 file")
claim("Slide 1", "Indian crude basket, March 2026", "$113", m26(icb, "2026-03"), "PPAC FY2025-26 file")
claim("Slide 1", "Rupee per US$, end-March 2026", "94.65", t133.loc[2025, 4], "RBI Table 133, end-year")
usd_end = t133[4].dropna()
fact("Slide 1", "End-March 2026 is the weakest year-end rupee rate in the table", "weakest year-end rate on record",
     usd_end.idxmax() == 2025, f"highest end-year value: {usd_end.max():.4f} in FY{usd_end.idxmax()} "
     f"(table starts FY{usd_end.index.min()})", "RBI Table 133")
claim("Slide 1", "Merchandise ToT after the last shock, FY2020-21 to FY2022-23", "−24%", pct(A.ntt[2020], A.ntt[2022]),
      "RBI Table 121, chain-linked")
# 2026: what the monthly data do and do not show
n22 = 100 * d22.uvi_x / d22.uvi_m
three = lambda s_, a_, b_: s_.loc[a_:b_].mean()
claim("Viva notes", "2026, base 2012-13: Apr-Jun vs Nov-Jan, three-month averages", "+5.5%",
      pct(three(d12.ntt, "2025-11", "2026-01"), three(d12.ntt, "2026-04", "2026-06")), "DGCI&S")
claim("Viva notes", "2026, base 2022-23: Apr-Jun vs Nov-Jan, three-month averages", "+3.4%",
      pct(three(n22, "2025-11", "2026-01"), three(n22, "2026-04", "2026-06")), "DGCI&S")
claim("Viva notes", "Feb to Jun 2026, single months, base 2012-13", "−13%", pct(m26(d12.ntt, "2026-02"), m26(d12.ntt, "2026-06")), "DGCI&S")
claim("Viva notes", "Feb to Jun 2026, single months, base 2022-23", "+8%", pct(m26(n22, "2026-02"), m26(n22, "2026-06")), "DGCI&S")
both = np.log(pd.DataFrame({"a": d12.ntt, "b": n22}).loc["2023-04":"2026-06"]).diff().dropna()
fact("Viva notes", "The two DGCI&S bases barely agree month to month", "correlation about zero",
     abs(both.corr().iloc[0, 1]) < 0.15, f"correlation of monthly changes {both.corr().iloc[0, 1]:.2f}, {len(both)} months",
     "DGCI&S, both bases")

# ---------------------------------------------------------------------------- slides 2-4
section("Slides 2-4: exposure, benchmark, RCA, Grubel-Lloyd")
claim("Slide 2", "Crude imports as % of crude refined (imports / (imports + output)), FY2025-26",
      "90%", 100 * t32.loc[2025, 3] / (t32.loc[2025, 3] + t32.loc[2025, 1]), "RBI Table 32 (2025-26 provisional)", tol=1)
share24 = E["IND"][2024] / E["WORL"][2024]
claim("Slide 2", "India's share of world oil consumption, 2024", "5.4%", 100 * share24, "EIA International Energy Data")
rank = sorted(((v[2024], k) for k, v in E.items() if 2024 in v and len(k) == 3 and k not in ("WORL",)), reverse=True)
countries = [k for _, k in rank if k.isalpha() and k.isupper()]
fact("Slide 2", "India is the 3rd-largest oil consumer", "3rd, after the US and China",
     countries[:3] == ["USA", "CHN", "IND"], "top three: " + ", ".join(countries[:3]), "EIA")
claim("Slide 3", "Offer-curve diagram, case A: ToT ray after the supply cut (h = 0.55)", "0.86",
      (0.55 / 1.0) ** (1 / 4), "Model in src/slide_figures.py (elasticities 1.5)")
claim("Slide 3", "Offer-curve diagram, case C: ToT ray after India's demand grows (k = 1.8)", "0.86",
      (1.0 / 1.8) ** (1 / 4), "Model in src/slide_figures.py")
claim("Slide 3", "Merchandise ToT, FY2020-21 to FY2022-23", "−24%", pct(A.ntt[2020], A.ntt[2022]), "RBI Table 121")
claim("Viva notes", "Same, one decimal", "−23.7%", pct(A.ntt[2020], A.ntt[2022]), "RBI Table 121")
claim("Notes", "Brent, Feb to Jun 2022", "+25%", pct(m26(pk.brent, "2022-02"), m26(pk.brent, "2022-06")), "Pink Sheet")
claim("Slide 4", "Benchmark s_x − s_m, FY1999-00", "−0.25", A.bench[1999], "RBI Table 111")
claim("Slide 4", "Benchmark s_x − s_m, FY2025-26", "−0.10", A.bench[2025], "RBI Table 111")
claim("Viva notes", "Oil share of exports, FY1990-91", "3%", 100 * A.s_x[1990], "RBI Table 111")
sx08 = A.s_x.loc[2008:2025]
claim("Slide 4 notes", "Lowest oil share of exports since FY2008", "9%", 100 * sx08.min(), "RBI Table 111",
      shown=f"{100 * sx08.min():.1f}% (FY{sx08.idxmin()})")
claim("Viva notes / notes", "Highest oil share of exports since FY2008", "22%", 100 * sx08.max(), "RBI Table 111",
      shown=f"{100 * sx08.max():.1f}% (FY{sx08.idxmax()})")
sm_ = A.s_m.loc[1987:2025]; sx_ = A.s_x.loc[1987:2025]
claim("Viva notes", "Oil share of imports, FY1987-2025: mean", "26%", 100 * sm_.mean(), "RBI Table 111")
claim("Viva notes", "Oil share of imports: lowest", "15%", 100 * sm_.min(), "RBI Table 111")
claim("Viva notes", "Oil share of imports: highest", "37%", 100 * sm_.max(), "RBI Table 111")
claim("Viva notes", "Oil share of exports, FY1987-2025: mean", "10%", 100 * sx_.mean(), "RBI Table 111")
claim("Viva notes", "Oil share of exports: lowest", "0.1%", 100 * sx_.min(), "RBI Table 111")
rca = pd.read_csv(RAW / "unctad" / "UNCTAD_US_RCA_India_extract.csv", dtype=str)
rca = rca.assign(Index=pd.to_numeric(rca.Index)).pivot(index="Year", columns="Product", values="Index")
rca.index = rca.index.astype(int)
claim("Slide 4", "RCA, refined petroleum (SITC 334), 1999", "0.06", rca.loc[1999, "334"], "UNCTADstat")
claim("Notes", "RCA, refined petroleum, 2000", "1.26", rca.loc[2000, "334"], "UNCTADstat")
claim("Slide 4", "RCA, refined petroleum, 2025", "4.37", rca.loc[2025, "334"], "UNCTADstat")
fact("Viva notes", "RCA in crude (SITC 333) is about zero", "about 0", rca["333"].loc[1995:2025].max() < 0.05,
     f"max {rca['333'].loc[1995:2025].max():.4f} over 1995-2025", "UNCTADstat")
cy = C.loc[2025]
x9, m9, x10, m10 = (0.0 if pd.isna(cy.get("X_2709")) else cy["X_2709"]), cy["M_2709"], cy["X_2710"], cy["M_2710"]
gl_one = 1 - abs((x9 + x10) - (m9 + m10)) / (x9 + x10 + m9 + m10)
gl_sep = 1 - (abs(x9 - m9) + abs(x10 - m10)) / (x9 + x10 + m9 + m10)
claim("Slide 4", "Grubel-Lloyd, oil as one industry, 2025", "0.55", gl_one, "UN Comtrade, HS 2709 + 2710")
claim("Slide 4", "Grubel-Lloyd, crude and products separately, 2025", "0.10", gl_sep, "UN Comtrade")
uv = (C["X_2710"] / (C["X_2710_kg"] / 1000)) / (C["M_2709"] / (C["M_2709_kg"] / 1000))
for y, q in [(2005, "1.28"), (2015, "1.41"), (2022, "1.40"), (2024, "1.23"), (2025, "1.27")]:
    claim("Backup: refining hedge", f"Refined-export / crude-import unit value, {y}", q, uv[y], "UN Comtrade")
uv_all = uv.dropna()
claim("Backup: refining hedge", "Unit value ratio, lowest year 2000-2025", "1.13", uv_all.min(), "UN Comtrade",
      shown=f"{uv_all.min():.3f} ({uv_all.idxmin()})")
claim("Backup: refining hedge", "Unit value ratio, highest year 2000-2025", "1.41", uv_all.max(), "UN Comtrade",
      shown=f"{uv_all.max():.3f} ({uv_all.idxmax()})")
inside = sorted(uv_all[uv_all <= 1.15].index)
fact("Backup: refining hedge", "Inside the ±15% band only in 2011 and 2012", "every year except 2011 and 2012",
     inside == [2011, 2012], f"years at or below 1.15: {inside}; {len(uv_all)} years with data", "UN Comtrade")
gl1 = C.apply(lambda r: 1 - abs((np.nan_to_num(r.get("X_2709", 0)) + r["X_2710"]) - (r["M_2709"] + r["M_2710"]))
              / (np.nan_to_num(r.get("X_2709", 0)) + r["X_2710"] + r["M_2709"] + r["M_2710"]), axis=1).loc[2010:2025]
gl2 = C.apply(lambda r: 1 - (abs(np.nan_to_num(r.get("X_2709", 0)) - r["M_2709"]) + abs(r["X_2710"] - r["M_2710"]))
              / (np.nan_to_num(r.get("X_2709", 0)) + r["X_2710"] + r["M_2709"] + r["M_2710"]), axis=1).loc[2010:2025]
claim("Notebook 02", "GL as one industry since 2010: lowest", "0.5", gl1.min(), "UN Comtrade", tol=0.02)
claim("Notebook 02", "GL as one industry since 2010: highest", "0.7", gl1.max(), "UN Comtrade", tol=0.03)
claim("Notebook 02", "GL separately since 2010: lowest", "0.04", gl2.min(), "UN Comtrade")
claim("Notebook 02", "GL separately since 2010: highest", "0.12", gl2.max(), "UN Comtrade")

# ---------------------------------------------------------------------------- slide 6: data problems
section("Slide 6: data and the problems we found")
claim("Slide 6", "1978-79 base NTT, FY1999-00 to FY2007-08", "+21.7%", pct(n["1978"][1999], n["1978"][2007]), "RBI Table 121")
claim("Slide 6", "1999-2000 base NTT, same years", "−21.0%", pct(n["1999"][1999], n["1999"][2007]), "RBI Table 121")
dup = t32.loc[1990:1997].values
fact("Slide 6", "Table 32 rows FY1990-97 repeat FY2000-07", "exact copy",
     np.array_equal(dup, t32.loc[2000:2007].values), "all 8 rows x 4 columns identical", "RBI Table 32")
claim("Slide 6", "DGCI&S export quantum index (base 2012-13), monthly minimum", "54", d12.qi_x.min(), "DGCI&S", tol=0.5)
claim("Slide 6", "DGCI&S export quantum index, monthly maximum", "2001", d12.qi_x.max(), "DGCI&S", tol=0.5)
bad = []
for b, df in T121.items():
    calc = 100 * df.ux / df.um
    bound = 0.05 + 100 * (0.05 / df.um + df.ux * 0.05 / df.um ** 2)    # rounding of the three published numbers
    bad += [f"FY{y} ({b} base)" for y in df.index[(calc - df.ntt_pub).abs() > bound]]
fact("Slide 6", "Published RBI NTT values that disagree with RBI's own indices beyond rounding", "three",
     len(bad) == 3, "; ".join(bad), "RBI Table 121")
claim("Slide 6", "Monthly sample length (months with DGCI&S base 2012-13 data)", "87", d12.ntt.loc["2019-04":"2026-06"].count(),
      "DGCI&S", shown=f"{d12.ntt.count()} months, {d12.index.min():%b %Y} to {d12.index.max():%b %Y}")

# ---------------------------------------------------------------------------- H1: ARDL
section("Slides 7-8 and backup: H1 (ARDL)")


def uecm(y, X, p, q):
    """ARDL(p, q...) in error-correction form, by OLS. Returns the fit and the column names."""
    d = pd.DataFrame({"dy": y.diff(), "y_1": y.shift(1)})
    for c in X:
        d[c + "_1"] = X[c].shift(1)
    for j in range(1, p):
        d[f"dy_{j}"] = y.diff().shift(j)
    for c in X:
        for j in range(q[c]):
            d[f"d{c}_{j}"] = X[c].diff().shift(j)
    d = d.dropna()
    return sm.OLS(d["dy"], sm.add_constant(d.drop(columns="dy"))), d


def ardl(ycol, xcols, s, e, maxlag):
    z = np.log(A.loc[s:e, [ycol] + xcols]).dropna().reset_index(drop=True)
    y, X = z[ycol], z[xcols]
    if maxlag > 1:
        sel = ardl_select_order(y, maxlag, X, maxlag, ic="aic", trend="c")
        p = max(sel.model.ardl_order[0], 1)
        q = {c: max(o, 1) for c, o in zip(xcols, sel.model.ardl_order[1:])}
    else:
        p, q = 1, {c: 1 for c in xcols}
    mod, d = uecm(y, X, p, q)
    f = mod.fit()
    al, b = f.params["y_1"], f.params[xcols[0] + "_1"]
    g = np.zeros(len(f.params)); g[list(f.params.index).index(xcols[0] + "_1")] = -1 / al
    g[list(f.params.index).index("y_1")] = b / al ** 2
    lr_se = float(np.sqrt(g @ f.cov_params().values @ g))
    lv = ["y_1"] + [c + "_1" for c in xcols]
    F = float(f.f_test(", ".join(f"{v} = 0" for v in lv)).fvalue)
    return dict(fit=f, sr=f.params[f"d{xcols[0]}_0"], sr_t=f.tvalues[f"d{xcols[0]}_0"], alpha=al,
                alpha_t=f.tvalues["y_1"], lr=-b / al, lr_se=lr_se, F=F, N=int(f.nobs), order=(p, q),
                hc1=mod.fit(cov_type="HC1"), y=y, X=X)


base = ardl("tot", ["real_avg", "real_nonenergy"], 1970, 2024, 2)
f = base["fit"]
fact("Slide 8", "Lag order chosen by AIC (max 2)", "ARDL(1,1,1)", base["order"] == (1, {"real_avg": 1, "real_nonenergy": 1}),
     str(base["order"]), "re-estimated")
claim("Slide 8", "Observations", "54", base["N"], "FY1970-71 to FY2024-25")
claim("Slide 8", "Short-run oil elasticity", "−0.24", base["sr"], "OLS on raw-built series")
claim("Backup: ARDL", "Short-run oil elasticity (3 decimals)", "−0.241", base["sr"], "re-estimated")
claim("Backup: ARDL", "Its standard error", "0.049", f.bse["dreal_avg_0"], "re-estimated")
claim("Backup: ARDL", "Its HC1 robust standard error", "0.040", base["hc1"].bse["dreal_avg_0"], "re-estimated")
fact("Slide 8", "p < 0.001 with robust s.e.", "p < 0.001", base["hc1"].pvalues["dreal_avg_0"] < 0.001,
     f"p = {base['hc1'].pvalues['dreal_avg_0']:.2e}", "re-estimated")
claim("Slide 8", "Error-correction coefficient α", "−0.31", base["alpha"], "re-estimated")
claim("Backup: ARDL", "α (3 decimals) and its s.e.", "−0.308", base["alpha"], "re-estimated")
claim("Backup: ARDL", "s.e. of α", "0.086", f.bse["y_1"], "re-estimated")
claim("Viva notes", "t-statistic of α", "−3.60", base["alpha_t"], "re-estimated")
claim("Slide 8", "Long-run oil elasticity", "−0.09", base["lr"], "re-estimated")
claim("Backup: ARDL", "Long-run elasticity and delta-method s.e.", "0.059", base["lr_se"], "re-estimated")
# the delta-method ratio is judged against the normal distribution, as in our table
lr_p = 2 * (1 - __import__("scipy").stats.norm.cdf(abs(base["lr"] / base["lr_se"])))
claim("Backup: ARDL", "p-value of the long-run elasticity (normal approximation)", "0.119", lr_p, "re-estimated")
lr_nonen = -f.params["real_nonenergy_1"] / base["alpha"]
claim("Backup: ARDL", "Long-run non-energy commodity elasticity", "−0.249", lr_nonen, "re-estimated")
claim("Slide 8", "Bounds F-statistic", "4.74", base["F"], "re-estimated")
lib = UECM(base["y"], 1, base["X"], 1, trend="c").fit().bounds_test(case=3, asymptotic=False, rng=2026)
claim("Slide 8", "Bounds p-value against the I(1) bound (simulated, seed 2026)", "0.07", lib.pvalue["upper"], "statsmodels")
claim("Backup: ARDL", "Bounds p-value against the I(0) bound", "0.025", lib.pvalue["lower"], "statsmodels")
cv = lib.critical_values
claim("Viva notes", "10% upper bound", "4.32", cv.loc[90.0, "upper"], "statsmodels finite-sample")
claim("Viva notes", "5% lower bound", "4.02", cv.loc[95.0, "lower"], "statsmodels finite-sample")
claim("Viva notes", "5% upper bound", "5.13", cv.loc[95.0, "upper"], "statsmodels finite-sample")
ols_f = sm.OLS(f.model.endog, f.model.exog).fit()
claim("Backup: ARDL", "Breusch-Godfrey (2 lags) p", "0.90", acorr_breusch_godfrey(ols_f, nlags=2)[1], "re-estimated")
claim("Backup: ARDL", "Breusch-Pagan p", "0.019", het_breuschpagan(ols_f.resid, ols_f.model.exog)[1], "re-estimated")
claim("Backup: ARDL", "Jarque-Bera p", "0.25", jarque_bera(ols_f.resid)[1], "re-estimated")
claim("Backup: ARDL", "Ramsey RESET p", "0.84", float(linear_reset(ols_f, power=2, use_f=True).pvalue), "re-estimated")
claim("Viva notes", "R-squared", "0.51", f.rsquared, "re-estimated")
claim("Viva notes", "Adjusted R-squared", "0.45", f.rsquared_adj, "re-estimated")
claim("Viva notes", "Half-life of a deviation (years)", "1.9", np.log(0.5) / np.log(1 + base["alpha"]), "derived")
specs = [("Oil only", "tot", ["real_avg"], 1970, 2024, 2, "−0.195"),
         ("Oil + non-oil + gold", "tot", ["real_avg", "real_nonenergy", "real_gold"], 1970, 2024, 2, "−0.217"),
         ("Brent instead of average crude", "tot", ["real_brent", "real_nonenergy"], 1970, 2024, 2, "−0.236"),
         ("Post-1980 sample", "tot", ["real_avg", "real_nonenergy"], 1980, 2024, 2, "−0.211"),
         ("Merchandise ToT, FY1994-2024", "ntt", ["real_avg", "real_nonenergy"], 1994, 2024, 1, "−0.277")]
srs, ts = [base["sr"]], [base["sr_t"]]
for name, yv, xv, s, e, L, q in specs:
    r = ardl(yv, xv, s, e, L)
    srs.append(r["sr"]); ts.append(r["sr_t"])
    claim("Backup: robustness", f"{name}: short-run elasticity", q, r["sr"], "re-estimated")
claim("Slide 8", "Short-run range across the six specifications: smallest (corrected from −0.20)", "−0.19", max(srs), "re-estimated")
claim("Slide 8", "Short-run range across the six specifications: largest", "−0.28", min(srs), "re-estimated")
fact("Slide 8", "Significant in every specification", "all six", max(ts) < -2.6, f"t from {min(ts):.2f} to {max(ts):.2f}",
     "re-estimated")
lt = np.log(A.tot.loc[1970:2025])
tr = sm.OLS(lt.values, sm.add_constant(np.arange(len(lt)))).fit()
claim("Viva notes", "ToT (goods and services), FY1970-71", "110", A.tot[1970], "WDI")
claim("Viva notes", "ToT (goods and services), FY2025-26", "98", A.tot[2025], "WDI")
claim("Viva notes", "p-value of a linear trend in ln ToT", "0.12", tr.pvalues[1], "WDI")
dd = np.log(A.loc[1970:2024, ["real_avg", "real_nonenergy"]]).diff().dropna()
claim("Viva notes", "Correlation of annual oil and non-energy price changes", "0.47", dd.corr().iloc[0, 1], "Pink Sheet")

# ---------------------------------------------------------------------------- slide 9: timing and benchmark
section("Slide 9: timing (local projections) and the benchmark test")


def local_projection(y, shock, H=6):
    d = pd.DataFrame({"y": y, "s": shock})
    d["dy"] = d.y.diff()
    out = []
    for h in range(H + 1):
        z = pd.DataFrame({"lhs": d.y.shift(-h) - d.y.shift(1), "s": d.s, "s_1": d.s.shift(1), "dy_1": d.dy.shift(1)}).dropna()
        r = sm.OLS(z.lhs, sm.add_constant(z[["s", "s_1", "dy_1"]])).fit(cov_type="HAC", cov_kwds={"maxlags": h + 1})
        out.append((r.params["s"], r.bse["s"], int(r.nobs)))
    return pd.DataFrame(out, columns=["beta", "se", "N"])


mm = pd.DataFrame({"y": 100 * np.log(d12.ntt)}).reindex(pk.loc["2019-01":"2026-06"].index)
mm["dlp"] = 100 * np.log(pk.brent).diff().loc["2019-01":"2026-06"]
mm = mm.dropna(subset=["dlp"])
lp = local_projection(mm.y, mm.dlp)
claim("Slide 9", "Response at 2 months", "−0.39", lp.beta[2], "re-estimated")
claim("Viva notes", "Response at 0 months", "−0.02", lp.beta[0], "re-estimated")
claim("Viva notes", "Response at 1 month", "−0.23", lp.beta[1], "re-estimated")
claim("Viva notes", "Response at 3 months", "−0.37", lp.beta[3], "re-estimated")
claim("Viva notes", "Response at 6 months", "−0.37", lp.beta[6], "re-estimated")
claim("Viva notes", "s.e. at 2 months", "0.13", lp.se[2], "re-estimated")
claim("Viva notes", "s.e. at 3 months", "0.08", lp.se[3], "re-estimated")
fact("Viva notes", "Significant (90%) at every horizon from 1 to 6 months", "1 to 6 months",
     (lp.beta[1:] / lp.se[1:] < -1.645).all(), "t: " + ", ".join(f"{t:.1f}" for t in lp.beta[1:] / lp.se[1:]), "re-estimated")
claim("Viva notes", "Observations at horizon 0", "85", lp.N[0], "re-estimated")
b = A.loc[1994:2024].copy()
b["dntt"], b["doil"], b["dnon"] = np.log(b.ntt).diff(), np.log(b.real_avg).diff(), np.log(b.real_nonenergy).diff()
b["bx"] = b.bench.shift(1) * b.doil
bt = ols(b.dntt, b[["bx", "dnon"]], "HAC", maxlags=1)
claim("Slide 9", "Benchmark-test coefficient (theory: 1)", "1.70", bt.params["bx"], "re-estimated")
claim("Viva notes", "Its HAC s.e.", "0.38", bt.bse["bx"], "re-estimated")
claim("Slide 9", "p-value for coefficient = 1", "0.07", float(bt.t_test("bx = 1").pvalue), "re-estimated")
claim("Viva notes", "Observations", "30", bt.nobs, "FY1995-96 to FY2024-25")
pe = ols(b.dntt, b[["doil", "dnon"]], "HAC", maxlags=1)
claim("Viva notes", "Plain merchandise oil elasticity, same years", "−0.30", pe.params["doil"], "re-estimated")
claim("Viva notes", "Average benchmark over the same years", "−0.16", b.bench.loc[1994:2024].mean(), "RBI Table 111")
claim("Slide 9", "Export unit values, Feb to Apr 2026", "+18%", pct(m26(d12.uvi_x, "2026-02"), m26(d12.uvi_x, "2026-04")), "DGCI&S")
claim("Viva notes", "Export unit values, Feb to Apr 2026 (one decimal)", "+18.1%", pct(m26(d12.uvi_x, "2026-02"), m26(d12.uvi_x, "2026-04")), "DGCI&S")
claim("Slide 9", "Import unit values, Feb to Apr 2026", "+16%", pct(m26(d12.uvi_m, "2026-02"), m26(d12.uvi_m, "2026-04")), "DGCI&S")
claim("Viva notes", "Import unit values, Feb to Apr 2026 (one decimal)", "+15.7%", pct(m26(d12.uvi_m, "2026-02"), m26(d12.uvi_m, "2026-04")), "DGCI&S")
claim("Viva notes", "Import unit values, Feb to Jun 2026", "+20%", pct(m26(d12.uvi_m, "2026-02"), m26(d12.uvi_m, "2026-06")), "DGCI&S")

# ---------------------------------------------------------------------------- slide 10: H2 and exposure
section("Slide 10 and backup: H2 (NARDL) and the rolling elasticity")


def nardl(ycol, xcol, s, e, control=True, extra=False):
    z = np.log(A.loc[s:e, [ycol, xcol, "real_nonenergy"]])
    dx = z[xcol].diff().fillna(0)
    d = pd.DataFrame({"dy": z[ycol].diff(), "y_1": z[ycol].shift(1),
                      "xp_1": dx.clip(lower=0).cumsum().shift(1), "xn_1": dx.clip(upper=0).cumsum().shift(1),
                      "dxp": dx.clip(lower=0).cumsum().diff(), "dxn": dx.clip(upper=0).cumsum().diff()})
    if control:
        d["z_1"], d["dz"] = z.real_nonenergy.shift(1), z.real_nonenergy.diff()
    if extra:
        d["dy_1"] = d.dy.shift(1)
    d = d.dropna()
    r = sm.OLS(d.dy, sm.add_constant(d.drop(columns="dy"))).fit()
    al = r.params["y_1"]
    return dict(Lp=-r.params["xp_1"] / al, Ln=-r.params["xn_1"] / al, Sp=r.params["dxp"], Sn=r.params["dxn"],
                pL=float(r.f_test("xp_1 = xn_1").pvalue), pS=float(r.f_test("dxp = dxn").pvalue), N=int(r.nobs))


nb = nardl("tot", "real_avg", 1970, 2024)
claim("Slide 10", "Short-run effect of a rise", "−0.27", nb["Sp"], "re-estimated")
claim("Slide 10", "Short-run effect of a fall", "−0.22", nb["Sn"], "re-estimated")
claim("Viva notes", "Short-run symmetry p (baseline)", "0.62", nb["pS"], "re-estimated")
claim("Viva notes", "Long-run effect of a rise (baseline)", "−0.16", nb["Lp"], "re-estimated")
claim("Viva notes", "Long-run effect of a fall (baseline)", "−0.23", nb["Ln"], "re-estimated")
claim("Viva notes", "Long-run symmetry p (baseline)", "0.035", nb["pL"], "re-estimated")
cases = [("No control", "tot", "real_avg", 1970, False, False), ("Brent", "tot", "real_brent", 1970, True, False),
         ("Extra lag of ΔToT", "tot", "real_avg", 1970, True, True), ("FY1975-2024", "tot", "real_avg", 1975, True, False),
         ("FY1980-2024", "tot", "real_avg", 1980, True, False), ("Merchandise", "ntt", "real_avg", 1994, True, False)]
res = {c[0]: nardl(c[1], c[2], c[3], 2024, c[4], c[5]) for c in cases}
pS = [nb["pS"]] + [r["pS"] for r in res.values()]
claim("Slide 10", "Short-run symmetry p, smallest of seven specifications", "0.54", min(pS), "re-estimated")
claim("Slide 10", "Short-run symmetry p, largest", "0.91", max(pS), "re-estimated")
claim("Slide 10", "Long-run symmetry p from FY1980", "0.28", res["FY1980-2024"]["pL"], "re-estimated")
claim("Viva notes", "Long-run symmetry p with an extra lag", "0.05", res["Extra lag of ΔToT"]["pL"], "re-estimated")
claim("Viva notes", "Long-run symmetry p from FY1975", "0.08", res["FY1975-2024"]["pL"], "re-estimated")
fact("Viva notes", "Merchandise: long-run asymmetry reversed, not significant", "reversed",
     res["Merchandise"]["Lp"] < res["Merchandise"]["Ln"] and res["Merchandise"]["pL"] > 0.1,
     f"rise {res['Merchandise']['Lp']:.3f}, fall {res['Merchandise']['Ln']:.3f}, p = {res['Merchandise']['pL']:.2f}",
     "re-estimated")
rr = np.log(A.loc[1970:2024, ["tot", "real_avg", "real_nonenergy"]]).diff().dropna()
roll = {}
for end in range(1989, 2025):
    w = rr.loc[end - 19:end]
    r = sm.OLS(w.tot, sm.add_constant(w[["real_avg", "real_nonenergy"]])).fit(cov_type="HC1")
    roll[end] = (r.params["real_avg"], r.bse["real_avg"])
claim("Slide 10", "Rolling elasticity, window ending FY1989", "−0.30", roll[1989][0], "re-estimated")
claim("Slide 10", "Rolling elasticity, window ending FY2024", "−0.11", roll[2024][0], "re-estimated")
claim("Viva notes", "Its s.e., first window", "0.09", roll[1989][1], "re-estimated")
claim("Viva notes", "Its s.e., last window", "0.06", roll[2024][1], "re-estimated")
claim("Viva notes", "Rolling elasticity, window ending FY2015", "−0.16", roll[2015][0], "re-estimated")
recent = [roll[y][0] for y in range(2019, 2025)]
claim("Notebook 05", "Most recent windows (ending FY2019-24): smallest effect", "−0.10", max(recent), "re-estimated")
claim("Notebook 05", "Most recent windows: largest effect", "−0.15", min(recent), "re-estimated")

# ---------------------------------------------------------------------------- slide 11: H3
section("Slide 11 and backup: H3 (supply- vs demand-driven oil prices)")
s = pd.DataFrame({"dlp": 100 * np.log(pk.avg).diff()}).join(bh).loc["1975-02":"2026-03"]
cols = ["supply", "activity", "consumption", "inventory"]
for c in cols:
    for j in (1, 2):
        s[f"{c}_{j}"] = s[c].shift(j)
rhs = cols + [f"{c}_{j}" for c in cols for j in (1, 2)]
st1 = sm.OLS(s.dlp, sm.add_constant(s[rhs]), missing="drop").fit()
claim("Viva notes", "First step: R-squared", "0.80", st1.rsquared, "re-estimated")
claim("Viva notes", "First step: months", "612", st1.nobs, "Feb 1975 to Mar 2026, less two lags")
P = st1.params
s["sup"] = sum(P[c] * s[c] for c in P.index if c.startswith("supply"))
s["dem"] = sum(P[c] * s[c] for c in P.index if c != "const" and not c.startswith("supply"))
fyp = s[["sup", "dem"]].groupby(s.index.map(fy_of)).sum(min_count=12).dropna()
yy = pd.DataFrame({"g": 100 * np.log(A.tot).diff(), "mx": 100 * np.log(A.ntt).diff()})
zz = fyp.join(yy, how="inner").loc[1975:2025]
r_g = ols(zz.g, zz[["sup", "dem"]], "HAC", maxlags=1)
r_x = ols(zz.mx, zz[["sup", "dem"]], "HAC", maxlags=1)
mo = pd.DataFrame({"dn": 100 * np.log(d12.ntt).diff()}).join(s[["sup", "dem"]]).loc["2019-04":"2026-06"]
for v in ("sup", "dem"):
    for j in (1, 2):
        mo[f"{v}_{j}"] = mo[v].shift(j)
r_m = ols(mo.dn, mo[["sup", "sup_1", "sup_2", "dem", "dem_1", "dem_2"]], "HAC", maxlags=3)
cs = r_m.t_test("sup + sup_1 + sup_2 = 0"); cd = r_m.t_test("dem + dem_1 + dem_2 = 0")
p_m = float(r_m.t_test("sup + sup_1 + sup_2 - dem - dem_1 - dem_2 = 0").pvalue)
claim("Backup: H3", "Annual G&S: supply-driven effect", "−0.068", r_g.params["sup"], "re-estimated")
claim("Backup: H3", "Annual G&S: demand-driven effect", "−0.106", r_g.params["dem"], "re-estimated")
claim("Backup: H3", "Annual G&S: p (equal)", "0.707", float(r_g.t_test("sup = dem").pvalue), "re-estimated")
claim("Backup: H3", "Annual merchandise: supply-driven", "−0.027", r_x.params["sup"], "re-estimated")
claim("Backup: H3", "Annual merchandise: demand-driven", "−0.130", r_x.params["dem"], "re-estimated")
claim("Backup: H3", "Annual merchandise: p (equal)", "0.547", float(r_x.t_test("sup = dem").pvalue), "re-estimated")
claim("Backup: H3", "Monthly, 3-month cumulative: supply-driven", "−0.242", float(cs.effect[0]), "re-estimated")
claim("Backup: H3", "Monthly, 3-month cumulative: demand-driven", "−0.373", float(cd.effect[0]), "re-estimated")
claim("Backup: H3", "Monthly: p (equal)", "0.535", p_m, "re-estimated")
pe3 = [float(r_g.t_test("sup = dem").pvalue), float(r_x.t_test("sup = dem").pvalue), p_m]
claim("Slide 11", "p (supply = demand), smallest of three samples (corrected from 0.54)", "0.53", min(pe3), "re-estimated")
claim("Slide 11", "p (supply = demand), largest", "0.71", max(pe3), "re-estimated")
# Känzig: is one unit of the news shock about a 10% oil price rise on impact?
kk = pd.DataFrame({"dlp": 100 * np.log(pk.avg).diff(), "k": kanzig}).loc["1975-01":"2025-12"].dropna()
imp = sm.OLS(kk.dlp, sm.add_constant(kk.k)).fit()
claim("Slide 11", "Oil price response to one Känzig news shock, same month (%)", "+10%", imp.params["k"], "Känzig series, Pink Sheet",
      tol=2.5)
ka = kanzig.loc["1975-01":"2025-12"].groupby(kanzig.loc["1975-01":"2025-12"].index.map(fy_of)).sum(min_count=12)
ka = pd.DataFrame({"k": ka}).join(yy.g).loc[1975:2024].dropna()
rk = ols(ka.g, ka[["k"]], "HAC", maxlags=1)
claim("Backup: H3", "Annual ToT response per Känzig shock (%)", "−0.95", rk.params["k"], "re-estimated")
claim("Backup: H3", "Its s.e.", "0.49", rk.bse["k"], "re-estimated")
mk = pd.DataFrame({"y": 100 * np.log(d12.ntt), "k": kanzig}).loc["2019-04":"2025-12"]
lpk = local_projection(mk.y, mk.k)
claim("Backup: H3", "Monthly ToT response to a Känzig shock, 2 months (%)", "−4.2", lpk.beta[2], "re-estimated")
claim("Backup: H3", "Monthly ToT response to a Känzig shock, 3 months (%)", "−4.7", lpk.beta[3], "re-estimated")
claim("Notebook 06", "Its t-statistic at 2 months", "−2.0", lpk.beta[2] / lpk.se[2], "re-estimated")
claim("Notebook 06", "Its t-statistic at 3 months", "−2.7", lpk.beta[3] / lpk.se[3], "re-estimated")
claim("Notebook 06", "March 2026 oil price change (100 x log)", "34", s.dlp.loc["2026-03"].iloc[0], "Pink Sheet", tol=0.5)
claim("Notebook 06", "March 2026: supply-driven part", "36", s.sup.loc["2026-03"].iloc[0], "re-estimated", tol=0.5)
fact("Notebook 06", "Feb 2022 rise mainly demand-driven; March 2022 has a supply part", "mainly demand",
     s.dem.loc["2022-02"].iloc[0] > s.sup.loc["2022-02"].iloc[0] and s.sup.loc["2022-03"].iloc[0] > 2,
     f"Feb: demand {s.dem.loc['2022-02'].iloc[0]:.1f}, supply {s.sup.loc['2022-02'].iloc[0]:.1f}; "
     f"Mar: demand {s.dem.loc['2022-03'].iloc[0]:.1f}, supply {s.sup.loc['2022-03'].iloc[0]:.1f}", "re-estimated")

# ---------------------------------------------------------------------------- backup: episodes and unit roots
section("Backup: oil episodes (fiscal-year averages)")
for name, a0, a1, q in [("1973 OPEC embargo", 1972, 1974, ("+284.1%", "−38.6%", None)),
                        ("1979 Iranian revolution", 1978, 1980, ("+110.2%", "−19.2%", None)),
                        ("1990 Gulf war", 1989, 1990, ("+21.1%", "−9.8%", None)),
                        ("2008 price spike", 2006, 2008, ("+19.9%", "+4.9%", "+5.8%")),
                        ("2014-16 collapse", 2013, 2015, ("−49.9%", "−1.0%", "+19.4%")),
                        ("2020 COVID crash", 2019, 2020, ("−26.4%", "+4.7%", "+9.6%")),
                        ("2022 Russia-Ukraine", 2020, 2022, ("+82.8%", "−14.4%", "−23.7%"))]:
    claim("Backup: episodes", f"{name}: real oil price", q[0], pct(A.real_avg[a0], A.real_avg[a1]), "Pink Sheet / MUV")
    claim("Backup: episodes", f"{name}: ToT goods and services", q[1], pct(A.tot[a0], A.tot[a1]), "WDI")
    if q[2]:
        claim("Backup: episodes", f"{name}: ToT merchandise", q[2], pct(A.ntt[a0], A.ntt[a1]), "RBI Table 121")
yr08 = pk.brent.loc["2008"]
fact("Viva notes", "2008: oil peaked in July and collapsed by December", "July peak, December low",
     yr08.idxmax().month == 7 and yr08.idxmin().month == 12,
     f"peak {yr08.max():.1f} ({yr08.idxmax():%b}), December {yr08.loc['2008-12'].iloc[0]:.1f}", "Pink Sheet")

section("Backup: unit-root tests (p-values)")
series = {"ln ToT goods & services": np.log(A.tot.loc[1970:2024]),
          "ln ToT merchandise": np.log(A.ntt.loc[1994:2024]),
          "ln real oil price": np.log(A.real_avg.loc[1970:2024]),
          "ln real non-energy prices": np.log(A.real_nonenergy.loc[1970:2024]),
          "ln real gold price": np.log(A.real_gold.loc[1970:2024])}
quoted_ur = {"ln ToT goods & services": ("0.057", "0.050", "0.100", "0.391"),
             "ln ToT merchandise": ("0.271", "0.392", "0.010", "0.062"),
             "ln real oil price": ("0.053", "0.050", "0.013", "0.533"),
             "ln real non-energy prices": ("0.355", "0.395", "0.100", "0.911"),
             "ln real gold price": ("0.945", "0.582", "0.010", "0.942")}
for k, sr in series.items():
    sr = sr.dropna()
    q = quoted_ur[k]
    claim("Backup: unit roots", f"{k}: ADF level p", q[0], adfuller(sr, autolag="AIC")[1], "re-tested")
    claim("Backup: unit roots", f"{k}: Phillips-Perron level p", q[1], PhillipsPerron(sr).pvalue, "re-tested")
    claim("Backup: unit roots", f"{k}: KPSS level p", q[2], kpss(sr, regression="c", nlags="auto")[1], "re-tested")
    claim("Backup: unit roots", f"{k}: Zivot-Andrews p", q[3], ZivotAndrews(sr, trend="c").pvalue, "re-tested")
    fact("Backup: unit roots", f"{k}: stationary in first differences (ADF)", "p ≈ 0.000",
         adfuller(sr.diff().dropna(), autolag="AIC")[1] < 0.01, f"p = {adfuller(sr.diff().dropna(), autolag='AIC')[1]:.4f}",
         "re-tested")

# ---------------------------------------------------------------------------- other numbers in the notes
section("Other numbers in the speaker notes and viva notes")
x = np.log(pd.DataFrame({"vol": t32.loc[1998:2025, 3], "bill": A.m_oil.loc[1998:2025], "p": A.avg.loc[1998:2025]})).diff().dropna()
iv = ols(x.vol, x[["p"]], "HAC", maxlags=1)
claim("Viva notes", "Crude import volume elasticity to the oil price", "0.16", iv.params["p"], "RBI Tables 32, 111")
claim("Viva notes", "Its s.e.", "0.09", iv.bse["p"], "re-estimated")
claim("Viva notes", "Correlation of oil import bill and oil price changes", "0.96", x.bill.corr(x.p), "RBI Table 111, Pink Sheet")
noi = 100 * (A.m_oil - A.x_oil) * 1e6 / A.gdp_usd
claim("Viva notes", "Net oil imports, % of GDP, FY2025-26", "3.0%", noi[2025], "RBI Table 111, WDI")
claim("Viva notes", "Net oil imports, % of GDP, peak", "5.6%", noi.max(), "RBI Table 111, WDI",
      shown=f"{noi.max():.2f}% (FY{noi.idxmax()})")
fact("Viva notes", "The peak year is FY2012-13", "FY2012", noi.idxmax() == 2012, f"FY{noi.idxmax()}", "RBI Table 111, WDI")
mon = d12.ntt.loc["2019-04":"2026-06"]
claim("Viva notes", "Monthly merchandise NTT: mean", "111.9", mon.mean(), "DGCI&S")
claim("Viva notes", "Monthly merchandise NTT: high (May 2020)", "163.2", mon.max(), "DGCI&S", shown=f"{mon.max():.3f} ({mon.idxmax():%b %Y})")
claim("Viva notes", "Monthly merchandise NTT: low (Jun 2022)", "89.4", mon.min(), "DGCI&S", shown=f"{mon.min():.3f} ({mon.idxmin():%b %Y})")
br = pk.brent.loc["2019-04":"2026-06"]
claim("Viva notes", "Brent Apr 2019-Jun 2026: mean", "$74", br.mean(), "Pink Sheet")
claim("Viva notes", "Brent: low (Apr 2020)", "$23", br.min(), "Pink Sheet", shown=f"{br.min():.1f} ({br.idxmin():%b %Y})")
claim("Viva notes", "Brent: high (Apr 2026)", "$120", br.max(), "Pink Sheet", shown=f"{br.max():.1f} ({br.idxmax():%b %Y})")
fred = pd.read_csv(RAW / "fred" / "DCOILBRENTEU.csv", na_values=".")
fred = fred.set_index(pd.to_datetime(fred.iloc[:, 0])).iloc[:, 1].resample("MS").mean()
j = pd.DataFrame({"wb": pk.brent, "fred": fred}).loc["1990":].dropna()
claim("Viva notes", "World Bank vs FRED Brent: correlation (logs)", "0.9998", np.corrcoef(np.log(j.wb), np.log(j.fred))[0, 1], "Pink Sheet, FRED")
claim("Viva notes", "Mean absolute difference (US$/bbl)", "0.33", (j.wb - j.fred).abs().mean(), "Pink Sheet, FRED")
claim("Viva notes", "Months compared", "441", len(j), "Pink Sheet, FRED")
ji = pd.DataFrame({"icb": icb, "b": pk.brent, "d": pk.dubai}).dropna().loc[:"2026-02"]
inside = ((ji.icb >= ji[["b", "d"]].min(axis=1) - 1.5) & (ji.icb <= ji[["b", "d"]].max(axis=1) + 1.5)).mean()
claim("Viva notes", "PPAC basket within the Dubai-Brent range (±$1.5), Apr 2020-Feb 2026", "95%", 100 * inside, "PPAC, Pink Sheet", tol=1)
ct = (C["M_2709_kg"] / 1e9).dropna()
ratio = (ct / t32[3]).dropna()
fact("Viva notes", "Comtrade (calendar year) vs RBI (fiscal year) crude import tonnes", "within ±9%",
     (ratio.sub(1).abs() <= 0.095).all(), f"ratio {ratio.min():.3f} to {ratio.max():.3f} over {len(ratio)} years",
     "UN Comtrade, RBI Table 32")
claim("Q&A G12", "Oil share of imports, FY2025-26", "22%", 100 * A.s_m[2025], "RBI Table 111")
sv, gs = wdi("BX.GSR.NFSV.CD"), wdi("BX.GSR.GNFS.CD")
claim("Q&A D4", "Services share of India's exports, 1990", "20%", 100 * sv[1990] / gs[1990], "WDI (BoP)", tol=1)
claim("Q&A D4", "Services share of India's exports, 2024 (\"almost half\")", "46%", 100 * sv[2024] / gs[2024], "WDI (BoP)", tol=1)
t115 = rbi("HBS2026_T115_Imports_Major_Commodities_USD.html")
labels = t115[0].astype(str)
last = t115.iloc[:, -1]
items = {l: float(v) for l, v in zip(labels, last) if re.match(r"\d+\. ", l) and "Other" not in l}
top = max(items, key=items.get)
fact("Speaker notes", "Oil is the largest single item in India's import bill", "largest item",
     "Petroleum" in top, f"FY2025-26: {top.split('. ')[1]} US${items[top] / 1000:.1f} bn; next "
     + ", ".join(f"{k.split('. ')[1]} {v / 1000:.1f}" for k, v in sorted(items.items(), key=lambda kv: -kv[1])[1:3]),
     "RBI Table 115")

# ============================================================================ report
EXTERNAL = (ROOT / "docs" / "number_check_external.md").read_text(encoding="utf-8")
lines = ["# Number check", "",
         "Every number we quote in the slides, the speaker notes and the viva notes, recomputed from the raw files.",
         "", "`src/check_numbers.py` does this without using our own pipeline: it parses `data/raw/` again, rebuilds",
         "the series, re-estimates every model with plain OLS and compares each result with the number as we write it",
         "(so \"−0.24\" passes if the recomputed value rounds to −0.24). Run it again after any change.", ""]
ok = sum(c[-1] for c in CLAIMS)
lines += [f"**{ok} of {len(CLAIMS)} checks pass.**", ""]
if ok < len(CLAIMS):
    lines += ["Checks that fail:", ""] + [f"- {c[1]}: {c[2]} (we say {c[3]}, data give {c[4]})" for c in CLAIMS if not c[-1]] + [""]
lines += ["Facts that come from outside our dataset (events, institutions, papers) are checked by hand at the end of",
          "this page, with links to the original sources.", ""]
current = None
for sec, where, what, quoted, shown, src, good in CLAIMS:
    if sec != current:
        lines += ["", f"## {sec}", "", "| | Where | What | We say | Recomputed | Source |", "|---|---|---|---|---|---|"]
        current = sec
    lines.append(f"| {'✓' if good else '✗'} | {where} | {what} | {quoted} | {shown} | {src} |")
lines += ["", EXTERNAL]
(ROOT / "docs" / "number_check.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{ok} of {len(CLAIMS)} checks pass")
for c in CLAIMS:
    if not c[-1]:
        print("FAIL:", c[1], "|", c[2], "| quoted", c[3], "| got", c[4])

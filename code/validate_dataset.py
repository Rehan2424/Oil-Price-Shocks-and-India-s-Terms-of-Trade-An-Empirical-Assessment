"""
Automatic data checks. Writes data/validation_report.md and exits with an error if a hard check fails.
Run from the repository root:  python code/validate_dataset.py
"""
from pathlib import Path
import glob
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_dataset as B  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"
m = pd.read_csv(P / "monthly.csv", parse_dates=["date"])
a = pd.read_csv(P / "annual_fy.csv")
c = pd.read_csv(P / "annual_cy.csv")

lines, failures = [], []


def check(name, ok, detail, hard=True):
    status = "PASS" if ok else ("FAIL" if hard else "NOTE")
    lines.append(f"| {status} | {name} | {detail} |")
    if hard and not ok:
        failures.append(name)


def note(name, detail):
    lines.append(f"| NOTE | {name} | {detail} |")


# 1. DGCI&S: recomputed NTT equals published NTT
for b in ("b12", "b22"):
    d = m.dropna(subset=[f"ntt_pub_{b}"])
    diff = (d[f"ntt_{b}"] - d[f"ntt_pub_{b}"]).abs().max()
    check(f"DGCI&S {b}: NTT = 100*UVI_x/UVI_m", diff < 0.01,
          f"{len(d)} months ({d.date.min():%Y-%m} to {d.date.max():%Y-%m}); max |diff| = {diff:.4f}")

# 2. DGCI&S fiscal-year UVI (from the FY files) vs RBI Handbook Table 121 (2012-13 base)
fis = []
for f in sorted(glob.glob(str(B.RAW / "dgcis" / "base2012-13" / "*FY*.xlsx"))):
    df = pd.read_excel(f, header=None)
    lab = df[1].map(B._norm)
    r_hdr = lab[lab.str.startswith("grand total indices")].index[0]
    rx = lab[lab.str.startswith("export grand total")].index[0]
    rm = lab[lab.str.startswith("import grand total")].index[0]
    for col in range(df.shape[1]):
        h = str(df.iat[r_hdr, col])
        mm = re.match(r"Fiscal\s*(\d{2})-(\d{2})", h)
        if mm:
            fis.append({"fy": 2000 + int(mm.group(1)), "uvi_x_dgcis": df.iat[rx, col], "uvi_m_dgcis": df.iat[rm, col]})
fis = pd.DataFrame(fis).merge(a[["fy", "uvi_x_rbi_2012", "uvi_m_rbi_2012"]], on="fy")
dx = (fis["uvi_x_dgcis"] - fis["uvi_x_rbi_2012"]).abs().max()
dm = (fis["uvi_m_dgcis"] - fis["uvi_m_rbi_2012"]).abs().max()
check("DGCI&S fiscal-year UVIs = RBI Table 121 (2012-13 base)", max(dx, dm) < 0.11,
      f"FY{fis.fy.min()}-{fis.fy.max()}; max |diff| exports {dx:.3f}, imports {dm:.3f} (RBI rounds to 1 decimal)")

# 3. RBI Table 121 internal consistency
t = B.rbi_t121()
# published UVIs are rounded; the NTT implied by any unrounded values must lie in [lo, hi]
step = t[["uvi_x", "uvi_m"]].apply(lambda s: 0.5 if (s % 1 == 0).all() else 0.05)
t["lo"] = 100 * (t.uvi_x - step.uvi_x) / (t.uvi_m + step.uvi_m) - 0.05
t["hi"] = 100 * (t.uvi_x + step.uvi_x) / (t.uvi_m - step.uvi_m) + 0.05
bad = t[(t.ntt < t.lo) | (t.ntt > t.hi)]
check("RBI Table 121: published NTT consistent with published UVIs (allowing for rounding)", len(bad) <= 3,
      f"{len(t) - len(bad)} of {len(t)} rows consistent. Inconsistent beyond rounding: "
      + "; ".join(f"FY{r.fy}-{str(r.fy + 1)[-2:]} ({r.base} base) published {r.ntt:.1f} vs "
                  f"{100 * r.uvi_x / r.uvi_m:.2f} from UVIs" for r in bad.itertuples())
      + ". We therefore recompute NTT from the UVIs.")

# 4. World Bank Brent vs FRED Brent (EIA daily, averaged by month)
fred = pd.read_csv(B.RAW / "fred" / "DCOILBRENTEU.csv")
fred["DCOILBRENTEU"] = pd.to_numeric(fred["DCOILBRENTEU"], errors="coerce")
fred["date"] = pd.to_datetime(fred["observation_date"]).dt.to_period("M").dt.to_timestamp()
fm = fred.groupby("date")["DCOILBRENTEU"].mean().rename("brent_fred").reset_index()
j = m[["date", "brent"]].merge(fm, on="date").dropna()
j = j[j.date >= "1990-01-01"]
mad = (j.brent - j.brent_fred).abs().mean()
corr = np.corrcoef(np.log(j.brent), np.log(j.brent_fred))[0, 1]
check("Brent: World Bank Pink Sheet vs FRED (EIA)", corr > 0.999 and mad < 1.0,
      f"{len(j)} months since 1990; corr(log) = {corr:.5f}; mean |diff| = ${mad:.2f}/bbl")

# 5. PPAC Indian basket vs World Bank Brent and Dubai
j = m.dropna(subset=["icb_ppac", "brent", "dubai"])
normal = j[j.date < "2026-03-01"]
inside = ((normal.icb_ppac >= normal[["brent", "dubai"]].min(axis=1) - 1.5) &
          (normal.icb_ppac <= normal[["brent", "dubai"]].max(axis=1) + 1.5)).mean()
check("PPAC Indian basket lies between WB Dubai and Brent (+/-$1.5), Apr 2020-Feb 2026", inside > 0.9,
      f"{inside:.0%} of {len(normal)} months; the basket uses Oman/Dubai average, not WB Dubai alone")
war = j[j.date >= "2026-03-01"][["date", "icb_ppac", "brent", "dubai"]]
note("PPAC basket during the 2026 Hormuz crisis",
     "; ".join(f"{r.date:%Y-%m}: ICB {r.icb_ppac:.1f}, Brent {r.brent:.1f}, Dubai {r.dubai:.1f}" for r in war.itertuples())
     + ". Sour Gulf grades (Oman) spiked, so the basket sits outside the WB Brent-Dubai range in Mar 2026.")
note("PPAC data gap", "PPAC website serves an April-2023 provisional file under FY2022-23, so the basket is "
     "missing for Apr 2022-Mar 2023 (file kept in data/raw/ppac with a descriptive name; not used).")

# 6. WDI and UNCTAD merchandise ToT are the same series
j = c.dropna(subset=["ntt_wdi", "ntt_unctad"])
check("WDI NBTT = UNCTAD terms-of-trade index", (j.ntt_wdi - j.ntt_unctad).abs().max() < 0.06,
      f"{len(j)} years; max |diff| = {(j.ntt_wdi - j.ntt_unctad).abs().max():.3f}")

# 7. Agreement between ToT measures (growth rates)
g = a[["fy", "tot_gs_na", "ntt_rbi_chained"]].dropna()
r1 = np.corrcoef(np.diff(np.log(g.tot_gs_na)), np.diff(np.log(g.ntt_rbi_chained)))[0, 1]
note("National-accounts ToT (goods+services) vs merchandise NTT (chained RBI)",
     f"corr of annual log changes = {r1:.2f} over FY{g.fy.min()}-{g.fy.max()} (services prices dilute the oil effect)")
mm = m.dropna(subset=["ntt_b12"]).copy()
mm["year"] = mm.date.dt.year
cy = mm.groupby("year").agg(n=("ntt_b12", "size"), ntt=("ntt_b12", "mean")).query("n == 12")
cy = cy.join(c.set_index("year")["ntt_unctad"]).dropna()
r2 = np.corrcoef(np.diff(np.log(cy.ntt)), np.diff(np.log(cy.ntt_unctad)))[0, 1] if len(cy) > 3 else np.nan
note("DGCI&S monthly NTT (CY average) vs UNCTAD NTT", f"corr of log changes = {r2:.2f}, {len(cy)} years")

# 8. Oil shares: RBI Table 111 vs Table 115
t115 = B._rbi_table("HBS2026_T115_Imports_Major_Commodities_USD.html")
row = t115[t115[0].astype(str).str.contains("Petroleum, Crude")].iloc[0]
yrs = [int(str(v)[:4]) for v in t115.iloc[1, 1:].tolist()]
diffs = []
for y, v in zip(yrs, row.tolist()[1:]):
    t111 = a.loc[a.fy == y, "m_oil_usdm"]
    if len(t111):
        diffs.append(abs(float(v) - float(t111.iloc[0])))
check("Oil imports: RBI Table 111 = Table 115 (Petroleum, crude & products)", max(diffs) < 1.0,
      f"{len(diffs)} years; max |diff| = US${max(diffs):.1f} mn")

# 9. Crude import volumes: UN Comtrade (CY, kg) vs RBI Table 32 (FY, MMT)
j = c[["year", "m_2709_kg"]].dropna().merge(a[["fy", "crude_imp_mmt"]], left_on="year", right_on="fy")
ratio = (j.m_2709_kg / 1e9) / j.crude_imp_mmt
check("Crude import tonnes: Comtrade (CY) vs RBI Table 32 (FY)", ratio.between(0.85, 1.15).mean() > 0.9,
      f"{len(j)} years; ratio range {ratio.min():.2f}-{ratio.max():.2f} (CY vs FY timing)")

# 10. WDI national-accounts year label = Indian fiscal year
t4 = B._rbi_table("HBS2026_T4_Components_of_GDP.html")
gdp_row = t4[t4[0].astype(str).str.startswith("Gross Domestic")].iloc[0].tolist()
labels = t4.iloc[2].tolist()
bases = t4.iloc[4].tolist()
wdi_gdp = B.wdi("NY.GDP.MKTP.CN")
ok = []
for lab_, base_, v in zip(labels[1:], bases[1:], gdp_row[1:]):
    if "2022" in str(base_) and str(lab_)[:4].isdigit() and int(str(lab_)[:4]) in (2022, 2023, 2024):
        y = int(str(lab_)[:4])
        ok.append(abs(wdi_gdp[y] / 1e7 - float(v)) < 1)
check("WDI India GDP year t = RBI FY t/t+1 (new 2022-23 base)", all(ok) and len(ok) == 3,
      "WDI 2022, 2023, 2024 equal RBI Table 4 FY2022-23, 2023-24, 2024-25 (Rs crore)")

# 11. Known artefacts / exclusions
q = m[["qi_x_b12"]].dropna()
note("DGCI&S export quantum index (2012-13 base) not used",
     f"monthly QI ranges {q.qi_x_b12.min():.0f}-{q.qi_x_b12.max():.0f}; this is why RBI Table 121 shows QI=473.6 "
     "and GTT=38.2 for 2025-26. Only unit value indices and NTT are used.")
note("WDI goods & services deflators 1960-69", "ratio frozen at 1.18413 (WDI back-cast with a common deflator); "
     "tot_gs_na starts in FY1970-71.")
ov = a.set_index("fy")
g78 = ov.loc[2007, "ntt_rbi_1978"] / ov.loc[1999, "ntt_rbi_1978"] - 1
g99 = ov.loc[2007, "ntt_rbi_1999"] / ov.loc[1999, "ntt_rbi_1999"] - 1
note("RBI base-year series disagree over the overlap 1999-00 to 2007-08",
     f"1978-79 base: {g78:+.1%}; 1999-2000 base: {g99:+.1%}. The old base uses outdated weights, so the chained "
     "series uses the newest base for each period (linked at 1999-00 and 2012-13).")

# 12. Fiscal-year averaging
j = m[(m.date >= "2022-04-01") & (m.date <= "2023-03-01")]
check("FY averaging: Brent FY2022-23 = mean(Apr 2022..Mar 2023)",
      abs(j.brent.mean() - a.loc[a.fy == 2022, "brent"].iloc[0]) < 1e-6, f"{j.brent.mean():.3f} $/bbl")

# 13. Facts quoted in slides
e = c.set_index("year")
rank_note = (f"India oil consumption 2024 = {e.loc[2024, 'oilcons_ind_kbd']:.0f} kb/d = "
             f"{e.loc[2024, 'india_share_world_oil_cons']:.1%} of world (EIA); 3rd after USA and China")
note("India's oil demand", rank_note)
note("Shock vintages", "Kanzig news shocks: vintage 2025M12 (data to 2025M12). Baumeister-Hamilton shocks: data to "
     f"{m.dropna(subset=['bh_supply']).date.max():%Y-%m}.")

report = ["# Validation Report (generated by code/validate_dataset.py)", "",
          f"Hard checks failed: **{len(failures)}**", "",
          "| Result | Check | Detail |", "|---|---|---|"] + lines
(ROOT / "data" / "validation_report.md").write_text("\n".join(report) + "\n")
print("\n".join(report))
if failures:
    sys.exit(1)

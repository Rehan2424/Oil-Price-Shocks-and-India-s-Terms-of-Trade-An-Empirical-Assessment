"""
Slide-sized figures and LaTeX tables for the Beamer deck (presentation/).

The notebook figures are drawn for a report page, so their labels would be tiny on a 16:9 slide.
This script redraws the charts we show in the talk at the size they actually appear (a Beamer
slide is only 16 cm wide), and writes the backup tables as small booktabs snippets.
Everything is read from data/processed and output/tables, so the slides never hold a typed number
that the analysis did not produce.

Run from the repository root:  python src/slide_figures.py
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from style import AQUA, AXIS, BLUE, GRID, INK, INK2, MUTED, ORANGE, SURFACE

ROOT = Path(__file__).resolve().parents[1]
P, T = ROOT / "data" / "processed", ROOT / "output" / "tables"
FIG = ROOT / "presentation" / "figures"
TAB = ROOT / "presentation" / "tables"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

# Slide figures use small physical sizes, so fonts are set in points as they will be seen.
mpl.rcParams.update({"font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5, "legend.fontsize": 7.5,
                     "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "lines.linewidth": 1.5,
                     "axes.titleweight": "bold", "axes.titlelocation": "left", "figure.facecolor": "white",
                     "axes.facecolor": "white", "savefig.facecolor": "white"})

CM = 1 / 2.54
a = pd.read_csv(P / "annual_fy.csv").set_index("fy")
m = pd.read_csv(P / "monthly.csv", parse_dates=["date"]).set_index("date")


def out(fig, name):
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02, metadata={"CreationDate": None})
    plt.close(fig)


# 1. Real oil price and India's terms of trade, 1970-2025 (two panels, shared axis, no dual y-axis)
d = a.loc[1970:2025]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.4 * CM, 6.0 * CM), sharex=True)
for ax in (ax1, ax2):
    for s, e in [(1973, 1974), (1979, 1980), (1990, 1990), (2021, 2022)]:
        ax.axvspan(s - 0.5, e + 0.5, color="#f0efec", lw=0, zorder=0)
ax1.plot(d.index, d.real_oil_avg, color=BLUE)
ax1.set_title("Real oil price (US$/bbl, 2010 prices)")
ax2.plot(d.index, d.tot_gs_na, color=ORANGE)
ax2.axhline(100, color=AXIS, lw=0.8)
ax2.set_title("India's terms of trade (FY2015-16 = 100)")
for x, lab in [(1973.5, "1973"), (1979.5, "1979"), (1990, "1990"), (2021.5, "2022")]:
    ax1.text(x, 0.97, lab, transform=ax1.get_xaxis_transform(), ha="center", va="top", fontsize=6.5, color=MUTED)
fig.tight_layout(h_pad=0.4)
out(fig, "oil_and_tot")

# 2. Oil shares of exports and imports (the ingredients of the theory benchmark)
d = a.loc[1987:2025]
fig, ax = plt.subplots(figsize=(8.0 * CM, 5.0 * CM))
ax.plot(d.index, 100 * d.s_m_oil, color=BLUE, label="share of imports, $s_m$")
ax.plot(d.index, 100 * d.s_x_oil, color=ORANGE, label="share of exports, $s_x$")
ax.set_title("Oil in India's merchandise trade (%)")
ax.legend(loc="upper left", ncol=2)   # one row, so it sits above the import line
ax.set_ylim(0, 50); ax.set_yticks([0, 10, 20, 30, 40])
fig.tight_layout()
out(fig, "oil_shares")

# 3. Offer curves for India vs the rest of the world (L22), larger fonts for the slide
eps, eta = 1.5, 1.5
p = np.linspace(0.25, 3, 400)
oc_india = lambda k: (k * p ** eps, k * p ** (1 + eps))
oc_world = lambda h: (h * p ** (-(1 + eta)), h * p ** (-eta))


def eq(k, h):
    ps = (h / k) ** (1 / (1 + eps + eta))
    return ps, k * ps ** eps, k * ps ** (1 + eps)


fig, axes = plt.subplots(1, 2, figsize=(9.0 * CM, 4.9 * CM), sharey=True)
cases = [("A: oil supply cut", (1.0, 1.0), (1.0, 0.55), "world"), ("C: India's demand grows", (1.0, 1.0), (1.8, 1.0), "india")]
for ax, (title, before, after, who) in zip(axes, cases):
    for (k, h), ls, lab in ((before, "-", "before"), (after, "--", "after")):
        if who == "world" or lab == "before":
            ax.plot(*oc_world(h), color=BLUE, ls=ls, lw=1.4)
        if who == "india" or lab == "before":
            ax.plot(*oc_india(k), color=ORANGE, ls=ls, lw=1.4)
        ps, xe, ye = eq(k, h)
        xs = np.linspace(0, 2.6, 10)
        ax.plot(xs, ps * xs, color=INK2 if lab == "before" else INK, lw=0.8, ls=":" if lab == "before" else "-")
        ax.plot([xe], [ye], "o", ms=4, color=INK, mec="white", mew=1, zorder=5)
    ax.set_xlim(0, 2.6); ax.set_ylim(0, 2.6); ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=8)
    ax.set_xlabel("India's exports X", fontsize=7.5)
axes[0].set_ylabel("Oil Y (India's import)", fontsize=7.5)
# the label is computed from the equilibrium, so it always matches the curves drawn
for ax, (title, before, after, who) in zip(axes, cases):
    ax.text(1.25, 0.25, f"ToT {eq(*before)[0]:.2f} → {eq(*after)[0]:.2f}", fontsize=7, color=INK)
fig.tight_layout(w_pad=0.6)
out(fig, "offer_curves")

# 4. Monthly local projections: response of ToT to a 1% Brent rise
lp = pd.read_csv(T / "t08_local_projections_monthly.csv", index_col=0)
fig, ax = plt.subplots(figsize=(8.0 * CM, 5.6 * CM))
ax.fill_between(lp.index, lp.beta - 1.645 * lp.se, lp.beta + 1.645 * lp.se, color=ORANGE, alpha=0.15, lw=0, label="90% band")
ax.plot(lp.index, lp.beta, color=ORANGE, marker="o", ms=4, label="estimate")
ax.axhline(0, color=AXIS, lw=0.8)
ax.set_xlabel("months after the oil price rise")
ax.set_title("ToT response (%) to a 1% Brent rise")
ax.legend(loc="lower left")
fig.tight_layout()
out(fig, "local_projections")

# 5. Rolling 20-year elasticity
roll = pd.read_csv(T / "t08b_rolling_elasticity.csv", index_col=0)
fig, ax = plt.subplots(figsize=(8.0 * CM, 5.6 * CM))
ax.fill_between(roll.index, roll.elasticity - 1.645 * roll.se, roll.elasticity + 1.645 * roll.se, color=ORANGE, alpha=0.15, lw=0)
ax.plot(roll.index, roll.elasticity, color=ORANGE, label="estimated (20-yr window, 90% band)")
bm = a.loc[1970:2024, "benchmark_elasticity"].rolling(20, min_periods=10).mean().loc[1989:2024]
ax.plot(bm.index, bm, color=BLUE, label="benchmark $s_x - s_m$")
ax.axhline(0, color=AXIS, lw=0.8)
ax.set_ylim(-0.5, 0.02)
ax.set_title("Oil elasticity of India's ToT")
ax.set_xlabel("last fiscal year of the window")
ax.legend(loc="lower right")
for y in (1989, 2024):
    ax.annotate(f"{roll.loc[y, 'elasticity']:.2f}".replace("-", "−"), (y, roll.loc[y, "elasticity"]), xytext=(0, 6), textcoords="offset points",
                ha="center", fontsize=7, color=INK2)
fig.tight_layout()
out(fig, "rolling_elasticity")

# 6. Supply- vs demand-driven oil price changes (dot and 90% interval)
h3 = pd.read_csv(T / "t09_supply_vs_demand.csv", index_col=0)
labels = ["Annual,\ngoods & services", "Annual,\nmerchandise", "Monthly,\n3-month"]
fig, ax = plt.subplots(figsize=(8.0 * CM, 5.6 * CM))
x = np.arange(3)
for off, col, se, c, lab in ((-0.13, "Supply-driven effect", "s.e. (supply)", BLUE, "supply-driven"),
                             (0.13, "Demand-driven effect", "s.e. (demand)", ORANGE, "demand-driven")):
    ax.errorbar(x + off, h3[col], yerr=1.645 * h3[se], fmt="o", ms=4.5, color=c, mec="white", mew=1, elinewidth=1.4, capsize=0, label=lab)
ax.axhline(0, color=AXIS, lw=0.8)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7)
ax.set_title("ToT effect of a 1% oil rise, by cause")
ax.legend(loc="lower left")
fig.tight_layout()
out(fig, "supply_vs_demand")

# 7. Monthly merchandise ToT and Brent, 2019-2026 (backup)
mm = m.loc["2019-04":"2026-06"]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14 * CM, 6.0 * CM), sharex=True)
ax1.plot(mm.index, mm.brent, color=BLUE); ax1.set_title("Brent (US$/bbl)")
ax2.plot(mm.index, mm.ntt_b12, color=ORANGE, lw=0.8, alpha=0.5)
ax2.plot(mm.index, mm.ntt_b12.rolling(3).mean(), color=ORANGE)
ax2.set_title("India's merchandise ToT, monthly and 3-month average (2012-13 = 100)")
fig.tight_layout(h_pad=0.3)
out(fig, "monthly_tot")

# 8. RCA and Grubel-Lloyd (backup)
c = pd.read_csv(P / "annual_cy.csv").set_index("year")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14 * CM, 4.6 * CM))
d = c.loc[1995:2025]
ax1.plot(d.index, d.rca_refined_334, color=ORANGE, label="refined (SITC 334)")
ax1.plot(d.index, d.rca_crude_333.fillna(0), color=BLUE, label="crude (SITC 333)")
ax1.axhline(1, color=INK2, lw=0.8, ls="--")
ax1.set_title("Revealed comparative advantage"); ax1.legend(loc="center right")
d = c.loc[2000:2025]
ax2.plot(d.index, d.gl_oil_hs2_like, color=ORANGE, label="oil as one industry")
ax2.plot(d.index, d.gl_oil_hs4_weighted, color=BLUE, label="crude, products separately")
ax2.set_ylim(0, 1); ax2.set_title("Grubel-Lloyd index of oil trade"); ax2.legend(loc="upper left")
fig.tight_layout()
out(fig, "rca_and_gl")


# ---------------------------------------------------------------- backup tables (booktabs snippets)
def fmt(v, dec=3):
    if pd.isna(v):
        return "--"
    if isinstance(v, (int, np.integer)) or (isinstance(v, float) and v.is_integer() and abs(v) >= 10):
        return f"{int(v)}"
    return f"{v:.{dec}f}".replace("-", "$-$")


def tex_table(df, name, header, dec=3, first_col_width=None):
    cols = "l" + "r" * (df.shape[1])
    lines = [r"\begin{tabular}{" + cols + "}", r"\toprule", " & ".join(header) + r" \\", r"\midrule"]
    for idx, row in df.iterrows():
        lines.append(" & ".join([str(idx).replace("&", r"\&").replace("%", r"\%")] + [fmt(v, dec) for v in row]) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (TAB / f"{name}.tex").write_text("\n".join(lines) + "\n")


ep = pd.read_csv(T / "t10_episodes.csv", index_col=0)[["From FY", "To FY", "Real oil price, % change",
                                                        "ToT goods & services, % change", "ToT merchandise, % change"]]
lines = [r"\begin{tabular}{llrrrr}", r"\toprule", r"Episode & Fiscal years & Real oil & ToT (G\&S) & ToT (merch.) \\", r"\midrule"]
for idx, r in ep.iterrows():
    lines.append(f"{idx} & {r['From FY']} to {r['To FY']} & " + " & ".join(
        ("--" if pd.isna(v) else f"{v:+.1f}\\%".replace("-", "$-$")) for v in r.iloc[2:]) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}"]
(TAB / "episodes.tex").write_text("\n".join(lines) + "\n")

ur = pd.read_csv(T / "t02_unit_roots.csv", index_col=0)
ur = ur[["ADF level p", "ADF diff p", "PP level p", "PP diff p", "KPSS level p", "ZA level p", "ZA break year"]]
tex_table(ur, "unit_roots", ["Series", "ADF lvl", "ADF diff", "PP lvl", "PP diff", "KPSS lvl", "ZA lvl", "ZA break"])

ar = pd.read_csv(T / "t03_ardl_main.csv", index_col=0)
ar.index = ["Short-run oil elasticity (same year)", "Long-run oil elasticity", "Long-run non-oil commodity elasticity",
            r"Error-correction speed $\alpha$"]
tex_table(ar, "ardl_main", ["", "Estimate", "Std. error", "p-value"])

rob = pd.read_csv(T / "t04_ardl_robustness.csv", index_col=0)[["N", "SR oil", "SR t", "LR oil", "ECT α", "Bounds F", "p (I1 bound)"]]
tex_table(rob, "ardl_robustness", ["Specification", "N", "SR oil", "t", "LR oil", r"ECT $\alpha$", "F", r"p (I(1))"])

nd = pd.read_csv(T / "t06_nardl_asymmetry.csv", index_col=0)
nd.index = [i.replace("Δ", r"$\Delta$") for i in nd.index]
tex_table(nd, "nardl", ["Specification", "N", r"$L^{+}$", r"$L^{-}$", "p (LR)", r"$\pi^{+}$", r"$\pi^{-}$", "p (SR)"])

tex_table(h3, "supply_demand", ["Sample", "N", "Supply", "s.e.", "Demand", "s.e.", "p (equal)"])

uv = pd.read_csv(T / "t11_unit_values_vertical_iit.csv", index_col=0)
tex_table(uv, "unit_values", ["Year", "Crude import (US\\$/t)", "Refined export (US\\$/t)", "Ratio"], dec=2)
print("slide figures and tables written to", FIG.parent)

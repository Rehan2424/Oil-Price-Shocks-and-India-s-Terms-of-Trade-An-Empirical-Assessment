"""Shared chart style for all figures (static PNGs for slides).

Palette: validated categorical slots 1-3 (blue, orange, aqua) on a light surface; text uses ink tokens,
never series colours; one y-axis per panel (two measures -> stacked panels, never a dual axis).
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "output" / "figures"
TAB = ROOT / "output" / "tables"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE, SHADE = "#e1e0d9", "#c3c2b7", "#fcfcfb", "#f0efec"

mpl.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "DejaVu Sans", "font.size": 11, "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.labelcolor": INK2, "axes.edgecolor": AXIS,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.8, "grid.linestyle": "-",
    "lines.linewidth": 2, "lines.solid_capstyle": "round", "lines.solid_joinstyle": "round",
    "legend.frameon": False, "legend.fontsize": 10, "figure.dpi": 110, "savefig.dpi": 200,
})

# Oil-shock episodes used for shading (Indian fiscal years, labelled by starting year)
EPISODES_FY = [(1973, 1974, "1973 OPEC\nembargo"), (1979, 1980, "1979 Iran\nrevolution"),
               (1990, 1990, "1990 Gulf\nwar"), (2007, 2008, "2008\nspike"), (2014, 2015, "2014-16\ncollapse"),
               (2021, 2022, "2022 Russia-\nUkraine"), (2025, 2025, "2026\nHormuz")]


def shade_episodes(ax, episodes=EPISODES_FY, label=True, y=0.98):
    for a, b, name in episodes:
        ax.axvspan(a - 0.5, b + 0.5, color=SHADE, zorder=0, lw=0)
        if label:
            ax.text((a + b) / 2, y, name, transform=ax.get_xaxis_transform(), ha="center", va="top",
                    fontsize=7.5, color=MUTED)


def save(fig, name, source):
    """Save with a source line (every chart on a slide carries its source)."""
    fig.text(0.01, 0.005, "Source: " + source, fontsize=8, color=MUTED, ha="left", va="bottom")
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight")
    return FIG / f"{name}.png"


def save_table(df, name, floatfmt=".3f"):
    df.to_csv(TAB / f"{name}.csv")
    (TAB / f"{name}.md").write_text(df.to_markdown(floatfmt=floatfmt) + "\n")
    return df

"""
Build viva-notes/Viva_Notes.pdf from the markdown files in viva-notes/.

The markdown files are the master copy (they read well on GitHub); the PDF is only for printing.
Needs pandoc and pdfLaTeX (with the FiraSans package, as for the slides).
If pandoc is not installed, `pip install pypandoc_binary` provides it.

Run from the repository root:  python src/build_viva_pdf.py
"""
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "viva-notes"
PARTS = ["00_one_page_summary", "01_theory", "02_data", "03_methods", "04_results", "05_QA_bank",
         "06_formula_sheet"]

# Fira Sans to match the slides, compiled with pdfLaTeX like the deck. pdfLaTeX does not know the
# Greek letters and maths symbols we type directly in the notes, so each one is mapped to LaTeX here.
SYMBOLS = {"−": "-", "→": r"\rightarrow", "≈": r"\approx", "≤": r"\leq", "∈": r"\in", "′": "'",
           "⁺": "^{+}", "⁻": "^{-}", "₀": "_{0}", "₁": "_{1}", "₂": "_{2}",
           "Δ": r"\Delta", "Σ": r"\Sigma", "α": r"\alpha", "β": r"\beta", "γ": r"\gamma",
           "ε": r"\varepsilon", "θ": r"\theta", "π": r"\pi", "φ": r"\varphi", "ψ": r"\psi"}

HEADER = r"""
\usepackage[sfdefault,scaled=.95]{FiraSans}
\usepackage{newunicodechar}
""" + "\n".join(rf"\newunicodechar{{{k}}}{{\ensuremath{{{v}}}}}" for k, v in SYMBOLS.items()) + r"""
\usepackage{xcolor}
\definecolor{oil}{HTML}{EB6834}
\definecolor{navy}{HTML}{0F1B2D}
\usepackage{titlesec}
\titleformat*{\section}{\Large\bfseries\color{navy}}
\titleformat*{\subsection}{\large\bfseries\color{navy}}
\newcommand{\sectionbreak}{\clearpage}
\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\color{gray}Oil price shocks and India's terms of trade \textperiodcentered{} viva notes}
\fancyhead[R]{\small\color{gray}\thepage}
\renewcommand{\headrulewidth}{0pt}
\setlength{\parskip}{4pt}
\renewcommand{\arraystretch}{1.25}
"""

# GitHub tables carry no column widths, so LaTeX would print every column on one line and long
# tables would run off the page. This filter gives each column a share of the page width in
# proportion to its longest entry (capped, so one long cell cannot squeeze everything else).
TABLE_WIDTHS = r"""
function Table(tbl)
  local n = #tbl.colspecs
  local len = {}
  for i = 1, n do len[i] = 4 end
  local function measure(rows)
    for _, row in ipairs(rows) do
      for i, cell in ipairs(row.cells) do
        local l = utf8.len(pandoc.utils.stringify(cell.contents)) or 0
        if i <= n and l > len[i] then len[i] = math.min(l, 45) end
      end
    end
  end
  measure(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do measure(body.body) end
  local total = 0
  for i = 1, n do total = total + len[i] end
  if total < 60 then return tbl end      -- narrow tables fit as they are
  for i = 1, n do tbl.colspecs[i] = {tbl.colspecs[i][1], 0.98 * len[i] / total} end
  return tbl
end
"""


def pandoc_binary():
    exe = shutil.which("pandoc")
    if exe:
        return exe
    try:
        import pypandoc
        return pypandoc.get_pandoc_path()
    except (ImportError, OSError):
        raise SystemExit("pandoc not found: install it, or run `pip install pypandoc_binary`")


def main():
    build = NOTES / "_build"
    build.mkdir(exist_ok=True)
    # one document: the files in order, each starting on a new page (via \sectionbreak)
    body = "\n\n".join((NOTES / f"{p}.md").read_text(encoding="utf-8") for p in PARTS)
    (build / "viva_notes.md").write_text(body, encoding="utf-8")
    (build / "header.tex").write_text(HEADER, encoding="utf-8")
    (build / "table_widths.lua").write_text(TABLE_WIDTHS, encoding="utf-8")

    # read as GitHub-flavoured markdown, so lists and tables come out exactly as they look on GitHub
    cmd = [pandoc_binary(), "-f", "gfm", str(build / "viva_notes.md"), "-o", str(NOTES / "Viva_Notes.pdf"),
           "--pdf-engine=pdflatex", "--include-in-header", str(build / "header.tex"),
           "--lua-filter", str(build / "table_widths.lua"),
           "--toc", "--toc-depth=1",
           "-V", "title=Viva notes", "-V", "subtitle=Oil Price Shocks and India's Terms of Trade",
           "-V", "geometry:margin=2cm", "-V", "fontsize=10pt", "-V", "papersize=a4",
           "-V", "colorlinks=true", "-V", "linkcolor=navy", "-V", "urlcolor=oil", "-V", "toccolor=navy"]
    subprocess.run(cmd, check=True, cwd=build)
    shutil.rmtree(build)
    print("written:", NOTES / "Viva_Notes.pdf")


if __name__ == "__main__":
    main()

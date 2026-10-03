# Viva notes

Our preparation for the 15-minute question round. Read them on GitHub, or print [`Viva_Notes.pdf`](Viva_Notes.pdf),
which has all seven files in one document.

| File | What's in it | Who should read it |
|---|---|---|
| [00 · One-page summary](00_one_page_summary.md) | The 60-second pitch, the numbers to know by heart, who answers what | Everyone, several times |
| [01 · Theory](01_theory.md) | Every course concept we use, applied to India, with the matching number | Everyone; P1 in depth |
| [02 · Data](02_data.md) | Sources, variable definitions, chain-linking, the errors we found in official data | Everyone; P2 in depth |
| [03 · Methods](03_methods.md) | Each test and model, why we chose it, how to read it, the classic traps | Everyone; P3 in depth |
| [04 · Results](04_results.md) | Every result in plain words, and where each number on the slides comes from | Everyone; P3 and P4 in depth |
| [05 · Question bank](05_QA_bank.md) | 140 likely questions with model answers, tagged by who answers first | Everyone |
| [06 · Formula sheet](06_formula_sheet.md) | All equations and test results on one page | Keep it open while revising |

## A plan for the last week

1. **Day 1.** Everyone reads 00 and 04, and watches the deck once with the speaker notes
   (`presentation/slides_with_notes.pdf`).
2. **Days 2–3.** Each presenter goes deep on their own file (P1 theory, P2 data, P3 methods, P4 results).
3. **Day 4.** Rehearse the talk with a timer. The scripts add up to about 13 minutes at a calm pace.
4. **Days 5–6.** Mock viva: one person reads random questions from 05, and the tagged presenter answers without
   notes. Mark the ones that went badly and redo them the next day.
5. **Day 7.** Read 00 and 06 again. Nothing new.

## Rebuilding the PDF

`Viva_Notes.pdf` is built from these markdown files. After editing them, run `python src/build_viva_pdf.py`
from the repository root.

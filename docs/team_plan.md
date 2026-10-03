# Team plan

How the work is split, what each of us owns, and what is left to do before the presentation.

## The talk in one paragraph

Oil shocks keep hitting India: 1973, 1979, 1990, 2022, and March 2026. We measure how much they move India's terms
of trade, the price of its exports relative to its imports. Offer curves (L22) give the hypotheses. A benchmark
built from the definition of the terms of trade (L21) gives the expected size. ARDL, NARDL, local projections and
identified oil shocks test them. The answer: a 10% oil rise costs about 2.4% of the terms of trade within a year,
rises and falls matter equally, the cause of the rise does not change the damage, and India's exposure has halved
because it became a refined-fuel exporter.

## Who owns what

| | Presents | Owns in the viva | Files to know best |
|---|---|---|---|
| **P1** | Hook, question and hypotheses, offer curves (slides 1–3, ~3.5 min) | Theory: terms of trade, offer curves, small vs large country, welfare | `docs/01_theory_framework.md`, `viva-notes/01_theory.md` |
| **P2** | Benchmark, literature, data (slides 4–6, ~3 min) | Benchmark, RCA and Grubel–Lloyd, literature, data sources and the data problems we fixed | `docs/02_literature_review.md`, `docs/03_data.md`, `viva-notes/02_data.md` |
| **P3** | Method, H1, monthly timing (slides 7–9, ~3.5 min) | Unit roots, ARDL and the bounds test, diagnostics, local projections, benchmark test | `docs/04_methodology.md`, `viva-notes/03_methods.md`, notebooks 03 and 05 |
| **P4** | H2 and exposure, H3, policy (slides 10–12, ~3 min) | NARDL, supply vs demand shocks, rolling elasticity, policy, limitations | `docs/05_results.md`, `viva-notes/04_results.md`, notebooks 04 and 06 |

Everyone reads `viva-notes/00_one_page_summary.md` and `viva-notes/04_results.md`, and goes through the question bank.

## Before the presentation

- [ ] Add our four names to the title slide: the `TODO` near the top of `presentation/slides.tex`. Recompile
      (or do it on Overleaf, see `presentation/README.md`).
- [ ] Hand-check the eleven values in `data/validation_log.md` against the original publications and sign them off.
      It takes about 30 minutes and is the best answer to "how do you know your data are right?".
- [ ] Read through the deck once with `presentation/slides_with_notes.pdf`, each presenter saying their part aloud.
- [ ] Two timed rehearsals. The scripts add up to about 13 minutes; aim to finish by 14 minutes.
- [ ] One mock viva with questions drawn at random from `viva-notes/05_QA_bank.md`.
- [ ] Know where the backup slides are (after the thank-you slide): episodes, unit roots, ARDL tables, NARDL,
      supply vs demand, the refining hedge, monthly data, limitations.
- [ ] On the day, bring `slides.pdf` on a USB stick as well as the laptop copy.

## Rules we followed (worth saying in the viva)

- **Data.** Official agencies and peer-reviewed replication data only (`data/SOURCE_POLICY.md`). Raw files are
  never edited, every file has a checksum, and every key series is checked against a second source.
- **Theory.** No theory slide stands alone. Every concept appears as an application to India with a number from our
  data.
- **Numbers.** No number is typed into the slides by hand without a source table. The mapping from each slide
  number to its table is in `viva-notes/04_results.md`.
- **Honesty about results.** Two of our three hypotheses were not supported, and we say so. The long-run ARDL
  result is weak, and we say that too.

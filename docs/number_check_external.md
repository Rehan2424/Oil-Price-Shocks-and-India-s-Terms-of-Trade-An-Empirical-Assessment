## Our raw files match the publishers' current files

On 4 October 2026 we downloaded the main sources again and compared them with the copies in `data/raw/`.

| Source | What was compared | Result |
|---|---|---|
| RBI Handbook 2025-26, Tables 32, 111, 115, 121, 133 (live pages, links in `data/SOURCES.md`) | 1,416 published numbers | identical |
| World Bank Pink Sheet, monthly (Brent, Dubai, average crude, gold) | 801 months × 4 series | identical |
| World Bank WDI: export and import values at current and constant prices, GDP in US$ | 66 years × 5 series | identical |
| FRED Brent (cross-check series) | 9,097 days | identical |
| Känzig (2021) oil supply news shocks, author's GitHub | 612 months | identical |

## Facts from outside our dataset

Checked against the original source or a report of it.

| Claim (where we use it) | What the source says | Source |
|---|---|---|
| The IEA called the 2026 Hormuz disruption the largest oil supply disruption on record (slide 1 notes, Q&A A9) | IEA Oil Market Report, March 2026: "the biggest oil supply disruption in history"; flows through Hormuz fell from about 20 mb/d to a trickle; strikes on Iran began on 28 February | [BNN Bloomberg, 12 Mar 2026](https://www.bnnbloomberg.ca/business/2026/03/12/world-faces-largest-ever-oil-supply-disruption-on-middle-east-war-iea-says/); [Business Today, 12 Mar 2026](https://www.businesstoday.in/amp/world/story/from-20-mn-barrels-a-day-to-a-trickle-iea-says-hormuz-closure-is-biggest-oil-supply-disruption-ever-520370-2026-03-12) |
| Jamnagar is the world's largest refining complex; first refinery 1999, export refinery 2008 (viva notes 01, Q&A B11) | Commissioned 1999; SEZ export refinery added 2008; 1.24 million barrels a day | [NS Energy](https://www.nsenergybusiness.com/projects/reliance-industries-jamnagar-refinery-india) |
| Strategic reserves of about 5.3 million tonnes at Visakhapatnam, Mangaluru and Padur, roughly 9–10 days (Q&A G3) | 1.33 + 1.50 + 2.50 = 5.33 million tonnes; about 9.5 days at full capacity | [Business Today, 24 Mar 2026](https://www.businesstoday.in/latest/economy/story/exclusive-indias-strategic-oil-reserves-cover-just-less-than-10-days-522058-2026-03-24); [Lok Sabha answer](https://eparlib.nic.in/bitstream/123456789/2974287/1/AU1056.pdf) |
| Excise duties raised in 2020, cut in November 2021 and May 2022 (Q&A G2) | Raised by ₹13 (petrol) and ₹16 (diesel) in March–May 2020; cut ₹5/₹10 on 4 Nov 2021 and ₹8/₹6 in May 2022 | [Autocar Pro](https://autocarpro.in/news-national/government-slashes-excise-duty-on-petrol-by-rs-5--diesel-by-rs-10-80387); [Outlook Business](https://www.outlookbusiness.com/amp/story/news/excise-duty-cut-petrol-price-slashed-by-rs-8-69-ltr-diesel-by-rs-7-05-ltr-news-197902) |
| Special duties on fuel exports and domestic crude from July 2022 (Q&A G6) | Imposed 1 July 2022 on domestic crude and on exports of petrol, diesel and ATF | [Drishti IAS, 22 Jul 2022](https://www.drishtiias.com/daily-updates/daily-news-analysis/windfall-tax/print_manually) |
| India shifted a large share of its crude purchases to Russia after 2022 (Q&A B17) | About 35% of India's crude imports in 2023 and FY2023-24, up from about 2% before the war | [S&P Global](https://spglobal.com/commodityinsights/en/market-insights/latest-news/oil/010824-red-sea-woes-unlikely-to-dent-russias-position-as-indias-top-crude-supplier); [Business Standard](https://www.business-standard.com/amp/economy/news/import-of-russian-crude-up-25-at-14-7-billion-in-q1-shows-data-124082500392_1.html) |
| Schmitt-Grohé and Uribe find terms-of-trade shocks explain under 10% of output movements, in 38 countries (literature slide, Q&A C9) | Country-specific SVARs for 38 countries; terms-of-trade shocks explain less than 10% of movements in aggregate activity | [RePEc](https://ideas.repec.org/a/wly/iecrev/v59y2018i1p85-111.html); [NBER WP 21253](https://www.nber.org/system/files/working_papers/w21253/w21253.pdf) |
| Backus and Crucini: oil explains much of the variation in the terms of trade (literature slide) | "Oil accounts for much of the variation in the terms of trade over the last twenty-five years" | [RePEc](https://ideas.repec.org/a/eee/inecon/v50y2000i1p185-213.html) |
| Deheri and Sahu: only oil-specific demand shocks significantly affect India's trade balances (literature slide, Q&A C8) | "Among oil market shocks, only oil-specific demand shocks have a significant impact on India's merchandise trade balances" | [Energy Research Letters](https://erl.scholasticahq.com/article/77528.pdf) |
| Lecture quotes (L17 "the more broadly an industry is defined…", L21 definition of the net barter terms of trade, L20 ±15% rule, L16 MR = p(1 − 1/e), L13 time horizons, L05 "fuels") | Found word for word in the lecture PDFs | `course-material/lectures/` |

## Corrections made after this check

Running the check found these mistakes in our own text, all now fixed in the slides, notes and docs:

1. **2026 terms of trade.** We had said India's merchandise terms of trade fell 13% from February to June 2026. That
   is true of those two months on DGCI&S's 2012-13 base, but February was an unusually high month, the new 2022-23
   base shows +8% for the same months, and in three-month averages neither base shows a fall. The slides now use
   the robust number from the last shock (−24%, FY2020-21 to FY2022-23) and say that 2026 shows no clear fall yet.
2. **Short-run range across the six ARDL specifications:** −0.19 to −0.28 (we had written −0.20).
3. **Jarque–Bera p-value:** 0.25 (we had written 0.26 by rounding 0.255 twice).
4. **H3, smallest p-value:** 0.53 (we had written 0.54).
5. **Refined/crude unit-value ratio:** 1.13–1.41 over 2000–2025, outside the ±15% band in every year except 2011 and
   2012 (we had quoted 1.2–1.4 from the five years in our table).
6. **Oil share of exports since FY2008:** 9–22% (we had written 12–22%; FY2020-21 was 8.8%).
7. **Services share of India's exports:** almost half today (46% in 2024), not "about a third".
8. **Monthly response after one to three months:** about 0.2–0.4% per 1% oil rise (we had written 0.3–0.45%).
9. **Rupee:** 94.65 is the weakest *year-end* rate on record (the table holds year-end rates, not daily lows).
10. **DGCI&S index formula:** the 1999-2000 series was a Fisher index; only the 2012-13 and 2022-23 bases are
    Laspeyres.
11. **Lecture 5:** it lists fuels among goods where India has a comparative advantage in the world market; we had
    paraphrased it as an advantage "over China".

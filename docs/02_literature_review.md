# Literature Review

Kept deliberately short (16 core references in four strands) so it fits the 15-minute presentation and can be defended in the viva. Every reference was checked against Crossref (DOI), RePEc or the publisher; the full list with DOIs is in [`references.md`](references.md).

## Strand 1: Why terms of trade matter

- **Harberger (1950)** and **Laursen & Metzler (1950)** show that a worse ToT lowers a country's real income. Households smooth consumption, so saving falls and the trade balance worsens: the *Harberger–Laursen–Metzler (HLM) effect*. This links a ToT shock to the current-account and BoP pressure that India felt in 1990-91, 2013 and 2022.
- **Mendoza (1995)** builds a model in which ToT shocks are a major source of business cycles in open economies. **Schmitt-Grohé & Uribe (2018)** test this with country-specific SVARs for 38 countries and find ToT shocks explain **less than 10%** of output movements, which they call a "disconnect" between models and data.
- **For us:** ToT changes have real income and BoP consequences, but their size must be measured, not assumed. This is why we estimate the elasticity rather than borrow one.

## Strand 2: Oil prices and the terms of trade / external balances

- **Backus & Crucini (2000)** is our anchor paper. Using a dynamic general-equilibrium trade model and data for industrial countries, they find **oil accounts for much of the variation in the terms of trade** over the previous 25 years. Its role varies over time, and the economy responds differently to oil supply shocks than to other shocks.
- **Kilian, Rebucci & Spatafora (2009)** estimate how oil **demand** and **supply** shocks affect oil exporters' and importers' oil trade balance, non-oil trade balance, current account and net foreign assets. The effect on the overall balance "depends critically on the response of the non-oil trade balance". This motivates separating oil from non-oil trade, and supply from demand shocks.
- **For us:** we take the Backus–Crucini question (how much does oil move ToT?) to India, with the Kilian–Rebucci–Spatafora distinction between kinds of shock.

## Strand 3: Defining and identifying oil shocks

- **Hamilton (1983)** shows oil price increases preceded most post-war US recessions.
  - **Mork (1989)** finds the effect is **asymmetric**: price rises hurt, but falls do not help symmetrically.
  - **Hamilton (2003)** proposes nonlinear "net oil price increase" measures. This is the motivation for our asymmetry test (H2).
- **Kilian (2009)** shows "not all oil price shocks are alike". Supply shocks, global demand shocks and oil-specific demand shocks have different effects, and much of the 2000s price surge was **demand-driven**.
- **Baumeister & Hamilton (2019)** relax Kilian's strict identification with Bayesian priors and find **supply disruptions matter more** than earlier estimates implied. Their shock series is the one we use for H3.
- **Känzig (2021)** identifies **oil supply news shocks** from oil-futures price moves around **OPEC announcements**. Negative news raises oil prices immediately and lowers activity. This gives us an exogenous supply shock that India does not cause (the price-taker problem, L11).

## Strand 4: Evidence for India

| Study | Data and method | Main finding | Relevance |
|---|---|---|---|
| **Bhanumurthy, Das & Bose (2012)**, NIPFP WP 2012-99 | Macro policy simulation model | Oil price shocks transmit through import, price and fiscal channels; pass-through policy shapes inflation, growth and deficits | Oil affects India mainly through the import bill |
| **Ghosh (2011)**, *Applied Energy* | Daily data Jul 2007–Nov 2008; GARCH/EGARCH | Rising oil prices **depreciate the rupee** against the US$ | Exchange-rate channel (REER control) |
| **Tiwari & Olayeni (2013)**, *Economics Bulletin* | Wavelet analysis | The oil price–trade balance link for India varies across time horizons | Short run vs long run differ (our ECM) |
| **Deheri & Sahu (2024)**, *Energy Research Letters* | SVAR with oil-market shocks | Adverse **oil-specific demand** shocks worsen India's aggregate and non-oil trade balances; only these shocks matter significantly | Kind of shock matters for India (our H3) |

## The gap and our contribution

Indian studies look at the **trade balance, inflation or the exchange rate**. None that we found models India's **terms of trade** directly, which is the price ratio at the heart of the trade theory in our course. We contribute five things:

1. A direct estimate of the oil → ToT elasticity, short and long run (ARDL bounds test, 1970–2025), on official data that we cross-checked and corrected (RBI/DGCI&S inconsistencies documented).
2. A **theory benchmark**, s_x − s_m from the definition of NTT, tested against the data.
3. Evidence that India's exposure has **roughly halved** as it built an acquired comparative advantage in refining (RCA, Grubel–Lloyd).
4. Tests of **asymmetry** (NARDL) and of **supply vs demand** shocks using Baumeister–Hamilton and Känzig shocks.
5. Coverage of the **2022 Russia–Ukraine** and **2026 Hormuz** shocks.

## Methods references

- Pesaran, Shin & Smith (2001): ARDL bounds test.
- Kripfganz & Schneider (2020): finite-sample critical values.
- Shin, Yu & Greenwood-Nimmo (2014): NARDL.
- Jordà (2005): local projections.
- Balassa (1965): RCA.
- Grubel & Lloyd (1971): intra-industry trade index.

# Structural Interpretation of Vector Autoregressions with Incomplete Identification: Revisiting the Role of Oil Supply and Demand Shocks

Christiane Baumeister and James D. Hamilton (2019), *American Economic Review* 109(5), 1873–1910

[Paper](https://doi.org/10.1257/aer.20151569) · [shock data (authors' site)](https://sites.google.com/site/cjsbaumeister/datasets)

## The question

- Kilian-style identification rests on strong assumptions, such as oil supply not reacting to prices within a month. What happens if we admit uncertainty about them?

## How they answer it

- Bayesian structural VARs with priors on the key elasticities instead of exact restrictions, for the global oil market.

## What they find

- Supply disruptions are a bigger factor in historical oil price movements, and inventory demand a smaller one, than earlier estimates implied.
- Supply shocks reduce global activity after a significant lag; oil demand shocks do not.

## What we use from it

- Their published monthly shock series (supply, economic activity, consumption demand, inventory demand, 1975–2026) is how we split each oil price change into a supply-driven and a demand-driven part for H3.
- Because they give supply shocks more weight than Kilian, they make H3 a tougher test.

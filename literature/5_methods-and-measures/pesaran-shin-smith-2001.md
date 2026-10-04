# Bounds Testing Approaches to the Analysis of Level Relationships

M. Hashem Pesaran, Yongcheol Shin and Richard J. Smith (2001), *Journal of Applied Econometrics* 16(3), 289–326

[Paper](https://doi.org/10.1002/jae.616)

## The problem it solves

- How to test for a long-run (level) relationship when you do not know whether the regressors are I(0) or I(1).

## The method

- Estimate an ARDL in error-correction form and test whether the lagged levels are jointly zero, with an F-test (and a t-test on the error-correction term).
- Two sets of critical values bound the answer: a lower bound if all regressors are I(0), an upper bound if all are I(1). Above the upper bound means a level relationship exists; below the lower bound means none; in between is inconclusive.

## What we use from it

- Our H1 model: ARDL(1,1,1) of India's terms of trade on the real oil price and real non-energy prices, FY1970-71 to FY2024-25.
- Bounds F = 4.74: above the 10% upper bound, between the 5% bounds. The short-run elasticity (−0.24) is our headline result.

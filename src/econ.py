"""Econometric helpers used by the analysis notebooks (statsmodels / arch)."""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from arch.unitroot import PhillipsPerron, ZivotAndrews
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan, linear_reset
from statsmodels.stats.stattools import jarque_bera
from statsmodels.tsa.ardl import UECM, ardl_select_order
from statsmodels.tsa.stattools import adfuller, kpss

warnings.filterwarnings("ignore", message="The test statistic is outside of the range")
ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"


def load():
    m = pd.read_csv(P / "monthly.csv", parse_dates=["date"]).set_index("date")
    a = pd.read_csv(P / "annual_fy.csv").set_index("fy")
    c = pd.read_csv(P / "annual_cy.csv").set_index("year")
    return m, a, c


def unit_root_row(s):
    """ADF, Phillips-Perron, KPSS on level and first difference; Zivot-Andrews (one break) on level."""
    s = s.dropna()
    ds = s.diff().dropna()
    _, za_p, za_break = zivot_andrews_break(s)
    return {"ADF level p": adfuller(s, autolag="AIC")[1], "ADF diff p": adfuller(ds, autolag="AIC")[1],
            "PP level p": PhillipsPerron(s).pvalue, "PP diff p": PhillipsPerron(ds).pvalue,
            "KPSS level p": kpss(s, regression="c", nlags="auto")[1],
            "KPSS diff p": kpss(ds, regression="c", nlags="auto")[1],
            "ZA level p": za_p, "ZA break year": za_break}


def zivot_andrews_break(s):
    s = s.dropna()
    za = ZivotAndrews(s, trend="c")
    # the arch implementation stores the break position in the regression results; recover it via grid search
    best, best_t = None, np.inf
    n = len(s)
    for k in range(int(0.15 * n), int(0.85 * n)):
        d = pd.DataFrame({"y": s.values})
        d["dy"] = d.y.diff()
        d["y1"] = d.y.shift(1)
        d["du"] = (np.arange(n) >= k).astype(float)
        d["dy1"] = d.dy.shift(1)
        r = smf.ols("dy ~ y1 + du + dy1", data=d.dropna()).fit()
        if r.tvalues["y1"] < best_t:
            best_t, best = r.tvalues["y1"], s.index[k]
    return za.stat, za.pvalue, best


def ardl_uecm(y, X, maxlag=2, fixed=None):
    """Select an ARDL by AIC (or use `fixed`), estimate its error-correction form and the bounds test.

    Returns a dict with the UECM fit, order, long-run coefficients (with delta-method s.e.),
    the error-correction coefficient and bounds-test results (Pesaran-Shin-Smith case 3,
    finite-sample critical values / p-values, Kripfganz & Schneider 2020)."""
    if fixed is None:
        sel = ardl_select_order(y, maxlag, X, maxlag, ic="aic", trend="c")
        p = max(sel.model.ardl_order[0], 1)
        q = {k: max(v, 1) for k, v in zip(X.columns, sel.model.ardl_order[1:])}
    else:
        p, q = fixed
    u = UECM(y, p, X, q, trend="c").fit()
    # Finite-sample p-values are simulated, so fix the seed: otherwise the third decimal moves
    # between runs and the tables would not match the slides exactly.
    bt = u.bounds_test(case=3, asymptotic=False, rng=2026)
    yname = y.name
    alpha = u.params[f"{yname}.L1"]
    lr = {}
    cov = u.cov_params()
    for x in X.columns:
        b = u.params[f"{x}.L1"]
        est = -b / alpha
        g = np.zeros(len(u.params))
        names = list(u.params.index)
        g[names.index(f"{x}.L1")] = -1 / alpha
        g[names.index(f"{yname}.L1")] = b / alpha ** 2
        se = float(np.sqrt(g @ cov.values @ g))
        lr[x] = (est, se)
    return {"fit": u, "order": (p, q), "alpha": alpha, "alpha_t": u.tvalues[f"{yname}.L1"],
            "lr": lr, "F": bt.statistic, "p_I0": bt.pvalue["lower"], "p_I1": bt.pvalue["upper"],
            "crit": bt.critical_values}


def as_ols(res):
    """Re-express a statsmodels ARDL/UECM fit as an equivalent OLS fit (same design matrix) for diagnostics."""
    import statsmodels.api as sm
    if hasattr(res.model, "_x") and not hasattr(res, "k_constant"):
        return sm.OLS(res.model._y, pd.DataFrame(res.model._x, columns=res.model.exog_names)).fit()
    return res


def diagnostics(res, lags=2):
    res = as_ols(res)
    bg = acorr_breusch_godfrey(res, nlags=lags)
    bp = het_breuschpagan(res.resid, res.model.exog)
    jb = jarque_bera(res.resid)
    try:
        reset = linear_reset(res, power=2, use_f=True)
        reset_p = float(reset.pvalue)
    except Exception:
        reset_p = np.nan
    return {"Breusch-Godfrey LM (serial corr.) p": bg[1], "Breusch-Pagan (heterosked.) p": bp[1],
            "Jarque-Bera (normality) p": jb[1], "Ramsey RESET p": reset_p}


def cusum(res):
    """Recursive-residual CUSUM and CUSUMSQ with 5% bands (Brown-Durbin-Evans)."""
    res = as_ols(res)
    y, X = res.model.endog, res.model.exog
    n, k = X.shape
    w = []
    for t in range(k, n):
        Xt, yt = X[:t], y[:t]
        beta = np.linalg.lstsq(Xt, yt, rcond=None)[0]
        xt = X[t]
        f = 1 + xt @ np.linalg.pinv(Xt.T @ Xt) @ xt
        w.append((y[t] - xt @ beta) / np.sqrt(f))
    w = np.array(w)
    sigma = w.std(ddof=1)
    cs = np.cumsum(w) / sigma
    m = len(w)
    t = np.arange(1, m + 1)
    band = 0.948 * (np.sqrt(m) + 2 * t / np.sqrt(m))
    css = np.cumsum(w ** 2) / np.sum(w ** 2)
    c0 = 0.20  # approx. 5% Durbin (1969) bound for m ~ 50
    return pd.DataFrame({"cusum": cs, "band": band, "cusumsq": css, "sq_mid": t / m,
                         "sq_lo": t / m - c0, "sq_hi": t / m + c0})


def nardl(df, y, x, controls=(), extra_ylag=False):
    """Shin-Yu-Greenwood-Nimmo (2014) NARDL(1,1) in error-correction form, estimated by OLS.
    x is split into positive and negative partial sums of its changes."""
    d = df[[y, x] + list(controls)].copy()
    dx = d[x].diff().fillna(0)
    d["xp"] = dx.clip(lower=0).cumsum()
    d["xn"] = dx.clip(upper=0).cumsum()
    d["dy"] = d[y].diff()
    d["y_1"] = d[y].shift(1)
    for v in ["xp", "xn"] + list(controls):
        d[f"{v}_1"] = d[v].shift(1)
        d[f"d{v}"] = d[v].diff()
    rhs = ["y_1", "xp_1", "xn_1", "dxp", "dxn"] + [f"{c}_1" for c in controls] + [f"d{c}" for c in controls]
    if extra_ylag:
        d["dy_1"] = d["dy"].shift(1)
        rhs.append("dy_1")
    r = smf.ols("dy ~ " + " + ".join(rhs), data=d[["dy"] + rhs].dropna()).fit()
    al = r.params["y_1"]
    out = {"fit": r, "LR_pos": -r.params["xp_1"] / al, "LR_neg": -r.params["xn_1"] / al,
           "SR_pos": r.params["dxp"], "SR_neg": r.params["dxn"], "alpha": al,
           "p_LR_sym": float(r.f_test("xp_1 = xn_1").pvalue), "p_SR_sym": float(r.f_test("dxp = dxn").pvalue),
           "N": int(r.nobs), "data": d}
    return out


def nardl_multipliers(res, horizons=10):
    """Cumulative dynamic multipliers of a NARDL(1,1) for a permanent +1 / -1 unit change in x."""
    p = res["fit"].params
    al = p["y_1"]
    out = []
    for sign, lvl, sr in ((+1, "xp_1", "dxp"), (-1, "xn_1", "dxn")):
        y_path = [0.0]
        x_level = 1.0 * sign
        # y_t - y_{t-1} = al*y_{t-1} + b*x_{t-1} + c*dx_t   with x stepping once at t=0
        y_prev = 0.0
        path = []
        for h in range(horizons + 1):
            dx = x_level if h == 0 else 0.0
            x_lag = 0.0 if h == 0 else x_level
            dy = al * y_prev + p[lvl] * x_lag + p[sr] * dx
            y_prev = y_prev + dy
            path.append(y_prev)
        out.append(pd.Series(path, name="rise" if sign > 0 else "fall"))
    return pd.concat(out, axis=1)


def local_projection(df, y, shock, horizons=6, controls_lags=1, hac=True):
    """Jorda (2005) local projections: y_{t+h} - y_{t-1} on shock_t (+ lags of shock and dy)."""
    d = df.copy()
    d["dy"] = d[y].diff()
    rows = []
    for h in range(horizons + 1):
        d["lhs"] = d[y].shift(-h) - d[y].shift(1)
        rhs = [shock]
        for L in range(1, controls_lags + 1):
            d[f"{shock}_l{L}"] = d[shock].shift(L)
            d[f"dy_l{L}"] = d["dy"].shift(L)
            rhs += [f"{shock}_l{L}", f"dy_l{L}"]
        r = smf.ols("lhs ~ " + " + ".join(rhs), data=d[["lhs"] + rhs].dropna()).fit(
            cov_type="HAC", cov_kwds={"maxlags": h + 1})
        rows.append({"h": h, "beta": r.params[shock], "se": r.bse[shock], "N": int(r.nobs)})
    return pd.DataFrame(rows).set_index("h")

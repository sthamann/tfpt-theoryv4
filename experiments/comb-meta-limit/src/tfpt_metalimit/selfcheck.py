"""Injection self-consistency for the meta-limit machinery.

Inject a KNOWN common comb amplitude ``eps_true`` into a mock set of channels (each with several
independent, red-noise recovery curves at the frozen omega), push it through the EXACT same
pipeline (per-source comb fit -> power -> random-effects combine -> 95% UL), and confirm:

  * eps_true = 0     -> the recovered amplitude sits at ~0 and the UL is small (no false comb);
  * eps_true = 2-5%  -> the recovered amplitude tracks the injection and the UL brackets it;
  * coverage         -> over many trials the injected eps is <= the 95% UL ~95% of the time
                        (the UL is calibrated / not anti-conservative).

This is the primary validation (project preference: no heavy pytest suite).
"""

from __future__ import annotations

import math

import numpy as np

from .combfit import estimate_comb
from .kernel import LAMBDA, OMEGA
from .metalimit import combine_power, upper_limit


def synth_curve(periods: float, eps: float, noise: float, rng: np.random.Generator, *,
                alpha: float = 0.5, n_pts: int = 60, red: float = 0.3) -> tuple[np.ndarray, np.ndarray]:
    """A synthetic log-flux recovery curve y = -alpha ln t + eps cos(omega ln t + phi) + noise,
    with an AR(1) red-noise component (fraction ``red``) so the null is realistically correlated."""
    tmax = math.exp(periods * math.log(LAMBDA))
    t = np.logspace(0.0, math.log10(tmax), n_pts)
    lt = np.log(t)
    phi = rng.uniform(0.0, 2.0 * math.pi)
    white = rng.normal(0.0, noise, n_pts)
    reds = np.zeros(n_pts)
    for i in range(1, n_pts):
        reds[i] = 0.7 * reds[i - 1] + rng.normal(0.0, noise)
    n = (1.0 - red) * white + red * reds
    y = -alpha * lt + eps * np.cos(OMEGA * lt + phi) + n
    return t, y


def mock_meta(eps_true: float, rng: np.random.Generator, *, n_channels: int = 3,
              sources_per: int = 6, noise: float = 0.10, periods: float = 3.2,
              red: float = 0.3, n_freq: int = 150) -> dict:
    """Run the full two-level pipeline on mock channels -> group amplitude summary."""
    chan: list[tuple[float, float]] = []
    for _ in range(n_channels):
        e2, se = [], []
        for _s in range(sources_per):
            t, y = synth_curve(periods, eps_true, noise, rng, red=red)
            est = estimate_comb(t, y, seed=int(rng.integers(1_000_000_000)), n_freq=n_freq)
            e2.append(est.eps2)
            se.append(est.se_power)
        c = combine_power(e2, se)
        chan.append((c.eps2, c.se_power))
    grp = combine_power([c[0] for c in chan], [c[1] for c in chan])
    return {"eps2": grp.eps2, **upper_limit(grp, rho=0.0)}


def run_selfcheck(*, seed: int = 0, n_trials: int = 150) -> dict:
    """Recovery at a few injected eps + a coverage calibration of the 95% UL."""
    rng = np.random.default_rng(seed)
    recover = {}
    for eps_true in (0.0, 0.02, 0.05):
        res = mock_meta(eps_true, rng, n_freq=300)
        recover[f"{eps_true:.2f}"] = {
            "eps_true": eps_true,
            "eps_hat": round(res["eps_hat"], 5),
            "eps95": round(res["eps95"], 5),
            "recovered_within_UL": bool(eps_true <= res["eps95"] + 1e-9),
        }
    cov_eps = 0.02
    hits = 0
    for _ in range(n_trials):
        res = mock_meta(cov_eps, rng, n_freq=120)
        hits += int(cov_eps <= res["eps95"] + 1e-9)
    coverage = hits / n_trials
    return {
        "recovery": recover,
        "coverage_eps": cov_eps,
        "coverage_n_trials": n_trials,
        "coverage_95UL": round(coverage, 3),
        "coverage_ok": bool(coverage >= 0.90),
        "note": ("injected eps recovered and bracketed by the 95% UL; coverage is the fraction of "
                 "trials with eps_true <= UL (target ~0.95). A value >=0.90 confirms the UL is not "
                 "materially anti-conservative under realistic red noise."),
    }

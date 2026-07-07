"""KC.03 -- discrete scale invariance in SIZE space: log-periodic decoration of the
burst-ENERGY distribution (the FRB analog of pulsar PG.01).

Statistic: Rayleigh power z(omega) = |sum exp(i omega ln E)|^2 / n at the frozen TFPT
log-period battery (quake BATTERY_LAMBDAS incl. the Z2 readings), each with a
>= 2.8-period range gate on the ln E span.

Nulls (per lambda, p = MAX over the three -- conservative, the PG.01 recipe):
  (1) log-normal fit to ln E;
  (2) KDE shape-preserving resample (smooth, follows the real envelope);
  (3) population-controlled GMM (BIC-selected k <= 3): the Li+2021 energy
      distribution is famously BIMODAL -- a two-population structure must never be
      sold as a comb.
Look-elsewhere: Bonferroni over the gated battery members.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.stats import gaussian_kde
from sklearn.mixture import GaussianMixture

from .data import Bursts

PHI = 0.5 * (1.0 + math.sqrt(5.0))
BATTERY: dict[str, float] = {
    "3/2 (1/Koide, fundamental)": 1.5,
    "phi (golden, g_car=5)": PHI,
    "2 (sheet doubling)": 2.0,
    "3 (N_fam)": 3.0,
    "4 (|mu4|)": 4.0,
    "5 (g_car)": 5.0,
    "8 (rank E8)": 8.0,
    "(3/2)^6 (recovery comb)": 1.5 ** 6,
    "30 (Coxeter h)": 30.0,
    "(3/2)^3 (Z2 half-period)": 1.5 ** 3,
    "(3/2)^4 (Z2 antiperiodic harmonic)": 1.5 ** 4,
    "(3/2)^12 (Z2 antiperiodic fundamental)": 1.5 ** 12,
}
MIN_PERIODS = 2.8
N_NULL = 2000


def _rayleigh(x: np.ndarray, omega: float) -> float:
    return float(np.abs(np.exp(1j * omega * x).sum()) ** 2 / len(x))


def _fit_gmm(x: np.ndarray, rng: np.random.Generator) -> GaussianMixture:
    best, best_bic = None, np.inf
    for k in (1, 2, 3):
        g = GaussianMixture(n_components=k, random_state=17).fit(x[:, None])
        bic = g.bic(x[:, None])
        if bic < best_bic:
            best, best_bic = g, bic
    return best


@dataclass
class KC03Result:
    source: str
    n_bursts: int
    ln_e_range: float
    battery: dict = field(default_factory=dict)
    n_gated: int = 0
    best_label: str = ""
    best_p: float = 1.0
    bonferroni_global_p: float = 1.0
    gmm_components: int = 0
    verdict: str = ""


def run(b: Bursts, *, seed: int = 0) -> KC03Result:
    x = np.log(b.energy)
    rng = np.random.default_rng(seed)
    span = float(x.max() - x.min())

    # the three null generators (frozen)
    mu, sd = float(x.mean()), float(x.std())
    kde = gaussian_kde(x)
    gmm = _fit_gmm(x, rng)

    def draws(kind: str) -> np.ndarray:
        if kind == "lognormal":
            return rng.normal(mu, sd, len(x))
        if kind == "kde":
            return kde.resample(len(x), seed=int(rng.integers(2**31))).ravel()
        # sklearn re-seeds from .random_state on EVERY .sample() call -- with a fixed
        # int every draw would be identical (a silent null-killer, caught 2026-07-06).
        gmm.random_state = int(rng.integers(2**31))
        s, _ = gmm.sample(len(x))
        return s.ravel()

    res = KC03Result(b.source, len(x), round(span, 2),
                     gmm_components=int(gmm.n_components))
    gated = []
    for label, lam in BATTERY.items():
        omega = 2.0 * math.pi / math.log(lam)
        periods = span / math.log(lam)
        entry = {"lambda": round(lam, 4), "omega": round(omega, 3),
                 "periods": round(periods, 2), "gated": bool(periods >= MIN_PERIODS)}
        if entry["gated"]:
            z_obs = _rayleigh(x, omega)
            ps = {}
            for kind in ("lognormal", "kde", "gmm"):
                zn = np.array([_rayleigh(draws(kind), omega) for _ in range(N_NULL)])
                ps[kind] = float((1 + np.sum(zn >= z_obs)) / (N_NULL + 1))
            entry["z"] = round(z_obs, 3)
            entry["p_by_null"] = {k: round(v, 4) for k, v in ps.items()}
            entry["p_max"] = round(max(ps.values()), 4)
            gated.append((label, entry["p_max"]))
        res.battery[label] = entry

    res.n_gated = len(gated)
    if gated:
        res.best_label, res.best_p = min(gated, key=lambda kv: kv[1])
        res.bonferroni_global_p = round(min(1.0, res.best_p * len(gated)), 4)
    res.verdict = (
        f"NULL -- no TFPT log-period is special in the ln E distribution after the "
        f"3-null battery + Bonferroni (global p={res.bonferroni_global_p}, best "
        f"{res.best_label} p={res.best_p}; GMM population null uses "
        f"k={res.gmm_components})" if res.bonferroni_global_p >= 0.05 else
        f"SIZE-SPACE DSI candidate at {res.best_label} (global p="
        f"{res.bonferroni_global_p}) -> escalate-only (needs 2nd source + "
        f"population-structure cross-check)")
    return res

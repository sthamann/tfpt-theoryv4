"""Hierarchical random-effects 95% UPPER LIMIT on the common comb amplitude eps.

The physical SOURCES feeding each channel are independent (a magnetar outburst, a GRB afterglow,
an AGN-disk TDE fade are unrelated astrophysics), but they share the SAME detector/processing
convention. We therefore combine in TWO levels, both as a DerSimonian-Laird random-effects
meta-analysis in comb-POWER (eps^2) space:

  level 1  sources  -> channel   (per-channel eps^2 +/- se, with between-source heterogeneity tau^2)
  level 2  channels -> group     (per-group  eps^2, upper limit)

Random-effects (not a naive product / not fixed-effect) is the honest choice: it inflates the
uncertainty by the excess scatter tau^2 between independent sources, so we never manufacture
significance. For the FINAL group limit we use the Hartung-Knapp-Sidik-Jonkman (HKSJ) t-based
interval, which is the recommended fix when only a few channels are combined -- the plain z-based
random-effects UL is anti-conservative there (verified by the injection coverage check). The
shared detector is a deterministic map (it injects no shared random noise); as a conservative
guard we also expose a cross-channel correlation ``rho`` that inflates the SE by sqrt(1+(k-1)rho).

The 95% one-sided upper limit is ``eps95 = sqrt(max(0, eps^2 + t_crit * se_power))``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import stats

from .kernel import EPS_PREDICTED

Z95 = 1.6448536269514722  # one-sided 95% normal quantile (k=1 fallback)
_SE_FLOOR = 1e-12


@dataclass
class PowerCombine:
    """DerSimonian-Laird random-effects combination of comb-power (eps^2) measurements."""

    k: int
    eps2: float        # combined debiased comb power (~ eps^2)
    se_power: float     # DL random-effects 1 sigma of the combined power
    tau2: float         # between-unit heterogeneity variance
    q_stat: float
    i2: float           # I^2 heterogeneity fraction
    se_hksj: float      # Hartung-Knapp robust SE (>= se_power); == se_power for k<=1
    dof: int            # t degrees of freedom for the HKSJ interval (k-1; 0 -> use z)


def combine_power(eps2_list: list[float], se_list: list[float]) -> PowerCombine:
    """Random-effects combine of (eps2_i, se_power_i) with a Hartung-Knapp robust SE."""
    eps2 = np.asarray(eps2_list, float)
    se = np.maximum(np.asarray(se_list, float), _SE_FLOOR)
    k = int(len(eps2))
    if k == 0:
        return PowerCombine(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)
    if k == 1:
        return PowerCombine(1, float(eps2[0]), float(se[0]), 0.0, 0.0, 0.0, float(se[0]), 0)
    w = 1.0 / se**2
    fe = float(np.sum(w * eps2) / np.sum(w))
    q = float(np.sum(w * (eps2 - fe) ** 2))
    c = float(np.sum(w) - np.sum(w**2) / np.sum(w))
    tau2 = max(0.0, (q - (k - 1)) / c) if c > 0 else 0.0
    w_re = 1.0 / (se**2 + tau2)
    eps2_re = float(np.sum(w_re * eps2) / np.sum(w_re))
    se_re = float(np.sqrt(1.0 / np.sum(w_re)))
    i2 = max(0.0, (q - (k - 1)) / q) if q > 0 else 0.0
    # Hartung-Knapp robust SE (truncated at se_re so it is never anti-conservative).
    q_hk = float(np.sum(w_re * (eps2 - eps2_re) ** 2) / ((k - 1) * np.sum(w_re)))
    se_hksj = max(math.sqrt(max(0.0, q_hk)), se_re)
    return PowerCombine(k, eps2_re, se_re, tau2, q, i2, se_hksj, k - 1)


def upper_limit(comb: PowerCombine, *, rho: float = 0.0, conf: float = 0.95) -> dict:
    """One-sided (HKSJ t-based) 95% UL on the amplitude from a combined power estimate.

    ``eps95`` uses the robust HKSJ SE + a t_{k-1} quantile (few-channel safe); ``eps95_rho`` adds
    the conservative shared-detector SE inflation sqrt(1+(k-1)rho)."""
    if comb.k == 0:
        return {"eps_hat": 0.0, "sigma_amp": 0.0, "eps95": float("nan"),
                "eps95_rho": float("nan"), "t_crit": float("nan")}
    t_crit = float(stats.t.ppf(conf, comb.dof)) if comb.dof >= 1 else Z95
    se_used = comb.se_hksj
    infl = math.sqrt(max(1.0, 1.0 + (comb.k - 1) * rho))
    eps95 = math.sqrt(max(0.0, comb.eps2 + t_crit * se_used))
    eps95_rho = math.sqrt(max(0.0, comb.eps2 + t_crit * se_used * infl))
    amp = power_to_amp(comb.eps2, comb.se_power)
    return {"eps_hat": amp["eps_hat"], "sigma_amp": amp["sigma_amp"],
            "eps95": eps95, "eps95_rho": eps95_rho, "t_crit": t_crit}


def power_to_amp(eps2: float, se_power: float) -> dict:
    """Amplitude point estimate + a continuous, non-degenerate 1 sigma from a power estimate.

    Near eps~0 the amplitude scale of a power uncertainty se_power is sqrt(se_power); away from 0
    it is the standard propagation se_power/(2 eps). We interpolate with the max of the two scales
    in the denominator so the reported sigma never collapses to 0 for a confidently-null channel."""
    eps_hat = float(np.sqrt(max(0.0, eps2)))
    scale = max(eps_hat, math.sqrt(max(0.0, se_power)))
    sigma_amp = se_power / (2.0 * scale) if scale > 0 else 0.0
    return {"eps_hat": eps_hat, "sigma_amp": float(sigma_amp)}


def classify(eps_hat: float, sigma_amp: float, eps95: float,
             eps_pred: float = EPS_PREDICTED) -> str:
    """Honest verdict enum vs the TFPT prediction eps ~ 2%.

    constrains    -- the 95% UL sits BELOW the predicted eps (soft tension for the dynamic kernel);
    consistent    -- a POSITIVE amplitude is measured (>1 sigma from 0) AND is within 1 sigma of
                     the predicted eps (the data actually sits near 2%);
    data_limited  -- the UL is above the predicted eps and no positive comb is measured, so the
                     data cannot yet constrain the prediction.
    """
    if math.isnan(eps95):
        return "data_limited"
    if eps95 < eps_pred:
        return "constrains"
    detected = eps_hat - sigma_amp > 0.0
    if detected and abs(eps_hat - eps_pred) <= max(sigma_amp, 1e-9):
        return "consistent"
    return "data_limited"


@dataclass
class GroupLimit:
    group: str
    channels_used: list[str]
    channels_enumerated: list[str]
    k_channels: int
    eps2: float
    se_power: float
    eps_hat: float
    sigma_amp: float
    eps95: float
    eps95_rho: float
    rho: float
    tau2: float
    i2: float
    t_crit: float
    eps_predicted: float
    verdict: str
    note: str

    def as_dict(self) -> dict:
        d = self.__dict__.copy()
        for key in ("eps2", "se_power", "eps_hat", "sigma_amp", "eps95", "eps95_rho",
                    "tau2", "i2", "t_crit", "eps_predicted"):
            v = float(d[key])
            d[key] = None if math.isnan(v) else round(v, 6)
        return d


def group_limit(group: str, used: list[dict], enumerated: list[str], *, rho: float = 0.3,
                eps_pred: float = EPS_PREDICTED, note: str = "") -> GroupLimit:
    """Combine the usable per-channel power measurements of one group into a 95% UL + verdict.

    ``used`` is a list of per-channel dicts with keys ``key``, ``eps2``, ``se_power``.
    ``enumerated`` lists every channel nominally in the group (used or data-limited).
    """
    keys = [c["key"] for c in used]
    if not used:
        return GroupLimit(group, [], enumerated, 0, 0.0, 0.0, 0.0, 0.0, float("nan"),
                          float("nan"), rho, 0.0, 0.0, float("nan"), eps_pred, "data_limited",
                          note or "no channel in this group yields an absolute eps -> data_limited")
    comb = combine_power([c["eps2"] for c in used], [c["se_power"] for c in used])
    ul = upper_limit(comb, rho=rho)
    verdict = classify(ul["eps_hat"], ul["sigma_amp"], ul["eps95"], eps_pred)
    return GroupLimit(group, keys, enumerated, comb.k, comb.eps2, comb.se_power, ul["eps_hat"],
                      ul["sigma_amp"], ul["eps95"], ul["eps95_rho"], rho, comb.tau2, comb.i2,
                      ul["t_crit"], eps_pred, verdict, note)

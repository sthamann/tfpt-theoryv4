"""HFQPO.H2 — the Boutelier/Barret/Torok selection null (the deflator).

Boutelier et al. 2010 (MNRAS 401, 1290) showed for neutron-star kHz QPOs that ratios of two
LINEARLY CORRELATED frequencies cluster near 3/2 even for a uniform underlying frequency
distribution, because both QPOs are preferentially DETECTED together where their rms
amplitudes are comparable — and Torok 2009 (A&A 497, 661) located that equal-rms crossing at
the 3/2 point. This module implements the preregistered Monte-Carlo of that mechanism for a
5-source BH census:

  * position x ~ U[0,1] along the frequency correlation; nu_l = 100 + 400 x;
  * GR-like monotone ratio r(x) = 2.2 - x  (ratio decreases toward the ISCO, crossing
    3/2 at x = 0.7);
  * detection selection: the *detected* position is drawn N(x_eq, sel_width_x), clipped to
    [0,1] — a sharp window around the equal-rms point x_eq;
  * measurement noise N(0, meas_sigma_r) on the ratio (median published sigma_r).

Statistic: P(>= 4 of 5 sources land within +-0.05 of 3/2). Variants (frozen in the YAML):
  anchored      x_eq = 0.7  — the equal-rms crossing sits AT the 3/2 point (Torok 2009);
  unanchored    x_eq ~ U[0,1] per source per trial — selection point physically unknown;
  no_selection  x ~ U[0,1], no detection weighting at all.

If the anchored variant reproduces the observed 4-of-5 cluster with non-trivial probability,
H1 consistency carries no discriminating weight for TFPT (or for the resonance model).
"""

from __future__ import annotations

from typing import Any

import numpy as np

from tfpt_hfqpo.constants import (
    H2_CLUSTER_K,
    H2_MEAS_SIGMA_R,
    H2_N_MC,
    H2_N_SOURCES,
    H2_RATIO_AT_0,
    H2_RATIO_SLOPE,
    H2_SEED,
    H2_SEL_WIDTH_X,
    H2_WINDOW,
    H2_X_EQ_ANCHORED,
    STEP_F,
)


def _cluster_prob(rng: np.random.Generator, variant: str, n_mc: int) -> dict[str, Any]:
    shape = (n_mc, H2_N_SOURCES)
    if variant == "no_selection":
        x = rng.uniform(0.0, 1.0, shape)
    else:
        x_eq = (np.full(shape, H2_X_EQ_ANCHORED) if variant == "anchored"
                else rng.uniform(0.0, 1.0, shape))
        x = np.clip(x_eq + rng.normal(0.0, H2_SEL_WIDTH_X, shape), 0.0, 1.0)
    r = H2_RATIO_AT_0 + H2_RATIO_SLOPE * x + rng.normal(0.0, H2_MEAS_SIGMA_R, shape)
    near = np.abs(r - STEP_F) <= H2_WINDOW
    n_near = near.sum(axis=1)
    return {
        "variant": variant,
        "p_source_near_3_2": float(near.mean()),
        "p_cluster_4_of_5": float((n_near >= H2_CLUSTER_K).mean()),
        "p_all_5": float((n_near == H2_N_SOURCES).mean()),
    }


def run_selection_null(seed: int = H2_SEED, n_mc: int = H2_N_MC) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    variants = [_cluster_prob(rng, v, n_mc) for v in ("anchored", "unanchored", "no_selection")]
    anchored = variants[0]["p_cluster_4_of_5"]
    return {
        "id": "HFQPO.H2_selection_null",
        "design": {"n_mc": n_mc, "seed": seed, "n_sources": H2_N_SOURCES,
                   "window": H2_WINDOW, "cluster_k": H2_CLUSTER_K,
                   "sel_width_x": H2_SEL_WIDTH_X, "meas_sigma_r": H2_MEAS_SIGMA_R,
                   "nu_l(x)": "100 + 400 x", "ratio(x)": "2.2 - x",
                   "x_eq_anchored": H2_X_EQ_ANCHORED},
        "variants": variants,
        "observed": "4 of 5 published BH pairs within +-0.05 of 3/2 (J1859+226 breaks it)",
        "deflator": {
            "p_anchored_cluster": anchored,
            "reading": ("selection alone reproduces the observed 4-of-5 cluster in "
                        f"{100 * anchored:.0f}% of trials once the equal-rms detection window "
                        "sits at the 3/2 crossing (empirically it does: Torok 2009) — the "
                        "observed clustering does NOT beat the selection null, so it counts "
                        "for nothing on its own")
            if anchored >= 0.01 else
            ("selection rarely manufactures the cluster (p < 0.01) — the observed clustering "
             "would carry weight IF the anchoring assumption failed"),
        },
        "verdict": "consistent",
        "honesty": "this is a null that DEFLATES H1, not a test of TFPT: it quantifies how "
                   "cheap the 3:2 cluster is under pure detection selection",
    }

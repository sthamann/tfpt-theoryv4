"""Synthetic 2D maps for the v2 (2DCS) amendment runs.

Two deterministic peak maps, both preregistered in the hypotheses YAML
(amendment_v2) BEFORE any 2D recovery run:

KA2D_synthetic_e8
    Known-answer E8 2DCS map at the CoNb2O6 scale m1 = 0.16 THz. Every
    coordinate lies inside the 0.6 THz instrument window on BOTH axes; rungs
    7 and 8 enter ONLY through F3 difference coordinates (the mechanism by
    which 2DCS can unlock masses that a 1D low-pass window hides). Two
    off-catalog contaminant peaks are added (generator asserts they are
    > 3 sigma from every catalog entry on the pump axis at the true scale).
    Deterministic 0.5-sigma jitter (seed 0) emulates read-off noise.

NEG2D_localized_limit
    The ACTUAL published 2DCS prediction for CoNb2O6 in the low-field
    localized regime (arXiv:2512.16829, Watanabe/Trebst/Hickey): TFIM+YZ
    localized-limit closed forms with J = 2.48 meV, alpha_yz = 0.226,
    h_plus = J*alpha_yz. Peaks are the folded (omega_tau, omega_t) positions
    of the three Lehmann terms of chi^(3;2)_yyyy with P, R in {eps_-, eps_+}
    and Q in {GS, omega_sym = J, 2eps_-, eps_- + eps_+, 2eps_+, lambda_1,
    lambda_3 = 2J, lambda_5}. This is a NON-E8 spectrum by construction --
    the E8 2D detector must reject it (preregistered negative control).
"""

from __future__ import annotations

import numpy as np

from .ladder import E8_LADDER
from .recover2d import GATE_SIGMA, build_catalog

# --- KA2D: synthetic E8 map at the CoNb2O6 THz scale ------------------------
KA_M1_THZ = 0.16          # CoNb2O6 m1 at 4.75 T (Amelin+ 2020)
KA_WINDOW_THZ = 0.60      # the paper's low-pass window (m7, m8 outside in 1D)
KA_SIGMA_THZ = 0.01       # per-coordinate sigma (same policy as the 1D bed)
KA_JITTER_FRACTION = 0.5  # deterministic jitter, units of sigma (seed 0)
KA_CONTAMINANTS = [(0.352, 0.585), (0.440, 0.205)]   # off-catalog, asserted


def ka2d_map() -> dict:
    """Known-answer E8 2D map (deterministic). Returns peaks, sigmas, truth."""
    m = KA_M1_THZ * E8_LADDER
    entries = [
        # F1 diagonals for the six 1D-window rungs (a = 1..6)
        *[((m[a], m[a]), f"F1({a+1},{a+1})") for a in range(6)],
        # one F2 cross peak (m2, m1)
        ((m[1], m[0]), "F2(2,1)"),
        # rung 7 ONLY via F3(6, |6-7|); rung 8 ONLY via F3(5, |5-8|)
        ((m[5], abs(m[5] - m[6])), "F3(6,|6-7|)"),
        ((m[4], abs(m[4] - m[7])), "F3(5,|5-8|)"),
    ]
    coords = np.array([c for c, _ in entries])
    labels = [lab for _, lab in entries]
    assert np.all(coords <= KA_WINDOW_THZ), "KA map must respect the window"

    # contaminants: assert off-catalog on the pump axis at the true scale
    cat = build_catalog(E8_LADDER)
    cat_tau = np.unique(KA_M1_THZ * cat.xy[:, 0])
    for cx, cy in KA_CONTAMINANTS:
        assert np.min(np.abs(cat_tau - cx)) > GATE_SIGMA * KA_SIGMA_THZ, \
            f"contaminant {cx} too close to a catalog pump-axis value"
        assert max(cx, cy) <= KA_WINDOW_THZ

    rng = np.random.default_rng(0)
    jitter = KA_JITTER_FRACTION * KA_SIGMA_THZ * rng.standard_normal(coords.shape)
    peaks = np.vstack([coords + jitter, np.array(KA_CONTAMINANTS)])
    labels = labels + ["contaminant_1", "contaminant_2"]
    sigmas = np.full(len(peaks), KA_SIGMA_THZ)
    return {
        "peaks": peaks, "sigmas": sigmas, "labels_reporting_only": labels,
        "unit": "THz", "m1_true": KA_M1_THZ, "window": KA_WINDOW_THZ,
        "provenance": ("synthetic known-answer map; E8 ratios exact "
                       "(ladder.py, bit-frozen), m1 = 0.16 THz per Amelin+ "
                       "PRB 102, 104431; 0.5-sigma deterministic jitter seed 0"),
    }


# --- NEG2D: localized-limit closed forms (arXiv:2512.16829) ------------------
NEG_J_MEV = 2.48          # Woodland+ PRB 108, 184417 parametrization
NEG_ALPHA_YZ = 0.226
NEG_SIGMA_MEV = 0.05      # conservative read-off sigma
NEG_DEDUP_MEV = 1e-6


def neg2d_map() -> dict:
    """Localized-limit 2DCS peak map of CoNb2O6 (analytic, non-E8)."""
    J, h_plus = NEG_J_MEV, NEG_J_MEV * NEG_ALPHA_YZ
    eps = [J - np.sqrt(2) * h_plus, J + np.sqrt(2) * h_plus]     # eps_-, eps_+
    q_states = {
        "GS": 0.0,
        "omega_sym_J": J,
        "2eps_minus": 2 * eps[0],
        "eps_minus_plus_eps_plus": eps[0] + eps[1],
        "2eps_plus": 2 * eps[1],
        "lambda_1": 2 * J - np.sqrt(3) * h_plus,
        "lambda_3": 2 * J,
        "lambda_5": 2 * J + np.sqrt(3) * h_plus,
    }
    raw: list[tuple[float, float, str]] = []
    for wp in eps:
        for wr in eps:
            for qname, wq in q_states.items():
                d = abs(wp - wq)
                raw.append((wp, d, f"t1 P={wp:.3f} Q={qname}"))
                raw.append((wr, d, f"t2 R={wr:.3f} Q={qname}"))
            raw.append((wp, wr, f"t3 P={wp:.3f} R={wr:.3f}"))
    peaks, labels = [], []
    for x, y, lab in raw:
        if y < NEG_DEDUP_MEV:      # zero-frequency rectification line: skip
            continue
        if not any(abs(x - px) < NEG_DEDUP_MEV and abs(y - py) < NEG_DEDUP_MEV
                   for px, py in peaks):
            peaks.append((x, y))
            labels.append(lab)
    peaks = np.array(peaks)
    sigmas = np.full(len(peaks), NEG_SIGMA_MEV)
    return {
        "peaks": peaks, "sigmas": sigmas, "labels_reporting_only": labels,
        "unit": "meV",
        "eps_minus_mev": eps[0], "eps_plus_mev": eps[1],
        "q_states_mev": {k: float(v) for k, v in q_states.items()},
        "provenance": ("analytic localized-limit closed forms, "
                       "arXiv:2512.16829 Sec. IV.3: eps_pm = J +/- sqrt(2)h+, "
                       "tetraquarks 2J +/- sqrt(3)h+, 2J +/- h+, 2J; "
                       "J = 2.48 meV, alpha_yz = 0.226, h+ = J*alpha_yz"),
    }

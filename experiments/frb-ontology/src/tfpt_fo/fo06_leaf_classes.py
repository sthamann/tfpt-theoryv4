"""FO.06 -- repeater/one-off dichotomy as Z2 leaf classes (diagnostic).

Prediction: exactly TWO morphological modes in (log width, log bandwidth) on the
only uniform-survey catalog (CHIME Cat1), and first-detection morphology aligns
with the repeater label. Prime-2 diagnostic; a hit is DEFAULT astro
(selection/exposure; Pleunis+2021) -- consistency typing only, never support.

  (i)  GMM BIC scan k = 1..4 -> prediction k = 2;
  (ii) 5-fold CV logistic AUC (repeater label from morphology) vs label
       permutation null;
  (iii) repeater fraction per GMM mode (odds ratio).
"""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

from .data import Cat1

N_LABEL_PERM = 1000


def _cv_auc(x: np.ndarray, y: np.ndarray, seed: int) -> float:
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    scores = np.zeros(len(y))
    for tr, te in skf.split(x, y):
        m = LogisticRegression(max_iter=1000).fit(x[tr], y[tr])
        scores[te] = m.predict_proba(x[te])[:, 1]
    return float(roc_auc_score(y, scores))


def run(cat: Cat1, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    x = np.stack([cat.log_width, cat.log_bw], axis=1)
    y = cat.is_repeater.astype(int)
    n, n_rep = len(y), int(y.sum())

    if n < 100 or n_rep < 10:
        return {"axis": "FO.06_leaf_classes", "n": n, "n_repeater_bursts": n_rep,
                "verdict": "data_limited",
                "note": "too few clean first sub-bursts after the flag gates"}

    # (i) mode count
    bic = {}
    for k in range(1, 5):
        g = GaussianMixture(n_components=k, covariance_type="full",
                            random_state=seed, n_init=5).fit(x)
        bic[k] = float(g.bic(x))
    best_k = int(min(bic, key=bic.get))

    # (iii) two-mode alignment with the repeater label
    g2 = GaussianMixture(n_components=2, covariance_type="full",
                         random_state=seed, n_init=5).fit(x)
    lab = g2.predict(x)
    frac = [float(y[lab == j].mean()) if np.any(lab == j) else np.nan for j in (0, 1)]
    counts = [int(np.sum(lab == j)) for j in (0, 1)]
    a = max(frac[0], 1e-6) / max(1 - frac[0], 1e-6)
    b = max(frac[1], 1e-6) / max(1 - frac[1], 1e-6)
    odds_ratio = float(max(a, b) / min(a, b))

    # (ii) morphology predicts the label
    auc_obs = _cv_auc(x, y, seed)
    auc_null = np.empty(N_LABEL_PERM)
    for i in range(N_LABEL_PERM):
        auc_null[i] = _cv_auc(x, rng.permutation(y), seed)
    p_auc = float((1 + np.sum(auc_null >= auc_obs)) / (N_LABEL_PERM + 1))

    pred_two_modes = best_k == 2
    pred_label = p_auc < 0.01
    if pred_two_modes and pred_label:
        verdict = "consistent"
        note = ("two morphological modes + label alignment (replicates Pleunis+2021; "
                "default reading: astro/selection, not TFPT support)")
    elif pred_label and not pred_two_modes:
        verdict = "not_confirmed_not_refuted"
        note = f"morphology predicts repetition but BIC prefers k={best_k}, not 2"
    else:
        verdict = "null"
        note = "the leaf-class reading fails on the uniform-survey catalog"

    return {
        "axis": "FO.06_leaf_classes",
        "n_first_subbursts": n,
        "n_repeater": n_rep,
        "n_flagged_out": cat.n_flagged_out,
        "bic_by_k": {str(k): round(v, 1) for k, v in bic.items()},
        "best_k": best_k,
        "gmm2_mode_sizes": counts,
        "gmm2_repeater_fraction_per_mode": [round(f, 4) for f in frac],
        "odds_ratio": round(odds_ratio, 2),
        "auc_cv": round(auc_obs, 4),
        "auc_null_mean": round(float(auc_null.mean()), 4),
        "p_auc_perm": p_auc,
        "caveats_on_record": ["bandwidth censored at the 400-800 MHz band",
                              "exposure/beam selection uncorrected"],
        "verdict": verdict,
        "note": note,
    }

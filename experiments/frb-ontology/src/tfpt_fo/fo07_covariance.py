"""FO.07 -- character-class BLOCK structure in the burst observable covariance.

S8 language applied to data: if transfer/mu4 character classes leak into the
observables at all, they should appear as block-diagonality of the
observable-observable correlation matrix (within-block strong, between-block
near zero) -- a state invariance rather than a visible number. No contract
names the observable-to-character assignment, so the test is for UNEXPECTED
block structure relative to a spectrum-preserving random-rotation null; the
found partition is reported, never interpreted as confirmation.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import ortho_group
from sklearn.cluster import SpectralClustering

from .data import PolCatalog, sessions

MIN_SESSION = 20
K_GRID = (2, 3, 4)
N_NULL = 500

# v1.3.1 escalation control (dated addendum, after the first run fired at
# Bonferroni p = 0.006): the STANDARD-PHYSICS sector split every magnetospheric/
# propagation model already predicts -- Faraday/geometry observables vs
# emission/intensity observables. A significant block structure whose partition
# coincides with this split carries no character-class content (default astro).
PHYS_SECTOR = frozenset({"DOC", "cos2PA", "sin2PA", "RM_res"})


def observable_matrix(cat: PolCatalog) -> tuple[np.ndarray, list[str]]:
    """Per-burst 10-observable matrix, robustly standardised within session."""
    names = ["log10Weff", "log10BW", "log10SNR", "DOL", "DOC",
             "cos2PA", "sin2PA", "RM_res", "DM_res", "log10Wait"]
    # reconstruct auxiliary columns not stored on PolCatalog
    import csv
    from .data import POL_CSV, _f
    bw, snr = {}, {}
    with POL_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            m = _f(r, "MJD_topo")
            if np.isfinite(m):
                bw[round(m, 9)] = _f(r, "Bandwidth(MHz)")
                snr[round(m, 9)] = _f(r, "S/N")
    rows = []
    for idx in sessions(cat.mjd):
        if idx.size < MIN_SESSION:
            continue
        t = cat.mjd[idx]
        wait = np.concatenate([[np.nan], np.diff(t) * 86400.0])
        pa = np.deg2rad(2.0 * cat.pa_deg[idx])
        block = np.column_stack([
            np.log10(np.where(cat.weff_ms[idx] > 0, cat.weff_ms[idx], np.nan)),
            np.log10([bw.get(round(m, 9), np.nan) for m in t]),
            np.log10([max(snr.get(round(m, 9), np.nan), 1e-9) for m in t]),
            cat.dol[idx], cat.doc[idx],
            np.cos(pa), np.sin(pa),
            cat.rm[idx] - np.nanmedian(cat.rm[idx]),
            cat.dm[idx] - np.nanmedian(cat.dm[idx]),
            np.log10(np.where(wait > 0, wait, np.nan)),
        ])
        # robust within-session standardisation (kills session-level drift)
        med = np.nanmedian(block, axis=0)
        mad = np.nanmedian(np.abs(block - med), axis=0) * 1.4826
        mad = np.where(mad < 1e-9, np.nan, mad)
        rows.append((block - med) / mad)
    X = np.vstack(rows)
    X = X[np.all(np.isfinite(X), axis=1)]
    return X, names


def _s_off(C: np.ndarray, labels: np.ndarray) -> float:
    off = ~np.eye(len(C), dtype=bool)
    between = labels[:, None] != labels[None, :]
    denom = float((C[off] ** 2).sum())
    return float((C[off & between] ** 2).sum() / max(denom, 1e-12))


def _best_partition(C: np.ndarray, k: int, seed: int) -> tuple[np.ndarray, float]:
    aff = np.abs(C)
    np.fill_diagonal(aff, 1.0)
    sc = SpectralClustering(n_clusters=k, affinity="precomputed",
                            random_state=seed, n_init=20)
    labels = sc.fit_predict(aff)
    return labels, _s_off(C, labels)


def _random_corr_same_spectrum(rng_seed: int, eigvals: np.ndarray) -> np.ndarray:
    Q = ortho_group.rvs(len(eigvals), random_state=rng_seed)
    M = Q @ np.diag(eigvals) @ Q.T
    d = np.sqrt(np.clip(np.diag(M), 1e-12, None))
    return M / np.outer(d, d)


def run(cat: PolCatalog, seed: int = 0) -> dict:
    X, names = observable_matrix(cat)
    C = np.corrcoef(X, rowvar=False)
    eig = np.linalg.eigvalsh(C)

    per_k = {}
    for k in K_GRID:
        labels, s_obs = _best_partition(C, k, seed)
        null = np.empty(N_NULL)
        for i in range(N_NULL):
            Cn = _random_corr_same_spectrum(seed * 1000 + 7 * i + k, eig)
            _, null[i] = _best_partition(Cn, k, seed)
        p = float((1 + np.sum(null <= s_obs)) / (N_NULL + 1))
        per_k[k] = {"s_off": round(s_obs, 4),
                    "null_median": round(float(np.median(null)), 4),
                    "p": p,
                    "blocks": [[names[i] for i in np.where(labels == j)[0]]
                               for j in range(k)]}

    p_bonf = min(1.0, min(v["p"] for v in per_k.values()) * len(K_GRID))

    # escalation: does the best k=2 partition just reproduce the known
    # physics sectors? Rand agreement over observable pairs.
    lab2, _ = _best_partition(C, 2, seed)
    phys = np.array([n in PHYS_SECTOR for n in names])
    same_found = lab2[:, None] == lab2[None, :]
    same_phys = phys[:, None] == phys[None, :]
    iu = np.triu_indices(len(names), k=1)
    rand_agreement = float(np.mean(same_found[iu] == same_phys[iu]))

    if p_bonf >= 0.05:
        verdict = "null"
        note = ("no unexpected block-diagonality beyond the spectrum-preserving "
                "null -> no visible character-class protection in the burst covariance")
    elif rand_agreement >= 0.9:
        verdict = "consistent"
        note = ("block structure real (beats the spectrum-preserving null) but the "
                "partition coincides with the STANDARD propagation/geometry-vs-"
                "emission sector split (Rand agreement "
                f"{rand_agreement:.2f}) -> default astro, no character-class "
                "content; the flagged first-run hint stays on record (v1.3.1)")
    else:
        verdict = "hint_flag"
        note = "escalate-only; partition reported, never confirmation"

    return {"axis": "FO.07_covariance_blocks",
            "n_bursts_complete": int(len(X)),
            "n_observables": len(names),
            "corr_extremes": {"max_abs_offdiag": round(float(
                np.max(np.abs(C - np.eye(len(C))))), 3)},
            "per_k": {str(k): v for k, v in per_k.items()},
            "bonferroni_p": p_bonf,
            "physics_partition_rand_agreement": round(rand_agreement, 3),
            "verdict": verdict,
            "note": note}

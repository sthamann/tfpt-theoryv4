"""FO.09 -- effective RANK of delay-embedded burst dynamics ('rank falls to 3').

If the dynamics live on a protected Perron mode + two decay modes, the
delay-embedded within-session dynamics should have effective rank <= 3 --
'not 2, not 5, not continuous'. Field-near and emission-agnostic; KC.06/FO.02b
constrain the FRB medium observables to little/no memory, so rank 0/1
(memoryless / single memory) is an expected honest outcome.

Per session: Hankel matrix (delay depth 8) of the standardised series;
sigma_k significant if above the 95th percentile of 200 within-session shuffle
surrogates (which preserve the marginal, destroy temporal structure).
Effective rank = largest significant k; source rank = median over sessions.
"""

from __future__ import annotations

import numpy as np

from .data import SourceBursts, sessions

DEPTH = 8
MIN_SESSION = 40
N_SURR = 200


def _hankel_sv(x: np.ndarray, depth: int) -> np.ndarray:
    n = len(x) - depth + 1
    H = np.lib.stride_tricks.sliding_window_view(x, depth)[:n].T
    return np.linalg.svd(H, compute_uv=False)


def _session_rank(rng: np.random.Generator, x: np.ndarray) -> int:
    x = (x - np.mean(x)) / max(np.std(x), 1e-12)
    sv = _hankel_sv(x, DEPTH)
    null = np.empty((N_SURR, len(sv)))
    for i in range(N_SURR):
        null[i] = _hankel_sv(rng.permutation(x), DEPTH)
    thresh = np.percentile(null, 95, axis=0)
    sig = sv > thresh
    return int(np.max(np.where(sig)[0]) + 1) if sig.any() else 0


def _source_rank(rng: np.random.Generator, sb: SourceBursts) -> dict | None:
    e = sb.energy
    if e is None:
        return None
    ranks = []
    for idx in sessions(sb.mjd):
        x = e[idx]
        ok = np.isfinite(x) & (x > 0)
        if ok.sum() < MIN_SESSION:
            continue
        ranks.append(_session_rank(rng, np.log10(x[ok])))
    if not ranks:
        return None
    return {"source": sb.source, "n_sessions": len(ranks),
            "ranks": ranks, "median_rank": float(np.median(ranks)),
            "max_rank": int(max(ranks))}


def run_energy(sources: list[SourceBursts], seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    per = [r for sb in sources if (r := _source_rank(rng, sb))]
    meds = [r["median_rank"] for r in per]
    if not per:
        verdict, note = "data_limited", "no session clears the gates"
    elif all(m <= 1 for m in meds):
        verdict = "null"
        note = ("median effective rank <= 1 in every source -> memoryless/"
                "single-memory burst-energy dynamics; no multi-mode (rank-3) "
                "structure visible (consistent with the FO.01 amplifier)")
    elif any(m >= 4 for m in meds):
        verdict = "tension"
        note = "effective rank >= 4 -> kills the 3-mode reading in that source"
    elif all(2.5 <= m <= 3.5 for m in meds) and len(per) >= 2:
        verdict = "hint_flag"
        note = "rank ~3 in >= 2 sources -> escalate-only"
    else:
        verdict = "not_confirmed_not_refuted"
        note = "mixed ranks; no replicated 3-mode structure"
    return {"axis": "FO.09_rank_drop", "per_source": per,
            "verdict": verdict, "note": note}


def run_medium(rng_seed: int, mjd: np.ndarray, obs: dict[str, np.ndarray]) -> dict:
    """(b) leg: multivariate v5 medium state, lag-embedded depth 4."""
    rng = np.random.default_rng(rng_seed)
    ranks = []
    for idx in sessions(mjd):
        cols = []
        for v in obs.values():
            x = v[idx]
            if np.isfinite(x).sum() >= 30:
                med = np.nanmedian(x)
                mad = np.nanmedian(np.abs(x - med)) * 1.4826
                cols.append((x - med) / max(mad, 1e-9))
        if len(cols) < 2:
            continue
        X = np.column_stack(cols)
        keep = np.all(np.isfinite(X), axis=1)
        X = X[keep]
        if len(X) < MIN_SESSION:
            continue
        depth = 4
        n = len(X) - depth + 1
        H = np.hstack([X[i:i + n] for i in range(depth)]).T
        sv = np.linalg.svd(H, compute_uv=False)
        null = np.empty((N_SURR // 2, len(sv)))
        for i in range(N_SURR // 2):
            Xp = X[rng.permutation(len(X))]
            Hp = np.hstack([Xp[i2:i2 + n] for i2 in range(depth)]).T
            null[i] = np.linalg.svd(Hp, compute_uv=False)
        sig = sv > np.percentile(null, 95, axis=0)
        ranks.append(int(np.max(np.where(sig)[0]) + 1) if sig.any() else 0)
    return {"n_sessions": len(ranks), "ranks": ranks,
            "median_rank": float(np.median(ranks)) if ranks else None,
            "note": ("DESCRIPTIVE ONLY: static cross-observable correlations "
                     "(the FO.07 sector structure) enter the multivariate "
                     "embedding, so these ranks conflate instantaneous "
                     "correlation rank with dynamics -- given the FO.02b "
                     "no-memory result they are NOT evidence of 3-mode "
                     "dynamics; the clean dynamics leg is the scalar energy one")}

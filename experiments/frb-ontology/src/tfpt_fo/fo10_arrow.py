"""FO.10 -- causal asymmetry (time arrow) in within-session energy sequences.

The retarded seed / recovery direction implies an arrow: forward and backward
reconstruction inequivalent as operator structure. Preregistered caveat:
irreversibility is generic in driven/dissipative systems -- a hit types as
'irreversible cascade physics', never TFPT support. The informative outcomes
are the NULL (reversible => memoryless/linear-Gaussian, consistent with the
FO.01 amplifier) and the direction typing.

Statistics (pooled over sessions, per source; both sign-odd under time
reversal, so the random per-session reversal null is exact under H0):
  (i)  skewness of increments dx;
  (ii) Pomeau asymmetry A = <x_t x_{t+1}^2> - <x_t^2 x_{t+1}>.
"""

from __future__ import annotations

import numpy as np

from .data import SourceBursts, sessions

MIN_SESSION = 20
N_REV = 2000


def _session_series(sb: SourceBursts) -> list[np.ndarray]:
    out = []
    if sb.energy is None:
        return out
    for idx in sessions(sb.mjd):
        x = sb.energy[idx]
        ok = np.isfinite(x) & (x > 0)
        if ok.sum() >= MIN_SESSION:
            z = np.log10(x[ok])
            out.append((z - z.mean()) / max(z.std(), 1e-12))
    return out


def _stats(series: list[np.ndarray]) -> tuple[float, float]:
    d = np.concatenate([np.diff(z) for z in series])
    skew = float(np.mean(d ** 3) / max(np.mean(d ** 2) ** 1.5, 1e-12))
    a = float(np.mean(np.concatenate(
        [z[:-1] * z[1:] ** 2 - z[:-1] ** 2 * z[1:] for z in series])))
    return skew, a


def run(sources: list[SourceBursts], seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    per, ps = [], []
    for sb in sources:
        series = _session_series(sb)
        if len(series) < 3:
            continue
        skew_obs, a_obs = _stats(series)
        null = np.empty((N_REV, 2))
        for i in range(N_REV):
            flipped = [z[::-1] if rng.random() < 0.5 else z for z in series]
            null[i] = _stats(flipped)
        p_skew = float((1 + np.sum(np.abs(null[:, 0]) >= abs(skew_obs))) / (N_REV + 1))
        p_a = float((1 + np.sum(np.abs(null[:, 1]) >= abs(a_obs))) / (N_REV + 1))
        per.append({"source": sb.source, "n_sessions": len(series),
                    "n_increments": int(sum(len(z) - 1 for z in series)),
                    "increment_skewness": round(skew_obs, 4), "p_skew": p_skew,
                    "pomeau_A": round(a_obs, 5), "p_pomeau": p_a})
        ps.extend([p_skew, p_a])

    n_tests = len(ps)
    p_bonf = min(1.0, min(ps) * n_tests) if ps else None
    if p_bonf is None:
        verdict, note = "data_limited", "no source clears the gates"
    elif p_bonf < 0.05:
        verdict = "consistent"
        note = ("time arrow present (generic irreversible cascade physics -- "
                "typed consistency with ANY directed relaxation incl. TFPT, "
                "never support; direction reported)")
    else:
        verdict = "null"
        note = ("within-session energy sequences are time-reversible at catalog "
                "statistics -> an arrow-free cascade; bounds every 'directed "
                "recovery' reading of burst trains")
    return {"axis": "FO.10_causal_asymmetry", "per_source": per,
            "bonferroni_p": p_bonf, "n_tests": n_tests,
            "open_control": "earthquake aftershocks (known irreversible) not run -- USGS data gitignored, on record",
            "verdict": verdict, "note": note}

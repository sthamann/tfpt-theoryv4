"""PG.02 / PG.03 -- per-pulsar kernel ladders in glitch *sizes* and *waiting times*.

The cross-domain claim of ``problem_1.txt`` is that the *same* boundary-recovery
kernel ``{1, (2/3)^6, (1/3)^6}`` (step ``3/2``) governs FRB sub-burst echoes, GW
ringdown echoes and pulsar-glitch recovery.  For a multi-glitch pulsar this means
consecutive glitch sizes should step by kernel factors:

    PG.02   |log10(s_{i+1}/s_i)|  piles up near  {log 3/2, log (3/2)^3, log (3/2)^6}
    PG.03   waiting-time ratios   pile up near the same comb / candidate ratios

Both are calibrated with a **within-pulsar shuffle null** (permute the per-pulsar
values, keeping each pulsar's own size/interval *set* but destroying the step
ordering), so a detection cannot be faked by the global size distribution.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .catalog import GlitchRecord, by_pulsar
from .constants import kernel_log_ratios


def _consecutive_log_size_ratios(series: list[GlitchRecord]) -> list[float]:
    s = [r.df_f for r in series if r.df_f is not None and r.df_f > 0]
    return [abs(np.log10(s[i + 1] / s[i])) for i in range(len(s) - 1)]


def _consecutive_waiting_ratios(series: list[GlitchRecord]) -> list[float]:
    t = [r.mjd for r in series if r.mjd is not None]
    dt = [t[i + 1] - t[i] for i in range(len(t) - 1) if t[i + 1] > t[i]]
    return [abs(np.log10(dt[i + 1] / dt[i])) for i in range(len(dt) - 1)]


def _nearest_tooth_frac(log_ratios: np.ndarray, teeth: np.ndarray,
                        tol_dex: float) -> float:
    """Fraction of |log-ratio| values within ``tol_dex`` of any kernel tooth."""
    if len(log_ratios) == 0:
        return 0.0
    d = np.abs(log_ratios[:, None] - teeth[None, :]).min(axis=1)
    return float(np.mean(d <= tol_dex))


@dataclass
class LadderResult:
    channel: str            # "size" (PG.02) or "waiting" (PG.03)
    n_pulsars: int
    n_ratios: int
    teeth_dex: list[float]
    tol_dex: float
    frac_on_comb: float     # observed fraction within tol of a kernel tooth
    null_mean: float
    p_value: float          # P(shuffle fraction >= observed)
    verdict: str


def _ladder_test(per_pulsar_logratios: list[list[float]], *, channel: str,
                 teeth: np.ndarray, tol_dex: float = 0.05,
                 n_shuffle: int = 2000, seed: int = 0) -> LadderResult:
    pooled = np.array([v for lst in per_pulsar_logratios for v in lst], dtype=float)
    n_pulsars = sum(1 for lst in per_pulsar_logratios if lst)
    obs = _nearest_tooth_frac(pooled, teeth, tol_dex)

    rng = np.random.default_rng(seed)
    null = np.empty(n_shuffle)
    for k in range(n_shuffle):
        shuffled: list[float] = []
        for lst in per_pulsar_logratios:
            if not lst:
                continue
            # a within-pulsar shuffle of the SIGNED steps is equivalent to a
            # random reordering of |log-ratios|; resampling with replacement from
            # the pulsar's own values preserves its set, destroys the step comb
            v = np.array(lst)
            shuffled.extend(rng.permutation(v).tolist())
        null[k] = _nearest_tooth_frac(np.array(shuffled), teeth, tol_dex)
    null_mean = float(np.mean(null))
    p = float((1 + np.sum(null >= obs)) / (n_shuffle + 1))
    verdict = (f"{channel} ladder ON kernel comb (frac={obs:.2f} vs null "
               f"{null_mean:.2f}, p={p:.3f})" if p < 0.05 else
               f"{channel} ladder consistent with shuffle (frac={obs:.2f} vs "
               f"null {null_mean:.2f}, p={p:.3f}) -- no kernel comb")
    return LadderResult(channel, n_pulsars, len(pooled),
                        teeth.tolist(), tol_dex, obs, null_mean, p, verdict)


def size_ratio_ladder(records: list[GlitchRecord], *, min_glitches: int = 3,
                      tol_dex: float = 0.05, n_shuffle: int = 2000,
                      seed: int = 0) -> LadderResult:
    """PG.02 -- consecutive glitch-size ratios vs the kernel log-comb."""
    groups = by_pulsar(records)
    teeth = np.array(list(kernel_log_ratios().values()))
    per_pulsar = [_consecutive_log_size_ratios(g) for g in groups.values()
                  if sum(1 for r in g if r.df_f) >= min_glitches]
    return _ladder_test(per_pulsar, channel="size", teeth=teeth, tol_dex=tol_dex,
                        n_shuffle=n_shuffle, seed=seed)


def waiting_ratio_ladder(records: list[GlitchRecord], *, min_glitches: int = 4,
                         tol_dex: float = 0.05, n_shuffle: int = 2000,
                         seed: int = 0) -> LadderResult:
    """PG.03 -- consecutive inter-glitch waiting-time ratios vs the kernel comb."""
    groups = by_pulsar(records)
    teeth = np.array(list(kernel_log_ratios().values()))
    per_pulsar = [_consecutive_waiting_ratios(g) for g in groups.values()
                  if sum(1 for r in g if r.mjd) >= min_glitches]
    return _ladder_test(per_pulsar, channel="waiting", teeth=teeth, tol_dex=tol_dex,
                        n_shuffle=n_shuffle, seed=seed)


def prolific_glitchers(records: list[GlitchRecord], top: int = 10) -> list[tuple[str, int]]:
    """The most-glitching pulsars (context for the ladder tests)."""
    groups = by_pulsar(records)
    counts = sorted(((k, len(v)) for k, v in groups.items()),
                    key=lambda kv: kv[1], reverse=True)
    return counts[:top]

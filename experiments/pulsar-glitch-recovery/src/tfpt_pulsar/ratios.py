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


def _log_ratios(values: list[float]) -> list[float]:
    """Consecutive ``|log10|`` step ratios of an *ordered* value sequence.

    The ordering matters: the result depends on which value follows which, so a
    reordering of ``values`` yields a genuinely different multiset of ratios (this
    is what makes the within-pulsar shuffle null non-trivial).
    """
    return [abs(np.log10(values[i + 1] / values[i])) for i in range(len(values) - 1)]


def _per_pulsar_sizes(series: list[GlitchRecord]) -> list[float]:
    """Time-ordered positive glitch sizes ``Delta nu / nu`` for one pulsar."""
    return [r.df_f for r in series if r.df_f is not None and r.df_f > 0]


def _per_pulsar_waiting_times(series: list[GlitchRecord]) -> list[float]:
    """Time-ordered positive inter-glitch waiting intervals for one pulsar."""
    t = [r.mjd for r in series if r.mjd is not None]
    return [t[i + 1] - t[i] for i in range(len(t) - 1) if t[i + 1] > t[i]]


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


def _ladder_test(per_pulsar_values: list[list[float]], *, channel: str,
                 teeth: np.ndarray, tol_dex: float = 0.05,
                 n_shuffle: int = 2000, seed: int = 0) -> LadderResult:
    # Observation: consecutive log-ratios taken in the recorded (chronological)
    # order, pooled across pulsars.
    obs_logratios = [_log_ratios(v) for v in per_pulsar_values]
    pooled = np.array([r for lst in obs_logratios for r in lst], dtype=float)
    n_pulsars = sum(1 for lst in obs_logratios if lst)
    obs = _nearest_tooth_frac(pooled, teeth, tol_dex)

    # Within-pulsar shuffle null: permute each pulsar's RAW size/interval sequence
    # (keeping its value *set* intact) and RECOMPUTE the consecutive log-ratios.
    # The test statistic is order-invariant, so permuting the already-computed
    # |log-ratios| would leave the pooled multiset unchanged and reproduce the
    # observation exactly (p == 1 by construction); reordering the raw values
    # before differencing is what actually breaks the step comb.
    rng = np.random.default_rng(seed)
    null = np.empty(n_shuffle)
    for k in range(n_shuffle):
        shuffled: list[float] = []
        for v in per_pulsar_values:
            if len(v) < 2:
                continue
            perm = rng.permutation(np.asarray(v, dtype=float))
            shuffled.extend(_log_ratios(perm.tolist()))
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
    per_pulsar = [_per_pulsar_sizes(g) for g in groups.values()
                  if sum(1 for r in g if r.df_f) >= min_glitches]
    return _ladder_test(per_pulsar, channel="size", teeth=teeth, tol_dex=tol_dex,
                        n_shuffle=n_shuffle, seed=seed)


def waiting_ratio_ladder(records: list[GlitchRecord], *, min_glitches: int = 4,
                         tol_dex: float = 0.05, n_shuffle: int = 2000,
                         seed: int = 0) -> LadderResult:
    """PG.03 -- consecutive inter-glitch waiting-time ratios vs the kernel comb."""
    groups = by_pulsar(records)
    teeth = np.array(list(kernel_log_ratios().values()))
    per_pulsar = [_per_pulsar_waiting_times(g) for g in groups.values()
                  if sum(1 for r in g if r.mjd) >= min_glitches]
    return _ladder_test(per_pulsar, channel="waiting", teeth=teeth, tol_dex=tol_dex,
                        n_shuffle=n_shuffle, seed=seed)


def prolific_glitchers(records: list[GlitchRecord], top: int = 10) -> list[tuple[str, int]]:
    """The most-glitching pulsars (context for the ladder tests)."""
    groups = by_pulsar(records)
    counts = sorted(((k, len(v)) for k, v in groups.items()),
                    key=lambda kv: kv[1], reverse=True)
    return counts[:top]

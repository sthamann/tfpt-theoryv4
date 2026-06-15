"""FRB.09 -- recovery-clock dynamics (the *time* structure of boundary recovery).

All earlier axes test the recovery kernel's *eigenvalues* (the ratios 64/729,
8/27, 2/3, ...). This axis tests the kernel's **dynamics** -- the one structure
the Origin Theory adds that no ratio test captures (verification ``v124``):

    rate(n) = -p2 * ln(1 - n/N_fam),   p2 = 6, N_fam = 3      (the resummed clock)

It makes two predictions that are *firewall-compliant* (residual boundary-recovery
dynamics, NOT a direct horizon/Hawking signature) and not encoded in FRB.01-FRB.08:

  (A) THE WALL.  The clock diverges at n = N_fam = 3, so a recovery cascade has at
      most N_fam = 3 elements (2 steps). A *monotone-decay* burst run (a discharge
      relaxing through the kernel) must therefore be CAPPED at length 3 -- long
      decreasing-energy cascades should be SUPPRESSED relative to a within-session
      energy shuffle.
  (B) THE ACCELERATION.  Within a 3-burst cascade the relaxation accelerates,
      rate(1)=6 ln(3/2)=2.433, rate(2)=6 ln 3=6.592, so the inter-burst gaps obey
          g1/g2 = rate(2)/rate(1) = ln 3 / ln(3/2) = 2.7095
      (the first gap ~2.7x longer than the second). We test for an excess of
      decreasing-energy triplets with that gap ratio, calibrated against a
      within-session energy shuffle AND a placebo of arbitrary (non-clock) ratios.

Both are honest *search targets*. A clean null means the recovery clock leaves no
trace in the burst timing -- exactly the kind of negative the firewall expects.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .data_io import RepeaterSeries
from .recovery_kernel import CYCLE  # p2 = 6 (Z6/A3 transport exponent)
from .tfpt_ladder import N_FAM  # = 3

P2 = CYCLE


def _clock_rate(n: int, n_fam: int = N_FAM, p2: int = P2) -> float:
    """The resummed recovery-clock rate at step n (v124)."""
    return -p2 * math.log(1.0 - n / n_fam)


# g1/g2 = rate(2)/rate(1) = ln(N/(N-2)) / ln(N/(N-1))  (independent of p2)
CLOCK_GAP_RATIO: float = _clock_rate(2) / _clock_rate(1)        # 2.7095 for N_fam=3
LOG_CLOCK_GAP: float = math.log10(CLOCK_GAP_RATIO)
WALL_LEN: int = N_FAM                                           # max cascade length (elements)


def _session_sequences(series: RepeaterSeries):
    """Per session: (energy, mjd) arrays time-ordered, finite, >0, length>=3."""
    val = series.energy if np.isfinite(series.energy).sum() else series.fluence
    if not np.isfinite(val).sum():
        return []
    sess = series.session_id if series.session_id.size else np.zeros(len(series.mjd))
    mjd = series.mjd
    out = []
    for s in np.unique(sess):
        m = sess == s
        v, t = np.asarray(val)[m], np.asarray(mjd)[m]
        ok = np.isfinite(v) & (v > 0) & np.isfinite(t)
        v, t = v[ok], t[ok]
        if len(v) < 3:
            continue
        order = np.argsort(t)
        out.append((v[order], t[order]))
    return out


def _max_descending_runs(seqs) -> np.ndarray:
    """Lengths (in elements) of maximal strictly-decreasing-energy runs."""
    lengths = []
    for v, _ in seqs:
        run = 1
        for i in range(1, len(v)):
            if v[i] < v[i - 1]:
                run += 1
            else:
                lengths.append(run)
                run = 1
        lengths.append(run)
    return np.array(lengths, dtype=int) if lengths else np.array([], dtype=int)


def _triplet_gap_logratios(seqs) -> np.ndarray:
    """log10(g1/g2) for every within-session strictly-decreasing-energy triplet."""
    out = []
    for v, t in seqs:
        for i in range(len(v) - 2):
            if v[i] > v[i + 1] > v[i + 2]:           # a monotone-decay cascade
                g1, g2 = t[i + 1] - t[i], t[i + 2] - t[i + 1]
                if g1 > 0 and g2 > 0:
                    out.append(math.log10(g1 / g2))
    return np.array(out) if out else np.array([])


@dataclass
class RecoveryClockResult:
    source: str
    available: bool
    n_bursts: int
    n_sessions: int
    # (A) wall
    n_long_cascades: int = 0          # observed cascades with > N_fam elements
    wall_enrichment: float = float("nan")   # obs/null mean (<1 => suppressed = wall-like)
    wall_p_deficit: float = float("nan")    # p that nulls have <= obs long cascades
    wall_supported: bool = False
    # (B) acceleration
    n_triplets: int = 0
    accel_obs: int = 0                # triplets near the clock gap ratio
    accel_enrichment: float = float("nan")
    accel_p: float = float("nan")
    placebo_max_enrichment: float = float("nan")   # best arbitrary-ratio enrichment
    accel_supported: bool = False
    verdict: str = ""


def recovery_clock_test(series: RepeaterSeries, half_window_dex: float = 0.10,
                        n_surrogate: int = 1000, seed: int = 0) -> RecoveryClockResult:
    """Test the resummed recovery clock (wall + acceleration) on one source."""
    if not series.available:
        return RecoveryClockResult(series.source, False, 0, 0, verdict="data-limited")
    seqs = _session_sequences(series)
    n_bursts = int(sum(len(v) for v, _ in seqs))
    n_sessions = len(seqs)
    if n_bursts < 30:
        return RecoveryClockResult(series.source, True, n_bursts, n_sessions,
                                   verdict=f"too few cascade-capable bursts ({n_bursts})")

    rng = np.random.default_rng(seed)

    # ---- (A) the wall: are long monotone-decay cascades suppressed? -----------
    runs = _max_descending_runs(seqs)
    obs_long = int(np.sum(runs > WALL_LEN))

    # ---- (B) acceleration: gap ratio near the clock value ---------------------
    tri = _triplet_gap_logratios(seqs)
    n_tri = len(tri)
    accel_obs = int(np.sum(np.abs(tri - LOG_CLOCK_GAP) <= half_window_dex))
    placebo_targets = [1.7, 2.2, 3.3, 4.5]      # arbitrary non-clock gap ratios
    placebo_log = [math.log10(r) for r in placebo_targets]
    accel_placebo_obs = [int(np.sum(np.abs(tri - pl) <= half_window_dex)) for pl in placebo_log]

    # surrogates: within-session energy shuffle (keeps the gap structure + the
    # energy marginal, destroys the energy-time cascade correlation)
    null_long, null_accel = [], []
    null_placebo = [[] for _ in placebo_log]
    val0 = series.energy if np.isfinite(series.energy).sum() else series.fluence
    sess = series.session_id if series.session_id.size else np.zeros(len(series.mjd))
    for _ in range(n_surrogate):
        v2 = np.asarray(val0, dtype=float).copy()
        for s in np.unique(sess):
            idx = np.where(sess == s)[0]
            v2[idx] = rng.permutation(v2[idx])
        shuffled = RepeaterSeries(series.source, True, series.mjd, energy=v2,
                                  session_id=sess)
        sq = _session_sequences(shuffled)
        null_long.append(int(np.sum(_max_descending_runs(sq) > WALL_LEN)))
        st = _triplet_gap_logratios(sq)
        null_accel.append(int(np.sum(np.abs(st - LOG_CLOCK_GAP) <= half_window_dex)))
        for j, pl in enumerate(placebo_log):
            null_placebo[j].append(int(np.sum(np.abs(st - pl) <= half_window_dex)))

    null_long = np.array(null_long)
    mean_long = float(null_long.mean()) or 1e-9
    wall_enr = obs_long / mean_long
    wall_p_def = float((1 + np.sum(null_long <= obs_long)) / (n_surrogate + 1))
    wall_supported = bool(wall_p_def < 0.05 and wall_enr < 1.0)

    null_accel = np.array(null_accel)
    mean_accel = float(null_accel.mean()) or 1e-9
    accel_enr = accel_obs / mean_accel
    accel_p = float((1 + np.sum(null_accel >= accel_obs)) / (n_surrogate + 1))
    placebo_enr = []
    for j in range(len(placebo_log)):
        mp = float(np.mean(null_placebo[j])) or 1e-9
        placebo_enr.append(accel_placebo_obs[j] / mp)
    placebo_max = float(max(placebo_enr)) if placebo_enr else float("nan")
    # accel is "supported" only if the clock value beats both the null AND every
    # arbitrary placebo ratio (i.e. the clock value is genuinely special)
    accel_supported = bool(accel_p < 0.05 and accel_enr > 1.2 and accel_enr > placebo_max
                           and n_tri >= 20)

    if wall_supported and accel_supported:
        verdict = "recovery-clock candidate: cascade wall AND accelerating gaps"
    elif wall_supported:
        verdict = f"cascade-wall hint (long cascades suppressed, p={wall_p_def:.3f})"
    elif accel_supported:
        verdict = f"accelerating-gap hint near clock ratio {CLOCK_GAP_RATIO:.3f} (p={accel_p:.3f})"
    else:
        verdict = "clean null (no cascade wall, no accelerating-gap excess)"
    return RecoveryClockResult(
        series.source, True, n_bursts, n_sessions,
        obs_long, wall_enr, wall_p_def, wall_supported,
        n_tri, accel_obs, accel_enr, accel_p, placebo_max, accel_supported, verdict)


@dataclass
class MultiSourceClock:
    sources: list[str]
    per_source: dict = field(default_factory=dict)
    wall_sources: list[str] = field(default_factory=list)
    accel_sources: list[str] = field(default_factory=list)
    replicated: bool = False
    verdict: str = ""


def multi_source_recovery_clock(series_list: list[RepeaterSeries], n_surrogate: int = 600,
                                seed: int = 0) -> MultiSourceClock:
    """Run the recovery-clock test on each source; a sub-test counts as replicated
    when it is supported in >= 2 independent sources."""
    per: dict = {}
    names, wall_ok, accel_ok = [], [], []
    for s in series_list:
        r = recovery_clock_test(s, n_surrogate=n_surrogate, seed=seed)
        if not r.available or r.n_bursts < 30:
            continue
        names.append(r.source)
        per[r.source] = {
            "n_bursts": r.n_bursts, "n_sessions": r.n_sessions,
            "n_long_cascades": r.n_long_cascades, "wall_enrichment": r.wall_enrichment,
            "wall_p_deficit": r.wall_p_deficit, "wall_supported": r.wall_supported,
            "n_triplets": r.n_triplets, "accel_enrichment": r.accel_enrichment,
            "accel_p": r.accel_p, "placebo_max_enrichment": r.placebo_max_enrichment,
            "accel_supported": r.accel_supported, "verdict": r.verdict,
        }
        if r.wall_supported:
            wall_ok.append(r.source)
        if r.accel_supported:
            accel_ok.append(r.source)
    replicated = len(wall_ok) >= 2 or len(accel_ok) >= 2
    verdict = (f"wall: {'REPLICATED' if len(wall_ok) >= 2 else 'null'} ({len(wall_ok)}/{len(names)}); "
               f"acceleration: {'REPLICATED' if len(accel_ok) >= 2 else 'null'} "
               f"({len(accel_ok)}/{len(names)})")
    return MultiSourceClock(names, per, wall_ok, accel_ok, replicated, verdict)

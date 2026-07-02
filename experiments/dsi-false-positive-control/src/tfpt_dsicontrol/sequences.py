"""Per-sequence control statistics: the frozen detector + two nulls on non-TFPT cascades.

Each control sequence is a point process (aftershocks after a mainshock, flares after a big
X-flare). The recovery observable is the SAME construction the TFPT quake channel uses
(``recovery-comb-domains/src/tfpt_combdomains/quake.py::rate_curve``): equal-ln(t) bins of event
COUNTS, y = ln(count). For an Omori rate ~ t^-p the per-bin count is ~t^(1-p) (near-flat at p~1),
so equal-ln(t) bins weight ln(t) uniformly — the natural frame for a log-periodic comb — and the
detector's degree-2 poly-in-ln(t) baseline absorbs the smooth decay.

Per sequence we report:
  1. the FROZEN detector verdict at the kernel omega=2.583 (off-kernel periodogram-rank p +
     the hard >=2.8 comb-period ln-range gate) — ``comb.run_comb`` unchanged;
  2. a RATE-PRESERVING SHUFFLE null: surrogate event sets redistributed over the same ln(t) bins
     with probabilities from the fitted smooth (degree-2 in ln t) rate — preserves the Omori
     trend and total count, destroys any ripple — p_shuffle = rank of the observed kernel gain;
  3. an off-kernel PERIODOGRAM SCAN over omega in [1,6]: where does the kernel rank? what is the
     sequence's own best free omega (its Sornette-type DSI scale, if any) and is THAT special
     under the same shuffle null (look-elsewhere-uncorrected, labelled as such)?
  4. the fitted ripple amplitude eps at the kernel, next to the TFPT prediction ~0.017.

The aggregate deliverable is the FALSE-POSITIVE RATE of the kernel frequency across all gated
control sequences (frozen criterion, and the stricter frozen+shuffle double criterion).
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .comb import (
    DETREND_DEG,
    MIN_COMB_PERIODS,
    OMEGA,
    P_THRESHOLD,
    _comb_gain,
    comb_periods,
    run_comb,
)

SEQ = Path(__file__).resolve().parents[2] / "data" / "sequences"

OMEGA_SCAN_LO = 1.0     # preregistered scan band omega in [1, 6]
OMEGA_SCAN_HI = 6.0
N_SCAN = 501
N_SHUFFLE = 500


@dataclass(frozen=True)
class Sequence:
    name: str
    kind: str            # "aftershock" | "flare"
    t_days: np.ndarray   # event times since t0 (>0), days
    size: np.ndarray     # magnitude (quake) or peak flux (flare); documentation only


def load_sequences() -> list[Sequence]:
    """Read every normalised data/sequences/<name>.csv (written by the fetchers)."""
    out = []
    for path in sorted(SEQ.glob("*.csv")):
        t, s = [], []
        with path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                t.append(float(row["t_days"]))
                s.append(float(row["size"]))
        t_arr = np.asarray(t)
        kind = "aftershock" if t_arr.max() > 100 else "flare"
        out.append(Sequence(path.stem, kind, t_arr, np.asarray(s)))
    return out


def rate_curve(days: np.ndarray, *, n_bins: int = 80, min_count: int = 2
               ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Equal-ln(t) bins of event counts -> (t_center, y=ln count, edges, counts). Identical
    construction to recovery-comb-domains quake.rate_curve (bins below min_count dropped)."""
    lt = np.log(days[days > 0])
    edges = np.linspace(lt.min(), lt.max(), n_bins + 1)
    idx = np.clip(np.digitize(lt, edges) - 1, 0, n_bins - 1)
    counts = np.bincount(idx, minlength=n_bins)
    keep = counts >= min_count
    tc = np.exp(0.5 * (edges[:-1] + edges[1:]))[keep]
    return tc, np.log(counts[keep].astype(float)), edges, counts


def shuffle_pvalue(t: np.ndarray, y: np.ndarray, counts: np.ndarray, edges: np.ndarray,
                   omega: float, *, n_shuffle: int = N_SHUFFLE, min_count: int = 2,
                   seed: int = 0) -> float:
    """Rate-preserving shuffle null. Fit the detector's own smooth baseline (degree-2 poly in
    ln t) to the observed binned curve, convert to expected counts per bin, and redistribute the
    SAME total number of events multinomially over the bins. Each surrogate preserves the smooth
    Omori trend + total count but has no ripple; p = rank of the observed kernel comb gain."""
    g_obs = _comb_gain(np.log(t), y, omega)
    centers = 0.5 * (edges[:-1] + edges[1:])
    used = counts >= min_count
    coef = np.polyfit(centers[used], np.log(counts[used].astype(float)), DETREND_DEG)
    lam = np.exp(np.polyval(coef, centers))          # smooth expected count per bin
    prob = lam / lam.sum()
    n_events = int(counts.sum())
    rng = np.random.default_rng(seed)
    hits = valid = 0
    for _ in range(n_shuffle):
        c = rng.multinomial(n_events, prob)
        k = c >= min_count
        if int(k.sum()) < 6:
            continue
        valid += 1
        g = _comb_gain(centers[k], np.log(c[k].astype(float)), omega)
        hits += int(g >= g_obs)
    return float((1 + hits) / (valid + 1)) if valid else 1.0


def omega_scan(t: np.ndarray, y: np.ndarray) -> dict:
    """Dense comb-gain periodogram over the preregistered band omega in [1,6]: the kernel's rank
    among all scanned frequencies, and the sequence's own best free omega/lambda. The raw argmax
    tends to pin at the low edge (slow trend residue the degree-2 baseline leaves behind, NOT a
    DSI scale), so the best free omega is also reported over the LOCALISABLE sub-band — omegas
    the curve spans for >= MIN_COMB_PERIODS cycles (omega >= 2 pi MIN_COMB_PERIODS / ln-range),
    the same requirement the kernel itself must meet."""
    lt = np.log(t)
    grid = np.linspace(OMEGA_SCAN_LO, OMEGA_SCAN_HI, N_SCAN)
    spec = np.array([_comb_gain(lt, y, w) for w in grid])
    g0 = _comb_gain(lt, y, OMEGA)
    off = np.abs(grid - OMEGA) > 0.1 * OMEGA        # exclude the kernel's own neighbourhood
    rank = int(1 + np.sum(spec[off] > g0))
    n_off = int(off.sum())
    i_best = int(np.argmax(spec))
    w_best = float(grid[i_best])
    ln_range = float(lt.max() - lt.min())
    w_loc = 2.0 * math.pi * MIN_COMB_PERIODS / ln_range
    loc = grid >= w_loc
    out = {"kernel_gain": round(float(g0), 5), "kernel_rank": rank, "n_scanned": n_off,
           "kernel_rank_frac": round(rank / (n_off + 1), 4),
           "best_free_omega": round(w_best, 3),
           "best_free_lambda": round(math.exp(2.0 * math.pi / w_best), 3),
           "best_free_gain": round(float(spec[i_best]), 5),
           "localisable_omega_min": round(w_loc, 3)}
    if loc.any():
        j = int(np.argmax(np.where(loc, spec, -1.0)))
        w_j = float(grid[j])
        out.update({"best_localisable_omega": round(w_j, 3),
                    "best_localisable_lambda": round(math.exp(2.0 * math.pi / w_j), 3),
                    "best_localisable_gain": round(float(spec[j]), 5)})
    else:
        out.update({"best_localisable_omega": None, "best_localisable_lambda": None,
                    "best_localisable_gain": None})
    return out


def eps_at_kernel(t: np.ndarray, y: np.ndarray, *, omega: float = OMEGA) -> float:
    """Fitted fractional ripple amplitude at the kernel: y = poly2(ln t) + a cos + b sin, and in
    y = ln(count) the ripple amplitude hypot(a, b) IS the fractional eps (cf. EPS_PREDICTED)."""
    lt = np.log(t)
    X = np.column_stack([np.vander(lt, DETREND_DEG + 1), np.cos(omega * lt), np.sin(omega * lt)])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(math.hypot(b[-2], b[-1]))


def analyze_sequence(seq: Sequence, *, seed: int = 0) -> dict:
    """The full per-sequence control record."""
    t, y, edges, counts = rate_curve(seq.t_days)
    frozen = run_comb(t, y, seed=seed)
    p_shuf = shuffle_pvalue(t, y, counts, edges, OMEGA, seed=seed)
    scan = omega_scan(t, y)
    w_best = scan["best_localisable_omega"] or scan["best_free_omega"]
    p_shuf_best = shuffle_pvalue(t, y, counts, edges, w_best, seed=seed + 1)
    fired = bool(frozen["comb_detected"])                       # the FROZEN criterion
    fired_strict = bool(fired and p_shuf < P_THRESHOLD)         # frozen AND rate-preserving null
    return {"name": seq.name, "kind": seq.kind, "n_events": int(len(seq.t_days)),
            "t_min_days": round(float(seq.t_days.min()), 4),
            "t_max_days": round(float(seq.t_days.max()), 2),
            "n_bins": int(len(t)),
            "ln_range": round(float(np.log(t.max() / t.min())), 2),
            "comb_periods": frozen["comb_periods"],
            "range_sufficient": frozen["range_sufficient"],
            "p_kernel_periodogram": frozen["p_value"],
            "p_kernel_shuffle": round(p_shuf, 4),
            "eps_fit_at_kernel": round(eps_at_kernel(t, y), 4),
            "scan": scan,
            "p_best_localisable_shuffle_uncorrected": round(p_shuf_best, 4),
            "fired_at_kernel_frozen": fired,
            "fired_at_kernel_strict": fired_strict}


def wilson_ci(k: int, n: int, *, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a binomial rate (small-n honest)."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1.0 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def aggregate(records: list[dict]) -> dict:
    """The headline number: how often does the KERNEL frequency fire on non-TFPT cascades?"""
    gated = [r for r in records if r["range_sufficient"]]
    k_frozen = sum(r["fired_at_kernel_frozen"] for r in gated)
    k_strict = sum(r["fired_at_kernel_strict"] for r in gated)
    lo_f, hi_f = wilson_ci(k_frozen, len(gated))
    lo_s, hi_s = wilson_ci(k_strict, len(gated))
    return {"n_sequences": len(records), "n_gated": len(gated),
            "kernel_fp_frozen": {"fired": k_frozen,
                                 "rate": round(k_frozen / len(gated), 4) if gated else None,
                                 "wilson95": [round(lo_f, 4), round(hi_f, 4)]},
            "kernel_fp_strict": {"fired": k_strict,
                                 "rate": round(k_strict / len(gated), 4) if gated else None,
                                 "wilson95": [round(lo_s, 4), round(hi_s, 4)]},
            "nominal_rate_at_threshold": P_THRESHOLD,
            "min_comb_periods_gate": MIN_COMB_PERIODS}

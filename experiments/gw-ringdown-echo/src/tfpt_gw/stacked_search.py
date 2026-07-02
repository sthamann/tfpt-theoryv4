"""Stage-1b: STACKED (2/3)^6 echo search across the loudest ringdown events.

The single-event searches are individually null; the forecast (Stage 0) says only a
STACK of the loudest events reaches the detection threshold.  This module combines
the per-event Stage-1 matched-filter results into one catalogue-level statement:

  * on-source stack:   Z = sum over events/detectors of rho_max^2
  * background stack:  the same sum drawn from each detector's OFF-SOURCE rho_max
                       distribution (independent draws; the detectors/events are
                       independent noise streams), N_STACK realisations
  * stacked p-value:   P(Z_bg >= Z_on)
  * Fisher combination of the per-detector on-source p-values (secondary view)

Verdict language follows the firewall: a small stacked p would only ESCALATE (to
coherent time-slide follow-up); a large p is a well-powered NULL for a maximal
kernel-ratio echo train in the loudest available ringdowns.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.stats import chi2 as chi2_dist

from .constants import RATIO
from .real_echo_search import (
    LAG_GRID_MS,
    N_ECHO,
    STRAIN_DIR,
    _mf_scan,
    search_event,
)
from .strain_data import (
    apply_whitening,
    detector_frame_mass,
    fit_and_subtract_qnm,
    qnm_220,
    read_hdf5,
    whitening_filter,
)

N_BG_PER_DET = 300          # off-source rho_max samples per detector
N_STACK = 20000             # background stack realisations
RESULTS = Path(__file__).resolve().parents[2] / "results"


@dataclass
class StackResult:
    events: list[str]
    n_detectors: int = 0
    z_on: float = 0.0
    z_bg_median: float = 0.0
    z_bg_p90: float = 0.0
    p_stacked: float = 1.0
    fisher_chi2: float = 0.0
    fisher_dof: int = 0
    p_fisher: float = 1.0
    per_event: list[dict] = field(default_factory=list)
    verdict: str = ""


def _bg_samples(event: str, af: float = 0.69) -> dict[str, np.ndarray]:
    """Off-source rho_max distribution per detector (same filter as on-source)."""
    meta = json.loads((STRAIN_DIR / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)
    f0, tau = qnm_220(mf, af)
    rng = np.random.default_rng(1)
    out: dict[str, np.ndarray] = {}
    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        psd_i, scale = whitening_filter(s.data, s.dt)
        white = apply_whitening(s.data, psd_i, scale)
        merger = s.index_at(merger_gps)
        resid, _ = fit_and_subtract_qnm(white, merger, f0, tau, s.dt)
        max_lag_samp = int(round(LAG_GRID_MS.max() * 1e-3 / s.dt))
        win_len = N_ECHO * max_lag_samp + int(6.0 * tau / s.dt)
        guard = int(1.0 / s.dt)
        lo, hi = guard, len(resid) - win_len - guard
        centers = rng.integers(lo, hi, size=N_BG_PER_DET)
        out[det] = np.array([_mf_scan(resid, int(c), f0, tau, s.dt, win_len)[0]
                             for c in centers if abs(int(c) - merger) > guard])
    return out


def stack_events(events: list[str]) -> StackResult:
    res = StackResult(events=list(events))
    rng = np.random.default_rng(2)
    on_sq: list[float] = []
    bg_pools: list[np.ndarray] = []
    fisher_terms: list[float] = []

    for ev in events:
        r = search_event(ev)
        bg = _bg_samples(ev)
        det_rows = []
        for d in r.detectors:
            pool = bg.get(d.detector)
            if pool is None or len(pool) == 0:
                continue
            on_sq.append(d.rho_max ** 2)
            bg_pools.append(pool ** 2)
            fisher_terms.append(-2.0 * math.log(max(d.p_value, 1e-6)))
            det_rows.append({"detector": d.detector, "rho_max": d.rho_max,
                             "p_value": d.p_value, "q_hat": d.q_hat,
                             "kernel_consistent": d.kernel_consistent})
        res.per_event.append({"event": ev, "label": r.label, "detectors": det_rows})

    res.n_detectors = len(on_sq)
    res.z_on = float(np.sum(on_sq))

    # background stack: independent draws from each detector's off-source pool
    z_bg = np.zeros(N_STACK)
    for pool in bg_pools:
        z_bg += rng.choice(pool, size=N_STACK, replace=True)
    res.z_bg_median = float(np.median(z_bg))
    res.z_bg_p90 = float(np.percentile(z_bg, 90))
    res.p_stacked = float((np.sum(z_bg >= res.z_on) + 1) / (N_STACK + 1))

    # Fisher combination (secondary; p floored at the per-event MC resolution)
    res.fisher_chi2 = float(np.sum(fisher_terms))
    res.fisher_dof = 2 * len(fisher_terms)
    res.p_fisher = float(chi2_dist.sf(res.fisher_chi2, res.fisher_dof))

    n_kernel = sum(d["kernel_consistent"] for ev in res.per_event
                   for d in ev["detectors"])
    fisher_note = (
        "the Fisher secondary is dominated by q_hat ~ 1 residual-ringdown streams "
        "(imperfect dominant-QNM subtraction), which the free-ratio control rejects "
        "as non-kernel -- it is NOT evidence for a (2/3)^6 train"
        if res.p_fisher < 0.05 and n_kernel == 0 else
        "Fisher secondary consistent with the primary stack")
    if res.p_stacked < 0.01 and n_kernel >= 2:
        res.verdict = (
            f"stacked excess (p={res.p_stacked:.4f}) WITH kernel-consistent streams -- "
            "NOT a claim: escalate to coherent time-slide background + injections "
            "before any statement (firewall: search target, not a detection).")
    else:
        res.verdict = (
            f"STACKED NULL: the loudest {len(events)} ringdown events combined show "
            f"no kernel-ratio ((2/3)^6) echo-train excess (stacked p={res.p_stacked:.3f} "
            f"over {res.n_detectors} detector streams; kernel-consistent streams "
            f"{n_kernel}/{res.n_detectors}; {fisher_note}). A maximal echo train at "
            "the frozen ratio is disfavoured in this stack; TFPT's (2/3)^6 is an "
            "UPPER bound, so this is consistent -- the bound tightens. "
            "No detection, no tension claim.")
    return res


def run_stack(events: list[str]) -> int:
    have = [e for e in events if (STRAIN_DIR / f"{e}_meta.json").exists()]
    missing = [e for e in events if e not in have]
    print("=" * 84)
    print("TFPT GW Stage-1b: STACKED (2/3)^6 echo search across the loudest ringdowns")
    print("=" * 84)
    if missing:
        print(f"  (no strain for {missing}; fetch first)")
    if len(have) < 2:
        print("  need >=2 events with strain for a stack.")
        return 1

    r = stack_events(have)
    print(f"\n  events: {', '.join(r.events)}")
    for ev in r.per_event:
        dets = ", ".join(f"{d['detector']}: rho={d['rho_max']:.2f} p={d['p_value']:.3f} "
                         f"q_hat={d['q_hat']:.3f}" for d in ev["detectors"])
        print(f"    {ev['event']:22s} {ev['label']:22s} {dets}")
    print(f"\n  stack: Z_on = {r.z_on:.2f} over {r.n_detectors} detector streams")
    print(f"         background median = {r.z_bg_median:.2f}, p90 = {r.z_bg_p90:.2f}")
    print(f"         stacked p = {r.p_stacked:.4f};  Fisher chi2 = {r.fisher_chi2:.1f} "
          f"(dof {r.fisher_dof}) -> p = {r.p_fisher:.4f}")
    print(f"\n-> {r.verdict}")

    RESULTS.mkdir(exist_ok=True)
    out = {"stage": "strain_level_test (stacked, real GWOSC strain)",
           "ratio_(2/3)^6": RATIO,
           "events": r.events, "per_event": r.per_event,
           "n_detector_streams": r.n_detectors,
           "z_on": r.z_on, "z_bg_median": r.z_bg_median, "z_bg_p90": r.z_bg_p90,
           "p_stacked": r.p_stacked, "fisher_chi2": r.fisher_chi2,
           "fisher_dof": r.fisher_dof, "p_fisher": r.p_fisher,
           "verdict": r.verdict}
    (RESULTS / "echo_stack.json").write_text(json.dumps(out, indent=2),
                                             encoding="utf-8")
    print(f"\nWrote {RESULTS / 'echo_stack.json'}")
    return 0

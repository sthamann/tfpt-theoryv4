"""Stage-1g: DRIFT + PRECESSION robustness scan -- the last two distortions.

Closes the two remaining signature-distortion axes from the systematics
review (the third, NR-informed subtraction, is approximated by the battery's
--aggressive greedy residual modelling):

  LAG DRIFT   : a relaxing ECO cavity changes size over the first bounces, so
                the inter-echo spacing drifts: position of echo k
                    p_k = sum_{j<=k} dt (1 + delta (j-1))
                with drift delta scanned over {-10%, -5%, +5%, +10%} around
                the C=3/8 predicted spacing (+-25% grid).  Coherent matched
                filter with kernel ratios, dphi in {0, pi}.
  PRECESSION  : a precessing remnant modulates the per-echo amplitude by a
                slowly varying geometric factor, breaking the r^k ordering
                while keeping the POSITIONS.  Proxy statistic: POSITION-ONLY
                incoherent sum -- free phase per echo AND uniform amplitude
                weights (tests train positions without amplitude ordering):
                    S_pos = (1/sqrt(K)) sum_k a_k .

OFF-SOURCE (event-gated) PSD throughout; backgrounds from off-source windows;
Bonferroni over the ACTUAL per-detector variant count.  Escalation requires
>=2 coincident detectors.  Search-target firewall: upper-bound kernel,
post-hoc strain, no detection claim.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .signature_battery import (
    GATE_POST_S,
    GATE_PRE_S,
    N_ECHO,
    qnm_22n,
    subtract_qnm_multimode,
)
from .strain_data import (
    GMSUN_OVER_C3,
    apply_whitening,
    damped_sinusoid,
    detector_frame_mass,
    read_hdf5,
    whitening_filter_gated,
)

STRAIN_DIR = Path(__file__).resolve().parents[2] / "data" / "strain"
RESULTS = Path(__file__).resolve().parents[2] / "results"

DELAY_COEFF = 2.288
LAG_TOL = 0.25
N_LAG = 7
DRIFTS = (-0.10, -0.05, 0.05, 0.10)
RATIOS = [("amp_(2/3)^6", (2.0 / 3.0) ** 6), ("energy->(2/3)^3", (2.0 / 3.0) ** 3)]
PHASES = [("dphi0", 0.0), ("dphi180", np.pi)]
JITTER_S = 0.005
N_BACKGROUND = 400
GUARD_S = 1.0


def drift_positions(lag_samp: int, delta: float) -> list[int]:
    """Echo positions with per-bounce spacing drift delta."""
    pos = []
    p = 0.0
    for j in range(1, N_ECHO + 1):
        p += lag_samp * (1.0 + delta * (j - 1))
        pos.append(int(round(p)))
    return pos


def drift_template(n: int, lag_samp: int, delta: float, ratio: float, dphi: float,
                   f0: float, tau: float, dt: float) -> np.ndarray:
    h = np.zeros(n)
    for k, p in enumerate(drift_positions(lag_samp, delta), start=1):
        if p >= n:
            break
        h += (ratio ** k) * damped_sinusoid(n, p, f0, tau, dt, phi=k * dphi)
    return h


def correlate_template(resid: np.ndarray, tmpl: np.ndarray) -> np.ndarray:
    n = len(resid)
    norm = math.sqrt(float(tmpl @ tmpl))
    tp = np.zeros(n)
    tp[:len(tmpl)] = tmpl
    return np.fft.irfft(np.fft.rfft(resid) * np.conj(np.fft.rfft(tp)), n=n) / norm


def position_only_stat(resid: np.ndarray, t0: int, lag_samp: int,
                       f0: float, tau: float, dt: float) -> float:
    """Uniform-weight free-phase per-echo sum (precession-robust)."""
    n = len(resid)
    vals = []
    for k in range(1, N_ECHO + 1):
        start = t0 + k * lag_samp
        end = min(n, start + int(6.0 * tau / dt))
        if start >= n or end - start < 8:
            break
        c = damped_sinusoid(n, start, f0, tau, dt, phi=0.0)[start:end]
        s = damped_sinusoid(n, start, f0, tau, dt, phi=-np.pi / 2)[start:end]
        seg = resid[start:end]
        nc, ns = float(c @ c), float(s @ s)
        if nc == 0 or ns == 0:
            break
        vals.append(math.hypot(float(seg @ c) / math.sqrt(nc),
                               float(seg @ s) / math.sqrt(ns)))
    return float(np.sum(vals) / math.sqrt(len(vals))) if vals else 0.0


@dataclass
class ScanDetector:
    detector: str
    variants: list[dict] = field(default_factory=list)


@dataclass
class ScanEvent:
    event: str
    mf_det: float
    lag_pred_ms: float
    detectors: list[ScanDetector] = field(default_factory=list)
    label: str = ""


def scan_event(event: str, af: float = 0.69) -> ScanEvent:
    meta = json.loads((STRAIN_DIR / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)
    f0, tau0 = qnm_22n(mf, af, 0)
    f1, tau1 = qnm_22n(mf, af, 1)
    lag_pred_s = DELAY_COEFF * mf * GMSUN_OVER_C3
    res = ScanEvent(event, round(mf, 1), round(lag_pred_s * 1e3, 3))
    rng = np.random.default_rng(13)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        merger = s.index_at(merger_gps)
        psd_i, scale = whitening_filter_gated(
            s.data, s.dt, merger - int(GATE_PRE_S / s.dt),
            merger + int(GATE_POST_S / s.dt))
        white = apply_whitening(s.data, psd_i, scale)
        resid, _ = subtract_qnm_multimode(white, merger,
                                          [(f0, tau0), (f1, tau1)], s.dt)

        lag0 = lag_pred_s / s.dt
        lags_samp = np.unique(np.round(
            lag0 * np.linspace(1.0 - LAG_TOL, 1.0 + LAG_TOL, N_LAG)).astype(int))
        lags_samp = lags_samp[lags_samp > 0]
        jit = int(JITTER_S / s.dt)
        max_train = int(lags_samp.max()) * N_ECHO * 2 + int(6.0 * tau0 / s.dt)
        guard = int(GUARD_S / s.dt)
        lo, hi = guard, len(resid) - max_train - jit - guard
        centers = rng.integers(lo, hi, size=N_BACKGROUND)
        centers = centers[np.abs(centers - merger) > guard]

        dres = ScanDetector(det)
        # DRIFT variants (coherent): max over the lag grid per (delta, ratio, phase)
        for delta in DRIFTS:
            for rn, ratio in RATIOS:
                for pn, dphi in PHASES:
                    rho = np.stack([
                        correlate_template(
                            resid,
                            drift_template(
                                int(ls) * N_ECHO * 2 + int(6.0 * tau0 / s.dt),
                                int(ls), delta, ratio, dphi, f0, tau0, s.dt))
                        for ls in lags_samp])
                    s_on = float(rho[:, merger:merger + jit].max())
                    bg = np.array([rho[:, int(c):int(c) + jit].max()
                                   for c in centers])
                    p_raw = float((np.sum(bg >= s_on) + 1) / (len(bg) + 1))
                    dres.variants.append({
                        "variant": f"drift{delta:+.2f}_{rn}_{pn}",
                        "statistic": "drift_coherent", "drift": delta,
                        "ratio": round(ratio, 4), "s_on": round(s_on, 2),
                        "p_raw": round(p_raw, 4)})
        # PRECESSION proxy (position-only, uniform weights, free phase per echo)
        best_on = 0.0
        for ls in lags_samp:
            for t0 in range(merger, merger + jit, max(1, jit // 8)):
                best_on = max(best_on, position_only_stat(
                    resid, t0, int(ls), f0, tau0, s.dt))
        bg = []
        for c in centers[:300]:
            b = 0.0
            for ls in lags_samp[::3]:
                b = max(b, position_only_stat(resid, int(c), int(ls),
                                              f0, tau0, s.dt))
            bg.append(b)
        bg = np.asarray(bg)
        p_raw = float((np.sum(bg >= best_on) + 1) / (len(bg) + 1))
        dres.variants.append({
            "variant": "position_only", "statistic": "precession_proxy",
            "drift": 0.0, "ratio": None, "s_on": round(best_on, 2),
            "p_raw": round(p_raw, 4)})

        n_var = max(1, len(dres.variants))
        for v in dres.variants:
            v["p_bonf"] = round(min(1.0, v["p_raw"] * n_var), 4)
        res.detectors.append(dres)

    esc = 0
    if res.detectors:
        names = [v["variant"] for v in res.detectors[0].variants]
        for name in names:
            n_hit = sum(1 for d in res.detectors for v in d.variants
                        if v["variant"] == name and v["p_bonf"] < 0.01)
            esc = max(esc, n_hit)
    res.label = "ESCALATE" if esc >= 2 else "NO_DRIFT_OR_PRECESSION_ECHO"
    return res


def run_scan(events: list[str]) -> int:
    have = [e for e in events if (STRAIN_DIR / f"{e}_meta.json").exists()]
    print("=" * 88)
    print("TFPT GW Stage-1g: DRIFT + PRECESSION robustness scan")
    print(f"  spacing drift delta in {DRIFTS} per bounce (relaxing cavity) x kernel")
    print("  ratios x {0, pi}; + position-only free-phase statistic (precession proxy);")
    print("  OFF-SOURCE PSD; Bonferroni over actual per-detector variants")
    print("=" * 88)
    if not have:
        print("  no strain -> nothing to do.")
        return 1

    out = []
    best = {"p": 1.01, "where": "none below 1"}
    for ev in have:
        r = scan_event(ev)
        print(f"\n  {ev}: M_det={r.mf_det} Msun, base lag = {r.lag_pred_ms} ms"
              f"  ->  {r.label}")
        for d in r.detectors:
            p_drift = min((v["p_raw"] for v in d.variants
                           if v["statistic"] == "drift_coherent"), default=1.0)
            p_pos = min((v["p_raw"] for v in d.variants
                         if v["statistic"] == "precession_proxy"), default=1.0)
            print(f"    {d.detector:3s}  best drift p={p_drift:.3f}   "
                  f"position-only p={p_pos:.3f}")
            for v in d.variants:
                if v["p_bonf"] < best["p"]:
                    best = {"p": v["p_bonf"],
                            "where": f"{ev}/{d.detector}/{v['variant']}"}
        out.append({"event": r.event, "mf_det": r.mf_det,
                    "lag_pred_ms": r.lag_pred_ms, "label": r.label,
                    "detectors": [{"detector": d.detector, "variants": d.variants}
                                  for d in r.detectors]})

    any_esc = any(e["label"] == "ESCALATE" for e in out)
    verdict = (
        "ESCALATE: a Bonferroni-surviving drift/precession-robust excess is "
        "coincident in >=2 detectors -- injections + time-slides required."
        if any_esc else
        f"NO DRIFT OR PRECESSION ECHO: per-bounce spacing drift (relaxing cavity, "
        f"delta +-5/10%) and the precession-robust position-only statistic (free "
        f"phase, uniform weights) both show no Bonferroni-surviving excess "
        f"coincident in >=2 detectors on any event (best p_bonf = "
        f"{min(best['p'], 1.0):.3f} at {best['where']}). With Stage 1c-1f this "
        f"closes the last two signature-distortion axes accessible without "
        f"NR-informed waveform subtraction; upper-bound kernel: no detection, "
        f"no tension claim.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "robustness_scan.json").write_text(json.dumps({
        "stage": "strain_level_test (drift + precession robustness scan)",
        "drifts": list(DRIFTS), "delay_model": "2.288 M_det +-25%",
        "events": out, "best_p_bonf": best, "verdict": verdict},
        indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'robustness_scan.json'}")
    return 0

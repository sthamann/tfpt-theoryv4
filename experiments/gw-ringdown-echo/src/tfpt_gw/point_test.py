"""Stage-1d: the TFPT POINT TEST -- theory-fixed lag x kernel-fixed ratio.

The battery (Stage 1c) scans the lag freely; but TFPT PREDICTS the lag: the
gravastar-compactness experiment fixes the horizonless-object compactness to
the Nariai rational C = 3/8, whose tortoise round-trip delay is

    Delta t = 2.288 M            (geometric units; detector-frame M)

-- e.g. 0.77 ms for GW250114 (M_det = 68.6 Msun).  Combining the predicted
delay with the kernel-fixed amplitude ratio gives a POINT hypothesis with a
minimal look-elsewhere budget -- the sharpest TFPT-specific echo test.

Statistics per (event, detector) -- systematic-hardened (2026-07-02 round 2):

  COHERENT  : the Stage-1c matched filter, restricted to the predicted lag
              +-25% (mass/model tolerance), ratios {(2/3)^6, (2/3)^3} x mu4
              per-bounce phases {0, pi/2, pi, 3pi/2}  (8 variants).
  INCOHERENT: per-echo quadrature matching -- each echo is fit with FREE
              phase (cos+sin at the predicted position), only the positions
              (k Delta t) and the amplitude weights r^k are fixed  (2
              variants).  Robust to intra-echo morphology (barrier low-pass).
  SKIP-FIRST: incoherent statistic over echoes k = 2..5 only -- the first
              reflection samples the strongest (nonlinear) field regime and
              may break the geometric progression  (2 variants).
  JOINT-FIT : the short-lag repair.  The predicted ECO lag (~0.8 ms) is
              SMALLER than the ringdown tau (~4 ms), so echoes OVERLAP the
              primary ringdown and subtract-then-search partially absorbs
              the signal into the QNM fit.  Here the QNM (220+221 cos/sin)
              and the echo train are fit JOINTLY on the whitened data and
              the statistic is the F-ratio of the train block, calibrated on
              off-source windows  (1 variant, kernel ratio, dphi = 0).

SYSTEMATICS: whitening uses the OFF-SOURCE (event-gated) PSD so the filter
cannot ring after the merger; the remnant spin is scanned af in {0.60, 0.69,
0.80} (template f0/tau systematic; the best-af result is reported and the
scan counts in the Bonferroni budget via the variant count).

Bonferroni over all variants.  Escalation still requires >=2 coincident
detectors.  Post-hoc honesty: delay + ratios are preregistered numbers, but
the strain has been seen by earlier stages -- search-target statement only.
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
    correlate_bank,
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

DELAY_COEFF = 2.288                 # Delta t = 2.288 M (gravastar C = 3/8)
LAG_TOL = 0.25                      # +-25% tolerance around the predicted lag
N_LAG = 11
JITTER_S = 0.005
N_BACKGROUND = 800
GUARD_S = 1.0
SPINS = (0.60, 0.69, 0.80)          # remnant-spin systematic scan (Kerr f0/tau)

RATIOS = [("amp_(2/3)^6", (2.0 / 3.0) ** 6), ("energy->(2/3)^3", (2.0 / 3.0) ** 3)]
PHASES = [("dphi0", 0.0), ("dphi90", np.pi / 2),
          ("dphi180", np.pi), ("dphi270", 3 * np.pi / 2)]
# coherent (ratio x phase) + incoherent (ratio) + skip-first (ratio) + joint-fit,
# times the spin scan
N_VARIANTS = (len(RATIOS) * len(PHASES) + 2 * len(RATIOS) + 1) * len(SPINS)


@dataclass
class PointVariant:
    variant: str
    statistic: str          # "coherent" | "incoherent" | "skip_first" | "joint_fit"
    ratio: float
    spin: float
    s_on: float
    p_raw: float
    p_bonf: float


@dataclass
class PointDetector:
    detector: str
    variants: list[PointVariant] = field(default_factory=list)


@dataclass
class PointEvent:
    event: str
    mf_det: float
    lag_pred_ms: float
    detectors: list[PointDetector] = field(default_factory=list)
    label: str = ""


def _incoherent_stat(resid: np.ndarray, t0: int, lag_samp: int, ratio: float,
                     f0: float, tau: float, dt: float, k_min: int = 1) -> float:
    """S_inc = sum_k r^k a_k / sqrt(sum r^{2k}); a_k = free-phase quadrature
    amplitude of echo k at the predicted position (morphology-robust).
    k_min = 2 skips the first (potentially nonlinear) reflection."""
    n = len(resid)
    num = 0.0
    den = 0.0
    for k in range(k_min, N_ECHO + 1):
        start = t0 + k * lag_samp
        end = min(n, start + int(6.0 * tau / dt))
        if start >= n or end - start < 8:
            break
        # segment-local damped sinusoid == damped_sinusoid(n, start, ...)[start:end]
        # (built directly to avoid full-length allocations at 16 kHz)
        t = np.arange(end - start) * dt
        envelope = np.exp(-t / tau)
        c = envelope * np.cos(2.0 * np.pi * f0 * t)
        s = envelope * np.cos(2.0 * np.pi * f0 * t - np.pi / 2)
        seg = resid[start:end]
        nc, ns = float(c @ c), float(s @ s)
        if nc == 0 or ns == 0:
            break
        a_k = math.hypot(float(seg @ c) / math.sqrt(nc), float(seg @ s) / math.sqrt(ns))
        w = ratio ** k
        num += w * a_k
        den += w * w
    return num / math.sqrt(den) if den > 0 else 0.0


def _joint_fit_stat(white: np.ndarray, t0: int, lags_samp: np.ndarray, ratio: float,
                    f0: float, tau0: float, f1: float, tau1: float,
                    dt: float) -> float:
    """Short-lag repair: fit QNM(220+221) and the echo train JOINTLY on the
    un-subtracted whitened data; statistic = max-over-lag F-ratio of the train
    block.  Avoids the subtract-then-search self-absorption when the lag is
    shorter than the ringdown tau (echoes overlap the primary ringdown)."""
    n = len(white)
    fit_len = int(8.0 * tau0 / dt) + int(lags_samp.max()) * N_ECHO
    end = min(n, t0 + fit_len)
    m = end - t0
    if m < 32:
        return 0.0
    y = white[t0:end]
    qnm_cols = []
    for f, tau in ((f0, tau0), (f1, tau1)):
        for phi in (0.0, -np.pi / 2):
            qnm_cols.append(damped_sinusoid(m, 0, f, tau, dt, phi=phi))
    A0 = np.vstack(qnm_cols).T
    beta0, *_ = np.linalg.lstsq(A0, y, rcond=None)
    rss0 = float(np.sum((y - A0 @ beta0) ** 2))
    best_f = 0.0
    for ls in lags_samp:
        tr_c = np.zeros(m)
        tr_s = np.zeros(m)
        for k in range(1, N_ECHO + 1):
            if k * int(ls) >= m:
                break
            tr_c += (ratio ** k) * damped_sinusoid(m, k * int(ls), f0, tau0, dt, phi=0.0)
            tr_s += (ratio ** k) * damped_sinusoid(m, k * int(ls), f0, tau0, dt,
                                                   phi=-np.pi / 2)
        A1 = np.column_stack([A0, tr_c, tr_s])
        beta1, *_ = np.linalg.lstsq(A1, y, rcond=None)
        rss1 = float(np.sum((y - A1 @ beta1) ** 2))
        if rss1 <= 0:
            continue
        f_stat = ((rss0 - rss1) / 2.0) / (rss1 / max(1, m - 6))
        best_f = max(best_f, f_stat)
    return best_f


def meta_name(event: str, hires: bool = False) -> str:
    """Meta-file convention: <event>_meta.json (4 kHz) / <event>_meta16k.json
    (16 kHz crops from scripts/fetch_strain_16k.py; ~12 samples per predicted
    C=3/8 lag step instead of ~3)."""
    return f"{event}_meta16k.json" if hires else f"{event}_meta.json"


def point_event(event: str, hires: bool = False) -> PointEvent:
    meta = json.loads((STRAIN_DIR / meta_name(event, hires)).read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)
    lag_pred_s = DELAY_COEFF * mf * GMSUN_OVER_C3
    res = PointEvent(event, round(mf, 1), round(lag_pred_s * 1e3, 3))
    rng = np.random.default_rng(5)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        merger = s.index_at(merger_gps)
        # OFF-SOURCE PSD (event-gated Welch): the filter cannot ring after
        # the merger it never saw
        psd_i, scale = whitening_filter_gated(
            s.data, s.dt, merger - int(GATE_PRE_S / s.dt),
            merger + int(GATE_POST_S / s.dt))
        white = apply_whitening(s.data, psd_i, scale)

        lag0 = lag_pred_s / s.dt
        lags_samp = np.unique(np.round(
            lag0 * np.linspace(1.0 - LAG_TOL, 1.0 + LAG_TOL, N_LAG)).astype(int))
        lags_samp = lags_samp[lags_samp > 0]
        jit = int(JITTER_S / s.dt)
        guard = int(GUARD_S / s.dt)

        dres = PointDetector(det)
        for af in SPINS:
            f0, tau0 = qnm_22n(mf, af, 0)
            f1, tau1 = qnm_22n(mf, af, 1)
            resid, _ = subtract_qnm_multimode(white, merger,
                                              [(f0, tau0), (f1, tau1)], s.dt)
            train_len = int(lags_samp.max()) * N_ECHO + int(6.0 * tau0 / s.dt)
            lo, hi = guard, len(resid) - train_len - jit - guard
            centers = rng.integers(lo, hi, size=N_BACKGROUND)
            centers = centers[np.abs(centers - merger) > guard]

            # coherent variants (predicted-lag window only)
            for rn, ratio in RATIOS:
                for pn, dphi in PHASES:
                    rho = correlate_bank(resid, lags_samp, ratio, dphi, f0, tau0, s.dt)
                    s_on = float(rho[:, merger:merger + jit].max())
                    bg = np.array([rho[:, int(c):int(c) + jit].max() for c in centers])
                    p_raw = float((np.sum(bg >= s_on) + 1) / (len(bg) + 1))
                    dres.variants.append(PointVariant(
                        f"{rn}_{pn}_a{af:.2f}", "coherent", round(ratio, 4), af,
                        round(s_on, 2), round(p_raw, 4),
                        round(min(1.0, p_raw * N_VARIANTS), 4)))
            # incoherent + skip-first (free phase per echo, morphology-robust)
            for k_min, stat_name in ((1, "incoherent"), (2, "skip_first")):
                for rn, ratio in RATIOS:
                    best_on = 0.0
                    for ls in lags_samp:
                        for t0 in range(merger, merger + jit, max(1, jit // 8)):
                            best_on = max(best_on, _incoherent_stat(
                                resid, t0, int(ls), ratio, f0, tau0, s.dt, k_min))
                    bg = []
                    for c in centers[:300]:
                        b = 0.0
                        for ls in lags_samp[::3]:
                            b = max(b, _incoherent_stat(resid, int(c), int(ls), ratio,
                                                        f0, tau0, s.dt, k_min))
                        bg.append(b)
                    bg = np.asarray(bg)
                    p_raw = float((np.sum(bg >= best_on) + 1) / (len(bg) + 1))
                    tag = "incoh" if k_min == 1 else "skip1"
                    dres.variants.append(PointVariant(
                        f"{rn}_{tag}_a{af:.2f}", stat_name, round(ratio, 4), af,
                        round(best_on, 2), round(p_raw, 4),
                        round(min(1.0, p_raw * N_VARIANTS), 4)))
            # joint fit (short-lag repair; kernel ratio, dphi = 0)
            ratio = RATIOS[0][1]
            f_on = _joint_fit_stat(white, merger, lags_samp, ratio,
                                   f0, tau0, f1, tau1, s.dt)
            bg = np.array([_joint_fit_stat(white, int(c), lags_samp[::3], ratio,
                                           f0, tau0, f1, tau1, s.dt)
                           for c in centers[:300]])
            p_raw = float((np.sum(bg >= f_on) + 1) / (len(bg) + 1))
            dres.variants.append(PointVariant(
                f"jointF_a{af:.2f}", "joint_fit", round(ratio, 4), af,
                round(f_on, 2), round(p_raw, 4),
                round(min(1.0, p_raw * N_VARIANTS), 4)))
        res.detectors.append(dres)

    # escalation: same variant Bonferroni-surviving in >=2 detectors
    esc = 0
    names = [v.variant for v in res.detectors[0].variants] if res.detectors else []
    for name in names:
        n_hit = sum(1 for d in res.detectors for v in d.variants
                    if v.variant == name and v.p_bonf < 0.01)
        esc = max(esc, n_hit)
    res.label = "ESCALATE" if esc >= 2 else "NO_POINT_ECHO"
    return res


def run_point(events: list[str], hires: bool = False) -> int:
    have = [e for e in events if (STRAIN_DIR / meta_name(e, hires)).exists()]
    fs_note = "16 kHz crops (_meta16k)" if hires else "4 kHz crops"
    print("=" * 88)
    print("TFPT GW Stage-1d: POINT TEST v2 -- theory-fixed lag (C=3/8: dt = 2.288 M_det)")
    print("  x kernel ratios x mu4 phases; + incoherent / skip-first (morphology,")
    print("  first-echo nonlinearity) + JOINT QNM+train fit (short-lag repair);")
    print(f"  OFF-SOURCE (event-gated) PSD; spin scan af={SPINS};")
    print(f"  Bonferroni x{N_VARIANTS}; lag tol +-25%; strain: {fs_note}")
    print("=" * 88)
    if not have:
        print("  no strain -> nothing to do.")
        return 1

    out = []
    best = {"p": 1.0, "where": ""}
    for ev in have:
        r = point_event(ev, hires)
        print(f"\n  {ev}: M_det={r.mf_det} Msun, predicted lag = {r.lag_pred_ms} ms"
              f"  ->  {r.label}")
        for d in r.detectors:
            parts = []
            for stat in ("coherent", "incoherent", "skip_first", "joint_fit"):
                p = min((v.p_raw for v in d.variants if v.statistic == stat),
                        default=1.0)
                parts.append(f"{stat} p={p:.3f}")
            print(f"    {d.detector:3s}  " + "   ".join(parts))
            for v in d.variants:
                if v.p_bonf < best["p"]:
                    best = {"p": v.p_bonf, "where": f"{ev}/{d.detector}/{v.variant}"}
        out.append({"event": r.event, "mf_det": r.mf_det,
                    "lag_pred_ms": r.lag_pred_ms, "label": r.label,
                    "detectors": [{"detector": d.detector,
                                   "variants": [vars(v) for v in d.variants]}
                                  for d in r.detectors]})

    any_esc = any(e["label"] == "ESCALATE" for e in out)
    verdict = (
        "ESCALATE: a Bonferroni-surviving point-hypothesis excess is coincident in "
        ">=2 detectors -- coherent time-slide follow-up + injections required "
        "before ANY claim." if any_esc else
        f"NO POINT ECHO (v2, systematic-hardened): the TFPT point hypothesis -- "
        f"delay fixed by the C=3/8 gravastar compactness (dt = 2.288 M_det, "
        f"+-25%), kernel ratios (2/3)^6 / (2/3)^3, mu4 per-bounce phases -- "
        f"tested with OFF-SOURCE (event-gated) whitening (no filter ringing), a "
        f"remnant-spin scan af={SPINS}, a morphology-robust incoherent statistic, "
        f"a skip-first-echo variant (first-reflection nonlinearity), and a JOINT "
        f"QNM+train fit that repairs the short-lag subtract-then-search "
        f"self-absorption: no Bonferroni-surviving excess coincident in >=2 "
        f"detectors on any event (best p_bonf = {best['p']:.3f} at "
        f"{best['where']}). The sharpest TFPT echo test is null under all "
        f"systematic variations; upper-bound kernel: no detection, no tension.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out_name = "point_test_16k.json" if hires else "point_test.json"
    (RESULTS / out_name).write_text(json.dumps({
        "stage": f"strain_level_test (TFPT point test v2, Bonferroni x{N_VARIANTS})",
        "strain": fs_note,
        "delay_model": "dt = 2.288 M_det (gravastar-compactness C = 3/8), tol +-25%",
        "systematics": {"psd": "off-source (event-gated) Welch",
                        "spin_scan": list(SPINS),
                        "statistics": ["coherent", "incoherent", "skip_first",
                                       "joint_fit (short-lag repair)"]},
        "ratios": {n: r for n, r in RATIOS},
        "phases_rad": {n: p for n, p in PHASES},
        "events": out, "best_p_bonf": best, "verdict": verdict},
        indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / out_name}")
    return 0

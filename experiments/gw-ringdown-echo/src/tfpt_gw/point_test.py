"""Stage-1d: the TFPT POINT TEST -- theory-fixed lag x kernel-fixed ratio.

The battery (Stage 1c) scans the lag freely; but TFPT PREDICTS the lag: the
gravastar-compactness experiment fixes the horizonless-object compactness to
the Nariai rational C = 3/8, whose tortoise round-trip delay is

    Delta t = 2.288 M            (geometric units; detector-frame M)

-- e.g. 0.77 ms for GW250114 (M_det = 68.6 Msun).  Combining the predicted
delay with the kernel-fixed amplitude ratio gives a POINT hypothesis with a
minimal look-elsewhere budget -- the sharpest TFPT-specific echo test.

Two statistics per (event, detector):

  COHERENT  : the Stage-1c matched filter, restricted to the predicted lag
              +-25% (mass/model tolerance), ratios {(2/3)^6, (2/3)^3} x mu4
              per-bounce phases {0, pi/2, pi, 3pi/2}  (8 variants).
  INCOHERENT: per-echo quadrature matching -- each echo is fit with FREE
              phase (cos+sin at the predicted position), only the positions
              (k Delta t) and the amplitude weights r^k are fixed:
                  S_inc = sum_k r^k a_k / sqrt(sum_k r^{2k})
              with a_k the per-echo quadrature amplitude.  This is robust to
              intra-echo morphology changes (barrier low-pass filtering,
              phase mixing) that degrade the coherent template  (2 variants).

Bonferroni over the 10 variants.  Escalation still requires >=2 coincident
detectors + ratio consistency.  Post-hoc honesty: the delay formula and the
ratios are preregistered numbers (gravastar-compactness / frozen kernel),
but the strain has been seen by earlier stages -- so this stays a
search-target robustness statement, never a detection claim.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .signature_battery import (
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
    whitening_filter,
)

STRAIN_DIR = Path(__file__).resolve().parents[2] / "data" / "strain"
RESULTS = Path(__file__).resolve().parents[2] / "results"

DELAY_COEFF = 2.288                 # Delta t = 2.288 M (gravastar C = 3/8)
LAG_TOL = 0.25                      # +-25% tolerance around the predicted lag
N_LAG = 11
JITTER_S = 0.005
N_BACKGROUND = 800
GUARD_S = 1.0

RATIOS = [("amp_(2/3)^6", (2.0 / 3.0) ** 6), ("energy->(2/3)^3", (2.0 / 3.0) ** 3)]
PHASES = [("dphi0", 0.0), ("dphi90", np.pi / 2),
          ("dphi180", np.pi), ("dphi270", 3 * np.pi / 2)]
N_VARIANTS = len(RATIOS) * len(PHASES) + len(RATIOS)   # coherent + incoherent


@dataclass
class PointVariant:
    variant: str
    statistic: str          # "coherent" | "incoherent"
    ratio: float
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
                     f0: float, tau: float, dt: float) -> float:
    """S_inc = sum_k r^k a_k / sqrt(sum r^{2k}); a_k = free-phase quadrature
    amplitude of echo k at the predicted position (morphology-robust)."""
    n = len(resid)
    num = 0.0
    den = 0.0
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
        a_k = math.hypot(float(seg @ c) / math.sqrt(nc), float(seg @ s) / math.sqrt(ns))
        w = ratio ** k
        num += w * a_k
        den += w * w
    return num / math.sqrt(den) if den > 0 else 0.0


def point_event(event: str, af: float = 0.69) -> PointEvent:
    meta = json.loads((STRAIN_DIR / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)
    f0, tau0 = qnm_22n(mf, af, 0)
    f1, tau1 = qnm_22n(mf, af, 1)
    lag_pred_s = DELAY_COEFF * mf * GMSUN_OVER_C3
    res = PointEvent(event, round(mf, 1), round(lag_pred_s * 1e3, 3))
    rng = np.random.default_rng(5)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        psd_i, scale = whitening_filter(s.data, s.dt)
        white = apply_whitening(s.data, psd_i, scale)
        merger = s.index_at(merger_gps)
        resid, _ = subtract_qnm_multimode(white, merger, [(f0, tau0), (f1, tau1)], s.dt)

        lag0 = lag_pred_s / s.dt
        lags_samp = np.unique(np.round(
            lag0 * np.linspace(1.0 - LAG_TOL, 1.0 + LAG_TOL, N_LAG)).astype(int))
        lags_samp = lags_samp[lags_samp > 0]
        jit = int(JITTER_S / s.dt)
        train_len = int(lags_samp.max()) * N_ECHO + int(6.0 * tau0 / s.dt)
        guard = int(GUARD_S / s.dt)
        lo, hi = guard, len(resid) - train_len - jit - guard
        centers = rng.integers(lo, hi, size=N_BACKGROUND)
        centers = centers[np.abs(centers - merger) > guard]

        dres = PointDetector(det)
        # coherent variants (predicted-lag window only)
        for rn, ratio in RATIOS:
            for pn, dphi in PHASES:
                rho = correlate_bank(resid, lags_samp, ratio, dphi, f0, tau0, s.dt)
                s_on = float(rho[:, merger:merger + jit].max())
                bg = np.array([rho[:, int(c):int(c) + jit].max() for c in centers])
                p_raw = float((np.sum(bg >= s_on) + 1) / (len(bg) + 1))
                dres.variants.append(PointVariant(
                    f"{rn}_{pn}", "coherent", round(ratio, 4), round(s_on, 2),
                    round(p_raw, 4), round(min(1.0, p_raw * N_VARIANTS), 4)))
        # incoherent variants (free phase per echo, morphology-robust)
        for rn, ratio in RATIOS:
            best_on = 0.0
            for ls in lags_samp:
                for t0 in range(merger, merger + jit, max(1, jit // 8)):
                    best_on = max(best_on, _incoherent_stat(
                        resid, t0, int(ls), ratio, f0, tau0, s.dt))
            bg = []
            for c in centers[:300]:
                b = 0.0
                for ls in lags_samp[::3]:
                    b = max(b, _incoherent_stat(resid, int(c), int(ls), ratio,
                                                f0, tau0, s.dt))
                bg.append(b)
            bg = np.asarray(bg)
            p_raw = float((np.sum(bg >= best_on) + 1) / (len(bg) + 1))
            dres.variants.append(PointVariant(
                f"{rn}_incoh", "incoherent", round(ratio, 4), round(best_on, 2),
                round(p_raw, 4), round(min(1.0, p_raw * N_VARIANTS), 4)))
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


def run_point(events: list[str]) -> int:
    have = [e for e in events if (STRAIN_DIR / f"{e}_meta.json").exists()]
    print("=" * 88)
    print("TFPT GW Stage-1d: POINT TEST -- theory-fixed lag (C=3/8: dt = 2.288 M_det)")
    print("  x kernel-fixed ratios {(2/3)^6, (2/3)^3} x mu4 phases + morphology-robust")
    print(f"  incoherent per-echo statistic; Bonferroni x{N_VARIANTS}; lag tol +-25%")
    print("=" * 88)
    if not have:
        print("  no strain -> nothing to do.")
        return 1

    out = []
    best = {"p": 1.0, "where": ""}
    for ev in have:
        r = point_event(ev)
        print(f"\n  {ev}: M_det={r.mf_det} Msun, predicted lag = {r.lag_pred_ms} ms"
              f"  ->  {r.label}")
        for d in r.detectors:
            coh = min((v.p_raw for v in d.variants if v.statistic == "coherent"),
                      default=1.0)
            inc = min((v.p_raw for v in d.variants if v.statistic == "incoherent"),
                      default=1.0)
            print(f"    {d.detector:3s}  best coherent p={coh:.3f}   "
                  f"best incoherent p={inc:.3f}")
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
        f"NO POINT ECHO: the TFPT-specific point hypothesis -- delay fixed by the "
        f"C=3/8 gravastar compactness (dt = 2.288 M_det, +-25%), amplitude ratio "
        f"fixed by the kernel ((2/3)^6 and the energy reading (2/3)^3), mu4 "
        f"per-bounce phases, PLUS a morphology-robust incoherent per-echo "
        f"statistic (free phase per echo; robust to barrier low-pass filtering) "
        f"-- shows no Bonferroni-surviving excess coincident in >=2 detectors on "
        f"any event (best p_bonf = {best['p']:.3f} at {best['where']}). The "
        f"sharpest TFPT echo test is null; upper-bound kernel: no detection, no "
        f"tension claim.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "point_test.json").write_text(json.dumps({
        "stage": f"strain_level_test (TFPT point test, Bonferroni x{N_VARIANTS})",
        "delay_model": "dt = 2.288 M_det (gravastar-compactness C = 3/8), tol +-25%",
        "ratios": {n: r for n, r in RATIOS},
        "phases_rad": {n: p for n, p in PHASES},
        "events": out, "best_p_bonf": best, "verdict": verdict},
        indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'point_test.json'}")
    return 0

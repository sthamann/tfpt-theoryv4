"""Stage-1e: the AREA-QUANTUM spectral comb -- Bekenstein-Mukhanov lines from
TFPT's Delta A = 4 ln3.

BH-specific theory input (tfpt_horizon_readouts / v57, and the archived
prediction set): TFPT fixes the black-hole area quantum to

    Delta A = 4 ln 3  l_p^2  =  ln(N_fam^4) = ln 81 .

Bekenstein-Mukhanov quantisation then makes the horizon a system with a
DISCRETE transition spectrum: the elementary transition (angular) frequency is

    omega_BM = kappa * Delta A / (8 pi) = ln3 / (8 pi M)  =  T_H ln 3

-- exactly the Hod frequency, now read as a LINE SPECTRUM: the horizon
absorbs/reflects preferentially at harmonics f_n = n * f_BM,
f_BM = ln3 / (16 pi^2 M_det_sec).  For a 68 Msun detector-frame remnant
f_BM ~ 20.6 Hz, i.e. ~20 harmonics across the LVK band -- a COMB in the
post-merger residual spectrum.  This signature was never tested before
(the echo searches test time-domain trains; this is the frequency-domain
face of the same quantisation).

Statistic: the post-merger residual (off-source-gated whitening, joint
220+221 subtraction) is Fourier-analysed in a [T_START, T_END] window after
the merger; S_comb = mean residual power in bins at f_n = n f_BM (n >= 2,
within [F_LO, F_HI]) divided by the mean in interleaved off-comb bins.
Backgrounds: (a) off-source windows (noise-only comb statistic), and
(b) a SPACING battery: the same statistic at scaled spacings
{0.8, 0.9, 1.1, 1.25} x f_BM -- the TFPT spacing must be special, not any
comb (template-specificity control).  Bonferroni over the spin scan.

HONEST SCOPE: a null here is weak evidence at current sensitivity (the
line widths, the coupling of the comb to the exterior, and the fraction of
residual power that would carry the lines are all model-dependent) -- this
is a search target with a documented power limitation, not a kill test.
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
    qnm_22n,
    subtract_qnm_multimode,
)
from .strain_data import (
    GMSUN_OVER_C3,
    apply_whitening,
    detector_frame_mass,
    read_hdf5,
    whitening_filter_gated,
)

STRAIN_DIR = Path(__file__).resolve().parents[2] / "data" / "strain"
RESULTS = Path(__file__).resolve().parents[2] / "results"

LN3 = math.log(3.0)
T_START_S = 0.005          # analysis window after merger (skip the loud ringdown)
T_END_S = 1.0
F_LO, F_HI = 24.0, 512.0   # band for comb harmonics
N_MIN = 2                  # skip the fundamental (at/below the seismic wall)
SPACING_BATTERY = (0.8, 0.9, 1.0, 1.1, 1.25)
N_BACKGROUND = 300
SPINS = (0.60, 0.69, 0.80)
N_TRIALS = len(SPINS)      # Bonferroni: spin scan (spacing battery is a control)


def f_bm_hz(mf_det_msun: float) -> float:
    """Bekenstein-Mukhanov fundamental f_BM = ln3/(16 pi^2 M) for Delta A = 4 ln3."""
    m_sec = mf_det_msun * GMSUN_OVER_C3
    return LN3 / (16.0 * math.pi ** 2 * m_sec)


def comb_statistic(seg: np.ndarray, dt: float, spacing_hz: float) -> float:
    """Mean residual power at comb harmonics / mean in interleaved off-comb bins."""
    n = len(seg)
    win = np.hanning(n)
    spec = np.abs(np.fft.rfft(seg * win)) ** 2
    freqs = np.fft.rfftfreq(n, dt)
    df = freqs[1] - freqs[0]
    on, off = [], []
    k = N_MIN
    while True:
        f_on = k * spacing_hz
        if f_on > F_HI:
            break
        if f_on >= F_LO:
            i_on = int(round(f_on / df))
            i_off = int(round((f_on + 0.5 * spacing_hz) / df))
            if 0 < i_on < len(spec) and 0 < i_off < len(spec):
                on.append(spec[i_on - 1:i_on + 2].mean())
                off.append(spec[i_off - 1:i_off + 2].mean())
        k += 1
    if len(on) < 4 or np.mean(off) <= 0:
        return 0.0
    return float(np.mean(on) / np.mean(off))


@dataclass
class CombDetector:
    detector: str
    n_harmonics: int
    s_on: dict = field(default_factory=dict)      # spacing_scale -> statistic
    p_raw: float = 1.0
    p_bonf: float = 1.0
    spacing_specific: bool = False
    best_spin: float = 0.69


@dataclass
class CombEvent:
    event: str
    mf_det: float
    f_bm_hz: float
    detectors: list[CombDetector] = field(default_factory=list)
    label: str = ""


def comb_event(event: str) -> CombEvent:
    meta = json.loads((STRAIN_DIR / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)
    fbm = f_bm_hz(mf)
    res = CombEvent(event, round(mf, 1), round(fbm, 2))
    rng = np.random.default_rng(7)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        merger = s.index_at(merger_gps)
        psd_i, scale = whitening_filter_gated(
            s.data, s.dt, merger - int(GATE_PRE_S / s.dt),
            merger + int(GATE_POST_S / s.dt))
        white = apply_whitening(s.data, psd_i, scale)

        i0 = merger + int(T_START_S / s.dt)
        i1 = merger + int(T_END_S / s.dt)
        seg_len = i1 - i0
        guard = int(1.0 / s.dt)
        lo, hi = guard, len(white) - seg_len - guard
        centers = rng.integers(lo, hi, size=N_BACKGROUND)
        centers = centers[np.abs(centers - merger) > guard]

        best = None
        for af in SPINS:
            f0, tau0 = qnm_22n(mf, af, 0)
            f1, tau1 = qnm_22n(mf, af, 1)
            resid, _ = subtract_qnm_multimode(white, merger,
                                              [(f0, tau0), (f1, tau1)], s.dt)
            seg = resid[i0:i1]
            s_scales = {sc: comb_statistic(seg, s.dt, sc * fbm)
                        for sc in SPACING_BATTERY}
            s_on = s_scales[1.0]
            bg = np.array([comb_statistic(resid[int(c):int(c) + seg_len], s.dt, fbm)
                           for c in centers])
            p_raw = float((np.sum(bg >= s_on) + 1) / (len(bg) + 1))
            if best is None or p_raw < best[0]:
                best = (p_raw, af, s_scales)

        p_raw, af_best, s_scales = best
        n_harm = sum(1 for k in range(N_MIN, 1000)
                     if F_LO <= k * fbm <= F_HI)
        # spacing specificity: the TFPT spacing must beat the scaled controls
        specific = all(s_scales[1.0] >= s_scales[sc]
                       for sc in SPACING_BATTERY if sc != 1.0)
        res.detectors.append(CombDetector(
            det, n_harm, {str(sc): round(v, 3) for sc, v in s_scales.items()},
            round(p_raw, 4), round(min(1.0, p_raw * N_TRIALS), 4),
            specific, af_best))

    n_hit = sum(1 for d in res.detectors
                if d.p_bonf < 0.01 and d.spacing_specific)
    res.label = "ESCALATE" if n_hit >= 2 else "NO_BM_COMB"
    return res


def run_bm_comb(events: list[str]) -> int:
    have = [e for e in events if (STRAIN_DIR / f"{e}_meta.json").exists()]
    print("=" * 88)
    print("TFPT GW Stage-1e: AREA-QUANTUM SPECTRAL COMB (Bekenstein-Mukhanov lines,")
    print("  Delta A = 4 ln3 => f_n = n ln3/(16 pi^2 M_det); off-source PSD;")
    print(f"  spacing battery {SPACING_BATTERY} as specificity control; spin scan)")
    print("=" * 88)
    if not have:
        print("  no strain -> nothing to do.")
        return 1

    out = []
    best = {"p": 1.0, "where": ""}
    for ev in have:
        r = comb_event(ev)
        print(f"\n  {ev}: M_det={r.mf_det} Msun, f_BM = {r.f_bm_hz} Hz  ->  {r.label}")
        for d in r.detectors:
            print(f"    {d.detector:3s}  S(comb)={d.s_on['1.0']:.3f} "
                  f"(controls {', '.join(f'{k}x:{v:.3f}' for k, v in d.s_on.items() if k != '1.0')}) "
                  f"p={d.p_raw:.3f} specific={d.spacing_specific} "
                  f"[{d.n_harmonics} harmonics, af={d.best_spin}]")
            if d.p_bonf < best["p"]:
                best = {"p": d.p_bonf, "where": f"{ev}/{d.detector}"}
        out.append({"event": r.event, "mf_det": r.mf_det, "f_bm_hz": r.f_bm_hz,
                    "label": r.label,
                    "detectors": [vars(d) for d in r.detectors]})

    any_esc = any(e["label"] == "ESCALATE" for e in out)
    verdict = (
        "ESCALATE: a spacing-specific BM-comb excess is coincident in >=2 "
        "detectors -- injections + time-slides required before ANY claim."
        if any_esc else
        f"NO BM COMB: the Bekenstein-Mukhanov line comb implied by TFPT's area "
        f"quantum Delta A = 4 ln3 (f_n = n ln3/(16 pi^2 M_det), ~10-25 harmonics "
        f"in band) shows no spacing-specific, Bonferroni-surviving excess "
        f"coincident in >=2 detectors on any event (best p_bonf = {best['p']:.3f} "
        f"at {best['where']}). HONEST POWER NOTE: line widths, exterior coupling "
        f"and the residual-power fraction carrying the lines are model-dependent "
        f"-- this is a well-defined search-target null at current sensitivity, "
        f"not a kill test of the area quantum.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "bm_comb.json").write_text(json.dumps({
        "stage": "strain_level_test (area-quantum BM spectral comb, first run)",
        "area_quantum": "Delta A = 4 ln3 = ln 81 (v57 / horizon readouts)",
        "f_bm_model": "f_BM = ln3/(16 pi^2 M_det_sec); harmonics n>=2 in 24-512 Hz",
        "spacing_battery": list(SPACING_BATTERY),
        "spin_scan": list(SPINS),
        "events": out, "best_p_bonf": best, "verdict": verdict},
        indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'bm_comb.json'}")
    return 0

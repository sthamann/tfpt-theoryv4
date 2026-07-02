"""Stage-1f: the OFFSET-TRAIN point test -- scrambling delay x cavity spacing.

All earlier stages anchor the echo train at the merger with offset = spacing.
TFPT motivates a DIFFERENT geometry: the fast-scrambling time of the horizon,

    t_scr = (beta/2pi) ln S = 4 M ln S,      ln S = 2 ln(M/l_P) + ln 4pi,

(~0.25 s for a 68 Msun detector-frame remnant) can delay the FIRST re-emission
globally, while the cavity keeps the Nariai/gravastar spacing

    Delta t = 2.288 M          (C = 3/8, detector frame).

That is a TWO-number point hypothesis (offset ~ t_scr, spacing = 2.288 M) that
no previous stage tested: a train starting ~0.25 s after merger with ~0.8 ms
spacing.  Bonus: at t_scr the primary ringdown (tau ~ 4 ms) has decayed by
e^{-60} -- NO QNM subtraction is needed, removing that whole systematic.

Scan: offset window [0.5, 1.5] x t_scr (coupling/entropy-prefactor tolerance),
spacing grid +-25% around 2.288 M (7 points), ratios {(2/3)^6, (2/3)^3},
phases {0, pi}; statistic = max matched-filter rho over the offset window and
spacing grid (FFT bank gives all offsets at once); background = the same max
over random off-source windows of equal length.  OFF-SOURCE (event-gated)
PSD.  Bonferroni over the 28 coherent variants.  Escalation requires >=2
coincident detectors.  Search-target firewall: upper-bound kernel, post-hoc
strain, no detection claim.
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
    correlate_bank,
    qnm_22n,
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

M_SUN_METERS = 1476.6250          # GM_sun/c^2
L_PLANCK_M = 1.616255e-35
DELAY_COEFF = 2.288               # cavity spacing (C = 3/8), in M
SPACING_TOL = 0.25
N_SPACING = 7
OFFSET_WINDOW = (0.5, 1.5)        # x t_scr
N_BACKGROUND = 400
GUARD_S = 2.0

RATIOS = [("amp_(2/3)^6", (2.0 / 3.0) ** 6), ("energy->(2/3)^3", (2.0 / 3.0) ** 3)]
PHASES = [("dphi0", 0.0), ("dphi180", np.pi)]
N_VARIANTS = len(RATIOS) * len(PHASES) * N_SPACING


def t_scrambling_s(mf_det_msun: float) -> float:
    """Fast-scrambling time t_scr = 4 M ln S, ln S = 2 ln(M/l_P) + ln 4pi."""
    m_sec = mf_det_msun * GMSUN_OVER_C3
    m_meters = mf_det_msun * M_SUN_METERS
    ln_s = 2.0 * math.log(m_meters / L_PLANCK_M) + math.log(4.0 * math.pi)
    return 4.0 * m_sec * ln_s


@dataclass
class OffsetDetector:
    detector: str
    variants: list[dict] = field(default_factory=list)


@dataclass
class OffsetEvent:
    event: str
    mf_det: float
    t_scr_s: float
    spacing_ms: float
    detectors: list[OffsetDetector] = field(default_factory=list)
    label: str = ""


def offset_event(event: str, af: float = 0.69) -> OffsetEvent:
    meta = json.loads((STRAIN_DIR / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)
    f0, tau0 = qnm_22n(mf, af, 0)
    t_scr = t_scrambling_s(mf)
    spacing_s = DELAY_COEFF * mf * GMSUN_OVER_C3
    res = OffsetEvent(event, round(mf, 1), round(t_scr, 4),
                      round(spacing_s * 1e3, 3))
    rng = np.random.default_rng(11)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        merger = s.index_at(merger_gps)
        psd_i, scale = whitening_filter_gated(
            s.data, s.dt, merger - int(GATE_PRE_S / s.dt),
            merger + int(GATE_POST_S / s.dt))
        white = apply_whitening(s.data, psd_i, scale)
        # no QNM subtraction needed: the offset window sits ~60 e-folds after
        # the ringdown -- the train is searched on the whitened data directly

        spacings = np.unique(np.round(
            (spacing_s / s.dt)
            * np.linspace(1.0 - SPACING_TOL, 1.0 + SPACING_TOL, N_SPACING)).astype(int))
        spacings = spacings[spacings > 0]
        w0 = merger + int(OFFSET_WINDOW[0] * t_scr / s.dt)
        w1 = merger + int(OFFSET_WINDOW[1] * t_scr / s.dt)
        win_len = w1 - w0
        guard = int(GUARD_S / s.dt)
        lo, hi = guard, len(white) - win_len - guard
        centers = rng.integers(lo, hi, size=N_BACKGROUND)
        centers = centers[np.abs(centers - merger) > guard]

        dres = OffsetDetector(det)
        for rn, ratio in RATIOS:
            for pn, dphi in PHASES:
                rho = correlate_bank(white, spacings, ratio, dphi, f0, tau0, s.dt)
                # per-spacing statistics (spacing is part of the trials budget;
                # note: at 4 kHz the ~0.8 ms cavity spacing is only ~3 samples,
                # so the integer spacing grid is coarse for low-mass events)
                for i, sp in enumerate(spacings):
                    s_on = float(rho[i, w0:w1].max())
                    bg = np.array([rho[i, int(c):int(c) + win_len].max()
                                   for c in centers])
                    p_raw = float((np.sum(bg >= s_on) + 1) / (len(bg) + 1))
                    dres.variants.append({
                        "variant": f"{rn}_{pn}_sp{sp * s.dt * 1e3:.2f}ms",
                        "ratio": round(ratio, 4),
                        "spacing_ms": round(sp * s.dt * 1e3, 2),
                        "s_on": round(s_on, 2), "p_raw": round(p_raw, 4)})
        # Bonferroni over the ACTUAL per-detector variant count (the integer
        # spacing grid can collapse below the nominal N_SPACING)
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
    res.label = "ESCALATE" if esc >= 2 else "NO_OFFSET_TRAIN"
    return res


def run_offset(events: list[str]) -> int:
    have = [e for e in events if (STRAIN_DIR / f"{e}_meta.json").exists()]
    print("=" * 88)
    print("TFPT GW Stage-1f: OFFSET-TRAIN point test -- scrambling delay x cavity spacing")
    print("  offset ~ t_scr = 4 M ln S (window 0.5-1.5x), spacing = 2.288 M +-25%;")
    print(f"  no QNM subtraction needed (window ~60 e-folds post-ringdown);")
    print(f"  OFF-SOURCE PSD; Bonferroni x{N_VARIANTS}")
    print("=" * 88)
    if not have:
        print("  no strain -> nothing to do.")
        return 1

    out = []
    best = {"p": 1.01, "where": "none below 1"}
    for ev in have:
        r = offset_event(ev)
        print(f"\n  {ev}: M_det={r.mf_det} Msun, t_scr = {r.t_scr_s*1e3:.0f} ms, "
              f"spacing = {r.spacing_ms} ms  ->  {r.label}")
        for d in r.detectors:
            p_min = min(v["p_raw"] for v in d.variants)
            print(f"    {d.detector:3s}  best raw p = {p_min:.3f} over "
                  f"{len(d.variants)} (ratio x phase x spacing) variants")
            for v in d.variants:
                if v["p_bonf"] < best["p"]:
                    best = {"p": v["p_bonf"],
                            "where": f"{ev}/{d.detector}/{v['variant']}"}
        out.append({"event": r.event, "mf_det": r.mf_det, "t_scr_s": r.t_scr_s,
                    "spacing_ms": r.spacing_ms, "label": r.label,
                    "detectors": [{"detector": d.detector, "variants": d.variants}
                                  for d in r.detectors]})

    any_esc = any(e["label"] == "ESCALATE" for e in out)
    verdict = (
        "ESCALATE: a Bonferroni-surviving offset-train excess is coincident in >=2 "
        "detectors -- injections + time-slides required before ANY claim."
        if any_esc else
        f"NO OFFSET TRAIN: the two-number TFPT point hypothesis -- first echo "
        f"delayed by the scrambling time t_scr = 4 M ln S (~0.25 s at 68 Msun), "
        f"train spaced by the C=3/8 cavity delay 2.288 M (~0.8 ms) -- shows no "
        f"Bonferroni-surviving excess coincident in >=2 detectors on any of the "
        f"10 loudest events (best p_bonf = {min(best['p'], 1.0):.3f} at {best['where']}). "
        f"The offset != spacing geometry, the last untested train configuration, "
        f"is null; upper-bound kernel: no detection, no tension claim.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "offset_train.json").write_text(json.dumps({
        "stage": f"strain_level_test (offset-train point test, Bonferroni x{N_VARIANTS})",
        "offset_model": "t_scr = 4 M ln S, ln S = 2 ln(M/l_P) + ln 4pi; window 0.5-1.5x",
        "spacing_model": "2.288 M_det (gravastar C = 3/8), +-25%",
        "events": out, "best_p_bonf": best, "verdict": verdict},
        indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'offset_train.json'}")
    return 0

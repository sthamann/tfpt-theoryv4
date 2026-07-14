"""Stage-1h: INJECTION CAMPAIGN -> absolute echo-amplitude upper limits (eps_90).

The nine Stage-1 null stages say "no echo found"; this module says HOW LOUD an
echo would have had to be for the pipeline to find it -- turning the nulls into
CALIBRATED ABSOLUTE UPPER LIMITS (the number the comb-meta-limit horizon tier
lists as missing).

Method (per event, per detector, on REAL strain):

  1. Whiten with the EXACT Stage-1d off-source (event-gated) PSD and subtract
     the joint (2,2,0)+(2,2,1) QNM -- identical preprocessing to the point test.
  2. Inject synthetic C=3/8 kernel echo trains into OFF-SOURCE stretches of the
     whitened residual: delay = 2.288 M_det (detector frame, rounded to the
     sample grid), per-echo amplitude ratio (2/3)^6, dphi = 0, af = 0.69 QNM
     morphology (the battery's echo_template); first-echo amplitude
     = eps_inj x A220, where A220 is the event's measured (2,2,0) amplitude
     from the same joint QNM fit (whitened units).
  3. Run the EXACT Stage-1d coherent point statistic on each injection: the
     correlate_bank matched filter over the predicted-lag grid (+-25%, N_LAG
     points), max over the 5 ms anchor-jitter window, p_raw against the same
     off-source background (N_BACKGROUND centers).  The statistic is LINEAR in
     the data, so the injection's contribution to the correlation map is a
     precomputed, shift-invariant response (computed through correlate_bank
     itself on the injection alone -- zero convention drift); each injection
     then costs one window-max, and the campaign runs >>50 injections exactly.
  4. eps_90 = the smallest eps_inj recovered with p_raw < 0.01 in >= 90% of
     N_INJ injections (log-grid bracket + bisection, then a 200-injection
     confirmation at the reported value).

Absolute statement per event (the calibration of the on-source null):
"on-source null => first-echo amplitude < eps_90 x A220 at 90% CL" (coherent
kernel-template limit).  The statement is only valid for streams whose
ON-SOURCE statistic is itself null at the recovery threshold (p_on >= 0.01
for the same coherent kernel variant) -- streams that fired on-source
(GW200129/V1's known single-stream excess, rejected by Bonferroni +
coincidence) get an eps_90 for the record but CANNOT anchor the limit; the
event limit is the best eps_90 among the on-source-null streams.  Stack
level: the conservative combined limit is the best single event's eps_90
(each event alone is a valid 90% CL test under the universal-eps
hypothesis); the joint product limit is also reported.

HONEST SCOPE: these are COHERENT-TEMPLATE limits (injected morphology = search
template, af = 0.69, exact predicted lag).  Morphology-robust limits (barrier
low-pass, phase decoherence, lag/spin mismatch) would be somewhat weaker, and
the off-source calibration does not include the partial absorption of an
on-source train by the QNM fit (the short-lag overlap that Stage-1d's joint
fit addresses) -- both effects would weaken the effective limit somewhat.
eps_90 is relative to the MEASURED A220 of the existing QNM fit; events where
that fit is weak (low whitened A220) get correspondingly weak eps_90.
Upper-bound kernel firewall: no detection, no tension claim.
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
    echo_template,
    qnm_22n,
    subtract_qnm_multimode,
)
from .strain_data import (
    GMSUN_OVER_C3,
    align_ringdown,
    apply_whitening,
    detector_frame_mass,
    highpass,
    read_hdf5,
    whitening_filter_gated,
)
from .point_test import (
    DELAY_COEFF,
    GUARD_S,
    JITTER_S,
    LAG_TOL,
    N_BACKGROUND,
    N_LAG,
    meta_name,
)

STRAIN_DIR = Path(__file__).resolve().parents[2] / "data" / "strain"
RESULTS = Path(__file__).resolve().parents[2] / "results"

RATIO = (2.0 / 3.0) ** 6            # kernel per-echo amplitude ratio
AF_INJ = 0.69                       # injection/recovery QNM spin (scan centre)
P_RECOVER = 0.01                    # Stage-1d raw-p recovery criterion
FRAC_RECOVER = 0.90                 # eps_90 definition
N_INJ = 60                          # injections per eps trial (>= 50)
N_CONFIRM = 200                     # confirmation injections at the reported eps_90
EPS_GRID = np.geomspace(0.05, 25.6, 10)  # common bracket grid (factor-2 steps)
N_BISECT = 6                        # log-bisection steps inside the bracket


@dataclass
class DetectorLimit:
    detector: str
    amp220: float
    lag_samp: int
    n_lags: int
    eps90: float | None
    recovery_at_eps90: float
    p_on: float = 1.0                     # on-source p of the SAME coherent variant
    on_source_null: bool = True           # p_on >= P_RECOVER: the limit is valid
    eps_grid: list[float] = field(default_factory=list)
    recovery_grid: list[float] = field(default_factory=list)
    note: str = ""


@dataclass
class EventLimit:
    event: str
    mf_det: float
    lag_pred_ms: float
    fs_hz: float
    detectors: list[DetectorLimit] = field(default_factory=list)
    eps90_event: float | None = None      # best limit among on-source-null streams


def _recovery_fraction(rho_data: np.ndarray, resp: np.ndarray, bg_sorted: np.ndarray,
                       amp: float, positions: np.ndarray, offsets: np.ndarray,
                       jit: int) -> float:
    """Fraction of injections (amplitude `amp`, anchors positions+offsets)
    recovered at p_raw < P_RECOVER against the off-source background."""
    n_bg = len(bg_sorted)
    # p_raw = (#bg >= s_on + 1)/(n_bg + 1) < P_RECOVER  <=>  #bg >= s_on <= k_max
    k_max = int(math.ceil(P_RECOVER * (n_bg + 1) - 1)) - 1
    if k_max < 0:
        return 0.0
    s_thresh = bg_sorted[k_max]           # bg sorted descending; need s_on > bg[k_max]
    hits = 0
    for t0, u in zip(positions, offsets):
        window = rho_data[:, t0:t0 + jit] + amp * resp[:, jit - u:2 * jit - u]
        if float(window.max()) > s_thresh:
            hits += 1
    return hits / len(positions)


def limit_event(event: str, hires: bool = False, align: bool = False,
                highpass_hz: float | None = None) -> EventLimit:
    meta = json.loads((STRAIN_DIR / meta_name(event, hires)).read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)
    lag_pred_s = DELAY_COEFF * mf * GMSUN_OVER_C3
    res = EventLimit(event, round(mf, 1), round(lag_pred_s * 1e3, 3), 0.0)
    rng = np.random.default_rng(11)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        res.fs_hz = round(s.fs)
        merger = s.index_at(merger_gps)
        # OPT-IN (default off = frozen behavior): high-pass to remove sub-hz seismic power
        # that a single-Welch whitening mishandles on O4 4 kHz data (needed for GW250114).
        data = highpass(s.data, s.dt, highpass_hz) if highpass_hz else s.data
        n = len(data)

        # EXACT Stage-1d preprocessing: off-source gated PSD -> whiten -> joint
        # (220)+(221) subtraction; amp220 is the measured A220 (whitened units). With the
        # O4 conditioning on (highpass set), use a median-Welch PSD (robust to the
        # non-stationary lines that otherwise over-whiten and suppress the ringdown).
        psd_i, scale = whitening_filter_gated(
            data, s.dt, merger - int(GATE_PRE_S / s.dt),
            merger + int(GATE_POST_S / s.dt),
            average="median" if highpass_hz else "mean")
        white = apply_whitening(data, psd_i, scale)
        # OPT-IN (default off = frozen behavior): align the QNM start to the whitened
        # ringdown-envelope peak (fixes the ~15-40 ms nominal-merger early-start bias).
        if align:
            merger = align_ringdown(white, merger, s.dt)
        f0, tau0 = qnm_22n(mf, AF_INJ, 0)
        f1, tau1 = qnm_22n(mf, AF_INJ, 1)
        resid, amp220 = subtract_qnm_multimode(white, merger,
                                               [(f0, tau0), (f1, tau1)], s.dt)

        # EXACT Stage-1d coherent filter: predicted-lag grid, kernel ratio, dphi=0
        lag0 = lag_pred_s / s.dt
        lags_samp = np.unique(np.round(
            lag0 * np.linspace(1.0 - LAG_TOL, 1.0 + LAG_TOL, N_LAG)).astype(int))
        lags_samp = lags_samp[lags_samp > 0]
        jit = int(JITTER_S / s.dt)
        guard = int(GUARD_S / s.dt)
        train_len = int(lags_samp.max()) * N_ECHO + int(6.0 * tau0 / s.dt)
        rho_data = correlate_bank(resid, lags_samp, RATIO, 0.0, f0, tau0, s.dt)

        # off-source background of the on-statistic (identical to the point test)
        lo, hi = guard, n - train_len - jit - guard
        centers = rng.integers(lo, hi, size=N_BACKGROUND)
        centers = centers[np.abs(centers - merger) > guard]
        bg = np.array([rho_data[:, int(c):int(c) + jit].max() for c in centers])
        bg_sorted = np.sort(bg)[::-1]

        # on-source p of the SAME variant: only a null stream can anchor a limit
        s_on = float(rho_data[:, merger:merger + jit].max())
        p_on = float((np.sum(bg >= s_on) + 1) / (len(bg) + 1))

        # unit-first-echo injection response through correlate_bank itself:
        # train = echo_template / RATIO (first echo amplitude exactly 1) at the
        # PREDICTED lag rounded to the sample grid
        lag_inj = max(1, int(round(lag0)))
        t_ref = n // 2
        inj_vec = np.zeros(n)
        tmpl = echo_template(train_len, lag_inj, RATIO, 0.0, f0, tau0, s.dt) / RATIO
        inj_vec[t_ref:t_ref + train_len] = tmpl
        rho_unit = correlate_bank(inj_vec, lags_samp, RATIO, 0.0, f0, tau0, s.dt)
        resp = rho_unit[:, t_ref - jit:t_ref + jit]     # delta in [-jit, jit)

        # injection anchors: off-source, clear of the event and the edges
        pos_lo, pos_hi = guard + jit, n - train_len - 2 * jit - guard
        positions = rng.integers(pos_lo, pos_hi, size=4 * N_INJ + N_CONFIRM)
        positions = positions[np.abs(positions - merger) > guard + train_len]
        offsets = rng.integers(0, jit, size=len(positions))

        def recovery(eps: float, n_use: int = N_INJ) -> float:
            return _recovery_fraction(rho_data, resp, bg_sorted,
                                      eps * amp220, positions[:n_use],
                                      offsets[:n_use], jit)

        dres = DetectorLimit(det, round(amp220, 3), lag_inj, len(lags_samp),
                             None, 0.0, round(p_on, 4), p_on >= P_RECOVER)
        if not dres.on_source_null:
            dres.note = (f"on-source p = {p_on:.4f} < {P_RECOVER} for this variant "
                         "(known single-stream excess, Bonferroni/coincidence-"
                         "rejected) -- eps_90 recorded but cannot anchor the limit")
        if amp220 <= 0:
            dres.note = "A220 fit non-positive -- no relative limit possible"
            res.detectors.append(dres)
            continue

        # recovery curve on the common grid, then bracket + log-bisection
        rec_grid = [recovery(float(e)) for e in EPS_GRID]
        dres.eps_grid = [round(float(e), 4) for e in EPS_GRID]
        dres.recovery_grid = [round(r, 3) for r in rec_grid]
        i_hit = next((i for i, r in enumerate(rec_grid) if r >= FRAC_RECOVER), None)
        if i_hit is None:
            dres.note = (f"recovery < {FRAC_RECOVER:.0%} even at eps = "
                         f"{EPS_GRID[-1]:.1f} -- detector stream insensitive")
            res.detectors.append(dres)
            continue
        if i_hit == 0:
            eps_lo, eps_hi = EPS_GRID[0] / 4.0, float(EPS_GRID[0])
        else:
            eps_lo, eps_hi = float(EPS_GRID[i_hit - 1]), float(EPS_GRID[i_hit])
        for _ in range(N_BISECT):
            mid = math.sqrt(eps_lo * eps_hi)
            if recovery(mid) >= FRAC_RECOVER:
                eps_hi = mid
            else:
                eps_lo = mid
        eps90 = eps_hi                                   # smallest eps seen to pass
        # BINDING confirmation: the reported eps_90 must pass the criterion on
        # the larger N_CONFIRM sample (the N_INJ bisection has ~4% binomial
        # noise at 90%); step up until it does
        rec_conf = recovery(eps90, N_CONFIRM)
        while rec_conf < FRAC_RECOVER:
            eps90 *= 1.15
            rec_conf = recovery(eps90, N_CONFIRM)
        dres.eps90 = round(eps90, 4)
        dres.recovery_at_eps90 = round(rec_conf, 3)
        res.detectors.append(dres)

    got = [d.eps90 for d in res.detectors
           if d.eps90 is not None and d.on_source_null]
    res.eps90_event = min(got) if got else None
    return res


def run_inject(events: list[str], hires: bool = False) -> int:
    have = [e for e in events if (STRAIN_DIR / meta_name(e, hires)).exists()]
    fs_note = "16 kHz crops (_meta16k)" if hires else "4 kHz crops"
    print("=" * 88)
    print("TFPT GW Stage-1h: INJECTION CAMPAIGN -> absolute first-echo amplitude limits")
    print(f"  kernel train (delay 2.288 M_det, ratio (2/3)^6, af={AF_INJ}) injected into")
    print("  OFF-SOURCE real whitened strain; EXACT Stage-1d coherent point statistic;")
    print(f"  eps_90 = first-echo amplitude (x A220) recovered at p_raw<{P_RECOVER} in")
    print(f"  >={FRAC_RECOVER:.0%} of {N_INJ} injections (confirmed with {N_CONFIRM}); "
          f"strain: {fs_note}")
    print("=" * 88)
    missing = [e for e in events if e not in have]
    if missing:
        print(f"  (no strain for {missing}; fetch first)")
    if not have:
        print("  no strain -> nothing to do.")
        return 1

    out = []
    for ev in have:
        r = limit_event(ev, hires)
        print(f"\n  {ev}: M_det={r.mf_det} Msun, predicted lag = {r.lag_pred_ms} ms "
              f"({r.fs_hz:.0f} Hz strain)")
        for d in r.detectors:
            if d.eps90 is None:
                print(f"    {d.detector:3s}  A220={d.amp220:7.3f}  eps_90 = --   {d.note}")
            else:
                gate = "" if d.on_source_null else "  [NOT limit-anchoring]"
                print(f"    {d.detector:3s}  A220={d.amp220:7.3f}  lag={d.lag_samp:3d} samp "
                      f"({d.n_lags} lag steps)  p_on={d.p_on:.3f}  "
                      f"eps_90 = {d.eps90:7.4f}  (recovery {d.recovery_at_eps90:.1%})  "
                      f"=> first echo < {d.eps90 * d.amp220:.3f} whitened units{gate}")
                if d.note:
                    print(f"         note: {d.note}")
        if r.eps90_event is not None:
            print(f"    -> event limit (best detector): first-echo amplitude "
                  f"< {r.eps90_event:.4f} x A220 at 90% CL")
        out.append({"event": r.event, "mf_det": r.mf_det,
                    "lag_pred_ms": r.lag_pred_ms, "fs_hz": r.fs_hz,
                    "eps90_event": r.eps90_event,
                    "detectors": [vars(d) for d in r.detectors]})

    # stack-level: conservative = best single event (each event alone is a valid
    # 90% CL test of a universal eps); joint product limit as the secondary view
    per_event = [(e["event"], e["eps90_event"]) for e in out
                 if e["eps90_event"] is not None]
    stack_cons = min((x for _, x in per_event), default=None)
    stack_joint = None
    if per_event:
        # joint: smallest grid eps where 1 - prod(1 - r_e) >= 0.9, using each
        # event's best-detector recovery curve on the common grid
        joint_miss = np.ones(len(EPS_GRID))
        for e in out:
            dets = [d for d in e["detectors"]
                    if d["eps90"] is not None and d["on_source_null"]]
            if not dets:
                continue
            best = min(dets, key=lambda d: d["eps90"])
            joint_miss *= 1.0 - np.asarray(best["recovery_grid"])
        idx = np.nonzero(1.0 - joint_miss >= FRAC_RECOVER)[0]
        if idx.size:
            stack_joint = round(float(EPS_GRID[idx[0]]), 4)

    verdict = (
        "ABSOLUTE LIMITS (coherent kernel template): the nine-stage on-source null, "
        "calibrated by off-source injections of the C=3/8 kernel train "
        "(delay 2.288 M_det, ratio (2/3)^6) into the real whitened strain, implies "
        "per event 'first-echo amplitude < eps_90 x A220 at 90% CL': "
        + "; ".join(f"{ev} eps_90 = {x:.3f}" for ev, x in per_event)
        + (f". Stack (universal eps, conservative single-best-event): eps_90 = "
           f"{stack_cons:.3f}" if stack_cons is not None else "")
        + (f"; joint product view: {stack_joint:.3f}" if stack_joint is not None else "")
        + ". Only on-source-null streams (p_on >= 0.01 for the same variant) anchor "
          "the limits. Coherent-template limits -- morphology-robust limits and the "
          "on-source QNM-fit train absorption would weaken them somewhat. eps_90 is "
          "relative to the measured whitened A220 of each stream. Upper-bound "
          "kernel: no detection, no tension claim.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    out_name = "injection_limits_16k.json" if hires else "injection_limits.json"
    (RESULTS / out_name).write_text(json.dumps({
        "stage": "strain_level_test (Stage 1h: injection-calibrated absolute limits)",
        "strain": fs_note,
        "injection_model": ("coherent kernel train: delay 2.288 M_det (C=3/8), "
                            "per-echo ratio (2/3)^6, dphi=0, af=0.69 QNM morphology; "
                            "first-echo amplitude = eps x measured A220 "
                            "(whitened units, joint 220+221 fit)"),
        "recovery_criterion": {"statistic": "Stage-1d coherent point statistic "
                                            "(predicted-lag grid +-25%, 5 ms jitter, "
                                            "off-source background)",
                               "p_raw": P_RECOVER, "fraction": FRAC_RECOVER,
                               "n_injections": N_INJ, "n_confirm": N_CONFIRM,
                               "limit_gate": "only streams with on-source p_on >= "
                                             "0.01 for the same coherent variant "
                                             "anchor a limit"},
        "events": out,
        "stack": {"eps90_conservative_best_event": stack_cons,
                  "eps90_joint_product": stack_joint,
                  "assumption": "universal eps across events (kernel bound is "
                                "universal); joint view additionally assumes "
                                "independent streams"},
        "verdict": verdict}, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / out_name}")
    return 0

"""Stage-1c: SIGNATURE BATTERY -- "could the echo signature be different?"

The primary Stage-1/1b searches froze ONE template reading: amplitude ratio
q = (2/3)^6, coherent phase, lags 0.5-40 ms, dominant-QNM (2,2,0) subtraction
only.  This module re-runs the search over the honest battery of alternative
readings that the kernel and the physics allow, on the same events:

  RATIO SEMANTICS (the FRB lesson: energy vs amplitude)
    * amp   = (2/3)^6 = 64/729  -- the kernel eigenvalue read as an AMPLITUDE
                                   ratio (the original frozen reading)
    * amp   = (2/3)^3 = 8/27    -- the kernel eigenvalue read as an ENERGY
                                   ratio (GW energy ~ amplitude^2), so the
                                   strain amplitude steps by (2/3)^3
    * amp   = 2/3               -- the single-step reading (kernel step 3/2)
  PER-BOUNCE PHASE (the boundary-birefringence analogue)
    * phase increment per echo dphi in {0, pi/2, pi, 3pi/2} -- the mu4 clock
      characters.  The propagation-path GW birefringence implied by parity
      violation (c_- = 8 != 0) is COMMON to all echoes of one event (same
      path), so it cancels in the inter-echo ratio; what does NOT cancel is a
      parity phase acquired PER REFLECTION at the boundary.  TFPT's natural
      value is the mu4 quarter turn (i per step => dphi = pi/2); {0, pi} are
      the Dirichlet/Neumann cases; all four mu4 characters are scanned.
  LAG WINDOWS
    * fine   0.5-40 ms  (ECO/gravastar C=3/8 ~ 0.7 ms; cavity scales)
    * coarse 40-350 ms  (Planckian reflection ~ 8M ln(M/l_P) ~ 0.23 s @63 Msun)
  DETECTOR-FRAME FREQUENCY (redshift -- found in this revision)
    * the GWTC catalogue reports SOURCE-frame masses; the observed ringdown is
      at f0/(1+z).  All templates here use mf_det = mf_src (1+z) -- for
      GW190521 (z = 0.56) the earlier searches filtered ~1.6x too high.
  RESIDUAL HYGIENE
    * JOINT (2,2,0)+(2,2,1) Kerr QNM subtraction (Berti-Cardoso-Will 2006
      fits) -- the q_hat~1 excesses of the primary search are overtone power.

HONEST FRAMING: this is a POST-HOC robustness battery (the strain was already
seen by the primary search), so every p-value is Bonferroni-corrected over the
12 template variants and the verdict language stays search-target/firewall:
escalation (not detection) requires a Bonferroni-surviving, ratio-consistent,
template-SPECIFIC, >=2-detector-coincident excess.  NOT covered (documented
limits): frequency-dependent barrier filtering of successive echoes,
spin-dependent inter-echo lag drift, precessing remnants.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .strain_data import (
    apply_whitening,
    damped_sinusoid,
    detector_frame_mass,
    read_hdf5,
    whitening_filter,
)

GMSUN_OVER_C3 = 4.925490947e-6
STRAIN_DIR = Path(__file__).resolve().parents[2] / "data" / "strain"
RESULTS = Path(__file__).resolve().parents[2] / "results"

N_ECHO = 5
JITTER_S = 0.01                 # on-source start jitter (train anchored at merger)
N_BACKGROUND = 800
GUARD_S = 1.0

_RATIOS = [
    ("amp_(2/3)^6", (2.0 / 3.0) ** 6),
    ("energy->(2/3)^3", (2.0 / 3.0) ** 3),
    ("step_2/3", 2.0 / 3.0),
]
_PHASES = [("dphi0", 0.0), ("dphi90", np.pi / 2),
           ("dphi180", np.pi), ("dphi270", 3 * np.pi / 2)]
VARIANTS = [(f"{rn}_{pn}", r, p) for rn, r in _RATIOS for pn, p in _PHASES]
N_VARIANTS = len(VARIANTS)          # 12: mu4 phase characters x ratio semantics

LAGS_FINE_MS = np.arange(0.5, 40.0, 0.5)
LAGS_COARSE_MS = np.arange(40.0, 350.0, 5.0)
LAGS_MS = np.concatenate([LAGS_FINE_MS, LAGS_COARSE_MS])


# ---------------------------------------------------------------------------
# Kerr (l=2, m=2) QNMs, n = 0 and n = 1 (Berti-Cardoso-Will 2006 fits)
# ---------------------------------------------------------------------------
def qnm_22n(mf_msun: float, af: float, n: int) -> tuple[float, float]:
    j = float(np.clip(af, 0.0, 0.99))
    if n == 0:
        m_omega = 1.5251 - 1.1568 * (1.0 - j) ** 0.1292
        q_fac = 0.7000 + 1.4187 * (1.0 - j) ** (-0.4990)
    elif n == 1:
        m_omega = 1.3673 - 1.0260 * (1.0 - j) ** 0.1628
        q_fac = 0.1000 + 0.5436 * (1.0 - j) ** (-0.4731)
    else:
        raise ValueError(n)
    m_sec = mf_msun * GMSUN_OVER_C3
    f = m_omega / m_sec / (2.0 * np.pi)
    tau = q_fac / (np.pi * f)
    return float(f), float(tau)


def subtract_qnm_multimode(white: np.ndarray, merger: int, modes, dt: float,
                           n_tau: float = 8.0) -> tuple[np.ndarray, float]:
    """Joint LS fit of (cos, sin) for every mode in `modes`; returns residual +
    the (2,2,0) amplitude for q_hat normalisation."""
    n = len(white)
    tau_max = max(tau for _, tau in modes)
    end = min(n, merger + int(n_tau * tau_max / dt))
    cols = []
    for f0, tau in modes:
        cols.append(damped_sinusoid(n, merger, f0, tau, dt, phi=0.0))
        cols.append(damped_sinusoid(n, merger, f0, tau, dt, phi=-np.pi / 2))
    sl = slice(merger, end)
    A = np.vstack([c[sl] for c in cols]).T
    coef, *_ = np.linalg.lstsq(A, white[sl], rcond=None)
    model = sum(c * co for c, co in zip(cols, coef))
    amp220 = float(np.hypot(coef[0], coef[1]))
    return white - model, amp220


# ---------------------------------------------------------------------------
# template bank + FFT correlation
# ---------------------------------------------------------------------------
def echo_template(n: int, lag_samp: int, ratio: float, dphi: float,
                  f0: float, tau: float, dt: float) -> np.ndarray:
    """Echo train with per-bounce phase increment dphi (mu4 characters)."""
    h = np.zeros(n)
    for k in range(1, N_ECHO + 1):
        h += (ratio ** k) * damped_sinusoid(n, k * lag_samp, f0, tau, dt,
                                            phi=k * dphi)
    return h


def correlate_bank(resid: np.ndarray, lags_samp: np.ndarray, ratio: float,
                   dphi: float, f0: float, tau: float, dt: float) -> np.ndarray:
    """rho[l, t0] = normalised match of an echo train starting at t0, per lag."""
    n = len(resid)
    R = np.fft.rfft(resid)
    tmpl_len = int(lags_samp.max()) * N_ECHO + int(6.0 * tau / dt)
    rho = np.empty((len(lags_samp), n))
    for i, ls in enumerate(lags_samp):
        T = echo_template(min(tmpl_len, n), int(ls), ratio, dphi, f0, tau, dt)
        norm = math.sqrt(float(T @ T))
        Tp = np.zeros(n)
        Tp[:len(T)] = T
        # cross-correlation: rho(t0) = sum_k resid[t0+k] T[k]
        rho[i] = np.fft.irfft(R * np.conj(np.fft.rfft(Tp)), n=n) / norm
    return rho


@dataclass
class VariantResult:
    variant: str
    ratio: float
    rho_on: float
    best_lag_ms: float
    p_raw: float
    p_bonf: float
    q1_hat: float
    step_hat: float
    ratio_consistent: bool


@dataclass
class DetectorBattery:
    detector: str
    amp220: float
    variants: list[VariantResult] = field(default_factory=list)
    template_agnostic: bool = False   # ALL variants at low p = broadband residual
    note: str = ""


@dataclass
class EventBattery:
    event: str
    mf_msun: float
    f0_hz: float
    detectors: list[DetectorBattery] = field(default_factory=list)
    n_escalation: int = 0
    label: str = ""


def _ratio_consistency(resid: np.ndarray, t0: int, lag_samp: int, ratio: float,
                       f0: float, tau: float, dt: float,
                       amp220: float) -> tuple[float, float, bool]:
    """LS per-echo amplitudes at the best template.  A kernel echo must have
    BOTH (a) the fitted geometric step near the variant ratio (within 50%) AND
    (b) the absolute first-echo amplitude q1_hat = a1/A220 near the ratio
    (within a factor 2) -- residual merger/ringdown power fails (b)."""
    n = len(resid)
    comps = []
    for k in range(1, N_ECHO + 1):
        start = t0 + k * lag_samp
        if start >= n:
            return 0.0, 0.0, False
        comps.append(damped_sinusoid(n, start, f0, tau, dt))
    seg_end = min(n, t0 + N_ECHO * lag_samp + int(6 * tau / dt))
    sl = slice(t0, seg_end)
    A = np.vstack([c[sl] for c in comps]).T
    coef, *_ = np.linalg.lstsq(A, resid[sl], rcond=None)
    a = np.abs(coef)
    q1_hat = float(a[0] / amp220) if amp220 > 0 else 0.0
    if np.any(a[:-1] < 1e-12):
        return q1_hat, 0.0, False
    step_hat = float(np.median(a[1:] / a[:-1]))
    ok = (abs(step_hat - ratio) / ratio < 0.5
          and q1_hat > 0 and 0.5 < q1_hat / ratio < 2.0)
    return q1_hat, step_hat, ok


def battery_event(event: str, af: float = 0.69) -> EventBattery:
    meta = json.loads((STRAIN_DIR / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)      # observed (redshifted) ringdown
    f0, tau0 = qnm_22n(mf, af, 0)
    f1, tau1 = qnm_22n(mf, af, 1)
    res = EventBattery(event, round(mf, 1), round(f0, 1))
    rng = np.random.default_rng(3)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        psd_i, scale = whitening_filter(s.data, s.dt)
        white = apply_whitening(s.data, psd_i, scale)
        merger = s.index_at(merger_gps)
        resid, amp220 = subtract_qnm_multimode(
            white, merger, [(f0, tau0), (f1, tau1)], s.dt)

        lags_samp = np.unique(np.round(LAGS_MS * 1e-3 / s.dt).astype(int))
        lags_samp = lags_samp[lags_samp > 0]
        jit = int(JITTER_S / s.dt)
        train_len = int(lags_samp.max()) * N_ECHO + int(6.0 * tau0 / s.dt)
        guard = int(GUARD_S / s.dt)
        lo, hi = guard, len(resid) - train_len - jit - guard
        centers = rng.integers(lo, hi, size=N_BACKGROUND)
        centers = centers[np.abs(centers - merger) > guard]

        dres = DetectorBattery(det, round(amp220, 3))
        for name, ratio, dphi in VARIANTS:
            rho = correlate_bank(resid, lags_samp, ratio, dphi, f0, tau0, s.dt)
            on_block = rho[:, merger:merger + jit]
            i_lag, _ = np.unravel_index(np.argmax(on_block), on_block.shape)
            rho_on = float(on_block.max())
            best_lag_samp = int(lags_samp[i_lag])
            bg = np.array([rho[:, int(c):int(c) + jit].max() for c in centers])
            p_raw = float((np.sum(bg >= rho_on) + 1) / (len(bg) + 1))
            p_bonf = min(1.0, p_raw * N_VARIANTS)
            t_best = merger + int(np.argmax(on_block[i_lag]))
            q1_hat, step_hat, cons = _ratio_consistency(
                resid, t_best, best_lag_samp, ratio, f0, tau0, s.dt, amp220)
            rc = p_raw < 0.05 and cons
            dres.variants.append(VariantResult(
                name, round(ratio, 4), round(rho_on, 2),
                round(best_lag_samp * s.dt * 1e3, 1),
                round(p_raw, 4), round(p_bonf, 4),
                round(q1_hat, 4), round(step_hat, 4), rc))
        # TEMPLATE-AGNOSTICISM CONTROL: an echo train prefers ONE (ratio, phase,
        # lag) reading; broadband post-merger residual power matches EVERY
        # template equally.  If all variants sit at low p together, the excess
        # is template-independent -- residual power, not an echo signature.
        low = [v for v in dres.variants if v.p_raw < 0.05]
        if len(low) == N_VARIANTS:
            dres.template_agnostic = True
            dres.note = (f"all {N_VARIANTS} variants low-p together -> "
                         "template-agnostic broadband residual power, not an "
                         "echo-train signature")
        res.detectors.append(dres)

    # escalation requires: Bonferroni-surviving AND ratio-consistent AND
    # template-SPECIFIC (not the broadband-residual pattern) AND >=2 detectors
    for name, _, _ in VARIANTS:
        n_hit = sum(1 for d in res.detectors for v in d.variants
                    if v.variant == name and v.p_bonf < 0.01
                    and v.ratio_consistent and not d.template_agnostic)
        res.n_escalation = max(res.n_escalation, n_hit)
    res.label = ("ESCALATE" if res.n_escalation >= 2 else "NO_VARIANT_ECHO")
    return res


def run_battery(events: list[str]) -> int:
    have = [e for e in events if (STRAIN_DIR / f"{e}_meta.json").exists()]
    print("=" * 88)
    print("TFPT GW Stage-1c: SIGNATURE BATTERY (ratio semantics x mu4 per-bounce phases x")
    print("  extended lags; DETECTOR-FRAME (redshifted) QNM frequencies; joint 220+221")
    print(f"  subtraction; post-hoc robustness sweep, Bonferroni x{N_VARIANTS})")
    print("=" * 88)
    missing = [e for e in events if e not in have]
    if missing:
        print(f"  (no strain for {missing}; fetch first)")
    if not have:
        return 1

    out_events = []
    worst = {name: 1.0 for name, _, _ in VARIANTS}
    for ev in have:
        r = battery_event(ev)
        print(f"\n  {ev}: M_f={r.mf_msun} Msun, f0={r.f0_hz} Hz  ->  {r.label}")
        for d in r.detectors:
            row = "  ".join(
                f"{v.variant}: p={v.p_raw:.3f}"
                f"{' [q1=' + str(v.q1_hat) + ' RC]' if v.ratio_consistent else ''}"
                for v in d.variants)
            print(f"    {d.detector:3s} (A220={d.amp220:6.1f})  {row}")
            if d.note:
                print(f"        note: {d.note}")
            for v in d.variants:
                if not d.template_agnostic:
                    worst[v.variant] = min(worst[v.variant], v.p_bonf)
        out_events.append({
            "event": r.event, "mf": r.mf_msun, "label": r.label,
            "detectors": [
                {"detector": d.detector, "amp220": d.amp220,
                 "template_agnostic": d.template_agnostic, "note": d.note,
                 "variants": [vars(v) for v in d.variants]}
                for d in r.detectors]})

    print("\n  best (smallest) Bonferroni p per variant across all streams:")
    for name, p in worst.items():
        print(f"    {name:24s} p_bonf_min = {p:.4f}")

    any_esc = any(e["label"] == "ESCALATE" for e in out_events)
    verdict = (
        "ESCALATE: a Bonferroni-surviving, ratio-consistent variant excess is "
        "coincident in >=2 detectors -- coherent time-slide follow-up + injections "
        "required before ANY claim (firewall: search target)."
        if any_esc else
        "NO VARIANT ECHO: the full signature battery -- amplitude (2/3)^6, energy "
        "reading (2/3)^3, step 2/3, each with the four mu4 per-bounce phase "
        "characters dphi in {0, pi/2, pi, 3pi/2} (the boundary-birefringence "
        "analogue; path birefringence cancels in the inter-echo ratio), lags "
        "0.5-350 ms (ECO ~0.7 ms through Planckian ~0.23 s), DETECTOR-FRAME "
        "(redshift-corrected) QNM frequencies, "
        "after joint (2,2,0)+(2,2,1) subtraction -- shows no Bonferroni-surviving, "
        "ratio-consistent, template-SPECIFIC excess coincident in >=2 detectors "
        "on any event. Streams where ALL 12 variants fire together are broadband "
        "post-merger residual power (an echo train would prefer ONE reading) -- "
        "the template-agnosticism control rejects them. The primary null is "
        "ROBUST against the alternative signature readings. Post-hoc battery, "
        "upper-bound kernel: no detection, no tension claim.")
    print(f"\n-> {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "signature_battery.json").write_text(json.dumps({
        "stage": f"strain_level_test (post-hoc signature battery, Bonferroni x{N_VARIANTS})",
        "variants": [{"name": n, "amp_ratio": r, "per_bounce_phase_rad": p}
                     for n, r, p in VARIANTS],
        "lag_range_ms": [float(LAGS_MS.min()), float(LAGS_MS.max())],
        "qnm_subtraction": "joint (2,2,0)+(2,2,1), Berti-Cardoso-Will 2006 fits",
        "frequency_frame": "detector frame: mf_det = mf_src (1+z), z from GWTC catalogue",
        "birefringence_note": ("propagation-path GW birefringence (parity, c_-=8) is "
                               "common to all echoes of one event and cancels in the "
                               "inter-echo ratio; the per-bounce boundary phase does "
                               "not cancel and is scanned over the mu4 characters"),
        "events": out_events,
        "best_p_bonf_per_variant": worst,
        "verdict": verdict}, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'signature_battery.json'}")
    return 0

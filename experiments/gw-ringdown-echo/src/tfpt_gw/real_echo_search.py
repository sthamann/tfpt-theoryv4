"""Stage-1 echo search on REAL GWOSC strain.

For each event: whiten the strain ONCE (Welch PSD), locate the merger, subtract the dominant
Kerr ringdown (l=m=2,n=0), and matched-filter the residual with the echo-train template at the
FROZEN amplitude ratio (2/3)^6 (free lag, scanned). Significance comes from an OFF-SOURCE
background (the same echo bank slid to many noise-only times), and a free-ratio control q_hat
checks anti-numerology.

Speed/scope (honest, first pass): the matched filter runs in a SHORT post-event window on the
once-whitened series and correlates with the time-domain template (the whitened data is ~white,
so this is a valid, slightly sub-optimal statistic with a self-consistent background); dominant-
QNM subtraction only (no NR-informed multi-mode), incoherent detector combination, off-source
(not coincident time-slide) background. Real p-value on real strain; full multi-mode + coherent
stacking is the next step. TFPT's (2/3)^6 is an UPPER bound, so a null is consistent.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .constants import DET_THRESHOLD, RATIO
from .strain_data import (
    apply_whitening,
    damped_sinusoid,
    detector_frame_mass,
    fit_and_subtract_qnm,
    qnm_220,
    read_hdf5,
    whitening_filter,
)

STRAIN_DIR = Path(__file__).resolve().parents[2] / "data" / "strain"
LAG_GRID_MS = np.concatenate([
    np.arange(0.5, 2.0, 0.05),   # gravastar / ECO scale (0.7 ms template)
    np.arange(2.0, 40.0, 0.5),
])
N_ECHO = 5
KERNEL = RATIO                              # (2/3)^6 frozen amplitude ratio
Q_TOL = 0.5
N_BACKGROUND = 400                          # off-source windows for the noise distribution


def _echo_window(length: int, lag_samp: int, f0: float, tau: float, dt: float,
                 ratio: float = KERNEL) -> np.ndarray:
    """Echo train inside a local window: echoes at offsets k*lag_samp, amplitude ratio^k."""
    h = np.zeros(length)
    for k in range(1, N_ECHO + 1):
        h += (ratio ** k) * damped_sinusoid(length, k * lag_samp, f0, tau, dt)
    return h


def _mf_scan(series_w: np.ndarray, center: int, f0: float, tau: float, dt: float,
             win_len: int) -> tuple[float, float]:
    """Max normalised matched-filter value over the lag grid in a short window at `center`."""
    seg = series_w[center:center + win_len]
    if len(seg) < win_len:
        return -1e9, 0.0
    best_rho, best_lag = -1e9, 0.0
    for lag_ms in LAG_GRID_MS:
        lag_samp = int(round(lag_ms * 1e-3 / dt))
        temp = _echo_window(win_len, lag_samp, f0, tau, dt)
        norm = math.sqrt(float(temp @ temp))
        if norm == 0:
            continue
        rho = float(seg @ temp / norm)
        if rho > best_rho:
            best_rho, best_lag = rho, lag_ms
    return best_rho, best_lag


@dataclass
class DetectorResult:
    detector: str
    rho_max: float
    best_lag_ms: float
    q_hat: float
    p_value: float
    kernel_consistent: bool = False     # excess AND q_hat ~ (2/3)^6 (a faint echo, not residual)


@dataclass
class EventResult:
    event: str
    mf_msun: float
    f0_hz: float
    tau_ms: float
    detectors: list[DetectorResult] = field(default_factory=list)
    rho_net: float = 0.0
    n_kernel_consistent: int = 0
    label: str = ""
    note: str = ""


def _q_hat(seg: np.ndarray, lag_ms: float, f0: float, tau: float, dt: float,
           win_len: int, amp_qnm: float) -> float:
    """Per-echo ratio: least-squares amplitude of the FIRST echo over the QNM amplitude."""
    lag_samp = int(round(lag_ms * 1e-3 / dt))
    e1 = damped_sinusoid(win_len, lag_samp, f0, tau, dt)
    norm2 = float(e1 @ e1)
    if norm2 == 0 or amp_qnm == 0:
        return 0.0
    return float(seg @ e1 / norm2) / amp_qnm


def search_event(event: str, af: float = 0.69) -> EventResult:
    meta = json.loads((STRAIN_DIR / f"{event}_meta.json").read_text(encoding="utf-8"))
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)      # observed (redshifted) ringdown
    f0, tau = qnm_220(mf, af)
    res = EventResult(event, round(mf, 1), round(f0, 1), round(tau * 1e3, 2))
    rng = np.random.default_rng(0)

    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN_DIR / Path(fname).name))
        psd_i, scale = whitening_filter(s.data, s.dt)
        white = apply_whitening(s.data, psd_i, scale)
        merger = s.index_at(merger_gps)
        resid, amp_qnm = fit_and_subtract_qnm(white, merger, f0, tau, s.dt)
        max_lag_samp = int(round(LAG_GRID_MS.max() * 1e-3 / s.dt))
        win_len = N_ECHO * max_lag_samp + int(6.0 * tau / s.dt)

        rho_on, lag_on = _mf_scan(resid, merger, f0, tau, s.dt, win_len)
        q_hat = _q_hat(resid[merger:merger + win_len], lag_on, f0, tau, s.dt, win_len, amp_qnm)

        guard = int(1.0 / s.dt)
        lo, hi = guard, len(resid) - win_len - guard
        centers = rng.integers(lo, hi, size=N_BACKGROUND)
        bg = np.array([_mf_scan(resid, int(c), f0, tau, s.dt, win_len)[0]
                       for c in centers if abs(int(c) - merger) > guard])
        p_val = float((np.sum(bg >= rho_on) + 1) / (len(bg) + 1))
        # a TFPT echo is FAINT: q_hat ~ (2/3)^6.  A loud excess with q_hat ~ 1 is residual
        # ringdown power (imperfect dominant-mode subtraction), NOT an echo -> the free-ratio
        # control rejects it.
        kc = bool(p_val < 0.01 and abs(q_hat - KERNEL) / KERNEL < Q_TOL)
        res.detectors.append(DetectorResult(det, round(rho_on, 2), lag_on,
                                             round(q_hat, 4), round(p_val, 4), kc))

    res.rho_net = round(math.sqrt(sum(d.rho_max ** 2 for d in res.detectors)), 2)
    res.n_kernel_consistent = sum(d.kernel_consistent for d in res.detectors)
    # a candidate needs a FAINT (kernel-ratio) excess COINCIDENT in >=2 detectors
    if res.n_kernel_consistent >= 2:
        res.label = "KERNEL_ECHO_CANDIDATE"
    else:
        res.label = "NO_SIGNIFICANT_ECHO"
    loud = [d for d in res.detectors if d.p_value < 0.01]
    if loud and res.n_kernel_consistent == 0:
        res.note = (f"low-p excess in {[d.detector for d in loud]} but q_hat="
                    f"{[d.q_hat for d in loud]} far from (2/3)^6={KERNEL:.3f} "
                    f"-> residual ringdown power, not a faint kernel echo (free-ratio control)")
    return res

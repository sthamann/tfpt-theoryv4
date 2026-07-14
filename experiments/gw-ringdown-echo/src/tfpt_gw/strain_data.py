"""Real GWOSC strain I/O + whitening + Kerr (l=m=2,n=0) QNM, for the Stage-1 echo search.

GWOSC HDF5 layout (32 s tutorial / event-API files): dataset ``strain/Strain`` with attr
``Xspacing`` = dt, group ``meta`` with ``GPSstart``/``Detector``. Read with h5py (no gwpy).
The dominant ringdown frequency/damping come from the Berti-Cardoso-Will fits to the
Kerr l=m=2, n=0 quasinormal mode (Berti+ 2006), so no LAL/qnm package is needed.

REDSHIFT: the GWTC catalogue reports SOURCE-frame masses; the observed ringdown
frequency is redshifted, so all QNM templates must use the DETECTOR-frame mass
``mf_det = mf_src * (1 + z)`` (``detector_frame_mass``).  Without this the template
frequency is wrong by up to ~1.6x for the high-z events (e.g. GW190521, z = 0.56).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import h5py
import numpy as np
from scipy.signal import butter, sosfiltfilt, welch

GMSUN_OVER_C3 = 4.925490947e-6   # s per solar mass (geometric time unit)
CATALOG_CSV = Path(__file__).resolve().parents[2] / "data" / "gwtc_events.csv"
_Z_CACHE: dict[str, float] = {}


def catalog_redshift(event: str) -> float:
    """Redshift z from the GWTC catalogue (0.0 if the event/value is missing)."""
    if not _Z_CACHE and CATALOG_CSV.exists():
        with open(CATALOG_CSV, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    _Z_CACHE[row["name"]] = float(row["z"])
                except (KeyError, TypeError, ValueError):
                    continue
    return _Z_CACHE.get(event, 0.0)


def detector_frame_mass(event: str, mf_source: float) -> float:
    """Detector-frame final mass mf_src * (1+z) — what the QNM template must use."""
    return mf_source * (1.0 + catalog_redshift(event))


@dataclass
class Strain:
    detector: str
    data: np.ndarray
    dt: float
    gps_start: float

    @property
    def fs(self) -> float:
        return 1.0 / self.dt

    def index_at(self, gps: float) -> int:
        return int(round((gps - self.gps_start) / self.dt))


def read_hdf5(path: str) -> Strain:
    with h5py.File(path, "r") as f:
        st = f["strain/Strain"]
        data = np.asarray(st[:], dtype=float)
        dt = float(st.attrs["Xspacing"])
        gps_start = float(f["meta"]["GPSstart"][()])
        det = f["meta"]["Detector"][()]
        det = det.decode() if isinstance(det, bytes) else str(det)
    return Strain(det, data, dt, gps_start)


def qnm_220(mf_msun: float, af: float = 0.69) -> tuple[float, float]:
    """Dominant Kerr ringdown frequency f0 [Hz] and damping tau [s] (Berti+ 2006 fits)."""
    j = float(np.clip(af, 0.0, 0.99))
    m_omega_r = 1.5251 - 1.1568 * (1.0 - j) ** 0.1292        # M omega_R (geometric)
    q_factor = 0.7000 + 1.4187 * (1.0 - j) ** (-0.4990)      # quality factor
    m_sec = mf_msun * GMSUN_OVER_C3
    omega_r = m_omega_r / m_sec                               # rad/s
    f0 = omega_r / (2.0 * np.pi)
    tau = q_factor / (np.pi * f0)
    return float(f0), float(tau)


def whitening_filter(x: np.ndarray, dt: float, seg_s: float = 4.0) -> tuple[np.ndarray, float]:
    """Welch-PSD whitening filter for length-len(x) signals: returns (psd_on_rfftfreqs, scale).

    `scale` is the robust std of the whitened data, so the SAME filter applied to a template
    keeps data and template on one footing (the matched filter stays consistent)."""
    fs = 1.0 / dt
    nperseg = int(min(len(x), seg_s * fs))
    f_psd, psd = welch(x, fs=fs, nperseg=nperseg, window="hann")
    freqs = np.fft.rfftfreq(len(x), dt)
    psd_i = np.interp(freqs, f_psd, psd, left=psd[0], right=psd[-1])
    psd_i[psd_i <= 0] = psd_i[psd_i > 0].min()
    white = np.fft.irfft(np.fft.rfft(x) / np.sqrt(psd_i), n=len(x))
    scale = float(np.median(np.abs(white)) / 0.6745) or 1.0
    return psd_i, scale


def apply_whitening(y: np.ndarray, psd_i: np.ndarray, scale: float) -> np.ndarray:
    """Apply a precomputed whitening filter (same length as the calibration data)."""
    return np.fft.irfft(np.fft.rfft(y) / np.sqrt(psd_i), n=len(y)) / scale


def whiten(x: np.ndarray, dt: float, seg_s: float = 4.0) -> np.ndarray:
    psd_i, scale = whitening_filter(x, dt, seg_s)
    return apply_whitening(x, psd_i, scale)


def whitening_filter_gated(x: np.ndarray, dt: float, gate_start: int, gate_end: int,
                           seg_s: float = 4.0, average: str = "mean") -> tuple[np.ndarray, float]:
    """OFF-SOURCE whitening filter: Welch PSD estimated EXCLUDING the gated
    (event) stretch, so the filter cannot adapt to -- and ring after -- the
    loud transient (signature-revision hardening, 2026-07-02).

    The pre-gate and post-gate stretches are Welch-averaged weighted by their
    lengths; the robust-std scale is computed off-gate as well. ``average`` selects the
    Welch periodogram averaging: ``"mean"`` (frozen default) or ``"median"`` (robust to
    non-stationary lines/glitches -- required for O4 data, e.g. GW250114)."""
    fs = 1.0 / dt
    nperseg = int(seg_s * fs)
    stretches = [seg for seg in (x[:max(0, gate_start)], x[gate_end:])
                 if len(seg) >= 2 * nperseg]
    if not stretches:
        return whitening_filter(x, dt, seg_s)
    freqs = np.fft.rfftfreq(len(x), dt)
    acc = np.zeros_like(freqs)
    w_tot = 0.0
    for seg in stretches:
        f_psd, psd = welch(seg, fs=fs, nperseg=nperseg, window="hann", average=average)
        acc += len(seg) * np.interp(freqs, f_psd, psd, left=psd[0], right=psd[-1])
        w_tot += len(seg)
    psd_i = acc / w_tot
    psd_i[psd_i <= 0] = psd_i[psd_i > 0].min()
    white = np.fft.irfft(np.fft.rfft(x) / np.sqrt(psd_i), n=len(x))
    off = np.concatenate([white[:max(0, gate_start)], white[gate_end:]])
    scale = float(np.median(np.abs(off)) / 0.6745) or 1.0
    return psd_i, scale


def highpass(x: np.ndarray, dt: float, fc: float = 20.0, order: int = 4) -> np.ndarray:
    """Zero-phase Butterworth high-pass. O4 4 kHz strain carries enormous sub-20 Hz seismic
    power that a single-Welch whitening mishandles (heavy-tailed whitened output); high-passing
    first removes it. O1 data (e.g. GW150914) was already cleaner, but the high-pass is
    harmless there (the ringdown is at ~250 Hz)."""
    sos = butter(order, fc, "highpass", fs=1.0 / dt, output="sos")
    return sosfiltfilt(sos, x)


def align_ringdown(white: np.ndarray, merger: int, dt: float,
                   back_ms: float = 2.0, fwd_ms: float = 50.0,
                   smooth_ms: float = 1.0) -> int:
    """Refine the merger index to the whitened ringdown-envelope peak in a small forward
    window [merger-back_ms, merger+fwd_ms].

    The catalog coalescence GPS lands a few M before the post-peak ringdown, and the
    whitening filter adds a small group delay, so the QNM fit at the *nominal* merger
    systematically starts ~15-40 ms early (verified across GW150914/GW200129/GW190521),
    under-measuring A220. Aligning to the smoothed |whitened| envelope peak (data-driven,
    template-independent) fixes this without touching the frozen kernel."""
    lo = max(0, merger - int(back_ms * 1e-3 / dt))
    hi = min(len(white), merger + int(fwd_ms * 1e-3 / dt))
    env = np.abs(white[lo:hi])
    k = max(1, int(smooth_ms * 1e-3 / dt))
    if k > 1:
        env = np.convolve(env, np.ones(k) / k, mode="same")
    return lo + int(np.argmax(env))


def damped_sinusoid(n: int, start: int, f0: float, tau: float, dt: float,
                    phi: float = 0.0) -> np.ndarray:
    """Unit-amplitude ringdown e^{-t/tau} cos(2 pi f0 t + phi) for samples >= start."""
    h = np.zeros(n)
    k = np.arange(n)
    m = k >= start
    t = (k[m] - start) * dt
    h[m] = np.exp(-t / tau) * np.cos(2.0 * np.pi * f0 * t + phi)
    return h


def fit_and_subtract_qnm(white: np.ndarray, merger: int, f0: float, tau: float,
                         dt: float, n_tau: float = 6.0) -> tuple[np.ndarray, float]:
    """Least-squares fit of the dominant QNM (cos+sin) at the merger and subtract it.

    Returns (residual, qnm_amplitude) with amplitude sqrt(a_cos^2 + a_sin^2) in whitened units."""
    n = len(white)
    end = min(n, merger + int(n_tau * tau / dt))
    c = damped_sinusoid(n, merger, f0, tau, dt, phi=0.0)
    s = damped_sinusoid(n, merger, f0, tau, dt, phi=-np.pi / 2)   # sin component
    sl = slice(merger, end)
    A = np.vstack([c[sl], s[sl]]).T
    coef, *_ = np.linalg.lstsq(A, white[sl], rcond=None)
    amp = float(np.hypot(coef[0], coef[1]))
    return white - (coef[0] * c + coef[1] * s), amp

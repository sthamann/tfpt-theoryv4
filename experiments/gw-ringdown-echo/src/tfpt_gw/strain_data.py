"""Real GWOSC strain I/O + whitening + Kerr (l=m=2,n=0) QNM, for the Stage-1 echo search.

GWOSC HDF5 layout (32 s tutorial / event-API files): dataset ``strain/Strain`` with attr
``Xspacing`` = dt, group ``meta`` with ``GPSstart``/``Detector``. Read with h5py (no gwpy).
The dominant ringdown frequency/damping come from the Berti-Cardoso-Will fits to the
Kerr l=m=2, n=0 quasinormal mode (Berti+ 2006), so no LAL/qnm package is needed.
"""

from __future__ import annotations

from dataclasses import dataclass

import h5py
import numpy as np
from scipy.signal import welch

GMSUN_OVER_C3 = 4.925490947e-6   # s per solar mass (geometric time unit)


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

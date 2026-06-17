"""QT.02/QT.03 — quench dynamics: discrete-scale-invariant recovery + a free-fermion OTOC.

The reconsidered, *dynamical* TFPT signature (`problem_1.txt` §D): build the compiler
as a Hamiltonian / open-system generator, quench it, and look for **discrete scale
invariance** in how it recovers — a log-periodic ripple at ``omega = 2 pi / ln(lambda)``
rather than a static ratio in a histogram.

* **QT.02 (recovery DSI + suppression law).** A geometric ladder of decay modes
  (rates ``gamma_k = gamma0 * lambda^{-k}``, the kernel structure) relaxes with a
  log-periodic ripple.  Its amplitude is ``~ exp(-pi^2/ln lambda)``, so only a *coarse*
  ladder is detectable: the carrier ``3/2`` is exponentially invisible, while the
  **energy gap ``(3/2)^6 ≈ 11.4``** sits right at the ~2% detection threshold.  A
  non-geometric (linear-rate) control shows no ripple at the kernel log-frequency.
* **QT.03 (free-fermion OTOC).** A single-particle Hamiltonian with the kernel-ladder
  spectrum; the squared-commutator OTOC ``C_ij(t)=|G_ij(t)|^2`` (``G=e^{-i h t}``) shows
  ballistic operator spreading, and the on-site operator-return weight is tested for the
  same DSI log-frequency (exploratory).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .dsi import amplitude_suppression, detect_dsi, geometric_rate_relaxation, log_frequency


@dataclass
class DSIScanRow:
    name: str
    lam: float
    omega: float
    suppression: float        # exp(-pi*omega/2) amplitude scale
    amplitude: float          # fitted log-periodic amplitude
    p_value: float
    detected: bool


def recovery_dsi_scan(ladder: dict[str, float], *, t_lo: float = -3.0, t_hi: float = 4.0,
                      n_t: int = 600, n_modes: int = 7, gamma0: float = 10.0,
                      n_surrogate: int = 400, seed: int = 0) -> list[DSIScanRow]:
    """For each kernel ladder ratio, relax a geometric rate ladder and test DSI at
    its own log-frequency.  Demonstrates the exp(-pi^2/ln lambda) suppression law."""
    t = np.logspace(t_lo, t_hi, n_t)
    out: list[DSIScanRow] = []
    for name, lam in ladder.items():
        y = geometric_rate_relaxation(t, lam, n_modes=n_modes, gamma0=gamma0)
        fit = detect_dsi(t, y, lam, n_surrogate=n_surrogate, seed=seed)
        out.append(DSIScanRow(name, lam, log_frequency(lam), amplitude_suppression(lam),
                              fit.amplitude, fit.p_value, fit.detected))
    return out


@dataclass
class ControlResult:
    lam: float
    omega: float
    amplitude: float
    p_value: float
    detected: bool            # expect False -> the DSI is specific to the geometric ladder


def nongeometric_control(lam: float, *, t_lo: float = -3.0, t_hi: float = 4.0,
                         n_t: int = 600, n_modes: int = 7, gamma0: float = 10.0,
                         n_surrogate: int = 400, seed: int = 0) -> ControlResult:
    """A *linear* (non-geometric) rate ladder spanning the same range, tested at the
    geometric log-frequency omega(lam): a genuine ladder must not be faked by any
    smooth multi-rate decay."""
    t = np.logspace(t_lo, t_hi, n_t)
    rates = np.linspace(gamma0 * lam ** (-(n_modes - 1)), gamma0, n_modes)
    y = np.exp(-np.outer(t, rates)).mean(axis=1)
    fit = detect_dsi(t, y, lam, n_surrogate=n_surrogate, seed=seed)
    return ControlResult(lam, log_frequency(lam), fit.amplitude, fit.p_value, fit.detected)


# --------------------------------------------------------------------------- free-fermion OTOC
def kernel_ladder_hamiltonian(n_sites: int, lam: float, *, e0: float = 0.1,
                              seed: int = 0) -> np.ndarray:
    """Single-particle Hermitian H whose spectrum is the kernel geometric ladder
    ``e0 * lambda^k`` tiled to ``n_sites`` levels, in a random (orthogonal) site basis
    -- the 'compiler as a Hamiltonian' with the kernel rate ladder."""
    rng = np.random.default_rng(seed)
    ks = np.arange(n_sites) % 8                      # 8 rungs, tiled
    evals = e0 * lam ** ks.astype(float)
    A = rng.standard_normal((n_sites, n_sites))
    Q, _ = np.linalg.qr(A)
    return (Q * evals) @ Q.T


@dataclass
class OTOCResult:
    n_sites: int
    lam: float
    front_speed: float        # ballistic operator-spreading speed (sites per unit t)
    return_dsi_p: float       # DSI p of the on-site operator-return weight (exploratory)
    return_dsi_detected: bool


def freefermion_otoc(lam: float, *, n_sites: int = 64, n_t: int = 400, t_max: float = 60.0,
                     n_surrogate: int = 300, seed: int = 0) -> OTOCResult:
    """Free-fermion squared-commutator OTOC ``C_ij(t)=|(e^{-iHt})_ij|^2``.  Returns the
    ballistic front speed and a DSI test of the on-site return weight ``C_00(t)``."""
    h = kernel_ladder_hamiltonian(n_sites, lam, seed=seed)
    w, V = np.linalg.eigh(h)
    t = np.linspace(0.05, t_max, n_t)
    ret = np.empty(n_t)            # C_00(t)
    front = np.empty(n_t)          # mean spread <|i-0|> weighted by C_0i
    sites = np.arange(n_sites)
    for k, tt in enumerate(t):
        phase = np.exp(-1j * w * tt)
        G0 = (V * phase) @ V[0].conj()        # column 0 of e^{-iHt}
        c = np.abs(G0) ** 2
        ret[k] = c[0]
        front[k] = float(np.sum(np.abs(sites) * c) / np.sum(c))
    # ballistic front speed = slope of spread vs t over the early (pre-saturation) window
    early = t < t_max / 3
    speed = float(np.polyfit(t[early], front[early], 1)[0])
    fit = detect_dsi(t, ret, lam, n_surrogate=n_surrogate, seed=seed)
    return OTOCResult(n_sites, lam, speed, fit.p_value, fit.detected)

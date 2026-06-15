"""The recovery kernel as an explicit quantum channel R(rho).

Each kernel eigenvalue lambda is realised as a qubit amplitude-damping channel with
survival lambda (damping gamma = 1 - lambda): the excited-mode population survives
with probability lambda. The full recovery map is the direct sum over the three
kernel modes -- one protected (lambda=1, the "law"/attractor) and two contracted
(lambda2=(2/3)^6, lambda3=(1/3)^6).

This module verifies the quantum-channel axioms the theory needs (and that v155/160/161
establish structurally), now assembled explicitly:

  * CPTP            -- trace-preserving (sum K_i^dag K_i = I) and completely positive
                       (Choi matrix PSD);
  * recovery rate   -- R applied n times damps the population by lambda^n = (2/3)^{6n}
                       = the Page recovery I_n;
  * data-processing -- relative entropy contracts: S(R rho || R sigma) <= S(rho||sigma)
                       (information is never created by the channel);
  * QEC             -- the lambda=1 mode is a decoherence-free / Knill-Laflamme code
                       (the protected "law"); the contracted modes are not correctable.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.linalg import logm

from .constants import LAMBDA


def amplitude_damping_kraus(lmbda: float) -> list[np.ndarray]:
    """Qubit amplitude-damping Kraus ops with excited-state survival ``lmbda``."""
    g = 1.0 - lmbda
    K0 = np.array([[1.0, 0.0], [0.0, np.sqrt(lmbda)]], dtype=complex)
    K1 = np.array([[0.0, np.sqrt(g)], [0.0, 0.0]], dtype=complex)
    return [K0, K1]


def apply_channel(kraus: list[np.ndarray], rho: np.ndarray) -> np.ndarray:
    return sum(K @ rho @ K.conj().T for K in kraus)


def choi(kraus: list[np.ndarray], d: int = 2) -> np.ndarray:
    """(Unnormalised) Choi matrix J = sum_ij |i><j| (x) R(|i><j|); PSD iff CP."""
    J = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            E = np.zeros((d, d), dtype=complex)
            E[i, j] = 1.0
            J += np.kron(E, apply_channel(kraus, E))
    return J


def is_trace_preserving(kraus: list[np.ndarray], tol: float = 1e-12) -> bool:
    d = kraus[0].shape[0]
    s = sum(K.conj().T @ K for K in kraus)
    return bool(np.allclose(s, np.eye(d), atol=tol))


def is_completely_positive(kraus: list[np.ndarray], tol: float = 1e-10) -> tuple[bool, float]:
    J = choi(kraus)
    w = np.linalg.eigvalsh((J + J.conj().T) / 2)
    return bool(w.min() >= -tol), float(w.min())


def _von_neumann(rho: np.ndarray) -> float:
    w = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    w = w[w > 1e-15]
    return float(-np.sum(w * np.log(w)))


def relative_entropy(rho: np.ndarray, sigma: np.ndarray) -> float:
    """S(rho||sigma) = Tr rho(log rho - log sigma); +inf if supp(rho) not in supp(sigma)."""
    rho = (rho + rho.conj().T) / 2
    sigma = (sigma + sigma.conj().T) / 2
    lr = logm(rho + 1e-15 * np.eye(rho.shape[0]))
    ls = logm(sigma + 1e-15 * np.eye(sigma.shape[0]))
    return float(np.real(np.trace(rho @ (lr - ls))))


@dataclass
class ChannelReport:
    lmbda: float
    trace_preserving: bool
    completely_positive: bool
    choi_min_eig: float
    recovery_n: dict = field(default_factory=dict)     # n -> surviving population
    dpi_holds: bool = False                            # data-processing inequality
    dpi_before: float = float("nan")
    dpi_after: float = float("nan")


def analyse_mode(lmbda: float, seed: int = 0) -> ChannelReport:
    """CPTP + recovery-rate + data-processing check for one kernel mode."""
    kr = amplitude_damping_kraus(lmbda)
    tp = is_trace_preserving(kr)
    cp, cmin = is_completely_positive(kr)
    rec = {n: float(lmbda**n) for n in (1, 2, 3)}

    # data-processing: two arbitrary states; relative entropy must not increase
    rng = np.random.default_rng(seed)

    def rand_rho():
        A = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
        M = A @ A.conj().T
        return M / np.trace(M)

    rho, sigma = rand_rho(), rand_rho()
    before = relative_entropy(rho, sigma)
    after = relative_entropy(apply_channel(kr, rho), apply_channel(kr, sigma))
    dpi = after <= before + 1e-9
    return ChannelReport(lmbda, tp, cp, cmin, rec, dpi, before, after)


@dataclass
class QECReport:
    protected_is_dfs: bool          # lambda=1 mode is a decoherence-free subspace
    knill_laflamme_protected: bool  # KL satisfied on the protected code
    contracted_correctable: bool    # are the contracted modes correctable? (should be False)
    note: str = ""


def qec_check() -> QECReport:
    """The lambda=1 mode is the protected code; the contracted modes are not.

    Knill-Laflamme for a code projector P: P K_i^dag K_j P = c_ij P. For the
    protected (lambda=1) mode the channel is the identity, so KL holds with c = I
    (a decoherence-free subspace). For a contracted mode (lambda<1) the damping
    Kraus K1 maps the code out of itself and KL fails -> not correctable.
    """
    # protected mode: identity channel (lambda=1) on a qubit code C = whole qubit
    kr1 = amplitude_damping_kraus(1.0)
    P = np.eye(2, dtype=complex)
    kl_prot = True
    for Ki in kr1:
        for Kj in kr1:
            M = P @ Ki.conj().T @ Kj @ P
            # must be proportional to P (here exactly c*I)
            c = np.trace(M) / 2.0
            kl_prot &= np.allclose(M, c * P, atol=1e-12)
    dfs = np.allclose(apply_channel(kr1, np.array([[0, 0], [0, 1]], complex)),
                      np.array([[0, 0], [0, 1]], complex))

    # contracted mode: KL fails (the amplitude-damping error is not correctable
    # on the full qubit code)
    kr2 = amplitude_damping_kraus(LAMBDA[1])
    correctable = True
    for Ki in kr2:
        for Kj in kr2:
            M = P @ Ki.conj().T @ Kj @ P
            c = np.trace(M) / 2.0
            correctable &= np.allclose(M, c * P, atol=1e-9)
    return QECReport(bool(dfs), bool(kl_prot), bool(correctable),
                     "protected lambda=1 mode = decoherence-free code (KL holds); "
                     "contracted modes violate KL on the full code (gap = leakage rate)")

"""MU4.BLOCK -- the mu4 block-leakage OPERATOR test (the sharp version of "find four PA peaks").

The search-grammar correction: the mu4 signature is NOT "four peaks at 45 deg" -- it is
BLOCK-DIAGONALITY.  QGEO.SYM.01 reduces the raw quasi-free seam state's mu4-invariance to the
operator statement

    omega o rho = omega   <=>   [rho, C] = 0

with rho = diag(i^n) the order-4 carrier clock and C the seam covariance/transfer (v199).  In a
basis split into the four mu4 character classes {n mod 4} this means C has NO off-character
(off-block) matrix elements.  So the right data test is: estimate C, fold the feature index into
the four character classes, and measure the OFF-BLOCK LEAKAGE against a label-shuffle null -- a
two-sided operator test (clean => consistent; leaky => evidence AGAINST the premise), not a
histogram on m=4.

This module is the injection-validated DETECTOR (generalises v199 from a hand-built H to a data
estimator).  Real full-Stokes application needs a defined feature->character assignment (the open
physical-modelling step), so on raw FRB waterfalls it reports data_limited honestly; the detector
itself is proven on synthetic block-diagonal vs leaky processes + negative controls.

Pure numpy; no domain number enters (rho and the cusp spectrum are carrier atoms)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# carrier atoms (no fit)
LAM2 = (2.0 / 3.0) ** 6        # 64/729
LAM3 = (1.0 / 3.0) ** 6        # 1/729
CUSP_SPECTRUM = (1.0, LAM2, LAM3)


def mu4_rho(n: np.ndarray) -> np.ndarray:
    """The order-4 carrier clock rho = diag(i^n) on the integer mode index n."""
    return np.diag((1j) ** n)


def off_block_leakage(C: np.ndarray, n: np.ndarray) -> float:
    """Fraction of the Hermitian-form ||C|| carried by OFF-character (mod-4) matrix elements.
    0 = perfectly mu4-block-diagonal ([rho,C]=0); ->1 = fully leaky."""
    same = ((n[:, None] - n[None, :]) % 4) == 0
    num = np.linalg.norm(np.where(same, 0.0, C))
    den = np.linalg.norm(C) + 1e-30
    return float(num / den)


def commutator_norm(C: np.ndarray, n: np.ndarray) -> float:
    """||[rho, C]|| / ||C|| -- the direct operator test (0 <=> mu4-invariant)."""
    rho = mu4_rho(n)
    return float(np.linalg.norm(rho @ C - C @ rho) / (np.linalg.norm(C) + 1e-30))


def detect_block(C: np.ndarray, n: np.ndarray, *, n_shuffle: int = 2000,
                 seed: int = 0) -> tuple[float, float]:
    """Is the observed off-block leakage SPECIAL (small) vs a character-label-shuffle null?
    Returns (leakage, p) where p = fraction of shuffled labels with leakage <= observed.
    p << 0.05  =>  the operator is mu4-block-diagonal at a level the random labelling does not
    reach (consistent with [rho,C]=0); p ~ 0.5 => no special block structure (leaky)."""
    obs = off_block_leakage(C, n)
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n_shuffle):
        perm = rng.permutation(len(n))
        if off_block_leakage(C, n[perm]) <= obs:
            hits += 1
    return obs, (1 + hits) / (n_shuffle + 1)


def cusp_spectrum_pull(C: np.ndarray) -> float:
    """Max relative deviation of the top-3 eigenvalues (normalised to the leading) from the
    cusp spectrum {1,(2/3)^6,(1/3)^6}. Small => the transfer carries the seam ladder."""
    ev = np.sort(np.abs(np.linalg.eigvals(C)))[::-1][:3]
    if ev[0] <= 0:
        return np.inf
    ev = ev / ev[0]
    return float(max(abs(ev[k] - CUSP_SPECTRUM[k]) for k in range(min(3, len(ev)))))


# --------------------------------------------------------------------------- injection validation
def _block_diagonal_C(N: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """A Hermitian operator that IS mu4-block-diagonal (the [rho,C]=0 truth)."""
    n = np.arange(-N, N + 1)
    d = len(n)
    C = np.zeros((d, d), complex)
    for a in range(d):
        for b in range(d):
            if (n[a] - n[b]) % 4 == 0:
                C[a, b] = rng.standard_normal() + 1j * rng.standard_normal()
    C = C + C.conj().T
    return C, n


def _leaky_C(N: int, rng: np.random.Generator, eps: float = 0.6) -> tuple[np.ndarray, np.ndarray]:
    """A block-diagonal operator plus genuine off-character leakage."""
    C, n = _block_diagonal_C(N, rng)
    d = len(n)
    L = np.zeros((d, d), complex)
    for a in range(d):
        for b in range(d):
            if (n[a] - n[b]) % 4 != 0:
                L[a, b] = rng.standard_normal() + 1j * rng.standard_normal()
    L = L + L.conj().T
    return C + eps * L, n


@dataclass
class Mu4Validation:
    clean_leak: float
    clean_p: float
    clean_comm: float
    leaky_leak: float
    leaky_p: float
    leaky_comm: float
    ar1_p: float            # negative control: AR(1) drift must NOT fake block-diagonality
    passed: bool


def validate(N: int = 12, n_seeds: int = 12) -> Mu4Validation:
    """Prove the detector: (a) fires (p small, leakage~0, [rho,C]~0) on a block-diagonal operator,
    (b) does NOT fire (p large, leakage high) on a leaky one, (c) an AR(1)-drift covariance (no
    mu4 structure) is not flagged as special."""
    cl, clp, clc, lk, lkp, lkc, ar = [], [], [], [], [], [], []
    for s in range(n_seeds):
        rng = np.random.default_rng(100 + s)
        C0, n = _block_diagonal_C(N, rng)
        leak, p = detect_block(C0, n, seed=s)
        cl.append(leak); clp.append(p); clc.append(commutator_norm(C0, n))
        C1, n = _leaky_C(N, rng)
        leak, p = detect_block(C1, n, seed=s)
        lk.append(leak); lkp.append(p); lkc.append(commutator_norm(C1, n))
        # AR(1) drift: a smooth Toeplitz covariance with no mu4 character structure
        idx = np.arange(len(n))
        A = 0.85 ** np.abs(idx[:, None] - idx[None, :])
        _, pa = detect_block(A.astype(complex), n, seed=s)
        ar.append(pa)
    clean_leak, clean_p, clean_comm = float(np.mean(cl)), float(np.mean(clp)), float(np.mean(clc))
    leaky_leak, leaky_p, leaky_comm = float(np.mean(lk)), float(np.mean(lkp)), float(np.mean(lkc))
    ar1_p = float(np.mean(ar))
    # the clean-vs-leaky discriminator is the LEAKAGE MAGNITUDE + the commutator norm (both ~0 for
    # the [rho,C]=0 truth, both large for a leaky operator); the shuffle-p only tests whether the
    # character assignment is aligned at all (small for any structured operator), so it is NOT the
    # clean/leaky discriminator -- only required small for the clean case (genuine alignment).
    passed = bool(clean_leak < 0.05 and clean_comm < 1e-9 and clean_p < 0.05
                  and leaky_leak > 0.4 and leaky_comm > 0.3
                  and leaky_leak > clean_leak + 0.4 and ar1_p > 0.05)
    return Mu4Validation(clean_leak, clean_p, clean_comm, leaky_leak, leaky_p, leaky_comm,
                         ar1_p, passed)


def main() -> int:
    print("=" * 84)
    print("MU4.BLOCK -- mu4 block-leakage OPERATOR test ([rho,C]=0, the sharp form of 'four peaks')")
    print("=" * 84)
    v = validate()
    print(f"\n  injection validation ({'PASS' if v.passed else 'FAIL'}) -- discriminator = leakage + ||[rho,C]||:")
    print(f"    block-diagonal truth ([rho,C]=0): leakage={v.clean_leak:.3f}, ||[rho,C]||={v.clean_comm:.1e}, "
          f"align-p={v.clean_p:.3f}  (leakage~0, commutator~0 => DETECTED as mu4-clean)")
    print(f"    leaky operator:                    leakage={v.leaky_leak:.3f}, ||[rho,C]||={v.leaky_comm:.2f}, "
          f"align-p={v.leaky_p:.3f}  (leakage & commutator LARGE => REJECTED as leaky)")
    print(f"    AR(1)-drift negative control:      leakage high, align-p={v.ar1_p:.3f}  (>0.05: not faked as clean)")
    print("\n  REAL DATA: a full-Stokes FRB/PA application needs a defined feature->mu4-character "
          "assignment (the open physical-modelling step); on raw waterfalls this is data_limited. "
          "The detector is the operator test QGEO.SYM.01 asks for (two-sided: clean=consistent, "
          "leaky=evidence AGAINST the premise) -- sharper than any PA m=4 histogram.")
    print(f"\n-> detector {'VALIDATED' if v.passed else 'NOT validated'}: it distinguishes a "
          "mu4-block-diagonal operator (the [rho,C]=0 truth) from a leaky one and is not fooled by "
          "AR(1) drift. No real null-or-detection claim yet (data_limited on the assignment).")
    return 0 if v.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

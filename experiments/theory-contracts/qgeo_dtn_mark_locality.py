"""QGEO DtN mark-locality -- a THEORY CONTRACT (not an empirical scorecard row).

Claim (boundary/DtN sector): the Z4 mark structure forces the boundary state to be
mark-rotation invariant.  Concretely, with marks placed at theta = j*pi/2 (j=0..3),

    Lambda  = |D_theta| + M_f ,      f(theta) = sum_{j=0}^{3} g(theta - j*pi/2)

    (1) Fourier support of f is ONLY n = 0 mod 4   (the 4 translates cancel all other n);
    (2) => [rho, Lambda] = 0   where rho is rotation by pi/2 (the Z4 generator);
    (3) => omega . rho = omega for the Lambda-canonical (Gibbs/spectral) state omega.

This is verified numerically on the circle, together with the negative controls the
contract must FAIL on:

    * Z3 marks (theta = j*2pi/3): support 0 mod 3, NOT pi/2-periodic  -> [rho,Lambda] != 0;
    * 4 generic (unequal) marks: mixed support                        -> [rho,Lambda] != 0.

Pure mathematics: it belongs in theory-contracts, never in evidence_scorecard.json.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

N = 64                       # grid points on the circle (divisible by 4)
KAPPA = 4.0                  # von Mises concentration of the mark bump g
BETA = 0.05                  # inverse "temperature" for the Lambda-canonical state
THETA = 2.0 * np.pi * np.arange(N) / N
MODES = np.fft.fftfreq(N, d=1.0 / N)     # integer Fourier modes n
RESULTS = Path(__file__).resolve().parent / "qgeo_dtn_results.json"


def _g(theta: np.ndarray) -> np.ndarray:
    """A smooth mark bump with nonzero Fourier weight on every mode."""
    return np.exp(KAPPA * np.cos(theta))


def _marks(angles: list[float]) -> np.ndarray:
    return sum(_g(THETA - a) for a in angles)


def _absD() -> np.ndarray:
    """|D_theta| as an N x N matrix (diagonal |n| in the Fourier basis)."""
    F = np.fft.fft(np.eye(N), axis=0) / np.sqrt(N)        # unitary DFT
    return (F.conj().T @ np.diag(np.abs(MODES)) @ F)


def _rho() -> np.ndarray:
    """Rotation by pi/2: (rho psi)(theta) = psi(theta - pi/2) = roll by N/4."""
    return np.roll(np.eye(N), N // 4, axis=0)


def _fourier_support(f: np.ndarray) -> dict:
    fh = np.fft.fft(f)
    mag = np.abs(fh)
    peak = mag.max()
    off = mag[(MODES.astype(int) % 4) != 0].max() / peak
    on3 = mag[(MODES.astype(int) % 3) != 0].max() / peak
    return {"max_off_mod4_rel": float(off), "max_off_mod3_rel": float(on3)}


def _commutator_norm(Lam: np.ndarray, rho: np.ndarray) -> float:
    C = rho @ Lam - Lam @ rho
    return float(np.linalg.norm(C) / np.linalg.norm(Lam))


def _state_invariance(Lam: np.ndarray, rho: np.ndarray, n_test: int = 8) -> float:
    """max_A |omega(rho A rho^dag) - omega(A)| for the Gibbs state of Lambda."""
    W = expm(-BETA * Lam)
    W = W / np.trace(W)
    rng = np.random.default_rng(7)
    worst = 0.0
    for _ in range(n_test):
        M = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
        A = (M + M.conj().T) / 2.0
        oa = np.trace(W @ A).real
        ora = np.trace(W @ (rho @ A @ rho.conj().T)).real
        worst = max(worst, abs(ora - oa) / (np.linalg.norm(A) / np.sqrt(N)))
    return float(worst)


def run() -> dict:
    absD = _absD()
    rho = _rho()
    cases = {
        "z4_marks_jpi2": [j * np.pi / 2 for j in range(4)],
        "z3_marks_2pij3": [j * 2 * np.pi / 3 for j in range(3)],
        "generic_4_marks": [0.0, 0.7, 2.1, 4.0],
    }
    tol = 1e-9
    out: dict = {"tol": tol, "cases": {}}
    for name, angles in cases.items():
        f = _marks(angles)
        Lam = absD + np.diag(f)
        sup = _fourier_support(f)
        comm = _commutator_norm(Lam, rho)
        inv = _state_invariance(Lam, rho)
        out["cases"][name] = {
            "support_mod4_clean": bool(sup["max_off_mod4_rel"] < tol),
            "max_off_mod4_rel": sup["max_off_mod4_rel"],
            "commutator_rho_Lambda": comm,
            "commutes": bool(comm < 1e-9),
            "state_invariance_dev": inv,
            "omega_rho_eq_omega": bool(inv < 1e-9),
        }

    z4 = out["cases"]["z4_marks_jpi2"]
    z3 = out["cases"]["z3_marks_2pij3"]
    gen = out["cases"]["generic_4_marks"]
    holds = (z4["support_mod4_clean"] and z4["commutes"] and z4["omega_rho_eq_omega"]
             and not z3["commutes"] and not gen["commutes"])
    out["contract_holds"] = bool(holds)
    out["verdict"] = (
        "CONTRACT HOLDS: Z4 marks at j*pi/2 give f with Fourier support only n=0 mod 4, "
        "hence [rho,Lambda]=0 and omega.rho=omega; the Z3 and 4-generic negative controls "
        "both break the commutator as required."
        if holds else
        "CONTRACT FAILED: see per-case diagnostics."
    )
    return out


def main() -> int:
    print("=" * 76)
    print("QGEO DtN mark-locality -- theory contract (Lambda=|D_theta|+M_f, rho=Z4 rotation)")
    print("=" * 76)
    res = run()
    for name, c in res["cases"].items():
        print(f"\n  {name}")
        print(f"    Fourier support clean mod 4 : {c['support_mod4_clean']}  "
              f"(max off-mode {c['max_off_mod4_rel']:.2e})")
        print(f"    [rho, Lambda] / |Lambda|    : {c['commutator_rho_Lambda']:.2e}  "
              f"-> commutes={c['commutes']}")
        print(f"    omega.rho = omega           : {c['omega_rho_eq_omega']}  "
              f"(dev {c['state_invariance_dev']:.2e})")
    print(f"\n-> {res['verdict']}")
    RESULTS.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS}")
    return 0 if res["contract_holds"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

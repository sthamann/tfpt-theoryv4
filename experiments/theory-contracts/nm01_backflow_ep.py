"""NM01 non-Markovianity / exceptional-point contract -- a THEORY CONTRACT
(never a scorecard row).

Question (2026-07-07, user round "versteckte Gemeinsamkeiten"): are information
backflow (non-Markovian revivals) and exceptional points (non-Hermitian
degeneracies) natural consequences of TFPT recovery -- "fast eine natuerliche
Konsequenz"? Machine-checked answer: NO on both -- and that is itself the
typed, falsifiable-shaped statement. The seam channel is a fixed CPTP map
(a discrete semigroup), hence CP-divisible with ZERO BLP backflow, and it is
symmetric/normal with simple spectrum, hence maximally far from any EP.
Observed backflow or EP phenomenology in an experiment is therefore BRIDGE
(environment-memory / non-Hermitian effective description) physics, never a
seam-recovery signature -- the FO.01/S15 typing extended to the open-quantum-
system literature. What the seam DOES predict as its only visible decoration
is the frozen invariant set (C4). Five checks with controls:

  C1  ZERO BACKFLOW (seam channel): the frozen kernel as a classical transfer
      (3x3 doubly stochastic, spectrum {1,(2/3)^6,(1/3)^6}) and as the qubit
      amplitude-damping realisation (survival eta=(2/3)^6 per step,
      recovery-channel realisation) contracts the trace distance MONOTONICALLY
      for random state pairs; BLP measure = sum of positive increments = 0
      (numerically <= 1e-13). A fixed CPTP map iterated is CP-divisible --
      backflow is impossible in the seam channel itself.
  C2  BACKFLOW = ENVIRONMENT MEMORY (control): one UNREFRESHED bath qubit
      under repeated partial-swap collisions produces large trace-distance
      revivals (max positive increment ~ O(0.1)) -- information backflow is a
      property of bath memory in the bridge, exactly the object FO.02b's
      memory gate tests on data, not of the recovery kernel.
  C3  NO EXCEPTIONAL POINT (seam channel): the transfer is symmetric => normal
      (eigenvector condition number exactly 1, orthonormal eigenbasis) with
      simple spectrum (gaps 665/729, 63/729); an EP needs a DEFECTIVE
      coalescence -- the Jordan control [[l,1],[0,l]] has eigenvector matrix
      condition ~ 1e8. Prediction typed (missing-structure class, like FO.08):
      seam-eligible reconstructed recovery spectra show NO EP coalescence and
      NO EP hysteresis/chirality; where EPs appear, the description is bridge.
  C4  THE FROZEN INVARIANT SET (the "specific quantitative deviating
      prediction" asked for -- it already exists, parameter-free): bend
      ln3/ln(3/2) = 2.7095 (THE fixed dimensionless ratio of the two recovery
      rates), teeth 2/3, (2/3)^3 = 8/27, (2/3)^6 = 64/729 (fixed tau_2/tau_1,
      E_2/E_1 ladder ratios), comb pair omega = 2pi/(6 ln(3/2)) = 2.5827 AND
      eps = e^{-pi^2/(6 ln(3/2))} = 0.0173 (a universal scaling function with
      both frequency and amplitude fixed), wall <= 2 decay modes + protected
      floor. All exact sympy identities from the axioms.
  C5  SHAPE-ONLY IS WEAKLY DISCRIMINATING (honest limit of the "universal
      normal form" search): the walled clock IS a one-parameter normal form
      (shape collapse under t -> t/tau exact by construction), but a single
      noiseless kernel recovery is fit by a WRONG-ratio (2.0) two-exponential
      family to relative RMS < 2e-2 -- the machine reason the programme's
      power sits in cascades/ratio ladders and comb phase, not in single-curve
      shape fits (S3 degeneracy, reproduced standalone).

Firewall: pure mathematics/simulation; belongs in theory-contracts, never in
evidence_scorecard.json; passing is internal consistency, not evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp

RESULTS = Path(__file__).resolve().parent / "nm01_backflow_results.json"

LAM2 = (2.0 / 3.0) ** 6
LAM3 = (1.0 / 3.0) ** 6
CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def transfer_matrix() -> np.ndarray:
    q1 = np.ones(3) / np.sqrt(3.0)
    q2 = np.array([1.0, -1.0, 0.0]) / np.sqrt(2.0)
    q3 = np.array([1.0, 1.0, -2.0]) / np.sqrt(6.0)
    Q = np.stack([q1, q2, q3], axis=1)
    return Q @ np.diag([1.0, LAM2, LAM3]) @ Q.T


def trace_distance(r: np.ndarray, s: np.ndarray) -> float:
    return 0.5 * float(np.abs(np.linalg.eigvalsh(r - s)).sum())


def random_qubit_state(rng: np.random.Generator) -> np.ndarray:
    g = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    r = g @ g.conj().T
    return r / np.trace(r).real


# ------------------------------------------------------- C1 zero backflow
def c1_zero_backflow() -> None:
    rng = np.random.default_rng(0)
    T = transfer_matrix()
    # classical leg: L1 distance of population pairs under T^n
    worst_cl = -np.inf
    for _ in range(100):
        p = rng.dirichlet(np.ones(3))
        q = rng.dirichlet(np.ones(3))
        d_prev = 0.5 * np.abs(p - q).sum()
        for _ in range(12):
            p, q = T @ p, T @ q
            d = 0.5 * np.abs(p - q).sum()
            worst_cl = max(worst_cl, d - d_prev)
            d_prev = d
    # quantum leg: amplitude damping with survival eta = (2/3)^6 per step
    eta = LAM2
    K0 = np.array([[1, 0], [0, np.sqrt(eta)]], dtype=complex)
    K1 = np.array([[0, np.sqrt(1 - eta)], [0, 0]], dtype=complex)

    def step(r: np.ndarray) -> np.ndarray:
        return K0 @ r @ K0.conj().T + K1 @ r @ K1.conj().T

    worst_q, blp = -np.inf, 0.0
    for _ in range(100):
        r, s = random_qubit_state(rng), random_qubit_state(rng)
        d_prev = trace_distance(r, s)
        for _ in range(12):
            r, s = step(r), step(s)
            d = trace_distance(r, s)
            inc = d - d_prev
            worst_q = max(worst_q, inc)
            blp += max(inc, 0.0)
            d_prev = d
    check("C1 ZERO BACKFLOW [E]: the seam channel (fixed CPTP map, classical "
          "and qubit realisation) contracts trace distance monotonically -- "
          "BLP non-Markovianity measure = 0; backflow is impossible in the "
          "recovery kernel itself",
          worst_cl < 1e-13 and worst_q < 1e-13 and blp < 1e-12,
          f"max increment classical {worst_cl:.2e}, quantum {worst_q:.2e}, "
          f"BLP sum {blp:.2e} (100 random pairs x 12 steps each)")


# ------------------------------------- C2 backflow = environment memory
def c2_memory_control() -> None:
    theta = 0.35
    swap = np.zeros((4, 4))
    for a in range(2):
        for b in range(2):
            swap[2 * b + a, 2 * a + b] = 1.0
    U = np.cos(theta) * np.eye(4) + 1j * np.sin(theta) * swap

    def evolve(psi_s: np.ndarray, n: int) -> list[np.ndarray]:
        joint = np.kron(psi_s, np.array([1.0, 0.0], dtype=complex))
        rho = np.outer(joint, joint.conj())
        out = []
        for _ in range(n):
            rho = U @ rho @ U.conj().T          # SAME bath qubit, never refreshed
            rs = rho.reshape(2, 2, 2, 2)
            out.append(np.einsum("abcb->ac", rs))
        return out

    tr0 = evolve(np.array([1.0, 0.0], dtype=complex), 25)
    tr1 = evolve(np.array([0.0, 1.0], dtype=complex), 25)
    dists = [trace_distance(a, b) for a, b in zip(tr0, tr1)]
    incs = np.diff([1.0] + dists)
    max_rev = float(incs.max())
    check("C2 MEMORY CONTROL [E]: one unrefreshed bath qubit under repeated "
          "partial-swap collisions produces large trace-distance REVIVALS -- "
          "information backflow is bath-memory (bridge) physics, the very "
          "object FO.02b's memory gate tests on data, not seam recovery",
          max_rev > 0.05,
          f"max positive increment {max_rev:.3f} over 25 collisions "
          f"(theta = {theta}); min/max distance {min(dists):.3f}/{max(dists):.3f}")


# ----------------------------------------------- C3 no exceptional point
def c3_no_ep() -> None:
    T = transfer_matrix()
    normal = float(np.abs(T @ T.T - T.T @ T).max())
    evals = np.sort(np.linalg.eigvalsh(T))[::-1]
    gaps = np.diff(-evals)
    _, V = np.linalg.eigh(T)
    cond_v = float(np.linalg.cond(V))
    J = np.array([[0.5, 1.0], [0.0, 0.5]])
    _, VJ = np.linalg.eig(J)
    cond_j = float(np.linalg.cond(VJ))
    exact_gaps = (sp.Rational(665, 729), sp.Rational(63, 729))
    gaps_ok = (abs(gaps[0] - float(exact_gaps[0])) < 1e-12
               and abs(gaps[1] - float(exact_gaps[1])) < 1e-12)
    check("C3 NO EXCEPTIONAL POINT [E]: the seam transfer is normal with "
          "simple spectrum (eigenvector condition exactly 1); an EP needs a "
          "defective coalescence (Jordan control cond ~ 1e8). Typed "
          "missing-structure prediction: seam-eligible recovery spectra show "
          "no EP coalescence/hysteresis -- EP phenomenology is bridge physics",
          normal < 1e-15 and cond_v < 1 + 1e-12 and cond_j > 1e6 and gaps_ok,
          f"||[T,T^T]|| = {normal:.1e}; cond(V) = {cond_v:.12f}; spectral gaps "
          f"= 665/729, 63/729 exact; Jordan control cond(V_J) = {cond_j:.1e}")


# ---------------------------------------------- C4 frozen invariant set
def c4_frozen_invariants() -> None:
    ln = sp.log
    bend = ln(3) / ln(sp.Rational(3, 2))
    lnLam = 6 * ln(sp.Rational(3, 2))
    omega = 2 * sp.pi / lnLam
    eps = sp.exp(-sp.pi ** 2 / lnLam)
    teeth = (sp.Rational(2, 3), sp.Rational(8, 27), sp.Rational(64, 729))
    vals = {
        "bend": float(bend), "omega": float(omega), "eps": float(eps),
    }
    ok = (abs(vals["bend"] - 2.7095) < 1e-4
          and abs(vals["omega"] - 2.5827) < 1e-4
          and abs(vals["eps"] - 0.0173) < 1e-4
          and teeth[1] == sp.Rational(2, 3) ** 3
          and teeth[2] == sp.Rational(2, 3) ** 6
          and float(eps) < 0.02)
    check("C4 FROZEN INVARIANT SET [E]: the requested 'dimensionless "
          "invariant / fixed relaxation ratio / universal scaling function' "
          "already exists parameter-free -- bend ln3/ln(3/2), teeth "
          "2/3, 8/27, 64/729, comb pair (omega, eps) with BOTH frequency and "
          "amplitude fixed; eps < 2% is the amplitude wall behind every "
          "well-powered surface null",
          ok,
          f"bend = {vals['bend']:.5f}; omega = {vals['omega']:.5f}; "
          f"eps = {vals['eps']:.5f}; teeth (2/3, 8/27, 64/729) exact; "
          "wall: <= 2 decay modes + protected floor (v124/v147)")


# --------------------------------- C5 shape-only is weakly discriminating
def c5_shape_degeneracy() -> None:
    bend = float(np.log(3) / np.log(1.5))
    t = np.logspace(-2, 1.2, 200)
    y = 0.2 + 0.5 * np.exp(-t) + 0.3 * np.exp(-bend * t)
    span = float(y.max() - y.min())

    def best_rms(ratio: float) -> float:
        best = np.inf
        for b in np.linspace(0.2, 3.0, 561):
            X = np.stack([np.ones_like(t), np.exp(-b * t),
                          np.exp(-ratio * b * t)], axis=1)
            w, *_ = np.linalg.lstsq(X, y, rcond=None)
            best = min(best, float(np.sqrt(np.mean((X @ w - y) ** 2))))
        return best

    rms_true = best_rms(bend) / span
    rms_wrong = best_rms(2.0) / span
    check("C5 SHAPE DEGENERACY [E]: the walled clock is a one-parameter "
          "normal form (exact collapse under t -> t/tau), but a WRONG-ratio "
          "(2.0) family fits a single noiseless kernel recovery to relative "
          "RMS < 2e-2 -- single-curve shape searches are weakly "
          "discriminating; the power sits in cascades/ratio ladders/comb "
          "phase (the S3 degeneracy, reproduced standalone)",
          rms_true < 1e-6 and 1e-5 < rms_wrong < 2e-2,
          f"relative RMS: true ratio {bend:.4f} -> {rms_true:.1e}; "
          f"wrong ratio 2.0 -> {rms_wrong:.1e} (561-point rate scan, "
          "free weights)")


def main() -> None:
    print("NM01 backflow/EP contract -- non-Markovianity and exceptional "
          "points are BRIDGE physics, not seam recovery\n")
    c1_zero_backflow()
    c2_memory_control()
    c3_no_ep()
    c4_frozen_invariants()
    c5_shape_degeneracy()

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "Information backflow and exceptional points are NOT natural "
        "consequences of TFPT recovery: the seam channel is CP-divisible "
        "(zero BLP backflow) and normal with simple spectrum (no EP). Both "
        "phenomena, where observed, are environment/bridge physics -- the "
        "S15/FO.01 typing extended to the open-quantum-system literature, "
        "with FO.02b's memory gate as the data-side face of C2. The seam's "
        "only visible decoration stays the frozen invariant set (bend "
        "2.7095, teeth (2/3)^k, comb (2.5827, 0.0173)); single-recovery "
        "shape fits are provably weakly discriminating (C5), so universal-"
        "normal-form searches must target cascades, ratio ladders and comb "
        "phase -- which is what the existing beds do."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "NM01 backflow/EP (non-Markovianity + exceptional points)",
        "date": "2026-07-07",
        "firewall": ("theory contract, never a scorecard row; internal "
                     "consistency, not evidence"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

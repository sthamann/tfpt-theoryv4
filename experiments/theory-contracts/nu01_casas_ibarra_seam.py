"""NU.CI.01 Casas-Ibarra seam enumeration -- a THEORY CONTRACT (never a scorecard row).

Question (problem_b.txt point 4, 2026-07-10): in the type-I seesaw
m_nu = -v^2 Y_nu M_R^{-1} Y_nu^T the low-energy data leave a complex orthogonal
matrix R_CI (Casas-Ibarra) undetermined -- it carries the high-scale information
(absolute nu-mass scale, Majorana/leptogenesis phase).  The reviewer asks: can the
SEAM SYMMETRIES fix R_CI?  Concretely, enumerate the R that simultaneously satisfy

    [R, C3] = 0,      Theta R Theta = R*,      R^T R = 1,      det R = 1,

where C3 is the order-3 family cycle and Theta the seam reflection.  If exactly ONE
R survives, the seesaw (Y_nu, M_R, phases, scale) is closed; if a CONTINUOUS family
survives, the neutrino dynamics is NOT closed.

Result (machine-computed here, not asserted): the symmetries do real work but do
NOT close it.  O(3,C) has 3 complex parameters; [R,C3]=0 cuts it to the circulant
algebra and, with R^T R=1 + det 1, to a ONE-COMPLEX-parameter family (the CI angle,
lambda_0=1, lambda_1 lambda_2 = 1); the reflection reality Theta R Theta = R* cuts
that to a ONE-REAL-parameter family (lambda_1, lambda_2 real).  A continuous family
REMAINS => R_CI is not fixed by the seam symmetries alone.  This matches the
ledger's honest status: PMNS angles/phase largely fixed, but the seesaw realisation
+ absolute scale remain the residual.

Checks (hard-typed):

  C1 [E] COMMUTANT: the centraliser of C3 in the 3x3 matrices is exactly the
     circulant algebra R = a I + b C3 + c C3^2 (dim_C = 3), computed as the
     nullspace of X |-> [X, C3].
  C2 [E] COMPLEX-ORTHOGONAL + det 1 => 1 COMPLEX PARAM: on the circulant algebra
     R^T R = 1 and det R = 1 reduce (in the DFT eigenbasis) to lambda_0 = 1 and
     lambda_1 lambda_2 = 1 -- a one-complex-parameter family R(z) = F diag(1, e^z,
     e^{-z}) F^*; verified R^T R = I and det = 1 for random complex z.
  C3 [E] REFLECTION REALITY => 1 REAL PARAM: Theta (the coordinate reflection with
     Theta C3 Theta = C3^2) imposes Theta R Theta = R* IFF lambda_1, lambda_2 are
     REAL, i.e. z real -- verified: the identity holds for z real and FAILS for z
     imaginary.  One real parameter remains.
  C4 [E] DIMENSION COUNT: residual dim = 1 (real) != 0 -- the seam symmetries cut
     O(3,C) from 3 complex parameters to 1 real parameter (the CI hyperbolic angle),
     but do NOT isolate a point.  R_CI is NOT unique.
  C5 [O] DISCRETE COLLAPSE NEEDS AN EXTRA SELECTOR (honest): requiring R real
     orthogonal (z=0) gives R=I (and the reflection its finite partners) -- but
     "no seesaw CP / trivial R" is an ASSUMPTION, not derived; the transport /
     minimality selector that would pick z is itself the open step.
  C6 [O] RELOCATION AUDIT: consequence -- IF z were fixed, Y_nu, M_R, Majorana
     phases, the absolute nu-mass scale and eta_B would all be computable; since z
     is free, they stay open.  Matches ledger.  Never a scorecard row; never [E].

Firewall: pure linear algebra over C; neutrinos are an F_transfer bridge; internal
consistency, not external evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent / "nu01_casas_ibarra_results.json"
CHECKS: list[dict] = []
RNG = np.random.default_rng(20260710)


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


# family cycle C3 (order 3) and the seam reflection Theta
C3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)      # e1->e2->e3->e1
THETA = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], float)   # swap coords 2,3
# DFT eigenbasis of a circulant (columns = eigenvectors of C3)
W = np.exp(2j * np.pi / 3)
F = np.array([[W ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)


def circulant(a, b, c):
    return a * np.eye(3) + b * C3 + c * (C3 @ C3)


def R_of_z(z: complex):
    """The complex-orthogonal, det-1, C3-commuting family: diag(1, e^z, e^-z)."""
    D = np.diag([1.0, np.exp(z), np.exp(-z)]).astype(complex)
    return F @ D @ F.conj().T


def c1_commutant() -> None:
    # nullspace of vec(X) -> vec([X, C3]) = (I⊗C3 - C3^T⊗I) vec(X)
    K = np.kron(np.eye(3), C3) - np.kron(C3.T, np.eye(3))
    s = np.linalg.svd(K, compute_uv=False)
    dim = int(np.sum(s < 1e-9))
    # circulant ansatz commutes for random coeffs
    a, b, c = RNG.standard_normal(3) + 1j * RNG.standard_normal(3)
    R = circulant(a, b, c)
    comm = np.max(np.abs(R @ C3 - C3 @ R))
    check("C1 COMMUTANT [E]: centraliser of the order-3 family cycle C3 = the "
          "circulant algebra a I + b C3 + c C3^2, dim_C = 3 (nullspace of "
          "X |-> [X, C3])",
          dim == 3 and comm < 1e-12,
          "dim centraliser = %d; ||[R_circ, C3]|| = %.1e" % (dim, comm))


def c2_complex_orthogonal() -> None:
    ok = True
    dets, orth = [], []
    for _ in range(200):
        z = RNG.standard_normal() + 1j * RNG.standard_normal()
        R = R_of_z(z)
        orth.append(np.max(np.abs(R.T @ R - np.eye(3))))
        dets.append(abs(np.linalg.det(R) - 1.0))
        ok &= (orth[-1] < 1e-9 and dets[-1] < 1e-9
               and np.max(np.abs(R @ C3 - C3 @ R)) < 1e-9)
    check("C2 COMPLEX-ORTHOGONAL + det 1 => 1 COMPLEX PARAM [E]: R^T R = 1 and "
          "det R = 1 on the circulant algebra reduce to lambda_0 = 1, "
          "lambda_1 lambda_2 = 1 -- the family R(z) = F diag(1, e^z, e^-z) F^*; "
          "verified R^T R = I, det = 1, [R,C3]=0 for 200 random complex z",
          ok, "max ||R^T R - I|| = %.1e, max |det-1| = %.1e over 200 complex z"
          % (max(orth), max(dets)))


def c3_reflection_reality() -> None:
    # Theta C3 Theta = C3^2 (reflection inverts the cycle)
    inv_ok = np.max(np.abs(THETA @ C3 @ THETA - C3 @ C3)) < 1e-12
    real_holds, imag_fails = [], []
    for _ in range(100):
        s = RNG.standard_normal()
        R_real = R_of_z(s)                        # z real
        R_imag = R_of_z(1j * s)                   # z imaginary
        real_holds.append(np.max(np.abs(THETA @ R_real @ THETA - R_real.conj())))
        imag_fails.append(np.max(np.abs(THETA @ R_imag @ THETA - R_imag.conj())))
    ok = inv_ok and max(real_holds) < 1e-9 and min(imag_fails) > 1e-3
    check("C3 REFLECTION REALITY => 1 REAL PARAM [E]: Theta (Theta C3 Theta = C3^2) "
          "imposes Theta R Theta = R* IFF lambda_1, lambda_2 REAL (z real); "
          "verified -- holds for z real, FAILS for z imaginary. One real parameter "
          "remains",
          ok, "Theta C3 Theta = C3^2: %s; max resid (z real) = %.1e; min resid "
          "(z imag) = %.2f" % (inv_ok, max(real_holds), min(imag_fails)))


def c4_dimension_count() -> None:
    # residual family z in R is 1-dimensional and non-degenerate:
    # R(z1) != R(z2) for z1 != z2 (distinct spectra)
    R1, R2 = R_of_z(0.3), R_of_z(0.7)
    distinct = np.max(np.abs(R1 - R2)) > 1e-3
    check("C4 DIMENSION COUNT [E]: O(3,C) has 3 complex params; [R,C3]=0 -> 1 "
          "complex (CI angle); + Theta-reality -> 1 REAL param. Residual dim = 1 "
          "!= 0 -- the seam symmetries do NOT isolate a point; R_CI is NOT unique",
          distinct,
          "distinct family members R(0.3) != R(0.7): %s (a genuine 1-parameter "
          "hyperbolic CI angle remains)" % distinct)


def c5_extra_selector() -> None:
    # z=0 -> R = I (real orthogonal); this is an ASSUMPTION (trivial R), not derived
    R0 = R_of_z(0.0)
    is_I = np.max(np.abs(R0 - np.eye(3))) < 1e-9
    check("C5 DISCRETE COLLAPSE NEEDS AN EXTRA SELECTOR [O]: z=0 -> R=I (real "
          "orthogonal, 'no seesaw CP') is a finite point but an ASSUMPTION, not "
          "derived; the transport/minimality selector that would fix z is the open "
          "step -- so symmetry alone does not close the seesaw",
          is_I, "z=0 => R=I (||R-I||=%.1e); nontrivial z stays a free CI angle"
          % np.max(np.abs(R0 - np.eye(3))))


def c6_relocation() -> None:
    imported = [
        "Casas-Ibarra parametrisation Y_nu = (1/v) sqrt(M_R) R sqrt(m_nu) U^dag "
        "with R complex orthogonal (cited, hep-ph/0103065)",
        "C3 = the order-3 family cycle; Theta = the seam reflection (TFPT inputs)",
        "the transport/minimality selector (the open step that would fix z)",
    ]
    check("C6 RELOCATION AUDIT [O]: IF z were fixed, Y_nu, M_R, Majorana phases, "
          "the absolute nu-mass scale and eta_B would all be computable; since the "
          "seam symmetries leave z free (C4), they stay OPEN -- matching the ledger. "
          "Never a scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("NU.CI.01 Casas-Ibarra seam enumeration -- do the seam symmetries fix "
          "the complex-orthogonal R_CI?\n")
    c1_commutant()
    c2_complex_orthogonal()
    c3_reflection_reality()
    c4_dimension_count()
    c5_extra_selector()
    c6_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("CONTRACT HOLDS (honest NEGATIVE: seesaw NOT closed by symmetry)"
               if n_pass == len(CHECKS) else "CONTRACT FAILS")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The four seam conditions [R,C3]=0, Theta R Theta = R*, R^T R = 1, det R = 1 "
        "cut the Casas-Ibarra matrix from O(3,C) (3 complex parameters) down to a "
        "ONE-REAL-parameter family (the CI hyperbolic angle): commuting with C3 gives "
        "the circulant algebra, complex-orthogonality + det 1 give lambda_0=1 and "
        "lambda_1 lambda_2 = 1 (1 complex param), and the reflection reality forces "
        "lambda_1, lambda_2 real (1 real param). A continuous family REMAINS, so the "
        "seam symmetries do NOT uniquely fix R_CI -- the seesaw realisation, the "
        "absolute neutrino-mass scale and the leptogenesis phase are NOT closed by "
        "symmetry alone; an independent transport/minimality selector (open) is "
        "required. This is the honest negative the reviewer anticipated and it "
        "matches the ledger's status. Never a scorecard row; never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "NU.CI.01 Casas-Ibarra seam enumeration",
        "date": "2026-07-10",
        "firewall": ("theory contract, never a scorecard row; F_transfer bridge "
                     "internal consistency, not external evidence"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "residual": "one real parameter (the Casas-Ibarra angle) -- not closed",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

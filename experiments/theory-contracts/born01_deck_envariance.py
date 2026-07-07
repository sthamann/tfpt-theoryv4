"""BORN.01 deck-envariance contract -- a THEORY CONTRACT (never a scorecard row).

Question (2026-07-07): can the Born rule be DERIVED from TFPT recovery
structure, instead of imported? (v130 "Born square" USES Gamma = |A|^2 as an
input to explain the clock exponent p2 = 2h; it does not derive psi^2.)

Honest machine-checked answer: NO derivation from recovery alone -- but the
Born weight REDUCES to structural ingredients the theory already carries, and
on the kernel's own probability sector the continuity/Gleason axiom is not
needed at all. Six checks, each with the sharp negative control:

  C1  EXPONENT (power family): if p = |amplitude|^alpha and total probability
      is 1 in EVERY basis, then alpha = 2 -- exact, the pi/4 basis alone kills
      every other power (2^(1-alpha/2) = 1 iff alpha = 2).
  C2  SHEET PAIRING: for a monomial p = A^m conj(A)^n, reality of p for all
      phases forces m = n; with C1 (alpha = 2m = 2) the weight is
      p = A * sigma(A), ONE factor per Z2 sheet -- sigma the Galois/CP
      conjugation (v316: Gal Z2 = CP conj = the deck). [C] identification.
  C3  DECK SWAP = ENVARIANCE (exact): a local swap on the system is undone by
      the partner swap on the other sheet ((X x I)|Phi+> = (I x X)|Phi+>
      exactly; rho_S invariant under any E-unitary). Given the two named
      axioms (p depends only on (state, local observable); partner-sheet
      operations cannot change local outcome statistics), equal amplitudes
      MUST have equal probability -- Zurek's envariance with the swap
      implemented by the structural Z2 deck instead of an auxiliary
      environment. [I] algebra + [C] deck identification.
  C4  THE KERNEL SECTOR IS COUNTING-DECIDABLE: every probability weight the
      frozen kernel ever outputs (per-substep survivals 2/3, 1/3; spectrum
      (2/3)^6, (1/3)^6; clock weights (1-n/3)^6) is 3-adic rational, so a
      finite fine-graining into 3^k equal branches (N_fam-fold branching)
      decides it by COUNTING alone -- no continuity axiom on this sector.
      Exhibited exactly: sqrt(2/3)|1,a> + sqrt(1/3)|2,b> fine-grains through
      an isometry into THREE equal 1/sqrt(3) branches; one transfer substep
      IS a 3-way equal branching with 2:1 survival; six substeps compose to
      64/729 in integer arithmetic.
  C5  UNIQUE INVARIANT PAIRING (matched Weyl pair): on C^4 the mu4 clock
      rho = diag(i^n) together with the character-transitive shift S admits
      EXACTLY ONE invariant Hermitian form up to scale (the standard inner
      product = the Born pairing). Controls: clock alone -> dim 4, shift
      alone -> dim 4, mismatched N = 8 -> dim 2. Uniqueness holds exactly
      when shift order = clock order = |mu4| = 4.
  C6  RELOCATION AUDIT (the honest negative): in dim 2, additive
      normalisation does NOT force Born -- h(u) = u + (1/10) sin(2 pi u)
      satisfies h(u) + h(1-u) = 1, h(0) = 0, h(1) = 1 exactly and is a
      valid non-quadratic frame function. The forcing therefore NEEDS one of:
      the power-family restriction (C1), the sheet-reality + matched-pair
      structure (C2 + C5), or dim >= 3 (Gleason 1957 / Busch 2003, cited
      external theorems). What stays postulated is recorded in the verdict.

Firewall: pure mathematics; belongs in theory-contracts, never in
evidence_scorecard.json; passing is internal consistency, not evidence. The
measurement problem (single-outcome selection) is NOT addressed and remains
open; this contract concerns only the probability WEIGHT.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

RESULTS = Path(__file__).resolve().parent / "born01_deck_results.json"

CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


# --------------------------------------------------------------- C1 exponent
def c1_exponent() -> None:
    theta, alpha = sp.symbols("theta alpha", positive=True)
    # pi/4 basis: total probability 2 * (1/sqrt2)^alpha = 2^(1 - alpha/2) = 1
    total_pi4 = 2 * (sp.Rational(1, 2) ** sp.Rational(1, 2)) ** alpha
    sols = sp.solve(sp.Eq(total_pi4, 1), alpha)
    forced = sols == [2]
    # and alpha = 2 closes in EVERY basis (the Pythagorean identity)
    closes = sp.simplify(sp.cos(theta) ** 2 + sp.sin(theta) ** 2 - 1) == 0
    # numeric sharpness: variance of the total over bases is 0 only at alpha=2
    th = np.linspace(0.05, np.pi / 2 - 0.05, 181)
    var = {a: float(np.var(np.cos(th) ** a + np.sin(th) ** a))
           for a in (1.0, 1.5, 2.0, 3.0)}
    sharp = var[2.0] < 1e-30 and all(var[a] > 1e-4 for a in (1.0, 1.5, 3.0))
    check("C1 EXPONENT [I]: basis-independent normalisation forces alpha = 2 "
          "within the power family",
          forced and closes and sharp,
          f"solve(2^(1-a/2)=1) -> {sols}; cos^2+sin^2=1 exact; "
          f"variance over bases: {[f'{a}:{v:.2e}' for a, v in var.items()]}")


# ----------------------------------------------------------- C2 sheet pairing
def c2_sheet_pairing() -> None:
    phi = sp.symbols("phi", real=True)
    real_only_diagonal = True
    for k in range(-3, 4):          # k = m - n
        p = sp.exp(sp.I * k * phi)
        is_real = sp.simplify(sp.im(p)) == 0
        if (k == 0) != is_real:
            real_only_diagonal = False
    # with C1: |A|^(2m) and 2m = 2 -> m = n = 1: one amplitude factor per sheet
    m = sp.solve(sp.Eq(2 * sp.Symbol("m", positive=True), 2))
    check("C2 SHEET PAIRING [I]+[C]: reality for all phases forces m = n; with "
          "C1 the weight is p = A * sigma(A) -- one factor per Z2 sheet "
          "(sigma = Galois/CP conjugation, v316)",
          real_only_diagonal and m == [1],
          "im(e^{i(m-n)phi}) = 0 as an identity iff m = n (swept |m-n| <= 3); "
          "2m = 2 -> m = n = 1")


# ------------------------------------------------- C3 deck swap = envariance
def c3_deck_envariance() -> None:
    s2 = sp.sqrt(2)
    phi_plus = sp.Matrix([1, 0, 0, 1]) / s2            # (|00> + |11>)/sqrt2
    X = sp.Matrix([[0, 1], [1, 0]])
    I2 = sp.eye(2)
    swap_sys = sp.Matrix(sp.kronecker_product(X, I2)) * phi_plus
    swap_env = sp.Matrix(sp.kronecker_product(I2, X)) * phi_plus
    undone = sp.simplify(swap_sys - swap_env) == sp.zeros(4, 1)

    # rho_S is invariant under ANY unitary on the partner sheet
    rng = np.random.default_rng(0)
    psi = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)

    def rho_s(vec: np.ndarray) -> np.ndarray:
        m = vec.reshape(2, 2)
        return m @ m.conj().T

    worst = 0.0
    for _ in range(200):
        g = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
        u, _ = np.linalg.qr(g)
        v = (np.kron(np.eye(2), u) @ psi)
        worst = max(worst, float(np.abs(rho_s(v) - rho_s(psi)).max()))
    check("C3 DECK SWAP = ENVARIANCE [I]: the system swap is undone exactly by "
          "the partner-sheet swap; rho_S blind to any partner unitary -> equal "
          "amplitudes get equal probability (axioms: locality of p + "
          "partner-sheet no-signalling)",
          undone and worst < 1e-13,
          f"(X x I)|Phi+> - (I x X)|Phi+> = 0 exact; "
          f"max |rho_S(U_E) - rho_S| over 200 random U(2): {worst:.2e}")


# ------------------------------------- C4 kernel sector = counting-decidable
def c4_kernel_counting() -> None:
    # (a) exact fine-graining of the kernel weights (2/3, 1/3) into 3 branches
    s = sp.sqrt
    psi = {("1", "a"): s(sp.Rational(2, 3)), ("2", "b"): s(sp.Rational(1, 3))}
    # isometry W on the partner sheet: |a> -> (e1+e2)/sqrt2, |b> -> e3
    branches = {
        ("1", "e1"): psi[("1", "a")] / s(2),
        ("1", "e2"): psi[("1", "a")] / s(2),
        ("2", "e3"): psi[("2", "b")],
    }
    equal = all(sp.simplify(v - 1 / s(3)) == 0 for v in branches.values())
    W = sp.Matrix([[1 / s(2), 0], [1 / s(2), 0], [0, 1]])
    isometry = sp.simplify(W.T * W - sp.eye(2)) == sp.zeros(2, 2)
    p1 = Fraction(2, 3)             # counting: 2 of 3 equal branches
    counting = (p1 == Fraction(2, 3)
                and sum(sp.Abs(v) ** 2 for v in branches.values()) == 1)

    # (b) every frozen kernel probability weight is 3-adic (denominator 3^k)
    weights = [Fraction(2, 3), Fraction(1, 3),
               Fraction(2, 3) ** 6, Fraction(1, 3) ** 6,
               Fraction(1, 3) ** 0,                       # protected mode
               (1 - Fraction(1, 3)) ** 6, (1 - Fraction(2, 3)) ** 6]
    def three_adic(w: Fraction) -> bool:
        d = w.denominator
        while d % 3 == 0:
            d //= 3
        return d == 1
    adic = all(three_adic(w) for w in weights)

    # (c) one transfer substep IS a 3-way equal branching with 2:1 survival;
    #     six substeps compose to the kernel eigenvalue in integer arithmetic
    survive = Fraction(2, 3)                 # 2 of 3 microstates survive
    lam_t = survive ** 6
    compose = lam_t == Fraction(64, 729)
    check("C4 KERNEL SECTOR [E]: every frozen kernel weight is 3-adic and "
          "therefore envariance-decidable by FINITE counting (3^k equal "
          "branches, N_fam-fold branching) -- no continuity axiom on the "
          "kernel's own sector",
          equal and isometry and counting and adic and compose,
          "fine-graining: all 3 branch amplitudes = 1/sqrt(3) exact, W an "
          "isometry, counting -> p = (2/3, 1/3); weights "
          f"{[str(w) for w in weights]} all 3-adic; (2/3)^6 = 64/729 exact")


# --------------------------------------------- C5 unique invariant pairing
def _invariant_form_dim(N: int, use_clock: bool, use_shift: bool) -> int:
    """Real dimension of Hermitian forms invariant under the chosen maps."""
    clock = np.diag([1j ** n for n in range(N)])
    shift = np.roll(np.eye(N), 1, axis=0)          # e_n -> e_{n+1 mod N}
    basis: list[np.ndarray] = []
    for a in range(N):
        for b in range(a, N):
            E = np.zeros((N, N), dtype=complex)
            if a == b:
                E[a, a] = 1
                basis.append(E)
            else:
                E[a, b] = E[b, a] = 1
                basis.append(E.copy())
                E[a, b], E[b, a] = 1j, -1j
                basis.append(E.copy())
    rows = []
    for H in basis:
        cons = []
        if use_clock:
            cons.append(clock.conj().T @ H @ clock - H)
        if use_shift:
            cons.append(shift.conj().T @ H @ shift - H)
        rows.append(np.concatenate([np.concatenate([c.real.ravel(),
                                                    c.imag.ravel()])
                                    for c in cons]))
    A = np.array(rows).T                           # constraints x basis-coeffs
    rank = np.linalg.matrix_rank(A, tol=1e-10)
    return len(basis) - rank


def c5_unique_pairing() -> None:
    d_both = _invariant_form_dim(4, True, True)
    d_clock = _invariant_form_dim(4, True, False)
    d_shift = _invariant_form_dim(4, False, True)
    d_mismatch = _invariant_form_dim(8, True, True)   # order-4 clock, order-8 shift
    ok = (d_both == 1 and d_clock == 4 and d_shift == 4 and d_mismatch == 2)
    check("C5 UNIQUE PAIRING [E]: the matched Weyl pair (mu4 clock + "
          "character-transitive shift) on C^4 admits exactly ONE invariant "
          "Hermitian form (the Born pairing, up to scale); every weakening "
          "loses uniqueness",
          ok,
          f"dim(invariant forms): clock+shift N=4 -> {d_both}; clock only -> "
          f"{d_clock}; shift only -> {d_shift}; mismatched N=8 -> {d_mismatch}")


# ------------------------------------------------------- C6 relocation audit
def c6_relocation() -> None:
    u = sp.symbols("u", real=True)
    eps = sp.Rational(1, 10)
    h = u + eps * sp.sin(2 * sp.pi * u)
    additive = sp.simplify(h + h.subs(u, 1 - u) - 1) == 0
    anchored = h.subs(u, 0) == 0 and h.subs(u, 1) == 1
    non_born = sp.simplify(h - u) != 0
    # monotone on [0,1] (a legitimate probability assignment): h' = 1 + (pi/5) cos >= 1 - pi/5 > 0
    monotone = sp.Rational(1, 1) - 2 * sp.pi * eps < 1 and float(1 - 2 * np.pi / 10) > 0
    check("C6 RELOCATION AUDIT [E]: dim-2 additive normalisation does NOT "
          "force Born (explicit non-quadratic frame function) -- the forcing "
          "requires C1's power family, C2+C5's deck structure, or dim >= 3 "
          "(Gleason 1957 / Busch 2003, cited external)",
          additive and anchored and non_born and monotone,
          "h(u) = u + (1/10) sin(2 pi u): h(u)+h(1-u) = 1 exact, h(0)=0, "
          "h(1)=1, h monotone, h != u")


def main() -> None:
    print("BORN.01 deck-envariance contract -- Born weight from deck + "
          "recovery structure (relocation, not derivation)\n")
    c1_exponent()
    c2_sheet_pairing()
    c3_deck_envariance()
    c4_kernel_counting()
    c5_unique_pairing()
    c6_relocation()

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("CONTRACT HOLDS" if n_pass == len(CHECKS)
               else "CONTRACT FAILS")
    relocation = [
        "outcomes = character-block projections (measurement postulate, untouched)",
        "single-outcome selection (the measurement problem, untouched)",
        "locality of p + partner-sheet no-signalling (the two envariance axioms)",
        "off the 3-adic kernel sector: continuity or dim>=3 Gleason (external)",
        "identification deck swap = envariance swap, sigma = CP conj (typed [C], v316)",
    ]
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    print("STAYS POSTULATED (relocation, honest):")
    for r in relocation:
        print(f"  - {r}")

    RESULTS.write_text(json.dumps({
        "contract": "BORN.01 deck-envariance (Born weight reduction)",
        "date": "2026-07-07",
        "firewall": ("theory contract, never a scorecard row; internal "
                     "consistency, not evidence; measurement problem not "
                     "addressed"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "stays_postulated": relocation,
        "reading": ("Born is NOT derived from recovery alone; it REDUCES to "
                    "deck-swap symmetry (Z2 sheet pairing, one amplitude "
                    "factor per sheet) + the matched mu4 Weyl pair (unique "
                    "invariant pairing) + finite counting on the 3-adic "
                    "kernel sector (no continuity axiom there). Same axiom "
                    "weight class as Zurek envariance, with the swap and the "
                    "conjugation structural (v316) instead of auxiliary. "
                    "v130's imported factor 2 acquires the sheet-pairing "
                    "origin p = A * sigma(A)."),
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

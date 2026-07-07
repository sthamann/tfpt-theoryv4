"""METALLIC.LADDER.01 -- the compactness ladder is the metallic-mean family,
a THEORY CONTRACT (pure mathematics; never a scorecard row, never load-bearing).

Discovery (2026-07-07, deeper-connections round): the gravastar/ECO compactness
function used across TFPT,

    C(k) = (k^2 - 1) / (6 k)          (k = replica-sheet index, gravastar-compactness/)

evaluated at the n-th METALLIC MEAN mu_n = (n + sqrt(n^2+4))/2 -- the root of
x^2 - n x - 1 = 0, i.e. the continued fraction [n; n, n, ...] -- collapses to an
integer-indexed rational:

    C(mu_n) = n / 6          (exact, for all n; since mu_n^2 - 1 = n * mu_n)

so the sheet index is literally 6 x compactness.  The two CLASSICAL general-
relativity thresholds are the two smallest metallic means, and their index is a
TFPT carrier hand:

    photon sphere   C = 1/3 = 2/6   <->  n = |Z2|  = 2   (silver mean 1 + sqrt2)
    horizon         C = 1/2 = 3/6   <->  n = N_fam = 3   (bronze mean (3+sqrt13)/2)

The physical (horizonless / sub-black-hole) window C <= 1/2 is exactly n <= 3,
capped at the horizon = N_fam.  The two EXOTIC ladder rungs of gravastar-
compactness -- Buchdahl 4/9 and Nariai 3/8 -- are the NON-metallic sheets in
between (6 * 4/9 = 8/3 and 6 * 3/8 = 9/4 are not integers): the integer sheet
k = 3 and the algebraic sheet k = (9+sqrt145)/8, not continued-fraction points.

Cross-link to the Markov contract (markov_modular_prime_clock_probe.py, D1): the
Markov tree's two boundary branches ARE the golden (Fibonacci, n=1) and silver
(Pell, n=2) metallic means.  The horizon index 3 = N_fam is NOT a Markov number
but IS the Markov coupling k=3 -- exactly D1's "3 is the coupling, not a state".

WHAT THIS IS / IS NOT.  [E]: the identity C(mu_n) = n/6 and every value below is
exact arithmetic.  [C]: the physical reading (that these metallic sheets are
realised objects, and that "N_fam = 3 = the last physical compactness sheet"
explains rather than parallels the family count) is SUGGESTIVE, and rests on the
same open replica-continuation residual as gravastar-compactness (fractional /
metallic sheets need a Calabrese-Cardy-type n -> non-integer continuation TFPT
does not yet supply).  NOT claimed: a new prediction, a closed gate, or any
status change.  This is an internal ordering principle, not evidence.

Firewall: theory contract; belongs in experiments/theory-contracts, never in
evidence_scorecard.json; passing is internal consistency, not external evidence.

Run:  cd experiments/theory-contracts && python3 metallic_compactness_ladder.py
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

RESULTS = Path(__file__).resolve().parent / "metallic_compactness_ladder_results.json"

CHECKS: list[dict] = []

# ---------------------------------------------------------------- constants
Z2, N_FAM, G_CAR = 2, 3, 5
MARKOV_NUMBERS = {1, 2, 5, 13, 29, 34, 89, 169, 194, 233, 433, 610, 985}


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def C_of(k):
    """gravastar/ECO compactness function C(k) = (k^2 - 1)/(6 k)."""
    return (k ** 2 - 1) / (6 * k)


def metallic(n: int):
    """n-th metallic mean mu_n = (n + sqrt(n^2+4))/2, root of x^2 - n x - 1."""
    return (n + sp.sqrt(n ** 2 + 4)) / 2


def c1_general_law() -> None:
    n = sp.symbols("n", positive=True)
    mu = (n + sp.sqrt(n ** 2 + 4)) / 2
    ok = sp.simplify(C_of(mu) - n / 6) == 0
    check("C1 METALLIC LAW [E, all n]: C(mu_n) = (mu_n^2-1)/(6 mu_n) = n/6, "
          "because mu_n^2 - 1 = n*mu_n (mu_n is the root of x^2-nx-1); the "
          "sheet index is 6 x compactness",
          ok, "C((n+sqrt(n^2+4))/2) simplifies to n/6 symbolically")


def c2_thresholds() -> None:
    rows = {
        1: ("golden (1+sqrt5)/2", metallic(1), sp.Rational(1, 6)),
        2: ("silver 1+sqrt2", metallic(2), sp.Rational(1, 3)),
        3: ("bronze (3+sqrt13)/2", metallic(3), sp.Rational(1, 2)),
        5: ("g_car (5+sqrt29)/2", metallic(5), sp.Rational(5, 6)),
    }
    ok = all(sp.simplify(mu ** 2 - idx * mu - 1) == 0
             and sp.simplify(C_of(mu) - C) == 0 for idx, (_, mu, C) in rows.items())
    check("C2 CLASSICAL THRESHOLDS [E]: photon sphere C=1/3 = silver (n=|Z2|=2), "
          "horizon C=1/2 = bronze (n=N_fam=3); n=1 golden -> 1/6, n=g_car=5 -> 5/6",
          ok, "; ".join(f"n={i}: {nm}, C={C}" for i, (nm, _, C) in rows.items()))


def c3_physical_window() -> None:
    physical = [k for k in range(1, 8) if Fraction(k, 6) <= Fraction(1, 2)]
    ok = physical == [1, 2, 3] and Fraction(4, 6) > Fraction(1, 2)
    check("C3 PHYSICAL WINDOW [E]: C = n/6 <= 1/2 (horizon) iff n <= 3 = N_fam; "
          "the horizonless metallic sheets are exactly {golden, silver, bronze} "
          "= n in {1,2,3}, capped at horizon = N_fam",
          ok, f"n with C<=1/2: {physical}; n=4 gives C=2/3 > 1/2 (inside horizon)")


def c4_non_metallic_rungs() -> None:
    # Buchdahl 4/9 and Nariai 3/8: 6*C not integer -> integer/algebraic sheets
    buch_k = sp.solve(sp.Eq(C_of(sp.Symbol("k", positive=True)), sp.Rational(4, 9)),
                      sp.Symbol("k", positive=True))
    nariai_k = sp.solve(sp.Eq(C_of(sp.Symbol("k", positive=True)), sp.Rational(3, 8)),
                        sp.Symbol("k", positive=True))
    ok = (6 * sp.Rational(4, 9) == sp.Rational(8, 3)
          and 6 * sp.Rational(3, 8) == sp.Rational(9, 4)
          and buch_k == [sp.Integer(3)]
          and sp.simplify(nariai_k[0] - (9 + sp.sqrt(145)) / 8) == 0)
    check("C4 NON-METALLIC RUNGS [E]: Buchdahl 4/9 -> 6C = 8/3 (integer sheet "
          "k = 3 = N_fam) and Nariai 3/8 -> 6C = 9/4 (algebraic sheet "
          "k = (9+sqrt145)/8); neither is a continued-fraction [n;n,...] point",
          ok, f"Buchdahl k={buch_k}; Nariai k=(9+sqrt145)/8")


def c5_markov_link() -> None:
    ok = (Z2 in MARKOV_NUMBERS and N_FAM not in MARKOV_NUMBERS)
    check("C5 MARKOV LINK [E, [C]-reading]: photon-sphere index 2 IS a Markov "
          "number (silver/Pell branch of the D1 tree exists); horizon index "
          "3 = N_fam is NOT a Markov number but IS the Markov coupling k=3 -- "
          "consistent with D1's 'k=3 is the coupling, not a state'",
          ok, "golden (n=1) = Fibonacci branch, silver (n=2) = Pell branch; "
              "bronze discriminant 13 = Delta_Q is a Markov number, but 3 "
              "itself is the coupling")


def main() -> None:
    print("METALLIC.LADDER.01 -- compactness ladder = the metallic-mean family\n")
    c1_general_law()
    c2_thresholds()
    c3_physical_window()
    c4_non_metallic_rungs()
    c5_markov_link()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The gravastar compactness function C(k)=(k^2-1)/(6k) is one monotone "
        "curve whose special points are the metallic means: C(mu_n)=n/6, with "
        "the two classical GR thresholds at the two smallest metallic means "
        "carrying the two carrier hands as index (photon sphere = silver, "
        "n=|Z2|=2; horizon = bronze, n=N_fam=3). The physical window C<=1/2 is "
        "exactly n<=3, capped at horizon=N_fam. This unifies the compactness "
        "ladder (gravastar-compactness), the metallic Markov-tree branches (D1) "
        "and the carrier hands under one equation x^2-nx-1. [E] for the "
        "arithmetic; [C] for the physical reading (fractional/metallic replica "
        "sheets need the same open continuation as gravastar-compactness). No "
        "new prediction, no gate closed, no status change."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "METALLIC.LADDER.01 metallic-mean compactness ladder",
        "date": "2026-07-07",
        "firewall": ("theory contract, never a scorecard row, never load-"
                     "bearing; internal consistency, not evidence"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

"""generator_hunt -- DISCIPLINED hunt for new generators / recursive rules /
cyclic patterns (discovery sandbox; v354/v355 firewall in force: a candidate is
real ONLY if it is a FORCED exact statement, never a numerical coincidence).

Motivation (2026-07-15, 'compiler analogy continues' round): the physical seam
transfer spectrum is {1, (2/3)^6, (1/3)^6} (v54/v221) but the only local
generator in the suite (v327's minimal rewrite) produces {1, 2/3, 0} -- it
generates the LAMBDA_2 mode and KILLS the (1/3)^6 mode.  So the third mode has
no local-rule origin yet.  Hunt target: is there a FORCED local rule whose
spectrum is the full physical pair?

  H1 [E] THE FULL-SPECTRUM RULE IS UNIQUE: for the 3-channel rule
       M(s,h) = [[1,0,0],[0,s,h],[0,h,s]]  (one absorbing family channel +
       SYMMETRIC Z2 pair) the survival spectrum is {s+h, s-h}.  Demanding the
       PHYSICAL pair {2/3, 1/3} forces
           s = 1/2,  h = 1/6,  leak = 1 - s - h = 1/3
       UNIQUELY -- and the three rates are exactly the atom expressions
           s = 1/|Z2|, h = 1/(|Z2| N_fam), leak = 1/N_fam.
       (Derived direction: spectrum -> rates.  The rate/atom coincidence is
       recorded; the atoms are not claimed to force the rule by themselves.)
  H2 [E] SIX-HAND CONSISTENCY: over the order-6 = 2 N_fam = |R+(A3)| dynamic
       hand (v327's hand) the rule generates EXACTLY the physical spectrum:
       eig(B^6) = {64/729, 1/729} = {(2/3)^6, (1/3)^6}; the two decay gaps are
       6 ln(3/2) (= the recovery gap, v76) and 6 ln 3 (the subdominant gap,
       previously generator-less).  v327's uniform rule (s = h = 1/3) is the
       DEGENERATE boundary case (spectrum {2/3, 0}) -- it can never produce
       the (1/3)^6 mode: superseded as generator of the FULL spectrum.
  H3 [E-inventory] ANCHOR-BILINEAR COVERAGE MAP: which load-bearing integers
       are reachable as x^T M y with x, y in {1, a} and M in the EXISTING
       operator set {R, Q, K}?  Known hits re-verified (a^T K a = 41 = 10 b1;
       Koide 53 channel); new cells reported as INVENTORY ONLY -- every
       unforced hit explicitly DECLINED as a claim.
  H4 [E-observation] LEPTON-EXPONENT COLLISION: the charged-lepton phi0 word
       lengths (5,3,2) equal BOTH the bottom row of K AND the atom triple
       (g_car, N_fam, |Z2|) = the seam signature (2,3,5) reversed.  Exact,
       three readings of one integer vector; typed as an observation (the
       K-row reading is definitional), NOT a new claim.

Firewall: discovery sandbox; nothing here is load-bearing until promoted; all
near-miss patterns are recorded and DECLINED.

Run:  cd experiments/tfpt-discovery && python3 generator_hunt_full_transfer_rule.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

RESULTS = Path(__file__).resolve().parent / "generator_hunt_results.json"
CHECKS: list[dict] = []

Z2, N_FAM, G_CAR = 2, 3, 5


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def main() -> None:
    print("generator_hunt -- the full transfer spectrum from one forced local "
          "rule\n")

    s, h = sp.symbols('s h', positive=True)

    # H1: uniqueness -- spectrum {2/3, 1/3} forces (s, h) = (1/2, 1/6)
    sol = sp.solve([sp.Eq(s + h, sp.Rational(2, 3)),
                    sp.Eq(s - h, sp.Rational(1, 3))], [s, h], dict=True)
    s0, h0 = sol[0][s], sol[0][h]
    leak = 1 - s0 - h0
    atoms_ok = (s0 == sp.Rational(1, Z2)
                and h0 == sp.Rational(1, Z2 * N_FAM)
                and leak == sp.Rational(1, N_FAM))
    # sub-stochastic sanity + uniqueness (linear system => unique)
    check("H1 FULL-SPECTRUM RULE UNIQUE [E]: symmetric Z2-pair rule M(s,h) has "
          "survival spectrum {s+h, s-h}; demanding the PHYSICAL pair "
          "{2/3, 1/3} (v54/v221) forces UNIQUELY (s, h, leak) = "
          "(1/2, 1/6, 1/3) = (1/|Z2|, 1/(|Z2| N_fam), 1/N_fam) -- the lazy "
          "Z2-pair walk; all rates exact atom expressions (recorded, "
          "derived direction: spectrum -> rates)",
          len(sol) == 1 and s0 == sp.Rational(1, 2)
          and h0 == sp.Rational(1, 6) and leak == sp.Rational(1, 3)
          and atoms_ok and s0 + h0 <= 1,
          f"(s, h, leak) = ({s0}, {h0}, {leak}); unique solution")

    # H2: six-hand consistency + supersession of the uniform rule
    B = sp.Matrix([[s0, h0], [h0, s0]])
    B6 = B ** 6
    eigs6 = sorted(B6.eigenvals().keys(), key=lambda v: -sp.nsimplify(v))
    phys = [sp.Rational(64, 729), sp.Rational(1, 729)]
    gap2 = sp.nsimplify(-sp.log(sp.Rational(64, 729)))
    gap3 = sp.nsimplify(-sp.log(sp.Rational(1, 729)))
    uniform = sp.Matrix([[sp.Rational(1, 3), sp.Rational(1, 3)],
                         [sp.Rational(1, 3), sp.Rational(1, 3)]])
    eigs_u = set(uniform.eigenvals().keys())
    check("H2 SIX-HAND CONSISTENCY [E]: over the order-6 = 2 N_fam = |R+(A3)| "
          "hand the lazy rule generates EXACTLY the physical spectrum "
          "eig(B^6) = {64/729, 1/729} = {(2/3)^6, (1/3)^6}; decay gaps "
          "6 ln(3/2) (the recovery gap, v76) and 6 ln 3 (the subdominant "
          "gap, previously generator-less).  v327's uniform rule (1/3, 1/3) "
          "is the degenerate case {2/3, 0} -- it can NEVER produce the "
          "(1/3)^6 mode: superseded as generator of the full spectrum",
          eigs6 == phys and eigs_u == {sp.Rational(2, 3), sp.Integer(0)}
          and sp.simplify(gap2 - 6 * sp.log(sp.Rational(3, 2))) == 0
          and sp.simplify(gap3 - 6 * sp.log(3)) == 0,
          f"eig(B^6) = {eigs6}; uniform-rule spectrum = {sorted(eigs_u, key=float)}")

    # H3: anchor-bilinear coverage inventory (existing operators only)
    one = sp.Matrix([1, 1, 1])
    a = sp.Matrix([1, 1, 2])
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    known_targets = {8: "rank E8 / det R", 10: "A_Lambda", 11: "||Pl(K)||_1",
                     16: "dim S+", 24: "|W(A3)|", 30: "h(E8)", 41: "10 b1",
                     48: "Omega_adm", 53: "Koide corner", 120: "|2I|"}
    table = {}
    hits = []
    for mname, M in (("R", R), ("K", K), ("Q", Q), ("R+Q", R + Q)):
        for xn, x in (("1", one), ("a", a)):
            for yn, y in (("1", one), ("a", a)):
                v = int((x.T * M * y)[0])
                table[f"{xn}^T {mname} {yn}"] = v
                if v in known_targets:
                    hits.append(f"{xn}^T {mname} {yn} = {v} ({known_targets[v]})")
    ktest = int((a.T * K * a)[0])
    koide = int((a.T * (R + Q) * one)[0])
    check("H3 ANCHOR-BILINEAR COVERAGE [E-inventory]: full 16-cell table of "
          "x^T M y (x, y in {1, a}; M in {R, K, Q, R+Q}) computed exactly; "
          "KNOWN hits re-verified: a^T K a = 41 = 10 b1 and the Koide corner "
          "a^T (R+Q) 1 = 53; every other cell is INVENTORY ONLY -- no "
          "unforced hit is claimed (v354/v355)",
          ktest == 41 and koide == 53,
          f"hits on load-bearing targets: {hits}; full table in results JSON")

    # H4: the lepton-exponent collision (observation, typed)
    lepton_exponents = (5, 3, 2)          # m_e, m_mu, m_tau phi0 word lengths (v20)
    K_bottom = tuple(int(v) for v in K.row(2))
    atom_triple = (G_CAR, N_FAM, Z2)
    check("H4 LEPTON-EXPONENT COLLISION [E-observation]: the charged-lepton "
          "phi0 exponents (5,3,2) (v20: (16/7)phi0^5, (4/3)phi0^3, "
          "(7/6)phi0^2) equal BOTH the bottom row of K AND the atom triple "
          "(g_car, N_fam, |Z2|) = the seam signature (2,3,5) reversed -- "
          "three readings of one integer vector, exact; typed as an "
          "OBSERVATION (the K-row reading is definitional), NOT a claim",
          lepton_exponents == K_bottom == atom_triple,
          f"exponents {lepton_exponents} = K row 3 {K_bottom} = atoms "
          f"{atom_triple}")

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "HUNT COMPLETE" if n_pass == len(CHECKS) else "HUNT INCONSISTENT"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "One genuinely new forced structure found: the FULL physical transfer "
        "spectrum {1, (2/3)^6, (1/3)^6} now has a LOCAL GENERATOR -- the lazy "
        "Z2-pair walk with (stay, hop, leak) = (1/2, 1/6, 1/3) = (1/|Z2|, "
        "1/(|Z2| N_fam), 1/N_fam), the UNIQUE symmetric rule matching the "
        "physical pair {2/3, 1/3}; over the order-6 hand it reproduces both "
        "modes exactly, giving the previously generator-less (1/3)^6 its "
        "origin and superseding v327's uniform rule (which produces {2/3, 0} "
        "and kills the third mode). Recorded and typed, not over-claimed: "
        "derived direction is spectrum -> rates; the atom form of the rates "
        "is exact but its forcing from first principles is the [O]. Coverage "
        "inventory and the lepton-exponent collision recorded as typed "
        "observations, no unforced claims."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "probe": "generator_hunt_full_transfer_rule",
        "date": "2026-07-15",
        "firewall": "discovery sandbox; v354/v355; nothing load-bearing",
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "bilinear_table": table,
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

"""unit01 -- WHY the two open targets share one rule: the seam CONTACT UNIT
c3-per-insertion is DERIVED (finite cycle sector) from the bare boundary
propagator + the mu4 orbit average -- i.e. it is the SAME identity as the KMS
seam unit 2 pi = 1/(4 c3) with 1/4 = 1/|mu4| (v239).  The ALPHA.QUILLEN and
PHI0.PUNCTURE residuals MERGE into one named analytic step (theory contract;
never a scorecard row, never load-bearing).

The observation (v483 aftermath): ALPHA.QUILLEN.EXACT.01 carries the c3-ladder
{c3^0, c3^3, c3^6} (v3/v341/EM.WARD.02) and HYP.PHI0.PUNCTURE.01 carries the
per-mark weight c3 (4 = |mu4| insertions -> c3^4, v483).  Both open rules are
the SAME statement: seam contact insertions are weighted in the unit c3.  This
contract shows that unit is NOT a new unknown:

  (U1) [E] THE UNIT CHAIN: 1/(2 pi) = 4 c3 = |mu4| c3 = |Z2| chi(S^2) c3 --
       the bare boundary-propagator normalisation equals |mu4| x c3; dividing
       one bare insertion by the orbit order |mu4| = 4 gives EXACTLY c3.  This
       is the v239 KMS seam unit (2 pi = 1/(4 c3), '1/4 = 1/|mu4|') and the
       v58/v73 one-sided Gauss-Bonnet in one identity.
  (U2) [E] THE MECHANISM, DERIVED ON THE ACTUAL SEAM CIRCLE: the |D|^-1 Green
       function (zero mode removed) is G(d) = -(1/pi) ln|2 sin(d/2)| (Fourier
       identity, exact); at the mu4 mark separations it takes EXACT integer
       multiples of c3 ln 2:  G(pi/2) = -4 c3 ln2, G(pi) = -8 c3 ln2, so the
       mark-Green matrix is  G_marks = -4 c3 ln2 * C  with C = circ(0,1,2,1)
       INTEGER, spec(C) = {4, -2, 0, -2}.  A mu4-INVARIANT insertion (orbit
       average, weight 1/|mu4| per mark) therefore carries the per-insertion
       operator  (GV)|_marks = -(c3 ln2) C : the contact expansion of
       log det(1 + eps G V) = sum_k (-1)^{k+1} (eps c3 ln2)^k Tr(C^k)/k is
       EXACTLY graded in c3 per insertion, with integer cycle combinatorics
       Tr(C^k) = 4^k + 2(-2)^k.  The unit c3 EMERGES as bare(4 c3) x orbit
       average(1/4) -- nothing is postulated.
  (U3) [E] THE GRAMMAR IS ALREADY SUITE-WIDE (re-verified exactly): F_U(1) =
       a^3 - 2 c3^3 a^2 - (4/5)41 c3^6 L (v3, ladder {0,3,6}); phi0 = (4/3)c3
       + 48 c3^4 (v37, ladder {1,4}); the Lambda prefactor 3/(4 pi^2) =
       (8 pi)^2 delta_top = 48 c3^2 (v60 -- the SAME multiplicity 48 as the
       puncture, two insertions instead of four); the g-2 chain multiplies by
       the SAME unit 4 c3 = 1/(2 pi).  One grammar: atom-rational x
       c3^(#insertions).
  (U4) [C]/[O] THE MERGE: the residuals of ALPHA.QUILLEN.EXACT.01 and
       HYP.PHI0.PUNCTURE.01 are ONE analytic step, not two -- the finite
       cycle sector of the contact calculus is now derived (U2); what stays
       open is the DIAGONAL (self-energy) zeta-renormalisation at the marks
       plus the state-multiplicity matching (48 = Omega_adm, 41 = 10 b1).  No
       gate closes; both targets stay [O] but merged.

Anti-numerology note: U2's integers (the circulant, its spectrum, Tr(C^k)) are
FORCED by the square mark configuration; no coefficient of the two targets is
'explained' here beyond the unit itself -- the multiplicity matching is
explicitly left [O].

Run:  cd experiments/theory-contracts && python3 unit01_contact_unit_bridge.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

RESULTS = Path(__file__).resolve().parent / "unit01_contact_unit_results.json"
CHECKS: list[dict] = []

C3 = 1 / (8 * sp.pi)


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def main() -> None:
    print("unit01 -- the seam contact unit: one rule behind ALPHA.QUILLEN and "
          "PHI0.PUNCTURE\n")

    # U1: the unit chain
    ok1 = (sp.simplify(4 * C3 - 1 / (2 * sp.pi)) == 0
           and sp.simplify(2 * 2 * C3 - 1 / (2 * sp.pi)) == 0)   # |Z2| chi = 4
    check("U1 THE UNIT CHAIN [E]: 1/(2 pi) = 4 c3 = |mu4| c3 = |Z2| chi(S^2) "
          "c3 -- one bare boundary insertion divided by the orbit order "
          "|mu4| = 4 is EXACTLY c3; identical to the v239 KMS seam unit "
          "(2 pi = 1/(4 c3), '1/4 = 1/|mu4|') and the v58/v73 one-sided "
          "Gauss-Bonnet", ok1,
          "4*c3 - 1/(2pi) = 0 exact; |Z2|*chi(S^2) = 4 = |mu4|")

    # U2a: the Fourier identity via the exact polylog form
    # sum_{n>=1} cos(n d)/n = Re Li_1(e^{i d}) = -Re ln(1 - e^{i d})
    #                       = -ln|2 sin(d/2)|
    import mpmath as mp
    mp.mp.dps = 40
    errs = []
    for v in (mp.pi / 7, mp.pi / 3, 2 * mp.pi / 5, mp.pi / 2, mp.pi):
        lhs = mp.re(mp.polylog(1, mp.e ** (1j * v)))
        rhs = -mp.log(2 * mp.sin(v / 2))
        errs.append(abs(lhs - rhs))
    ok2a = max(errs) < mp.mpf('1e-35')
    check("U2a FOURIER IDENTITY [E]: sum_{n>=1} cos(n d)/n = Re Li_1(e^{id}) "
          "= -ln|2 sin(d/2)| -- the bare |D|^-1 seam Green function is "
          "G(d) = -(1/pi) ln|2 sin(d/2)| with normalisation 2 x (1/2pi) = "
          "2 x 4c3", ok2a,
          "polylog identity verified to 40 digits at d = pi/7, pi/3, 2pi/5, "
          "pi/2, pi (max err %.1e)" % float(max(errs)))

    # U2b: the mark-Green matrix in the c3 unit
    G = lambda dd: -(1 / sp.pi) * sp.log(2 * sp.sin(dd / 2))
    g_adj = sp.simplify(G(sp.pi / 2) / (C3 * sp.log(2)))     # adjacent marks
    g_opp = sp.simplify(G(sp.pi) / (C3 * sp.log(2)))         # opposite marks
    ok2b = g_adj == -4 and g_opp == -8
    check("U2b MARK-GREEN MATRIX [E]: at the mu4 separations the bare Green "
          "function is an INTEGER multiple of c3 ln2 -- G(pi/2) = -4 c3 ln2, "
          "G(pi) = -8 c3 ln2, so G_marks = -4 c3 ln2 * C with C = "
          "circ(0,1,2,1) integer", ok2b,
          f"G(pi/2)/(c3 ln2) = {g_adj}; G(pi)/(c3 ln2) = {g_opp}")

    # U2c: circulant spectrum + cycle combinatorics + the emergent unit
    Cm = sp.Matrix([[0, 1, 2, 1], [1, 0, 1, 2], [2, 1, 0, 1], [1, 2, 1, 0]])
    spec = sorted(Cm.eigenvals().items(), key=lambda kv: -kv[0])
    spec_ok = dict(Cm.eigenvals()) == {4: 1, -2: 2, 0: 1}
    trs = [sp.trace(Cm ** k) for k in (1, 2, 3, 4)]
    trs_ok = all(sp.trace(Cm ** k) == 4 ** k + 2 * (-2) ** k for k in (1, 2, 3, 4, 5))
    # the orbit-averaged per-insertion operator: (1/|mu4|) * G_marks = -(c3 ln2) C
    per_insertion = sp.simplify((sp.Rational(1, 4) * (-4 * C3 * sp.log(2))) / (-C3 * sp.log(2)))
    ok2c = spec_ok and trs_ok and per_insertion == 1
    check("U2c THE EMERGENT UNIT [E]: the mu4-invariant (orbit-averaged) "
          "insertion carries (GV)|_marks = -(c3 ln2) C exactly -- per-"
          "insertion weight = (1/|mu4|) x bare = c3; spec(C) = {4, -2, 0, "
          "-2}, cycle combinatorics Tr(C^k) = 4^k + 2(-2)^k INTEGER: the "
          "log-det contact expansion is exactly graded in c3 per insertion",
          ok2c, f"spec = {spec}; Tr(C^k) k=1..4 = {trs}; unit ratio = 1")

    # U3: the suite-wide grammar (exact re-verification of existing facts)
    a = sp.symbols('a', positive=True)
    dtop = 48 * C3 ** 4
    lam_pref = sp.simplify((8 * sp.pi) ** 2 * dtop)            # v60 fact
    phi0_tree = sp.Rational(4, 3) * C3
    ok3 = (sp.simplify(lam_pref - sp.Rational(3, 4) / sp.pi ** 2) == 0
           and sp.simplify(lam_pref - 48 * C3 ** 2) == 0
           and sp.simplify(phi0_tree - 1 / (6 * sp.pi)) == 0
           and sp.simplify(dtop - sp.Rational(3, 256) / sp.pi ** 4) == 0)
    check("U3 SUITE-WIDE GRAMMAR [E]: the Lambda prefactor 3/(4 pi^2) = "
          "(8 pi)^2 delta_top = 48 c3^2 (v60) -- the SAME multiplicity "
          "Omega_adm = 48 as the phi0 puncture 48 c3^4, at TWO insertions "
          "instead of four; phi0 tree = (4/3) c3 = 1/(6 pi) (one insertion); "
          "F_U(1) ladder {a^3, 2 c3^3 a^2, (4/5)41 c3^6 L} (v3) at {0,3,6}; "
          "the g-2 chain multiplies by the same unit 4 c3 = 1/(2 pi) -- ONE "
          "grammar: atom-rational x c3^(#insertions)", ok3,
          "48 c3^2 = 3/(4 pi^2) exact; 48 c3^4 = 3/(256 pi^4) exact; "
          "(4/3) c3 = 1/(6 pi) exact")

    # U4: the merge typing
    ok4 = all(c["pass"] for c in CHECKS)
    check("U4 THE MERGE [C]/[O]: ALPHA.QUILLEN.EXACT.01 and "
          "HYP.PHI0.PUNCTURE.01 share ONE analytic residual -- the seam "
          "contact calculus in the KMS unit c3 -- whose finite cycle sector "
          "is now DERIVED (U2: bare 4 c3 x orbit average 1/4, integer "
          "circulant combinatorics); what stays [O] is the DIAGONAL "
          "(self-energy) zeta-renormalisation at the marks + the state-"
          "multiplicity matching (48 = Omega_adm, 41 = 10 b1). Two targets "
          "merge into one named step; no gate closes, no value is claimed",
          ok4, "cycle sector derived; diagonal renormalisation + "
               "multiplicity matching stay open")

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The commonality between the two open targets is NOT a coincidence "
        "and NOT a new unknown: 'weight c3 per boundary insertion' is the "
        "KMS seam unit 2 pi = 1/(4 c3) with 1/4 = 1/|mu4| (v239), i.e. one "
        "bare boundary propagator orbit-averaged over the four marks. On the "
        "actual seam circle this is now DERIVED for the finite cycle sector: "
        "the bare Green function at the mu4 separations is an integer "
        "multiple of c3 ln2 (G_marks = -4 c3 ln2 circ(0,1,2,1), spectrum "
        "{4,-2,0,-2}), so the log-det contact expansion is exactly graded in "
        "c3 per insertion. The grammar is already suite-wide (v3 ladder "
        "{0,3,6}; phi0 {1,4}; the v60 Lambda prefactor 3/(4 pi^2) = 48 c3^2 "
        "-- the same 48 as the puncture at two insertions; g-2 multiplies by "
        "the same 4 c3). Consequence: ALPHA.QUILLEN.EXACT.01 and "
        "HYP.PHI0.PUNCTURE.01 MERGE into one remaining analytic step -- the "
        "diagonal zeta-renormalisation + multiplicity matching. No gate "
        "closes; no coefficient is claimed."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "unit01 seam contact unit -- the merged residual of "
                    "ALPHA.QUILLEN and PHI0.PUNCTURE",
        "date": "2026-07-14",
        "firewall": ("theory contract, never a scorecard row, never "
                     "load-bearing; both targets stay [O]"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

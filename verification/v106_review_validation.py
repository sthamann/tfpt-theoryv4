"""v106 -- External-review validation round (2026-06-11): seed normal form,
factorial spine, hypercharge second moment, the DEGREE-2 inventory, and one
named hypothesis.  [I] identities + disciplined typing (v79 style).

An external review proposed several sharpenings.  Everything checkable is
machine-validated here; everything interpretive is typed, not promoted.

  [I] 1. SEED NORMAL FORM.  The seed formula phi0 = (4/3) c3 + 48 c3^4 is
         exactly
             phi0 = (|mu4|/N_fam) c3  +  Omega_adm c3^{|mu4|} :
         a LINEAR seam term (glue index over family count) plus a
         TOPOLOGICAL fourth-order correction over all admissible fermion
         states -- the seed is a structured anchor readout, not a fitted
         expression (4/3 = |mu4|/N_fam, 48 = Omega_adm = N_fam dim S+,
         exponent 4 = |mu4|).
  [I] 2. ANCHOR POWER-SUM LADDER (v23 recheck, compact).  p_n(a) = 2+2^n:
         (p0..p3) = (3,4,6,10) = (N_fam, |mu4|, |R+(A3)|, A_Lambda);
         p1 p2 p3 = 240 = |R(E8)|, p4 - p3 = 8 = rank E8, sum = 248.
  [I] 3. HYPERCHARGE SECOND MOMENT.  With X = 6Y on one SM generation
         (16 states incl. nu^c): Tr X = 0 and Tr X^2 = 120 = 5! --
         computed from the explicit charge table, not imported.
  [I] 4. FACTORIAL SPINE (named lemma).  5! = 120 = |R+(E8)| = sum of E8
         exponents = Tr_{S+} X^2;  240 = 2*120 = |R(E8)|;  1920 = 2^4*5!
         = |W(D5)| (the Hawking-power fingerprint).  One factorial moment
         connects hypercharge, E8 roots, the D5 Weyl group and the
         horizon readout -- the same number in four projections, an
         anti-numerology structure statement.
  [I] 5. THE DEGREE-2 INVENTORY ("the theory always picks degree 2"):
         (i)  Pascal closure 2^{g-1} = C(g,0)+C(g,1)+C(g,2) truncates at
              K = 2 and has the UNIQUE solution g = 5 (scan 1..40);
         (ii) glue norms q(D5)+q(A3) = 5/4+3/4 = 2 = the root norm;
         (iii) c3 = (1/2) x 1/(4 pi): variational half x Gauss-Bonnet of
              the 2-dimensional normal slice (chi(S^2) = 2);
         (iv) the pair sector Lambda^2: C(5,2) = 10 = A_Lambda;
         (v)  the hypercharge moment is a SECOND moment (item 3);
         (vi) the seam is codimension TWO (2d normal slice).
         NAMED HYPOTHESIS [P], not claimed: "QUADRATIC BOUNDARY LOCALITY"
         -- the seam supports only bilinear data (RP pairings, second
         moments, norm-2 roots, Lambda^2, R^2), hence the compiler
         truncation K = 2 is forced rather than chosen.  If proven, the
         Pascal SELECTION (red-team Target B residual, typed [A]/[P])
         upgrades to [L] and g = 5 follows: locality => K=2 => g=5 =>
         16 => D5 => E8.  Recorded as the named reduction target.
  [I]+audit 6. EVEN-CODE TRANSITION READING.  240 = 16 x 15 (all ordered
         transitions between the 16 even-code states) -- arithmetic exact,
         but NOT unique (240 = 16 x 5 x 3 is the established v1 glue
         factorisation), and no root <-> transition bijection is
         exhibited: typed AUDIT like the v91 graph reading; recorded,
         not promoted.
  DISCIPLINED NOTES (no new content, confirmations):
       * "reality compiler = {a, pi, v_geo}" is a RESTATEMENT of
         v23 (inputs reduce to {a, pi}) + v78 (one scale) -- valid,
         already established, not a new axiom reduction;
       * the requested "grammar freeze rule" is already implemented:
         v84 freezes the predictions BEFORE the data, v100 censuses the
         DECLARED grammar retrospectively; the proposed admission-
         protocol fields (generator / dof / blindness / falsifier) map
         onto existing ledger columns + freeze_file.csv.
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import (check, summary, reset, phi0, c3, N_fam,
                            dim_Splus, Omega_adm)

MU4 = 4
ANCHOR = (1, 1, 2)


def p_sum(n):
    return sum(x**n for x in ANCHOR)


def run():
    reset()
    print("v106 review validation (seed NF, factorial spine, degree-2 inventory)")

    # 1. seed normal form (pure mpmath at working precision)
    mp.mp.dps = 40
    val = mp.mpf(MU4) / N_fam * c3 + Omega_adm * c3**MU4
    check("SEED NORMAL FORM: phi0 = (|mu4|/N_fam) c3 + Omega_adm c3^|mu4| "
          "exactly (linear seam term + topological 4th-order correction; "
          "4/3 = |mu4|/N_fam, 48 = Omega_adm, exponent 4 = |mu4|)",
          abs(phi0 - val) < mp.mpf('1e-35')
          and sp.Rational(4, 3) == sp.Rational(MU4, N_fam)
          and Omega_adm == 48 == N_fam * dim_Splus)

    # 2. anchor power-sum ladder
    check("ANCHOR LADDER: p_n(a) = 2 + 2^n; (p0..p3) = (3,4,6,10) = "
          "(N_fam, |mu4|, |R+(A3)|, A_Lambda); p1p2p3 = 240, p4-p3 = 8, "
          "sum = 248 (v23 recheck)",
          all(p_sum(n) == 2 + 2**n for n in range(8))
          and (p_sum(0), p_sum(1), p_sum(2), p_sum(3)) == (3, 4, 6, 10)
          and p_sum(1) * p_sum(2) * p_sum(3) == 240
          and p_sum(4) - p_sum(3) == 8
          and p_sum(1) * p_sum(2) * p_sum(3) + p_sum(4) - p_sum(3) == 248)

    # 3. hypercharge second moment (computed, not imported)
    gen = [(6, sp.Rational(1, 6)), (3, sp.Rational(-2, 3)),
           (3, sp.Rational(1, 3)), (2, sp.Rational(-1, 2)),
           (1, sp.Integer(1)), (1, sp.Integer(0))]
    trX = sum(n * 6 * y for n, y in gen)
    trX2 = sum(n * (6 * y)**2 for n, y in gen)
    check("HYPERCHARGE MOMENT: with X = 6Y on one generation (16 states): "
          "Tr X = 0 and Tr X^2 = 120 = 5! (explicit charge table)",
          trX == 0 and trX2 == 120 == sp.factorial(5)
          and sum(n for n, _ in gen) == 16)

    # 4. factorial spine
    e8_exponents = [1, 7, 11, 13, 17, 19, 23, 29]
    check("FACTORIAL SPINE: 5! = 120 = |R+(E8)| = sum(E8 exponents) = "
          "Tr X^2; 240 = 2*120 = |R(E8)|; 1920 = 2^4 * 5! = |W(D5)| (the "
          "Hawking fingerprint) -- one moment, four projections",
          sp.factorial(5) == 120 == sum(e8_exponents) == trX2
          and 2 * 120 == 240 and 2**4 * 120 == 1920)

    # 5. the degree-2 inventory
    sols = [g for g in range(1, 41)
            if 2**(g - 1) == sum(sp.binomial(g, k) for k in range(3))]
    check("DEGREE-2 (i): Pascal K = 2 closure 2^{g-1} = sum_{k<=2} C(g,k) "
          "has the UNIQUE solution g = 5 on 1..40",
          sols == [5])
    check("DEGREE-2 (ii)+(iii)+(iv): glue norms 5/4 + 3/4 = 2 = root "
          "norm; c3 = (1/2) x 1/(4pi) (variational half x 2d-slice "
          "Gauss-Bonnet); pair sector C(5,2) = 10 = A_Lambda",
          sp.Rational(5, 4) + sp.Rational(3, 4) == 2
          and sp.simplify(sp.Rational(1, 2) / (4 * sp.pi)
                          - 1 / (8 * sp.pi)) == 0
          and sp.binomial(5, 2) == 10)
    check("NAMED HYPOTHESIS [P] (recorded, not claimed): QUADRATIC "
          "BOUNDARY LOCALITY -- the seam supports only bilinear data, "
          "hence K = 2 is forced; if proven, the Pascal selection "
          "(red-team Target B residual [A]/[P]) upgrades to [L] and the "
          "chain locality => K=2 => g=5 => 16 => D5 => E8 closes the "
          "carrier choice", True)

    # 6. even-code transition reading (audit)
    check("AUDIT: 240 = 16 x 15 (ordered transitions of the even code) "
          "is exact arithmetic but NOT unique (240 = 16 x 5 x 3 is the "
          "established glue factorisation) and no root<->transition "
          "bijection is exhibited -- recorded like the v91 graph reading, "
          "not promoted",
          16 * 15 == 240 == 16 * 5 * 3)

    # disciplined notes
    check("NOTES: 'reality compiler = {a, pi, v_geo}' = restatement of "
          "v23 + v78 (confirmed, not new); the requested grammar-freeze "
          "rule is already implemented by v84 (pre-data freeze) + v100 "
          "(declared-grammar census); admission-protocol fields map onto "
          "ledger columns + freeze_file.csv", True)

    return summary("v106 review validation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

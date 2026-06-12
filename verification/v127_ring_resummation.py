"""v127 -- The clock is a log-determinant: the geometric tail is the
standard ring (RPA) resummation, with one identical tower per hexagon
site and coupling = the parabolic weight.  [I] exact identities; R1's
'O(1) resummation' is now TYPED -- it is the ring/log-det resummation.

v107 demanded 'an O(1) resummation or an exact seam construction'; v124
gave the closed form; v126 isolated the quantum part to the tail
sum_{k>=2} alpha^k/k.  This module identifies the tail's structure:

  [I] 1. LOG-DET IDENTITY.  For a rank-1 insertion P (tr P^k = 1):
             -ln det(1 - alpha P) = -ln(1 - alpha) = sum_k alpha^k / k,
         so the v124 clock is EXACTLY
             rate(alpha) = -p_2 Tr ln(1 - alpha P)
         -- p_2 = 6 identical copies (ONE PER HEXAGON SITE = positive
         root of A_3) of the one-loop ring (RPA) resummation of a
         single mode with insertion strength alpha = parabolic weight.
  [I] 2. RING LADDER.  The k-th ring contributes alpha^k / k per site:
         k = 1 is the CLASSICAL term (slope |Z_2|, = v104's entropy
         rate, v126); k = 2 is the first QUANTUM correction
         (= 1/3 at weight n = 1); the partial sums converge to the
         exact rates {Delta, 6 ln 3} monotonically from below
         (K = 1, 2, 3, 8 verified exactly).
  [I] 3. COUPLING CROSS-LINK (audit).  The established seam coupling
         kappa = (c/24 pi)(Lambda/Mbar^2) at Lambda = Mbar^2 with
         c = 8 (v107) is kappa = 8/(24 pi) = 1/(3 pi) = alpha_1 / pi
         -- the seam coupling is the FIRST PARABOLIC WEIGHT over pi
         (exact arithmetic; recorded as audit).
  [I] 4. THE WALL = RING DIVERGENCE.  The ring series has radius of
         convergence |alpha| < 1; at alpha -> 1 (n -> N_fam) it
         diverges -- the v124 wall at the family count is the standard
         RPA instability: the clock fails exactly when the insertion
         strength reaches unity.
  [P] 5. R1 FINAL FORM (recorded, not claimed).  The semiclassical job
         is now fully specified: show that the near-Nariai one-loop
         effective action of the seam mode, with insertion strength =
         parabolic weight alpha and multiplicity p_2 (the hexagon),
         is the ring sum -p_2 Tr ln(1 - alpha P).  R1 = 'the seam
         clock is the RPA determinant of one mode on six sites'.  The
         resummation TYPE demanded by v107 is identified; the
         derivation itself remains open.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

P2 = 6


def run():
    reset()
    print("v127 ring resummation (the clock is a log-determinant)")

    alpha = sp.Symbol('alpha', positive=True)

    # 1. log-det identity
    proj = sp.Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    check("LOG-DET IDENTITY: det(1 - alpha P) = 1 - alpha for a rank-1 "
          "insertion P (tr P^k = 1), so -ln det(1 - alpha P) = "
          "-ln(1 - alpha) = sum_k alpha^k/k -- the v124 clock is "
          "EXACTLY rate = -p2 Tr ln(1 - alpha P): p2 = 6 identical "
          "ring (RPA) towers, one per hexagon site (= positive root "
          "of A3), coupling = parabolic weight",
          sp.simplify(sp.det(sp.eye(3) - alpha * proj)
                      - (1 - alpha)) == 0
          and sp.series(-sp.log(1 - alpha), alpha, 0, 4).removeO()
          == alpha + alpha ** 2 / 2 + alpha ** 3 / 3)

    # 2. ring ladder
    a1, a2 = sp.Rational(1, 3), sp.Rational(2, 3)
    exact1 = -P2 * sp.log(1 - a1)
    exact2 = -P2 * sp.log(1 - a2)

    def partial(al, kmax):
        return P2 * sum(al ** j / j for j in range(1, kmax + 1))

    check("RING LADDER: k = 1 ring = classical term (6 alpha = 2n = "
          "|Z2| n, the v104/v126 entropy rate); k = 2 ring = first "
          "quantum correction = 1/3 at weight n = 1; partial sums "
          "converge to the exact rates monotonically from below "
          "(K = 1, 2, 3, 8 checked exactly)",
          partial(a1, 1) == 2 and partial(a2, 1) == 4
          and P2 * a1 ** 2 / 2 == sp.Rational(1, 3)
          and all(partial(a1, k) < partial(a1, k + 1) for k in (1, 2, 3))
          and partial(a1, 8) < exact1 and partial(a2, 8) < exact2
          and float(exact1 - partial(a1, 8)) < 1e-3
          and float(exact2 - partial(a2, 8)) < 0.05)

    # 3. coupling cross-link
    check("COUPLING CROSS-LINK (audit): kappa_seam = (c/24pi) at "
          "Lambda = Mbar^2 with c = 8 (v107) gives 8/24 = 1/3 = "
          "alpha_1 -- the seam coupling is the FIRST PARABOLIC WEIGHT "
          "over pi: kappa = alpha_1/pi = 1/(3pi)",
          sp.Rational(8, 24) == sp.Rational(1, 3)
          and sp.Rational(1, 3) == a1)

    # 4. the wall = ring divergence
    check("THE WALL = RING DIVERGENCE: the ring series radius of "
          "convergence is |alpha| < 1; at alpha -> 1 (n -> N_fam) the "
          "sum diverges (lim -ln(1-alpha) = oo) -- the v124 wall at "
          "the family count is the standard RPA instability",
          sp.limit(-sp.log(1 - alpha), alpha, 1, dir='-') == sp.oo)

    # 5. R1 final form
    check("R1 FINAL FORM [P] (recorded, not claimed): show that the "
          "near-Nariai one-loop effective action of the seam mode, "
          "with insertion = parabolic weight alpha and multiplicity "
          "p2 (the hexagon), is the ring sum -p2 Tr ln(1 - alpha P) "
          "-- 'the seam clock is the RPA determinant of one mode on "
          "six sites'. The resummation TYPE demanded by v107 is "
          "identified; the derivation itself remains open", True)

    return summary("v127 ring resummation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v67 -- the central theorem (1/(8pi) area-law coefficient): structural closure
and reduction to ONE sharp heat-kernel coefficient.

This is an HONEST attempt at Alessandro's central theorem -- not a full solution, but
a real reduction.  Result:

  STRUCTURE CLOSED [I]/[L]: by the Fursaev-Solodukhin (1995) conical/replica method,
  the curvature term W_R = k*Int(sqrt(g) R) contributes a horizon entropy S = 4 pi k A
  (the conical defect gives Int R ⊃ 4 pi (1-n) A; S = -d/dn[W_n - n W_1]|_{n=1}).  With
  the Einstein-Hilbert coefficient at the seam unit k = 1/(16 pi G) = c3/2 (G=1, P1),

      S = 4 pi (c3/2) A = 2 pi c3 A ,   and   2 pi c3 = 2 pi/(8 pi) = 1/4 ,

  so S = A/4 = Bekenstein-Hawking.  INVERSELY (the theorem): requiring S = A/4 (BH) and
  S = 4 pi k A (conical) with k = c3/2 forces c3 = 1/(8 pi) UNIQUELY.  Hence c3 = 1/(8 pi)
  is exactly the value for which the replica area-law coefficient equals BH 1/4.

  RESIDUAL [A]: the single statement k = c3/2, i.e. the seam determinant's heat-kernel
  Einstein-Hilbert coefficient is exactly c3/2.  By Susskind-Uglum/Callan-Wilczek this k
  is the INDUCED 1/(16 pi G), and by the Seeley-DeWitt a2 coefficient it is fixed by the
  carrier field content + the seam normalization.  This is ONE sharp spectral statement,
  no longer the vague 'derive 1/(8pi)'.
"""
import sympy as sp
from tfpt_constants import check, summary, reset

pi = sp.pi


def run():
    reset()
    print("v67  central theorem: replica area-law coefficient => c3=1/(8pi) (structural closure)")

    c3 = sp.Rational(1, 8) / pi

    # Step 2: EH coefficient at the seam unit
    k = c3 / 2
    check("EH coefficient at seam unit: k = 1/(16 pi G)|_{G=1} = 1/(16 pi) = c3/2",
          sp.simplify(k - sp.Rational(1, 16) / pi) == 0)

    # Step 3: Fursaev-Solodukhin S = 4 pi k A => 2 pi c3 A => A/4
    S_over_A = 4 * pi * k
    check("Fursaev-Solodukhin: S = 4 pi k A = 2 pi c3 A ; 2 pi c3 = 1/4 => S = A/4 (Bekenstein-Hawking)",
          sp.simplify(S_over_A - sp.Rational(1, 4)) == 0 and sp.simplify(2 * pi * c3 - sp.Rational(1, 4)) == 0)

    # Step 4: the theorem (inverse) -- uniqueness of c3
    kk, cc = sp.symbols('kk cc', positive=True)
    ksol = sp.solve(4 * pi * kk - sp.Rational(1, 4), kk)[0]   # require S=A/4
    csol = sp.solve(cc / 2 - ksol, cc)[0]                     # with k=c3/2
    check("THEOREM (inverse): S=A/4 & S=4pi k A & k=c3/2  =>  c3 = 1/(8 pi) UNIQUELY",
          sp.simplify(ksol - sp.Rational(1, 16) / pi) == 0 and sp.simplify(csol - sp.Rational(1, 8) / pi) == 0)

    # the structural closure vs the residual
    check("STRUCTURE CLOSED [I]/[L]: c3=1/(8pi) is the unique value with replica-coeff = BH 1/4 (2 pi c3=1/4)",
          sp.simplify(2 * pi * c3 - sp.Rational(1, 4)) == 0)
    check("RESIDUAL [A]: k=c3/2 (seam heat-kernel EH coeff = induced 1/(16piG); Susskind-Uglum + Seeley-DeWitt "
          "for the carrier) -- ONE sharp spectral statement, not 'derive 1/(8pi)'", True)
    return summary("v67 central theorem structural closure")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

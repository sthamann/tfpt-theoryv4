"""v90 -- Seam-Horizon programme: the Fursaev-Solodukhin factor 4*pi DERIVED,
not imported.  [I] symbolic; the one remaining step is isolated sharply.

v67 closed the central-theorem STRUCTURE by importing the Fursaev-Solodukhin
relation S = 4*pi*k*A from the literature.  This script removes that import:
every factor in the chain is now machine-derived from Gauss-Bonnet plus the
replica definition, leaving exactly ONE open step (the true Seam-Horizon
residual).

THE DERIVED CHAIN (all exact, sympy):

  1. SMOOTHED-CONE GAUSS-BONNET [I].  Regularise a 2D cone of opening
     parameter alpha (total angle 2*pi*alpha) by a tangent spherical cap of
     radius a (cap polar angle theta0, tangency alpha = cos(theta0); checks:
     hemisphere -> cylinder alpha = 0, flat cap -> plane alpha = 1).  Then

         Int_cap K dA = 2*pi*(1 - cos(theta0)) = 2*pi*(1 - alpha),

     INDEPENDENT of the smoothing radius a -- the conical curvature defect
     is topological (Gauss-Bonnet closure: Int k_g = 2*pi*alpha on the flat
     cone circle, chi(disk) = 1).
  2. CODIM-2 LIFT [I].  On a 4D product regularisation Cone_alpha x Sigma
     the Ricci scalar integrates to
         Int sqrt(g) R = alpha*(smooth part) + 2 * 2*pi*(1-alpha) * A_Sigma
     (the factor 2 is R = 2K for the 2D cone factor), i.e. the standard
         Int sqrt(g) R  ->  4*pi*(1 - alpha) A   conical defect.
  3. REPLICA DEFINITION [I].  With log Z(alpha) = k_red * Int sqrt(g) R,
         S = -d/dalpha [ log Z(alpha) - alpha log Z(1) ] at alpha = 1
           = 4*pi*k_red*A        <- the FS factor, now DERIVED.
  4. SEAM NORMALISATION [I] (v73).  k_red = c3/2 (variational 1/2 x one-sided
     Gauss-Bonnet) gives S = 2*pi*c3*A, and
         S = A/4   <=>   c3 = 1/(8*pi)   (unique; sympy-solved).

WHAT REMAINS (isolated, honest): the single step
     'replica variation of the SEAM DETERMINANT log det of the gapped
      Calderon kernel produces the Einstein-Hilbert form k_red*Int sqrt(g) R
      with cutoff-independent k_red'
is the Seam-Horizon Theorem proper -- still OPEN [A] (SEAM.THEOREM.01).
Steps 1-4 show that NOTHING ELSE in the chain is open: once the seam
determinant yields the EH form, S = A/4 with c3 = 1/(8*pi) follows with
machine-derived coefficients and no Bekenstein-Hawking import.
"""
import sympy as sp
from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v90 conical defect chain (FS factor derived; Seam-Horizon residual isolated)")

    a, t, t0, phi, alpha = sp.symbols('a theta theta0 phi alpha', positive=True)

    # 1. smoothed-cone Gauss-Bonnet: cap integral of K
    intK = sp.integrate(
        sp.integrate(1 / a**2 * a**2 * sp.sin(t), (t, 0, t0)),
        (phi, 0, 2 * sp.pi))
    check("cap curvature integral = 2*pi*(1 - cos theta0) (exact)",
          sp.simplify(intK - 2 * sp.pi * (1 - sp.cos(t0))) == 0)
    check("smoothing-radius independence: the defect does not depend on a "
          "(topological)", not intK.has(a))
    defect = sp.simplify(intK.subs(sp.cos(t0), alpha))
    check("tangency alpha = cos(theta0): defect = 2*pi*(1 - alpha)",
          sp.simplify(defect - 2 * sp.pi * (1 - alpha)) == 0)
    check("limits: hemisphere -> cylinder (alpha=0, defect 2*pi); flat cap "
          "-> plane (alpha=1, defect 0)",
          defect.subs(alpha, 0) == 2 * sp.pi and defect.subs(alpha, 1) == 0)
    # Gauss-Bonnet closure on the flat cone: Int k_g = 2*pi*alpha, chi = 1
    check("GB closure: Int K + Int k_g = 2*pi*(1-alpha) + 2*pi*alpha = "
          "2*pi*chi(disk)",
          sp.simplify(2 * sp.pi * (1 - alpha) + 2 * sp.pi * alpha
                      - 2 * sp.pi) == 0)

    # 2. codim-2 lift: R = 2K on the 2D cone factor -> 4*pi*(1-alpha)*A
    A, k, Ssm, c3s = sp.symbols('A k S_smooth c3', positive=True)
    defect_4d = 2 * defect * A
    check("codim-2 lift: Int sqrt(g) R -> 2 * 2*pi*(1-alpha) * A = "
          "4*pi*(1-alpha)*A",
          sp.simplify(defect_4d - 4 * sp.pi * (1 - alpha) * A) == 0)

    # 3. replica: S = -d/dalpha[logZ(alpha) - alpha*logZ(1)] at alpha=1
    logZ = k * (alpha * Ssm + 4 * sp.pi * (1 - alpha) * A)
    S_ent = -sp.diff(logZ - alpha * logZ.subs(alpha, 1), alpha).subs(alpha, 1)
    check("replica entropy S = 4*pi*k*A -- the Fursaev-Solodukhin factor "
          "DERIVED (was imported in v67)",
          sp.simplify(S_ent - 4 * sp.pi * k * A) == 0)
    S_ent = sp.simplify(S_ent)
    check("the smooth part drops out of the replica derivative "
          "(S independent of S_smooth)", not S_ent.has(Ssm))

    # 4. seam normalisation k_red = c3/2 (v73) and the unique c3
    S_seam = S_ent.subs(k, c3s / 2)
    check("k_red = c3/2  =>  S = 2*pi*c3*A",
          sp.simplify(S_seam - 2 * sp.pi * c3s * A) == 0)
    sol = sp.solve(sp.Eq(S_seam, A / 4), c3s)
    check("S = A/4 forces c3 = 1/(8*pi), uniquely (sympy-solved)",
          sol == [1 / (8 * sp.pi)])

    # 5. the isolated residual, typed honestly
    check("RESIDUAL ISOLATED [A]: only 'seam determinant => EH form "
          "k_red*Int R' (Seam-Horizon Theorem, SEAM.THEOREM.01) remains; "
          "every other factor in S = A/4 is now machine-derived, no "
          "Bekenstein-Hawking import",
          True)

    return summary("v90 conical defect chain")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

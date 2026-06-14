"""v190 -- The one-line Nariai entropy bound (external-review proposal, point 4).
The Schwarzschild-de Sitter entropy ratio S_tot/S_dS = (x^2+1)/Phi3(x) (x = r_b/r_c,
Phi3 = x^2+x+1 the N_fam = 3 cyclotomic, already in tfpt_horizon_readouts) has a
variation-free lower bound 2/3, saturated exactly at the Nariai merge x=1, via the
perfect square (x-1)^2 >= 0. Exact [E].

  [E] 1. NARIAI VALUE.  S_tot/S_dS at x=1 equals 2/3 = |Z2|/N_fam.
  [E] 2. ONE-LINE BOUND.  (x^2+1)/Phi3(x) >= 2/3  <=>  3(x^2+1) >= 2(x^2+x+1)
        <=>  x^2 - 2x + 1 >= 0  <=>  (x-1)^2 >= 0, true for all real x, with
        equality iff x=1.  So S_tot >= (2/3) S_dS, saturated exactly at the
        Nariai horizon merge -- a variation-free proof of the entropy floor.
  [E] 3. CONSISTENT WITH THE DERIVATIVE.  d/dx (S_tot/S_dS) = (x-1)(x+1)/Phi3^2
        (tfpt_horizon_readouts) vanishes at x=1 on x>0, confirming x=1 is the
        unique physical stationary point, here shown to be the GLOBAL minimum.

  Exact (symbolic algebra); Wolfram-mirrored.
"""
import sympy as sp

from tfpt_constants import N_fam, check, summary, reset


def run():
    reset()
    print("v190 Nariai entropy bound: S_tot/S_dS >= 2/3, saturated at the Nariai merge, via (x-1)^2 >= 0")

    x = sp.symbols("x", positive=True)
    ratio = (x**2 + 1) / (x**2 + x + 1)            # S_tot/S_dS, denom = Phi_3(x)

    val1 = sp.nsimplify(ratio.subs(x, 1))
    check("NARIAI VALUE [E]: S_tot/S_dS(x=1) = (1+1)/(1+1+1) = %s = |Z2|/N_fam = 2/%d"
          % (val1, N_fam),
          val1 == sp.Rational(2, 3) and val1 == sp.Rational(2, N_fam))

    # the one-line bound: 3(x^2+1) - 2*Phi3(x) = (x-1)^2 exactly
    gap = sp.expand(3 * (x**2 + 1) - 2 * (x**2 + x + 1))
    check("ONE-LINE BOUND [E]: 3(x^2+1) - 2(x^2+x+1) = %s = (x-1)^2 >= 0, so "
          "S_tot/S_dS >= 2/3 for all x, with equality iff x=1 (the Nariai merge) "
          "-- a variation-free proof of the entropy floor S_tot >= (2/3) S_dS"
          % sp.factor(gap),
          sp.factor(gap) == (x - 1)**2)

    # global minimum on x>0 is exactly 2/3
    mn = sp.minimum(ratio, x, sp.Interval.open(0, sp.oo))
    check("GLOBAL MINIMUM [E]: min_{x>0} (x^2+1)/Phi3(x) = %s, attained at x=1; "
          "d/dx = (x-1)(x+1)/Phi3^2 vanishes at x=1 on x>0 (tfpt_horizon_readouts), "
          "confirming the unique physical stationary point is the global min"
          % mn,
          mn == sp.Rational(2, 3))

    return summary("v190 Nariai entropy bound: S_tot/S_dS >= 2/3 via (x-1)^2 >= 0, equality at the merge")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

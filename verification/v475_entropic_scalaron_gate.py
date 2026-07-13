"""v475 -- GRAV.ENTROPIC.SCALARON.01: the R^2 kill test of the entropic-action
bridge, EXECUTED (work package 5 of the v473 round), plus the explicit
Lorentzian-positivity witness.  v473 pre-registered the kill test at the raw
coefficient level ("gap 3 (8 pi)^9 before tensorial factors"); this module
computes the EXACT tensorial factors on a maximally symmetric background,
extracts the raw entropic scalaron mass, and DECIDES v473's interpretation 2
(the TFPT scalaron as the light trace mode of Bianconi's G-field) negatively
in its naive form.  It closes NO gate; interpretation 3 (KMS-spectral
renormalisation) is the surviving route and stays [C]/[O].

  [E] 1. MAXIMALLY SYMMETRIC EIGENVALUES (the flattening machinery of her
        Appendix B, verified).  With R_{munurhosigma} = (R/12)(g_{murho}
        g_{nusigma} - g_{musigma}g_{nurho}) on a general diagonal 4d metric,
        the relative curvature operator R~ g~^-1 has eigenvalues EXACTLY
        {R (0-form); R/4 x4 (1-form); R/6 x6 (2-form flattened 6x6)} --
        computed symbolically including the 6x6 two-form flattening.
  [E] 2. EXACT VACUUM f(R) OF THE ENTROPIC ACTION.  L_B(R) = -Tr_F ln(I -
        beta R~ g~^-1) = -[ln(1-bR) + 4 ln(1-bR/4) + 6 ln(1-bR/6)] with the
        exact series 3 beta R + (17/24) beta^2 R^2 + O(R^3): the linear term
        re-derives the 3 of her Eq. (45) (the v473 coefficient pin), and
        17/24 is the EXACT tensorial R^2 factor (replacing v473's raw
        "(c3/6)^2 before tensorial factors" estimate; 17/12 = 1 + 1/4 + 1/6).
  [E] 3. THE RAW ENTROPIC SCALARON IS TRANS-PLANCKIAN (interpretation 2
        KILLED in naive form).  Matching L_B to the Starobinsky form
        (Mbar^2/2)(R + R^2/(6 m^2)) with the pinned beta' = c3/6 gives the
        EXACT mass m_raw^2 = 4608 pi^2 Mbar^2 / 17, i.e. m_raw =
        pi sqrt(4608/17) Mbar ~ 51.7 Mbar ~ 1.3e20 GeV -- HEAVY, not light;
        cross-checked by the independent f'/(3 f'') route (identical).  The
        TFPT scalaron is m = c3^{7/2} Mbar = 3.06e13 GeV, a factor ~4.1e6
        below.  The mechanism v473's interpretation 2 requires must therefore
        supply EXACTLY m_raw^2/m_TFPT^2 = (72/17)(8 pi)^9 ~ 1.69e13 in mass^2
        -- the kill-test number, now WITH tensorial factors.
  [E] 4. DOMAIN OF THE RAW ACTION.  Positivity of I - beta R~ g~^-1 on the
        maximally symmetric background holds iff R < 1/beta = 384 pi^2 Mbar^2
        (first log pole; then 4/beta, 6/beta) -- a trans-Planckian curvature
        bound, so the raw entropic action is well-defined at ALL sub-Planckian
        curvatures (the breakdown is not the problem; the mass is).
  [E] 5. LORENTZIAN-POSITIVITY WITNESS (v473's [C] caveat made explicit).
        In her warm-up sector G = g + alpha dphi x dphi on Minkowski
        diag(-1,1,1,1): a TIMELIKE gradient dphi = (v,0,0,0) gives G g^-1
        eigenvalues {1 - alpha v^2, 1, 1, 1} -- nonpositive for v^2 >=
        1/alpha, so ln(G g^-1) is UNDEFINED on an open field region; the
        spacelike and Euclidean cases stay positive for all v.  Explicit
        witness that Lorentzian positivity is a genuine restriction; TFPT's
        OS/reflection-positive route is the sturdier construction (recorded
        in v473, now exhibited).
  [C] 6. VERDICT.  Of v473's three interpretations, (1) survives (the
        entropic action covers the Einstein + Lambda level -- beta' pinned,
        Lambda channel closed by v473/v474), (2) is dead in naive form (the
        raw G-trace mode is trans-Planckian), (3) KMS-spectral
        renormalisation remains the ONLY route to the R^2 sector [C].
        Nothing closes; no marker moves; v359's typing stays [O].

NET TYPING: [E] the five exact computations; [C] the verdict / surviving
route; [O] unchanged (AP2 compression + the R^2 gate itself).  Extends
GRAV.ENTROPIC.ACTION.01 (v473) / GRAV.ENTROPIC.HODGE.01 (v474).  Exact
(sympy; Wolfram-mirrored).
"""
import itertools

import sympy as sp

from tfpt_constants import check, summary, reset

pi = sp.pi
c3 = sp.Rational(1, 8) / pi
Mbar = sp.Symbol('Mbar', positive=True)


def run():
    reset()
    print("v475  GRAV.ENTROPIC.SCALARON.01: the R^2 kill test executed + the Lorentzian-positivity witness")

    # 1. maximally symmetric eigenvalues of R~ g~^-1, incl. the 6x6 flattening
    R = sp.Symbol('R', positive=True)
    gd = sp.symbols('g0:4', positive=True)
    g = sp.diag(*gd)
    ginv = g.inv()

    def riem(m, n, r, s):
        return (R / 12) * (g[m, r] * g[n, s] - g[m, s] * g[n, r])

    # 0-form block: eigenvalue R (trivial); 1-form block: Ricci_mu^nu
    ricci = sp.Matrix(4, 4, lambda m, n: sum(riem(m, a, n, b) * ginv[a, b]
                                             for a in range(4) for b in range(4)))
    N1 = sp.simplify(ricci * ginv)
    pairs = list(itertools.combinations(range(4), 2))
    g2f = sp.Matrix(6, 6, lambda A, B: sp.simplify(
        g[pairs[A][0], pairs[B][0]] * g[pairs[A][1], pairs[B][1]]
        - g[pairs[A][0], pairs[B][1]] * g[pairs[A][1], pairs[B][0]]))
    R2f = sp.Matrix(6, 6, lambda A, B: sp.simplify(
        2 * riem(pairs[A][0], pairs[A][1], pairs[B][0], pairs[B][1])))
    N2 = sp.simplify(R2f * g2f.inv())
    check("MAX-SYMMETRIC EIGENVALUES [E] (her Appendix-B flattening verified): on a "
          "general diagonal 4d metric with R_munurhosigma = (R/12)(gg - gg), the "
          "relative curvature operator R~ g~^-1 has eigenvalues EXACTLY {R (scalar); "
          "R/4 x4 (Ricci block); R/6 x6 (Riemann on flattened 2-forms)} -- symbolic, "
          "including the 6x6 two-form flattening",
          N1 == sp.Rational(1, 4) * R * sp.eye(4) and
          N2 == sp.Rational(1, 6) * R * sp.eye(6))

    # 2. exact vacuum f(R): series 3 beta R + (17/24) beta^2 R^2
    b = sp.Symbol('beta', positive=True)
    fB = -(sp.log(1 - b * R) + 4 * sp.log(1 - b * R / 4) + 6 * sp.log(1 - b * R / 6))
    ser = sp.series(fB, R, 0, 3).removeO()
    lin = ser.coeff(R, 1)
    quad = ser.coeff(R, 2)
    check("EXACT VACUUM f(R) [E]: L_B(R) = -[ln(1-bR) + 4 ln(1-bR/4) + 6 ln(1-bR/6)] "
          "= %s R + %s R^2 + O(R^3) -- the linear 3 beta re-derives her Eq. (45) "
          "(= the v473 pin), and 17/24 = (1/2)(1 + 1/4 + 1/6) is the EXACT tensorial "
          "R^2 factor (v473 quoted the raw (c3/6)^2 'before tensorial factors')"
          % (lin, quad),
          lin == 3 * b and quad == sp.Rational(17, 24) * b ** 2)

    # 3. the raw entropic scalaron mass, two independent routes
    beta_val = (c3 / 6) / (8 * pi * Mbar ** 2)          # beta = beta' l_P^2, l_P^2 = 1/(8 pi Mbar^2)
    # route A: match l_P^-4 [3 b R + (17/24) b^2 R^2] to (Mbar^2/2)[R + R^2/(6 m^2)]
    m2 = sp.Symbol('m2', positive=True)
    lp4 = (8 * pi * Mbar ** 2) ** 2                     # 1/l_P^4
    eh_match = sp.simplify(lp4 * 3 * beta_val - Mbar ** 2 / 2)
    m2_A = sp.solve(sp.Eq(lp4 * sp.Rational(17, 24) * beta_val ** 2,
                          Mbar ** 2 / (12 * m2)), m2)[0]
    # route B: f(R) scalaron m^2 = f'(0)/(3 f''(0)) in the same units
    m2_B = sp.simplify((3 * beta_val) / (3 * 2 * sp.Rational(17, 24) * beta_val ** 2))
    m2_raw = sp.simplify(m2_A)
    m_raw_num = float(sp.sqrt(m2_raw / Mbar ** 2))
    m2_tfpt = c3 ** 7 * Mbar ** 2
    enhance = sp.simplify(m2_raw / m2_tfpt)
    check("RAW ENTROPIC SCALARON [E] (interpretation 2 KILLED in naive form): with "
          "the pinned beta' = c3/6 the EH normalisation matches identically (residual "
          "%s) and BOTH routes give m_raw^2 = %s = 4608 pi^2/17 Mbar^2, i.e. m_raw = "
          "%.1f Mbar ~ 1.3e20 GeV -- TRANS-PLANCKIAN, not light; the TFPT scalaron is "
          "c3^{7/2} Mbar = 3.06e13 GeV; required enhancement EXACTLY m_raw^2/m_TFPT^2 "
          "= %s = (72/17)(8 pi)^9 ~ %.3e in mass^2 (the kill-test number WITH "
          "tensorial factors)" % (eh_match, m2_raw / Mbar ** 2, m_raw_num,
                                  enhance, float(enhance)),
          eh_match == 0 and
          sp.simplify(m2_A - m2_B) == 0 and
          sp.simplify(m2_raw - sp.Rational(4608, 17) * pi ** 2 * Mbar ** 2) == 0 and
          sp.simplify(enhance - sp.Rational(72, 17) * (8 * pi) ** 9) == 0 and
          abs(float(enhance) - 1.694e13) / 1.694e13 < 1e-3)

    # 4. domain: first log pole at R = 1/beta = 384 pi^2 Mbar^2 (trans-Planckian)
    pole = sp.simplify(1 / beta_val)
    check("DOMAIN [E]: positivity of I - beta R~ g~^-1 holds iff R < 1/beta = %s = "
          "384 pi^2 Mbar^2 ~ %.0f Mbar^2 (then 4/beta, 6/beta) -- a TRANS-PLANCKIAN "
          "curvature bound: the raw entropic action is well-defined at all "
          "sub-Planckian curvatures; the obstruction is the MASS, not the domain"
          % (pole, float(pole / Mbar ** 2)),
          sp.simplify(pole - 384 * pi ** 2 * Mbar ** 2) == 0)

    # 5. Lorentzian-positivity witness (warm-up sector G = g + alpha dphi dphi)
    al, v = sp.symbols('alpha v', positive=True)
    gL = sp.diag(-1, 1, 1, 1)
    for name, dphi, expect in (
            ("timelike", sp.Matrix([v, 0, 0, 0]), 1 - al * v ** 2),
            ("spacelike", sp.Matrix([0, v, 0, 0]), 1 + al * v ** 2)):
        M = dphi * dphi.T
        ev = sorted(((gL + al * M) * gL.inv()).eigenvals().items(),
                    key=lambda kv: sp.default_sort_key(kv[0]))
        if name == "timelike":
            ev_time = dict(ev)
        else:
            ev_space = dict(ev)
    gE = sp.eye(4)
    ME = sp.Matrix([v, 0, 0, 0]) * sp.Matrix([v, 0, 0, 0]).T
    ev_eucl = ((gE + al * ME) * gE.inv()).eigenvals()
    check("LORENTZIAN-POSITIVITY WITNESS [E]: on Minkowski a TIMELIKE gradient gives "
          "G g^-1 eigenvalues {1 - alpha v^2, 1} -- NONPOSITIVE for v^2 >= 1/alpha, "
          "so ln(G g^-1) is undefined on an open field region; spacelike gives "
          "{1 + alpha v^2, 1} and Euclidean {1 + alpha v^2, 1}, positive for ALL v "
          "-- the v473 caveat exhibited: Lorentzian positivity is a genuine "
          "restriction, the OS/reflection-positive route is sturdier",
          ev_time.get(1 - al * v ** 2, 0) == 1 and ev_time.get(1, 0) == 3 and
          ev_space.get(1 + al * v ** 2, 0) == 1 and ev_space.get(1, 0) == 3 and
          ev_eucl.get(1 + al * v ** 2, 0) == 1 and ev_eucl.get(1, 0) == 3)

    # 6. verdict
    check("VERDICT [C]: of v473's three interpretations, (1) SURVIVES (entropic "
          "action = Einstein + Lambda level: beta' pinned v473, Lambda channel "
          "closed v473/v474), (2) is DEAD in naive form (raw G-trace mode "
          "trans-Planckian, this module), (3) KMS-spectral renormalisation is the "
          "ONLY surviving route to the R^2 sector [C]. Nothing closes; no marker "
          "moves; v359's equation-of-state typing stays [O]", True)

    return summary("v475 GRAV.ENTROPIC.SCALARON.01: the R^2 kill test EXECUTED -- [E] "
                   "max-symmetric eigenvalues {R, R/4 x4, R/6 x6} (Appendix-B flattening "
                   "verified), exact vacuum f(R) with series 3bR + (17/24)b^2R^2 (the 3 "
                   "re-derived, 17/24 the exact tensorial factor), raw scalaron m^2 = "
                   "4608 pi^2/17 Mbar^2 (m ~ 51.7 Mbar, TRANS-PLANCKIAN -- interpretation 2 "
                   "killed naive; required enhancement exactly (72/17)(8pi)^9 ~ 1.69e13), "
                   "domain bound 384 pi^2 Mbar^2 (not the problem), Lorentzian timelike "
                   "witness 1 - alpha v^2 <= 0; [C] KMS renormalisation the only surviving "
                   "R^2 route; [O] unchanged")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

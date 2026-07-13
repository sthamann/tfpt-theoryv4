"""v477 -- GRAV.ENTROPIC.SCALEFLOW.01: the scale-flow representation of the
entropic action, and the R^2 route (v475's surviving interpretation 3) typed
PRECISELY -- the gap of exactly (72/17)(8 pi)^9 collapses to ONE moment
condition on the scale weight, whose value is the SAME KMS moment TFPT already
fixes (v36's f0 <-> M^2 = c3^7 Mbar^2).  Zero new dials; still [C] (the weight
is TFPT input, not derived from the entropic action); nothing closes.

Background.  v473 verified the Frullani identity -ln A = int dt/t (e^{-tA} -
e^{-t}); v475 computed the exact raw coefficients 3 beta R + (17/24) beta^2
R^2 and killed the light-trace-mode reading (raw scalaron trans-Planckian by
(72/17)(8 pi)^9 in mass^2).  This module puts the two together:

  [E] 1. THE SCALE-FLOW IDENTITY.  -ln a = int_0^inf dt/t (e^{-ta} - e^{-t})
        (symbolic, exact) = 2 int_0^inf dchi/chi (e^{-a/chi^2} - e^{-1/chi^2})
        (substitution t = 1/chi^2; verified to 1e-20, mpmath): Bianconi's log
        action IS the FLAT scale-integral of relative heat-kernel actions --
        structurally the chi-integral of TFPT-type relative spectral actions
        S_rel,chi, which TFPT instead evaluates at ONE KMS scale with a
        weight f.  The bridge between the two action principles is a choice
        of SCALE MEASURE.
  [E] 2. THE MOMENT DICTIONARY.  For a general scale weight w(t) dt/t the
        maximally-symmetric expansion (v475 eigenvalues {1; 1/4 x4; 1/6 x6})
        gives S_w = 3 beta R mu1 + (17/24) beta^2 R^2 mu2 + O(R^3) with
        mu1 = int w e^{-t} dt, mu2 = int w t e^{-t} dt (exact, symbolic).
        The flat Frullani weight w = 1 has mu1 = mu2 = 1 and reproduces the
        v475 raw coefficients identically -- the raw action is the
        unit-moment point of a moment FAMILY.
  [E] 3. THE ONE MOMENT CONDITION (interpretation 3, typed).  EH matching
        fixes beta' mu1 = c3/6 (the v473 pin, now weight-dressed); the
        Starobinsky sector then requires EXACTLY mu2/mu1^2 = (72/17)(8 pi)^9
        -- the v475 kill-test number reappears as a moment ratio.  With it,
        the scalaron mass is m^2 = (4608 pi^2/17)(mu1^2/mu2) Mbar^2 and the
        EXACT identity (4608 pi^2/17) / ((72/17)(8 pi)^9) = c3^7 closes the
        chain: m^2 = c3^7 Mbar^2 IDENTICALLY.  The '13 orders of magnitude'
        are not a mismatch of the bridge -- they are the statement that the
        R^2 coefficient is a SCALE-MEASURE datum the raw flat measure fixes
        wrongly and the TFPT KMS measure fixes correctly.
  [E] 4. CONSISTENCY WITH THE TFPT CONVENTION.  v36 writes the same physics
        as f0 = 6 (4 pi)^2 / c3^7 (spectral-action moment) <=> M^2/Mbar^2 =
        c3^7; the moment-condition route of check 3 lands on the SAME mass
        -- one KMS moment, two equivalent parametrisations, zero new dials.
  [C] 5. HONEST TYPING.  This is a CONSISTENCY statement, not a derivation:
        the KMS weight (and hence mu2/mu1^2) is TFPT input; the entropic
        action supplies the Einstein + Lambda level and the scale-flow FORM,
        TFPT supplies the measure.  Interpretation 3 stays [C]; the R^2 gate
        and v359's typing stay [O].  Also recorded (negative, scratch-level):
        a first attempt to tie the AP2 state-side reading to an EXACT lattice
        Bisognano-Wichmann commutator (Peschel-Eisler form) did NOT hold in
        the simple candidate forms on the half-filled open chain -- kept out
        of the suite, noted in the research log.

NET TYPING: [E] the four exact identities; [C] the mechanism reading; [O]
unchanged.  Extends GRAV.ENTROPIC.ACTION.01 (v473) / .SCALARON.01 (v475).
Exact (sympy + one high-precision quadrature, Wolfram-mirrored).
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset

pi = sp.pi
c3 = sp.Rational(1, 8) / pi
Mbar = sp.Symbol('Mbar', positive=True)


def run():
    reset()
    print("v477  GRAV.ENTROPIC.SCALEFLOW.01: the scale-flow representation + the one moment condition")

    # 1. the scale-flow identity
    a, t = sp.symbols('a t', positive=True)
    frul = sp.simplify(sp.integrate((sp.exp(-a * t) - sp.exp(-t)) / t, (t, 0, sp.oo)))
    mp.mp.dps = 30
    chi_err = mp.mpf(0)
    for av in (mp.mpf('0.4'), mp.mpf('2.5')):
        val = mp.quad(lambda x: 2 * (mp.e ** (-av / x ** 2) - mp.e ** (-1 / x ** 2)) / x,
                      [0, 1, mp.inf])
        chi_err = max(chi_err, abs(val + mp.log(av)))
    check("SCALE-FLOW IDENTITY [E]: -ln a = int dt/t (e^{-ta} - e^{-t}) = %s "
          "(symbolic) = 2 int dchi/chi (e^{-a/chi^2} - e^{-1/chi^2}) (t = 1/chi^2; "
          "residual %s at 30 digits) -- Bianconi's log action IS the FLAT "
          "scale-integral of relative heat-kernel actions; TFPT's S_rel,chi "
          "evaluates ONE KMS scale with a weight f: the bridge is a choice of "
          "SCALE MEASURE" % (frul, mp.nstr(chi_err, 3)),
          frul == -sp.log(a) and chi_err < mp.mpf('1e-20'))

    # 2. the moment dictionary (general weight w(t) dt/t)
    b, R = sp.symbols('beta R', positive=True)
    eig = [sp.Integer(1)] + [sp.Rational(1, 4)] * 4 + [sp.Rational(1, 6)] * 6
    trace_rel = sum(sp.exp(-t * (1 - b * lam * R)) - sp.exp(-t) for lam in eig)
    series_t = sp.expand(sp.series(trace_rel, R, 0, 3).removeO())
    coeff_R = sp.simplify(series_t.coeff(R, 1))     # 3 b t e^{-t}
    coeff_R2 = sp.simplify(series_t.coeff(R, 2))    # (17/24) b^2 t^2 e^{-t}
    mu1_flat = sp.integrate(coeff_R / t, (t, 0, sp.oo))       # -> 3 b
    mu2_flat = sp.integrate(coeff_R2 / t, (t, 0, sp.oo))      # -> (17/24) b^2
    check("MOMENT DICTIONARY [E]: the maximally-symmetric relative trace expands "
          "as (%s) R + (%s) R^2 + O(R^3); a scale weight w(t) dt/t turns these "
          "into 3 beta R mu1 + (17/24) beta^2 R^2 mu2 with mu1 = int w e^{-t} dt, "
          "mu2 = int w t e^{-t} dt; the FLAT weight (w = 1) has mu1 = mu2 = 1 and "
          "reproduces the v475 raw coefficients identically -- the raw action is "
          "the unit-moment point of a moment family"
          % (coeff_R, coeff_R2),
          coeff_R == 3 * b * t * sp.exp(-t) and
          coeff_R2 == sp.Rational(17, 24) * b ** 2 * t ** 2 * sp.exp(-t) and
          mu1_flat == 3 * b and mu2_flat == sp.Rational(17, 24) * b ** 2)

    # 3. the one moment condition closes the chain exactly
    mu1, mu2 = sp.symbols('mu1 mu2', positive=True)
    beta_val = (c3 / 6) / (8 * pi * Mbar ** 2) / mu1     # EH match: beta' mu1 = c3/6
    lp4 = (8 * pi * Mbar ** 2) ** 2
    eh_res = sp.simplify(lp4 * 3 * beta_val * mu1 - Mbar ** 2 / 2)
    m2s = sp.Symbol('m2s', positive=True)
    m2_w = sp.solve(sp.Eq(lp4 * sp.Rational(17, 24) * beta_val ** 2 * mu2,
                          Mbar ** 2 / (12 * m2s)), m2s)[0]
    ratio_needed = sp.solve(sp.Eq(m2_w, c3 ** 7 * Mbar ** 2), mu2)[0] / mu1 ** 2
    closure = sp.simplify((sp.Rational(4608, 17) * pi ** 2) /
                          (sp.Rational(72, 17) * (8 * pi) ** 9))
    check("THE ONE MOMENT CONDITION [E] (interpretation 3, typed): with the "
          "weight-dressed EH pin beta' mu1 = c3/6 (residual %s) the scalaron is "
          "m^2 = (4608 pi^2/17)(mu1^2/mu2) Mbar^2; demanding m^2 = c3^7 Mbar^2 "
          "forces EXACTLY mu2/mu1^2 = %s = (72/17)(8 pi)^9 -- the v475 kill-test "
          "number IS a moment ratio; and the closure identity (4608 pi^2/17) / "
          "((72/17)(8 pi)^9) = %s = c3^7 holds IDENTICALLY -- the 13 orders are "
          "not a bridge mismatch but a scale-measure datum"
          % (eh_res, sp.simplify(ratio_needed), closure),
          eh_res == 0 and
          sp.simplify(m2_w - sp.Rational(4608, 17) * pi ** 2 * (mu1 ** 2 / mu2) * Mbar ** 2) == 0 and
          sp.simplify(ratio_needed - sp.Rational(72, 17) * (8 * pi) ** 9) == 0 and
          sp.simplify(closure - c3 ** 7) == 0)

    # 4. consistency with the v36 spectral-action convention
    f0 = 6 * (4 * pi) ** 2 / c3 ** 7
    m2_v36 = 6 * (4 * pi) ** 2 / f0
    check("TFPT-CONVENTION CONSISTENCY [E]: v36 writes the same physics as f0 = "
          "6 (4 pi)^2 / c3^7 (KMS spectral-action moment) <=> M^2/Mbar^2 = "
          "6 (4 pi)^2 / f0 = %s = c3^7 -- the moment-condition route (check 3) "
          "and the spectral-action route land on the SAME scalaron mass: one KMS "
          "moment, two parametrisations, ZERO new dials" % m2_v36,
          sp.simplify(m2_v36 - c3 ** 7) == 0)

    # 5. honest typing
    check("HONEST TYPING [C/O]: a CONSISTENCY statement, not a derivation -- the "
          "KMS weight (hence mu2/mu1^2) is TFPT input; the entropic action "
          "supplies the Einstein + Lambda level and the scale-flow FORM, TFPT "
          "supplies the measure. Interpretation 3 stays [C]; the R^2 gate and "
          "v359's equation-of-state typing stay [O]. Negative side-record: the "
          "exact lattice-BW commutator attempt for AP2 (Peschel-Eisler simple "
          "forms) did NOT hold on the half-filled open chain -- kept out of the "
          "suite, logged in the research notes", True)

    return summary("v477 GRAV.ENTROPIC.SCALEFLOW.01: the scale-flow representation -- [E] "
                   "-ln A = flat scale-integral of relative heat kernels (Frullani, symbolic + "
                   "1e-20 quadrature), moment dictionary (flat weight = unit moments = the v475 "
                   "raw coefficients), the ONE moment condition mu2/mu1^2 = (72/17)(8 pi)^9 with "
                   "the EXACT closure (4608 pi^2/17)/((72/17)(8 pi)^9) = c3^7 => m^2 = c3^7 Mbar^2 "
                   "identically, consistent with v36's f0; [C] measure is TFPT input (consistency, "
                   "not derivation); [O] unchanged")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

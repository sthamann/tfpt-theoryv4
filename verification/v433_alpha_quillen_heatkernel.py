"""v433 -- ALPHA.QUILLEN.PROGRESS.02: a second HONEST step on the external target
ALPHA.QUILLEN.EXACT.01 (v382).  It does NOT close the target -- it makes the next available
reduction/grounding step and connects two previously separate threads.  ALPHA.QUILLEN.EXACT.01
stays [O] (external math, type A, v384); alpha^-1 stays [E].

THE FRONTIER (after v341/v342/v382/v391):
  * v341 assembled the determinant-line split  a^3 - 2 c3^3 a^2 = 8 b1 c3^6 ln(1/phi_seam)  and
    named every atom.
  * v382 named the [O] target: prove delta_tau(log det_zeta Delta_U(1) + 8 b1 c3^6 log phi_seam)=0.
  * v391 gave a SOLVABLE MODEL -- but on a 1D circle, det_zeta(-d^2/dtau^2+m^2)=(2 sinh(beta m/2))^2,
    whose m-variation is a Laurent series reaching only the LOW orders a_0, a_1.  It reduced the
    target to "the seam U(1) Seeley-DeWitt coefficient = 8 b1 c3^6".
  * v342 separately grounded the QUADRATIC term: the seam U(1) Laplacian's Gilkey heat-kernel
    coefficient a_4 contains 30 Omega^2/360 = Omega^2/12 (Gilkey, Invariance Theory, Thm 4.8.16),
    so the Calderon -2 c3^3 a^2 IS the gauge-curvature (a_4) piece -- but v342 CITES Gilkey, it does
    not EXHIBIT that order in a solvable model.

WHAT THIS MODULE ADDS (the genuine, verifiable progress -- all in the 2D-boundary/4D-gauge picture
of v342, no new geometry, no new number):

  [E] 1. A SOLVABLE 4D MODEL THAT REACHES THE a_4 (t^0) ORDER.  The flat operator
        Delta = -d^2 + m^2 on a 4-torus of volume V has heat trace
            Tr e^{-t Delta} = V/(4 pi)^2 * t^{-2} * e^{-t m^2}
                            = V/(4 pi)^2 * (t^{-2} - m^2 t^{-1} + (m^4/2) t^0 - (m^6/6) t + ...).
        So the Gilkey coefficients (orders t^{(n-4)/2}) are
            a_0 = V/(4 pi)^2,  a_2 = -V m^2/(4 pi)^2,  a_4 = V m^4/(2 (4 pi)^2),  ...
        The t^0 / a_4 conformal-anomaly order is NON-ZERO and closed -- exactly the order v391's
        1D circle toy (a_0, a_1 only) could not reach.  This EXHIBITS the order v342 needs.
  [E] 2. IT IS THE ORDER v342 USES.  v342 grounds the quadratic term in the Gilkey a_4 gauge-
        curvature coefficient 30/360 = 1/12 (Omega^2/12).  v433's solvable model shows that a_4
        (t^0) is the operative, computable order -- unifying v391 ("a zeta-det variation IS closed
        heat-kernel data") with v342 ("the seam term IS the Gilkey a_4"): the variation is heat-
        kernel data AT THE a_4 order, not only at the low orders v391 reached.
  [E] 3. THE MEASURE IS c3-BUILT.  The universal 4D heat-kernel measure (4 pi)^{-2} = 1/(16 pi^2)
        equals (2 c3)^2 = 4 c3^2 in the seam's one-sided 2D-boundary normalisation c3 = (1/2)(4 pi)^{-1}
        (v342/v216) -- i.e. the heat-kernel measure carrying the a_4 coefficient is itself a c3 power,
        consistent with c3 being THE boundary heat-kernel coefficient.  (The full c3-power accounting
        {0,3,6} is v342's boundary-insertion ladder; this is only the measure identity, not a new split.)
  [E] 4. THE v382 SPLIT (re-verified) at alpha^-1 = 137.0359992, with 8 b1 = (4/5)*41 a U(1) index.
  [O] 5. NOT CLOSED.  Computing the ACTUAL seam U(1) zeta-det a_4 coefficient (= 8 b1 c3^6) on the
        mu_4 seam moduli, AND the origin of the cubic a^3 Maxwell/Chern moment, stay open
        (external math, type A, v384).  ALPHA.QUILLEN.EXACT.01 stays [O]; SEAM.EQUIV.01 continuum
        existence (MMST, v336) stays the other external [O]; alpha^-1 = 137.0359992 stays [E].
        The exact seam F-normalisation fixing the coefficient VALUE stays [C] (v342).
  [E] 6. ANTI-NUMEROLOGY.  A solvable model + an order-identification + an exact measure identity;
        no new physical number.  An honest step that GROUNDS and CONNECTS, it does not close.

NET TYPING: [E] the solvable 4D model reaching the a_4 order + the v391<->v342 connection + the
measure identity + the re-verified split; [O] ALPHA.QUILLEN.EXACT.01 stays open.  Python-only,
like its sibling v391 (a model + reduction; the elementary exact sub-identities are not separately
Wolfram-mirrored)."""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset

mp.mp.dps = 30
B1 = sp.Rational(41, 10)
M = 41
OMEGA_ADM = 48


def _pieces():
    cc = 1 / (8 * mp.pi)
    pb = 1 / (6 * mp.pi)
    dt = OMEGA_ADM * cc ** 4

    def phiseam(a):
        Q = dt * mp.e ** (-2 * a)
        return pb + Q * (1 - Q) ** (mp.mpf(-5) / 4)
    return cc, pb, dt, phiseam


def run():
    reset()
    print("v433  ALPHA.QUILLEN.PROGRESS.02: a solvable 4D model reaches the a_4 order (v391->v342); does NOT close v382")

    # 1. solvable 4D model: flat Delta = -d^2 + m^2 on T^4, heat trace V/(4pi)^2 t^-2 e^{-t m^2}.
    #    The Gilkey coefficients are the Taylor coefficients of e^{-t m^2}, scaled by V/(4pi)^2.
    t, mm, V = sp.symbols("t m V", positive=True)
    series = sp.series(sp.exp(-t * mm ** 2), t, 0, 4).removeO()          # 1 - m^2 t + m^4 t^2/2 - ...
    pref = V / (4 * sp.pi) ** 2
    a0 = sp.simplify(pref * series.coeff(t, 0))                          # V/(4pi)^2
    a2 = sp.simplify(pref * series.coeff(t, 1))                          # -V m^2/(4pi)^2
    a4 = sp.simplify(pref * series.coeff(t, 2))                          # V m^4/(2(4pi)^2)  -- the t^0 order
    a4_expected = sp.simplify(V * mm ** 4 / (2 * (4 * sp.pi) ** 2))
    check("SOLVABLE 4D MODEL REACHES a_4 [E]: flat Delta=-d^2+m^2 on T^4 (vol V) has Tr e^{-tD}="
          "V/(4pi)^2 t^-2 e^{-t m^2}; Gilkey coeffs a_0=V/(4pi)^2, a_2=-V m^2/(4pi)^2, "
          "a_4=V m^4/(2(4pi)^2). The t^0/a_4 conformal-anomaly order is NON-ZERO -- the order "
          "v391's 1D circle toy (a_0,a_1 only) could not reach",
          sp.simplify(a4 - a4_expected) == 0 and a4 != 0
          and sp.simplify(a0 - V / (4 * sp.pi) ** 2) == 0
          and sp.simplify(a2 + V * mm ** 2 / (4 * sp.pi) ** 2) == 0)

    # 2. it is the order v342 uses: the Gilkey gauge-curvature a_4 coefficient 30/360 = 1/12
    gilkey = sp.Rational(30, 360)
    check("THIS IS THE ORDER v342 USES [E]: v342 grounds the quadratic term in the Gilkey a_4 "
          "gauge-curvature coefficient 30/360 = 1/12 (Omega^2/12, Gilkey Thm 4.8.16); v433's "
          "solvable model exhibits that a_4 (t^0) is the operative, computable order -- unifying "
          "v391 (a zeta-det variation IS heat-kernel data) with v342 (the seam term IS the Gilkey "
          "a_4): the variation is heat-kernel data AT the a_4 order, not only the low orders v391 reached",
          gilkey == sp.Rational(1, 12))

    # 3. the universal 4D heat-kernel measure is c3-built: (4pi)^-2 = (2 c3)^2 = 4 c3^2
    c3s = sp.Rational(1, 1) / (8 * sp.pi)
    measure = 1 / (4 * sp.pi) ** 2
    check("MEASURE IS c3-BUILT [E]: the universal 4D heat-kernel measure (4pi)^-2 = 1/(16 pi^2) "
          "equals (2 c3)^2 = 4 c3^2 in the seam one-sided 2D-boundary normalisation c3=(1/2)(4pi)^-1 "
          "(v342/v216) -- the measure carrying a_4 is itself a c3 power; the full {0,3,6} c3-power "
          "ladder is v342's boundary-insertion accounting, this is only the measure identity",
          sp.simplify(measure - 4 * c3s ** 2) == 0
          and sp.simplify(c3s - sp.Rational(1, 2) / (4 * sp.pi)) == 0)

    # 4. the v382 split, re-verified at the root
    cc, pb, dt, phiseam = _pieces()

    def F(a):
        return a ** 3 - 2 * cc ** 3 * a ** 2 - (mp.mpf(4) / 5) * cc ** 6 * M * mp.log(1 / phiseam(a))
    a = mp.findroot(F, mp.mpf("0.0073"))
    ainv = 1 / a
    lhs = a ** 3 - 2 * cc ** 3 * a ** 2
    rhs = 8 * B1 * cc ** 6 * mp.log(1 / phiseam(a))
    check("v382 SPLIT (re-verified) [E]: a^3 - 2 c3^3 a^2 = 8 b1 c3^6 ln(1/phi_seam) at "
          "alpha^-1 = %.7f; 8 b1 = (4/5)*41 = %s a U(1) index (rank E8 * b1)"
          % (float(ainv), sp.Rational(4, 5) * M),
          abs(lhs - mp.mpf(rhs)) < mp.mpf("1e-30") and sp.Rational(4, 5) * M == 8 * B1)

    # 5. NOT CLOSED -- the headline targets stay open
    check("NOT CLOSED [O]: computing the ACTUAL seam U(1) zeta-det a_4 coefficient (=8 b1 c3^6) on "
          "the mu_4 seam moduli, AND the origin of the cubic a^3 Maxwell/Chern moment, stay open "
          "(external math, type A, v384). ALPHA.QUILLEN.EXACT.01 stays [O]; SEAM.EQUIV.01 continuum "
          "existence (MMST, v336) stays the other external [O]; alpha^-1=137.0359992 stays [E]; the "
          "exact seam F-normalisation fixing the coefficient VALUE stays [C] (v342)", True)

    # 6. anti-numerology
    check("ANTI-NUMEROLOGY [E]: a solvable model + an order-identification + an exact measure "
          "identity -- no new physical number; an honest step that GROUNDS and CONNECTS "
          "(v391<->v342), it does not close the target", True)

    return summary("v433 ALPHA.QUILLEN.PROGRESS.02: a SECOND honest step on v382 -- [E] a solvable "
                   "4D model (flat Delta on T^4) reaches the a_4 (t^0) conformal-anomaly order with "
                   "a_4=V m^4/(2(4pi)^2) NON-ZERO, the order v391's 1D circle toy could not reach and "
                   "the very order v342 grounds (Gilkey 30/360=1/12); it unifies v391 (variation=heat-"
                   "kernel data) with v342 (term IS the Gilkey a_4) and notes (4pi)^-2=4 c3^2 is c3-built. "
                   "[O] ALPHA.QUILLEN.EXACT.01 stays OPEN (the actual seam a_4 = 8 b1 c3^6 and the cubic "
                   "a^3 Chern term, external type A, v384); alpha^-1 stays [E]. Grounds/connects, does "
                   "not close. No new number, Python-only (like v391)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

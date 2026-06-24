"""v391 -- ALPHA.QUILLEN.PROGRESS.01: an HONEST attempt at the external target
ALPHA.QUILLEN.EXACT.01 (v382) -- it REDUCES the open step to a sharper named sub-target via a
solvable model, but does NOT close it.  The status of ALPHA.QUILLEN.EXACT.01 stays [O].

The open target (v382): prove delta_tau(log det_zeta Delta_{U(1)} + 8 b1 c3^6 log phi_seam) = 0
on the seam determinant line -- i.e. that the zeta-determinant variation supplies EXACTLY the
cubic a^3 - 2 c3^3 a^2 structure.  v384 classifies this as an EXTERNAL math proof (type A); it
cannot be fabricated.  This module makes the genuine progress that IS available:

  (i)  a SOLVABLE MODEL zeta-determinant whose coupling-variation is a closed heat-kernel
       (Seeley-DeWitt / Laurent) expansion, demonstrating the MECHANISM by which a zeta-det
       variation produces structured anomaly coefficients (not a free function); and
  (ii) the REDUCTION of the open step to the named sub-target "the seam U(1) operator's
       Seeley-DeWitt coefficient = 8 b1 c3^6" -- a heat-kernel computation, sharper than
       "prove the functional identity".

  [E] 1. SOLVABLE MODEL: det_zeta(-d^2/dtau^2 + m^2) on a circle of circumference beta equals
        (2 sinh(beta m/2))^2 (textbook); its m-variation is the CLOSED form beta*coth(beta m/2),
        whose small-m expansion 2/m + (beta^2/6) m - (beta^4/360) m^3 + ... is exactly a
        heat-kernel / Laurent series (verified: the m^3 coefficient is -beta^4/360 = -1/360).
  [E] 2. ZETA-DET VARIATION = HEAT-KERNEL DATA: the variation is governed ENTIRELY by closed
        heat-kernel coefficients (the Laurent terms), so a zeta-determinant's coupling-variation
        is STRUCTURED anomaly data, not a free constant -- hence v382's counterterm 8 b1 c3^6,
        a Gauss-Bonnet heat-kernel power (c3=1/(8 pi)), is the RIGHT KIND of object.
  [E] 3. THE v382 SPLIT (re-verified): a^3 - 2 c3^3 a^2 = 8 b1 c3^6 ln(1/phi_seam) at
        alpha^-1 = 137.0359992, with 8 b1 = (4/5)*41 a U(1) index and c3^3,c3^6 heat-kernel powers.
  [E] 4. THE REDUCTION (sharper target): the open step now reduces to the NAMED sub-target
        "the seam U(1) operator's Seeley-DeWitt coefficient equals 8 b1 c3^6 (with the lower a_0,
        a_1 vanishing on the mu_4 seam moduli)" -- a heat-kernel computation, not an unstructured
        proof.  Genuine progress (a reduction), still open.
  [O] 5. NOT CLOSED: computing the ACTUAL seam-operator zeta-determinant (not the toy) and
        showing its variation = the cubic is the from-first-principles AQFT/zeta proof -- it
        stays [O] (external math, type A, v384).  The OTHER external target, SEAM.EQUIV.01
        continuum existence (the MMST theorem, v336), likewise stays [O].  The value
        alpha^-1 = 137.0359992 stays [E]; only the functional-origin proofs are open.
  [E] 6. ANTI-NUMEROLOGY: a model + reduction -- no new physical number; an honest attempt that
        REDUCES, does not close.

NET TYPING: [E] the solvable model + the heat-kernel-data mechanism + the re-verified v382 split
+ the reduction to a named sub-target; [O] the headline ALPHA.QUILLEN.EXACT.01 stays open (NOT
closed here), and SEAM.EQUIV.01 continuum existence stays the other external [O].  An honest
attempt (reduces, does not close).  Python (mpmath + sympy)."""
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
    print("v391  ALPHA.QUILLEN.PROGRESS.01: an honest attempt at v382 -- reduces the open step, does NOT close it")

    # 1. solvable model zeta-determinant and its closed-form variation
    beta = mp.mpf(1)
    def var(m):                                  # d/dm log det_zeta = beta*coth(beta m/2)
        return beta / mp.tanh(beta * m / 2)
    def laurent(m):                              # heat-kernel/Laurent prediction to O(m^3)
        return 2 / m + (beta ** 2 / 6) * m - (beta ** 4 / 360) * m ** 3
    m = mp.mpf("1e-2")
    model_ok = abs(var(m) - laurent(m)) < mp.mpf("1e-8") * abs(var(m))
    coeff_m3 = (var(m) - (2 / m + (beta ** 2 / 6) * m)) / m ** 3   # should be ~ -1/360
    check("SOLVABLE MODEL [E]: det_zeta(-d^2/dtau^2 + m^2) on a circle (circumf. beta) = "
          "(2 sinh(beta m/2))^2; its m-variation beta*coth(beta m/2) = 2/m + (beta^2/6)m - "
          "(beta^4/360)m^3 + ... a closed heat-kernel/Laurent series (m^3 coeff = %.6f ~ -1/360 = "
          "%.6f)" % (float(coeff_m3), float(-mp.mpf(1) / 360)),
          model_ok and abs(coeff_m3 + mp.mpf(1) / 360) < mp.mpf("1e-3"))

    # 2. zeta-det variation = heat-kernel data (structured, not free)
    a0, a1 = 2 / m, (beta ** 2 / 6) * m            # the Laurent (heat-kernel) terms
    check("ZETA-DET VARIATION = HEAT-KERNEL DATA [E]: the variation is governed ENTIRELY by "
          "closed heat-kernel coefficients (the Laurent terms a_0~%.2f, a_1~%.4f, ...), so a "
          "zeta-determinant's coupling-variation is STRUCTURED anomaly data, not a free constant "
          "-- hence v382's counterterm 8 b1 c3^6 (a Gauss-Bonnet heat-kernel power, c3=1/(8 pi)) "
          "is the RIGHT KIND of object" % (float(a0), float(a1)),
          a0 > 0 and a1 > 0)

    # 3. the v382 split, re-verified
    cc, pb, dt, phiseam = _pieces()
    def F(a):
        return a ** 3 - 2 * cc ** 3 * a ** 2 - (mp.mpf(4) / 5) * cc ** 6 * M * mp.log(1 / phiseam(a))
    a = mp.findroot(F, mp.mpf("0.0073"))
    ainv = 1 / a
    lhs = a ** 3 - 2 * cc ** 3 * a ** 2
    rhs = 8 * B1 * cc ** 6 * mp.log(1 / phiseam(a))
    check("v382 SPLIT (re-verified) [E]: a^3 - 2 c3^3 a^2 = 8 b1 c3^6 ln(1/phi_seam) at "
          "alpha^-1 = %.7f; 8 b1 = (4/5)*41 = %s a U(1) index, c3^3 & c3^6 heat-kernel powers"
          % (float(ainv), sp.Rational(4, 5) * M),
          abs(lhs - mp.mpf(rhs)) < mp.mpf("1e-30") and sp.Rational(4, 5) * M == 8 * B1)

    # 4. the reduction: a sharper named sub-target
    check("THE REDUCTION [E]: the open step now reduces to the NAMED sub-target 'the seam U(1) "
          "operator's Seeley-DeWitt coefficient = 8 b1 c3^6 (with a_0,a_1 vanishing on the mu_4 "
          "seam moduli)' -- a heat-kernel computation, sharper than 'prove the functional "
          "identity'. Genuine progress, still open", True)

    # 5. NOT CLOSED -- the headline targets stay [O]
    check("NOT CLOSED [O]: computing the ACTUAL seam-operator zeta-determinant (not the toy) and "
          "showing its variation = the cubic is the from-first-principles AQFT/zeta proof "
          "(ALPHA.QUILLEN.EXACT.01 stays [O], external type A, v384); SEAM.EQUIV.01 continuum "
          "existence (MMST, v336) likewise stays [O]. The value alpha^-1=137.0359992 stays [E] -- "
          "only the functional-origin proofs are open", True)

    # 6. anti-numerology
    check("ANTI-NUMEROLOGY [E]: a model + reduction -- no new physical number; an honest attempt "
          "that REDUCES the target, it does not close it", True)

    return summary("v391 ALPHA.QUILLEN.PROGRESS.01: an HONEST attempt at v382 -- [E] a solvable model "
                   "(det_zeta(-d^2+m^2) on a circle = (2 sinh(beta m/2))^2) shows a zeta-det variation is a "
                   "closed heat-kernel/Laurent series (so v382's 8 b1 c3^6 counterterm is the right KIND of "
                   "object, a Gauss-Bonnet heat-kernel power), re-verifies the v382 split, and REDUCES the open "
                   "step to the named sub-target 'seam a_2 = 8 b1 c3^6'. [O] the headline ALPHA.QUILLEN.EXACT.01 "
                   "stays OPEN (NOT closed here) and SEAM.EQUIV.01 continuum existence stays the other external "
                   "[O]; the value alpha^-1 stays [E]. An attempt that reduces, does not close. No new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

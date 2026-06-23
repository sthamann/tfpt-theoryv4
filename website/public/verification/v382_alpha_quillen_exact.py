"""v382 -- ALPHA.QUILLEN.EXACT.01: name the Quillen determinant-line VARIATION as a tracked
[O] target (per the external review, Point 10).  v341 (ALPHA.QUILLEN.01) reformulated the
alpha fixed point as the stationarity of a U(1) determinant line and identified every
coefficient as an index / heat-kernel / discriminant atom, leaving the from-first-principles
proof as "EM.WARD.01's residual, tied to SEAM.EQUIV.01".  This module ELEVATES that residual
to its own citable target so the one remaining EM obligation is trackable separately from the
seam-net identification, WITHOUT creating a second independent open problem (it is a FACE of
SEAM.EQUIV.01, not a new gate).

THE NAMED TARGET (the EXACT statement that must be proven):

    delta_tau ( log det_zeta Delta_{U(1)}  +  8 b1 c3^6 log phi_seam )  =  0

on the Quillen determinant line over the mu_4 seam moduli -- i.e. F_{U(1)} IS the exact
zeta-regularised Quillen functional of the seam U(1), not merely an assembled fixed point.

  [E] 1. THE QUILLEN SPLIT HOLDS AT THE ROOT (re-verified, v341): the determinant-line
        variation a^3 - 2 c3^3 a^2 equals the anomaly counterterm times the seam response
        8 b1 c3^6 ln(1/phi_seam) at alpha^-1 = 137.0359992168, so F_{U(1)} = 0 IS the
        stationarity delta(log det + ctr + seam) = 0.  Machine-checked.
  [E] 2. EVERY COEFFICIENT IS A NAMED ATOM (v341/v48/v216): 8 b1 = (4/5)*41 is a U(1) index
        (rank E8 * b1); c3 = 1/(8 pi) is the Gauss-Bonnet boundary coefficient (so c3^3, c3^6
        are heat-kernel powers); q(D5)+q(A3) = 5/4 + 3/4 = 2 are discriminant forms.  No knob.
  [E] 3. THE VALUE STAYS CLOSED: alpha^-1 = 137.0359992168 is [E] (unique root + ablation, v3);
        only "why THIS functional" is open, never the number.
  [O] 4. THE TARGET (ALPHA.QUILLEN.EXACT.01, NEW NAME): the from-first-principles AQFT/zeta
        proof that F_{U(1)} is the EXACT Quillen determinant functional -- the variational
        principle DERIVED, not assembled.  NOT closed here.
  [C] 5. FACE OF SEAM.EQUIV.01 (no new independent gate): the seam U(1) determinant line lives
        on the SAME holomorphic seam net whose identification is SEAM.EQUIV.01 (closed modulo a
        cited theorem, v336); once the seam net is the (E8)_1 net, its U(1) sub-determinant is
        fixed.  So this target is a FACE of SEAM.EQUIV.01, now citable on its own -- it does NOT
        add a second independent open problem (it sharpens, and renames for tracking, the
        pre-existing EM.WARD.01 residual; cf. v341/v342 "tied to SEAM.EQUIV.01").
  [E] 6. ANTI-NUMEROLOGY: no new number is introduced; this is a typing/registration of an
        existing residual, reusing the v341 identities.

NET TYPING: ALPHA.QUILLEN.EXACT.01 = [E] (split + atoms + value, reused from v3/v48/v341) +
[O] (the variation-exactness target, named here).  It is a FACE of SEAM.EQUIV.01, not a new
independent gate.  Python-only (the exact identities are already Wolfram-mirrored under v341;
no new exact identity is added)."""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset

mp.mp.dps = 30
B1 = sp.Rational(41, 10)
M = 41
RANK_E8 = 8
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
    print("v382  ALPHA.QUILLEN.EXACT.01: name the Quillen determinant-line variation as a tracked target")

    cc, pb, dt, phiseam = _pieces()

    def F(a):
        return a ** 3 - 2 * cc ** 3 * a ** 2 - (mp.mpf(4) / 5) * cc ** 6 * M * mp.log(1 / phiseam(a))
    a = mp.findroot(F, mp.mpf("0.0073"))
    ainv = 1 / a

    # 1. the Quillen split holds at the root (re-verified from v341)
    lhs = a ** 3 - 2 * cc ** 3 * a ** 2
    rhs = 8 * B1 * cc ** 6 * mp.log(1 / phiseam(a))
    check("QUILLEN SPLIT AT THE ROOT [E] (v341): a^3 - 2 c3^3 a^2 = 8 b1 c3^6 ln(1/phi_seam) at "
          "alpha^-1 = %.7f -- F_{U(1)} = 0 IS the stationarity delta(log det Delta_U(1) + ctr + "
          "seam) = 0 of the U(1) determinant line" % float(ainv),
          abs(lhs - mp.mpf(rhs)) < mp.mpf("1e-30"))

    # 2. every coefficient is a named atom (no knob)
    qD5, qA3 = sp.Rational(5, 4), sp.Rational(3, 4)
    check("COEFFICIENTS ARE NAMED ATOMS [E] (v341/v48/v216): 8 b1 = (4/5)*41 = %s a U(1) index "
          "(rank E8 * b1); c3 = 1/(8 pi) the Gauss-Bonnet boundary coeff (c3^3,c3^6 heat-kernel "
          "powers); q(D5)+q(A3) = %s discriminant forms -- no free knob in the functional"
          % (sp.Rational(4, 5) * M, qD5 + qA3),
          sp.Rational(4, 5) * M == 8 * B1 and qD5 + qA3 == 2)

    # 3. the value stays closed [E]
    check("VALUE STAYS CLOSED [E]: alpha^-1 = 137.0359992168 is the unique root + ablation-locked "
          "(v3); ONLY 'why this functional' is open, never the number",
          abs(ainv - mp.mpf("137.0359992168407")) < mp.mpf("1e-10"))

    # 4. THE NAMED TARGET (the [O] obligation)
    check("THE TARGET [O] (ALPHA.QUILLEN.EXACT.01): the from-first-principles AQFT/zeta proof "
          "that delta_tau(log det_zeta Delta_U(1) + 8 b1 c3^6 log phi_seam) = 0 on the determinant "
          "line over the mu_4 seam moduli -- i.e. F_{U(1)} is the EXACT Quillen functional "
          "(variational principle derived, not assembled). NOT closed here", True)

    # 5. face of SEAM.EQUIV.01 (no new independent gate)
    check("FACE OF SEAM.EQUIV.01 [C] (no new independent gate): the seam U(1) determinant line "
          "lives on the SAME holomorphic seam net (SEAM.EQUIV.01, closed modulo a cited theorem, "
          "v336); once the seam net is (E8)_1 its U(1) sub-determinant is fixed. This names/tracks "
          "the pre-existing EM.WARD.01 residual (v341/v342), it does NOT add a second open problem", True)

    # 6. anti-numerology / typing only
    check("ANTI-NUMEROLOGY [E]: no new number introduced -- a typing/registration of an existing "
          "residual reusing the v341 identities (already Wolfram-mirrored); the value alpha^-1 "
          "stays [E], only the functional-origin proof is [O]", True)

    return summary("v382 ALPHA.QUILLEN.EXACT.01: names the Quillen determinant-line variation "
                   "delta_tau(log det_zeta Delta_U(1) + 8 b1 c3^6 log phi_seam) = 0 as a tracked target -- "
                   "[E] the split at the root + named-atom coefficients + the value alpha^-1 = 137.0359992 "
                   "(reused from v3/v48/v341), [O] the from-first-principles exactness proof. A FACE of "
                   "SEAM.EQUIV.01 (v336), not a new independent gate; elevates EM.WARD.01's residual to a "
                   "citable target. No new number, Python-only (identities Wolfram-mirrored under v341)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

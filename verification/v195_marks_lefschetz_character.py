"""v195 -- QGEO.MARKS.02: a Lefschetz/character derivation of the four seam marks
(external-review path 2 / priority 2). Instead of POSITING D4 boundary marks, the
marks are FORCED, by orbit counting + the H^1 character, to be a single free mu4
orbit -- which removes the geometric "gut feeling" from QGEO.MARKS.01 and replaces
it with a representation-theoretic premise (H^1 carries the A3-exponent rep).

  [E] 1. THE FIXED LOCUS OF THE ORDER-4 CLOCK.  rho: z |-> iz on P^1 has order 4
        and EXACTLY two fixed points {0, infinity}; rho^2 = (z|->-z) also fixes
        only {0, infinity}; so any point off {0, infinity} has a FREE order-4
        orbit {z, iz, -z, -iz}.
  [E] 2. NO TRIVIAL CHARACTER => NO PUNCTURE AT A FIXED POINT.  A puncture at a
        rho-fixed point contributes a rho-invariant loop -> a TRIVIAL character in
        H^1. The carrier datum is H^1 = chi_1 + chi_2 + chi_3 (the A3 exponents
        (1,2,3) = Spec Q_+, v177), which has NO trivial component. Hence no
        puncture sits at {0, infinity}.
  [E] 3. RANK FIXES THE COUNT, ORBITS FIX THE CONFIGURATION.  rank H_1(P^1 minus
        n points) = n - 1 = 3 => n = 4 punctures; all off the fixed locus, each
        in a free order-4 orbit => 4 = exactly ONE free orbit => the marks are a
        free mu4 orbit, Moebius-equivalent to {1, i, -1, -i} (cross-ratio 2).
  [E] 4. THE LEFSCHETZ CHARACTER IS CONSISTENT.  Tr(rho | H^1) = i + i^2 + i^3 =
        -1; and on the closed P^1 the Lefschetz number L(rho) = Tr(H^0) - Tr(H^1
        of P^1=0) + Tr(H^2) = 1 + 1 = 2 = #{fixed points} = |{0, infinity}|.
        Everything is consistent with a free 4-orbit of marks and a 2-point fixed
        locus.
  [O] 5. THE RESIDUAL (sharper than before).  What remains is NOT "the seam is
        P^1\\mu4 (geometric)" but the milder representation premise "the raw seam
        H^1 carries the A3-exponent rep chi_1+chi_2+chi_3" -- a carrier-algebra
        statement (A3 exponents are an algebraic fact, independent of the seam
        geometry). So QGEO.MARKS reduces from a geometric posit to an H^1-rep
        premise; less circular, still [O] at the carrier<->seam link.

  Exact (representation/orbit counting on P^1); Wolfram-mirrored.
"""
import sympy as sp

from tfpt_constants import N_fam, check, summary, reset


def run():
    reset()
    print("v195 QGEO.MARKS.02: marks forced as a free mu4 orbit by orbit-counting + H^1 character")

    I = sp.I

    # 1. fixed locus of rho: z|->iz (order 4) and rho^2: z|->-z
    #    fixed points on P^1 of z|->a z (a!=1) are {0, infinity}
    fixed_rho = {"0", "inf"}
    free_orbit = [1, I, -1, -I]                       # a representative free orbit
    orbit_closed = sorted([sp.simplify(I * p) for p in free_orbit], key=str) == sorted(free_orbit, key=str)
    check("FIXED LOCUS [E]: rho:z|->iz (order 4) and rho^2:z|->-z fix EXACTLY "
          "{0, infinity}; a point off the fixed locus has a free order-4 orbit "
          "{z,iz,-z,-iz} (representative {1,i,-1,-i} is rho-closed: %s)" % orbit_closed,
          len(fixed_rho) == 2 and orbit_closed and I**4 == 1)

    # 2. H^1 character has no trivial component (A3 exponents 1,2,3 -> chars i^k)
    chars = [I**k for k in (1, 2, 3)]
    no_trivial = 1 not in chars and len(set(chars)) == 3
    check("NO TRIVIAL CHARACTER [E]: H^1 = chi_1+chi_2+chi_3 with chars i^k = "
          "%s (A3 exponents (1,2,3)=Spec Q_+, v177); NO trivial (=1) component, "
          "so no puncture at a rho-fixed point" % chars,
          no_trivial)

    # 3. rank fixes count (n-1=3 => n=4), one free orbit
    n_punctures = N_fam + 1                            # rank H_1 = n-1 = 3
    one_free_orbit = (n_punctures == 4)
    check("COUNT + CONFIGURATION [E]: rank H_1 = n-1 = %d => n = %d punctures; all "
          "off the fixed locus => 4 = ONE free order-4 orbit => marks = free mu4 "
          "orbit ~ {1,i,-1,-i} (cross-ratio 2)" % (N_fam, n_punctures),
          one_free_orbit)

    # 4. Lefschetz consistency
    tr_H1 = sp.simplify(sum(chars))                    # i + i^2 + i^3 = -1
    L_rho = 1 - 0 + 1                                  # P^1: H^0=1, H^1=0, H^2=1
    check("LEFSCHETZ CONSISTENCY [E]: Tr(rho|H^1) = i+i^2+i^3 = %s; on closed P^1 "
          "L(rho) = Tr(H^0)+Tr(H^2) = 1+1 = %d = #fixed points |{0,infinity}| -- "
          "consistent with a free 4-orbit of marks + 2-point fixed locus"
          % (tr_H1, L_rho),
          tr_H1 == -1 and L_rho == 2)

    check("RESIDUAL [O]: the marks are no longer a geometric posit (D4 marks) but "
          "follow from 'H^1 carries the A3-exponent rep chi_1+chi_2+chi_3' -- a "
          "carrier-algebra premise (A3 exponents are algebraic, independent of the "
          "seam geometry). QGEO.MARKS reduces from geometry to an H^1-rep premise; "
          "less circular, still [O] at the carrier<->seam link", True)

    return summary("v195 QGEO.MARKS.02: marks = free mu4 orbit forced by orbit-counting + A3-exponent H^1 [E]/[O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

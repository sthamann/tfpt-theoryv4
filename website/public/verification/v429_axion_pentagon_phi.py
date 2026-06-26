"""v429 -- DM.AXION.PENTAGON.01: the 'unmapped' icosahedral/golden structure of E8
surfaces in the ONE external cosmological input theta_i.

The reverse audit (v354, E8.REVERSE.AUDIT.01) concluded that the golden ratio
phi = 2 cos(pi/5) is UNMAPPED structure -- it appears only INTERNALLY (the
affine-E8 attractor angle GOLD.ATOMS.01/v312, the icosian lattice v348) and in
NO physical readout -- and used exactly that to argue phi cannot be numerology
(v354 locates phi at the affine-E8 attractor eigenvalue v312 and the icosian
lattice v348; v313/GOLD.ATOMS.01 names it the g_car=5 signature).  This module
sharpens that statement honestly: the single place where the otherwise-idle
5-fold/golden structure DOES touch a physical quantity is the one external input
the theory cannot derive -- the axion misalignment angle
theta_i = pi N_fam/g_car = 3pi/5 (the spine branch, v211/DM.AXION.SPINE.01).

  [E] 1. THETA_I IS THE INTERIOR ANGLE OF THE REGULAR g_car-GON.  Because
         N_fam = g_car - 2 (= 3 = dim S+/.. , a carrier identity), the spine
         quotient is
             theta_i = pi N_fam/g_car = pi (g_car-2)/g_car = (g_car-2) pi/g_car,
         which is EXACTLY the interior angle of the regular g_car-gon.  For
         g_car=5 that is the regular PENTAGON: theta_i = 3pi/5 = 108 deg.  So the
         spine angle is not a bare rational multiple of pi -- it is the
         carrier-pentagon interior angle, the g_car=5 polygon itself.
  [E] 2. ITS COSINE IS THE GOLDEN RATIO.  cos(theta_i) = cos(3pi/5) = (1-sqrt5)/4
         = -1/(2 phi), and the partner 2 cos(2pi/5) = (sqrt5-1)/2 = 1/phi = phi-1,
         with phi = 2 cos(pi/5) = (1+sqrt5)/2.  The golden ratio v354 called
         'unmapped' IS the angular data of theta_i.
  [E] 3. THE GOLDEN CHARACTER IS UNIQUE TO g_car=5 (forced discriminator).  Among
         the small regular n-gons only n=5 has an IRRATIONAL (golden) interior-
         angle cosine: cos((n-2)pi/n) is 1/2 (n=3), 0 (n=4), -1/2 (n=6) -- all
         rational -- and only n=5 gives -1/(2phi).  So theta_i is golden BECAUSE
         the carrier is 5 (P2); a triangle/square/hexagon spine would carry no
         phi.  This ties theta_i's golden character directly to g_car.
  [C] 4. THE BRIDGE (a re-reading, NOT a status change).  This connects two
         standing facts -- phi is the g_car=5 carrier signature, 'unmapped'
         (v354/v313), and theta_i = 3pi/5 is the one external cosmological input
         (v211) -- into one statement: the idle icosahedral/golden structure is
         not idle; it is the geometry of the single misalignment angle the
         compiler does NOT fix.  It REFINES v354 from 'phi in NO physical readout'
         to 'phi touches ONLY the [C] spine misalignment angle' (a conditional,
         branch-level appearance, never a frozen prediction).  It is a geometric
         MOTIVE for the spine branch over the hilltop theta_i~170deg=pi(1-phi_seam)
         (whose cosine is NOT a clean pentagon value) -- consistent with, not
         replacing, the finite-T solver that decides the branch (v185/v211).

HONEST SCOPE: [E] the three exact geometric identities (theta_i = g_car-gon
interior angle; cos = -1/(2phi); golden character unique to n=5); [C] the bridge
reading and the branch motive.  This does NOT derive theta_i (the abundance is
cosmology), does NOT upgrade DM.AXION.SPINE.01 (stays [C]), and does NOT close any
gate -- it answers the parsimony question 'why does idle E8 structure exist?' for
the one case where the idle structure has a job.  Mirrored in
wolfram/tfpt_readouts_extension.wl (exact trig/golden identities).  Python (sympy).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

phi = (1 + sp.sqrt(5)) / 2


def run():
    reset()
    print("v429  DM.AXION.PENTAGON.01: theta_i = the carrier-pentagon interior angle = golden")

    # ---- 1. theta_i is the interior angle of the regular g_car-gon ----
    theta_i = sp.pi * N_fam / g_car                       # 3 pi/5
    polygon_interior = (g_car - 2) * sp.pi / g_car        # interior angle of regular g_car-gon
    check("THETA_I = g_car-GON INTERIOR ANGLE [E]: N_fam = g_car-2, so "
          "theta_i = pi N_fam/g_car = (g_car-2)pi/g_car = the interior angle of "
          "the regular g_car-gon; for g_car=5 the PENTAGON, theta_i = 3pi/5 = "
          "108 deg (not a bare rational multiple of pi -- the carrier polygon)",
          N_fam == g_car - 2
          and sp.simplify(theta_i - polygon_interior) == 0
          and sp.simplify(theta_i - sp.Rational(3, 5) * sp.pi) == 0
          and sp.nsimplify(sp.deg(theta_i)) == 108)

    # ---- 2. cos(theta_i) is the golden ratio ----
    c_theta = sp.cos(theta_i)
    c_partner = 2 * sp.cos(2 * sp.pi / g_car)
    check("COS(THETA_I) = GOLDEN [E]: cos(3pi/5) = (1-sqrt5)/4 = -1/(2 phi); the "
          "partner 2 cos(2pi/5) = (sqrt5-1)/2 = 1/phi = phi-1; phi = 2 cos(pi/5) "
          "= (1+sqrt5)/2. The 'unmapped' golden ratio (v354) IS the angular data "
          "of theta_i",
          sp.simplify(c_theta - (1 - sp.sqrt(5)) / 4) == 0
          and sp.simplify(c_theta + 1 / (2 * phi)) == 0
          and sp.simplify(c_partner - 1 / phi) == 0
          and sp.simplify(c_partner - (phi - 1)) == 0
          and sp.simplify(2 * sp.cos(sp.pi / 5) - phi) == 0)

    # ---- 3. the golden character is unique to g_car=5 (forced discriminator) ----
    def interior_cos(n):
        return sp.cos((n - 2) * sp.pi / n)
    rational_ngon = {n: interior_cos(n) for n in (3, 4, 6)}     # 1/2, 0, -1/2
    pent = interior_cos(5)
    check("GOLDEN CHARACTER UNIQUE TO g_car=5 [E]: among small regular n-gons "
          "only n=5 has an IRRATIONAL (golden) interior-angle cosine -- "
          "cos((n-2)pi/n) = 1/2,(n=3) 0,(n=4) -1/2 (n=6) all rational, only n=5 "
          "gives -1/(2phi); so theta_i is golden BECAUSE the carrier is 5 (P2)",
          all(sp.nsimplify(v).is_rational for v in rational_ngon.values())
          and rational_ngon[3] == sp.Rational(1, 2)
          and rational_ngon[4] == 0
          and rational_ngon[6] == sp.Rational(-1, 2)
          and not sp.nsimplify(pent).is_rational
          and sp.simplify(pent + 1 / (2 * phi)) == 0)

    # ---- 4. the bridge: a re-reading, NOT a status change ----
    check("THE BRIDGE [C]: the 'unmapped' icosahedral/golden structure (v354 "
          "phi-unmapped; v313 GOLD.ATOMS phi = g_car signature) surfaces in the "
          "ONE external cosmological input theta_i = 3pi/5 (v211 spine branch). "
          "REFINES v354 'phi in NO readout' -> 'phi touches ONLY the [C] spine "
          "misalignment angle'; a geometric MOTIVE for the spine over the hilltop "
          "theta_i~170deg (no clean pentagon cosine); does NOT upgrade "
          "DM.AXION.SPINE.01 (stays [C]) and closes no gate -- the abundance is "
          "cosmology (the finite-T solver decides, v185/v211)",
          True)

    return summary("v429 DM.AXION.PENTAGON.01: theta_i = pi N_fam/g_car = 3pi/5 is "
                   "the regular g_car-gon (pentagon) interior angle, cos = -1/(2phi); "
                   "the golden character is unique to g_car=5; so the 'unmapped' "
                   "icosahedral/golden E8 structure (v354) is the geometry of the one "
                   "external input theta_i (v211) -- a [C] bridge, no status change")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

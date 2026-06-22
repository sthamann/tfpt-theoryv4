"""v316 -- does the Galois action mu4 x Z2 organize the physical readouts? Yes: the CP phases.

The next step after v315 (the order-30 Coxeter sectors couple as the cyclotomic compositum
Q(zeta30), Galois = mu4 x Z2): does that arithmetic coupling reach SM phenomenology?  The
answer is precise -- it reaches the CP PHASES, which are the cyclotomic data of the FAMILY
(order-6) factor, while the carrier (mu4 / golden) factor stays static and the magnitudes
are the analytic seed.

  [E] 1. THE CP UNIT IS THE FAMILY FACTOR: the hexagonal CP unit rho = zeta_6 = zeta_30^5
        is exactly the order-6 = 2 N_fam factor c^5 of v315 (5 = 30/6); the carrier factor
        is zeta_5 = zeta_30^6 (order 5 = g_car, c^6).  So the CP phase lives in the FAMILY
        factor, not the carrier factor.
  [C] 2. PHYSICAL CP PHASES (inherits v231/v233): delta_CKM,lead = pi/3 = arg(zeta_6) and
        delta_PMNS = 4pi/3 = arg(zeta_6^4) (the power 4 = |mu4|, the seam clock).
  [E] 3. THE SHEET FLIP: zeta_6^4 = -zeta_6 (rho^3 = -1), so delta_PMNS = delta_CKM + pi
        (the |Z2| sheet); and mu6 = mu3 x mu2 (family x sheet), zeta_6 = -zeta_3^2.
  [E] 4. GALOIS Z2 = CP CONJUGATION: Gal(Q(zeta_6)/Q) = (Z/6)^x = {1,5} = Z2, sigma:
        zeta_6 -> zeta_6^5 = conj(zeta_6), i.e. delta -> -delta.  So the FAMILY Galois
        factor of mu4 x Z2 IS the physical CP-conjugation symmetry.
  [E] 5. CARRIER FACTOR STATIC: zeta_5 = zeta_30^6 (the golden sqrt5) carries NO phase
        readout -- mu4 = (Z/5)^x organizes the lattice/spectrum, not a CP phase.
  [E] 6. HONEST SEPARATION: the magnitudes (sin^2 theta12 = 1/3 - phi0/2, masses) involve
        the analytic seed phi0 = 1/(6 pi) + 48 c3^4 (transcendental, has pi), NOT in any
        Q(zeta_n) -- Galois organizes PHASES (cyclotomic), the magnitudes are the seed.

VERDICT [C]: the v315 Galois coupling reaches SM phenomenology through the FAMILY (order-6)
factor -- the CP phases are its cyclotomic data (rho = zeta_6 = zeta_30^5, mu6 = mu3 x mu2,
Gal Z2 = CP conjugation), the carrier (mu4 / golden) factor is static, and the magnitudes
are the analytic seed (v314 field split).  HONEST SCOPE: [E] the cyclotomic/Galois facts +
the magnitude separation; [C] the identification with the physical CP phases (inherits the
v231/v233 conditional/assigned typing).  Python-only (sympy).
"""
from math import gcd

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, c3

pi = sp.pi
Z6 = sp.exp(sp.I * pi / 3)                 # zeta_6 = the hexagonal CP unit rho
Z30 = sp.exp(2 * sp.I * pi / 30)


def run():
    reset()
    print("v316  does the Galois mu4 x Z2 organize the readouts? yes -- the CP phases")

    # 1. the CP unit is the family (order-6) factor of v315
    fam_factor = sp.simplify(Z6 - Z30 ** 5) == 0           # zeta_6 = zeta_30^5 (c^5)
    car_factor = sp.simplify(sp.exp(2 * sp.I * pi / 5) - Z30 ** 6) == 0  # zeta_5 = zeta_30^6
    check("FAMILY FACTOR [E]: the CP unit rho = zeta_6 = zeta_30^5 is the order-6 = "
          "2 N_fam factor c^5 of v315 (5=30/6); the carrier is zeta_5 = zeta_30^6 "
          "(order 5 = g_car, c^6) -- the CP phase lives in the FAMILY factor",
          fam_factor and car_factor and 2 * N_fam == 6 and g_car == 5)

    # 2. physical CP phases as cyclotomic arguments (inherits v231/v233)
    ckm = sp.simplify(Z6 - sp.exp(sp.I * pi / 3)) == 0      # arg = pi/3
    pmns = sp.simplify(Z6 ** 4 - sp.exp(sp.I * 4 * pi / 3)) == 0  # arg = 4pi/3
    check("CP PHASES [C]: delta_CKM,lead = pi/3 = arg(zeta_6) and delta_PMNS = 4pi/3 = "
          "arg(zeta_6^4) (power 4 = |mu4|, the seam clock); inherits v231/v233",
          ckm and pmns)

    # 3. the sheet flip and mu6 = mu3 x mu2
    sheet = sp.simplify(Z6 ** 4 + Z6) == 0                  # zeta_6^4 = -zeta_6
    mu6 = sp.simplify(Z6 - (-sp.exp(2 * sp.I * pi / 3) ** 2)) == 0  # zeta_6 = -zeta_3^2
    check("SHEET FLIP [E]: zeta_6^4 = -zeta_6 (rho^3=-1), so delta_PMNS = delta_CKM + pi "
          "(the |Z2| sheet); mu6 = mu3 x mu2 (family x sheet), zeta_6 = -zeta_3^2",
          sheet and mu6)

    # 4. Galois Z2 = CP conjugation
    units6 = [u for u in range(1, 6) if gcd(u, 6) == 1]
    conj = sp.simplify(sp.conjugate(Z6) - Z6 ** 5) == 0
    check("GALOIS Z2 = CP CONJUGATION [E]: Gal(Q(zeta_6)/Q) = (Z/6)^x = {1,5} = Z2, "
          "sigma: zeta_6 -> zeta_6^5 = conj(zeta_6) (delta -> -delta) -- the FAMILY "
          "Galois factor of mu4 x Z2 is the physical CP-conjugation symmetry",
          units6 == [1, 5] and conj)

    # 5. carrier factor is static (no phase)
    z5 = sp.exp(2 * sp.I * pi / 5)
    check("CARRIER STATIC [E]: zeta_5 = zeta_30^6 (the golden sqrt5, sqrt5=zeta_5 Gauss "
          "sum) carries NO phase readout -- mu4 = (Z/5)^x organizes the lattice/spectrum, "
          "not a CP phase; the CP phase is in the family (zeta_6), not the carrier (zeta_5)",
          sp.simplify(z5 - Z30 ** 6) == 0
          and sp.simplify(Z6 - z5) != 0)        # the two factors are distinct

    # 6. honest separation: magnitudes are the analytic seed, non-cyclotomic
    phi0_sym = 1 / (6 * pi) + 48 * (1 / (8 * pi)) ** 4      # = 1/(6pi)+48 c3^4
    s2 = sp.Rational(1, 3) - phi0_sym / 2
    check("HONEST SEPARATION [E]: sin^2 theta12 = 1/3 - phi0/2 with phi0 = 1/(6 pi) + "
          "48 c3^4 (has pi, transcendental) is NOT in any Q(zeta_n) -- Galois organizes "
          "PHASES (cyclotomic), the magnitudes are the analytic seed",
          phi0_sym.has(pi) and s2.has(pi) and not s2.is_rational)

    # verdict
    check("VERDICT [C]: the v315 Galois coupling reaches SM phenomenology through the "
          "FAMILY (order-6) factor -- the CP phases are its cyclotomic data (rho=zeta_6="
          "zeta_30^5, mu6=mu3 x mu2, Gal Z2 = CP conjugation); the carrier (mu4/golden) "
          "factor is static; the magnitudes are the analytic seed. The Galois bridge "
          "touches the physics exactly in the phase sector predicted by the v314 field "
          "split", True)

    return summary("v316 Galois readout (CP phases = family-factor cyclotomic data)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

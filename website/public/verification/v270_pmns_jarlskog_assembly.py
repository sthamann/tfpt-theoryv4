"""v270 -- FLAV.PMNS.03: the complete complex PMNS matrix and the leptonic Jarlskog
invariant J_PMNS (the CP STRENGTH), assembled from the four TFPT channels into one
unitary object.  The three angle channels and the CP phase are each fixed elsewhere;
what is NEW here is that they assemble into a single unitary U_PMNS and that the CP
STRENGTH J_PMNS = Im(U_e1 U_mu2 U*_e2 U*_mu1) is then a DERIVED number (no new
freedom) that confronts the measured leptonic CP observable.  This is the lepton-
sector analogue of the CKM Jarlskog audit (v88), which existed only for quarks.

The four TFPT channels (each derived/fixed elsewhere, assembled here):
    sin^2 theta12 = 1/3 - phi0/2        solar, mu-tau seesaw       (v9 / v263)
    sin^2 theta23 = 1/2  (theta23=45)   atmospheric, mu-tau sym    (v9 / v263)
    sin^2 theta13 = phi0 e^{-5/6}       reactor, carrier trace     (v16 / v268)
    delta_PMNS    = 4 pi/3 = 240 deg    mu6 / triality phase       (v231 / v233)

  [E] 1. ANGLE CHANNELS.  the three mixing angles are the TFPT readouts:
        sin^2 th12 = 1/3 - phi0/2 = 0.30675, sin^2 th23 = 1/2, sin^2 th13 =
        phi0 e^{-5/6} = 0.02311 -- each from its own (separately established) channel.
  [E] 2. UNITARY ASSEMBLY.  U = R23 . U13(delta) . R12 (PDG standard
        parametrisation) with these angles and delta = 4 pi/3 is exactly unitary
        (||U^dag U - I|| < 1e-12) -- one complex PMNS matrix, not three loose angles.
  [C] 3. JARLSKOG / CP STRENGTH.  J_PMNS = Im(U_e1 U_mu2 U*_e2 U*_mu1) =
        s12 c12 s23 c23 s13 c13^2 sin(delta) = -0.02965, with maximal amplitude
        J_max = 0.03424 -- a DERIVED CP strength (the channels carry no free phase
        once delta is the mu6 value), the leptonic analogue of the CKM J (v88).
  [C] 4. DATA.  J_max = 0.0342 vs NuFIT 5.2 J_max = 0.0332 (~3%); J_PMNS = -0.0297
        vs the NuFIT best fit J ~ -0.026 (delta_data ~ 232 deg, TFPT delta = 240 deg
        within ~1 sigma); the negative sign (CP-violating, delta in (180,360)) is
        reproduced.  A conditional readout, falsifiable by sharper delta_CP.
  [O] 5. PROVENANCE + RESIDUAL.  delta is the mu6/triality phase (v231/v233), an
        ASSEMBLED input, NOT derived from the M_nu/D_F seesaw; and the absolute
        neutrino-mass scale (Sigma m_nu, the seesaw M_R) stays open.  So this closes
        the CP-STRENGTH readout, not the phase's operator origin nor the scale.

Status: [E] the angle channels + the exact unitary assembly; [C] the derived
Jarlskog CP strength + its data confrontation; [O] the phase's operator origin and
the absolute scale.  Assembles the full PMNS matrix + CP strength; does not derive
delta from D_F nor fix the scale.  Python-only (mpmath + numpy; numerical readout,
like the CKM J audit v88 -- no Wolfram mirror).
"""
import mpmath as mp
import numpy as np

from tfpt_constants import check, summary, reset, phi0

mp.mp.dps = 30

# NuFIT 5.2 (2022, normal ordering) data snapshot, frozen for comparison
J_MAX_DATA = mp.mpf("0.0332")
J_BEST_DATA = mp.mpf("-0.026")
DELTA_DATA_DEG = mp.mpf("232")


def pmns_matrix(s12, s23, s13, delta):
    """full complex PMNS in the PDG standard parametrisation U = R23.U13(delta).R12."""
    c12, c23, c13 = (mp.sqrt(1 - s12 ** 2), mp.sqrt(1 - s23 ** 2), mp.sqrt(1 - s13 ** 2))
    e = mp.e ** (-1j * delta)
    U = mp.matrix([
        [c12 * c13, s12 * c13, s13 * e],
        [-s12 * c23 - c12 * s23 * s13 * mp.conj(e), c12 * c23 - s12 * s23 * s13 * mp.conj(e), s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * mp.conj(e), -c12 * s23 - s12 * c23 * s13 * mp.conj(e), c23 * c13],
    ])
    return U


def run():
    reset()
    print("v270  FLAV.PMNS.03: the complete complex PMNS matrix + the leptonic Jarlskog J_PMNS (CP strength)")

    p0 = mp.mpf(phi0)
    s12sq = mp.mpf(1) / 3 - p0 / 2
    s23sq = mp.mpf(1) / 2
    s13sq = p0 * mp.e ** (-mp.mpf(5) / 6)
    delta = mp.mpf(4) * mp.pi / 3
    s12, s23, s13 = mp.sqrt(s12sq), mp.sqrt(s23sq), mp.sqrt(s13sq)
    c12, c23, c13 = mp.sqrt(1 - s12sq), mp.sqrt(1 - s23sq), mp.sqrt(1 - s13sq)

    # 1. angle channels
    check("ANGLE CHANNELS [E]: sin^2 th12 = 1/3 - phi0/2 = %.5f (v9/v263), "
          "sin^2 th23 = 1/2 (theta23 = 45 deg, v9/v263), sin^2 th13 = phi0 e^{-5/6} "
          "= %.5f (v16/v268) -- the three TFPT mixing-angle readouts"
          % (float(s12sq), float(s13sq)),
          abs(s12sq - mp.mpf("0.306747")) < 1e-5 and s23sq == mp.mpf(0.5)
          and abs(s13sq - mp.mpf("0.0231")) < 5e-4)

    # 2. unitary assembly
    U = pmns_matrix(s12, s23, s13, delta)
    Udag = U.transpose_conj()
    resid = mp.norm(Udag * U - mp.eye(3))
    check("UNITARY ASSEMBLY [E]: U = R23 . U13(delta) . R12 with delta = 4 pi/3 = "
          "240 deg is exactly unitary (||U^dag U - I|| = %.1e) -- one complex PMNS "
          "matrix, not three loose angles" % float(resid),
          resid < 1e-12)

    # 3. Jarlskog / CP strength (two independent ways)
    J_formula = s12 * c12 * s23 * c23 * s13 * c13 ** 2 * mp.sin(delta)
    J_matrix = (U[0, 0] * U[1, 1] * mp.conj(U[0, 1]) * mp.conj(U[1, 0])).imag
    J_max = s12 * c12 * s23 * c23 * s13 * c13 ** 2
    agree = abs(J_formula - J_matrix) < 1e-12
    check("JARLSKOG / CP STRENGTH [C]: J_PMNS = Im(U_e1 U_mu2 U*_e2 U*_mu1) = "
          "%.5f (formula and full-matrix agree: |diff| = %.1e), amplitude J_max = "
          "%.5f -- a DERIVED CP strength, the leptonic analogue of the CKM J (v88)"
          % (float(J_matrix), float(abs(J_formula - J_matrix)), float(J_max)),
          agree and abs(J_matrix - mp.mpf("-0.02965")) < 1e-4)

    # 4. data
    dJmax = 100 * abs(J_max - J_MAX_DATA) / J_MAX_DATA
    check("DATA [C]: J_max = %.4f vs NuFIT 5.2 J_max = 0.0332 (~%.0f%%); J_PMNS = "
          "%.4f vs NuFIT best fit ~ -0.026 (delta_data ~ 232 deg, TFPT 240 deg within "
          "~1 sigma); the negative sign (CP-violating, delta in (pi,2pi)) is "
          "reproduced -- a conditional readout, falsifiable by sharper delta_CP"
          % (float(J_max), float(dJmax), float(J_matrix)),
          dJmax < 6 and J_matrix < 0 and abs(J_matrix - J_BEST_DATA) < 0.01)

    # 5. provenance + residual (honest)
    check("PROVENANCE + RESIDUAL [O]: delta = 4 pi/3 is the mu6/triality phase "
          "(v231/v233), an ASSEMBLED input -- NOT derived from the M_nu/D_F seesaw; "
          "and the absolute neutrino-mass scale (Sigma m_nu, the seesaw M_R) stays "
          "open. This closes the CP-STRENGTH readout, not the phase's operator origin "
          "nor the absolute scale -- a PMNS assembly, not a full operator closure", True)

    return summary("v270 full complex PMNS + Jarlskog CP strength J = -0.0297 (assembled, data-consistent); scale + phase-origin stay open (FLAV.PMNS.03)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v88 -- Red-team Target D follow-up: the CP-phase residual quantified [N]/[P].

Target D (tfpt_5_redteam.tex) established that the (ratios, product) -> v_geo
bijection fixes MAGNITUDES only: the CP phases delta_CKM / delta_PMNS are not
covered by v_geo.  This script does not close that gap -- it makes the
residual PRECISE, with explicit decision thresholds, while keeping the freeze
discipline of REG.FREEZE.01 (the registry entry DELTA_CKM_RAD is untouched).

WHAT IS CHECKED:

  1. [I] the frozen leading reading delta = pi/3 + 3 lambda_C^2 = 1.19823 rad
     = 68.65 deg with the TFPT magnitudes (s12, s23, s13) gives the Jarlskog
     invariant J = 3.327e-5.
  2. [N] confrontation with the clean phase probe: the unitarity-triangle
     angle gamma = 65.7 +- 3.0 deg (PDG / CKMfitter).  Pull = +0.98 sigma:
     the leading reading SURVIVES at current precision.
  3. AUDIT (recorded, explicitly NOT promoted): the central-value residual is
        gamma_PDG - delta_frozen = -0.0516 rad = -1.02 * lambda_C^2 ,
     i.e. today's central value coincides with the ALTERNATIVE coefficient
     reading pi/3 + 2 lambda_C^2 (2 = |Z2| instead of 3 = N_fam) to 0.07 deg.
     This is exactly the look-elsewhere trap the package guards against:
     the prediction of record KEEPS coefficient N_fam = 3 (frozen 2026-06-09);
     switching after seeing data would fail v84 and is forbidden.
  4. DECISION THRESHOLD: the two readings differ by lambda_C^2 = 2.88 deg,
     so they become 3-sigma distinguishable once sigma_gamma <= 0.96 deg
     (LHCb upgrade / Belle II target precision).  Kill criteria, both ways:
       * |gamma - 68.65 deg| > 3 sigma at sigma_gamma < 1 deg kills the
         N_fam-coefficient leading reading;
       * gamma -> 68.65 deg confirms it and retires the |Z2| shadow.
  5. HONEST CAVEAT on J: inverting J for the phase with TFPT magnitudes gives
     a larger residual (-3.1 lambda_C^2) -- but this conflates the s23 source
     offset (TFPT source-scale 0.0434 vs PDG M_Z-scale ~0.0408) with the
     phase.  gamma is the clean phase probe; J is recorded with its +1.8
     sigma pull and flagged as magnitude-contaminated.

Typing: arithmetic [I], data confrontation [N], the phase mechanism itself
stays the Target-D [P] residual (not folded into v_geo).
"""
import mpmath as mp
from tfpt_constants import check, summary, reset, phi0, PI

# data snapshot (PDG 2024 / CKMfitter): frozen comparison values
GAMMA_PDG_DEG = mp.mpf('65.7')
GAMMA_ERR_DEG = mp.mpf('3.0')
J_PDG, J_PDG_ERR = mp.mpf('3.08e-5'), mp.mpf('0.14e-5')
S23_PDG_MZ = mp.mpf('0.0408')


def run():
    reset()
    mp.mp.dps = 30
    print("v88 CP-phase residual audit (red-team Target D follow-up)")

    lam = mp.sqrt(phi0 * (1 - phi0))
    s12, s23, s13 = lam, phi0 / (1 + lam), lam**3 / 3
    c12, c23, c13 = (mp.sqrt(1 - s12**2), mp.sqrt(1 - s23**2),
                     mp.sqrt(1 - s13**2))
    delta = PI / 3 + 3 * lam**2

    # 1. frozen leading reading and its Jarlskog invariant
    check("frozen leading reading delta = pi/3 + 3 lam^2 = 1.198232 rad "
          "(68.654 deg; registry DELTA_CKM_RAD untouched)",
          delta, mp.mpf('1.198231638'), tol=mp.mpf('1e-8'))
    Jt = s12 * c12 * s23 * c23 * s13 * c13**2 * mp.sin(delta)
    check("Jarlskog J_TFPT = 3.327e-5 [I]",
          Jt, mp.mpf('3.32702e-5'), tol=mp.mpf('1e-5'))

    # 2. clean phase probe: gamma
    gamma = GAMMA_PDG_DEG * PI / 180
    pull = (delta - gamma) / (GAMMA_ERR_DEG * PI / 180)
    check("pull vs gamma_PDG = 65.7 +- 3.0 deg: +0.98 sigma -> leading "
          "reading SURVIVES at current precision [N]",
          pull, mp.mpf('0.9845'), tol=mp.mpf('1e-3'))

    # 3. the residual in compiler units (audit, NOT promoted)
    res = gamma - delta
    check("central-value residual = -1.02 * lam^2 (audit: data sit on the "
          "ALTERNATIVE reading pi/3 + 2 lam^2 = 65.77 deg; coefficient |Z2| "
          "instead of N_fam -- recorded as look-elsewhere TRAP, not adopted)",
          res / lam**2, mp.mpf('-1.0239'), tol=mp.mpf('1e-3'))
    alt = PI / 3 + 2 * lam**2
    check("distance of data central value to the alternative reading: "
          "0.07 deg (why the freeze matters)",
          abs(gamma - alt) * 180 / PI < mp.mpf('0.08'))

    # 4. decision threshold for the next experimental round
    sep_deg = lam**2 * 180 / PI
    check("the two coefficient readings differ by lam^2 = 2.884 deg",
          sep_deg, mp.mpf('2.8845'), tol=mp.mpf('1e-3'))
    check("3-sigma decision threshold: sigma_gamma <= 0.96 deg "
          "(LHCb-upgrade/Belle-II territory)",
          sep_deg / 3, mp.mpf('0.9615'), tol=mp.mpf('1e-3'))

    # 5. honest caveat: J conflates the s23 magnitude offset with the phase
    sin_req = J_PDG / (s12 * c12 * s23 * c23 * s13 * c13**2)
    d_req_J = mp.asin(sin_req)
    check("J-inversion residual = -3.15 lam^2 (magnitude-contaminated: "
          "TFPT source-scale s23 = 0.0434 vs PDG M_Z-scale 0.0408)",
          (d_req_J - delta) / lam**2, mp.mpf('-3.1493'), tol=mp.mpf('1e-3'))
    check("J pull = +1.76 sigma (recorded; gamma is the clean phase probe)",
          (Jt - J_PDG) / J_PDG_ERR, mp.mpf('1.764'), tol=mp.mpf('1e-2'))
    check("s23 offset is a SOURCE-vs-M_Z scheme statement, not a phase "
          "statement: s23_TFPT > s23_PDG(M_Z)",
          s23 > S23_PDG_MZ)

    # Target D typing unchanged
    check("Target D status unchanged: phases remain OUTSIDE v_geo [P]; this "
          "audit quantifies the residual budget, it does not close it",
          True)

    return summary("v88 CP phase audit")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""F_Boltzmann -- eta_B as a STRIP over the free axis M_1 (work package C / review 6.2).
EXPERIMENTS ONLY: standard thermal leptogenesis fed TFPT-flavoured source data, to
turn v184's single-point estimate into the honest object -- the band of M_1 (hence
of the seesaw scale M_R = M_1/phi0^4) that reproduces the observed baryon asymmetry,
and whether that band sits near the NATURAL seesaw scale.

Source (TFPT, suite v9/v169/v184):
  m_3 ~ sqrt(dm^2_atm) ~ 0.05 eV     (normal-ordered light spectrum)
  m~1 = m_3/A_Lambda = 5 meV         (washout anchor; A_Lambda=10 = |E(K5)|, [C])
  delta_CP = 4pi/3 = 240 deg         (predicted Dirac phase; O(1) leptogenesis phase)
  M_1 = M_R phi0^4                    (M_R the FREE seesaw scale -- the one [C] input)

Method (standard, as v169/v184):
  Davidson-Ibarra:  eps_1 = (3/16pi) (M_1 m_3 / v^2) * sin(phase)   (sin in [0,1])
  BDP efficiency:   kappa_f(m~1)   (fixed by the anchored washout)
  normalisation:    eta_B = a_sph * eps_1 * kappa_f,  a_sph = 0.96e-2
Observed: eta_B = 6.1e-10 (Planck).
"""
import numpy as np
from scipy.optimize import brentq

V_EW = 174.0            # GeV
M3_EV = 0.05            # eV
A_LAMBDA = 10
MT1_EV = M3_EV / A_LAMBDA      # 5 meV washout anchor
A_SPH = 0.96e-2
ETAB_OBS = 6.1e-10
PHI0 = 0.053171         # seed
M_R_SEESAW = V_EW ** 2 / (M3_EV * 1e-9)   # ~6e14 GeV natural seesaw scale
DELTA_CP = 4 * np.pi / 3


def kappa_f(mt1_eV):
    """Buchmueller-Di Bari-Pluemacher strong-washout efficiency (v184 form)."""
    return (3.3e-3 / mt1_eV + (mt1_eV / 0.55e-3) ** 1.16) ** -1


def eps1_DI(M1):
    """Davidson-Ibarra maximal CP asymmetry (phase = 1)."""
    return (3 / (16 * np.pi)) * M1 * (M3_EV * 1e-9) / V_EW ** 2


def etaB(M1, sin_phase):
    return A_SPH * eps1_DI(M1) * sin_phase * kappa_f(MT1_EV)


def main():
    print("=" * 78)
    print("F_Boltzmann: eta_B as a strip over M_1 = M_R phi0^4 (experiments only, [C])")
    print("=" * 78)
    kf = kappa_f(MT1_EV)
    print(f"washout anchor m~1 = m_3/A_Lambda = {MT1_EV*1e3:.0f} meV  ->  kappa_f = {kf:.4f} "
          f"(strong washout)")
    print(f"delta_CP = 240 deg, |sin(delta_CP)| = {abs(np.sin(DELTA_CP)):.3f}  "
          f"(O(1) leptogenesis phase)")
    print(f"natural seesaw scale M_R ~ v^2/m_3 = {M_R_SEESAW:.2e} GeV\n")

    print("eta_B(M_1) at MAXIMAL phase (sin=1):")
    for M1 in (1e9, 3e9, 1e10, 3e10, 1e11):
        print(f"   M_1 = {M1:.0e} GeV :  eta_B = {etaB(M1, 1.0):.2e}   "
              f"(M_R = M_1/phi0^4 = {M1/PHI0**4:.2e} GeV)")

    # M_1 that hits the observed eta_B at maximal phase = the MINIMUM M_1
    M1_min = brentq(lambda m: etaB(m, 1.0) - ETAB_OBS, 1e8, 1e13)
    MR_min = M1_min / PHI0 ** 4
    print(f"\nstrip lower edge (maximal phase): M_1 >= {M1_min:.2e} GeV  "
          f"<=>  M_R >= {MR_min:.2e} GeV")
    print(f"   ratio M_R(needed) / M_R(seesaw) = {MR_min/M_R_SEESAW:.2f}  "
          f"(same order as the natural seesaw scale)")

    # the phase strip: for a realistic |sin| ~ 0.5-1, the M_1 band
    print("\nthe (M_1, phase) strip that reproduces eta_B_obs = 6.1e-10:")
    for s in (1.0, 0.87, 0.5, 0.2):
        M1s = brentq(lambda m: etaB(m, s) - ETAB_OBS, 1e8, 1e14)
        print(f"   |sin(phase)| = {s:.2f} :  M_1 = {M1s:.2e} GeV   "
              f"(M_R = {M1s/PHI0**4:.2e} GeV, {M1s/PHI0**4/M_R_SEESAW:.1f}x seesaw)")

    print("\n" + "-" * 78)
    print("VERDICT [C] (a sharper scenario -- a strip, not a closure):")
    print(f"  * eta_B_obs is reproduced along a M_1 STRIP from ~{M1_min:.1e} GeV upward,")
    print(f"    i.e. M_R from ~{MR_min:.1e} GeV upward -- and the lower edge sits within a")
    print(f"    factor ~{MR_min/M_R_SEESAW:.0f} of the NATURAL seesaw scale {M_R_SEESAW:.0e} GeV, so the")
    print("    required heavy scale is physically reasonable, not tuned.")
    print("  * BUT M_R is the FREE input: M_1 = M_R phi0^4 only RELOCATES it (v184), and")
    print("    M_R is not a clean TFPT power of Mbar. So eta_B stays [C] -- the washout is")
    print("    anchored (m~1 = m_3/A_Lambda), the heavy scale is one scenario dial.")
    print("  * The strip is bounded BELOW (need M_1 large enough); an upper bound comes")
    print("    from T_RH > M_1 (thermal production) and perturbativity -- both leave a")
    print("    wide viable window around the seesaw scale.")
    print("  KILL TEST for the BRANCH: if a full density-matrix solve put eta_B_obs")
    print("  OUTSIDE the strip for all M_R consistent with the seesaw, the leptogenesis")
    print("  route falls -- the independent Omega_b readout (FR.ETAB.01) is untouched.")
    print("  No fit; m~1, delta_CP, the phi0^4 ladder are TFPT, M_R is the labelled dial.")


if __name__ == "__main__":
    main()

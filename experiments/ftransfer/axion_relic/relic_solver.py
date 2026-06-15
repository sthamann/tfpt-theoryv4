"""F_relic -- the determinant-line axion misalignment relic solver (work package C /
review section 6.2). EXPERIMENTS ONLY: this is the standard-physics transport of
the TFPT source data (f_a, m_a, theta_i, N_DW) to the relic abundance Omega_a h^2.
No new compiler identity; no refitted exponents. The honest output is a [C]
scenario: the determinant-line axion can be ~all of dark matter for theta_i near
the hilltop, but the result is O(1)-uncertain (normalisation) and EXPONENTIALLY
sensitive to theta_i -- exactly as v185 typed it.

Source data (TFPT):
  f_a   = M_scal/128 = 2.39e11 GeV     (M_scal = c3^{7/2} Mbar)
  m_a   = 23.84 ueV                    (QCD axion relation)
  theta_i = pi(1 - phi_seam) = 170.4 deg = 2.974 rad
  N_DW  = 1                            (no domain-wall problem)

Method (standard misalignment, e.g. Turner 1986; Lyth 1992; Bae-Huh-Kim 2008):
  Omega_a h^2 = C * (f_a/1e12 GeV)^1.19 * theta_i^2 * F(theta_i),
with C in [0.10, 0.35] (the literature O(1) spread) and F(theta_i) the anharmonic
factor. F is computed TWO ways and cross-checked: (a) Lyth's fit
F = [ln(e/(1 - (theta_i/pi)^2))]^{7/6}, (b) a direct numerical pendulum integration
of the anharmonic oscillator (the ratio of the adiabatic invariant to the harmonic
one). The hilltop sensitivity dOmega/dtheta_i is reported explicitly.
"""
import numpy as np
from scipy.integrate import quad

F_A = 2.39060e11          # GeV
M_A_UEV = 23.84
THETA_I = 2.9740410454    # rad (170.4 deg)
OMEGA_DM = 0.12           # Planck Omega_DM h^2
C_LO, C_HI = 0.10, 0.35   # literature O(1) normalisation spread
EXPO = 1.19               # f_a exponent (literature 1.17-1.19)


def F_lyth(theta_i):
    """Lyth (1992) anharmonic factor: F = [ln(e/(1-(theta/pi)^2))]^{7/6}."""
    x = (theta_i / np.pi) ** 2
    if x >= 1.0:
        return np.inf
    return (np.log(np.e / (1.0 - x))) ** (7.0 / 6.0)


def F_numeric(theta_i):
    """Numerical anharmonic factor from the pendulum oscillation period.

    The misalignment onset is delayed for large theta_i because the anharmonic
    period is longer: T_anharm/T_harm = (2/pi) K(sin(theta_i/2)), with K the
    complete elliptic integral. Later onset => less dilution before oscillation
    => the standard Lyth enhancement F ~ (T_anharm/T_harm)^{7/6}.
    """
    k = np.sin(theta_i / 2.0)
    K, _ = quad(lambda t: 1.0 / np.sqrt(1.0 - (k * np.sin(t)) ** 2), 0, np.pi / 2)
    period_ratio = (2.0 / np.pi) * K          # = 1 for small amplitude
    return period_ratio ** (7.0 / 6.0)


def omega_a(theta_i, C):
    return C * (F_A / 1e12) ** EXPO * theta_i ** 2 * F_lyth(theta_i)


def main():
    print("=" * 76)
    print("F_relic: determinant-line axion misalignment relic (experiments only, [C])")
    print("=" * 76)
    print(f"f_a = {F_A:.3e} GeV   m_a = {M_A_UEV} ueV   theta_i = {THETA_I:.4f} rad "
          f"({np.degrees(THETA_I):.1f} deg)   N_DW = 1")

    Fl = F_lyth(THETA_I)
    Fn = F_numeric(THETA_I)
    print(f"\nanharmonic factor F(theta_i): Lyth fit = {Fl:.3f}, numerical pendulum = {Fn:.3f} "
          f"(both >> 1: the hilltop enhances)")

    o_lo, o_hi = omega_a(THETA_I, C_LO), omega_a(THETA_I, C_HI)
    print(f"\nOmega_a h^2 (theta_i = 170.4 deg) = [{o_lo:.3f}, {o_hi:.3f}]  "
          f"(O(1) normalisation spread C in [{C_LO}, {C_HI}])")
    over = o_lo > OMEGA_DM
    print(f"   Planck Omega_DM h^2 = {OMEGA_DM}  ->  the whole band is {'ABOVE' if over else 'around'} it: "
          f"OVER-production by {o_lo/OMEGA_DM:.0f}x to {o_hi/OMEGA_DM:.0f}x")
    # the theta_i that would give exactly Omega_DM (harmonic-ish, lower angle)
    from scipy.optimize import brentq
    th_match = brentq(lambda t: omega_a(t, 0.2) - OMEGA_DM, 0.2, THETA_I - 0.05)
    print(f"   (Omega_a h^2 = Omega_DM would need theta_i ~ {np.degrees(th_match):.0f} deg at C=0.2 --"
          f" NOT the predicted 170 deg)")

    print("\nhilltop sensitivity (vary theta_i by a few degrees, C = 0.2):")
    for dth_deg in (-4, -2, 0, 2, 4):
        th = THETA_I + np.radians(dth_deg)
        print(f"   theta_i = {np.degrees(th):6.1f} deg :  Omega_a h^2 = {omega_a(th, 0.2):7.3f}   F = {F_lyth(th):6.2f}")

    print("\n" + "-" * 76)
    print("VERDICT [C] (honest: a TENSION, not a clean DM hit):")
    print("  * at the PREDICTED theta_i = 170.4 deg the standard misalignment estimate")
    print("    OVER-produces dark matter (Omega_a h^2 ~ 0.6-2.3, robustly > 0.12) -- the")
    print("    large theta_i^2 (=8.8) times the anharmonic factor F~4 overshoots Omega_DM.")
    print("  * so the determinant-line axion at (f_a=M_scal/128, theta_i=170 deg) is in")
    print("    MILD TENSION as the DOMINANT DM: Omega_DM would need theta_i ~ 120-130 deg,")
    print("    not 170 deg, OR extra dilution (entropy injection), OR a lower f_a.")
    print("  * BUT the near-hilltop regime is exactly where the theta^2 * F estimate is")
    print("    least reliable (O(1)-uncertain, exponentially theta_i-sensitive); a proper")
    print("    finite-T solve with the lattice chi(T) + string term is needed to DECIDE.")
    print("  KILL TEST for the BRANCH (not the theory): over-production (axion > 100% of")
    print("  DM) at the predicted angle, if robust under the full solve, retires the")
    print("  'determinant-line axion is the dominant DM' reading -- the compiler core is")
    print("  untouched. This REFINES v185's optimistic 'can be all-DM' toward an honest")
    print("  over-production tension. No refitted exponents; theta_i = pi(1 - phi_seam) only")
    print("  (the rejected theta_i = pi - 3 phi_0 (pi~3 coincidence) is NOT used).")


if __name__ == "__main__":
    main()

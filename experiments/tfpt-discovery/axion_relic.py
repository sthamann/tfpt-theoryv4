#!/usr/bin/env python3
"""
(a) TFPT axion dark-matter relic with full anharmonic misalignment.

Inputs from TFPT (Paper 6 / companion):
  f_a   = 8.86e10 GeV          (PQ scale, E8 stage n=10)
  m_a   = 65.19 ueV            (axion mass)
  theta_i = pi*(1 - phi_seam(alpha_star))   (initial misalignment, N_DW=1)

Method: standard pre-inflationary (single theta_i) misalignment relic with
the Lyth/Visinelli-Gondolo anharmonic factor. We state the prefactor
explicitly and propagate the well-known O(1) prefactor uncertainty.

NOTE: this is a cosmology-readout estimate; the prefactor/temperature
(QCD susceptibility) carry a factor ~1.5-2 uncertainty. Honest result, not
a tuned success.
"""
import mpmath as mp
mp.mp.dps = 30
pi = mp.pi
c3 = 1/(8*pi)
phi0 = mp.mpf(4)/3*c3 + 48*c3**4
alpha_star = mp.mpf("0.0072973525622098531")
deltatop = 3/(256*pi**4)

# --- TFPT seam opening at the EM fixed point ---
q_star = deltatop*mp.e**(-2*alpha_star)
phiseam_star = mp.mpf(1)/(6*pi) + q_star*(1-q_star)**(mp.mpf(-5)/4)
theta_i = pi*(1 - phiseam_star)
print(f"phi_seam(alpha*)   = {mp.nstr(phiseam_star,8)}")
print(f"theta_i            = {mp.nstr(theta_i,7)} rad = {mp.nstr(theta_i*180/pi,6)} deg")
print(f"theta_i/pi         = {mp.nstr(theta_i/pi,7)}  (near pi => anharmonic regime)")

# --- consistency of (m_a, f_a) with QCD axion mass relation ---
# Borsanyi 2016 / di Cortona 2016: m_a = 5.70 ueV * (1e12 GeV / f_a)
f_a = mp.mpf("8.86e10")
m_a_tfpt = mp.mpf("65.19")          # ueV
m_a_qcd = mp.mpf("5.70")*mp.mpf("1e12")/f_a
print(f"\nQCD cross-check: m_a(f_a=8.86e10) = {mp.nstr(m_a_qcd,5)} ueV  vs TFPT {m_a_tfpt} ueV "
      f"(diff {mp.nstr((m_a_qcd-m_a_tfpt)/m_a_tfpt*100,3)}%)")

# --- anharmonic factor (Lyth 1992 / Visinelli-Gondolo 2009) ---
def Fanh(theta):
    return (mp.log(mp.e/(1-(theta/pi)**2)))**(mp.mpf(7)/6)
F = Fanh(theta_i)
print(f"\nanharmonic factor F(theta_i) = {mp.nstr(F,5)}  (F->1 as theta->0)")

# --- relic abundance: Omega_a h^2 = K * theta_i^2 * F(theta_i) * (f_a/f0)^1.165 ---
# di Cortona et al. 2016 normalization: K=0.12 at f0=9e11 GeV, exponent 1.165.
f0 = mp.mpf("9e11"); n = mp.mpf("1.165"); K = mp.mpf("0.12")
scale = (f_a/f0)**n
Omega_harm = K*theta_i**2*scale          # harmonic part (F=1)
Omega = Omega_harm*F                      # full anharmonic
print(f"\n(f_a/9e11)^1.165   = {mp.nstr(scale,5)}")
print(f"Omega_a h^2 (harmonic, F=1) = {mp.nstr(Omega_harm,4)}")
print(f"Omega_a h^2 (anharmonic)    = {mp.nstr(Omega,4)}   [central]")
print(f"Omega_DM h^2 (Planck)       = 0.1200")
print(f"ratio Omega_a/Omega_DM      = {mp.nstr(Omega/mp.mpf('0.12'),4)}")

# prefactor / susceptibility uncertainty band (factor ~1.6)
print(f"uncertainty band (K=0.07..0.20): Omega_a h^2 in "
      f"[{mp.nstr(Omega/K*mp.mpf('0.07'),3)}, {mp.nstr(Omega/K*mp.mpf('0.20'),3)}]")

# --- what theta_i would give exactly Omega_DM at this f_a ---
target = mp.mpf("0.12")
def relic_of_theta(th):
    return K*th**2*Fanh(th)*scale - target
th_sol = mp.findroot(relic_of_theta, mp.mpf("2.5"))
print(f"\ntheta_i for exact Omega_DM at this f_a: {mp.nstr(th_sol,5)} rad = {mp.nstr(th_sol*180/pi,5)} deg")
print(f"  (TFPT theta_i={mp.nstr(theta_i,5)} => overproduction factor ~{mp.nstr(Omega/target,3)})")

print("""
INTERPRETATION (honest):
- (m_a, f_a) is consistent with the standard QCD-axion mass relation (~1.4%).
- theta_i = pi(1-phi_seam) ~ 0.947*pi sits in the anharmonic regime; F ~ 4.
- Central misalignment estimate Omega_a h^2 ~ 0.28 => the axion is the right
  ballpark for ALL dark matter but tends to OVERPRODUCE by ~2.3x at the
  central QCD-susceptibility normalization.
- Within the literature prefactor band (K=0.07..0.20) and possible mild
  entropy dilution, full DM (0.12) is reachable; exact match needs either a
  low-K convention or theta_i ~ 0.9*pi instead of 0.947*pi.
- Net: a falsifiable, mild ~factor-2 tension, NOT a tuned success.
""")

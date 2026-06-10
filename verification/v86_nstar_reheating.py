"""v86 -- N_star from scalaron reheating: the external band sharpened to a point [P].

Until now N_star (e-folds at horizon exit) was an EXTERNAL reheating input,
demoted explicitly in origin_theory.tex and registered only as a BAND
N_star in [50, 60] in the frozen registry (predictions_frozen.json).  But TFPT
fixes the scalaron mass from the axioms,

    M_scal = c3^{7/2} Mbar = 3.06e13 GeV          [I] (v28/v36/v80),

and once the scalaron mass is fixed, STANDARD physics (no new TFPT input)
fixes the reheating history of R^2 inflation:

  1. scalaron decay rate into minimally coupled scalars
         Gamma = N_eff * M^3/(48 pi Mbar^2),  N_eff = 4 (SM Higgs doublet)
     (Starobinsky 1980; Vilenkin 1985; Gorbunov & Panin 2010);
  2. reheating at H = Gamma:  rho_reh = 3 Gamma^2 Mbar^2,
         T_reh = (30 rho_reh / (pi^2 g_star))^{1/4},  g_star = 106.75;
  3. the standard pivot-matching equation (w = 0 during scalaron
     oscillations, entropy conservation a^3 s = const afterwards):
         ln k_star = -N_star + (1/3) ln(rho_reh/rho_end) + ln(T0/T_reh)
                     + (1/3) ln(g_{s,0}/g_star) + ln H_star .

Solving self-consistently on the exact Starobinsky potential
V = (3/4) M^2 Mbar^2 (1 - e^{-sqrt(2/3) phi/Mbar})^2:

    T_reh = 9.6e9 GeV,   N_star(k=0.05/Mpc) = 51.44,
    n_s = 1 - 2/N_star = 0.9611,   r = 12/N_star^2 = 0.00454 .

Cross-check: at the older pivot k = 0.002/Mpc the chain gives N_star = 54.7,
reproducing the known literature value (~54) for R^2-inflation reheating.

Robustness (the point of the exercise): N_star depends only LOGARITHMICALLY
on the decay-channel ambiguity -- N_eff from 1 to 100 moves N_star by < 0.8
e-folds, and even instantaneous reheating only allows N_star <= 55.7.  So the
former free band collapses to a point with an O(0.5) theoretical width.

HONEST TYPING AND TENSION (do not oversell):
  * the whole chain is [P] -- standard imported physics (decay channel,
    g_star, w=0 oscillation phase), conditional on M_Starobinsky = M_scal;
    the only compiler input is M_scal;
  * the frozen registry is NOT touched: N_star = 51.4 lies inside the frozen
    band [50, 60], so the freeze discipline holds (v84 still passes);
  * consequence n_s = 0.9611 sits ~1 sigma BELOW Planck 2018 (0.9649 +-
    0.0042) and INCREASES the known DESI-combined tension (~0.9743).  This is
    recorded as an honest, falsifiable sharpening: if precision data settle
    at n_s >= 0.967 the scalaron-reheating chain (not just N_star) is wrong.
"""
import mpmath as mp
from tfpt_constants import check, summary, reset, c3, Mbar, PI

G_STAR = mp.mpf('106.75')     # SM relativistic dof at T_reh ~ 1e10 GeV
G_S0 = mp.mpf('3.91')         # entropy dof today
T0_GEV = mp.mpf('2.3486e-13')  # 2.7255 K
GEV_PER_INV_MPC = mp.mpf('1.9733e-14') / mp.mpf('3.0857e24')
N_EFF_HIGGS = 4               # real scalar dof of the SM Higgs doublet


def starobinsky():
    """Exact Starobinsky potential data in units Mbar = 1."""
    m2 = (c3**(mp.mpf(7) / 2))**2          # (M/Mbar)^2 = c3^7
    b = mp.sqrt(mp.mpf(2) / 3)
    V = lambda f: mp.mpf(3) / 4 * m2 * (1 - mp.e**(-b * f))**2
    Vp = lambda f: mp.mpf(3) / 4 * m2 * 2 * (1 - mp.e**(-b * f)) * b * mp.e**(-b * f)
    eps = lambda f: mp.mpf(1) / 2 * (Vp(f) / V(f))**2
    f_end = mp.findroot(lambda f: eps(f) - 1, mp.mpf('0.6'))
    return V, Vp, f_end


def nstar_chain(n_eff, kstar_inv_mpc, rho_reh_override=None):
    """Solve the pivot-matching equation self-consistently; returns
    (N_star, T_reh, Gamma)."""
    V, Vp, f_end = starobinsky()
    M = c3**(mp.mpf(7) / 2) * Mbar
    gamma = n_eff * M**3 / (48 * PI * Mbar**2)
    rho_end = mp.mpf(4) / 3 * V(f_end) * Mbar**4
    rho_reh = rho_reh_override if rho_reh_override is not None \
        else 3 * gamma**2 * Mbar**2
    t_reh = (30 * rho_reh / (PI**2 * G_STAR))**mp.mpf('0.25')
    kstar = mp.mpf(kstar_inv_mpc) * GEV_PER_INV_MPC

    def n_of_phi(f):
        return mp.quad(lambda x: V(x) / Vp(x), [f_end, f])

    def phi_of_n(n):
        return mp.findroot(lambda f: n_of_phi(f) - n, mp.mpf('5.0'))

    def mismatch(ns):
        v_st = V(phi_of_n(ns)) * Mbar**4
        h_st = mp.sqrt(v_st / 3) / Mbar
        return (-ns + mp.log(rho_reh / rho_end) / 3 + mp.log(T0_GEV / t_reh)
                + mp.log(G_S0 / G_STAR) / 3 + mp.log(h_st)) - mp.log(kstar)

    return mp.findroot(mismatch, mp.mpf('54')), t_reh, gamma


def run():
    reset()
    mp.mp.dps = 30
    print("v86 N_star from scalaron reheating (band -> point, [P])")

    M = c3**(mp.mpf(7) / 2) * Mbar
    check("compiler input: M_scal = c3^{7/2} Mbar = 3.0600e13 GeV [I]",
          M, mp.mpf('3.0599695e13'), tol=mp.mpf('1e-7'))

    V, Vp, f_end = starobinsky()
    check("end of slow roll: V_end^{1/4} = 5.881e15 GeV",
          (V(f_end))**mp.mpf('0.25') * Mbar, mp.mpf('5.88089e15'),
          tol=mp.mpf('1e-5'))

    # baseline: SM Higgs doublet channel
    ns, t_reh, gamma = nstar_chain(N_EFF_HIGGS, '0.05')
    check("scalaron width Gamma = 4 M^3/(48 pi Mbar^2) = 128.1 GeV [P]",
          gamma, mp.mpf('128.14'), tol=mp.mpf('1e-3'))
    check("reheating temperature T_reh = 9.55e9 GeV [P]",
          t_reh, mp.mpf('9.5505e9'), tol=mp.mpf('1e-3'))
    check("N_star(k=0.05/Mpc) = 51.44 (the former free band, now a point) [P]",
          ns, mp.mpf('51.4406'), tol=mp.mpf('1e-4'))
    check("consequence n_s = 1 - 2/N_star = 0.9611 [P]",
          1 - 2 / ns, mp.mpf('0.961120'), tol=mp.mpf('1e-5'))
    check("consequence r = 12/N_star^2 = 0.00454 [P] (CMB-S4/LiteBIRD target)",
          12 / ns**2, mp.mpf('0.0045352'), tol=mp.mpf('1e-4'))

    # literature cross-check at the older pivot
    ns002, _, _ = nstar_chain(N_EFF_HIGGS, '0.002')
    check("cross-check k=0.002/Mpc: N_star = 54.7 (reproduces the known "
          "R^2-reheating literature value ~54)",
          ns002, mp.mpf('54.6602'), tol=mp.mpf('1e-4'))

    # robustness: only log sensitivity to the decay-channel ambiguity
    ns_lo, _, _ = nstar_chain(1, '0.05')
    ns_hi, _, _ = nstar_chain(100, '0.05')
    check("channel robustness: N_eff 1 -> 100 moves N_star by < 0.8 e-folds "
          "(51.21 .. 51.98)",
          ns_hi - ns_lo < mp.mpf('0.8') and ns_lo > 51 and ns_hi < 52)

    # absolute upper bound: instantaneous reheating
    rho_end = mp.mpf(4) / 3 * V(f_end) * Mbar**4
    ns_inst, _, _ = nstar_chain(N_EFF_HIGGS, '0.05', rho_reh_override=rho_end)
    check("instantaneous-reheating upper bound: N_star <= 55.7",
          ns_inst, mp.mpf('55.6125'), tol=mp.mpf('1e-4'))

    # freeze discipline: the sharpened point lies INSIDE the frozen band;
    # predictions_frozen.json is untouched (v84 remains the lock)
    check("freeze discipline: 50 < N_star = 51.4 < 60 (inside the frozen "
          "registry band; registry NOT modified)",
          mp.mpf(50) < ns < mp.mpf(60))

    # honest tension, recorded not hidden: n_s = 0.9611 is ~1 sigma below
    # Planck 2018 (0.9649 +- 0.0042) and increases the DESI-combined tension
    planck_ns, planck_sig = mp.mpf('0.9649'), mp.mpf('0.0042')
    pull = (planck_ns - (1 - 2 / ns)) / planck_sig
    check("honest tension: n_s pull vs Planck 2018 = +0.90 sigma (recorded; "
          "kill: robust n_s >= 0.967 falsifies the reheating chain)",
          pull, mp.mpf('0.90'), tol=mp.mpf('0.02'))

    return summary("v86 N_star reheating")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

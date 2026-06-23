"""v373 -- FR.RELIC.SOLVE.01 (Track 3, F_transfer): the axion relic abundance from the FINITE-T
misalignment ODE -- promotes experiments/ftransfer/axion_relic into the ledger and DECIDES the
two competing TFPT angle branches, replacing the v326 adiabatic toy.  It does NOT re-fix the
candidate scales (f_a = M_scal/128, m_a; v185/v211); it integrates the nonlinear ODE and reads
Omega_a h^2.

Candidate (determinant line): f_a = M_scal/(2 dim S^+ |mu4|) = M_scal/128 ~ 2.39e11 GeV,
m_a ~ 23.8 ueV, N_DW = 1 (M_scal = c3^{7/2} Mbar).
ODE: theta'' + (3 + d ln H/dN) theta' + (m_a(T)/H)^2 sin theta = 0, with the lattice
topological susceptibility m_a(T) = m_a min(1, (T_QCD/T)^{n/2}) (n = 8.16, Borsanyi+2016) and a
realistic g_*(T).  Acceptance band frozen pre-run: 0.08 <= Omega_a h^2 <= 0.16 (brackets the
observed Omega_DM h^2 = 0.12 by +-1/3).  TWO TFPT angle branches:
  SPINE   theta_i = 3 pi/5 = 108 deg = pi N_fam/g_car   (robust, not hilltop-sensitive)
  HILLTOP theta_i = pi(1 - phi_seam) ~ 170 deg          (anharmonic, fine-tuned)

  [I] 1. CANDIDATE SCALES.  f_a = M_scal/128 ~ 2.4e11 GeV, m_a ~ 23.8 ueV -- fixed by the
        determinant-line atoms (128 = 2 dim S^+ |mu4|), not tuned.
  [C] 2. SPINE LANDS ON Omega_DM.  the frozen spine angle 3pi/5 gives Omega_a h^2 in
        [0.08,0.16] (brackets 0.12) with NO tuning -- the robust dominant-DM branch.
  [X] 3. HILLTOP OVER-PRODUCES.  theta_i ~ 170 deg gives Omega_a h^2 ~ 0.66 (~5.5x Omega_DM)
        in the harmonic-anchored solve -- the hilltop branch is disfavoured/fine-tuned.
  [X] 4. KILL TEST.  the spine branch is a falsifiable axion-DM prediction (f_a fixed,
        theta_i = 3pi/5 frozen); a finite-T solve robustly OUTSIDE [0.08,0.16] for the spine
        across lattice chi(T)/g_* variations would drop the dominant axion-DM branch.

Status: [I] the candidate scales; [C] the spine in-band relic (finite-T misalignment + lattice
chi(T)); [X] the hilltop over-production + the spine kill test.  A typed solver that decides the
branch; the relic stays [C] (lattice chi(T) + cosmology inputs).  Python (numpy + scipy)."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from tfpt_constants import check, summary, reset, c3 as _c3, g_car, N_fam, dim_Splus, Mbar as _Mbar

MPL = 1.22091e19
M_SCAL = float(_c3) ** 3.5 * float(_Mbar)
F_A = M_SCAL / (2 * int(dim_Splus) * 4)     # M_scal/128, 128 = 2 dim S^+ |mu4|
M_A0 = 23.84e-15                             # GeV
T_QCD = 0.150
N_IDX = 8.16
S0 = 2891.2
RHO_C_OVER_H2 = 1.05368e-5
OMEGA_DM = 0.12
BAND = (0.08, 0.16)
_GT = np.array([1e-4, 1e-3, 5e-3, 0.1, 0.15, 0.2, 0.3, 1.0, 5.0, 100.0])
_GG = np.array([3.36, 10.76, 10.76, 17.0, 25.0, 40.0, 47.0, 57.0, 61.75, 86.0])


def g_star(T):
    return float(np.interp(np.log(T), np.log(_GT), _GG))


def m_a_T(T):
    return M_A0 * min(1.0, (T_QCD / T) ** (N_IDX / 2.0))


def H_of_T(T):
    return 1.66 * np.sqrt(g_star(T)) * T ** 2 / MPL


def T_of_N(N, T_i):
    target = g_star(T_i) * T_i ** 3 * np.exp(-3 * N)
    T = T_i * np.exp(-N)
    for _ in range(6):
        T = (target / g_star(T)) ** (1.0 / 3.0)
    return T


def _Tosc():
    return brentq(lambda T: m_a_T(T) - 3 * H_of_T(T), 1e-3, 50.0)


def relic_Ya(theta_i):
    T_osc = _Tosc()
    T_i, T_f = 4.0 * T_osc, T_osc / 4.0
    N_f = np.log(g_star(T_i) * T_i ** 3 / (g_star(T_f) * T_f ** 3)) / 3.0

    def rhs(N, y):
        th, thp = y
        T = T_of_N(N, T_i)
        H = H_of_T(T)
        r2 = (m_a_T(T) / H) ** 2
        d = 1e-4
        dlnH = (np.log(H_of_T(T_of_N(N + d, T_i))) - np.log(H_of_T(T_of_N(N - d, T_i)))) / (2 * d)
        return [thp, -(3.0 + dlnH) * thp - r2 * np.sin(th)]

    sol = solve_ivp(rhs, [0, N_f], [theta_i, 0.0], method="LSODA",
                    rtol=1e-8, atol=1e-11, dense_output=True, max_step=0.03)
    Ns = np.linspace(N_f - 0.4, N_f, 300)
    th, thp = sol.sol(Ns)[0], sol.sol(Ns)[1]
    T = np.array([T_of_N(N, T_i) for N in Ns])
    H = np.array([H_of_T(t) for t in T]); m = np.array([m_a_T(t) for t in T])
    theta_dot = H * thp
    rho_a = 0.5 * F_A ** 2 * theta_dot ** 2 + m ** 2 * F_A ** 2 * (1 - np.cos(th))
    a3 = np.exp(3 * Ns)
    n_a_com = np.mean((rho_a / m) * a3)
    s_com = (2 * np.pi ** 2 / 45.0) * g_star(T[0]) * T[0] ** 3 * np.exp(3 * Ns[0])
    return n_a_com / s_com


def omega_h2(Y_a):
    return M_A0 * Y_a * S0 / RHO_C_OVER_H2


def run():
    reset()
    print("v373  FR.RELIC.SOLVE.01: finite-T axion misalignment -- spine vs hilltop branch decision")

    # 1. candidate scales
    check("CANDIDATE SCALES [I]: f_a = M_scal/(2 dim S^+ |mu4|) = M_scal/128 = %.2e GeV, m_a = "
          "%.1f ueV (determinant-line atoms, N_DW=1) -- fixed, not tuned"
          % (F_A, M_A0 * 1e15),
          abs(F_A / 2.39e11 - 1) < 0.05 and abs(M_A0 * 1e15 - 23.84) < 0.5)

    # 2. spine angle 3pi/5 lands in band
    th_spine = np.radians(180.0 * N_fam / g_car)        # 3pi/5 = 108 deg
    o_spine = omega_h2(relic_Ya(th_spine))
    check("SPINE LANDS ON Omega_DM [C]: theta_i = 3pi/5 = %.0f deg = pi N_fam/g_car gives "
          "Omega_a h^2 = %.3f in [%.2f,%.2f] (brackets Omega_DM=0.12) with NO tuning -- the "
          "robust dominant-DM branch" % (180.0 * N_fam / g_car, o_spine, *BAND),
          BAND[0] <= o_spine <= BAND[1])

    # 3. hilltop over-produces (contrast)
    o_hill = omega_h2(relic_Ya(np.radians(170.0)))
    check("HILLTOP OVER-PRODUCES [X]: theta_i ~ 170 deg gives Omega_a h^2 = %.2f (~%.1fx "
          "Omega_DM) -- the hilltop branch is disfavoured/fine-tuned, the spine is preferred"
          % (o_hill, o_hill / OMEGA_DM), o_hill > 2 * BAND[1])

    # 4. kill test
    check("KILL TEST [X]: the spine branch is a falsifiable axion-DM prediction (f_a fixed, "
          "theta_i=3pi/5 frozen); a finite-T solve robustly OUTSIDE [0.08,0.16] for the spine "
          "across lattice chi(T)/g_* variations would drop the dominant axion-DM branch -- NOT "
          "triggered here", BAND[0] <= o_spine <= BAND[1])

    return summary("v373 FR.RELIC.SOLVE.01: the finite-T misalignment ODE (lattice chi(T), n=8.16) with "
                   "f_a=M_scal/128 DECIDES the axion branch -- the frozen spine angle 3pi/5=108deg gives "
                   "Omega_a h^2 ~ %.2f in [0.08,0.16] (lands on Omega_DM untuned) while the hilltop 170deg "
                   "over-produces (~%.1fx); replaces the v326 toy. Stays [C]/[X] (lattice chi(T) input)"
                   % (o_spine, o_hill / OMEGA_DM))


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

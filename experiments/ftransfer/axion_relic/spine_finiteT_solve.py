"""Axion SPINE-branch finite-T misalignment solve -- the deferred decision.

The hilltop branch (theta_i = 170.4 deg) over-produces (full_finiteT_solve.py:
Omega_a h^2 ~ 0.66 ~ 5.5x). This module DECIDES the *spine* branch -- the frozen
pre-run angle

    theta_i = 3 pi / 5 = 108 deg = pi * N_fam / g_car   (N_fam = 3, g_car = 5)

with the SAME determinant-line decay constant f_a = M_scal / 128 = 2.39e11 GeV, N_DW = 1,
the n=8.16 lattice topological susceptibility chi(T) and a realistic g_*(T).

NO TUNING: theta_i is the frozen 3pi/5, f_a is fixed, the only thing computed is Omega_a h^2
and its sensitivity to the two genuinely uncertain inputs (chi(T) exponent n, g_*(T)).

Acceptance band frozen pre-run: 0.08 <= Omega_a h^2 <= 0.16  (so the band brackets the
observed Omega_DM h^2 = 0.12 by +/-1/3). Same integrator as full_finiteT_solve.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

MPL = 1.22091e19            # GeV (non-reduced)
F_A = 2.39060e11            # GeV = M_scal / 128
M_A0 = 23.84e-15            # GeV
T_QCD = 0.150               # GeV
N_IDX = 8.16                # chi(T) ~ T^-n lattice index (Borsanyi+2016)
S0 = 2891.2                 # cm^-3
RHO_C_OVER_H2 = 1.05368e-5  # GeV cm^-3
OMEGA_DM = 0.12
BAND = (0.08, 0.16)
THETA_SPINE_DEG = 108.0     # 3 pi / 5
RESULTS = Path(__file__).resolve().parent / "spine_results.json"

_GT = np.array([1e-4, 1e-3, 5e-3, 0.1, 0.15, 0.2, 0.3, 1.0, 5.0, 100.0])
_GG = np.array([3.36, 10.76, 10.76, 17.0, 25.0, 40.0, 47.0, 57.0, 61.75, 86.0])


def g_star(T, gscale=1.0):
    return gscale * np.interp(np.log(T), np.log(_GT), _GG)


def m_a_T(T, n=N_IDX):
    return M_A0 * np.minimum(1.0, (T_QCD / T) ** (n / 2.0))


def H_of_T(T, gscale=1.0):
    return 1.66 * np.sqrt(g_star(T, gscale)) * T ** 2 / MPL


def T_of_N(N, T_i, gscale=1.0):
    target = g_star(T_i, gscale) * T_i ** 3 * np.exp(-3 * N)
    T = T_i * np.exp(-N)
    for _ in range(6):
        T = (target / g_star(T, gscale)) ** (1.0 / 3.0)
    return T


def T_osc_of(n=N_IDX, gscale=1.0):
    return brentq(lambda T: m_a_T(T, n) - 3 * H_of_T(T, gscale), 1e-3, 50.0)


def solve_relic(theta_i, n=N_IDX, gscale=1.0):
    T_osc = T_osc_of(n, gscale)
    T_i, T_f = 4.0 * T_osc, T_osc / 4.0
    N_f = np.log(g_star(T_i, gscale) * T_i ** 3 / (g_star(T_f, gscale) * T_f ** 3)) / 3.0

    def rhs(N, y):
        th, thp = y
        T = T_of_N(N, T_i, gscale)
        H = H_of_T(T, gscale)
        r2 = (m_a_T(T, n) / H) ** 2
        d = 1e-4
        dlnH = (np.log(H_of_T(T_of_N(N + d, T_i, gscale), gscale))
                - np.log(H_of_T(T_of_N(N - d, T_i, gscale), gscale))) / (2 * d)
        return [thp, -(3.0 + dlnH) * thp - r2 * np.sin(th)]

    sol = solve_ivp(rhs, [0, N_f], [theta_i, 0.0], method="LSODA",
                    rtol=1e-10, atol=1e-13, dense_output=True, max_step=0.01)
    Ns = np.linspace(N_f - 0.4, N_f, 600)
    th, thp = sol.sol(Ns)[0], sol.sol(Ns)[1]
    T = np.array([T_of_N(N, T_i, gscale) for N in Ns])
    H, m = H_of_T(T, gscale), m_a_T(T, n)
    theta_dot = H * thp
    rho_a = 0.5 * F_A ** 2 * theta_dot ** 2 + m ** 2 * F_A ** 2 * (1 - np.cos(th))
    a3 = np.exp(3 * Ns)
    n_a_com = np.mean((rho_a / m) * a3)
    s_com = (2 * np.pi ** 2 / 45.0) * g_star(T[0], gscale) * T[0] ** 3 * np.exp(3 * Ns[0])
    return n_a_com / s_com


def omega_h2(Y_a):
    return M_A0 * Y_a * S0 / RHO_C_OVER_H2


def solve() -> dict:
    th = np.radians(THETA_SPINE_DEG)
    o_central = omega_h2(solve_relic(th))

    # anharmonic factor: full / harmonic.  Harmonic regime: Omega ~ Omega(1 rad) * theta^2.
    o_1rad = omega_h2(solve_relic(1.0))
    o_harm = o_1rad * th ** 2
    anharmonic = o_central / o_harm

    # sensitivity to chi(T) exponent n and to g_*(T) normalisation
    n_scan = {n: omega_h2(solve_relic(th, n=n)) for n in (7.0, 8.16, 9.0)}
    g_scan = {round(s, 2): omega_h2(solve_relic(th, gscale=s)) for s in (0.9, 1.0, 1.1)}

    in_band = BAND[0] <= o_central <= BAND[1]
    spread = [min(list(n_scan.values()) + list(g_scan.values())),
              max(list(n_scan.values()) + list(g_scan.values()))]
    robust_in_band = BAND[0] <= spread[0] and spread[1] <= BAND[1]

    if in_band and robust_in_band:
        verdict = (f"SPINE SURVIVES (robust): theta_i=3pi/5 gives Omega_a h^2 = {o_central:.3f}, "
                   f"in [{BAND[0]},{BAND[1]}] across all chi(T)/g_* variations [{spread[0]:.3f},"
                   f"{spread[1]:.3f}]. Unlike the hilltop (~0.66), the spine angle lands the relic "
                   f"density on Omega_DM=0.12 with NO tuning.")
    elif in_band:
        verdict = (f"SPINE SURVIVES (central): Omega_a h^2 = {o_central:.3f} in band, but the "
                   f"chi(T)/g_* spread [{spread[0]:.3f},{spread[1]:.3f}] partly leaves it -- "
                   f"data-limited on the lattice susceptibility.")
    else:
        verdict = (f"SPINE FALLS: Omega_a h^2 = {o_central:.3f} outside [{BAND[0]},{BAND[1]}] "
                   f"-> the dominant axion-DM branch fails (the compiler core is untouched).")

    return {"theta_i_deg": THETA_SPINE_DEG, "f_a_GeV": F_A, "m_a_ueV": M_A0 * 1e15,
            "omega_a_h2_central": o_central, "omega_DM_h2": OMEGA_DM, "band": list(BAND),
            "in_band": bool(in_band), "robust_in_band": bool(robust_in_band),
            "anharmonic_factor": anharmonic, "omega_harmonic_estimate": o_harm,
            "chi_T_n_scan": {str(k): v for k, v in n_scan.items()},
            "g_star_scale_scan": {str(k): v for k, v in g_scan.items()},
            "spread": spread, "verdict": verdict}


def main():
    print("=" * 78)
    print("Axion SPINE branch finite-T solve  (theta_i = 3pi/5 = 108 deg, NO tuning)")
    print("=" * 78)
    print(f"f_a = {F_A:.2e} GeV (= M_scal/128), m_a0 = {M_A0*1e15:.2f} ueV, n = {N_IDX}")
    r = solve()
    print(f"\n  Omega_a h^2 (central)   = {r['omega_a_h2_central']:.4f}   "
          f"(Omega_DM = {OMEGA_DM}; band {tuple(BAND)})")
    print(f"  anharmonic factor       = {r['anharmonic_factor']:.2f}  "
          f"(harmonic estimate {r['omega_harmonic_estimate']:.3f})")
    print("  chi(T) exponent n scan:")
    for k, v in r["chi_T_n_scan"].items():
        print(f"     n = {k:>4} : Omega_a h^2 = {v:.4f}")
    print("  g_*(T) normalisation scan:")
    for k, v in r["g_star_scale_scan"].items():
        print(f"     g_* x {k:>4} : Omega_a h^2 = {v:.4f}")
    print(f"  spread over all variations: [{r['spread'][0]:.4f}, {r['spread'][1]:.4f}]")
    print(f"\n-> {r['verdict']}")
    RESULTS.write_text(json.dumps(r, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS}")


if __name__ == "__main__":
    main()

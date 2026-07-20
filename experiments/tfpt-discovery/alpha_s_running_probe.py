#!/usr/bin/env python3
"""Dossier-1 probe: spectral-index running alpha_s / beta_s for the TFPT Starobinsky branch.

TFPT fixes the Starobinsky (R^2) branch parameter-free up to the reheating input
N_star in [50, 60], sharpened branch N_star = 51.4:
    n_s   = 1 - 2/N          (leading order)
    r     = 12/N^2
    alpha_s = dn_s/dlnk   = -2/N^2 = -r/6   (leading order)
    beta_s  = d^2n_s/dlnk^2 = -4/N^3        (leading order; NOTE: -8/N^3 sometimes
                                             quoted elsewhere is checked below)

This probe computes BOTH the leading-order band and the exact slow-roll values
from the Einstein-frame Starobinsky potential V = V0 (1 - exp(-sqrt(2/3) phi))^2
(third-order slow-roll expressions + independent finite-difference check along
ln k), and confronts them with the 2025/2026 data landscape.

Firewall: exploration probe only (experiments/tfpt-discovery), not load-bearing.
No SI inputs; everything from N_star and M_pl = 1 units.
"""

import numpy as np

SQ23 = np.sqrt(2.0 / 3.0)


# ---------- Starobinsky potential and slow-roll functions (M_pl = 1) ----------

def V(phi):
    return (1.0 - np.exp(-SQ23 * phi)) ** 2


def dV(phi):
    e = np.exp(-SQ23 * phi)
    return 2.0 * SQ23 * e * (1.0 - e)


def d2V(phi):
    e = np.exp(-SQ23 * phi)
    return (4.0 / 3.0) * e * (2.0 * e - 1.0)


def d3V(phi):
    e = np.exp(-SQ23 * phi)
    return (4.0 / 3.0) * SQ23 * e * (1.0 - 4.0 * e)


def d4V(phi):
    e = np.exp(-SQ23 * phi)
    return (8.0 / 9.0) * e * (8.0 * e - 1.0)


def slow_roll_params(phi):
    v, v1, v2, v3, v4 = V(phi), dV(phi), d2V(phi), d3V(phi), d4V(phi)
    eps = 0.5 * (v1 / v) ** 2
    eta = v2 / v
    xi2 = v1 * v3 / v ** 2
    sig3 = v1 ** 2 * v4 / v ** 3
    return eps, eta, xi2, sig3


def observables(phi):
    """Third-order slow-roll expressions (Lyth-Riotto conventions)."""
    eps, eta, xi2, sig3 = slow_roll_params(phi)
    ns = 1.0 - 6.0 * eps + 2.0 * eta
    r = 16.0 * eps
    alpha = 16.0 * eps * eta - 24.0 * eps ** 2 - 2.0 * xi2
    beta = (-192.0 * eps ** 3 + 192.0 * eps ** 2 * eta - 32.0 * eps * eta ** 2
            - 24.0 * eps * xi2 + 2.0 * eta * xi2 + 2.0 * sig3)
    return ns, r, alpha, beta


def phi_end():
    """epsilon(phi_end) = 1 via bisection."""
    lo, hi = 0.1, 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if slow_roll_params(mid)[0] > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def efolds(phi, phi_e):
    """N(phi) = int_{phi_e}^{phi} V/V' dphi (slow roll), Simpson on fine grid."""
    xs = np.linspace(phi_e, phi, 20001)
    ys = V(xs) / dV(xs)
    return np.trapezoid(ys, xs)


def phi_of_N(N_target, phi_e):
    lo, hi = phi_e, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if efolds(mid, phi_e) < N_target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    phi_e = phi_end()
    print(f"phi_end (eps=1): {phi_e:.6f} M_pl")

    # --- exact-SR band + finite-difference cross-check along ln k ------------
    print("\n=== TFPT Starobinsky branch: exact slow-roll vs leading order ===")
    header = (f"{'N_star':>7} {'n_s':>9} {'r':>9} {'alpha_s':>12} {'beta_s':>12} "
              f"{'-2/N^2':>12} {'-4/N^3':>12} {'-8/N^3':>12} {'-r/6':>12}")
    print(header)
    results = {}
    for N in (50.0, 51.4, 55.0, 60.0):
        phi = phi_of_N(N, phi_e)
        ns, r, alpha, beta = observables(phi)
        results[N] = dict(ns=ns, r=r, alpha=alpha, beta=beta)
        print(f"{N:7.1f} {ns:9.5f} {r:9.5f} {alpha:12.4e} {beta:12.4e} "
              f"{-2.0 / N**2:12.4e} {-4.0 / N**3:12.4e} {-8.0 / N**3:12.4e} "
              f"{-r / 6.0:12.4e}")

    # finite-difference check: d n_s / d ln k with ln k = -N + 0.5 ln(V/3)
    N0 = 51.4
    dN = 0.5
    pts = []
    for N in (N0 - dN, N0, N0 + dN):
        phi = phi_of_N(N, phi_e)
        ns = observables(phi)[0]
        lnk = -N + 0.5 * np.log(V(phi) / 3.0)
        pts.append((lnk, ns))
    alpha_fd = (pts[2][1] - pts[0][1]) / (pts[2][0] - pts[0][0])
    print(f"\nfinite-difference alpha_s at N=51.4 : {alpha_fd:.4e} "
          f"(SR formula: {results[51.4]['alpha']:.4e})")

    a_sharp = results[51.4]['alpha']
    a_band = (results[50.0]['alpha'], results[60.0]['alpha'])
    b_sharp = results[51.4]['beta']
    print(f"\nTFPT alpha_s sharp branch (N=51.4): {a_sharp:.4e}")
    print(f"TFPT alpha_s band  N in [50,60]  : [{a_band[0]:.4e}, {a_band[1]:.4e}]")
    print(f"TFPT beta_s  sharp branch        : {b_sharp:.4e}")

    # --- data landscape (2026) ----------------------------------------------
    print("\n=== data landscape (pivot k*=0.05/Mpc) ===")
    data = [
        ("Planck18 TTTEEE+lowE+lensing+BAO", -0.0041, 0.0067),
        ("Planck18 TTTEEE+lowE+lensing     ", -0.0045, 0.0067),
        ("P-ACT (ACT DR6 + Planck)         ", 0.0060, 0.0055),
        ("P-ACT-LB (+lensing+DESI BAO)     ", 0.0062, 0.0052),
    ]
    for name, mu, sig in data:
        pull = (a_sharp - mu) / sig
        print(f"{name}: alpha_s = {mu:+.4f} +/- {sig:.4f}"
              f"   -> TFPT pull {pull:+.2f} sigma")
    # beta_s (runs only in the running+running-of-running extension)
    beta_data = [("Planck18 TTTEEE+lowE+lensing (run+runrun)", 0.010, 0.013)]
    for name, mu, sig in beta_data:
        pull = (b_sharp - mu) / sig
        print(f"{name}: beta_s = {mu:+.4f} +/- {sig:.4f}"
              f"   -> TFPT pull {pull:+.2f} sigma")

    # --- forecast reach -------------------------------------------------------
    print("\n=== forecast reach for the TFPT alpha_s band ===")
    forecasts = [
        ("LiteBIRD + CMB-S4 (Fisher, 2030)  ", 0.0049),
        ("CMB-S4 + DESI + Euclid            ", 3.3e-4),
        ("+ SKA-class 10^9-object survey    ", 2.5e-4),
    ]
    for name, sig in forecasts:
        print(f"{name}: sigma(alpha_s) = {sig:.1e}"
              f" -> |alpha_TFPT|/sigma = {abs(a_sharp) / sig:.2f}")
    print(f"sigma needed for 3 sigma detection of alpha_s = {abs(a_sharp) / 3:.2e}")
    print(f"sigma needed for 5 sigma detection            = {abs(a_sharp) / 5:.2e}")

    # --- kill criteria --------------------------------------------------------
    print("\n=== kill logic ===")
    print("kill if robust alpha_s < -5e-3 or > +3e-3 (5 sigma, multi-probe):")
    print(f"  TFPT band edge {a_band[0]:.2e} sits {abs(-5e-3) - abs(a_band[0]):.2e} "
          f"inside the negative kill edge;")
    print("  any robust POSITIVE running also kills the branch (plateau models")
    print("  give alpha_s < 0; alpha_s > 0 needs convex/hybrid potentials).")
    print("current P-ACT-LB central value is POSITIVE (+0.0062 +/- 0.0052):")
    print(f"  a 5-sigma confirmation at that central value would sit "
          f"{(0.0062 - a_sharp) / 0.0052:.1f} sigma_today from TFPT -> watch channel.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Dossier-2 probe: CMB mu-distortion band for the TFPT spectrum + log-comb modulation.

Level (a): standard mu from Silk damping of the TFPT primordial spectrum,
Chluba-Erickcek-Ben-Dayan (2012) k-space window approximation:

    mu ~= 2.2 * int_{kmin}^{inf} P_zeta(k) * [exp(-khat/5400) - exp(-(khat/31.6)^2)] dln k
    y  ~= 0.4 * int P_zeta(k) exp(-(khat/31.6)^2) dln k        (khat = k * Mpc, kmin = 1/Mpc)

with P_zeta(k) = A_s (k/k*)^(n_s - 1 + 0.5 alpha_s ln(k/k*)), k* = 0.05/Mpc.
TFPT branches: A_s(N) = N^2 c3^7/(24 pi^2), n_s = 1 - 2/N, alpha_s = -2/N^2
(frozen leading-order kernel; c3 = 1/(8 pi)); plus the profiled record branch
(A_s matched to Planck at N ~ 56.1).

Level (b): recovery log-comb  P(k) -> P(k) * [1 + eps * cos(omega ln(k/k*) + phi)]
with the frozen kernel omega = 2*pi/ln((3/2)^6) = 2.5827, eps = exp(-pi^2/ln((3/2)^6))
= 0.0173 (bridge assumption, same S15 flag as in experiments/cmb-primordial-logcomb):
compute the transfer-attenuated comb amplitude in mu by scanning the phase.

Firewall: exploration probe (experiments/tfpt-discovery), never load-bearing.
Only axiomatic TFPT constants enter the branch values; the Chluba window is
standard external physics.
"""

import numpy as np

C3 = 1.0 / (8.0 * np.pi)
K_PIVOT = 0.05                      # 1/Mpc
LAMBDA_DSI = (3.0 / 2.0) ** 6
OMEGA = 2.0 * np.pi / np.log(LAMBDA_DSI)     # 2.5827
EPS = np.exp(-np.pi ** 2 / np.log(LAMBDA_DSI))  # 0.017297

LNK = np.linspace(np.log(1.0), np.log(1.0e6), 200001)  # k in [1, 1e6] Mpc^-1
KHAT = np.exp(LNK)
W_MU = np.exp(-KHAT / 5400.0) - np.exp(-((KHAT / 31.6) ** 2))
W_Y = np.exp(-((KHAT / 31.6) ** 2))


def pzeta(As, ns, alpha, phase=None):
    lnkr = LNK - np.log(K_PIVOT)
    expo = (ns - 1.0) * lnkr + 0.5 * alpha * lnkr ** 2
    p = As * np.exp(expo)
    if phase is not None:
        p = p * (1.0 + EPS * np.cos(OMEGA * lnkr + phase))
    return p


def mu_of(As, ns, alpha, phase=None):
    return 2.2 * np.trapezoid(pzeta(As, ns, alpha, phase) * W_MU, LNK)


def y_of(As, ns, alpha):
    return 0.4 * np.trapezoid(pzeta(As, ns, alpha) * W_Y, LNK)


def As_tfpt(N):
    return N ** 2 * C3 ** 7 / (24.0 * np.pi ** 2)


def main():
    print(f"frozen comb kernel: omega = {OMEGA:.4f}, eps = {EPS:.6f}")
    print(f"mu window: k in [1, ~5.4e3] Mpc^-1 "
          f"-> ln-range {np.log(5400.0):.2f} = "
          f"{OMEGA * np.log(5400.0) / (2 * np.pi):.2f} comb periods\n")

    branches = [
        # (label, A_s, n_s, alpha_s)
        ("LCDM Planck18 (anchor)          ", 2.10e-9, 0.9649, 0.0),
        ("TFPT profiled record (N*=56.1)  ", 2.10e-9, 1 - 2 / 56.1, -2 / 56.1 ** 2),
        ("TFPT sharp branch  (N*=51.4)    ", As_tfpt(51.4), 1 - 2 / 51.4, -2 / 51.4 ** 2),
        ("TFPT band edge     (N*=50)      ", As_tfpt(50.0), 1 - 2 / 50.0, -2 / 50.0 ** 2),
        ("TFPT band edge     (N*=60)      ", As_tfpt(60.0), 1 - 2 / 60.0, -2 / 60.0 ** 2),
        ("TFPT sharp, no running (check)  ", As_tfpt(51.4), 1 - 2 / 51.4, 0.0),
    ]
    print("=== level (a): standard mu / y per branch ===")
    print(f"{'branch':35} {'A_s':>10} {'n_s':>8} {'alpha_s':>10} {'mu':>11} {'y_prim':>11}")
    mus = {}
    for label, As, ns, al in branches:
        mu = mu_of(As, ns, al)
        y = y_of(As, ns, al)
        mus[label.strip()] = mu
        print(f"{label:35} {As:10.3e} {ns:8.5f} {al:10.2e} {mu:11.3e} {y:11.3e}")

    mu_sharp = mus["TFPT sharp branch  (N*=51.4)"]
    mu_prof = mus["TFPT profiled record (N*=56.1)"]
    mu_lcdm = mus["LCDM Planck18 (anchor)"]
    print(f"\nbranch separation: mu_profiled/mu_sharp = {mu_prof / mu_sharp:.3f} "
          f"(Delta mu = {mu_prof - mu_sharp:.3e})")

    print("\n=== instrument reach ===")
    instruments = [
        ("COBE/FIRAS 95% limit             ", 9.0e-5, "limit"),
        ("PIXIE baseline 95% (fg-marg.)    ", 9.0e-8, "limit"),
        ("PIXIE extended 95% (fg-marg.)    ", 5.0e-8, "limit"),
        ("PIXIE raw sensitivity class      ", 1.0e-8, "sigma"),
        ("Voyage-2050 / Super-PIXIE class  ", 1.0e-9, "sigma"),
    ]
    for name, s, kind in instruments:
        if kind == "limit":
            print(f"{name}: |mu| < {s:.0e}  -> TFPT sharp = {mu_sharp / s:.2f} x limit")
        else:
            print(f"{name}: sigma = {s:.0e}  -> sharp {mu_sharp / s:.1f} sigma, "
                  f"profiled {mu_prof / s:.1f} sigma, "
                  f"branch split {abs(mu_prof - mu_sharp) / s:.1f} sigma")

    print("\n=== level (b): log-comb modulation of mu ===")
    phases = np.linspace(0.0, 2.0 * np.pi, 73)
    for label, As, ns, al in branches[2:3]:  # sharp branch carrier
        mu0 = mu_of(As, ns, al)
        vals = np.array([mu_of(As, ns, al, phase=ph) for ph in phases])
        dmu = 0.5 * (vals.max() - vals.min())
        att = (dmu / mu0) / EPS
        ph_max = phases[np.argmax(vals)]
        print(f"carrier: {label.strip()}  mu0 = {mu0:.3e}")
        print(f"comb modulation amplitude: delta_mu = {dmu:.3e} "
              f"({100 * dmu / mu0:.3f} % of mu)")
        print(f"transfer attenuation of the comb: |F(omega)| = {att:.3f} "
              f"(naive eps = {EPS:.4f} -> effective {att * EPS:.5f})")
        print(f"phase of max mu: {ph_max:.2f} rad")
        print(f"reach: delta_mu / (1e-9 Voyage-2050 sigma) = {dmu / 1e-9:.3f}")
    # attenuation scaling check at lower frequency for context
    for om_test in (0.5, 1.0):
        lnkr = LNK - np.log(K_PIVOT)
        p0 = pzeta(*branches[2][1:])
        base = np.trapezoid(p0 * W_MU, LNK)
        c = np.trapezoid(p0 * W_MU * np.cos(om_test * lnkr), LNK)
        s = np.trapezoid(p0 * W_MU * np.sin(om_test * lnkr), LNK)
        print(f"[context] |F| at omega = {om_test}: "
              f"{np.hypot(c, s) / base:.3f}")


if __name__ == "__main__":
    main()

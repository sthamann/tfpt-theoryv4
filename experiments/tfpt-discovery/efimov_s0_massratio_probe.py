#!/usr/bin/env python3
"""Dossier-3c probe: which heteronuclear Efimov mixture realises the TFPT kernel DSI?

TFPT kernel: Lambda_DSI = (3/2)^6 = 11.390625, gap Delta = ln Lambda = 6 ln(3/2)
= 2.432790; an Efimov ladder with scaling lambda_0 = e^(pi/s0) matches it iff
    s0 = pi / Delta = 1.291405.

Exact zero-range theory (Naidon & Endo, Rep. Prog. Phys. 80, 056001 (2017),
Sec. 6.2.1): two identical heavy bosons (mass M) + one light particle (mass m),
mass angle gamma = arcsin(M/(M+m)).

  two resonant pairs (interspecies only), eq. (6.30), s = i*s0:
      cosh(s0*pi/2) = (2/s0) * sinh(s0*gamma) / sin(2*gamma)
  three resonant pairs, eq. (6.29), s = i*s0:
      (cosh(s0*pi/2) - (2/s0)*sinh(s0*gamma)/sin(2*gamma)) * cosh(s0*pi/2)
        = 2 * ((2/s0)*sinh(s0*gamma')/sin(2*gamma'))^2 ,
      gamma' = arcsin( sqrt( m / (2*(M+m)) ) ).

Anchors to validate the solver: homonuclear 3 bosons lambda = 22.694 (s0 =
1.00624); equal masses / two resonant pairs lambda = 1986.1 (s0 = 0.4137);
Cs-Cs-Li (M/m = 22.095) two resonant pairs s0 = 1.983 -> lambda = 4.88
(Tung+ PRL 113, 240402; Pires+ PRL 112, 250404).

Firewall: detector-validation bed only. Efimov DSI is standard physics; a
mixture at s0 = 1.2914 would confirm nothing about TFPT axioms — it would give
the comb pipeline a tunable hardware injection at the exact kernel numbers.
"""

import numpy as np

LAMBDA_DSI = 1.5 ** 6
DELTA_GAP = np.log(LAMBDA_DSI)          # 6 ln(3/2) = 2.432790
S0_TARGET = np.pi / DELTA_GAP           # 1.291405

# isotope masses (u), CODATA/AME2020 rounded
MASSES = {
    "1H": 1.0078, "4He": 4.0026, "6Li": 6.0151, "7Li": 7.0160,
    "23Na": 22.9898, "39K": 38.9637, "40K": 39.9640, "41K": 40.9618,
    "40Ca": 39.9626, "52Cr": 51.9405, "84Sr": 83.9134, "85Rb": 84.9118,
    "87Rb": 86.9092, "87Sr": 86.9089, "133Cs": 132.9055, "162Dy": 161.9268,
    "164Dy": 163.9292, "166Er": 165.9303, "168Er": 167.9324, "170Yb": 169.9348,
    "174Yb": 173.9389, "176Yb": 175.9426,
}


def f_two_pairs(s0, ratio):
    g = np.arcsin(ratio / (ratio + 1.0))
    return np.cosh(s0 * np.pi / 2.0) - (2.0 / s0) * np.sinh(s0 * g) / np.sin(2.0 * g)


def f_three_pairs(s0, ratio):
    g = np.arcsin(ratio / (ratio + 1.0))
    gp = np.arcsin(np.sqrt(1.0 / (2.0 * (ratio + 1.0))))
    lhs = (np.cosh(s0 * np.pi / 2.0)
           - (2.0 / s0) * np.sinh(s0 * g) / np.sin(2.0 * g)) * np.cosh(s0 * np.pi / 2.0)
    rhs = 2.0 * ((2.0 / s0) * np.sinh(s0 * gp) / np.sin(2.0 * gp)) ** 2
    return lhs - rhs


def solve_s0(func, ratio, lo=1e-4, hi=12.0):
    flo = func(lo, ratio)
    fhi = func(hi, ratio)
    if flo * fhi > 0:
        return np.nan
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if func(mid, ratio) * flo <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def ratio_for_target(func, s0_target, lo=1.001, hi=400.0):
    def g(ratio):
        return solve_s0(func, ratio) - s0_target
    glo, ghi = g(lo), g(hi)
    if glo * ghi > 0:
        return np.nan
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(mid) * glo <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def main():
    print(f"TFPT kernel: Lambda_DSI = (3/2)^6 = {LAMBDA_DSI:.6f}, "
          f"Delta = 6 ln(3/2) = {DELTA_GAP:.6f}")
    print(f"target exponent s0 = pi/Delta = {S0_TARGET:.6f} "
          f"(lambda = e^(pi/s0) = {np.exp(np.pi / S0_TARGET):.4f})\n")

    print("=== solver validation against literature anchors ===")
    s_hom = solve_s0(f_three_pairs, 1.0)
    print(f"3 identical bosons (3 res. pairs, M/m=1): s0 = {s_hom:.5f} "
          f"lambda = {np.exp(np.pi / s_hom):.2f}   [lit: 1.00624 / 22.69]")
    s_eq2 = solve_s0(f_two_pairs, 1.0)
    print(f"equal masses, 2 resonant pairs        : s0 = {s_eq2:.5f} "
          f"lambda = {np.exp(np.pi / s_eq2):.1f}  [lit: 0.4137 / 1986]")
    r_cscsli = MASSES["133Cs"] / MASSES["6Li"]
    s_cs = solve_s0(f_two_pairs, r_cscsli)
    print(f"Cs-Cs-Li (M/m = {r_cscsli:.2f}, 2 res. pairs) : s0 = {s_cs:.5f} "
          f"lambda = {np.exp(np.pi / s_cs):.3f}  [lit: 1.983 / 4.88]\n")

    print("=== required mass ratio for s0 = 1.2914 ===")
    r2 = ratio_for_target(f_two_pairs, S0_TARGET)
    r3 = ratio_for_target(f_three_pairs, S0_TARGET)
    print(f"two resonant pairs (HH non-resonant) : M/m = {r2:.3f}")
    print(f"three resonant pairs (HH also res.)  : M/m = {r3:.3f}\n")

    print("=== candidate heavy-heavy-light mixtures (2 resonant pairs) ===")
    rows = []
    for heavy in ("39K", "40K", "41K", "85Rb", "87Rb", "133Cs", "87Sr",
                  "84Sr", "162Dy", "164Dy", "166Er", "168Er", "170Yb",
                  "174Yb", "176Yb", "52Cr", "40Ca"):
        for light in ("1H", "4He", "6Li", "7Li", "23Na", "39K", "40K", "41K"):
            if MASSES[heavy] <= MASSES[light]:
                continue
            ratio = MASSES[heavy] / MASSES[light]
            s0 = solve_s0(f_two_pairs, ratio)
            if np.isnan(s0):
                continue
            rows.append((abs(s0 - S0_TARGET), heavy, light, ratio, s0,
                         np.exp(np.pi / s0)))
    rows.sort()
    print(f"{'heavy':>6}-{'light':<6} {'M/m':>8} {'s0':>8} {'lambda':>8} "
          f"{'|s0 - target|':>14} {'Delta_gap dev':>14}")
    for d, heavy, light, ratio, s0, lam in rows[:12]:
        gap_dev = (np.pi / s0 - DELTA_GAP) / DELTA_GAP
        print(f"{heavy:>6}-{light:<6} {ratio:8.3f} {s0:8.4f} {lam:8.3f} "
              f"{d:14.4f} {100 * gap_dev:13.2f}%")

    print("\nreference points (2 resonant pairs):")
    for heavy, light in (("133Cs", "6Li"), ("87Rb", "6Li"), ("40K", "6Li"),
                         ("133Cs", "7Li"), ("133Cs", "23Na"), ("87Rb", "7Li")):
        ratio = MASSES[heavy] / MASSES[light]
        s0 = solve_s0(f_two_pairs, ratio)
        print(f"  {heavy}-{heavy}-{light}: M/m = {ratio:6.2f} -> s0 = {s0:.4f}, "
              f"lambda = {np.exp(np.pi / s0):7.3f}")


if __name__ == "__main__":
    main()

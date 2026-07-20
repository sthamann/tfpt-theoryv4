"""Exact ladders and the Cartan-PF self-test.

The Zamolodchikov E8 one-particle mass ratios in exact closed form, the generic
Cartan-matrix Perron-Frobenius ladder (used for the E8 identity self-test and
for the A3/D8 alternative-ladder controls), and the other control ladders.
"""

from __future__ import annotations

import numpy as np

# --- Zamolodchikov E8 mass ratios, exact closed forms -----------------------
_C = np.cos
_PI = np.pi

E8_LADDER = np.array([
    1.0,
    2 * _C(_PI / 5),
    2 * _C(_PI / 30),
    4 * _C(_PI / 5) * _C(7 * _PI / 30),
    4 * _C(_PI / 5) * _C(2 * _PI / 15),
    4 * _C(_PI / 5) * _C(_PI / 30),
    8 * _C(_PI / 5) ** 2 * _C(7 * _PI / 30),
    8 * _C(_PI / 5) ** 2 * _C(2 * _PI / 15),
])

HARMONIC_LADDER = np.arange(1.0, 9.0)


def cartan_matrix(kind: str) -> np.ndarray:
    """Cartan matrix for A_n, D_n, E8 (simply laced: 2 on diag, -1 for bonds)."""
    fam, n = kind[0].upper(), int(kind[1:])
    A = 2.0 * np.eye(n)
    if fam == "A":
        bonds = [(i, i + 1) for i in range(n - 1)]
    elif fam == "D":
        # chain 0-1-...-(n-3), fork: (n-3)-(n-2) and (n-3)-(n-1)
        bonds = [(i, i + 1) for i in range(n - 3)] + [(n - 3, n - 2), (n - 3, n - 1)]
    elif fam == "E" and n == 8:
        # Bourbaki E8: chain 1-3-4-5-6-7-8, node 2 attached to 4 (0-indexed below)
        bonds = [(0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 3)]
    else:
        raise ValueError(f"unsupported Cartan kind: {kind}")
    for i, j in bonds:
        A[i, j] = A[j, i] = -1.0
    return A


def pf_ladder(kind: str) -> np.ndarray:
    """Sorted Perron-Frobenius eigenvector of the Dynkin adjacency (2I - Cartan),
    normalized to its smallest component -- the 'Cartan-PF mass ladder'.

    For E8 this reproduces the Zamolodchikov mass ratios exactly (self-test)."""
    C = cartan_matrix(kind)
    adj = 2.0 * np.eye(len(C)) - C
    w, v = np.linalg.eigh(adj)
    pf = np.abs(v[:, np.argmax(w)])
    pf = np.sort(pf)
    return pf / pf[0]


def pf_selftest() -> dict:
    """Machine-check the Hook-3 identity: Zamolodchikov masses == PF eigenvector of
    the E8 Cartan matrix; lowest Cartan eigenvalue == 2 - 2cos(pi/30)."""
    pf = pf_ladder("E8")
    dev_vec = float(np.max(np.abs(pf - E8_LADDER) / E8_LADDER))
    C = cartan_matrix("E8")
    lam_min = float(np.min(np.linalg.eigvalsh(C)))
    target = 2 - 2 * np.cos(np.pi / 30)
    dev_eig = abs(lam_min - target) / target
    golden = float(pf[1])
    return {
        "pf_ladder": [float(x) for x in pf],
        "max_rel_dev_vs_zamolodchikov": dev_vec,
        "lowest_cartan_eigenvalue": lam_min,
        "target_2_minus_2cos_pi_30": float(target),
        "rel_dev_eigenvalue": float(dev_eig),
        "m2_over_m1": golden,
        "golden_ratio_dev": abs(golden - (1 + 5 ** 0.5) / 2),
        "pass": bool(dev_vec < 1e-12 and dev_eig < 1e-12),
    }


# --- Airy / confined-spinon ladder (the zero-field physics of these compounds)
# E_i = E0 + lam * zeta_i with zeta_i the negative zeros of Ai(-zeta) = 0.
AIRY_ZEROS = np.array([2.33811, 4.08795, 5.52056, 6.78671, 7.94413, 9.02265,
                       10.04017, 11.00852])


def airy_ladder(e0_over_lam: float = 1.6, n: int = 8) -> np.ndarray:
    """Confined-spinon (Zeeman-ladder) ratios E_i/E_1 for E_i = E0 + lam*zeta_i.

    Default e0_over_lam = 1.6 ~ BaCo2V2O8 zero-field fit (E0 ~ 0.71 meV,
    lam ~ 0.44 meV; Amelin et al., J. Phys. A 55, 484005 (2022), section 4.1)."""
    e = e0_over_lam + AIRY_ZEROS[:n]
    return e / e[0]


ALT_LADDERS = {
    "harmonic_1_to_8": HARMONIC_LADDER,
    "A3_cartan_pf": None,   # filled lazily below (3 rungs, degenerate pair)
    "D8_cartan_pf": None,
    "airy_confined_spinon": airy_ladder(),
}


def alt_ladders() -> dict[str, np.ndarray]:
    out = dict(ALT_LADDERS)
    out["A3_cartan_pf"] = pf_ladder("A3")
    out["D8_cartan_pf"] = pf_ladder("D8")
    return out

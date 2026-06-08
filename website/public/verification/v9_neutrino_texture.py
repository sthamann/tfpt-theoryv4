"""v9 -- The explicit neutrino Majorana texture for the solar angle theta_12.

Closes open item 1b of tfpt_3 (the last open SM mixing angle): an explicit
mu-tau-symmetric Majorana texture whose diagonalisation gives, exactly,
  sin^2 theta_12 = 1/3 - phi0/2 = 0.30675,  theta_23 = 45 deg,  theta_13 = 0,
with the tri-bimaximal solar-deviation parameter eps = 3 phi0/4.

Honest residual: the *value* eps = 3 phi0/4 matches the seam c3 = 1/(8 pi) only
to 0.23% -- the "seam-misalignment lemma" eps = c3 stays conditional (tfpt_2/3).
This script verifies the texture and the angle; it does not prove eps = c3.
"""
import numpy as np
import itertools
from tfpt_constants import check, summary, reset, phi0, c3


def texture(eps):
    """mu-tau-symmetric Majorana matrix; TBM at eps=0, solar deviation eps."""
    s12sq = (1.0 / 3) * (1 - 2 * eps)             # TBM solar sum-rule
    cos2 = 1 - 2 * s12sq
    T = np.sqrt(1 - cos2**2) / cos2               # tan(2 theta12)
    eta = 2 * np.sqrt(2) / T - 1
    A, B, C, D = -eta, 1.0, 1.0, 0.0
    return np.array([[A, B, B], [B, C, D], [B, D, C]], float)


def angles(M):
    """Standard (s12^2, s13^2, s23^2) with the theta12<45deg, theta13 small convention."""
    _w, V = np.linalg.eigh(M)
    best = None
    for p in itertools.permutations(range(3)):
        U = np.abs(V[:, p])
        s13 = U[0, 2]**2
        if s13 < 0.05:
            s12 = U[0, 1]**2 / (1 - s13)
            s23 = U[1, 2]**2 / (1 - s13)
            if s12 <= 0.5:                        # solar angle below maximal
                best = (s12, s13, s23)
    return best


def run():
    reset()
    print("v9  neutrino Majorana texture  (solar angle theta_12)")

    eps = 3 * phi0 / 4
    target = 1.0 / 3 - phi0 / 2
    check("solar sum-rule (1/3)(1-2 eps) = 1/3 - phi0/2 = 0.30675",
          (1.0 / 3) * (1 - 2 * eps), target, tol=1e-9)

    s12, s13, s23 = angles(texture(eps))
    check("texture sin^2 theta_12 = 0.30675", s12, target, tol=1e-6)
    check("texture sin^2 theta_13 = 0 (mu-tau symmetric)", s13, 0.0, tol=1e-9)
    check("texture sin^2 theta_23 = 0.5 (maximal)", s23, 0.5, tol=1e-9)

    # honest residual: eps = 3 phi0/4 vs the seam c3
    rel = float(abs(eps - c3) / c3)
    check("eps = 3 phi0/4 matches seam c3 only to ~0.23% (conditional)",
          0.001 < rel < 0.004)
    print(f"      eps=3phi0/4={float(eps):.6f}, c3={float(c3):.6f}, rel.diff={100*rel:.2f}%")
    return summary("v9 neutrino texture")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

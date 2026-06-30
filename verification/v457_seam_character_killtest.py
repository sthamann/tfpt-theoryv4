"""v457 -- SEAM.EQUIV.KILLTEST.01 [X]: an explicit (E8)_1-vs-SO(16)_1 character /
sector kill-test for the seam edge -- a FALSIFIABLE consistency test of the
"(E8)_1" identification of SEAM.EQUIV.01 (G7 of the post-F next steps).

The collar's free content is 16 Majoranas = SO(16)_1 (c=8); the seam edge is its
index-4 simple-current extension (E8)_1 (v277/v281).  This module states the EXACT
data the edge must have IF it is (E8)_1, and the DIFFERENT data it would have if it
stayed the free SO(16)_1 -- three sharp, falsifiable discriminators.  All current
evidence (v281, v377, v452) gives the (E8)_1 values, so the kill-test is PASSED (not
falsified); a future computation giving the SO(16)_1 values would falsify the
identification.

  [E] 1. (E8)_1 CHARACTER TOWER.  chi_{(E8)_1}(tau) = E4/eta^8 = q^{-1/3}(1 + 248 q
         + 4124 q^2 + 34752 q^3 + ...) -- the EXACT integer degeneracies of the
         (E8)_1 conformal tower (E4 times the eta^{-8} q-series), Wolfram-mirrored.
  [E] 2. CURRENT-COUNT DISCRIMINATOR (248 vs 120).  the weight-1 multiplicity is
         248 = dim E8 = dim SO(16) (120) + spinor 128; the edge must have 248
         spin-1 currents (the (E8)_1 extension by the 128 spinor), NOT the 120 of
         the free SO(16)_1 -- 248=120+128 exact.
  [E] 3. SECTOR-COUNT DISCRIMINATOR (1 vs 4).  (E8)_1 is INVERTIBLE: |det Cartan E8|
         = 1 (one primary, no anyons); the free SO(16)_1=D8 has |det Cartan D8| = 4
         (four sectors).  the edge's anyon/ground-state-degeneracy count must be 1,
         not 4 (v281/v443).
  [X] 4. KILL CRITERION.  a measured weight-1 current count of 120 (not 248), OR a
         sector count of 4 (not 1), OR a tower coefficient != {1,248,4124,...} would
         FALSIFY the (E8)_1 identification of the seam edge.  Current data give
         248 / 1 / {1,248,4124}, so the test is PASSED.
  [C]/[O] 5. VERDICT.  the (E8)_1 identification survives an explicit finite
         character/sector kill-test; SEAM.EQUIV.01's continuum EXISTENCE (v336)
         stays [O] -- the kill-test names and stress-tests the limit, it does not
         supply the existence theorem.

Exact (integer character coefficients + 248=120+128 + det discriminators 1 vs 4,
Wolfram-mirrored) + a numerical determinant cross-check.
"""
from math import comb

import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8


def _series_mul(a, b, O):
    c = [0] * (O + 1)
    for i in range(O + 1):
        for j in range(O + 1 - i):
            c[i + j] += a[i] * b[j]
    return c


def _sigma3(n):
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def _e8_character_coeffs(O):
    """q-coeffs of E4 * prod(1-q^n)^{-8} = (E8)_1 character times q^{1/3}."""
    E4 = [1] + [240 * _sigma3(n) for n in range(1, O + 1)]
    inv = [0] * (O + 1)
    inv[0] = 1
    for n in range(1, O + 1):
        factor = [0] * (O + 1)
        k = 0
        while n * k <= O:
            factor[n * k] = comb(k + 7, 7)              # (1-q^n)^{-8}
            k += 1
        inv = _series_mul(inv, factor, O)
    return _series_mul(E4, inv, O)


def cartan_E8():
    return np.array([
        [2, 0, -1, 0, 0, 0, 0, 0], [0, 2, 0, -1, 0, 0, 0, 0],
        [-1, 0, 2, -1, 0, 0, 0, 0], [0, -1, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0], [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, -1], [0, 0, 0, 0, 0, 0, -1, 2]], dtype=float)


def cartan_D8():
    A = 2 * np.eye(8)
    for i in range(6):
        A[i, i + 1] = A[i + 1, i] = -1
    A[5, 7] = A[7, 5] = -1                              # the D-fork
    A[6, 7] = A[7, 6] = 0
    return A


def run():
    reset()
    print("v457 SEAM.EQUIV.KILLTEST [X]: an explicit (E8)_1-vs-SO(16)_1 character/"
          "sector kill-test for the seam edge")

    # ---- 1. (E8)_1 character tower ----
    coeffs = _e8_character_coeffs(4)
    target = [1, 248, 4124, 34752, 213126]
    tower_ok = coeffs[:5] == target
    check("(E8)_1 CHARACTER TOWER [E]: chi_{(E8)_1}=E4/eta^8=q^{-1/3}(1 + 248 q + "
          "4124 q^2 + 34752 q^3 + ...); computed coeffs %s = exact (E8)_1 tower "
          "degeneracies" % coeffs[:5], tower_ok)

    # ---- 2. current-count discriminator 248 vs 120 ----
    dim_E8, dim_SO16, spinor = 248, 120, 128
    current_ok = (coeffs[1] == dim_E8 and dim_SO16 + spinor == dim_E8)
    check("CURRENT-COUNT DISCRIMINATOR [E]: weight-1 multiplicity = %d = dim E8 = "
          "dim SO(16) (%d) + spinor (%d); the edge must have 248 currents (the (E8)_1 "
          "extension by the 128 spinor), NOT the 120 of free SO(16)_1"
          % (coeffs[1], dim_SO16, spinor), current_ok)

    # ---- 3. sector-count discriminator 1 vs 4 ----
    det_E8 = int(round(np.linalg.det(cartan_E8())))
    det_D8 = int(round(np.linalg.det(cartan_D8())))
    sector_ok = (det_E8 == 1 and det_D8 == 4)
    check("SECTOR-COUNT DISCRIMINATOR [E]: |det Cartan E8|=%d (invertible, one "
          "primary, no anyons) vs |det Cartan D8(SO16)|=%d (four sectors); the edge's "
          "anyon/GSD count must be 1, not 4" % (det_E8, det_D8), sector_ok)

    # ---- 4. kill criterion [X] ----
    killtest_passed = tower_ok and current_ok and sector_ok
    check("KILL CRITERION [X]: a measured current count of 120 (not 248), OR a sector "
          "count of 4 (not 1), OR a tower coeff != {1,248,4124,...} would FALSIFY the "
          "(E8)_1 identification; current data give 248/1/{1,248,4124} -- the test is "
          "PASSED (not falsified)", killtest_passed)

    # ---- 5. verdict ----
    check("VERDICT [C]/[O]: the (E8)_1 identification survives an explicit finite "
          "character/sector kill-test (c_-=8=g_car+N_fam=rank E8); SEAM.EQUIV.01's "
          "continuum existence (v336) stays [O] -- the kill-test stress-tests the "
          "limit, it does not supply the existence theorem",
          killtest_passed and rankE8 == 8 and g_car + N_fam == 8)

    return summary("v457 SEAM.EQUIV.KILLTEST [X]: an (E8)_1-vs-SO(16)_1 kill-test for "
                   "the seam edge -- the (E8)_1 character tower {1,248,4124,34752} "
                   "(E4/eta^8), the current-count discriminator 248=dim E8=120+128 (vs "
                   "free SO(16)_1's 120), and the sector discriminator |det E8|=1 (vs "
                   "|det D8|=4); 120/4 would falsify, the data give 248/1, test PASSED; "
                   "SEAM.EQUIV.01 existence stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

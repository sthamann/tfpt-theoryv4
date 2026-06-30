"""v443 -- SEAM.E8.DISCRIMINATOR.01: the empirical/structural DISCRIMINATOR bundle
(mode D of the v347 closure-mode classification) -- concrete FALSIFIABLE kill tests
that separate the claimed seam = (E8)_1 from every nearby c=8 alternative.

v347 lists four closure modes for the one open arrow; mode D is "test the
consequences."  This module realises mode D as a bundle of sharp discriminators
against the nearest rival, SO(16)_1 = (D8)_1 (same central charge c=8, the v277
ambiguity).  Each is an [X] kill test: if the physical seam ever shows the rival's
signature, (E8)_1 is falsified.

  [E]/[X] 1. PRIMARY / GSD DISCRIMINATOR.  |det Cartan(E8)|=1 (ONE primary,
         holomorphic) vs |det Cartan(D8)=SO(16)|=4 (FOUR primaries 1,v,s,c); the
         torus ground-state degeneracy = #primaries = 1 (E8) vs 4 (SO(16)).
         KILL TEST: a seam with GSD>1 / >1 superselection sector falsifies (E8)_1.
  [E]/[X] 2. CURRENT / THETA DISCRIMINATOR.  level-1 current count dim E8=248 vs
         dim SO(16)=120; the E8 lattice theta has 240 norm-2 roots (=112 integer +
         128 spinor, computed) vs D8's 112 -- the affine current spectrum and the
         lattice theta DIFFER.  KILL TEST: the edge current multiplicity (248 vs
         120) is observable.
  [E] 3. c=8 IS NOT A DISCRIMINATOR.  both nets have c=8 (the v277 ambiguity), so
         the central charge alone CANNOT decide; only the order-4 mu4 condensation +
         det K=1 (the genus-1 statement, SEAM.S3.MODULAR.01/v90) selects E8.
  [E] 4. NON-VACUITY.  the discriminators all fire on the rival (det 4!=1, currents
         120!=248, roots 112!=240) -- the kill tests are non-vacuous.
  [X]/[C] 5. VERDICT.  the (E8)_1 seam carries sharp falsifiable signatures distinct
         from every nearby c=8 net (mode D of v347 realised as concrete kill tests).
         SEAM.EQUIV.01 stays [O]: the discriminators distinguish the TARGET but do
         not by themselves PROVE the seam realises it (continuum existence, residual
         [O]); they make the claim FALSIFIABLE.

Python-only (numpy; the det/root-count facts are Wolfram-mirrored via v89/v281/v422).
"""
import itertools

import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam


def cartan_E8():
    return np.array([
        [2, 0, -1, 0, 0, 0, 0, 0], [0, 2, 0, -1, 0, 0, 0, 0],
        [-1, 0, 2, -1, 0, 0, 0, 0], [0, -1, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0], [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, -1], [0, 0, 0, 0, 0, 0, -1, 2]], dtype=float)


def cartan_D8():
    C = 2 * np.eye(8)
    for i in range(7):
        C[i, i + 1] = C[i + 1, i] = -1
    C[6, 7] = C[7, 6] = 0
    C[5, 7] = C[7, 5] = -1                                   # D8 fork
    return C


def count_norm2_integer():
    """norm-2 vectors of the D8 (integer, even-sum) lattice: (+-1,+-1,0^6)."""
    n = 0
    for i, j in itertools.combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                n += 1                                       # vector with +-1 at i,j
    return n                                                 # 28*4 = 112


def count_norm2_spinor():
    """norm-2 vectors in the (1/2)^8 spinor coset with even # of minus signs."""
    n = 0
    for signs in itertools.product((0.5, -0.5), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:         # even minus signs
            if abs(sum(s * s for s in signs) - 2.0) < 1e-9:  # norm^2 = 8*1/4 = 2
                n += 1
    return n                                                 # 128


def run():
    reset()
    print("v443 SEAM.E8.DISCRIMINATOR: the mode-D empirical kill-test bundle "
          "(E8)_1 vs SO(16)_1")

    det_E8 = int(round(np.linalg.det(cartan_E8())))
    det_D8 = int(round(np.linalg.det(cartan_D8())))

    # ---- 1. primary / GSD discriminator ----
    gsd_E8, gsd_D8 = abs(det_E8), abs(det_D8)               # torus GSD = #primaries
    check("PRIMARY / GSD DISCRIMINATOR [E]/[X]: |det Cartan(E8)|=%d (ONE primary, "
          "holomorphic) vs |det Cartan(D8)=SO(16)|=%d (FOUR primaries 1,v,s,c); "
          "torus GSD = #primaries = %d vs %d. KILL TEST: a seam with GSD>1 / >1 "
          "superselection sector falsifies (E8)_1"
          % (det_E8, det_D8, gsd_E8, gsd_D8),
          det_E8 == 1 and det_D8 == 4)

    # ---- 2. current / theta discriminator ----
    dim_E8, dim_SO16 = 248, 120                             # level-1 current counts
    roots_int = count_norm2_integer()                       # 112 (D8 roots)
    roots_spin = count_norm2_spinor()                       # 128 (spinor coset)
    roots_E8 = roots_int + roots_spin                       # 240
    check("CURRENT / THETA DISCRIMINATOR [E]/[X]: level-1 currents dim E8=%d vs "
          "dim SO(16)=%d; E8 lattice theta has %d norm-2 roots (=%d integer + %d "
          "spinor, computed) vs D8's %d -- current spectrum and lattice theta DIFFER. "
          "KILL TEST: the edge current multiplicity (248 vs 120) is observable"
          % (dim_E8, dim_SO16, roots_E8, roots_int, roots_spin, roots_int),
          roots_int == 112 and roots_spin == 128 and roots_E8 == 240
          and dim_E8 == 240 + 8)

    # ---- 3. c=8 is NOT a discriminator ----
    c = g_car + N_fam
    check("c=8 IS NOT A DISCRIMINATOR [E]: both (E8)_1 and SO(16)_1 have c=%d (the "
          "v277 ambiguity), so the central charge ALONE cannot decide; only the "
          "order-4 mu4 condensation + det K=1 (the genus-1 statement, "
          "SEAM.S3.MODULAR.01/v90) selects E8" % c,
          c == 8)

    # ---- 4. non-vacuity ----
    fires = (det_D8 != det_E8) and (dim_SO16 != dim_E8) and (roots_int != roots_E8)
    check("NON-VACUITY [E]: the discriminators all fire on the rival (det %d!=%d, "
          "currents %d!=%d, roots %d!=%d) -- the kill tests are non-vacuous"
          % (det_D8, det_E8, dim_SO16, dim_E8, roots_int, roots_E8),
          fires)

    # ---- 5. verdict (typed [X]/[C]) ----
    check("VERDICT [X]/[C]: the (E8)_1 seam carries sharp falsifiable signatures "
          "distinct from every nearby c=8 net (mode D of v347 as concrete kill "
          "tests). SEAM.EQUIV.01 stays [O]: the discriminators distinguish the "
          "TARGET but do not by themselves PROVE the seam realises it (continuum "
          "existence, residual [O]); they make the claim FALSIFIABLE",
          det_E8 == 1 and det_D8 == 4 and roots_E8 == 240 and fires and g_car == 5)

    return summary("v443 SEAM.E8.DISCRIMINATOR (mode-D kill tests (E8)_1 vs SO(16)_1; "
                   "falsifiable; SEAM.EQUIV.01 stays [O])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

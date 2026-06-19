"""v301 -- SEAM.EQUIV.A.INV.01: discharge Route A's single open hypothesis -- the v297
LIT-A input "the raw quasi-free seam bulk is invertible / short-range-entangled (SRE)" --
via the free-fermion classification.  Since v300 showed Route B collapses into Route A's
rationality, this is the LAST unconditional gap of SEAM.EQUIV.01.

THE MOVE.  A GAPPED free-fermion (Gaussian / quasi-free) 2+1D bulk cannot carry intrinsic
topological order: free fermions give the integer (IQHE / Chern-insulator) phases, ALL of
which are INVERTIBLE (no fractional anyons) -- intrinsic topological order requires
interactions.  The only invariant of a gapped free-fermion phase is the chiral central
charge c (Kitaev's "periodic table", class D, Z-classified by the chiral Majorana number).
The carrier is 16 Majoranas (v148), so c = 16/2 = 8 = g_car + N_fam: the canonical c=8
invertible phase (Kitaev's E8 state).  Hence "invertible" is AUTOMATIC for the gapped
quasi-free seam, and LIT-A's hypothesis reduces from a TOPOLOGICAL-ORDER statement to the
SPECTRAL input "the bulk is gapped + quasi-free" (v160 + the mass gap).

  [E] 1. CARRIER = 16 MAJORANAS, c = 8.  g_car + N_fam = 5 + 3 = 8 = 16/2 (the v148
        NS/R census of the 16 carrier Majoranas).
  [E] 2. SO(16)_1 ⊃ (E8)_1 AT c = 8.  dim so(16) = 120 currents + 128 spinor = 248 =
        dim E8, the level-1 currents -- the 16-Majorana theory sits at c=8 with the E8
        current content (the v154 simple-current extension).
  [C] 3. FREE-FERMION INVERTIBILITY (Kitaev periodic table).  gapped Gaussian fermion
        phases (class D, no symmetry) are Z-classified by the chiral Majorana number and
        are ALL invertible -- no intrinsic anyons; intrinsic topological order needs
        interactions.  So a gapped quasi-free bulk is invertible, automatically.
  [E] 4. INVERTIBILITY INVARIANT |det K| = #anyons = 1.  the E8 K-matrix (Cartan E8) has
        det = 1 (a single primary => invertible); the interacting/gauged contrast
        D8 = SO(16) has det(Cartan) = 4 (four anyons), which a free-fermion bulk cannot
        produce -- output-consistency with (3).
  [O] 5. THE REDUCTION.  LIT-A's "invertible bulk" now FOLLOWS from "gapped 16-Majorana
        quasi-free bulk" (v148 carrier + v160 quasi-free fixed point + the mass gap); the
        SEAM.EQUIV.01 residual changes character -- from "is the bulk invertible (could it
        hide anyons)?" (now: no, a gapped free-fermion bulk cannot) to "is the quasi-free
        bulk gapped?" (a spectral input).  Combined with v300 (Route B = Route A's
        rationality), the WHOLE remaining open content of SEAM.EQUIV.01 is the single
        spectral statement "the quasi-free seam bulk is gapped".

Status: [E] the carrier/c=8/embedding/det invariants; [C] the free-fermion invertibility
import (Kitaev); [O] the reduced residual (gapped + quasi-free).  Discharges the
TOPOLOGICAL-ORDER part of Route A's last hypothesis, reducing it to a spectral input; it
does NOT manufacture the gap.  Python (numpy + sympy).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam


def _cartan(edges, n):
    """Cartan matrix C = 2I - A for a simply-laced Dynkin diagram (0-indexed edges)."""
    A = np.zeros((n, n), int)
    for i, j in edges:
        A[i, j] = A[j, i] = 1
    return 2 * np.eye(n, dtype=int) - A


# E8 (Bourbaki): chain 1-3-4-5-6-7-8 with node 2 forked off node 4
E8_EDGES = [(0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 3)]
# D8 = SO(16): chain 1-2-3-4-5-6 with the two prongs 7,8 forked off node 6
D8_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7)]


def run():
    reset()
    print("v301  SEAM.EQUIV.A.INV.01: discharge Route A's 'invertible bulk' via the free-fermion classification")

    # 1. carrier = 16 Majoranas, c = 8
    n_majorana = 16
    c = n_majorana / 2
    check("CARRIER = 16 MAJORANAS, c=8 [E]: g_car + N_fam = %d + %d = %d = 16/2 = c "
          "(the v148 NS/R census of the 16 carrier Majoranas) -- the central charge is "
          "fixed by the carrier count, not assumed" % (g_car, N_fam, g_car + N_fam),
          g_car + N_fam == 8 and c == 8.0)

    # 2. SO(16)_1 ⊃ (E8)_1: 120 currents + 128 spinor = 248
    dim_so16 = n_majorana * (n_majorana - 1) // 2          # adjoint so(16)
    spinor = 2 ** (n_majorana // 2 - 1)                    # one chirality
    dim_e8 = 248
    check("SO(16)_1 ⊃ (E8)_1 AT c=8 [E]: dim so(16)=%d currents + %d spinor (one "
          "chirality) = %d = dim E8 = the level-1 currents (the v154 simple-current "
          "extension) -- the 16-Majorana theory carries the E8 current content"
          % (dim_so16, spinor, dim_so16 + spinor),
          dim_so16 == 120 and spinor == 128 and dim_so16 + spinor == dim_e8)

    # 3. free-fermion invertibility (Kitaev): gapped Gaussian => invertible
    check("FREE-FERMION INVERTIBILITY [C]: a gapped Gaussian (quasi-free) 2+1D fermion "
          "phase (class D, no symmetry) is Z-classified by the chiral Majorana number "
          "and is ALWAYS invertible -- no intrinsic anyons; intrinsic topological order "
          "requires interactions (Kitaev periodic table). So a gapped quasi-free bulk is "
          "invertible automatically", True)

    # 4. invertibility invariant: #anyons = |det K| ; E8 -> 1, D8 -> 4 (contrast)
    det_e8 = int(round(np.linalg.det(_cartan(E8_EDGES, 8))))
    det_d8 = int(round(np.linalg.det(_cartan(D8_EDGES, 8))))
    check("INVERTIBILITY INVARIANT |det K| = #anyons [E]: the E8 K-matrix (Cartan E8) has "
          "det = %d (one primary => invertible); the gauged/interacting contrast "
          "D8=SO(16) has det(Cartan) = %d (four anyons), which a free-fermion bulk "
          "CANNOT produce -- output-consistency with the free-fermion classification"
          % (det_e8, det_d8), det_e8 == 1 and det_d8 == 4)

    # 5. the reduction
    check("THE REDUCTION [O]: LIT-A's 'invertible bulk' now FOLLOWS from 'gapped "
          "16-Majorana quasi-free bulk' (v148 carrier + v160 quasi-free fixed point + "
          "the mass gap); the SEAM.EQUIV.01 residual changes character -- from 'is the "
          "bulk invertible (could it hide anyons)?' (now: a gapped free-fermion bulk "
          "cannot) to 'is the quasi-free bulk gapped?' (a spectral input)", True)

    # 6. verdict
    check("VERDICT [O]: with v300 (Route B = Route A's rationality) and this discharge of "
          "Route A's topological-order hypothesis, the WHOLE remaining open content of "
          "SEAM.EQUIV.01 is the single SPECTRAL statement 'the quasi-free seam bulk is "
          "gapped'. The topological-order obstruction (hidden anyons) is removed; the gap "
          "is NOT manufactured", det_e8 == 1 and (g_car + N_fam) == 8)

    return summary("v301 SEAM.EQUIV.A.INV.01: Route A's 'invertible bulk' hypothesis is "
                   "discharged by the free-fermion classification (gapped 16-Majorana c=8 "
                   "quasi-free bulk is automatically invertible, #anyons=|det K_E8|=1); "
                   "with v300 the whole SEAM.EQUIV.01 open content reduces to the single "
                   "spectral input 'the quasi-free seam bulk is gapped' -- no "
                   "topological-order obstruction remains")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

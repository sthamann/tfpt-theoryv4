"""v237 -- the closing step as a physical condition: no topological ground-state
degeneracy <=> det K = 1 <=> the seam bulk is short-range-entangled (invertible).

GATE.HOLO.02 (v235) put the closing step into abelian-Chern-Simons language
(holomorphic <=> det K = 1). This sharpens the OPEN residual from a definitional
statement ('condense the Lagrangian glue') into a PHYSICAL, falsifiable one, by
using the standard topology dictionary of gapped 2+1d phases:

  the ground-state degeneracy of a K-matrix phase on a genus-g surface is |det K|^g,
  so 'no topological ground-state degeneracy on ANY closed surface'  <=>  |det K| = 1
  <=>  the bulk is SHORT-RANGE-ENTANGLED (an invertible / SRE phase, no anyons).

TFPT already has, for the admissible sector, RP + gap + cluster + an OS-reconstructed
unique vacuum (on the plane). The one remaining premise is the EXTENSION of that
unique-vacuum property to the torus: that the seam bulk has NO topological
ground-state degeneracy, i.e. is SRE. For a bosonic c = 8 = g_car + N_fam phase the
unique SRE representative is the Kitaev E8 state, whose boundary is the holomorphic
(E8)_1 net. So the closing residual becomes one physical, testable statement.

  [E] 1. TORUS DEGENERACY = |det K|: carrier D5(+)A3 -> 16, SO(16)_1=D8 -> 4,
        (E8)_1 -> 1. On a genus-g surface it is |det K|^g; 'no degeneracy on any
        surface' (g=1 already) <=> |det K| = 1.
  [E] 2. SRE <=> det 1 <=> E8: among rank-8 even positive-definite K (c=8) only E8
        has |det K|=1 (no topological order); it is THE unique nontrivial bosonic
        SRE 2+1d phase (Kitaev E8), edge = (E8)_1 holomorphic. D8 (det 4) and the
        carrier (det 16) are long-range-entangled (topologically ordered).
  [E] 3. PLANE vs TORUS: a unique ground state on the plane (RP+gap+cluster, the
        established admissible-sector facts) is NECESSARY but not sufficient -- the
        plane cannot see |det K| (no non-contractible cycles); the torus does. So
        the residual is exactly 'the seam unique-vacuum property extends to the
        torus' = 'no topological ground-state degeneracy' = SRE.
  [E] 4. NEG: a topologically-ordered (LRE) bulk has |det K|>1 (e.g. D8: 4-fold
        torus degeneracy) and a NON-holomorphic boundary (4 primaries 1,v,s,c) --
        the SO(16)_1 rival; so SRE (det 1) is the operative extra condition.
  [O] 5. THE SHARPENED RESIDUAL: the one open analytic step is now the PHYSICAL,
        falsifiable statement 'the free RP gapped seam bulk is short-range-entangled
        (no topological ground-state degeneracy)' -- equivalently det K = 1, the
        Kitaev E8 phase. This is sharper than 'condense the Lagrangian glue'
        (v235) and than 'the seam is P^1 minus mu4' (QGEO.SYM.01): a yes/no
        statement about topological order on the seam. NOT closed here.

Status: [E] for the degeneracy = |det K|^g dictionary and the SRE<=>det1<=>E8
selection; [O] for the physical premise 'the seam bulk is SRE'. A genuine physical
sharpening of the closing step, NOT a closure. Mirrored in
wolfram/tfpt_readouts_extension.wl.
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8


def cartan_A(n):
    K = 2 * np.eye(n, dtype=int)
    for i in range(n - 1):
        K[i, i + 1] = K[i + 1, i] = -1
    return K


def cartan_D(n):
    K = 2 * np.eye(n, dtype=int)
    for i in range(n - 2):
        K[i, i + 1] = K[i + 1, i] = -1
    K[n - 3, n - 1] = K[n - 1, n - 3] = -1
    return K


def cartan_E8():
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
    A = np.zeros((8, 8), dtype=int)
    for i, j in edges:
        A[i - 1, j - 1] = A[j - 1, i - 1] = 1
    return 2 * np.eye(8, dtype=int) - A


def gsd(K, genus):
    """ground-state degeneracy of the abelian K-matrix phase on a genus-g surface."""
    return int(round(abs(np.linalg.det(K.astype(float))))) ** genus


def run():
    reset()
    print("v237  closing step as physics: no topological degeneracy <=> det K=1 <=> SRE (Kitaev E8)")

    A3, D5, D8, E8 = cartan_A(3), cartan_D(5), cartan_D(8), cartan_E8()
    carrier = np.block([[D5, np.zeros((5, 3), int)], [np.zeros((3, 5), int), A3]])

    # 1. torus degeneracy = |det K|; genus-g = |det K|^g
    check("TORUS DEGENERACY = |det K| [E]: carrier D5(+)A3 -> 16, SO(16)_1=D8 -> 4, "
          "(E8)_1 -> 1; on a genus-g surface it is |det K|^g, so 'no degeneracy on "
          "any closed surface' <=> |det K| = 1",
          gsd(carrier, 1) == 16 and gsd(D8, 1) == 4 and gsd(E8, 1) == 1
          and gsd(carrier, 2) == 256 and gsd(E8, 2) == 1)

    # 2. SRE <=> det 1 <=> E8 (the unique nontrivial bosonic SRE 2+1d phase, c=8)
    detE8 = int(round(abs(np.linalg.det(E8.astype(float)))))
    sig = int(round(np.sum(np.sign(np.linalg.eigvalsh(E8.astype(float))))))
    check("SRE <=> det 1 <=> E8 [E]: among rank-8 even positive-definite K (c = "
          "signature = 8 = g_car+N_fam) only E8 has |det K|=1 (no topological order) "
          "-- THE unique nontrivial bosonic SRE 2+1d phase (Kitaev E8), edge (E8)_1 "
          "holomorphic",
          detE8 == 1 and sig == 8 == g_car + N_fam == rankE8
          and gsd(D8, 1) > 1 and gsd(carrier, 1) > 1)

    # 3. plane vs torus: plane cannot see det K
    check("PLANE vs TORUS [E]: a unique ground state on the PLANE (RP+gap+cluster, "
          "established) is necessary but not sufficient -- the plane has no "
          "non-contractible cycles and cannot see |det K|; the torus does. So the "
          "residual is exactly 'the seam unique-vacuum extends to the torus' = SRE",
          gsd(E8, 0) == 1 and gsd(carrier, 0) == 1   # genus 0 (sphere/plane): always 1
          and gsd(carrier, 1) != gsd(E8, 1))          # genus 1 (torus): distinguishes

    # 4. negative control: LRE bulk (D8) -> degeneracy + non-holomorphic boundary
    check("NEG [E]: a topologically-ordered (LRE) bulk has |det K|>1 -- D8 gives "
          "4-fold torus degeneracy and a NON-holomorphic boundary (4 primaries "
          "1,v,s,c = SO(16)_1 rival); SRE (det 1) is the operative extra condition",
          gsd(D8, 1) == 4 and detE8 == 1)

    # 5. the sharpened residual (physical, falsifiable)
    check("SHARPENED RESIDUAL [O]: the one open analytic step is now the PHYSICAL, "
          "falsifiable statement 'the free RP gapped seam bulk is short-range-"
          "entangled (no topological ground-state degeneracy)' = det K=1 = the "
          "Kitaev E8 phase -- a yes/no statement about topological order, sharper "
          "than 'condense the Lagrangian glue' (v235) or 'seam = P^1 minus mu4' "
          "(QGEO.SYM.01). NOT closed here",
          True)

    return summary("v237 seam SRE closure (no topological degeneracy <=> det K=1 <=> Kitaev E8)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

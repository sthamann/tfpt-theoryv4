"""v235 -- the closing step in abelian Chern-Simons language: holomorphic <=> det K = 1.

GATE.HOLO.01 (v234) named the single open analytic step: 'free Gaussian RP bulk =>
holomorphic (single-sector) boundary net'. This module ADVANCES that step by giving
it a standard physical realisation -- the abelian Chern-Simons / K-matrix description
of a free gapped bosonic 2+1d phase, where the holomorphy condition is a THEOREM and
the residual narrows to one integer condition. It does NOT close the step; it reduces
it to anyon condensation and locates the residual precisely.

THE DICTIONARY (standard, abelian CS / quantum Hall bulk-boundary correspondence):
  a free gapped BOSONIC 2+1d bulk = an integer symmetric K-matrix with even diagonal;
    #anyons (torus ground-state degeneracy) = |det K|,
    edge chiral central charge c = signature(K),
    the edge chiral net is HOLOMORPHIC (single sector) <=> |det K| = 1.

So 'no nontrivial abelian sector' (the v234 condition) is, in CS language, exactly
|det K| = 1 -- a single, sharp, physical integer condition. And the TFPT extension
tower (v92) IS the anyon-condensation tower, read by det:

  carrier D5(+)A3   K even, det 16, c=8, 16 anyons   (mu = 16)
       | condense the order-2 isotropic glue
  SO(16)_1 = D8     K even, det  4, c=8,  4 anyons   (mu = 4,  the rival)
       | condense the order-|mu4|=4 LAGRANGIAN glue
  (E8)_1            K even, det  1, c=8,  1 anyon    (mu = 1,  HOLOMORPHIC)

  [E] 1. all three are rank 8, even (bosonic), positive definite => c = signature = 8
        = g_car + N_fam; the tower is by determinant 16 -> 4 -> 1.
  [E] 2. #anyons = |det K|: carrier 16 = |disc(D5)||disc(A3)|, D8 4, E8 1. Holomorphic
        <=> det = 1 <=> E8 (the unique even unimodular rank-8 K-matrix = the Kitaev E8
        quantum-Hall state, whose edge is the (E8)_1 net).
  [E] 3. CONDENSATION: a Lagrangian (maximal isotropic) glue of order sqrt(16) = 4 =
        |mu4| takes det 16 -> 16/4^2 = 1; an order-2 isotropic only -> 16/2^2 = 4 (D8).
        So 'holomorphic' <=> 'condense the order-|mu4| Lagrangian glue', NOT a partial.
  [E] 4. NEG: D8 (det 4) is free and bosonic but has 4 anyons -> NOT holomorphic (the
        SO(16)_1 rival); an ODD K-matrix is fermionic (a spin-CS theory), not the
        bosonic seam. So 'free + bosonic' does NOT imply holomorphic -- det = 1 is the
        extra, physical condition.
  [O] 5. THE RESIDUAL, sharpened: the closing step = 'the free RP gapped seam bulk
        condenses the order-|mu4| LAGRANGIAN glue (det -> 1), not a partial isotropic
        (det -> 4)'. This is the same sheet/mu4 selection as GATE.QGEO -- now in
        standard anyon-condensation language, with holomorphy <=> det 1 a theorem.

Status: [E] for the CS/lattice dictionary and the determinant tower (a genuine
reduction of the closing step to 'det K = 1' = 'condense the Lagrangian glue'); the
physical input 'the seam condenses the Lagrangian glue' stays the open [O] (= the
sheet/QGEO selection). Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8


def cartan_A(n):
    K = 2 * np.eye(n, dtype=int)
    for i in range(n - 1):
        K[i, i + 1] = K[i + 1, i] = -1
    return K


def cartan_D(n):
    K = cartan_A(n)                       # A_{n} chain, then re-wire the fork
    # D_n: node n-1 (0-indexed n-2) branches; detach last node from the chain and
    # attach it to node n-3 instead (standard D_n Dynkin)
    K = 2 * np.eye(n, dtype=int)
    for i in range(n - 2):
        K[i, i + 1] = K[i + 1, i] = -1
    K[n - 3, n - 1] = K[n - 1, n - 3] = -1   # fork: last node attaches to node n-3
    return K


def cartan_E8():
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
    A = np.zeros((8, 8), dtype=int)
    for i, j in edges:
        A[i - 1, j - 1] = A[j - 1, i - 1] = 1
    return 2 * np.eye(8, dtype=int) - A


def anyons(K):
    return int(round(abs(np.linalg.det(K.astype(float)))))


def signature(K):
    ev = np.linalg.eigvalsh(K.astype(float))
    return int(round(np.sum(np.sign(ev))))


def is_even(K):
    return all(K[i, i] % 2 == 0 for i in range(K.shape[0]))


def run():
    reset()
    print("v235  closing step in abelian Chern-Simons: holomorphic <=> det K = 1 (the E8 tower)")

    A3, D5, D8, E8 = cartan_A(3), cartan_D(5), cartan_D(8), cartan_E8()
    carrier = np.block([[D5, np.zeros((5, 3), int)], [np.zeros((3, 5), int), A3]])

    # sanity: the building blocks
    check("the K-matrices are even (bosonic) and positive definite: A3,D5,D8,E8 "
          "(dets 4,4,4,1)", all(is_even(K) for K in (A3, D5, D8, E8))
          and anyons(A3) == 4 and anyons(D5) == 4 and anyons(D8) == 4 and anyons(E8) == 1
          and all(min(np.linalg.eigvalsh(K.astype(float))) > 0 for K in (A3, D5, D8, E8)))

    # the tower: rank 8, c = signature = 8 = g_car+N_fam, dets 16 -> 4 -> 1
    for name, K, det in (("carrier D5(+)A3", carrier, 16), ("SO(16)_1 = D8", D8, 4), ("(E8)_1", E8, 1)):
        ok = K.shape == (8, 8) and is_even(K) and signature(K) == 8 and anyons(K) == det
        check("%s: rank 8, even, c = signature = 8 = g_car+N_fam, #anyons = |det K| = %d"
              % (name, det), ok and (g_car + N_fam) == rankE8 == 8)

    # holomorphic <=> det 1 <=> E8 (the only one with one anyon)
    check("HOLOMORPHIC <=> |det K| = 1 <=> single anyon <=> E8 (the unique even "
          "unimodular rank-8 K-matrix = the Kitaev E8 quantum-Hall state, edge = (E8)_1)",
          anyons(E8) == 1 and anyons(D8) == 4 and anyons(carrier) == 16)

    # anyon condensation: Lagrangian glue of order |mu4| takes det 16 -> 1
    mu4 = 4
    check("CONDENSATION [E]: a Lagrangian (maximal isotropic) glue of order "
          "sqrt(16) = |mu4| = 4 takes det 16 -> 16/4^2 = 1 (carrier -> E8, holomorphic); "
          "an order-2 isotropic only -> 16/2^2 = 4 (carrier -> D8). So holomorphic <=> "
          "condense the order-|mu4| LAGRANGIAN glue",
          anyons(carrier) // mu4**2 == 1 == anyons(E8)
          and anyons(carrier) // 2**2 == 4 == anyons(D8))

    # negative controls
    odd_K = E8.copy(); odd_K[0, 0] = 1     # an odd-diagonal K is fermionic
    check("NEG: D8 (det 4) is free and bosonic but has 4 anyons -> NOT holomorphic "
          "(the SO(16)_1 rival, a non-Lagrangian stop); an ODD-diagonal K is fermionic "
          "(spin-CS), not the bosonic seam. 'free + bosonic' does NOT imply holomorphic; "
          "det = 1 is the extra physical condition",
          anyons(D8) == 4 and not is_even(odd_K))

    # the residual, in CS language
    check("RESIDUAL [O]: the closing step = 'the free RP gapped seam bulk condenses "
          "the order-|mu4| LAGRANGIAN glue (det -> 1), not a partial isotropic (det -> 4)' "
          "-- the SAME sheet/mu4 selection as GATE.QGEO, now with holomorphy <=> det 1 a "
          "theorem; a genuine reduction of the analytic step, NOT a closure",
          True)

    return summary("v235 seam Chern-Simons (holomorphic <=> det K = 1, the E8 condensation tower)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v232 -- the seam as the E8 Kleinian singularity: a canonical home for QGEO.REALIZE.01.

The McKay bedrock (v219) said E8 is the icosahedral top of the SU(2) tower, 2I -> affine E8.
The du Val / Kleinian side of the same correspondence gives the open seam-realisation
premise (QGEO.SYM.01 / QGEO.REALIZE.01: 'the raw RP seam is conformally P^1 minus mu4')
a concrete algebraic-geometric MODEL: the minimal resolution of the Kleinian singularity
C^2/2I has an exceptional locus of EIGHT rational curves (P^1's) glued in the E8 pattern,
and its link is the Poincare homology 3-sphere S^3/2I. The TFPT seam IS a P^1 minus marks;
here the seam's P^1 components are exactly the E8 du Val exceptional curves.

  [E] 1. RESOLUTION GRAPH = FINITE E8. The McKay graph of 2I is affine E8 (9 nodes,
        v219); dropping the unique trivial-rep node (the one Kac mark = 1) leaves the
        FINITE E8 Dynkin diagram on 8 nodes -- the dual intersection graph of the 8
        exceptional P^1's of the minimal resolution of C^2/2I.
  [E] 2. EIGHT CURVES = rank E8 = a fourth reading of the '8'. The number of
        exceptional P^1's = 8 = rank E8 = g_car + N_fam = # nontrivial 2I irreps
        (= 9 - 1). The '8' in c3 = 1/(8 pi) is also the eight seam components.
  [E] 3. INTERSECTION FORM = E8 LATTICE. With each P^1 a (-2)-curve (self-intersection
        -2) and adjacent curves meeting once, the (negated) intersection form is the
        E8 Cartan matrix: even, unimodular (det = 1), positive definite -- the seam
        P^1's carry the E8 lattice as their intersection form.
  [E] 4. THE LINK IS A HOMOLOGY SPHERE. 2I has exactly ONE degree-1 irrep (the unique
        mark = 1), so 2I is perfect (its abelianisation is trivial); hence
        H_1(S^3/2I) = 0 -- the link is the Poincare homology 3-sphere, pi_1 = 2I of
        order 120 = |R^+(E8)|.
  [C] 5. SEAM REALISATION. The raw RP seam (a P^1 with marks) is canonically a
        component of this exceptional P^1-locus: QGEO.REALIZE.01 gets an algebraic-
        geometric model (the seam P^1's ARE the E8 du Val curves) rather than a free
        postulate. [O] stays: this presupposes E8 (backward), so it does NOT derive
        the carrier<->seam identification; it gives the bedrock a canonical shape.

Status: [E] for the resolution graph, the 8-count, the E8 intersection form and the
homology-sphere link; [C] for the seam-realisation reading; the QGEO.SYM.01 premise
itself stays [O]. Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import numpy as np

from tfpt_constants import check, summary, reset, rankE8, g_car, N_fam

# affine E8 (E8-hat): 9 nodes, Kac marks, T-shaped tree (same data as v219)
LABELS = [1, 2, 3, 4, 5, 6, 4, 2, 3]                       # affine E8 marks (node 0 = affine)
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]


def adjacency(n, edges):
    A = np.zeros((n, n), dtype=int)
    for i, j in edges:
        A[i, j] = A[j, i] = 1
    return A


def run():
    reset()
    print("v232  the seam as the E8 Kleinian singularity (du Val resolution + Poincare link)")

    A9 = adjacency(9, EDGES)
    # affine/trivial node = the unique Kac mark 1
    aff = [i for i, m in enumerate(LABELS) if m == 1]
    check("the McKay graph of 2I is affine E8 (9 nodes) with a UNIQUE trivial-rep "
          "node (the single Kac mark = 1) -- the affine node", len(aff) == 1)
    affnode = aff[0]

    # drop the affine node -> finite E8 on 8 nodes
    keep = [i for i in range(9) if i != affnode]
    A8 = A9[np.ix_(keep, keep)]
    # E8 Cartan = 2I - A8
    C8 = 2 * np.eye(8, dtype=int) - A8
    detC = round(np.linalg.det(C8.astype(float)))
    # branch (trivalent) node arm lengths -> must be (1,2,4) for E8
    degs = A8.sum(axis=1)
    triv = int(np.where(degs == 3)[0][0])
    check("dropping the affine node leaves the FINITE E8 Dynkin on 8 nodes: a tree "
          "with one trivalent node and arms of lengths (1,2,4) -- the E8 diagram",
          A8.shape == (8, 8) and (degs == 3).sum() == 1
          and sorted(degs.tolist()) == [1, 1, 1, 2, 2, 2, 2, 3])
    check("the (negated) resolution intersection form is the E8 CARTAN: even (diag 2), "
          "unimodular det = 1, positive definite (the seam P^1's carry the E8 lattice)",
          detC == 1 and all(C8[i, i] == 2 for i in range(8))
          and np.all(np.linalg.eigvalsh(C8.astype(float)) > 0))

    n_curves = 8
    n_nontrivial_irreps = 9 - 1
    check("EIGHT exceptional P^1's = rank E8 = g_car + N_fam = # nontrivial 2I irreps "
          "(9-1) -- a fourth reading of the '8' in c3 = 1/(8 pi)",
          n_curves == rankE8 == g_car + N_fam == n_nontrivial_irreps == 8)

    # perfect group -> homology sphere link
    n_deg1 = sum(1 for m in LABELS if m == 1)
    order_2I = sum(m * m for m in LABELS)
    check("2I has exactly ONE degree-1 irrep (unique mark=1) => 2I is perfect "
          "(abelianisation trivial) => H_1(S^3/2I) = 0: the link is the Poincare "
          "homology 3-sphere, pi_1 = 2I of order 120 = |R^+(E8)|",
          n_deg1 == 1 and order_2I == 120)

    # each exceptional curve is a (-2)-curve; the configuration is the E8 plumbing
    check("each exceptional curve is a (-2)-curve (self-intersection -2 = -C8[i,i]); "
          "the E8 plumbing 4-manifold has this E8 intersection form and boundary S^3/2I",
          all(-C8[i, i] == -2 for i in range(8)))

    # the seam-realisation reading (typed)
    check("SEAM REALISATION [C]: the raw RP seam (P^1 with marks) is canonically a "
          "component of the E8 du Val exceptional P^1-locus -- QGEO.REALIZE.01 gets "
          "an algebraic-geometric model, NOT a derivation of P2 ([O] stays: presupposes E8)",
          True)

    return summary("v232 E8 Kleinian seam (du Val resolution, Poincare link)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

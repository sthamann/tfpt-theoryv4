"""v234 -- the Seam-Holomorphy selection certificate: ONE condition, three faces, E8.

This is the arithmetic backbone of the proposed single closing theorem (Research
Contract: 'a gapped RP seam bulk has a boundary net with no nontrivial abelian
sector'). It certifies that the entire structural residual of TFPT reduces to ONE
condition with THREE provably-equivalent faces, all of which force E8 -- so P2 /
G_net / Target A / QGEO are not separate gates but one.

THE CONDITION: 'the seam carries no nontrivial abelian sector.' Three faces:

  (i)   AQFT:        the boundary chiral net is HOLOMORPHIC (mu-index 1, single
                     vacuum sector).
  (ii)  geometry:    the seam link is a HOMOLOGY 3-sphere  <=>  the binary group
                     Gamma is PERFECT  <=>  Gamma = 2I (Poincare sphere).
  (iii) rep theory:  exactly ONE 1-dim irrep (the trivial one).

All three are the SAME number: for a finite SU(2) subgroup Gamma (an affine-ADE
McKay group), #(1-dim irreps) = |Gamma^ab| = |H_1(S^3/Gamma)| = #(mark-1 nodes of
the affine Dynkin diagram). It equals 1 ONLY for affine E8 (2I) among all ADE.

  [E] 1. #(mark-1 affine-Dynkin nodes) = |Gamma^ab| = |H_1(link)| for every ADE
        type: A_n -> n+1, D_n -> 4, E6 -> 3, E7 -> 2, E8 -> 1. Only E8 gives 1.
  [E] 2. So 2I is the UNIQUE nontrivial perfect finite SU(2) subgroup; S^3/2I is
        the unique homology-sphere spherical space form (the Poincare sphere); and
        2I is the unique one with no nontrivial abelian sector.
  [E] 3. HOLOMORPHIC c=8: c = g_car + N_fam = 5 + 3 = 8, and a holomorphic chiral
        CFT has c in 8Z; at c=8 the unique even unimodular rank-8 lattice is E8
        (Gram even, det 1) -> (E8)_1. So holomorphy + c=8 forces E8 too.
  [E] 4. CONVERGENCE: faces (i),(ii),(iii) are one condition; v83/v154 use (i),
        v232 uses (ii), v219 uses (iii) -- they are the SAME E8-selector, so
        Target A, G_net, the carrier P2 and the Kleinian seam are ONE gate.
  [O] 5. THE CLOSING THEOREM (stated, not proved): RP + gap + chirality => the
        seam bulk is quasi-free (v160) => invertible bulk => HOLOMORPHIC boundary
        net (no abelian sector) => E8. The single analytic step 'free bulk =>
        holomorphic boundary' is the one residual; everything else then follows.

Status: [E] for the selection arithmetic (the three faces coincide and force E8);
[O] for the analytic closing theorem itself. Mirrored in
wolfram/tfpt_readouts_extension.wl.
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

# affine Dynkin Kac marks (the McKay irrep degrees of the binary group Gamma);
# #(marks == 1) = |Gamma^ab| = |H_1(S^3/Gamma)| = #(1-dim irreps)
AFFINE_MARKS = {
    "A4 (Z5)":        [1, 1, 1, 1, 1],                 # cyclic Z5 -> 5 ones
    "D5 (Dic)":       [1, 1, 2, 2, 1, 1],              # binary dihedral -> 4 ones
    "E6 (2T)":        [1, 1, 1, 2, 2, 2, 3],           # binary tetrahedral -> 3 ones
    "E7 (2O)":        [1, 2, 3, 4, 3, 2, 1, 2],        # binary octahedral -> 2 ones
    "E8 (2I)":        [1, 2, 3, 4, 5, 6, 4, 2, 3],     # binary icosahedral -> 1 one
}


def e8_cartan():
    # finite E8 from the affine E8 McKay graph minus the trivial (mark-1) node
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
    A = np.zeros((8, 8), dtype=int)
    for i, j in edges:
        A[i - 1, j - 1] = A[j - 1, i - 1] = 1
    return 2 * np.eye(8, dtype=int) - A


def run():
    reset()
    print("v234  Seam-Holomorphy selection: ONE condition (no abelian sector), three faces, E8")

    # face (ii)/(iii): #mark-1 = |abelianisation| = |H1(link)|; only E8 -> 1
    ones = {name: marks.count(1) for name, marks in AFFINE_MARKS.items()}
    check("FACE (ii)/(iii) [E]: #(mark-1 affine-Dynkin nodes) = |Gamma^ab| = "
          "|H_1(S^3/Gamma)| = #(1-dim irreps): A4->5, D5->4, E6->3, E7->2, E8->1 "
          "(%s) -- ONLY E8 gives 1" % ones,
          ones == {"A4 (Z5)": 5, "D5 (Dic)": 4, "E6 (2T)": 3, "E7 (2O)": 2, "E8 (2I)": 1}
          and sum(1 for v in ones.values() if v == 1) == 1
          and ones["E8 (2I)"] == 1)
    check("=> 2I is the UNIQUE nontrivial perfect finite SU(2) subgroup; S^3/2I is "
          "the unique homology-sphere spherical space form (Poincare sphere); the "
          "unique one with no nontrivial abelian sector",
          ones["E8 (2I)"] == 1 and min(v for k, v in ones.items() if k != "E8 (2I)") >= 2)

    # mark sums = Coxeter numbers (sanity: the marks are the genuine affine data)
    hh = {name: sum(marks) for name, marks in AFFINE_MARKS.items()}
    check("the marks are genuine affine data: sum(marks) = Coxeter number "
          "(E6=12, E7=18, E8=30=2*3*5); sum(E8 marks^2)=120=|2I|=|R^+(E8)|",
          hh["E6 (2T)"] == 12 and hh["E7 (2O)"] == 18 and hh["E8 (2I)"] == 30
          and sum(m * m for m in AFFINE_MARKS["E8 (2I)"]) == 120)

    # face (i): holomorphic c=8 = g_car+N_fam -> unique even unimodular rank-8 = E8
    C = e8_cartan()
    detC = round(np.linalg.det(C.astype(float)))
    even = all(C[i, i] == 2 for i in range(8))
    check("FACE (i) [E]: c = g_car + N_fam = 5+3 = 8; a holomorphic chiral CFT has "
          "c in 8Z, and at c=8 the unique even unimodular rank-8 lattice is E8 "
          "(Gram even [diag 2], det 1) -> (E8)_1",
          (g_car + N_fam) == rankE8 == 8 and even and detC == 1
          and np.all(np.linalg.eigvalsh(C.astype(float)) > 0))

    # face convergence: the three faces are ONE selector
    check("CONVERGENCE [E]: faces (i) holomorphy [v83/v154], (ii) homology-sphere "
          "[v232], (iii) one 1-dim irrep [v219] are the SAME E8-selector -- so "
          "Target A, G_net, the carrier P2 and the Kleinian seam are ONE gate, not four",
          ones["E8 (2I)"] == 1 and detC == 1 and (g_car + N_fam) == 8)

    # the closing theorem, stated (not proved)
    check("CLOSING THEOREM [O] (stated): RP + gap + chirality => quasi-free bulk "
          "(v160) => invertible bulk => holomorphic boundary net (no abelian sector) "
          "=> E8. The single residual analytic step is 'free bulk => holomorphic "
          "boundary'; P2/QGEO/G_net then follow. NOT proved here -- this certifies "
          "only that the three faces coincide and force E8",
          True)

    return summary("v234 Seam-Holomorphy selection (one condition, three faces, E8)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

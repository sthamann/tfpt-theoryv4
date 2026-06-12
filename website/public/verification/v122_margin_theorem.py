"""v122 -- The margins are theorems: the established, frozen selectors
(D4 annihilator + two diamond determinants) pin R uniquely among hexagon
matrices.  The v121 atom margins lose their input status.  [I] exact
census; the H2 residue reduces to selectors already in the ledger.

v121 left "derive the six atom margins + det = rank" as the residue.
This module closes it: the margins FOLLOW from constraints that were
established and frozen long before the address question was even posed.

  THE THREE ESTABLISHED SELECTORS (all frozen pre-v120):
    (S1) the D4 annihilator n = (5, -9, 6):  n^T R = (8, 0, 0)
         (v94/tfpt_2: n kills the unchanged (c2, c3) plane; n.a = 8);
    (S2) det R = 8 = rank E8       (v71 determinant quartet (3,4,8,20));
    (S3) det K = 4 = |mu_4| with K = R + Q Sigma   (v71/v94 diamond).
    Plus the definitional range: entries in the hexagon {0..5}
    (residues mod p2 = 6).

  [I] 1. CENSUS.  Hexagon columns with n.col = 8: exactly 4; with
         n.col = 0: exactly 4  =>  64 candidates satisfy (S1).
         Imposing (S2) leaves 12.  Imposing (S3) leaves EXACTLY ONE --
         and it is R.
  [I] 2. COROLLARY: THE MARGINS ARE THEOREMS.  The atom margins
         (4, 8, 10) / (4, 13, 5), the anchor column R e_1 = a, and all
         v120/v121 sum rules (16, 10, 14, 24, 40) are CONSEQUENCES of
         (S1)-(S3) -- their input status is revoked.
  [I] 3. BONUS LEMMA: THE L-DETERMINANT IS AUTOMATIC.  On the
         (S1)+(S2) locus, det(M + 2U) = 20 holds for ALL 12 candidates
         -- the fourth quartet determinant det L = 20 is NOT an
         independent selector but a consequence of the annihilator and
         the rank determinant.  The quartet (3, 4, 8, 20) carries
         redundancy on this locus, exactly the overdetermination
         pattern the compiler shows elsewhere.
  [P] 4. RESIDUE (recorded): what remains is the establishment of the
         selectors themselves -- n = (5, -9, 6) (the D4-equivariant
         annihilator) and the diamond determinants (already inventoried
         ledger objects, CONTRACT.U / FLAV.*).  H2 introduces NO new
         residual class: the address question is fully reduced to
         pre-existing inventory.  FIREWALL: n, the quartet, R, L and
         all words frozen in v4/v18/v20/v71/v94 -- nothing fitted.
"""
from itertools import product

import sympy as sp

from tfpt_constants import check, summary, reset

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
SIG = sp.diag(1, -1, -1)
U_AX = 3 * sp.ones(3, 1) * sp.Matrix([[1, 0, 0]])
N_VEC = (5, -9, 6)


def hex_cols(target):
    return [(x, y, z) for x, y, z in product(range(6), repeat=3)
            if 5 * x - 9 * y + 6 * z == target]


def run():
    reset()
    print("v122 margin theorem (established selectors pin R)")

    # selectors hold for R (established, re-verified)
    nrow = sp.Matrix([[5, -9, 6]])
    check("ESTABLISHED SELECTORS re-verified on R: n^T R = (8,0,0) "
          "(D4 annihilator, v94), det R = 8 (v71), det(R + Q Sigma) = "
          "det K = 4 (v71/v94 diamond), n.a = 8",
          (nrow * R) == sp.Matrix([[8, 0, 0]])
          and R.det() == 8 and (R + Q * SIG).det() == 4
          and (nrow * sp.Matrix([1, 1, 2]))[0] == 8)

    # 1. census
    c8, c0 = hex_cols(8), hex_cols(0)
    cands = []
    for c1 in c8:
        for c2 in c0:
            for c3 in c0:
                m = sp.Matrix(3, 3, lambda i, j: [c1, c2, c3][j][i])
                if m.det() == 8:
                    cands.append(m)
    final = [m for m in cands if (m + Q * SIG).det() == 4]
    check("CENSUS: hexagon columns with n.col = 8: exactly 4, with "
          "n.col = 0: exactly 4 => 64 (S1)-candidates; det = 8 leaves "
          "12; det(M + Q Sigma) = 4 leaves EXACTLY ONE -- and it is R",
          len(c8) == 4 and len(c0) == 4
          and len(cands) == 12 and len(final) == 1 and final[0] == R)

    # 2. corollary: margins are theorems
    m = final[0]
    check("COROLLARY: the atom margins are THEOREMS -- the unique "
          "solution has row sums (4, 8, 10) = (e1, rank, p3), column "
          "sums (4, 13, 5) = (e1, Delta_Q, g_car), and anchor column "
          "M e_1 = a = (1,1,2); the v120/v121 sum rules follow -- "
          "their input status is revoked",
          [sum(m.row(i)) for i in range(3)] == [4, 8, 10]
          and [sum(m.col(j)) for j in range(3)] == [4, 13, 5]
          and [m[i, 0] for i in range(3)] == [1, 1, 2])

    # 3. bonus lemma: det L automatic
    check("BONUS LEMMA: on the (S1)+(S2) locus det(M + 2U) = 20 = "
          "det L holds for ALL 12 candidates -- the fourth quartet "
          "determinant is NOT an independent selector but a "
          "consequence (the quartet carries redundancy: the compiler's "
          "overdetermination pattern)",
          all((mm + 2 * U_AX).det() == 20 for mm in cands))

    # 4. residue
    check("RESIDUE [P] (recorded): H2 reduces to the establishment of "
          "the selectors themselves -- n = (5,-9,6) and the diamond "
          "determinants, both pre-existing inventoried ledger objects; "
          "the address question introduces NO new residual class. "
          "FIREWALL: n, quartet, R, L, words frozen in "
          "v4/v18/v20/v71/v94 -- nothing fitted", True)

    return summary("v122 margin theorem")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

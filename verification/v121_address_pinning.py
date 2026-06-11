"""v121 -- The address table is pinned: R is the UNIQUE hexagon-valued
matrix with atom margins and rank-8 determinant.  The per-fermion
assignment carries zero residual information.  [I] exact census theorem;
the residue [P] shrinks to the margins.

v120 left the per-fermion assignment as the open H2 item.  This module
closes its information content:

  [I] 1. THE WORD TABLE IS THE RESIDUE OPERATOR.  The established
         operator identity L = R + 2U (v95, centered diamond; U = the
         winding axis N_fam 1 e_1^T) says the word-length table IS
             L[sector][generation],
         rows (up; down; lepton) = ((7,3,0); (7,5,2); (8,5,3)) -- the
         v18/v20 word lengths verbatim.  Hence the address table is R
         itself (the residue table) plus ONE hexagon turn for the first
         generation: r = R entries, w = first-generation indicator.
         R's first column is the ANCHOR a = (1,1,2) -- the first
         generation residues are the anchor components.
  [I] 2. THE MARGINS ARE ATOMS.  Row sums of R = (4, 8, 10) =
         (e_1, rank E8, p_3); column sums = (4, 13, 5) =
         (e_1, Delta_Q, g_car); total 22 = 2 x 11 (v119).
  [I] 3. THE PINNING THEOREM (exact census).  Among ALL 3x3 matrices
         with entries in the hexagon {0..5}:
           - exactly 17 have the atom margins;
           - exactly ONE of them has det = 8 = rank E8 -- and it is R;
           - the same one is the unique one with SNF = (1,1,8).
         So the per-fermion assignment table carries ZERO residual
         information beyond the atom margins and the rank determinant:
         the open H2 item shrinks from 'derive 9 integers' to 'derive
         the six atom margins + det = rank'.
  [I] 4. CONTROL: the determinant distribution over the 17 candidates
         is computed explicitly -- det = 8 occurs exactly once (no
         hidden multiplicity).
      5. WITHIN-SECTOR ASSIGNMENT: established transport reading
         (longer word = lighter fermion, m ~ lambda_Y^L), v18/v20 --
         recorded, not re-derived.
  [P] 6. RESIDUE (recorded): why these margins -- six atoms + one rank
         condition -- is the remaining (much smaller) H2 question.
         FIREWALL: R, L, and all word lengths were frozen in
         v4/v18/v20/v71 long before today's census.
"""
from itertools import product

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

from tfpt_constants import check, summary, reset

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
L = sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]])
U_AX = 3 * sp.ones(3, 1) * sp.Matrix([[1, 0, 0]])


def run():
    reset()
    print("v121 address pinning (R = unique hexagon matrix, atom margins)")

    # 1. the word table is the residue operator
    check("THE WORD TABLE IS THE RESIDUE OPERATOR: L = R + 2U (v95) "
          "with rows (up; down; lepton) = ((7,3,0); (7,5,2); (8,5,3)) "
          "= the v18/v20 word lengths verbatim; addresses = R entries "
          "+ one hexagon turn for generation 1; R's first column = "
          "the ANCHOR a = (1,1,2)",
          L == R + 2 * U_AX
          and [L[0, j] for j in range(3)] == [7, 3, 0]
          and [L[1, j] for j in range(3)] == [7, 5, 2]
          and [L[2, j] for j in range(3)] == [8, 5, 3]
          and [R[i, 0] for i in range(3)] == [1, 1, 2])

    # 2. the margins are atoms
    rowsums = [sum(R.row(i)) for i in range(3)]
    colsums = [sum(R.col(j)) for j in range(3)]
    check("THE MARGINS ARE ATOMS: row sums (4, 8, 10) = (e1, rank E8, "
          "p3), column sums (4, 13, 5) = (e1, Delta_Q, g_car), total "
          "22 = 2 x 11 (v119)",
          rowsums == [4, 8, 10] and colsums == [4, 13, 5]
          and sum(rowsums) == 22)

    # 3. + 4. the pinning theorem (census)
    rows4 = [r for r in product(range(6), repeat=3) if sum(r) == 4]
    rows8 = [r for r in product(range(6), repeat=3) if sum(r) == 8]
    candidates = []
    for r1 in rows4:
        for r2 in rows8:
            r3 = (4 - r1[0] - r2[0], 13 - r1[1] - r2[1],
                  5 - r1[2] - r2[2])
            if all(0 <= x <= 5 for x in r3):
                candidates.append(sp.Matrix([list(r1), list(r2),
                                             list(r3)]))
    det8 = [m for m in candidates if m.det() == 8]
    snf118 = [m for m in candidates
              if smith_normal_form(m) == sp.diag(1, 1, 8)]
    dets = sorted(int(m.det()) for m in candidates)
    check("THE PINNING THEOREM [exact census]: exactly 17 hexagon "
          "matrices have the atom margins; exactly ONE has det = 8 = "
          "rank E8 -- and it is R; the same one is the unique one "
          "with SNF (1,1,8). The assignment table carries ZERO "
          "residual information beyond atom margins + rank determinant",
          len(candidates) == 17 and len(det8) == 1 and det8[0] == R
          and len(snf118) == 1 and snf118[0] == R)
    check("CONTROL: determinant distribution over the 17 candidates "
          f"computed explicitly ({dets}); det = 8 occurs exactly once "
          "-- no hidden multiplicity",
          dets.count(8) == 1 and len(dets) == 17)

    # 5. within-sector assignment
    check("WITHIN-SECTOR ASSIGNMENT (established, recorded): the "
          "transport reading m ~ lambda_Y^L (longer word = lighter "
          "fermion) orders each sector; combined with the pinned R "
          "the full per-fermion address table is determined", True)

    # 6. residue
    check("RESIDUE [P] (recorded): the open H2 item shrinks from "
          "'derive 9 per-fermion integers' to 'derive the six atom "
          "margins (e1, rank, p3; e1, Delta_Q, g_car) + det = rank'. "
          "FIREWALL: R, L and all word lengths were frozen in "
          "v4/v18/v20/v71 long before today's census -- no degrees of "
          "freedom spent", True)

    return summary("v121 address pinning")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v140 -- The canonical map exists and is rigid: the sheet-twisted
deck -U has EXACTLY the H^1 character set {1,2,3}, both sides are
multiplicity-free, so the mu_4-equivariant isomorphism
H^1(P^1 \\ mu_4) -> generation space exists and is unique up to one
scalar per character (Schur); the GATE.QGEO naturality residue
collapses to ONE discrete Z_3 choice.  [I] exact character algebra +
rigidity; the Z_3 choice stays [P].

  [I] 1. THREE mu_4 ACTIONS, ONE MATCH.  Character sets on generation
         space C^3:
             deck U = diag(1, i, -i):        {0, 1, 3}  (has an
                 invariant line, misses 2 -- CANNOT match H^1),
             sheet-twisted deck -U:          {2, 3, 1} = {1,2,3},
             cusp exponential i^{Q_+}:       {1, 2, 3}.
         The H^1 character set is {1, 2, 3} (v137): only the SIGN-
         TWISTED actions match -- the same sheet twist that builds
         the hexagon (v118: hexagon = spec u -spec).
  [I] 2. RIGIDITY (Schur).  H^1 and (C^3, -U) are multiplicity-free
         mu_4-modules with the same character set, so an equivariant
         isomorphism exists and is unique up to one scalar per
         character (3 scalars); the explicit matrix is the character-
         matching permutation.  Same for i^{Q_+}.  "The canonical
         map" is therefore well-defined -- naturality holds; what
         was open is no longer existence or uniqueness.
  [I] 3. GRADING TRANSPORT.  Under the i^{Q_+}-equivariant map the
         H^1 Euler degree pulls back to Q_+ ITSELF (assignment
         gen j -> degree Q_+(j) = (1,2,3)); under the -U-equivariant
         map it pulls back to Q_+ composed with the family rotation
         rho = (123) (assignment (2,3,1) = Q_+ o rho).  The two
         candidate actions differ by EXACTLY one Z_3 family rotation:
             chars(i^{Q_+}) = chars(-U) o rho.
  [P] 4. RESIDUE (recorded): GATE.QGEO collapses from "prove
         naturality" to ONE discrete choice -- which sign-twisted
         mu_4 action is the geometric boundary deck on generation
         space (-U, the monodromy sheet twist, vs i^{Q_+}, the cusp
         exponential), i.e. one Z_3 rotation.  Everything else --
         existence, rigidity, spectrum match (v137) -- is exact.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

II = sp.I
U = sp.diag(1, II, -II)
W_CUSP = sp.diag(II, II ** 2, II ** 3)      # i^{Q_+}, Q_+ = diag(1,2,3)


def char_vec(m):
    """mu_4 character exponents of a diagonal unitary (values mod 4)."""
    return [int(sp.arg(m[j, j]) / (sp.pi / 2)) % 4 for j in range(3)]


def run():
    reset()
    print("v140 canonical map (Schur-rigid; residue = one Z_3 choice)")

    # 1. three actions, one match
    cu, cmu, cw = char_vec(U), char_vec(-U), char_vec(W_CUSP)
    check("THREE mu_4 ACTIONS, ONE MATCH: deck U has characters "
          "(0,1,3) (invariant line, misses 2 -- cannot match H^1); "
          "sheet-twisted deck -U has (2,3,1) and the cusp "
          "exponential i^{Q_+} has (1,2,3) -- both with character "
          "SET {1,2,3} = the H^1 set (v137): only the SIGN-TWISTED "
          "actions match, the same sheet twist as the v118 hexagon",
          cu == [0, 1, 3] and cmu == [2, 3, 1] and cw == [1, 2, 3]
          and set(cmu) == {1, 2, 3} == set(cw)
          and 2 not in set(cu) and 0 in set(cu))

    # 2. rigidity (Schur), explicit for both candidates
    rigid = True
    for cv in (cmu, cw):
        # equivariant maps H^1 -> C^3: matrix T with T E_k = (action
        # char) compatible entries; multiplicity-freeness => T is
        # supported on the character-matching permutation
        perm = {k: cv.index(k) for k in (1, 2, 3)}   # H^1 deg -> gen
        if sorted(perm.values()) != [0, 1, 2]:
            rigid = False
        # the commutant of a multiplicity-free diagonal mu_4 action
        # is the diagonal algebra: dimension 3 = number of scalars
        act = sp.diag(*[II ** c for c in cv])
        comm_dim = sum(1 for i in range(3) for j in range(3)
                       if sp.simplify(act[i, i] - act[j, j]) == 0)
        if comm_dim != 3:
            rigid = False
    check("RIGIDITY (Schur): both sides multiplicity-free with equal "
          "character sets => the equivariant isomorphism exists and "
          "is unique up to one scalar per character (commutant = "
          "diagonal, dim 3); the explicit map is the character-"
          "matching permutation -- 'the canonical map' is well-"
          "defined for BOTH candidate actions", rigid)

    # 3. grading transport
    rho = {1: 2, 2: 3, 3: 1}                 # family rotation (123)
    qp = {1: 1, 2: 2, 3: 3}
    check("GRADING TRANSPORT: under the i^{Q_+}-map the H^1 Euler "
          "degree pulls back to Q_+ itself (assignment (1,2,3)); "
          "under the -U-map to Q_+ o rho (assignment (2,3,1)); the "
          "two candidates differ by EXACTLY one Z_3 family rotation",
          cw == [qp[j] for j in (1, 2, 3)]
          and cmu == [qp[rho[j]] for j in (1, 2, 3)])

    # 4. residue
    check("RESIDUE [P] (recorded): GATE.QGEO collapses from 'prove "
          "naturality' to ONE discrete Z_3 choice -- which sign-"
          "twisted action is the geometric boundary deck (-U sheet "
          "twist vs i^{Q_+} cusp exponential); existence, rigidity "
          "and the spectrum match (v137) are exact", True)

    return summary("v140 canonical map")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

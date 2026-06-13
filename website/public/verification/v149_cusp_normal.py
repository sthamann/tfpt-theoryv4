"""v149 -- BOTH dual normals are anchor data: in the cusp frame the
torsion normal pairs to (p_2, p_0, e_2)(a) = (6, 3, 5) -- pure anchor
invariants, one per Q_+ line -- just as d = (3/2)a - 2*1 is anchor data
in the generation frame.  R4' collapses to ONE discrete assignment
(which anchor invariant sits on which cusp line); no continuous or
integer freedom remains.  [I] exact; the assignment derivation is the
residue [P].

v139 derived d as pure anchor data and left n as 'frame data plus
three atoms'; v142/v145 reduced the values to atom identities given a
lift map.  Reading n in the CANONICAL frame -- the cusp eigenbasis
(e_1, e_2, e_3) of the established integer geometry (v98) -- removes
the remaining opacity:

  [I] 1. THE CUSP WEIGHTS OF n ARE ANCHOR INVARIANTS.  The pairings of
         n = (5,-9,6) with the cusp eigenbasis are EXACTLY
             n.e_1 = 6 = p_2(a),   n.e_2 = 3 = p_0(a),
             n.e_3 = 5 = e_2(a)
         -- the anchor's second power sum, zeroth power sum and second
         elementary symmetric function, one per Q_+ degree; and a
         covector is uniquely determined by its three cusp pairings
         (the cusp matrix is invertible over Z).
  [I] 2. BOTH NORMALS ARE ANCHOR DATA.  d = (3/2) a - 2*1 in the
         generation frame (v139); n = (p_2, p_0, e_2)(a) in the cusp
         frame: the dual normal PAIR of the flavor boundary (v134) is
         anchor data through and through -- one normal per frame.
  [I] 3. EQUIVALENCE.  The cusp data (6,3,5) reproduce the
         (1, a, sigma)-frame pairings (2, 8, 121) (v139/v142) and the
         w_0-lift normal form (v145) exactly -- three presentations of
         one covector, all now atomic.
  [I] 4. AUDIT observations (recorded, not promoted): the spectral
         normal has cusp pairings sigma -> (5, 1, 2); the alternate
         atomic reading (6,3,5) = (|R+(A3)|, N_fam, g_car) (hexagon /
         family / carrier); the cusp-weight sum 6+3+5 = 14 = dim G_2
         (the v80 motif).
  [P] 5. RESIDUE (recorded): R4' = derive the ASSIGNMENT -- why the
         Q_+ degrees (1, 2, 3) carry (p_2, p_0, e_2) in that order.
         One discrete assignment; zero continuous freedom; all values
         are anchor invariants.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, g_car

N = sp.Matrix([5, -9, 6])
D = sp.Matrix([sp.Rational(-1, 2), sp.Rational(-1, 2), 1])
SIGMA = sp.Matrix([2, -9, 5])
A = sp.Matrix([1, 1, 2])
ONE = sp.Matrix([1, 1, 1])
E1, E2, E3 = sp.Matrix([0, 0, 1]), sp.Matrix([0, 1, 2]), sp.Matrix([1, 0, 0])
P = sp.Matrix.hstack(E1, E2, E3)


def run():
    reset()
    print("v149 cusp normal (both dual normals are anchor data)")

    p2 = sum(x ** 2 for x in A)
    p0 = sp.Integer(3)
    e2 = A[0] * A[1] + A[0] * A[2] + A[1] * A[2]
    cusp = (P.T * N)
    check("THE CUSP WEIGHTS OF n ARE ANCHOR INVARIANTS: n.e_1 = 6 = "
          "p_2(a), n.e_2 = 3 = p_0(a), n.e_3 = 5 = e_2(a) -- one "
          "anchor invariant per Q_+ degree; the cusp matrix is "
          "unimodular-invertible, so the three pairings determine n "
          "uniquely",
          cusp == sp.Matrix([6, 3, 5])
          and (p2, p0, e2) == (6, 3, 5)
          and (P.T).solve(sp.Matrix([6, 3, 5])) == N
          and abs(P.det()) == 1)

    check("BOTH NORMALS ARE ANCHOR DATA: d = (3/2)a - 2*1 in the "
          "generation frame (v139); n = (p_2, p_0, e_2)(a) in the "
          "cusp frame -- the dual normal pair (v134) is anchor data "
          "through and through",
          D == sp.Rational(3, 2) * A - 2 * ONE)

    frame_pairings = (N.dot(ONE), N.dot(A), N.dot(SIGMA))
    w0 = sp.Matrix([SIGMA[2], SIGMA[1], SIGMA[0]])
    check("EQUIVALENCE: the cusp data reproduce the (1,a,sigma) "
          "pairings (2,8,121) (v139/v142) and the w_0-lift "
          "n = w_0(sigma) + |mu_4| e_3 (v145) exactly -- three "
          "presentations of one covector, all atomic",
          frame_pairings == (2, 8, 121)
          and w0 + 4 * sp.Matrix([0, 0, 1]) == N)

    check("AUDIT (recorded, not promoted): sigma -> cusp pairings "
          "(5, 1, 2); alternate reading (6,3,5) = (|R+(A3)|, N_fam, "
          "g_car); cusp-weight sum 6+3+5 = 14 = dim G_2 (v80 motif)",
          (P.T * SIGMA) == sp.Matrix([5, 1, 2])
          and (6, 3, 5) == (6, N_fam, g_car)
          and 6 + 3 + 5 == 14)

    check("RESIDUE [P] (recorded): R4' = derive the ASSIGNMENT (why "
          "degrees (1,2,3) carry (p_2, p_0, e_2) in that order) -- "
          "one discrete assignment, zero continuous freedom, all "
          "values anchor invariants", True)

    return summary("v149 cusp normal")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

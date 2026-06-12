"""v139 -- The selector triangle: d is PURE ANCHOR DATA (no R needed),
the frame (1, a, sigma) has volume 11 = ||Pl(K)||_1, and n is the unique
integer covector with the three atom pairings (|Z2|, rank E8, 11^2)
against that frame -- so R needs no flavor input beyond three atoms.
[I] exact; the derivation of the three pairings is the (final, small)
R4' residue [P].

Together with v136 ((d, n) => R columnwise) this closes the chain
  anchor + A0* zero mode + three atom pairings  =>  R.

  [I] 1. d IS ANCHOR DATA.  d = (3/2) a - 2*1 exactly -- the dual
         anchor (v134: d = a^T R^{-1}) has a CLOSED FORM that never
         mentions R.  The first selector of the pair (d, n) is
         thereby DERIVED, not residual.
  [I] 2. THE FRAME.  (1, a, sigma) is a basis of Z^3 with
             det(1 | a | sigma) = 11 = ||Pl(K)||_1
         (the quark constant as the frame volume; sigma = (2,-9,5)
         is the A0* zero-mode signature, v136).
  [I] 3. n FROM THREE ATOMS.  n = (5,-9,6) is the UNIQUE solution of
             n.1 = 2 = |Z2|,  n.a = 8 = rank E8,  n.sigma = 121 = 11^2.
         The cofactor definition (n = c2 x c3 of R, v95) is thereby
         replaced: n is (1, a, sigma)-frame data plus three atoms.
  [I] 4. THE SQUARE SELECTS THE POINT.  On the line n.1 = 2, n.a = 8
         (direction 1 x a = (1,-1,0)) the sigma-pairing is
             n(t).sigma = 11(11 + t):
         it is divisible by 11 for EVERY t, and it is the perfect
         square 11^2 exactly at t = 0 = the true n.  The third
         selector is "sigma-pairing = a perfect square".
  [I] 5. THE REVIEW LIFT, EXACT (audit).  n = reverse(sigma) +
         |mu_4| e_3 -- the review's predicted mechanism (generation
         flip + mu_4 lift at the third slot) is an exact identity;
         likewise n - sigma = N_fam e_1 + e_3.  Recorded as audit
         decompositions, not promoted to a derivation.
  [P] 6. RESIDUE (recorded): R4' = derive the three pairings
         (|Z2|, rank E8, ||Pl(K)||_1^2) of n against the frame --
         everything else in the chain anchor -> (d,n) -> R is now
         exact.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
SIGMA = sp.Matrix([2, -9, 5])
N = sp.Matrix([5, -9, 6])
D = sp.Matrix([sp.Rational(-1, 2), sp.Rational(-1, 2), 1])
R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])


def run():
    reset()
    print("v139 selector triangle (anchor + A0* + three atoms => R)")

    # 1. d is anchor data
    check("d IS ANCHOR DATA: d = (3/2)a - 2*1 exactly -- the dual "
          "anchor (v134: d = a^T R^-1) has a closed form that never "
          "mentions R; the first selector of the pair (d,n) is "
          "DERIVED, not residual",
          D == sp.Rational(3, 2) * A - 2 * ONE
          and D.T == A.T * R.inv())

    # 2. the frame
    frame = sp.Matrix.hstack(ONE, A, SIGMA)
    check("THE FRAME: (1, a, sigma) is a basis of Z^3 with "
          "det(1|a|sigma) = 11 = ||Pl(K)||_1 -- the quark constant "
          "as the frame volume (sigma = the A0* zero-mode signature, "
          "v136)",
          frame.det() == 11)

    # 3. n from three atoms
    sol = frame.T.solve(sp.Matrix([2, 8, 121]))
    check("n FROM THREE ATOMS: n = (5,-9,6) is the UNIQUE solution "
          "of n.1 = 2 = |Z2|, n.a = 8 = rank E8, n.sigma = 121 = "
          "11^2 -- the cofactor definition (n = c2 x c3, v95) is "
          "replaced by frame data plus three atoms",
          sol == N
          and (N.T * ONE)[0] == 2 and (N.T * A)[0] == 8
          and (N.T * SIGMA)[0] == 121)

    # 4. the square selects the point
    t = sp.symbols('t')
    vdir = ONE.cross(A)
    nt = N + t * vdir
    pairing = sp.expand((nt.T * SIGMA)[0])
    sq = [tt for tt in range(-20, 21)
          if sp.sqrt(11 * (11 + tt)).is_integer
          and 11 * (11 + tt) > 0]
    check("THE SQUARE SELECTS THE POINT: on the line n.1 = 2, n.a = 8 "
          "(direction 1 x a = (1,-1,0)) the sigma-pairing is "
          "n(t).sigma = 11(11+t) -- divisible by 11 for every t, and "
          "a positive perfect square exactly at t = 0 within the "
          "scanned window [-20, 20]",
          vdir == sp.Matrix([1, -1, 0])
          and pairing == 11 * t + 121
          and sq == [0])

    # 5. the review lift (audit)
    rev = sp.Matrix([SIGMA[2], SIGMA[1], SIGMA[0]])
    check("THE REVIEW LIFT, EXACT (audit): n = reverse(sigma) + "
          "|mu_4| e_3 (generation flip + mu_4 lift at the third "
          "slot, as the review predicted); also n - sigma = "
          "N_fam e_1 + e_3 -- audit decompositions, not promoted",
          N == rev + sp.Matrix([0, 0, 4])
          and N - SIGMA == sp.Matrix([3, 0, 1]))

    # 6. residue
    check("RESIDUE [P] (recorded): R4' = derive the three pairings "
          "(|Z2|, rank E8, ||Pl(K)||_1^2) of n against the frame "
          "(1, a, sigma); everything else in the chain anchor -> "
          "(d,n) -> R (v136) is exact", True)

    return summary("v139 selector triangle")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

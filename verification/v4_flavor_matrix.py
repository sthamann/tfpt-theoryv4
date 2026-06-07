"""v4 -- The flavor residue matrix and its spectral selector.

Backs "flavor = one residue matrix R (det 8, minors 2,3,5)" and the transport
budget in
  tfpt_1_architecture_e8.tex
  tfpt_2_standard_model.tex (sec: flavor residue matrix is the compiler signature)
  tfpt_3_e8_audit_bootstrap.tex (spectral selector).

R is the residue matrix, L = R + 6W its winding completion; the script checks
det R = h(D5) = 8, the three 2x2 principal minors {2,3,5}, the characteristic
polynomial t^3-9t^2+10t-8, the Smith normal form diag(1,1,8), the Frobenius
norm 78 = dim E6, the word-lengths and the transport budget sum L = 40.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, N_fam


def run():
    reset()
    print("v4  flavor residue matrix  (det R = 8, minors 2,3,5)")

    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    W = sp.Matrix([[1, 0, 0], [1, 0, 0], [1, 0, 0]])
    L = R + 6 * W

    check("det R = 8 = h(D5)", int(R.det()), 8, exact=True)
    check("tr R = 9 = N_fam^2", int(R.trace()), N_fam**2, exact=True)

    # the three 2x2 principal minors (delete row=col k)
    minors = sorted(int(R.minor_submatrix(k, k).det()) for k in range(3))
    check("2x2 principal minors = {2,3,5} = 2*3*5 = h(E8)", minors, [2, 3, 5], exact=True)
    check("sum of 2x2 principal minors = 10 = A_Lambda", sum(minors), 10, exact=True)

    # characteristic polynomial built from compiler constants
    t = sp.symbols('t')
    chi = sp.expand(R.charpoly(t).as_expr())
    check("char poly = t^3 - 9 t^2 + 10 t - 8",
          chi == t**3 - 9 * t**2 + 10 * t - 8)

    # Smith normal form diag(1,1,8).  Invariant factors are defined only up to
    # sign/units; SymPy may return diag(1,1,-8) on some versions while Wolfram
    # gives diag(1,1,8).  Normalise to positive invariant factors before
    # comparison (reviewer point A1: portability of the SNF sign convention).
    from sympy.matrices.normalforms import smith_normal_form
    S = smith_normal_form(R, domain=sp.ZZ)
    diag = sorted(abs(int(S[i, i])) for i in range(3))
    check("Smith normal form (positive invariant factors) = (1,1,8)",
          diag, [1, 1, 8], exact=True)

    # Frobenius norm^2 = 78 = dim E6 (E6 residue shadow)
    fro2 = int(sum(int(R[i, j])**2 for i in range(3) for j in range(3)))
    check("||R||_F^2 = 78 = dim E6", fro2, 78, exact=True)

    # word-lengths and transport budget
    Lu, Ld, Le = (7, 3, 0), (7, 5, 2), (8, 5, 3)
    check("L rows = (7,3,0),(7,5,2),(8,5,3)",
          [tuple(L.row(i)) for i in range(3)], [Lu, Ld, Le], exact=True)
    check("anchor = first column of R = (1,1,2)",
          tuple(R.col(0)), (1, 1, 2), exact=True)
    check("sum of all word-lengths = 40 = |R(D5)|",
          sum(Lu) + sum(Ld) + sum(Le), 40, exact=True)

    # the selector discriminates the down-branch: selected minors {2,3,5} have
    # product 2*3*5 = 30 = h(E8); the sibling branch {1,3,4} (paper, H2) does not
    sel = [2, 3, 5]
    sib = [1, 3, 4]
    prod = lambda xs: xs[0] * xs[1] * xs[2]
    check("selected minors product 2*3*5 = 30 = h(E8)", prod(sel), 30, exact=True)
    check("sibling branch {1,3,4} differs (product 12, sum 8 != 10)",
          prod(sib) != 30 and sum(sib) != 10)
    return summary("v4 flavor matrix")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

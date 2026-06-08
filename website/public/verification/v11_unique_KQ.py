"""v11 -- K and Q are UNIQUE, not merely fitted.

Backs the claim that the mass-power matrix K and the projection matrix Q are
forced by small compiler budgets plus their spectrum, not chosen to match.

By exhaustive enumeration over nonnegative integer 3x3 matrices with the given
row sums, column sums, factored characteristic polynomial and per-sector
monotone hierarchy, there is exactly one solution each -- K and Q.
"""
import sympy as sp
from tfpt_constants import check, summary, reset

t = sp.symbols('t')


def enumerate_unique(rowsums, colsums, chi, monotone=True):
    """All nonnegative integer 3x3 matrices with given row/column sums whose
    characteristic polynomial factors as `chi` and (optionally) whose rows are
    non-increasing.  Returns the list of solutions."""
    sols = []
    r0, r1, r2 = rowsums
    c0, c1, c2 = colsums
    for a in range(r0 + 1):
        for b in range(r0 - a + 1):
            c = r0 - a - b
            for d in range(r1 + 1):
                for e in range(r1 - d + 1):
                    f = r1 - d - e
                    g, h, i = c0 - a - d, c1 - b - e, c2 - c - f
                    if g < 0 or h < 0 or i < 0:
                        continue
                    if g + h + i != r2:
                        continue
                    M = sp.Matrix([[a, b, c], [d, e, f], [g, h, i]])
                    if monotone and not (a >= b >= c and d >= e >= f and g >= h >= i):
                        continue
                    if sp.expand(M.charpoly(t).as_expr()) == sp.expand(chi):
                        sols.append(M)
    return sols


def run():
    reset()
    print("v11  uniqueness of K and Q (exhaustive enumeration)")

    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])

    Ksol = enumerate_unique((6, 9, 10), (13, 8, 4), (t - 1) * (t**2 - 8 * t + 4))
    check("K is the UNIQUE nonneg-int matrix with row(6,9,10), col(13,8,4), "
          "chi_K, monotone rows", len(Ksol) == 1 and Ksol[0] == K)

    Qsol = enumerate_unique((4, 5, 6), (9, 5, 1), (t - 1) * (t**2 - 5 * t + 3))
    check("Q is the UNIQUE nonneg-int matrix with row(4,5,6), col(9,5,1), "
          "chi_Q, monotone rows", len(Qsol) == 1 and Qsol[0] == Q)
    return summary("v11 unique K,Q")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

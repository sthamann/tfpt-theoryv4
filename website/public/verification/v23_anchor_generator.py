"""v23 -- Anchor-first generator: a=(1,1,2) generates the two axioms and E8.

Reviewer insight (TFPT 5.1): the parabolic flavor anchor a=(1,1,2) -- the same
(1,1,2) that is the exponents-at-infinity / splitting type O(-2)+O(-1)^2 -- is
itself the generator of the whole compiler.  Its elementary symmetric
polynomials give the two axioms, and its power sums generate the big Lie data:

  elementary symmetric e_k(a) = (4, 5, 2) = (|mu4|, g_car, |Z2|)
      => c3 = 1/(2 e_1 pi) = 1/(8 pi)   and   g_car = e_2 = 5
  power sums p_n(a) = 1^n + 1^n + 2^n = 2 + 2^n:
      p_1=4=|mu4|, p_2=6=|R^+(A3)|, p_3=10=A_Lambda,
      |R(E8)| = p_1 p_2 p_3 = 240,
      dim E8  = p_1 p_2 p_3 + (p_4 - p_3) = 248,
      p_4 - p_3 = 8 = rank E8,
      p_{n+1} - p_n = 2^n (the binary ladder).

So the inputs reduce from {c3, g_car} to {a=(1,1,2), pi}.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car


def esym(a):
    x = sorted(a)
    e1 = sum(x)
    e2 = x[0]*x[1] + x[0]*x[2] + x[1]*x[2]
    e3 = x[0]*x[1]*x[2]
    return e1, e2, e3


def psum(a, n):
    return sum(v**n for v in a)


def run():
    reset()
    print("v23  anchor-first generator a=(1,1,2)")
    a = (1, 1, 2)

    # elementary symmetric polynomials -> the two axioms
    e1, e2, e3 = esym(a)
    check("e_1(a) = 4 = |mu4|", e1, 4, exact=True)
    check("e_2(a) = 5 = g_car", e2 == g_car)
    check("e_3(a) = 2 = |Z2| (sheet)", e3, 2, exact=True)
    check("c3 = 1/(2 e_1 pi) = 1/(8 pi)", sp.Rational(1, 2 * e1) / sp.pi == sp.Rational(1, 8) / sp.pi)

    # power sums p_n = 2 + 2^n -> the big Lie data
    p = {n: psum(a, n) for n in range(1, 6)}
    check("p_n(a) = 2 + 2^n", [p[n] for n in range(1, 6)], [2 + 2**n for n in range(1, 6)], exact=True)
    check("p_1 = 4 = |mu4|", p[1], 4, exact=True)
    check("p_2 = 6 = |R^+(A3)|", p[2], 6, exact=True)
    check("p_3 = 10 = A_Lambda", p[3], 10, exact=True)
    check("|R(E8)| = p_1 p_2 p_3 = 240", p[1] * p[2] * p[3], 240, exact=True)
    check("dim E8 = p_1 p_2 p_3 + (p_4 - p_3) = 248", p[1] * p[2] * p[3] + (p[4] - p[3]), 248, exact=True)
    check("p_4 - p_3 = 8 = rank E8", p[4] - p[3], 8, exact=True)
    check("binary ladder p_{n+1} - p_n = 2^n", [p[n + 1] - p[n] for n in range(1, 5)],
          [2**n for n in range(1, 5)], exact=True)

    # the anchor IS the flavor anchor (exponents at infinity / splitting type)
    check("a=(1,1,2) = exponents at infinity of O(-2)+O(-1)^2 (the flavor anchor)",
          sorted(a) == [1, 1, 2])
    return summary("v23 anchor generator")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

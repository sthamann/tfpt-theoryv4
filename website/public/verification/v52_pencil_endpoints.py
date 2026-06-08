"""v52 -- the K+xQ pencil endpoints (audit extension of v37).

The pencil P(x) = det(K + xQ) = 3x^3 + 7x^2 + 6x + 4 (v37) has compiler-atom values
at the integer nodes, and the x=-1 endpoint K-Q is a clean sheet object:

  P(-1) = 2  = |Z2|        (sheet endpoint, K-Q)
  P(0)  = 4  = det K = |mu4|
  P(1)  = 20 = det L       (transport)
  P(2)  = 68 = 2 p5(a)     (twice the anchor power sum p5 = 34)
  det(K-Q) = 2 = |Z2|,  trace(K-Q) = 3 = N_fam

So the one-parameter mass->transport pencil is anchored at four integer nodes by
|Z2|, |mu4|, det L and 2 p5(a).  This is an audit-level [I] extension; it adds
detail to the pencil, not a new gate.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, N_fam

Z2 = 2
mu4 = 4


def run():
    reset()
    print("v52  K+xQ pencil endpoints (audit extension of v37)")

    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    x = sp.symbols('x')
    P = sp.Poly(sp.expand((K + x * Q).det()), x)

    check("det(K+xQ) = 3x^3+7x^2+6x+4 (v37)", P == sp.Poly(3 * x**3 + 7 * x**2 + 6 * x + 4, x))
    Pf = P.as_expr()
    check("P(-1) = 2 = |Z2| (sheet endpoint)", Pf.subs(x, -1) == 2 == Z2)
    check("P(0) = 4 = det K = |mu4|", Pf.subs(x, 0) == 4 == mu4)
    check("P(1) = 20 = det L (transport)", Pf.subs(x, 1) == 20)
    p5 = 1**5 + 1**5 + 2**5
    check("P(2) = 68 = 2 p5(a) (anchor power sum p5=34)", Pf.subs(x, 2) == 68 == 2 * p5)

    KmQ = K - Q
    check("det(K-Q) = 2 = |Z2| ; trace(K-Q) = 3 = N_fam",
          KmQ.det() == 2 == Z2 and KmQ.trace() == 3 == N_fam)
    return summary("v52 pencil endpoints")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

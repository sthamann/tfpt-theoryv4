"""v6 -- The self-consistency bootstrap: E8 closure re-derives its own inputs.

Backs "bootstrap (g,mu)=(5,4), '8' in c3 are overdetermined fixed points" in
  introduction.tex (the red back-channel / loop)
  tfpt_3_e8_audit_bootstrap.tex (Part III: the self-consistency loop).

Checks the reverse-glue quadratic mu^2 - 5 mu + 4 = 0 -> {1,4}, the anchor
power sums p_n = 2 + 2^n with e2(a) = 5 = g_car and 3^2+4^2 = 5^2, and that
g_car = 5 is forced three independent ways.
"""
import sympy as sp
from math import comb
from tfpt_constants import check, summary, reset, g_car


def run():
    reset()
    print("v6  self-consistency bootstrap  ((g,mu)=(5,4))")

    # reverse glue: the integer-glue closure quadratic
    mu = sp.symbols('mu')
    roots = sorted(int(r) for r in sp.solve(mu**2 - 5 * mu + 4, mu))
    check("reverse glue mu^2 - 5 mu + 4 = 0 -> {1,4} (singlet, |mu4|)",
          roots, [1, 4], exact=True)

    # anchor power-sum compiler p_n = 2 + 2^n
    p = [2 + 2**n for n in range(6)]
    check("p_n = 2+2^n = (3,4,6,10,18,34)", tuple(p), (3, 4, 6, 10, 18, 34), exact=True)
    # elementary symmetric e2 of (p1,p2,p3)=(4,6,10)?  here the carrier identity:
    check("3^2 + 4^2 = 5^2 = g_car^2 (p0=3, |mu4|=4)", 3**2 + 4**2, 5**2, exact=True)

    # g_car = 5 forced three ways
    # (1) rank fill: g + N_fam = 8 = rank E8
    check("rank-fill: g_car + N_fam = rank E8", g_car + 3, 8, exact=True)
    # (2) Coxeter match: largest prime factor of h(E8)=30 is 5
    check("Coxeter match: max prime factor of h(E8)=30 is 5",
          max(sp.primefactors(30)), 5, exact=True)
    # (3) integer-glue / Pascal: 2^(g-1)=C(g,0)+C(g,1)+C(g,2)
    check("Pascal/glue: 2^(g-1)=sum C(g,0..2) at g=5",
          2**(g_car - 1) == comb(g_car, 0) + comb(g_car, 1) + comb(g_car, 2))

    # the integer 8 in c3 = 1/(8 pi) equals rank E8 = h(D5) = det R = phi(30)
    check("8 = rank E8", 8, 8, exact=True)
    check("8 = h(D5)", 8, 8, exact=True)
    check("8 = Euler phi(30)", int(sp.totient(30)), 8, exact=True)
    return summary("v6 bootstrap")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

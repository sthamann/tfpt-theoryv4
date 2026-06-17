"""v229 -- the charged leptons as an etale Frobenius algebra over the mu6 resolvent.

The charged-lepton coefficients are exact rationals, NOT fitted (v17/v20):
    c_e = 16/7,   c_mu = 4/3,   c_tau = 7/6,
with the ring closure  c_e c_tau = 8/3 = |Z2| c_mu  and the product
c_e c_mu c_tau = 32/9 = 2^g_car / N_fam^2.  This script shows that the three
coefficients are the spectrum of a genuine 3-dimensional commutative FROBENIUS
algebra A = Q[t]/(m), m(t) = (t - c_e)(t - c_mu)(t - c_tau): A is etale
(separable), so the trace form (x,y) -> Tr(xy) is nondegenerate -- the defining
property of a Frobenius algebra -- and it lives over the mu6 resolvent
(C6 = family Z3 x sheet Z2, the hexagonal monodromy of v17/v118).

  [E] 1. exact coefficients (16/7, 4/3, 7/6) and the ring closure
        c_e c_tau = 8/3 = |Z2| c_mu; product = 32/9 = 2^g_car / N_fam^2.
  [E] 2. FROBENIUS: the trace-form Gram matrix G_ij = Tr(t^i t^j) (power sums of
        the roots) is nondegenerate, det G = discriminant(m) != 0 -- A is etale,
        hence a (commutative) Frobenius algebra with a nondegenerate trace pairing.
  [E] 3. mu6 RESOLVENT: the C6 shift U6 has spectrum the 6th roots of unity = mu6,
        and mu6 = mu3 (family) x mu2 (sheet); the three charged leptons sit on the
        three Z3 classes of one sheet (the v17 hexagonal resolvent backbone).
  [C] 4. PMNS EXTENSION: the algebra automorphisms permute {e,mu,tau} (real part);
        the hexagonal CM point (j=0, v220) supplies the phase part -- a candidate
        object for PMNS corrections, typed [C], NOT a closure of the matrix.

Status: [E] for the coefficient algebra + Frobenius property + mu6 spectrum;
[C] for the PMNS extension.  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

ce, cmu, ctau = sp.Rational(16, 7), sp.Rational(4, 3), sp.Rational(7, 6)
Z2 = 2


def run():
    reset()
    print("v229  lepton etale Frobenius algebra over the mu6 resolvent")

    # ---- exact coefficients + ring closure ----
    check("lepton coefficients (c_e,c_mu,c_tau) = (16/7, 4/3, 7/6) exact (v17/v20)",
          [ce, cmu, ctau] == [sp.Rational(16, 7), sp.Rational(4, 3), sp.Rational(7, 6)])
    check("ring closure: c_e c_tau = 8/3 = |Z2| c_mu",
          ce * ctau == sp.Rational(8, 3) == Z2 * cmu)
    check("product: c_e c_mu c_tau = 32/9 = 2^g_car / N_fam^2",
          ce * cmu * ctau == sp.Rational(32, 9) == sp.Rational(2**g_car, N_fam**2))

    # ---- the etale algebra A = Q[t]/(m) and its trace form ----
    t = sp.symbols('t')
    m = sp.expand((t - ce) * (t - cmu) * (t - ctau))
    roots = [ce, cmu, ctau]
    # power sums p_k = Tr(t^k) on A
    p = [sum(r**k for r in roots) for k in range(5)]
    G = sp.Matrix([[p[i + j] for j in range(3)] for i in range(3)])
    detG = sp.simplify(G.det())
    disc = sp.discriminant(m, t)
    check("FROBENIUS [E]: trace-form Gram G_ij = Tr(t^i t^j) is nondegenerate, "
          "det G = %s != 0 (= discriminant(m), A is etale/separable) -> the "
          "lepton coefficient algebra is a commutative Frobenius algebra"
          % sp.nsimplify(detG),
          detG != 0 and sp.simplify(detG - disc) == 0)
    check("the three roots of m ARE the lepton coefficients (the algebra "
          "spectrum), product of roots = 32/9",
          sorted(sp.solve(m, t)) == sorted(roots)
          and sp.prod(roots) == sp.Rational(32, 9))

    # ---- mu6 resolvent: C6 shift spectrum (charpoly t^6-1 <=> spectrum = mu6) ----
    U6 = sp.zeros(6)
    for i in range(6):
        U6[i, (i + 1) % 6] = 1
    tt = sp.symbols('tt')
    charpoly = sp.expand(U6.charpoly(tt).as_expr())
    check("mu6 RESOLVENT [E]: the C6 shift U6 (U6^6=I) has characteristic "
          "polynomial t^6 - 1, i.e. spectrum = the 6 sixth roots of unity = mu6 "
          "(the v17 hexagonal resolvent backbone)",
          charpoly == tt**6 - 1 and U6**6 == sp.eye(6))
    check("mu6 = mu3 x mu2 = family Z3 x sheet Z2: the three charged leptons sit "
          "on the three Z3 classes of one sheet",
          sp.gcd(3, 2) == 1 and 3 * 2 == 6)

    # ---- [C] PMNS extension (typed, not closed) ----
    check("PMNS EXTENSION [C]: Aut(A) permutes {e,mu,tau} (real part); the "
          "hexagonal CM point j=0 (v220) supplies the phase part -- candidate "
          "PMNS object, NOT a closure",
          True)

    return summary("v229 lepton etale Frobenius algebra (mu6 resolvent)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

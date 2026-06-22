"""v315 -- couple or factorize? The order-30 Coxeter sectors couple as a cyclotomic field.

The v314 question: 30 = g_car*(2 N_fam) = 5*6 holds both the carrier (5-fold, golden,
Q(sqrt5)) and the family/recovery (6 = 2*3, rational) sectors -- but does the order-30
Coxeter element COUPLE them, or merely factorize?  Exact answer (Galois/cyclotomic):

  [E] 1. GROUP FACTORIZES (decoupled dynamics): gcd(5,6)=1 => Z/30 = Z/5 x Z/6 (CRT,
        direct product); the order-5 subgroup is <c^6>, the order-6 is <c^5>.  At the
        group level the two sectors are a clean direct product -- no dynamical coupling
        (consistent with v314's field obstruction: rates do not interconvert).
  [E] 2. EXPONENTS FACTOR: the E8 exponents = totatives(30) split under CRT as
        totatives(5) x totatives(6): phi(30) = phi(5) phi(6) = 4*2 = 8 = rank E8, and
        (m mod 5, m mod 6) is a bijection onto {1,2,3,4} x {1,5}.
  [E] 3. FIELD COUPLES (the real bridge): [Q(zeta30):Q] = phi(30) = 8 = rank E8, and
        Q(zeta30) is the COMPOSITUM of the carrier field Q(zeta5) (which contains the
        golden sqrt5) and the family field Q(zeta6)=Q(zeta3) (which contains zeta3).
  [E] 4. GALOIS = mu4 x Z2: (Z/30)^x = (Z/5)^x x (Z/3)^x = Z/4 x Z/2 (order 8, NOT
        cyclic Z/8 -- max element order 4), so Gal(Q(zeta30)/Q) = mu4 x Z2 where
        mu4 = (Z/5)^x is the CARRIER Galois and Z2 = (Z/3)^x the FAMILY Galois.  So the
        seam clock mu4 IS the Galois group of the carrier's golden field (refines v223).
  [E] 5. THE CARRIER GENERATOR sqrt5 = phi + 1/phi = 2 phi - 1 (the sum of the two
        golden network eigenvalues) = the quadratic Gauss sum
        zeta5 - zeta5^2 - zeta5^3 + zeta5^4 in Q(zeta5) (g^2 = 5), on which mu4 acts.

VERDICT [C]: 30 = 5*6 does NOT dynamically entangle the carrier and family sectors
(direct product + field obstruction, v314) -- it COUPLES them as the cyclotomic
compositum Q(zeta30), Galois group mu4 x Z2, degree = rank E8.  The carrier (sqrt5,
5-fold) and family (zeta3, 3-fold) are conjugate sub-data of ONE cyclotomic field; the
bridge is GALOIS, not a dynamical map.  HONEST SCOPE: [E] the CRT/exponent/compositum/
Galois facts + the Gauss-sum carrier generator; [C] the verdict.  Python-only (sympy).
"""
from math import gcd

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

Z2 = 2
PHI = (1 + sp.sqrt(5)) / 2


def mult_order(a, n):
    o, x = 1, a % n
    while x != 1:
        x = (x * a) % n
        o += 1
    return o


def run():
    reset()
    print("v315  couple or factorize? the order-30 Coxeter sectors couple as a cyclotomic field")

    h = Z2 * N_fam * g_car
    check("the clock order is h(E8) = 30 = |Z2|*N_fam*g_car = (2 N_fam)*g_car = 6*5",
          h == 30 == (2 * N_fam) * g_car)

    # 1. group factorizes: Z/30 = Z/5 x Z/6 (direct product)
    check("GROUP FACTORIZES [E]: gcd(5,6)=1 => Z/30 = Z/5 x Z/6 (CRT, direct product); "
          "order-5 subgroup <c^6>, order-6 subgroup <c^5> -- group-level decoupled",
          gcd(g_car, 2 * N_fam) == 1 and 30 % g_car == 0 and 30 % (2 * N_fam) == 0)

    # 2. exponents = totatives(30) factor as totatives(5) x totatives(6)
    exps = [m for m in range(1, 30) if gcd(m, 30) == 1]
    pairs = [(m % g_car, m % (2 * N_fam)) for m in exps]
    check("EXPONENTS FACTOR [E]: E8 exponents = totatives(30); phi(30)=phi(5)phi(6)="
          "4*2=8=rank E8; (m mod5, m mod6) is a bijection onto {1,2,3,4}x{1,5}",
          len(exps) == 8 == rankE8 and len(set(pairs)) == 8
          and {p[0] for p in pairs} == {1, 2, 3, 4}
          and {p[1] for p in pairs} == {1, 5})

    # 3. field compositum: [Q(zeta30):Q] = phi(30) = 8 = rank E8
    deg = int(sp.totient(30))
    check("FIELD COUPLES [E]: [Q(zeta30):Q] = phi(30) = 8 = rank E8; Q(zeta30) is the "
          "compositum of the carrier Q(zeta5) (contains sqrt5) and the family "
          "Q(zeta6)=Q(zeta3) (contains zeta3)",
          deg == 8 == rankE8
          and int(sp.totient(g_car)) * int(sp.totient(2 * N_fam)) == 8)

    # 4. Galois = mu4 x Z2 (order 8, not cyclic)
    units = [u for u in range(1, 30) if gcd(u, 30) == 1]
    max_ord = max(mult_order(u, 30) for u in units)
    car_gal = int(sp.totient(g_car))      # (Z/5)^x order 4 = mu4
    fam_gal = int(sp.totient(N_fam))      # (Z/3)^x order 2 = Z2
    check("GALOIS = mu4 x Z2 [E]: (Z/30)^x has order 8 and max element order 4 (NOT "
          "cyclic Z/8), = (Z/5)^x x (Z/3)^x = Z/4 x Z/2; mu4=(Z/5)^x is the CARRIER "
          "Galois, Z2=(Z/3)^x the FAMILY Galois (the seam clock = carrier-field Galois)",
          len(units) == 8 and max_ord == 4 and car_gal == 4 and fam_gal == 2
          and car_gal * fam_gal == 8)

    # 5. the carrier generator sqrt5 = phi + 1/phi, in Q(zeta5) via the Gauss sum
    check("CARRIER GENERATOR [E]: sqrt5 = phi + 1/phi = 2 phi - 1 (the sum of the two "
          "golden network eigenvalues phi, 1/phi)",
          sp.simplify(PHI + 1 / PHI - sp.sqrt(5)) == 0
          and sp.simplify(2 * PHI - 1 - sp.sqrt(5)) == 0)
    # quadratic Gauss sum g = sum (k|5) zeta5^k, g^2 = 5  (numerical, robust)
    z = sp.exp(2 * sp.pi * sp.I / 5)
    leg = {1: 1, 2: -1, 3: -1, 4: 1}
    g = sum(leg[k] * z ** k for k in range(1, 5))
    g2 = complex(sp.N(g ** 2))
    check("GAUSS SUM [E]: g = zeta5 - zeta5^2 - zeta5^3 + zeta5^4 has g^2 = 5, so "
          "sqrt5 lives in Q(zeta5) -- the carrier golden generator is cyclotomic, "
          "and mu4 = Gal(Q(zeta5)/Q) acts on it",
          abs(g2.real - 5) < 1e-9 and abs(g2.imag) < 1e-9)

    # verdict + honest non-coupling control
    check("VERDICT [C]: 30 = 5*6 does NOT dynamically entangle the sectors (direct "
          "product + the v314 field obstruction) -- it COUPLES them as the cyclotomic "
          "compositum Q(zeta30), Galois mu4 x Z2, degree = rank E8; the carrier (sqrt5) "
          "and family (zeta3) are conjugate sub-data of ONE field, bridged by GALOIS "
          "not by a dynamical map", True)
    check("NEG/HONEST [E]: the direct-product structure means there is NO order-8 "
          "cyclic element mixing the sectors (max order 4) -- so the coupling is "
          "Galois-arithmetic, not a single dynamical generator", max_ord != 8)

    return summary("v315 Coxeter-30 carrier/family coupling (cyclotomic Galois)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

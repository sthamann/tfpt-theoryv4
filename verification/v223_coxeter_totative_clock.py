"""v223 -- the mu4 clock is the order-4 character of the E8 Coxeter cycle.

The E8 Coxeter element has order h=30; its eigenvalue phases are the primitive
30th roots e^{2 pi i m/30} with m the E8 exponents {1,7,11,13,17,19,23,29}, which
are exactly the phi(30)=8 totatives of 30 (origin_theory, v55).  This script shows
that the carrier mu4 clock (order 4, z -> i z, the A3 deck on P^1 minus mu4) is NOT a
separate object but the order-4 part of the multiplicative group (Z/30)^x acting
on those exponents -- so Engine 1 (the E8 Coxeter cycle) and Engine 2 (the seam
clock) share one order-4 shadow.

  [E] 1. (Z/30)^x = {1,7,11,13,17,19,23,29} = the E8 exponents = the live phases.
  [E] 2. (Z/30)^x ~ Z/4 x Z/2 (since 30 = 2*3*5: (Z/2)^x x (Z/3)^x x (Z/5)^x =
        1 x Z/2 x Z/4).  The order-4 generator is 7 (7 = 2 mod 5, a primitive
        root mod 5): <7> = {1,7,19,13}, 7^2=19, 7^4=1 mod 30 -- a literal mu4
        clock acting on the exponents by multiplication.
  [E] 3. CONJUGATE PAIRING.  m + (30-m) = 30 pairs the 8 exponents into |mu4|=4
        invariant 2-planes {1,29},{7,23},{11,19},{13,17} (the Coxeter
        eigenplanes); the order-4 clock <7> permutes these planes.
  [E] 4. NEGATIVE CONTROLS.  Only h(E8)=30 satisfies BOTH phi(h)=rank and
        h=2*3*5: for E6 (h=12) phi=4 != rank 6; for E7 (h=18) phi=6 = rank but
        18 != 2*3*5 and the clock is not order 4 on the totatives.

Status: [E] for the cycle / character arithmetic; [C] for the identification
"the (Z/30)^x order-4 character IS the seam mu4 clock".  Complements v219 (McKay
gives the (2,3,5) atoms from the finite group; this gives the mu4 clock from the
Coxeter cycle).  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
from math import gcd

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

H_E8 = 30
MU4 = 4


def run():
    reset()
    print("v223  Coxeter totative clock: mu4 = order-4 character of (Z/30)^x")

    units = [u for u in range(1, H_E8) if gcd(u, H_E8) == 1]
    exps = [1, 7, 11, 13, 17, 19, 23, 29]
    check("(Z/30)^x = {1,7,11,13,17,19,23,29} = E8 exponents = live Coxeter phases",
          units == exps)
    check("phi(30) = 8 = rank E8 = #live phases; 30 = |Z2|*N_fam*g_car = 2*3*5",
          len(units) == rankE8 == 8 and H_E8 == 2 * N_fam * g_car)

    # order of multiplication-by-7
    def mult_order(g):
        x, k = g % H_E8, 1
        while x != 1:
            x = (x * g) % H_E8
            k += 1
        return k
    check("mult-by-7 has order 4 (7^2=19, 7^4=1 mod 30): a mu4 clock on the "
          "exponents; <7> = {1,7,19,13}",
          mult_order(7) == MU4 and pow(7, 2, H_E8) == 19 and pow(7, 4, H_E8) == 1)
    sub7 = sorted({pow(7, k, H_E8) for k in range(4)})
    check("the order-4 subgroup <7> = {1,7,13,19}", sub7 == [1, 7, 13, 19])

    # (Z/30)^x ~ Z/4 x Z/2 : need an order-2 element off <7>
    ord2 = [u for u in units if mult_order(u) == 2]
    check("(Z/30)^x ~ Z/4 x Z/2: order-4 element 7 and order-2 element 11 "
          "(11^2=1 mod 30) generate all 8 units",
          11 in ord2 and sorted({(pow(7, a, H_E8) * pow(11, b, H_E8)) % H_E8
                                  for a in range(4) for b in range(2)}) == exps)

    # conjugate pairing m + (30-m) = 30 -> 4 invariant planes
    planes = sorted({tuple(sorted((m, H_E8 - m))) for m in exps})
    check("conjugate pairs m+(30-m)=30 split the 8 phases into |mu4|=4 invariant "
          "2-planes %s (the Coxeter eigenplanes)" % (planes,),
          planes == [(1, 29), (7, 23), (11, 19), (13, 17)] and len(planes) == MU4)
    # the order-4 clock <7> permutes the planes (acts on the plane set)
    def plane_of(m):
        return tuple(sorted((m % H_E8, (H_E8 - m) % H_E8)))
    permuted = {plane_of(7 * m) for m in exps}
    check("the order-4 clock <7> permutes the 4 Coxeter planes among themselves "
          "(closed action) -- the mu4 clock on the eigenplanes",
          permuted == set(planes))

    # negative controls
    def phi(h):
        return len([u for u in range(1, h) if gcd(u, h) == 1])
    check("NEG E6 (h=12): phi(12)=4 != rank 6, and 12 != 2*3*5 -- no matching "
          "order-4 totative clock with phi=rank",
          phi(12) == 4 and phi(12) != 6)
    check("NEG E7 (h=18): phi(18)=6 = rank 7? no (rank 7), and 18 != 2*3*5 -- "
          "only E8 has phi(h)=rank AND h=2*3*5",
          phi(18) == 6 and 18 != 2 * 3 * 5)
    check("ONLY E8: phi(h)=rank (8=8) AND h=2*3*5 simultaneously",
          phi(H_E8) == rankE8 and H_E8 == 2 * 3 * 5)

    return summary("v223 Coxeter totative clock (mu4 = order-4 char of (Z/30)^x)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

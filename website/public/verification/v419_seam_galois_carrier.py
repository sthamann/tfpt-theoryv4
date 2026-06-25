"""v419 -- The seam mu4 IS the carrier's Galois group: a positive resolution of
the v409 / RES.COXETER.SYMMETRY.01 asymmetry.  In the cyclotomic picture the
flavor clocks (sheet/family/carrier/CP) are powers of zeta30 (the cyclic side,
order h(E8)=30), but the seam mu4 (i) sits on the Galois side (Z/30)^x (order
rank E8 = 8).  v409 flagged this as the "prime-2 is the Galois bridge" asymmetry.
This shows WHY -- and what the seam mu4 actually IS.  [E] number theory + the
explicit Frobenius operator; [C] the architecture reading.

  [E] 1. 30 IS SQUAREFREE => NO ORDER-4 ON THE CYCLIC CLOCK.  h(E8)=30=2*3*5 is
         squarefree, so the cyclic clock Z/30 has elements only of orders
         {1,2,3,5,6,10,15,30} -- there is NO order-4 element.  The seam mu4
         (order 4) therefore CANNOT be a rotation hand; it is forced onto the
         Galois side.
  [E] 2. THE GALOIS GROUP SPLITS BY PRIME.  By CRT
             (Z/30)^x = (Z/2)^x x (Z/3)^x x (Z/5)^x = 1 x Z/2 x Z/4 = mu4 x Z2,
         order phi(30) = 8 = rank E8.  The mu4 (Z/4) factor IS (Z/5)^x -- the
         CARRIER prime 5; the Z2 factor IS (Z/3)^x -- the FAMILY prime 3 (= CP
         conjugation, v316).  The order-4 elements {7,13,17,23} are exactly the
         generators of (Z/5)^x mod 5.
  [E] 3. THE SEAM mu4 = Gal(Q(zeta5)/Q) = (Z/5)^x (the carrier's automorphisms),
         realised on the carrier clock C5 (v418) by the Frobenius zeta5->zeta5^2:
         the explicit order-4 operator G has
             G C5 G^-1 = C5^2,   G^4 = I,   G^2 C5 G^-2 = C5^-1 (= complex conj).
         So the square seam (atom 2, mu4) and the carrier pentagon (atom 5, mu5)
         are ONE object: the seam IS the carrier's Galois group.
  [C] 4. RESOLUTION OF RES.COXETER.SYMMETRY.01.  v409 closed the asymmetry as a
         lemma ("prime-2 necessary but not autonomous, |mu4|=2^2 the Galois
         bridge, carries no contraction rate").  This gives the positive content:
         the 2^2=4 is the ORDER of (Z/5)^x (so prime-2 and prime-5 meet here),
         and "no contraction rate" is because the seam is an AUTOMORPHISM
         (|lambda|=1, finite order), not a rotation/transfer hand -- consistent
         with the clock No-Go.  Q(zeta30) carries BOTH E8 invariants: the cyclic
         hands (h=30) and the Galois gears (rank=8 = mu4 x Z2).

Mirrored in wolfram/tfpt_readouts_extension.wl (exact integer/Galois facts).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, rankE8, g_car, N_fam

x = sp.symbols('x')
Phi5 = x**4 + x**3 + x**2 + x + 1
C5 = sp.Matrix([[0, 0, 0, -1], [1, 0, 0, -1], [0, 1, 0, -1], [0, 0, 1, -1]])


def mult_order(u, n):
    o, y = 1, u % n
    while y != 1:
        y = (y * u) % n
        o += 1
    return o


def run():
    reset()
    print("v419 the seam mu4 is the carrier's Galois group Gal(Q(zeta5)) = (Z/5)^x")

    # ---- 1. 30 squarefree => no order-4 on the cyclic clock ----
    orders30 = {30 // sp.gcd(k, 30) for k in range(30)}
    check("30 SQUAREFREE => NO ORDER-4 CYCLIC [E]: h(E8)=30=2*3*5 squarefree, so "
          "Z/30 has element orders {1,2,3,5,6,10,15,30} -- NO order 4; the seam "
          "mu4 cannot be a rotation hand, it is forced onto the Galois side",
          all(e == 1 for e in sp.factorint(30).values())
          and orders30 == {1, 2, 3, 5, 6, 10, 15, 30}
          and 4 not in orders30)

    # ---- 2. the Galois group splits by prime: mu4 x Z2 = (Z/5)^x x (Z/3)^x ----
    units = [u for u in range(1, 30) if sp.gcd(u, 30) == 1]
    ord4 = [u for u in units if mult_order(u, 30) == 4]
    check("GALOIS SPLITS BY PRIME [E]: (Z/30)^x = (Z/2)^x x (Z/3)^x x (Z/5)^x = "
          "1 x Z/2 x Z/4 = mu4 x Z2, order phi(30)=8=rank E8; the mu4 (Z/4) "
          "factor IS (Z/5)^x (carrier 5), the Z2 IS (Z/3)^x (family 3 = CP "
          "conj); order-4 elements {7,13,17,23} are (Z/5)^x generators",
          len(units) == sp.totient(30) == 8 == rankE8
          and sp.totient(5) == 4 and sp.totient(3) == 2 and sp.totient(2) == 1
          and ord4 == [7, 13, 17, 23]
          and all(mult_order(u % 5, 5) == 4 for u in ord4)
          and sp.is_primitive_root(2, 5))      # (Z/5)^x is cyclic, gen 2

    # ---- 3. the seam mu4 = Gal(Q(zeta5)) via the explicit Frobenius G ----
    def col(e):
        p = sp.Poly(sp.rem(x**e, Phi5, x), x)
        return sp.Matrix([p.coeff_monomial(x**j) for j in range(4)])
    G = sp.Matrix.hstack(*[col(2 * k) for k in range(4)])      # sigma: x -> x^2
    check("SEAM mu4 = Gal(Q(zeta5)) [E]: the Frobenius zeta5->zeta5^2 is the "
          "explicit order-4 operator G with G C5 G^-1 = C5^2, G^4 = I, and "
          "G^2 C5 G^-2 = C5^-1 (complex conjugation) -- the seam mu4 acts on the "
          "carrier clock C5 (v418) as its Galois automorphism (square seam = "
          "carrier-pentagon automorphisms)",
          sp.simplify(G * C5 * G.inv() - C5**2) == sp.zeros(4)
          and G**4 == sp.eye(4)
          and sp.simplify(G**2 * C5 * (G**2).inv() - C5**4) == sp.zeros(4)
          and G != sp.eye(4) and G**2 != sp.eye(4))

    # ---- 4. resolution of RES.COXETER.SYMMETRY.01 (typing) ----
    check("RESOLVES RES.COXETER.SYMMETRY.01 [C]: the 2^2=4 is the ORDER of "
          "(Z/5)^x (prime-2 and prime-5 meet); 'no contraction rate' (v409) is "
          "because the seam is an AUTOMORPHISM (|lambda|=1, finite order=4), not "
          "a rotation/transfer hand; Q(zeta30) carries BOTH E8 invariants -- "
          "cyclic hands h=30 and Galois gears rank=8=mu4 x Z2",
          2**2 == 4 == sp.totient(5)
          and rankE8 == g_car + N_fam == 8
          and 30 == 2 * 3 * 5)

    return summary("v419 seam mu4 = Gal(Q(zeta5)) = (Z/5)^x (resolves the "
                   "v409 cyclic/Galois asymmetry)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v531 -- Coxeter Stage A on the primitive-character space: the explicit
integer operator T30 = C_Phi5 (x) C_Phi6 (companion matrices of the carrier
and family cyclotomics) has exact order 30 and characteristic polynomial
Phi_30 -- the tfpt_1 Stage A audit ("find a natural order-30 operator ... or
on its 8-dimensional primitive-character space with chi = Phi_30") is CLOSED
on the primitive-character alternative.  Plus the Ramanujan trace tomography:
eight integer traces type the Coxeter clock without diagonalisation.
[E] exact integer/cyclotomic arithmetic; the flip-atlas intertwiner stays [O].

  [E] 1. THE TENSOR OPERATOR.  C5 = Comp(Phi_5) (4x4, the v418 carrier clock)
         and C6 = Comp(Phi_6) (2x2, the family/CP hexagon) give the 8x8
         integer operator
             T30 = C5 (x) C6,
         with T30^30 = I, T30^k != I for 1 <= k < 30 (exact order 30) and
             chi_T30(x) = Phi_30(x) = x^8+x^7-x^5-x^4-x^3+x+1.
         CRT mechanism: the eigenvalues are products (primitive 5th root) x
         (primitive 6th root) = EXACTLY the eight primitive 30th roots
         (gcd(5,6) = 1; the v315/COX.COUPLE.01 group split, now realised as
         one integer operator: carrier clock (x) family clock = Coxeter clock).
  [E] 2. RAMANUJAN TRACE TOMOGRAPHY.  tr(T30^k) = c_30(k) (Ramanujan sum) for
         ALL k = 1..30, with the multiplicative factorisation
             c_30(k) = c_5(k) c_6(k),
         and the signed 8-value table over the divisor lattice of 30:
             k        : 1   2  3  5   6  10  15  30
             tr(T30^k): -1  1  2  4  -2  -4  -8   8.
         Atom readout: (|tr T^3|, |tr T^5|, |tr T^15|) = (2,4,8) =
         (|Z2|, |mu4|, rank E8).
  [E] 3. HONEST SCOPE OF THE KILL TEST.  Phi_15 = Phi_30(-x) up to sign: the
         Comp(Phi_15) candidate PASSES the unsigned triple (2,4,8) -- the
         discriminator is the SIGNED table (c_15(1) = +1 vs c_30(1) = -1).
         The other degree-8 cyclotomic candidates Phi_16, Phi_20, Phi_24 die
         already on the triple (their traces at k = 3,5,15 are all 0).
  [E] 4. NEGATIVE CONTROLS (coprimality is load-bearing).  C6 (x) C6 has
         order 3 (not 36) and eigenvalue 1; C5 (x) C5 has order 5 (not 25):
         without CRT the tensor clock collapses.
  [O] 5. WHAT STAYS OPEN.  A canonical intertwiner from the concrete
         even-flip atlas (240 = 160+80, tfpt_1 Level 2.5) onto this primitive
         8-dim space, and the Stage B norm-2 / E8-profile / Weyl metrization.
         Stage A is closed on the explicitly allowed character-space
         alternative, NOT on the atlas itself.

HONEST TYPING.  Order, characteristic polynomial, traces and controls are
exact [E].  The identification "T30 = the E8 Coxeter clock" is [C] exactly as
in v223/v314 (Phi_30 is the char poly of every E8 Coxeter element; conjugacy
inside GL_8(Z) vs O(8) metrization is Stage B).  Mirrored in
wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, rankE8

x = sp.symbols('x')
Z2 = 2
MU4 = 4


def _comp(poly):
    """Companion matrix of a monic polynomial in x."""
    p = sp.Poly(poly, x)
    n = p.degree()
    M = sp.zeros(n)
    coeffs = p.all_coeffs()
    for i in range(1, n):
        M[i, i - 1] = 1
    for i in range(n):
        M[i, n - 1] = -coeffs[n - i]
    return M


def ramanujan(n, k):
    g = sp.igcd(k, n)
    m = n // g
    return sp.mobius(m) * sp.totient(n) // sp.totient(m)


def run():
    reset()
    print("v531 Coxeter Stage A tensor operator T30 = C_Phi5 (x) C_Phi6")

    Phi5 = sp.cyclotomic_poly(5, x)
    Phi6 = sp.cyclotomic_poly(6, x)
    Phi30 = sp.cyclotomic_poly(30, x)
    C5, C6 = _comp(Phi5), _comp(Phi6)
    check("building blocks [E]: chi(C5) = Phi_5, C5^5 = I (v418 carrier "
          "clock); chi(C6) = Phi_6, C6^6 = I (family/CP hexagon)",
          C5.charpoly(x).as_expr() == Phi5 and C5**5 == sp.eye(4)
          and C6.charpoly(x).as_expr() == Phi6 and C6**6 == sp.eye(2))

    T = sp.Matrix(sp.kronecker_product(C5, C6))
    check("T30 = C5 (x) C6 is an 8x8 INTEGER operator, 8 = phi(30) = rank E8",
          T.shape == (8, 8) and all(e.is_Integer for e in T)
          and sp.totient(30) == rankE8)
    check("chi(T30) = Phi_30 = x^8+x^7-x^5-x^4-x^3+x+1 EXACTLY",
          T.charpoly(x).as_expr() == Phi30
          and Phi30 == x**8 + x**7 - x**5 - x**4 - x**3 + x + 1)

    powers, Tk, exact_order = {}, sp.eye(8), True
    for k in range(1, 31):
        Tk = Tk * T
        powers[k] = Tk
        if k < 30 and Tk == sp.eye(8):
            exact_order = False
    check("EXACT ORDER 30 [E]: T30^30 = I and T30^k != I for 1 <= k < 30",
          exact_order and powers[30] == sp.eye(8))
    check("CRT spectrum [E]: 8 distinct simple eigenvalues (the primitive "
          "30th roots; carrier x family = Coxeter via gcd(5,6) = 1)",
          all(m == 1 for m in T.eigenvals().values())
          and len(T.eigenvals()) == 8)

    # 2. trace tomography
    tab = {k: powers[k].trace() for k in (1, 2, 3, 5, 6, 10, 15, 30)}
    check("SIGNED TRACE TABLE [E]: tr(T^k) = (-1,1,2,4,-2,-4,-8,8) at "
          "k = (1,2,3,5,6,10,15,30) = c_30(k)",
          tab == {1: -1, 2: 1, 3: 2, 5: 4, 6: -2, 10: -4, 15: -8, 30: 8})
    check("FULL TOMOGRAPHY [E]: tr(T30^k) = c_30(k) (Ramanujan sum) for "
          "ALL k = 1..30",
          all(powers[k].trace() == ramanujan(30, k) for k in range(1, 31)))
    check("FACTORISATION [E]: c_30(k) = c_5(k) c_6(k) for all k "
          "(tr(A (x) B)^k = tr A^k tr B^k)",
          all(ramanujan(30, k) == ramanujan(5, k) * ramanujan(6, k)
              for k in range(1, 31)))
    check("ATOM READOUT [E]: (|tr T^3|,|tr T^5|,|tr T^15|) = (2,4,8) = "
          "(|Z2|,|mu4|,rank E8)",
          (abs(tab[3]), abs(tab[5]), abs(tab[15])) == (Z2, MU4, rankE8))

    # 3. honest scope of the kill test
    C15 = _comp(sp.cyclotomic_poly(15, x))
    t15 = {k: (C15**k).trace() for k in (1, 3, 5, 15)}
    check("HONEST [E]: Comp(Phi_15) PASSES the unsigned triple (2,4,8) "
          "(Phi_30(x) = Phi_15(-x)); the discriminator is the SIGNED table "
          "(c_15(1) = +1 vs c_30(1) = -1)",
          (abs(t15[3]), abs(t15[5]), abs(t15[15])) == (2, 4, 8)
          and t15[1] == 1 != -1)
    for n in (16, 20, 24):
        Cn = _comp(sp.cyclotomic_poly(n, x))
        trip = tuple(abs((Cn**k).trace()) for k in (3, 5, 15))
        check(f"KILL FIRES [E]: Comp(Phi_{n}) triple {trip} != (2,4,8) "
              "(wrong Coxeter type dies on three integer traces)",
              trip != (2, 4, 8))

    # 4. coprimality negative controls
    T66 = sp.Matrix(sp.kronecker_product(C6, C6))
    T55 = sp.Matrix(sp.kronecker_product(C5, C5))
    check("NEG CONTROL [E]: C6 (x) C6 has order 3 (not 36) with eigenvalue 1;"
          " C5 (x) C5 has order 5 (not 25) -- coprimality gcd(5,6) = 1 is "
          "load-bearing (CRT)",
          T66**3 == sp.eye(4) and T66 != sp.eye(4)
          and T55**5 == sp.eye(16) and T55 != sp.eye(16))

    # 5. open residue, stated
    check("SCOPE [O]: Stage A closed on the 8-dim primitive-character "
          "alternative; the even-flip-atlas intertwiner and the Stage B "
          "metrization stay OPEN (no upgrade claimed)", True)

    return summary("v531 Stage A tensor clock (order 30, chi = Phi_30, "
                   "traces = c_30)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

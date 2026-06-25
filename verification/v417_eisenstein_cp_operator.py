"""v417 -- The Eisenstein/CP operator: the hexagonal dual of the Gaussian seam
operator v415.  Where v415 put the SQUARE seam (tau=i, mu4) on operators via
J=[U,V]/3, this puts the HEX/flavor side (tau=omega, mu3/mu6) on operators via
the family rotation P=( 1 2 3 ) and the CP clock W=-P^2, and unifies both with
the seam into one order-30 Coxeter clock Q(zeta30).  [E] algebra, [C] readings.

  [E] 1. THE FAMILY ROTATION IS THE ORDER-3 EISENSTEIN DECK.  P=(1 2 3) has
         P^3=I, chi_P=x^3-1, and P^2+P+I = ONES (the all-ones matrix), so on the
         2-plane orthogonal to (1,1,1) it satisfies the Eisenstein relation
         omega^2+omega+1=0 -- the order-3 dual of J^2=-I (v415).
  [E] 2. THE HEX NORM 7 AS AN OPERATOR (dual of v415's square 13).
             (3I+2P)(3I+2P^2) = 7 I + 6 ONES,   Spec = {7, 7, 25}:
         7 = N_Z[omega](3+2omega) = scalaron on the omega-plane (the Eisenstein
         CM norm, v222/v230), 25 = g_car^2 on the (1,1,1) line (because the
         "real" slot reads (3+2)^2 = g_car^2).  Compare v415 square
         (3I+2J)(3I-2J) -> {13,13,9}.  Negative control (v222 rigidity):
         (5I+4P)(5I+4P^2) -> {21,21,81}, so N_omega(5,4)=21 != 41.
  [E] 3. THE CP CLOCK W = -P^2 (= omega^2 * (-1) = rho of v233), order 6.
             W^3 = -I,  W^2 = P,  chi_W = x^3+1,  Spec(W) = {-1, zeta6, zeta6^-1}.
         Both CP phases are arguments of powers of this ONE operator:
             delta_CKM,lead = arg(zeta6)   = pi/3   (eigenvalue of W),
             delta_PMNS     = arg(zeta6^4) = 4pi/3  (eigenvalue of W^4 = P^2),
         and W^3=-I IS the Z2 sheet flip rho^3=-1 (v231/v233/v316/v320).  So
         mu6 = mu3 x mu2 in one operator (W^2=family, W^3=sheet).
  [E] 4. ONE ORDER-30 CLOCK.  All flavor-side clocks are powers of the E8
         Coxeter unit zeta30 = e^{2pi i/30} (h(E8)=30=2*3*5=|Z2|*N_fam*g_car):
             zeta30^15 = -1   (sheet, mu2),    zeta30^10 = omega (family, mu3),
             zeta30^6  = zeta5 (carrier, mu5), zeta30^5  = zeta6 (CP, mu6).
         The SEAM mu4 (i) is NOT a power of zeta30 (4 does not divide 30): it is
         the GALOIS side, Gal(Q(zeta30)/Q)=(Z/30)^x of order phi(30)=8=rank E8
         = mu4 x Z2 (the totatives {7,13,17,23} have multiplicative order 4).  So
         Q(zeta30) carries BOTH E8 invariants: the cyclic h=30 (flavor hands) and
         the Galois rank=8 (the seam).
  [C] 5. OPERATOR REALISATIONS + the honest carrier gap.  J=[U,V]/3 (mu4, v415),
         P (mu3), W=-P^2 (mu6) and -I/sigma (mu2) are explicit 3x3 operators; the
         CARRIER mu5 (zeta5) has NO clean 3x3 operator (it needs dim>=4; the
         golden phi=2cos(pi/5) shows up only as an OUTPUT-side trace, v313/v349).
         Honest negatives: no U,V-diamond operator carries x^2-x+1 (zeta6) -- only
         -P does; the seam and family clocks do NOT combine ([D,P] != 0, no mu12);
         and N(3+2 zeta6)=19 != 7 (the clean 7 is the omega-norm, not the zeta6-norm).

Mirrored in wolfram/tfpt_readouts_extension.wl (exact identities only); the CP
phase values delta_CKM/delta_PMNS are the v316/v320 frozen readouts.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

I3 = sp.eye(3)
ONES = sp.ones(3, 3)
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
U = Q * sp.diag(1, 0, 0)
V = Q * sp.diag(0, 1, 1)
J = (U * V - V * U) / 3
D = sp.simplify(-I3 + J - J * J)                       # the v415 seam deck (order 4)
P = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])       # family rotation (1 2 3)
W = -P**2                                              # the CP clock (order 6)
sigma = sp.diag(1, -1, -1)

omega = sp.exp(2 * sp.I * sp.pi / 3)
zeta6 = sp.exp(sp.I * sp.pi / 3)
z30 = sp.exp(2 * sp.I * sp.pi / 30)
SCALARON = 7


def N_eisen(a, b):
    return a * a - a * b + b * b


def run():
    reset()
    print("v417 Eisenstein/CP operator: family rotation -> norm 7, W=-P^2 -> CP "
          "phases, one order-30 clock")

    x = sp.symbols('x')

    # ---- 1. the family rotation is the order-3 Eisenstein deck ----
    check("EISENSTEIN DECK [E]: P=(1 2 3) has P^3=I, chi_P=x^3-1, and "
          "P^2+P+I=ONES (so on the plane perp to (1,1,1): omega^2+omega+1=0) "
          "-- the order-3 dual of J^2=-I (v415)",
          P**3 == I3 and P.charpoly(x).as_expr() == x**3 - 1
          and (P**2 + P + I3) == ONES
          and sp.simplify((P - omega * I3).det()) == 0)

    # ---- 2. the hex norm 7 as an operator (dual of square 13) ----
    Nhex = sp.simplify((3 * I3 + 2 * P) * (3 * I3 + 2 * P**2))
    N54 = sp.simplify((5 * I3 + 4 * P) * (5 * I3 + 4 * P**2))
    check("HEX NORM 7 AS OPERATOR [E]: (3I+2P)(3I+2P^2)=7I+6 ONES, Spec={7,7,25} "
          "-- 7=N_omega(3+2omega)=scalaron on the omega-plane, 25=g_car^2 on "
          "(1,1,1) (the dual of v415's (3I+2J)(3I-2J)->{13,13,9}); NEG control "
          "(5I+4P)(5I+4P^2)->{21,21,81}, N_omega(5,4)=21!=41 (v222 rigidity)",
          Nhex == 7 * I3 + 6 * ONES
          and Nhex.eigenvals() == {SCALARON: 2, g_car**2: 1}
          and N_eisen(3, 2) == SCALARON == 7
          and N54.eigenvals() == {21: 2, N_fam**4: 1}
          and N_eisen(5, 4) == 21 != 41)

    # ---- 3. the CP clock W = -P^2 ----
    dckm = sp.arg(zeta6)
    dpmns = sp.Rational(4, 3) * sp.pi
    check("CP CLOCK [E]: W=-P^2 (=omega^2*(-1)=rho, v233) has W^3=-I, W^2=P, "
          "chi_W=x^3+1, Spec={-1,zeta6,zeta6^-1}; delta_CKM,lead=arg(zeta6)=pi/3 "
          "(eigenvalue of W), delta_PMNS=arg(zeta6^4)=4pi/3 (eigenvalue of "
          "W^4=P^2); W^3=-I is the Z2 sheet flip rho^3=-1 (v231/v233/v316/v320)",
          W**3 == -I3 and W**2 == P and W.charpoly(x).as_expr() == x**3 + 1
          and sp.simplify((W - zeta6 * I3).det()) == 0
          and dckm == sp.pi / 3
          and sp.simplify((W**4 - sp.exp(sp.I * dpmns) * I3).det()) == 0
          and W**4 == P**2)

    # ---- 4. one order-30 Coxeter clock ----
    check("ORDER-30 CLOCK [E]: all flavor-side clocks are powers of "
          "zeta30=e^{2pi i/30} (h(E8)=30=|Z2|*N_fam*g_car): zeta30^15=-1 (mu2), "
          "zeta30^10=omega (mu3), zeta30^6=zeta5 (mu5), zeta30^5=zeta6 (mu6); "
          "the SEAM mu4 (i) is NOT a power (4 does not divide 30) -- it is the "
          "Galois side (Z/30)^x, order phi(30)=8=rank E8=mu4 x Z2",
          sp.simplify(z30**15 + 1) == 0
          and sp.simplify(z30**10 - omega) == 0
          and sp.simplify(z30**6 - sp.exp(2 * sp.I * sp.pi / 5)) == 0
          and sp.simplify(z30**5 - zeta6) == 0
          and 30 % 4 != 0
          and sp.totient(30) == 8 == rankE8
          and sorted(u for u in range(1, 30) if sp.gcd(u, 30) == 1)
          == [1, 7, 11, 13, 17, 19, 23, 29])

    # ---- 5. operator realisations + honest negatives ----
    diamond = {'J': J, 'D': D, 'V': V, 'U': U, '[U,V]': U * V - V * U, 'C': Q}
    no_zeta6 = all(sp.rem(M.charpoly(x).as_expr(), x**2 - x + 1, x) != 0
                   for M in diamond.values())
    has_zeta6 = sp.rem((-P).charpoly(x).as_expr(), x**2 - x + 1, x) == 0
    Nz6 = sp.nsimplify(sp.expand_complex((3 + 2 * zeta6) * (3 + 2 / zeta6)))
    check("REALISATIONS + HONEST NEGATIVES [E]/[C]: J(mu4)/P(mu3)/W=-P^2(mu6)/"
          "sigma(mu2) are 3x3 operators, but the CARRIER mu5 has none (needs "
          "dim>=4; golden phi only as an output trace, v313/v349); no U,V-diamond "
          "operator carries x^2-x+1 (only -P does); [D,P]!=0 (no mu12); "
          "N(3+2 zeta6)=19!=7 (the clean 7 is the omega-norm)",
          no_zeta6 and has_zeta6
          and sp.simplify(D * P - P * D) != sp.zeros(3)
          and Nz6 == 19 != SCALARON
          and sigma**2 == I3)

    return summary("v417 Eisenstein/CP operator (P->7, W=-P^2->CP phases, one "
                   "order-30 clock)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

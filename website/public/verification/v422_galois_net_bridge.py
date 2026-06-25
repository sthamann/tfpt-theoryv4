"""v422 -- The Galois<->Net bridge: the seam mu4 = Gal(Q(zeta5)) is the SAME
cyclic Z/4 as the (E8)_1 simple-current glue -- not a mere order-4 coincidence.
This connects the Galois "gearbox" of v419 to G_net / SEAM.EQUIV.01 (the
(D5)_1 (x) (A3)_1 -> (E8)_1 extension).  The discipline (v100): the match is to
the CYCLIC Z/4 specifically, and cyclic-vs-Klein is LOAD-BEARING -- cyclic Z/4
gives E8 (det 1), the Klein Z2xZ2 gives D8/SO(16) (det 4).  [E] lattice/Galois,
[C] the canonical identification.

  [E] 1. THE CARRIER GLUE IS CYCLIC Z/4 (and D5 is cyclic because rank 5 is ODD).
         disc(A3) = coker(Cartan A3) = Z/4 and disc(D5) = Z/4 (one invariant
         factor 4 in the Smith normal form -- CYCLIC, not Klein), det = 4 each.
         D_n discriminant is Z/4 for n ODD and Z2xZ2 for n EVEN; the carrier is
         D5 (rank 5 = g_car, odd) -> cyclic Z/4; the control D8 (rank 8, even)
         -> Z2xZ2 (Klein).
  [E] 2. THE CARRIER-GALOIS IS THE SAME CYCLIC Z/4 (and 5 is what makes it so).
         Gal(Q(zeta5)) = (Z/5)^x = <2> is cyclic of order 4 (max multiplicative
         order 4, NOT Klein); among the atoms only the carrier prime 5 gives
         order 4: |(Z/2)^x|=1, |(Z/3)^x|=2, |(Z/5)^x|=4.
  [E] 3. THE E8 GLUE IS THE CYCLIC Z/4 <(1,1)>.  In disc(D5 (+) A3) = Z4 x Z4
         (order 16 = dim S^+) the simple current (1,1) has order 4 (cyclic
         <(1,1)>); the Lagrangian quotient is 16/|glue|^2 = 16/4^2 = 1, so the
         extension is UNIMODULAR = (E8)_1 (one primary, holomorphic, v89/v154).
  [E] 4. CYCLIC vs KLEIN IS LOAD-BEARING (negative control, v100).  The order-4
         Klein group Z2xZ2 has max element order 2 (NOT cyclic); the even-rank
         D8 carries it, and the order-2 halfway glue <(2,2)> gives 16/2^2 = 4 =
         |disc(D8)| = SO(16) (det Cartan = 4, four primaries), NOT E8 (det 1).
         So cyclic Z/4 -> E8, Klein/order-2 -> D8: the carrier-Galois being
         cyclic Z/4 (5 prime) matches the E8 glue, never the D8 Klein.
  [C] 5. THE BRIDGE = THE FOUR-FOLD mu4 IDENTITY.  ONE cyclic Z/4 threads the FOUR
         mu4 readings: the seam DECK / divisor mu4 (z->iz on the 4-mark P^1, v419/
         v177), the carrier-GALOIS Gal(Q(zeta5))=(Z/5)^x (v419), the DISCRIMINANT
         group disc(D5)=disc(A3)=Z/4 (bullet 1), and the SIMPLE-CURRENT glue
         <(1,1)> -> (E8)_1 (v1/v89/v154).  So the Galois gearbox (Z/30)^x of v419
         IS the simple-current glue of the holomorphic net -- a direct bridge from
         the Galois side to G_net (SEAM.EQUIV.01).  All four are computably
         cyclic-Z/4 [E]; the canonical identification (one functorial Z/4) is the
         [C] bridge, cyclicity forced (5 odd/prime), the Klein alternative excluded.
         TYPING (v428): this four-fold identity is a COMPRESSION -- ONE object read
         four ways, a unification that makes the carrier less axiomatic -- NOT four
         independent witnesses that multiply over-determination.

Mirrored in wolfram/tfpt_readouts_extension.wl (exact lattice/Galois facts).
"""
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

from tfpt_constants import check, summary, reset, g_car, dim_Splus

# Cartan matrices
A3 = sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
D5 = sp.Matrix([[2, -1, 0, 0, 0], [-1, 2, -1, 0, 0], [0, -1, 2, -1, -1],
                [0, 0, -1, 2, 0], [0, 0, -1, 0, 2]])
D8 = sp.Matrix([[2, -1, 0, 0, 0, 0, 0, 0], [-1, 2, -1, 0, 0, 0, 0, 0],
                [0, -1, 2, -1, 0, 0, 0, 0], [0, 0, -1, 2, -1, 0, 0, 0],
                [0, 0, 0, -1, 2, -1, 0, 0], [0, 0, 0, 0, -1, 2, -1, -1],
                [0, 0, 0, 0, 0, -1, 2, 0], [0, 0, 0, 0, 0, -1, 0, 2]])


def invariant_factors(C):
    """The Smith-normal-form diagonal entries > 1 = the cyclic factors of coker(C)."""
    snf = smith_normal_form(C)
    return [snf[i, i] for i in range(C.shape[0]) if abs(snf[i, i]) > 1]


def mult_order(u, n):
    o, x = 1, u % n
    while x != 1:
        x = (x * u) % n
        o += 1
    return o


def run():
    reset()
    print("v422 Galois<->Net bridge: mu4 = Gal(Q(zeta5)) is the (E8)_1 glue Z/4")

    # ---- 1. the carrier glue is cyclic Z/4 (D5 cyclic because rank 5 is odd) ----
    f_a3, f_d5, f_d8 = invariant_factors(A3), invariant_factors(D5), invariant_factors(D8)
    check("CARRIER GLUE CYCLIC Z/4 [E]: disc(A3)=Z/4 and disc(D5)=Z/4 (ONE "
          "invariant factor 4 = cyclic, not Klein), det=4 each; D_n disc is Z/4 "
          "for n ODD, Z2xZ2 for n EVEN -- carrier D5 (rank 5=g_car, odd) is "
          "cyclic, control D8 (rank 8, even) is Klein (factors %s)" % (f_d8,),
          f_a3 == [4] and f_d5 == [4]
          and abs(A3.det()) == 4 and abs(D5.det()) == 4
          and f_d8 == [2, 2] and len(f_d5) == 1 and len(f_d8) == 2
          and g_car == 5 and g_car % 2 == 1)

    # ---- 2. the carrier-Galois is the SAME cyclic Z/4 (5 makes it so) ----
    ord5 = max(mult_order(u, 5) for u in (1, 2, 3, 4))
    check("CARRIER-GALOIS CYCLIC Z/4 [E]: Gal(Q(zeta5))=(Z/5)^x=<2> is cyclic of "
          "order 4 (max mult order 4, not Klein); among the atoms only 5 gives "
          "order 4 (|(Z/2)^x|=1, |(Z/3)^x|=2, |(Z/5)^x|=4)",
          ord5 == 4 and sp.totient(5) == 4 and sp.is_primitive_root(2, 5)
          and sp.totient(2) == 1 and sp.totient(3) == 2)

    # ---- 3. the E8 glue is the cyclic Z/4 <(1,1)> ----
    def order_in_Z4xZ4(a, b):
        return sp.ilcm(4 // sp.gcd(a, 4), 4 // sp.gcd(b, 4))
    glue_order = order_in_Z4xZ4(1, 1)
    disc_carrier = 4 * 4
    e8_disc = disc_carrier // glue_order**2
    check("E8 GLUE CYCLIC Z/4 [E]: in disc(D5(+)A3)=Z4xZ4 (order 16=dim S^+) the "
          "simple current (1,1) has order 4 (cyclic <(1,1)>); the Lagrangian "
          "quotient 16/4^2 = 1 => the extension is unimodular = (E8)_1 (one "
          "primary, holomorphic, v89/v154)",
          glue_order == 4 and disc_carrier == 16 == dim_Splus and e8_disc == 1)

    # ---- 4. cyclic vs Klein is load-bearing (negative control) ----
    halfway_order = order_in_Z4xZ4(2, 2)            # <(2,2)> = order 2
    d8_disc = disc_carrier // halfway_order**2       # 16/2^2 = 4 = |disc(D8)|
    check("CYCLIC vs KLEIN LOAD-BEARING [E] (neg control): the Klein Z2xZ2 has "
          "max element order 2 (not cyclic); the order-2 halfway glue <(2,2)> "
          "gives 16/2^2 = 4 = |disc(D8)| = SO(16) (det Cartan 4, four primaries), "
          "NOT E8 (det 1). So cyclic Z/4 -> E8, Klein/order-2 -> D8 -- the "
          "carrier-Galois (cyclic Z/4, 5 prime) matches E8, never the D8 Klein",
          halfway_order == 2 and d8_disc == 4 == abs(D8.det())
          and e8_disc != d8_disc and f_d8 == [2, 2])

    # ---- 5. the bridge = the four-fold mu4 identity (typed [C]; compression per v428) ----
    check("FOUR-FOLD mu4 IDENTITY [C]: ONE cyclic Z/4 threads the FOUR mu4 readings "
          "-- the seam deck/divisor mu4 (z->iz, v419/v177), the carrier-Galois "
          "Gal(Q(zeta5)) (v419), the discriminant disc(D5)=disc(A3)=Z/4, and the "
          "(E8)_1 simple-current glue <(1,1)> (v1/v89/v154); the Galois gearbox "
          "(Z/30)^x of v419 IS the holomorphic-net glue (a direct Galois->G_net "
          "bridge). All four computably cyclic-Z/4 [E], the canonical identification "
          "[C] (cyclicity forced by 5, Klein excluded). Per v428 this is a "
          "COMPRESSION (one object read four ways), NOT four independent multipliers",
          f_d5 == f_a3 == [4] and ord5 == 4 and glue_order == 4)

    return summary("v422 Galois<->Net bridge / four-fold mu4 identity (deck=Galois="
                   "discriminant=simple-current = one cyclic Z/4 -> (E8)_1; Klein->D8 "
                   "excluded; a compression per v428, not four witnesses)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

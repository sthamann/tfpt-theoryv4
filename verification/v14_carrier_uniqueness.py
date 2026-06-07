"""v14 -- A2: the carrier rank g=5 and the 3+2 split are FORCED, not assumed.

Two clean uniqueness statements (Tier-A item A2):

  (1) g_car = 5 is the UNIQUE positive integer with
        dim S+ = 2^(g-1),  N_fam = (2^(g-1)-1)/g in Z+,  rank E8 = g + N_fam = 8.
      Equivalently the single equation  g + (2^(g-1)-1)/g = 8  has the unique
      admissible solution g=5.

  (2) the split (b,s)=(3,2) is the UNIQUE solution of
        b + s = g = 5,   b^2 + s^2 = 13 = |R(A3)| + 1   (b > s >= 1),
      and it reproduces dim g_SM = (b^2-1)+(s^2-1)+1 = 12 = |R(A3)|.

  (3) the resulting hypercharge assignment is anomaly-free over one generation:
        Tr Y = 0  and  Tr Y^3 = 0.

This hardens P2 from "axiom" to "forced given the E8 closure + SM gauge algebra".
The seam->carrier *interface* itself remains a declared input (honest).
"""
import sympy as sp
from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v14  carrier uniqueness (A2): g=5 and 3+2 are forced")

    # (1) g=5 unique with N_fam integer AND rank E8 = g + N_fam = 8
    sols = []
    for g in range(1, 40):
        num = 2**(g - 1) - 1
        if num % g == 0:
            nf = num // g
            if g + nf == 8:
                sols.append(g)
    check("g=5 is the UNIQUE rank with N_fam in Z+ and g+N_fam=8", sols == [5])
    # also list the integer-N_fam carriers to show 5 is selected by rank 8
    intg = [g for g in range(2, 12) if (2**(g - 1) - 1) % g == 0]
    check("integer-N_fam carriers are {3,5,7,...}; only g=5 has rank 8",
          3 in intg and 5 in intg and 7 in intg and (5 in sols) and (3 not in sols) and (7 not in sols))

    # (2) (b,s)=(3,2) unique: b+s=5, b^2+s^2=13, b>s>=1
    bs = [(b, 5 - b) for b in range(1, 5) if b > (5 - b) >= 1
          and b**2 + (5 - b)**2 == 13]
    check("(b,s)=(3,2) is the UNIQUE split with b+s=5, b^2+s^2=13", bs == [(3, 2)])
    b, s = 3, 2
    check("b^2+s^2 = 13 = |R(A3)|+1 (the Q-discriminant)", b**2 + s**2, 13, exact=True)
    check("dim g_SM = (b^2-1)+(s^2-1)+1 = 12 = |R(A3)|",
          (b**2 - 1) + (s**2 - 1) + 1, 12, exact=True)

    # (3) anomaly freedom of the induced hypercharge over one generation (16 states)
    #   Q_L: mult 6 (3 colour x 2 weak), Y=1/6 ; u^c: 3, -2/3 ; d^c: 3, 1/3 ;
    #   L_L: 2, -1/2 ; e^c: 1, 1 ; nu^c: 1, 0
    gen = [(6, sp.Rational(1, 6)), (3, sp.Rational(-2, 3)), (3, sp.Rational(1, 3)),
           (2, sp.Rational(-1, 2)), (1, sp.Integer(1)), (1, sp.Integer(0))]
    trY = sum(m * Y for m, Y in gen)
    trY3 = sum(m * Y**3 for m, Y in gen)
    check("total multiplicity = 16 = dim S+", sum(m for m, _ in gen), 16, exact=True)
    check("Tr Y = 0 (mixed/gravitational anomaly-free)", trY == 0)
    check("Tr Y^3 = 0 (cubic hypercharge anomaly-free)", trY3 == 0)
    return summary("v14 carrier uniqueness")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

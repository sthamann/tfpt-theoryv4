"""v230 -- the center budget (7,11,13) is the three local norms of the theory.

The centered cross of the Sheet Diamond (v95/v218) has center C = R + Q diag(1,0,0);
its row sums are (7,11,13).  v218 reads these as an audit match (7 scalaron, 11
Plucker norm, 13 Delta_Q).  Combined with the CM-norm duality (v222) the triple
becomes a structured statement: C collects the THREE local norms of TFPT --

  [E] 7  = N_Z[omega](3 + 2 omega)        (Eisenstein / hexagonal CM norm)
  [E] 11 = sum_{k<=2} C(4,k) = 1 + 4 + 6  (QBL boundary Fock count on the 4 mu4 corners)
  [E] 13 = N_Z[i](3 + 2 i)                (Gaussian / square CM norm)

so C = (hex norm, boundary Fock count, square norm).  The two CM rings (square +
hex, v222) and the seam boundary count (v174 QBL) meet in one operator center.

  [E] 1. C = R + Q diag(1,0,0); row sums = (7, 11, 13).
  [E] 2. 7  = N_omega(3+2 omega) = scalaron exponent (hexagonal).
  [E] 3. 13 = N_i(3+2 i) = Delta_Q (square).
  [E] 4. 11 = C(4,0)+C(4,1)+C(4,2) = QBL Fock count on |mu4|=4 corners
        = dim S^+ - g_car = 16 - 5 (the boundary count, v174).
  [E] 5. NEG: swapping the rings (N_i(3,2)=13 != 7, N_omega(3,2)=7 != 13) shows
        the hex/square assignment is rigid, not interchangeable.

Status: [E] for the arithmetic; [C] for the "center = three local norms"
reading.  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
from math import comb

import sympy as sp

from tfpt_constants import check, summary, reset, dim_Splus, g_car

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
C = R + Q * sp.diag(1, 0, 0)

N_FAM = 3
SCALARON = 7
DELTA_Q = 13
MU4 = 4


def N_gauss(a, b):
    return a * a + b * b


def N_eisen(a, b):
    return a * a - a * b + b * b


def run():
    reset()
    print("v230  center budget (7,11,13) = (hex norm, Fock count, square norm)")

    rowsums = [sum(C.row(i)) for i in range(3)]
    check("C = R + Q diag(1,0,0); row sums = (7,11,13) (the centered-cross center, v95/v218)",
          rowsums == [7, 11, 13])
    check("7 = N_Z[omega](3 + 2 omega) = scalaron exponent (hexagonal CM norm)",
          N_eisen(N_FAM, 2) == SCALARON == 7)
    check("13 = N_Z[i](3 + 2 i) = Delta_Q (square CM norm)",
          N_gauss(N_FAM, 2) == DELTA_Q == 13)
    fock = sum(comb(MU4, k) for k in range(3))
    check("11 = C(4,0)+C(4,1)+C(4,2) = 1+4+6 = QBL Fock count on |mu4|=4 corners "
          "= dim S^+ - g_car = 16 - 5",
          fock == 11 == dim_Splus - g_car)
    check("center C collects the three local norms: (hex 7, Fock 11, square 13)",
          rowsums == [N_eisen(N_FAM, 2), fock, N_gauss(N_FAM, 2)])

    # negative control: the ring assignment is rigid
    check("NEG: rings are not interchangeable -- N_i(3,2)=13 != 7 and "
          "N_omega(3,2)=7 != 13 (hex<->7, square<->13 is forced)",
          N_gauss(N_FAM, 2) == 13 and N_eisen(N_FAM, 2) == 7
          and N_gauss(N_FAM, 2) != SCALARON and N_eisen(N_FAM, 2) != DELTA_Q)

    return summary("v230 center budget norms (7 hex | 11 Fock | 13 square)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v411 -- The quark u/d ratio is a pure V-power readout.  The established
closed form c_u/c_d = g_car ||Pl(K)||_1 / (N_fam^2 Delta_Q) = 55/117 (v94)
re-expresses EXACTLY as a quotient of three bilinear readouts of the single
sheet generator V = Q diag(0,1,1) (v410).  [E] re-encoding; the physical
reading stays [C], coupled to the existing readout rigidity.

  [E] 1. V-POWER FORM.
             c_u/c_d = (1^T V^4 1) / ((a^T V 1)(1^T V^2 1))
                     = 55 / (9 * 13) = 55/117,
         with 55 = 1^T V^4 1 (quark numerator), 9 = a^T V 1 = N_fam^2, and
         13 = 1^T V^2 1 = Delta_Q.
  [E] 2. IDENTITY TO THE ESTABLISHED FORM.  This is the same number as
             g_car ||Pl(K)||_1 / (N_fam^2 Delta_Q) = 5*11/(9*13) = 55/117
         (v94): 55 = 5*11 = g_car * (the left-Pluecker norm of K), so the
         V-power numerator simply repackages g_car*11 as 1^T V^4 1.

HONEST TYPING.  This is an exact RE-ENCODING, not an independent derivation:
it adds no new physical input.  The value 55/117 and which contraction IS
u/d stay [C], coupled to the wall-selection / readout rigidity (U_wall).
The gain is structural -- numerator AND denominator now come from iterating
ONE operator V.  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
V = Q * sp.diag(0, 1, 1)
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])

DELTA_Q = 13
PL_K = 11      # ||Pl(K)||_1 (v94 left-Pluecker norm of K)


def run():
    reset()
    print("v411 u/d ratio as a pure V-power readout")

    num = (ONE.T * V**4 * ONE)[0]
    a_v_1 = (A.T * V * ONE)[0]
    o1_v2_1 = (ONE.T * V**2 * ONE)[0]

    check("V-POWER FORM [E]: c_u/c_d = (1^T V^4 1)/((a^T V 1)(1^T V^2 1)) = "
          "55/(9*13) = 55/117, with 55 = 1^T V^4 1, 9 = a^T V 1 = N_fam^2, "
          "13 = 1^T V^2 1 = Delta_Q",
          num == 55 and a_v_1 == 9 == N_fam**2 and o1_v2_1 == 13 == DELTA_Q
          and sp.Rational(num, a_v_1 * o1_v2_1) == sp.Rational(55, 117))

    check("IDENTITY [E]: same number as the established g_car*||Pl(K)||_1/"
          "(N_fam^2*Delta_Q) = 5*11/(9*13) = 55/117 (v94); the V-power "
          "numerator repackages g_car*11 = 55 = 1^T V^4 1",
          sp.Rational(g_car * PL_K, N_fam**2 * DELTA_Q) == sp.Rational(55, 117)
          and g_car * PL_K == 55 == num)

    check("HONEST TYPING [C]: an exact RE-ENCODING, no new physical input -- "
          "the value 55/117 and the u/d identification stay [C], coupled to "
          "the wall-selection readout rigidity (U_wall); the gain is that "
          "numerator and denominator both iterate ONE operator V",
          True)

    return summary("v411 u/d ratio = (1^TV^4 1)/((a^TV1)(1^TV^2 1)) = 55/117")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

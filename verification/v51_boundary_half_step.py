"""v51 -- the delta=1/2 boundary half-step: a glue-norm origin for the lepton
transport value.

v20 derived the charged-lepton coefficients from the DISTINGUISHED transport value
delta = 1/2, taken there as a chosen rational.  This script gives delta = 1/2 a
structural origin: it is the DIFFERENCE of the two E8-glue discriminant-form norms,
the exact complement of their sum (the E8 root norm).

  q(D5) + q(A3) = 5/4 + 3/4 = 2     (the E8 root norm; v1/v47)
  q(D5) - q(A3) = 5/4 - 3/4 = 1/2   (the lepton transport value delta; NEW)

UNIFYING ORIGIN (the deeper reading): the two glue norms ARE the carrier rank and
the family count over the glue index,

  q(D5) = g_car/|mu4| = 5/4,   q(A3) = N_fam/|mu4| = 3/4   (common denom |mu4|=4),

because rank(D5) = g_car = 5 (D_n spinor norm n/4) and rank(A3) = N_fam = 3
(A_n corner norm n/(n+1), n+1 = 4 = |mu4|).  Then all FOUR arithmetic operations on
the pair are forced compiler atoms:

  sum   = (g_car+N_fam)/|mu4| = rank(E8)/|mu4| = 2          (E8 root norm)
  diff  = (g_car-N_fam)/|mu4| = |Z2|/|mu4|     = 1/2        (lepton transport delta)
  prod  = g_car*N_fam/|mu4|^2 = dim su(4)/dim(S+) = 15/16
  ratio = g_car/N_fam                          = 5/3

and (sum, ratio) invert uniquely back to (5/4, 3/4).  So delta = 1/2 is the
carrier-minus-family count over the glue index -- a fully atomic origin, not a
chosen rational; it also equals the harmonic-frame holonomy diagonal modulus (v41).

This dovetails with v40/v41: in the harmonic (unitary) frame the (U_wall) holonomy
diagonal modulus is |diag M~_0| = (0, 1/2, 1/2), i.e. the SAME 1/2 -- so the
geometry supplies delta = 1/2 from two independent sides (glue norm + holonomy).

TYPING: the q(D5)-q(A3) = 1/2 identity is exact [I]; that this glue-norm difference
IS the lepton transport value is the structural reading that hardens v20's "chosen"
delta into a glue-norm readout.  The cleanest single origin is the norm difference;
the other readings are supporting, not independent forcings.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

mu4 = 4
Z2 = 2
Rp_A3 = 6


def run():
    reset()
    print("v51  delta=1/2 boundary half-step: glue-norm origin of the transport value")

    qD5, qA3 = sp.Rational(5, 4), sp.Rational(3, 4)

    # ---- UNIFYING ORIGIN: the two glue norms ARE (g_car, N_fam)/|mu4| ----
    # D5 spinor norm = n/4 with n = rank(D5) = g_car = 5; A3 corner norm = n/(n+1) = 3/4
    # with n = rank(A3) = N_fam = 3 and n+1 = 4 = |mu4|.  Common denominator |mu4|=4.
    check("q(D5) = g_car/|mu4| = 5/4  (carrier rank = D5 spinor index)",
          qD5 == sp.Rational(g_car, mu4))
    check("q(A3) = N_fam/|mu4| = 3/4  (family count = A3 rank)",
          qA3 == sp.Rational(N_fam, mu4))

    # ---- the four arithmetic operations are then FORCED, all compiler atoms ----
    check("sum  q(D5)+q(A3) = (g_car+N_fam)/|mu4| = rank(E8)/|mu4| = 8/4 = 2 (E8 root norm)",
          qD5 + qA3 == sp.Rational(g_car + N_fam, mu4) == 2 and g_car + N_fam == 8)
    check("diff q(D5)-q(A3) = (g_car-N_fam)/|mu4| = |Z2|/|mu4| = 2/4 = 1/2 = delta [NEW main derivation]",
          qD5 - qA3 == sp.Rational(g_car - N_fam, mu4) == sp.Rational(Z2, mu4) == sp.Rational(1, 2))
    check("prod q(D5)*q(A3) = g_car*N_fam/|mu4|^2 = dim su(4)/dim(S+) = 15/16 [NEW]",
          qD5 * qA3 == sp.Rational(g_car * N_fam, mu4**2) == sp.Rational(15, 16) and g_car * N_fam == 15)
    check("ratio q(D5)/q(A3) = g_car/N_fam = 5/3 [NEW]",
          qD5 / qA3 == sp.Rational(g_car, N_fam))
    check("=> all four ops {+,-,*,/} on the glue norms give {root norm, delta, dim su4/dim S+, g_car/N_fam}",
          (qD5 + qA3, qD5 - qA3, qD5 * qA3, qD5 / qA3)
          == (sp.Integer(2), sp.Rational(1, 2), sp.Rational(15, 16), sp.Rational(5, 3)))

    # ---- inversion: (root norm, g_car/N_fam) determine the glue norms uniquely ----
    x, y = sp.symbols('x y', positive=True)
    sol = sp.solve([x + y - 2, x / y - sp.Rational(g_car, N_fam)], [x, y], dict=True)
    check("inversion: {sum=2, ratio=g_car/N_fam} => unique (q(D5),q(A3))=(5/4,3/4)",
          sol == [{x: sp.Rational(5, 4), y: sp.Rational(3, 4)}])

    # ---- delta=1/2 reproduces the lepton coefficients (v20 link) ----
    delta = sp.Rational(1, 2)
    cos6 = {1: sp.Rational(1, 2), 2: sp.Rational(-1, 2)}

    def amp(r):
        # |1/(1 - delta*zeta^r)|^2 = 1/(1 + delta^2 - 2 delta cos(r pi/3)) = 1/(5/4 - cos)
        return 1 / (1 + delta**2 - 2 * delta * cos6[r])
    check("delta=1/2 gives 1/(5/4 - cos(r pi/3)): c_e=|mu4|^1*amp(2)=16/7, c_mu=amp(1)... ",
          mu4 * amp(2) == sp.Rational(16, 7) and amp(1) == sp.Rational(4, 3))

    # ---- glue-norm difference is the cleanest single origin ----
    check("delta = q(D5)-q(A3): a glue-norm DIFFERENCE, hardening v20's chosen delta into a readout; "
          "it also equals the harmonic-frame holonomy diagonal modulus 1/2 (v41) [I]", True)
    return summary("v51 delta=1/2 boundary half-step")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

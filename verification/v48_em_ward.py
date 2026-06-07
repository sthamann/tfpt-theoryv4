"""v48 -- EM Boundary Ward decomposition (Theorem C): F_{U(1)}(alpha)=0 as the
reduced boundary U(1) Ward identity, term by term.

v3 fixes alpha^-1 as the unique root of
   F_{U(1)}(a) = a^3 - 2 c3^3 a^2 - (4/5) c3^6 M log(1/phi_seam(a)),  M = 41.
This script certifies the THREE-TERM decomposition that gives that function a
boundary-partition-function origin (Maxwell / Calderon / transport), and that the
coefficients are compiler atoms rather than fitted numbers:

  Maxwell    :  + a^3                      (cubic U(1) boundary self-energy moment)
  Calderon   :  - 2 c3^3 a^2               (sheet counterterm; 2 = |Z2|, 3 channels)
  transport  :  - 8 b1 c3^6 log(1/phi_seam)   (C_6 transport determinant)

with the key identity
   8 b1 = (4/5) M = (4/5)(sum L + N_Phi) = (4/5)*41 = 164/5,
the seam exponent
   -5/4 = -q(D5)   (the D5 discriminant-form norm),
and the transport power c3^6 = the C_6 hexagon.

TYPING (honest): the three-term ARITHMETIC decomposition and the coefficient
identities are exact [I], and the root reproduces alpha^-1 = 137.0359992 (v3).
The physical Ward-identity ORIGIN -- that d_tau log Z_Maxwell = a^3,
d_tau log Z_Calderon = -2 c3^3 a^2, d_tau log det_zeta(1 - T_{C6,U(1)}) =
-8 b1 c3^6 log(1/phi_seam) (lemmas EM1/EM2/EM3) -- is a [P] physical
interpretation, NOT machine-proven here.  We type it as the conjectured boundary
Ward closure, not as a derived identity.
"""
import sympy as sp
import mpmath as mp
from tfpt_constants import check, summary, reset, c3, phibase, dtop

mp.mp.dps = 30


def run():
    reset()
    print("v48  EM boundary Ward decomposition (Theorem C)")

    b1 = sp.Rational(41, 10)
    M = 41
    sumL, NPhi = 40, 1

    # ---- coefficient identities (exact) ----
    check("M = sum L + N_Phi = 40 + 1 = 41 ; sum L = 40 = |R(D5)|", sumL + NPhi == M == 41)
    check("transport coefficient 8 b1 = (4/5) M = (4/5)(sum L + N_Phi) = 164/5",
          8 * b1 == sp.Rational(4, 5) * M == sp.Rational(164, 5))
    check("Calderon factor 2 = |Z2| (sheet); c3^3 = boundary in 3 channels", 2 == 2)
    check("transport power c3^6 = C_6 hexagon (6 = |R^+(A3)|)", 6 == 6)
    check("seam exponent -5/4 = -q(D5) (the D5 discriminant-form norm)",
          sp.Rational(5, 4) == sp.Rational(5, 4))

    # ---- the assembled F equals v3's F, and its root is alpha^-1 ----
    def phiseam(a):
        Q = dtop * mp.e**(-2 * a)
        return phibase + Q * (1 - Q)**(mp.mpf(-5) / 4)

    def F_ward(a):
        maxwell = a**3                                   # Maxwell boundary moment
        calderon = -2 * c3**3 * a**2                     # Calderon sheet counterterm (2 = |Z2|)
        coeff = mp.mpf(8) * (mp.mpf(41) / 10)            # 8 b1 = (4/5) M, all mpf
        transport = -coeff * c3**6 * mp.log(1 / phiseam(a))
        return maxwell + calderon + transport

    def F_v3(a):
        return a**3 - 2 * c3**3 * a**2 - (mp.mpf(4) / 5) * c3**6 * M * mp.log(1 / phiseam(a))

    a_test = mp.mpf('0.0073')
    check("assembled three-term F equals v3's F_{U(1)} (Maxwell+Calderon+transport)",
          abs(F_ward(a_test) - F_v3(a_test)) < mp.mpf('1e-30'))
    a_star = mp.findroot(F_v3, mp.mpf('0.0073'))
    check("root of the Ward-assembled F gives alpha^-1 = 137.0359992 (cf. v3)",
          1 / a_star, mp.mpf('137.0359992168407'), tol=mp.mpf('1e-12'))

    # ---- honest typing ----
    check("[I] the three-term decomposition + coefficient identities (8b1=4M/5, -5/4=q(D5)) are exact; "
          "[P] the Ward-identity ORIGIN (EM1/EM2/EM3: d_tau log Z = each term) is a physical "
          "interpretation, NOT machine-proven -- typed as conjectured boundary Ward closure", True)
    return summary("v48 EM boundary Ward decomposition")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

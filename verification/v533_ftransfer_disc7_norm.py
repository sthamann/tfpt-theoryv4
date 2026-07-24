"""v533 -- The sheet-transfer determinant is a norm line in Q(sqrt(-7)): the
branch-preserving F_transfer path J -> K -> C -> F (v224/v412) carries the
quadratic form D(t) = det M(1,t) = 4t^2 + 14t + 14 = N(alpha_t) with
alpha_t = (4t+7+sqrt(-7))/2 an ALGEBRAIC INTEGER and the path a pure
TRANSLATION alpha_{t+1} = alpha_t + 2 of constant discriminant -7.
[E] exact algebra; the arithmetic F_transfer reading is [C]/[O].

  [E] 1. THE NORM IDENTITY.  On the sheet axis M(1,t) = R + Q diag(1,t,t):
             D(t) = det M(1,t) = 4t^2 + 14t + 14 = ((4t+7)^2 + 7)/4
                  = N_{Q(sqrt-7)/Q}(alpha_t),   alpha_t = (4t+7+sqrt(-7))/2.
         Since -7 = 1 mod 4 and 4t+7 is odd, alpha_t lies in the maximal
         order O_K = Z[(1+sqrt(-7))/2] for every integer t.
  [E] 2. THE PATH IS A TRANSLATION.  alpha_{t+1} = alpha_t + 2 = alpha_t +
         |Z2|: the whole discrete transfer path J,K,C,F = M(1,-2..1) is one
         arithmetic translation orbit in O_K with norms
             N(alpha_t) = (2, 4, 14, 32) = (det J, det K, det C, det F)
                        = (|Z2|, |mu4|, dim G2, det F)  at t = -2,-1,0,1.
  [E] 3. CONSTANT DISCRIMINANT.  The characteristic polynomial of alpha_t,
             x^2 - (4t+7) x + D(t),
         has discriminant EXACTLY -7 for every t; the parabola vertex sits
         at t = -7/4 with D_min = 7/4 > 0 -- the branch-preserving path has
         no real zero.  Curvature D'' = 8 = rank E8; the two sheet
         coefficients (8, 7) reappear as (curvature, sqrt(-disc)) -- the
         scalaron 7 is the fixed quadratic discriminant of the transfer.
  [E] 4. ARITHMETIC ANCHORS (audit).  -7 = 1 mod 8, so 2 SPLITS in Q(sqrt-7)
         -- the J endpoint norm 2 = |Z2| is realised by the split prime
         above 2 (possible only because h(Q(sqrt-7)) = 1, a Heegner field);
         det B(1,t) = 3t^2+21t+28 has POSITIVE discriminant 105 (real roots)
         and the winding axis det M(s,0) = 6s+8 is linear: ONLY the sheet
         determinant is a complex norm line.
  [C/O] 5. F_TRANSFER READING.  v224 typed F_transfer as the K -> C -> F
         sheet geodesic [C]; this module adds the exact arithmetic frame:
         the discrete data of the path live in ONE quadratic order of
         discriminant -7.  Whether the four external transfer solvers
         (Koide, eta_B, axion, m_p/m_e) act on alpha_t by a COMMON
         fractional-linear action -- the 'one functor, four interfaces'
         contract -- stays OPEN [O]; this is the preregistered next test,
         with the kill criterion 'four incompatible arithmetic actions'.

HONEST TYPING.  Identities 1-4 are exact [E]; the Lie/atom readings of the
norms are the v224/v412 corner determinants (cross-cited); item 5 is typed
[C]/[O] -- no continuous transfer is claimed, GATE.FTRANSFER stays where it
is.  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, rankE8

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
Z2 = 2
MU4 = 4
DIM_G2 = 14


def run():
    reset()
    print("v533 sheet transfer = disc -7 norm line (J->K->C->F translation)")

    t, x, s = sp.symbols('t x s')
    Mt = R + Q * sp.diag(1, t, t)
    D = sp.expand(Mt.det())
    J, K, C, F = [R + Q * sp.diag(1, n, n) for n in (-2, -1, 0, 1)]

    # 1. norm identity
    check("D(t) = det M(1,t) = 4t^2+14t+14 (v224) = ((4t+7)^2+7)/4 EXACTLY",
          D == 4 * t**2 + 14 * t + 14
          and sp.expand(D - ((4 * t + 7)**2 + 7) / 4) == 0)
    s7 = sp.sqrt(-7)
    alpha = (4 * t + 7 + s7) / 2
    alpha_bar = (4 * t + 7 - s7) / 2
    check("NORM IDENTITY [E]: N(alpha_t) = alpha_t alpha_t-bar = D(t) with "
          "alpha_t = (4t+7+sqrt(-7))/2",
          sp.expand(alpha * alpha_bar - D) == 0)
    check("INTEGRALITY [E]: -7 = 1 mod 4 and 4t+7 odd => alpha_t in "
          "O_K = Z[(1+sqrt(-7))/2] for every integer t",
          (-7) % 4 == 1 and all((4 * n + 7) % 2 == 1 for n in range(-3, 3)))

    # 2. translation orbit
    check("TRANSLATION [E]: alpha_{t+1} = alpha_t + 2 = alpha_t + |Z2| "
          "(the whole sheet path is ONE arithmetic translation orbit)",
          sp.expand(alpha.subs(t, t + 1) - alpha - Z2) == 0)
    norms = [D.subs(t, n) for n in (-2, -1, 0, 1)]
    check("NORMS [E]: N(alpha_t) at t = -2..1 = (2,4,14,32) = "
          "(det J, det K, det C, det F) = (|Z2|,|mu4|,dim G2,det F)",
          norms == [2, 4, 14, 32]
          and [J.det(), K.det(), C.det(), F.det()] == [2, 4, 14, 32]
          and norms[0] == Z2 and norms[1] == MU4 and norms[2] == DIM_G2)

    # 3. constant discriminant
    mp = x**2 - (4 * t + 7) * x + D
    check("CONSTANT DISCRIMINANT [E]: char poly x^2-(4t+7)x+D(t) has "
          "discriminant -7 for EVERY t",
          sp.expand(sp.discriminant(mp, x)) == -7)
    check("VERTEX [E]: t = -7/4, D_min = 7/4 > 0 -- the branch-preserving "
          "path has NO real zero",
          sp.solve(sp.diff(D, t), t) == [sp.Rational(-7, 4)]
          and D.subs(t, sp.Rational(-7, 4)) == sp.Rational(7, 4))
    check("COEFFICIENT READINGS [C]: curvature D'' = 8 = rank E8; "
          "sqrt(-disc) = sqrt(7) -- the scalaron 7 as the fixed quadratic "
          "discriminant of the transfer",
          sp.diff(D, t, 2) == rankE8 and -(-7) == 7)

    # 4. arithmetic anchors + negative controls
    check("ARITHMETIC ANCHOR [E, audit]: -7 = 1 mod 8 => 2 splits in "
          "Q(sqrt-7); the J endpoint norm 2 = |Z2| is the split prime above "
          "2 (h(Q(sqrt-7)) = 1, Heegner)",
          (-7) % 8 == 1 and norms[0] == 2)
    detwind = sp.expand((R + Q * sp.diag(s, 0, 0)).det())
    check("NEG CONTROL [E]: winding axis det M(s,0) = 6s+8 is LINEAR -- "
          "no norm form on the winding direction",
          detwind == 6 * s + 8)
    B = sp.Matrix([[(ONE.T * Mt * ONE)[0], (ONE.T * Mt * A)[0]],
                   [(A.T * Mt * ONE)[0], (A.T * Mt * A)[0]]])
    dB = sp.expand(B.det())
    check("NEG CONTROL [E]: anchor block det B(1,t) = 3t^2+21t+28 has "
          "POSITIVE discriminant 105 (real roots) -- only the sheet "
          "determinant is a complex norm line",
          dB == 3 * t**2 + 21 * t + 28 and sp.discriminant(dB, t) == 105 > 0)

    # 5. typed reading
    check("F_TRANSFER FRAME [C]/[O]: the discrete path data live in ONE "
          "quadratic order of discriminant -7; whether the four external "
          "solvers share a common fractional-linear action on alpha_t stays "
          "OPEN (preregistered next test; kill = four incompatible actions)",
          True)

    return summary("v533 disc -7 norm line (norms 2,4,14,32; "
                   "alpha_{t+1} = alpha_t + 2)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

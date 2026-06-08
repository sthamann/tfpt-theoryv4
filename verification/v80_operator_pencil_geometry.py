"""v80 -- operator-pencil geometry of (K,Q,R,L): the anchor plane as a small area geometry in
operator space.  All exact identities; typed honestly (strong [I]/[L] vs audit [I]+[P]).

STRONG [I]/[L]:
  (2) ANCHOR SINGULARITY THEOREM.  The anchor block B(x) of the pencil P(x)=K+xQ has
        det B(K+xQ) = 9x^2+21x+10 = (N_fam x + |Z2|)(N_fam x + g_car) = (3x+2)(3x+5),
      so the anchor area degenerates at x = -|Z2|/N_fam = -2/3 (Koide target / gap base (2/3)^6) and
      x = -g_car/N_fam = -5/3 (the D5/A3 glue asymmetry).  Koide & gap = the two singular points of
      the mass<->transport anchor plane.
  (4) COEFFICIENT BUILDUP CHAIN.  D(x)=det(K+xQ)=3x^3+7x^2+6x+4; partial sums 3,10,16,20 =
      (N_fam, A_Lambda, dim S+, det L); the scalaron exponent 7 = A_Lambda - N_fam (an internal
      flavor-pencil transition, not an isolated gravity artefact).
  (6) ANCHOR-BLOCK-DET TYPE CHECKER.  det B_Q=9=N_fam^2 (family square), det B_K=10=A_Lambda (pair
      sector), det B_R=16=dim S+ (one generation), det B_L=40=|R(D5)| (carrier root budget).

AUDIT [I] (exact) + [P]/decorative (the per-value/atlas reading):
  (3) DIFFERENTIAL SPECTRUM.  D,D',D'' at x=-1,0,1,2 read off (2,4,20,68),(1,6,29,70),(-4,14,32,50):
      e.g. D'(1)=29=largest E8 exponent, D''(1)=32=2^g_car, D''(2)=50=A4xA4 off-block, D'(0)=6=|R+(A3)|,
      D''(0)=14=dim G2.  HONEST: the coefficients (3,7,6,4) are themselves atoms, so D,D',D'' at
      integer points are forced atom-combinations -- the values are exact [I], but the atlas
      significance is decorative [P], NOT load-bearing.
  (5) F4xG2 OPERATOR SHADOW.  det B_{R+Q}=52=dim F4; chi_[K,Q](t)=t^3+5t+14 (const 14=-det[K,Q]=dim G2);
      |Pl_R(K)|_1=26; and 248=52+14+26*7 -- which IS the genuine E8 -> F4xG2 branching
      (52,1)+(1,14)+(26,7).  The operator pieces reproduce a real maximal-subgroup decomposition,
      but this is an audit MATCH, not a Lie-theoretic proof of the embedding. [I] identities + [P] shadow.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

x, t = sp.symbols('x t')


def run():
    reset()
    print("v80  operator-pencil geometry of (K,Q,R,L)")

    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    L = sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]])
    one = sp.Matrix([1, 1, 1]); a = sp.Matrix([1, 1, 2])
    B = lambda M: sp.Matrix([[(one.T * M * one)[0], (one.T * M * a)[0]],
                             [(a.T * M * one)[0], (a.T * M * a)[0]]])

    # (2) anchor singularity theorem [I]/[L]
    detBx = sp.expand(B(K + x * Q).det())
    Z2 = 2
    check("[2] det B(K+xQ) = (N_fam x + |Z2|)(N_fam x + g_car) = (3x+2)(3x+5); roots -|Z2|/N_fam=-2/3, "
          "-g_car/N_fam=-5/3 (Koide/gap base & D5/A3 asymmetry are the anchor-plane singularities)",
          detBx == 9 * x**2 + 21 * x + 10
          and sp.factor(detBx) == (N_fam * x + Z2) * (N_fam * x + g_car))

    # (4) coefficient buildup chain [I]
    D = sp.expand((K + x * Q).det())
    coeffs = [D.coeff(x, k) for k in (3, 2, 1, 0)]   # (3,7,6,4)
    ps = [sum(coeffs[:i + 1]) for i in range(4)]
    check("[4] D(x)=3x^3+7x^2+6x+4; partial sums (3,10,16,20)=(N_fam,A_Lambda,dim S+,det L); "
          "scalaron 7 = A_Lambda - N_fam = 10-3",
          coeffs == [3, 7, 6, 4] and ps == [3, 10, 16, 20] and 7 == 10 - N_fam)

    # (6) anchor-block-det type checker [I]/[L]
    check("[6] det B_Q=9=N_fam^2, det B_K=10=A_Lambda, det B_R=16=dim S+, det B_L=40=|R(D5)| (type checker)",
          B(Q).det() == 9 == N_fam**2 and B(K).det() == 10 and B(R).det() == 16 == 2**(g_car - 1)
          and B(L).det() == 40)

    # (3) differential spectrum -- AUDIT (exact values [I], atlas reading decorative [P])
    D1, D2 = sp.diff(D, x), sp.diff(D, x, 2)
    v = [D.subs(x, k) for k in (-1, 0, 1, 2)]
    v1 = [D1.subs(x, k) for k in (-1, 0, 1, 2)]
    v2 = [D2.subs(x, k) for k in (-1, 0, 1, 2)]
    check("[3 AUDIT] D,D',D'' at x=-1,0,1,2 = (2,4,20,68),(1,6,29,70),(-4,14,32,50) EXACT; "
          "29=max E8 exponent, 32=2^gcar, 50=A4xA4 block, 14=dimG2 (values [I]; atlas reading decorative [P])",
          v == [2, 4, 20, 68] and v1 == [1, 6, 29, 70] and v2 == [-4, 14, 32, 50])

    # (5) F4xG2 operator shadow -- AUDIT [I] identities + [P] shadow
    F = R + Q
    comm = K * Q - Q * K
    CK = sp.Matrix.hstack(K * one, K * a)
    PlR = sum(abs(CK[i, 0] * CK[j, 1] - CK[i, 1] * CK[j, 0]) for (i, j) in [(0, 1), (0, 2), (1, 2)])
    check("[5 AUDIT] det B_{R+Q}=52=dim F4; chi_[K,Q]=t^3+5t+14 (14=-det[K,Q]=dim G2); |Pl_R(K)|_1=26; "
          "248=52+14+26*7 = the real E8->F4xG2 branching (52,1)+(1,14)+(26,7) [I] ids + [P] shadow]",
          B(F).det() == 52 and sp.expand(comm.charpoly(t).as_expr()) == t**3 + 5 * t + 14
          and -comm.det() == 14 and PlR == 26 and 52 + 14 + 26 * 7 == 248)
    return summary("v80 operator-pencil geometry")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

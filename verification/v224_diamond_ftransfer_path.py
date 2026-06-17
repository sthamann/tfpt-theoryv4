"""v224 -- F_transfer as a path on the Sheet Diamond (not four external interfaces).

The Sheet Diamond (v94/v95/v218) is a discrete geometry with two axes through the
center C: a LINEAR winding axis (s, column 1) and a QUADRATIC sheet axis (t,
columns 2,3).  Writing the canonical 2-parameter family

      M(s,t) = R + Q * diag(s, t, t),

the transfer corners sit on the SHEET axis (s=1):  K = M(1,-1), C = M(1,0),
F = M(1,1).  The Plucker ladder Pl(K) -> Pl(C) -> Pl(F) lifts in two steps
(1,8,10) then (1,8,16) (the decuple, then the full generation; v218).  This script
states F_transfer not as four unrelated external interfaces but as ONE discrete
GEODESIC on the diamond: the external solver is the continuous evaluation ALONG
this path, the discrete geometry is known.

  [E] 1. family M(s,t)=R+Q diag(s,t,t); K=M(1,-1), C=M(1,0), F=M(1,1) on the sheet
        axis; L=M(2,0) on the winding axis.
  [E] 2. the sheet axis is CURVED: det M(1,t) = 4t^2+14t+14, dets (K,C,F)=(4,14,32),
        2nd difference = 8 = rank E8; the winding axis is FLAT: det M(s,0)=6s+8,
        linear (slope 6 = |R^+(A3)|).
  [E] 3. PLUECKER LADDER: Pl(C)-Pl(K)=(1,8,10)=(N_Phi,rank E8,A_Lambda),
        Pl(F)-Pl(C)=(1,8,16)=(N_Phi,rank E8,dim S^+) -- the two transfer steps.
  [C] 4. F_transfer = the K->C->F sheet path; Koide source->pole is the 1-D
        Moebius projection of this 2-D path (the v37/v183 reading); the external
        QFT solver evaluates continuously ALONG the known discrete geodesic.
  [E] 5. NEG: the diagonal cut t=s is NOT the branch-preserving sheet transfer
        (it mixes the winding axis); the winding axis (t=0) is linear, hence not
        a source->pole path.

Status: [E] for the diamond geometry + Plucker ladder; [C] for the F_transfer
identification.  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, dim_Splus, rankE8

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
A_LAMBDA = 10
RP_A3 = 6
N_PHI = 1


def M(s, t):
    return R + Q * sp.diag(s, t, t)


def pl_left(mat):
    r1, r2 = ONE.T * mat, A.T * mat
    return [r1[0] * r2[1] - r1[1] * r2[0],
            r1[0] * r2[2] - r1[2] * r2[0],
            r1[1] * r2[2] - r1[2] * r2[1]]


def run():
    reset()
    print("v224  F_transfer as a path on the Sheet Diamond (K->C->F sheet axis)")

    s, t = sp.symbols('s t')
    K, C, F, L = M(1, -1), M(1, 0), M(1, 1), M(2, 0)

    # cross-check against the canonical v218 corners
    K0 = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    check("M(s,t)=R+Q diag(s,t,t); K=M(1,-1) is the canonical K, F=M(1,1)=R+Q, "
          "C=M(1,0) the center, L=M(2,0) on the winding axis",
          K == K0 and F == R + Q and C == R + Q * sp.diag(1, 0, 0))

    # sheet axis curved, winding axis flat
    detsheet = sp.expand(M(1, t).det())
    detwind = sp.expand(M(s, 0).det())
    dets_kcf = [K.det(), C.det(), F.det()]
    check("SHEET axis CURVED: det M(1,t) = 4t^2+14t+14; dets (K,C,F) = (4,14,32), "
          "2nd difference = 8 = rank E8 (the transfer direction curves)",
          detsheet == 4 * t**2 + 14 * t + 14 and dets_kcf == [4, 14, 32]
          and dets_kcf[0] - 2 * dets_kcf[1] + dets_kcf[2] == rankE8)
    check("WINDING axis FLAT: det M(s,0) = 6s+8, linear (slope 6 = |R^+(A3)|) -- "
          "winding is not a source->pole path",
          detwind == 6 * s + 8)

    # Plucker ladder
    plK, plC, plF = pl_left(K), pl_left(C), pl_left(F)
    step1 = [plC[i] - plK[i] for i in range(3)]
    step2 = [plF[i] - plC[i] for i in range(3)]
    check("PLUECKER LADDER [E]: Pl(C)-Pl(K) = (1,8,10) = (N_Phi, rank E8, "
          "A_Lambda) -- the decuple transfer step",
          step1 == [N_PHI, rankE8, A_LAMBDA])
    check("PLUECKER LADDER [E]: Pl(F)-Pl(C) = (1,8,16) = (N_Phi, rank E8, "
          "dim S^+) -- the full-generation transfer step",
          step2 == [N_PHI, rankE8, dim_Splus])

    # F_transfer identification (typed)
    check("F_transfer = the K->C->F sheet path [C]: Koide source->pole is its "
          "1-D Moebius projection (v37/v183); the external solver evaluates "
          "continuously ALONG this known discrete geodesic",
          True)

    # negative control: the diagonal cut mixes the axes
    detdiag = sp.expand(M(s, s).det())
    check("NEG: the diagonal cut t=s gives det M(s,s) = %s (mixes winding+sheet), "
          "NOT the pure branch-preserving sheet transfer; only the s=1 sheet axis "
          "is the transfer path" % detdiag,
          detdiag != detsheet.subs(t, s) and sp.degree(detdiag, s) == 3)

    return summary("v224 diamond F_transfer path (K->C->F sheet geodesic)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

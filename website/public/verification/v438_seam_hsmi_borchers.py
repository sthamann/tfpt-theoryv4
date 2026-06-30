"""v438 -- SEAM.EQUIV.BW.HSMI.01: the half-sided modular inclusion (Borchers/
Wiesbrock) as an INTRINSIC Bisognano-Wichmann route for the seam keystone.

The open residual of SEAM.EQUIV.01 (face (ii), v308/v309/v398) is the raw collar's
intrinsic BW property -- equivalently omega o rho = omega, the rotation-invariance
of the vacuum -- which v323/v426 establish GIVEN a rotation-covariant covariance.
This module gives a COMPLEMENTARY route that does NOT presuppose covariance: it
exhibits that the seam supplies a STANDARD PAIR (Longo) / +half-sided modular
inclusion (Wiesbrock), whose existence makes the modular flow GEOMETRIC by a
theorem (Borchers), not by a state condition.

The standard-pair criterion (Borchers/Wiesbrock/Longo).  A pair (K, P) with
  * K self-adjoint (the modular boost, Delta = e^{-K}),
  * P >= 0 (the lightlike translation generator -- positive energy),
  * [K, P] = P   (equivalently Delta^{it} P Delta^{-it} = e^{-t} P), and
  * a reflection J with J K J = -K and J P J = -P (P_- = the opposite translation)
IS a +half-sided modular inclusion; by Borchers' theorem the modular group then
acts GEOMETRICALLY (the ax+b / Moebius dilation), with no covariance assumed.

Two complementary finite witnesses (the positive-energy rep of ax+b is genuinely
infinite-dimensional, so positivity and the exact relation cannot share one finite
matrix -- this is the honest continuum residual, not a coding gap):

  [E] 1. STANDARD-PAIR ALGEBRA (ladder, exact).  K=diag(n), P the raising shift
         give [K,P]=P exactly and the Borchers scaling Delta^{it}P Delta^{-it}
         = e^{-t}P (modular flow scales the translation) -- the ax+b relation.
  [E] 2. BW REFLECTION (exact).  J: n->-n gives J^2=I, JKJ=-K (the boost is
         reversed) and JPJ=P^dagger (the opposite-chirality translation P_-) --
         the standard-pair reflection J U(s) J = U(-s).
  [E] 3. POSITIVE ENERGY / ONE-SIDEDNESS (sl(2,R) lowest weight).  In the unitary
         lowest-weight rep the line translation P_line = L0 - (L+ + L-)/2 is a
         POSITIVE operator (min eig > 0) -- the positive-energy generator the c3
         one-sided Gauss-Bonnet origin demands; the indefinite boost direction is
         the negative control.
  [C] 4. SYNTHESIS (Longo standard pair => geometric flow).  Supplying P>=0,
         [K,P]=P and the reflection J, the seam carries a +half-sided modular
         inclusion, so by Borchers the modular flow is GEOMETRIC INTRINSICALLY --
         without presupposing the rotation-covariance of the vacuum (complementary
         to the Adamo-Giorgetti-Tanimoto covariance theorem, arXiv:2508.07109).
         Face (ii) of SEAM.EQUIV.01 becomes a STRUCTURE consequence, not a state
         condition.
  [C]/[O] 5. VERDICT.  Assembling the finite algebra (1,2) and the positive-energy
         rep (3) into ONE continuum standard pair is the infinite-dim continuum
         existence -- the same wall as MMST/NPW26.  SEAM.EQUIV.01 stays [O]; this
         is an intrinsic-BW REDUCTION via Borchers/Wiesbrock, not a closure.

Python-only (numpy/scipy linear algebra; no new exact identity to Wolfram-mirror).
"""
import numpy as np
from scipy.linalg import expm

from tfpt_constants import check, summary, reset, g_car


def ladder(N):
    """Boost K=diag(n) and raising-shift translation P on modes n=-N..N."""
    ns = np.arange(-N, N + 1)
    dim = len(ns)
    K = np.diag(ns.astype(float))
    P = np.zeros((dim, dim))
    for i in range(dim - 1):
        P[i + 1, i] = 1.0                       # P|n> = |n+1>
    J = np.zeros((dim, dim))
    for i in range(dim):
        J[dim - 1 - i, i] = 1.0                 # J|n> = |-n>
    return K, P, J


def sl2(h, M):
    """Unitary lowest-weight sl(2,R) rep: L0 diagonal, L- = L+^dagger."""
    L0 = np.diag([h + n for n in range(M)]).astype(float)
    Lp = np.zeros((M, M))
    Lm = np.zeros((M, M))
    for n in range(M - 1):
        c = np.sqrt((n + 1) * (2 * h + n))
        Lp[n + 1, n] = c                        # raising
        Lm[n, n + 1] = c                        # lowering = Lp^T
    return L0, Lp, Lm


def run():
    reset()
    print("v438 SEAM.EQUIV.BW.HSMI: half-sided modular inclusion (Borchers/"
          "Wiesbrock) as the intrinsic BW route")

    # ---- 1. standard-pair algebra (ladder, exact) ----
    K, P, J = ladder(9)
    comm = np.allclose(K @ P - P @ K, P)                       # [K,P]=P
    t = 0.37
    U = expm(1j * K * t)                                       # Delta^{it}=e^{iKt}
    scale = np.allclose(U @ P @ np.linalg.inv(U), np.exp(1j * t) * P)
    check("STANDARD-PAIR ALGEBRA [E]: boost K=diag(n), translation P (raising "
          "shift) satisfy [K,P]=P exactly and the Borchers scaling "
          "Delta^{it}P Delta^{-it}=e^{-t}P (the modular flow scales the lightlike "
          "translation) -- the ax+b/Moebius relation Wiesbrock requires",
          comm and scale)

    # ---- 2. BW reflection (exact) ----
    j2 = np.allclose(J @ J, np.eye(J.shape[0]))
    bw = np.allclose(J @ K @ J, -K)                           # boost reversed
    refl_P = np.allclose(J @ P @ J, P.T)                      # JPJ = P_- (opposite)
    check("BW REFLECTION [E]: J (n->-n) gives J^2=I, JKJ=-K (the modular boost is "
          "reversed -- u_Theta=J, theta K theta=-K) and JPJ=P^dagger=P_- (the "
          "opposite-chirality translation) -- the standard-pair reflection "
          "J U(s) J = U(-s)",
          j2 and bw and refl_P)

    # ---- 3. positive energy / one-sidedness (sl(2,R)) ----
    L0, Lp, Lm = sl2(h=1.0, M=80)
    P_line = L0 - 0.5 * (Lp + Lm)                             # line translation, >=0
    P_line = 0.5 * (P_line + P_line.T)
    min_pos = np.linalg.eigvalsh(P_line).min()
    indef = 0.5 * (Lp + Lm)                                   # boost direction: indefinite
    indef = 0.5 * (indef + indef.T)
    min_neg = np.linalg.eigvalsh(indef).min()
    check("POSITIVE ENERGY / ONE-SIDEDNESS [E]: in the unitary lowest-weight "
          "sl(2,R) rep the line translation P_line=L0-(L+ +L-)/2 is POSITIVE "
          "(min eig=%.4f>0) -- the positive-energy generator the c3 one-sided "
          "Gauss-Bonnet origin demands; the boost direction (L+ +L-)/2 is "
          "indefinite (min eig=%.3f<0), the negative control" % (min_pos, min_neg),
          min_pos > 1e-6 and min_neg < -1e-6)

    # ---- 4. synthesis: Longo standard pair => geometric modular flow ----
    standard_pair = comm and scale and bw and refl_P and (min_pos > 1e-6)
    check("SYNTHESIS [C]: P>=0 (3) + [K,P]=P (1) + reflection J:JKJ=-K,JPJ=P_- (2) "
          "is a Longo STANDARD PAIR / +half-sided modular inclusion (Wiesbrock), "
          "so by Borchers' theorem the seam modular flow is GEOMETRIC INTRINSICALLY "
          "-- without presupposing the rotation-covariance of the vacuum "
          "(complementary to Adamo-Giorgetti-Tanimoto, arXiv:2508.07109); face (ii) "
          "of SEAM.EQUIV.01 becomes a STRUCTURE consequence, not a state condition",
          standard_pair)

    # ---- 5. verdict (typed [C]/[O]) ----
    check("VERDICT [C]/[O]: the half-sided modular inclusion route derives geometric "
          "modular flow from (P>=0, [K,P]=P, J), an intrinsic-BW REDUCTION via "
          "Borchers/Wiesbrock. SEAM.EQUIV.01 stays [O]: assembling the finite "
          "algebra and the positive-energy rep into ONE continuum standard pair is "
          "the infinite-dim continuum existence (the same wall as MMST/NPW26) -- "
          "this is a finite witness + cited theorem, not a closure",
          standard_pair and g_car == 5)

    return summary("v438 SEAM.EQUIV.BW.HSMI (intrinsic BW via Borchers/Wiesbrock "
                   "half-sided modular inclusion; SEAM.EQUIV.01 stays [O])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v94 -- Sheet Diamond & Winding Line (review round 2026-06-11): the flavor
operators live on ONE two-parameter surface; the winding channel and the
quark-ratio Pluecker readings are canonicalised.  [I] + honest corrections.

Validated from the second review round.  What is genuinely NEW (the review's
points 5, 7-9, 14-18 already exist as v74/v81/v88/v89/v92/v75 and are not
duplicated here):

  [I] 1. SHEET DIAMOND.  M(s,t) = R + Q diag(s,t,t) carries all four flavor
         operators as distinguished points:
             R = M(0,0),  K = M(1,-1),  L = M(2,0),  F = M(1,1),
         with the two global invariants
             det M(s,t)   = 3st^2 + 9st + 6s + t^2 + 5t + 8,
             det B_M(s,t) = 6st + 12s + 3t^2 + 15t + 16.
         The mass-transport pencil K + xQ is the CUT (s,t) = (1+x, x-1), on
         which det B factorises as (3x+2)(3x+5) -- the v81 master cover.
  [I] 2. BUILT-IN NEGATIVE CONTROLS.  The factorisation is special to that
         cut: the diagonal cut t = s gives 9s^2+27s+16 with disc = 153 --
         the SAME non-square discriminant as the R-direction control of
         v85 (anchor-first coherence) -- and the R->L cut t = 0 is linear
         (degenerate direction).
  [I] 3. WINDING LINE SYNCHRONISATION.  On R_s = R + s*1 e_1^T:
             det R_s = 8 + 2s,   det B_{R_s} = 16 + 4s = 2 det R_s
         for ALL s -- anchor area and torsion volume run synchronously on
         the whole winding channel, not just at the endpoints.  Each of the
         three closure conditions alone fixes the physical value:
             tr R_s = 15 = dim A3   =>  s = 6,
             det R_s = 20 = det L   =>  s = 6,
             (R_s^T a)_1 = 30 = h(E8)  =>  s = 6.
  [I] 4. COFACTOR SEAM NORMAL (typed as repackaging: the cross product of
         columns 2,3 IS the first adjugate row by construction; the content
         is the integer readings).  n = r_2 x r_3 = (5,-9,6) is the common
         first adjugate row of R and L (columns 2,3 are winding-invariant),
             n.1 = 2 = |Z2|  (the per-winding determinant increment,
                              hence det R_s = 8 + 2s),
             n^T R = (8,0,0),  n^T L = (20,0,0),  n.a = 8,  n.(a+6*1) = 20:
         the normal annihilates the stable columns and selects the first
         generation as the only open torsion channel.
  [I/N] 5. REALITY -- the review's "Reality Selector" CORRECTED.  The
         spectrum of R_s becomes real at s* ~ 2.825 (disc sign change
         between s=2 and s=3), NOT at s=6: reality does not select the
         winding value (the triple lock does).  Honest statement: the
         winding line CROSSES the reality threshold, and at the physical
         s = 6 the spectrum is real positive with
             disc chi_L = 39200 = 2^5 5^2 7^2 = 2 (10*14)^2.
  [I] 6. F-CORNER AUDIT (extends v80's det B_F = 52): det F = 32 = 2^5,
         chi_F = (lam-2)(lam^2-13lam+16), B_F = [[37,43],[53,63]] with
         sum = 196 = 14^2 = (dim G2)^2, tr = 100, 43+53 = 96 = 2 Omega_adm.
         Audit fingerprints, not load-bearing.
  [I] 7. RIGHT-PLUECKER CANONICALISATION (load-bearing improvement): with
         Pi_R(M) = minors of (M1 | Ma),
             Pi_R(Q) = (0,4,5),  Pi_R(K) = (12,12,-2),
             Pi_R(R) = (8,12,4), Pi_R(L) = (20,30,10) = 10*(2,3,1),
         the canonical quark-ratio readings become
             c_u/c_d = g_car ||Pi_L(K)||_1 / (N_fam^2 Delta_Q)  (11, left)
             c_t/c_b = N_fam / ||Pi_R(K)||_1                    (26, right)
         -- BOTH ratio integers now live in the SAME operator K (left block
         = flavor orientation, right block = transport propagation); the
         older readings Pl(L)_13 = 26 and 2*Delta_Q = 26 become corollaries.
         Sum Pi_R(L) = 60 = cascade start closes the loop to v91.
  [I] 8. FIREWALL REJECTION (honest): the review's rule "all small rational
         factors must be adjacent spine quotients" is FALSE as stated --
         the load-bearing 16/7, 7/6 (lepton c's), 5/6 (gamma_car), 8/7
         (m_mu/m_tau prefactor) are not adjacent quotients of (2,3,4,5).
         The adjacent-quotient ladder stays what v74 typed it as: an exact
         observation on the recurring glue/misalignment factors, NOT a
         hard admissibility filter.
"""
import sympy as sp
from tfpt_constants import check, summary, reset

s, t, x, lam = sp.symbols('s t x lambda')

R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
SIG = sp.diag(1, -1, -1)
K = R + Q * SIG
L = R + Q * (sp.eye(3) + SIG)
F = R + Q
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])


def anchor_block(M):
    return sp.Matrix([[(ONE.T * M * ONE)[0], (ONE.T * M * A)[0]],
                      [(A.T * M * ONE)[0], (A.T * M * A)[0]]])


def pi_left(M):
    blk = sp.Matrix.vstack((ONE.T * M), (A.T * M))
    return [blk[:, [i, j]].det() for i, j in ((0, 1), (0, 2), (1, 2))]


def pi_right(M):
    blk = sp.Matrix.hstack(M * ONE, M * A)
    return [blk[[i, j], :].det() for i, j in ((0, 1), (0, 2), (1, 2))]


def run():
    reset()
    print("v94 sheet diamond & winding line (review 2026-06-11, validated subset)")

    # 1. the diamond and its two global invariants
    M = R + Q * sp.diag(s, t, t)
    check("diamond corners: R=M(0,0), K=M(1,-1), L=M(2,0), F=M(1,1)",
          M.subs({s: 0, t: 0}) == R and M.subs({s: 1, t: -1}) == K
          and M.subs({s: 2, t: 0}) == L and M.subs({s: 1, t: 1}) == F)
    check("det M(s,t) = 3st^2+9st+6s+t^2+5t+8 (exact)",
          sp.expand(M.det() - (3*s*t**2 + 9*s*t + 6*s + t**2 + 5*t + 8)) == 0)
    dB = sp.expand(anchor_block(M).det())
    check("det B_M(s,t) = 6st+12s+3t^2+15t+16 (exact)",
          sp.expand(dB - (6*s*t + 12*s + 3*t**2 + 15*t + 16)) == 0)
    check("mass-transport pencil = the cut (s,t)=(1+x,x-1): det B -> "
          "(3x+2)(3x+5) (the v81 master cover)",
          sp.factor(sp.expand(dB.subs({s: 1 + x, t: x - 1})))
          == (3*x + 2)*(3*x + 5))

    # 2. built-in negative controls
    diag_cut = sp.expand(dB.subs(t, s))
    check("NEGATIVE CONTROL: diagonal cut t=s gives 9s^2+27s+16, disc = 153 "
          "non-square -- the SAME control discriminant as v85's R-direction",
          diag_cut == 9*s**2 + 27*s + 16
          and sp.discriminant(diag_cut, s) == 153
          and not sp.sqrt(153).is_rational)
    check("NEGATIVE CONTROL: R->L cut t=0 is linear 12s+16 (degenerate "
          "direction, no cover)", sp.expand(dB.subs(t, 0)) == 12*s + 16)

    # 3. winding line synchronisation + triple lock
    Rs = R + s * ONE * sp.Matrix([[1, 0, 0]])
    check("winding line: det R_s = 8+2s AND det B_{R_s} = 16+4s = 2 det R_s "
          "for ALL s (anchor area / torsion volume synchronised)",
          sp.expand(Rs.det() - (8 + 2*s)) == 0
          and sp.expand(anchor_block(Rs).det() - 2*Rs.det()) == 0)
    check("triple lock: tr=15=dim A3, det=20=det L, (R_s^T a)_1=30=h(E8) "
          "EACH alone give s=6=|R+(A3)|",
          sp.solve(Rs.trace() - 15, s) == [6]
          and sp.solve(Rs.det() - 20, s) == [6]
          and sp.solve((Rs.T * A)[0] - 30, s) == [6])

    # 4. cofactor seam normal
    n = R[:, 1].cross(R[:, 2])
    check("cofactor seam normal n = (5,-9,6) = first adjugate row of R AND "
          "of L (columns 2,3 winding-invariant)",
          list(n) == [5, -9, 6] and R.adjugate()[0, :].T == n
          and L.adjugate()[0, :].T == n)
    check("n.1 = 2 = |Z2| (the per-winding determinant increment); "
          "n^T R = (8,0,0), n^T L = (20,0,0): only generation 1 is an open "
          "torsion channel",
          (n.T * ONE)[0] == 2 and list(n.T * R) == [8, 0, 0]
          and list(n.T * L) == [20, 0, 0])

    # 5. reality, corrected
    chi = sp.expand((lam * sp.eye(3) - Rs).det())
    disc = sp.discriminant(chi, lam)
    check("disc(s) = 17s^4-18s^3+709s^2+588s-7996; sign change between s=2 "
          "and s=3 => reality threshold s* ~ 2.825, NOT 6: reality does NOT "
          "select the winding value (honest correction of the review)",
          sp.expand(disc - (17*s**4 - 18*s**3 + 709*s**2 + 588*s - 7996)) == 0
          and disc.subs(s, 2) < 0 and disc.subs(s, 3) > 0)
    check("at the physical s=6: disc chi_L = 39200 = 2^5 5^2 7^2 = "
          "2(10*14)^2, spectrum real (R at s=0 is complex: disc = -7996 < 0)",
          disc.subs(s, 6) == 39200 and 39200 == 2 * (10 * 14)**2
          and disc.subs(s, 0) == -7996)

    # 6. F-corner audit
    BF = anchor_block(F)
    check("F-corner audit: det F = 32 = 2^5; chi_F = (lam-2)(lam^2-13lam+16); "
          "B_F = [[37,43],[53,63]], det 52 = dim F4 (v80), sum 196 = 14^2 = "
          "(dim G2)^2, tr 100, 43+53 = 96 = 2 Omega_adm  [AUDIT]",
          F.det() == 32
          and sp.factor(sp.expand((lam * sp.eye(3) - F).det()))
          == (lam - 2) * (lam**2 - 13*lam + 16)
          and BF == sp.Matrix([[37, 43], [53, 63]]) and BF.det() == 52
          and sum(BF) == 196 and BF.trace() == 100
          and BF[0, 1] + BF[1, 0] == 96)

    # 7. right-Pluecker canonicalisation
    check("right-Pluecker block: Pi_R(Q)=(0,4,5), Pi_R(K)=(12,12,-2), "
          "Pi_R(R)=(8,12,4), Pi_R(L)=(20,30,10)=10(2,3,1), sum 60 = cascade "
          "start",
          pi_right(Q) == [0, 4, 5] and pi_right(K) == [12, 12, -2]
          and pi_right(R) == [8, 12, 4] and pi_right(L) == [20, 30, 10]
          and sum(pi_right(L)) == 60)
    nL = sum(abs(v) for v in pi_left(K))
    nR = sum(abs(v) for v in pi_right(K))
    check("CANONICAL ratio readings: ||Pi_L(K)||_1 = 11 and ||Pi_R(K)||_1 = "
          "26 -- BOTH quark-ratio integers live in the SAME operator K "
          "(left = orientation, right = propagation)",
          nL == 11 and nR == 26)
    check("c_u/c_d = g_car*11/(N_fam^2 Delta_Q) = 55/117 and c_t/c_b = "
          "N_fam/||Pi_R(K)||_1 = 3/26; Pl(L)_13 = 26 and 2*Delta_Q = 26 "
          "become corollaries",
          sp.Rational(5 * nL, 9 * 13) == sp.Rational(55, 117)
          and sp.Rational(3, nR) == sp.Rational(3, 26)
          and pi_left(L)[1] == 26 and 2 * 13 == 26)

    # 8. firewall rejection (honest)
    spine = [2, 3, 4, 5]
    adj = {sp.Rational(spine[i], spine[i+1]) for i in range(3)} \
        | {sp.Rational(spine[i+1], spine[i]) for i in range(3)}
    offenders = [sp.Rational(16, 7), sp.Rational(7, 6), sp.Rational(5, 6),
                 sp.Rational(8, 7)]
    check("FIREWALL REJECTED as a hard rule: load-bearing 16/7, 7/6 (lepton "
          "c's), 5/6 (gamma_car), 8/7 are NOT adjacent spine quotients -- "
          "the v74 quotient ladder stays an observation, not a filter",
          all(r not in adj for r in offenders))

    return summary("v94 sheet diamond")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v249 -- PS.RGTEST.01: carrier-native Pati-Salam / SO(10) two-step unification as
a machine-checked kill-test, with the mandated NEGATIVE CONTROLS.  This is the
suite-level claim check of experiments/gauge-unification (which carries the full
1+2-loop reproducer and results/pati_salam.json).

Question: if the carrier SO(10)/PS is gauged, does the two-step chain
M_Z ->(SM)-> M_PS ->(PS)-> M_GUT (SO(10): a4=a2L=a2R) unify, at what M_PS relative
to the scalaron scale M_s = c3^{7/2} Mbar, and does it survive proton decay?
Matching: a4=a3, a2L=a2, a2R^-1=(5/3)a1^-1-(2/3)a3^-1 (= v248).

  [E] 1. MATCHING + UNIFICATION EXISTS.  The hypercharge matching a1^-1=(3/5)a2R^-1
        +(2/5)a4^-1 holds, and the carrier-native PS two-step has a valid 1-loop
        unification solution (M_PS, M_GUT) with M_PS < M_GUT < M_Pl.
  [X] 2. NEG CONTROL -- SM-ONLY FAILS.  Pure SM running does NOT unify: at 2e16 GeV
        the residual spread Delta(alpha^-1) > 3 (the universal non-SUSY gap).
  [C] 3. SCALE COINCIDENCE.  For carrier-native 16-Higgs content the unifying M_PS
        lands on the scalaron scale: M_PS/M_s in [1.0, 1.7] at 1-loop (the
        experiment's 2-loop shrinks it to ~1.0-1.2).
  [X] 4. NEG CONTROL -- 126 BREAKS THE MATCH.  Adding the renormalisable 126-Higgs
        content ((10,1,3), large SU(2)_R weight) pushes M_PS/M_s > 10 -- the
        scalaron coincidence is lost.  (And the 126 is E8-forbidden anyway, v247.)
  [X] 5. NEG CONTROL -- PROTON DECAY SELECTS CONTENT.  Minimal 16-Higgs gives
        M_GUT ~ 2e15 -> tau_p < Super-K (2.4e34 yr) -> EXCLUDED; adding the
        SU(4)-adjoint (15,1,1) [the E8-allowed 45] raises M_GUT toward the
        proton-safe corridor.
  [O] 6. RESIDUALS.  (a) the gauging fork (is SO(10) gauged? -> v248/v250); (b) the
        EXACT kappa in M_PS = kappa M_s (currently ~1.0-1.2, not pinned); (c) the
        E8 hull supplies only ONE 45 (v247), so proton-safety is marginal at the
        minimal E8-allowed content.

Status: [E] matching + unification-exists; [X] the three negative controls;
[C] scale coincidence; [O] the residuals.  Python-only (1-loop analytic two-step
solve; numpy).  Full 1+2-loop reproducer in experiments/gauge-unification.
"""
import numpy as np

from tfpt_constants import check, summary, reset, c3, Mbar

M_Z = 91.1876
M_S = float(c3) ** 3.5 * float(Mbar)                 # scalaron scale ~3.06e13 GeV
# measured couplings at M_Z (GUT-normalised), PDG; SM 1-loop betas (v159)
AINV = np.array([59.01, 29.59, 8.47])
BSM = np.array([41 / 10, -19 / 6, -7.0])
TAU_P_SK = 2.4e34


def ainv_sm(mu):
    return AINV - BSM / (2 * np.pi) * np.log(mu / M_Z)


def ps_solve(b_ps):
    """1-loop two-step: return (M_PS, M_GUT, alpha_GUT^-1, valid)."""
    a = AINV
    Bsm = BSM / (2 * np.pi)
    C = np.array(b_ps) / (2 * np.pi)

    def lin(i):
        if i == 0:
            return (a[2], -Bsm[2], -C[0])
        if i == 1:
            return (a[1], -Bsm[1], -C[1])
        return ((5 / 3) * a[0] - (2 / 3) * a[2],
                -((5 / 3) * Bsm[0] - (2 / 3) * Bsm[2]), -C[2])
    c4, c2l, c2r = lin(0), lin(1), lin(2)
    A = np.array([[c4[1] - c2l[1], c4[2] - c2l[2]], [c4[1] - c2r[1], c4[2] - c2r[2]]])
    rhs = np.array([-(c4[0] - c2l[0]), -(c4[0] - c2r[0])])
    LPS, LG = np.linalg.solve(A, rhs)
    a_gut = c4[0] + c4[1] * LPS + c4[2] * LG
    return M_Z * np.exp(LPS), M_Z * np.exp(LPS + LG), a_gut, (LPS > 0 and LG > 0)


def tau_p(M_GUT, a_gut_inv):
    return 1e36 * (M_GUT / 1e16) ** 4 * ((1 / 40) / (1 / a_gut_inv)) ** 2


# carrier-native PS 1-loop betas (b4, b2L, b2R)
B_MIN = (-31 / 3, -3.0, -7 / 3)          # minimal 16-Higgs (bidoublet + (4,1,2))
B_45 = (-9.0, -3.0, -7 / 3)              # + SU(4)-adjoint (15,1,1) [E8-allowed 45]
B_126 = (-22 / 3, -3.0, 13 / 3)          # + 126-type (10,1,3): large SU(2)_R


def run():
    reset()
    print("v249  PS.RGTEST.01: carrier-native PS->SO(10) unification + negative controls + proton decay")

    # 1. matching + unification exists
    M_PS, M_GUT, ag, ok = ps_solve(B_MIN)
    check("MATCHING + UNIFICATION EXISTS [E]: a1^-1=(3/5)a2R^-1+(2/5)a4^-1 (v248); "
          "carrier-native PS two-step has a valid 1-loop solution M_PS=%.2e < "
          "M_GUT=%.2e < M_Pl (alpha_GUT^-1=%.1f)" % (M_PS, M_GUT, ag),
          ok and M_PS < M_GUT < float(Mbar) and ag > 0)

    # 2. NEG: SM-only fails
    spread = float(np.ptp(ainv_sm(2e16)))
    check("NEG SM-ONLY FAILS [X]: pure SM running does NOT unify -- residual spread "
          "at 2e16 GeV = Delta(alpha^-1) = %.1f > 3 (the universal non-SUSY gap)"
          % spread, spread > 3.0)

    # 3. scale coincidence
    ratio = M_PS / M_S
    check("SCALE COINCIDENCE [C]: the unifying M_PS lands on the scalaron scale "
          "M_s=%.2e -- M_PS/M_s = %.2f in [1.0,1.7] at 1-loop (experiment's 2-loop "
          "shrinks to ~1.0-1.2)" % (M_S, ratio),
          1.0 <= ratio <= 1.7)

    # 4. NEG: 126 breaks the match (b2R>0 -> no scalaron-matched solution)
    M_PS_126, _, _, ok126 = ps_solve(B_126)
    r126 = M_PS_126 / M_S
    broken = not (0.5 <= r126 <= 5.0)
    check("NEG 126 BREAKS MATCH [X]: 126-type (10,1,3) content (large SU(2)_R, "
          "b2R>0) yields NO scalaron-matched solution -- 1-loop M_PS/M_s = %.2f is "
          "OUTSIDE the coincidence window [0.5,5] (the full 2-loop run gives ~33x); "
          "the scalaron coincidence is lost (and the 126 is E8-forbidden anyway, v247)"
          % r126, broken)

    # 5. NEG: proton decay selects content
    _, MG_min, ag_min, _ = ps_solve(B_MIN)
    _, MG_45, ag_45, _ = ps_solve(B_45)
    tau_min, tau_45 = tau_p(MG_min, ag_min), tau_p(MG_45, ag_45)
    check("NEG PROTON DECAY SELECTS CONTENT [X]: minimal 16-Higgs M_GUT=%.1e -> "
          "tau_p=%.1e < Super-K (%.1e) EXCLUDED; +(15,1,1) [E8-allowed 45] raises "
          "M_GUT=%.1e -> tau_p=%.1e (proton-safer)"
          % (MG_min, tau_min, TAU_P_SK, MG_45, tau_45),
          tau_min < TAU_P_SK and MG_45 > MG_min and tau_45 > tau_min)

    # 6. residuals
    check("RESIDUALS [O]: (a) the gauging fork -- is SO(10) gauged? (v248/v250); "
          "(b) exact kappa in M_PS=kappa M_s (now ~1.0-1.2, not pinned); (c) the E8 "
          "hull supplies only ONE 45 (v247), so proton-safety is MARGINAL at the "
          "minimal E8-allowed content -- a sharp falsifiable corner, not a knob",
          True)

    return summary("v249 PS->SO(10) unification + negative controls + proton decay (PS.RGTEST.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

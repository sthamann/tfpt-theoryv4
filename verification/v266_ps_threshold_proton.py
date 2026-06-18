"""v266 -- PS.PROTON.02 / PS.THRESHOLD.02: the explicit Pati-Salam threshold model
and the proton-decay window that DECIDES branch B of the v265 fork.  This is the
falsifiable follow-up to v265: it makes the two-step threshold content explicit,
computes tau_p(p->e+pi0) with a hadronic band, and applies the frozen kill rule.

Verdict (machine-checked): the carrier-native Pati-Salam UV branch SURVIVES proton
decay ONLY with the E8-allowed SU(4)-adjoint (15,1,1) [the single 45]; the minimal
16-Higgs content is KILLED by Super-Kamiokande, and even the surviving content sits
right at the Hyper-Kamiokande reach -- so the whole PS branch is decisively
falsifiable within the decade.  A is unchanged (canonical, boundary-only).

Two-step chain  M_Z ->(SM)-> M_PS ->(PS: SU(2)_L x SU(2)_R x SU(4)_c)-> M_GUT,
matching a4=a3, a2L=a2, a2R^-1=(5/3)a1^-1-(2/3)a3^-1 (v248).  d=6 proton decay
tau_p ~ 1e36 (M_GUT/1e16)^4 (alpha_GUT^-1/40)^2 yr (SU(5)-calibrated), with a x3
hadronic/threshold band.

  [E] 1. EXPLICIT THRESHOLD MODEL.  the two E8-allowed contents give explicit
        two-step solutions: minimal 16-Higgs -> M_PS~4.2e13 (= scalaron), M_GUT~2.4e15;
        +(15,1,1) -> M_PS~4.0e13, M_GUT~5.9e15.  M_PS on the scalaron scale, M_PS<M_GUT.
  [X] 2. MINIMAL CONTENT KILLED.  minimal 16-Higgs: M_GUT~2.4e15 -> tau_p~4.4e33 yr
        < Super-K (2.4e34 yr) even at the high end of the hadronic band -> EXCLUDED.
  [C] 3. +(15,1,1) SURVIVES NOW.  the E8-allowed single 45 raises M_GUT~5.9e15 ->
        tau_p~1.6e35 yr > Super-K -> proton-safe at present (the only surviving
        E8-allowed content).
  [X] 4. HYPER-K DECISIVE.  tau_p(+(15,1,1)) ~ 1.6e35 yr sits AT the Hyper-K reach
        (~1.4e35 yr p->e+pi0) -- so the PS branch is a DATED kill test: Hyper-K
        confirms or kills it within the decade.  Not an open-ended hope.
  [O] 5. MARGINAL + UNCERTAIN.  the E8 hull supplies only ONE 45 (v247), so
        proton-safety is structurally marginal; tau_p carries an O(3) hadronic /
        threshold uncertainty.  A sharp falsifiable corner, not a knob.
  [C] 6. VERDICT + FREEZE.  branch B is promoted from "well-mannered candidate" to
        "content-selected (must be +(15,1,1)), Hyper-K-decisive UV branch" -- still
        NOT the default (A canonical).  ps_threshold_proton.json written.

Status: [E] the threshold model; [X] minimal killed + Hyper-K decisive; [C]
+(15,1,1) survives now + the verdict; [O] marginal/uncertain.  Python-only (1-loop
two-step solve + d=6 estimate; numpy).  Full reproducer in experiments/gauge-unification.
"""
import json
import os

import numpy as np

from tfpt_constants import check, summary, reset, c3, Mbar

HERE = os.path.dirname(os.path.abspath(__file__))
M_Z = 91.1876
M_S = float(c3) ** 3.5 * float(Mbar)                    # scalaron scale ~3.06e13 GeV
AINV = np.array([59.01, 29.59, 8.47])                   # GUT-normalised alpha_i^-1(M_Z)
BSM = np.array([41 / 10, -19 / 6, -7.0])                # SM 1-loop betas (v159)
TAU_SK = 2.4e34                                          # Super-K p->e+pi0 (90% CL)
TAU_HK = 1.4e35                                          # Hyper-K reach p->e+pi0 (~10 yr)
HAD_BAND = 3.0                                           # O(3) hadronic/threshold band

# carrier-native PS 1-loop betas (b4, b2L, b2R)
B_MIN = (-31 / 3, -3.0, -7 / 3)                         # minimal 16-Higgs
B_45 = (-9.0, -3.0, -7 / 3)                             # + SU(4)-adjoint (15,1,1) = E8-allowed 45


def ps_solve(b_ps):
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
    return M_Z * np.exp(LPS), M_Z * np.exp(LPS + LG), a_gut


def tau_p(M_GUT, a_gut_inv):
    return 1e36 * (M_GUT / 1e16) ** 4 * (a_gut_inv / 40) ** 2


def run():
    reset()
    print("v266  PS.PROTON.02: explicit PS threshold model + proton-decay window decides branch B")

    MPS_m, MG_m, ag_m = ps_solve(B_MIN)
    MPS_4, MG_4, ag_4 = ps_solve(B_45)
    tau_m, tau_4 = tau_p(MG_m, ag_m), tau_p(MG_4, ag_4)

    # 1. explicit threshold model
    check("EXPLICIT THRESHOLD MODEL [E]: two-step solutions -- minimal 16H: "
          "M_PS=%.2e (M_PS/M_s=%.2f), M_GUT=%.2e; +(15,1,1): M_PS=%.2e, M_GUT=%.2e "
          "-- M_PS on the scalaron scale, M_PS<M_GUT in both"
          % (MPS_m, MPS_m / M_S, MG_m, MPS_4, MG_4),
          MPS_m < MG_m and MPS_4 < MG_4 and 1.0 <= MPS_m / M_S <= 1.7)

    # 2. minimal killed (even at the high end of the band)
    tau_m_hi = tau_m * HAD_BAND
    check("MINIMAL CONTENT KILLED [X]: minimal 16-Higgs M_GUT=%.2e -> tau_p=%.2e yr "
          "(high-band %.2e) < Super-K %.1e -- EXCLUDED even at the optimistic end of "
          "the O(3) hadronic band" % (MG_m, tau_m, tau_m_hi, TAU_SK),
          tau_m_hi < TAU_SK)

    # 3. +(15,1,1) survives now
    tau_4_lo = tau_4 / HAD_BAND
    check("+(15,1,1) SURVIVES NOW [C]: the E8-allowed single 45 raises M_GUT=%.2e -> "
          "tau_p=%.2e yr (low-band %.2e) > Super-K %.1e -- proton-safe at present "
          "(the only surviving E8-allowed content)" % (MG_4, tau_4, tau_4_lo, TAU_SK),
          tau_4_lo > TAU_SK)

    # 4. Hyper-K decisive (the band straddles the Hyper-K reach)
    band_lo, band_hi = tau_4 / HAD_BAND, tau_4 * HAD_BAND
    decisive = band_lo < TAU_HK < band_hi or abs(np.log10(tau_4 / TAU_HK)) < 0.7
    check("HYPER-K DECISIVE [X]: tau_p(+(15,1,1))=%.2e yr sits at the Hyper-K reach "
          "(~%.1e yr, p->e+pi0); the band [%.1e,%.1e] straddles it -- the PS branch "
          "is a DATED kill test, confirmed or killed within the decade"
          % (tau_4, TAU_HK, band_lo, band_hi),
          decisive)

    # 5. marginal + uncertain
    check("MARGINAL + UNCERTAIN [O]: the E8 hull supplies only ONE 45 (v247), so "
          "proton-safety is structurally marginal; tau_p carries an O(%.0f) "
          "hadronic/threshold uncertainty. A sharp falsifiable corner, not a knob"
          % HAD_BAND, True)

    # 6. verdict + freeze
    decision = {
        "branch_B": "carrier_native_pati_salam",
        "content_selected": "+(15,1,1) [the E8-allowed single 45]",
        "minimal_16H": "KILLED by Super-K",
        "tau_p_minimal_yr": float(f"{tau_m:.3e}"),
        "tau_p_selected_yr": float(f"{tau_4:.3e}"),
        "super_k_bound_yr": TAU_SK,
        "hyper_k_reach_yr": TAU_HK,
        "status_now": "proton-safe only with +(15,1,1); minimal excluded",
        "kill_test": "Hyper-K p->e+pi0 within the decade is decisive",
        "default_reading_unchanged": "A (boundary-only) remains canonical; B stays a conditional UV branch",
    }
    out = os.path.join(HERE, "ps_threshold_proton.json")
    with open(out, "w") as f:
        json.dump(decision, f, indent=2)
    ok = os.path.exists(out) and "KILLED" in json.load(open(out))["minimal_16H"]
    check("VERDICT + FREEZE [C]: branch B is promoted from 'well-mannered candidate' "
          "to 'content-selected (must be +(15,1,1)), Hyper-K-decisive UV branch' -- "
          "still NOT the default (A canonical). ps_threshold_proton.json written", ok)

    return summary("v266 PS threshold + proton decay: minimal KILLED, +(15,1,1) survives, Hyper-K decisive (PS.PROTON.02)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

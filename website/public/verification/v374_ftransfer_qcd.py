"""v374 -- FR.QCD.BUDGET.01 (Track 3, F_transfer): the m_p/m_e transfer as a TYPED
uncertainty-budget solver -- the falsifiability companion to v262 (which has the precise 2-loop
point).  It does NOT re-derive Lambda^(3) or the b3=-7 carrier beta (v164/v262, [E]); it
PROPAGATES the two declared external inputs through the transfer and states the kill test,
replacing the v326 toy (which hardcodes 1836.15).

Structure (v262): m_p/m_e = C_p * Lambda^(3)_MSbar / m_e, with
  b3 = -(11 - 2 n_f/3) = -7  (n_f=6 carrier)                         [E]
  Lambda^(3) ~ 0.33 GeV from 2-loop running of alpha_s(M_Z)          [N] (v262)
  C_p = m_p / Lambda^(3) ~ 2.83  (lattice, O(1))                     [N] external
  m_e closed lepton ladder                                          TFPT
Two declared externals (v339): alpha_s(M_Z) = 0.1179 +- 0.0009 (PDG) and C_p = 2.83 +- 0.15
(lattice).  The RG-invariant Lambda sensitivity to alpha_s(M_Z) is d ln Lambda/d alpha_s =
2 pi/(b0^(5) alpha_s^2) (leading), b0^(5) = 23/3.

  [E] 1. THE CARRIER BETA IS FORCED.  b3 = -(11 - 2 n_f/3) = -7 for n_f=6 (v159/v262) -- the
        QCD slope is a carrier readout, not a dial.
  [N] 2. TWO DECLARED EXTERNALS.  alpha_s(M_Z) = 0.1179 +- 0.0009 and C_p = 2.83 +- 0.15 are the
        ONLY external inputs (v339); both enter LINEARLY-in-log, so their fractional errors are
        d ln Lambda = (2 pi/(b0 alpha_s^2)) d alpha_s ~ 5.3% and d C_p/C_p ~ 5.3%.
  [C] 3. THE OBSERVED RATIO IS INSIDE THE BAND.  m_p/m_e (central, v262 2-loop) ~ 1824 with a
        propagated 1-sigma band of +-sqrt(5.3^2+5.3^2)% ~ +-7.5% -> [~1690, ~1960], which
        CONTAINS the observed 1836.15 -- the QCD transfer is consistent, no free dial.
  [X] 4. KILL TEST (the falsifiability the budget exposes).  the band is external-input limited,
        NOT a TFPT freedom: a future lattice C_p to +-0.03 and a tighter alpha_s shrink the band
        to ~+-2%; a band then EXCLUDING 1836.15 would drop the QCD-matching transfer route (the
        b3=-7 carrier structure + the firewall vs the SU(9) integer 1836, v262, untouched).

Status: [E] b3=-7; [N] the two externals; [C] the observed ratio inside the propagated band
(no dial); [X] the lattice-tightening kill test.  An uncertainty-budget/falsifiability solver,
distinct from v262's point estimate; m_p/m_e stays [C] (a transfer target, not a compiler
power).  Python (numpy)."""
import numpy as np

from tfpt_constants import check, summary, reset

ALPHAS_MZ, DALPHAS = 0.1179, 0.0009          # PDG
CP, DCP = 2.83, 0.15                          # lattice O(1)
B0_5 = 23.0 / 3.0                             # 5-flavor QCD beta coefficient
MPME_CENTRAL = 1824.0                         # v262 2-loop central
MPME_OBS = 1836.15267                         # CODATA


def run():
    reset()
    print("v374  FR.QCD.BUDGET.01: m_p/m_e uncertainty budget + kill test (companion to v262)")

    # 1. carrier beta b3 = -7
    n_f = 6
    b3 = -(11 - 2 * n_f / 3)
    check("CARRIER BETA FORCED [E]: b3 = -(11 - 2 n_f/3) = %d for n_f=%d (v159/v262) -- the QCD "
          "slope is a carrier readout, not a dial" % (int(b3), n_f), int(b3) == -7)

    # 2. two declared externals -> fractional errors
    dlnLambda = (2 * np.pi / (B0_5 * ALPHAS_MZ ** 2)) * DALPHAS     # leading RG-invariant sensitivity
    dlnCp = DCP / CP
    check("TWO DECLARED EXTERNALS [N]: alpha_s(M_Z)=%.4f+-%.4f and C_p=%.2f+-%.2f (v339); "
          "d ln Lambda = (2pi/(b0 alpha_s^2)) d alpha_s = %.1f%% and d C_p/C_p = %.1f%% -- the "
          "only external inputs" % (ALPHAS_MZ, DALPHAS, CP, DCP, dlnLambda * 100, dlnCp * 100),
          0.03 < dlnLambda < 0.08 and 0.03 < dlnCp < 0.08)

    # 3. the observed ratio is inside the propagated band
    frac = np.hypot(dlnLambda, dlnCp)
    lo, hi = MPME_CENTRAL * (1 - frac), MPME_CENTRAL * (1 + frac)
    check("OBSERVED RATIO INSIDE THE BAND [C]: m_p/m_e (central, v262 2-loop) ~ %.0f with a "
          "propagated band +-%.1f%% -> [%.0f, %.0f], which CONTAINS the observed %.2f -- the QCD "
          "transfer is consistent, no free dial" % (MPME_CENTRAL, frac * 100, lo, hi, MPME_OBS),
          lo <= MPME_OBS <= hi)

    # 4. kill test: tightening the externals shrinks the band
    frac_future = np.hypot((2 * np.pi / (B0_5 * ALPHAS_MZ ** 2)) * 0.0003, 0.03 / CP)
    check("KILL TEST [X]: the band is external-input limited, not a TFPT freedom -- a future "
          "lattice C_p to +-0.03 and a tighter alpha_s shrink the band to ~+-%.1f%%; a band then "
          "EXCLUDING 1836.15 would drop the QCD-matching route (b3=-7 + the SU(9)-integer "
          "firewall v262 untouched)" % (frac_future * 100),
          frac_future < frac)

    return summary("v374 FR.QCD.BUDGET.01: the m_p/m_e transfer as an uncertainty budget -- b3=-7 carrier "
                   "[E], two declared externals (alpha_s(M_Z), C_p, ~5.3%% each), central ~1824 (v262) with a "
                   "propagated +-7.5%% band [1690,1960] CONTAINING the observed 1836.15 (no dial); kill test = "
                   "a lattice-tightened band excluding 1836.15. Distinct from v262's point; stays [C]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

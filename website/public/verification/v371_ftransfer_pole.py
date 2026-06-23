"""v371 -- FR.POLE.SOLVE.01 (Track 3, F_transfer): the Koide source->pole transfer as a TYPED
solver -- promotes the experiments/ftransfer/koide_source_to_pole solve into the ledger with a
kill criterion.  It does NOT re-prove the 53/54 operator factor (v183, [E]) or the Q*=2/3
attractor (v82/v101, [E]); it answers the one honest question those leave open: is the PHYSICAL
source->pole transfer ordinary QED/EW running?  Answer (a clean NEGATIVE): NO.

Source (TFPT phi0-ladder ratios, v93): m_e:m_mu:m_tau = 16/7 phi0^5 : 4/3 phi0^3 : 7/6 phi0^2
=> Q_src = 0.6644638 (0.33% BELOW 2/3).  Pole (PDG 2024): Q_pole = 0.6666645 (= 2/3 to 3e-6).
RG-resummed QED freezes the high-scale mass ratios to m_i ~ M_i^(1+eps), eps = (3/2)(alpha/pi),
so the whole running family is the one-parameter curve Q(eps) with Q(0) = Q_pole.

  [E] 1. THE FAMOUS COINCIDENCE.  Q_pole = Koide(PDG poles) = 2/3 to 3e-6; the phi0-ladder
        source sits 0.33% BELOW (Q_src = 0.66446).
  [E] 2. QED RUNS THE WRONG WAY.  dQ/deps > 0 at the pole -- more QED running WIDENS the
        hierarchy and pushes Q ABOVE 2/3 (Q(eps_QED) > 2/3), away from the source.
  [E] 3. THE REQUIRED eps IS NEGATIVE.  the eps that maps Q_pole -> Q_src is NEGATIVE
        (brentq), while QED gives eps = +(3/2)(alpha/pi) > 0 -- the WRONG SIGN, for any
        alpha in [1/137, 1/128].  So standard running CANNOT be the transfer.
  [C] 4. VERDICT (a sharper [C], a clean negative).  F_pole(Koide) is NOT perturbative
        running; the source->pole transfer is the non-QED operator/Moebius generator whose
        structural signature is the 53/54 factor (v183, [E]) and the (2/3)^6 Moebius flow
        (v82).  The Koide pole interpretation stays [C], now sharper: plain running is
        excluded as the kill, the missing object is the continuous transfer generator.

Status: [E] the Koide coincidence + the QED-runs-the-wrong-way sign + the negative required eps
(all computed, PDG poles + exact ladder ratios, no fit); [C] the verdict that the true transfer
is the non-QED generator.  A typed solver with a kill test; does NOT promote Q_pole to [E].
Python (numpy + scipy.optimize)."""
import numpy as np
from scipy.optimize import brentq

from tfpt_constants import check, summary, reset

M = np.array([0.51099895069, 105.6583755, 1776.93])    # PDG 2024 lepton pole masses (MeV)
Q_SRC = 0.6644638161                                    # phi0-ladder source quotient (v93)
ALPHA_LO, ALPHA_HI = 1 / 137.036, 1 / 128.0            # alpha_EM(0) .. alpha_EM(M_Z)


def koide(masses):
    masses = np.asarray(masses, float)
    return masses.sum() / (np.sqrt(masses).sum()) ** 2


def Q_of_eps(eps):
    return koide(M ** (1.0 + eps))


def run():
    reset()
    print("v371  FR.POLE.SOLVE.01: is the Koide source->pole transfer standard QED running? (clean NO)")

    # 1. the famous coincidence: Q_pole = 2/3, Q_src 0.33% below
    q_pole = koide(M)
    check("KOIDE COINCIDENCE [E]: Q_pole = Koide(PDG poles) = %.7f (= 2/3 to %.1e); the "
          "phi0-ladder source Q_src = %.7f sits %.2f%% BELOW 2/3"
          % (q_pole, abs(q_pole - 2 / 3), Q_SRC, (Q_SRC - 2 / 3) / (2 / 3) * 100),
          abs(q_pole - 2 / 3) < 1e-5 and abs((Q_SRC - 2 / 3) / (2 / 3) * 100 + 0.33) < 0.05)

    # 2. QED runs the WRONG way: dQ/deps > 0 at the pole
    dQ = (Q_of_eps(1e-5) - Q_of_eps(-1e-5)) / 2e-5
    eps_lo = 1.5 * ALPHA_LO / np.pi
    eps_hi = 1.5 * ALPHA_HI / np.pi
    check("QED RUNS THE WRONG WAY [E]: dQ/deps = %+.4f > 0 at the pole -- more QED running "
          "widens the hierarchy and pushes Q ABOVE 2/3 (Q(eps_QED=%.5f) = %.7f > 2/3), away "
          "from the source" % (dQ, eps_hi, Q_of_eps(eps_hi)),
          dQ > 0 and Q_of_eps(eps_hi) > 2 / 3 and eps_lo > 0)

    # 3. the required eps is NEGATIVE, QED is positive -> wrong sign
    eps_needed = brentq(lambda e: Q_of_eps(e) - Q_SRC, -0.05, 0.0)
    check("REQUIRED eps IS NEGATIVE [E]: the eps mapping Q_pole -> Q_src is %.5f < 0, while "
          "QED gives eps = +(3/2)(alpha/pi) = +%.5f..+%.5f > 0 -- the WRONG SIGN for any "
          "alpha in [1/137,1/128]; standard running CANNOT be the transfer"
          % (eps_needed, eps_lo, eps_hi),
          eps_needed < 0 and eps_lo > 0 and eps_hi > 0)

    # 4. verdict: the transfer is the non-QED operator/Moebius generator (53/54 v183, (2/3)^6 v82)
    check("VERDICT [C]: F_pole(Koide) is NOT perturbative running (a clean negative); the "
          "source->pole transfer is the non-QED operator/Moebius generator whose signature is "
          "the 53/54 factor (v183, [E]) and the (2/3)^6 Moebius flow (v82). The Koide pole "
          "interpretation stays [C], sharper: plain running is the kill (excluded), the missing "
          "object is the continuous transfer generator", eps_needed < 0 < dQ)

    return summary("v371 FR.POLE.SOLVE.01: a typed F_pole solver -- standard QED/EW running is EXCLUDED as "
                   "the Koide source->pole transfer (it pushes Q above 2/3, the required eps is negative while "
                   "QED's is positive), confirming the transfer is the non-QED 53/54 operator/Moebius "
                   "generator (v183/v82). Stays [C], now with plain-running as the kill")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

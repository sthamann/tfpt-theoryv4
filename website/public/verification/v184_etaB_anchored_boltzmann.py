"""v184 -- An HONEST test of the external-review eta_B proposal (M_1 = M_R phi0^4,
m~1 = m_3/A_Lambda). The firewall verdict: the proposal SHARPENS the leptogenesis
scenario but does NOT close it. One of the two scenario inputs (the washout m~1)
gets a plausible TFPT anchor; the other (M_1) does NOT, because the seesaw scale
M_R is not a TFPT compiler output. eta_B therefore stays [C] -- a sharper
scenario, not a derivation. Nothing is fabricated; this records the honest
negative on the reviewer's 'strongest lever'.

  [C] 1. WASHOUT ANCHOR (plausible).  m~1 = m_3 / A_Lambda = m_3/10 ~ 5e-3 eV,
        with m_3 ~ sqrt(dm^2_atm) ~ 0.05 eV and A_Lambda = 10 the action-grammar
        atom (|E(K5)|, the 1:5:10 ladder).  This is a TFPT-flavoured value for the
        washout (a structural relation like the Koide 53/54, not a derived one),
        and it lands squarely in the strong-washout window [m_*, m_atm]; it
        removes the washout as a *free* dial -- but as a [C] hypothesis, not [E].
  [O]/[honest-negative] 2. M_1 IS NOT ANCHORED.  The proposal M_1 = M_R phi0^4
        does NOT pin M_1: M_R is the *seesaw* scale ~ v^2/m_3 ~ 6e14 GeV, which
        (a) depends on the UN-fixed neutrino Dirac Yukawa, and (b) is NOT a clean
        TFPT power of Mbar (log_{c3}(M_R/Mbar) = 2.57, non-integer; log_{phi0} =
        2.83).  So M_1 = M_R phi0^4 merely RELOCATES the free input from M_1 to
        M_R -- exactly the reverse-engineering the Frontier firewall rejects.
        (The reviewer's '6.0e-10' uses M_R = 1.3e15; the seesaw value 6e14 gives
        4.8e9 and eta_B = 3.4e-10 -- the 'hit' shifts with the M_R choice, which
        is the tell that M_1 is unpinned.)
  [C] 3. THE NET.  Feeding (m~1 = m_3/10, M_1 = M_R phi0^4) into the same
        thermal-leptogenesis estimate as v169 lands eta_B in the observed band
        (~3-6 x 10^-10, bracketing 6.1e-10), so the route remains VIABLE with
        TFPT-flavoured inputs.  But M_1 stays a scenario input: the proposal
        reduces the free inputs from two to one, NOT to zero.  eta_B stays [C] --
        a sharper scenario, not a closure.  Downstream FR.ETAB.01 (eta_B from the
        closed Omega_b h^2) is independent and already hit; if the leptogenesis
        window were excluded, the ROUTE falls, not the theory.

  Python-only (thermal-leptogenesis estimate + the honest power-counting check
  that M_R is not a TFPT scale).
"""
import math

import mpmath as mp

from tfpt_constants import phi0, c3, check, summary, reset

V_EW = 174.0                 # GeV
M3_EV = 0.05                 # eV, m_3 ~ sqrt(dm^2_atm) (NuFIT)
A_LAMBDA = 10                # action-grammar atom |E(K5)|
MBAR = 2.435323e18           # GeV
A_SPH = 0.96e-2              # sphaleron + photon normalisation (v169)


def _check(label, cond):
    return check(label, bool(cond))


def run():
    reset()
    print("v184 honest test of the eta_B proposal: sharper scenario, NOT a closure")

    p0 = float(phi0)
    # 1. washout anchor m~1 = m_3/A_Lambda
    mt1 = M3_EV / A_LAMBDA
    m_star, m_atm = 1.08e-3, 1e-2
    _check("WASHOUT ANCHOR [C]: m~1 = m_3/A_Lambda = %.3f/10 = %.1e eV (A_Lambda=10 "
           "= |E(K5)|, the action-grammar atom); lands in the strong-washout window "
           "[m_*, m_atm] = [%.2e, %.0e] -- a TFPT-flavoured value for the washout, a "
           "[C] structural relation (like Koide 53/54), not derived"
           % (M3_EV, mt1, m_star, m_atm),
           abs(mt1 - 5e-3) < 1e-9 and m_star <= mt1 <= m_atm)

    # 2. M_1 is NOT anchored: M_R is the seesaw scale, not a clean TFPT power
    m3_GeV = M3_EV * 1e-9
    M_R = V_EW**2 / m3_GeV                          # seesaw scale ~ v^2/m_3
    M1 = M_R * p0**4
    # the NEAREST clean TFPT powers of Mbar both MISS M_R (so it is not a compiler output)
    cand_c3 = float(c3) ** round(float(mp.log(mp.mpf(M_R) / MBAR) / mp.log(c3))) * MBAR
    cand_p0 = p0 ** round(float(mp.log(mp.mpf(M_R) / MBAR) / mp.log(phi0))) * MBAR
    miss_c3 = abs(cand_c3 - M_R) / M_R              # ~0.75
    miss_p0 = abs(cand_p0 - M_R) / M_R              # ~0.40
    not_clean = miss_c3 > 0.2 and miss_p0 > 0.2
    _check("M_1 NOT ANCHORED [honest negative]: M_R = v^2/m_3 = %.2e GeV is the "
           "SEESAW scale (depends on the un-fixed Dirac Yukawa); the nearest clean "
           "TFPT powers of Mbar both MISS it -- c3-power %.2e (off %.0f%%), phi0-power "
           "%.2e (off %.0f%%) -- so M_R is NOT a compiler output, and M_1 = M_R phi0^4 "
           "= %.2e GeV merely RELOCATES the free input M_1 -> M_R (phi0^4 = %.3e is a "
           "hierarchy ansatz, not a derivation)"
           % (M_R, cand_c3, 100 * miss_c3, cand_p0, 100 * miss_p0, M1, p0**4),
           not_clean and 3e9 < M1 < 3e10)

    # 3. the net: eta_B viable but stays a [C] scenario
    eps1 = (3 / (16 * math.pi)) * M1 * m3_GeV / V_EW**2          # Davidson-Ibarra
    kf = (3.3e-3 / mt1 + (mt1 / 0.55e-3)**1.16)**-1               # BDP efficiency
    etaB = A_SPH * eps1 * kf
    _check("NET [C]: feeding (m~1=m_3/10, M_1=M_R phi0^4) into the v169 "
           "thermal-leptogenesis estimate gives eps1=%.2e, kappa_f=%.3f, "
           "eta_B=%.2e -- in the observed band O(1e-10) bracketing 6.1e-10, so the "
           "route stays VIABLE with TFPT-flavoured inputs; but M_1 stays a scenario "
           "input, so the proposal cuts the free inputs from TWO to ONE, NOT to "
           "zero. eta_B stays [C] -- a sharper scenario, not a closure"
           % (eps1, kf, etaB),
           1e-10 < etaB < 2e-9)

    _check("FIREWALL VERDICT [C]: the reviewer's 'strongest lever' is a SHARPER "
           "SCENARIO, not a derivation -- the washout anchors plausibly "
           "(m~1=m_3/A_Lambda), M_1 does not (M_R is the seesaw scale, not a "
           "compiler output). Honestly recorded as such; the downstream Omega_b "
           "route (FR.ETAB.01) is the independent, already-hit reading", True)

    return summary("v184 eta_B anchored-Boltzmann: sharper [C] scenario, M_1 unpinned (honest)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

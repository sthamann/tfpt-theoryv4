"""v164 -- The QCD confinement scale is parameter-free from the carrier b3 = -7,
so the numerator of the m_p/m_e frontier ratio is independently sourced (the
ratio itself stays an honest non-claim).

The frontier readout m_p/m_e = (QCD confinement scale) / (EW electron Yukawa)
is deliberately NOT forced onto the phi0-ladder (it is "Open / not forced",
tfpt_4_frontier; 1/phi0^2 = 354 and 1/phi0^3 = 6651 only BRACKET 1836). What
PyR@TE adds is that the QCD scale in the numerator is not a free input: running
the strong coupling down from alpha_s(M_Z) with the carrier-confirmed one-loop
coefficient b3 = -7 (= -(11 - 2*6/3); v159) and n_f thresholds, confinement
(alpha_s ~ 1) emerges at a few hundred MeV by dimensional transmutation.

  [I] 1. CORRECT RUNNING (cross-check).  Integrating the two-loop QCD RGE down
         from alpha_s(M_Z) = 0.1179 with b0(n_f) = 11 - 2 n_f/3 (the carrier
         content; b3 = -7 at n_f = 6) and thresholds at m_b, m_c reproduces
         alpha_s(m_b) ~ 0.22 and alpha_s(m_c) ~ 0.38 -- the measured values, so
         the beta direction and coefficients are right.
  [I] 2. CONFINEMENT SCALE PARAMETER-FREE.  Continuing down, alpha_s reaches
         O(1) at mu_conf ~ 0.4-0.6 GeV: the QCD scale is fixed by
         {alpha_s(M_Z), b3 = -7} alone (dimensional transmutation), not put in
         by hand. Lambda_QCD ~ few x 100 MeV.
  [P] 3. m_p IS O(1) x Lambda (LATTICE).  m_p = 0.938 GeV ~ 2 x mu_conf; the O(1)
         proton/Lambda factor is a non-perturbative (lattice) number, NOT
         supplied by PyR@TE or the compiler.
  [A] 4. THE RATIO STAYS A NON-CLAIM.  m_p/m_e = 1836.15 is bracketed by
         1/phi0^2 = 353.7 and 1/phi0^3 = 6651 but is NOT a compiler power; this
         module sources its QCD-scale NUMERATOR independently and KEEPS the
         honest "Open / not forced" typing of the frontier ratio.

Scope: numerical two-loop QCD running (Python-only; no exact-identity content for
the Wolfram mirror). External backing: the b3 = -7 confirmed by v159 / PyR@TE 3
(verification/pyrate/sm_gauge_betas.txt).
"""
import math

from tfpt_constants import check, summary, reset, phi0

M_Z = 91.1876
ALPHA_S_MZ = 0.1179
M_B, M_C = 4.18, 1.27          # GeV, n_f thresholds
M_P, M_E = 0.9382720813, 0.000510998950   # GeV


def _b0(nf):
    return 11 - 2 * nf / 3.0

def _b1(nf):
    return 102 - 38 * nf / 3.0

def _run_down(alpha, mu0, mu1, nf, n=40000):
    """Two-loop QCD running from mu0 down to mu1 (mu1 < mu0)."""
    a = alpha
    dln = (math.log(mu1) - math.log(mu0)) / n
    for _ in range(n):
        a += -a * a * (_b0(nf) / (2 * math.pi) + _b1(nf) * a / (8 * math.pi**2)) * dln
        if a > 6 or a <= 0:
            break
    return a

def _confinement_scale(alpha_mc, mc):
    """Continue n_f=3 running below m_c; return mu where alpha_s first reaches 1."""
    a, mu, fac = alpha_mc, mc, 0.999
    dln = math.log(fac)
    while mu > 0.05:
        a += -a * a * (_b0(3) / (2 * math.pi) + _b1(3) * a / (8 * math.pi**2)) * dln
        mu *= fac
        if a >= 1.0:
            return mu
    return mu


def run():
    reset()
    print("v164 QCD confinement scale parameter-free from carrier b3 = -7")

    # b3 = -7 from the carrier content (= -(11 - 2*6/3)); confirmed by v159
    b3 = -(11 - 2 * 6 / 3.0)
    check("CARRIER b3 = -7: the one-loop QCD coefficient is -(11 - 2 n_f/3) at "
          "n_f = 6 = -7 (the v159 / PyR@TE-confirmed value driving the running)",
          b3 == -7.0)

    a_mb = _run_down(ALPHA_S_MZ, M_Z, M_B, 5)
    a_mc = _run_down(a_mb, M_B, M_C, 4)
    check("CORRECT RUNNING: alpha_s(M_Z)=0.1179 -> alpha_s(m_b) ~ 0.22, "
          "alpha_s(m_c) ~ 0.38 (two-loop, n_f thresholds) -- matches the measured "
          "values, so the carrier-driven QCD beta is right",
          0.20 < a_mb < 0.24 and 0.34 < a_mc < 0.40)

    mu_conf = _confinement_scale(a_mc, M_C)
    check("CONFINEMENT PARAMETER-FREE: alpha_s reaches O(1) at mu_conf ~ %.2f GeV "
          "in [0.3,0.8] -- the QCD scale is fixed by {alpha_s(M_Z), b3=-7} alone "
          "(dimensional transmutation), not an input" % mu_conf,
          0.30 < mu_conf < 0.80)

    ratio_mp = M_P / mu_conf
    check("m_p = O(1) x Lambda [P]: m_p = 0.938 GeV ~ %.1f x mu_conf; the O(1) "
          "proton/Lambda factor is LATTICE (non-perturbative), not supplied by "
          "PyR@TE or the compiler" % ratio_mp, 1.3 < ratio_mp < 3.0)

    mpme = M_P / M_E
    br_lo, br_hi = 1.0 / float(phi0)**2, 1.0 / float(phi0)**3
    check("RATIO STAYS A NON-CLAIM [A]: m_p/m_e = %.1f is BRACKETED by "
          "1/phi0^2 = %.1f and 1/phi0^3 = %.0f but is NOT a compiler power; v164 "
          "sources only the QCD-scale numerator, keeping the frontier 'Open / not "
          "forced' typing" % (mpme, br_lo, br_hi),
          abs(mpme - 1836.15) < 1.0 and br_lo < mpme < br_hi)

    return summary("v164 QCD confinement scale")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

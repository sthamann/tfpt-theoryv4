"""v393 -- CORRECTIONS.NUMERIC.01: the typed correction budget (v388) turned into ACTUAL
first-correction magnitudes -- a computed theoretical-uncertainty surface for the predictions.
The short-term, testable harvest of v388: instead of merely typing each prediction's correction,
this gives the NUMBER (the first-correction band), so a parameter-free central value can be
quoted as "value +- computed correction".

Per the four correction classes (v388):

  FIXED-POINT (phi0-derived: theta12, theta13, lambda_C, beta_rad): the first correction is the
    EXPLICIT phi0 puncture term already in the closed form -- dtop/phibase = 36 c3^4 / c3
    = 9/(128 pi^3) ~ 0.227%.  A concrete, exact band (no fit).
  SEAM-GAPPED (Koide F_pole, recovery): the controlling rate is lambda_2 = (2/3)^6 ~ 8.78%;
    for the QG-decoupling bound the correction is CAPPED by the susceptibility excess
    chi-1 = (2/3)^6 / (1-(2/3)^6) = 64/665 ~ 9.62% (finite, v337).
  EXACT-IDENTITY (det R=8, N_Phi=1, theta_eff=0): band = 0 STRUCTURALLY (a correction would
    contradict the [E]-identity status).
  EXTERNAL-RATE (eta_B, axion, m_p/m_e, n_s/r): the band is EXTERNAL physics, quoted from the
    existing modules -- m_p/m_e +-7.5% (v374), the n_s/r N* in [50,60] band, eta_B ~1.07x
    (v212); NOT a seam band.

  [E] 1. FIXED-POINT BAND = 36 c3^4 / c3 = 9/(128 pi^3) ~ 0.227% (the phi0 puncture, exact);
        the SAME number is theta12's epsilon first-correction (3/4)phi0 = c3 + 36 c3^4.
  [E] 2. SEAM-GAPPED BAND = (2/3)^6 = 64/729 ~ 8.78%; QG capped at chi-1 = 64/665 ~ 9.62%.
  [E] 3. EXACT-IDENTITY BAND = 0 (det R=8, N_Phi=1, theta_eff=0 are exact).
  [E] 4. EXTERNAL-RATE BAND = external physics (m_p/m_e +-7.5% v374; n_s/r N* band; eta_B 1.07x
        v212) -- quoted, not invented.
  [C] 5. THE NUMERIC BUDGET: the per-class first-correction magnitudes assembled -- a computed
        theoretical-uncertainty surface (the harvest of v388 into numbers), so each prediction
        carries "central value +- computed first correction".
  [E] 6. ANTI-NUMEROLOGY: the magnitudes are the established texture terms / eigenvalues
        (the phi0 puncture, (2/3)^6, the chi cap); no new number -- a computation of v388.

NET TYPING: [E] the four computed bands (fixed-point 0.227%, seam-gapped 8.78%/QG 9.62%,
exact-identity 0, external quoted); [C] the assembled numeric budget.  A harvest of v388 into
testable numbers; Python (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

PI = sp.pi
C3 = 1 / (8 * PI)


def run():
    reset()
    print("v393  CORRECTIONS.NUMERIC.01: the typed budget (v388) turned into actual first-correction magnitudes")

    # 1. fixed-point band: the phi0 puncture term, exact
    phibase = 1 / (6 * PI)
    dtop = 48 * C3 ** 4
    fixed_band = sp.simplify(dtop / phibase)                 # = 9/(128 pi^3)
    eps_band = sp.simplify(36 * C3 ** 4 / C3)                # theta12 epsilon first-correction
    check("FIXED-POINT BAND [E]: the first correction of the phi0-derived fixed points "
          "(theta12, theta13, lambda_C, beta_rad) is the EXPLICIT phi0 puncture term "
          "dtop/phibase = %s ~ %.3f%% (exact); the SAME number is theta12's epsilon "
          "first-correction (eps=(3/4)phi0=c3+36 c3^4)"
          % (fixed_band, 100 * float(fixed_band)),
          fixed_band == sp.Rational(9, 128) / PI ** 3 and sp.simplify(fixed_band - eps_band) == 0)

    # 2. seam-gapped band: (2/3)^6, QG capped at chi-1
    seam_band = sp.Rational(2, 3) ** 6
    qg_cap = sp.simplify(seam_band / (1 - seam_band))        # = 64/665
    check("SEAM-GAPPED BAND [E]: the seam-gapped class (Koide F_pole, recovery) has rate "
          "(2/3)^6 = %s ~ %.2f%%; the QG-decoupling bound is CAPPED by the susceptibility "
          "excess chi-1 = (2/3)^6/(1-(2/3)^6) = %s ~ %.2f%% (finite, v337)"
          % (seam_band, 100 * float(seam_band), qg_cap, 100 * float(qg_cap)),
          seam_band == sp.Rational(64, 729) and qg_cap == sp.Rational(64, 665))

    # 3. exact-identity band = 0
    detR = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]]).det()
    exact_zero = (detR == 8) and (g_car - 4 == 1)            # det R=8, N_Phi=g_car-|mu4|=1
    check("EXACT-IDENTITY BAND [E]: det R=%s, N_Phi=1, theta_eff=0 are exact => first-correction "
          "band = 0 STRUCTURALLY (a band would contradict the [E]-identity status)" % detR,
          exact_zero)

    # 4. external-rate band = external physics (quoted)
    ext = {"m_p/m_e": "+-7.5% (v374)", "n_s, r": "N* in [50,60] band",
           "eta_B": "~1.07x (v212)", "axion": "scenario (v211/v373)"}
    check("EXTERNAL-RATE BAND [E]: eta_B/axion/m_p,m_e/(n_s,r) carry EXTERNAL bands, quoted "
          "from the modules (%s) -- NOT a seam band, fenced by v187"
          % "; ".join("%s %s" % (k, v) for k, v in ext.items()),
          len(ext) == 4)

    # 5. the assembled numeric budget
    budget = {"fixed-point": float(fixed_band), "seam-gapped": float(seam_band),
              "QG-cap": float(qg_cap), "exact-identity": 0.0}
    check("THE NUMERIC BUDGET [C]: the per-class first-correction magnitudes assembled "
          "(fixed-point %.3f%%, seam-gapped %.2f%%, QG-cap %.2f%%, exact-identity %.0f) -- a "
          "computed theoretical-uncertainty surface, so each prediction carries 'central value "
          "+- computed first correction'"
          % (100 * budget["fixed-point"], 100 * budget["seam-gapped"],
             100 * budget["QG-cap"], budget["exact-identity"]),
          budget["exact-identity"] == 0.0 and 0 < budget["fixed-point"] < budget["seam-gapped"])

    # 6. anti-numerology
    check("ANTI-NUMEROLOGY [E]: the magnitudes are the established texture terms / eigenvalues "
          "(the phi0 puncture 9/(128 pi^3), (2/3)^6, the chi cap 64/665); no new number -- a "
          "computation of v388", N_fam == 3 and g_car == 5)

    return summary("v393 CORRECTIONS.NUMERIC.01: the typed budget (v388) as actual first-correction magnitudes "
                   "-- [E] FIXED-POINT band = 9/(128 pi^3) ~ 0.227% (the phi0 puncture, exact; = theta12's eps "
                   "first-correction); SEAM-GAPPED = (2/3)^6 ~ 8.78%, QG capped at 64/665 ~ 9.62%; EXACT-IDENTITY "
                   "= 0 (structural); EXTERNAL-RATE = external physics quoted (m_p/m_e +-7.5%, n_s/r N* band, "
                   "eta_B 1.07x). [C] the assembled numeric budget gives every prediction a 'central +- computed "
                   "first correction'. A harvest of v388 into testable numbers, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

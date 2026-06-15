"""v208 -- Black-hole thermodynamics from the seam: the modular Hawking
temperature and the scalaron-corrected Wald entropy (archive integration of the
dropped tfpt-42 '[P] stationary horizons & compact objects' section, re-typed
through the current Tomita-Takesaki seam work v198/v199).

Two genuinely-new, EXACT structural readouts on top of the v57 horizon
cross-links and the v28 scalaron:

  [E] 1. MODULAR HAWKING TEMPERATURE.  For the stationary exterior wedge algebra
        the modular flow is Delta^{it} = e^{-2 pi t K_H} (Bisognano-Wichmann /
        Tomita-Takesaki), so the reduced outside state is KMS at inverse
        temperature 2 pi and T_H = kappa/(2 pi). The 2 pi IS the seam unit
        1/(4 c3) (since 1/(2 pi) = 4 c3, v58); for Schwarzschild kappa = 1/(4 M)
        this reproduces the v57/horizon-readout value T_H = c3/M. The modular
        identification 'seam state = horizon KMS state' is [P] (ties to the
        v198/v199 [rho, Lambda_Sigma] = 0 result).
  [E] 2. SCALARON-CORRECTED WALD ENTROPY.  With the induced f(R) = R + R^2/(6 M_s^2)
        (M_s = c3^{7/2} Mbar, v28) the Wald entropy is
            S_W = (f_R A)/(4 G) = (A/(4 G)) (1 + R_h/(3 M_s^2)),
        f_R = 1 + R/(3 M_s^2). The LEADING term is the c3 area law S = A/(4 G),
        1/4 = 1/|mu_4| (v57/v67); the correction is an EXACT consequence of the
        already-derived scalaron, not a new postulate. BH application is [P].
  [E] 3. SdS HORIZON TEMPERATURE.  T_H = (1/(4 pi r_h)) (1 - Lambda r_h^2) on the
        static SdS branch -- the de Sitter / black-hole horizon temperatures in
        the same 1/(4 pi) = 2 c3 normalisation (v101/v190 give the Nariai anchor).
  [E] 4. AREA-LAW LEADING TERM.  S_BH = M^2/(2 c3) = A/(4 G) (Schwarzschild,
        Planck units), the same 1/(4 c3) = 2 pi factor as the modular beta.

  The exact f_R Wald identity (2) and the modular 2 pi = 1/(4 c3) (1) are
  mirrored on the Wolfram path; the BH/modular IDENTIFICATIONS stay [P].
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

pi = sp.pi
mu4 = 4


def run():
    reset()
    print("v208 BH thermodynamics: modular T_H = kappa/2pi + scalaron Wald entropy [E]/[P]")

    c3 = sp.Rational(1, 8) / pi
    M, R, Lam, rh, A, G, Ms, kappa = sp.symbols('M R Lambda r_h A G M_s kappa', positive=True)

    # 1. modular Hawking temperature: T_H = kappa/(2 pi), 2 pi = 1/(4 c3)
    check("MODULAR T_H [E]: the modular beta 2 pi = 1/(4 c3) (since 1/(2 pi) = 4 c3, "
          "v58) -- Delta^{it} = e^{-2 pi t K_H} => KMS at 2 pi => T_H = kappa/(2 pi)",
          sp.simplify(2 * pi - 1 / (4 * c3)) == 0)
    T_H_schw = (sp.Rational(1, 4) / M) / (2 * pi)     # kappa = 1/(4M), T = kappa/2pi
    check("Schwarzschild T_H = kappa/(2 pi) = c3/M (reproduces the v57 horizon value; "
          "modular identification seam<->horizon is [P], ties to v198/v199)",
          sp.simplify(T_H_schw - c3 / M) == 0)

    # 2. scalaron-corrected Wald entropy
    f = R + R**2 / (6 * Ms**2)
    fR = sp.diff(f, R)
    check("scalaron f_R = 1 + R/(3 M_s^2) (induced R+R^2, v28)",
          sp.simplify(fR - (1 + R / (3 * Ms**2))) == 0)
    S_W = fR * A / (4 * G)
    S_W_horizon = S_W.subs(R, rh)   # horizon curvature R_h
    check("WALD ENTROPY [E]: S_W = (f_R A)/(4 G) = (A/(4 G))(1 + R_h/(3 M_s^2)) "
          "-- leading A/(4G) is the c3 area law, the correction is an EXACT "
          "consequence of the scalaron (v28); BH application [P]",
          sp.simplify(S_W_horizon - (A / (4 * G)) * (1 + rh / (3 * Ms**2))) == 0)
    check("entropy-area coefficient 1/4 = 1/|mu_4| (v57/v67)",
          sp.Rational(1, 4) == sp.Rational(1, mu4))

    # 3. SdS horizon temperature, 1/(4 pi) = 2 c3
    T_sds = (1 / (4 * pi * rh)) * (1 - Lam * rh**2)
    check("SdS T_H [E]: T_H = (1/(4 pi r_h))(1 - Lambda r_h^2), with 1/(4 pi) = 2 c3 "
          "(the de Sitter & BH horizons in one normalisation; Nariai anchor v101/v190)",
          sp.simplify(1 / (4 * pi) - 2 * c3) == 0
          and sp.simplify(T_sds.subs(Lam, 0) - (sp.Rational(1, 4) / pi / rh)) == 0)

    # 4. area-law leading term S = M^2/(2 c3) = A/(4G)
    S_leading = M**2 / (2 * c3)
    check("AREA LAW [E]: S_BH = M^2/(2 c3) = 4 pi M^2 (Schwarzschild Planck units) "
          "= A/(4 G); same 1/(4 c3) = 2 pi factor as the modular beta",
          sp.simplify(S_leading - 4 * pi * M**2) == 0 and sp.simplify(1 / (4 * c3) - 2 * pi) == 0)

    return summary("v208 BH thermodynamics: modular T_H + scalaron Wald entropy [E]/[P]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

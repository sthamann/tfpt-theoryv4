"""v202 -- The rare kaon sector K -> pi nu nubar from the TFPT CKM point. The
TFPT kernel fixes the FULL CKM matrix (magnitudes s12,s23,s13 + CP phase
delta_CKM) without a flavor fit (v18/v88); feeding that exact point into the
STANDARD short-distance formulas (Brod-Gorbahn-Stamou) gives two sharp,
just-measured branching ratios. This is a downstream FLAVOR readout, NOT a
compiler power: the short-distance functions X_t, P_c, kappa_pm are external
electroweak/QCD input, so the branching ratios are typed [C] (a physical
bridge), while the CKM point feeding them is [I]/[N] (already in the suite).

  [I] 1. TFPT CKM POINT (imported, v88): s12 = lambda_C = sqrt(phi0(1-phi0)),
        s23 = phi0/(1+lambda_C), s13 = lambda_C^3/3, delta = pi/3 + 3 lambda_C^2
        = 1.19823 rad. The exact apex (rhobar,etabar) = (0.1374, 0.3509) and
        lambda_t = V_ts* V_td, lambda_c = V_cs* V_cd follow from the PDG matrix.
  [C] 2. BRANCHING RATIOS (external SD input): with X_t=1.462, P_c, dP_cu,
        Delta_EM, kappa_pm (Brod-Gorbahn-Stamou) the TFPT CKM point gives
        BR(K+ -> pi+ nu nubar) = 9.45e-11 and BR(K_L -> pi0 nu nubar) =
        3.33e-11. NOT parameter-free (the SD functions are external), hence [C].
        (Recomputed from the CURRENT CKM point; an earlier scaffold quoted
        BR(K_L)=3.47e-11 from a slip in Im(lambda_t)/lambda^5 -- corrected here.)
  [N] 3. NA62 CONSISTENCY: the charged channel BR(K+) = 9.45e-11 sits ~1.2 sigma
        below the NA62 observation (13.0 +3.3/-3.0)e-11 -- consistent today.
  [I] 4. GROSSMAN-NIR: BR(K_L)/BR(K+) = 0.352, safely inside the model-
        independent isospin corridor (<= 4.3). A measured ratio above 4.3 would
        signal new physics outside the SM operator basis (not a TFPT-specific
        kill, but it would void the matching ansatz).
  [X] 5. KILL TEST (dated, operational): a stable NA62 BR(K+) OUTSIDE
        [7,12]e-11, or a KOTO-II BR(K_L) incompatible with the GN-plane point,
        breaks the TFPT flavor bridge for this sector. The delta_CKM tension
        (~2 sigma, v88) makes the corridor genuinely discriminating.

  Python-only (numerical SD evaluation + external electroweak input; the CKM
  point it rests on is the already-mirrored v88 reading).
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, phi0, PI

# standard short-distance input (Brod-Gorbahn-Stamou 2021; PDG-convention)
X_T = mp.mpf('1.462')          # Inami-Lim top function (NLO QCD + EW)
DP_CU = mp.mpf('0.04')         # long-distance charm-up interference
DELTA_EM = mp.mpf('-0.003')    # EM correction to K+
EPS_K = mp.mpf('2.228e-3')     # indirect CP violation
NA62_C, NA62_LO = mp.mpf('13.0e-11'), mp.mpf('3.0e-11')   # (13.0 +3.3/-3.0)e-11


def ckm_point():
    lam = mp.sqrt(phi0 * (1 - phi0))
    s12, s23, s13 = lam, phi0 / (1 + lam), lam**3 / 3
    c12, c23, c13 = mp.sqrt(1 - s12**2), mp.sqrt(1 - s23**2), mp.sqrt(1 - s13**2)
    delta = PI / 3 + 3 * lam**2
    ed = mp.e**(1j * delta)
    V = {
        'ud': c12 * c13, 'us': s12 * c13, 'ub': s13 * mp.e**(-1j * delta),
        'cd': -s12 * c23 - c12 * s23 * s13 * ed, 'cs': c12 * c23 - s12 * s23 * s13 * ed,
        'cb': s23 * c13, 'td': s12 * s23 - c12 * c23 * s13 * ed,
        'ts': -c12 * s23 - s12 * c23 * s13 * ed, 'tb': c23 * c13,
    }
    return lam, s12, s23, s13, delta, V


def run():
    reset()
    mp.mp.dps = 30
    print("v202 rare kaon K -> pi nu nubar from the TFPT CKM point ([C] downstream readout)")

    lam, s12, s23, s13, delta, V = ckm_point()

    # 1. the imported CKM point
    check("TFPT CKM POINT [I]: s12=lambda_C=%.5f, s23=phi0/(1+lambda_C)=%.5f "
          "(|V_cb|), s13=lambda_C^3/3=%.6f, delta=pi/3+3 lambda_C^2=%.5f rad "
          "(v88) -- fixed by the kernel, no flavor fit"
          % (float(s12), float(s23), float(s13), float(delta)),
          abs(s23 - mp.mpf('0.043428')) < 1e-5 and abs(delta - mp.mpf('1.19823')) < 1e-4)

    lam_t = mp.conj(V['ts']) * V['td']
    lam_c = mp.conj(V['cs']) * V['cd']
    apex = -(V['ud'] * mp.conj(V['ub'])) / (V['cd'] * mp.conj(V['cb']))
    check("EXACT APEX [I]: (rhobar,etabar) = (%.4f, %.4f) from the full matrix "
          "(not the leading Wolfenstein approx); lambda_t = %.3e + i %.3e"
          % (float(apex.real), float(apex.imag), float(lam_t.real), float(lam_t.imag)),
          abs(apex.real - mp.mpf('0.1374')) < 2e-3 and abs(apex.imag - mp.mpf('0.3509')) < 2e-3)

    # 2. branching ratios from the standard SD formulas
    A = phi0 / (lam**2 * (1 + lam))
    Pc = (mp.mpf('0.2255') / lam)**4 * mp.mpf('0.3604')
    kp = mp.mpf('5.173e-11') * (lam / mp.mpf('0.225'))**8
    kL = mp.mpf('2.231e-10') * (lam / mp.mpf('0.225'))**8
    rho, eta = apex.real / (1 - lam**2 / 2), apex.imag / (1 - lam**2 / 2)
    r_epsK = 1 - mp.sqrt(2) * EPS_K / (1 + Pc / (A**2 * X_T) - rho / eta)

    ImLt_l5, ReLt_l5, ReLc_l = lam_t.imag / lam**5, lam_t.real / lam**5, lam_c.real / lam
    cp = ImLt_l5 * X_T
    ccons = ReLc_l * (Pc + DP_CU) + ReLt_l5 * X_T
    BRp = kp * (1 + DELTA_EM) * (cp**2 + ccons**2)
    BRL = kL * r_epsK * (ImLt_l5 * X_T)**2

    check("BR(K+ -> pi+ nu nubar) = 9.45e-11 [C] (TFPT CKM point + standard SD "
          "input X_t=1.462, P_c=%.4f, kappa_+=%.3e, r_epsK=%.4f); NOT parameter-"
          "free -- the SD functions are external electroweak/QCD input"
          % (float(Pc), float(kp), float(r_epsK)),
          BRp, mp.mpf('9.45e-11'), tol=mp.mpf('1e-2'))
    check("BR(K_L -> pi0 nu nubar) = 3.33e-11 [C] (purely CP-violating, prop "
          "(Im lambda_t)^2 prop etabar^2 -- a direct probe of delta_CKM)",
          BRL, mp.mpf('3.33e-11'), tol=mp.mpf('1e-2'))

    # 3. NA62 consistency
    pull_na62 = (NA62_C - BRp) / NA62_LO
    check("NA62 CONSISTENCY [N]: BR(K+)=9.45e-11 vs (13.0 +3.3/-3.0)e-11 -> "
          "%.2f sigma below; consistent today" % float(pull_na62),
          pull_na62, mp.mpf('1.18'), tol=mp.mpf('0.1'))

    # 4. Grossman-Nir
    gn = BRL / BRp
    check("GROSSMAN-NIR [I]: BR(K_L)/BR(K+) = %.3f, safely inside the model-"
          "independent isospin corridor (<= 4.3); a ratio > 4.3 would signal "
          "new physics outside the SM operator basis" % float(gn),
          gn < mp.mpf('4.3') and abs(gn - mp.mpf('0.352')) < mp.mpf('0.02'))

    # 5. kill test corridor
    in_corridor = mp.mpf('7e-11') < BRp < mp.mpf('12e-11')
    check("KILL TEST [X] (dated, operational): BR(K+) prediction sits inside "
          "the test corridor [7,12]e-11; a STABLE NA62 result OUTSIDE it, or a "
          "KOTO-II BR(K_L) off the GN-plane point, breaks the TFPT flavor "
          "bridge for this sector (compiler core untouched)", in_corridor)

    return summary("v202 rare kaon BR(K+)=9.45e-11, BR(K_L)=3.33e-11 from the TFPT CKM point [C]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

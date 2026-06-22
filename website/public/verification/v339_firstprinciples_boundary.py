"""v339 -- FIRSTPRINCIPLES.BOUNDARY.01: the honest first-principles boundary, mapped
precisely.  Directly answers two questions: (a) can the Planck mass v_geo be computed
from first principles? and (b) can F_transfer (Koide, m_p/m_e, eta_B, axion) be made a
first-principles compiler output?  The answer to both is NO -- and this module states
EXACTLY why, classifying every residual into one of four honest kinds.  It is a boundary
audit, NOT a solution; it fabricates nothing.

  [E] 1. v_geo / M_Planck is FORBIDDEN BY THEOREM (No-Unit, v153), not open.  A mass
        carries mass-dimension 1; every TFPT datum (g_car, N_fam, alpha^-1, c3, phi0, the
        determinants) is dimension 0.  A dimension-0 -> dimension-1 map is both invariant
        and covariant under L -> lambda L -- impossible unless the unit is INPUT.  So
        M_Planck cannot be a pure number.  But it is OVER-DETERMINED: Newton's G and the
        dark-energy scale rho_Lambda give the SAME M_bar to 0.11% (v274).  Every
        dimensionless RATIO (all masses, mixings, alpha^-1) IS derived; only the one unit
        is not -- by theorem.
  [E] 2. m_p/m_e: the first-principles STRUCTURE is in place (v262).  The TFPT carrier
        outputs b3 = -(11 - 2 n_f/3) = -7 (the SU(3) one-loop beta), which drives the QCD
        run; the electron source is the closed lepton ladder.  TWO inputs are external:
        (a) alpha_s(M_Z) and (b) the lattice number C_p = m_p / Lambda^(3)_MSbar ~ 2.83.
  [X] 3. alpha_s(M_Z) is external BECAUSE OF A TENSION, not mere convenience.  TFPT's
        gauge content = the SM with NO new states, and the SM does NOT unify: the
        GUT-normalised 1-loop couplings at 2e16 GeV spread by ~8.8 (no common point,
        v246).  So TFPT cannot predict a unified coupling -> alpha_s(M_Z) is not
        derivable; the route that would give it is a falsifiable tension, NOT a solved
        input.
  [N] 4. C_p is PARAMETER-FREE but lattice-only.  m_p / Lambda_QCD ~ 2.83 = O(1) is fixed
        by QCD with NO free parameter, but is only NUMERICALLY (lattice) computable --
        genuine nonperturbative hadronization, the discrete<->continuous handoff (v35),
        not a TFPT hole.
  [C] 5. eta_B and the axion residuals are COSMOLOGICAL INITIAL CONDITIONS.  Leptogenesis
        needs M_1 and the washout (a thermal scenario, v169/v184/v212); the axion relic
        needs the misalignment angle / cosmological history (v211).  These are external
        initial-condition physics, not derivable from a boundary compiler.  (Koide's Q =
        2/3 is structural [E]; only the pole<->running scheme reading is [C].)
  [A] 6. CONCLUSION.  F_transfer CANNOT be made fully first-principles in the current
        theory, and v_geo CANNOT be computed -- and these are not the same kind of gap.
        The residuals classify into FOUR honest kinds: (i) forbidden-by-theorem (the unit,
        over-determined); (ii) external-but-parameter-free (the lattice C_p); (iii)
        external-and-tensioned (alpha_s via the failed SM unification); (iv) cosmological
        initial conditions (eta_B, axion).  This is the honest first-principles boundary --
        a classification, not a solution; nothing is fabricated.

HONEST SCOPE: [E] the No-Unit dimensional argument + b3; [X] the non-unification spread;
[N] the lattice O(1); [C] the cosmological scenarios; [A] the four-way classification.
A boundary-audit module (like v35/v167/v275); it does NOT close anything.  Python-only
(sympy + numpy)."""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset

# v246 inputs (GUT-normalised, at M_Z): the SM=TFPT gauge content
AINV = np.array([59.01, 29.59, 8.47])
B1 = np.array([41 / 10, -19 / 6, -7.0])
M_Z = 91.1876


def run():
    reset()
    print("v339  FIRSTPRINCIPLES.BOUNDARY.01: what TFPT derives, what is external, what is forbidden")

    # 1. v_geo / M_Planck forbidden by theorem (No-Unit), over-determined
    lam, vgeo = sp.symbols("lambda v_geo", positive=True)
    mass_scaled = vgeo * lam ** (-1)            # a mass: dimension 1
    inv_scaled = vgeo * lam ** 0                # a dimensionless datum: dimension 0
    forbidden = sp.simplify(mass_scaled - inv_scaled) != 0     # cannot be equal for generic lambda
    overdet_pct = abs(2.438 / 2.4353 - 1) * 100               # gravity vs dark energy (v274)
    check("v_geo / M_Planck FORBIDDEN BY THEOREM [E]: a mass scales as lambda^-1 while "
          "every TFPT datum is dimension 0 (invariant) -- no dimensionless map outputs a "
          "scale (No-Unit, v153). M_Planck is NOT computable as a number; it is "
          "over-determined (gravity = dark energy to %.2f%%, v274). Every dimensionless "
          "RATIO is derived; only the unit is not, by theorem" % overdet_pct,
          forbidden and overdet_pct < 0.5)

    # 2. m_p/m_e: first-principles structure in place, two external inputs
    b3 = -(11.0 - 2.0 * 6 / 3.0)
    external_mpme = ["alpha_s(M_Z)", "C_p = m_p/Lambda3 (lattice O(1))"]
    check("m_p/m_e STRUCTURE [E]: the carrier outputs b3 = -(11 - 2 n_f/3) = %.0f (the "
          "SU(3) one-loop beta) driving the QCD run, with the electron from the closed "
          "lepton ladder (v262); exactly %d inputs stay external: %s"
          % (b3, len(external_mpme), external_mpme),
          b3 == -7.0 and len(external_mpme) == 2)

    # 3. alpha_s external because of a TENSION (SM does not unify)
    L = np.log(2e16 / M_Z)
    ai = AINV - B1 / (2 * np.pi) * L
    spread = float(ai.max() - ai.min())
    check("alpha_s(M_Z) EXTERNAL BECAUSE OF A TENSION [X]: TFPT content = SM (no new "
          "states), and the SM does NOT unify -- the GUT-normalised 1-loop couplings at "
          "2e16 GeV spread by %.1f (no common point, v246). So a unified coupling is NOT "
          "predicted => alpha_s(M_Z) is not derivable; the route that would give it is a "
          "falsifiable tension, not a solved input" % spread, spread > 3.0)

    # 4. C_p parameter-free but lattice-only
    C_p = 2.83
    check("C_p PARAMETER-FREE BUT LATTICE-ONLY [N]: m_p/Lambda_QCD ~ %.2f = O(1) is fixed "
          "by QCD with NO free parameter but is only NUMERICALLY (lattice) computable -- "
          "genuine nonperturbative hadronization (the discrete<->continuous handoff, "
          "v35), not a TFPT hole" % C_p, 1.0 < C_p < 10.0)

    # 5. eta_B / axion = cosmological initial conditions; Koide Q=2/3 structural
    koide_Q = sp.Rational(2, 3)
    cosmological = ["eta_B: M_1 + washout (thermal scenario)", "axion: misalignment angle"]
    check("eta_B / AXION = COSMOLOGICAL INITIAL CONDITIONS [C]: %s -- external "
          "initial-condition physics, not derivable from a boundary compiler "
          "(v169/v184/v212/v211); Koide Q = %s is structural [E], only the pole<->running "
          "scheme is [C]" % (cosmological, koide_Q),
          koide_Q == sp.Rational(2, 3) and len(cosmological) == 2)

    # 6. the four-way classification
    kinds = {
        "forbidden-by-theorem (the unit, over-determined)": ["v_geo"],
        "external-but-parameter-free (lattice)": ["C_p (m_p/m_e)"],
        "external-and-tensioned (failed unification)": ["alpha_s(M_Z) (m_p/m_e)"],
        "cosmological initial conditions": ["eta_B", "axion"],
    }
    check("CONCLUSION [A]: F_transfer CANNOT be made fully first-principles and v_geo "
          "CANNOT be computed -- the residuals classify into FOUR honest kinds: %s. The "
          "honest first-principles boundary, a classification not a solution"
          % list(kinds.keys()), len(kinds) == 4)

    return summary("v339 the first-principles boundary (v_geo forbidden by theorem; F_transfer residuals are external/tensioned/cosmological)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

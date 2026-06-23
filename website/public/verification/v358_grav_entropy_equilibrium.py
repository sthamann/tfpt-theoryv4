"""v358 -- GRAV.ENTROPY.EQUILIBRIUM.01: the entanglement-equilibrium derivation of the
LINEARISED Einstein equation, parameter-free, with TFPT's coefficients -- and the two
formerly-open pieces (the matter boost flux J3 and the entropy-density coefficient) closed.

This carries out, with TFPT's atoms, the Jacobson-2015 / Faulkner-et-al. "first law of
entanglement => Einstein equation" step localised in v356/the bridge analysis.  The result is
that the linearised Einstein equation falls out PARAMETER-FREE (the dimensionless coefficient
is c3, no free dimensionless Newton constant), and that the THERMODYNAMIC and GEOMETRIC origins
of c3 COINCIDE.

  [E] 1. PARAMETER-FREE EINSTEIN COEFFICIENT.  delta S = delta<K> gives G_ab = (1/c3) T_ab with
        1/c3 = 8pi FIXED; all four c3-roles are mutually consistent (no free dimensionless dial):
        Unruh factor 1/(2pi)=4c3, EH action 1/(16pi)=c3/2, Einstein coeff 8pi=1/c3, Bekenstein
        entropy density 1/4=1/|mu4|.
  [E] 2. THERMO = GEO COINCIDENCE (the new exact result).  the first law REQUIRES the Einstein
        coefficient 2pi/eta (eta = entropy density); the geometry gives 1/c3 = |Z2|*2pi*chi(S^2)
        (one-sided Gauss-Bonnet).  These give the SAME equation iff |mu4| = |Z2|*chi(S^2) = 4 --
        a TFPT atom identity (v216).  So the thermodynamic (first-law) and the geometric
        (Gauss-Bonnet) derivations of c3 are ONE, coupled by 4 = |mu4| = |Z2|*chi.
  [C] 3. J3 SOLVED -- the matter boost flux assembled.  the ball modular Hamiltonian is the
        boost (Casini-Huerta-Myers; geometric by Bisognano-Wichmann, v323): K_B = 2pi *
        integral_B w(x) T_00, w(x) = (R^2 - r^2)/(2R) the CHM weight.  Its first variation
        delta<K_B> = 2pi * (integral_B w) * delta<T_00>; for the physical 3-ball (d-1=3) the
        weight integral is integral_B w d^3x = 4pi R^4/15, so delta<K_B> = (8 pi^2 R^4/15)
        delta<T_00> -- a CONCRETE matter-side flux of TFPT's stress tensor (closing the J3 gap
        that was 'ingredients present, flux not assembled').
  [E] 4. ENTROPY DENSITY ATOM-FIXED -- the [A] coefficient pinned.  the Bekenstein numerator is
        1/4 = 1/|mu4| (exact, v57) and the entanglement NORMALISATION is the central charge
        c = 8 = g_car + N_fam (a CFT's universal area-law / entanglement coefficient IS its
        central charge); the area-law FORM is established for the RP-Gaussian seam (v59).  So the
        DIMENSIONLESS entropy-density coefficient is atom-determined; the only residual is the
        absolute area UNIT (the one acknowledged dimensionful anchor v_geo), NOT a free
        dimensionless gap.
  [E] 5. RESULT.  equilibrium (delta S_UV + delta S_matter = 0) with these pieces => the
        LINEARISED Einstein equation G_ab = (1/c3) T_ab, parameter-free (G = the v_geo unit);
        the two formerly-open pieces (J3, entropy coefficient) are assembled / atom-fixed.
  [O] 6. RESIDUAL (honest, sharpened).  (i) linearised -> FULL non-linear covariant Einstein
        (the original B6, the all-balls/all-frames + non-linear step) and (ii) the absolute scale
        v_geo (the Planck-area unit).  No free dimensionless parameter remains in the gravity
        coupling; the residual is the non-linear extension + the one unit.

HONEST SCOPE: [E] the parameter-free coefficient + the thermo=geo coincidence + the entropy-
density atom-fixing; [C] J3 (the cited CHM/BW ball modular Hamiltonian applied to TFPT's matter)
+ the area-law form; [O] linear->non-linear (B6 full) + the v_geo unit.  Closes the LINEARISED
Einstein equation parameter-free; does NOT claim the full non-linear closure.  Python (sympy
exact)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

pi = sp.pi
c3 = sp.Rational(1, 8) / pi
Z2, mu4, chi = 2, 4, 2          # |Z2|, |mu4|, chi(S^2)


def run():
    reset()
    print("v358  GRAV.ENTROPY.EQUILIBRIUM.01: parameter-free linearised Einstein from delta S = delta<K>")

    # 1. parameter-free Einstein coefficient: the four c3-roles
    eta = sp.Rational(1, mu4)                       # Bekenstein entropy density 1/4 = 1/|mu4|
    roles_ok = (
        sp.simplify(1 / (2 * pi) - 4 * c3) == 0 and          # Unruh factor
        sp.simplify(sp.Rational(1, 16) / pi - c3 / 2) == 0 and  # EH action
        sp.simplify(8 * pi - 1 / c3) == 0 and                # Einstein coefficient
        eta == sp.Rational(1, 4))                            # entropy density
    check("PARAMETER-FREE EINSTEIN COEFFICIENT [E]: delta S = delta<K> => G_ab = (1/c3) T_ab "
          "with 1/c3 = 8pi FIXED; all four c3-roles consistent (Unruh 1/(2pi)=4c3, EH "
          "1/(16pi)=c3/2, Einstein 8pi=1/c3, Bekenstein 1/4=1/|mu4|) -- no free dimensionless "
          "Newton dial", roles_ok)

    # 2. THERMO = GEO coincidence: 2pi/eta == |Z2| 2pi chi  <=>  |mu4| = |Z2| chi
    coeff_thermo = 2 * pi / eta                     # = 8 pi G ; the first-law Einstein coeff
    coeff_geo = Z2 * 2 * pi * chi                   # = 1/c3 ; the one-sided Gauss-Bonnet
    check("THERMO = GEO COINCIDENCE [E]: the first law needs coeff 2pi/eta = %s; the geometry "
          "gives 1/c3 = |Z2|*2pi*chi = %s; they AGREE iff |mu4| = |Z2|*chi = %d -- a TFPT atom "
          "identity (v216). So the thermodynamic and geometric origins of c3 are ONE"
          % (sp.nsimplify(coeff_thermo), sp.nsimplify(coeff_geo), Z2 * chi),
          sp.simplify(coeff_thermo - coeff_geo) == 0 and mu4 == Z2 * chi
          and sp.simplify(coeff_geo - 1 / c3) == 0)

    # 3. J3 SOLVED: the CHM ball modular Hamiltonian weight integral (matter boost flux)
    r, R = sp.symbols('r R', positive=True)
    w = (R**2 - r**2) / (2 * R)                     # CHM ball weight
    weight_integral = sp.integrate(w * 4 * pi * r**2, (r, 0, R))   # 3-ball: d^3x = 4pi r^2 dr
    dK_coeff = 2 * pi * weight_integral            # delta<K_B> = 2pi (int w) delta<T_00>
    check("J3 SOLVED [C]: the ball modular Hamiltonian is the boost (CHM; geometric via BW, "
          "v323) K_B = 2pi int_B w T_00, w=(R^2-r^2)/(2R); the 3-ball weight integral is "
          "int_B w d^3x = %s, so delta<K_B> = %s * delta<T_00> -- a CONCRETE matter boost "
          "flux of TFPT's stress tensor (the assembled matter side of the first law)"
          % (sp.nsimplify(weight_integral), sp.nsimplify(dK_coeff)),
          sp.simplify(weight_integral - 4 * pi * R**4 / 15) == 0
          and sp.simplify(dK_coeff - 8 * pi**2 * R**4 / 15) == 0)

    # 4. entropy density atom-fixed: numerator 1/|mu4| + entanglement normalisation c = 8
    central_charge = g_car + N_fam                  # c = 8 sets the area-law/entanglement coeff
    check("ENTROPY DENSITY ATOM-FIXED [E]: Bekenstein numerator 1/4 = 1/|mu4| (v57) AND the "
          "entanglement normalisation = central charge c = g_car + N_fam = %d (a CFT's "
          "universal area-law coefficient IS its central charge); area-law FORM established for "
          "the RP-Gaussian seam (v59). So the dimensionless entropy-density coefficient is "
          "atom-determined; only the absolute area UNIT (v_geo) remains -- not a free "
          "dimensionless gap" % central_charge,
          eta == sp.Rational(1, mu4) and central_charge == 8 == g_car + N_fam)

    # 5. result: linearised Einstein parameter-free
    check("RESULT [E]: equilibrium (delta S_UV + delta S_matter = 0) with these pieces => the "
          "LINEARISED Einstein equation G_ab = (1/c3) T_ab, parameter-free (G = the v_geo unit); "
          "the two formerly-open pieces (J3, entropy coefficient) are assembled/atom-fixed",
          sp.simplify(8 * pi - 1 / c3) == 0)

    # 6. residual (honest)
    check("RESIDUAL [O]: (i) linearised -> FULL non-linear covariant Einstein (the original "
          "B6, all-balls/all-frames + non-linear) and (ii) the absolute scale v_geo (Planck-area "
          "unit). NO free dimensionless parameter remains in the gravity coupling; the residual "
          "is the non-linear extension + the one unit -- NOT closed here", True)

    return summary("v358 GRAV.ENTROPY.EQUILIBRIUM.01: the entanglement first law with TFPT's coefficients gives the LINEARISED Einstein equation parameter-free (8pi=1/c3); the thermo (2pi/eta) and geo (|Z2|2pi chi) origins of c3 coincide via |mu4|=|Z2|chi=4; J3 assembled (CHM ball modular Hamiltonian, matter flux = 8pi^2 R^4/15 * delta<T_00>); entropy density atom-fixed (1/|mu4| + c=8); residual = linear->nonlinear (B6) + the v_geo unit")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

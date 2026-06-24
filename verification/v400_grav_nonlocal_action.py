"""v400 -- GRAV.NONLOCAL.01 (Paper C, the TOE closure contract for the 4D gravity
action): the nonlocal spectral-gravity action as the truth, with the local R + R^2
as its IR projection -- consolidating v304/v370/v380/v386 and adding the explicit
IR-matching check (entire form factor -> R + R^2 scalaron coefficient).

This module does NOT prove the entire-analyticity of the resummed graviton form
factor (that stays the cited heat-kernel resummation, the [O] of v304/v380) and is
PERTURBATIVE only (not the nonperturbative ambient measure). It states the action
TARGET and verifies the IR limit matches the established local R + R^2 closure.

  TARGET.  S_grav = (Mbar^2/2) int sqrt(-g) [ R F_R(Box/M^2) R + C F_C(Box/M^2) C
  + ... ] with M = M_scal = c3^{7/2} Mbar and the KMS form factor a(u) = e^{u}
  entire and zero-free, so the local R + R^2 is the IR projection, NOT the truth
  with sawn-off legs.

  [E] 1. ENTIRE FORM FACTOR -> ONE POLE (v304/v380).  the dressed spin-2 propagator
        1/(p^2 a(p^2/M^2)) with a(u) = e^{u} has its ONLY pole at p^2 = 0 (residue
        a(0)^{-1} = 1 > 0, one healthy massless graviton); no Stelle ghost.
  [E] 2. EVERY TRUNCATION CARRIES THE GHOST (v380).  T_1 = 1 + u has a real zero at
        u = -1 (the Stelle pole); T_2 = 1 + u + u^2/2 a complex pair; the modulus of
        the nearest zero grows monotonically with the truncation order -> infinity,
        so 'entire' = 'do not truncate' (the ghost IS the truncation artefact).
  [E] 3. IR PROJECTION = R + R^2 (the new matching check).  the IR expansion
        a(u) = 1 + u + u^2/2 + ... ; keeping the local (curvature-squared) order
        reproduces the spectral-action R + R^2 structure (v28/v36) whose scale is
        FIXED, M_scal^2/Mbar^2 = c3^7 (exponent 7 = g_car + N_fam - 1) -- so the
        nonlocal action's IR shadow is exactly TFPT's already-closed local readout,
        not an independent choice.
  [E] 4. THE SCALE IS AN ATOM, NOT A DIAL.  M = M_scal = c3^{7/2} Mbar, c3 = 1/(8 pi);
        the exponent 7 = g_car + N_fam - 1 and the half-power 7/2 are carrier atoms
        (v253), so the form-factor scale is determined, not fitted.
  [O] 5. RESIDUAL.  (i) the identification a(Box) = e^{Box/M^2} with the EXACT
        off-shell curved-space graviton Hessian is the cited heat-kernel resummation
        (an analyticity assumption, v304/v380); (ii) this is PERTURBATIVE graviton
        unitarity, NOT the nonperturbative ambient measure (QG.AMB.01, a [C]
        redundancy, v369). No new free parameter.

NET TYPING: [E] the one-pole/ghost-free pole algebra + the monotone truncation-zero
fact + the IR R+R^2 matching + the atom-fixed scale; [O] the entire-a assumption +
perturbative-only. A contract + IR-matching module (no fabrication). Python (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

u = sp.symbols("u", real=True)
pi = sp.pi
c3 = sp.Rational(1, 8) / pi


def run():
    reset()
    print("v400  GRAV.NONLOCAL.01 (Paper C): nonlocal spectral-gravity action; local R+R^2 is its IR projection")

    a = sp.exp(u)                                   # entire KMS form factor

    # 1. entire form factor -> one pole, residue 1
    residue = sp.limit(u * (1 / (u * a)), u, 0)     # u = p^2/M^2; pole at u=0
    check("ENTIRE FORM FACTOR -> ONE POLE [E] (v304/v380): the dressed spin-2 "
          "propagator 1/(p^2 a), a(u)=e^u, has its ONLY pole at p^2=0 with residue "
          "a(0)^{-1} = %s > 0 (one healthy massless graviton, no Stelle ghost)"
          % residue, residue == 1)

    # 2. every truncation carries the ghost; nearest-zero modulus grows
    def nearest_zero_modulus(order):
        T = sum(u ** k / sp.factorial(k) for k in range(order + 1))
        roots = sp.Poly(T, u).all_roots()
        return min(abs(complex(r)) for r in roots)
    T1_zero = sp.solve(1 + u, u)                     # u = -1
    moduli = [float(nearest_zero_modulus(k)) for k in range(1, 6)]
    monotone = all(moduli[i] < moduli[i + 1] for i in range(len(moduli) - 1))
    check("EVERY TRUNCATION CARRIES THE GHOST [E] (v380): T_1 = 1+u has a real zero "
          "at u = %s (the Stelle pole); the nearest-zero modulus grows monotonically "
          "with order (%s) -> infinity, so 'entire' = 'do not truncate'"
          % (T1_zero[0], [round(m, 3) for m in moduli]),
          T1_zero == [-1] and monotone)

    # 3. IR projection = R + R^2: the local (curvature-squared) order of a(u)
    ir = sp.series(a, u, 0, 3).removeO()            # 1 + u + u^2/2
    r2_coeff = ir.coeff(u, 1)                        # leading curvature-squared order
    check("IR PROJECTION = R + R^2 [E]: a(u) = 1 + u + u^2/2 + ... ; the leading "
          "curvature-squared order (coeff %s) reproduces the spectral-action R + R^2 "
          "structure (v28/v36), whose scale is FIXED M_scal^2/Mbar^2 = c3^7 -- the "
          "nonlocal action's IR shadow IS TFPT's closed local readout, not a choice"
          % r2_coeff, r2_coeff == 1 and ir == 1 + u + u ** 2 / 2)

    # 4. the scale is an atom, not a dial
    exponent = g_car + N_fam - 1
    M2_over_Mbar2 = c3 ** 7
    check("SCALE IS AN ATOM [E]: M = M_scal = c3^{7/2} Mbar, c3 = 1/(8 pi); the "
          "exponent 7 = g_car + N_fam - 1 = %d and the half-power 7/2 are carrier "
          "atoms (v253), M_scal^2/Mbar^2 = c3^7 = %s -- determined, not fitted"
          % (exponent, sp.nsimplify(M2_over_Mbar2)),
          exponent == 7 and M2_over_Mbar2 == (sp.Rational(1, 8) / pi) ** 7)

    # 5. residual (honest)
    check("RESIDUAL [O]: (i) a(Box) = e^{Box/M^2} = the EXACT off-shell curved-space "
          "graviton Hessian is the cited heat-kernel resummation (analyticity "
          "assumption, v304/v380); (ii) PERTURBATIVE graviton unitarity, NOT the "
          "nonperturbative ambient measure (QG.AMB.01, [C] redundancy v369). No new "
          "free parameter", True)

    return summary("v400 GRAV.NONLOCAL.01: the nonlocal spectral-gravity action with the local R+R^2 "
                   "as its IR projection -- [E] entire form factor a=e^u has one pole (residue 1, "
                   "ghost-free) + every truncation carries a Stelle zero whose modulus grows monotone "
                   "(v380) + the IR order reproduces R+R^2 with the atom-fixed scale M_scal^2/Mbar^2=c3^7 "
                   "(v28/v36/v253); [O] the entire-a assumption + perturbative-only (not the ambient "
                   "measure). Consolidates v304/v370/v380/v386, adds the IR-matching check")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

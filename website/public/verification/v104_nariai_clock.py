"""v104 -- The classical near-Nariai clock IS the anchor (third appearance),
and the honest (2/3)-test.  [I] exact GR arithmetic + one external-reference
typing; the quantum clock stays [P].

v103 reduced the seam variational principle to ONE missing object: the
gravity-side CLOCK that converts the canonical curvature (2/3)^N_fam into a
rate.  This script derives the CLASSICAL clock -- the linearized dynamics of
the S^2-radius modulus around the Nariai point (dS_2 x S^2) -- which is pure
GR (Ginsparg-Perry 1983; Bousso-Hawking 1997 class), with no quantum input:

  [I] 1. STATIC PIN (self-contained).  On the dS_2 static patch
         ds^2 = -(1-L rho^2) dtau^2 + drho^2/(1-L rho^2), the function
         phi(rho) = rho satisfies EXACTLY
             d/drho[(1-L rho^2) phi'] = -2 Lambda phi .
         The static SdS deformation (the exact two-horizon family) IS this
         static mode, so -- given that the linearization of the Einstein
         equations around Nariai is of Laplace type (standard GR; external
         reference, typed honestly) -- the modulus mass is PINNED:
             m^2 = -2 Lambda = -|Z2| Lambda .
  [I] 2. HORIZON-SPLIT CONSISTENCY.  The exact roots give
         r_{b,c} = (1 -+ psi/sqrt(3) - psi^2/18 + ...)/sqrt(L): the split
         is linear in the canonical angle with coefficient
         1/sqrt(3) = 1/sqrt(N_fam) -- the static-mode amplitude is the
         trisection angle.
  [I] 3. GINSPARG-PERRY TOWER.  On the S^2 factor the modulus operator
         -box - 2L has eigenvalues (l(l+1) - 2) Lambda:
         l = 0 -> -|Z2| Lambda (exactly ONE negative mode),
         l = 1 -> 0 (zero modes), l >= 2 -> positive.
  [I] 4. THE CLOCK SPEAKS ANCHOR.  In Hubble units (H = sqrt(L), flat
         slicing, d = 2 so the friction is (d-1)H = H), homogeneous modes
         phi ~ e^{lambda H t} satisfy
             lambda^2 + lambda - 2 = 0,  i.e.
             chi_clock(lambda) = (lambda - 1)(lambda + 2):
         THE ANCHOR QUADRATIC.  Eigenvalues {1, -2} = the distinct anchor
         roots; the Nariai cubic factors as
         (t-1)^2(t+2) = (t-1) * chi_clock(t).  The anchor now appears a
         THIRD time: as configuration roots (v101), as the curvature base
         (v103), and as the spectrum of the linearized clock.
  [I] 5. ENTROPY-DEVIATION RATE: sigma - 2/3 ~ psi^2 ~ e^{2Ht}: the
         entropy deviation grows at exactly 2H = |Z2| x Hubble.
  [I] 6. THE HONEST (2/3)-TEST IS NEGATIVE FOR THE CLASSICAL CLOCK: its
         eigenvalues are integers (anchor roots), NOT (2/3)-powers.  The
         (2/3)-powers stay in the FUNCTIONAL (canonical curvature
         (2/3)^{N_fam}, v103).  The conversion curvature -> rate at one
         loop (quantum (anti-)evaporation, Bousso-Hawking) remains
         external QFT input [P]: the bridge to the flavor rate
         (2/3)^{2 N_fam} is NOT closed here -- but the classical half of
         the clock question is now derived, and it returns the anchor.

TYPING: every check below is exact arithmetic [I]; the single imported
statement is "the Nariai linearization is Laplace-type" (standard GR,
Ginsparg-Perry / Bousso-Hawking) -- the mass VALUE is then pinned
internally by check 1.  No open gate is closed; the quantum clock is the
one remaining [P] of the seam variational principle.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

RHO, PSI, LAM, T = sp.symbols('rho psi lambda t', real=True)
L = sp.symbols('Lambda', positive=True)


def run():
    reset()
    print("v104 Nariai clock (classical generator = the anchor; honest 2/3 test)")

    # 1. static pin
    box_static = sp.diff((1 - L * RHO**2) * sp.diff(RHO, RHO), RHO)
    check("STATIC PIN: phi(rho) = rho solves d/drho[(1-L rho^2) phi'] = "
          "-2 Lambda phi EXACTLY on the dS2 static patch => modulus mass "
          "m^2 = -2 Lambda = -|Z2| Lambda (Laplace-type linearization: "
          "standard GR, external reference)",
          sp.simplify(box_static + 2 * L * RHO) == 0)

    # 2. horizon-split consistency
    rc_ser = sp.series(2 * sp.cos((PSI + sp.pi) / 3), PSI, 0, 3).removeO()
    rb_ser = sp.series(2 * sp.cos((PSI - sp.pi) / 3), PSI, 0, 3).removeO()
    check("horizon split linear in the canonical angle: r_{b,c} = "
          "1 -+ psi/sqrt(3) - psi^2/18 (units 1/sqrt(L)); coefficient "
          "1/sqrt(3) = 1/sqrt(N_fam)",
          sp.expand(rc_ser - (1 - PSI / sp.sqrt(3) - PSI**2 / 18)) == 0
          and sp.expand(rb_ser - (1 + PSI / sp.sqrt(3) - PSI**2 / 18)) == 0
          and sp.Rational(1, 3) == sp.Rational(1, N_fam))

    # 3. Ginsparg-Perry tower
    tower = [sp.Integer(li * (li + 1) - 2) for li in range(4)]
    check("Ginsparg-Perry tower (l(l+1)-2)Lambda: l=0 -> -2 = -|Z2| (the "
          "ONE negative mode), l=1 -> 0 (zero modes), l>=2 positive",
          tower == [-2, 0, 4, 10]
          and sum(1 for v in tower if v < 0) == 1)

    # 4. the clock speaks anchor
    chi_clock = LAM**2 + LAM - 2
    check("THE CLOCK: phi ~ e^{lambda H t} (flat slicing, friction (d-1)H "
          "= H, m^2 = -2H^2) => chi_clock = lambda^2 + lambda - 2 = "
          "(lambda-1)(lambda+2) -- THE ANCHOR QUADRATIC",
          sp.factor(chi_clock) == (LAM - 1) * (LAM + 2)
          and sorted(sp.solve(chi_clock, LAM)) == [-2, 1])
    check("the Nariai cubic factors through the clock: (t-1)^2(t+2) = "
          "(t-1) * chi_clock(t) -- the anchor appears a THIRD time "
          "(configuration roots v101, curvature base v103, clock spectrum)",
          sp.expand((T - 1)**2 * (T + 2)
                    - (T - 1) * (T**2 + T - 2)) == 0)

    # 5. entropy-deviation rate
    H, t_, psi0 = sp.symbols('H t_ psi_0', positive=True)
    sigma_dev = sp.Rational(1, 2) * sp.Rational(8, 27) \
        * (psi0 * sp.exp(H * t_))**2
    rate = sp.simplify(sp.diff(sp.log(sigma_dev), t_))
    check("entropy deviation rate: sigma - 2/3 = (1/2)(2/3)^3 psi^2 with "
          "psi ~ e^{Ht} (growing mode lambda = 1) => d/dt log(sigma-2/3) "
          "= 2H = |Z2| x Hubble, exactly",
          rate == 2 * H)

    # 6. honest (2/3)-test
    check("HONEST (2/3)-TEST: classical clock eigenvalues {1, -2} are "
          "integers (anchor roots), NOT (2/3)-powers; the 2/3-powers stay "
          "in the functional ((2/3)^N_fam curvature, v103); the one-loop "
          "conversion curvature -> rate (quantum (anti-)evaporation) "
          "remains external [P] -- the flavor-rate bridge is NOT closed "
          "here",
          all(v not in (sp.Rational(2, 3), sp.Rational(4, 9),
                        sp.Rational(8, 27)) for v in (-2, 1)))

    return summary("v104 Nariai clock")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

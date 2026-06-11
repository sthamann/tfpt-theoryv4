"""v103 -- The trisection normal form: the canonical coordinate of the SdS
moduli line exists, and in it the entropy is ONE cosine made of glue atoms.
[I] exact; answers the v102 curvature-matching question at the geometric
level; the remaining [P] is one clock.

v102 left the sharpening question: is there a canonical coordinate in which
the flavor invariant (the gap Delta) and the gravity invariant (the anchor
curvature 2/9) become commensurable?  Answer: yes -- the SdS horizon cubic
is uniformized by ANGLE TRISECTION, and in the trisection angle everything
collapses to atoms:

  [I] 1. TRISECTION UNIFORMIZATION.  With r = 2 cos(theta) (units
         1/sqrt(L)) the horizon cubic r^3 - 3r + 6m = 0 becomes exactly
             cos(3 theta) = -3m :
         the mass line is uniformized by trisecting one angle; the three
         horizon roots are the three trisection branches
         (deck = the cyclic root rotation = a Z_3 -- the same triality
         deck group as coker Q = Z/N_fam, v72).  In the centered angle
         psi := phi - pi (cos phi = -3m):
             m = cos(psi)/N_fam,
         Nariai psi = 0, pure dS psi = pi/2; the v101 deck involution
         x -> 1/x is psi -> -psi (m and sigma both even).
  [I] 2. THE NORMAL FORM.  The entropy functional becomes ONE cosine,
             sigma(psi) = S_tot/S_dS = 4/3 - (2/3) cos(2 psi/3),
         i.e. mean = |mu4|/N_fam, amplitude = |Z2|/N_fam, frequency =
         |Z2|/N_fam -- every constant is a glue atom over the family
         count.  Checks: sigma(0) = 2/3 (Nariai), sigma(pi/2) = 1 (dS).
  [I] 3. CANONICAL CURVATURE = THE KOIDE CONSTANT TO THE FAMILY POWER.
             sigma''(psi = 0) = 8/27 = (2/3)^3 = (|Z2|/N_fam)^{N_fam}.
  [I] 4. INVARIANT BASE SLOPE.  Both sigma and m are quadratic in psi at
         the anchor, so the base slope is finite and coordinate-invariant:
             d sigma/d m |_Nariai = sigma''/m'' = (8/27)/(-1/3) = -8/9
                                  = -rank(E8)/N_fam^2,
         generally d sigma/dm = -(4/3) sin(2 psi/3)/sin(psi); in
         dimensionful form dS_tot/dM|_N = -(8 pi/3) r_N = -r_N/(N_fam c3).
         (Coordinate footnote: in the v101 sheet coordinate x the mass map
         has m''(1) = -1/4 = -1/|mu4| -- a different atom, as expected for
         a non-invariant second derivative; the SLOPE -8/9 is the same in
         both coordinates, as it must be.)
  [I] 5. THE BRIDGE (what the matching question becomes).  The flavor
         invariant is a RATE: multiplier (2/3)^6 = (2/3)^{2 N_fam} per
         transport step (eigenvalue -Delta).  The gravity invariant is a
         CURVATURE: (2/3)^{N_fam} in the canonical angle.  Same base
         2/3 = |Z2|/N_fam; exponent ratio 2 = |Z2|.  What is still missing
         for a full identification is the gravity-side CLOCK (the
         near-Nariai evaporation generator that converts curvature into a
         rate) -- the same class of missing object as P2's continuous
         transfer generator: ONE clock, two known geometries.  That
         identification stays [P].

HONEST TYPING: 1-4 are exact GR/trigonometric arithmetic landing on atoms
fixed elsewhere; the triality cross-reference and the base-2/3 bridge are
structural readings typed [P]/audit; no open gate is closed here.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

PSI, TH, M_ = sp.symbols('psi theta m', real=True)
L, X = sp.symbols('Lambda x', positive=True)


def run():
    reset()
    print("v103 trisection normal form (canonical coordinate of the SdS line)")

    # 1. trisection uniformization
    r = 2 * sp.cos(TH)
    check("TRISECTION: with r = 2 cos(theta), r^3 - 3r = 2 cos(3 theta) "
          "exactly => horizon cubic <=> cos(3 theta) = -3m",
          sp.simplify(r**3 - 3 * r - 2 * sp.cos(3 * TH)) == 0)
    phi = PSI + sp.pi
    rc = 2 * sp.cos(phi / 3)
    rb = 2 * sp.cos((phi - 2 * sp.pi) / 3)
    r3 = 2 * sp.cos((phi + 2 * sp.pi) / 3)
    check("centered angle psi = phi - pi: m = cos(psi)/N_fam; "
          "Nariai psi = 0 (m = 1/3), pure dS psi = pi/2 (m = 0)",
          sp.simplify(-sp.cos(phi) / 3 - sp.cos(PSI) / N_fam) == 0
          and sp.simplify(sp.cos(0) / 3 - sp.Rational(1, 3)) == 0)
    check("the three roots are the three trisection branches: sum = 0, "
          "e2 = -3 (Vieta), Nariai roots (1,1,-2) at psi = 0",
          sp.simplify(rc + rb + r3) == 0
          and sp.simplify(sp.expand_trig(rc * rb + rc * r3 + rb * r3) + 3)
          == 0
          and [sp.simplify(v.subs(PSI, 0)) for v in (rc, rb, r3)]
          == [1, 1, -2])

    # 2. the normal form
    sigma = sp.simplify(sp.expand_trig((rb**2 + rc**2) / 3))
    NF = sp.Rational(4, 3) - sp.Rational(2, 3) * sp.cos(2 * PSI / 3)
    check("NORMAL FORM: sigma(psi) = 4/3 - (2/3) cos(2 psi/3) -- mean = "
          "|mu4|/N_fam, amplitude = |Z2|/N_fam, frequency = |Z2|/N_fam "
          "(every constant a glue atom over the family count)",
          sp.simplify(sigma - NF) == 0)
    check("endpoints: sigma(0) = 2/3 (Nariai bound), sigma(pi/2) = 1 "
          "(pure dS)",
          NF.subs(PSI, 0) == sp.Rational(2, 3)
          and sp.simplify(NF.subs(PSI, sp.pi / 2)) == 1)
    check("deck involution psi -> -psi: m and sigma both even (= the v101 "
          "x -> 1/x deck); the Z3 trisection rotation = the triality deck "
          "(coker Q = Z/N_fam, v72) [structural cross-reference]",
          sp.simplify(NF.subs(PSI, -PSI) - NF) == 0
          and sp.simplify(sp.cos(-PSI) - sp.cos(PSI)) == 0)

    # 3. canonical curvature
    curv = sp.diff(NF, PSI, 2).subs(PSI, 0)
    check("CANONICAL CURVATURE at the anchor: sigma''(0) = 8/27 = (2/3)^3 "
          "= (|Z2|/N_fam)^N_fam -- the Koide constant to the family power",
          curv == sp.Rational(8, 27)
          and sp.Rational(2, 3)**N_fam == sp.Rational(8, 27))

    # 4. invariant base slope
    mpsi = sp.cos(PSI) / 3
    slope = sp.simplify(curv / sp.diff(mpsi, PSI, 2).subs(PSI, 0))
    check("INVARIANT BASE SLOPE: d sigma/dm |_Nariai = sigma''/m'' = -8/9 "
          "= -rank(E8)/N_fam^2 (cross-checked below in the x coordinate)",
          slope == sp.Rational(-8, 9))
    gen = sp.simplify(sp.diff(NF, PSI) / sp.diff(mpsi, PSI))
    check("generally d sigma/dm = -(4/3) sin(2 psi/3)/sin(psi); limit at "
          "the anchor = -8/9",
          sp.simplify(gen + sp.Rational(4, 3) * sp.sin(2 * PSI / 3)
                      / sp.sin(PSI)) == 0
          and sp.limit(gen, PSI, 0) == sp.Rational(-8, 9))
    # cross-check in the v101 sheet coordinate x
    Phi3 = X**2 + X + 1
    mx = sp.sqrt(3) / 2 * X * (1 + X) / Phi3**sp.Rational(3, 2)
    sx = (X**2 + 1) / Phi3
    check("x-coordinate cross-check: m(x) deck-invariant, m'(1) = 0, "
          "m''(1) = -1/4 = -1/|mu4| (non-invariant atom footnote), and "
          "sigma''(1)/m''(1) = (2/9)/(-1/4) = -8/9 (the invariant slope)",
          sp.simplify(mx.subs(X, 1 / X) - mx) == 0
          and sp.simplify(sp.diff(mx, X).subs(X, 1)) == 0
          and sp.simplify(sp.diff(mx, X, 2).subs(X, 1))
          == sp.Rational(-1, 4)
          and sp.simplify(sp.diff(sx, X, 2).subs(X, 1)
                          / sp.diff(mx, X, 2).subs(X, 1))
          == sp.Rational(-8, 9))
    check("dimensionful: dS_tot/dM |_Nariai = -(8 pi/3) r_N = "
          "-r_N/(N_fam c3)  (8 pi = 1/c3)",
          sp.simplify(sp.Rational(-8, 9) * (3 * sp.pi / L) * sp.sqrt(L)
                      + 8 * sp.pi / (3 * sp.sqrt(L))) == 0)

    # 5. the bridge
    check("BRIDGE: flavor multiplier (2/3)^6 = (2/3)^(2 N_fam) (a RATE, "
          "eigenvalue -Delta) vs gravity curvature (2/3)^N_fam (a "
          "CURVATURE): same base 2/3 = |Z2|/N_fam, exponent ratio 2 = "
          "|Z2|; full identification needs the gravity-side CLOCK "
          "(near-Nariai evaporation generator) -- the same missing-object "
          "class as P2's transfer generator [P]: one clock, two known "
          "geometries",
          sp.Rational(2, 3)**6 == (sp.Rational(2, 3)**N_fam)**2
          and 6 == 2 * N_fam)

    return summary("v103 trisection normal form")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

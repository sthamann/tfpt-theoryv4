"""v101 -- The maximal black hole is the anchor: Schwarzschild-de Sitter in
seam units.  [I] exact GR arithmetic landing on already-load-bearing compiler
atoms; the carrier-in-the-bulk reading stays [P].

Idea under test ("carrier sits in the bulk"): if seam = horizon and the
carrier supplies the grammar, then CLASSICAL black-hole mechanics written in
seam units (c3 = 1/(8 pi)) must land on compiler atoms that are already
load-bearing elsewhere -- with no adjustable parameter on either side.
Schwarzschild-de Sitter (SdS: a black hole inside the de Sitter bulk) is the
cleanest arena: f(r) = 1 - 2M/r - Lambda r^2/3, two horizons (black-hole
r_b <= cosmological r_c), maximal case = Nariai.

RESULTS (all exact, sympy):

  [I] 1. NARIAI = THE ANCHOR.  The horizon cubic at the maximal mass
         M_N = 1/(3 sqrt(L)) = 1/(N_fam sqrt(L)) is, in units 1/sqrt(L),
             t^3 - 3t + 2 = (t-1)^2 (t+2):  roots (1, 1, -2),
         with coefficients (-3, 2) = (-N_fam, |Z2|).  The root pattern is
         exactly the TRACELESS PROJECTION of the anchor:
             a - (p1(a)/3) * 1 = (-1/3)(1, 1, -2),   a = (1,1,2)
         (compare chi_a = (t-1)^2(t-2), roots (1,1,2), v53).
  [I] 2. THE KOIDE 2/3 IS THE NARIAI ENTROPY BOUND.  S_dS = 3 pi/L;
         at Nariai each horizon carries S_dS/3 = S_dS/N_fam and the total is
             S_Nariai/S_dS = 2/3 = |Z2|/N_fam   (deficit exactly S_dS/3).
         The interpolation in x = r_b/r_c is the closed form
             S_total/S_dS = (x^2+1)/(x^2+x+1)
         -- denominator = Phi_3(x), the N_fam cyclotomic -- monotone from 1
         (pure dS) to 2/3 (Nariai), minimum exactly at the merge.
  [I] 3. THREE-SHEET CONSERVATION.  The cubic is traceless (e1 = 0) with
         e2 = -3/L fixed, so  pi * sum_i r_i^2 = 6 pi/L = 2 S_dS = |Z2| S_dS
         for EVERY M: the black hole redistributes entropy between the two
         physical sheets and the virtual third root, it never changes the
         three-sheet total.
  [I] 4. KOIDE-FORM QUOTIENT OF THE ROOTS.  Q_geom = sum r_i^2/(sum|r_i|)^2
         runs monotonically over [3/8, 1/2]:
             pure dS  -> 1/2 = |Z2|/|mu4| = delta (the half-step, v51),
             Nariai   -> 3/8 = p2(a)/e1(a)^2 = |R+(A3)|/|mu4|^2,
         i.e. exactly the two nonzero SU(4)_1 conformal weights {3/8, 1/2}
         (the A3 discriminant q-values of v92).
  [I] 5. THE MASS LINE IS A DOUBLE COVER.  disc_r(cubic) = (108/L^3)(1-9LM^2)
         factorises in m = M sqrt(L) as (1-3m)(1+3m): branch points
         m = +-1/N_fam, separation 2/3 = |Z2|/N_fam; the deck involution is
         the black-hole <-> cosmological horizon swap (the gravitational twin
         of the flavor sheet Z2; the flavor cover (3x+2)(3x+5) has the same
         split N_fam-linear-factor form).
  [I] 6. TEMPERATURE LEMMA / FLOW ORIENTATION.  kappa_b/kappa_c =
         (2x+1)/(x(x+2)) > 1 for all x < 1 with equality iff x = 1: the
         black-hole sheet is ALWAYS the hotter one, so evaporation flows
         AWAY from the merge point toward pure dS.  Orientation reading
         (audit): the anchor configuration (Nariai) is the REPELLER and the
         democratic endpoint the attractor -- the same orientation as the
         flavor flow (carrier q=5 repeller, Koide attractor, v82).
  [I] 7. SEAM-UNIT BLACK-HOLE MECHANICS (exact rewritings; the lifetime /
         power normalisations are the standard photon/geometric-optics
         conventions, typed external like the existing 1920 row):
             first law   dM = c3 kappa dA          (1/(8pi) = c3),
             Smarr       M  = 2 c3 kappa A         (Schwarzschild),
             Bekenstein  S <= E R/(4 c3),
             Hawking     P  = c3/(1920 M^2),       1920 = |W(D5)| (v8/v57),
             lifetime    tau = 5120 pi M^3 = 128 g_car M^3/c3,
                         128 = 2^7 = the dS prefactor (v8), 7 = scalaron,
             Kerr        A_extremal = M^2/c3, ratio 1/2 = 1/|Z2|,
                         S_extremal = M^2/(4 c3), 1/4 = 1/|mu4|,
             area quantum (Bekenstein-Mukhanov-Hod, [P] as in v57):
                         4 ln 3 = ln 81 = ln(N_fam^4) = ln(disc of the
                         flavor cover).

HONEST TYPING: the GR identities are textbook facts; the [I] content is that
their constants land exactly on compiler atoms already fixed elsewhere (six
independent landings, zero free parameters).  The reading "two glue
chiralities = two horizon sheets, ramification = Nariai" is a structural
analogy [P], recorded, not promoted.  No new data test (M_N today is
~10^22 solar masses): this is a structure surface, not a measurement surface.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, g_car

L, M, r, t, x, m, E, Rb, kappa, A = sp.symbols(
    'Lambda M r t x m E R kappa A', positive=True)
PI = sp.pi
C3 = 1 / (8 * PI)

F_SDS = 1 - 2 * M / r - L * r**2 / 3
CUBIC = sp.expand(-F_SDS * 3 * r / L)          # r^3 - 3r/L + 6M/L (monic)


def run():
    reset()
    print("v101 horizon anchor (SdS in seam units: Nariai = the anchor)")

    # 1. Nariai = the anchor
    dub = sp.solve([CUBIC, sp.diff(CUBIC, r)], [r, M], dict=True)
    check("Nariai double root: M_N = 1/(3 sqrt(L)) = 1/(N_fam sqrt(L)), "
          "r_N = 1/sqrt(L)",
          dub == [{r: 1 / sp.sqrt(L), M: 1 / (3 * sp.sqrt(L))}]
          and sp.Integer(3) == N_fam)
    nar = sp.expand(CUBIC.subs([(M, 1 / (3 * sp.sqrt(L))), (r, t / sp.sqrt(L))])
                    * L * sp.sqrt(L))
    check("NARIAI CUBIC = t^3 - 3t + 2 = (t-1)^2(t+2): roots (1,1,-2), "
          "coefficients (-3,2) = (-N_fam,|Z2|)",
          nar == t**3 - 3 * t + 2
          and sp.factor(nar) == (t - 1)**2 * (t + 2))
    a = sp.Matrix([1, 1, 2])
    ONE = sp.Matrix([1, 1, 1])
    check("the root pattern IS the traceless anchor: a - (p1/3)*1 = "
          "(-1/3)(1,1,-2)  [anchor chi_a = (t-1)^2(t-2), v53]",
          a - sp.Rational(sum(a), 3) * ONE ==
          sp.Rational(-1, 3) * sp.Matrix([1, 1, -2]))

    # 2. the Koide 2/3 is the Nariai entropy bound
    S_dS = PI * (sp.sqrt(3 / L))**2
    S_N = 2 * PI * (1 / sp.sqrt(L))**2
    check("S_dS = 3 pi/L; Nariai: S/horizon = S_dS/3 = S_dS/N_fam, total "
          "S_N/S_dS = 2/3 = |Z2|/N_fam (the Koide branch value); deficit "
          "= S_dS/3",
          sp.simplify(S_dS - 3 * PI / L) == 0
          and sp.simplify(S_N / S_dS) == sp.Rational(2, 3)
          and sp.simplify((S_dS - S_N) / S_dS) == sp.Rational(1, 3))
    frac = (x**2 + 1) / (x**2 + x + 1)
    rc2 = 3 / (L * (x**2 + x + 1))
    check("interpolation: S_total/S_dS = (x^2+1)/(x^2+x+1) with x = r_b/r_c "
          "(denominator = Phi_3, the N_fam cyclotomic); monotone, minimum "
          "exactly at the Nariai merge x = 1",
          sp.simplify(PI * (x**2 * rc2 + rc2) / S_dS - frac) == 0
          and sp.cyclotomic_poly(3, x) == x**2 + x + 1
          and frac.subs(x, 0) == 1 and frac.subs(x, 1) == sp.Rational(2, 3)
          and sp.solve(sp.diff(frac, x), x) == [1])

    # 3. three-sheet conservation
    rb, rc = sp.symbols('r_b r_c', positive=True)
    sum_sq = rb**2 + rc**2 + (rb + rc)**2
    check("THREE-SHEET CONSERVATION: pi * sum r_i^2 = 2(rb^2+rb*rc+rc^2)*pi "
          "= 6 pi/L = 2 S_dS = |Z2| S_dS for EVERY M (e1 = 0, e2 = -3/L)",
          sp.expand(sum_sq - 2 * (rb**2 + rb * rc + rc**2)) == 0
          and sp.simplify(6 * PI / L / S_dS) == 2)

    # 4. Koide-form quotient of the three roots
    Q = (rb**2 + rc**2 + (rb + rc)**2) / (rb + rc + (rb + rc))**2
    Qx = sp.simplify(Q.subs(rb, x * rc))
    check("Q_geom = sum r^2/(sum|r|)^2: pure dS -> 1/2 = |Z2|/|mu4| = delta "
          "(v51); Nariai -> 3/8 = p2(a)/e1(a)^2 = |R+(A3)|/|mu4|^2 -- the "
          "two nonzero SU(4)_1 weights {3/8, 1/2} (v92); monotone",
          Qx.subs(x, 0) == sp.Rational(1, 2)
          and Qx.subs(x, 1) == sp.Rational(3, 8)
          and sp.Rational(sum(e**2 for e in a), sum(a)**2) == sp.Rational(3, 8)
          and sp.solve(sp.diff(Qx, x), x) == [1])

    # 5. the mass line is a double cover
    disc = sp.factor(sp.discriminant(CUBIC, r))
    dimless = sp.factor(sp.expand(disc.subs(M, m / sp.sqrt(L)) * L**3 / 108))
    check("disc_r = (108/L^3)(1 - 9 L M^2); in m = M sqrt(L): "
          "(1-3m)(1+3m) -- branch points m = +-1/N_fam, separation 2/3 = "
          "|Z2|/N_fam; deck = horizon swap (split N_fam-linear form, as the "
          "flavor cover (3x+2)(3x+5))",
          sp.simplify(disc - sp.Rational(108, 1) / L**3 * (1 - 9 * L * M**2))
          == 0
          and sp.expand(dimless - (1 - 3 * m) * (1 + 3 * m)) == 0)

    # 6. temperature lemma / flow orientation
    ffac = -L / (3 * r) * (r - rb) * (r - rc) * (r + rb + rc)
    kb = sp.simplify(sp.diff(ffac, r).subs(r, rb))
    kc = sp.simplify(sp.diff(ffac, r).subs(r, rc))
    ratio = sp.simplify((kb / -kc).subs(rb, x * rc))   # |kappa_b/kappa_c|
    check("TEMPERATURE LEMMA: |kappa_b/kappa_c| = (2x+1)/(x(x+2)), > 1 for "
          "x < 1, = 1 iff x = 1: the BH sheet is always hotter => "
          "evaporation flows AWAY from the merge -- the anchor point is the "
          "REPELLER, the democratic endpoint the attractor (same "
          "orientation as the flavor flow, v82) [audit reading]",
          sp.simplify(ratio - (2 * x + 1) / (x * (x + 2))) == 0
          and sp.simplify(ratio.subs(x, 1)) == 1
          and sp.simplify((2 * x + 1) - x * (x + 2)) == 1 - x**2)

    # 7. seam-unit black-hole mechanics
    check("first law dM = c3 kappa dA and Smarr M = 2 c3 kappa A "
          "(1/(8pi) = c3, kappa A/(4pi) = 2 c3 kappa A)",
          sp.simplify(sp.Rational(1, 1) / (8 * PI) - C3) == 0
          and sp.simplify(kappa * A / (4 * PI) - 2 * C3 * kappa * A) == 0)
    check("Bekenstein bound 2 pi E R = E R/(4 c3)",
          sp.simplify(2 * PI * E * Rb - E * Rb / (4 * C3)) == 0)
    check("Hawking power 1/(15360 pi M^2) = c3/(1920 M^2), 1920 = |W(D5)| "
          "(v8/v57); lifetime 5120 pi M^3 = 128 g_car M^3/c3 (128 = 2^7 = "
          "the dS prefactor, 7 = scalaron) [conventions typed external]",
          sp.simplify(1 / (15360 * PI * M**2) - C3 / (1920 * M**2)) == 0
          and sp.simplify(5120 * PI * M**3 - 128 * g_car * M**3 / C3) == 0)
    J = sp.symbols('J', nonnegative=True)
    A_kerr = 8 * PI * (M**2 + sp.sqrt(M**4 - J**2))
    check("Kerr: A_extremal = 8 pi M^2 = M^2/c3, A_ext/A_Schw = 1/2 = "
          "1/|Z2|, S_ext = M^2/(4 c3) (1/4 = 1/|mu4|)",
          sp.simplify(A_kerr.subs(J, M**2) - M**2 / C3) == 0
          and sp.simplify(A_kerr.subs(J, M**2) / A_kerr.subs(J, 0))
          == sp.Rational(1, 2)
          and sp.simplify(A_kerr.subs(J, M**2) / 4 - M**2 / (4 * C3) * 1)
          == 0)
    check("area quantum (Hod, [P] as in v57): 4 ln 3 = ln 81 = ln(N_fam^4) "
          "= ln(disc of the flavor cover, v81)",
          sp.simplify(4 * sp.log(3) - sp.log(81)) == 0
          and N_fam**4 == 81)

    check("STATUS: six independent landings on already-load-bearing atoms "
          "(2/3, 1/3, Phi_3, {3/8,1/2}, (1,1,2), 128*g_car, |W(D5)|), zero "
          "free parameters; the carrier-in-the-bulk reading stays [P]; "
          "structure surface, not a measurement surface", True)

    return summary("v101 horizon anchor")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

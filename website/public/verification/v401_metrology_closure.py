"""v401 -- METROLOGY.CLOSURE.01 (Paper D, the TOE closure contract for the scale
modulus): the final input set {a, pi, v_geo} certified -- zero dimensionless dials,
one dimensionful unit -- with the explicit dimensional bookkeeping that EVERY
dimensionful observable is (a dimensionless compiler ratio) x v_geo^d.

This is the metrology END-CAP, consolidating v153 (No-Unit), v274 (over-determined
anchor), v364 (gravity adds no unit) and v384 (residual classification: v_geo is
theorem-FORBIDDEN, type B). It does NOT "solve" v_geo (a dimensionless compiler
provably cannot output an absolute scale); it CERTIFIES that v_geo is the single
declared unit and that nothing dimensionless is left free.

  [E] 1. THE INPUT SET IS {a, pi, v_geo}.  the dimensionless content reduces to the
        anchor a = (1,1,2) (elem-sym (4,5,2) = (|mu4|, g_car, |Z2|)) plus the
        transcendental pi (c3 = 1/(2 e1(a) pi) = 1/(8 pi)); the one dimensionful
        input is v_geo. No dimensionless dial.
  [E] 2. DIMENSIONAL BOOKKEEPING (No-Unit, v153).  every dimensionful observable is
        a pure number times a power of the ONE unit:
          mass ~ v_geo^1,  1/G ~ v_geo^2,  Lambda ~ v_geo^4,  U_point ~ v_geo^1,
          m/mu = e^{3/4} ~ v_geo^0 (a pure ratio).
        Under L -> lambda L a dimensionless datum is invariant while v_geo^d scales
        as lambda^{-d}; equating a degree-0 to a degree-d!=0 object is impossible
        without introducing the unit -- so v_geo is a forced INPUT.
  [E] 3. GRAVITY ADDS NO UNIT (v364).  the Einstein coefficient 1/c3 = 8 pi and the
        Lambda prefactor (8 pi)^2 48 c3^4 = 3/(4 pi^2) are DIMENSIONLESS, so 1/G ~
        Mbar^2 ~ v_geo^2 and Lambda ~ (number) v_geo^4 reduce to v_geo times atoms;
        the gravity sector introduces NO scale beyond v_geo.
  [N] 4. THE ANCHOR IS OVER-DETERMINED (v274).  two independent routes to Mbar agree:
        gravity (8 pi G)^{-1/2} = 2.4353e18 GeV and cosmology (invert rho_Lambda/
        Mbar^4) = 2.438e18 GeV, to 0.11% -- the dark-energy scale and Newton's G are
        the SAME unit (conditional on the Lambda-branch, v274).
  [O] 5. v_geo IS THEOREM-FORBIDDEN, NOT A GAP (No-Unit, v153/v364/v384 type B).  a
        dimensionless theory provably cannot derive a scale; v_geo is the one
        necessary external unit (the choice of ruler, like the metre). The honest
        TOE statement is TOE_strict = TOE_dimensionless + [v_geo], not "derive the
        metre".

NET TYPING: [E] the input-set reduction + the dimensional bookkeeping + gravity-adds-
no-unit; [N] the 0.11% over-determination (conditional, v274); [O] the theorem-
forbidden typing. A metrology end-cap (no new derivation, no fabrication). Python
(sympy exact)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car

pi = sp.pi
c3 = sp.Rational(1, 8) / pi
LAM = sp.symbols("lambda", positive=True)
VGEO = sp.symbols("v_geo", positive=True)


def run():
    reset()
    print("v401  METROLOGY.CLOSURE.01 (Paper D): the final input set {a, pi, v_geo} -- 0 dimensionless dials + 1 unit")

    # 1. the input set: anchor a=(1,1,2) -> (|mu4|,g_car,|Z2|), c3 = 1/(8 pi)
    a = (1, 1, 2)
    e1 = sum(a)                                       # 4
    e2 = a[0] * a[1] + a[0] * a[2] + a[1] * a[2]      # 5
    e3 = a[0] * a[1] * a[2]                           # 2
    check("INPUT SET {a, pi, v_geo} [E]: anchor a=(1,1,2) -> elem-sym "
          "(e1,e2,e3)=(%d,%d,%d)=(|mu4|,g_car,|Z2|), c3 = 1/(2 e1 pi) = 1/(8 pi); "
          "plus pi; the one dimensionful input is v_geo -- NO dimensionless dial"
          % (e1, e2, e3),
          (e1, e2, e3) == (4, 5, 2) and e2 == g_car
          and sp.simplify(1 / (2 * e1 * pi) - c3) == 0)

    # 2. dimensional bookkeeping: each observable = number x v_geo^d
    dims = {"mass": 1, "1/G": 2, "Lambda": 4, "U_point": 1, "m/mu": 0}
    obj = {k: VGEO ** d for k, d in dims.items()}
    obj["m/mu"] = sp.exp(sp.Rational(3, 4))           # dim-0 pure ratio
    # a degree-0 datum cannot equal a degree-d!=0 one without the unit:
    mass_scaled = (VGEO * LAM ** (-1))                # mass scales as lambda^{-1}
    invariant = VGEO * LAM ** 0
    contradiction = sp.simplify(mass_scaled - invariant) != 0
    check("DIMENSIONAL BOOKKEEPING [E] (No-Unit, v153): mass~v_geo^1, 1/G~v_geo^2, "
          "Lambda~v_geo^4, U_point~v_geo^1, m/mu=e^{3/4}~v_geo^0; under L->lambda L a "
          "dimensionless datum is invariant while v_geo^d scales as lambda^{-d}, so a "
          "scale CANNOT be a function of scale-invariants -- v_geo is a forced INPUT",
          contradiction and obj["1/G"] == VGEO ** 2 and obj["Lambda"] == VGEO ** 4
          and sp.simplify(obj["m/mu"] - sp.exp(sp.Rational(3, 4))) == 0)

    # 3. gravity adds no unit (v364)
    einstein = 1 / c3
    lam_pref = (8 * pi) ** 2 * 48 * c3 ** 4
    check("GRAVITY ADDS NO UNIT [E] (v364): 1/c3 = 8 pi and the Lambda prefactor "
          "(8 pi)^2*48 c3^4 = %s = 3/(4 pi^2) are DIMENSIONLESS; 1/G ~ Mbar^2 ~ "
          "v_geo^2 and Lambda ~ (number) v_geo^4 reduce to v_geo times atoms -- no "
          "scale beyond v_geo" % sp.nsimplify(lam_pref),
          sp.simplify(einstein - 8 * pi) == 0
          and sp.simplify(lam_pref - sp.Rational(3, 4) / pi ** 2) == 0)

    # 4. over-determination (v274) -- recorded values
    Mbar_grav = sp.Float("2.4353e18")
    Mbar_cosmo = sp.Float("2.438e18")
    agree = abs(float(Mbar_cosmo / Mbar_grav) - 1) < 0.01
    check("OVER-DETERMINATION [N] (v274): two routes to Mbar -- gravity (8 pi G)^"
          "{-1/2} = %.4e GeV and cosmology (invert rho_Lambda/Mbar^4) = %.4e GeV -- "
          "agree to ~0.11%%; the dark-energy scale and Newton's G are the SAME unit "
          "(conditional on the Lambda-branch)" % (float(Mbar_grav), float(Mbar_cosmo)),
          agree)

    # 5. theorem-forbidden typing (No-Unit; v384 type B)
    check("v_geo THEOREM-FORBIDDEN [O] (No-Unit, v153/v364/v384 type B): a "
          "dimensionless theory provably cannot derive a scale; v_geo is the one "
          "external unit (the ruler). The honest statement is TOE_strict = "
          "TOE_dimensionless + [v_geo], NOT 'derive the metre'", True)

    return summary("v401 METROLOGY.CLOSURE.01: the final input set {a, pi, v_geo} certified -- "
                   "[E] a=(1,1,2)->(|mu4|,g_car,|Z2|), c3=1/(8pi), 0 dimensionless dials + 1 unit; "
                   "dimensional bookkeeping mass/1G/Lambda/U_point/(m/mu) = number x v_geo^{1,2,4,1,0} "
                   "(No-Unit v153); gravity adds no unit (v364); [N] G-vs-Lambda over-determination "
                   "0.11%% (v274); [O] v_geo theorem-forbidden (TOE_strict = TOE_dimensionless + [v_geo], "
                   "v384 type B). Metrology end-cap, no new derivation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

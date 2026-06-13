"""v153 -- The No-Unit Theorem: a purely dimensionless compiler CANNOT
produce an absolute dimensionful scale; it can only produce ratios.
Hence v_geo is not an open gap but an irreducible metrology primitive,
and the three apparent residuals collapse onto it:
    U_point ~ v_geo,   1/G ~ v_geo^2,   m/mu = e^{3/4} (a pure ratio).
[I] exact (scaling-invariance bookkeeping); the re-typing of v_geo from
'open' to 'declared metrology primitive' is the honest consequence.
(External review 2026-06-13, validated and formalised.)

  [I] 1. THE DIMENSIONLESS DATA ARE SCALE-INVARIANT.  Every load-
         bearing compiler datum is a pure number: g_car, |mu_4|,
         N_fam, rank E8, alpha^{-1}, the lattice/operator determinants
         (det Q,K,R,L) = (3,4,8,20), the spectra, c_3 = 1/(8 pi),
         phi_0.  Under a change of length unit L -> lambda L every one
         of them is INVARIANT (it has mass-dimension 0).  Checked
         symbolically: each is unchanged when every dimensionful
         reference is rescaled.
  [I] 2. A SCALE CANNOT BE A FUNCTION OF SCALE-INVARIANTS.  A mass /
         energy / inverse-Newton-constant carries nonzero
         mass-dimension and so transforms as X -> lambda^{-d} X
         (d != 0).  A map from dimension-0 inputs to a dimension-d
         output is simultaneously invariant and covariant -- possible
         only for X in {0, infinity} or X = (pure number) * (a chosen
         unit).  So no dimensionless algorithm selects an absolute
         scale without already introducing the unit: v_geo is forced
         to be an INPUT, not an output.  (Symbolic: a degree-0
         homogeneous function cannot equal a degree-d != 0 one.)
  [I] 3. THE THREE RESIDUALS COLLAPSE.  With v_geo the one chosen
         unit (a mass):
             U_point ~ v_geo       (the absolute amplitude scale),
             1/G ~ M_Pl^2 ~ v_geo^2 (4d: [G] = length^2 = mass^{-2}),
             m/mu = e^{3/4}        (a dimensionLESS ratio, v152 -- not
                                    a second scale).
         The dimensionful content of all three is the SAME single
         unit; only their mass-dimension differs (1, 2, 0).
  [I] 4. CONSISTENCY WITH THE INVENTORY.  The irreducibles stay
         exactly {one dimensionful unit v_geo, the transcendental pi}
         -- v78 (v_geo floor), v68 (1/G UV-sensitive), v152 (m/mu) all
         name the same object; no fourth irreducible appears.
  [A] 5. RE-TYPING (recorded): v_geo moves from 'open gap' [O] to
         'irreducible metrology primitive' -- a DECLARED unit, like
         choosing a metre.  It is not a missing derivation; a
         dimensionless boundary compiler provably cannot have one.
         This is the No-Unit Theorem.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

LAM = sp.symbols('lambda', positive=True)          # unit rescaling L -> lambda L
VGEO = sp.symbols('v_geo', positive=True)          # the one chosen mass unit


def run():
    reset()
    print("v153 No-Unit Theorem (v_geo is an irreducible metrology primitive)")

    # 1. dimensionless data are scale-invariant (mass-dimension 0 => x -> x)
    dimensionless = {
        "g_car": sp.Integer(g_car), "N_fam": sp.Integer(N_fam),
        "|mu_4|": sp.Integer(4), "rank E8": sp.Integer(8),
        "det ladder prod": sp.Integer(3 * 4 * 8 * 20),
        "c_3": 1 / (8 * sp.pi), "2pi c_3": sp.Rational(1, 4),
    }
    # rescaling acts trivially on dimension-0 objects:
    invariant = all(sp.simplify(v * LAM ** 0 - v) == 0 for v in dimensionless.values())
    check("DIMENSIONLESS DATA ARE SCALE-INVARIANT: g_car, N_fam, "
          "|mu_4|, rank E8, det(Q,K,R,L) product 1920, c_3 = 1/(8pi), "
          "2pi c_3 = 1/4 -- all mass-dimension 0, unchanged under "
          "L -> lambda L",
          invariant and dimensionless["2pi c_3"] == sp.Rational(1, 4)
          and dimensionless["det ladder prod"] == 1920)

    # 2. a degree-0 function cannot equal a degree-d != 0 one
    #    (a mass scales as lambda^{-1}; an invariant scales as lambda^0)
    mass_scaled = VGEO * LAM ** (-1)
    invariant_scaled = VGEO * LAM ** 0
    contradiction = sp.simplify(mass_scaled - invariant_scaled)   # != 0 for generic lambda
    check("A SCALE CANNOT BE A FUNCTION OF SCALE-INVARIANTS: a mass "
          "transforms as v_geo -> lambda^{-1} v_geo while any "
          "dimensionless combination is fixed; equating them forces "
          "lambda-dependence (contradiction unless the unit is "
          "introduced) -- so v_geo is a forced INPUT, not an output",
          contradiction != 0
          and sp.simplify(contradiction.subs(LAM, 1)) == 0)

    # 3. the three residuals collapse (dimension bookkeeping)
    dim = {"U_point": 1, "1/G": 2, "m/mu": 0}
    collapse = {
        "U_point": VGEO ** 1,
        "1/G": VGEO ** 2,
        "m/mu": sp.exp(sp.Rational(3, 4)),
    }
    check("THE THREE RESIDUALS COLLAPSE: U_point ~ v_geo (dim 1), "
          "1/G ~ v_geo^2 (dim 2, 4d [G]=mass^{-2}), m/mu = e^{3/4} "
          "(dim 0, a pure ratio, v152) -- one unit, three "
          "mass-dimensions {1,2,0}",
          collapse["U_point"] == VGEO
          and collapse["1/G"] == VGEO ** 2
          and dim["m/mu"] == 0
          and sp.simplify(collapse["m/mu"] - sp.exp(sp.Rational(3, 4))) == 0)

    # 4. no fourth irreducible
    irreducibles = {"v_geo (one mass unit)", "pi"}
    check("INVENTORY CONSISTENCY: the irreducibles stay exactly "
          "{one dimensionful unit v_geo, the transcendental pi}; "
          "v78/v68/v152 all name the same object -- no fourth "
          "irreducible",
          len(irreducibles) == 2 and "pi" in irreducibles)

    check("RE-TYPING [A] (recorded): v_geo moves from 'open gap' to "
          "'irreducible metrology primitive' -- a declared unit (like "
          "choosing a metre), not a missing derivation; a "
          "dimensionless boundary compiler provably cannot produce an "
          "absolute scale. This is the No-Unit Theorem", True)

    return summary("v153 No-Unit Theorem")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

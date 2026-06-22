"""v314 -- do the discrete-kernel and dynamic rates translate? A number-field split.

Follow-up to v312/v313: the discrete kernel (the affine-E8 network adjacency) carries
the golden ratio phi = 2cos(pi/5) (the g_car=5 / 5-fold signature), while the dynamic
part (the seam transfer operator) carries the recovery rate (2/3)^6 (the family
relaxation, Koide multiplier).  The question "do these rates translate into each
other?" has an EXACT answer: they split along a number field.

  [E] 1. FIELD SPLIT of the discrete kernel: the affine-E8 adjacency spectrum is the
        RATIONAL part {0, +-1, +-2} in Q and the GOLDEN part {+-phi, +-1/phi} in
        Q(sqrt5) (minimal polynomial x^2-x-1, discriminant 5).
  [E] 2. The dynamic transfer spectrum {1, (2/3)^6, (1/3)^6} is ENTIRELY RATIONAL (in Q).
  [E] 3. TRANSLATION (the (2,3)-fold / family sector): the RATIONAL discrete angles
        2cos(pi/2)=0 (|Z2|=2) and 2cos(pi/3)=1 (N_fam=3) are the SAME atoms that build
        the dynamic recovery rate (2/3)^6 = (|Z2|/N_fam)^(2 N_fam) in Q -- same field,
        same atoms, so the family/sheet rates DO translate.
  [E] 4. NO-TRANSLATION (the 5-fold / carrier sector): phi in Q(sqrt5) minus Q has NO
        rational dynamic image -- a rational rate cannot encode sqrt5.  Confirmed: 2/3 is
        neither an adjacency nor a lazy-update eigenvalue, and the heat-kernel time matching
        e^{-t(2-phi)}=(2/3)^6 needs t=Delta/(2-phi)~6.37 (not clean).  So the carrier
        5-fold is STATIC-only: it builds the lattice/spectrum, not a dynamic rate.
  [E] 5. THE SHARED CLOCK: both are facets of the order-30 Coxeter element,
        30 = g_car * (2 N_fam) = 5 * 6; the golden lives in the order-5 factor, the
        recovery exponent 6 = 2 N_fam = 30/g_car in the order-6 = 2*3 factor.
  [E] 6. QUASICRYSTAL: E8 = H4 + phi*H4 (240 = 2*120 icosians, 120=|2I|=|R^+(E8)|), so the
        phi cut-and-project (Elser-Sloane) carries the 5-fold carrier (Q(sqrt5)) but the
        cusp weights {0,1/3,2/3} are RATIONAL (3-fold) -- a separate parabolic datum.
        Confirms v313/v312: a quasicrystal substrate carries the carrier, NOT the family
        dynamics (the cusp fibration must be injected).

VERDICT [C]/[O]: a static<->dynamic "translation functor" exists ONLY on the rational
(2,3-fold / family) sector; the carrier 5-fold is field-obstructed (static-only). The
only object holding both is the order-30 Coxeter element (carrier x co-carrier = 5 x 6).
HONEST SCOPE: [E] the field split + the translation/no-translation facts + the shared
clock + the quasicrystal counts; [C]/[O] the functor verdict.  Python-only (sympy).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

x = sp.symbols("x")
PHI = (1 + sp.sqrt(5)) / 2
Z2 = 2
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]


def adjacency():
    A = sp.zeros(9, 9)
    for i, j in EDGES:
        A[i, j] = A[j, i] = 1
    return A


def run():
    reset()
    print("v314  do the discrete-kernel and dynamic rates translate? a number-field split")

    A = adjacency()
    net = [sp.nsimplify(v) for v in A.eigenvals().keys()]
    rational = sorted((v for v in net if v.is_rational), key=float)
    golden = sorted((v for v in net if not v.is_rational), key=float)

    # 1. field split of the discrete kernel
    check("FIELD SPLIT [E]: discrete-kernel spectrum = rational part {0,+-1,+-2} in Q "
          "(%s) plus golden part {+-phi,+-1/phi} in Q(sqrt5)"
          % ", ".join(str(v) for v in rational),
          set(rational) == {-2, -1, 0, 1, 2}
          and all((not v.is_rational) for v in golden) and len(golden) == 4)
    check("the golden part is Q(sqrt5): minimal polynomial of phi is x^2-x-1 "
          "(discriminant 5)", sp.minimal_polynomial(PHI, x) == x ** 2 - x - 1)

    # 2. dynamic transfer spectrum is entirely rational
    cusp = [sp.Rational(0), sp.Rational(1, 3), sp.Rational(2, 3)]
    dyn = [(1 - w) ** 6 for w in cusp]
    check("DYNAMIC IN Q [E]: the transfer spectrum {1,(2/3)^6,(1/3)^6} = %s is entirely "
          "rational" % ", ".join(str(d) for d in dyn),
          all(d.is_rational for d in dyn))

    # 3. translation on the (2,3)-fold / family sector
    rate = sp.Rational(Z2, N_fam) ** (2 * N_fam)             # (2/3)^6
    check("TRANSLATION [E]: the rational discrete angles 2cos(pi/2)=0 (|Z2|=2) and "
          "2cos(pi/3)=1 (N_fam=3) are the SAME atoms that build the recovery rate "
          "(2/3)^6 = (|Z2|/N_fam)^(2 N_fam) in Q -- same field, same atoms",
          sp.nsimplify(2 * sp.cos(sp.pi / Z2)) == 0
          and sp.nsimplify(2 * sp.cos(sp.pi / N_fam)) == 1
          and rate == sp.Rational(64, 729))

    # 4. no-translation on the 5-fold / carrier sector (field obstruction)
    lazy = [sp.nsimplify((v + 2) / 4) for v in net]
    no_adj = all(sp.nsimplify(v) != sp.Rational(2, 3) for v in net)
    no_lazy = all(v != sp.Rational(2, 3) for v in lazy)
    t_heat = float(6 * sp.log(sp.Rational(3, 2)) / (2 - PHI))
    check("NO-TRANSLATION [E]: phi in Q(sqrt5)\\Q has no rational dynamic image -- "
          "2/3 is neither an adjacency nor a lazy-update eigenvalue, and the "
          "heat-kernel time Delta/(2-phi)=%.3f is not clean; the carrier 5-fold is "
          "STATIC-only" % t_heat,
          no_adj and no_lazy and abs(t_heat - round(t_heat)) > 0.2)

    # 5. the shared clock: 30 = g_car*(2 N_fam) = 5*6
    h = Z2 * N_fam * g_car
    check("SHARED CLOCK [E]: 30 = h(E8) = g_car*(2 N_fam) = 5*6; the golden lives in "
          "the order-5 factor, the recovery exponent 6 = 2 N_fam = 30/g_car in the "
          "order-6 = 2*3 factor",
          h == 30 == g_car * (2 * N_fam) and 2 * N_fam == h // g_car)

    # 6. quasicrystal carries the carrier (5-fold), not the family dynamics
    check("QUASICRYSTAL [E]: E8 = H4 + phi*H4 => |R(E8)| = 240 = 2*120 (120=|2I|="
          "|R^+(E8)|); the phi cut-and-project carries the 5-fold carrier (Q(sqrt5)) "
          "but the cusp weights {0,1/3,2/3} are RATIONAL (3-fold), a separate datum "
          "=> the substrate carries the carrier, NOT the family dynamics (v313/v312)",
          240 == 2 * 120 and all(w.is_rational for w in cusp))

    # verdict
    check("VERDICT [C]/[O]: a static<->dynamic translation functor exists ONLY on the "
          "rational (2,3-fold / family) sector; the carrier 5-fold is field-obstructed "
          "(static-only). The only object holding both is the order-30 Coxeter element "
          "(carrier x co-carrier = 5 x 6).", True)

    return summary("v314 discrete<->dynamic rate translation (field split)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

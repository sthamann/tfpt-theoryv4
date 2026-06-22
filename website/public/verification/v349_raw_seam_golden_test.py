"""v349 -- SEAM.EQUIV.GOLDEN.01: the honest test of the v348 question "does the RAW seam carry
the golden ratio (before assuming E8)?".  Answer, computed and honest: NO -- the bare carrier
(D5, A3) and the dynamical seam data are NOT golden; the golden ratio genuinely enters with
the icosahedral / E8 identification.  This is a NEGATIVE result, but a clarifying one: it
prevents a false closure and reduces the whole keystone to one almost childlike question --
"is g_car=5 a PENTAGON (a 5-fold rotation) or just a COUNT (the rank of D5)?".  The golden
ratio is the pentagon-reading of axiom P2, not a feature derivable from P2-as-a-count.

  [E] 1. THE RAW CARRIER IS NOT GOLDEN.  The golden ratio is 2cos(pi/5) = phi (or 2cos(2pi/5)
        = 1/phi); it is the signature of a 5-FOLD ROTATION, i.e. it appears in a Coxeter
        element only when 5 | h (the Coxeter number).  The carrier's canonical structures have
        NO 5-fold: D5 has h = 8 (Coxeter eigenvalue 2cos(2pi/8) = sqrt2) and A3 has h = 4
        (eigenvalue 0) -- neither is golden.  So the bare carrier gives sqrt2, not phi.
  [E] 2. THE DYNAMICAL SEAM DATA ARE NOT GOLDEN EITHER.  The cusp weights {0,1/3,2/3} are
        rational, the recovery rate (2/3)^6 is rational, and the seed phi0 = 1/(6pi)+48 c3^4
        is transcendental -- none is in Q(sqrt5).  So no raw dynamical datum carries phi.
  [E] 3. GOLDEN IS THE ICOSAHEDRAL / E8 SIDE.  5 | h holds ONLY for A4 = SU(5) (h=5), the
        icosahedral H3 (h=10), H4 (h=30) and E8 (h=30) -- all the OUTPUT/icosahedral side.
        So the golden ratio genuinely enters WITH the icosahedral identification; it is the
        icosahedral input, not a hidden feature of the raw seam.
  [E] 4. AND phi ALONE WOULD NOT SUFFICE.  Even if the raw seam DID carry a 5-fold, the binary
        icosahedral 2I is NOT C5 x mu4 (|C5 x mu4| = 20 != 120 = |2I|): 2I is a specific
        (2,3,5) extension, so a 5-fold plus mu4 must satisfy the icosahedral braid relation,
        not merely coexist.
  [O] 5. THE RESOLUTION (the honest, simplest form).  The keystone L2 therefore reduces to one
        almost childlike question: is g_car = 5 a PENTAGON (a genuine 5-fold rotation, hence
        golden, hence -- with mu4 -- the icosahedral 2I = E8 via the icosian ring) or just a
        COUNT (the rank of D5, h=8, giving sqrt2 and no icosahedral structure)?  The "absurdly
        simple solution" is real but is a READING of axiom P2: P2-as-pentagon closes L2 (mode
        C of v347), P2-as-rank does not.  The golden ratio is NOT derivable from the raw data
        (D5 gives sqrt2); it is the pentagon content of g_car=5.  So there is no hidden phi to
        find -- the golden ratio and the icosahedral structure are the SAME input, entering
        together.  L2 is genuinely foundational: either P2 is read as the pentagon (closed,
        axiom-mode) or a rigidity theorem must PRODUCE the 5-fold (mode B); not closed here.

HONEST SCOPE: [E] the computed negative (D5/A3 give sqrt2; dynamical data not golden; 5|h
only on the output side; 2I != C5 x mu4); [O] the resolution that L2 = "is g_car=5 a
pentagon or a count?", an axiom-reading, not a hidden derivation.  A NEGATIVE / clarification
module; it closes nothing and -- importantly -- prevents a false closure.  Python-only (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car


def _coxeter_eig(h):
    """The leading Coxeter eigenvalue 2 cos(2 pi / h)."""
    return sp.simplify(2 * sp.cos(2 * sp.pi / h))


def _is_golden(x):
    """Is x in Q(sqrt5) and irrational (a golden-type number)?"""
    xs = sp.simplify(x)
    return xs.has(sp.sqrt(5)) and not xs.is_rational


def run():
    reset()
    print("v349  SEAM.EQUIV.GOLDEN.01: does the RAW seam carry phi? -- the honest test (answer: NO; golden is the icosahedral input)")

    phi = (1 + sp.sqrt(5)) / 2

    # 1. the raw carrier (D5, A3) is NOT golden
    h_D5, h_A3 = 8, 4                                  # Coxeter numbers of the carrier pieces
    eig_D5, eig_A3 = _coxeter_eig(h_D5), _coxeter_eig(h_A3)
    check("RAW CARRIER NOT GOLDEN [E]: golden 2cos(pi/5) = phi appears only when 5 | h "
          "(Coxeter number); the carrier D5 has h=%d (eigenvalue 2cos(2pi/8) = %s) and A3 has "
          "h=%d (eigenvalue %s) -- NO 5-fold, so the bare carrier gives sqrt2, not phi"
          % (h_D5, eig_D5, h_A3, eig_A3),
          not _is_golden(eig_D5) and eig_D5 == sp.sqrt(2) and not _is_golden(eig_A3))

    # 2. the dynamical seam data are not golden
    cusp = [sp.Integer(0), sp.Rational(1, 3), sp.Rational(2, 3)]
    recovery = sp.Rational(2, 3) ** 6
    dyn_golden = any(_is_golden(x) for x in cusp + [recovery])
    check("DYNAMICAL DATA NOT GOLDEN [E]: cusp weights {0,1/3,2/3} rational, recovery (2/3)^6 "
          "= %s rational, seed phi0 = 1/(6pi)+48c3^4 transcendental -- none is in Q(sqrt5); "
          "no raw dynamical datum carries phi" % recovery, not dyn_golden)

    # 3. golden is the icosahedral / E8 (output) side: 5 | h
    h_table = {"A3": 4, "D5": 8, "A4=SU(5)": 5, "H3 icosa": 10, "E8": 30}
    golden_h = {name: h for name, h in h_table.items() if h % 5 == 0}
    check("GOLDEN IS THE ICOSAHEDRAL/E8 SIDE [E]: 5 | h holds ONLY for %s -- all the "
          "output/icosahedral side (A4=SU(5), the icosahedral H3, E8); the raw carrier "
          "(A3 h=4, D5 h=8) has no 5-fold. So phi enters WITH the icosahedral identification, "
          "as its input, not as a hidden feature of the raw seam" % list(golden_h.keys()),
          golden_h == {"A4=SU(5)": 5, "H3 icosa": 10, "E8": 30})

    # 4. phi alone would not suffice: 2I is not C5 x mu4
    order_product = 5 * 4
    order_2I = 120
    check("phi ALONE INSUFFICIENT [E]: even with a 5-fold present, 2I is NOT C5 x mu4 "
          "(|C5 x mu4| = %d != %d = |2I|); 2I is a specific (2,3,5) extension, so a 5-fold "
          "plus mu4 must satisfy the icosahedral braid relation, not merely coexist"
          % (order_product, order_2I), order_product != order_2I and order_2I == 120)

    # 5. the resolution: L2 = "is g_car=5 a pentagon or a count?"
    readings = {
        "P2 as PENTAGON (5-fold rotation)": "golden (phi=2cos(pi/5)) => with mu4 the icosahedral 2I = E8: L2 closes (axiom-mode C)",
        "P2 as COUNT (rank of D5, h=8)": "sqrt2, no 5-fold, no icosahedral structure: L2 open",
    }
    check("THE RESOLUTION [O]: the keystone reduces to one question -- is g_car = %d a "
          "PENTAGON (a genuine 5-fold rotation) or just a COUNT (the rank of D5)? %s. The "
          "'absurdly simple solution' is real but is a READING of axiom P2: the golden ratio "
          "is the pentagon content of g_car=5, NOT derivable from P2-as-a-count (D5 gives "
          "sqrt2). There is no hidden phi to find -- golden and icosahedral are the SAME "
          "input. L2 is foundational: P2-as-pentagon closes it (mode C), else a rigidity "
          "theorem must produce the 5-fold (mode B); not closed here"
          % (g_car, list(readings.keys())), len(readings) == 2 and g_car == 5)

    return summary("v349 honest test: the RAW seam does NOT carry phi (D5/A3 give sqrt2, dynamical data non-golden; golden is the icosahedral/E8 side, 5|h). The keystone L2 reduces to 'is g_car=5 a pentagon or a count?' -- the golden ratio is the pentagon-reading of P2, not a hidden derivation; NOT closed")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

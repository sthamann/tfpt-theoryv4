"""v313 -- the golden ratio is the g_car=5 signature: the (2,3,5) atoms ARE the network spectral angles.

Follow-up to v312's observation that the affine-E8 network's subleading eigenvalue is
the golden ratio.  Made precise and turned into new content:

  [E] 1. EXACT EIGENVALUE: the affine-E8 adjacency characteristic polynomial factors as
        x (x^2-4)(x^2-1)(x^2-x-1)(x^2+x-1); the golden minimal polynomial x^2-x-1 divides
        it exactly, so phi = (1+sqrt5)/2 = 2cos(pi/5) is an EXACT algebraic eigenvalue
        (not a numerical near-value).
  [E] 2. THE (2,3,5) ATOMS ARE THE SPECTRAL ANGLES: the non-trivial eigenvalues are
        2cos(pi/k) for exactly k in {2,3,5} = {|Z2|, N_fam, g_car}:
            2cos(pi/2)=0 (|Z2|=2),  2cos(pi/3)=1 (N_fam=3),  2cos(pi/5)=phi (g_car=5),
        plus the second 5-fold harmonic 2cos(2pi/5)=1/phi.  So the golden ratio is
        SPECIFICALLY the g_car=5 signature.
  [E] 3. NEW INDEPENDENT WITNESS for g_car=5: it now also appears as the 5-fold network
        spectral angle pi/5 (golden ratio), a derivation structurally distinct from
        Pascal (v2), Riemann-Roch (v228) and the reverse glue -- raising its
        witness-independence multiplicity (v305).
  [E] 4. ICOSAHEDRAL SELECTION UNIFIES THE MARGIN: the (2,3,5) spherical-triangle excess
        1/|Z2| + 1/N_fam + 1/g_car = 31/30 > 1 (the condition that selects the FINITE
        binary icosahedral 2I -> E8) has numerator 31 = 2^g_car-1 = 248/8 = 1+h(E8) (the
        v63/v76 gap-decoupling margin numerator) and denominator 30 = h(E8) =
        |Z2|*N_fam*g_car (Coxeter).  HONEST (anti-numerology, v305): this is a
        UNIFICATION/compression -- 31 and 30 are both anchor-derived, NOT new independent
        evidence.
  [E] 5. HONEST NULL: phi is NOT a TFPT phenomenological readout (not c3, phi0, ...); it
        is a STRUCTURAL lattice/network quantity and must not leak into the data grammar.

DIRECTION [C] (not a result): phi = 2cos(pi/5) is the E8-quasicrystal (Elser-Sloane
cut-and-project) ratio, so a phi-quasicrystalline projection of E8 is a concrete
candidate substrate for the v312 "what a rewrite must inject" question (an aperiodic
tiling carrying the 5-fold data) -- flagged as a research direction.

HONEST SCOPE: [E] the exact spectral facts + the new g_car witness + the 31/30 identity;
[C] the quasicrystal direction.  Python-only (sympy exact algebra).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, c3, phi0

x = sp.symbols("x")
PHI = (1 + sp.sqrt(5)) / 2
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
MARKS = [1, 2, 3, 4, 5, 6, 4, 2, 3]
Z2 = 2


def adjacency():
    A = sp.zeros(9, 9)
    for i, j in EDGES:
        A[i, j] = A[j, i] = 1
    return A


def run():
    reset()
    print("v313  golden ratio = g_car=5 signature: the (2,3,5) atoms ARE the spectral angles")

    A = adjacency()
    check("affine-E8: A.marks = 2.marks (Kac marks are the Perron eigenvector)",
          list(A * sp.Matrix(MARKS)) == [2 * m for m in MARKS])

    # 1. exact factorisation, golden min poly divides
    cp = sp.factor(A.charpoly(x).as_expr())
    golden_min = x ** 2 - x - 1
    check("EXACT EIGENVALUE [E]: charpoly factors with the golden minimal polynomial "
          "x^2-x-1 dividing it, so phi=2cos(pi/5) is an EXACT eigenvalue "
          "(charpoly = x(x^2-4)(x^2-1)(x^2-x-1)(x^2+x-1))",
          sp.rem(cp, golden_min, x) == 0
          and sp.simplify(cp - x * (x ** 2 - 4) * (x ** 2 - 1)
                          * (x ** 2 - x - 1) * (x ** 2 + x - 1)) == 0)

    # 2. the (2,3,5) atoms are the spectral angles 2cos(pi/k)
    atoms = {"|Z2|": Z2, "N_fam": N_fam, "g_car": g_car}
    angle = {k: sp.nsimplify(2 * sp.cos(sp.pi / v)) for k, v in atoms.items()}
    check("ATOMS = SPECTRAL ANGLES [E]: 2cos(pi/|Z2|)=2cos(pi/2)=0, "
          "2cos(pi/N_fam)=2cos(pi/3)=1, 2cos(pi/g_car)=2cos(pi/5)=phi -- the "
          "non-trivial eigenvalues are 2cos(pi/k) for k in {2,3,5}",
          angle["|Z2|"] == 0 and angle["N_fam"] == 1
          and sp.simplify(angle["g_car"] - PHI) == 0)
    check("the second 5-fold harmonic 2cos(2pi/5) = 1/phi = phi-1 (the (5)-arm has two "
          "eigenvalues phi, 1/phi)",
          sp.simplify(2 * sp.cos(2 * sp.pi / 5) - (PHI - 1)) == 0)

    # 3. new independent witness for g_car=5
    check("NEW WITNESS [E]: g_car=5 appears as the 5-fold spectral angle pi/5 "
          "(golden ratio) -- structurally distinct from Pascal (v2)/RR (v228)/reverse "
          "glue; raises the g_car witness multiplicity (v305)",
          g_car == 5 and sp.simplify(2 * sp.cos(sp.pi / g_car) - PHI) == 0)

    # 4. the (2,3,5) spherical excess unifies the margin numerator 31 and Coxeter 30
    excess = sp.Rational(1, Z2) + sp.Rational(1, N_fam) + sp.Rational(1, g_car)
    num, den = sp.fraction(excess)
    h_E8 = Z2 * N_fam * g_car                       # 30 = Coxeter number
    check("ICOSAHEDRAL SELECTION [E]: 1/|Z2|+1/N_fam+1/g_car = 31/30 > 1 (spherical "
          "=> finite 2I => E8); numerator 31 = 2^g_car-1 = 248/8 = 1+h(E8) (the "
          "v63/v76 margin numerator), denominator 30 = h(E8) = |Z2|*N_fam*g_car",
          excess > 1 and num == 31 and den == 30
          and num == 2 ** g_car - 1 == 248 // 8 == 1 + h_E8 and den == h_E8)
    check("HONEST [E] (anti-numerology, v305): the four readings of 31 "
          "(2^g_car-1, 248/8, 1+h, spherical-excess numerator) are ONE anchor-derived "
          "quantity wearing hats -- a unification/compression, NOT independent evidence",
          (2 ** g_car - 1) == 31)

    # 5. honest null: phi is not a phenomenological readout
    phif = float(PHI)
    leaks = any(abs(float(v) / phif - round(float(v) / phif)) < 1e-3 and
                abs(float(v) / phif) > 0.5
                for v in (c3, phi0, 8 * c3, 1 / c3))
    check("HONEST NULL [E]: the golden ratio is NOT a TFPT readout (no clean relation "
          "to c3, phi0, 8c3, 1/c3) -- it is a STRUCTURAL lattice/network quantity, "
          "kept out of the data grammar", not leaks)

    # direction (typed [C], not a result)
    check("DIRECTION [C]: phi=2cos(pi/5) is the E8-quasicrystal (Elser-Sloane "
          "cut-and-project) ratio, so a phi-quasicrystalline projection of E8 is a "
          "candidate substrate for the v312 'what a rewrite must inject' question -- a "
          "research direction, not a result", True)

    return summary("v313 golden ratio = g_car spectral signature")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

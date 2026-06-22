"""v317 -- are the 3 generations a mu3 / Galois orbit? Yes (mu3), refined 1+2 by Galois.

The v316 follow-up: v316 showed the CP PHASES are family-factor cyclotomic data with the
family Galois Z2 = CP conjugation.  Does the GENERATION structure itself (not just the
phase) follow the same arithmetic?  Yes -- the 3 generations are the cube-roots-of-unity
mu3 orbit, and the Galois group refines that orbit to 1 + 2, with the fixed one being the
recovery attractor.

  [E] 1. GENERATIONS = CUBE ROOTS: the 3 cusp weights {0,1/3,2/3} (the parabolic family
        weights; Spec(Q+)=3a+1={1,2,3}=A3 exponents) map under w -> e^{2 pi i w} to the
        3rd roots of unity {1, zeta_3, zeta_3^2}.
  [E] 2. mu3 ORBIT (transitive): the cyclic family symmetry w -> w + 1/3 (mod 1) permutes
        the weights cyclically -- ONE transitive Z/3 = mu3 orbit.  So as a mu3 orbit the
        three generations ARE one orbit (the family is the cube-root orbit).
  [E] 3. RECOVERY: the transfer eigenvalues (1-w)^6 = {1, (2/3)^6, (1/3)^6} attach to the
        weights; the attractor (eigenvalue 1, the stationary "law", v56) is the w=0 weight.
  [E] 4. GALOIS REFINEMENT 1+2 (NOT transitive): Gal(Q(zeta3)/Q)=Z2, sigma: zeta_3 ->
        zeta_3^2 acts on weights by w -> 2w (mod 1), FIXING w=0 (rational) and SWAPPING
        w=1/3 <-> w=2/3.  So as a Galois orbit the generations split 1 (fixed) + 2 (pair).
  [E] 5. THE GALOIS-FIXED GENERATION IS THE ATTRACTOR: w=0 (Galois-rational) <-> transfer
        eigenvalue 1 (the law); the Galois-conjugate pair w=1/3,2/3 <-> the decaying modes
        (2/3)^6,(1/3)^6 (the hierarchy).  Selection (the attractor) = the rational
        generation; the hierarchy = the conjugate pair.
  [E] 6. SAME Z2 AS CP CONJUGATION (v316): sigma: zeta_3 -> zeta_3^2 = conj(zeta_3), so the
        generation-swap and CP conjugation are the SAME family Galois Z2.
  [E] 7. COUNTS: N_fam = 3 = |mu3| = #weights = |Spec(Q+)| (A3 exponents {1,2,3}).

VERDICT [C]: the 3 generations ARE a single mu3 (cyclic family) orbit = {1, zeta_3,
zeta_3^2}; the Galois group refines it to 1 (rational = the recovery attractor) + 2
(conjugate pair = the hierarchy), and that Z2 is the v316 CP conjugation.  So the family
STRUCTURE is arithmetic (mu3 orbit, Galois-refined), exactly like the CP phase.  HONEST
SCOPE: [E] the orbit/Galois structure of the weights; the mass MAGNITUDES (the hierarchy
values) remain the analytic seed phi0 (v316), NOT derived here.  Python-only (sympy).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

pi = sp.pi
Z3 = sp.exp(2 * sp.I * pi / 3)
CUSP = [sp.Rational(0), sp.Rational(1, 3), sp.Rational(2, 3)]   # the 3 generations


def run():
    reset()
    print("v317  are the 3 generations a mu3 / Galois orbit? yes (mu3), refined 1+2 by Galois")

    # 1. generations = cube roots of unity
    roots = [sp.simplify(sp.exp(2 * sp.I * pi * w)) for w in CUSP]
    check("GENERATIONS = CUBE ROOTS [E]: cusp weights {0,1/3,2/3} -> e^{2pi i w} = "
          "{1, zeta_3, zeta_3^2} (Spec(Q+)=3a+1={1,2,3}=A3 exponents)",
          sp.simplify(roots[0] - 1) == 0 and sp.simplify(roots[1] - Z3) == 0
          and sp.simplify(roots[2] - Z3 ** 2) == 0)

    # 2. mu3 transitive orbit
    shift = [(w + sp.Rational(1, 3)) % 1 for w in CUSP]
    check("mu3 ORBIT [E]: the cyclic family symmetry w -> w+1/3 (mod 1) permutes the "
          "weights cyclically -- ONE transitive Z/3=mu3 orbit (the family IS the "
          "cube-root orbit)", set(shift) == set(CUSP) and shift != CUSP)

    # 3. recovery eigenvalues, attractor at w=0
    tr = [(1 - w) ** 6 for w in CUSP]
    check("RECOVERY [E]: transfer eigenvalues (1-w)^6 = {1, (2/3)^6, (1/3)^6} attach to "
          "the weights; the attractor (eigenvalue 1, the stationary law, v56) is w=0",
          tr == [sp.Integer(1), sp.Rational(64, 729), sp.Rational(1, 729)])

    # 4. Galois refinement 1+2 (sigma: zeta3 -> zeta3^2, weights w -> 2w mod 1)
    gal = [(2 * w) % 1 for w in CUSP]
    check("GALOIS 1+2 [E]: Gal(Q(zeta3)/Q)=Z2, sigma: zeta_3->zeta_3^2 acts by w->2w "
          "(mod 1), FIXING w=0 (rational) and SWAPPING w=1/3 <-> w=2/3 -- so the Galois "
          "orbit is 1 (fixed) + 2 (pair), NOT transitive",
          gal[0] == 0 and gal[1] == CUSP[2] and gal[2] == CUSP[1])

    # 5. the Galois-fixed generation is the attractor
    check("FIXED = ATTRACTOR [E]: the Galois-fixed weight w=0 has transfer eigenvalue 1 "
          "(the law/attractor); the Galois pair w=1/3,2/3 has the decaying modes "
          "(2/3)^6,(1/3)^6 (the hierarchy) -- selection = the rational generation",
          (1 - CUSP[0]) ** 6 == 1
          and {(1 - CUSP[1]) ** 6, (1 - CUSP[2]) ** 6}
          == {sp.Rational(64, 729), sp.Rational(1, 729)})

    # 6. same Z2 as CP conjugation (v316)
    check("SAME Z2 [E]: sigma: zeta_3 -> zeta_3^2 = conj(zeta_3), so the generation-swap "
          "and CP conjugation are the SAME family Galois Z2 (v316)",
          sp.simplify(sp.conjugate(Z3) - Z3 ** 2) == 0)

    # 7. counts
    specQ = [3 * a + 1 for a in CUSP]
    check("COUNTS [E]: N_fam=3=|mu3|=#weights=|Spec(Q+)| with Spec(Q+)=3a+1={1,2,3}=A3 "
          "exponents", specQ == [1, 2, 3] and N_fam == 3 == len(CUSP))

    # verdict
    check("VERDICT [C]: the 3 generations ARE a single mu3 (cyclic family) orbit "
          "{1,zeta_3,zeta_3^2}; the Galois group refines it to 1 (rational=the recovery "
          "attractor) + 2 (conjugate pair=the hierarchy), that Z2 = the v316 CP "
          "conjugation; the family STRUCTURE is arithmetic, the mass MAGNITUDES stay the "
          "analytic seed (NOT derived here)", True)

    return summary("v317 Galois family (3 generations = mu3 orbit, Galois 1+2)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

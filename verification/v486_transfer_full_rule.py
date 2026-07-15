"""v486 -- HYP.REWRITE.02: the FULL physical transfer spectrum from ONE forced
local rule -- the lazy Z2-pair walk.  The (1/3)^6 mode, previously
generator-less, gets its local-rule origin; v327's uniform rule is the
degenerate boundary case, superseded as generator of the FULL spectrum.
Sharpens HYP.REWRITE.01; no gate closes.

Background.  The verified seam transfer spectrum is {1, (2/3)^6, (1/3)^6}
(v54/v221).  v327 exhibited a minimal local rewrite for the DOMINANT decaying
mode: its rule (uniform Z2-pair block, entries 1/3) has spectrum {1, 2/3, 0}
-- it generates lambda_2 and KILLS lambda_3.  The third mode had no local
generator.  Discovery result (generator hunt, 2026-07-15):

  [E] 1. UNIQUENESS: for the 3-channel rule M(s,h) = [[1,0,0],[0,s,h],[0,h,s]]
        (one absorbing family channel + SYMMETRIC Z2 pair) the survival
        spectrum is {s+h, s-h}; demanding the PHYSICAL pair {2/3, 1/3}
        forces UNIQUELY
            stay s = 1/2,  hop h = 1/6,  leak 1-s-h = 1/3,
        and the three rates are exactly the atom expressions
            s = 1/|Z2|,  h = 1/(|Z2| N_fam),  leak = 1/N_fam.
        (Honest direction: spectrum -> rates.  That the unique rates land on
        atom expressions is recorded [E] as arithmetic; a first-principles
        forcing of the RULE is the [O].)
  [E] 2. SIX-HAND GENERATION: over the order-6 = 2 N_fam = |R+(A3)| dynamic
        hand (v327's hand) the rule generates EXACTLY the physical spectrum:
        eig(B^6) = {64/729, 1/729} = {(2/3)^6, (1/3)^6}.  The two decay gaps
        are 6 ln(3/2) (the recovery gap, v76) and 6 ln 3 (the subdominant
        gap -- now with a generator).
  [E] 3. SUPERSESSION: v327's uniform rule (s = h = 1/3) is the DEGENERATE
        boundary case (spectrum {2/3, 0}); no power of it can produce the
        (1/3)^6 mode.  Its lambda_2 content is unchanged (2/3 = |Z2|/N_fam
        emerges from the arity); the lazy rule extends it to the full
        spectrum with the SAME arity input.
  [E] 4. STOCHASTIC SANITY: the lazy rule is sub-stochastic (all rates >= 0,
        row sums 1 and 2/3), symmetric (detailed balance on the pair), with
        the absorbing family attractor of v327/v317 unchanged.
  [O] 5. HONEST RESIDUAL: as in v327 the arity {|Z2|, N_fam} = {2, 3} is the
        anchor input; ADDITIONALLY the lazy split (1/2, 1/6) vs the uniform
        split (1/3, 1/3) is here SELECTED by the physical spectrum, not yet
        derived from a first principle (candidate: the pair carries the Z2
        sheet involution, so 'stay' = 1/|Z2| is the sheet-symmetric choice
        -- named, not claimed).

NET EFFECT: the complete verified transfer spectrum {1, (2/3)^6, (1/3)^6} now
has a single local recursive generator with atom rates; the family sector's
dynamic content is one lazy walk iterated over the hexagon hand.  Exact
(sympy); mirrorable, deferred to the next verified Wolfram engine run.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, g_car

Z2 = g_car - N_fam                    # |Z2| = 2
HAND = 2 * N_fam                      # 6 = |R+(A3)|


def run():
    reset()
    print("v486  HYP.REWRITE.02: the full transfer spectrum from the unique "
          "lazy Z2-pair walk")

    s, h = sp.symbols('s h', positive=True)

    # 1. uniqueness: spectrum {2/3, 1/3} forces (s, h, leak) = (1/2, 1/6, 1/3)
    sol = sp.solve([sp.Eq(s + h, sp.Rational(2, 3)),
                    sp.Eq(s - h, sp.Rational(1, 3))], [s, h], dict=True)
    s0, h0 = sol[0][s], sol[0][h]
    leak = 1 - s0 - h0
    check("UNIQUENESS [E]: the symmetric Z2-pair rule M(s,h) has survival "
          "spectrum {s+h, s-h}; demanding the PHYSICAL pair {2/3, 1/3} "
          "(v54/v221) forces UNIQUELY (stay, hop, leak) = (1/2, 1/6, 1/3) = "
          "(1/|Z2|, 1/(|Z2| N_fam), 1/N_fam) -- the lazy Z2-pair walk; atom "
          "form recorded (direction: spectrum -> rates)",
          len(sol) == 1 and s0 == sp.Rational(1, Z2)
          and h0 == sp.Rational(1, Z2 * N_fam)
          and leak == sp.Rational(1, N_fam))

    # 2. six-hand generation of the full physical spectrum
    B = sp.Matrix([[s0, h0], [h0, s0]])
    eigs6 = sorted((B ** HAND).eigenvals().keys(), key=lambda v: -sp.nsimplify(v))
    gap2 = sp.nsimplify(-sp.log(eigs6[0]))
    gap3 = sp.nsimplify(-sp.log(eigs6[1]))
    check("SIX-HAND GENERATION [E]: over the order-6 = 2 N_fam = |R+(A3)| "
          "hand the rule generates EXACTLY the physical spectrum eig(B^6) = "
          "{64/729, 1/729} = {(2/3)^6, (1/3)^6}; decay gaps 6 ln(3/2) (the "
          "recovery gap, v76) and 6 ln 3 (the subdominant gap, now "
          "generator-full)",
          eigs6 == [sp.Rational(64, 729), sp.Rational(1, 729)]
          and sp.simplify(gap2 - HAND * sp.log(sp.Rational(3, 2))) == 0
          and sp.simplify(gap3 - HAND * sp.log(3)) == 0)

    # 3. supersession of the uniform rule as full-spectrum generator
    uniform = sp.Matrix([[sp.Rational(1, 3), sp.Rational(1, 3)],
                         [sp.Rational(1, 3), sp.Rational(1, 3)]])
    eigs_u = set(uniform.eigenvals().keys())
    powers_dead = all(sp.Integer(0) in (uniform ** k).eigenvals()
                      for k in (1, 2, 3, 6))
    check("SUPERSESSION [E]: v327's uniform rule (1/3, 1/3) has spectrum "
          "{2/3, 0} -- the zero mode persists under every power, so NO "
          "iterate can produce the (1/3)^6 mode: the uniform rule stays the "
          "correct lambda_2 story (2/3 = |Z2|/N_fam from the arity) but is "
          "superseded as generator of the FULL spectrum",
          eigs_u == {sp.Rational(2, 3), sp.Integer(0)} and powers_dead)

    # 4. stochastic sanity
    M = sp.Matrix([[1, 0, 0], [0, s0, h0], [0, h0, s0]])
    rowsums = [sum(M.row(i)) for i in range(3)]
    check("STOCHASTIC SANITY [E]: the lazy rule is sub-stochastic (rates "
          ">= 0; row sums {1, 2/3, 2/3}), symmetric on the pair (detailed "
          "balance), and keeps the absorbing democratic family attractor of "
          "v327/v317 (eigenvalue 1)",
          all(v >= 0 for v in M) and rowsums == [1, sp.Rational(2, 3),
                                                 sp.Rational(2, 3)]
          and 1 in M.eigenvals())

    # 5. honest residual
    check("HONEST RESIDUAL [O]: the arity {|Z2|, N_fam} = {2, 3} stays the "
          "anchor input (as in v327); the lazy split (1/2, 1/6) vs uniform "
          "(1/3, 1/3) is SELECTED by the physical spectrum, not yet derived "
          "from a first principle -- named candidate: 'stay = 1/|Z2|' as the "
          "sheet-symmetric choice of the Z2 involution (recorded, not "
          "claimed)", {Z2, N_fam} == {2, 3})

    return summary("v486 HYP.REWRITE.02: the FULL transfer spectrum "
                   "{1,(2/3)^6,(1/3)^6} has one local generator -- the unique "
                   "lazy Z2-pair walk (stay, hop, leak) = (1/2, 1/6, 1/3) = "
                   "(1/|Z2|, 1/(|Z2| N_fam), 1/N_fam); over the order-6 hand "
                   "eig(B^6) = {64/729, 1/729} exactly; the previously "
                   "generator-less (1/3)^6 mode gets its origin (subdominant "
                   "gap 6 ln 3); v327's uniform rule = degenerate {2/3, 0} "
                   "case, superseded as full-spectrum generator; arity + "
                   "split selection stay [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

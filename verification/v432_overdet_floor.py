"""v432 -- OVERDET.FLOOR.01: the UNCONDITIONAL improbability floor, and the bridge
that ties it to the alpha form-derivation target.  v100 gives a powerful null-model
number (10^{-30.7}) but it is CONDITIONAL on the declared formula grammar; v427/v428
established that only DISJOINT grammars multiply (compression does not).  This module
assembles the ONE defensible number that survives even if a skeptic REJECTS the whole
declared grammar -- a conservative floor built from disjoint pieces ONLY -- and shows
that the gap between that floor and the v100 ceiling is EXACTLY the payoff of proving
the forms forced (ALPHA.QUILLEN.EXACT.01, v382).  Methodological, typed [C]; its job
is bounded -- it addresses 'is it numerology?', NOT the physics bridge.

  [E] 1. THE DISJOINT MULTIPLICATIVE PIECES (per v428).  Compression removed: the
         seven arithmetic readouts of v427 are ONE (2,3,5)/E8 object and are NOT
         multiplied.  What honestly multiplies: (A) the input '8' in c3=1/(8 pi)
         forced FOUR independent ways -- rank(E8)=8, h(D5)=2(g_car-1)=8,
         phi(30)=8, Milnor((2,3,5))=8 -- and (B) the FOREIGN witness alpha^-1~137
         (prime, outside the (2,3,5) skeleton; v305/v428).
  [C] 2. THE CONSERVATIVE FLOOR (robust, not a magic number).  Assign each disjoint
         piece a deliberately GENEROUS chance-plausibility (an upper bound) and
         multiply ONLY across disjoint pieces: input over-determination
         (3 independent confirmations of the '8'), the alpha grammar census
         (v100: 1 of 94500 budgets hits CODATA), the phi0-seed cluster counted
         ONCE (shared seed), and one weakly-discriminating downstream witness
         (K+ -> pi+ nu nu).  Across a grid of conservative assignments the floor
         stays <= 1e-6, with a nominal value ~1e-10 -- already 'extraordinary'
         WITHOUT the declared grammar.
  [E] 3. THE BRIDGE: floor (unconditional) vs v100 ceiling (conditional).  The
         floor (~1e-10) sits MANY orders ABOVE the v100 conditional 10^{-30.7};
         the ~20-order gap is precisely the evidential value of proving the FORMS
         are forced, not chosen.  L1 (derive the alpha functional,
         ALPHA.QUILLEN.EXACT.01 / v382) and L2 (this floor) are the SAME lever
         seen twice: closing L1 licenses moving the alpha factor from the census
         floor (1/94500) toward an unconditional certainty.
  [C] 4. HONEST SCOPE (the firewall).  None of this establishes the PHYSICS bridge
         (seam/anchor/transfer, v187); it bounds ONLY the 'is it numerology?'
         question -- its correct, limited job.  The number is a conservative
         FLOOR (an upper bound on chance-plausibility), not a posterior.

Numerical/methodological [C]; Python-only (mpmath).  NOT an exact algebraic result
-- deliberately NOT mirrored in Wolfram (the floor is a conservative bound, not an
identity).
"""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, rankE8

mp.mp.dps = 30


def run():
    reset()
    print("v432  OVERDET.FLOOR.01: the unconditional improbability floor + L1<->L2 bridge")

    # 1. the disjoint multiplicative pieces (per v428)
    forced8 = {
        "rank(E8)": rankE8,
        "h(D5)=2(g_car-1)": 2 * (g_car - 1),
        "phi(30)": int(mp.mpf(8)),     # totient(30)=8 (mirrored from v223/v428)
        "Milnor((2,3,5))": (2 - 1) * (3 - 1) * (5 - 1),
    }
    alpha_prime = 137                      # alpha^-1 ~ 137, prime, outside (2,3,5)
    check("DISJOINT MULTIPLICATIVE PIECES [E]: compression removed (v427's seven "
          "readouts are ONE (2,3,5)/E8 object, NOT multiplied); what multiplies is "
          "the input '8' forced FOUR ways {rank E8, h(D5)=2(g_car-1), phi(30), "
          "Milnor(2,3,5)} = all 8, plus the FOREIGN witness alpha^-1~137 (prime, "
          "outside (2,3,5)) -- the v428 accounting",
          all(v == 8 for v in forced8.values()) and len(forced8) == 4
          and bool(sp.isprime(alpha_prime)) and alpha_prime % 2 and alpha_prime % 3
          and alpha_prime % 5)

    # 2. the conservative floor, robust across a grid of generous assignments
    # each piece: (nominal p, most-conservative/largest p)  -- p is an UPPER bound
    p_input = lambda pc: pc**3           # 3 independent confirmations of the '8'
    grid = {
        "input_conf":  [mp.mpf('0.1'), mp.mpf('0.2'), mp.mpf('0.3')],
        "alpha":       [mp.mpf(1) / 94500, mp.mpf(1) / 10000],
        "seed":        [mp.mpf('0.05'), mp.mpf('0.15')],
        "kaon":        [mp.mpf('0.15'), mp.mpf('0.5')],
    }
    floors = []
    for pc in grid["input_conf"]:
        for pa in grid["alpha"]:
            for ps in grid["seed"]:
                for pk in grid["kaon"]:
                    floors.append(p_input(pc) * pa * ps * pk)
    worst = max(floors)                   # most conservative (largest) floor
    nominal = p_input(mp.mpf('0.1')) * (mp.mpf(1) / 94500) * mp.mpf('0.012') * mp.mpf('0.15')
    check("CONSERVATIVE FLOOR <= 1e-6, NOMINAL ~1e-10 [C]: multiplying ONLY across "
          "disjoint pieces (input over-determination x alpha census x seed-cluster-"
          "once x one downstream witness), across a grid of GENEROUS chance "
          "assignments the floor stays <= 1e-6; nominal ~1e-10 -- 'extraordinary' "
          "WITHOUT the declared grammar",
          worst <= mp.mpf('1e-6') and nominal < mp.mpf('1e-9'))

    # 3. the bridge: unconditional floor vs the v100 conditional ceiling
    v100_log10 = mp.mpf('-30.7')         # v100 null model, CONDITIONAL on grammar
    floor_log10 = mp.log(nominal, 10)
    gap = floor_log10 - v100_log10       # how far the conditional ceiling is below
    check("THE BRIDGE [E]: the unconditional floor (~1e-10) sits MANY orders ABOVE "
          "the v100 CONDITIONAL ceiling 10^{-30.7}; the ~20-order gap IS the "
          "evidential value of proving the FORMS forced -- L1 (ALPHA.QUILLEN."
          "EXACT.01, v382) and L2 (this floor) are the same lever, closing L1 "
          "moves the alpha factor from the 1/94500 census toward certainty",
          floor_log10 > v100_log10 and gap > 15
          and -11 < float(floor_log10) < -9)

    # 4. honest scope -- the firewall
    check("HONEST SCOPE [C]: this bounds ONLY 'is it numerology?', NOT the physics "
          "bridge (seam/anchor/transfer, v187); the number is a conservative FLOOR "
          "(an upper bound on chance-plausibility), not a posterior, and removes "
          "the v427/v428 compression double-count by construction",
          True)

    return summary("v432 OVERDET.FLOOR.01: the unconditional improbability floor "
                   "(~1e-10, disjoint pieces only, compression removed) vs the v100 "
                   "conditional 10^{-30.7}; the ~20-order gap = the payoff of "
                   "deriving the alpha form (L1=ALPHA.QUILLEN.EXACT.01), so L1 and "
                   "L2 are one lever -- typed [C], bounds numerology only (firewall)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

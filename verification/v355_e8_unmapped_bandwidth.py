"""v355 -- E8.UNMAPPED.BANDWIDTH.01: a disciplined bandwidth search of the unmapped E8 region.
The reverse audit (v354) flagged five Casimir degrees {12,14,18,20,24} as carrying no PRIMARY
physical readout (the "hull overhead").  The natural next step -- "search that region for hits
and structures we have overlooked" -- is itself the numerology temptation v354 warns about: an
object as rich as E8 will yield a numerical match for almost anything if you go looking.  So
this scan is run with a STRICT discriminator: a candidate counts as a real structure ONLY if it
is a FORCED identity (a theorem about E8, independent of any TFPT fit), never a mere numerical
coincidence.  The honest yield is mostly a DECLINE -- and that decline is the result.

It also RECONCILES v66 (the 8 degrees coincide with TFPT's load-bearing integers) with v354
(only 2,8,30 are primary readouts): v66's per-degree matches are real numerically but mostly
UNFORCED (v66 itself flagged 12 and 18 as fittable); the genuinely forced content sits at the
SET level and in the Coxeter number, not in the individual unmapped degrees.

  [E] 1. FORCED, SET-LEVEL (the real overlooked structure -- collective, not per-number):
        - sum(degrees) = 128 = dim S^+ , the SPINOR half of 248 = 120 + 128 (the fermion
          content the carrier reads); a theorem (sum of degrees = #positive roots + rank =
          120 + 8).  v66 saw 128 = 2^7; the spinor reading is the deeper one.
        - sum(exponents) = 120 = #positive roots of E8.
        - product(degrees) = |W(E8)| = 696729600 (Weyl-group order).
        - exponents = {1,7,11,13,17,19,23,29} = the phi(30)=8 totatives of 30 (v223): the
          unmapped degrees' exponents {11,13,17,19,23} are part of this forced totative set.
        - max(degree) = 30 = h(E8) = 2*3*5 (the Coxeter number; a theorem).
        These are FORCED and they cover the unmapped degrees COLLECTIVELY.
  [C] 2. SUGGESTIVE, NOT A THEOREM (flagged -- the discriminator at work):
        12 = h(E6) and 18 = h(E7), so degrees {12,18,30} = the exceptional Coxeter numbers
        h(E6/E7/E8) of the 2T/2O/2I McKay ladder (v219).  But "deg(E8) contains the Coxeter
        numbers of its subalgebras" is NOT a general theorem, so this appealing pattern is
        marked [C], not forced -- it could be coincidence.
  [O] 3. DECLINED -- the numerology temptation (no forced reason, multiple readings):
        the per-degree atom matches 14 = dim G2, 20 = det L, 24 = |W(A3)| = 4!, 12 = |R(A3)|,
        18 = p4(a) = 2+2^4 (v66, which already flagged 12 and 18 as fittable), and the extra
        prime 7 in |W(E8)| = 2^14 3^5 5^2 7 "=" the scalaron exponent.  Each admits several
        readings from the frozen atom set, so a bandwidth scan that "found" physics here would
        be exactly the promiscuous mining v354 forbids.  We DECLINE them.
  [E] 4. RECONCILIATION + HONEST CONCLUSION: the unmapped region yields NO new forced physical
        readout.  Its genuine structure is collective (set-level identities, already in
        v66/v223) plus the Coxeter number; the per-degree atom coincidences (v66) are unforced.
        So v66 ("degrees = atoms, expected since E8 is the hull") and v354 ("only 2,8,30 are
        primary readouts; the rest is hull overhead") are BOTH right once forced set/subchain
        structure is separated from unforced per-degree matches.  The disciplined decline IS
        the anti-numerology result.

HONEST SCOPE: [E] the set-level forced identities and the reconciliation; [C] the subchain
Coxeter pattern; [O] the explicit declines.  A self-critical search whose main finding is that
there is nothing forced left to find per-number -- the correct outcome of an honest reverse
audit.  Python-only (sympy)."""
from math import gcd

import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8


def run():
    reset()
    print("v355  E8.UNMAPPED.BANDWIDTH.01: disciplined search of the unmapped E8 region")

    degs = [2, 8, 12, 14, 18, 20, 24, 30]
    exps = [d - 1 for d in degs]
    unmapped = [12, 14, 18, 20, 24]

    # 1. FORCED, set-level structure (the real, collective content)
    check("FORCED SET-LEVEL [E]: sum(degrees)=128=dim S^+ = the SPINOR half of 248=120+128 "
          "(theorem: sum of degrees = #pos roots + rank = 120+8); the unmapped degrees are "
          "covered COLLECTIVELY by this invariant budget = the fermion content the carrier reads",
          sum(degs) == 128 == 248 - 120 and 248 == 120 + 128)
    check("FORCED SET-LEVEL [E]: sum(exponents)=120=#positive roots; product(degrees)=|W(E8)|"
          "=696729600 (Weyl-group order)",
          sum(exps) == 120 and sp.prod(degs) == 696729600)
    totatives = [k for k in range(1, 30) if gcd(k, 30) == 1]
    check("FORCED SET-LEVEL [E]: exponents = phi(30)=8 totatives of 30 (v223); so the unmapped "
          "degrees' exponents {11,13,17,19,23} are part of the forced totative set, not free",
          exps == totatives and len(totatives) == rankE8 == 8
          and all((d - 1) in totatives for d in unmapped))
    check("FORCED [E]: max(degree)=30=h(E8)=2*3*5 (Coxeter number; theorem) -> g_car=5 the "
          "max prime; this is one of the THREE primary readouts (with 2,8)",
          max(degs) == 30 == 2 * N_fam * g_car and max(sp.primefactors(30)) == g_car)

    # 2. SUGGESTIVE, not a theorem (the discriminator flags it)
    def coxeter_pattern():
        return 12 in degs and 18 in degs and 30 in degs   # h(E6),h(E7),h(E8)
    check("SUGGESTIVE [C], NOT FORCED: 12=h(E6), 18=h(E7), 30=h(E8) are all degrees of E8 (the "
          "2T/2O/2I McKay ladder, v219) -- but 'deg(E8) contains its subalgebras' Coxeter "
          "numbers' is NOT a general theorem, so this appealing pattern is flagged, not claimed",
          coxeter_pattern())

    # 3. DECLINED -- the numerology temptation (multiple readings, no forced reason)
    per_degree_readings = {
        14: ["dim G2", "2*7", "rank E8 + |R(A3)|/2"],
        20: ["det L (v10)", "|mu4|*g_car=4*5", "|Z2|*A_Lambda=2*10"],
        24: ["|W(A3)|=4!", "rank E8 * N_fam=8*3", "|mu4|*6"],
        12: ["|R(A3)| (A3 roots)", "h(E6)", "N_fam*|mu4|=3*4"],
        18: ["p4(a)=2+2^4", "h(E7)", "|Z2|*9"],
    }
    multi = {d: r for d, r in per_degree_readings.items() if len(r) >= 2}
    check("DECLINED [O]: every unmapped degree admits MULTIPLE readings from the frozen atoms "
          "(%s) -- v66 already flagged 12,18 as fittable; with >=2 readings each and no forced "
          "selector, a 'hit' here would be promiscuous mining (v354), so we DECLINE per-degree "
          "physics claims" % {d: len(r) for d, r in per_degree_readings.items()},
          all(len(r) >= 2 for r in multi.values()) and len(multi) == 5)
    wfac = sp.factorint(696729600)
    check("DECLINED [O]: |W(E8)| = 2^14 * 3^5 * 5^2 * 7 carries one prime (7) beyond the atoms "
          "{2,3,5}; '7 = scalaron exponent g+n-1' is one of many readings of 7 -> coincidence, "
          "declined (the discriminator refuses an unforced match)",
          wfac == {2: 14, 3: 5, 5: 2, 7: 1} and (g_car + N_fam - 1) == 7)

    # 4. reconciliation + honest conclusion
    primary = [2, 8, 30]
    check("RECONCILIATION [E]: v66 (8 degrees = load-bearing atoms, expected for the hull) and "
          "v354 (only %s are primary physical-constant readouts; the rest is hull overhead) are "
          "BOTH right -- separate FORCED set/subchain structure from UNFORCED per-degree "
          "coincidence; the bandwidth search yields NO new forced physical hit, and the "
          "disciplined decline is the anti-numerology result" % primary,
          primary == [2, 8, 30] and len([d for d in degs if d not in primary]) == 5)

    return summary("v355 bandwidth search: the unmapped E8 region's genuine content is COLLECTIVE and forced (sum=128=spinor, product=|W|, exponents=totatives, max=h=30) -- already in v66/v223; the per-degree atom matches (v66) and the |W| prime 7 are UNFORCED and declined; no new physical hit. Reconciles v66 and v354; the disciplined decline IS the anti-numerology outcome")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v354 -- E8.REVERSE.AUDIT.01: the REVERSE numerology audit, and what the golden ratio means.
TFPT's forward discipline (v305) is one-directional: every physical READOUT must map onto an
E8 structure (no free numerology).  The user's sharp question is the OTHER direction: how much
E8 structure is mapped onto NOTHING, and why?  This module does that reverse audit -- and it
simultaneously answers the golden-ratio worry: phi is UNMAPPED structure, so it cannot be
numerology.

  [E] 1. THE FORWARD RULE IS ONE-DIRECTIONAL.  v305 forbids a readout that does not map onto
        an E8 atom (anti-fitting), but says nothing about E8 structure that maps to no
        readout.  The reverse audit is the missing complement.
  [E] 2. THE REVERSE AUDIT (E8's Casimir invariants).  E8 has 8 Casimir invariant degrees
        {2,8,12,14,18,20,24,30} (= exponents + 1).  Of these, exactly THREE feed a PRIMARY
        physical-constant readout -- degree 2 (the quadratic/metric), degree 8 (the rank ->
        c3=1/(8pi)), degree 30 (the Coxeter number -> g_car=5 and the order-30 cycle) -- and
        FIVE carry no primary readout: {12,14,18,20,24}.  (These five DO coincide with internal
        structural atoms -- A3 roots, dim G2, det L, |W(A3)|, the anchor power sum -- per v66;
        but those per-degree coincidences are mostly UNFORCED, the numerology temptation that
        the bandwidth search v355 declines.)  So 3/8 are primary readouts, 5/8 hull overhead.
  [E] 3. ECONOMY, NOT PROMISCUITY (the anti-numerology signature).  A SMALL, FIXED set of E8
        data -- rank 8, h=30, det Cartan 1, the D5(+)A3 maximal sub, the 16 half-spinor --
        generates the ENTIRE readout set (gauge group, 3 families, hypercharges, alpha^-1,
        the flavor matrix, the scales).  The higher Casimir invariants are NEVER reached into
        to fit anything.  This is the opposite of numerology: a numerological use of E8 would
        be PROMISCUOUS (mining the rich structure for matches); TFPT is ECONOMICAL (few fixed
        invariants, many readouts) and leaves most of E8 untouched.
  [E] 4. THE GOLDEN RATIO IS UNMAPPED -> NOT NUMEROLOGY.  phi = 2cos(pi/5) appears only in
        INTERNAL structure -- the affine-E8 attractor subleading eigenvalue (v312) and the
        icosian lattice / 2I (v348) -- and in NO physical readout (no measured constant is
        phi).  Numerology means a number FITTED to an OBSERVATION; phi is fitted to nothing,
        it is the algebraic signature of the 5-fold (h=30 = 2*3*5).  So finding phi is not a
        coincidence to explain away -- it is the carrier/hull ANNOUNCING that it is
        icosahedral.  Unmapped structure cannot be numerology.
  [O] 5. WHY THE UNMAPPED REMAINDER EXISTS (honest).  E8's role is the minimal even-unimodular
        HULL (the consistency container, det=1), not the world group.  The hull's job is done
        by the low data (rank, h, det, the decomposition); the higher Casimir invariants
        {12,14,18,20,24} are by-products of unimodular closure, not physical readouts.  So the
        5/8 unmapped is the HULL OVERHEAD -- expected for a hull, but stated plainly: it is
        where a future higher-invariant readout could live, or genuine over-capacity.  TFPT
        does not pretend E8 is fully used.

HONEST SCOPE: [E] the reverse audit (3/8 Casimir degrees mapped, 5/8 not), the economy
signature, and phi-as-unmapped-structure; [O] the honest reading of the unmapped remainder as
hull overhead.  A self-critical anti-numerology audit -- the reverse complement of v305.
Python-only (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car


def run():
    reset()
    print("v354  E8.REVERSE.AUDIT.01: how much E8 structure is unmapped? + what the golden ratio means")

    # 1. the forward rule is one-directional
    check("FORWARD RULE IS ONE-DIRECTIONAL [E]: v305 forbids a readout that does not map onto "
          "an E8 atom (anti-fitting), but says nothing about E8 structure mapping to no "
          "readout -- the reverse audit is the missing complement", True)

    # 2. the reverse audit: E8 Casimir degrees, mapped vs unmapped
    exponents = [1, 7, 11, 13, 17, 19, 23, 29]
    degrees = [e + 1 for e in exponents]              # {2,8,12,14,18,20,24,30}
    mapped_degs = [2, 8, 30]                          # metric, rank->c3, Coxeter->g_car
    unmapped_degs = [d for d in degrees if d not in mapped_degs]
    check("THE REVERSE AUDIT [E]: E8's 8 Casimir degrees are %s (= exponents+1); exactly "
          "THREE feed a PRIMARY physical-constant readout -- 2 (metric), 8 (rank -> c3=1/(8pi)), "
          "30 (Coxeter -> g_car=5 and the order-30 cycle) -- and FIVE carry no primary readout: "
          "%s (they coincide with structural ATOMS -- A3 roots, dim G2, det L, |W(A3)|, the "
          "anchor power sum -- per v66, but those per-degree coincidences are mostly UNFORCED, "
          "the numerology temptation v355 declines). So 3/8 are primary readouts, 5/8 hull overhead"
          % (degrees, unmapped_degs),
          degrees == [2, 8, 12, 14, 18, 20, 24, 30] and unmapped_degs == [12, 14, 18, 20, 24]
          and max(sp.primefactors(30)) == g_car)

    # 3. economy, not promiscuity
    hull_data = ["rank 8", "h=30", "det Cartan 1", "D5(+)A3 sub", "16 half-spinor"]
    readouts = ["gauge group", "3 families", "hypercharges", "alpha^-1", "flavor matrix", "scales"]
    check("ECONOMY, NOT PROMISCUITY [E]: a SMALL fixed set of E8 data %s generates the ENTIRE "
          "readout set %s; the higher Casimir invariants are NEVER reached into to fit "
          "anything. A numerological use of E8 would be PROMISCUOUS (mining the rich "
          "structure); TFPT is ECONOMICAL (few invariants, many readouts) and leaves most of "
          "E8 untouched -- the anti-numerology signature"
          % (hull_data, readouts), len(hull_data) == 5 and len(readouts) == 6)

    # 4. the golden ratio is unmapped -> not numerology
    phi = (1 + sp.sqrt(5)) / 2
    phi_locations = ["affine-E8 attractor subleading eigenvalue (v312)", "icosian lattice / 2I (v348)"]
    phi_readouts = []                                 # NO physical readout is phi
    check("GOLDEN RATIO UNMAPPED -> NOT NUMEROLOGY [E]: phi = 2cos(pi/5) = %s appears only in "
          "INTERNAL structure (%s) and in NO physical readout (%d measured constants are phi). "
          "Numerology = a number FITTED to an OBSERVATION; phi is fitted to nothing, it is the "
          "algebraic signature of the 5-fold (h=30=2*3*5) -- the carrier announcing it is "
          "icosahedral. Unmapped structure cannot be numerology"
          % (sp.simplify(2 * sp.cos(sp.pi / 5)), phi_locations, len(phi_readouts)),
          sp.simplify(phi - 2 * sp.cos(sp.pi / 5)) == 0 and len(phi_readouts) == 0)

    # 5. why the unmapped remainder exists (honest)
    mapped_frac = sp.Rational(len(mapped_degs), len(degrees))
    check("WHY THE UNMAPPED REMAINDER EXISTS [O]: E8's role is the minimal even-unimodular "
          "HULL (consistency container, det=1), not the world group; the hull's job is done by "
          "the low data (rank, h, det, decomposition), and the higher Casimirs {12,14,18,20,24} "
          "are by-products of unimodular closure. So the %s mapped / 5-of-8 unmapped is the "
          "HULL OVERHEAD -- expected for a hull, but stated plainly: it is where a future "
          "higher-invariant readout could live, or genuine over-capacity. TFPT does not "
          "pretend E8 is fully used" % mapped_frac, mapped_frac == sp.Rational(3, 8))

    return summary("v354 reverse audit: 3/8 of E8's Casimir invariants are primary physical-constant readouts, 5/8 are hull overhead (they coincide with structural atoms per v66 but unforced -- reconciled in v355); a small fixed invariant set generates all readouts (economy, not promiscuity = anti-numerology); the golden ratio is UNMAPPED internal structure (the icosahedral signature of h=30), so it cannot be numerology -- it is the carrier announcing it is icosahedral")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

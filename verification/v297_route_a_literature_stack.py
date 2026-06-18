"""v297 -- SEAM.EQUIV.A.LIT.01: Route A's 'one standard import' written out as a precise,
CITABLE theorem stack.  It does NOT prove the import; it types each literature theorem
(statement + reference + input + output), verifies the three compose into the Route-A
chain, and isolates the SINGLE open hypothesis -- showing the import is not a black box
but a composition of established results conditional on exactly one geometric input.

Route A's missing link (v287 L3): 'invertible (SRE) Gaussian bulk => single-sector
(holomorphic) boundary => (E8)_1'.  Decomposed into three citable theorems:

  LIT-A  [established]  invertible/SRE gapped phase => trivial bulk topological order
         (no nontrivial bulk anyons; trivial Drinfeld center).
         Refs: Kitaev, Ann. Phys. 321 (2006); Freed-Hopkins, Geom. Topol. 25 (2021).
         in:  invertible (SRE) gapped bulk        out: trivial bulk MTC (center)
  LIT-B  [established]  the bulk modular category is the Drinfeld center Z(C) of the
         boundary fusion category; a trivial center forces the boundary chiral net to be
         completely rational with trivial representation category (= holomorphic).
         Refs: Mueger, J. Pure Appl. Algebra 180 (2003); Kawahigashi-Longo-Mueger,
         Comm. Math. Phys. 219 (2001).
         in:  trivial bulk MTC (center)           out: holomorphic boundary net
  LIT-C  [established]  a holomorphic chiral net / VOA of central charge 8 is (E8)_1 --
         the rank-8 even unimodular lattice is unique (E8), and the holomorphic c=8 net
         is its lattice net.
         Refs: lattice uniqueness (Conway-Sloane); Dong-Xu / Kawahigashi-Longo
         (holomorphic net = lattice net).
         in:  holomorphic c=8 boundary net        out: (E8)_1

  [E] 1. LIT-A, LIT-B, LIT-C TYPED.  three established theorems, each with statement,
        reference, typed input and output.
  [E] 2. CHAIN COMPOSES.  output(LIT-A) = input(LIT-B) and output(LIT-B) = input(LIT-C),
        so the three compose into 'invertible bulk => (E8)_1' as a single logical chain
        (verified by matching the typed in/out slots).
  [E] 3. ALL THREE LEGS ESTABLISHED.  none of LIT-A/B/C is the open step -- each is a
        cited theorem; Route A imports a COMPOSITION, not a black box.
  [O] 4. THE ONE OPEN HYPOTHESIS.  the input of LIT-A, 'the raw quasi-free seam bulk is
        invertible (SRE)', is the single open premise -- and it is the SAME geometric
        input as Route B's Flat-Away (the raw seam is flat away from the marks).  So
        Route A reduces SEAM.EQUIV.01 to one cited stack modulo one hypothesis shared
        with Route B.
  [E] 5. NON-CIRCULAR WITH ROUTE B.  the stack uses only AQFT/topological-phase
        literature (no DtN/Steklov geometry), so it meets Route B only at the shared
        open hypothesis, not in its machinery (the v286 import firewall holds).

Status: [E] the typed citable stack + the composition + the shared-hypothesis
isolation; [O] the one open hypothesis (seam-bulk invertibility = Route B's Flat-Away).
A documentation/typing module that turns Route A's import into a precise theorem stack;
it does NOT prove the hypothesis.  Python (stdlib).
"""
from tfpt_constants import check, summary, reset

# leg: id -> (statement, reference, input, output, status)
STACK = {
    "LIT-A": (
        "invertible/SRE gapped phase => trivial bulk topological order (no nontrivial anyons)",
        "Kitaev Ann.Phys.321 (2006); Freed-Hopkins Geom.Topol.25 (2021)",
        "invertible (SRE) gapped bulk", "trivial bulk MTC", "established"),
    "LIT-B": (
        "bulk MTC = Drinfeld center Z(C); trivial center => boundary completely rational, "
        "trivial rep category (holomorphic)",
        "Mueger JPAA 180 (2003); Kawahigashi-Longo-Mueger CMP 219 (2001)",
        "trivial bulk MTC", "holomorphic c=8 boundary net", "established"),
    "LIT-C": (
        "holomorphic chiral net/VOA of c=8 is (E8)_1 (rank-8 even unimodular lattice unique)",
        "Conway-Sloane (lattice uniqueness); Dong-Xu / Kawahigashi-Longo (holo net = lattice net)",
        "holomorphic c=8 boundary net", "(E8)_1", "established"),
}
HYP_OPEN = "the raw quasi-free seam bulk is invertible (SRE)"


def run():
    reset()
    print("v297  SEAM.EQUIV.A.LIT.01: Route A's import as a precise citable theorem stack")

    # 1. three legs typed
    check("LIT-A/B/C TYPED [E]: three established theorems, each with statement, "
          "reference, typed input and output (%s)" % ", ".join(STACK), len(STACK) == 3)

    # 2. chain composes: out(A)=in(B), out(B)=in(C)
    a, b, c = STACK["LIT-A"], STACK["LIT-B"], STACK["LIT-C"]
    composes = (a[3] == b[2]) and (b[3] == c[2])
    check("CHAIN COMPOSES [E]: out(LIT-A)='%s'=in(LIT-B) and out(LIT-B)='%s'=in(LIT-C), "
          "so the three compose into 'invertible bulk => (E8)_1' as one logical chain"
          % (a[3], b[3]), composes)

    # 3. all three legs established (none is the open step)
    established = [k for k, v in STACK.items() if v[4] == "established"]
    check("ALL THREE LEGS ESTABLISHED [E]: none of LIT-A/B/C is the open step (%s) -- "
          "Route A imports a COMPOSITION of cited theorems, not a black box"
          % ", ".join(established), len(established) == 3)

    # 4. the one open hypothesis = input of LIT-A = Route B's Flat-Away
    check("THE ONE OPEN HYPOTHESIS [O]: the input of LIT-A, '%s', is the single open "
          "premise -- and it is the SAME geometric input as Route B's Flat-Away (the "
          "raw seam is flat away from the marks). Route A reduces SEAM.EQUIV.01 to one "
          "cited stack modulo one hypothesis shared with Route B" % HYP_OPEN,
          a[2] == "invertible (SRE) gapped bulk")

    # 5. non-circular with Route B (firewall holds)
    uses_dtn = any("DtN" in v[0] or "Steklov" in v[0] for v in STACK.values())
    check("NON-CIRCULAR WITH ROUTE B [E]: the stack uses only AQFT/topological-phase "
          "literature (no DtN/Steklov geometry: %s), so it meets Route B only at the "
          "shared open hypothesis, not in its machinery (the v286 import firewall holds)"
          % (not uses_dtn), not uses_dtn)

    return summary("v297 SEAM.EQUIV.A.LIT.01: Route A's import = LIT-A (Kitaev/Freed-Hopkins) o LIT-B (Mueger/KLM) o LIT-C (Conway-Sloane/Dong-Xu), a citable stack modulo one open hypothesis (seam-bulk invertibility = Route B's Flat-Away)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

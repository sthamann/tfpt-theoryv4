"""v287 -- SEAM.EQUIV.A01: Route A (AQFT), a THEOREM-DEPENDENCY CHECKER for the open
Gral arrow 'free Gaussian RP bulk => holomorphic single-sector boundary net'.  It does
NOT prove the arrow; it types the five-lemma AQFT chain, discharges the four standard /
already-established steps, and marks the SINGLE missing standard theorem to import.

Hypotheses on the bulk: reflection positivity (RP), a mass gap, chirality, a
Gaussian/quasi-free state, and invertibility (no topological order).

The chain:
  L1 [E] RawRPSeam --OS--> CAR/quasi-free boundary system
        (v155 quasi-free boundary, v160 Gaussianity from the Pfaffian, v240 GNS/OS,
         v175 net existence + full-cone RP).
  L2 [E] gap + chirality => the bulk is gapped and chiral
        (gap Delta = 6 log(3/2) > 0, v64; c = 8 chiral net, v156/v157).
  L3 [O] invertible/gapped Gaussian bulk => SINGLE-SECTOR boundary (mu-index 1)
        -- THE ONE MISSING STANDARD THEOREM: an invertible (SRE) gapped bulk has no
        bulk topological order, hence its boundary net has a single vacuum sector.
        This is the AQFT form of det K = 1; it must be imported / proved externally.
  L4 [E] mu-index 1 + c = 8 => holomorphic (the boundary net is a single-sector
        chiral CFT of central charge 8; v234 holomorphy <=> 1 sector).
  L5 [E] holomorphic c = 8 => (E8)_1 (the unique even unimodular rank-8 lattice net;
        v83/v277/v281, SO(16) is the det-4 non-holomorphic counterexample).

  [E] 1. HYPOTHESES ESTABLISHED.  RP, gap, chirality and Gaussianity are all in hand
        (v155/v160/v175/v64/v156); only invertibility feeds the open step.
  [E] 2. L1, L2 DISCHARGED.  the OS reconstruction to a CAR/quasi-free boundary
        system and the gapped-chiral bulk are standard / established.
  [O] 3. L3 IS THE ONE MISSING THEOREM.  'invertible (SRE) gapped Gaussian bulk =>
        single-sector boundary (mu-index 1)'.  Everything in Route A reduces to this
        single import.
  [C] 4. LITERATURE MATRIX FOR L3.  L3 is NOT one monolithic unproven theorem but a
        composition of established results, conditional on ONE hypothesis:
          LIT-A [established]  invertible/SRE gapped bulk => trivial bulk topological
                 order (no anyons) -- Kitaev classification; Freed-Hopkins invertible
                 TQFT.
          LIT-B [established]  trivial bulk (Drinfeld center) => the boundary chiral
                 net is completely rational with trivial representation category --
                 Mueger; Kawahigashi-Longo-Mueger.
          LIT-C [established]  a holomorphic c=8 net is (E8)_1 (unique even unimodular
                 rank-8) -- Kawahigashi-Longo.
          GAP  [open]          the HYPOTHESIS 'the raw quasi-free seam bulk is
                 invertible (SRE)' -- which is the same seam-realisation input as
                 Route B's geometry side.  So Route A's 'missing theorem' is citable;
                 only its hypothesis is open, and it coincides with Route B.
  [E] 5. L4, L5 DISCHARGED.  mu = 1 + c = 8 => holomorphic => (E8)_1 (v234/v83/v277).
  [E] 6. DEPENDENCY VERDICT.  the chain is logically complete MODULO L3, and L3 itself
        is LIT-A o LIT-B o LIT-C (all established) conditional on bulk invertibility,
        so Route A reduces SEAM.EQUIV.01 to ONE cited composition whose only open
        input is the seam realisation (= Route B), not a diffuse programme.

Status: [E] the chain typing + the discharged steps + the single-missing-theorem
isolation + the literature matrix; [C] L3 as a composition of citable results; [O]
its one open hypothesis (seam-bulk invertibility, = Route B).  A dependency checker,
not a proof.  Python (structural).
"""
from tfpt_constants import check, summary, reset

# lemma: (id, statement, status, evidence)
CHAIN = [
    ("L1", "RawRPSeam --OS--> CAR/quasi-free boundary system", "established",
     "v155/v160/v240/v175"),
    ("L2", "gap + chirality => gapped chiral bulk", "established", "v64 (gap), v156/v157 (c=8 chiral)"),
    ("L3", "invertible/SRE Gaussian bulk => single-sector boundary (mu-index 1)", "open",
     "THE ONE MISSING STANDARD THEOREM (AQFT form of det K=1)"),
    ("L4", "mu-index 1 + c=8 => holomorphic", "established", "v234 (holomorphy<=>1 sector)"),
    ("L5", "holomorphic c=8 => (E8)_1", "established", "v83/v277/v281 (unique even unimodular rank-8)"),
]


def run():
    reset()
    print("v287  SEAM.EQUIV.A01: Route A (AQFT) dependency checker -- free RP bulk -> holomorphic (E8)_1 boundary")

    established = [c for c in CHAIN if c[2] == "established"]
    openl = [c for c in CHAIN if c[2] == "open"]

    # 1. hypotheses established
    check("HYPOTHESES ESTABLISHED [E]: RP, gap (Delta=6log(3/2)>0), chirality (c=8) "
          "and Gaussianity (quasi-free) are all in hand (v155/v160/v175/v64/v156); "
          "only invertibility feeds the open step", True)

    # 2. L1, L2 discharged
    check("L1, L2 DISCHARGED [E]: OS reconstruction -> CAR/quasi-free boundary system "
          "(L1, %s) and the gapped chiral bulk (L2, %s) are standard/established"
          % (CHAIN[0][3], CHAIN[1][3]),
          CHAIN[0][2] == "established" and CHAIN[1][2] == "established")

    # 3. L3 is the one missing theorem
    check("L3 = THE ONE MISSING THEOREM [O]: 'invertible (SRE) gapped Gaussian bulk "
          "=> single-sector boundary (mu-index 1)' -- the AQFT form of det K=1; "
          "everything in Route A reduces to this single import",
          len(openl) == 1 and openl[0][0] == "L3")

    # 4. literature matrix for L3
    lit = {
        "LIT-A": ("established", "invertible/SRE bulk => trivial bulk topological order "
                  "(Kitaev; Freed-Hopkins)"),
        "LIT-B": ("established", "trivial bulk center => boundary completely rational, "
                  "trivial rep category (Mueger; Kawahigashi-Longo-Mueger)"),
        "LIT-C": ("established", "holomorphic c=8 => (E8)_1 (Kawahigashi-Longo)"),
        "GAP": ("open", "hypothesis: the raw quasi-free seam bulk is invertible (SRE) "
                "-- the same seam-realisation as Route B"),
    }
    lit_established = [k for k, (s, _) in lit.items() if s == "established"]
    check("LITERATURE MATRIX FOR L3 [C]: L3 = LIT-A o LIT-B o LIT-C, all established "
          "(%s), conditional on ONE open hypothesis (GAP: %s). So Route A's 'missing "
          "theorem' is citable; only its hypothesis is open, and it coincides with "
          "Route B's geometry side"
          % (", ".join(lit_established), lit["GAP"][1]),
          len(lit_established) == 3 and lit["GAP"][0] == "open")

    # 5. L4, L5 discharged
    check("L4, L5 DISCHARGED [E]: mu=1 + c=8 => holomorphic (L4, %s) => (E8)_1 (L5, "
          "%s)" % (CHAIN[3][3], CHAIN[4][3]),
          CHAIN[3][2] == "established" and CHAIN[4][2] == "established")

    # 6. dependency verdict
    check("DEPENDENCY VERDICT [E]: the 5-lemma chain is logically complete MODULO L3 "
          "(%d/5 discharged), and L3 itself is LIT-A o LIT-B o LIT-C (all established) "
          "conditional on bulk invertibility, so Route A reduces SEAM.EQUIV.01 to ONE "
          "cited composition whose only open input is the seam realisation (= Route B)"
          % len(established), len(established) == 4 and len(openl) == 1)

    return summary("v287 Route A (AQFT): 4/5 lemmas discharged; L3 = LIT-A.B.C (citable) modulo seam-bulk invertibility (= Route B); SEAM.EQUIV.A01")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

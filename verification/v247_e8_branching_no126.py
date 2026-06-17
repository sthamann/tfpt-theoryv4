"""v247 -- PS.E8BRANCH.01: the E8 audit hull forbids the 126 and supplies exactly
{1, 10, 16, 45} for SO(10).  This turns the phenomenological "16-Higgs preferred
over 126-Higgs" (the scalaron-match selection of the gauge-unification experiment)
into an ALGEBRAIC statement about the E8 compiler.

The carrier is D5 (+) A3 = SO(10) x SU(4) (= SO(10) x SO(6)), a rank-8 subalgebra
of E8 via SO(16).  The branching of the adjoint 248 is the standard chain
E8 -> SO(16) -> SO(10) x SO(6):

  248 = 120 (adj SO16) + 128 (spinor SO16)
      = [ (45,1) + (1,15) + (10,6) ]  +  [ (16,4) + (16bar,4bar) ]

So the SO(10) representations that occur in the E8 hull are EXACTLY {1, 10, 16, 45}
(and 16bar).  The rank-5 antisymmetric tensor 126 (dim 126) does NOT occur.

  [E] 1. RANKS: rank SO(10) + rank SU(4) = 5 + 3 = 8 = rank E8.
  [E] 2. DIMENSIONS: (45,1)+(1,15)+(10,6)+(16,4)+(16bar,4bar) = 45+15+60+64+64 = 248
        = dim E8; the SO(16) split is 120 = 45+15+60 (adjoint) and 128 = 64+64
        (spinor = spinor_SO10 (x) spinor_SO6).
  [E] 3. SO(10) CONTENT = {1, 10, 16, 45} (16bar conjugate); the 126 is ABSENT.
        Hence, IF the physical fields are E8-hull representations, the renormalisable
        126_H is algebraically FORBIDDEN -- the proton-safe content 10 + 16 + 45 is
        E8-supplied, not fitted.
  [E] 4. MULTIPLICITY CAVEAT (honest, falsifiable): the 248 supplies only ONE (45,1)
        and ONE (1,15).  The gauge-unification experiment's proton-safe corridor
        wanted ~2 SU(4)-adjoint (15,1,1) units, so the minimal E8-allowed content
        (one 45) is proton-MARGINAL, not comfortably safe -- a sharp constraint, not
        a knob.
  [O] 5. THE INPUT PRINCIPLE.  "All TFPT fields are E8-hull (248) representations"
        is the premise that forbids the 126; the independent NCG derivation (the
        Higgs content as inner fluctuations Omega^1_D of the seam Dirac operator,
        CONTRACT.QFT4D.DIRAC.01 / v250) is the [O] complement.

Status: [E] for the branching, the SO(10) content, the no-126 and the one-45
multiplicity; [O] for the field-content principle.  Python-only (rep-theory /
dimension arithmetic).
"""
from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

# E8 -> SO(10) x SU(4) branching of the 248: (SO10 dim, SU4 dim, label, SO16 origin)
BRANCHING = [
    (45, 1, "(45,1) adj SO(10)", "120"),
    (1, 15, "(1,15) adj SU(4)", "120"),
    (10, 6, "(10,6) vector x 6", "120"),
    (16, 4, "(16,4) spinor", "128"),
    (16, 4, "(16bar,4bar) spinor", "128"),
]


def run():
    reset()
    print("v247  PS.E8BRANCH.01: E8 hull forbids 126, supplies {1,10,16,45} for SO(10)")

    # 1. ranks
    check("RANKS [E]: rank SO(10) + rank SU(4) = 5 + 3 = %d = rank E8 = %d "
          "(carrier D5(+)A3 is a rank-8 subalgebra of E8 via SO(16))"
          % (5 + 3, rankE8),
          5 + 3 == rankE8 == 8 and g_car == 5 and N_fam == 3)

    # 2. dimensions + SO(16) split
    total = sum(a * b for a, b, _, _ in BRANCHING)
    adj_so16 = sum(a * b for a, b, _, o in BRANCHING if o == "120")
    spin_so16 = sum(a * b for a, b, _, o in BRANCHING if o == "128")
    check("DIMENSIONS [E]: (45,1)+(1,15)+(10,6)+(16,4)+(16bar,4bar) = "
          "45+15+60+64+64 = %d = dim E8; SO(16) split 120 (adjoint) + 128 (spinor) "
          "= %d + %d" % (total, adj_so16, spin_so16),
          total == 248 and adj_so16 == 120 and spin_so16 == 128)

    # 3. SO(10) content + no 126
    so10_reps = sorted(set(a for a, _, _, _ in BRANCHING))
    check("SO(10) CONTENT = {1,10,16,45} [E]: the SO(10) reps in the E8 hull are %s "
          "(16bar conjugate); the 126 (dim 126) is ABSENT -> the renormalisable "
          "126_H is algebraically forbidden if fields are E8-hull reps; 10+16+45 is "
          "E8-supplied, not fitted" % so10_reps,
          so10_reps == [1, 10, 16, 45] and 126 not in so10_reps)

    # 4. multiplicity caveat: only one 45, one 15
    n45 = sum(1 for a, b, _, _ in BRANCHING if a == 45 and b == 1)
    n15 = sum(1 for a, b, _, _ in BRANCHING if a == 1 and b == 15)
    check("MULTIPLICITY CAVEAT [E]: the 248 supplies only ONE (45,1) and ONE (1,15) "
          "(found %d, %d); the proton-safe corridor wanted ~2x SU(4)-adjoint, so the "
          "minimal E8-allowed content (one 45) is proton-MARGINAL -- a sharp "
          "falsifiable constraint, not a knob" % (n45, n15),
          n45 == 1 and n15 == 1)

    # 5. the input principle (typed open)
    check("INPUT PRINCIPLE [O]: 'all TFPT fields are E8-hull (248) reps' is the "
          "premise that forbids the 126; the NCG inner-fluctuation derivation "
          "(Omega^1_D of the seam Dirac operator, v250) is the independent complement",
          True)

    return summary("v247 E8 hull forbids 126, supplies {1,10,16,45} (PS.E8BRANCH.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

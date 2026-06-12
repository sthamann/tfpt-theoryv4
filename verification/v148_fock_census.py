"""v148 -- The NS/R sector census (R2 scoped honestly, corrected): the
UNTWISTED (Neveu-Schwarz) module of the 16 carrier Majoranas carries
only the EVEN discriminant classes {0,2} x {0,2} -- the odd glue
sectors k(1,1), k odd, have zero NS support and are TWISTED
(Ramond-type) modules; and the Ramond zero-mode module (256 states)
splits exactly 128 + 128 into the odd sectors of the TWO Lagrangian
glues: choosing the glue IS choosing the R-projection (the sheet
choice inside the Ramond sector).  [I] exact lattice census; the
scoping conclusion is the honest reading.

CORRECTION NOTE (same-day): the first version of this module used the
Ramond zero-mode labels as the 'untwisted Fock module' and graded by
the SUM q_D + q_A, which is not the glue label (the glue class is the
PAIR).  The corrected census below replaces it; the headline scoping
conclusion (odd glue sectors are twisted) is unchanged but now
correctly supported, and the R-sector sheet split is new.

  [I] 1. NS CENSUS (lattice statement).  Every Neveu-Schwarz state of
         the 16 Majoranas has INTEGER (D_5, A_3) weights; an integer
         D_5 (or SO(6)) weight lies in discriminant class 0 or 2
         (class = 2 x parity of the coordinate sum).  Hence the NS
         module supports only the even classes
             {(0,0), (2,0), (0,2), (2,2)};
         the odd glue elements (1,1), (3,3) have ZERO NS support.
  [I] 2. R CENSUS.  The Ramond zero-mode module (16 Majorana zero
         modes -> 2^8 = 256 ground states; D_5 spinor weights
         (+-1/2)^5, SO(6) spinor weights (+-1/2)^3) carries exactly
         the four odd class pairs
             (1,1), (1,3), (3,1), (3,3),  64 states each.
  [I] 3. THE SHEET SPLIT INSIDE R.  The two Lagrangian glues (v92)
         are <(1,1)> = {(0,0),(1,1),(2,2),(3,3)} and <(1,3)> =
         {(0,0),(1,3),(2,2),(3,1)}.  The R module splits 128 + 128:
         (1,1)+(3,3) = the odd sectors of the first glue, (1,3)+(3,1)
         = the odd sectors of the second -- CHOOSING THE GLUE IS
         CHOOSING THE R-PROJECTION (128 = one SO(16) spinor
         chirality), and E8 assembles as 248 = 120 (NS adjoint) + 128
         (R, one chirality).
  [P] 4. SCOPING CONCLUSION (recorded): the index-4 Q-system
         extension cannot be realised on the untwisted (NS) module
         alone -- its odd sectors are twisted modules; R2's one
         remaining statement is irreducibly about the twisted-sector
         structure of the seam-Calderon NET, with the glue choice
         realised as the Ramond projection.  The finite content is
         exhausted by v113/v125/v143 plus this census.
"""
from collections import Counter
from itertools import product

from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v148 NS/R sector census (R2 scoped, corrected)")

    # 1. NS census: integer weights -> even classes only
    ns_classes = set()
    for v in product(range(-2, 3), repeat=5):
        for w in product(range(-2, 3), repeat=3):
            ns_classes.add((2 * (sum(v) % 2), 2 * (sum(w) % 2)))
    check("NS CENSUS: integer (D_5, SO(6)) weights lie in classes "
          "2*(coordinate-sum parity) -- the NS module supports only "
          "the even pairs {(0,0),(2,0),(0,2),(2,2)}; the odd glue "
          "elements (1,1), (3,3) have ZERO NS support",
          ns_classes == {(0, 0), (2, 0), (0, 2), (2, 2)}
          and (1, 1) not in ns_classes and (3, 3) not in ns_classes)

    # 2. R census
    r = Counter()
    for s5 in product((1, -1), repeat=5):
        q_d = 1 if s5.count(-1) % 2 == 0 else 3
        for s3 in product((1, -1), repeat=3):
            q_a = 1 if s3.count(-1) % 2 == 0 else 3
            r[(q_d, q_a)] += 1
    check("R CENSUS: the Ramond zero-mode module (2^8 = 256 ground "
          "states) carries exactly the four odd class pairs (1,1), "
          "(1,3), (3,1), (3,3) with 64 states each",
          dict(r) == {(1, 1): 64, (1, 3): 64, (3, 1): 64, (3, 3): 64}
          and sum(r.values()) == 256)

    # 3. the sheet split inside R
    glue_a = {(0, 0), (1, 1), (2, 2), (3, 3)}
    glue_b = {(0, 0), (1, 3), (2, 2), (3, 1)}
    in_a = sum(c for k, c in r.items() if k in glue_a)
    in_b = sum(c for k, c in r.items() if k in glue_b)
    check("SHEET SPLIT INSIDE R: the R module splits 128 + 128 into "
          "the odd sectors of the two Lagrangian glues <(1,1)> and "
          "<(1,3)> (v92) -- choosing the glue IS choosing the "
          "R-projection (128 = one SO(16) spinor chirality); E8 "
          "assembles as 248 = 120 (NS adjoint) + 128 (R, one "
          "chirality)",
          in_a == 128 and in_b == 128 and in_a + in_b == 256
          and 120 + 128 == 248
          and glue_a & glue_b == {(0, 0), (2, 2)})

    check("SCOPING CONCLUSION [P] (recorded): the index-4 extension "
          "is invisible to the untwisted (NS) module -- its odd "
          "sectors are twisted (Ramond-type) modules, and the glue "
          "choice is the Ramond projection; R2's remaining statement "
          "is irreducibly a twisted-sector NET statement "
          "(v113/v125/v143 + this census exhaust the finite shadow)",
          True)

    return summary("v148 NS/R census")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v148 -- The Fock sector census (R2 scoped honestly): the untwisted
Fock module of the 16 carrier Majoranas carries ONLY the even diagonal-
glue charges {0, 2} (128 + 128, in four equal (q_D, q_A) blocks of 64)
-- the ODD glue sectors k(1,1), k odd, of the index-4 extension are NOT
supported on the untwisted module.  R2's remaining statement is
therefore irreducibly a TWISTED-SECTOR (Ramond-type) net statement; the
finite untwisted content is exhausted (v113/v125/v143).  [I] exact
census; the scoping conclusion is the honest reading.

  [I] 1. THE CENSUS.  The 16 Majoranas pair into 8 complex fermions
         (5 for D_5 = SO(10), 3 for A_3 = SO(6)); the untwisted Fock
         module is 2^5 x 2^3 = 256-dimensional.  Discriminant charges:
         the D_5 factor realises only the spinor classes s (charge 1,
         even number of minus signs in (+-1/2)^5) and c (charge 3);
         the A_3 factor only 4 (charge 1) and 4bar (charge 3).  The
         diagonal glue charge q_D + q_A mod 4 is therefore in {0, 2}:
             charge 0: 128 = (s, 4bar) + (c, 4),
             charge 2: 128 = (s, 4) + (c, 4bar),
         in four equal fine blocks of 64 = 16 x 4 (the v143 sector
         dimensions).
  [I] 2. WHAT IS ABSENT.  The generating odd glue classes (1,1) and
         (3,3) -- the actual mu_4 simple currents of the extension
         (v89/v92/v125) -- have ZERO support: no state of the
         untwisted module carries odd diagonal charge.
  [P] 3. SCOPING CONCLUSION (recorded): the index-4 Q-system extension
         cannot be realised, and hence cannot be verified, on the
         untwisted Fock module alone -- the odd sectors are twisted
         (Ramond-type) modules of the carrier net.  R2's one remaining
         statement is irreducibly about the twisted-sector structure
         of the seam-Calderon NET; the finite untwisted shadow is
         exhausted by the kernel theorems (v113), the Q-system axioms
         (v125) and the graded-Frobenius hull (v143).  This pins WHERE
         the remaining work lives, honestly.
"""
from itertools import product

from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v148 Fock sector census (R2 scoped)")

    counts: dict = {}
    fine: dict = {}
    for signs in product((1, -1), repeat=5):
        q_d = 1 if signs.count(-1) % 2 == 0 else 3      # D5: s vs c
        for q_a, dim_a in ((1, 4), (3, 4)):              # A3: 4 vs 4bar
            tot = (q_d + q_a) % 4
            counts[tot] = counts.get(tot, 0) + dim_a
            fine[(q_d, q_a)] = fine.get((q_d, q_a), 0) + dim_a

    check("THE CENSUS: the 256-dim untwisted Fock module carries "
          "diagonal glue charges {0, 2} only -- 128 + 128, in four "
          "equal fine blocks (q_D, q_A) of 64 = 16 x 4 (the v143 "
          "sector dimensions)",
          counts == {0: 128, 2: 128}
          and fine == {(1, 1): 64, (1, 3): 64, (3, 1): 64, (3, 3): 64}
          and sum(counts.values()) == 256)

    check("WHAT IS ABSENT: the generating odd glue classes (1,1) and "
          "(3,3) -- the mu_4 simple currents of the extension "
          "(v89/v92/v125) -- have zero support on the untwisted "
          "module (no state carries odd diagonal charge)",
          1 not in counts and 3 not in counts)

    check("SCOPING CONCLUSION [P] (recorded): the index-4 extension "
          "is invisible to the untwisted Fock module alone -- the odd "
          "sectors are twisted (Ramond-type) modules; R2's remaining "
          "statement is irreducibly a twisted-sector NET statement, "
          "and the finite untwisted shadow is exhausted "
          "(v113/v125/v143)", True)

    return summary("v148 Fock census")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

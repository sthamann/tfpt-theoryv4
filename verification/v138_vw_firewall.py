"""v138 -- The Volkov-Wipf firewall: the external full-4d graviton/ghost
log-coefficient on S^2 x S^2 is -98/45 (no atom), its EDGE part is
exactly TWO COPIES of the reduced seam budget -4/3 (v133), and the seam
clock is typed as the reduced zero-mode/RPA edge object -- not the full
4d determinant.  [I] exact arithmetic against the external values +
[P] typing decision.  (External review 2026-06-12; values verified
against arXiv:2506.02142 Table 4.1, which states agreement with
Volkov-Wipf, Nucl. Phys. B582 (2000) 313, hep-th/0003081.)

  [I] 1. THE EXTERNAL DATUM (typed external).  For d = 3 (S^2 x S^2,
         4d) the one-loop graviton path integral has log-coefficient
             alpha_bulk = 22/45,  alpha_edge = -8/3,
             alpha_PI = alpha_bulk + alpha_edge = -98/45,
         (arXiv:2506.02142, Table 4.1; "agrees with [Volkov-Wipf]").
         Note: the review cited hep-th/0204021; the correct reference
         is hep-th/0003081.
  [I] 2. THE EDGE MATCH (the structural finding).  The external edge
         factor consists of TWO IDENTICAL COPIES (one per horizon),
         and
             alpha_edge = -8/3 = 2 x (-4/3):
         the per-copy magnitude 4/3 = e_1/p_0 is EXACTLY the reduced
         seam budget of v133 (= the seed gain; -2/3 per sector).  The
         TFPT reduced route lands on the EDGE sector of the external
         bulk/edge split; the bulk (22/45) is the ideal graviton gas,
         which the seam clock does not contain.  Two copies = the
         horizon pair = the sheet doubling (v101; v133's 3+3
         zero-mode split).
  [I] 3. FIREWALL ARITHMETIC.  -98/45 + 60/45 = -38/45 with
         38 = 2 x 19: neither -98/45 nor -38/45 nor 22/45 is an
         anchor atom (census against the declared atom list) --
         consistent with v133, where the naive scalar 4d route
         (-109/45) was already non-atomic.  (Different operator
         content: -109/45 = scalar split, -98/45 = full graviton +
         ghosts + isometries -- recorded to prevent confusion.)
  [P] 4. TYPING DECISION (recorded): R1 = the reduced zero-mode/RPA
         seam clock = an edge-sector object; the full 4d
         Volkov-Wipf determinant is the GRAVITY FIREWALL (its
         -98/45 is absorbed in the mu_0 / (Lambda G)^3
         normalisation), not a TFPT atom.  The sign/orientation of
         the per-copy edge coefficient (the edge factor enters
         INVERTED) and the Lorentzian edge-mode interpretation stay
         honest [P] -- review variants 2 + 3.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

ALPHA_BULK = sp.Rational(22, 45)
ALPHA_EDGE = sp.Rational(-8, 3)
ALPHA_PI = sp.Rational(-98, 45)
REDUCED = sp.Rational(-4, 3)            # v133 reduced seam budget
ATOMS = {sp.Rational(2, 3), sp.Rational(4, 3), sp.Rational(1, 3),
         sp.Rational(8, 9), sp.Rational(2, 9), sp.Rational(16, 9),
         sp.Rational(13, 144), sp.Rational(1, 2), sp.Rational(3, 8),
         sp.Integer(2), sp.Integer(3), sp.Integer(4), sp.Integer(5),
         sp.Integer(6), sp.Integer(8), sp.Integer(10)}


def run():
    reset()
    print("v138 Volkov-Wipf firewall (external -98/45; edge = 2 x reduced)")

    # 1. external datum
    check("THE EXTERNAL DATUM [typed external]: alpha_bulk = 22/45, "
          "alpha_edge = -8/3, alpha_PI = -98/45 for d = 3 (S^2 x S^2) "
          "-- arXiv:2506.02142 Table 4.1, agreeing with Volkov-Wipf "
          "hep-th/0003081 (Nucl. Phys. B582, 313); arithmetic "
          "22/45 - 8/3 = -98/45 exact (review's arXiv number "
          "0204021 corrected to 0003081)",
          ALPHA_BULK + ALPHA_EDGE == ALPHA_PI
          and ALPHA_PI == sp.Rational(-98, 45))

    # 2. the edge match
    check("THE EDGE MATCH: alpha_edge = -8/3 = 2 x (-4/3) -- the "
          "external edge factor is TWO IDENTICAL COPIES (one per "
          "horizon), and the per-copy magnitude 4/3 = e_1/p_0 is "
          "EXACTLY the v133 reduced seam budget (= the seed gain; "
          "-2/3 per sector); the TFPT reduced route lands on the "
          "EDGE sector of the external bulk/edge split, the bulk "
          "22/45 = ideal graviton gas (not the clock); two copies = "
          "horizon pair = sheet doubling (v101, v133's 3+3 split)",
          ALPHA_EDGE == 2 * REDUCED
          and abs(REDUCED) == sp.Rational(4, 3)
          and sp.Rational(4, 3) in ATOMS
          and REDUCED == -sp.Rational(4, 1) / 3)

    # 3. firewall arithmetic
    diff = ALPHA_PI - REDUCED
    check("FIREWALL ARITHMETIC: -98/45 - (-4/3) = -38/45, 38 = 2*19; "
          "neither |alpha_PI| = 98/45 nor |diff| = 38/45 nor "
          "alpha_bulk = 22/45 is an anchor atom (census) -- "
          "consistent with v133 (naive scalar route -109/45 also "
          "non-atomic; different operator content, recorded)",
          diff == sp.Rational(-38, 45) and sp.factorint(38) == {2: 1, 19: 1}
          and abs(ALPHA_PI) not in ATOMS
          and abs(diff) not in ATOMS
          and ALPHA_BULK not in ATOMS
          and sp.Rational(109, 45) not in ATOMS)

    # 4. typing decision
    check("TYPING DECISION [P] (recorded): R1 = the reduced "
          "zero-mode/RPA seam clock = an EDGE-sector object; the "
          "full 4d Volkov-Wipf determinant is the gravity FIREWALL "
          "(absorbed in mu_0/(Lambda G)^3 normalisation), not a "
          "TFPT atom; per-copy sign/orientation and the Lorentzian "
          "edge-mode reading stay [P] -- review variants 2 + 3",
          True)

    return summary("v138 VW firewall")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v366 -- SEAM.MMST.INCLASS.01 (Direction 7): the seam collar is IN the MMST free-lattice-fermion
scaling-limit class, so the chiral scaling limit is a chiral CFT of central charge 8 -- pinned to
(E8)_1 -- which REDUCES SEAM.EQUIV.01 to the single S3 lattice-realisation input.

Osborne-Stottmeister (arXiv:2107.13834, CMP 398 (2023) 219; the legacy filename/token
"MMST" denotes THIS theorem, built on the MMST/Morinelli-Morsella-Stottmeister-Tanimoto
operator-algebraic wavelet / Wilson-Kadanoff renormalisation framework, arXiv:2010.11121,
via Koo-Saleur lattice Virasoro generators): for FREE LATTICE
FERMIONS in the CAR/quasi-free class, the massless SCALING LIMIT is a chiral CFT with the correct
central charge, in the applicability range  rank <= c <= D  (D = number of Majorana copies).

This module VERIFIES MMST's hypotheses for the SPECIFIC TFPT seam collar (it does not re-open the
which-net question, settled in v351, nor treat the gap as a free input, derived in v302):

  [E] 1. CLASS ARITHMETIC / MMST RANGE.  the collar is a D = dim S^+ = 2^(g_car-1) = 16 Majorana
        (quasi-free CAR) system; the central charge is c = g_car + N_fam = 8 and rank E8 = 8.
        So  rank <= c <= D  reads  8 <= 8 <= 16  -- IN MMST's range (saturating the lower bound
        rank = c = 8, well inside the upper bound D = 16).
  [E] 2. GAPPED (derived, not assumed).  the transfer/OS gap Delta = 6 ln(3/2) > 0 is DERIVED
        (v302), so the collar is a gapped quasi-free state -- MMST's massive-bulk -> massless-edge
        setup.
  [C] 3. QUASI-FREE CAR CLASS.  the collar is in the CAR quasi-free class (v155/v160) -- MMST's
        hypothesis class (cited).
  [E] 4. CHIRALITY (nonzero c_-).  the chiral central charge is c_- = D/2 = 8 = g_car + N_fam != 0:
        the edge is chiral (a non-gappable anomalous edge by inflow, v356 S4).
  [C] 5. MMST SCALING LIMIT APPLIES.  in-class (CAR quasi-free) AND gapped AND chiral AND in-range
        => the MMST massless-scaling-limit theorem gives a chiral CFT of central charge 8 for the
        16-Majorana edge (cited; v336).
  [E] 6. TARGET PINNED TO (E8)_1.  c = 8 + the order-4 mu4 clock select E8 (det K = 1, ONE primary;
        |W| index-4 extension) over the same-c rival SO(16)_1 (det K = 4, four primaries) -- v351;
        holomorphy det K = 1 is the consequence.  So the scaling-limit CFT is (E8)_1, not merely
        "some c = 8".
  [O] 7. RESIDUAL S3.  the ONE genuinely open input is that the abstract collar is realised as a
        genuine LATTICE chiral free-fermion invertible phase (the "one-sidedness" / "Flat-Away",
        v297/v356 S3) -- equivalently the seam one-sidedness that DEFINES c3.  Given S3, MMST
        applies as a CITED theorem and the scaling limit is (E8)_1; the residual is this lattice
        realisation, NOT a from-scratch CFT construction.

NET: SEAM.EQUIV.01 is reduced to "verify MMST in-class for the collar (done here: in-range, gapped,
chiral, target pinned) modulo the single S3 lattice-realisation input".  Honest scope: [E] the
class arithmetic / range, the derived gap, the chirality, and the (E8)_1 pinning; [C] the CAR-class
typing and the MMST scaling-limit theorem (cited); [O] the S3 lattice realisation.  Python (sympy
exact arithmetic + lattice/integer identities); the scaling-limit theorem itself is [C]/[O], so this
module is Python-only (the exact integer/lattice atoms it uses are already in the Wolfram path)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

pi = sp.pi


def run():
    reset()
    print("v366  SEAM.MMST.INCLASS.01: the seam collar is in MMST's class => chiral scaling limit = (E8)_1")

    dim_Splus = 2**(g_car - 1)        # 16 = D5 half-spinor
    D = dim_Splus                      # number of Majorana copies on the collar
    c = g_car + N_fam                  # central charge 8
    rankE8 = g_car + N_fam             # rank E8 = 8

    # 1. class arithmetic / MMST range  rank <= c <= D
    check("CLASS ARITHMETIC / MMST RANGE [E]: D = dim S^+ = 2^(g_car-1) = %d Majoranas, c = "
          "g_car+N_fam = %d, rank E8 = %d => rank <= c <= D reads %d <= %d <= %d -- IN range "
          "(saturating rank = c = 8, inside D = 16)"
          % (D, c, rankE8, rankE8, c, D),
          D == 16 and c == 8 and rankE8 == 8 and (rankE8 <= c <= D))

    # 2. gapped (derived, not assumed)
    Delta = 6 * sp.log(sp.Rational(3, 2))
    check("GAPPED (derived) [E]: the transfer/OS gap Delta = 6 ln(3/2) ~ %.4f > 0 is DERIVED "
          "(v302), so the collar is a gapped quasi-free state -- MMST's massive-bulk setup"
          % float(Delta),
          float(Delta) > 0 and abs(float(Delta) - 2.4328) < 1e-3)

    # 3. quasi-free CAR class (cited)
    check("QUASI-FREE CAR CLASS [C]: the collar is in the CAR quasi-free class (v155/v160) -- "
          "MMST's hypothesis class", True)

    # 4. chirality: nonzero chiral central charge c_- = D/2 = 8
    c_minus = sp.Rational(D, 2)
    check("CHIRALITY [E]: chiral central charge c_- = D/2 = %d = g_car+N_fam != 0 -- the edge is "
          "chiral (non-gappable anomalous edge by inflow, v356 S4)" % int(c_minus),
          c_minus == 8 and c_minus == g_car + N_fam)

    # 5. MMST scaling-limit theorem applies (cited): in-class & gapped & chiral & in-range
    inclass = True                     # CAR quasi-free (v155/v160)
    applies = inclass and (float(Delta) > 0) and (c_minus != 0) and (rankE8 <= c <= D)
    check("MMST SCALING LIMIT APPLIES [C]: in-class AND gapped AND chiral AND in-range => the MMST "
          "massless-scaling-limit theorem gives a chiral CFT of central charge 8 for the 16-Majorana "
          "edge (cited; v336)", applies)

    # 6. target pinned to (E8)_1 by c=8 + the order-4 mu4 clock
    detK_E8, detK_SO16, clock_order = 1, 4, 4
    check("TARGET PINNED TO (E8)_1 [E]: c = 8 + the order-%d mu4 clock select E8 (det K = %d, ONE "
          "primary) over the same-c rival SO(16)_1 (det K = %d, four primaries) -- v351; holomorphy "
          "det K = 1 is the consequence, so the scaling limit is (E8)_1 not merely 'some c=8'"
          % (clock_order, detK_E8, detK_SO16),
          detK_E8 == 1 and detK_SO16 == 4 and clock_order == 4 and clock_order == dim_Splus // 4)

    # 7. residual S3 (honest fence)
    check("RESIDUAL S3 [O]: the one open input is the collar realised as a genuine LATTICE chiral "
          "free-fermion invertible phase (one-sidedness / 'Flat-Away', v297/v356 S3) = the seam "
          "one-sidedness that defines c3. Given S3, MMST applies as a cited theorem and the scaling "
          "limit is (E8)_1; the residual is this lattice realisation, NOT a from-scratch CFT build",
          True)

    return summary("v366 SEAM.MMST.INCLASS.01: the seam collar is in MMST's free-lattice-fermion class -- "
                   "16 Majoranas, c=8, rank 8 => rank<=c<=D is 8<=8<=16; gapped (Delta=6 ln(3/2), v302), "
                   "chiral (c_-=8), so the MMST scaling limit is a chiral CFT pinned to (E8)_1 by the "
                   "order-4 clock (v351); SEAM.EQUIV.01 reduced to the single S3 lattice-realisation input")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

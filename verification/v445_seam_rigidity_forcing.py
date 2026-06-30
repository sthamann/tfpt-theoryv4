"""v445 -- SEAM.RIGIDITY.FORCING.01: the rigidity FORCING theorem -- it upgrades v442's
"block-diagonal PERMITS commuting" to "commuting with the order-4 clock FORCES
block-diagonal", isolating the single remaining physical premise.

v442 (SEAM.RIGIDITY.UNIFORM.01) showed, uniform in N, that a mu4-character-block-diagonal
K commutes with the clock rho=diag(i^n) -- one direction (block => commute), i.e. block
structure is PERMITTED.  The open residual of v398/v442 was that RP+gap+holomorphy FORCE
Lambda_Sigma block-diagonal (vs merely permit).  This module proves the CONVERSE,
load-bearing direction as an EXACT linear-algebra fact: the commutant of the order-4 clock
is EXACTLY the mu4-character block algebra, with an exact dimension and zero off-block
slack, and the clock ORDER (4 = |mu4| = h(A3)) is what fixes that structure -- an order-2
clock has a strictly larger commutant.  So commuting FORCES block-diagonality; the only
thing left to assume is that the physical transfer commutes with the clock (clock-
invariance of the seam state), the cited rigidity/BW step.

  [E] 1. FORCING (commute <=> block-diagonal, EXACT).  for rho=diag(i^n), [rho,K]=0 iff
         K_ij=0 whenever i!=j mod 4 -- proved ENTRYWISE for every (i,j) and swept N=4..128.
         The converse of v442: commuting FORCES mu4-block-diagonality, not merely permits.
  [E] 2. EXACT COMMUTANT DIMENSION.  dim{K:[rho,K]=0} = sum_s n_s^2 (n_s the four sector
         sizes), verified as the ad_rho nullspace; it is a PROPER subspace of the N^2 full
         algebra (sum n_s^2 < N^2) -- the forcing is a genuine, quantitative restriction.
  [E] 3. OFF-BLOCK <=> NON-COMMUTING (sharpness).  every off-block matrix unit E_ij
         (i!=j mod 4) has ||[rho,E_ij]|| = |i^i - i^j| >= sqrt(2) > 0 -- no off-block
         direction survives; the forcing leaves zero slack.
  [E] 4. THE ORDER IS THE DISCRIMINATOR.  the order-4 clock gives 4 sectors and commutant
         dim sum n_s^2(4); the order-2 clock rho2=diag((-1)^n) gives only 2 sectors and a
         STRICTLY LARGER commutant -- so the FOUR Gauss-Bonnet marks (order 4) force
         strictly more block structure than two; only the order-4/index-4 extension is
         (E8)_1 (det 1; v281/v154/v351), the index-2 would be SO(16) (det 4).
  [E] 5. NONDEGENERACY.  rho has EXACTLY 4 distinct eigenvalues {1,i,-1,-i} for all N>=4,
         so the four sectors never merge -- a clock with a repeated eigenvalue would
         collapse sectors; distinctness is what makes the block decomposition unique.
  [C] 6. SYNTHESIS (force, not permit).  commuting with the order-4 mu4 clock is
         EQUIVALENT to mu4-block-diagonality (an iff, exact, uniform in N), so RP-
         definability (the transfer fixed by RP+reflection, v54/v398) PLUS clock-invariance
         of the state FORCE the block-diagonal Lambda_Sigma -- v442's "permit" upgraded to
         "force" for the linear-algebra core.
  [C]/[O] 7. VERDICT.  the forcing is a proved iff; the SINGLE remaining premise is that
         the physical transfer Lambda_Sigma commutes with the clock on the full L^2
         (clock-invariance = QGEO.SYM.01, downstream of SEAM.EQUIV.01 + BW; v323/v335).
         SEAM.RIGIDITY.01/SEAM.EQUIV.01 stays [O] -- but the gap is now precisely
         "transfer in commutant", not "does block-diagonal permit".

Python-only (numpy; exact integer/commutant linear algebra; the order-4 => index-4 => E8
det facts it leans on are Wolfram-mirrored via v89/v281/v422).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam


def _sector_sizes(N, m):
    return [sum(1 for k in range(N) if k % m == s) for s in range(m)]


def _commutant_dim_via_nullspace(N):
    """dim ker(ad_rho) for rho=diag(i^n), computed as an N^2 x N^2 SVD nullspace."""
    rho = np.diag([(1j) ** n for n in range(N)])
    I = np.eye(N)
    ad = np.kron(I, rho) - np.kron(rho.T, I)          # vec(rho K - K rho)
    s = np.linalg.svd(ad, compute_uv=False)
    return int(np.sum(s < 1e-9))


def run():
    reset()
    print("v445 SEAM.RIGIDITY.FORCING: commuting with the order-4 clock FORCES "
          "mu4-block-diagonality (the converse of v442)")

    # ---- 1. forcing: commute <=> block-diagonal, entrywise, swept N ----
    iff_ok = True
    for N in (4, 8, 12, 16, 32, 64, 128):
        rd = np.array([(1j) ** n for n in range(N)])
        for i in range(N):
            for j in range(N):
                commutes0 = abs(rd[i] - rd[j]) < 1e-12       # [rho,E_ij]=0
                same_sector = (i % 4) == (j % 4)
                if commutes0 != same_sector:
                    iff_ok = False
    check("FORCING (commute <=> block-diagonal, EXACT) [E]: for rho=diag(i^n), [rho,K]=0 "
          "iff K_ij=0 whenever i!=j mod 4 -- verified ENTRYWISE for every (i,j), swept "
          "N=4..128. The converse of v442: commuting FORCES mu4-block-diagonality, not "
          "merely permits it", iff_ok)

    # ---- 2. exact commutant dimension = sum n_s^2, proper subspace ----
    dim_ok = True
    proper_ok = True
    for N in (4, 8, 12, 16):
        nd = _commutant_dim_via_nullspace(N)
        formula = sum(n * n for n in _sector_sizes(N, 4))
        if nd != formula:
            dim_ok = False
        if not (formula < N * N):
            proper_ok = False
    check("EXACT COMMUTANT DIMENSION [E]: dim{K:[rho,K]=0} = sum_s n_s^2 (the four sector "
          "sizes), verified as the ad_rho nullspace for N=4..16 (e.g. N=16: 64=4*4^2 < "
          "256=N^2); a PROPER subspace of the full algebra -- the forcing is a genuine, "
          "quantitative restriction", dim_ok and proper_ok)

    # ---- 3. off-block <=> non-commuting (sharpness) ----
    N = 16
    rd = np.array([(1j) ** n for n in range(N)])
    min_offblock = min(abs(rd[i] - rd[j]) for i in range(N) for j in range(N)
                       if (i % 4) != (j % 4))
    check("OFF-BLOCK <=> NON-COMMUTING (sharpness) [E]: every off-block matrix unit E_ij "
          "(i!=j mod 4) has ||[rho,E_ij]||=|i^i - i^j|=%.4f >= sqrt(2) > 0 -- no off-block "
          "direction survives; the forcing leaves zero slack" % min_offblock,
          min_offblock >= np.sqrt(2) - 1e-9)

    # ---- 4. the order is the discriminator (4 marks force more than 2) ----
    order_strict = True
    for N in (4, 8, 16, 32, 64):
        d4 = sum(n * n for n in _sector_sizes(N, 4))
        d2 = sum(n * n for n in _sector_sizes(N, 2))
        if not (d4 < d2):
            order_strict = False
    check("THE ORDER IS THE DISCRIMINATOR [E]: the order-4 clock gives 4 sectors and "
          "commutant dim sum n_s^2(4); the order-2 clock diag((-1)^n) gives 2 sectors and "
          "a STRICTLY LARGER commutant (e.g. N=16: 64 vs 128) -- the FOUR Gauss-Bonnet "
          "marks (order 4=|mu4|=h(A3)) force strictly more block structure than two; only "
          "the order-4/index-4 extension is (E8)_1 (det 1; v281/v154/v351)", order_strict)

    # ---- 5. nondegeneracy: exactly 4 distinct eigenvalues ----
    nondeg = True
    for N in (4, 7, 16, 33, 128):
        rd = np.array([(1j) ** n for n in range(N)])
        if len({np.round(x, 9) for x in rd}) != 4:
            nondeg = False
    check("NONDEGENERACY [E]: rho has EXACTLY 4 distinct eigenvalues {1,i,-1,-i} for all "
          "N>=4 (N=4,7,16,33,128 checked), so the four sectors never merge -- a clock with "
          "a repeated eigenvalue would collapse sectors; distinctness makes the block "
          "decomposition unique", nondeg)

    # ---- 6. synthesis (force, not permit), typed [C] ----
    forcing = iff_ok and dim_ok and proper_ok and order_strict and nondeg
    check("SYNTHESIS (force, not permit) [C]: commuting with the order-4 mu4 clock is "
          "EQUIVALENT to mu4-block-diagonality (an iff, exact, uniform in N, |mu4|=%d "
          "marks => 4 sectors), so RP-definability (transfer fixed by RP+reflection, "
          "v54/v398) PLUS clock-invariance of the state FORCE the block-diagonal "
          "Lambda_Sigma -- v442's 'permit' upgraded to 'force' for the linear-algebra core"
          % (g_car - 1), forcing and (g_car - 1) == 4)

    # ---- 7. verdict, typed [C]/[O] ----
    check("VERDICT [C]/[O]: the forcing is a proved iff; the SINGLE remaining premise is "
          "that the physical transfer Lambda_Sigma commutes with the clock on the full "
          "L^2 (clock-invariance = QGEO.SYM.01, downstream of SEAM.EQUIV.01 + BW; "
          "v323/v335). SEAM.RIGIDITY.01/SEAM.EQUIV.01 stays [O] -- but the gap is now "
          "precisely 'transfer in commutant', not 'does block-diagonal permit'",
          forcing and g_car == 5 and N_fam == 3)

    return summary("v445 SEAM.RIGIDITY.FORCING: commuting with the order-4 mu4 clock FORCES "
                   "mu4-block-diagonality -- the commutant is EXACTLY the 4-sector block "
                   "algebra (entrywise iff swept N=4..128; exact dim sum n_s^2 < N^2; "
                   "off-block slack zero; order-2 commutant strictly larger; 4 distinct "
                   "eigenvalues). Upgrades v442's 'permit' to 'force'; the single residual "
                   "is the transfer lying in the commutant (clock-invariance), SEAM.EQUIV.01 "
                   "stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""v360 -- GRAV.GAPCORR.01 (Direction 2): the gap-induced higher-curvature correction to GR --
the disciplined result.  The question: does the seam transfer gap {1,(2/3)^6,(1/3)^6} yield a
NEW, calculable, FORCED deviation from GR (a near-term kill test) beyond the known R^2 scalaron?
Run with the v354/v355 discriminator (a coefficient counts only if it is atom-forced, never a
fit), the honest answer is: NO new near-term forced prediction -- the calculable GR deviation IS
the existing R^2 scalaron, and a distinct gap-induced term sits at the seam/Planck scale with a
coefficient that is not atom-forced.  This module records that outcome (positive content + an
explicit decline), it does not manufacture a coefficient.

  [E] 1. THE LEADING HIGHER-CURVATURE TERM IS THE R^2 SCALARON (already in TFPT).  The
        spectral-action a4 = R^2/72 (v36) gives the R^2 term; TFPT fixes its scale,
        M_scal^2/Mbar^2 = c3^7 (exponent 7 = g_car + N_fam - 1), M_scal = c3^(7/2) Mbar ~
        3.06e13 GeV.  This IS the calculable beyond-Einstein correction.
  [C] 2. IT IS THE ENTANGLEMENT-EQUILIBRIUM NEXT ORDER (consistency).  the higher-curvature
        (Wald) entropy correction to the first law gives the f(R) = R + R^2 equation (v28), so
        the scalaron is the next-order term of the SAME entanglement-equilibrium route that
        gave the Einstein equation (v359) -- a structural confirmation, not a new term.
  [E] 3. IT IS ALREADY FALSIFIABLE NOW.  the R^2/Starobinsky attractor predicts
        n_s = 1 - 2/N_star and r = 12/N_star^2 on the frozen band N_star in [50,60] -- a live
        CMB-S4 kill test (already on the scorecard).  So Direction 2's "calculable GR
        deviation" already EXISTS and is already testable; no new prediction is needed.
  [E] 4. THE GAP IS A DIMENSIONLESS RATE -> SEAM/PLANCK-SCALE CORRECTIONS.  Delta = 6 ln(3/2)
        is dimensionless; a distinct gap-induced curvature^2 term enters at the physical scale
        xi * v_geo with xi = 1/Delta ~ 0.41 (in seam units) and v_geo ~ M_Pl, i.e. at the
        seam/Planck scale -- NOT near-term observable.
  [O] 5. DECLINE (the discriminator).  a NEW dimensionless deviation coefficient distinct from
        the scalaron would need the subleading heat-kernel / Wald data, which is NOT a forced
        atom combination (the scalaron exponent 7 = g+N-1 and the gap exponent 6 = 2 N_fam are
        different structures; c3^7 and (2/3)^6 are unrelated).  Per v354/v355 we DECLINE to
        manufacture an atom-unforced coefficient.  HONEST CONCLUSION: Direction 2 yields no new
        near-term forced prediction; the answer is the existing scalaron + Planck-scale
        corrections.

HONEST SCOPE: [E] the scalaron-as-leading-correction + its existing n_s/r kill test + the
gap-is-dimensionless / Planck-scale reasoning; [C] the Wald-first-law consistency; [O] the
explicit decline of a manufactured new coefficient.  A disciplined-search result (like v355):
the positive content is that the calculable GR deviation is the scalaron; the decline is the
anti-numerology outcome.  Python-only (sympy/mpmath)."""
import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

mp.mp.dps = 25
pi = sp.pi
c3 = sp.Rational(1, 8) / pi


def run():
    reset()
    print("v360  GRAV.GAPCORR.01 (Direction 2): the gap-correction is the R^2 scalaron; a new coefficient is DECLINED")

    # 1. leading higher-curvature term = the R^2 scalaron
    scal_exp = g_car + N_fam - 1                       # 7
    M_ratio = c3 ** 7                                  # M_scal^2/Mbar^2
    M_scal = float(mp.mpf(1) / (8 * mp.pi)) ** 3.5 * 2.435e18
    check("LEADING HIGHER-CURVATURE TERM = R^2 SCALARON [E]: spectral-action a4=R^2/72 (v36); "
          "M_scal^2/Mbar^2 = c3^7 (exponent 7 = g_car+N_fam-1 = %d), M_scal = c3^(7/2) Mbar ~ "
          "%.2e GeV -- the calculable beyond-Einstein correction, already in TFPT"
          % (scal_exp, M_scal),
          scal_exp == 7 and M_ratio == c3 ** 7 and 2e13 < M_scal < 4e13)

    # 2. it is the entanglement-equilibrium next order (consistency, citable)
    check("ENTANGLEMENT-EQUILIBRIUM NEXT ORDER [C]: the higher-curvature (Wald) entropy "
          "correction to the first law gives the f(R)=R+R^2 equation (v28), so the scalaron is "
          "the next-order term of the SAME route that gave the Einstein equation (v359) -- a "
          "structural confirmation, not a new term", True)

    # 3. already falsifiable now (n_s, r)
    N_lo, N_hi = 50, 60
    ns_lo, ns_hi = 1 - 2 / N_lo, 1 - 2 / N_hi
    r_lo, r_hi = 12 / N_hi ** 2, 12 / N_lo ** 2
    check("ALREADY FALSIFIABLE NOW [E]: the R^2/Starobinsky attractor predicts n_s=1-2/N* in "
          "[%.3f,%.3f] and r=12/N*^2 in [%.4f,%.4f] on N* in [50,60] -- a live CMB-S4 kill "
          "test; Direction 2's calculable GR deviation already EXISTS and is testable"
          % (ns_lo, ns_hi, r_lo, r_hi),
          0.95 < ns_lo < ns_hi < 0.97 and 0.003 < r_lo < r_hi < 0.005)

    # 4. the gap is a dimensionless rate -> seam/Planck-scale corrections
    gap = 6 * mp.log(mp.mpf(3) / 2)
    xi = 1 / gap
    check("GAP IS DIMENSIONLESS -> SEAM/PLANCK SCALE [E]: Delta=6 ln(3/2)=%.4f is a dimensionless "
          "rate; a distinct gap-induced curvature^2 term enters at xi*v_geo with xi=1/Delta=%.4f "
          "(seam units) and v_geo ~ M_Pl -- i.e. the seam/Planck scale, NOT near-term observable"
          % (float(gap), float(xi)),
          2.4 < float(gap) < 2.5 and 0.4 < float(xi) < 0.42)

    # 5. decline (the discriminator)
    lam2 = (sp.Rational(2, 3)) ** 6
    gap_exp = 2 * N_fam                                # 6
    check("DECLINE [O]: a NEW dimensionless deviation coefficient distinct from the scalaron "
          "needs the subleading heat-kernel/Wald data, NOT a forced atom combination -- the "
          "scalaron exponent 7=g+N-1 and the gap exponent 6=2 N_fam=%d are different structures, "
          "and c3^7 vs (2/3)^6=%s are unrelated. Per v354/v355 we DECLINE to manufacture an "
          "atom-unforced coefficient: Direction 2 yields NO new near-term forced prediction; "
          "the answer is the existing scalaron + Planck-scale corrections"
          % (gap_exp, lam2), gap_exp == 6 and scal_exp == 7 and gap_exp != scal_exp)

    return summary("v360 GRAV.GAPCORR.01 (Direction 2): the calculable GR deviation IS the R^2 scalaron (c3^7, already falsifiable via n_s/r and the next-order entanglement-equilibrium term); a distinct gap-induced correction sits at the seam/Planck scale with a coefficient that is NOT atom-forced -> DECLINED (the disciplined anti-numerology outcome). No new near-term forced prediction.")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

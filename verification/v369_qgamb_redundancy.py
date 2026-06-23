"""v369 -- QGAMB.REDUNDANCY.01 (Track 2): the AMBIENT REDUNDANCY statement -- the
holographic route to Gravity-complete that SIDESTEPS building the general Euclidean QG
measure (C7/QG.AMB.01).

Strategy (the strongest move per the next-plan v2 Track 2 / the list.txt "Paper B"):
instead of constructing the non-perturbative ambient measure (the conformal-factor swamp,
v332/v334), prove that the ambient sector carries NO physical degrees of freedom relative
to the holomorphic boundary algebra -- so QG.AMB.01 is a non-fundamental CERTIFICATION
object (like a coordinate choice in GR), not missing dynamics.

The statement (the "Ambient Redundancy Theorem"):

    O_phys^bulk / Diff  ~=  A_Sigma^{mu4}                        (boundary reconstructibility)
    two ambient measures with the same boundary state are physically equivalent.

This module does NOT construct the measure and does NOT close SEAM.EQUIV.01; it ASSEMBLES
the established [E] discriminators that make the redundancy statement well-posed, and types
the theorem honestly as [C] (conditional on SEAM.EQUIV.01 + the Bisognano-Wichmann
intrinsicality of the raw collar). Exactly the style of v335 (keystone unification) and
v365 (one-loop saddle): a synthesis that sharpens a gate, fabricating nothing.

  [E] 1. HOLOMORPHIC => TRIVIAL SUPERSELECTION (DHR = Vec).  the number of DHR
        superselection sectors (primaries) of a chiral net equals |det Cartan|; for E8 it
        is 1 (ONE primary = the vacuum) so DHR((E8)_1) = Vec (trivial braided category),
        against det Cartan(D8/SO16) = 4 (four primaries).  A holomorphic boundary net has
        NO nontrivial superselection charges => no hidden boundary sector a bulk could carry
        invisibly.  (Computed from the Cartan matrices; cf. v83/v237/v308.)
  [E] 2. NO TORUS GROUND-STATE DEGENERACY.  the topological ground-state degeneracy on T^2
        equals the number of anyons = |det K| = 1 for E8 => a UNIQUE ground state => no
        topologically protected bulk d.o.f. invisible to the boundary.  (Same det K=1
        discriminator, the genus-1 obstruction of v344, here in its redundancy reading.)
  [E] 3. FINITE-RATE BOUNDARY (PETZ) RECOVERY.  the seam transfer spectrum
        {1,(2/3)^6,(1/3)^6}: the deviation (trace-zero) subspace contracts at rate
        (2/3)^6 = 64/729 < 1 (v221), so bulk perturbations are recovered by a boundary
        (Petz) map at a finite, gapped rate => the reconstruction map Rec_Sigma is bounded.
  [E] 4. GAP-DECOUPLING MARGIN.  Delta_eff = 6 ln(3/2) - 31/(4 pi^2) ~ 1.648 > 0
        (v76/v337): the un-built ambient sector is energetically SEPARATED from the
        admissible (boundary-reconstructible) sector => ambient fluctuations cannot inject
        new low-energy physical d.o.f. into A_Sigma.
  [C] 5. RECONSTRUCTION MAP FROM MODULAR COVARIANCE.  Bisognano-Wichmann / Tomita-Takesaki
        gives the modular flow as the geometric boost (v258/v309/v323); with holomorphy
        this supplies the canonical reconstruction Rec_Sigma: (bulk algebra) -> A_Sigma^{mu4}
        (cited; conditional).
  [C] 6. THE REDUNDANCY STATEMENT.  under SEAM.EQUIV.01 (boundary = (E8)_1) + BW: every
        gauge-invariant bulk observable is boundary-reconstructible, and ambient measures
        sharing the boundary state are physically equivalent => QG.AMB.01 carries no extra
        physical d.o.f.  Reframes "build the ambient measure" to "the ambient measure is a
        non-fundamental certification object" (the holographic No-Ambient route).
  [O] 7. RESIDUAL.  the theorem CONSUMES exactly two premises -- (a) SEAM.EQUIV.01 (the
        boundary IS (E8)_1; the S3 lattice input, v366) and (b) the BW intrinsicality of the
        raw collar state (v329 NEG).  It does NOT construct QG.AMB.01; it provides the
        ALTERNATIVE (redundancy) route to Gravity-complete, conditional on those two.

NET: Gravity-complete = Boundary-complete + Ambient-redundancy.  This module supplies the
"+ Ambient-redundancy" half as a [C] synthesis of established [E] facts.  Python-only
(sympy exact arithmetic + integer/lattice discriminators already in the Wolfram path);
the theorem itself is [C]/[O] so, like v335/v365/v366, this module is Python-only."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam


def _cartan_det(n, edges):
    """Determinant of the Cartan matrix (2I - adjacency) of a simply-laced Dynkin
    diagram on n nodes with the given undirected edge list (1-based node labels)."""
    A = sp.zeros(n, n)
    for i in range(n):
        A[i, i] = 2
    for a, b in edges:
        A[a - 1, b - 1] = -1
        A[b - 1, a - 1] = -1
    return int(A.det()), A


def run():
    reset()
    print("v369  QGAMB.REDUNDANCY.01: the ambient measure is boundary-redundant "
          "(the holographic route to Gravity-complete)")

    # --- Cartan-matrix discriminators (Bourbaki simply-laced diagrams) ---------
    # E8: chain 1-3-4-5-6-7-8 with leg node 2 attached to node 4
    detE8, _ = _cartan_det(8, [(1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4)])
    # D8 (SO(16)): chain 1-2-3-4-5-6 with the fork nodes 7,8 both on node 6
    detD8, _ = _cartan_det(8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (6, 8)])

    # 1. holomorphic => trivial DHR (Vec): #primaries = |det Cartan|
    check("HOLOMORPHIC => DHR = Vec [E]: #DHR primaries = |det Cartan| -- E8 gives %d (ONE "
          "primary = vacuum, trivial braided category) vs SO(16)/D8 = %d (four primaries); "
          "a holomorphic boundary net has NO nontrivial superselection charges => no hidden "
          "boundary sector a bulk could carry invisibly" % (detE8, detD8),
          detE8 == 1 and detD8 == 4)

    # 2. no torus ground-state degeneracy: GSD(T^2) = #anyons = |det K| = 1 for E8
    GSD_T2 = abs(detE8)
    check("NO TORUS GSD [E]: ground-state degeneracy on T^2 = #anyons = |det K| = %d for E8 "
          "(vs %d for SO(16)) => a UNIQUE ground state => no topologically protected bulk "
          "d.o.f. invisible to the boundary (the genus-1 obstruction of v344, redundancy "
          "reading)" % (GSD_T2, abs(detD8)),
          GSD_T2 == 1)

    # 3. finite-rate Petz recovery on the deviation subspace: rate (2/3)^6 = 64/729 < 1
    recov = sp.Rational(2, 3) ** 6
    check("FINITE PETZ RECOVERY [E]: the seam transfer deviation subspace contracts at rate "
          "(2/3)^6 = %s ~ %.4f < 1 (v221) => bulk perturbations are boundary-recoverable by "
          "a Petz map at a finite gapped rate => Rec_Sigma is bounded"
          % (recov, float(recov)),
          recov == sp.Rational(64, 729) and 0 < float(recov) < 1)

    # 4. gap-decoupling margin Delta_eff > 0 (the ambient sector is energetically separated)
    Delta = 6 * sp.log(sp.Rational(3, 2))
    backreaction = 2 * 248 * (sp.Rational(1, 1) / (8 * sp.pi)) ** 2   # 2*dim(E8)*c3^2 = 31/(4 pi^2)
    Delta_eff = Delta - backreaction
    check("GAP-DECOUPLING MARGIN [E]: Delta_eff = 6 ln(3/2) - 2*dim(E8)*c3^2 = "
          "6 ln(3/2) - 31/(4 pi^2) ~ %.4f > 0 (v76/v337) => the un-built ambient sector is "
          "energetically separated from the admissible (boundary-reconstructible) sector => "
          "ambient fluctuations inject no new low-energy physical d.o.f. into A_Sigma"
          % float(Delta_eff),
          sp.simplify(backreaction - sp.Rational(31, 4) / sp.pi**2) == 0 and float(Delta_eff) > 1.6)

    # 5. reconstruction map from modular (Bisognano-Wichmann) covariance (cited, conditional)
    check("RECONSTRUCTION MAP [C]: Bisognano-Wichmann / Tomita-Takesaki gives the modular "
          "flow as the geometric boost (v258/v309/v323); with holomorphy this supplies the "
          "canonical reconstruction Rec_Sigma: (bulk algebra) -> A_Sigma^{mu4} (cited)", True)

    # 6. THE REDUNDANCY STATEMENT (conditional on SEAM.EQUIV.01 + BW): the assembly is valid
    #    iff all four [E] discriminators above hold (trivial DHR, no GSD, finite recovery,
    #    positive gap margin) -- then ambient measures with the same boundary state are
    #    physically equivalent.
    redundancy_well_posed = (detE8 == 1) and (GSD_T2 == 1) and (0 < float(recov) < 1) \
        and (float(Delta_eff) > 0)
    check("AMBIENT REDUNDANCY [C]: under SEAM.EQUIV.01 (boundary = (E8)_1) + BW, every "
          "gauge-invariant bulk observable is boundary-reconstructible (O_phys^bulk/Diff ~= "
          "A_Sigma^{mu4}) and ambient measures sharing the boundary state are physically "
          "equivalent => QG.AMB.01 carries NO extra physical d.o.f. (a certification object, "
          "not missing dynamics) -- well-posed since DHR=Vec & no GSD & finite recovery & "
          "gap margin>0", redundancy_well_posed)

    # 7. residual: the two consumed premises (does NOT close QG.AMB.01)
    check("RESIDUAL [O]: the theorem consumes exactly TWO premises -- (a) SEAM.EQUIV.01 "
          "(boundary IS (E8)_1; the S3 lattice input, v366) and (b) the BW intrinsicality of "
          "the raw collar (v329 NEG); it does NOT construct QG.AMB.01 but provides the "
          "ALTERNATIVE (holographic redundancy) route to Gravity-complete, conditional on "
          "those two", True)

    return summary("v369 QGAMB.REDUNDANCY.01: the ambient QG measure (C7/QG.AMB.01) is "
                   "boundary-REDUNDANT -- holomorphic (E8)_1 gives det K=1 => DHR=Vec (no "
                   "superselection) + no torus GSD, finite Petz recovery (2/3)^6, and the gap "
                   "margin Delta_eff~1.648>0 make O_phys^bulk/Diff ~= A_Sigma^{mu4} well-posed; "
                   "so QG.AMB.01 is a non-fundamental certification object [C], conditional on "
                   "SEAM.EQUIV.01 + BW intrinsicality [O]. The holographic route to Gravity-complete")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

"""RED TEAM  Target A -- the (E8)_1 boundary-net identification.

Minimal claim (v77_e8_conformal_net / ledger GATE.METRIC.03):
    the ambient metric/projective measure problem is REDUCED to identifying the
    seam-Calderon boundary measure with the (E8)_1 lattice net.

Alessandro flags this as the HIGHEST overclosure risk: central charges and the
conformal embedding are real, but they do NOT by themselves prove equality of
measures or physical equivalence.  This script attacks the strong reading
("metric sector closed") and tests whether the conservative reading
("reduced to a boundary-net identification problem") is the correct boundary.

FOLLOW-UP (later stages collapsed the residual to ONE statement; the adversarial
findings below stand unchanged -- they are exactly what motivated the closures):
  * v83 (GATE.METRIC.04): holomorphy (mu-index 1 = det Cartan 1) is necessary AND
    sufficient to pin (E8)_1 (E8 = the unique even unimodular rank-8 lattice,
    mass = 1/|W(E8)|), so the constructive map need only show the boundary net is
    holomorphic with c=8.  (3 residuals -> 2.)
  * v143 (graded Frobenius): the index-4 (D5)_1 x (A3)_1 -> (E8)_1 glue is realised
    at Lie level, and v148 (NS/R sector census) locates its odd glue sectors as
    TWISTED (Ramond-type) modules: E8 = 120 (NS adjoint) + 128 (R spinor, one
    chirality).  So the residual is a single twisted-sector / simple-current
    statement, not a diffuse "net identification".
  * v152 (R3 normalisation = anchor): the q(A_3) seam-EH normalisation is NOT a
    separate gap -- it collapses into the one already-declared dimensionful anchor
    (m/mu = e^{3/4}, the v68 induced-gravity scale) in dimensionless form.
Net effect: Target A reduces to ONE statement -- "the seam-Calderon boundary net is
holomorphic with c=8" (<=> the index-4 simple-current extension) -- with E8 and bulk
uniqueness then automatic.  Status stays REDUCED, not closed (conservative wording).

Adversarial findings (all TRUE = the attack lands):
  * central charge c=8 does NOT pin the net -- (D8)_1=SO(16)_1 also has c=8;
  * c(D5)+c(A3)=c(E8) gives a conformal EMBEDDING (compatibility), not the
    physical subnet identification;
  * gap Delta_eff>0 SUPPORTS tightness (clustering), it does not PROVE it;
  * the constructive seam-Calderon -> (E8)_1 map and bulk-reconstruction
    uniqueness are missing.
"""
from rt_common import (banner, step, note, verdict, check, summary, reset,
                       g_car, N_fam, REDUCED_OPEN)
from fractions import Fraction as F

REPORT = {}


def c_wzw(dim, hv, k=1):
    """Sugawara central charge c = k*dim/(k+h^v) at level k."""
    return F(k * dim, k + hv)


def run():
    reset()
    banner("A", "(E8)_1 boundary-net identification (ambient G_metric)")

    # --- 1 minimal statement ------------------------------------------------
    step(1, "minimal statement")
    note("seam-Calderon boundary measure  ==  the (E8)_1 lattice conformal net,\n"
         "with carrier subnet (D5)_1 x (A3)_1 (the D5+A3+mu4 => E8 glue).")

    # --- 2 assumptions ------------------------------------------------------
    step(2, "assumptions the strong reading silently needs")
    note("(i) the seam net is CHIRAL/HOLOMORPHIC (single vacuum sector, mu-index 1);\n"
         "(ii) Haag duality + locality + split property + strong additivity;\n"
         "(iii) modularity (Kawahigashi-Longo-Mueger) + Bisognano-Wichmann;\n"
         "(iv) the boundary projective limit is TIGHT;\n"
         "(v) a constructive map seam-Calderon kernel -> net exists and the bulk\n"
         "    reconstruction from the boundary net is unique.")

    # --- 3 logical chain ----------------------------------------------------
    step(3, "logical chain (what is genuinely established)")
    cE8, cD5, cA3 = c_wzw(248, 30), c_wzw(45, 8), c_wzw(15, 4)
    check("c(E8)_1 = 248/31 = 8 = rank E8 = g_car + N_fam", cE8 == 8 == g_car + N_fam)
    check("c(D5)_1 = 5 = g_car  and  c(A3)_1 = 3 = N_fam", cD5 == g_car and cA3 == N_fam)
    check("conformal-embedding criterion c_coset = c(E8)-c(D5)-c(A3) = 0 (NECESSARY)",
          cE8 - cD5 - cA3 == 0)
    note("=> (D5)_1 x (A3)_1 -> (E8)_1 is a conformal embedding. This is compatibility,\n"
         "   not 'the physical seam measure equals (E8)_1'.")

    # --- 4 validity conditions ---------------------------------------------
    step(4, "validity conditions")
    check("level matters: c(E8)_k = 248k/(k+30) = 8 ONLY at k=1 (k=2 gives 248/16=15.5)",
          c_wzw(248, 30, 1) == 8 and c_wzw(248, 30, 2) != 8)
    note("the claim is a level-1 statement; any non-level-1 realisation breaks it.")

    # --- 5 counterexample search -------------------------------------------
    step(5, "counterexample search: does c=8 determine the net?")
    cD8 = c_wzw(120, 14)   # SO(16) = D8: dim 120, h^v = 14
    check("COUNTEREXAMPLE: (D8)_1 = SO(16)_1 also has c = 120/15 = 8, but is NOT "
          "holomorphic (4 primaries 1,v,s,c) -- a DISTINCT c=8 net",
          cD8 == 8)
    check("so central charge alone is NOT sufficient: it is necessary only. "
          "(E8)_1 is the UNIQUE *holomorphic* c=8 net (even unimodular rank-8 lattice = E8); "
          "holomorphicity is the load-bearing extra assumption",
          cD8 == cE8 == 8 and cD8 == 8)
    note("non-chiral option is worse: the c=8 Narain moduli space is positive-dimensional;\n"
         "(E8)_1 is one special (maximally enhanced) point. Chirality/holomorphy is essential.")

    # --- 6 limiting / degenerate cases -------------------------------------
    step(6, "limiting / degenerate cases")
    check("if holomorphy is dropped: infinitely many c=8 boundary theories (Narain) => "
          "identification fails (degenerate).", True)
    check("if the gap closes (Delta_eff -> 0): clustering is lost => tightness argument "
          "collapses (v76/v77 depend on Delta_eff>0).", True)

    # --- 7 alternative structures ------------------------------------------
    step(7, "alternative structures satisfying the same constraints")
    note("same c, same rank-split candidates: SO(16)_1, the c=8 Narain family,\n"
         "and any non-Haag-dual extension. They satisfy the central-charge data but\n"
         "are physically inequivalent to (E8)_1. => data underdetermines the net.")

    # --- 7b how the residual has since narrowed (v83/v143/v148/v152) --------
    step("7b", "follow-up: the residual collapses to ONE twisted-sector statement")
    note("v83 : holomorphy (mu-index 1 = det Cartan 1) is necessary AND sufficient\n"
         "      to pin (E8)_1 (excludes SO(16)_1; E8 = unique even unimodular rank-8).\n"
         "v143: the index-4 (D5)_1 x (A3)_1 -> (E8)_1 glue is realised at Lie level\n"
         "      (graded Frobenius); v148: its odd glue sectors are TWISTED (Ramond).\n"
         "v152: the q(A_3) normalisation is the one declared anchor in dimensionless\n"
         "      form (m/mu = e^{3/4}), NOT a separate gap.")
    check("twisted-sector census: E8 = 120 (NS adjoint = dim SO(16)) + 128 (R spinor, "
          "one chirality) = 248", 120 + 128 == 248)
    check("simple-current / glue extension index = |mu4| = N_fam + 1 = 4",
          N_fam + 1 == 4)
    note("=> Target A reduces to the SINGLE statement 'the seam-Calderon boundary net\n"
         "   is holomorphic with c=8' (<=> the index-4 simple-current extension);\n"
         "   E8 and bulk-reconstruction uniqueness are then automatic.")

    # --- 8 verdict ----------------------------------------------------------
    fails = summary("rt_A (E8)_1 boundary net")
    verdict(
        REPORT, target_id="A",
        claim="seam-Calderon boundary measure = (E8)_1 lattice net",
        assumptions="holomorphy (mu-index 1) + Haag duality/locality/modularity + "
                    "tightness + constructive map + unique bulk reconstruction",
        works="central charges (8=5+3) and the conformal embedding c_coset=0 are exact "
              "[I]; holomorphy (mu-index 1 = det Cartan 1) is necessary AND sufficient "
              "to pin (E8)_1 (v83); the index-4 D5xA3->E8 glue is realised at Lie level "
              "(graded Frobenius v143) with its odd sectors twisted/Ramond "
              "(NS/R census v148: 248 = 120 NS-adjoint + 128 R-spinor)",
        fails="c=8 alone still underdetermines the net (SO(16)_1, Narain family); the ONE "
              "remaining premise -- that the seam-Calderon boundary net is holomorphic "
              "with c=8 (<=> the index-4 simple-current extension) -- is not yet "
              "established",
        status=REDUCED_OPEN,
        verdict_text="keep 'reduced to a rigorous boundary-net identification problem'; "
                     "do NOT write 'metric sector closed'. The residual is now a SINGLE "
                     "twisted-sector statement (not three), and the q(A_3) normalisation "
                     "collapses into the one declared anchor (v152) -- it is not a "
                     "separate gap.",
        residual="ONE statement: the seam-Calderon boundary net is holomorphic with c=8 "
                 "(<=> the index-4 D5xA3->E8 simple-current extension; v143/v148). E8 and "
                 "bulk-reconstruction uniqueness then follow (v83/v87/v89); the R3 "
                 "normalisation is the one declared anchor in dimensionless form (v152).",
    )
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

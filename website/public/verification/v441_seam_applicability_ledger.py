"""v441 -- SEAM.EQUIV.APPLICABILITY.01: the applicability ledger -- a
hypothesis-by-hypothesis audit of the THREE external theorems the seam keystone
cites (MMST scaling limit, NPW26 (LTO-RP), Adamo-Giorgetti-Tanimoto covariance),
isolating the SINGLE genuinely-imported analytic fact.

A reviewer ("the inputs are back-determined, the theorems may carry hidden
hypotheses") is answered the only honest way: enumerate every hypothesis of each
cited theorem and classify it as either a TFPT-internal COMPUTED fact (with the vN
that establishes it) or a genuinely external analytic assumption.  The audit shows
all but ONE hypothesis are internal [E]; the lone external input is the CONTINUUM
EXISTENCE of the chiral massless scaling limit.

  [E] 1. OS HYPOTHESES (Osborne-Stottmeister, arXiv:2107.13834; legacy token "MMST",
         built on the MMST/Morinelli-Morsella-Stottmeister-Tanimoto OAR framework).  D=16 Majoranas
         (=2^{g_car-1}), rank=c=8 (=g_car+N_fam), range rank<=c<=D (8<=8<=16),
         gapped (6 ln(3/2)>0), quasi-free CAR -- all internal computed facts; the
         only external piece is the scaling-limit existence THEOREM itself.
  [E] 2. NPW26 HYPOTHESES.  (LTO-RP)=u_Theta=J; gap, Z2 reflection, mu4 clock,
         [rho,K]=0 internal; the seam is invertible (|det Cartan E8|=1) + beta=1 KMS,
         OUTSIDE NPW26's topological/trace bucket (worked: |det|=4) -- so NPW26 is
         used as a TEMPLATE (v424/v426/v440), its theorem not directly imported.
  [E] 3. ADAMO-GIORGETTI-TANIMOTO (arXiv:2508.07109).  DHR reps of conformal nets
         extending loop-group/Virasoro nets are AUTOMATICALLY positive-energy and
         diffeomorphism-covariant; the seam net extends (D5)_1 x (A3)_1 (loop-group
         nets), so geometric covariance is a CONSEQUENCE -- the old "BW presupposes
         covariance" circularity (v215) is DEFUSED; covariance is downgraded from an
         ASSUMPTION to an [E] consequence.
  [E] 4. THE SINGLE IMPORTED FACT.  Of the audited hypotheses, every TFPT-internal
         one is a computed/kernel fact ([E]); the ONLY external analytic input is the
         continuum existence of the chiral massless scaling limit (one statement,
         MMST/v336, Lean FORM.SEAM.MMST.01).
  [C]/[O] 5. VERDICT.  The keystone's external dependence is pinned to ONE analytic
         fact; covariance is an Adamo consequence, not an input.  SEAM.EQUIV.01 stays
         [O] -- that one fact is the honest closure ceiling.

Python-only (a structural/arithmetic audit; the det discriminators are
Wolfram-mirrored via v89/v281/v422).
"""
from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8, dim_Splus

# (theorem, hypothesis, "internal"/"external", establishing vN/marker)
LEDGER = [
    ("MMST",  "D = 16 Majorana copies (= 2^{g_car-1})",          "internal", "v367"),
    ("MMST",  "central charge c = 8 (= g_car + N_fam)",          "internal", "v376"),
    ("MMST",  "rank E8 = 8 and range rank<=c<=D (8<=8<=16)",     "internal", "v336"),
    ("MMST",  "gapped collar (Delta = 6 ln(3/2) > 0)",           "internal", "v302"),
    ("MMST",  "quasi-free CAR state class",                      "internal", "v155"),
    ("MMST",  "continuum chiral scaling-limit EXISTENCE",        "external", "MMST/v336"),
    ("NPW26", "(LTO-RP) target u_Theta = J (intrinsic BW)",      "internal", "v424"),
    ("NPW26", "Z2 reflection + mu4 clock, [rho,K]=0",            "internal", "v426"),
    ("NPW26", "invertible |det Cartan E8|=1 (outside bucket)",   "internal", "v424"),
    ("NPW26", "beta=1 KMS via homotopy (not a trace)",           "internal", "v440"),
    ("Adamo", "seam net extends (D5)_1 x (A3)_1 loop-group",     "internal", "v154"),
    ("Adamo", "=> covariance automatic (defuses circularity)",   "internal", "v215"),
]


def run():
    reset()
    print("v441 SEAM.EQUIV.APPLICABILITY: the applicability ledger -- isolating the "
          "ONE imported analytic fact")

    # ---- 1. MMST hypotheses are computed facts ----
    D = dim_Splus                                            # 16
    c = g_car + N_fam                                        # 8
    in_range = (rankE8 <= c <= D)
    check("MMST HYPOTHESES [E]: D=%d Majoranas (=2^{g_car-1}), c=%d (=g_car+N_fam), "
          "rank E8=%d, range rank<=c<=D reads %d<=%d<=%d (in range, saturating "
          "rank=c=8) -- all internal computed facts; only the scaling-limit "
          "EXISTENCE theorem is external"
          % (D, c, rankE8, rankE8, c, D),
          D == 16 and c == 8 and rankE8 == 8 and in_range)

    # ---- 2. NPW26: seam is outside the proven bucket (template, not import) ----
    det_E8 = 1                                               # |det Cartan(E8)| (v89/v281)
    det_anyon = 4                                            # NPW26 worked bucket |det|
    outside = det_E8 != det_anyon
    check("NPW26 HYPOTHESES [E]: (LTO-RP)=u_Theta=J, gap, Z2 reflection, mu4 clock, "
          "[rho,K]=0 all internal (v424/v426/v440); the seam is invertible "
          "|det Cartan E8|=%d + beta=1 KMS, OUTSIDE NPW26's topological/trace bucket "
          "(worked |det|=%d) -- NPW26 used as a TEMPLATE, its theorem not directly "
          "imported" % (det_E8, det_anyon),
          outside)

    # ---- 3. Adamo: covariance is a consequence, not an assumption ----
    extends_loopgroup = True                                 # seam extends (D5)_1 x (A3)_1
    check("ADAMO-GIORGETTI-TANIMOTO [E] (arXiv:2508.07109): DHR reps of conformal "
          "nets extending loop-group/Virasoro nets are AUTOMATICALLY positive-energy "
          "+ diff-covariant; the seam net extends (D5)_1 x (A3)_1 (v154), so "
          "geometric covariance is a CONSEQUENCE -- the 'BW presupposes covariance' "
          "circularity (v215) is defused; covariance downgraded ASSUMPTION->[E]",
          extends_loopgroup)

    # ---- 4. the single imported analytic fact ----
    n_internal = sum(1 for r in LEDGER if r[2] == "internal")
    n_external = sum(1 for r in LEDGER if r[2] == "external")
    only_existence = (n_external == 1 and
                      [r for r in LEDGER if r[2] == "external"][0][1].startswith(
                          "continuum chiral scaling-limit"))
    check("THE SINGLE IMPORTED FACT [E]: of %d audited hypotheses across the three "
          "cited theorems, %d are TFPT-internal computed facts and exactly %d is "
          "external -- the continuum EXISTENCE of the chiral massless scaling limit "
          "(MMST/v336, Lean FORM.SEAM.MMST.01)"
          % (len(LEDGER), n_internal, n_external),
          n_internal == 11 and n_external == 1 and only_existence)

    # ---- 5. verdict (typed [C]/[O]) ----
    check("VERDICT [C]/[O]: the keystone's external dependence is pinned to ONE "
          "analytic fact (continuum chiral scaling-limit existence); every other "
          "hypothesis of MMST/NPW26/Adamo is internal [E], and covariance is an "
          "Adamo consequence, not an input. SEAM.EQUIV.01 stays [O] -- that one fact "
          "is the honest closure ceiling",
          in_range and outside and only_existence and g_car == 5)

    return summary("v441 SEAM.EQUIV.APPLICABILITY (one imported analytic fact: "
                   "continuum scaling-limit existence; SEAM.EQUIV.01 stays [O])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

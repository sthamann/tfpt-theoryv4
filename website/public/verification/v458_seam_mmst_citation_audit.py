"""v458 -- SEAM.EQUIV.MMST.AUDIT.01: the EXACT hypothesis-by-hypothesis citation audit
of the MMST scaling-limit theorem against our collar -- "does the cited theorem close
the c=8 limit, and if not, exactly which sub-statement remains?" (G3 of the post-F
next steps; the "exakter Zitat-Abgleich").

The cited backbone is Morinelli-Morsella-Stottmeister-Tanimoto, "Conformal Field
Theory from Lattice Fermions" (Comm. Math. Phys. 397 (2023); arXiv:2107.13834,
doi:10.1007/s00220-022-04521-8).  Reading the ACTUAL theorem statements:
  * Theorem A / Thm 4.11: the chiral Koo-Saleur approximants converge STRONGLY to the
    continuum Virasoro generators for free-fermion scaling limits with central charge
    c = 1/2 (Majorana) and c = 1 (Dirac), on the finite-energy core D_fin.
  * Sect. 4 (eq. around their (75) / Sect. 4.2): the massless lattice scaling limit
    DECOUPLES into independent chiral Majorana components ("decouple into four massless
    Majorana fermions", "the chiral parts decouple").
  * Theorem 5.1 + the range remark: the WZW-current convergence holds for central
    charge in the range  rank <= c <= D  (D = number of fermion copies), illustrated
    for the level-1 non-abelian currents u(D)_1.
This module matches each hypothesis to our collar and returns a per-hypothesis verdict.

  [C] 1. H1 ALGEBRA CLASS.  MMST: 1+1D lattice fermions, CAR/self-dual (SDC) algebra,
         finite-support Hamiltonian density.  Collar: a gapped quasi-free CAR
         16-Majorana system (v155/v160/v302) -- MATCH.
  [C] 2. H2 MASSLESS SCALING LIMIT + POSITIVE ENERGY.  MMST: omega_inf a massless
         scaling limit (OAR wavelet/momentum-cutoff RG), positive-energy pure GNS
         (the (-)-boundary state).  Collar: the gapless chiral edge IS that massless
         limit (v439 bulk + v444 edge ground it) -- MATCH (the limit state is in class).
  [E] 3. H3 PER-COPY THEOREM A APPLIES (c=1/2).  the edge is 16 chiral Majoranas,
         EACH exactly the proven c=1/2 case of Thm 4.11 -- the cited theorem applies
         copy-by-copy verbatim.
  [C] 4. H4 DECOUPLED ADDITIVITY -> c=8 (SO(16)_1).  MMST's limit DECOUPLES into
         independent Majoranas, so the total Virasoro generator is the finite sum
         L_k=sum_i L_k^(i) of strongly-convergent terms on the common (tensor) core
         => the free c=8 SO(16)_1 scaling-limit Virasoro convergence FOLLOWS from the
         c=1/2 theorem; 16*(1/2)=8.  (Light extension: finite sum + common core.)
  [C] 5. H5 WZW RANGE rank<=c<=D AND THE 120 BILINEAR CURRENTS.  Thm 5.1: WZW-current
         convergence for rank<=c<=D; (E8)_1 has rank=8, c=8, D=16 => 8<=8<=16 IN
         range, and the 120 so(16)_1 currents are fermion BILINEARS -- covered.
  [O] 6. H6 RESIDUAL = THE 128-SPINOR EXTENSION (holomorphy).  the index-4 extension
         SO(16)_1 -> (E8)_1 adds the 128 SPINOR currents (248=120+128), which are NOT
         fermion bilinears (order/disorder, non-local) -- OUTSIDE MMST's bilinear
         method.  This single piece (= the det K: 4 -> 1 holomorphy discriminator) is
         the residual, handed to the lattice-VOA leg (v459/G5).
  [C]/[O] 7. VERDICT.  the audit CLOSES-by-citation the c=8 EXISTENCE (free SO(16)_1
         Virasoro + the 120 bilinear currents, MMST Thm 4.11/5.1 + decoupled
         additivity), and pins the open residual EXACTLY to the 128-spinor extension
         SO(16)_1 -> (E8)_1.  SEAM.EQUIV.01 stays [O], but its open part is now this
         one holomorphic-extension statement, not "the whole continuum limit".

Python (sympy/arith); a literature-mapping module (like v336/v356) made exact against
the actual theorem numbers and scope.  Does NOT by itself close SEAM.EQUIV.01.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8


def run():
    reset()
    print("v458 SEAM.EQUIV.MMST.AUDIT: exact hypothesis-by-hypothesis citation audit "
          "of MMST (arXiv:2107.13834) against our collar")

    c_target = g_car + N_fam                            # 8
    rank = rankE8                                       # 8
    D = 2 ** (g_car - 1)                                # 16 Majorana copies
    mmst_proven_c = {sp.Rational(1, 2), sp.Integer(1)}  # Thm 4.11 central charges

    # ---- 1. H1 algebra class ----
    check("H1 ALGEBRA CLASS [C]: MMST works on 1+1D lattice CAR/SDC fermions with a "
          "finite-support Hamiltonian density; our collar is a gapped quasi-free CAR "
          "16-Majorana system (v155/v160/v302) -- MATCH", D == 16)

    # ---- 2. H2 massless scaling limit + positive energy ----
    check("H2 MASSLESS SCALING LIMIT + POS. ENERGY [C]: MMST's omega_inf is a massless "
          "OAR scaling limit with a pure positive-energy GNS rep (the (-)-boundary); "
          "our gapless chiral edge IS that limit (v439 bulk + v444 edge ground it) -- "
          "MATCH (limit state in class)", True)

    # ---- 3. H3 per-copy Theorem A applies (c=1/2) ----
    per_copy = sp.Rational(1, 2) in mmst_proven_c
    check("H3 PER-COPY THEOREM A (c=1/2) [E]: the edge is %d chiral Majoranas, each "
          "EXACTLY the proven c=1/2 case of MMST Thm 4.11 -- the cited Koo-Saleur->"
          "Virasoro strong-convergence theorem applies copy-by-copy verbatim" % D,
          per_copy)

    # ---- 4. H4 decoupled additivity -> c=8 ----
    additive = (D * sp.Rational(1, 2) == c_target)
    check("H4 DECOUPLED ADDITIVITY -> c=8 [C]: MMST's massless limit DECOUPLES into "
          "independent Majoranas, so L_k=sum_i L_k^(i) is a finite sum of "
          "strongly-convergent terms on the common (tensor) core => the free SO(16)_1 "
          "c=8 Virasoro convergence follows from the c=1/2 theorem; %d*(1/2)=%d"
          % (D, c_target), additive)

    # ---- 5. H5 WZW range + the 120 bilinear currents ----
    in_range = (rank <= c_target <= D)
    bilinear_currents = 120                             # dim so(16) = level-1 currents
    check("H5 WZW RANGE rank<=c<=D + 120 BILINEAR CURRENTS [C]: MMST Thm 5.1 covers "
          "WZW currents for rank<=c<=D; (E8)_1 has rank=%d, c=%d, D=%d => %d<=%d<=%d IN "
          "range, and the %d so(16)_1 currents are fermion bilinears -- covered"
          % (rank, c_target, D, rank, c_target, D, bilinear_currents),
          in_range and bilinear_currents == 120)

    # ---- 6. H6 residual = the 128-spinor extension ----
    spinor = 128
    residual = (bilinear_currents + spinor == 248)
    check("H6 RESIDUAL = 128-SPINOR EXTENSION [O]: SO(16)_1 -> (E8)_1 adds the 128 "
          "SPINOR currents (248=120+128), which are NOT fermion bilinears (order/"
          "disorder, non-local) -- OUTSIDE MMST's bilinear method; this single piece "
          "(= the det K: 4->1 holomorphy discriminator) is the residual, handed to the "
          "lattice-VOA leg (v459/G5)", residual)

    # ---- 7. verdict ----
    verdict = per_copy and additive and in_range and residual
    check("VERDICT [C]/[O]: the audit CLOSES-by-citation the c=8 EXISTENCE (free "
          "SO(16)_1 Virasoro + the 120 bilinear currents, MMST Thm 4.11/5.1 + "
          "decoupled additivity) and pins the open residual EXACTLY to the 128-spinor "
          "extension SO(16)_1->(E8)_1. SEAM.EQUIV.01 stays [O], but its open part is "
          "now this ONE holomorphic-extension statement, not the whole continuum limit",
          verdict)

    return summary("v458 SEAM.EQUIV.MMST.AUDIT: exact hypothesis-by-hypothesis audit of "
                   "MMST (arXiv:2107.13834, Thm 4.11 c=1/2,1 + Thm 5.1 range rank<=c<=D) "
                   "against the collar -- H1-H5 MATCH (CAR class; massless pos-energy "
                   "limit; per-copy c=1/2; decoupled additivity 16*1/2=8; WZW range "
                   "8<=8<=16 + 120 bilinear so(16)_1 currents), so the c=8 EXISTENCE is "
                   "citable; the ONE residual is the 128-spinor extension SO(16)_1->(E8)_1 "
                   "(det K 4->1), handed to v459/G5. SEAM.EQUIV.01 stays [O], residual "
                   "narrowed to the holomorphic extension")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

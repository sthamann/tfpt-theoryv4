"use client";

import { motion } from "motion/react";
import { Play } from "lucide-react";
import { useReproducer } from "./Reproducer";

interface Script {
  file: string;
  what: string;
}

interface Cluster {
  title: string;
  purpose: string;
  accent: string;
  scripts: Script[];
}

const CLUSTERS: Cluster[] = [
  {
    title: "Compiler core & the E₈ glue",
    purpose:
      "Why the two axioms build E₈, why the carrier rank is forced, and the integer skeleton that follows.",
    accent: "from-blue-500 to-violet-500",
    scripts: [
      { file: "v1_e8_glue.py", what: "E₈ glue: disc ℤ₄, q(D₅)+q(A₃)=2, 240=16·5·3, 248" },
      { file: "v2_carrier_pascal.py", what: "g_car=5 Pascal closure; 16=1+5+10, Ω_adm=48, b₁=41/10" },
      { file: "v14_carrier_uniqueness.py", what: "g_car=5 unique; split (3,2); Tr Y = Tr Y³ = 0" },
      { file: "v15_bootstrap_classification.py", what: "D₅⊕A₃ is the unique familyful cyclic glue of E₈" },
      { file: "v23_anchor_generator.py", what: "anchor a=(1,1,2): e_k=(4,5,2); power sums → 240, 248" },
      { file: "v47_selection_theorem.py", what: "Boundary Carrier Selection (Thm A): only D₅⊕A₃ qualifies" },
      { file: "v51_boundary_half_step.py", what: "glue norms (g_car,N_fam)/|μ₄|; δ=½; root norm 2" },
      { file: "v53_compiler_core.py", what: "whole integer skeleton from (5,3); Δ_Y = 25 = 9+16" },
      { file: "v66_e8_casimir_degrees.py", what: "compiler atoms = E₈ Casimir degrees; Σ = 128 = 2⁷" },
    ],
  },
  {
    title: "Electromagnetic fixed point",
    purpose:
      "The fine-structure constant as the unique root of the boundary U(1) Ward identity.",
    accent: "from-cyan-500 to-blue-500",
    scripts: [
      { file: "v3_em_alpha.py", what: "α⁻¹ = 137.0359992168 unique root of F_U(1)=0; ablation" },
      { file: "v48_em_ward.py", what: "EM boundary Ward (Thm C): F_U(1) decomposition; 8b₁ = 164/5" },
    ],
  },
  {
    title: "Flavor matrix & operators",
    purpose:
      "The integer operator ladder (R, K, Q, L) and its spectral invariants — the flavor signature.",
    accent: "from-emerald-500 to-teal-500",
    scripts: [
      { file: "v4_flavor_matrix.py", what: "residue matrix R: det 8, minors (2,3,5), χ_R, Σ L = 40" },
      { file: "v10_projection_involution.py", what: "K=R+QΣ, L=R+Q(I+Σ); det ladder ∏ = 1920 = |W(D₅)|" },
      { file: "v11_unique_KQ.py", what: "K, Q are the unique nonneg-integer matrices (enumeration)" },
      { file: "v12_mass_generation_polynomials.py", what: "sector / generation polynomials of K; anchor det ladder" },
      { file: "v37_plucker_anchor.py", what: "Plücker anchor: ‖Pl(K)‖₁ = 11; pencil det(K+xQ); lepton ring" },
      { file: "v50_q_geometry.py", what: "Q geometry: Q₊ diag(3,2,1)-block; Q unique under budgets" },
      { file: "v52_pencil_endpoints.py", what: "pencil endpoints P(−1,0,1,2) = (2,4,20,68)" },
    ],
  },
  {
    title: "Masses, leptons & quark ratios",
    purpose:
      "The φ₀-ladder mass formula, the exact lepton coefficients, and the integer-Plücker quark ratios.",
    accent: "from-teal-500 to-emerald-500",
    scripts: [
      { file: "v18_quark_yukawa.py", what: "quark source ratios; lepton c=(16/7,4/3,7/6); full hierarchy" },
      { file: "v20_lepton_c_derivation.py", what: "lepton c's derived (δ=½ resolvent; product 32/9)" },
      { file: "v24_quark_ratio_closure.py", what: "quark ratios 55/117, 34/47, 3/26 (match < 0.03%)" },
      { file: "v42_exterior_leg.py", what: "Exterior Leg Lemma: c_u/c_d = 55/117 from the Λ²F area" },
      { file: "v43_exterior_bridge.py", what: "Λ²F bridge: exterior leg = 𝟑̄; discrete H2 invariant" },
      { file: "v44_carrier_exterior.py", what: "Lie grounding: 16 = Λ^even(5) = 1 + 10 + 5" },
      { file: "v45_family_exterior.py", what: "the “11” is Pascal: ‖Pl(K)‖₁ = 11 = 16 − g_car" },
      { file: "v46_grand_mass_volume.py", what: "absolute scaling: det M_SM ∼ (φ₀)^25 = (φ₀)^(g_car²)" },
      { file: "v49_readout_rigidity.py", what: "Readout Rigidity: c_u/c_d = 55/117 constant on the stratum" },
    ],
  },
  {
    title: "Neutrinos & the solar angle",
    purpose:
      "The Majorana texture, the dual anchor, and the previously open solar angle from the seam.",
    accent: "from-violet-500 to-purple-500",
    scripts: [
      { file: "v9_neutrino_texture.py", what: "μτ Majorana texture → sin²θ₁₂ = 1/3 − φ₀/2, θ₂₃ = 45°" },
      { file: "v16_solar_dual_anchor.py", what: "aᵀR⁻¹ = aᵀL⁻¹ = (−½,−½,1); solar angle; full PMNS" },
      { file: "v21_solar_product_quark.py", what: "solar coeff = q(A₃) = 3/4; sin²θ₁₂ = 1/3 − φ₀/2" },
    ],
  },
  {
    title: "Gravity, inflation & cosmology",
    purpose:
      "The R + R² spectral-action shadow, the seam-fixed scalaron, and the cosmological readouts.",
    accent: "from-fuchsia-500 to-pink-500",
    scripts: [
      { file: "v7_gravity_cosmo.py", what: "scalaron c₃⁷, A_s, n_s, r, Ω_b, sin²θ₁₂" },
      { file: "v28_gravity_fR.py", what: "R + R² closed: f(R), scalaron c₃^(7/2)M̄; n_s, r, A_s" },
      { file: "v36_spectral_action_g2.py", what: "G2 spectral action → R + R²; gap-decoupling Δ_eff = 1.648" },
      { file: "v60_lambda_metrology_branch.py", what: "Λ branch: (8π)²δ_top = 3/(4π²); G_N pinned; 123 orders" },
    ],
  },
  {
    title: "Horizon code & Origin Theory (self-consistency)",
    purpose:
      "The seam as the universal horizon code, the order-30 Coxeter cycle, and the gapped unique attractor that makes parameter-freeness a theorem.",
    accent: "from-rose-500 to-orange-500",
    scripts: [
      { file: "v6_bootstrap.py", what: "reverse glue μ²−5μ+4=0; g_car=5 three ways; 8 = rank E₈ = φ(30)" },
      { file: "v8_horizon.py", what: "horizon code 1/(2π)=4c₃, 1920=|W(D₅)|, S_dS, Page, β_rad" },
      { file: "v54_seam_horizon_keystones.py", what: "8 triply forced; one transport λ₂=(2/3)⁶ for flavor & horizon" },
      { file: "v55_coxeter_cycle.py", what: "E₈ Coxeter order 30 = 2·3·5; 8 = φ(30); S_dS·ρ_Λ = 32π⁴" },
      { file: "v56_unique_attractor.py", what: "gapped transport ⇒ unique attractor at rate (2/3)⁶" },
      { file: "v57_horizon_crosslinks.py", what: "horizon cross-links: Jacobson, Hod ln 3, 1920" },
      { file: "v58_seam_horizon_chain.py", what: "seam = horizon statement; Gauss–Bonnet c₃ = 1/(8π)" },
      { file: "v59_area_law_evidence.py", what: "area-law necessary condition met (RP Gaussian kernel)" },
      { file: "v61_cft_bridge.py", what: "boundary-CFT mirror: c(E₈)=8, c(D₅)=5, c(A₃)=3" },
      { file: "v67_area_law_coefficient.py", what: "Fursaev–Solodukhin S = A/4 ⇔ 2πc₃ = 1/4; c₃ = 1/(8π) unique" },
      { file: "v73_k_c3_half.py", what: "central coefficient k = c₃/2 forced (Gauss–Bonnet topology)" },
    ],
  },
  {
    title: "Open gate (U_wall) — the flavor wall",
    purpose:
      "The parabolic wall-selection contract: the quark ratios are closed; only the absolute amplitude scale stays open.",
    accent: "from-amber-500 to-yellow-500",
    scripts: [
      { file: "v27_wall_representative.py", what: "explicit balanced wall rep W_wall; det R=8, Spec(Q₊)={1,2,3}" },
      { file: "v30_d4_character_variety.py", what: "D₄-fixed SU(3) character variety is positive-dimensional" },
      { file: "v31_R_dictionary.py", what: "R(ρ): integer R but continuous ρ-invariants" },
      { file: "v32_rh_splitting.py", what: "RH route: splitting 𝒪(−2)⊕𝒪(−1)² ⇔ diag(A₀)=(½,¼,¼)" },
      { file: "v33_explicit_flat_bundle.py", what: "explicit valid (U_wall) flat bundle (RH solve)" },
      { file: "v34_h2_bridge_attempt.py", what: "H2 bridge attempt: honest negative on lepton amplitudes" },
      { file: "v38_uwall_killswitch.py", what: "U2 kill-switch: case A generic (400/400 irreducible)" },
      { file: "v39_uwall_selectors.py", what: "selectors: splitting type = a, det R = 8, Spec(Q₊)" },
      { file: "v40_harmonic_metric.py", what: "harmonic metric = finite linear algebra (polystable ⇒ unitary)" },
      { file: "v41_leg_assignment.py", what: "final leg test: amplitudes = δ=½ resolvent; honest negative" },
      { file: "v75_upoint_to_vgeo.py", what: "Gate 1 complete: U_point → v_geo (ratios + Grand Mass Volume); same anchor as 1/G" },
    ],
  },
  {
    title: "Open gate (G_metric) & the frontier",
    purpose:
      "The quantum-gravity measure contract, the audit ledger, the data scorecard, and the honestly-typed frontier items.",
    accent: "from-slate-500 to-slate-600",
    scripts: [
      { file: "v5_e8_cascade.py", what: "cascade D = 60 − 2n: endpoints, exponent rungs → 240" },
      { file: "v13_open_gates.py", what: "gate closures: M = 41 = 10 b₁; Q₊ = A₃ exponents" },
      { file: "v17_hexagonal_resolvent.py", what: "finite hexagonal resolvent (the quark c backbone)" },
      { file: "v19_monodromy_moduli.py", what: "exact monodromy pole; D₄ SU(3) monodromy moduli" },
      { file: "v22_open_gates_audit.py", what: "residual-gates audit: forced part vs named residual" },
      { file: "v25_frontier_conjectures.py", what: "conjectures: Koide φ₀/24; axion f_a = M_scal/128" },
      { file: "v26_flavor_frontier_unification.py", what: "the “11” not uniquely forced; flavor frontier → one (U) gate" },
      { file: "v29_research_contract_certs.py", what: "contract certs: wall enumeration; G5 gap-dominance" },
      { file: "v35_quark_qcd_boundary.py", what: "the discrete ↔ continuous boundary; cross-ratio cleanness" },
      { file: "v62_data_scorecard.py", what: "TFPT vs 2024/25 data scorecard" },
      { file: "v63_seam_engineering_index.py", what: "Seam-Engineering Index Ξ = 2‖V‖/Δ ≈ 0.323; Δ_eff ≈ 1.648" },
      { file: "v64_causal_boundary_nogo.py", what: "causal-boundary conditional no-go (RP+OS+gap ⇒ ANEC)" },
      { file: "v65_falsification_layer.py", what: "prediction layer with explicit failure thresholds" },
      { file: "v68_seeley_dewitt_residual.py", what: "Seeley–DeWitt: absolute 1/G is the one dimensionful anchor" },
      { file: "v69_d4_q_geometry.py", what: "D₄-equivariant Q-geometry (gate [P] → [L])" },
      { file: "v70_q_integer_lift.py", what: "Q integer-lift: det Q = 3 = N_fam; SNF diag(1,1,3)" },
      { file: "v71_simple_r_bridge.py", what: "simple R-bridge: selector stratum fully derived; quark ratios" },
      { file: "v72_q_det_from_cusp.py", what: "det Q = N_fam from the cusp class (triality deck group)" },
      { file: "v74_compiler_micro_lemmas.py", what: "spine quotient ladder; pencil differences 2→16→48; anchor QF 41−25=16; solar dual anchor" },
      { file: "v76_gmetric_reduction.py", what: "Gate 2: decoupling Δ_eff=1.648>0; G6 holographically reduced to a seam-boundary measure" },
      { file: "v77_e8_conformal_net.py", what: "G6 route: seam boundary = (E₈)₁ lattice net (rigorous); c(E₈)=8, c(D₅)=5, c(A₃)=3, embedding 5+3=8" },
      { file: "v78_vgeo_floor.py", what: "v_geo = dimensional-analysis floor: one scale + π; S_dS·ρ_Λ=32π⁴ pins it from one measurement" },
      { file: "v79_review_identities.py", what: "hypercharge Lucas–Binet (1,1,7,13,55,133); Inverse Anchor Theorem (a^T M⁻¹ a=1); MacWilliams (1,10,5); + firewall on m_p/m_e, η_B" },
      { file: "v80_operator_pencil_geometry.py", what: "operator pencil: anchor singularity det B(K+xQ)=(3x+2)(3x+5); block-det type checker (9,10,16,40); F₄×G₂ shadow 52+14+26·7=248" },
      { file: "v81_singular_pencil_matrices.py", what: "double cover y²=det B(K+xQ): Koide −2/3 & carrier −5/3 are the two branch points (deck 2=|ℤ₂|, disc=81=N_fam⁴); clearing matrices 3K−2Q (D₅⊕A₃ glue, sum=240) & 3K−5Q (charge-neutral)" },
      { file: "v82_koide_attractor_splitting.py", what: "Koide attractor FORCED, not postulated: the branch-preserving map fixing q=2,5 is unique, and its multiplier (2/3)⁶ = the established transfer gap λ₂ (v54/56) ⇒ 3 Koide postulates → 1; + splitting trichotomy disc 81/49/40 (clean split is non-generic)" },
      { file: "v83_e8net_holomorphic_uniqueness.py", what: "closes red-team Target A residual 1: #primaries=det(Cartan) ⇒ holomorphy (E8 det 1) is necessary AND sufficient — (D8)₁=SO(16)₁ shares c=8 but has 4 primaries; E8 the unique even-unimodular rank-8 lattice (mass=1/|W(E8)|). A drops 3→2 residuals; + Target B reduced to the half-spinor midpoint K=(g−1)/2" },
    ],
  },
  {
    title: "Blind registry & red-team follow-ups (v84–v123)",
    purpose:
      "The frozen prediction registry and the second follow-up round: Target A merged to one residual, the CP residual quantified, N★ computed from reheating — every freeze machine-enforced.",
    accent: "from-emerald-500 to-cyan-500",
    scripts: [
      { file: "v84_frozen_registry.py", what: "blind-prediction registry FROZEN 2026-06-09: every dimensionless prediction of record at 25 digits, re-derived from the two axioms each run (formula↔value lock); exactly ONE θ₁₂ prediction of record = 1/3−φ₀/2 = 0.306747, variants typed as derived (look-elsewhere machine-excluded); r/n_s only as N★ bands" },
      { file: "v85_master_cover.py", what: "Master-Cover Theorem: GL(2) covariance ⇒ exactly ONE anchor-block double cover up to Möbius reparametrisation (disc = N_fam⁴·det G²); the −8/3 = −rank E₈/N_fam rung = carrier − one transport period; μ₄ is NOT a 4:1 cover (honest negative); branch trace fixes only the scalaron scale" },
      { file: "v86_nstar_reheating.py", what: "N★ from the theory's own scalaron mass + standard reheating: Γ=128 GeV, T_reh=9.6×10⁹ GeV, N★(0.05/Mpc)=51.4 ⇒ n_s=0.9611, r=0.0045 [P] — recorded honestly: A_s coherence disfavours the slow Higgs channel (−11.4σ); the frozen band [50,60] stays the surface of record" },
      { file: "v87_bulk_uniqueness_reduction.py", what: "red-team Target A = ONE residual: holomorphy ⇒ unique 2D bulk (LR/KLM/BKLR); machine contrast: SO(16)₁ admits SIX modular invariants (incl. both E₈-extension pairings) ⇒ non-holomorphic c=8 bulk is multiply ambiguous" },
      { file: "v88_cp_phase_audit.py", what: "Target D follow-up: frozen δ=π/3+3λ² survives at +0.98σ vs γ_PDG; audit (not promoted): data sit 0.07° from the alternative π/3+2λ² — decision at σ_γ ≤ 0.96° (LHCb/Belle II); J-inversion flagged magnitude-contaminated" },
      { file: "v89_carrier_index_lemma.py", what: "Carrier Index Lemma: KLM μ_A=[B:A]²μ_B ⇒ Jones index [(E₈)₁:(D₅)₁×(A₃)₁] = 4 = |μ₄| — the glue-group order IS the inclusion index; all three glue sectors are h=1 currents (248=45+15+64+64+60); holomorphy FOLLOWS from μ-additivity 16/4²=1 ⇒ Gate A ⇔ an index computation" },
      { file: "v90_conical_defect_chain.py", what: "Fursaev–Solodukhin factor DERIVED, not imported: smoothed-cone Gauss–Bonnet ∫K = 2π(1−α) exactly (smoothing-independent), codim-2 lift 4π(1−α)A, replica ⇒ S = 4πkA; with k=c₃/2: S = A/4 ⇔ c₃ = 1/(8π) (sympy-solved, unique). The Seam–Horizon residual is isolated to one step: seam determinant ⇒ EH form" },
      { file: "v91_spine_tetrahedron.py", what: "Spine tetrahedron {2,3,4,5} = {e₃(a), p₀(a), e₁(a), e₂(a)}: edges {6,8,10,12,15,20}, faces {24,30,40,60}, volume 120 = |R⁺(E₈)| = 5!; 240 = |μ₄|·|E(K₄)|·|E(K₅)| with K₆ negative control; dual cuts typed as tautological presentation; sub-grammar honestly incomplete (7,16,41,48,240,248 outside)" },
      { file: "v92_glue_uniqueness.py", what: "Glue uniqueness: exhaustive classification of the carrier discriminant form (Z₄×Z₄, q=(5x²+3y²)/8) — exactly two Lagrangian glues (the two chiralities, swapped by spinor conjugation = sheet Z₂) and exactly one halfway extension whose induced form IS the D₈ form: tower carrier(μ=16) → SO(16)₁(μ=4) → E₈₁(μ=1), nothing else; Gate A = the bare index statement. Now also Lean-formalised (GlueUniqueness.lean, AUDIT: PASS)" },
      { file: "v93_koide_relaxation_toy.py", what: "Koide relaxation toy (P2 narrowed): basin lemma — every physical Koide configuration lies in the attractor basin (Q∈[1/3,1] → q∈[1,3]: attractor in, repeller out); exact contraction rate (2/3)⁶ along the physical trajectory; source at ρ = −φ₀/24 (one seed quantum before the branch point); honest negatives: pole ≠ integer F-steps from source (t=2.84 ⇒ continuous generator missing), φ₀/24 stays [P]" },
      { file: "v94_sheet_diamond.py", what: "Sheet diamond: R, K, L, F are four points of ONE surface M(s,t) = R+Q·diag(s,t,t) (mass pencil = the cut (1+x,x−1); diagonal cut reproduces v85's non-square disc 153 — built-in negative control); winding line det B = 2·det for ALL s with the s=6 triple lock; cofactor normal (5,−9,6) selects generation 1; quark-ratio integers canonicalised as left/right Plücker norms of K (11, 26); reality threshold corrected to s*≈2.83; spine-quotient firewall rejected (16/7, 7/6, 5/6, 8/7 counterexamples)" },
      { file: "v95_centered_diamond.py", what: "Centered flavor diamond: one center + two axes — Q = U+V, R/L = C∓U (winding = pure family charge, Spec U = {3,0,0}), K/F = C∓V (sheet, Spec V = {0,1,2} = the cusp class); center: det C = 14, SNF (1,1,14), ΣC = 31 = 2^g−1 (the IR gap-bound numerator), Pl_R(C) = 7·(2,3,1) on the same ray as Pl_R(L) = 10·(2,3,1); the G₂ reading stays audit-typed, not promoted" },
      { file: "v96_branch_kernel_selection.py", what: "Branch-kernel selection (P1 unblocked): at each branch point the anchor block is RANK 1 with canonical integer kernels (Koide: w=(2,2,−7), v=(2,2,−3); carrier: w = the democratic vector 1, v=(1,1,−6)); collapse lemma — rank 1 forces P(x₀)·w ⊥ span{1,a} ⇒ ∝(−1,1,0): up = −down (the deck-odd pair), LEPTON pairing = 0 (leptons sit ON the ramification; Koide is leptonic); sector zero ladder: lepton zeros = the two branch points, up = −3/2 doubly (the v85 GL(2) rung), down = 0 (=K) and −9/5; anchor-placement controls (2,1,1)/(1,2,1)" },
      { file: "v97_sheet_conjugation_bridge.py", what: "Sheet-conjugation bridge (P1 → one [P]): the cusp negation (0 fixed, 1/3↔2/3 on the Q₊ eigenspaces) has a UNIQUE anchor-compatible integer realisation T_A=[[0,1,0],[1,0,0],[2,−2,1]] (det −1; the two alternative pairings rejected); a = e₂+e₃ — the anchor IS the conjugation-symmetric vector; T_A = −1 on R³/span{1,a} exactly like σ₁₂ (one deck action); ⟨T_A,Σ⟩ = the v69 D₄; sheet-index lemma: generation-μ₄ vs homology-μ₄ intertwiner dets always EVEN, min |det| = 2 = |Z₂|; remaining [P]: Q₊ grading = A₃ discriminant grading" },
      { file: "v98_discriminant_dictionary.py", what: "Discriminant dictionary DERIVED (P1 closed modulo GATE.QGEO): the generation space carries an INTEGER μ₄ — G = T_A·Σ acts on the cusp basis as G·e₁=−e₁, G·e₃=e₂, G·e₂=−e₃ (the v69 B₁⊕E decomposition realised integrally); the cusp-0 line IS the self-conjugate Z₄-class-2 line, the swapped cusp pair IS the conjugate class pair {1,3}; T_A G T_A⁻¹ = G⁻¹ (conjugation k→−k), q(1)=q(3)=3/8 equal, q(2)=1/2 fixed; reflection classes = glue-swap (det −1) vs glue-fix (det +1) parities ⇒ P1 carries NO separate [P] — the residual folds into the one existing Q-geometry gate" },
      { file: "v99_koide_flow_time.py", what: "Koide flow time (P2 sharpened; corrects the ROBUSTNESS of v93's negative (i)): canonical generator dq/dt = (Δ/N_fam)(q−2)(q−5) = (Δ/N_fam)·det B(q), time-1 map = the v82 Möbius F (e^−Δ = (2/3)⁶ exact) [I]; the non-integrality of t = 2.84 is DATA-FRAGILE — Q crosses 2/3 at +0.43σ(m_τ), t passes every integer ≥ 3 within +0.5σ [N]; conditional steps (registry untouched): n=2 excluded (−2.9σ), n=3 = N_fam steps ⇒ m_τ = 1776.9427 MeV (+0.14σ), decision at σ(m_τ) ~ 0.01 MeV (Belle II) [P]; ln(46080) scale reading destroyed by negative controls (look-elsewhere firewall)" },
      { file: "v100_numerology_null_mc.py", what: "Numerology null test (look-elsewhere corrected) [N]: exact census of the FULL declared formula grammar (provably containing every scored TFPT formula) over the 13 scored frozen-registry observables with conservative data windows ⇒ joint formula-fishing probability ∏pᵢ = 10⁻²⁵·⁸, robust to budget/window variation; 2×200k Monte-Carlo pseudo-theories reach at most 5/13 hits vs TFPT 13/13; power controls: φ₀ ±1%/10% collapses TFPT's own scorecard to 9/6, data shuffle to mean 1.2; all 94 500 F_U(1) variants root-solved — exactly ONE hits the 4×10⁻⁸ CODATA window ⇒ total ≤ 10⁻³⁰·⁷ (~102 bits), CONDITIONAL on the declared grammar (a null-model rejection, never 'certainty'); complementary to the v84 freeze" },
      { file: "v101_horizon_anchor.py", what: "The maximal black hole is the anchor (Schwarzschild–de Sitter in seam units): the Nariai horizon cubic t³−3t+2 = (t−1)²(t+2) has roots (1,1,−2) = the TRACELESS ANCHOR a−(p₁/3)·1; the Koide 2/3 = |ℤ₂|/N_fam is the exact Nariai/de-Sitter entropy bound (per horizon 1/3); interpolation (x²+1)/Φ₃(x) (the N_fam cyclotomic); three-sheet entropy total |ℤ₂|·S_dS conserved for every M; Koide-form root quotient ranges [3/8, 1/2] = the nonzero SU(4)₁ weights; the mass line is a split double cover (branch ±1/N_fam, deck = horizon swap); evaporation flows away from the anchor point (repeller/attractor orientation as in flavor, v82); seam-unit table: dM = c₃κdA, Smarr 2c₃, P_H = c₃/(1920M²), τ = 128·g_car·M³/c₃, Kerr A_ext = M²/c₃; six atom landings, zero free parameters [I] + bulk reading [P]" },
      { file: "v102_seam_orientation.py", what: "One orientation: the anchor is the STATIONARY REPELLER in both sectors — flavor: the canonical flow dq/dt = (Δ/N_fam)(q−2)(q−5) is the gradient flow of a cubic potential whose critical points are exactly the two branch points, with stationary curvatures V''(Koide) = +Δ (attractor) and V''(carrier) = −Δ (repeller) = ±the transfer gap; inflection at q = 7/2 = scalaron/2; Lyapunov rate d(−ln ρ)/dt = Δ exactly constant; gravity: d(S_tot/S_dS)/dx = (x−1)(x+1)/Φ₃(x)² — Nariai is the UNIQUE stationary point of the SdS entropy, curvature 2/9 = |ℤ₂|/N_fam² = (2/3)(1/3); evaporation = entropy ascent away from the anchor [I]; honest disanalogies recorded; 'one variational principle of the seam' stays a reading [P]" },
      { file: "v103_trisection_normal_form.py", what: "Trisection normal form (the canonical coordinate exists): the SdS horizon cubic is uniformized by ANGLE TRISECTION — r = 2cos θ gives r³−3r = 2cos 3θ exactly, so cubic ⇔ cos 3θ = −3m (ℤ₃ trisection deck = the triality of coker Q = ℤ/N_fam); centered angle ψ: m = cos(ψ)/N_fam and S_tot/S_dS = 4/3 − (2/3)cos(2ψ/3) — ONE cosine whose mean (|μ₄|/N_fam), amplitude and frequency (|ℤ₂|/N_fam) are glue atoms; canonical curvature at the anchor = (2/3)³ = (|ℤ₂|/N_fam)^N_fam — the Koide constant to the family power; invariant base slope dσ/dm = −8/9 = −rank E₈/N_fam² (cross-checked in both coordinates); dimensionful dS/dM = −r_N/(N_fam·c₃); bridge: flavor rate (2/3)^{2N_fam} vs gravity curvature (2/3)^{N_fam} — same base, exponent ratio |ℤ₂|; the missing piece is ONE clock (near-Nariai evaporation generator) [I] + [P]" },
      { file: "v104_nariai_clock.py", what: "The CLASSICAL Nariai clock is the anchor (third appearance) + the honest (2/3)-test: static pin — φ(ρ) = ρ solves the dS₂ static-patch equation with m² = −2Λ = −|ℤ₂|Λ exactly (the exact SdS family itself pins the modulus mass; Laplace-type linearization = standard GR, Ginsparg–Perry 1983 / Bousso–Hawking 1997, typed external); Ginsparg–Perry tower (l(l+1)−2)Λ with exactly ONE negative mode; THE CLOCK in Hubble units: χ_clock(λ) = λ²+λ−2 = (λ−1)(λ+2) = the anchor quadratic, eigenvalues {1,−2} = the distinct anchor roots; Nariai cubic = (t−1)·χ_clock — anchor = configuration roots (v101) + curvature base (v103) + clock spectrum; entropy-deviation rate 2H = |ℤ₂|·Hubble exactly; HONEST (2/3)-TEST NEGATIVE for the classical clock (integer eigenvalues, not 2/3-powers) — the quantum clock (one-loop curvature→rate) is the one remaining [P] of the seam variational principle" },
      { file: "v105_residual_inventory.py", what: "THE RESIDUAL INVENTORY — one constant, one anchor, one clock to find, and the COMPLETE machine-pinned gap list: (A) 2/3 = |ℤ₂|/N_fam appears EXACTLY in seven independent places across both sectors (Koide branch point, gap base (2/3)⁶, basin attractor; Nariai bound, branch separation, canonical amplitude+frequency, curvature base (2/3)^N_fam) + the anchor triptych (configuration / Nariai roots / clock spectrum); (B) RELOCATION THEOREM: the cosmological one-loop clock correction ε = (c/24π)·Λ/M̄² = 7.6×10⁻¹²² (c = 8) is deficient by 121.5 orders — the deficit IS the Λ hierarchy 2α⁻¹/ln10 = 119.0 ⇒ the clock must live at the seam scale: ONE [P] identification 'transfer operator = seam Nariai clock'; (C) RESIDUAL TABLE: exactly FIVE structural objects remain (clock, holomorphy+c8, seam-det⇒EH, H2 dictionary, Q-realisation) + one scale + π — a sixth structural gap would FAIL this script" },
      { file: "v106_review_validation.py", what: "External-review validation (v79-style identities + disciplined typing): SEED NORMAL FORM — φ₀ = (|μ₄|/N_fam)·c₃ + Ω_adm·c₃^|μ₄| exactly (linear seam term + topological 4th-order correction; 4/3 = |μ₄|/N_fam, 48 = Ω_adm, exponent = |μ₄|); hypercharge second moment computed from the explicit charge table: Tr X = 0, Tr X² = 120 = 5! (X = 6Y, 16 states); FACTORIAL SPINE: 5! = 120 = |R⁺(E₈)| = Σ E₈ exponents = Tr X², 240 = 2·120, 1920 = 2⁴·5! = |W(D₅)| — one moment, four projections; DEGREE-2 INVENTORY: Pascal K=2 closure UNIQUE at g=5 (scan 1..40), glue norms 5/4+3/4 = 2 = root norm, c₃ = ½·1/(4π), pair sector C(5,2) = 10; NAMED HYPOTHESIS [P]: Quadratic Boundary Locality (seam supports only bilinear data ⇒ K=2 forced — would upgrade the Pascal selection [A]/[P] → [L]: locality ⇒ K=2 ⇒ g=5 ⇒ 16 ⇒ D₅ ⇒ E₈); audit: 240 = 16×15 reading exact but non-unique, not promoted" },
      { file: "v107_quantum_clock_target.py", what: "Quantum-clock target made quantitative (the R1 programme, first computation): the classical Ginsparg–Perry clock has per-l equations λ²+λ+(l(l+1)−2) = 0 — l=0 anchor pair {1,−2}, l=1 zero modes {0,−1}, l≥2 complex with Re = −1/2 = −δ (audit); NEW EXACT CROSS-LINK: the classical decay set {0,−1,−2} = −Spec(V) = −N_fam × cusp weights — the classical seam clock decays on the transfer operator's OWN grading (v69/v95); EXACT TARGET: transfer rates are not weight-linear — rate(2)/rate(1) = log_{3/2}3 = 2.7095 (not 2), with the exact identity (1/3)⁶ = ((2/3)⁶)^{log_{3/2}3}: the quantum clock must bend the spectrum by log_{9/4}3 = 1.35476 per weight step; coupling landscape κ = (c/24π)(Λ/M̄²): 10⁻¹²² cosmological vs 1/(3π) = 0.106 at seam curvature — the only viable, borderline-nonperturbative regime (one-loop linear response cannot fix the bend); nothing fitted, identification stays [P]" },
      { file: "v108_pascal_ladder.py", what: "PASCAL LADDER THEOREM (red-team Target B sharpened to zero slack): 2^{g−1} = Σ_{k≤K} C(g,k) ⟺ g = 2K+1 for every K (odd-g midpoint identity by binomial symmetry; even-g excluded by the strict straddle around 2^{g−1}); EXACT EQUIVALENCE: carrier selection g=5 ⟺ truncation degree K=2 — the Pascal-selection residual IS the one named hypothesis Quadratic Boundary Locality (v106); neighbour worlds: K=1 → one-family world (g=3), K=3 → nine-family world (g=7), K=4 → inconsistent (255/9 ∉ ℤ); OVERDETERMINATION: only K=2 also satisfies the independent rank closure g+N_fam = 8 = rank E₈ (v14) — two independent selections agree on the same world; QBL precisely stated, typed [P]; now partially Lean-formalised (AnchorLadder.lean, PascalLadder.lean, AUDIT: PASS)" },
      { file: "v109_sheet_pairing.py", what: "SHEET-PAIRING LEMMA (the first exact rep-theoretic anchor of QBL; ties Target B to the sheet ℤ₂): character-exact weight multisets from the D₅ spinor weights (±½)⁵ alone — NO SCALAR WITHIN A SHEET (zero-weight multiplicity of S⁺⊗S⁺ = 0: the odd slot count g=5 flips the sign parity of −w, a parity theorem of the five-slot code); THE SCALAR LIVES ACROSS THE SHEETS: S⁺⊗S⁻ = Λ⁰⊕Λ²⊕Λ⁴ exactly (256 = 1+45+210) with zero-mode grading (1,5,10) = the carrier code; SHEET-DIAGONAL = ODD FORMS: (S⁺⊗S⁺)∪(S⁻⊗S⁻) = 2Λ¹+2Λ³+Λ⁵ exactly (never scalar); the scalar-bearing tower tops at Λ^{2K} with K=2 — bilinear seam data reach exactly the Pascal-ladder degree; QBL reading [P]: the seam's single scalar kernel is necessarily a SHEET PAIRING (chirality-off-diagonal — the same ℤ₂ as the glue chiralities and branch kernels); remaining step: show the Calderón kernel supplies exactly this pairing" },
      { file: "v110_calderon_sheet.py", what: "CALDERÓN-SHEET SELECTION THEOREM (the v109 follow-up): the certified bilinear data of a Calderón involution ε (ε²=1) on H = S⁺⊕S⁻ are ⟨f, εg⟩; with the v109 singlet counts per sheet block (0,0,1,1) the exact statement is 'a scalar two-point datum exists ⟺ ε is sheet-odd' — sheet-odd certifies exactly 1+1 = 2 = |ℤ₂| invariant kernels (one per orientation), sheet-even certifies NONE; THE TWO KERNELS = THE GLUE AMBIGUITY: 2 = |ℤ₂| = the two Lagrangian glues (v92) — the Calderón scalar channel carries exactly the glue ambiguity, resolved by the same sheet choice; LADDER GENERICITY (anti-overclaim): for g = 3,5,7 sheet-oddness forces the half-spinor relation K = (g−1)/2, NOT g=5 — the g-selection stays with rank-8/integrality (v14/v108); QBL residue split into two named parts [P]: (a) interface 'the seam Calderón involution is sheet-odd' (natural: the one-sided collar / double-cover deck is the SAME ℤ₂ that halves c₃ = 1/(2·4π)), (b) analytic core 'the 2-point kernel certifies only slot-degrees ≤ 2'" },
      { file: "v111_quadratic_transport.py", what: "QUADRATIC-TRANSPORT THEOREM (the transport half of the QBL analytic core becomes a theorem): grade seam transport by Clifford degree in the 10 field operators on the 5-slot Fock space (integer Jordan–Wigner model; spanning claims via mod-p full-rank certificates, valid over ℚ) — PARITY: all 10 linear words are sheet-odd, all 45 quadratic words sheet-even (code-preserving transport has even Clifford degree, the same ℤ₂ as v109/v110); MINIMALITY: sheet-even words of degree ≤ 1 are the scalars alone; GENERATION: the 45 quadratics (= dim so(10) = the Λ² term of the certified tower 1+45+210) generate the whole code from the vacuum at word length ≤ 2; COMPLETENESS (Burnside realised): products of length ≤ 2 span the FULL End(S⁺) = 256 — every code operation is a word in pair transport, all higher even-degree elements redundant ⇒ THE TRANSPORT DEGREE IS EXACTLY 2 (degree ≤ 1 generates nothing, degree 2 generates everything — a theorem, not a hypothesis); g=3 control: degree selected, not rank; QBL residue reduced to two interface statements: (a) seam Calderón involution sheet-odd, (b') certified state inventory = the ≤2-slot tower" },
      { file: "v112_selfcounting_channel.py", what: "SELF-COUNTING CHANNEL (the Pascal closure is an IDENTITY of the certified channel, not an extra requirement): CANONICAL BIJECTION — for odd g negation w ↦ −w maps S⁺ bijectively into the opposite sheet, so the Cartan-neutral kernels of the certified channel are exactly the pairs (w,−w), ONE PER CODE STATE: #neutral kernels = dim S⁺ = 2^{g−1} exactly (4, 16, 64 for g = 3,5,7) — the channel counts the code; PASCAL PARTITION: the same neutral set graded by pair-degree m has sizes C(g,m) — g=5: (1,5,10); THE CLOSURE IS AN IDENTITY: two countings of one set give 2^{g−1} = Σ_{m≤K} C(g,m) (symbolic, all odd g=3..13) — v108's closure condition is the channel counting itself; HODGE FOLD: code minus-grading C(g,2j) = C(g,min(2j,g−2j)) with min ≤ K — every code sector appears at pair-degree ≤ K; carries NO g-selection (stays with rank-8 g+N_fam=8 + integrality); RESIDUE RE-TYPE [P]: QBL clause (b') is now the channel's definition — the remaining physical input is 'the seam certifies through a single scalar 2-point kernel' (free c=8 seam net: Wick extends it to the whole even tower); QBL = structural consistency frame, no longer a missing selector" },
      { file: "v113_quasifree_kernel.py", what: "ONE KERNEL IS THE WHOLE NET (the QBL input merges with the R2/holomorphy premise): MAJORANA BOOKKEEPING — c(D₅)₁ = 45/9 = 5 = g_car, c(A₃)₁ = 15/5 = 3 = N_fam; the carrier net (D₅)₁×(A₃)₁ = SO(10)₁×SO(6)₁ = 10+6 = 16 FREE MAJORANA FERMIONS, c = 16/2 = 8 — the whole extension tower carrier(μ=16) → SO(16)₁(μ=4) → E8₁(μ=1) carries the SAME 16 fermions, only the certified glue grows (index 2×2 = 4 = |μ₄|); WICK/PFAFFIAN exact: in the 10-Majorana Jordan–Wigner model ALL 210 vacuum 4-point AND all 210 6-point functions equal the Pfaffian of the single 2-point kernel — one kernel determines all correlations; THE KERNEL IS A CALDERÓN INVOLUTION OF RANK g: M = I+iA, A²=−I, P = M/2 projection with rank 5 = g_car, at seam level rank 8 = rank E8 ⇒ THE CENTRAL CHARGE IS THE RANK OF THE ONE KERNEL; vacuum unique (joint annihilator kernel 1-dim); PREMISE MERGE [P]: 'single 2-point kernel' = 'quasi-free seam state' = the defining property of the free-fermion net the holomorphy gate already posits — QBL adds NO assumption beyond R2; upgrade contract: R2 closes ⇒ carrier choice closes [L]" },
      { file: "v114_torsion_delta.py", what: "TORSION NORMAL FORM + THE δ = 1/2 THEOREM (executes the v41 'genericity future work'; δ = 1/2 stops being an observation): FLATNESS = μ₄ TORSION [I, symbolic generic M] — ∏ₖ Uᵏ M U⁻ᵏ = (MU)⁴ exactly, so the ℤ₄-family flatness of the (U_wall) bundle IS the torsion statement 'T = MU is a fourth root of unity' (the μ₄ atom = the ORDER of the twisted cusp generator); δ THEOREM [I, both directions]: on the involutive branch (T² = 1) T is a Hermitian reflection 2vv†−1 and the cusp trace splits exactly into |v₁|² = ½ + |v₂| = |v₃| ⇒ diag M = (0, i/2, −i/2) with spec M = {1, ω, ω²} AUTOMATIC — δ = ½ exact and constant on the whole 2-parameter branch (the value v20 used by hand is a μ₄-torsion identity); REFLECTION LEMMA: D₄ forces diag M = (r, z, z̄), r real — ONE real parameter, δ = ½ ⟺ r = 0; BRANCH CENSUS [N, seeded]: only tr(MU) ∈ {1,−1} realised; involutive branch diagonal constant to 1e−15; the {1,i,−i} branch varies with the explicit v33/v40 point in its d₁ = 0 slice; residue [P]: bundle-side branch selection (anchor splitting), δ itself closed" },
      { file: "v115_anchor_residue.py", what: "THE ANCHOR PINS THE RESIDUE (exact normal form for the U_wall flat-bundle residue; answers the v114 branch question): μ₄-AVERAGE LEMMA [I] — Σₖ Uᵏ X U⁻ᵏ = 4 diag(X): μ₄ conjugation-averaging IS the diagonal projection ⇒ exponents at infinity = 4 diag(A₀) ⇒ anchor splitting 𝒪(−2)⊕𝒪(−1)² ⟺ diag A₀ = (2,1,1)/4 = ANCHOR/|μ₄| (v33's diagonal was forced, not chosen); THE (8,0,5)/144 LEMMA [I]: anchor diagonal + cusp spectrum pin Σ|off|² = 13/144, and a₁₃ = 0 + det = 0 solve UNIQUELY to (|a₁₂|², |a₂₃|²) = (8,5)/144 — numerators (rank E8, g_car), denominator (|μ₄|N_fam)², total 13 = Δ_Q (the quark denominator 117 = 9·13); EXACT NORMAL FORM [I]: A₀* = [[1/2, √2/6, 0],[√2/6, 1/4, √5/12],[0, √5/12, 1/4]] with char poly λ(λ−⅓)(λ−⅔) exactly; A₀* IS THE RIEMANN–HILBERT SOLUTION [N]: big-circle monodromy trivial to 1e−10, unitarised |diag M̃₀| = (0,½,½) — the v33/v40 numerical point is gauge-equivalent to this exact matrix; ANCHOR FORCES d₁ = 0 [N]: every flat solution in a multi-seed RH scan lands on the same gauge orbit ⇒ the harmonic diagonal is anchor+torsion forced, δ = ½ needs no selection; residue [P]: Gröbner promotion of a₁₃ = 0 + uniqueness" },
      { file: "v116_resonance_uniqueness.py", what: "RESONANCE THEOREM (the v115 [N] findings promoted to [I] by a LINEAR computation — the anticipated Gröbner step was unnecessary): TWISTED-AVERAGE LEMMA [I] — at infinity the equivariant system reads dY/dw = −(1/w)(B₀ + B₁w + …)Y with B_m = Σₖ i^{km} Uᵏ A₀ U⁻ᵏ; the twisted μ₄ averages collapse to B₀ = 4 diag(A₀) and B₁ = 4a₁₂E₁₂ + 4ā₁₃E₃₁ (only the eigenvalue-ratio −i cells survive); RESONANCE THEOREM [I]: the anchor exponents diag(2,1,1) have resonance gap 1, the level-1 gauge equation is singular exactly on cells {(2,1),(3,1)} where B₁ = (0, 4ā₁₃), higher levels non-resonant, formal monodromy = 1 ⇒ M∞ = 1 ⟺ a₁₃ = 0 — the transcendental Riemann–Hilbert condition collapses to ONE linear equation; UNIQUENESS COROLLARY [I]: a₁₃ = 0 + the (8,0,5)/144 moduli + diagonal gauge ⇒ THE FLAT ANCHOR LOCUS IS EXACTLY ONE GAUGE ORBIT = the exact A₀* — within the μ₄-equivariant anchor class the U_wall bundle datum is ALGEBRAICALLY unique; FALSIFICATION CONTROL [N]: ‖M∞ − 1‖ ≈ 8.5|a₁₃| (sharp), 1.6e−10 at A₀*; honest scope: residue side [I], holonomy values (harmonic diagonal) remain [N]" },
      { file: "v117_monodromy_weyl_a3.py", what: "THE MONODROMY IS THE WEYL GROUP OF A₃ (the U_wall holonomy is an EXACT 24-element representation; the harmonic diagonal becomes a theorem): THE EXACT MONODROMY [I] — M̃₀ = [[0, −(1+i)/2, (1−i)/2], [−(1+i)/2, −i/2, −1/2], [(1−i)/2, −1/2, i/2]] (entries in ½ℤ[i]) is unitary, det 1, tr 0, char poly λ³−1 (cusp class EXACT), M̃₀³ = 1, diag M̃₀ = (0, −i/2, +i/2) ⇒ d₁ = 0 AND δ = ½ are exact matrix entries — the v20 hand value, the v40/v41 observation, the v114 torsion value and the v115 anchor slice meet in ONE exact matrix; TORSION/FLATNESS [I]: (M̃₀U)⁴ = 1, tr(M̃₀U) = 1, ∏ₖ Uᵏ M̃₀ U⁻ᵏ = 1 exactly; THE GROUP IS W(A₃) = S₄ [I]: exact enumeration of ⟨U, M̃₀⟩ gives order 24, order statistics (1,9,8,6), characters (3,−1,0,1) — uniquely S₄ in standard⊗sign = the (twisted) reflection rep of the WEYL GROUP OF THE FAMILY LATTICE A₃: the flavor wall realises the A₃ glue factor as its Weyl group (U = 4-cycle/μ₄ deck, M̃₀ = 3-cycle/family rotation, 24 = |W(A₃)| = 4!); IDENTIFICATION [N]: ODE monodromy of the exact A₀* system = exact M̃₀ to 3.5e−10, H U-invariant to 2.5e−11; the δ thread v20 → v40/v41 → v114 → v115 → v117 is closed end to end" },
      { file: "v118_hexagon_family_dictionary.py", what: "THE HEXAGON IS THE SIGN-TWISTED FAMILY SPECTRUM (first exact piece of the H2 dictionary; the v20 lepton coefficients are resolvent determinants of the exact W(A₃) monodromy): SIGN-TWIST LEMMA [I] — −M̃₀ has order 6 ((−M̃₀)³ = −1) and spec(M̃₀) ∪ spec(−M̃₀) = μ₆: the 6-site hypercharge hexagon spectrum IS the family monodromy spectrum plus its sheet twist (ℤ₆ = ℤ₂×ℤ₃ = (−1)×⟨M̃₀⟩); the v20 denominators 5/4 − cos(rπ/3) = |1 − ζ₆ʳ/2|² are the eigen-denominators of the two family resolvents (1 ∓ M̃₀/2)⁻¹; CYCLOTOMIC DETERMINANT [I]: det(1 − tM̃₀) = 1 − t³ = (1−t)Φ₃(t) ⇒ det(1 ∓ M̃₀/2) = (7/8, 9/8); LEPTON COEFFICIENTS = RESOLVENT DETERMINANTS [I]: c_e = |μ₄|/(2det₋) = 16/7, c_μ = N_fam/(2det₊) = 4/3, c_τ = |μ₄|det₋/N_fam = 7/6, product rule = |μ₄|/det₊ = 32/9 — the lepton 7 and 9 ARE the family-resolvent determinants (×8), and δ = ½ = |(M̃₀)₂₂| is supplied by the matrix itself; the e/μ/τ leg assignment stays v20's established input (nothing re-fished); SHEET-EXTENDED GROUP [I]: ⟨U, M̃₀, −1⟩ has order 48 = Ω_adm = N_fam·dim S⁺ (the seed quartic coefficient); residue [P]: the dictionary's VALUES are exact, its ADDRESS TABLE (site per fermion, quark composition) remains open" },
      { file: "v119_review_validation_2.py", what: "SECOND EXTERNAL-REVIEW VALIDATION (triad + 121 audit + micro-identities, all exact): ANCHOR RATIO TRIAD [I] — the three elementary symmetric values of the anchor normalised by the family count, (e₃,e₁,e₂)/p₀ = (2/3, 4/3, 5/3) = (Koide branch/sheet ratio, seed gain |μ₄|/N_fam, carrier branch); the canonical flow's critical points are EXACTLY (2,5) = (e₃,e₂) with inflection 7/2 = (e₃+e₂)/2 — the recurring fractions are the three normalised anchor coefficients, not scattered numbers; THE 121 AUDIT LEMMA [I, audit-typed]: (1+a)ᵀR(1+a) = 121 = 11² = ‖Pl(K)‖₁² = (p₃+1)² — the quark-ratio 11 appears a second independent time as the quadratic anchor norm of the residue operator R; sensitivity: orderings give {105,121,135}, only the canonical anchor ordering yields 121; bonus: 1ᵀR1 = 22 = 2·11, aᵀRa = 40 = p₁p₃ = 10b₁−1 (oriented Plücker stays the derivation); MICRO-IDENTITIES: Ω_adm = 2p₁p₂ = 48, 10b₁ = 1+p₁p₃ = 41, Δ_Y = e₂² = p₀²+2·rank = 25, h(E8) = e₃p₀e₂ = 30, rank = p₀+e₂; flavor surface M(s,t) claim = established v94/v95 (presentational); μ₄ projection/triptych/interior-free already closed (v115/v116, v104/v105, v113)" },
      { file: "v120_address_table.py", what: "THE ADDRESS TABLE (the open H2 item structured; exact arithmetic on FROZEN v18/v20 integers — the red-team firewall): THE LEPTON WORDS ARE THE COMPILER ATOMS [I] — (L_e, L_μ, L_τ) = (8, 5, 3) = (rank E8, g_car, N_fam) = (p₀+e₂, e₂, p₀), in mass order (longest word = lightest lepton); ADDRESSES = EUCLIDEAN DIVISION BY THE HEXAGON [I]: (r,w) = L divmod p₂ with p₂ = 6 = |R⁺(A₃)| itself an atom: e → (2,1), μ → (5,0), τ → (3,0); Σr = 10 = p₃ = A_Λ, ΣL = 16 = dim S⁺; SHEET PARITY [I] (the v118 dictionary applied): e on the untwisted sheet (ω ∈ spec M̃₀), μ/τ on the twisted sheet (−ω, −1) — the anchor lepton τ occupies the unique REAL twisted eigenvalue −1, exactly the site where v20's product rule replaces the resolvent; QUARK SUM RULES [I] (frozen v18 words 7,7,5,3,2,0): up-sum = 10 = p₃, down-sum = 14 = p₁+p₃, ALL QUARKS = 24 = |W(A₃)| (the monodromy group order, v117), ALL NINE CHARGED FERMIONS = 40 = p₁p₃ = aᵀRa (v119); top at the vacuum site (0,0) — zero word, the ladder anchor; residue [P]: five closures (16, 10, 14, 24, 40) constrain the map, the per-fermion assignment derivation remains the open H2 content" },
      { file: "v121_address_pinning.py", what: "THE ADDRESS TABLE IS PINNED (the per-fermion assignment closes at the information level; exact census theorem): THE WORD TABLE IS THE RESIDUE OPERATOR [I] — the established identity L = R + 2U (v95) says the word-length table IS L[sector][generation] with rows (up; down; lepton) = ((7,3,0); (7,5,2); (8,5,3)) = the v18/v20 words verbatim; addresses = R's entries + one hexagon turn for generation 1, and R's first column is THE ANCHOR a = (1,1,2); THE MARGINS ARE ATOMS [I]: row sums (4,8,10) = (e₁, rank E8, p₃), column sums (4,13,5) = (e₁, Δ_Q, g_car); PINNING THEOREM [I, exact census]: among ALL 3×3 matrices with entries in the hexagon {0..5}, exactly 17 have the atom margins and exactly ONE has det = 8 = rank E8 — and it is R (also unique with SNF (1,1,8); all 17 determinants distinct — control computed explicitly) ⇒ THE ASSIGNMENT TABLE CARRIES ZERO RESIDUAL INFORMATION beyond atom margins + rank determinant; within-sector ordering = established transport reading; residue [P]: H2 shrinks from 'derive 9 integers' to 'derive the six atom margins + det = rank'; firewall: R, L, words frozen in v4/v18/v20/v71" },
      { file: "v122_margin_theorem.py", what: "THE MARGINS ARE THEOREMS (the established frozen selectors pin R uniquely — the v121 atom margins lose their input status): three selectors, all frozen BEFORE the address question was posed — (S1) the D₄ annihilator n = (5,−9,6) with nᵀR = (8,0,0) (v94: kills the (c₂,c₃) plane, n·a = 8), (S2) det R = 8 = rank E8 (v71 quartet (3,4,8,20)), (S3) det K = 4 = |μ₄| with K = R + QΣ (the diamond), plus the definitional hexagon range {0..5}; CENSUS [I]: 4×4×4 = 64 (S1)-candidates, (S2) leaves 12, (S3) leaves EXACTLY ONE — and it is R; COROLLARY [I]: the atom margins (4,8,10)/(4,13,5), the anchor column Re₁ = a, and ALL v120/v121 sum rules (16,10,14,24,40) are CONSEQUENCES — input status revoked; BONUS LEMMA [I]: on the (S1)+(S2) locus det(M+2U) = 20 = det L for ALL 12 candidates — the fourth quartet determinant is redundant (the compiler's overdetermination pattern); residue [P]: H2 reduces to the establishment of the selectors themselves (pre-existing inventoried objects) — the address question introduces NO new residual class" },
      { file: "v123_inventory_update.py", what: "RESIDUAL INVENTORY UPDATED (post v110–v122; the v105 gap list re-pinned with sharper contents, same cardinality): thirteen new ledger rows machine-checked (CAR.PAIR.02, CAR.QTRANS.01, CAR.COUNT.01, CAR.QFREE.01, GATE.UWALL.06–09, FLAV.H2.02–05, ARCH.TRIAD.01); R2 CARRIES THREE LOADS — the single index-4 boundary-net statement closes, when proven, the metric gate (GATE.METRIC.06), the carrier choice (CAR.QFREE.01 upgrade contract) and the QBL programme (ARCH.QUAD.01): one theorem, three doors; UPDATED RESIDUAL TABLE, exactly FIVE structural classes: R1 seam quantum clock (bend log₃∕₂3 at ~1/3π) [P], R2 index-4 seam net (3 loads) [P]/[A], R3 seam determinant ⇒ EH [A], R4' SELECTOR ESTABLISHMENT (n = (5,−9,6) + diamond determinants; replaces the DISCHARGED 'H2 dictionary') [A]/[P], R5 parabolic realisation of Q (GATE.QGEO; P1) [P] — plus v_geo and π; a sixth structural class would FAIL the script; THE FLAVOR SIDE HAS NO OPEN ANALYSIS CLASS OF ITS OWN anymore — H2 values exact, addresses pinned, margins theorems, residue = five frozen selector integers" },
    ],
  },
];

const TOTAL = CLUSTERS.reduce((n, c) => n + c.scripts.length, 0);

export function ScriptIndex() {
  const { open } = useReproducer();
  return (
    <div>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <p className="max-w-3xl text-sm leading-relaxed text-slate-400">
          The suite is organised by what it proves. Each script is one claim
          cluster, cited inline in the documents via{" "}
          <span className="font-mono text-slate-300">\veri&#123;vN&#125;</span>{" "}
          and registered in <span className="font-mono text-slate-300">run_all.py</span>,
          which ends <span className="font-mono text-emerald-300">ALL CHECKS PASSED</span>.{" "}
          <span className="text-slate-300">Click any script to run it live in your browser.</span>
        </p>
        <span className="rounded-full bg-slate-800/60 px-3 py-1 text-[11px] font-mono uppercase tracking-widest text-slate-300 ring-1 ring-slate-700/40">
          {TOTAL} scripts
        </span>
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        {CLUSTERS.map((c, i) => (
          <motion.section
            key={c.title}
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.5, delay: (i % 2) * 0.05 }}
            className="glass relative overflow-hidden rounded-2xl ring-1 ring-slate-700/40"
          >
            <div
              aria-hidden
              className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${c.accent} opacity-70`}
            />
            <div className="p-5 sm:p-6">
              <div className="flex items-center justify-between gap-3">
                <h3 className="font-serif text-base font-semibold text-slate-50">
                  {c.title}
                </h3>
                <span className="rounded-full bg-slate-800/60 px-2 py-0.5 text-[10px] font-mono text-slate-400">
                  {c.scripts.length}
                </span>
              </div>
              <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
                {c.purpose}
              </p>
              <ul className="mt-4 space-y-1">
                {c.scripts.map((s) => (
                  <li key={s.file}>
                    <button
                      type="button"
                      onClick={() => open(s.file)}
                      className="group flex w-full items-start gap-2 rounded-md px-2 py-1.5 text-left transition-colors hover:bg-blue-500/5"
                      title={`Run ${s.file} in your browser`}
                    >
                      <span className="mt-0.5 font-mono text-[11px] font-semibold text-blue-300 group-hover:text-blue-200">
                        {s.file.split("_")[0]}
                      </span>
                      <span className="flex-1 text-[11px] leading-snug text-slate-300">
                        {s.what}
                      </span>
                      <Play
                        size={12}
                        className="mt-0.5 flex-none text-slate-600 transition-colors group-hover:text-blue-300"
                        aria-hidden
                      />
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </motion.section>
        ))}
      </div>
    </div>
  );
}

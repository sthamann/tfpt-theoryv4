"use client";

import { useState } from "react";
import { motion } from "motion/react";
import { FileCode2, Play } from "lucide-react";
import { cn } from "@/lib/utils";
import { RichText } from "@/lib/richtext";
import { useReproducer } from "./Reproducer";
import { Expandable } from "./Expandable";

/**
 * Interactive dependency DAG of the TFPT compiler closure.
 *
 * Nodes are the load-bearing objects of the introduction's dependency graph;
 * edges are named dependencies. Clicking a node reveals what it is, its status
 * marker, its inputs/outputs, its failure mode, and the verification scripts
 * that machine-check it (deep-linked to the GitHub repository). The dashed rose
 * edges are the bootstrap / self-consistency loop: the E₈ closure feeds back to
 * fix the two axioms.
 */

type Tone = "axiom" | "lattice" | "identity" | "numerical" | "conditional";

const TONE: Record<
  Tone,
  { dot: string; ring: string; activeRing: string; chip: string }
> = {
  axiom: {
    dot: "bg-slate-400",
    ring: "ring-slate-400/40",
    activeRing: "ring-slate-300",
    chip: "bg-slate-500/15 text-slate-200 ring-slate-400/30",
  },
  lattice: {
    dot: "bg-cyan-400",
    ring: "ring-cyan-400/40",
    activeRing: "ring-cyan-300",
    chip: "bg-cyan-500/15 text-cyan-200 ring-cyan-400/30",
  },
  identity: {
    dot: "bg-emerald-400",
    ring: "ring-emerald-400/40",
    activeRing: "ring-emerald-300",
    chip: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30",
  },
  numerical: {
    dot: "bg-violet-400",
    ring: "ring-violet-400/40",
    activeRing: "ring-violet-300",
    chip: "bg-violet-500/15 text-violet-200 ring-violet-400/30",
  },
  conditional: {
    dot: "bg-amber-400",
    ring: "ring-amber-400/40",
    activeRing: "ring-amber-300",
    chip: "bg-amber-500/15 text-amber-200 ring-amber-400/30",
  },
};

interface DagNode {
  id: string;
  label: string;
  x: number; // percent
  y: number; // percent
  tone: Tone;
  marker: string;
  title: string;
  summary: string;
  inputs: string[];
  outputs: string[];
  failure: string;
  scripts: string[];
}

const NODES: DagNode[] = [
  {
    id: "P1",
    label: "c₃ = 1/(8π)",
    x: 7,
    y: 30,
    tone: "axiom",
    marker: "[O] axiom",
    title: "P1 — the seam constant",
    summary:
      "The reflection-positive boundary kernel. A declared input but NOT a free knob: it reduces to the parabolic anchor a = (1,1,2) via c₃ = 1/(2·e₁(a)·π) = 1/(8π) (e₁(a) = 4 = |ℤ₄|; v23), and the '8' is the one-sided Gauss–Bonnet of the seam normal slice (|ℤ₂|·2π·χ(S²) = 8π, χ = 2; v58/v73). On the dimensionless axis the only transcendental primitive is π.",
    inputs: ["anchor a = (1,1,2) + π"],
    outputs: ["c₃ = 1/(8π)"],
    failure: "No reflection-positive seam.",
    scripts: [
      "v58_seam_horizon_chain.py",
      "v67_area_law_coefficient.py",
      "v73_k_c3_half.py",
    ],
  },
  {
    id: "P2",
    label: "g_car = 5",
    x: 7,
    y: 70,
    tone: "axiom",
    marker: "[O] axiom · [E] Lean",
    title: "P2 — the five-slot carrier",
    summary:
      "The carrier rank g_car = 5 (3 colour + 2 weak) — a declared input, but over-determined, not a free choice. It is forced three independent ways by the E₈ closure: the bootstrap quadratic μ²−5μ+4 = 0 (v6), the Pascal condition 2^g = g²+g+2 ⇒ g = 5 (Lean-formalised, 0 sorry), and the anchor moment e₂(a) = 5. Sharper (v491): given the four marks and the weight typing (3 positive integers summing to 4), the partition {1,1,2} is unique, so g_car = e₂ = 5 and |Z₂| = e₃ = 2 are arithmetic corollaries — with negative controls on every dropped assumption; the residual is the weight-typing postulate, and P2 stays the declared axiom. That typing is itself hardened (v499): the anchor is the Birkhoff–Grothendieck splitting type of the Deligne canonical extension of the flavor connection, so given the four marks, rank 3, the cusp class and unitarity (U), integrality, positivity (h⁰ = 0 via Mehta–Seshadri stability) and the sum 4 (residue traces) are theorems — the residual shrinks to the module identification plus (U), both [C]; and that module-identification rest is now ONE residual with the QGEO modulus rest: both reduce to the same order-4 clock = Coxeter of W(A₃) = the cusp-class carrier datum (v503, QGEO.EMERGE.LIGHT.01 — the emergence-light test shows marks and square are derived while the clock is the input; markers unchanged). The clock-rigidity theorems (v506, SEAM.CLOCK.RIGIDITY.01) reduce that common residual to ONE alignment bit — 'the collar deck is the central involution of the mark-D₄' — with the clock's ORDER fermionically forced (U² = (−1)^F exactly on the NS seam, nonsplit ℤ₄; the ℤ₈ tower V² ∝ U, V⁴ ∝ (−1)^F explains 8 = 2|μ₄|); harmonicity alone is insufficient (exact counterexample), markers unchanged. The bit-origin theorems (v507, SEAM.BIT.ORIGIN.01) then refute the tautology objection: marks and deck DO share one torus origin (marks = the four half-periods, every mark-free collar deck IS a half-period translation — the deck's CLASS is derived), yet the origin does not force the alignment (in-family silver witness); the bit is an equivalence tetrad (clock ⟺ τ = i with the CM-fixed half-period ⟺ deck central in the mark-D₄ ⟺ harmonic deck pairs ⟺ nonsplit NS Fock extension) with a physical face — the Fidkowski–Kitaev-type extension class (central U² = (−1)^F vs edge U² = +1, split) — distinguished but not derived; only the POSITION (which half-period) stays the carrier input, markers unchanged. The freedom theorems (v510, SEAM.BIT.FREEDOM.01) then type that position half as TOPOLOGY: the collar deck is a COVERING deck, hence free on the seam circle — the unique free involution is the antipode (Aut(C₁₆) = D₁₆, complete census), NONSPLIT ⟺ FREE over all 17 involutions in exact Cl(16), and the edge/silver class (whose mark circle passes through the deck poles — the restriction of the BRANCHED pillowcase involution) is excluded; harmonic + free solves exactly to b = ±i, so the alignment bit reduces from 'harmonic AND central' to the square-modulus datum τ = i alone, markers unchanged. The flag-transitivity web (v512, SEAM.TAU.FLAG.01) then gives that modulus datum its sharp DISCRETE form: on the free circle bare mark-transitivity is automatic for EVERY deck-invariant configuration M(δ) = {±1, ±e^{iδ}} (the pair-exchanging V₄; no local jet sees the side bit — 'transitivity from local equality' is falsified), and what selects δ = π/2 ⟺ τ = i is exactly FLAG transitivity (marks AND their two sides indistinguishable, the V₄ → D₄ symmetry lift), welded into a 13-fold exact equivalence web (clock rotation, mark mirror, odd-doublet split (2/π)ln cot(δ/2), arc-Laplacian degeneracy, the K3 indicator in closed form, ρ-twist existence, cusp-4-cycle implementability, harmonicity, j = 1728, and the D₄ closure of the OS-reflection group — face #13, v521) — the reduction state: four marks + one discrete symmetry-lift bit (flag transitivity ⟺ τ = i) + π, markers unchanged. And the candidate closure route through free OS positivity is decided NEGATIVE (v521, SEAM.BIT.RPBLIND.01): free RP and Θ existence (the v519 battery) are side-blind along the whole M(δ) family — bond-cut spectra identical to 40 digits for every δ, the N = 16 odd-m failure a placement artifact resolved at N = 32, the continuum kernel exactly 1/sin((s+t)/2) with the axis position dropping out — the EIGHTH side-blind test on the v512 scoreboard (7 → 8); the only δ-sensitive clauses presuppose the clock, and the honest [O] gap is the mark-decorated/interacting state class: the bit remains genuine discrete input, markers unchanged. The QBL chain (v108–v113) reduces it to one boundary-net premise — closing the index-4, c = 8 net closes this axiom to [E].",
    inputs: ["anchor a = (1,1,2) (g_car = e₂)"],
    outputs: ["g_car = 5"],
    failure: "Wrong family / charge lattice.",
    scripts: ["v2_carrier_pascal.py", "v14_carrier_uniqueness.py", "v219_icosahedral_mckay.py", "v228_rr_index_gate.py", "v491_p2_partition_corollary.py", "v499_p2_weights_deligne_bg.py", "v506_seam_clock_rigidity.py", "v507_seam_bit_origin.py", "v510_seam_bit_freedom.py", "v512_seam_tau_flag.py", "v521_seam_bit_rp_blind.py"],
  },
  {
    id: "D5",
    label: "C⁺ = D₅",
    x: 27,
    y: 17,
    tone: "identity",
    marker: "[E] identity",
    title: "D₅ — the carrier half-spinor",
    summary:
      "The even-Hamming code on the five carrier slots is the D₅ = so(10) half-spinor. Its dimension is the Pascal sum 1 + 5 + 10 = 16, carrying one chiral family and the hypercharge generator Y.",
    inputs: ["P1", "P2"],
    outputs: ["dim S⁺ = 16, Y"],
    failure: "Group / matter mismatch.",
    scripts: [
      "v2_carrier_pascal.py",
      "v1_e8_glue.py",
      "v44_carrier_exterior.py",
      "v108_pascal_ladder.py",
      "v109_sheet_pairing.py",
      "v110_calderon_sheet.py",
      "v111_quadratic_transport.py",
      "v112_selfcounting_channel.py",
      "v113_quasifree_kernel.py",
    ],
  },
  {
    id: "A3",
    label: "ℙ¹∖μ₄ = A₃",
    x: 27,
    y: 83,
    tone: "identity",
    marker: "[E] identity",
    title: "A₃ — the family geometry",
    summary:
      "The four-puncture geometry ℙ¹∖μ₄ is the A₃ = su(4) atom. It fixes N_fam = 3 = rank A₃ = dim H₁(ℙ¹∖μ₄) and the ℤ₆ structure.",
    inputs: ["P1", "P2"],
    outputs: ["N_fam = 3, ℤ₆"],
    failure: "Wrong multiplicity.",
    scripts: ["v1_e8_glue.py", "v15_bootstrap_classification.py"],
  },
  {
    id: "E8",
    label: "E₈",
    x: 48,
    y: 50,
    tone: "lattice",
    marker: "[E] lattice theorem",
    title: "E₈ — the μ₄ glue (audit hull)",
    summary:
      "D₅ and A₃ share the discriminant group ℤ₄; their glue norms add to the root norm, q(D₅) + q(A₃) = 5/4 + 3/4 = 2. So E₈ = (D₅ ⊕ A₃) + μ₄ closes as a lattice theorem — the unimodular audit hull, not a gauge group; 240 = 16·5·3 roots, 248 = 240 + 8. It is the forced choice, not a guess: no nontrivial abelian sector ⇔ holomorphy ⇔ det K = 1 selects (E₈)₁ uniquely (v234/v235/v237), and the whole (2,3,5) skeleton drops out of the Brieskorn capstone (v236). The golden ratio φ is not a fitted number but the icosahedral (2,3,5) signature — an output of the bootstrap-forced geometry, not an input (v349/v354) — and a reverse numerology audit of the unmapped E₈ region finds no missed primary readout under a strict discriminator (v355). The sheet/deck complement (v430) closes the adversarial follow-up: the seam's “other side” (the double-cover deck |ℤ₂| = 2 and the conjugate half-spinor S⁻ = part of the 128-spinor, ∑deg) is matched structure, forced-disjoint from the five unmapped Casimir degrees {12,14,18,20,24}. Those five are not diffuse overhead either: they are the forced two-family decomposition deg(E₈) = 6·spine{2,3,4,5} ⊔ ({2}∪det-ladder{8,14,20}), the residue classes {0,2} mod 6 forced by h = 30 = 2·3·5 (v431) — exact arithmetic, with the functorial flavour identification honestly kept [P].",
    inputs: ["D₅", "A₃"],
    outputs: ["240 roots, 248 = dim E₈"],
    failure: "Not even-unimodular; glue norms do not sum to 2.",
    scripts: [
      "v1_e8_glue.py",
      "v6_bootstrap.py",
      "v15_bootstrap_classification.py",
      "v47_selection_theorem.py",
      "v170_diamond_slice_compression.py",
      "v223_coxeter_totative_clock.py",
      "v227_degree_exponent_channel_split.py",
      "v232_e8_kleinian_seam.py",
      "v234_seam_holomorphy_selection.py",
      "v235_seam_chern_simons.py",
      "v236_brieskorn_capstone.py",
      "v237_seam_sre_closure.py",
      "v349_raw_seam_golden_test.py",
      "v354_e8_reverse_audit.py",
      "v355_e8_unmapped_bandwidth.py",
      "v430_other_side_reverse_audit.py",
      "v431_e8_degree_ladder.py",
    ],
  },
  {
    id: "RL",
    label: "R, L",
    x: 68,
    y: 50,
    tone: "identity",
    marker: "[E] identity",
    title: "R, L — the flavor residue matrix",
    summary:
      "The residue + winding matrix on the anchor a = (1,1,2). det R = 8 = h(D₅); the principal 2-minors (2,3,5) have product h(E₈) = 30. Its operator core T = 3 B(Q)⁻¹B(K) = [[5,11/3],[0,2]] has Spec {2,5}, trace 7 (scalaron) and det 10 = A_Λ — the basis-invariant heart of every readout. The Koide attractor is the unique branch-preserving Möbius map fixing q = 2,5, with multiplier (2/3)⁶ = the transfer gap λ₂ (v54/56). The old sheet / Q-grading question is now derived (G = T_A·Σ acts integrally), so it carries no separate open status.",
    inputs: ["E₈ / A₃"],
    outputs: ["det 8, minors (2,3,5), Σ L = 40"],
    failure: "Wrong D₆ branch.",
    scripts: [
      "v4_flavor_matrix.py",
      "v10_projection_involution.py",
      "v37_plucker_anchor.py",
      "v52_pencil_endpoints.py",
      "v79_review_identities.py",
      "v80_operator_pencil_geometry.py",
      "v81_singular_pencil_matrices.py",
      "v82_koide_attractor_splitting.py",
      "v85_master_cover.py",
      "v96_branch_kernel_selection.py",
      "v97_sheet_conjugation_bridge.py",
      "v98_discriminant_dictionary.py",
      "v99_koide_flow_time.py",
    ],
  },
  {
    id: "alpha",
    label: "α⁻¹",
    x: 90,
    y: 15,
    tone: "numerical",
    marker: "[E] numerical fixed point",
    title: "α⁻¹ — the electromagnetic fixed point",
    summary:
      "The fine-structure constant is the unique positive root of the boundary U(1) Ward identity F_U(1)(α) = 0, built from c₃ and the abelian coefficient 41 = 10 b₁. Existence and uniqueness are proved; α⁻¹ = 137.0359992168, 1.9σ from CODATA-2022. F_U(1) = 0 is the stationarity of a U(1) determinant line, every coefficient a named index/heat-kernel/discriminant atom (v341/v342); the one residual — the from-first-principles proof that this IS the exact Quillen functional — is the tracked target ALPHA.QUILLEN.EXACT.01 (v382), a face of SEAM.EQUIV.01, never the value (which stays [E]). Four honest steps narrow it: a solvable 4D model reaches the a₄ order (v433), the matter factor b₁ is the U(1)_Y a₄ heat-kernel coefficient via β = a₄ so the three residuals collapse to one [C] (seam F-normalisation) + one [O] (v434), and a π-power test isolates the cubic α³ as the unique metric-independent (π⁰) topological rung whose coefficient is a conditional integer Chern-Simons level (v435). A fifth step (v470) upgrades both leftovers: the α³ level equals the computed bulk Chern invariant |C| = 1 of the same collar model that realises S3 (TKNN/Avron–Seiler–Simon quantisation + Callan–Harvey inflow + the APS/Witten η=CS reading of δ log det), replacing v435's minimality assumption; and the seam F-normalisation is the affine embedding index k_Y = tr(Y²)/tr(T₃²) = 5/3 (Ginsparg 1987; (3/5)·(41/6) = 41/10 = b₁ exactly) — zero independent content, a face of SEAM.EQUIV.01. One invertible phase, two quantised responses (c₋ = 8 gravitational, C = 1 U(1)). A sixth step (v472) exhibits the bridge lemma at the finite level: the determinant line of the occupied frame over the U(1)-twist moduli of the same collar (the moduli space of flat U(1) connections — the Quillen-shaped object) carries FHS curvature = 1 = the inflow level, exactly and size-independently, with clean controls (trivial 0, orientation −1), the twist-moduli integer equal to the Bloch-BZ integer (Niu–Thouless–Wu) and the Dai–Freed section globally defined. What stays [O] is the continuum ζ-det identification on the abstract seam (= the SEAM.EQUIV.01 face). A seventh step (v484) merges this target with the φ₀-puncture target: the shared 'c₃ per boundary insertion' rule IS the KMS seam unit 2π = 1/(4c₃) with 1/4 = 1/|μ₄| (one bare boundary propagator orbit-averaged over the four marks), derived on the seam circle for the finite cycle sector — the two [O] targets are now ONE remaining analytic step (diagonal ζ-renormalisation + multiplicity matching). An eighth step (v485) settles that step at the computable level: the renormalised diagonal vanishes exactly at the KMS seam circumference (G_reg(0;ℓ) = (1/π)ln(ℓ/2π), zero iff ℓ = 1/(4c₃)), the mark determinant resums closed-form (det(I−uC) = (1−4u)(1+2u)², BFK route v151), and the 48/41 multiplicities are one state set under two response weights — the residual is the abstract-seam ζ-det identification, a face of SEAM.EQUIV.01 alone. ALPHA.QUILLEN.EXACT.01 stays [O]; α⁻¹ stays [E].",
    inputs: ["c₃ (P1)", "M = 41 = 10 b₁ (from R, L)"],
    outputs: ["α⁻¹ = 137.0359992168"],
    failure: "No root, or a second admissible root.",
    scripts: [
      "v3_em_alpha.py",
      "v48_em_ward.py",
      "v159_pyrate_gauge_crosscheck.py",
      "v341_alpha_quillen.py",
      "v342_em_ward_heatkernel.py",
      "v382_alpha_quillen_exact.py",
      "v391_alpha_quillen_progress.py",
      "v433_alpha_quillen_heatkernel.py",
      "v434_alpha_quillen_betafunction.py",
      "v435_alpha_quillen_chernlevel.py",
      "v470_alpha_inflow_level.py",
      "v472_quillen_detline_moduli.py",
      "v484_seam_contact_unit.py",
      "v485_contact_diagonal_closed.py",
    ],
  },
  {
    id: "masses",
    label: "masses, CKM/PMNS",
    x: 90,
    y: 40,
    tone: "identity",
    marker: "[E] / [C]",
    title: "Masses & mixings — the φ₀-ladder",
    summary:
      "All nine masses, CKM and the PMNS skeleton from one master formula m = (v/√2) λ_Y^L Λ with the seed φ₀. The charged-lepton coefficients (16/7, 4/3, 7/6) are exact and the quark mass ratios (55/117, …) are integer Plücker readouts. The ratios are closed; only one overall amplitude v_geo remains — the same dimensionful anchor as gravity's 1/G, confirmed as the single dimensionful input of the whole theory (v364). The downstream F_transfer readouts are now typed, runnable solvers each with a kill test — Koide source→pole (v371), η_B via the BDP Boltzmann network (v372), the finite-T axion relic (v373), m_p/m_e (v374) — folded into a status-typed prediction-observatory CI (v375); they stay [C] bridges, never compiler outputs. The absolute neutrino scale has a named one-parameter CANDIDATE (v481, FLAV.NUSCALE.02): under the carrier normalisation y_ν = y_t the (y_ν, M_R) trade-off collapses to M_R alone, with the required M_R = 9.3×10¹³ GeV inside the PS window at log_c₃ rung 3.15 and the integer c₃³-rung explicitly declined at 1-loop — and meanwhile EXCLUDED unstructured by the bracketed decision computation (v482: the rung needs ×1.67 in m₃, generous >3σ input envelopes reach at most ×1.165 combined; the 5/3-proximate Majorana structure escape is recorded post-hoc and declined) — nothing closes, the frozen record is untouched. The φ₀ seed's puncture term is geometry-exact (v483): all twisted pillowcase heat traces are t-independent rationals, so the π⁻⁴ in 48c₃⁴ must sit in the per-mark coupling weight — the puncture target narrows to that one rule.",
    inputs: ["R, L", "φ₀ (from c₃)"],
    outputs: ["9 masses, mixings"],
    failure: "Hierarchy mismatch.",
    scripts: [
      "v18_quark_yukawa.py",
      "v20_lepton_c_derivation.py",
      "v229_lepton_frobenius_algebra.py",
      "v24_quark_ratio_closure.py",
      "v46_grand_mass_volume.py",
      "v224_diamond_ftransfer_path.py",
      "v230_center_budget_norms.py",
      "v410_sheet_generator_binary.py",
      "v411_ud_ratio_vpower.py",
      "v412_sheet_source_corner_J.py",
      "v413_sheet_characteristic_calculus.py",
      "v414_center_resolvent_portal.py",
      "v49_readout_rigidity.py",
      "v75_upoint_to_vgeo.py",
      "v88_cp_phase_audit.py",
      "v202_rare_kaon.py",
      "v114_torsion_delta.py",
      "v115_anchor_residue.py",
      "v116_resonance_uniqueness.py",
      "v117_monodromy_weyl_a3.py",
      "v118_hexagon_family_dictionary.py",
      "v119_review_validation_2.py",
      "v120_address_table.py",
      "v121_address_pinning.py",
      "v122_margin_theorem.py",
      "v123_inventory_update.py",
      "v124_resummed_clock.py",
      "v125_glue_qsystem.py",
      "v126_clock_wall_bridge.py",
      "v127_ring_resummation.py",
      "v128_graded_hull.py",
      "v129_entropy_power_law.py",
      "v130_born_square.py",
      "v131_measure_is_area.py",
      "v132_detratio_anomaly.py",
      "v133_zeta_budget.py",
      "v134_dual_anchor.py",
      "v135_det_surface.py",
      "v136_dual_normal_selector.py",
      "v137_qplus_cohomology.py",
      "v138_vw_firewall.py",
      "v139_selector_triangle.py",
      "v140_canonical_map.py",
      "v141_deck_selection.py",
      "v142_frame_integrality.py",
      "v143_graded_frobenius.py",
      "v144_detratio_family.py",
      "v145_pairing_atoms.py",
      "v146_moebius_d4.py",
      "v147_clock_gaussian.py",
      "v148_fock_census.py",
      "v149_cusp_normal.py",
      "v150_replica_eh_model.py",
      "v151_bfk_split.py",
      "v152_norm_is_anchor.py",
      "v153_no_unit_theorem.py",
      "v154_simple_current_theorem.py",
      "v155_quasifree_boundary.py",
      "v156_seam_net_construction.py",
      "v157_rigid_fixed_point.py",
      "v158_fixed_point_stable.py",
      "v159_pyrate_gauge_crosscheck.py",
      "v160_seam_gaussianity_from_pf.py",
      "v161_one_particle_reduction.py",
      "v162_seam_transport_identification.py",
      "v163_rg_stability_flavor.py",
      "v164_qcd_scale.py",
      "v165_premise_a_closure.py",
      "v166_higgs_free_seam.py",
      "v168_qgeo_rigidity.py",
      "v172_trace_anomaly_seed.py",
      "v173_pfaffian_cp_car.py",
      "v174_seam_fock_readings.py",
      "v175_net_existence_full_cone.py",
      "v176_seam_collar_realisation.py",
      "v177_seam_marking_kernel.py",
      "v178_marks_kernel_attempt.py",
      "v179_conformal_realisation.py",
      "v180_clock_is_mobius.py",
      "v181_clock_is_conformal_symmetry.py",
      "v182_reviewer_residual_map.py",
      "v183_koide_f_corner_transfer.py",
      "v184_etaB_anchored_boltzmann.py",
      "v185_axion_relic_solver.py",
      "v211_axion_spine_angle.py",
      "v212_leptogenesis_decuple.py",
      "v187_ftransfer_laws.py",
      "v213_ftransfer_functor.py",
      "v303_ftransfer_dynamics.py",
      "v188_frontier_wording_guard.py",
      "v189_riemann_roch_carrier.py",
      "v190_nariai_entropy_bound.py",
      "v191_universal_branch_line.py",
      "v192_qgeo_energy_clock.py",
      "v193_qgeo_energy_commutator.py",
      "v194_raw_seam_dtn_rp.py",
      "v195_marks_lefschetz_character.py",
      "v196_seam_energy_functional.py",
      "v197_rr_carrier_clifford_d5.py",
      "v198_modular_commutator_reduction.py",
      "v199_seam_state_invariance.py",
      "v200_seam_variational_scan.py",
      "v201_seam_subprincipal_marks.py",
      "v210_mark_local_dtn.py",
      "v214_seam_pillowcase.py",
      "v215_seam_deck_killtest.py",
      "v216_marks_gauss_bonnet.py",
      "v217_marks_emergence_scan.py",
      "v503_qgeo_emergence_light.py",
      "v507_seam_bit_origin.py",
      "v510_seam_bit_freedom.py",
      "v512_seam_tau_flag.py",
      "v364_vgeo_sharpen.py",
      "v371_ftransfer_pole.py",
      "v372_ftransfer_boltzmann.py",
      "v373_ftransfer_relic.py",
      "v374_ftransfer_qcd.py",
      "v375_observatory_registry.py",
      "v397_external_clock_probe.py",
      "v481_seesaw_carrier_ladder.py",
      "v482_seesaw_rung_decision.py",
      "v483_pillowcase_exact_traces.py",
    ],
  },
  {
    id: "theta12",
    label: "sin²θ₁₂",
    x: 90,
    y: 64,
    tone: "numerical",
    marker: "[E] / [C]",
    title: "Solar angle — the seam misalignment",
    summary:
      "Tri-bimaximal 1/3 plus the seam misalignment ε = q(A₃)φ₀ = (3/4)φ₀ gives sin²θ₁₂ = 1/3 − φ₀/2 = 0.306747 — 0.1% from NuFIT 6.0, the live JUNO test. It is the frozen prediction of record in the machine-enforced blind registry (v84): exactly one θ₁₂ number is committed in advance, seam / non-linear variants typed as the same texture, never alternatives.",
    inputs: ["R, L", "φ₀"],
    outputs: ["sin²θ₁₂ = 0.306747 (frozen)"],
    failure: "Seam-misalignment lemma fails.",
    scripts: [
      "v9_neutrino_texture.py",
      "v16_solar_dual_anchor.py",
      "v21_solar_product_quark.py",
      "v84_frozen_registry.py",
      "v163_rg_stability_flavor.py",
      "v220_cp_hexagonal_modulus.py",
      "v225_dual_normal_frame.py",
      "v231_cp_mu6_phases.py",
      "v233_cp_triality_phase.py",
    ],
  },
  {
    id: "cosmo",
    label: "Λ, A_s, n_s, r",
    x: 90,
    y: 88,
    tone: "conditional",
    marker: "[E]/[C] mixed",
    title: "Gravity & cosmology — the geometry channel",
    summary:
      "The spectral action gives R + R²; the scalaron mass is M = c₃^(7/2) M̄ = 3.06×10¹³ GeV (exponent 7 = Ω_adm − 10 b₁). NEW (v358/v359): beyond the R + R² action, the classical field equation is parameter-free — the fixed-volume entanglement equilibrium (Jacobson; Faulkner et al.) gives the FULL covariant Einstein equation G_ab + Λ g_ab = c₃⁻¹ T_ab with BOTH coefficients fixed: c₃⁻¹ = 8π (no free Newton dial; thermo 2π/η = geo |Z₂|·2π·χ via |μ₄| = |Z₂|·χ = 4 — so c₃ is triply over-determined, anchor v23/geometry v58/thermo v358) and Λ from α (ρ_Λ = (3/4π²)e^{−2α⁻¹}, v60). The Einstein tensor (not Ricci) is forced by Lovelock at fixed volume, so matter conservation ∇ᵃT_ab = 0 is an output (v359) — B6's full covariant field equation, parameter-free at the local level. The seam's gap-induced higher-curvature correction to GR is disciplined and bounded, and the matter–gravity backreaction with the explicit J3 flux is a forced result with an honest decline on the rest (Directions 2/5, v360/v361). An external candidate for the missing action level — Bianconi's entropic action (PRD 111, 066001 (2025)) — is quantified in v473 (β′_B = c₃/6 pinned exactly), its operator level executed in v474, and the R² kill test executed in v475: the raw entropic scalaron is trans-Planckian (m² = 4608π²/17 M̄², ≈ 51.7 M̄), so the light-trace-mode reading is dead — v477 then resolves the gap as ONE scale-measure moment (satisfied by TFPT's own KMS moment, zero new dials), the compression conjecture is made well-posed (v476) with continuum evidence that the state-side modular data flows to the CHM/BW form (v478); nothing closes, the equation-of-state typing stays [O]. From the same attractor n_s = 1 − 2/N★, r = 12/N★² on the frozen band N★ ∈ [50,60]; the reheating chain (v86) sharpens this conditionally to N★ = 51.4 ⇒ n_s = 0.9611, r = 0.0045 (recorded with its A_s tension). The branch's next derivative and next observable are machine-backed too (v494): the running α_s = −2/N★² = −r/6 (exact slow roll −7.09×10⁻⁴ at 51.4; +0.57σ Planck 2018, −1.33σ P-ACT-LB record leg; any robust positive running kills the plateau branch), and the μ-distortion band 1.5–2.3×10⁻⁸ as the future A_s/N★ branch discriminator (Δμ = 3×10⁻⁹ = 3σ at Voyage-2050 σ_μ = 10⁻⁹; the frozen log-comb is structurally blind in the μ window). Λ ∼ e⁻²ᵅ⁻¹, H₀ ∼ √Λ. The metric sector reduces to the rigorously-constructed (E₈)₁ lattice net (c = 8 = 5 + 3), now closed modulo cited theorems via the Seam Equivalence Theorem's MMST route SEAM.EQUIV.MMST.01 ('the raw seam IS (E₈)₁ at τ=i', det K = 1, the Kitaev E₈ phase; parent SEAM.EQUIV.01 [O], twistor route SEAM.EQUIV.TWISTOR.01 [O]) — pinned at every computable level by an explicit lattice model (v367/v368) and the S3 closure stack (v376–v379, ground-state witnesses v489/v490), residual [O] = the cited MMST continuum existence only (extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O]); see the boundary-QFT node (v276/v282/v286/v288). Classical fingerprint (v101): the maximal de Sitter (Nariai) black hole carries the traceless anchor (1,1,−2) and the Koide-2/3 entropy bound, and evaporates away from the anchor — the same orientation as flavor relaxation. Every scale is a ratio to one v_geo.",
    inputs: ["c₃ (P1)", "E₈"],
    outputs: ["Λ, A_s, n_s, r, scalaron M"],
    failure: "Ambient reflection-positivity fails.",
    scripts: [
      "v7_gravity_cosmo.py",
      "v28_gravity_fR.py",
      "v343_four_routes_analysis.py",
      "v358_grav_entropy_equilibrium.py",
      "v359_grav_nonlinear_einstein.py",
      "v360_grav_gap_corrections.py",
      "v361_grav_backreaction.py",
      "v473_entropic_action_bridge.py",
      "v474_entropic_hodge_carrier.py",
      "v475_entropic_scalaron_gate.py",
      "v476_entropic_compression_toy.py",
      "v477_entropic_scaleflow.py",
      "v478_entropic_continuum_legs.py",
      "v36_spectral_action_g2.py",
      "v60_lambda_metrology_branch.py",
      "v76_gmetric_reduction.py",
      "v77_e8_conformal_net.py",
      "v78_vgeo_floor.py",
      "v83_e8net_holomorphic_uniqueness.py",
      "v86_nstar_reheating.py",
      "v494_cosmo_running_mu_record.py",
      "v87_bulk_uniqueness_reduction.py",
      "v101_horizon_anchor.py",
      "v102_seam_orientation.py",
      "v103_trisection_normal_form.py",
      "v104_nariai_clock.py",
      "v203_eht_achromatic.py",
      "v105_residual_inventory.py",
      "v107_quantum_clock_target.py",
      "v169_etaB_boltzmann_interface.py",
    ],
  },

  {
    id: "qft",
    label: "boundary QFT + seam bedrock",
    x: 48,
    y: 84,
    tone: "conditional",
    marker: "[E]/[C] closed modulo cited theorems",
    title: "Boundary QFT & the seam bedrock",
    summary:
      "On top of E₈ the boundary QFT is one relative object — the Modular Spectral Closure (v258–v261): the finite Dirac is the covariance induction of the seam KMS state, the spectral-action cutoff IS that KMS weight (f₂/f₀ = 1), and the seam, carrier-16 and E₈ live on one Kummer/K3. The perturbative 4D S-matrix S_pert is Epstein–Glaser-constructible with the SM gauge β-coefficients (41/10, −19/6, −7), LSZ-bridged with one-loop unitarity for matter+gauge — now closed to all orders as a typed EG/BRST contract (v381: dim-4 power-counting ⇒ finite counterterms, BRST nilpotency for su(3)×su(2), the seam gap ⇒ adiabatic limit, with imported all-order Tₙ existence and Slavnov–Taylor) — and the R²/Weyl² gravity sector's Stelle ghost is a Seeley–DeWitt truncation artefact (the untruncated KMS spectral-action Hessian is entire and zero-free, so resummation decouples it), so perturbative spin-2 graviton unitarity is established [C] (v304/v370/v380). The ambient QG.AMB.01 measure is discharged as a redundancy (v369 + v379) — a certification object, not missing dynamics, gap-decoupled (Decoupling Theorem v337: every readout factors through the gapped admissible spectrum, susceptibility χ=729/665, margin 1.648>0) and conditional only on SEAM.EQUIV.01 + Bisognano–Wichmann. The whole layer closes modulo cited theorems via ONE keystone's MMST route, SEAM.EQUIV.MMST.01, of the Seam Equivalence Theorem (SEAM.EQUIV.01): 'the raw RP seam state IS the holomorphic (E₈)₁ boundary net at τ=i'. Its conformal-deck face QGEO.SYM.01 is a corollary (a conformal net's vacuum is rotation-invariant by axiom, v335). The target net is pinned at every computable level by an explicit gapped lattice model (v367/v368) and the S3 closure stack (central charge c = 8 from the lattice v376, the (E₈)₁ character 248/1 v377, genus-1 torus GSD = 1 v378, reflection positivity v379; premise (i) c₋ = 8 additionally carries a ground-state witness — the Kim–Shehab–Kim modular commutator on the exact BdG ground state gives c₋ = 8 = g_car + N_fam with trivial/orientation controls, independent of the Chern and KLM routes, v489 — and μ_pre = 4 is lattice-witnessed by the T² spin-structure parity census (per layer (+,+,+,−), all four sectors even for 16 layers ⇒ gauged torus GSD = 4 = μ(SO(16)₁); θ_v = 1 exactly at ν = 2c₋ = 16; TEE fence: γ_f = 0 for both phases, no discriminator; v490), and its two heavy legs are literature-anchored (v336): the continuum scaling limit (Osborne–Stottmeister, arXiv:2107.13834, free lattice fermions → chiral CFT) and the OS reconstruction of unitary lattice VOAs (Adamo–Moriwaki–Tanimoto), with (E₈)₁ inside their range — so the one residual is [O] = the abstract continuum scaling-limit existence only (v336), a cited published theorem (closed modulo a cited theorem, not solved). Its 128-spinor extension leg is certified at net level by the peer-reviewed crossed-product package (v469: locality integer h_s = 16/16 = 1 ∈ ℤ, Longo–Rehren 1995 / Böckenhauer 1996 / Böckenhauer–Evans 1998 / KLM μ = 4/2² = 1 ⇒ holomorphic), with the AGT/AMT lattice-VOA route demoted to an independent second witness, and the realisation input reduced from model fiat to invariant level R1′ (quasi-free + gap + class D + c₋ = 8 from P1; computed FHS Chern |C| = 1, ν = 16, the Kitaev 16-fold-way class; Lean parallel route seamResidualClosed'). SEAM.EQUIV.01 stays [O]. Two further reductions sharpen the residual without moving it: the R3 'attractor graph IS the du Val singularity' bridge is discharged to Kronheimer's 1989 ALE hyper-Kähler quotient theorems with every finite input a compiler output (v479: Kac marks = null/Perron vector, quotient dim 4, |2I| = 120, unimodular −E₈ resolution — the premise transforms to 'the raw seam supplies the ALE/orbifold datum'); and the four μ₄ marks are the exactly solvable four-interval multilocal free-fermion geometry (v480: binary clock ρ⁴ = −1, exact 8th-root sector decoupling, ω∘ρ = ω manifest at the state level, Casini–Huerta mixing shadow — the bedrock mechanism in the cited multi-interval class, raw-seam premise unchanged). Lean-pinned (FORM.SEAM.MMST.01, SeamScalingLimit.lean) to those named steps plus the derived Recovery gap Δ = 6·ln(3/2) ≈ 2.43 > 0. A fourth research contract (CELEST.SEAM.01, v492+v493+v495+v496+v497+v498+v500+v501) opens the celestial-holographic route: the E₈ μ₄-glue is verified as the flat ℤ₄ monodromy of the glue-equivariant celestial chiral algebra on the A₃ ALE space ℂ²/ℤ₄ (zero modes = the carrier, the 4-sector (E₈)₁ character with discriminant-form weights), with the exact correction clock² = deck (ℤ₈ spin bridge, 8 = 2|μ₄|), and its WP2 deformation theory is executed too (v493): the clock-invariant family XY = Z⁴ + a₀ is a pure seam scale with the τ = i pillowcase frozen, the clock IS the Picard–Lefschetz/Coxeter monodromy, and the BHS deformed algebra transfers ℤ₂ → ℤ₄ with no sector leak — structural arithmetic only (verdict B each). Its WP3 alignment test is executed (v495): the Green–Schwarz coefficient of celestial E₈ is exactly λ̃ = 6 with (κ/c₃)² = 12 = |μ₄|·N_fam, but the same alignment format passes for all 8 algebras on Costello's list (8/8) — alignment survives, selectivity does not (compatibility, not E₈-selective evidence). And its WP4 type-mismatch test is executed (v496, verdict B(ii)): the (E₈)₁ character is provably NOT a conformal block of the celestial S-algebra in its jet grading (null ideal 27000 = h∨³ localised), surviving only as a boundary/limit shadow at the current stratum — exactly the SEAM.EQUIV.01 scaling-limit shape. Its first WP5 milestone WP5a is executed too (v497): the boundary limit is made a precise coefficientwise limit (χ_w family, stabilisation threshold w = n+1, w = 2 = the chiral jet grading) and the null ideal is DERIVED from root data (Sym²(248) = 27000+3875+1, 27000 = h∨³; quotient 31124−27000 = 4124 = the independent μ₄ theta-split sector sum; SO(16)₁ negative control: four blocks, 5304 ≠ 14³, h = 1/2 breaks fusion) — the celestial route now has the same two-step shape as MMST (limit + maximal ideal). And its second WP5 milestone WP5b is executed as well (v498, success on the preregistered criterion): the deleting object is explicit — |s⟩ = (E^θ_{−1})²|0⟩ in a machine-built Chevalley/Frenkel–Kac basis, J^a_1|s⟩ = 0 on all 248 generators (case tally 190/57/1, exactly one case sees the level k), level dial 2(1−k) (only k = 1 deletes; no deletion object in the centerless loop algebra), μ₄-compatible (j(θ) = 1, clock phase −1, class(2θ) = 2 sheet-even, 8 quarters = q²), U(g)|s⟩ = THE 27000 with the lowering-orbit BFS matching Freudenthal through depth 4 — with the one-block closure typed E₈/μ₄-specific against the SO(16)₁ contrast (h = 1/2 breaks fusion) and the twisted-slot moding tension flagged as the precise WP5c question. Its third WP5 milestone WP5c is executed (v500, success on the preregistered criterion): the GNS limit state exists — the quasi-free family ω_w (affine k = 1 vacuum via the machine-determined compact anti-involution, x^(wr)-contracted radial oscillators) is positive for every finite w, stabilises exactly at the WP5a threshold w = N+1, and its limit carries the null ideal in its GNS kernel (the complete 9361-block exact level-2 Gram: rank 4124 = χ₂, kernel 27000 = V(2θ) weight by weight, every block PSD, clock-class split (1036,1024,1040,1024) = the per-period theta-split at the STATE level, |s⟩ = the GNS zero vector — the WP5b tension resolved), with a CCR obstruction proving the family formulation necessary (KILL not triggered). And its fourth milestone WP5d-α is executed as well (v501): the KLM two-interval index measured entropically on the 16-layer seam edge — fermionic MI extensive (μ = 1 reference), the orbifold prescription pays exactly one classical bit (ln 2 plateau at machine precision), μ_gauged = 4 = the v490 parity census (two independent lattice witnesses), and the condensation arithmetic 16 → 4 → 1 (KLM/Longo–Rehren quotients, Σd², θ_v = 1 exactly at ν = 16) closes with μ = 1 — the preregistered kill ('μ-offset ≠ 0 after condensation') does not fire. WP5d-β completes the KLM triple on the lattice (v504): strong additivity is algebraically EXACT with the shared boundary Majorana (Even(A) ∨ Even(B) = Even(A∪B), GF2 spans full, rank 32/32; disjoint exactly index 2 = the v501 ln 2 bit), the entropic touching defect stays BOUNDED < ln 2 with the Ising ¼-exponent approach while the preregistered U(1)/Dirac control DIVERGES (Klich–Levitov pinned — bounded-vs-divergent is the discriminator, Longo–Xu), the split property is witnessed at the elliptic-nome rate πK(1−x)/K(x) (1.3–2.0%) with EXACT orbifold inheritance (C → −C + the Λ²C compound, Longo heredity), and Pimsner–Popa E(a) − a/2 = PaP/2 holds identically (λ = 1/2 = 1/[F:F_even] with integer attainment, λ_E4 = 1/4 = 1/μ, exp(Δ∞) = 2 = 1/λ_PP — two independent index routes): all three KLM ingredients of complete rationality carry lattice witnesses; the continuum uplift is honestly fenced ('finite-group orbifolds of completely rational nets are completely rational' is Xu's theorem — cited, not claimed). And the WP5e α stage is executed (v502, CELEST.WP5E.ALPHA.01): the q^(−1/3) prefactor of E₄/η⁸ is exact μ₄ vacuum-energy bookkeeping (the clock is inner ⇒ shift orbifold θ = 0⁸, every sector at −c/24 = −1/3; discriminant form = Casimir via spectral flow AND the 16-Majorana seam carrier; deck rotation fails 3/16 ≠ 3/8), and k = 1 is forced three independent ways (current condition h(J) = k = 1; conformal embedding 47(k−1)(k+266/47) = 0; central charge 240(k−1) = 0; plus the WP5b singular-vector dial 31124 − 27000 = 4124), with the honest sharpening that glue-h integrality holds for ALL k and fixes nothing; the later WP5e stages land both faces of the twistor uplift (β equivariant ledger v505, γ exchange no-go v508, ε₂ level-from-flux v509, δ₂ full-tensor ledger v511, the c_d negative certificate v513, ε₁ bulk-axion slot v514), and all three back-reaction milestones M1–M3 are executed (v515/v516/v517, each SUCCESS on its preregistered criterion): the back-reacted Ω_N is closed-form on the A₃ twistor family with all S³/ℤ₄ periods (2πi)²-integral, the lockstep flux vector and the lens-forced source charge 4 = |μ₄| (v515; honest fence: integrality alone does not discriminate, 0/24 on the forbidden family); the twisted KS measure — on the DECLARED completion reading, fence [C] — carries the exact completion-weight identity w = 4h = −4·ch₂ (no free scale), turns every twisted channel into the same perfect Okubo square 36⟨x,x⟩²/det_j, cancels the 32·T₃ residual and supplies the v511 ψ = 64 slice exactly, so the cubic d-channel is not needed (v516); and the a₀ uplift couples the log-type correction to the centre count on four scales (kernel log 4 = |μ₄|, GLT tower p_{4k} = 4(−a₀)^k, exceptional-locus log, period response 1/4 integrating to the Coxeter monodromy i; v517) — the v514 fence M1–M3 is fully worked off; and the δ₁ chain is DECIDED (v518, CELEST.WP5E.DELTA1.01): the derived chiral measure — blockwise SL(2,ℤ) covariance solved for, the μ₄ multiplier obstruction a character cancelled exactly by the twisted fibre block f₁f₃ = G — fails all three preregistered testers, a genuine kill on the derived surface in stated tension with the declared v516 reading (both exact); and the measure question is since DECIDED at probe level (v520, CELEST.WP5E.MEASURE.01, ERFOLG-A): single-valuedness of the one-loop lattice factor is DERIVED from two independent constructive sources — F-independence of the moduli integral (every chiral option carries a nontrivial character, so fundamental-domain independence forces ∫ = 0) and the Quillen pairing (|t·conj(t) − 1| < 8.3e−40 on all 15 pairs, the doubled 256-dim system closes at trivial character with the physical columns contained, hol⊗hol empty) — under the typed premises TP-1..TP-4; the exact invariant subspace span{e_H, e_H'} = E₄ then forces the v516 completion reading, the consistency circle closes levelwise, and the v518 kill is sharpened; and the w_m normalisation is since DERIVED constructively (v523, CELEST.WP5E.WM.01, ERFOLG): 1/det_j is the Atiyah–Bott/zeta-determinant fixed-point factor, computed from three independent sources (the equivariant mode ledger with Abel value (1/2, 1/4, 1/2), the zeta/reflection determinant with the unique real positive Quillen section, the δ₁f block constant term 1/det_b) with the v516 chain reproduced number by number under the typed premises TP-REG/TP-Q/TP-NUM/TP-CH. The WOIT β₁ stage is executed too (v522, WOIT.BETA1.GSO.01, typed UNDECIDED): the μ₄ clock average violates Hermiticity exactly (the clock is Woit's euclidean rotation — time-like), the gaugeable part of its tower is exactly the GSO/fermion-parity ℤ₂, gauge-fixed RP holds under that typing ((29,0,0)/(8,0,0) PD), kill test (2)'s free shadow does not fire, and the clock-equivariant statement moves to β₂ — since executed as well (v524, WOIT.BETA2.OS.01, SUCCESS, [C]-typed per contract precision (iii)): the OS quotient of the free system is explicit (H_phys PD at both levels, 37 = 29⊕8 and 16 = 4² thermal/KMS), the clock is a positive self-adjoint transfer step T^(N/4) with spectral calculus (exact N = 8 spectrum {1, √2−1}) and a reconstructed unitary rotation group, the v522 non-Hermiticity is resolved as the wrap artifact, and the pre-declared KMS deviation carries exactly the silver witnesses — β₃ is next; and the twist-state door on the alignment bit is decided side-blind (v525, SEAM.BIT.TWISTBLIND.01, KILL as preregistered: the ninth side-blind test, 8 → 9, the free-plus-twist class exhausted); the single remaining piece is WP5e proper (narrowed to the global BCOV integral beyond the fibre zero-mode factor; the continuum uplift of the WP5d lattice witnesses is Xu's theorem, cited not claimed); SEAM.EQUIV.01 unchanged. The full sprint-by-sprint reduction (v269 → v302) lives on the /changelog page.",
    inputs: ["E₈", "seam KMS / DtN state"],
    outputs: ["one relative object; S_pert (1-loop unitary, matter+gauge)"],
    failure: "the seam net is not holomorphic (det K ≠ 1) / not the flat τ=i state.",
    scripts: [
      "v258_dirac_covariance_induction.py",
      "v259_modular_cutoff_kappa.py",
      "v260_k3_kummer_unification.py",
      "v261_modular_spectral_closure.py",
      "v265_qft4d_fork_freeze.py",
      "v269_spert_paqft_skeleton.py",
      "v271_eg_oneloop_quartic.py",
      "v273_eg_gauge_running.py",
      "v278_lsz_bridge_unitarity.py",
      "v276_qgeo_flat_closes_commutator.py",
      "v277_seam_calderon_e8_match.py",
      "v279_qgeo_obligation_lemma.py",
      "v280_pillowcase_steklov.py",
      "v281_holomorphy_modular_data.py",
      "v282_e8_tau_i_unification.py",
      "v284_route_i_rp_uniqueness.py",
      "v285_route_ii_seam_condensation.py",
      "v286_seam_equivalence_contract.py",
      "v287_free_rp_bulk_to_holomorphic_boundary.py",
      "v288_full_l2_subprincipal_z4.py",
      "v289_marklocal_raw.py",
      "v290_z4_smooth_curvature_adversary.py",
      "v291_flataway_contract.py",
      "v292_flataway_heat_reduction.py",
      "v293_flataway_spectral_hessian.py",
      "v294_flataway_rp_energy.py",
      "v295_flataway_a2_exact.py",
      "v296_flataway_a2_closed.py",
      "v297_route_a_literature_stack.py",
      "v300_flataway_rigid.py",
      "v301_route_a_invertible.py",
      "v302_seam_gap.py",
      "v304_idg_nonlocal_ghost.py",
      "v335_seam_equiv_unify.py",
      "v336_continuum_limit.py",
      "v337_decoupling_theorem.py",
      "v344_detk_synthesis.py",
      "v345_hypergraph_homotopy.py",
      "v346_seam_geometric_bridge.py",
      "v347_seam_closure_modes.py",
      "v348_seam_rigidity_route.py",
      "v351_continuum_realisation_sharpened.py",
      "v356_continuum_mmst_applicability.py",
      "v365_qg_oneloop_saddle.py",
      "v366_mmst_seam_collar.py",
      "v367_seam_s3_lattice.py",
      "v368_seam_s3_inflow.py",
      "v369_qgamb_redundancy.py",
      "v370_grav_spin2_unitarity.py",
      "v376_seam_s3_centralcharge.py",
      "v377_seam_s3_e8character.py",
      "v378_seam_s3_modular.py",
      "v379_seam_s3_rp.py",
      "v392_seam_s3_scalinglimit.py",
      "v489_seam_modular_commutator.py",
      "v490_seam_parity_census.py",
      "v380_grav_kms_hessian.py",
      "v381_qft4d_eg_allorder.py",
      "v385_uvbranch_killtest.py",
      "v386_grav_amplitude.py",
      "v389_grav_loop_finiteness.py",
      "v458_seam_mmst_citation_audit.py",
      "v459_seam_lattice_voa_route.py",
      "v462_seam_spinor_continuum.py",
      "v463_seam_c8_holomorphic_uniqueness.py",
      "v464_seam_oneparticle_rigidity.py",
      "v469_seam_crossedproduct_route.py",
      "v471_seam_horizon_replica.py",
      "v479_kronheimer_quiver_bridge.py",
      "v480_multilocal_four_interval.py",
      "v492_celestial_z4_orbifold.py",
      "v493_celestial_wp2_clock_deformation.py",
      "v495_celestial_wp3_gs_alignment.py",
      "v496_celestial_wp4_character_shadow.py",
      "v497_celestial_wp5a_null_ideal.py",
      "v498_celestial_wp5b_singular_vector.py",
      "v500_celestial_wp5c_gns_limit_state.py",
      "v501_celestial_wp5d_two_interval_index.py",
      "v502_celestial_wp5e_prefactor_level.py",
      "v504_celestial_wp5d_klm_completeness.py",
      "v505_celestial_wp5e_beta_equivariant_ledger.py",
      "v508_celestial_wp5e_gamma_pairing.py",
      "v509_celestial_wp5e_eps2_level_from_flux.py",
      "v511_celestial_wp5e_delta2_tensor_ledger.py",
      "v513_celestial_dterm_nonderivation.py",
      "v514_celestial_wp5e_eps1_axion_slot.py",
      "v515_celestial_wp5e_m1_omega_n.py",
      "v516_celestial_wp5e_m2_twisted_ks_measure.py",
      "v517_celestial_wp5e_m3_a0_uplift.py",
      "v518_celestial_wp5e_delta1_derived_kill.py",
      "v519_woit_theta_rp_free.py",
      "v520_celestial_wp5e_measure_decision.py",
      "v521_seam_bit_rp_blind.py",
      "v522_woit_beta1_gso_gauge.py",
      "v523_celestial_wp5e_wm_derived.py",
      "v524_woit_beta2_os_quotient.py",
      "v525_seam_bit_twist_blind.py",
      "v526_seam_thermal_kms_nariai_bridge.py",
      "v527_seam_clock_silver_spectrum.py",
      "v528_seam_bit_twist_class_definition.py",
      "v529_seam_interacting_toy_fk.py",
    ],
  },
  {
    id: "boot",
    label: "self-consistency",
    x: 27,
    y: 50,
    tone: "lattice",
    marker: "[E] lattice theorem",
    title: "The bootstrap / self-consistency loop",
    summary:
      "The E₈ closure feeds back and fixes the two inputs: g_car = 5 is forced three independent ways (rank-fill, Coxeter-match, and the integer-glue quadratic μ² − 5μ + 4 = 0), and the 8 in c₃ equals rank E₈ = h(D₅) = φ(30). A gapped boundary transport (Δ = 6 log 3/2 > 0) then has, by Perron–Frobenius, a unique attractor at rate (2/3)⁶ — so parameter-freeness is a theorem, not a tuning. Only π stays irreducible. TFPT is therefore not a linear theory (axioms → theorems) but a closed self-consistent loop: the two 'axioms' are back-determined by the closure, not free choices (v350/v352/v353). The same gapped → unique-attractor structure recurs in every sector (compiler, flavor, QFT, gravity, QG), so parameter-freeness is ONE spectral-gap theorem theory-wide (v383); and the entire residual is now certification, not construction — every open item is an external math proof, theorem-forbidden, or external physics, with zero open internal mechanisms (v384).",
    inputs: ["E₈ closure"],
    outputs: ["g_car = 5, 8 = rank E₈; unique attractor"],
    failure: "g_car not forced three ways; the transport gap is not positive.",
    scripts: [
      "v6_bootstrap.py",
      "v14_carrier_uniqueness.py",
      "v54_seam_horizon_keystones.py",
      "v55_coxeter_cycle.py",
      "v56_unique_attractor.py",
      "v171_os_moment_cluster.py",
      "v222_cm_norm_duality.py",
      "v319_translation_clock.py",
      "v350_bootstrap_inputs_correction.py",
      "v352_framework_irreducible.py",
      "v353_selfloop_capstone.py",
      "v383_dynamics_universal.py",
      "v384_residual_certification.py",
      "v387_corrections_gap.py",
      "v388_corrections_budget.py",
      "v390_prime2_facet.py",
      "v393_corrections_numeric.py",
      "v394_coxeter_atoms.py",
    ],
  },
];

type EdgeKind = "normal" | "dressing" | "bootstrap";

interface DagEdge {
  from: string;
  to: string;
  kind: EdgeKind;
}

const EDGES: DagEdge[] = [
  { from: "P1", to: "D5", kind: "normal" },
  { from: "P2", to: "D5", kind: "normal" },
  { from: "P1", to: "A3", kind: "normal" },
  { from: "P2", to: "A3", kind: "normal" },
  { from: "D5", to: "E8", kind: "normal" },
  { from: "A3", to: "E8", kind: "normal" },
  { from: "E8", to: "RL", kind: "normal" },
  { from: "RL", to: "alpha", kind: "normal" },
  { from: "RL", to: "masses", kind: "normal" },
  { from: "RL", to: "theta12", kind: "normal" },
  { from: "E8", to: "cosmo", kind: "normal" },
  { from: "E8", to: "qft", kind: "normal" },
  { from: "P1", to: "alpha", kind: "dressing" },
  { from: "P1", to: "cosmo", kind: "dressing" },
  { from: "E8", to: "boot", kind: "bootstrap" },
  { from: "boot", to: "P1", kind: "bootstrap" },
  { from: "boot", to: "P2", kind: "bootstrap" },
];

const byId = (id: string) => NODES.find((n) => n.id === id)!;

const EDGE_STROKE: Record<EdgeKind, string> = {
  normal: "#64748b",
  dressing: "#d4a017",
  bootstrap: "#fb7185",
};

export function VerificationDag() {
  const [selected, setSelected] = useState<string>("E8");
  const node = byId(selected);
  const { open } = useReproducer();

  // An edge is "active" if it touches the selected node, or — for bootstrap
  // edges — whenever the bootstrap node is selected (it owns the whole loop).
  const isEdgeActive = (e: DagEdge) => {
    if (e.from === selected || e.to === selected) return true;
    if (e.kind === "bootstrap" && selected === "boot") return true;
    return false;
  };
  const connectedToSelected = (id: string) =>
    id === selected ||
    EDGES.some(
      (e) =>
        (e.from === selected && e.to === id) ||
        (e.to === selected && e.from === id) ||
        (selected === "boot" && e.kind === "bootstrap" && (e.from === id || e.to === id)),
    );

  return (
    <div className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Interactive dependency graph — click any node
        </span>
        <div className="flex flex-wrap items-center gap-3 text-[10px] font-medium text-slate-400">
          <LegendDot className="bg-slate-400" label="axiom" />
          <LegendDot className="bg-cyan-400" label="lattice" />
          <LegendDot className="bg-emerald-400" label="identity" />
          <LegendDot className="bg-violet-400" label="numerical" />
          <LegendDot className="bg-amber-400" label="conditional" />
          <span className="inline-flex items-center gap-1.5">
            <span className="inline-block h-0.5 w-4 bg-rose-400" />
            self-consistency
          </span>
        </div>
      </div>

      {/* Graph canvas — horizontally scrollable on small screens */}
      <div className="overflow-x-auto">
        <div className="relative mx-auto aspect-[16/9] min-w-[760px]">
          <svg
            className="absolute inset-0 h-full w-full"
            aria-hidden="true"
            preserveAspectRatio="none"
          >
            <defs>
              {(Object.keys(EDGE_STROKE) as EdgeKind[]).map((k) => (
                <marker
                  key={k}
                  id={`arrow-${k}`}
                  viewBox="0 0 10 10"
                  refX="8"
                  refY="5"
                  markerWidth="6"
                  markerHeight="6"
                  orient="auto-start-reverse"
                >
                  <path d="M 0 0 L 10 5 L 0 10 z" fill={EDGE_STROKE[k]} />
                </marker>
              ))}
            </defs>
            {EDGES.map((e, i) => {
              const a = byId(e.from);
              const b = byId(e.to);
              const active = isEdgeActive(e);
              return (
                <line
                  key={i}
                  x1={`${a.x}%`}
                  y1={`${a.y}%`}
                  x2={`${b.x}%`}
                  y2={`${b.y}%`}
                  stroke={EDGE_STROKE[e.kind]}
                  strokeWidth={active ? 2.4 : 1.3}
                  strokeOpacity={active ? 0.95 : e.kind === "normal" ? 0.4 : 0.3}
                  strokeDasharray={e.kind === "normal" ? undefined : "5 4"}
                  markerEnd={`url(#arrow-${e.kind})`}
                />
              );
            })}
          </svg>

          {NODES.map((n) => {
            const tone = TONE[n.tone];
            const isSel = n.id === selected;
            const isConn = connectedToSelected(n.id);
            const dim = !isSel && !isConn;
            return (
              <button
                key={n.id}
                type="button"
                onClick={() => setSelected(n.id)}
                aria-pressed={isSel}
                aria-label={`${n.title} (${n.marker})`}
                style={{ left: `${n.x}%`, top: `${n.y}%` }}
                className={cn(
                  "absolute -translate-x-1/2 -translate-y-1/2 rounded-xl px-3 py-2 text-center transition-all",
                  "border bg-slate-950/85 ring-1 backdrop-blur",
                  n.id === "boot"
                    ? "border-rose-400/40 ring-rose-400/30"
                    : "border-slate-700/60",
                  isSel
                    ? cn("z-20 scale-105 ring-2", tone.activeRing)
                    : cn("z-10", tone.ring),
                  dim ? "opacity-40" : "opacity-100",
                  "hover:z-20 hover:scale-105",
                )}
              >
                <span className="flex items-center justify-center gap-1.5">
                  <span
                    aria-hidden
                    className={cn("h-1.5 w-1.5 flex-none rounded-full", tone.dot)}
                  />
                  <span className="font-mono text-[11px] font-semibold text-slate-50 sm:text-xs">
                    {n.label}
                  </span>
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Detail panel */}
      <motion.div
        key={selected}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="border-t border-slate-800/60 p-5 sm:p-6"
        aria-live="polite"
      >
        <div className="flex flex-wrap items-center gap-2">
          <h3 className="font-serif text-lg font-semibold text-slate-50">
            {node.title}
          </h3>
          <span
            className={cn(
              "rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1",
              TONE[node.tone].chip,
            )}
          >
            {node.marker}
          </span>
        </div>
        <Expandable collapsedHeight={140} className="mt-2 max-w-3xl">
          <p className="break-words text-sm leading-relaxed text-slate-300">
            <RichText text={node.summary} />
          </p>
        </Expandable>

        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <DetailCell label="Inputs" items={node.inputs} />
          <DetailCell label="Outputs" items={node.outputs} highlight />
          <DetailCell label="How it can fail" items={[node.failure]} warn />
        </div>

        <div className="mt-4">
          <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
            Verified by ({node.scripts.length} script
            {node.scripts.length > 1 ? "s" : ""}) — click to run in your browser
          </div>
          <div className="mt-2 flex flex-wrap gap-2">
            {node.scripts.map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => open(s)}
                className="group inline-flex items-center gap-1.5 rounded-md border border-slate-700/50 bg-slate-900/60 px-2.5 py-1 font-mono text-[11px] text-slate-200 transition-colors hover:border-blue-400/50 hover:bg-blue-500/10 hover:text-blue-100"
              >
                <FileCode2 size={12} className="group-hover:hidden" aria-hidden />
                <Play size={12} className="hidden text-blue-300 group-hover:inline" aria-hidden />
                {s}
              </button>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
}

function LegendDot({ className, label }: { className: string; label: string }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <span className={cn("h-2 w-2 rounded-full", className)} aria-hidden />
      {label}
    </span>
  );
}

function DetailCell({
  label,
  items,
  highlight,
  warn,
}: {
  label: string;
  items: string[];
  highlight?: boolean;
  warn?: boolean;
}) {
  return (
    <div
      className={cn(
        "rounded-lg border p-3",
        highlight
          ? "border-emerald-400/25 bg-emerald-500/5"
          : warn
            ? "border-orange-400/25 bg-orange-500/5"
            : "border-slate-700/40 bg-slate-950/40",
      )}
    >
      <div
        className={cn(
          "text-[10px] font-semibold uppercase tracking-widest",
          highlight
            ? "text-emerald-300/85"
            : warn
              ? "text-orange-300/85"
              : "text-blue-300/80",
        )}
      >
        {label}
      </div>
      <ul className="mt-1.5 space-y-1 break-words text-xs leading-relaxed text-slate-300">
        {items.map((it, i) => (
          <li key={i}>
            <RichText text={it} />
          </li>
        ))}
      </ul>
    </div>
  );
}

"use client";

import { useState } from "react";
import { motion } from "motion/react";
import { FileCode2, Play } from "lucide-react";
import { cn } from "@/lib/utils";
import { useReproducer } from "./Reproducer";

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
      "The reflection-positive boundary kernel. The seam normaliser, Gauss–Bonnet-hardenable as c₃ = 1/(|ℤ₂|·∮ K) = 1/(8π). One of the two declared inputs.",
    inputs: ["— declared axiom"],
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
      "The carrier rank g_car = 5 (3 colour + 2 weak). The P2 algebra — hypercharge, anomaly-freedom, integer rigidity — is Lean-formalised (0 sorry). Theorem A is now also Lean-formalised: the Pascal carrier condition 2^g = g²+g+2 has the unique solution g = 5 (audited to the standard kernel axioms). Since the QBL theorem chain (v108–v113) the axiom is reduced to the boundary-net premise: the seam's one scalar kernel must pair the sheets (v110), the certified channel counts the code identically (v112), pair transport is minimally complete (v111), and the one quasi-free kernel — rank = c: 5 carrier block, 8 seam hull — is the defining datum of the free c=8 net (v113); closing the index-4 net statement closes this axiom to [E].",
    inputs: ["— declared axiom"],
    outputs: ["g_car = 5"],
    failure: "Wrong family / charge lattice.",
    scripts: ["v2_carrier_pascal.py", "v14_carrier_uniqueness.py"],
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
      "D₅ and A₃ share the discriminant group ℤ₄; their glue norms add to the root norm, q(D₅) + q(A₃) = 5/4 + 3/4 = 2. So E₈ = (D₅ ⊕ A₃) + μ₄ closes as a lattice theorem. E₈ is the unimodular audit hull, not a gauge group; 240 = 16·5·3 roots, 248 = 240 + 8.",
    inputs: ["D₅", "A₃"],
    outputs: ["240 roots, 248 = dim E₈"],
    failure: "Not even-unimodular; glue norms do not sum to 2.",
    scripts: [
      "v1_e8_glue.py",
      "v6_bootstrap.py",
      "v15_bootstrap_classification.py",
      "v47_selection_theorem.py",
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
      "The residue + winding matrix on the anchor a = (1,1,2). det R = 8 = h(D₅), principal 2-minors (2,3,5) with product h(E₈) = 30, ‖R‖_F² = 78 = dim E₆, χ_R = t³ − 9t² + 10t − 8, Σ L = 40. Inverse Anchor Theorem: 1ᵀM⁻¹1 = 1/atom and aᵀM⁻¹a = 1 for R, K, L. Operator-pencil geometry: det B(K+xQ) = (3x+2)(3x+5), a quadratic ⇒ y² = det B(K+xQ) is a double cover of the pencil line branched exactly at Koide x = −2/3 and carrier x = −5/3 — they are the two branch points (deck degree 2 = |ℤ₂| = the sheet; disc = 81 = N_fam⁴; separation = 1 transport period). Clearing matrices: 3K−2Q reproduces the D₅⊕A₃ glue (Σ = 240 = |R(E₈)|), 3K−5Q is charge-neutral. Block-det type checker det B = (9,10,16,40) for (Q,K,R,L). The relative operator T = 3 B(Q)⁻¹B(K) = [[5,11/3],[0,2]] has Spec {2,5}, tr 7 = scalaron, det 10 = A_Λ — the basis-invariant core. Forced Koide attractor: the unique branch-preserving Möbius map fixing q = 2,5 has multiplier (2/3)⁶ = the established transfer gap λ₂ (v54/56), so the Koide RG collapses to one identification; the clean rational split is non-generic (placement discriminants 81/49/40). Branch-kernel selection: at each branch point the anchor block is rank 1 with integer kernels (carrier kernel = the democratic vector 1); the collapse direction (−1,1,0) makes up/down the deck-odd pair and puts the leptons ON the ramification — and the anchor-forced cusp conjugation T_A (a = e₂+e₃) realises the same deck action. The dictionary 'Q₊ grading = A₃ discriminant grading' is now DERIVED (G = T_A·Σ acts integrally as B₁⊕E on the cusp basis), so the sheet question carries no separate [C]: its residual folds into the one existing Q-geometry gate. The Koide flow has the canonical generator dq/dt = (Δ/N_fam)·det B(q); the discrete-vs-continuous question is experimental (n=3 steps ⇔ m_τ = 1776.9427 MeV, decision at σ(m_τ) ~ 0.01 MeV).",
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
      "The fine-structure constant is the unique positive root of the boundary U(1) Ward identity F_U(1)(α) = 0, built from c₃ and the abelian coefficient 41 = 10 b₁. Existence and uniqueness are proved; α⁻¹ = 137.0359992168, 1.9σ from CODATA-2022.",
    inputs: ["c₃ (P1)", "M = 41 = 10 b₁ (from R, L)"],
    outputs: ["α⁻¹ = 137.0359992168"],
    failure: "No root, or a second admissible root.",
    scripts: ["v3_em_alpha.py", "v48_em_ward.py", "v159_pyrate_gauge_crosscheck.py"],
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
      "All nine masses, CKM and the PMNS skeleton from one master formula m = (v/√2) λ_Y^L Λ with the seed φ₀. Charged-lepton coefficients (16/7, 4/3, 7/6) are exact; quark mass ratios (55/117, …) are integer Plücker readouts. Gate 1 is now complete: the absolute amplitude U_point reduces to one overall scale v_geo (ratios + Grand Mass Volume) — the same dimensionful anchor as gravity's 1/G. New (v114): the distinguished transport value δ = 1/2 is a μ₄-torsion theorem — flatness of the U_wall family is exactly (MU)⁴ = 1, and on the involutive branch the cusp trace forces diag M = (0, i/2, −i/2) with the cusp class automatic.",
    inputs: ["R, L", "φ₀ (from c₃)"],
    outputs: ["9 masses, mixings"],
    failure: "Hierarchy mismatch.",
    scripts: [
      "v18_quark_yukawa.py",
      "v20_lepton_c_derivation.py",
      "v24_quark_ratio_closure.py",
      "v46_grand_mass_volume.py",
      "v49_readout_rigidity.py",
      "v75_upoint_to_vgeo.py",
      "v88_cp_phase_audit.py",
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
      "The previously open SM angle. Tri-bimaximal 1/3 plus the seam misalignment ε = q(A₃)φ₀ = (3/4)φ₀ gives sin²θ₁₂ = 1/3 − φ₀/2 = 0.306747 — 0.1% from NuFIT 6.0. The live JUNO test. Since 2026-06-09 this is the frozen prediction of record in the machine-enforced blind registry (v84): exactly one θ₁₂ number is committed in advance, and the seam/non-linear variants are typed as derived variants of the same texture, never as alternatives.",
    inputs: ["R, L", "φ₀"],
    outputs: ["sin²θ₁₂ = 0.306747 (frozen)"],
    failure: "Seam-misalignment lemma fails.",
    scripts: [
      "v9_neutrino_texture.py",
      "v16_solar_dual_anchor.py",
      "v21_solar_product_quark.py",
      "v84_frozen_registry.py",
      "v163_rg_stability_flavor.py",
    ],
  },
  {
    id: "cosmo",
    label: "Λ, A_s, n_s, r",
    x: 90,
    y: 88,
    tone: "conditional",
    marker: "[C] conditional",
    title: "Gravity & cosmology — the geometry channel",
    summary:
      "The spectral action gives R + R²; the scalaron mass is M = c₃^(7/2) M̄ = 3.06×10¹³ GeV (exponent 7 = Ω_adm − 10 b₁). From the same attractor: n_s = 1 − 2/N★ and r = 12/N★² over the frozen band N★ ∈ [50,60]; the scalaron-reheating chain (v86) sharpens this conditionally to N★ = 51.4 ⇒ n_s = 0.9611, r = 0.0045 — recorded with its tensions (A_s coherence disfavours the slow Higgs channel at −11.4σ; the measured A_s requires near-instantaneous reheating). Λ ∼ e⁻²ᵅ⁻¹, H₀ ∼ √Λ. Gate 2: the IR tier is gap-decoupled (Δ_eff = 1.648 > 0), and the ambient measure G6 is holographically reduced to the rigorously-constructed (E₈)₁ lattice net (c = 8 = 5 + 3). After v83 + v87 the whole Target-A gate is ONE theorem: prove the seam–Calderón boundary net is holomorphic with c = 8 — then (E₈)₁ is the unique net (Minkowski–Siegel) AND the 2D bulk is unique (LR/KLM/BKLR; SO(16)₁ counter-model admits six modular invariants). Every scale is a ratio to one v_geo — the dimensional-analysis floor. New classical-gravity fingerprint (v101): the maximal black hole in the de Sitter bulk (Nariai) has horizon roots (1,1,−2) = the traceless anchor, its entropy bound is exactly the Koide 2/3 = |ℤ₂|/N_fam, the SdS mass line is itself a split double cover (deck = horizon swap), and evaporation flows away from the anchor point — the same repeller/attractor orientation as the flavor relaxation. Six atom landings, zero free parameters.",
    inputs: ["c₃ (P1)", "E₈"],
    outputs: ["Λ, A_s, n_s, r, scalaron M"],
    failure: "Ambient reflection-positivity fails.",
    scripts: [
      "v7_gravity_cosmo.py",
      "v28_gravity_fR.py",
      "v36_spectral_action_g2.py",
      "v60_lambda_metrology_branch.py",
      "v76_gmetric_reduction.py",
      "v77_e8_conformal_net.py",
      "v78_vgeo_floor.py",
      "v83_e8net_holomorphic_uniqueness.py",
      "v86_nstar_reheating.py",
      "v87_bulk_uniqueness_reduction.py",
      "v101_horizon_anchor.py",
      "v102_seam_orientation.py",
      "v103_trisection_normal_form.py",
      "v104_nariai_clock.py",
      "v105_residual_inventory.py",
      "v107_quantum_clock_target.py",
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
      "The E₈ closure feeds back and fixes the two inputs: g_car = 5 is forced three independent ways (rank-fill, Coxeter-match, and the integer-glue quadratic μ² − 5μ + 4 = 0), and the 8 in c₃ equals rank E₈ = h(D₅) = φ(30). A gapped boundary transport (Δ = 6 log 3/2 > 0) then has, by Perron–Frobenius, a unique attractor at rate (2/3)⁶ — so parameter-freeness is a theorem, not a tuning. Only π stays irreducible.",
    inputs: ["E₈ closure"],
    outputs: ["g_car = 5, 8 = rank E₈; unique attractor"],
    failure: "g_car not forced three ways; the transport gap is not positive.",
    scripts: [
      "v6_bootstrap.py",
      "v14_carrier_uniqueness.py",
      "v54_seam_horizon_keystones.py",
      "v55_coxeter_cycle.py",
      "v56_unique_attractor.py",
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
        <p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-300">
          {node.summary}
        </p>

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
      <ul className="mt-1.5 space-y-1 text-xs leading-relaxed text-slate-300">
        {items.map((it, i) => (
          <li key={i}>{it}</li>
        ))}
      </ul>
    </div>
  );
}

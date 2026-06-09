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

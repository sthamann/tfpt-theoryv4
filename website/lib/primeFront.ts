/**
 * Live update feed for /prime-front ("The Prime Front").
 *
 * HOW TO POST A NEW ENTRY after a completed agent run:
 *   1. Open this file.
 *   2. Prepend a new object to `PRIME_FRONT_UPDATES` (newest first).
 *   3. Fill every field below; keep `summary` to 1–2 sentences.
 *   4. Rebuild / redeploy the website — no other files required for a feed post.
 *
 * Do not invent numbers. Copy verdicts and anchors from experiments/next.txt
 * (or the promoted verification/vN_*.py). Firewall: no "RH evidence" language.
 */

export type PrimeFrontBadge = "sandbox" | "machine-verified" | "running";

export type PrimeFrontVerdict =
  | "EXACT"
  | "PARTIAL"
  | "DEFLATED"
  | "DEAD"
  | "KILLED-AS-NAIVE"
  | "MIXED"
  | "BENCHMARK"
  | "REPAIRED"
  | "HARDENED"
  | "FOUNDED"
  | "PROMOTED"
  | "CLOSED"
  | "TERRAIN-MAPPED"
  | "RUNNING"
  | "TYPED";

export type PrimeFrontUpdate = {
  /** ISO date (YYYY-MM-DD) of the agent run. */
  date: string;
  /** Diary part number (Teil N). */
  part: number;
  title: string;
  verdict: PrimeFrontVerdict;
  /** 1–2 sentences; plain English; scientifically honest. */
  summary: string;
  badge: PrimeFrontBadge;
  /** Optional probe / verification script basename. */
  script?: string;
};

/**
 * Newest first. Future agent runs: prepend here.
 */
export const PRIME_FRONT_UPDATES: readonly PrimeFrontUpdate[] = [
  {
    date: "2026-07-24",
    part: 38,
    title: "Cuspidal bridge (in progress)",
    verdict: "RUNNING",
    summary:
      "Open lever: translate the cuspidal sector (where a_p lives, centre 2) toward a weight-½ / ξ-line object. Placeholder until the run completes.",
    badge: "running",
    script: "cuspidal_bridge_probe.py",
  },
  {
    date: "2026-07-24",
    part: 37,
    title: "Signed / scalable cusp evaluator (in progress)",
    verdict: "RUNNING",
    summary:
      "Building an independent O(p²)-scale character-sum evaluator for λ_geom that can extract signed a_p (not only a_p²). Placeholder until the run completes.",
    badge: "running",
    script: "e8_lambda_charsum_evaluator_probe.py",
  },
  {
    date: "2026-07-24",
    part: 40,
    title: "Stage-4 terrain map",
    verdict: "TERRAIN-MAPPED",
    summary:
      "Today's operator algebra has a two-point spectrum; a Hilbert–Pólya carrier needs infinitely many. Only two candidate classes remain (seam modular flow; adelic BC completion), each with preregistered kills. Distance to RH stated honestly: large.",
    badge: "sandbox",
    script: "weil_recovery_compiler_sector_probe.py",
  },
  {
    date: "2026-07-24",
    part: 39,
    title: "Centre atlas — abelian weight drop closed",
    verdict: "CLOSED",
    summary:
      "The ξ-line (centre 1/2) is reached exactly by weight ≤ 1 theta factors: Mellin(θ₃) → ζ(2s) and ζ_{ℚ(i)} = ζ(s)L(s,χ₄). Abelian drop = factorisation + Mellin, typed closed. Cuspidal channel remains at centre 2 — no spectral / RH content claimed.",
    badge: "sandbox",
    script: "zeta_center_atlas_probe.py",
  },
  {
    date: "2026-07-24",
    part: 36,
    title: "λ_geom evaluator — two-sided Eichler to p ≤ 5",
    verdict: "HARDENED",
    summary:
      "Independent f₈-free geometry: λ_geom = λ_i + λ_ii hits anchors λ_geom(3)=352 and λ_geom(5)=3784; residual R(p)=a_p² exactly. Two-sided confirmation (mod-p geometry ↔ eta product) at p ≤ 5; p ≥ 7 gated by shell size.",
    badge: "sandbox",
    script: "e8_lambda_charsum_evaluator_probe.py",
  },
  {
    date: "2026-07-24",
    part: 35,
    title: "Rankin–Selberg translates only the abelian shadow",
    verdict: "TYPED",
    summary:
      "RS-TRANSLATES-EISENSTEIN: multiplicative convolution of compiler factors yields exact ζ(s)L(s,χ₄)ζ(s−2)L(s−2,χ₄) products — but after weight normalisation no GL(1) factor sits on the ξ-line, and f₈ is invisible. Cuspidal channel does not cross this bridge.",
    badge: "sandbox",
    script: "rankin_selberg_functor_probe.py",
  },
  {
    date: "2026-07-24",
    part: 34,
    title: "Compiler functor founded with anchor",
    verdict: "FOUNDED",
    summary:
      "In-suite RH centre 1/2 is defined via Mellin((θ₃−1)/2); unique factorisation among 45 monomials picks only (2,6,0) for the signed glue theta. Bare Shimura on θ₃ sees a_p not at all — contract ZETA.COMPILER.FUNCTOR [O] founded with kills K1–K3.",
    badge: "sandbox",
    script: "compiler_functor_theta_probe.py",
  },
  {
    date: "2026-07-24",
    part: 33,
    title: "Many-prime hardening — Eichler identity",
    verdict: "HARDENED",
    summary:
      "HARDENED-TO-p≤100: geometric count splits as elementary Witt part + exactly a_p². Closed forms for all 24 odd primes ≤ 100; Ramanujan bound and cusp rule a_p = b − σ₃ hold. Smooth background + coherent interference.",
    badge: "sandbox",
    script: "e8_nu_rule_many_primes_probe.py",
  },
  {
    date: "2026-07-24",
    part: 32,
    title: "PROMOTED — Hecke from geometry (v535)",
    verdict: "PROMOTED",
    summary:
      "T27+T31+T32 consolidated into verification/v535_hecke_from_geometry.py (HECKE.GEOM.01, 25/25, AUDIT OK). The one load-bearing result of this series: Kneser + affine ν_p + 2-adic oldforms. No RH claim; weight-4→GL(1) stays open.",
    badge: "machine-verified",
    script: "v535_hecke_from_geometry.py",
  },
  {
    date: "2026-07-24",
    part: 32,
    title: "Census redundancy is 2-adic oldform structure",
    verdict: "EXACT",
    summary:
      "REDUNDANCY-IS-OLDFORM: dim V = 7 = 5 (E₄ copies, levels 1..16) + 2 (f₈ copies, levels 8,16). Recovery projectors π_cusp = (28−T₃)/32, π_Eis = (T₃+4)/32; new spaces each dim 1. Level census purely 2-adic.",
    badge: "sandbox",
    script: "census_newform_recovery_probe.py",
  },
  {
    date: "2026-07-24",
    part: 31,
    title: "Neighbour operator = affine Hecke element",
    verdict: "REPAIRED",
    summary:
      "REPAIRED-BY-DICTIONARY: ν_p = a·Id + b·T_p with b = σ₃ + a_p — one (a,b) for all shells/channels. Frozen geometry outputs a₃=−4, a₅=−2, |a₇|=24. T30's broken reading was a normalisation artifact.",
    badge: "sandbox",
    script: "e8_neighbor_operator_decomposition_probe.py",
  },
  {
    date: "2026-07-24",
    part: 30,
    title: "Uniformity test broken — p=3 coincidence",
    verdict: "DEAD",
    summary:
      "The Teil-28 reading a_p = #P³ − λ_odd/8 fails at p=5 (λ_odd=3784 ≠ 1264). Transport structure itself holds; only the eigenvalue reading was a coincidence. Named repair path → T31.",
    badge: "sandbox",
    script: "e8_transport_cusp_uniformity_probe.py",
  },
  {
    date: "2026-07-24",
    part: 29,
    title: "Primon transport category — relations verified",
    verdict: "EXACT",
    summary:
      "RELATIONS-VERIFIED: coprimality, ladder, and constructive decompositions of T_n hold on compiler channels. Stable 4×4 on (Tot, Spinor, Eis, f₈): T₃ = diag(28,28,28,−4), T₅ = diag(126,126,126,−2).",
    badge: "sandbox",
    script: "primon_transport_category_probe.py",
  },
  {
    date: "2026-07-24",
    part: 28,
    title: "Cusp coefficient visible from Kneser transport",
    verdict: "PARTIAL",
    summary:
      "At p=3, full enumeration of 1120 neighbour lattices yields a₃ = −4 exactly from mod-3 geometry — no modular-form import. Honest fence: uniformity untested (later broken at T30).",
    badge: "sandbox",
    script: "e8_kneser_transport_holonomy_probe.py",
  },
  {
    date: "2026-07-24",
    part: 27,
    title: "Kneser p-neighbours carry Hecke (Eisenstein half)",
    verdict: "PARTIAL",
    summary:
      "#iso_lines = σ₃(p)·#P³ enumerated at p=2,3,5,7 (135/1120/19656/137600). Eisenstein eigenvalue is lattice-native; μ4-refined line counts do not yet recover a_p(f₈). Later consolidated into v535.",
    badge: "sandbox",
    script: "e8_pneighbor_hecke_probe.py",
  },
  {
    date: "2026-07-24",
    part: 26,
    title: "Shell quotienting dead",
    verdict: "DEAD",
    summary:
      "Weyl-orbit and W(D5)×W(A3)×glue quotients break multiplicativity. Only classical primitive stratification β = r_prim/240 survives — still weight 4, no GL(1). Full W(E8) does not preserve μ4 glue class.",
    badge: "sandbox",
    script: "shell_multiplicity_one_quotient_probe.py",
  },
  {
    date: "2026-07-24",
    part: 25,
    title: "Scattering phase dead — arch route closed",
    verdict: "DEAD",
    summary:
      "Last non-counting observable fails: seam overlaps lack the thermal Unruh magnitude; discrete sector clock (π/4, π/2) remains. Arch-from-seam route closed in four preregistered stages. Seam = discrete μ4 clock, not a hidden Gamma.",
    badge: "sandbox",
    script: "seam_tate_phase_probe.py",
  },
  {
    date: "2026-07-24",
    part: 24,
    title: "Truncated-trace / RvM dictionary dead",
    verdict: "DEAD",
    summary:
      "Under the only allowed self-dual rule L=√T, Peschel counting leads 1/(2π²) not 1/(2π). The fit that would hit RvM is algebraically forbidden. π-factor misses in every allowed counting version.",
    badge: "sandbox",
    script: "seam_truncated_trace_rvm_probe.py",
  },
  {
    date: "2026-07-24",
    part: 23,
    title: "Boost–arch dictionary dead on three lines",
    verdict: "DEAD",
    summary:
      "Chord-vs-arc 2/π hypothesis fails; coupled cutoffs miss; digamma-in-the-seam finds no named ψ/log candidate. Seam carries the boost, not the archimedean slot of the explicit formula.",
    badge: "sandbox",
    script: "seam_boost_arch_dictionary_probe.py",
  },
  {
    date: "2026-07-24",
    part: 22,
    title: "Interval cut carries the missing log — dictionary still fails",
    verdict: "PARTIAL",
    summary:
      "Entanglement Hamiltonian of a seam half-cut has 1/ln L spacing and Peschel universal form (K1/K2). One-constant dictionary ln L ↔ ln(T/2π) misses by classical factor 2/π (K3).",
    badge: "sandbox",
    script: "seam_halfcut_dilation_arch_probe.py",
  },
  {
    date: "2026-07-24",
    part: 21,
    title: "Can TFPT predict primes? Three honest channels",
    verdict: "TYPED",
    summary:
      "Exact geometric primality: n prime ⟺ shell(2n) has 240(1+n³) vectors (0 errors to 10⁴). Glue characters predict two-squares type at 100%. Positional prediction needs the zero spectrum — that operator does not exist.",
    badge: "sandbox",
    script: "prime_prediction_mechanics_probe.py",
  },
  {
    date: "2026-07-24",
    part: 20,
    title: "Arch kernel killed as naive",
    verdict: "KILLED-AS-NAIVE",
    summary:
      "Raw seam mode density is flat/falling O(1); classical digamma arch kernel grows as log. Archimedean term does not live in free seam DOS. Route narrowed, not absolutely dead — until T25 closed it.",
    badge: "sandbox",
    script: "seam_archimedean_kernel_probe.py",
  },
  {
    date: "2026-07-24",
    part: 19,
    title: "Prime thinning ↔ seam truncation",
    verdict: "MIXED",
    summary:
      "At suite temperatures the small prime tower carries almost all of log ζ(β) ({2,3,5}: 99.962% at β=2π). Post-hoc 'exactly {2,3,5} is the 99% set' is dead. TFPT tones are not distinguished on the prime clock.",
    badge: "sandbox",
    script: "prime_thinning_seam_truncation_probe.py",
  },
  {
    date: "2026-07-24",
    part: 18,
    title: "Guinand–Weil benchmark standing; arch gap typed",
    verdict: "BENCHMARK",
    summary:
      "Classical Guinand–Weil balance verified as executable reference (500 zeros). Weil↔v221 dictionary for pole+prime; archimedean digamma term has no seam counterpart — the precise gap of ZETA.WEIL.RECOVERY.",
    badge: "sandbox",
    script: "zeta_weil_recovery_trace_probe.py",
  },
  {
    date: "2026-07-24",
    part: 17,
    title: "Functional-equation duality on the census",
    verdict: "PARTIAL",
    summary:
      "Poisson involution Λ_E8(s)=Λ_E8(4−s) to ≥20 digits; character channels form an exact dual pair with factor 1. Weight transport 4→½ remains open with kill preregistered.",
    badge: "sandbox",
    script: "zeta_funceq_duality_probe.py",
  },
  {
    date: "2026-07-24",
    part: 16,
    title: "One Hecke polynomial covers three character channels",
    verdict: "PARTIAL",
    summary:
      "Weight-4 Hecke polynomial 1−a_p x+p³x² covers trivial/μ4/μ3 channels; Eisenstein factors as (1−x)(1−p³x); f₈ Deligne-pure. Seam derivation of the Hecke operation and GL(1) transport stay open.",
    badge: "sandbox",
    script: "zeta_local_euler_probe.py",
  },
  {
    date: "2026-07-24",
    part: 15,
    title: "Arithmetic completion — lattice Hamiltonian",
    verdict: "PARTIAL",
    summary:
      "E8 shell Hamiltonian H|x⟩=log(|x|²/2) yields Tr e^{−sH}=240ζ(s)ζ(s−3) — all primes, but multiplicity 240σ₃(n)≠1. Naive all-N completion killed; contract narrowed to multiplicity-1 reduction.",
    badge: "sandbox",
    script: "zeta_arith_completion_probe.py",
  },
  {
    date: "2026-07-24",
    part: 14,
    title: "Self-dual width slogan deflated",
    verdict: "DEFLATED",
    summary:
      "v526 measures β_steps=N (kernel detailed balance); angle 2π is universal BW/Unruh conversion — 'measured 2π is the self-dual width' overreached. Only E8 among atlas lattices admits a Poisson-self-dual width. Kill chain begins here.",
    badge: "sandbox",
    script: "seam_selfdual_width_probe.py",
  },
  {
    date: "2026-07-24",
    part: 13,
    title: "Glue character atlas — μ4 is not alone",
    verdict: "EXACT",
    summary:
      "Nine maximal root sub-splits yield cyclic glue orders {2,3,4,5,6}. μ3 mirrors the Teil-11 pattern (Q(ω), η(3τ)⁸); μ5 is χ₅-blind on that resolution. Character content is glue-order-limited and split-selective.",
    badge: "sandbox",
    script: "e8_glue_character_atlas_probe.py",
  },
  {
    date: "2026-07-24",
    part: 12,
    title: "Surprise bridges — Apéry / ζ(3) and L-series",
    verdict: "EXACT",
    summary:
      "Cusp form f₈=η(2τ)⁴η(4τ)⁴ is the Beukers/Ahlgren–Ono form: Apéry numbers A((p−1)/2) ≡ a_p mod p² for all odd p≤97. Signed channel is the unique pole-free L-series. Self-dual-width slogan later deflated at T14.",
    badge: "sandbox",
    script: "e8_glue_lseries_selfdual_probe.py",
  },
  {
    date: "2026-07-24",
    part: 11,
    title: "Signed census — θ₃²·θ₄⁶ is a tensor factor",
    verdict: "EXACT",
    summary:
      "Counting E8 shell points by glue colour and taking the signed difference yields exactly θ₃²·θ₄⁶. The Gaussian-integer theta (π via L(1,χ₄)=π/4) is a literal tensor factor of the μ4-glue census. Three channels: total, signed, spinor.",
    badge: "sandbox",
    script: "e8_glue_chi4_signed_theta_probe.py",
  },
];

/** Display order for the narrative sections (anchor ids). */
export const PRIME_FRONT_SECTIONS = [
  { id: "hook", label: "Hook" },
  { id: "compiler", label: "Compiler" },
  { id: "census", label: "Signed census" },
  { id: "bridges", label: "Surprise bridges" },
  { id: "kill-chain", label: "Kill chain" },
  { id: "predict", label: "Prime prediction" },
  { id: "hecke", label: "Hecke from geometry" },
  { id: "eichler", label: "Eichler layer" },
  { id: "weight-drop", label: "Weight drop" },
  { id: "stage-4", label: "Stage-4 map" },
  { id: "meaning", label: "What it would mean" },
  { id: "updates", label: "Live updates" },
] as const;

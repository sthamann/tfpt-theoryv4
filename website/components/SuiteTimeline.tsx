"use client";

import { motion } from "motion/react";
import { FileCode2, Play } from "lucide-react";
import { cn } from "@/lib/utils";
import { useReproducer } from "./Reproducer";

/**
 * SuiteTimeline — the development phases of the verification suite as live
 * HTML (replaces the static script_timeline.png figure).
 *
 * The phase data mirrors verification/make_figures.py::fig_script_timeline
 * (the same source that generates the PDF figure in the papers). Every phase
 * lists a few representative scripts that run live in the browser via the
 * Pyodide reproducer — the same mechanism as the dependency graph below.
 */

type PhaseTone = "blue" | "green" | "gold" | "red";

const TONE: Record<PhaseTone, { dot: string; ring: string; text: string; chip: string }> = {
  blue: {
    dot: "bg-blue-400",
    ring: "border-blue-400/30 bg-blue-500/[0.06]",
    text: "text-blue-200",
    chip: "hover:border-blue-400/50 hover:bg-blue-500/10 hover:text-blue-100",
  },
  green: {
    dot: "bg-emerald-400",
    ring: "border-emerald-400/30 bg-emerald-500/[0.06]",
    text: "text-emerald-200",
    chip: "hover:border-emerald-400/50 hover:bg-emerald-500/10 hover:text-emerald-100",
  },
  gold: {
    dot: "bg-amber-400",
    ring: "border-amber-400/30 bg-amber-500/[0.06]",
    text: "text-amber-200",
    chip: "hover:border-amber-400/50 hover:bg-amber-500/10 hover:text-amber-100",
  },
  red: {
    dot: "bg-rose-400",
    ring: "border-rose-400/30 bg-rose-500/[0.06]",
    text: "text-rose-200",
    chip: "hover:border-rose-400/50 hover:bg-rose-500/10 hover:text-rose-100",
  },
};

interface Phase {
  range: string;
  title: string;
  body: string;
  tone: PhaseTone;
  scripts: string[];
}

const PHASES: Phase[] = [
  {
    range: "v1–v23",
    title: "Foundations",
    body: "Carrier D₅+A₃+μ₄, the E₈ glue, the α⁻¹ fixed point; the anchor a = (1,1,2) to which {c₃, g_car} reduce — the two axioms become {a, π}.",
    tone: "blue",
    scripts: ["v1_e8_glue.py", "v2_carrier_pascal.py", "v3_em_alpha.py"],
  },
  {
    range: "v24–v53",
    title: "Standard-Model readouts",
    body: "The φ₀ mass ladder, the flavor operators (Q, K, R, L), lepton/quark ratios, hypercharge, the compiler core (5,3).",
    tone: "green",
    scripts: ["v24_quark_ratio_closure.py", "v47_selection_theorem.py"],
  },
  {
    range: "v54–v100",
    title: "Seam = horizon",
    body: "One-sided Gauss–Bonnet c₃ = 1/(8π), the Coxeter-30 cycle, the gapped attractor (2/3)⁶, the frozen registry + look-elsewhere null-MC.",
    tone: "gold",
    scripts: ["v54_seam_horizon_keystones.py", "v56_unique_attractor.py", "v84_frozen_registry.py"],
  },
  {
    range: "v101–v140",
    title: "Horizon + flavor geometry",
    body: "Nariai = anchor, monodromy = W(A₃) = S₄, cusp weights {0, 1/3, 2/3}, H¹ cohomology, the canonical map.",
    tone: "blue",
    scripts: ["v101_horizon_anchor.py", "v117_monodromy_weyl_a3.py", "v140_canonical_map.py"],
  },
  {
    range: "v141–v158",
    title: "R1–R5 + premise (A)",
    body: "Deck selection, the EH mechanism, the No-Unit Theorem, the simple-current (E₈)₁, the free c = 8 fixed point isolated and stable.",
    tone: "green",
    scripts: ["v141_deck_selection.py", "v153_no_unit_theorem.py", "v158_fixed_point_stable.py"],
  },
  {
    range: "v159–v169",
    title: "PyR@TE cross-checks",
    body: "SM gauge/Yukawa/Higgs RGEs confirmed by an independent third-party generator (b₁ = 41/10), Λ_QCD, m_H near-criticality, η_B leptogenesis.",
    tone: "red",
    scripts: ["v159_pyrate_gauge_crosscheck.py", "v164_qcd_scale.py", "v166_higgs_free_seam.py"],
  },
  {
    range: "v170–v174",
    title: "AQFT bridges",
    body: "E₈ slice compression, OS moment/Sugawara, the trace-anomaly seed 4/3, the strong-CP Pfaffian, the Fock readings.",
    tone: "gold",
    scripts: ["v170_diamond_slice_compression.py", "v173_pfaffian_cp_car.py"],
  },
  {
    range: "v175–v181",
    title: "AQFT closure → geometric bedrock",
    body: "Net existence + full-cone reflection positivity [E]; the residual collapses to one premise: the carrier μ₄ clock is the seam's conformal deck.",
    tone: "blue",
    scripts: ["v175_net_existence_full_cone.py", "v181_clock_is_conformal_symmetry.py"],
  },
  {
    range: "v182–v213",
    title: "F_transfer functor + frontier",
    body: "The reviewer residual map; F_transfer as one typed functor (Koide, η_B, axion, m_p/m_e) + the machine wording guard.",
    tone: "red",
    scripts: ["v182_reviewer_residual_map.py", "v213_ftransfer_functor.py"],
  },
  {
    range: "v214–v218",
    title: "Pillowcase + Sheet Diamond",
    body: "The QGEO pillowcase (cross-ratio 2 ⇒ j = 1728), the four marks from Gauss–Bonnet, the Sheet-Diamond axis geometry.",
    tone: "gold",
    scripts: ["v214_seam_pillowcase.py", "v216_marks_gauss_bonnet.py"],
  },
  {
    range: "v219–v237",
    title: "Icosahedral capstone",
    body: "McKay: why {2,3,5}; the CM norms 41/7, CP triality, the Kleinian seam, det K = 1 = the Kitaev E₈ phase — the (2,3,5) Brieskorn singularity generates ALL.",
    tone: "green",
    scripts: ["v219_icosahedral_mckay.py", "v236_brieskorn_capstone.py", "v237_seam_sre_closure.py"],
  },
  {
    range: "v238–v261",
    title: "NCG / Modular Spectral Closure",
    body: "The 96-dim spectral triple, Dirac = covariance induction, cutoff = KMS weight; seam, carrier and E₈ on one K3: one relative object.",
    tone: "blue",
    scripts: ["v258_dirac_covariance_induction.py", "v261_modular_spectral_closure.py"],
  },
  {
    range: "v262–v275",
    title: "Frontier closure + QFT4D fork",
    body: "F_QCD m_p/m_e, the M_ν seesaw, S_pert (Epstein–Glaser, 1-loop + gauge betas), scale over-determination, the QG.AMB roadmap.",
    tone: "red",
    scripts: ["v265_qft4d_fork_freeze.py", "v273_eg_gauge_running.py"],
  },
  {
    range: "v276–v299",
    title: "The Gral: SEAM.EQUIV.01 + Flat-Away",
    body: "Seam = (E₈)₁ at τ=i named as ONE theorem; both routes reduced to one shared input (Flat-Away), the heat a₂ proved + Lean (v295/v296).",
    tone: "gold",
    scripts: ["v286_seam_equivalence_contract.py", "v295_flataway_a2_exact.py"],
  },
  {
    range: "v300–v302",
    title: "Closing arc: residual pinned",
    body: "Flat-Away hard-pinned from the (E₈)₁ Steklov data (v300); Route A invertible via free fermions (v301); the gap = derived 6 ln(3/2) > 0 (v302).",
    tone: "gold",
    scripts: ["v300_flataway_rigid.py", "v302_seam_gap.py"],
  },
  {
    range: "v303–v407",
    title: "Solvers + parameter-free gravity + closure",
    body: "Typed F_transfer solvers (Koide/η_B/m_p-m_e/axion, v371–v375/v402); the parameter-free Einstein equation, full nonlinear (v359); QG.AMB a [C] redundancy (v369).",
    tone: "green",
    scripts: ["v359_grav_nonlinear_einstein.py", "v371_ftransfer_pole.py", "v384_residual_certification.py"],
  },
  {
    range: "v408–v481",
    title: "Certification + external bridges",
    body: "The α-Quillen residual narrowed to the continuum ζ-det face (computed inflow level |C| = 1, det-line moduli; v470/v472); the sheet/deck complement + degree-ladder audits (v430/v431); the entropic-action bridge typed and bounded (v473–v478); the Kronheimer quiver bridge (v479), the four-interval μ₄ geometry (v480), the seesaw carrier-ladder candidate (v481).",
    tone: "blue",
    scripts: [
      "v470_alpha_inflow_level.py",
      "v479_kronheimer_quiver_bridge.py",
      "v480_multilocal_four_interval.py",
      "v481_seesaw_carrier_ladder.py",
    ],
  },
];

export function SuiteTimeline() {
  const { open } = useReproducer();

  return (
    <div className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          The suite timeline — {PHASES.length} phases, live
        </span>
        <span className="text-[10px] font-medium text-slate-400">
          click a script to run it in your browser
        </span>
      </div>

      <ol className="relative m-0 list-none space-y-3 p-5 sm:p-6">
        {/* the timeline spine */}
        <div
          aria-hidden
          className="absolute bottom-8 left-[27px] top-8 w-px bg-slate-700/60 sm:left-[31px]"
        />
        {PHASES.map((p, i) => {
          const tone = TONE[p.tone];
          return (
            <motion.li
              key={p.range}
              initial={{ opacity: 0, x: -10 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.4 }}
              transition={{ duration: 0.35, delay: Math.min(i, 6) * 0.03 }}
              className="relative flex items-start gap-4"
            >
              <span
                aria-hidden
                className={cn(
                  "relative z-10 mt-4 h-3 w-3 flex-none rounded-full ring-4 ring-slate-950",
                  tone.dot,
                )}
              />
              <div className={cn("min-w-0 flex-1 rounded-xl border p-4", tone.ring)}>
                <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1">
                  <span className={cn("font-mono text-xs font-semibold", tone.text)}>
                    {p.range}
                  </span>
                  <h4 className="font-serif text-base font-semibold text-slate-50">
                    {p.title}
                  </h4>
                </div>
                <p className="mt-1.5 break-words text-xs leading-relaxed text-slate-300">
                  {p.body}
                </p>
                <div className="mt-2.5 flex flex-wrap gap-1.5">
                  {p.scripts.map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => open(s)}
                      className={cn(
                        "group inline-flex max-w-full items-center gap-1.5 rounded-md border border-slate-700/50 bg-slate-950/60 px-2 py-0.5 font-mono text-[10px] text-slate-300 transition-colors",
                        tone.chip,
                      )}
                    >
                      <FileCode2 size={11} className="flex-none group-hover:hidden" aria-hidden />
                      <Play size={11} className="hidden flex-none group-hover:inline" aria-hidden />
                      <span className="min-w-0 break-all text-left">{s}</span>
                    </button>
                  ))}
                </div>
              </div>
            </motion.li>
          );
        })}
      </ol>

      <p className="border-t border-slate-800/60 px-5 py-4 text-xs leading-relaxed text-slate-400">
        The two axioms <span className="font-mono">c₃ = 1/(8π)</span> and{" "}
        <span className="font-mono">g_car = 5</span> are not free knobs: they reduce to the
        single parabolic anchor <span className="font-mono">a = (1,1,2)</span> plus π, and{" "}
        <span className="font-mono">g_car = 5</span> is a bootstrap fixed point (forced three
        ways, Lean-formalised). The full script→check map follows in the index below.
      </p>
    </div>
  );
}

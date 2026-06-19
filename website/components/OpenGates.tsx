"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { Math } from "./Math";
import { FTransferDynamics } from "./FTransferDynamics";

interface Gate {
  tag: string;
  marker: string;
  title: string;
  body: string;
  formula?: string;
  tone: string;
}

const GATES: Gate[] = [
  {
    tag: "Interface 1",
    marker: "[O]",
    title: "v_geo — the one scale anchor",
    body: "The quark mass ratios are closed (Readout Rigidity, c_u/c_d = 55/117) and the selector triangle pins R columnwise (the dual pair (d,n), v136/v139). Only the absolute amplitude scale v_geo remains — and the No-Unit theorem (v153) proves a dimensionless compiler cannot make an absolute scale. So this is not a gap but an irreducible metrology primitive, the same one as gravity's 1/G. Sharper still (v274): the anchor is over-determined — Newton's G and the compiler's dark-energy prediction (ρ_Λ/M̄⁴ = (3/4π²)e^{−2α⁻¹}) give the same reduced Planck mass to 0.11% (conditional on the Λ-branch readout; the gravity route is unconditional — red-team rt_F) — so it is the gravitational unit, not a missing derivation; and because the seam is a conformal c=8 CFT (scale-invariant by construction), 'no derivable absolute scale' is a theorem, not a gap. The absolute neutrino scale (v272) is the same single anchor. (Historical label: U_wall.)",
    formula: "\\det R = 8,\\ \\operatorname{Spec}(Q_+)=\\{1,2,3\\};\\ U_{\\mathrm{point}} \\to v_{\\mathrm{geo}}",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Interface 2",
    marker: "[E] target · [O] seam",
    title: "G_net — the metric-sector inclusion",
    body: "The target object is closed: (D₅)₁⊗(A₃)₁⋊μ₄ ≅ (E₈)₁ (Jones index 4 = |μ₄|, holomorphic c = 8; v154), with net existence and full-cone reflection positivity discharged to [E] on the 2¹⁶-dim Fock space (v175), R + R² heat-kernel grounded and the IR sector gap-decoupled (Δ_eff = 1.648 > 0). Only the physical coupling of the raw seam to that object is open — the single premise QGEO.SYM.01: the carrier μ₄ clock IS the seam's conformal deck. That is not a gap but TFPT's one fundamental postulate (the role 'c = const' plays in relativity), driven to its sharpest non-circular form (a μ₄-invariant quasi-free seam state, v198/v201) and Lean-formalised below the premise. As the synthesis above shows, this gate, the carrier P2, Target A and the entire boundary-QFT layer (the Modular Spectral Closure, v258–v261: Dirac = covariance induction, cutoff = KMS weight, seam/carrier/E₈ on one K3) are one condition — and in Chern-Simons language it is the single integer step 'det K = 1' (v234/v235). (Historical label: G_metric.)",
    formula: "[\\,(E_8)_1 : (D_5)_1\\times(A_3)_1\\,] = 4 = |\\mu_4| \\Rightarrow \\text{holomorphic } c = 8",
    tone: "border-amber-400/30 bg-amber-500/5",
  },
  {
    tag: "Interface 3",
    marker: "[C]",
    title: "F_transfer — one typed functor, four interfaces",
    body: "Not a bag of open topics but one functor F_transfer = F_observable ∘ F_threshold ∘ F_RG (standard physics fed TFPT source data), with exactly four interfaces: F_pole (Koide 53/54, exact readout [E], pole reading [C], v183), F_Boltzmann (η_B via the scalaron-decuple A_Λ = 10, v212), F_relic (axion, the θ_i = 3π/5 spine branch, v211), F_QCD (m_p/m_e via Λ_QCD, b₃ = −7, lattice [O]). A machine guard (v187) forbids ever promoting these to a primitive [E] compiler prediction; the functor contract CONTRACT.F.01 (v213) pins four structural axioms (μ₄-deck equivariance, Plücker preservation, positivity, explicit external modules). A consolidation, not a closure. (Historical label: F_frontier.)",
    tone: "border-slate-500/30 bg-slate-500/5",
  },
];

const RESIDUAL: { label: string; marker: string; blurb: string; tone: string }[] = [
  {
    label: "v_geo",
    marker: "[O]",
    blurb: "One dimensionful scale — irreducible by the No-Unit theorem and over-determined (gravity = dark energy = M̄_Pl to 0.11%, v274); the same primitive as gravity's 1/G.",
    tone: "from-amber-500/15 to-amber-500/[0.03] border-amber-400/30",
  },
  {
    label: "G_net",
    marker: "[E] target · [O] seam",
    blurb: "Metric inclusion: the (E₈)₁ target is closed; only the seam coupling (QGEO.SYM.01) is open.",
    tone: "from-amber-500/15 to-amber-500/[0.03] border-amber-400/30",
  },
  {
    label: "F_transfer",
    marker: "[C]",
    blurb: "One typed functor, four downstream interfaces — bridges, never primitive outputs.",
    tone: "from-slate-500/15 to-slate-500/[0.03] border-slate-500/30",
  },
];

/** The three provably-equivalent faces of the single structural condition (v234). */
const FACES: { face: string; statement: string }[] = [
  { face: "AQFT", statement: "boundary net holomorphic (μ-index 1)" },
  { face: "Geometry", statement: "seam link a homology 3-sphere (Γ perfect ⟺ 2I)" },
  { face: "Rep theory", statement: "exactly one 1-dim irrep (no abelian charge)" },
];

function ResidualTreemap() {
  return (
    <figure
      className="mt-8 rounded-2xl border border-slate-700/40 bg-slate-950/30 p-4 sm:p-5"
      aria-label="The complete open residual: v_geo, G_net and F_transfer"
    >
      <figcaption className="mb-3 text-center font-mono text-sm text-slate-300">
        Rest = <span className="text-amber-200">v_geo</span> ⊕{" "}
        <span className="text-amber-200">G_net</span> ⊕{" "}
        <span className="text-slate-200">F_transfer</span>
      </figcaption>
      <div className="grid gap-3 sm:grid-cols-3">
        {RESIDUAL.map((r) => (
          <div
            key={r.label}
            className={`flex flex-col gap-2 rounded-xl border bg-gradient-to-br p-4 ${r.tone}`}
          >
            <div className="flex items-center justify-between gap-2">
              <span className="font-mono text-base font-semibold text-slate-50">
                {r.label}
              </span>
              <span className="rounded-full bg-slate-900/60 px-2 py-0.5 font-mono text-[10px] font-semibold text-slate-300 ring-1 ring-slate-600/40">
                {r.marker}
              </span>
            </div>
            <p className="text-xs leading-relaxed text-slate-300">{r.blurb}</p>
          </div>
        ))}
      </div>
    </figure>
  );
}

/**
 * The single closing condition (v234/v235): the whole structural residual is one
 * condition with three provably-equivalent faces, all forcing E₈. Surfacing this
 * compactly is the headline — the wall of QGEO history now lives in the paper.
 */
function ClosingCondition() {
  return (
    <figure className="mt-8 rounded-2xl border border-emerald-400/25 bg-emerald-500/[0.04] p-5 sm:p-6">
      <figcaption className="text-sm font-semibold text-emerald-200">
        The structural residual is{" "}
        <span className="underline decoration-emerald-400/40 underline-offset-4">
          one condition
        </span>{" "}
        — the seam carries no nontrivial abelian sector
      </figcaption>
      <p className="mt-2 text-sm leading-relaxed text-slate-300">
        The metric inclusion (G_net), the carrier P2 and red-team Target A are not
        three gates but three faces of a single condition — and all three force E₈:
      </p>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        {FACES.map((f) => (
          <div
            key={f.face}
            className="rounded-xl border border-slate-700/40 bg-slate-950/40 p-3"
          >
            <div className="font-mono text-[11px] font-semibold uppercase tracking-wider text-emerald-300/80">
              {f.face}
            </div>
            <div className="mt-1 text-xs leading-relaxed text-slate-300">
              {f.statement}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/50 p-2.5">
        <Math
          block
          plain="The seam has exactly one one-dimensional representation (a trivial abelianisation, a homology-sphere link) if and only if it is E₈ — equivalently, the K-matrix has determinant one."
        >
          {"\\#(\\text{1-dim irreps}) = |\\Gamma^{\\mathrm{ab}}| = |H_1(S^3/\\Gamma)| = 1 \\iff E_8 \\iff |\\det K| = 1"}
        </Math>
      </div>
      <p className="mt-3 text-xs leading-relaxed text-slate-400">
        In abelian Chern–Simons language the boundary is holomorphic ⟺ det K = 1, and the
        extension tower D₅⊕A₃ (det 16) → D₈ (det 4) → E₈ (det 1) is anyon condensation —
        the Kitaev E₈ quantum-Hall state. So the one open analytic step is sharply located:{" "}
        <span className="text-slate-300">
          the free RP seam condenses the order-|μ₄| Lagrangian glue (det → 1)
        </span>{" "}
        = the deck premise QGEO.SYM.01 (v234/v235).
      </p>
      <p className="mt-3 rounded-lg border border-emerald-400/15 bg-emerald-500/[0.03] p-3 text-xs leading-relaxed text-slate-300">
        <span className="font-semibold text-emerald-200">And the whole boundary QFT collapses onto the same premise</span>{" "}
        (the <em>Modular Spectral Closure</em>, v258–v261): the finite Dirac is a covariance induction of the
        seam KMS state ([D_F] = [D_Σ]⊗[K_car], v258), the spectral-action cutoff <em>is</em> that KMS weight
        (f₂/f₀ = 1, v259), and the seam, the carrier-16 and E₈ live on one Kummer/K3 surface
        (H²(K3) = U³⊕E₈(−1)², v260). The assembly certificate (v261) pins one number 4 = [B:A] = |μ₄| = 2χ =
        |(ℤ/2)²| (index = marks = fixed points = glue order), one carrier-16 and one gap 6·log(3/2) — so Dirac,
        cutoff, gauging, glue and orientability are readouts of the one seam state. The boundary QFT is one
        relative object closed modulo QGEO.SYM.01 and adds <span className="text-emerald-200">no new open item</span>;
        the ambient QG measure is gap-decoupled (Δ_eff = 1.648 &gt; 0) and kept separate by design.
      </p>
      <p className="mt-3 rounded-lg border border-slate-700/40 bg-slate-950/40 p-3 text-xs leading-relaxed text-slate-300">
        <span className="font-semibold text-slate-100">The 4D perturbative S-matrix is now constructible</span>{" "}
        (S_pert, v269/v271/v273): the spectral-action interaction is power-counting renormalizable, so by the
        Epstein–Glaser theorem the perturbative S(g) exists order by order (one log counterterm per coupling, loop
        factor 1/(16π²)), giving the SM one-loop β-coefficients (b₁,b₂,b₃) = (41/10, −19/6, −7) from the carrier
        content. This is unitary for the <span className="text-slate-100">matter+gauge</span> sector only — the
        R²/Weyl² gravity sub-sector is renormalizable but non-unitary (the Stelle ghost; red-team rt_F), which is
        exactly why the one genuine structural frontier is the{" "}
        <span className="text-amber-200">nonperturbative</span> ambient measure QG.AMB.01, which now carries an
        explicit roadmap (v275): Tier A gap-decoupled, Tier B reduced to the holomorphic (E₈)₁ boundary net —
        reduced, not closed. Sharper still (v282): the flat τ=i geometry (QGEO.SYM.01) and the (E₈)₁ holomorphy
        (QG.AMB.01) are two faces of one object — χ_E8(i) = j(i)^{1/3} = 12, so τ=i is at once the order-4 CM
        point and the (E₈)₁ modulus — collapsing the two open obligations to one.
      </p>
      <p className="mt-3 rounded-lg border border-emerald-400/15 bg-emerald-500/[0.03] p-3 text-xs leading-relaxed text-slate-300">
        <span className="font-semibold text-emerald-200">That one statement is now a single named theorem</span>{" "}
        — the Seam Equivalence Theorem (SEAM.EQUIV.01, v286): <em>the raw RP seam state is the holomorphic
        (E₈)₁ boundary net at τ=i</em>. The contract concentrates the whole open structure on this one arrow and
        enforces an <span className="text-slate-100">import firewall</span> so its two proof routes can never feed
        each other (no "E₈ smuggled into the geometry and pulled back out"). Both routes are then attacked:{" "}
        <span className="text-slate-100">Route A</span> (AQFT, v287) reduces the theorem to <em>one</em> standard
        import — "invertible Gaussian bulk ⇒ single-sector boundary" (4/5 lemmas discharged); and{" "}
        <span className="text-slate-100">Route B</span> (DtN, v288) <em>proves</em> the full-L² lift of the
        subprincipal ℤ₄ block-diagonality, shrinking the residual to the single sharper question:{" "}
        <span className="text-slate-300">why is the raw seam subprincipal term mark-local?</span> — now
        decomposed (v289) into a 5-lemma chain whose <em>only</em> open link is Flat-Away (RP + gap + 4 marks
        ⇒ curvature vanishes away from the marks), 4/5 discharged. That is the best current attack; Route A's
        one standard import is itself citable (Kitaev/Freed–Hopkins, Müger/KLM, Kawahigashi–Longo) modulo the
        same seam-bulk invertibility — so both routes meet at one geometric input, no circularity.
      </p>
      <p className="mt-3 rounded-lg border border-slate-700/40 bg-slate-950/40 p-3 text-xs leading-relaxed text-slate-300">
        <span className="font-semibold text-slate-100">Honest red-team (v290):</span> ℤ₄-invariance is{" "}
        <em>not</em> mark-locality — a smooth ε·cos(4θ) off-mark curvature passes the v288 commutator yet
        shifts the DtN spectrum and heat trace. So the commutator is necessary, not sufficient; the modulus is
        excluded by the spectral data (the KMS weight and (E₈)₁ character), which is exactly why{" "}
        <span className="font-mono">Flat-Away</span> is now named as its own mini-theorem (v291, FLATAWAY.RP.01)
        with three independent attack routes — spectral-rigidity, heat-kernel and RP-energy/Troyanov (the flat
        seam is the <em>unique</em> spectral match of the smooth ℤ₄ family). Closing any one closes Route B.
        All three are now carried to a precise reduction: the heat-trace deviation is a positive-definite
        quadratic form ⟹ fix one coefficient a₂ (v292); the spectral-mismatch Hessian over the full smooth-ℤ₄
        space is positive-definite ⟹ flat is a strict isolated minimum (v293); and Troyanov uniqueness makes
        the flat cone metric the unique strictly-convex curvature-energy minimiser (v294). The heat route is
        now <em>exact</em>, not numerical (v295): convexity of the heat trace Λ↦Tr exp(−tΛ) plus the
        Gauss-Bonnet zero-mean condition makes the flat seam the global minimum (ΔTr ≥ 0, = 0 iff f = 0), and
        the Δ = 0 ⟺ flat step is
        machine-formalised in Lean (FORM.FLATAWAY.01, axiom-clean); the a₂ coefficient is now in closed form
        (v296). Route A&rsquo;s import is likewise a citable theorem stack (Kitaev/Freed–Hopkins → Müger/KLM →
        Conway–Sloane, v297) modulo the same input. The three converge on one external selection principle for
        the flat metric.
      </p>
      <p className="mt-3 text-sm leading-relaxed text-slate-300">
        <span className="font-semibold text-slate-100">Closing arc (v300–v302) — the shared fact pinned, no
        undischarged TFPT-internal assumption left.</span> Flat-Away is hardened from a <em>soft</em> minimum to a{" "}
        <em>discrete</em> degeneracy obstruction (any smooth off-mark mode splits a doubly-degenerate Steklov
        level, changing the spectral multiset), and its pin is <em>derived</em> from the (E₈)₁ integer-weight
        character E₄/η⁸ = q<sup>−1/3</sup>(1 + 248q + …) via 2d Steklov rigidity — so Route B&rsquo;s residual{" "}
        <em>coincides with</em> Route A&rsquo;s rationality (v300). Route A&rsquo;s one open hypothesis (
        <span className="font-mono">the quasi-free bulk is invertible</span>) is then discharged by the
        free-fermion classification: a gapped 16-Majorana (c = 8) Gaussian bulk is automatically invertible
        (#anyons = |det K<sub>E₈</sub>| = 1; the gauged D₈ = SO(16) contrast has det = 4) (v301). And the single
        spectral input that remains — <span className="font-mono">the quasi-free bulk is gapped</span> — is the{" "}
        <em>derived Recovery gap</em> Δ = 6·ln(3/2) ≈ 2.43 &gt; 0 of the frozen transfer spectrum
        {" "}{`{1,(2/3)⁶,(1/3)⁶}`} (margin Δ − 31/(4π²) ≈ 1.65 &gt; 0); by Osterwalder–Schrader / quasi-free
        clustering a transfer gap <em>is</em> a bulk mass gap (v302). <span className="font-semibold text-slate-100">
        Net:</span> SEAM.EQUIV.01 stays open (not machine-proved end-to-end), but its entire residual is now a
        composition of standard cited theorems (OS/clustering, Kitaev free-fermion, the v297 AQFT stack) over
        established TFPT facts — no undischarged TFPT-internal assumption remains.
      </p>
      <p className="mt-3 rounded-lg border border-slate-700/40 bg-slate-950/40 p-3 text-xs leading-relaxed text-slate-300">
        <span className="font-semibold text-slate-100">4D-QFT fork policy</span> (frozen decision tree, v265):
        Boundary QFT — complete modulo QGEO.SYM.01. Ambient QG — separate. <span className="text-amber-200">4D
        GUT — not claimed by default</span> (E₈ is the audit hull, not a 4D gauge group; SM-only unification
        is killed). Optional UV branch — carrier-native Pati-Salam, falsifiable by thresholds and proton
        decay (E₈-allowed content only, no 126, sin²θ_W = 3/8). Not an open ambiguity.
      </p>
    </figure>
  );
}

/**
 * Trust section: what is still open. The whole structural residual collapses to one
 * condition (no abelian sector ⟹ E₈), plus the one irreducible scale and the typed
 * transfer functor — surfaced near the top as a credibility signal, not a footnote.
 */
export function OpenGates() {
  return (
    <section
      id="open-gates"
      className="relative scroll-mt-20 py-20 sm:py-24"
      aria-labelledby="open-gates-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Honest boundaries"
          title="What is still open?"
          description="After the compiler closure the live residual is just three named items — Rest = v_geo ⊕ G_net ⊕ F_transfer. Sharper still: the structural part (the metric inclusion and the carrier P2) is one condition that forces E₈ three equivalent ways — and the entire boundary-QFT layer (Dirac, cutoff, gauging, glue) now collapses onto that same condition via the Modular Spectral Closure. Nothing is hidden, nothing is overclaimed."
        />

        <ClosingCondition />

        <ResidualTreemap />

        <div className="mt-10 grid gap-5 lg:grid-cols-3">
          {GATES.map((g, i) => (
            <motion.article
              key={g.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.05 }}
              transition={{ duration: 0.55, delay: i * 0.08 }}
              className={`flex flex-col rounded-2xl border p-6 ${g.tone}`}
            >
              <div className="flex items-center gap-2">
                <span className="rounded-full border border-slate-600/40 bg-slate-900/50 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-slate-300">
                  {g.tag}
                </span>
                <span className="rounded-full bg-rose-500/15 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-200 ring-1 ring-rose-400/30">
                  {g.marker}
                </span>
              </div>
              <h3 className="mt-3 font-serif text-base font-semibold text-slate-50">
                {g.title}
              </h3>
              <p className="mt-2 flex-1 text-sm leading-relaxed text-slate-300">
                {g.body}
              </p>
              {g.formula && (
                <div className="mt-3 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/40 p-2.5">
                  <Math block>{g.formula}</Math>
                </div>
              )}
            </motion.article>
          ))}
        </div>

        <FTransferDynamics />

        <div className="mt-6 flex flex-wrap items-center gap-3 text-sm text-slate-400">
          <span>The gates are written up as numbered research contracts.</span>
          <Link
            href="/papers/research-contracts"
            className="inline-flex items-center gap-1.5 font-semibold text-blue-300 transition-colors hover:text-blue-200"
          >
            Read the contracts
            <ArrowRight size={14} aria-hidden />
          </Link>
        </div>
      </div>
    </section>
  );
}

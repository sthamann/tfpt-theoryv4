"use client";

import { motion, useInView } from "motion/react";
import { useRef } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Math } from "./Math";
import { SectionHeader } from "./SectionHeader";

type StatusKind =
  | "operational"
  | "theorem-core"
  | "decoder"
  | "conditional"
  | "bridge"
  | "downstream";

interface StepNode {
  id: string;
  step: number | string;
  label: string;
  formula: string;
  input: string;
  fixed: string;
  notClaimed: string;
  fail: string;
  status: StatusKind;
}

const STATUS_META: Record<
  StatusKind,
  { label: string; tone: string; ring: string; chip: string }
> = {
  operational: {
    label: "Axiom — declared input",
    tone: "from-slate-400 to-slate-500",
    ring: "ring-slate-400/30",
    chip: "bg-slate-500/15 text-slate-200",
  },
  "theorem-core": {
    label: "Lattice / identity",
    tone: "from-blue-500 to-violet-500",
    ring: "ring-blue-400/40",
    chip: "bg-blue-500/15 text-blue-200",
  },
  decoder: {
    label: "Readout",
    tone: "from-violet-500 to-fuchsia-500",
    ring: "ring-violet-400/40",
    chip: "bg-violet-500/15 text-violet-200",
  },
  conditional: {
    label: "Open / frontier",
    tone: "from-orange-500 to-red-500",
    ring: "ring-orange-400/40",
    chip: "bg-orange-500/15 text-orange-200",
  },
  bridge: {
    label: "Bridge readout",
    tone: "from-emerald-500 to-teal-500",
    ring: "ring-emerald-400/40",
    chip: "bg-emerald-500/15 text-emerald-200",
  },
  downstream: {
    label: "Geometry channel",
    tone: "from-fuchsia-500 to-pink-500",
    ring: "ring-fuchsia-400/40",
    chip: "bg-fuchsia-500/15 text-fuchsia-200",
  },
};

const TRUNK_BEFORE: StepNode[] = [
  {
    id: "axioms",
    step: 1,
    label: "Two axioms",
    formula: "c_3 = \\tfrac{1}{8\\pi}, \\qquad g_{\\mathrm{car}} = 5",
    input: "Declared (P1 Gauss–Bonnet-hardenable, P2 Lean-formalised)",
    fixed: "The seam constant and the five-slot carrier — the only structural inputs",
    notClaimed: "No SM gauge group, no families, no α inserted by hand",
    fail: "No reflection-positive seam, or the wrong family/charge lattice",
    status: "operational",
  },
  {
    id: "atoms",
    step: 2,
    label: "The two atoms",
    formula: "C^+ = D_5\\ (16), \\qquad \\mathbb{P}^1\\setminus\\mu_4 = A_3",
    input: "The carrier g_car = 5 and the four-puncture family geometry",
    fixed: "The D₅ half-spinor (dim 16, hypercharge Y) and the A₃ family geometry (N_fam = 3)",
    notClaimed: "Not yet E₈ — the atoms are intermediate products of the inputs",
    fail: "Group/matter mismatch, or the wrong family multiplicity",
    status: "theorem-core",
  },
  {
    id: "glue",
    step: 3,
    label: "The μ₄ glue ⇒ E₈",
    formula: "E_8 = (D_5 \\oplus A_3) + \\mu_4",
    input: "D₅, A₃ with the common discriminant ℤ₄",
    fixed: "240 = 16·5·3 roots, 248 = 240 + 8; q(D₅)+q(A₃) = 5/4+3/4 = 2",
    notClaimed: "E₈ is the unimodular audit hull, not a physical gauge group",
    fail: "Not even-unimodular, or the glue norms do not sum to the root norm 2",
    status: "theorem-core",
  },
];

const DECODERS: StepNode[] = [
  {
    id: "decoder-sm",
    step: "4a",
    label: "Standard Model — Engine 1",
    formula: "N_{\\mathrm{fam}}=3,\\ \\Omega_{\\mathrm{adm}}=48,\\ b_1=\\tfrac{41}{10}",
    input: "E₈ projection + carrier traces",
    fixed:
      "The gauge group, 3 families, hypercharge, b₁ = 41/10, and the residue matrix R (det 8)",
    notClaimed: "No absolute quark amplitude scale (the v_geo anchor)",
    fail: "Hierarchy mismatch, or a robust fourth generation",
    status: "decoder",
  },
  {
    id: "decoder-constants",
    step: "4b",
    label: "Constants — Engine 2",
    formula: "\\alpha^{-1} = 137.0359992,\\quad \\theta_{\\mathrm{eff}} = 0",
    input: "The seed u = φ₀ and the abelian coefficient 41 = 10 b₁",
    fixed:
      "α⁻¹, the Cabibbo angle λ_C, sin²θ₁₃, β_rad, and the strong-CP null",
    notClaimed: "Not the dimensionful EW/QCD masses (those sit on the RG scheme layer)",
    fail: "No root or a second root of F_U(1)(α), or a robust nonzero neutron EDM",
    status: "decoder",
  },
  {
    id: "decoder-cosmos",
    step: "4c",
    label: "Gravity & cosmos — Engine 2",
    formula: "G_{ab} + \\Lambda g_{ab} = c_3^{-1} T_{ab}",
    input: "The seam constant via the geometry channel (entanglement first law + R + R²)",
    fixed:
      "Parameter-free Einstein equation Gₐᵦ+Λgₐᵦ=c₃⁻¹Tₐᵦ, both coefficients fixed (v358/v359); scalaron mass 3.06×10¹³ GeV, n_s = 0.965, r ≈ 0.004, Λ ∼ e⁻²ᵅ⁻¹, H₀ ∼ √Λ",
    notClaimed: "The absolute dark-energy density is a typed cosmology interface",
    fail: "A robust r ≳ 0.01, or a robust w ≠ −1",
    status: "downstream",
  },
];

const TRUNK_AFTER: StepNode[] = [
  {
    id: "ladder",
    step: 5,
    label: "The φ₀-ladder & flavor matrix",
    formula:
      "\\hat m_{f,j} = \\tfrac{v_{\\mathrm{geo}}}{\\sqrt2}\\,\\lambda_Y^{\\,L_{f,j}}\\,\\Lambda_{f,j}",
    input: "The residue matrix R and the seed φ₀",
    fixed:
      "All nine masses, CKM, the PMNS skeleton; the solar angle sin²θ₁₂ = 1/3 − φ₀/2",
    notClaimed: "Quark ratios closed; the absolute quark scale is the U_point anchor",
    fail: "The lepton φ₀-ladder mismatches the observed charged-lepton hierarchy",
    status: "bridge",
  },
  {
    id: "bootstrap",
    step: 6,
    label: "The bootstrap loop",
    formula: "E_8\\text{ closure} \\Rightarrow g_{\\mathrm{car}}{=}5,\\ \\ 8 = \\operatorname{rank}E_8",
    input: "The E₈ closure fed back to the inputs",
    fixed:
      "The two inputs are re-derived — the discrete core is overdetermined, not fitted; only π stays free",
    notClaimed: "Not creation from nothing — two inputs remain",
    fail: "g_car = 5 not forced three ways, or the reverse glue μ² − 5μ + 4 = 0 does not pick μ = 4",
    status: "theorem-core",
  },
  {
    id: "qft-closure",
    step: 7,
    label: "Boundary QFT — the Modular Spectral Closure",
    formula:
      "\\mathsf{TFPT}_{\\mathrm{QFT}} = (\\mathcal{A}_\\Sigma, \\omega_\\Sigma, \\Delta_\\Sigma, \\rho, A_F, H_F, D_F, J, \\gamma, S_{\\mathrm{rel}})",
    input: "The seam KMS state + the 96-dim carrier finite spectral triple",
    fixed:
      "One relative object: D_F = covariance induction of the seam state (v258), cutoff = the KMS weight ⇒ f₂/f₀ = 1 (v259), seam + carrier-16 + E₈ on one Kummer/K3 (v260); cross-checked 4 = [B:A] = |μ₄| = 2χ = |(ℤ/2)²| (v261)",
    notClaimed:
      "Closed modulo cited theorems via the keystone SEAM.EQUIV.01 (QGEO.SYM.01 is its corollary, v335; extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O]); the ambient QG measure is discharged as a redundancy [C] (v369+v379)",
    fail: "An invariant disagrees across the round (index ≠ marks, two carrier-16s, or two different gaps)",
    status: "bridge",
  },
  {
    id: "residual",
    step: 8,
    label: "The residual: two gates + interfaces",
    formula:
      "\\text{Rest} = (U_{\\mathrm{wall}}) \\oplus (G_{\\mathrm{metric}}) \\oplus (F_{\\mathrm{frontier}})",
    input: "The compiler closure",
    fixed:
      "One flavor wall-selection (v_geo, [O]); the ambient quantum-gravity measure now discharged as a redundancy [C] (v369+v379; the local field equation is itself parameter-free, v358/v359); and a set of typed runnable frontier solvers (F_transfer, v371–v375) — the whole boundary-QFT layer collapses onto the G_metric keystone (step 7), closed modulo cited theorems, adding no new open item",
    notClaimed: "No strict physical TOE certified end-to-end (the keystone SEAM.EQUIV.01 is closed only modulo a cited published theorem, v336 — extension leg crossed-product certified, v469; stays [O] — and v_geo stays the one unit). The ambient measure G6 is not an open hole — it is discharged as a redundancy [C]",
    fail: "A gate's closing theorem asserted before its lemma chain completes",
    status: "conditional",
  },
];

interface StepCardProps {
  node: StepNode;
  delay: number;
}

function StepCard({ node, delay }: StepCardProps) {
  const meta = STATUS_META[node.status];
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.05 }}
      transition={{ duration: 0.55, delay, ease: [0.16, 1, 0.3, 1] }}
      className={`group glass relative overflow-hidden rounded-2xl ring-1 ring-slate-700/40 transition-shadow hover:ring-slate-500/50`}
    >
      <div
        aria-hidden="true"
        className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${meta.tone} opacity-70`}
      />
      <div className="px-5 py-5 sm:px-6 sm:py-6">
        <div className="flex flex-wrap items-center gap-2">
          <span
            className={`flex h-8 min-w-8 flex-none items-center justify-center rounded-full bg-gradient-to-br ${meta.tone} px-2 font-mono text-xs font-semibold text-white shadow-md`}
          >
            {node.step}
          </span>
          <h3 className="font-serif text-lg font-semibold text-slate-50">
            {node.label}
          </h3>
          <span
            className={`ml-auto rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest ${meta.chip} ring-1 ring-inset ring-current/20`}
          >
            {meta.label}
          </span>
        </div>
        <div className="mt-3 overflow-x-auto formula-scroll">
          <Math block>{node.formula}</Math>
        </div>
        <dl className="mt-4 grid grid-cols-1 gap-3 text-xs sm:grid-cols-2">
          <Cell label="Input" body={node.input} />
          <Cell label="What is fixed" body={node.fixed} highlight />
          <Cell label="Not claimed here" body={node.notClaimed} />
          <Cell label="How it can fail" body={node.fail} warn />
        </dl>
      </div>
    </motion.div>
  );
}

function Cell({
  label,
  body,
  highlight,
  warn,
}: {
  label: string;
  body: string;
  highlight?: boolean;
  warn?: boolean;
}) {
  return (
    <div
      className={`rounded-lg border p-3 ${
        highlight
          ? "border-emerald-400/25 bg-emerald-500/5"
          : warn
            ? "border-orange-400/25 bg-orange-500/5"
            : "border-slate-700/40 bg-slate-950/40"
      }`}
    >
      <dt
        className={`text-[10px] font-semibold uppercase tracking-widest ${
          highlight
            ? "text-emerald-300/85"
            : warn
              ? "text-orange-300/85"
              : "text-blue-300/80"
        }`}
      >
        {label}
      </dt>
      <dd className="mt-1 leading-relaxed text-slate-300">{body}</dd>
    </div>
  );
}

function Connector({ label }: { label?: string }) {
  return (
    <div className="relative flex flex-col items-center" aria-hidden="true">
      <div className="h-8 w-px bg-gradient-to-b from-slate-600/40 via-slate-500/30 to-slate-600/40" />
      {label && (
        <span className="mt-1 rounded-full bg-slate-900/60 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-slate-400 ring-1 ring-slate-700/40">
          {label}
        </span>
      )}
    </div>
  );
}

export function ReconstructionChain() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, amount: 0.05 });

  return (
    <section
      id="chain"
      className="relative scroll-mt-20 py-24 sm:py-32"
      aria-labelledby="chain-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="The compiler pipeline"
          title="From two axioms to the observables"
          description="TFPT is a directed acyclic graph: two axioms at the source, the E₈ compiler in the middle, the observables as sinks. The compiler factorises into two engines — a discrete closure (from g_car) and a boundary dressing (from c₃) — that branch into three readouts, and the bootstrap loop feeds the output back to fix the inputs. On top, the boundary QFT assembles into one relative object — the Modular Spectral Closure — reduced to a single seam premise."
        />

        <div ref={ref} className="relative mx-auto mt-14 max-w-5xl space-y-3">
          {TRUNK_BEFORE.map((n, i) => (
            <div key={n.id}>
              <StepCard node={n} delay={i * 0.06} />
              {i < TRUNK_BEFORE.length - 1 ? <Connector /> : null}
            </div>
          ))}

          <Connector label="Three readouts (two engines)" />

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative grid gap-4 lg:grid-cols-3"
          >
            <div
              aria-hidden="true"
              className="pointer-events-none absolute inset-x-8 top-0 hidden h-px bg-gradient-to-r from-transparent via-violet-400/40 to-transparent lg:block"
            />
            {DECODERS.map((n, i) => (
              <StepCard key={n.id} node={n} delay={i * 0.08} />
            ))}
          </motion.div>

          <Connector label="Readouts feed the ladder, the bootstrap and the residual" />

          {TRUNK_AFTER.map((n, i) => (
            <div key={n.id}>
              <StepCard node={n} delay={i * 0.06} />
              {i < TRUNK_AFTER.length - 1 ? <Connector /> : null}
            </div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mx-auto mt-12 max-w-5xl rounded-2xl border border-amber-400/20 bg-amber-500/5 px-6 py-5 text-sm text-amber-100/90"
        >
          <strong className="font-semibold text-amber-200">Status discipline.</strong>
          <span className="ml-2 text-amber-100/85">
            The diagram is a status map of the dependency DAG, not a claim that
            all displayed outputs share the same grade. Axioms, lattice/identity
            steps, readouts, the bridge ladder and the open residual are all
            visibly distinct — and each carries its own &ldquo;not claimed
            here&rdquo; and &ldquo;how it can fail&rdquo; rows. The machine-checked
            ledger is the single source of truth.
          </span>
          <div className="mt-4">
            <Link
              href="/verification"
              className="inline-flex items-center gap-1.5 rounded-full border border-amber-400/30 bg-amber-500/10 px-4 py-2 text-xs font-semibold text-amber-100 transition-colors hover:bg-amber-500/20"
            >
              Explore the interactive dependency graph
              <ArrowRight size={13} aria-hidden />
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

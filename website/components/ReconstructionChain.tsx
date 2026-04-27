"use client";

import { motion, useInView } from "motion/react";
import { useRef } from "react";
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
    label: "Operational primitive",
    tone: "from-slate-400 to-slate-500",
    ring: "ring-slate-400/30",
    chip: "bg-slate-500/15 text-slate-200",
  },
  "theorem-core": {
    label: "Theorem core",
    tone: "from-blue-500 to-violet-500",
    ring: "ring-blue-400/40",
    chip: "bg-blue-500/15 text-blue-200",
  },
  decoder: {
    label: "Decoder",
    tone: "from-violet-500 to-fuchsia-500",
    ring: "ring-violet-400/40",
    chip: "bg-violet-500/15 text-violet-200",
  },
  conditional: {
    label: "Conditional closure",
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
    label: "Downstream interface",
    tone: "from-fuchsia-500 to-pink-500",
    ring: "ring-fuchsia-400/40",
    chip: "bg-fuchsia-500/15 text-fuchsia-200",
  },
};

const TRUNK_BEFORE: StepNode[] = [
  {
    id: "seed",
    step: 1,
    label: "Operational seed",
    formula: "\\mathfrak{S}_{\\min}",
    input: "Pre-physical primitive",
    fixed: "The minimal admissible seed of the framework",
    notClaimed: "No carrier, no Standard Model, no α",
    fail: "Misuse as a tunable phenomenological input",
    status: "operational",
  },
  {
    id: "boundary",
    step: 2,
    label: "Boundary datum",
    formula: "\\mathfrak{T}_\\partial = (\\mathcal{A}_+,\\mathcal{H}_+,D_+,J,\\Gamma,B_\\Sigma)",
    input: "Operational seed",
    fixed: "One-sided spectral datum from which all primitive structure is reconstructed",
    notClaimed: "No physical observables yet",
    fail: "The one-sided datum fails to determine the doubled datum or the Calderón polarization",
    status: "theorem-core",
  },
  {
    id: "kernel",
    step: 3,
    label: "Primitive kernel",
    formula: "(\\tau_{\\mathrm{dbl}},\\iota_C,P_{\\mathrm{prim}},[u_\\Sigma],c_3)",
    input: "Boundary datum",
    fixed: "Five primitive invariants from the Calderón polarization and the seam class",
    notClaimed: "No Standard Model gauge group, no α",
    fail: "A primitive invariant is not fixed by the boundary procedure",
    status: "theorem-core",
  },
  {
    id: "joint-solve",
    step: 4,
    label: "Joint discrete admissibility solve",
    formula: "d^\\star_{\\mathrm{disc}}",
    input: "Primitive kernel",
    fixed:
      "A single discrete admissibility solution that simultaneously determines the rank split, the seam normalization, and the bridge seed",
    notClaimed:
      "Not a sequential 'first carrier, then counting, then observables' chain — these are joint outputs of one discrete solve",
    fail:
      "An alternative admissible discrete solution survives all primitive constraints",
    status: "theorem-core",
  },
];

const DECODERS: StepNode[] = [
  {
    id: "decoder-Y",
    step: "5a",
    label: "Y — structure",
    formula: "Y = -\\tfrac{1}{3} P_- + \\tfrac{1}{2} P_+",
    input: "Joint solve, carrier block",
    fixed:
      "The hypercharge generator, the 3+2 rank split, the Standard Model packet, and the gauge quotient",
    notClaimed: "No flavor closure, no α value",
    fail: "The 3+2 split is not forced without an SM-side import",
    status: "decoder",
  },
  {
    id: "decoder-uSigma",
    step: "5b",
    label: "[u_Σ] = 1 — counting",
    formula: "[u_\\Sigma] = 1",
    input: "Joint solve, seam class",
    fixed:
      "Family count N_fam = 3, admissible occupancy Ω_adm = 48, Higgs index N_Φ = 1, abelian coefficient b₁ = 41/10",
    notClaimed: "No mass values, no flavor matrices",
    fail: "An admissible alternative seam normalization survives",
    status: "decoder",
  },
  {
    id: "decoder-phi0",
    step: "5c",
    label: "u = φ₀ — bridge seed",
    formula: "u := \\varphi_0 = \\tfrac{1}{6\\pi} + \\tfrac{3}{256\\pi^4}",
    input: "Joint solve, retained branch",
    fixed:
      "Bridge readouts λ_C = √(φ₀(1−φ₀)), β_rad = φ₀/(4π), sin²θ₁₃ = φ₀ e^{−γ}",
    notClaimed: "Not the exact electromagnetic root (that uses φ_seam(α) instead of φ₀)",
    fail:
      "Bridge readouts deviate from declared comparison rows beyond stated interface uncertainty",
    status: "decoder",
  },
];

const TRUNK_AFTER: StepNode[] = [
  {
    id: "admissibility",
    step: 6,
    label: "Admissibility selector",
    formula: "P_{\\mathrm{adm}} = P_{\\mathrm{prim}}\\,P_{\\mathrm{sing}}\\,P_\\Theta",
    input: "Joint solve outputs + analytic data",
    fixed:
      "Selection of the physical admissible sector and the strong-CP null θ_eff = 0",
    notClaimed: "Not the dynamics of the physical sector",
    fail: "Selector and dynamics are conflated, or positivity hypotheses are hidden",
    status: "conditional",
  },
  {
    id: "closure",
    step: 7,
    label: "Closure dynamics",
    formula:
      "Z_{\\mathrm{rel}} \\Rightarrow \\{S_n^T\\} \\Rightarrow (\\mathcal{H}_{\\mathrm{adm}},\\mathfrak{A}_{\\mathrm{adm}}) \\Rightarrow \\Gamma_k",
    input: "Admissibility selector",
    fixed:
      "Reflection positivity, OS reconstruction, local Minkowski net, exact admissible RG flow — under stated hypotheses",
    notClaimed: "No CMB fit, no Stage 2 sky realization",
    fail:
      "Positivity, gap, or OS hypotheses fail on the admissible sector under stated conditions",
    status: "conditional",
  },
  {
    id: "observables",
    step: 8,
    label: "Observable functor",
    formula:
      "\\mathfrak{T}_\\star \\xrightarrow{\\mathcal{R}_{\\mathrm{ren}}} \\Gamma_{\\mathrm{TFPT}}^{\\mathrm{ren}} \\xrightarrow{\\mathcal{M}_{\\mathrm{phys}}} \\mathbf{O}_{\\mathrm{phys}}^{\\mathrm{TFPT}}",
    input: "Closure dynamics + decoder outputs",
    fixed:
      "Renormalised observables and physical readouts (α, CKM, PMNS, β, …) only after explicit physical and scheme projection",
    notClaimed:
      "Scheme conventions are not theorem inputs; comparison rows are projected last",
    fail:
      "Scheme projection is allowed to feed back into the admissibility data",
    status: "bridge",
  },
  {
    id: "cosmo-interface",
    step: 9,
    label: "Cosmology interfaces",
    formula:
      "\\Lambda_{\\mathrm{IR}}, S_\\Sigma, N_{\\mathrm{DW}}, \\theta_i, T_R, \\eta_B, \\Sigma m_\\nu, m_a",
    input: "Closed branch T★ + seam transfer",
    fixed: "Downstream cosmology comparison surface",
    notClaimed:
      "Stage 1 spectra are programmatic targets; Stage 2 sky realization is conjectural",
    fail: "Cosmology is allowed to tune the primitive branch",
    status: "downstream",
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
          eyebrow="The staged reconstruction"
          title="From boundary datum to observable closure"
          description="TFPT is not a linear chain of independent claims. The primitive kernel feeds a single joint discrete admissibility solve from which three decoders branch in parallel — structure (Y), counting ([u_Σ]=1), and bridge observables (u = φ₀). The selector P_adm is downstream of the decoders, not parallel to them."
        />

        <div ref={ref} className="relative mx-auto mt-14 max-w-5xl space-y-3">
          {TRUNK_BEFORE.map((n, i) => (
            <div key={n.id}>
              <StepCard node={n} delay={i * 0.06} />
              {i < TRUNK_BEFORE.length - 1 ? <Connector /> : null}
            </div>
          ))}

          <Connector label="Three parallel decoders" />

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

          <Connector label="Joint outputs feed the admissibility/closure layer" />

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
            The diagram is a status map of the derivation chain, not a claim
            that all displayed outputs share the same proof status. Theorem
            core, decoder outputs, conditional closure, bridge readouts, and
            downstream interfaces are all visibly distinct — and labelled with
            their own &ldquo;not claimed here&rdquo; and &ldquo;how it can
            fail&rdquo; rows.
          </span>
        </motion.div>
      </div>
    </section>
  );
}

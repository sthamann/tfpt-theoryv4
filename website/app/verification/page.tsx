import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, Github, TerminalSquare } from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";
import { VerificationDag } from "@/components/VerificationDag";
import { ScriptIndex } from "@/components/ScriptIndex";
import { SCRIPT_TOTAL } from "@/lib/suite";
import { REPO_URL } from "@/lib/utils";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";

export const metadata: Metadata = {
  title: "Verification & Workflow — Every Number Machine-Checked",
  description:
    "How TFPT is verified: an interactive dependency graph showing exactly how each result is computed and on which inputs it depends (including the self-consistency loop), the four-path verification stack (Python suite, independent Wolfram mirror, Lean carrier proof, versioned status ledger), and the full script index linked to GitHub.",
  keywords: [
    "TFPT verification",
    "dependency graph",
    "reproducibility",
    "verification suite",
    "status ledger",
    "Wolfram",
    "Lean proof",
    "self-consistency",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/verification` },
  openGraph: {
    type: "article",
    title: "Verification & Workflow — Every Number Machine-Checked",
    description:
      "An interactive dependency graph of the TFPT compiler closure, the four-path verification stack, and the full script index — all linked to the public repository.",
    url: `${SITE_URL}/verification`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "Verification & Workflow — TFPT",
    description:
      "Interactive dependency graph + four-path verification stack + full script index.",
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "WebPage",
  name: "TFPT — Verification & Workflow",
  url: `${SITE_URL}/verification`,
  inLanguage: "en",
  description:
    "Interactive dependency graph of the TFPT compiler closure and the full verification stack.",
  sameAs: [REPO_URL],
  isBasedOn: REPO_URL,
};

const PATHS: { label: string; value: string; body: string }[] = [
  {
    label: "Python suite",
    value: `${SCRIPT_TOTAL} checks`,
    body: "One file per claim cluster; run_all.py ends ALL CHECKS PASSED. Exact sympy where possible, mpmath/numpy otherwise.",
  },
  {
    label: "Wolfram mirror",
    value: "116/116 + 224/224",
    body: "An independent second path for the exact algebraic / identity / lattice results, on the Wolfram Engine: the verified base file plus the v84+ extension file.",
  },
  {
    label: "Lean carrier",
    value: "0 sorry",
    body: "The P2 carrier algebra — hypercharge, anomaly-freedom, integer rigidity — formalised in Lean 4 with only kernel axioms.",
  },
  {
    label: "Status ledger",
    value: "1 source of truth",
    body: "status_ledger.csv types every claim (id, status, location, dependency, script) and is versioned. If the text and the ledger disagree, the ledger wins.",
  },
];

const MARKERS: { m: string; meaning: string; tone: string }[] = [
  { m: "[E]", meaning: "exact / machine-proven (fine types: identity, lattice/Lie, Lean-formalised, numerical fixed point)", tone: "text-emerald-200 bg-emerald-500/15 ring-emerald-400/30" },
  { m: "[C]", meaning: "conditional — holds under named hypotheses (fine type: physical bridge / readout)", tone: "text-amber-200 bg-amber-500/15 ring-amber-400/30" },
  { m: "[O]", meaning: "open / axiom — declared input or genuine gap", tone: "text-rose-200 bg-rose-500/15 ring-rose-400/30" },
  { m: "[X]", meaning: "falsifiable kill test (committed in advance)", tone: "text-blue-200 bg-blue-500/15 ring-blue-400/30" },
];

const REPRODUCE = `# 1. Compile the active document set      ->  "10 ok, 0 failed"
bash build.sh notes

# 2. Run the Python verification suite    ->  "ALL CHECKS PASSED"
cd verification && python run_all.py

# 3. Independent Wolfram path (optional)  ->  "ALL WOLFRAM CHECKS PASSED"
wolframscript -file verification/wolfram/tfpt_readouts.wl

# 4. Lean carrier-rigidity proof (optional) ->  "AUDIT: PASS"
cd experiments/lean4-carrier-rigidity && lake exe cache get && bash scripts/audit.sh

# 5. The sync audit (papers <-> suite <-> ledger <-> website)  ->  "AUDIT OK"
bash build.sh audit

# 6. Regenerate the reproducibility manifests (run last)
python verification/make_manifest.py`;

export default function VerificationPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <section className="relative isolate overflow-hidden pt-12 pb-12 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[500px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(16,185,129,0.35), rgba(99,102,241,0.25), transparent)",
          }}
        />
        <div className="relative mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Breadcrumb" className="mb-6">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
            >
              <ArrowLeft size={14} />
              Back to overview
            </Link>
          </nav>
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-emerald-200">
            <span className="uppercase">Verification &amp; workflow</span>
          </span>
          <h1 className="mt-6 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl md:text-6xl">
            Every number is{" "}
            <span className="text-gradient-blue">machine-checked</span>.
          </h1>
          <p className="mt-4 max-w-3xl text-base leading-relaxed text-slate-300 sm:text-lg">
            TFPT is built like a compiler, and verified like one. Nothing is
            marked closed that is not re-derived from the two axioms by an
            independent script, and no dimensionful quantity is claimed as a
            derivation from pure numbers. The graph below shows exactly how each
            result is computed, on which inputs it depends, and which scripts
            check it — including the self-consistency loop that fixes the inputs
            themselves. Every script is{" "}
            <span className="font-semibold text-slate-100">runnable live in your browser</span>{" "}
            — click one to execute the real Python (via Pyodide / WebAssembly)
            and watch the checks pass, step by step.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
            >
              <Github size={16} />
              Open the repository
            </Link>
            <Link
              href="#dag"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
            >
              Jump to the dependency graph
            </Link>
          </div>
        </div>
      </section>

      {/* Four-path stack + markers */}
      <section className="relative py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="The discipline"
            title="Four independent paths, one ledger"
            description="A claim is only as strong as the way it is checked. The dimensionless skeleton is verified three independent ways and typed in a single versioned ledger, so the papers, the suite and the ledger stay in lock-step."
          />
          <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {PATHS.map((p) => (
              <div
                key={p.label}
                className="glass flex flex-col rounded-2xl p-5 ring-1 ring-slate-700/40"
              >
                <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                  {p.label}
                </div>
                <div className="mt-1 font-serif text-2xl font-semibold text-slate-50">
                  {p.value}
                </div>
                <p className="mt-2 text-xs leading-relaxed text-slate-400">
                  {p.body}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-6 flex flex-wrap items-center gap-2 rounded-2xl border border-slate-700/40 bg-slate-950/40 px-5 py-4">
            <span className="mr-1 text-[11px] font-semibold uppercase tracking-widest text-slate-300">
              Status markers
            </span>
            {MARKERS.map((x) => (
              <span
                key={x.m}
                className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[11px] font-medium ring-1 ${x.tone}`}
              >
                <span className="font-mono font-semibold">{x.m}</span>
                {x.meaning}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* The interactive DAG */}
      <section
        id="dag"
        className="relative scroll-mt-20 border-t border-slate-800/60 py-12 sm:py-16"
      >
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="The dependency graph"
            title="How each result is computed"
            description="Two axioms at the source, the E₈ compiler in the middle, the observables as sinks. Click any node to see what it is, its status marker, its inputs and outputs, how it can fail, and the scripts that machine-check it — then click a script to run it live in your browser. The dashed rose edges are the bootstrap: the E₈ closure feeds back and fixes the inputs."
          />
          <div className="mt-10">
            <VerificationDag />
          </div>
        </div>
      </section>

      {/* Reproduce */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Reproduce it yourself"
            title="Five commands, from the repository root"
            description="Dependencies: a LaTeX distribution, Python 3 with sympy / mpmath / numpy / matplotlib; optionally the Wolfram Engine and Lean 4. Every script cited in run_all.py is also cited inline in the documents, and the status heatmap is generated directly from the ledger."
          />
          <div className="mt-8 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/70">
            <div className="flex items-center gap-2 border-b border-slate-800/60 px-4 py-2.5">
              <TerminalSquare size={14} className="text-slate-400" aria-hidden />
              <span className="font-mono text-[11px] uppercase tracking-widest text-slate-400">
                reproduce / verify
              </span>
            </div>
            <pre className="overflow-x-auto px-5 py-4 text-[12px] leading-relaxed text-slate-200">
              <code className="font-mono">{REPRODUCE}</code>
            </pre>
          </div>
        </div>
      </section>

      {/* Script index */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="The script index"
            title="What each script checks"
            description="The full verification suite, grouped by what it proves. Every script links to its source in the public repository."
          />
          <div className="mt-10">
            <ScriptIndex />
          </div>

          <div className="mt-10 flex flex-col items-center gap-3 rounded-2xl border border-blue-400/25 bg-gradient-to-br from-blue-500/10 to-violet-500/5 p-8 text-center">
            <h3 className="font-serif text-xl font-semibold text-slate-50">
              Independent scrutiny is the point
            </h3>
            <p className="max-w-2xl text-sm leading-relaxed text-slate-400">
              These checks are reproducible by anyone — that is what
              &ldquo;independent&rdquo; means here: the same result falls out on
              your machine, on an independent Wolfram path, and (for the carrier)
              in Lean. We do not claim external endorsements; we invite review.
              Open questions and known limitations are tracked openly in the
              research contracts and the status ledger — disagreements go in the
              issue tracker.
            </p>
            <div className="mt-1 flex flex-wrap items-center justify-center gap-3">
              <Link
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
              >
                <Github size={16} />
                Source, scripts &amp; ledger
              </Link>
              <Link
                href={`${REPO_URL}/issues`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
              >
                Open an issue / review
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

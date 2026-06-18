import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  CircleDot,
  FlaskConical,
  ShieldAlert,
  Target,
  XCircle,
} from "lucide-react";
import { SCRIPT_TOTAL } from "@/lib/suite";
import { SITE_VERSION } from "@/lib/version";
import { REPO_URL } from "@/lib/utils";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";

export const metadata: Metadata = {
  title: "Read this first — the skeptical reviewer's entry point",
  description:
    `A 5-minute orientation for a hostile reviewer of TFPT ${SITE_VERSION}: what is claimed, what is explicitly not claimed, what would kill it, what is machine-checked, what remains open, and how to reproduce one result in five minutes.`,
  keywords: [
    "TFPT review",
    "skeptical reviewer",
    "what TFPT claims",
    "what would kill TFPT",
    "machine-checked",
    "reproducibility",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/review` },
  openGraph: {
    type: "article",
    title: "Read this first — the skeptical reviewer's entry point",
    description:
      "Claims, non-claims, kill conditions, what is machine-checked, what is open, and a five-minute reproduction — for the hostile reviewer.",
    url: `${SITE_URL}/review`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "TFPT — read this first if you are skeptical",
    description:
      "Claims, non-claims, kill conditions, machine-checked layer, open residual, and a five-minute reproduction.",
  },
};

interface Block {
  icon: React.ReactNode;
  kicker: string;
  title: string;
  body: React.ReactNode;
  tone: string;
}

const BLOCKS: Block[] = [
  {
    icon: <Target size={18} aria-hidden />,
    kicker: "1 · The claim",
    title: "What TFPT claims",
    tone: "border-blue-400/30 bg-blue-500/[0.05]",
    body: (
      <>
        A two-input discrete compiler whose algebraic kernel derives the{" "}
        <strong className="text-slate-100">Standard-Model skeleton</strong> — the
        gauge group, three families, hypercharge and the flavor invariants — and
        several dimensionless readouts (α⁻¹, the neutrino angles, β_rad). It is
        built only from two axioms: the seam constant{" "}
        <span className="font-mono">c₃ = 1/(8π)</span> and the carrier rank{" "}
        <span className="font-mono">g_car = 5</span>. E₈ is the compiler&rsquo;s
        internal audit lattice, not a physical gauge group.
      </>
    ),
  },
  {
    icon: <XCircle size={18} aria-hidden />,
    kicker: "2 · The non-claims",
    title: "What TFPT does not claim",
    tone: "border-slate-500/30 bg-slate-500/[0.05]",
    body: (
      <>
        It is <strong className="text-slate-100">not</strong> an E₈ gauge theory
        (so the Distler–Garibaldi / Coleman–Mandula no-gos do not apply), and{" "}
        <strong className="text-slate-100">not</strong> a certified strict
        physical theory of everything — full quantum-gravity closure is a layer
        that is reduced to one definitional premise, not yet certified. The
        absolute mass scale is a single declared dimensionful anchor (v_geo), and{" "}
        <span className="font-mono">m_p/m_e</span> is explicitly not claimed as a
        compiler power. No experimental value is ever used as an input — only as
        a comparison row.
      </>
    ),
  },
  {
    icon: <ShieldAlert size={18} aria-hidden />,
    kicker: "3 · The kill conditions",
    title: "What would kill it",
    tone: "border-rose-400/30 bg-rose-500/[0.05]",
    body: (
      <>
        Any single one of: the α fixed-point equation{" "}
        <span className="font-mono">F_U(1)(α) = 0</span> failing or admitting a
        second admissible root; a robust neutron-EDM signal (θ_eff = 0 is
        structural); a second light seam-even Higgs doublet (N_Φ = 1); a robust
        tensor ratio <span className="font-mono">r ≳ 0.01</span>; a robust{" "}
        <span className="font-mono">w ≠ −1</span>; a JUNO solar angle clearly away
        from 0.307; or any verification script failing to reproduce its claim.{" "}
        <Link href="/falsification" className="font-semibold text-blue-300 hover:text-blue-200">
          The full kill board →
        </Link>
      </>
    ),
  },
  {
    icon: <CheckCircle2 size={18} aria-hidden />,
    kicker: "4 · The evidence",
    title: "What is machine-checked",
    tone: "border-emerald-400/30 bg-emerald-500/[0.05]",
    body: (
      <>
        Every exact identity, lattice/Lie theorem and numerical fixed point is
        re-derived from the two axioms by{" "}
        <strong className="text-slate-100">{SCRIPT_TOTAL} Python checks</strong>{" "}
        (<span className="font-mono">run_all.py</span> ends ALL CHECKS PASSED),
        mirrored on an independent Wolfram path, and the carrier algebra is
        formalised in Lean 4 with{" "}
        <span className="font-mono">0 sorry</span>. Every claim is typed in a
        single versioned ledger — if the prose and the ledger disagree, the
        ledger wins.{" "}
        <Link href="/verification" className="font-semibold text-blue-300 hover:text-blue-200">
          The verification stack →
        </Link>
      </>
    ),
  },
  {
    icon: <CircleDot size={18} aria-hidden />,
    kicker: "5 · The residual",
    title: "What remains open",
    tone: "border-amber-400/30 bg-amber-500/[0.05]",
    body: (
      <>
        Exactly three named interfaces, none hidden:{" "}
        <span className="font-mono">v_geo</span> (one dimensionful scale anchor,
        the same nature as 1/G), <span className="font-mono">G_net</span> (the
        seam-net metric inclusion — algebra discharged to [E], one definitional
        seam premise left [O]), and <span className="font-mono">F_transfer</span>{" "}
        (the source→pole/relic/cosmology transport — Koide, η_B, the axion relic,
        m_p/m_e are its four typed instances). The whole boundary-QFT layer
        (Dirac, cutoff, gauging, glue) collapses onto the same{" "}
        <span className="font-mono">G_net</span> premise via the Modular Spectral
        Closure (v258–v261) — one relative object, no new open item.{" "}
        <Link href="/#open-gates" className="font-semibold text-blue-300 hover:text-blue-200">
          The open residual →
        </Link>
      </>
    ),
  },
  {
    icon: <FlaskConical size={18} aria-hidden />,
    kicker: "6 · The five-minute test",
    title: "Reproduce one result in five minutes",
    tone: "border-violet-400/30 bg-violet-500/[0.05]",
    body: (
      <>
        Open the dependency graph and click the{" "}
        <span className="font-mono">α⁻¹</span> node: the real Python runs in your
        browser (via Pyodide / WebAssembly) and re-derives{" "}
        <span className="font-mono">α⁻¹ = 137.0359992…</span> as the unique root
        of the parameter-free cubic — no install, no fit.{" "}
        <Link href="/verification#dag" className="font-semibold text-blue-300 hover:text-blue-200">
          Run it now →
        </Link>{" "}
        Or clone the repository and run the whole suite locally.
      </>
    ),
  },
];

export default function ReviewPage() {
  return (
    <>
      <section className="relative isolate overflow-hidden pt-12 pb-8 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[500px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(99,102,241,0.4), rgba(16,185,129,0.2), transparent)",
          }}
        />
        <div className="relative mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Breadcrumb" className="mb-6">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
            >
              <ArrowLeft size={14} />
              Back to overview
            </Link>
          </nav>
          <span className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-blue-200">
            <span className="uppercase">For the skeptical reviewer</span>
          </span>
          <h1 className="mt-6 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl md:text-6xl">
            Read this <span className="text-gradient-blue">first</span>.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300 sm:text-lg">
            If the claim &ldquo;a derived Standard-Model skeleton&rdquo; set off
            an alarm, good — keep it on. This page is the five-minute orientation:
            what is claimed, what is <em>not</em>, what would falsify it, what is
            machine-checked, what is still open, and how to reproduce one result
            yourself. Nothing here is sold; a typed claim stack is dissected.
          </p>
        </div>
      </section>

      <section className="relative py-8 sm:py-12">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <ol className="grid gap-4">
            {BLOCKS.map((b) => (
              <li key={b.kicker}>
                <article className={`rounded-2xl border p-5 sm:p-6 ${b.tone}`}>
                  <div className="flex items-center gap-2 text-slate-200">
                    {b.icon}
                    <span className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">
                      {b.kicker}
                    </span>
                  </div>
                  <h2 className="mt-2 font-serif text-xl font-semibold text-slate-50">
                    {b.title}
                  </h2>
                  <p className="mt-2 text-sm leading-relaxed text-slate-300">{b.body}</p>
                </article>
              </li>
            ))}
          </ol>

          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href="/verification"
              className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
            >
              Verification stack
              <ArrowRight size={15} aria-hidden />
            </Link>
            <Link
              href="/falsification"
              className="inline-flex items-center gap-2 rounded-full border border-rose-400/40 bg-rose-500/10 px-5 py-2.5 text-sm font-semibold text-rose-100 transition-colors hover:bg-rose-500/20"
            >
              How to kill it
            </Link>
            <Link
              href="/objections"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
            >
              Objection ledger
            </Link>
            <Link
              href={`${REPO_URL}/issues`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
            >
              Open an issue
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}

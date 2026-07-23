import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, CheckCircle2, CircleDashed, MessageSquare } from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";
import { SCRIPT_TOTAL } from "@/lib/suite";
import { SITE_VERSION } from "@/lib/version";
import { REPO_URL, SITE_URL } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Replication status — self-verified, externally open",
  description:
    `An honest replication scorecard for TFPT ${SITE_VERSION}: three self-contained verification paths (Python, Wolfram, Lean) pass; no independent external reproduction is claimed yet; review is invited.`,
  keywords: [
    "TFPT replication",
    "independent reproduction",
    "verification",
    "external review",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/replication` },
  openGraph: {
    type: "article",
    title: "Replication status — self-verified, externally open",
    description:
      "Three self-contained verification paths pass; no independent external reproduction is claimed yet; review is invited.",
    url: `${SITE_URL}/replication`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "TFPT replication status",
    description: "Self-verified across three paths; external replication openly tracked.",
  },
};

const SELF_VERIFIED: { path: string; value: string; body: string }[] = [
  {
    path: "Python suite",
    value: `${SCRIPT_TOTAL} checks`,
    body: "One file per claim cluster; run_all.py ends ALL CHECKS PASSED. Exact sympy where possible, mpmath/numpy otherwise.",
  },
  {
    path: "Wolfram mirror",
    value: "116/116 + 552/552",
    body: "An independent second path for the exact algebraic / identity / lattice results, on the Wolfram Engine.",
  },
  {
    path: "Lean 4 carrier",
    value: "0 sorry",
    body: "The carrier algebra — hypercharge, anomaly-freedom, integer rigidity — formalised with only kernel axioms (AUDIT: PASS).",
  },
];

export default function ReplicationPage() {
  return (
    <>
      <section className="relative isolate overflow-hidden pt-12 pb-8 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[500px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(16,185,129,0.3), rgba(99,102,241,0.2), transparent)",
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
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-emerald-200">
            <span className="uppercase">Replication status</span>
          </span>
          <h1 className="mt-6 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl md:text-6xl">
            Self-verified. Externally <span className="text-gradient-blue">open</span>.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300 sm:text-lg">
            The honest replication picture, stated plainly. The dimensionless
            skeleton is reproduced three independent ways inside this project;
            no independent <em>external</em> reproduction is claimed yet. We do
            not claim endorsements — we invite review, and we will record what
            comes back here, including disputes.
          </p>
        </div>
      </section>

      {/* Tier 1 — self-verified */}
      <section className="relative py-8 sm:py-12" aria-labelledby="self-heading">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            id="self-heading"
            eyebrow="Tier 1 · in hand"
            title="Self-verified — three independent paths"
            description="Reproducible by anyone, today, from the public repository. This is what 'independent' means here: the same result falls out on your machine, on a separate Wolfram path, and (for the carrier) in Lean."
          />
          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            {SELF_VERIFIED.map((s) => (
              <div
                key={s.path}
                className="flex flex-col rounded-2xl border border-emerald-400/25 bg-emerald-500/[0.04] p-5"
              >
                <div className="flex items-center gap-2 text-emerald-300">
                  <CheckCircle2 size={16} aria-hidden />
                  <span className="text-[10px] font-semibold uppercase tracking-widest">
                    {s.path}
                  </span>
                </div>
                <div className="mt-1 font-serif text-2xl font-semibold text-slate-50">
                  {s.value}
                </div>
                <p className="mt-2 text-xs leading-relaxed text-slate-400">{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tier 2 — external reproduction */}
      <section className="relative border-t border-slate-800/60 py-8 sm:py-12" aria-labelledby="ext-heading">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            id="ext-heading"
            eyebrow="Tier 2 · open"
            title="Independently reproduced — none yet"
            description="No third party has yet published an independent reproduction. This is stated as a status, not hidden. The bar to clear is low: every script is public and runnable in the browser."
          />
          <div className="mt-8 flex items-start gap-3 rounded-2xl border border-slate-600/40 bg-slate-950/40 p-5">
            <CircleDashed size={18} className="mt-0.5 flex-none text-slate-400" aria-hidden />
            <div>
              <div className="text-sm font-semibold text-slate-100">
                Status: none yet — review invited
              </div>
              <p className="mt-1 text-sm leading-relaxed text-slate-300">
                If you reproduce a result (or fail to), we will record it here as
                confirmed, partial, or disputed, with a link to your write-up.
                The fastest way to start is the in-browser reproducer or a local
                clone.
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
                <Link
                  href="/verification#dag"
                  className="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-4 py-2 text-xs font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
                >
                  Run a check in your browser
                </Link>
                <Link
                  href={REPO_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 rounded-full border border-slate-600/60 bg-slate-900/60 px-4 py-2 text-xs font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
                >
                  Clone the repository
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tier 3 — external critique */}
      <section className="relative border-t border-slate-800/60 py-8 sm:py-12" aria-labelledby="crit-heading">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            id="crit-heading"
            eyebrow="Tier 3 · open"
            title="External critique — tracked in public"
            description="Open questions and known limitations are tracked openly in the research contracts and the status ledger; substantive disagreements belong in the issue tracker and will be answered there and reflected in the objection ledger."
          />
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href={`${REPO_URL}/issues`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
            >
              <MessageSquare size={15} aria-hidden />
              Open an issue / review
            </Link>
            <Link
              href="/objections"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
            >
              Objection ledger
            </Link>
            <Link
              href="/papers/research-contracts"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
            >
              Research contracts
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}

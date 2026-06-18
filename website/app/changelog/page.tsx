import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, FileText, Github } from "lucide-react";
import { Changelog } from "@/components/Changelog";
import { CHANGELOG, CHANGELOG_COUNT } from "@/lib/changelog";
import { REPO_URL, SITE_URL } from "@/lib/utils";
import { SITE_VERSION } from "@/lib/version";

const latest = CHANGELOG[0]?.date ?? "";
const earliest = CHANGELOG[CHANGELOG.length - 1]?.date ?? "";

export const metadata: Metadata = {
  title: "Changelog — Every Change and New Result, by Date",
  description:
    "The canonical, dated record of every change to TFPT: new verification modules (vN), status changes, editorial passes and infrastructure. Mirrored from the repository's changelog and kept in lock-step with the theory, the verification suite and the papers.",
  keywords: [
    "TFPT changelog",
    "verification modules",
    "status ledger",
    "release notes",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/changelog` },
  openGraph: {
    type: "article",
    title: "TFPT Changelog — every change, by date",
    description:
      "The dated record of every TFPT change: verification modules, status changes, papers and infrastructure. The single source is the repository changelog.",
    url: `${SITE_URL}/changelog`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "TFPT Changelog",
    description: "Every change and new result, by date.",
  },
};

export default function ChangelogPage() {
  return (
    <>
      <section className="relative isolate overflow-hidden pt-12 pb-8 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[460px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(59,130,246,0.3), rgba(139,92,246,0.25), transparent)",
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
            <span className="uppercase">Changelog</span>
            <span aria-hidden className="text-blue-400/60">·</span>
            <span className="font-mono">{CHANGELOG_COUNT} entries</span>
          </span>
          <h1 className="mt-6 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl">
            Every change and new result,{" "}
            <span className="text-gradient-blue">by date</span>.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300">
            The canonical, dated record of the TFPT development: new
            verification modules (<code className="font-mono text-slate-200">vN</code>),
            status changes, editorial passes and infrastructure. It is maintained
            in the same change as the work it records — and this page is generated
            directly from the repository&rsquo;s{" "}
            <code className="font-mono text-slate-200">changelog.tex</code>, so it
            never drifts from the source. Module numbers refer to{" "}
            <code className="font-mono text-slate-200">verification/vN_*.py</code>;
            claim IDs refer to rows of the status ledger.
          </p>
          <div className="mt-6 flex flex-wrap items-center gap-3">
            <Link
              href="/papers/changelog.pdf"
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
            >
              <FileText size={15} aria-hidden />
              Changelog (PDF)
            </Link>
            <Link
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium text-slate-300 ring-1 ring-slate-700/50 transition-colors hover:bg-white/5 hover:text-white"
            >
              <Github size={15} aria-hidden />
              Repository
            </Link>
            {latest && (
              <span className="font-mono text-xs text-slate-500">
                TFPT {SITE_VERSION} · {earliest} → {latest}
              </span>
            )}
          </div>

          <dl className="mt-6 flex flex-wrap gap-x-5 gap-y-1.5 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <span className="rounded bg-emerald-500/10 px-1 font-mono font-semibold text-emerald-300 ring-1 ring-emerald-400/30">
                [E]
              </span>
              <dd>exact / proven</dd>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="rounded bg-amber-500/10 px-1 font-mono font-semibold text-amber-300 ring-1 ring-amber-400/30">
                [C]
              </span>
              <dd>conditional</dd>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="rounded bg-slate-500/10 px-1 font-mono font-semibold text-slate-300 ring-1 ring-slate-400/30">
                [O]
              </span>
              <dd>open / axiom</dd>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="rounded bg-rose-500/10 px-1 font-mono font-semibold text-rose-300 ring-1 ring-rose-400/30">
                [X]
              </span>
              <dd>kill test</dd>
            </div>
          </dl>
        </div>
      </section>

      <section className="relative py-8 sm:py-12">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <Changelog />
        </div>
      </section>
    </>
  );
}

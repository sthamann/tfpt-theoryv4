import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";
import { KillBoard } from "@/components/falsification/KillBoard";
import { FalsificationTable } from "@/components/falsification/FalsificationTable";
import { KillCriteria } from "@/components/falsification/KillCriteria";
import { NoKnobsAudit } from "@/components/falsification/NoKnobsAudit";
import { SITE_VERSION } from "@/lib/version";
import { SITE_URL } from "@/lib/utils";

export const metadata: Metadata = {
  title: "How to kill TFPT — Falsification Surface and No-Knobs Audit",
  description:
    `An explicit falsification surface for the TFPT ${SITE_VERSION} compiler closure, paired with a no-knobs audit. The freeze file commits the decisive kill criteria — JUNO θ₁₂, the tensor ratio r, neutrino ordering, the strong-CP null, and w = −1 — in advance. The construction is killed by any single satisfied criterion.`,
  keywords: [
    "TFPT falsification",
    "How to kill TFPT",
    "Topological Fixed-Point Theory falsification",
    "No-knobs audit",
    "Freeze file",
    "Strong-CP null",
    "JUNO solar angle",
    "Tensor ratio r",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: {
    canonical: `${SITE_URL}/falsification`,
  },
  openGraph: {
    type: "article",
    title: "How to kill TFPT — Falsification Surface and No-Knobs Audit",
    description:
      `Explicit falsification surface for the TFPT ${SITE_VERSION} compiler closure, with a no-knobs audit. Every output has a committed kill criterion.`,
    url: `${SITE_URL}/falsification`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "How to kill TFPT — Falsification Surface",
    description:
      "Each TFPT output ships with its own committed kill criterion. Free knobs: 0.",
  },
};

const articleJsonLd = {
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  headline: "How to kill TFPT — Falsification Surface and No-Knobs Audit",
  alternateName: `TFPT ${SITE_VERSION} Falsification Map`,
  url: `${SITE_URL}/falsification`,
  inLanguage: "en",
  isPartOf: {
    "@type": "PublicationIssue",
    name: `TFPT ${SITE_VERSION} compiler-closure document set`,
  },
  author: [
    { "@type": "Person", name: "Stefan Hamann" },
    { "@type": "Person", name: "Alessandro Rizzo" },
  ],
  abstract:
    `An explicit falsification surface for the TFPT ${SITE_VERSION} compiler closure. For every output the page lists allowed inputs, forbidden inputs, free-knob count, and a committed kill criterion that, if satisfied, falsifies the construction.`,
  about: [
    "Falsification",
    "No-knobs audit",
    "Topological Fixed-Point Theory",
    "Strong-CP problem",
    "Solar neutrino angle",
    "Inflation tensor ratio",
  ],
};

export default function FalsificationPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleJsonLd) }}
      />

      <section className="relative isolate overflow-hidden pt-12 pb-12 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[500px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(244,63,94,0.4), rgba(168,85,247,0.2), transparent)",
          }}
        />
        <div className="relative mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Breadcrumb" className="mb-6">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
            >
              <ArrowLeft size={14} />
              Back to overview
            </Link>
          </nav>
          <span className="inline-flex items-center gap-2 rounded-full border border-rose-400/20 bg-rose-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-rose-200">
            <span className="uppercase">Falsification surface · 2026</span>
          </span>
          <h1 className="mt-6 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl md:text-6xl">
            How to <span className="text-gradient-blue">kill</span> TFPT.
          </h1>
          <p className="mt-3 max-w-2xl text-base leading-relaxed text-slate-300">
            A theory that cannot fail explains nothing. This page lists the
            committed kill criteria of the TFPT {SITE_VERSION} compiler closure — frozen in
            advance in the freeze file — together with the experiment or
            structural argument that would{" "}
            <span className="font-semibold text-slate-100">
              kill the construction
            </span>
            . The no-knobs audit underneath records what the theory may
            consume as input and what it may not.
          </p>
          <p className="mt-3 max-w-2xl text-sm leading-relaxed text-slate-400">
            Each output is killed by{" "}
            <em>any single</em> satisfied criterion. The construction does not
            survive on most outputs being right.
          </p>
        </div>
      </section>

      <section
        id="kill-board-section"
        className="relative scroll-mt-20 py-12 sm:py-16"
        aria-labelledby="kill-board-heading"
      >
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            id="kill-board-heading"
            eyebrow="The kill board"
            title="Every readout, its kill condition, and where it stands now"
            description="The full status-graded surface as a board: each card carries the predicted value, the single condition that would falsify it, and — where a standalone empirical audit exists in the experiments/ tree — its live status. These confrontations are search targets, not load-bearing claims; no card is upgraded by data proximity."
          />
          <KillBoard />
        </div>
      </section>

      <section
        id="confrontation-table-section"
        className="relative scroll-mt-20 border-t border-slate-800/60 py-12 sm:py-16"
        aria-labelledby="confrontation-table-heading"
      >
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            id="confrontation-table-heading"
            eyebrow="The confrontation table"
            title="Every readout against the data, with its decisive year"
            description="The same prediction surface as one dense table: for each readout, the derivation, the TFPT value, the current measured value, the deviation, the dated experimental source, and the experiment — with an approximate year — that will turn it into a definitive hit or kill (typically a sharper, future measurement). Every value is repo-documented; nothing is fitted."
          />
          <FalsificationTable />
        </div>
      </section>

      <section
        id="kill-criteria-section"
        className="relative scroll-mt-20 border-t border-slate-800/60 py-12 sm:py-16"
        aria-labelledby="kill-criteria-heading"
      >
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            id="kill-criteria-heading"
            eyebrow="Committed kill criteria"
            title="Each output has a single sufficient kill condition"
            description="The solar angle θ₁₂ (JUNO), the tensor ratio r (CMB-S4), neutrino ordering, the strong-CP null, dark-energy w, the EM fixed point, the E₈ glue, the flavor invariants, and no second Higgs — each row is sufficient on its own to falsify the construction. m_p/m_e is listed for honesty: it is explicitly not claimed as a compiler power."
          />
          <KillCriteria />
        </div>
      </section>

      <section
        id="no-knobs-section"
        className="relative scroll-mt-20 border-t border-slate-800/60 py-12 sm:py-16"
        aria-labelledby="no-knobs-heading"
      >
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            id="no-knobs-heading"
            eyebrow="No-knobs audit"
            title="Inputs allowed, inputs forbidden, free knobs"
            description="A claim of 'no fitted constants' is only as strong as the audit table behind it. For each TFPT output the matrix records the inputs the construction may use (the two axioms and their consequences), the inputs it explicitly may not use, the number of free parameters available for absorption, the single condition that would falsify the row, and a link to run the check live. The free-knob count is the bar to clear."
          />
          <NoKnobsAudit />
        </div>
      </section>
    </>
  );
}

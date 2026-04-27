import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";
import { KillCriteria } from "@/components/falsification/KillCriteria";
import { NoKnobsAudit } from "@/components/falsification/NoKnobsAudit";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";

export const metadata: Metadata = {
  title: "How to kill TFPT — Falsification Surface and No-Knobs Audit",
  description:
    "An explicit list of falsification surfaces for the TFPT 4.5 series, paired with a no-knobs audit. Each output is shown with its allowed inputs, forbidden inputs, and free-knob count. The construction is killed by any single satisfied criterion.",
  keywords: [
    "TFPT falsification",
    "How to kill TFPT",
    "Topological Fixed-Point Theory falsification",
    "No-knobs audit",
    "Strong-CP null",
    "Cosmic birefringence",
    "EHT achromatic intercept",
    "Axion haloscope",
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
      "Explicit falsification surface for the TFPT 4.5 series, with no-knobs audit. Every output has a stated kill criterion.",
    url: `${SITE_URL}/falsification`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "How to kill TFPT — Falsification Surface",
    description:
      "Each TFPT output ships with its own kill criterion. Free knobs: 0.",
  },
};

const articleJsonLd = {
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  headline: "How to kill TFPT — Falsification Surface and No-Knobs Audit",
  alternateName: "TFPT 4.5 Falsification Map",
  url: `${SITE_URL}/falsification`,
  inLanguage: "en",
  isPartOf: {
    "@type": "PublicationIssue",
    name: "TFPT 4.5 paper series",
  },
  author: [
    { "@type": "Person", name: "Stefan Hamann" },
    { "@type": "Person", name: "Alessandro Rizzo" },
  ],
  abstract:
    "An explicit falsification surface for the TFPT 4.5 series. For every output the page lists allowed inputs, forbidden inputs, free-knob count, and a kill criterion that, if satisfied, falsifies the construction.",
  about: [
    "Falsification",
    "No-knobs audit",
    "Topological Fixed-Point Theory",
    "Strong-CP problem",
    "Cosmic birefringence",
    "EHT polarimetry",
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
            A theory that cannot fail explains nothing. This page lists every
            output of the TFPT 4.5 series together with the experiment or
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
        id="kill-criteria-section"
        className="relative scroll-mt-20 py-12 sm:py-16"
      >
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Per-area kill criteria"
            title="Each output has a single sufficient kill condition"
            description="Carrier theorem, joint discrete solve, electromagnetic closure, strong-CP, Higgs sector, axion haloscope, cosmic birefringence, EHT residual intercept, and the cosmology comparison surface — each row is sufficient on its own to falsify the construction."
          />
          <KillCriteria />
        </div>
      </section>

      <section
        id="no-knobs-section"
        className="relative scroll-mt-20 border-t border-slate-800/60 py-12 sm:py-16"
      >
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="No-knobs audit"
            title="Inputs allowed, inputs forbidden, free knobs"
            description="A claim of 'no fitted constants' is only as strong as the audit table behind it. For each TFPT output, the table below records the inputs the construction may use, the inputs it explicitly may not use, and the number of free parameters available for absorption. The free-knob count is the bar to clear."
          />
          <NoKnobsAudit />
        </div>
      </section>
    </>
  );
}

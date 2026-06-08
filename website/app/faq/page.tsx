import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { HostileRefereeFAQ } from "@/components/HostileRefereeFAQ";
import { FAQ_ITEMS } from "@/lib/faq";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";

export const metadata: Metadata = {
  title: "Hostile-Referee FAQ — The Sharpest Objections, Answered",
  description:
    "The best objections to TFPT, answered directly: is this just E₈ unification, where does experimental input enter, what is fitted, what would kill the theory fastest, and what is still open. With the experimental comparison sources.",
  keywords: [
    "TFPT FAQ",
    "E8 unification objection",
    "Distler Garibaldi",
    "what is fitted",
    "falsification",
    "open gates",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/faq` },
  openGraph: {
    type: "article",
    title: "Hostile-Referee FAQ — TFPT",
    description:
      "The sharpest objections to TFPT, answered: E₈ as audit hull, where input enters, what is fitted, what kills it fastest, and what is open.",
    url: `${SITE_URL}/faq`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "Hostile-Referee FAQ — TFPT",
    description: "The sharpest objections, answered directly.",
  },
};

const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: FAQ_ITEMS.map((item) => ({
    "@type": "Question",
    name: item.q,
    acceptedAnswer: { "@type": "Answer", text: item.a },
  })),
};

export default function FaqPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />

      <section className="relative isolate overflow-hidden pt-12 pb-8 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[460px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(244,63,94,0.3), rgba(99,102,241,0.25), transparent)",
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
          <span className="inline-flex items-center gap-2 rounded-full border border-rose-400/20 bg-rose-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-rose-200">
            <span className="uppercase">Hostile-referee FAQ</span>
          </span>
          <h1 className="mt-6 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl">
            The sharpest objections, <span className="text-gradient-blue">answered</span>.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300">
            A theory at this scope deserves an adversary, not a cheerleader.
            These are the first questions a sceptical physicist asks — E₈,
            &ldquo;Standard Model derived&rdquo;, &ldquo;zero fitted
            constants&rdquo; — answered with the status discipline that backs
            them.
          </p>
        </div>
      </section>

      <section className="relative py-8 sm:py-12">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <HostileRefereeFAQ />
        </div>
      </section>
    </>
  );
}

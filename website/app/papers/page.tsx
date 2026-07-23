import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { PapersSection } from "@/components/PapersSection";
import { DownloadsSection } from "@/components/DownloadsSection";
import { SITE_URL } from "@/lib/utils";
import { SITE_VERSION } from "@/lib/version";

export const metadata: Metadata = {
  title: "Papers — TFPT Document Set",
  description:
    `The full TFPT ${SITE_VERSION} document set: reading guide, five core papers, and four companions — architecture, Standard Model, audit & bootstrap, frontier, Red Team, horizon, Origin Theory, research contracts, safeguards.`,
  alternates: { canonical: `${SITE_URL}/papers` },
  openGraph: {
    type: "website",
    title: "Papers — TFPT Document Set",
    description: `The TFPT ${SITE_VERSION} document set: reading guide, five core papers, four companions.`,
    url: `${SITE_URL}/papers`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
  },
};

export default function PapersIndexPage() {
  return (
    <>
      <div className="mx-auto max-w-7xl px-4 pt-10 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
        >
          <ArrowLeft size={14} aria-hidden />
          Back to start
        </Link>
      </div>
      <PapersSection />
      <DownloadsSection />
    </>
  );
}

import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { papers, STATUS_META } from "@/lib/papers";
import { getReleaseAsset, formatBytes } from "@/lib/release";
import { Math } from "@/components/Math";
import { PaperSection } from "@/components/PaperSection";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";

export function generateStaticParams() {
  return papers.map((p) => ({ slug: p.slug }));
}

interface PaperPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata(
  { params }: PaperPageProps,
): Promise<Metadata> {
  const { slug } = await params;
  const paper = papers.find((p) => p.slug === slug);
  if (!paper) return {};

  const meta = STATUS_META[paper.status];

  // One-sentence description: Inputs → Contribution → Not claimed.
  const oneSentence = [
    paper.contribution[0]
      ? paper.contribution[0]
      : "Single-paper development on the TFPT 4.5 series.",
    paper.notClaimed[0] ? `Not claimed: ${paper.notClaimed[0]}` : null,
  ]
    .filter(Boolean)
    .join(" ");

  const title = `Paper ${paper.number} — ${paper.title}`;

  return {
    title,
    description: oneSentence,
    keywords: [
      "TFPT",
      "Topological Fixed-Point Theory",
      `TFPT Paper ${paper.number}`,
      paper.title,
      paper.subtitle,
      meta.label,
      "Stefan Hamann",
      "Alessandro Rizzo",
    ],
    authors: [
      { name: "Stefan Hamann" },
      { name: "Alessandro Rizzo" },
    ],
    alternates: {
      canonical: `${SITE_URL}/papers/${paper.slug}`,
    },
    openGraph: {
      type: "article",
      title,
      description: oneSentence,
      url: `${SITE_URL}/papers/${paper.slug}`,
      siteName: "TFPT — Topological Fixed-Point Theory",
      locale: "en_US",
      authors: ["Stefan Hamann", "Alessandro Rizzo"],
      tags: [paper.title, meta.label, "TFPT 4.5"],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description: oneSentence,
    },
    other: {
      citation_title: paper.title,
      citation_author: "Hamann, Stefan",
      citation_author_2: "Rizzo, Alessandro",
      citation_publication_date: "2026",
      citation_pdf_url: `${SITE_URL}${paper.pdf}`,
      citation_language: "en",
    },
  };
}

export default async function PaperPage({ params }: PaperPageProps) {
  const { slug } = await params;
  const paper = papers.find((p) => p.slug === slug);
  if (!paper) notFound();

  const meta = STATUS_META[paper.status];
  const release = getReleaseAsset(paper.pdf);
  const idx = papers.findIndex((p) => p.id === paper.id);
  const prev = idx > 0 ? papers[idx - 1] : undefined;
  const next = idx < papers.length - 1 ? papers[idx + 1] : undefined;

  const articleJsonLd = {
    "@context": "https://schema.org",
    "@type": "ScholarlyArticle",
    headline: paper.title,
    alternateName: paper.subtitle,
    abstract: paper.abstract,
    url: `${SITE_URL}/papers/${paper.slug}`,
    inLanguage: "en",
    isPartOf: {
      "@type": "PublicationIssue",
      issueNumber: String(paper.number),
      name: "TFPT 4.5 paper series",
    },
    author: [
      { "@type": "Person", name: "Stefan Hamann" },
      { "@type": "Person", name: "Alessandro Rizzo" },
    ],
    encoding: {
      "@type": "MediaObject",
      contentUrl: `${SITE_URL}${paper.pdf}`,
      encodingFormat: "application/pdf",
      contentSize: release ? `${release.bytes}` : undefined,
      sha256: release?.sha256,
    },
    keywords: paper.keyFormulas.map((k) => k.label).join(", "),
  };

  const breadcrumbJsonLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "TFPT", item: SITE_URL },
      {
        "@type": "ListItem",
        position: 2,
        name: "Papers",
        item: `${SITE_URL}/#papers`,
      },
      {
        "@type": "ListItem",
        position: 3,
        name: `Paper ${paper.number}`,
        item: `${SITE_URL}/papers/${paper.slug}`,
      },
    ],
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleJsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }}
      />

      <section className="relative isolate overflow-hidden pt-12 pb-8 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[500px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(99,102,241,0.4), rgba(168,85,247,0.2), transparent)",
          }}
        />
        <div className="relative mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Breadcrumb" className="mb-4">
            <Link
              href="/#papers"
              className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
            >
              <ArrowLeft size={14} />
              Back to paper series
            </Link>
          </nav>
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full border border-slate-600/40 bg-slate-900/50 px-2.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-widest text-slate-300">
              Paper {paper.number} of the TFPT 4.5 series
            </span>
            <span
              className={`rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1 ${meta.bg} ${meta.color} ${meta.ring}`}
            >
              {meta.label}
            </span>
          </div>
          {release && (
            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-[11px] font-mono text-slate-500">
              <span>{release.version}</span>
              <span>{release.releaseDate}</span>
              <span>{formatBytes(release.bytes)}</span>
              <span title={release.sha256}>
                SHA-256 {release.sha256.slice(0, 8)}…{release.sha256.slice(-4)}
              </span>
            </div>
          )}
        </div>
      </section>

      <PaperSection paper={paper} />

      <section className="relative border-t border-slate-800/60 py-12">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <h2 className="font-serif text-xl font-semibold text-slate-100">
            Key formulas at a glance
          </h2>
          <ul className="mt-4 grid gap-4 md:grid-cols-2">
            {paper.keyFormulas.map((f) => (
              <li
                key={f.label}
                className="rounded-xl border border-slate-700/40 bg-slate-950/40 p-4"
              >
                <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                  {f.label}
                </div>
                <div className="mt-2 overflow-x-auto formula-scroll">
                  <Math block>{f.latex}</Math>
                </div>
                {f.description && (
                  <p className="mt-2 text-xs leading-snug text-slate-400">
                    {f.description}
                  </p>
                )}
              </li>
            ))}
          </ul>
        </div>
      </section>

      <nav
        aria-label="Paper navigation"
        className="mx-auto flex max-w-5xl flex-wrap justify-between gap-4 border-t border-slate-800/60 px-4 py-8 sm:px-6 lg:px-8"
      >
        {prev ? (
          <Link
            href={`/papers/${prev.slug}`}
            className="inline-flex flex-col gap-1 rounded-xl border border-slate-700/40 bg-slate-950/40 p-4 transition-colors hover:bg-slate-900/40"
          >
            <span className="inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
              <ArrowLeft size={11} />
              Previous · Paper {prev.number}
            </span>
            <span className="text-sm font-semibold text-slate-100">
              {prev.title}
            </span>
          </Link>
        ) : (
          <span aria-hidden />
        )}
        {next ? (
          <Link
            href={`/papers/${next.slug}`}
            className="ml-auto inline-flex flex-col gap-1 rounded-xl border border-slate-700/40 bg-slate-950/40 p-4 text-right transition-colors hover:bg-slate-900/40"
          >
            <span className="inline-flex items-center gap-1 self-end text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
              Next · Paper {next.number}
              <ArrowRight size={11} />
            </span>
            <span className="text-sm font-semibold text-slate-100">
              {next.title}
            </span>
          </Link>
        ) : (
          <span aria-hidden />
        )}
      </nav>
    </>
  );
}

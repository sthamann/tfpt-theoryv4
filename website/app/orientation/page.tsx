import type { Metadata } from "next";
import { OrientationHero } from "@/components/orientation/OrientationHero";
import { OrientationFrontBox } from "@/components/orientation/OrientationFrontBox";
import { WhatTfptClaims } from "@/components/orientation/WhatTfptClaims";
import { Decoders } from "@/components/orientation/Decoders";
import { StatusMatrix } from "@/components/orientation/StatusMatrix";
import { SeriesMap } from "@/components/orientation/SeriesMap";
import { PublicationOrder } from "@/components/orientation/PublicationOrder";
import { OrientationDownload } from "@/components/orientation/OrientationDownload";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";

export const metadata: Metadata = {
  title: "TFPT in One Map — The Compiler Closure (Introduction)",
  description:
    "The TFPT 5.0 reading guide. What Topological Fixed-Point Theory claims and does not claim, the compiler closure from two axioms {c₃ = 1/(8π), g_car = 5} to E₈, the two engines, the bootstrap loop, the status matrix, and the document map. By Stefan Hamann & Alessandro Rizzo.",
  keywords: [
    "TFPT introduction",
    "TFPT in one map",
    "Compiler closure",
    "E8 audit hull",
    "Two axioms",
    "Bootstrap loop",
    "Status ledger",
    "Stefan Hamann",
    "Alessandro Rizzo",
    "Topological Fixed-Point Theory",
  ],
  alternates: {
    canonical: `${SITE_URL}/orientation`,
  },
  openGraph: {
    type: "article",
    title: "TFPT in One Map — The Compiler Closure (Introduction)",
    description:
      "The entry document for the TFPT 5.0 set: the compiler closure from two axioms to E₈, the two engines, the bootstrap loop, the status matrix, and the document map.",
    url: `${SITE_URL}/orientation`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    publishedTime: "2026-06-08T00:00:00.000Z",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
    tags: [
      "Topological Fixed-Point Theory",
      "Compiler closure",
      "E8",
      "Standard Model",
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "TFPT in One Map — The Compiler Closure",
    description:
      "What TFPT claims, what it doesn't, the two engines, the bootstrap loop, and the document map.",
  },
};

const articleJsonLd = {
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  headline: "TFPT in One Map — The Compiler Closure (Introduction)",
  alternateName: "Reading guide, status assessment, and the dependency DAG",
  url: `${SITE_URL}/orientation`,
  inLanguage: "en",
  isPartOf: {
    "@type": "PublicationIssue",
    issueNumber: "0",
    name: "TFPT 5.0 compiler-closure document set",
  },
  author: [
    { "@type": "Person", name: "Stefan Hamann" },
    { "@type": "Person", name: "Alessandro Rizzo" },
  ],
  abstract:
    "The entry document for the TFPT 5.0 set. It states what TFPT claims and does not claim, the compiler closure from two axioms to E₈, the two engines, the bootstrap loop, and where each load-bearing argument is isolated in the document set.",
  about: [
    "Compiler closure",
    "Topological Fixed-Point Theory",
    "E8 audit hull",
    "Standard Model",
    "Status discipline",
  ],
  encoding: {
    "@type": "MediaObject",
    contentUrl: `${SITE_URL}/papers/introduction.pdf`,
    encodingFormat: "application/pdf",
  },
};

const breadcrumbJsonLd = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: [
    {
      "@type": "ListItem",
      position: 1,
      name: "TFPT",
      item: SITE_URL,
    },
    {
      "@type": "ListItem",
      position: 2,
      name: "Orientation",
      item: `${SITE_URL}/orientation`,
    },
  ],
};

export default function OrientationPage() {
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

      <OrientationHero />
      <OrientationFrontBox />
      <WhatTfptClaims />
      <Decoders />
      <StatusMatrix />
      <SeriesMap />
      <PublicationOrder />
      <OrientationDownload />
    </>
  );
}

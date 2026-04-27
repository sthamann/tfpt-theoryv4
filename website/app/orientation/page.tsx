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
  title: "TFPT in One Map — Orientation Note (Paper 0)",
  description:
    "The TFPT 4.5 orientation note. What Topological Fixed-Point Theory claims, what it does not claim, the staged reconstruction, the three decoders Y / [u_Σ]=1 / φ₀, the status matrix, the dependency map between Papers 1–6, and the recommended public reading order. By Stefan Hamann & Alessandro Rizzo.",
  keywords: [
    "TFPT orientation",
    "TFPT in one map",
    "Boundary polarization",
    "Carrier rigidity",
    "Three decoders",
    "Status matrix",
    "Series index",
    "Stefan Hamann",
    "Alessandro Rizzo",
    "Topological Fixed-Point Theory",
  ],
  alternates: {
    canonical: `${SITE_URL}/orientation`,
  },
  openGraph: {
    type: "article",
    title: "TFPT in One Map — Orientation Note (Paper 0)",
    description:
      "The public entry document for the TFPT 4.5 series: what is claimed at theorem level, what is downstream, the three decoders, the status matrix, and the dependency map between Papers 1–6.",
    url: `${SITE_URL}/orientation`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    publishedTime: "2026-04-27T00:00:00.000Z",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
    tags: [
      "Topological Fixed-Point Theory",
      "Boundary polarization",
      "Carrier rigidity",
      "Standard Model",
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "TFPT in One Map — Orientation Note",
    description:
      "What TFPT claims, what it doesn't, the three decoders, and the dependency map between Papers 1–6.",
  },
};

const articleJsonLd = {
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  headline: "TFPT in One Map — Orientation Note (Paper 0)",
  alternateName: "Boundary Polarization, Carrier Rigidity, and Observable Closure",
  url: `${SITE_URL}/orientation`,
  inLanguage: "en",
  isPartOf: {
    "@type": "PublicationIssue",
    issueNumber: "0",
    name: "TFPT 4.5 paper series",
  },
  author: [
    { "@type": "Person", name: "Stefan Hamann" },
    { "@type": "Person", name: "Alessandro Rizzo" },
  ],
  abstract:
    "The thin entry document for the TFPT 4.5 series. It states what TFPT claims, what it does not claim, how the closed branch is organized, and where each load-bearing argument is isolated in the paper sequence.",
  about: [
    "Boundary polarization",
    "Topological Fixed-Point Theory",
    "Carrier rigidity",
    "Standard Model",
    "Status discipline",
  ],
  encoding: {
    "@type": "MediaObject",
    contentUrl: `${SITE_URL}/papers/00_orientation_note.pdf`,
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

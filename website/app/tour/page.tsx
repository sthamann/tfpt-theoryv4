import type { Metadata } from "next";
import { TourShell } from "@/components/tour/TourShell";
import { VERIFICATION } from "@/components/tour/tourData";
import { SITE_VERSION } from "@/lib/version";
import { REPO_URL, SITE_URL } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Guided tour — What TFPT claims, in ten steps",
  description:
    `A distill-style guided tour of TFPT ${SITE_VERSION}: two axioms (c₃ = 1/(8π), g_car = 5), the discrete compiler D5 ⊕ A3 + μ4 ⇒ E8, α⁻¹ = 137.0359992, 27 frozen predictions, ${VERIFICATION.pythonModules} machine-checked modules, honesty markers [E]/[C]/[O], open gates, and how to reproduce or falsify — without a “proven TOE” claim.`,
  keywords: [
    "TFPT guided tour",
    "Topological Fixed-Point Theory introduction",
    "two axioms",
    "discrete compiler",
    "E8",
    "frozen predictions",
    "status ledger",
    "SEAM.EQUIV",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/tour` },
  openGraph: {
    type: "article",
    title: "Guided tour — What TFPT claims, in ten steps",
    description:
      "Plain English first, depth on demand: axioms, compiler, outputs, honesty discipline, the thermal seam, how to check it, how it could die, and what is still open.",
    url: `${SITE_URL}/tour`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "TFPT guided tour — ten steps",
    description:
      "Two axioms → discrete compiler → checkable outputs. Honest about open gates and kill tests.",
  },
};

const webpageJsonLd = {
  "@context": "https://schema.org",
  "@type": "WebPage",
  name: "TFPT — Guided tour",
  url: `${SITE_URL}/tour`,
  inLanguage: "en",
  description:
    "A ten-step guided introduction to Topological Fixed-Point Theory: axioms, compiler, outputs, verification, open gates, and falsification.",
  isPartOf: {
    "@type": "WebSite",
    name: "TFPT — Topological Fixed-Point Theory",
    url: SITE_URL,
  },
  author: [
    { "@type": "Person", name: "Stefan Hamann" },
    { "@type": "Person", name: "Alessandro Rizzo" },
  ],
  sameAs: [REPO_URL],
  isBasedOn: REPO_URL,
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
      name: "Guided tour",
      item: `${SITE_URL}/tour`,
    },
  ],
};

const howToJsonLd = {
  "@context": "https://schema.org",
  "@type": "HowTo",
  name: "Understand TFPT in ten steps",
  description:
    "A progressive-disclosure walkthrough from the two axioms to reproduction and falsification.",
  step: [
    {
      "@type": "HowToStep",
      position: 1,
      name: "Two numbers",
      url: `${SITE_URL}/tour#step-two-numbers`,
      text: "Start from c₃ = 1/(8π) and g_car = 5.",
    },
    {
      "@type": "HowToStep",
      position: 2,
      name: "The compiler",
      url: `${SITE_URL}/tour#step-compiler`,
      text: "Discrete compiler D5 ⊕ A3 + μ4 ⇒ E8 ⇒ SM readouts.",
    },
    {
      "@type": "HowToStep",
      position: 3,
      name: "What comes out",
      url: `${SITE_URL}/tour#step-outputs`,
      text: "α⁻¹, mixings, and 27 frozen predictions.",
    },
    {
      "@type": "HowToStep",
      position: 4,
      name: "Why not numerology",
      url: `${SITE_URL}/tour#step-not-numerology`,
      text: "Frozen predictions, null MCs, [E]/[C]/[O]/[X] honesty markers.",
    },
    {
      "@type": "HowToStep",
      position: 5,
      name: "The seam",
      url: `${SITE_URL}/tour#step-seam`,
      text: "Quarter-beat seam clock with T_seam = 4c₃.",
    },
    {
      "@type": "HowToStep",
      position: 6,
      name: "Check it yourself",
      url: `${SITE_URL}/tour#step-check-yourself`,
      text: "Run python run_all.py or use the Pyodide DAG.",
    },
    {
      "@type": "HowToStep",
      position: 7,
      name: "How it could die",
      url: `${SITE_URL}/tour#step-how-it-dies`,
      text: "Kill board, JUNO, and the published v529 toy kill.",
    },
    {
      "@type": "HowToStep",
      position: 8,
      name: "What's still open",
      url: `${SITE_URL}/tour#step-still-open`,
      text: "SEAM.EQUIV [O], the twist-class input bit, interacting seam.",
    },
    {
      "@type": "HowToStep",
      position: 9,
      name: "The two bridges",
      url: `${SITE_URL}/tour#step-two-bridges`,
      text: "Celestial measure chain derived; Woit α→β₂ executed.",
    },
    {
      "@type": "HowToStep",
      position: 10,
      name: "Join in",
      url: `${SITE_URL}/tour#step-join-in`,
      text: "Reproduce, review, falsify via /replication, /review, GitHub.",
    },
  ],
};

export default function TourPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(webpageJsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(howToJsonLd) }}
      />
      <TourShell />
    </>
  );
}

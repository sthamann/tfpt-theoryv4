import type { Metadata, Viewport } from "next";
import "./globals.css";
import "katex/dist/katex.min.css";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { papers } from "@/lib/papers";
import { predictions } from "@/lib/predictions";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";
const SITE_NAME = "TFPT — Topological Fixed-Point Theory";
const SITE_DESCRIPTION =
  "Topological Fixed-Point Theory (TFPT). A boundary-polarized spectral framework that derives the Standard-Model packet, the fine-structure constant α⁻¹(0) = 137.035 999 216 8, the Cabibbo angle, the PMNS matrix, strong-CP closure, and downstream cosmology — from a one-sided boundary datum, with no fitted constants.";

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#0b1220" },
    { media: "(prefers-color-scheme: dark)", color: "#06091a" },
  ],
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  colorScheme: "dark",
};

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${SITE_NAME}: Boundary Polarization, Carrier Rigidity & Observable Closure`,
    template: "%s · TFPT",
  },
  description: SITE_DESCRIPTION,
  applicationName: "TFPT",
  keywords: [
    "TFPT",
    "Topological Fixed-Point Theory",
    "Boundary polarization",
    "Carrier rigidity",
    "Standard Model derivation",
    "Fine-structure constant",
    "Strong CP problem",
    "θ_eff = 0",
    "Cabibbo angle",
    "PMNS matrix",
    "CKM matrix",
    "Calderón polarization",
    "Hodge closure",
    "Boundary spectral theory",
    "Stefan Hamann",
    "Alessandro Rizzo",
    "Theoretical physics",
    "Mathematical physics",
    "α = 137.0359992",
    "Quantum field theory",
    "TFPT 4.5 paper series",
  ],
  authors: [
    { name: "Stefan Hamann" },
    { name: "Alessandro Rizzo" },
  ],
  creator: "Stefan Hamann & Alessandro Rizzo",
  publisher: "TFPT Collaboration",
  category: "science",
  classification: "Theoretical & Mathematical Physics",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    siteName: SITE_NAME,
    title: `${SITE_NAME}: Boundary Polarization, Carrier Rigidity & Observable Closure`,
    description:
      "A boundary-polarized spectral framework that reconstructs the Standard-Model packet and predicts α⁻¹(0), λ_C, sin²θ₁₃, θ_eff = 0, and downstream cosmology — from a one-sided boundary datum, with no fitted constants.",
    locale: "en_US",
    url: SITE_URL,
  },
  twitter: {
    card: "summary_large_image",
    title: SITE_NAME,
    description:
      "A boundary-polarized spectral framework deriving the Standard-Model packet and observable closure — no fitted constants.",
    creator: "@tfpttheory",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
      "max-video-preview": -1,
    },
  },
  alternates: {
    canonical: SITE_URL,
  },
  other: {
    "google-site-verification": process.env.NEXT_PUBLIC_GOOGLE_VERIFICATION || "",
    "citation_title":
      "TFPT — Topological Fixed-Point Theory: Boundary Polarization, Carrier Rigidity & Observable Closure",
    "citation_author": "Hamann, Stefan",
    "citation_author_2": "Rizzo, Alessandro",
    "citation_publication_date": "2026",
    "citation_language": "en",
  },
};

const websiteJsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: SITE_NAME,
  url: SITE_URL,
  description: SITE_DESCRIPTION,
  inLanguage: "en",
  publisher: {
    "@type": "Organization",
    name: "TFPT Collaboration",
    url: SITE_URL,
    member: [
      { "@type": "Person", name: "Stefan Hamann" },
      { "@type": "Person", name: "Alessandro Rizzo" },
    ],
  },
  potentialAction: {
    "@type": "ReadAction",
    target: [`${SITE_URL}/orientation`],
  },
};

const researchProjectJsonLd = {
  "@context": "https://schema.org",
  "@type": "ResearchProject",
  name: SITE_NAME,
  url: SITE_URL,
  description: SITE_DESCRIPTION,
  keywords: [
    "Topological Fixed-Point Theory",
    "Boundary polarization",
    "Carrier rigidity",
    "Standard Model",
    "Fine-structure constant",
    "Strong CP",
    "PMNS",
    "CKM",
  ],
  member: [
    { "@type": "Person", name: "Stefan Hamann" },
    { "@type": "Person", name: "Alessandro Rizzo" },
  ],
  parentOrganization: {
    "@type": "Organization",
    name: "TFPT Collaboration",
  },
  about: [
    "Boundary spectral theory",
    "Calderón polarization",
    "Hodge closure",
    "Standard Model derivation",
    "Strong-CP closure",
  ],
};

const collectionJsonLd = {
  "@context": "https://schema.org",
  "@type": "Collection",
  name: "TFPT 4.5 Paper Series",
  url: `${SITE_URL}#papers`,
  description:
    "The TFPT 4.5 paper series, split by burden of proof: orientation, primitive kernel, carrier rigidity, EM closure, QFT closure, metrology, and cosmology interfaces.",
  hasPart: papers.map((p) => ({
    "@type": "ScholarlyArticle",
    name: p.title,
    headline: p.title,
    alternateName: p.subtitle,
    abstract: p.abstract,
    url: `${SITE_URL}#paper-${p.id}`,
    inLanguage: "en",
    author: [
      { "@type": "Person", name: "Stefan Hamann" },
      { "@type": "Person", name: "Alessandro Rizzo" },
    ],
    isPartOf: {
      "@type": "PublicationIssue",
      name: "TFPT 4.5 paper series",
      issueNumber: String(p.number),
    },
    encoding: {
      "@type": "MediaObject",
      contentUrl: `${SITE_URL}${p.pdf}`,
      encodingFormat: "application/pdf",
    },
  })),
};

const predictionsJsonLd = {
  "@context": "https://schema.org",
  "@type": "Dataset",
  name: "TFPT prediction surface",
  description:
    "Falsifiable predictions of the TFPT closed branch: α⁻¹(0), λ_C, sin²θ₁₃, β cosmic birefringence, strong-CP null θ_eff = 0, axion haloscope window, η_B leptogenesis, Σm_ν, m_ββ, rare kaons, and more.",
  url: `${SITE_URL}#predictions`,
  creator: [
    { "@type": "Person", name: "Stefan Hamann" },
    { "@type": "Person", name: "Alessandro Rizzo" },
  ],
  keywords: predictions.map((p) => p.shortTitle).join(", "),
  variableMeasured: predictions.map((p) => ({
    "@type": "PropertyValue",
    name: p.shortTitle,
    description: p.title,
    value: p.numericValue,
    unitText: p.unit,
  })),
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <head>
        <link
          rel="preconnect"
          href="https://fonts.googleapis.com"
          crossOrigin="anonymous"
        />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Newsreader:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
        />
        <link
          rel="alternate"
          type="application/rdf+xml"
          href="/sitemap.xml"
          title="TFPT sitemap"
        />
        <meta name="format-detection" content="telephone=no" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="apple-mobile-web-app-title" content="TFPT" />
      </head>
      <body className="font-sans antialiased text-slate-200 selection:bg-blue-500/30">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteJsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(researchProjectJsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(collectionJsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(predictionsJsonLd) }}
        />
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:rounded-md focus:bg-slate-900 focus:px-4 focus:py-2 focus:text-white focus:ring-2 focus:ring-blue-400"
        >
          Skip to main content
        </a>
        <Navbar />
        <main id="main" className="pt-16">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}

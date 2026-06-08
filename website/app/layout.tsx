import type { Metadata, Viewport } from "next";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";
import "katex/dist/katex.min.css";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { papers } from "@/lib/papers";
import { predictions } from "@/lib/predictions";
import { REPO_URL } from "@/lib/utils";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";
const SITE_NAME = "TFPT — Topological Fixed-Point Theory";
const SITE_DESCRIPTION =
  "Topological Fixed-Point Theory (TFPT). From two numbers, the seam constant c₃ = 1/(8π) and the carrier rank g_car = 5, a discrete compiler reads off the Standard Model, the constants (α⁻¹ = 137.0359992, 1.9σ from CODATA-2022), the flavor sector and the scale grammar. 20 falsifiable predictions, zero fitted constants; only π is irreducible.";

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
    default: `${SITE_NAME}: Two Axioms, One Compiler, the Standard Model Derived`,
    template: "%s · TFPT",
  },
  description: SITE_DESCRIPTION,
  applicationName: "TFPT",
  keywords: [
    "TFPT",
    "Topological Fixed-Point Theory",
    "Compiler closure",
    "E8 audit hull",
    "Two axioms",
    "Standard Model derivation",
    "Fine-structure constant",
    "Strong CP problem",
    "θ_eff = 0",
    "Cabibbo angle",
    "PMNS matrix",
    "CKM matrix",
    "D5 A3 E8 glue",
    "Bootstrap loop",
    "Coxeter compiler",
    "Stefan Hamann",
    "Alessandro Rizzo",
    "Theoretical physics",
    "Mathematical physics",
    "α = 137.0359992",
    "Quantum field theory",
    "TFPT 5.0",
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
    title: `${SITE_NAME}: Two Axioms, One Compiler, the Standard Model Derived`,
    description:
      "From two numbers, c₃ = 1/(8π) and g_car = 5, a discrete compiler reads off the Standard Model, α⁻¹ = 137.0359992 (1.9σ from CODATA-2022), the flavor sector, strong-CP closure, and the scale grammar. 20 falsifiable predictions, zero fitted constants.",
    locale: "en_US",
    url: SITE_URL,
  },
  twitter: {
    card: "summary_large_image",
    title: SITE_NAME,
    description:
      "Two axioms build E₈; E₈ reads off the Standard Model, the constants, and the scale grammar — no fitted constants, only π irreducible.",
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
    // Highwire Press tags (Google Scholar). The spec defines `citation_author`
    // and expects the meta tag to be repeated once per author. There is no
    // `citation_author_2` — using it makes the second author invisible to
    // Scholar. Next.js renders an array as repeated <meta> elements.
    citation_title:
      "TFPT — Topological Fixed-Point Theory: Two Axioms, One Compiler, the Standard Model Derived",
    citation_author: ["Hamann, Stefan", "Rizzo, Alessandro"],
    citation_publication_date: "2026",
    citation_language: "en",
  },
};

const websiteJsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: SITE_NAME,
  url: SITE_URL,
  description: SITE_DESCRIPTION,
  inLanguage: "en",
  sameAs: [REPO_URL],
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
  sameAs: [REPO_URL],
  keywords: [
    "Topological Fixed-Point Theory",
    "Compiler closure",
    "E8 audit hull",
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
    "Discrete compiler",
    "D5 A3 E8 glue",
    "Coxeter–cyclotomic compiler",
    "Standard Model derivation",
    "Strong-CP closure",
  ],
};

const collectionJsonLd = {
  "@context": "https://schema.org",
  "@type": "Collection",
  name: "TFPT 5.0 Compiler-Closure Document Set",
  url: `${SITE_URL}#papers`,
  description:
    "The TFPT 5.0 document set: the introduction reading guide, the architecture and E₈ compiler, the Standard Model, the E₈ audit and bootstrap, the honest frontier, Appendix H (horizon), the Origin Theory synthesis, and the research contracts.",
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
      name: "TFPT 5.0 compiler-closure document set",
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
    "Falsifiable predictions of the TFPT compiler closure: α⁻¹(0), the solar angle sin²θ₁₂ = 1/3 − φ₀/2, sin²θ₁₃, the inflation tensor ratio r, n_s, A_s, the strong-CP null θ_eff = 0, cosmic birefringence β, Ω_b, η_B, the axion window, and the flavor invariants (det R = 8).",
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
        <Analytics />
      </body>
    </html>
  );
}

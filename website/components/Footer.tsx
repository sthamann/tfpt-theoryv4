"use client";

import Link from "next/link";
import { Logo } from "./Logo";
import { trackPdfDownload, type DownloadKind } from "@/lib/track";

interface FooterLink {
  href: string;
  label: string;
  kind: DownloadKind;
}

const THEORY_MAP: FooterLink = {
  href: "/papers/theory_map.pdf",
  label: "Theory status map (PDF)",
  kind: "theory-map",
};
const SERIES_INDEX: FooterLink = {
  href: "/papers/series_index.pdf",
  label: "Series index",
  kind: "series-index",
};
const TECHNICAL_COMPANION: FooterLink = {
  href: "/papers/technical_companion.pdf",
  label: "Technical companion",
  kind: "companion",
};
const TWO_PAGE_SUMMARY: FooterLink = {
  href: "/predictions/tfpt_two_page_summary.pdf",
  label: "Two-page summary",
  kind: "summary",
};

function trackFooter(link: FooterLink) {
  trackPdfDownload({
    file: link.href,
    source: "footer",
    kind: link.kind,
    title: link.label,
  });
}

export function Footer() {
  return (
    <footer className="relative mt-24 border-t border-slate-800/80 bg-slate-950/60">
      <div className="absolute inset-x-0 -top-px h-px bg-gradient-to-r from-transparent via-blue-500/40 to-transparent" />
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-14 sm:px-6 lg:grid-cols-3 lg:px-8">
        <div>
          <Logo size={40} />
          <p className="mt-4 max-w-md text-sm leading-relaxed text-slate-400">
            Topological Fixed-Point Theory. A boundary-polarized spectral framework
            that derives the Standard-Model packet, predicts α⁻¹(0), the Cabibbo
            angle, the PMNS matrix, and downstream cosmology — from a one-sided
            boundary datum, with no fitted constants.
          </p>
          <p className="mt-4 text-xs text-slate-500">
            By <span className="text-slate-300">Stefan Hamann</span> &amp;{" "}
            <span className="text-slate-300">Alessandro Rizzo</span>.
          </p>
        </div>

        <div>
          <h3 className="font-serif text-sm font-semibold uppercase tracking-wider text-slate-200">
            Theory
          </h3>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <Link href="/#chain" className="text-slate-400 hover:text-white">
                Reconstruction chain
              </Link>
            </li>
            <li>
              <Link href="/#papers" className="text-slate-400 hover:text-white">
                Paper series
              </Link>
            </li>
            <li>
              <Link
                href="/#predictions"
                className="text-slate-400 hover:text-white"
              >
                Prediction surface
              </Link>
            </li>
            <li>
              <Link
                href={THEORY_MAP.href}
                target="_blank"
                rel="noopener"
                onClick={() => trackFooter(THEORY_MAP)}
                className="text-slate-400 hover:text-white"
              >
                {THEORY_MAP.label}
              </Link>
            </li>
          </ul>
        </div>

        <div>
          <h3 className="font-serif text-sm font-semibold uppercase tracking-wider text-slate-200">
            Downloads
          </h3>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <Link
                href="/orientation"
                className="text-slate-400 hover:text-white"
              >
                Orientation note
              </Link>
            </li>
            <li>
              <Link
                href={SERIES_INDEX.href}
                target="_blank"
                rel="noopener"
                onClick={() => trackFooter(SERIES_INDEX)}
                className="text-slate-400 hover:text-white"
              >
                {SERIES_INDEX.label}
              </Link>
            </li>
            <li>
              <Link
                href={TECHNICAL_COMPANION.href}
                target="_blank"
                rel="noopener"
                onClick={() => trackFooter(TECHNICAL_COMPANION)}
                className="text-slate-400 hover:text-white"
              >
                {TECHNICAL_COMPANION.label}
              </Link>
            </li>
            <li>
              <Link
                href={TWO_PAGE_SUMMARY.href}
                target="_blank"
                rel="noopener"
                onClick={() => trackFooter(TWO_PAGE_SUMMARY)}
                className="text-slate-400 hover:text-white"
              >
                {TWO_PAGE_SUMMARY.label}
              </Link>
            </li>
          </ul>
        </div>
      </div>

      <div className="border-t border-slate-800/80 px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-3 text-xs text-slate-500 sm:flex-row sm:items-center">
          <p>
            © {new Date().getFullYear()} Stefan Hamann &amp; Alessandro Rizzo.
            All papers and predictions distributed for academic use.
          </p>
          <p className="text-slate-600">
            TFPT 4.5 series — boundary polarization · carrier rigidity · observable closure
          </p>
        </div>
        <div className="mx-auto mt-3 max-w-7xl text-[11px] leading-relaxed text-slate-600">
          This site uses{" "}
          <Link
            href="https://vercel.com/docs/analytics/privacy-policy"
            target="_blank"
            rel="noopener"
            className="underline decoration-slate-700 underline-offset-2 hover:text-slate-400"
          >
            Vercel Web Analytics
          </Link>{" "}
          for cookie-free, anonymous aggregate page-view and PDF-download
          counts. No personal identifiers, no IP addresses, and no cookies are
          stored.
        </div>
      </div>
    </footer>
  );
}

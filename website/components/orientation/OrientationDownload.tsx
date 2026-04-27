"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { Download, FileText, ArrowRight } from "lucide-react";
import { trackPdfDownload, type DownloadKind } from "@/lib/track";

const ORIENTATION_PDF = "/papers/00_orientation_note.pdf";
const ORIENTATION_TITLE = "TFPT in One Map (Paper 0)";

interface SidebarLink {
  href: string;
  label: string;
  desc: string;
  kind: DownloadKind;
}

const SIDEBAR_LINKS: SidebarLink[] = [
  {
    href: "/papers/series_index.pdf",
    label: "Series index",
    desc: "Working index, dependency split",
    kind: "series-index",
  },
  {
    href: "/papers/theory_map.pdf",
    label: "Theory status map",
    desc: "Status of the staged derivation chain",
    kind: "theory-map",
  },
  {
    href: "/predictions/tfpt_two_page_summary.pdf",
    label: "Two-page summary",
    desc: "Compact claim + prediction surface",
    kind: "summary",
  },
];

export function OrientationDownload() {
  return (
    <section
      id="download"
      className="relative scroll-mt-24 py-20 sm:py-24"
      aria-labelledby="download-heading"
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.7 }}
          className="relative overflow-hidden rounded-3xl border border-slate-700/50 bg-slate-950/60 p-8 sm:p-12"
        >
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 -z-10"
            style={{
              background:
                "radial-gradient(ellipse 60% 80% at 100% 0%, rgba(99,102,241,0.18), transparent 50%), radial-gradient(ellipse 60% 80% at 0% 100%, rgba(236,72,153,0.14), transparent 50%)",
            }}
          />

          <div className="grid gap-8 lg:grid-cols-[1.4fr_1fr] lg:items-center">
            <div>
              <h2
                id="download-heading"
                className="font-serif text-3xl font-semibold leading-tight text-slate-50 sm:text-4xl"
              >
                Read the full orientation note.
              </h2>
              <p className="mt-3 max-w-xl text-base leading-relaxed text-slate-300">
                Paper 0 is the public entry document of the TFPT 4.5 series. It
                states the staged reconstruction, the three decoders, the status
                matrix, and the dependency map between the six papers — without
                imported numerics, without invisible assumptions.
              </p>

              <div className="mt-6 flex flex-wrap gap-3">
                <Link
                  href={ORIENTATION_PDF}
                  target="_blank"
                  rel="noopener"
                  onClick={() =>
                    trackPdfDownload({
                      file: ORIENTATION_PDF,
                      source: "orientation-download",
                      kind: "paper",
                      title: ORIENTATION_TITLE,
                    })
                  }
                  className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/30 ring-1 ring-blue-400/40 transition-transform hover:scale-105 focus:scale-105"
                >
                  <Download size={16} />
                  Download Paper 0 (PDF)
                </Link>
                <Link
                  href={ORIENTATION_PDF}
                  target="_blank"
                  rel="noopener"
                  onClick={() =>
                    trackPdfDownload({
                      file: ORIENTATION_PDF,
                      source: "orientation-download",
                      kind: "paper",
                      title: ORIENTATION_TITLE,
                    })
                  }
                  className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-6 py-3 text-sm font-semibold text-slate-100 backdrop-blur transition-colors hover:bg-slate-800/80"
                >
                  <FileText size={16} />
                  View in browser
                </Link>
              </div>

              <ul className="mt-8 grid gap-2 text-xs text-slate-400 sm:grid-cols-3">
                <li>· Stefan Hamann</li>
                <li>· Alessandro Rizzo</li>
                <li>· TFPT 4.5 paper series</li>
              </ul>
            </div>

            <div className="space-y-3">
              {SIDEBAR_LINKS.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  target="_blank"
                  rel="noopener"
                  onClick={() =>
                    trackPdfDownload({
                      file: link.href,
                      source: "orientation-sidebar",
                      kind: link.kind,
                      title: link.label,
                    })
                  }
                  className="group flex items-center justify-between rounded-xl border border-slate-700/40 bg-slate-950/40 p-4 transition-colors hover:bg-slate-900/40"
                >
                  <div>
                    <div className="font-serif text-sm font-semibold text-slate-100">
                      {link.label}
                    </div>
                    <div className="text-xs text-slate-400">{link.desc}</div>
                  </div>
                  <ArrowRight
                    size={16}
                    className="text-slate-500 transition-transform group-hover:translate-x-0.5 group-hover:text-slate-200"
                  />
                </Link>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

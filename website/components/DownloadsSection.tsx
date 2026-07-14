"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ArrowUpRight, Copy, Download, FileText, Github } from "lucide-react";
import { papers, STATUS_META, paperLabel } from "@/lib/papers";
import { cn, REPO_URL } from "@/lib/utils";
import { SectionHeader } from "./SectionHeader";
import { trackPdfInteraction } from "@/lib/track";
import {
  getReleaseAsset,
  formatBytes,
  formatHashShort,
} from "@/lib/release";
import { SITE_VERSION } from "@/lib/version";

export function DownloadsSection() {
  return (
    <section
      id="downloads"
      className="relative scroll-mt-20 py-24 sm:py-32"
      aria-labelledby="downloads-heading"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Downloads"
          title="Every document, in one place"
          description={`The full TFPT ${SITE_VERSION} document set — the introduction reading guide, the five numbered documents (architecture, Standard Model, audit & bootstrap, frontier, Red Team), and the three companions (Appendix H, the Origin Theory synthesis, and the research contracts). All distributed for academic use.`}
        />

        <div className="mt-12">
          <h3 className="font-serif text-lg font-semibold text-slate-100">
            The document set
          </h3>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {papers.map((p, i) => {
              const meta = STATUS_META[p.status];
              const release = getReleaseAsset(p.pdf);
              return (
                <motion.div
                  key={p.id}
                  initial={{ opacity: 0, y: 12 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.05 }}
                  transition={{ duration: 0.5, delay: i * 0.05 }}
                  className="group glass relative flex flex-col overflow-hidden rounded-xl ring-1 ring-slate-700/40 transition-all hover:ring-slate-500/60"
                >
                  <div
                    className={cn(
                      "absolute inset-x-0 top-0 h-px bg-gradient-to-r",
                      meta.gradient,
                    )}
                  />
                  <div className="flex flex-1 flex-col p-5">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full border border-slate-600/40 bg-slate-900/50 px-2.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-widest text-slate-300">
                        {paperLabel(p)}
                      </span>
                      <span
                        className={cn(
                          "rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1",
                          meta.bg,
                          meta.color,
                          meta.ring,
                        )}
                      >
                        {meta.label}
                      </span>
                    </div>
                    <h4 className="mt-3 font-serif text-base font-semibold leading-snug text-slate-50">
                      {p.title}
                    </h4>
                    <p className="mt-1 text-xs leading-relaxed text-slate-400">
                      {p.subtitle}
                    </p>

                    {release && <ReleaseLine release={release} />}

                    <div className="mt-auto flex items-center gap-3 pt-4">
                      <Link
                        href={p.pdf}
                        target="_blank"
                        rel="noopener"
                        onClick={() =>
                          trackPdfInteraction({
                            file: p.pdf,
                            source: "downloads-papers",
                            kind: "paper",
                            interaction: "download",
                            title: p.title,
                          })
                        }
                        className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-300 transition-colors hover:text-blue-200"
                      >
                        <Download size={13} />
                        Download
                      </Link>
                      <Link
                        href={p.pdf}
                        target="_blank"
                        rel="noopener"
                        onClick={() =>
                          trackPdfInteraction({
                            file: p.pdf,
                            source: "downloads-papers",
                            kind: "paper",
                            interaction: "view",
                            title: p.title,
                          })
                        }
                        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-300 transition-colors hover:text-slate-100"
                      >
                        <FileText size={13} />
                        View
                      </Link>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>

          {(() => {
            const changelog = getReleaseAsset("/papers/changelog.pdf");
            if (!changelog) return null;
            return (
              <div className="mt-6 flex flex-col gap-3 rounded-xl border border-slate-700/40 bg-slate-900/40 p-4 sm:flex-row sm:items-center sm:justify-between sm:p-5">
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <FileText size={16} className="flex-none text-slate-300" aria-hidden />
                    <h4 className="font-serif text-sm font-semibold text-slate-100">
                      Changelog — the dated record of every change
                    </h4>
                  </div>
                  <p className="mt-1 text-xs leading-relaxed text-slate-400">
                    {changelog.changelog}
                  </p>
                  <ReleaseLine release={changelog} compact />
                </div>
                <Link
                  href="/papers/changelog.pdf"
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={() =>
                    trackPdfInteraction({
                      file: "/papers/changelog.pdf",
                      source: "downloads-papers",
                      kind: "paper",
                      interaction: "download",
                      title: "Changelog",
                    })
                  }
                  className="inline-flex flex-none items-center gap-2 rounded-full border border-slate-600/50 bg-slate-900/60 px-4 py-2 text-xs font-semibold text-slate-200 transition-colors hover:border-slate-400/60 hover:text-white"
                >
                  <Download size={14} aria-hidden />
                  Changelog (PDF)
                </Link>
              </div>
            );
          })()}
        </div>

        <div className="mt-14 overflow-hidden rounded-2xl border border-blue-400/25 bg-gradient-to-br from-blue-500/10 to-violet-500/5 p-6 sm:p-8">
          <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr] lg:items-center">
            <div>
              <div className="flex items-center gap-2">
                <Github size={18} className="text-slate-200" aria-hidden />
                <h3 className="font-serif text-lg font-semibold text-slate-100">
                  Reproducibility — everything is on GitHub
                </h3>
              </div>
              <p className="mt-3 max-w-2xl text-sm leading-relaxed text-slate-300">
                Every claim marked exact identity, lattice theorem or numerical
                fixed point is re-derived from the two axioms by a self-contained
                Python verification suite, mirrored in an independent Wolfram
                path, and recorded in a single machine-checked status ledger. The
                carrier algebra (P2) is Lean-formalised (0 sorry, only kernel
                axioms). The full source — theory documents, scripts and ledger —
                lives in one public repository. If the text and the ledger ever
                disagree, the ledger wins.
              </p>
              <div className="mt-4 flex flex-wrap gap-2">
                {[
                  "Python verification suite",
                  "Independent Wolfram mirror",
                  "Lean-formalised carrier (P2)",
                  "Versioned status ledger",
                ].map((t) => (
                  <span
                    key={t}
                    className="rounded-full border border-slate-700/40 bg-slate-900/50 px-3 py-1 text-[11px] font-medium text-slate-300"
                  >
                    {t}
                  </span>
                ))}
              </div>
            </div>
            <div className="flex flex-col items-start gap-2 lg:items-end">
              <Link
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
              >
                <Github size={16} />
                View the source &amp; verification suite
                <ArrowUpRight size={16} />
              </Link>
              <span className="font-mono text-[11px] text-slate-500">
                github.com/sthamann/tfpt
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function ReleaseLine({
  release,
  compact = false,
}: {
  release: ReturnType<typeof getReleaseAsset> & object;
  compact?: boolean;
}) {
  const handleCopy = async () => {
    try {
      if (typeof navigator !== "undefined" && navigator.clipboard) {
        await navigator.clipboard.writeText(release.sha256);
      }
    } catch {
      // Clipboard API may be unavailable on insecure origins. Silent fallback.
    }
  };

  return (
    <dl
      className={cn(
        "mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 rounded-md border border-slate-800/60 bg-slate-950/60 px-2.5 py-1.5 text-[10px] text-slate-400",
        compact && "mt-2",
      )}
    >
      <div className="flex items-center gap-1">
        <dt className="font-semibold uppercase tracking-widest text-blue-300/80">
          Version
        </dt>
        <dd className="font-mono text-slate-200">{release.version}</dd>
      </div>
      <div className="flex items-center gap-1">
        <dt className="font-semibold uppercase tracking-widest text-blue-300/80">
          Date
        </dt>
        <dd className="font-mono text-slate-200">{release.releaseDate}</dd>
      </div>
      <div className="flex items-center gap-1">
        <dt className="font-semibold uppercase tracking-widest text-blue-300/80">
          Size
        </dt>
        <dd className="font-mono text-slate-200">{formatBytes(release.bytes)}</dd>
      </div>
      <div className="flex items-center gap-1">
        <dt className="font-semibold uppercase tracking-widest text-blue-300/80">
          SHA-256
        </dt>
        <dd className="font-mono text-slate-200" title={release.sha256}>
          {formatHashShort(release.sha256)}
        </dd>
        <button
          type="button"
          onClick={handleCopy}
          aria-label={`Copy SHA-256 hash to clipboard (${release.sha256})`}
          className="rounded p-0.5 text-slate-500 transition-colors hover:bg-slate-800/60 hover:text-slate-200"
          title="Copy full SHA-256"
        >
          <Copy size={11} aria-hidden />
        </button>
      </div>
      {release.changelog && (
        <div className="basis-full text-[10px] leading-snug text-slate-500">
          <span className="font-semibold text-slate-400">Changelog.</span>{" "}
          {release.changelog}
        </div>
      )}
    </dl>
  );
}

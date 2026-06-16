"use client";

import { useState } from "react";
import Link from "next/link";
import { Check, Copy, Download, Github } from "lucide-react";
import { REPO_URL } from "@/lib/utils";

interface CitationBoxProps {
  title: string;
  slug: string;
  canonicalUrl: string;
  pdfUrl: string;
  version?: string;
  releaseDate?: string;
  sha256?: string;
  statusLabel: string;
}

/**
 * A self-contained citation pack for a single document: a copyable BibTeX
 * entry plus the verifiable facts a reviewer needs (version, date, SHA-256,
 * status, source). Everything is derived from the release manifest — no
 * fabricated DOI is shown, since the archival DOI is the document-set deposit,
 * not a per-paper identifier.
 */
export function CitationBox({
  title,
  slug,
  canonicalUrl,
  pdfUrl,
  version,
  releaseDate,
  sha256,
  statusLabel,
}: CitationBoxProps) {
  const [copied, setCopied] = useState(false);

  const year = releaseDate ? releaseDate.slice(0, 4) : "2026";
  const noteParts = [version, releaseDate].filter(Boolean).join(", ");
  const shaNote = sha256 ? `, PDF SHA-256 ${sha256}` : "";

  const bibtex = `@misc{tfpt_${slug.replace(/-/g, "_")}_${year},
  title        = {${title}},
  author       = {Hamann, Stefan and Rizzo, Alessandro},
  year         = {${year}},
  howpublished = {\\url{${canonicalUrl}}},
  url          = {${pdfUrl}},
  note         = {${noteParts}${shaNote}}
}`;

  async function copy() {
    try {
      await navigator.clipboard.writeText(bibtex);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard API unavailable (e.g. insecure context) — the textarea below
      // still lets the user select and copy manually.
    }
  }

  const facts: { label: string; value: string }[] = [
    { label: "Authors", value: "Stefan Hamann, Alessandro Rizzo" },
    ...(version ? [{ label: "Version", value: version }] : []),
    ...(releaseDate ? [{ label: "Date", value: releaseDate }] : []),
    { label: "Claim status", value: statusLabel },
    ...(sha256 ? [{ label: "PDF SHA-256", value: sha256 }] : []),
  ];

  return (
    <section
      aria-labelledby="cite-heading"
      className="relative border-t border-slate-800/60 py-12"
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <h2 id="cite-heading" className="font-serif text-xl font-semibold text-slate-100">
          Cite this document
        </h2>
        <p className="mt-2 max-w-2xl text-sm text-slate-400">
          A reproducible citation pack: the BibTeX entry plus the verifiable
          release facts. The PDF SHA-256 pins the exact bytes; the source and
          ledger are public.
        </p>

        <div className="mt-5 grid gap-5 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)]">
          {/* BibTeX */}
          <div className="overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/70">
            <div className="flex items-center justify-between gap-2 border-b border-slate-800/60 px-4 py-2.5">
              <span className="font-mono text-[11px] uppercase tracking-widest text-slate-400">
                BibTeX
              </span>
              <button
                type="button"
                onClick={copy}
                className="inline-flex items-center gap-1.5 rounded-full border border-slate-600/60 bg-slate-900/60 px-3 py-1 text-[11px] font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
                aria-label="Copy the BibTeX citation to the clipboard"
              >
                {copied ? <Check size={12} aria-hidden /> : <Copy size={12} aria-hidden />}
                {copied ? "Copied" : "Copy"}
              </button>
            </div>
            <pre className="overflow-x-auto px-4 py-3 text-[12px] leading-relaxed text-slate-200">
              <code className="font-mono">{bibtex}</code>
            </pre>
            <span aria-live="polite" className="sr-only">
              {copied ? "BibTeX citation copied to clipboard" : ""}
            </span>
          </div>

          {/* Facts + links */}
          <div className="flex flex-col gap-4">
            <dl className="grid grid-cols-1 gap-2">
              {facts.map((f) => (
                <div
                  key={f.label}
                  className="flex flex-col gap-0.5 rounded-xl border border-slate-700/40 bg-slate-950/40 px-4 py-2.5"
                >
                  <dt className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                    {f.label}
                  </dt>
                  <dd className="break-all font-mono text-xs text-slate-200">{f.value}</dd>
                </div>
              ))}
            </dl>
            <div className="flex flex-wrap gap-2">
              <Link
                href={pdfUrl}
                target="_blank"
                rel="noopener"
                className="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-4 py-2 text-xs font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
              >
                <Download size={13} aria-hidden />
                PDF
              </Link>
              <Link
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 rounded-full border border-slate-600/60 bg-slate-900/60 px-4 py-2 text-xs font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
              >
                <Github size={13} aria-hidden />
                Source &amp; ledger
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

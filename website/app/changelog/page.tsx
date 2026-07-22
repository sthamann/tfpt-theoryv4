import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, FileText, Github } from "lucide-react";
import {
  ChangelogBrowser,
  type ChangelogDayEntry,
  type ChangelogIndexEntry,
  type DayMeta,
} from "@/components/ChangelogBrowser";
import {
  CHANGELOG,
  CHANGELOG_COUNT,
  CHANGELOG_MACROS,
  type ChangelogNode,
} from "@/lib/changelog";
import { REPO_URL, SITE_URL } from "@/lib/utils";
import { SITE_VERSION } from "@/lib/version";

const latest = CHANGELOG[0]?.date ?? "";
const earliest = CHANGELOG[CHANGELOG.length - 1]?.date ?? "";

export const metadata: Metadata = {
  title: "Changelog — Every Change and New Result, by Date",
  description:
    "The canonical, dated record of every change to TFPT: new verification modules (vN), status changes, editorial passes and infrastructure. Browse day by day, filter by module, claim or status. Mirrored from the repository's changelog and kept in lock-step with the theory, the verification suite and the papers.",
  keywords: [
    "TFPT changelog",
    "verification modules",
    "status ledger",
    "release notes",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/changelog` },
  openGraph: {
    type: "article",
    title: "TFPT Changelog — every change, by date",
    description:
      "The dated record of every TFPT change: verification modules, status changes, papers and infrastructure. The single source is the repository changelog.",
    url: `${SITE_URL}/changelog`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "TFPT Changelog",
    description: "Every change and new result, by date.",
  },
};

// --------------------------------------------------------------------------
// Server-side derivation of the browsing data. The full CHANGELOG (node trees,
// ~2 MB) stays server-only; the client receives the tiny day list, a compact
// searchable index and just the selected day's full entries.
// --------------------------------------------------------------------------

function nodesToText(nodes: ChangelogNode[]): string {
  return nodes
    .map((n) => {
      if (n.k === "t" || n.k === "m" || n.k === "c") return n.v ?? "";
      if (n.k === "s") return `[${n.v ?? "O"}]`;
      if ((n.k === "b" || n.k === "i") && n.c) return nodesToText(n.c);
      return "";
    })
    .join("");
}

function collectMarkers(nodes: ChangelogNode[], into: Set<string>): void {
  for (const n of nodes) {
    if (n.k === "s" && n.v) into.add(n.v);
    if ((n.k === "b" || n.k === "i") && n.c) collectMarkers(n.c, into);
  }
}

function hasModuleCode(nodes: ChangelogNode[]): boolean {
  return nodes.some((n) => {
    if (n.k === "c" && n.v && /^v\d+/.test(n.v)) return true;
    if ((n.k === "b" || n.k === "i") && n.c) return hasModuleCode(n.c);
    return false;
  });
}

const EXPERIMENT_RE = /experiments?\s+level\s+only|experiment-level|experiments\//i;
const EDITORIAL_RE = /\beditorial\b/i;

/** Assign an entry to a theory area from its claim ids / keywords. Heuristic
 *  navigational aid (not a load-bearing claim); first match wins. `text` is the
 *  already-lowercased search blob. */
function classifyArea(text: string, tags: string[]): string {
  if (/celest\.|celestial|twistor|\bwp5|bcov|\bwoit\b|costello|burns holograph/.test(text))
    return "celestial";
  if (/seam\.|seam\b|qgeo|pillowcase|\bclock\b|m(?:ö|oe)bius|\bfock\b|orbifold|\bdeck\b|kronheimer|steklov|\bmarks?\b/.test(text))
    return "seam";
  if (/\bp2\.|ax\.p2|\bcarrier\b|g_car|g_\{|partition corollary|deligne|weight[- ]typing/.test(text))
    return "p2";
  if (/alpha\.quillen|em\.ward|fine-structure|quillen|determinant line/.test(text))
    return "em";
  if (/flav\.|fr\.rarekaon|\bckm\b|koide|yukawa|\bpmns\b|lepton|quark|neutrino|\bkaon\b|jarlskog|cabibbo|seesaw|clebsch/.test(text))
    return "flavor";
  if (/cosmo\.|gravit|einstein|\blambda\b|inflation|leptogenesis|axion|n_s|scalaron|entropic|hubble|\bh_?0\b|reheating|running/.test(text))
    return "gravity";
  if (/\bhor\.|horizon|nariai|black[- ]hole|\bbh\b|\beht\b/.test(text))
    return "horizon";
  if (tags.includes("experiment") || /\bfrb\b|pulsar|\brxte\b|\bnicer\b|hfqpo|glitch|\bvela\b|recovery-comb|e8-ladder|efimov|burst/.test(text))
    return "experiment";
  if (tags.includes("editorial") || /registry|manifest|wolfram|website|currency sweep|cross-reference|gitignore|consolidation/.test(text))
    return "infra";
  return "core";
}

/** Extract the enumerator (e.g. "XXIII") that make_changelog_web.py appends to
 *  the date label as "YYYY-MM-DD · XXIII". */
function enumOf(label: string): string {
  const parts = label.split(" \u00b7 ");
  return parts.length > 1 ? parts[parts.length - 1].trim() : "";
}

function clip(s: string, n: number): string {
  const t = s.replace(/\s+/g, " ").trim();
  return t.length > n ? t.slice(0, n).trimEnd() + "\u2026" : t;
}

interface DerivedEntry {
  gi: number;
  date: string;
  label: string;
  enumr: string;
  heading: ChangelogNode[];
  items: ChangelogNode[][];
  anchor: string;
  lead: string;
  text: string;
  tags: string[];
  area: string;
}

function deriveEntry(entry: (typeof CHANGELOG)[number], gi: number): DerivedEntry {
  const allNodes: ChangelogNode[] = [
    ...entry.heading,
    ...entry.items.flat(),
  ];
  const fullText = [entry.heading, ...entry.items]
    .map((nodes) => nodesToText(nodes))
    .join(" ");

  const markers = new Set<string>();
  collectMarkers(allNodes, markers);

  const tags: string[] = [];
  if (hasModuleCode(allNodes)) tags.push("module");
  if (EDITORIAL_RE.test(fullText)) tags.push("editorial");
  if (EXPERIMENT_RE.test(fullText)) tags.push("experiment");
  for (const m of markers) tags.push(m);

  const leadSource =
    entry.heading.length > 0
      ? nodesToText(entry.heading)
      : entry.items.length > 0
        ? nodesToText(entry.items[0])
        : "";

  const text = clip(fullText, 900).toLowerCase();

  return {
    gi,
    date: entry.date,
    label: entry.dateLabel,
    enumr: enumOf(entry.dateLabel),
    heading: entry.heading,
    items: entry.items,
    anchor: `cl-${gi}`,
    lead: clip(leadSource, 220),
    text,
    tags,
    area: classifyArea(text, tags),
  };
}

export default async function ChangelogPage({
  searchParams,
}: {
  searchParams: Promise<{ day?: string }>;
}) {
  const derived = CHANGELOG.map((e, i) => deriveEntry(e, i));

  // Day list (newest first, CHANGELOG order preserved), with per-day counts.
  const days: DayMeta[] = [];
  const dayPos = new Map<string, number>();
  for (const e of derived) {
    const at = dayPos.get(e.date);
    if (at === undefined) {
      dayPos.set(e.date, days.length);
      days.push({ date: e.date, count: 1 });
    } else {
      days[at].count += 1;
    }
  }

  const sp = await searchParams;
  const selectedDay =
    sp.day && dayPos.has(sp.day) ? sp.day : days[0]?.date ?? "";

  const dayEntries: ChangelogDayEntry[] = derived
    .filter((e) => e.date === selectedDay)
    .map((e) => ({
      label: e.label,
      enumr: e.enumr,
      heading: e.heading,
      items: e.items,
      anchor: e.anchor,
      area: e.area,
    }));

  const index: ChangelogIndexEntry[] = derived.map((e) => ({
    date: e.date,
    label: e.label,
    enumr: e.enumr,
    lead: e.lead,
    text: e.text,
    anchor: e.anchor,
    tags: e.tags,
    area: e.area,
  }));

  return (
    <>
      <section className="relative isolate overflow-hidden pt-12 pb-8 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[460px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(59,130,246,0.3), rgba(139,92,246,0.25), transparent)",
          }}
        />
        <div className="relative mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Breadcrumb" className="mb-6">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
            >
              <ArrowLeft size={14} />
              Back to overview
            </Link>
          </nav>
          <span className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-blue-200">
            <span className="uppercase">Changelog</span>
            <span aria-hidden className="text-blue-400/60">·</span>
            <span className="font-mono">{CHANGELOG_COUNT} entries</span>
            <span aria-hidden className="text-blue-400/60">·</span>
            <span className="font-mono">{days.length} days</span>
          </span>
          <h1 className="mt-6 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl">
            Every change and new result,{" "}
            <span className="text-gradient-blue">by date</span>.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300">
            The canonical, dated record of the TFPT development: new
            verification modules (<code className="font-mono text-slate-200">vN</code>),
            status changes, editorial passes and infrastructure. Browse one day
            at a time, step between days, or filter across every entry. This page
            is generated directly from the repository&rsquo;s{" "}
            <code className="font-mono text-slate-200">changelog.tex</code>, so it
            never drifts from the source. Module numbers refer to{" "}
            <code className="font-mono text-slate-200">verification/vN_*.py</code>;
            claim IDs refer to rows of the status ledger.
          </p>
          <div className="mt-6 flex flex-wrap items-center gap-3">
            <Link
              href="/papers/changelog.pdf"
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
            >
              <FileText size={15} aria-hidden />
              Changelog (PDF)
            </Link>
            <Link
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium text-slate-300 ring-1 ring-slate-700/50 transition-colors hover:bg-white/5 hover:text-white"
            >
              <Github size={15} aria-hidden />
              Repository
            </Link>
            {latest && (
              <span className="font-mono text-xs text-slate-500">
                TFPT {SITE_VERSION} · {earliest} → {latest}
              </span>
            )}
          </div>

          <dl className="mt-6 flex flex-wrap gap-x-5 gap-y-1.5 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <span className="rounded bg-emerald-500/10 px-1 font-mono font-semibold text-emerald-300 ring-1 ring-emerald-400/30">
                [E]
              </span>
              <dd>exact / proven</dd>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="rounded bg-amber-500/10 px-1 font-mono font-semibold text-amber-300 ring-1 ring-amber-400/30">
                [C]
              </span>
              <dd>conditional</dd>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="rounded bg-slate-500/10 px-1 font-mono font-semibold text-slate-300 ring-1 ring-slate-400/30">
                [O]
              </span>
              <dd>open / axiom</dd>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="rounded bg-rose-500/10 px-1 font-mono font-semibold text-rose-300 ring-1 ring-rose-400/30">
                [X]
              </span>
              <dd>kill test</dd>
            </div>
          </dl>
        </div>
      </section>

      <section className="relative py-8 sm:py-12">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <ChangelogBrowser
            days={days}
            index={index}
            selectedDay={selectedDay}
            entries={dayEntries}
            macros={CHANGELOG_MACROS}
          />
        </div>
      </section>
    </>
  );
}

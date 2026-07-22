"use client";

import {
  Fragment,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import katex from "katex";
import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Search,
  X as XIcon,
} from "lucide-react";
import type { ChangelogNode } from "@/lib/changelog";
import { cn } from "@/lib/utils";

/**
 * Interactive changelog browser.
 *
 * The changelog has hundreds of very long entries. The page pages by DAY
 * (latest first), lets you step between days, and filter across every entry.
 * Each entry is a collapsible card: a theory-area badge + a capitalised title +
 * a plain quick summary up front, then the numbered key points and the detail
 * log on expand. Inline formulas are KaTeX-rendered in a cyan tint so they
 * stand out from the prose.
 *
 * Only the selected day's node trees are shipped from the server; a compact
 * index powers the global filter without shipping the full ~2 MB data.
 */

export interface DayMeta {
  date: string;
  count: number;
}

export interface ChangelogIndexEntry {
  date: string;
  label: string;
  enumr: string;
  lead: string;
  text: string;
  anchor: string;
  tags: string[];
  area: string;
}

export interface ChangelogDayEntry {
  label: string;
  enumr: string;
  heading: ChangelogNode[];
  items: ChangelogNode[][];
  anchor: string;
  area: string;
}

interface Props {
  days: DayMeta[];
  index: ChangelogIndexEntry[];
  selectedDay: string;
  entries: ChangelogDayEntry[];
  macros: Record<string, string>;
}

const MONTHS = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

function formatDay(iso: string): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if (!m) return iso;
  const [, y, mo, d] = m;
  return `${parseInt(d, 10)} ${MONTHS[parseInt(mo, 10) - 1]} ${y}`;
}

const MARKER: Record<string, { cls: string; title: string }> = {
  E: {
    cls: "bg-emerald-500/10 text-emerald-300 ring-emerald-400/30",
    title: "Exact / machine-proven (identity, lattice, formalised, numerical fixed point)",
  },
  C: {
    cls: "bg-amber-500/10 text-amber-300 ring-amber-400/30",
    title: "Conditional (physical / bridge / readout, under named hypotheses)",
  },
  O: {
    cls: "bg-slate-500/10 text-slate-300 ring-slate-400/30",
    title: "Open / axiom",
  },
  X: {
    cls: "bg-rose-500/10 text-rose-300 ring-rose-400/30",
    title: "Falsifiable kill test",
  },
};

const MARKER_ORDER = ["E", "C", "O", "X"];

/** Theory areas (navigational aid). Keys match classifyArea() in page.tsx. */
const AREA_META: Record<string, { label: string; cls: string; dot: string }> = {
  celestial: { label: "Celestial route", cls: "bg-violet-500/10 text-violet-200 ring-violet-400/30", dot: "bg-violet-400" },
  seam: { label: "Seam & QGEO", cls: "bg-blue-500/10 text-blue-200 ring-blue-400/30", dot: "bg-blue-400" },
  p2: { label: "P2 & carrier", cls: "bg-cyan-500/10 text-cyan-200 ring-cyan-400/30", dot: "bg-cyan-400" },
  em: { label: "EM fixed point", cls: "bg-amber-500/10 text-amber-200 ring-amber-400/30", dot: "bg-amber-400" },
  flavor: { label: "Flavor & masses", cls: "bg-emerald-500/10 text-emerald-200 ring-emerald-400/30", dot: "bg-emerald-400" },
  gravity: { label: "Gravity & cosmology", cls: "bg-sky-500/10 text-sky-200 ring-sky-400/30", dot: "bg-sky-400" },
  horizon: { label: "Horizon & BH", cls: "bg-indigo-500/10 text-indigo-200 ring-indigo-400/30", dot: "bg-indigo-400" },
  experiment: { label: "Experiments", cls: "bg-rose-500/10 text-rose-200 ring-rose-400/30", dot: "bg-rose-400" },
  infra: { label: "Infrastructure", cls: "bg-slate-500/10 text-slate-300 ring-slate-400/30", dot: "bg-slate-400" },
  core: { label: "Compiler core", cls: "bg-fuchsia-500/10 text-fuchsia-200 ring-fuchsia-400/30", dot: "bg-fuchsia-400" },
};

const AREA_ORDER = [
  "celestial", "seam", "p2", "em", "flavor",
  "gravity", "horizon", "experiment", "infra", "core",
];

function StatusMarker({ value }: { value: string }) {
  const m = MARKER[value] ?? MARKER.O;
  return (
    <span
      title={m.title}
      className={cn(
        "mx-0.5 inline-flex items-center rounded px-1 align-baseline font-mono text-[0.78em] font-semibold ring-1",
        m.cls,
      )}
    >
      [{value}]
    </span>
  );
}

function AreaBadge({ area }: { area: string }) {
  const m = AREA_META[area] ?? AREA_META.core;
  return (
    <span
      className={cn(
        "inline-flex shrink-0 items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[0.7rem] font-medium ring-1",
        m.cls,
      )}
    >
      <span aria-hidden className={cn("h-1.5 w-1.5 rounded-full", m.dot)} />
      {m.label}
    </span>
  );
}

/** One inline formula: SSR-safe raw TeX fallback, upgraded to KaTeX on mount.
 *  Tinted cyan so formulas are visually separable from the prose. */
function Math({ tex, macros }: { tex: string; macros: Record<string, string> }) {
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!ref.current) return;
    try {
      katex.render(tex, ref.current, {
        throwOnError: false,
        strict: "ignore",
        output: "html",
        trust: false,
        macros,
      });
    } catch {
      /* keep the raw TeX fallback on any error */
    }
  }, [tex, macros]);
  return (
    <span ref={ref} role="math" aria-label={tex} className="text-cyan-300">
      {tex}
    </span>
  );
}

function renderNodes(
  nodes: ChangelogNode[],
  macros: Record<string, string>,
): ReactNode {
  return nodes.map((nd, i) => {
    switch (nd.k) {
      case "t":
        return <Fragment key={i}>{nd.v}</Fragment>;
      case "m":
        return <Math key={i} tex={nd.v ?? ""} macros={macros} />;
      case "c":
        return (
          <code
            key={i}
            className="rounded bg-blue-500/10 px-1 py-0.5 font-mono text-[0.85em] font-medium text-blue-200 ring-1 ring-blue-400/20"
          >
            {nd.v}
          </code>
        );
      case "s":
        return <StatusMarker key={i} value={nd.v ?? "O"} />;
      case "b":
        return (
          <strong key={i} className="font-semibold text-slate-100">
            {renderNodes(nd.c ?? [], macros)}
          </strong>
        );
      case "i":
        return (
          <em key={i} className="italic text-slate-200">
            {renderNodes(nd.c ?? [], macros)}
          </em>
        );
      default:
        return null;
    }
  });
}

// --------------------------------------------------------------------------
// Heading structuring helpers
// --------------------------------------------------------------------------

function trimNodes(nodes: ChangelogNode[]): ChangelogNode[] {
  const out = nodes.map((n) => ({ ...n }));
  if (out.length && out[0].k === "t" && out[0].v) {
    out[0] = { ...out[0], v: out[0].v.replace(/^[\s\u00a0]+/, "") };
  }
  const last = out.length - 1;
  if (last >= 0 && out[last].k === "t" && out[last].v) {
    out[last] = { ...out[last], v: out[last].v.replace(/[\s\u00a0]+$/, "") };
  }
  return out.filter((n) => !(n.k === "t" && n.v === ""));
}

/** Upper-case the first alphabetic character of the first leading text node. */
function capitalizeNodes(nodes: ChangelogNode[]): ChangelogNode[] {
  const out = nodes.map((n) => ({ ...n }));
  for (const n of out) {
    if (n.k === "t" && n.v) {
      if (/[A-Za-z]/.test(n.v)) {
        n.v = n.v.replace(/^([^A-Za-z]*)([a-z])/, (_, pre, ch) => pre + ch.toUpperCase());
        break;
      }
      // leading text without letters (punctuation) -> keep scanning
      continue;
    }
    // starts with code / math / bold -> already fine, leave as is
    break;
  }
  return out;
}

function splitHeading(nodes: ChangelogNode[]): {
  title: ChangelogNode[];
  body: ChangelogNode[];
} {
  for (let i = 0; i < nodes.length; i++) {
    const nd = nodes[i];
    if (nd.k === "t" && nd.v) {
      const m = /:\s/.exec(nd.v);
      if (m && (i > 0 || m.index > 12)) {
        const before = nd.v.slice(0, m.index);
        const after = nd.v.slice(m.index + m[0].length);
        const title = nodes.slice(0, i);
        if (before.trim()) title.push({ k: "t", v: before });
        const body: ChangelogNode[] = [];
        if (after.trim()) body.push({ k: "t", v: after });
        body.push(...nodes.slice(i + 1));
        return { title: trimNodes(title), body: trimNodes(body) };
      }
    }
  }
  return { title: trimNodes(nodes), body: [] };
}

interface Segment {
  label?: string;
  nodes: ChangelogNode[];
}

/** Split at "(1) (2) (3) …" or "(Ä1) (Ä2) …" enumerators into numbered points. */
function splitEnumerated(nodes: ChangelogNode[]): Segment[] {
  const segs: Segment[] = [];
  let cur: Segment = { nodes: [] };
  const flush = () => {
    const trimmed = trimNodes(cur.nodes);
    if (trimmed.length || cur.label) segs.push({ label: cur.label, nodes: trimmed });
    cur = { nodes: [] };
  };
  const RE = /\((?:Ä|Ae)?(\d+)\)\s*/g;
  for (const nd of nodes) {
    if (nd.k === "t" && nd.v && RE.test(nd.v)) {
      RE.lastIndex = 0;
      const text = nd.v;
      let last = 0;
      let m: RegExpExecArray | null;
      while ((m = RE.exec(text)) !== null) {
        const chunk = text.slice(last, m.index);
        if (chunk) cur.nodes.push({ k: "t", v: chunk });
        flush();
        cur = { label: m[1], nodes: [] };
        last = RE.lastIndex;
      }
      const tail = text.slice(last);
      if (tail) cur.nodes.push({ k: "t", v: tail });
    } else {
      cur.nodes.push(nd);
    }
  }
  flush();
  return segs;
}

/** Peel a leading "(Ä1)" / "(1)" style label off a detail bullet. */
function peelLabel(nodes: ChangelogNode[]): { label?: string; nodes: ChangelogNode[] } {
  if (nodes.length && nodes[0].k === "t" && nodes[0].v) {
    const m = /^\((?:Ä|Ae)?(\d+)\)\s*/.exec(nodes[0].v);
    if (m) {
      const rest = nodes.map((n) => ({ ...n }));
      rest[0] = { ...rest[0], v: nodes[0].v!.slice(m[0].length) };
      return { label: m[1], nodes: trimNodes(rest) };
    }
  }
  return { nodes };
}

export function ChangelogBrowser({
  days,
  index,
  selectedDay,
  entries,
  macros,
}: Props) {
  const router = useRouter();
  const pathname = usePathname();

  const [query, setQuery] = useState("");
  const [activeAreas, setActiveAreas] = useState<Set<string>>(new Set());
  const [activeMarkers, setActiveMarkers] = useState<Set<string>>(new Set());
  const [open, setOpen] = useState<Set<string>>(new Set());

  const filtering =
    query.trim() !== "" || activeAreas.size > 0 || activeMarkers.size > 0;

  const dayIdx = days.findIndex((d) => d.date === selectedDay);
  const olderDay = dayIdx >= 0 ? days[dayIdx + 1] : undefined;
  const newerDay = dayIdx > 0 ? days[dayIdx - 1] : undefined;

  // Areas that actually occur (for the filter row).
  const presentAreas = useMemo(() => {
    const set = new Set(index.map((e) => e.area));
    return AREA_ORDER.filter((a) => set.has(a));
  }, [index]);

  // Pre-structure each entry once (title / summary / numbered points).
  const structured = useMemo(
    () =>
      entries.map((entry) => {
        const { title, body } = splitHeading(entry.heading);
        const segs = splitEnumerated(body);
        const hasPoints = segs.filter((s) => s.label).length >= 2;
        return {
          ...entry,
          title: capitalizeNodes(title),
          summary: capitalizeNodes(hasPoints ? segs[0]?.nodes ?? [] : body),
          points: hasPoints
            ? segs
                .filter((s) => s.label)
                .map((s) => ({ label: s.label, nodes: capitalizeNodes(s.nodes) }))
            : [],
        };
      }),
    [entries],
  );

  useEffect(() => {
    const hash = window.location.hash?.slice(1);
    const first = entries[0]?.anchor;
    const init = new Set<string>();
    if (first) init.add(first);
    if (hash && entries.some((e) => e.anchor === hash)) init.add(hash);
    setOpen(init);
  }, [selectedDay, entries]);

  useEffect(() => {
    if (filtering) return;
    const hash = window.location.hash?.slice(1);
    if (!hash) return;
    const el = document.getElementById(hash);
    if (!el) return;
    const t = window.setTimeout(() => {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      el.classList.add("cl-flash");
      window.setTimeout(() => el.classList.remove("cl-flash"), 1600);
    }, 80);
    return () => window.clearTimeout(t);
  }, [filtering, selectedDay]);

  const results = useMemo(() => {
    if (!filtering) return [];
    const q = query.trim().toLowerCase();
    return index.filter((e) => {
      if (q && !e.text.includes(q)) return false;
      if (activeAreas.size > 0 && !activeAreas.has(e.area)) return false;
      if (activeMarkers.size > 0 && ![...activeMarkers].some((m) => e.tags.includes(m)))
        return false;
      return true;
    });
  }, [filtering, query, activeAreas, activeMarkers, index]);

  function goToDay(date: string) {
    router.push(`${pathname}?day=${date}`, { scroll: true });
  }

  function clearFilters() {
    setQuery("");
    setActiveAreas(new Set());
    setActiveMarkers(new Set());
  }

  function toggle(set: Set<string>, value: string): Set<string> {
    const next = new Set(set);
    if (next.has(value)) next.delete(value);
    else next.add(value);
    return next;
  }

  function toggleOpen(anchor: string) {
    setOpen((s) => toggle(s, anchor));
  }

  const allOpen = structured.length > 0 && structured.every((e) => open.has(e.anchor));

  function setAll(o: boolean) {
    setOpen(o ? new Set(structured.map((e) => e.anchor)) : new Set());
  }

  return (
    <div>
      {/* ---- Controls: day paging + filter bar --------------------------- */}
      <div className="mb-8 space-y-4 rounded-2xl border border-slate-800/60 bg-slate-900/40 p-4 sm:p-5">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => olderDay && goToDay(olderDay.date)}
              disabled={!olderDay}
              aria-label="Older day"
              className="inline-flex h-9 w-9 items-center justify-center rounded-lg ring-1 ring-slate-700/60 text-slate-300 transition-colors hover:bg-white/5 disabled:cursor-not-allowed disabled:opacity-30"
            >
              <ChevronLeft size={18} />
            </button>
            <button
              type="button"
              onClick={() => newerDay && goToDay(newerDay.date)}
              disabled={!newerDay}
              aria-label="Newer day"
              className="inline-flex h-9 w-9 items-center justify-center rounded-lg ring-1 ring-slate-700/60 text-slate-300 transition-colors hover:bg-white/5 disabled:cursor-not-allowed disabled:opacity-30"
            >
              <ChevronRight size={18} />
            </button>
          </div>

          <div className="flex items-center gap-2">
            <label htmlFor="cl-day" className="sr-only">
              Jump to a day
            </label>
            <select
              id="cl-day"
              value={selectedDay}
              onChange={(e) => goToDay(e.target.value)}
              className="max-w-[16rem] rounded-lg border border-slate-700/60 bg-slate-950/60 px-3 py-2 text-sm text-slate-200 focus:border-blue-400/50 focus:outline-none"
            >
              {days.map((d) => (
                <option key={d.date} value={d.date}>
                  {formatDay(d.date)} · {d.count}
                </option>
              ))}
            </select>
          </div>

          <span className="ml-auto font-mono text-xs text-slate-500">
            {dayIdx + 1} / {days.length} days
          </span>
        </div>

        <div className="flex flex-col gap-3 border-t border-slate-800/60 pt-4">
          <div className="relative">
            <Search
              size={15}
              className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
              aria-hidden
            />
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search all entries — module id, claim id, keyword…"
              className="w-full rounded-lg border border-slate-700/60 bg-slate-950/60 py-2 pl-9 pr-9 text-sm text-slate-200 placeholder:text-slate-500 focus:border-blue-400/50 focus:outline-none"
            />
            {filtering && (
              <button
                type="button"
                onClick={clearFilters}
                aria-label="Clear filters"
                className="absolute right-2 top-1/2 -translate-y-1/2 inline-flex h-6 w-6 items-center justify-center rounded text-slate-400 hover:bg-white/5 hover:text-slate-200"
              >
                <XIcon size={15} />
              </button>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-1.5">
            {presentAreas.map((a) => {
              const meta = AREA_META[a];
              const on = activeAreas.has(a);
              return (
                <button
                  key={a}
                  type="button"
                  onClick={() => setActiveAreas((s) => toggle(s, a))}
                  className={cn(
                    "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ring-1 transition-opacity",
                    meta.cls,
                    on ? "opacity-100" : "opacity-45 hover:opacity-80",
                  )}
                >
                  <span aria-hidden className={cn("h-1.5 w-1.5 rounded-full", meta.dot)} />
                  {meta.label}
                </button>
              );
            })}
            <span aria-hidden className="mx-1 h-4 w-px bg-slate-700/60" />
            {MARKER_ORDER.map((m) => {
              const on = activeMarkers.has(m);
              return (
                <button
                  key={m}
                  type="button"
                  onClick={() => setActiveMarkers((s) => toggle(s, m))}
                  title={MARKER[m].title}
                  className={cn(
                    "inline-flex items-center rounded px-1.5 py-1 font-mono text-xs font-semibold ring-1 transition-opacity",
                    MARKER[m].cls,
                    on ? "opacity-100" : "opacity-40 hover:opacity-80",
                  )}
                >
                  [{m}]
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* ---- Filter results (global) ------------------------------------- */}
      {filtering ? (
        <div>
          <p className="mb-4 text-sm text-slate-400">
            <span className="font-semibold text-slate-200">{results.length}</span>{" "}
            {results.length === 1 ? "entry" : "entries"} match your filter.
          </p>
          {results.length === 0 ? (
            <div className="rounded-2xl border border-slate-800/60 bg-slate-900/30 px-6 py-10 text-center text-sm text-slate-400">
              No entries match. Try a different keyword or clear the filters.
            </div>
          ) : (
            <ul className="space-y-2.5">
              {results.map((r) => (
                <li key={r.anchor}>
                  <Link
                    href={`${pathname}?day=${r.date}#${r.anchor}`}
                    onClick={clearFilters}
                    className="group flex gap-3 rounded-xl border border-slate-800/60 bg-slate-900/30 px-4 py-3 transition-colors hover:border-slate-600/60 hover:bg-slate-900/60"
                  >
                    <div className="flex shrink-0 flex-col items-start gap-1">
                      <time
                        dateTime={r.date}
                        className="font-mono text-xs font-semibold text-blue-300"
                      >
                        {formatDay(r.date)}
                      </time>
                      <AreaBadge area={r.area} />
                    </div>
                    <p className="text-sm leading-relaxed text-slate-300 group-hover:text-slate-200">
                      {r.lead}
                    </p>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      ) : (
        /* ---- Day view (rich, collapsible) ------------------------------ */
        <div>
          <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-baseline gap-3">
              <h2 className="font-serif text-2xl font-semibold text-slate-50">
                {formatDay(selectedDay)}
              </h2>
              <span className="font-mono text-xs text-slate-500">
                {entries.length} {entries.length === 1 ? "update" : "updates"}
              </span>
            </div>
            {structured.length > 1 && (
              <button
                type="button"
                onClick={() => setAll(!allOpen)}
                className="rounded-full px-3 py-1 text-xs font-medium text-slate-400 ring-1 ring-slate-700/50 transition-colors hover:bg-white/5 hover:text-slate-200"
              >
                {allOpen ? "Collapse all" : "Expand all"}
              </button>
            )}
          </div>

          <ol className="space-y-4">
            {structured.map((entry) => {
              const isOpen = open.has(entry.anchor);
              return (
                <li key={entry.anchor} id={entry.anchor} className="scroll-mt-24">
                  <article className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
                    <button
                      type="button"
                      onClick={() => toggleOpen(entry.anchor)}
                      aria-expanded={isOpen}
                      className="flex w-full flex-col gap-2 px-5 py-4 text-left transition-colors hover:bg-white/[0.02] sm:px-6"
                    >
                      <div className="flex items-center gap-2">
                        <AreaBadge area={entry.area} />
                        {entry.enumr && (
                          <span className="rounded bg-slate-800/70 px-1.5 py-0.5 font-mono text-[0.65rem] font-semibold text-slate-400">
                            {entry.enumr}
                          </span>
                        )}
                        <ChevronDown
                          size={18}
                          aria-hidden
                          className={cn(
                            "ml-auto shrink-0 text-slate-500 transition-transform",
                            isOpen && "rotate-180",
                          )}
                        />
                      </div>
                      <div
                        className={cn(
                          "text-[0.98rem] font-semibold leading-snug text-slate-100",
                          !isOpen && "line-clamp-2",
                        )}
                      >
                        {renderNodes(entry.title, macros)}
                      </div>
                      {!isOpen && entry.summary.length > 0 && (
                        <div className="line-clamp-2 text-sm leading-relaxed text-slate-400">
                          {renderNodes(entry.summary, macros)}
                        </div>
                      )}
                    </button>

                    {isOpen && (
                      <div className="border-t border-slate-800/60 px-5 pb-5 pt-4 sm:px-6">
                        {entry.summary.length > 0 && (
                          <div className="rounded-xl border border-slate-800/50 bg-slate-900/40 px-4 py-3">
                            <p className="mb-1.5 text-[0.7rem] font-semibold uppercase tracking-wider text-slate-500">
                              Summary
                            </p>
                            <p className="text-sm leading-7 text-slate-200">
                              {renderNodes(entry.summary, macros)}
                            </p>
                          </div>
                        )}

                        {entry.points.length > 0 && (
                          <div className="mt-4">
                            <p className="mb-2.5 text-[0.7rem] font-semibold uppercase tracking-wider text-slate-500">
                              Key points
                            </p>
                            <ol className="space-y-2.5">
                              {entry.points.map((p, k) => (
                                <li key={k} className="flex gap-3">
                                  <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-blue-500/15 font-mono text-[0.7rem] font-semibold text-blue-200 ring-1 ring-blue-400/30">
                                    {p.label}
                                  </span>
                                  <div className="min-w-0 flex-1 text-sm leading-7 text-slate-300">
                                    {renderNodes(p.nodes, macros)}
                                  </div>
                                </li>
                              ))}
                            </ol>
                          </div>
                        )}

                        {entry.items.length > 0 && (
                          <div className="mt-5 border-t border-slate-800/40 pt-4">
                            <p className="mb-2.5 text-[0.7rem] font-semibold uppercase tracking-wider text-slate-500">
                              Details
                            </p>
                            <ul className="space-y-3">
                              {entry.items.map((item, j) => {
                                const { label, nodes } = peelLabel(item);
                                return (
                                  <li
                                    key={j}
                                    className={cn(
                                      "text-sm leading-7 text-slate-400",
                                      label
                                        ? "flex gap-2.5"
                                        : "relative pl-4 before:absolute before:left-0 before:top-[0.7em] before:h-1.5 before:w-1.5 before:rounded-full before:bg-slate-600",
                                    )}
                                  >
                                    {label && (
                                      <span className="mt-0.5 shrink-0 rounded bg-slate-800/70 px-1.5 py-0.5 font-mono text-[0.65rem] font-semibold text-slate-400">
                                        {label}
                                      </span>
                                    )}
                                    <div className={label ? "min-w-0 flex-1" : undefined}>
                                      {renderNodes(nodes, macros)}
                                    </div>
                                  </li>
                                );
                              })}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </article>
                </li>
              );
            })}
          </ol>

          <div className="mt-8 flex items-center justify-between gap-3">
            {olderDay ? (
              <button
                type="button"
                onClick={() => goToDay(olderDay.date)}
                className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-slate-300 ring-1 ring-slate-700/60 transition-colors hover:bg-white/5"
              >
                <ChevronLeft size={16} />
                {formatDay(olderDay.date)}
              </button>
            ) : (
              <span />
            )}
            {newerDay ? (
              <button
                type="button"
                onClick={() => goToDay(newerDay.date)}
                className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-slate-300 ring-1 ring-slate-700/60 transition-colors hover:bg-white/5"
              >
                {formatDay(newerDay.date)}
                <ChevronRight size={16} />
              </button>
            ) : (
              <span />
            )}
          </div>
        </div>
      )}
    </div>
  );
}

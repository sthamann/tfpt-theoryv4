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
import { ChevronLeft, ChevronRight, Search, X as XIcon } from "lucide-react";
import type { ChangelogNode } from "@/lib/changelog";
import { cn } from "@/lib/utils";

/**
 * Interactive changelog browser.
 *
 * The changelog has grown to hundreds of entries, many of them very long. The
 * page therefore pages by DAY: it shows one day's updates at a time (the latest
 * day by default), lets you step between days, and offers a global filter
 * (full-text search + kind/status facets) that searches across every entry.
 *
 * Only the selected day's full node trees are shipped from the server; day
 * switching is a normal `?day=` navigation so the payload stays bounded as the
 * changelog keeps growing. The lightweight `index` (short plain-text summaries)
 * powers the global filter without shipping the ~2 MB full data to the client.
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
}

export interface ChangelogDayEntry {
  label: string;
  enumr: string;
  heading: ChangelogNode[];
  items: ChangelogNode[][];
  anchor: string;
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

const KINDS: { id: string; label: string }[] = [
  { id: "module", label: "Modules (vN)" },
  { id: "editorial", label: "Editorial" },
  { id: "experiment", label: "Experiments" },
];

const MARKER_ORDER = ["E", "C", "O", "X"];

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

/** One inline formula: SSR-safe raw TeX fallback, upgraded to KaTeX on mount. */
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
    <span ref={ref} role="math" aria-label={tex}>
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
            className="rounded bg-slate-800/60 px-1 py-0.5 font-mono text-[0.85em] text-blue-200 ring-1 ring-slate-700/40"
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
  const [activeKinds, setActiveKinds] = useState<Set<string>>(new Set());
  const [activeMarkers, setActiveMarkers] = useState<Set<string>>(new Set());

  const filtering =
    query.trim() !== "" || activeKinds.size > 0 || activeMarkers.size > 0;

  const dayIdx = days.findIndex((d) => d.date === selectedDay);
  const olderDay = dayIdx >= 0 ? days[dayIdx + 1] : undefined;
  const newerDay = dayIdx > 0 ? days[dayIdx - 1] : undefined;

  const results = useMemo(() => {
    if (!filtering) return [];
    const q = query.trim().toLowerCase();
    return index.filter((e) => {
      if (q && !e.text.includes(q)) return false;
      if (activeKinds.size > 0 && ![...activeKinds].some((k) => e.tags.includes(k)))
        return false;
      if (
        activeMarkers.size > 0 &&
        ![...activeMarkers].some((m) => e.tags.includes(m))
      )
        return false;
      return true;
    });
  }, [filtering, query, activeKinds, activeMarkers, index]);

  // Scroll to a linked entry (#cl-<n>) after the day view renders.
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
    }, 60);
    return () => window.clearTimeout(t);
  }, [filtering, selectedDay]);

  function goToDay(date: string) {
    router.push(`${pathname}?day=${date}`, { scroll: true });
  }

  function clearFilters() {
    setQuery("");
    setActiveKinds(new Set());
    setActiveMarkers(new Set());
  }

  function toggle(set: Set<string>, value: string): Set<string> {
    const next = new Set(set);
    if (next.has(value)) next.delete(value);
    else next.add(value);
    return next;
  }

  return (
    <div>
      {/* ---- Controls: day paging + filter bar --------------------------- */}
      <div className="mb-8 space-y-4 rounded-2xl border border-slate-800/60 bg-slate-900/40 p-4 sm:p-5">
        {/* Day pager */}
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

        {/* Filter bar */}
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

          <div className="flex flex-wrap items-center gap-2">
            {KINDS.map((k) => {
              const on = activeKinds.has(k.id);
              return (
                <button
                  key={k.id}
                  type="button"
                  onClick={() => setActiveKinds((s) => toggle(s, k.id))}
                  className={cn(
                    "rounded-full px-3 py-1 text-xs font-medium ring-1 transition-colors",
                    on
                      ? "bg-blue-500/15 text-blue-200 ring-blue-400/40"
                      : "text-slate-400 ring-slate-700/50 hover:bg-white/5 hover:text-slate-200",
                  )}
                >
                  {k.label}
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
                      {r.enumr && (
                        <span className="rounded bg-slate-800/70 px-1.5 py-0.5 font-mono text-[0.65rem] text-slate-400">
                          {r.enumr}
                        </span>
                      )}
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
        /* ---- Day view (rich) ------------------------------------------- */
        <div>
          <div className="mb-6 flex flex-wrap items-baseline justify-between gap-3">
            <h2 className="font-serif text-2xl font-semibold text-slate-50">
              {formatDay(selectedDay)}
            </h2>
            <span className="font-mono text-xs text-slate-500">
              {entries.length} {entries.length === 1 ? "update" : "updates"}
            </span>
          </div>

          <ol className="relative space-y-7 border-l border-slate-800/70 pl-5 sm:pl-7">
            {entries.map((entry) => (
              <li key={entry.anchor} id={entry.anchor} className="relative scroll-mt-24">
                <span
                  aria-hidden
                  className="absolute -left-[1.6rem] top-1.5 h-2.5 w-2.5 rounded-full bg-gradient-to-br from-blue-400 to-violet-400 ring-4 ring-slate-950 sm:-left-[2.1rem]"
                />
                <article className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40 transition-shadow">
                  {entry.enumr && (
                    <header className="flex items-center gap-2 border-b border-slate-800/60 px-5 py-2.5 sm:px-6">
                      <span className="rounded bg-slate-800/70 px-2 py-0.5 font-mono text-xs font-semibold tracking-wide text-slate-300">
                        {entry.enumr}
                      </span>
                    </header>
                  )}
                  <div className="space-y-3 px-5 py-4 sm:px-6">
                    {entry.heading.length > 0 && (
                      <p className="text-sm leading-relaxed text-slate-200">
                        {renderNodes(entry.heading, macros)}
                      </p>
                    )}
                    {entry.items.length > 0 && (
                      <ul className="space-y-3">
                        {entry.items.map((item, j) => (
                          <li
                            key={j}
                            className="relative pl-4 text-sm leading-relaxed text-slate-300 before:absolute before:left-0 before:top-[0.55em] before:h-1.5 before:w-1.5 before:rounded-full before:bg-slate-600"
                          >
                            {renderNodes(item, macros)}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </article>
              </li>
            ))}
          </ol>

          {/* Bottom day pager */}
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

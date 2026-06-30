import { Fragment, type ReactNode } from "react";
import katex from "katex";
import {
  CHANGELOG,
  CHANGELOG_MACROS,
  type ChangelogNode,
} from "@/lib/changelog";

/**
 * Static, server-rendered changelog. The data is generated from changelog.tex
 * (the single source of truth) by verification/make_changelog_web.py and never
 * edited by hand. Inline math is rendered with KaTeX at build time, so the page
 * ships as plain HTML + the KaTeX stylesheet already loaded globally.
 */

const MARKER: Record<string, { label: string; cls: string; title: string }> = {
  E: {
    label: "E",
    cls: "bg-emerald-500/10 text-emerald-300 ring-emerald-400/30",
    title: "Exact / machine-proven (identity, lattice, formalised, numerical fixed point)",
  },
  C: {
    label: "C",
    cls: "bg-amber-500/10 text-amber-300 ring-amber-400/30",
    title: "Conditional (physical / bridge / readout, under named hypotheses)",
  },
  O: {
    label: "O",
    cls: "bg-slate-500/10 text-slate-300 ring-slate-400/30",
    title: "Open / axiom",
  },
  X: {
    label: "X",
    cls: "bg-rose-500/10 text-rose-300 ring-rose-400/30",
    title: "Falsifiable kill test",
  },
};

function InlineMath({ tex }: { tex: string }) {
  // output: "html" (not "htmlAndMathml") keeps the page well under Vercel's
  // 19 MB prerender limit: the duplicate MathML tree KaTeX emits per formula was
  // ~half the changelog HTML across ~10k formulas. Accessibility is preserved by
  // the role="math" aria-label={tex} wrapper below (the TeX is the accessible name).
  const html = katex.renderToString(tex, {
    throwOnError: false,
    strict: "ignore",
    output: "html",
    trust: false,
    macros: { ...CHANGELOG_MACROS },
  });
  return (
    <span role="math" aria-label={tex} dangerouslySetInnerHTML={{ __html: html }} />
  );
}

function StatusMarker({ value }: { value: string }) {
  const m = MARKER[value] ?? MARKER.O;
  return (
    <span
      title={m.title}
      className={`mx-0.5 inline-flex items-center rounded px-1 align-baseline font-mono text-[0.78em] font-semibold ring-1 ${m.cls}`}
    >
      [{m.label}]
    </span>
  );
}

function renderNodes(nodes: ChangelogNode[]): ReactNode {
  return nodes.map((nd, i) => {
    switch (nd.k) {
      case "t":
        return <Fragment key={i}>{nd.v}</Fragment>;
      case "m":
        return <InlineMath key={i} tex={nd.v ?? ""} />;
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
            {renderNodes(nd.c ?? [])}
          </strong>
        );
      case "i":
        return (
          <em key={i} className="italic text-slate-200">
            {renderNodes(nd.c ?? [])}
          </em>
        );
      default:
        return null;
    }
  });
}

export function Changelog() {
  return (
    <ol className="relative space-y-7 border-l border-slate-800/70 pl-5 sm:pl-7">
      {CHANGELOG.map((entry, idx) => (
        <li key={idx} className="relative">
          <span
            aria-hidden
            className="absolute -left-[1.6rem] top-1.5 h-2.5 w-2.5 rounded-full bg-gradient-to-br from-blue-400 to-violet-400 ring-4 ring-slate-950 sm:-left-[2.1rem]"
          />
          <article className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
            <header className="flex flex-wrap items-baseline gap-x-3 gap-y-1 border-b border-slate-800/60 px-5 py-3.5 sm:px-6">
              <time
                dateTime={entry.date}
                className="font-mono text-xs font-semibold tracking-wide text-blue-300"
              >
                {entry.dateLabel}
              </time>
              {entry.heading.length > 0 && (
                <h2 className="font-serif text-[0.98rem] font-semibold leading-snug text-slate-100">
                  {renderNodes(entry.heading)}
                </h2>
              )}
            </header>
            <ul className="space-y-3 px-5 py-4 sm:px-6">
              {entry.items.map((item, j) => (
                <li
                  key={j}
                  className="relative pl-4 text-sm leading-relaxed text-slate-300 before:absolute before:left-0 before:top-[0.55em] before:h-1.5 before:w-1.5 before:rounded-full before:bg-slate-600"
                >
                  {renderNodes(item)}
                </li>
              ))}
            </ul>
          </article>
        </li>
      ))}
    </ol>
  );
}

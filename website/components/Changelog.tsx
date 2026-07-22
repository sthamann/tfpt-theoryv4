import { Fragment, type ReactNode } from "react";
import {
  CHANGELOG,
  CHANGELOG_MACROS,
  type ChangelogNode,
} from "@/lib/changelog";
import { ChangelogMath } from "@/components/ChangelogMath";

/**
 * Server-rendered changelog. The data is generated from changelog.tex (the
 * single source of truth) by verification/make_changelog_web.py and never edited
 * by hand.
 *
 * Inline math is emitted as raw TeX in the server HTML and upgraded to KaTeX in
 * the browser by <ChangelogMath> (a single client-side pass). Rendering the
 * ~6.5k formulas to KaTeX HTML at build time pushed the prerendered page past
 * Vercel's 19.07 MB ISR limit (FALLBACK_BODY_TOO_LARGE); deferring the render
 * keeps the prerendered HTML small and bounded as the changelog grows, while the
 * TeX source stays in the DOM (data-cl-tex + aria-label) for a11y, SEO and
 * no-JS readability.
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
  // Emit only the raw TeX at build time; <ChangelogMath> renders it with KaTeX
  // in the browser. This keeps the prerendered page well under Vercel's 19.07 MB
  // ISR limit (the build-time KaTeX HTML across ~6.5k formulas was ~16 MB of it).
  // The TeX source stays in the DOM (data-cl-tex + aria-label) for a11y, SEO and
  // no-JS readability, and the visible text is the sensible pre-hydration fallback.
  return (
    <span role="math" aria-label={tex} data-cl-tex={tex}>
      {tex}
    </span>
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
    <>
      <ChangelogMath macros={CHANGELOG_MACROS} />
      <ol className="relative space-y-7 border-l border-slate-800/70 pl-5 sm:pl-7">
      {CHANGELOG.map((entry, idx) => (
        <li key={idx} className="relative">
          <span
            aria-hidden
            className="absolute -left-[1.6rem] top-1.5 h-2.5 w-2.5 rounded-full bg-gradient-to-br from-blue-400 to-violet-400 ring-4 ring-slate-950 sm:-left-[2.1rem]"
          />
          <article className="glass overflow-hidden rounded-2xl ring-1 ring-slate-700/40">
            <header className="border-b border-slate-800/60 px-5 py-3.5 sm:px-6">
              <time
                dateTime={entry.date}
                className="font-mono text-xs font-semibold tracking-wide text-blue-300"
              >
                {entry.dateLabel}
              </time>
            </header>
            <div className="space-y-3 px-5 py-4 sm:px-6">
              {entry.heading.length > 0 && (
                // The heading carries the whole entry summary (often several
                // hundred words). Render it as a readable lead paragraph, not as
                // a large serif heading, so long entries do not become a wall.
                <h2 className="text-sm leading-relaxed text-slate-200">
                  {renderNodes(entry.heading)}
                </h2>
              )}
              {entry.items.length > 0 && (
                <ul className="space-y-3">
                  {entry.items.map((item, j) => (
                    <li
                      key={j}
                      className="relative pl-4 text-sm leading-relaxed text-slate-300 before:absolute before:left-0 before:top-[0.55em] before:h-1.5 before:w-1.5 before:rounded-full before:bg-slate-600"
                    >
                      {renderNodes(item)}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </article>
        </li>
      ))}
      </ol>
    </>
  );
}

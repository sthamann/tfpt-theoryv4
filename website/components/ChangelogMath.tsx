"use client";

import { useEffect } from "react";
import katex from "katex";

/**
 * Client-side KaTeX hydrator for the /changelog page.
 *
 * The changelog carries ~6.5k inline formulas across ~280 dated entries. When
 * these were rendered to KaTeX HTML at build time the prerendered page grew past
 * Vercel's 19.07 MB ISR limit (FALLBACK_BODY_TOO_LARGE) and the build failed.
 *
 * Instead the server component (components/Changelog.tsx) now emits only the raw
 * TeX per formula (a few bytes each, inside `span[data-cl-tex]`), keeping the
 * prerendered HTML small and bounded as the changelog keeps growing. This
 * component upgrades those spans to rendered KaTeX in the browser after mount.
 *
 * It deliberately operates on the static, server-rendered DOM via a single pass
 * (not one client component per formula) so the 2.28 MB CHANGELOG data is never
 * shipped to the client — only the tiny macro table is passed in as a prop.
 */
export function ChangelogMath({ macros }: { macros: Record<string, string> }) {
  useEffect(() => {
    const spans =
      document.querySelectorAll<HTMLElement>("span[data-cl-tex]");
    spans.forEach((span) => {
      if (span.dataset.clRendered === "1") return;
      const tex = span.getAttribute("data-cl-tex") ?? "";
      try {
        katex.render(tex, span, {
          throwOnError: false,
          strict: "ignore",
          // "html" (not "htmlAndMathml") keeps the DOM light across ~6.5k
          // formulas; the TeX source stays available via data-cl-tex + aria-label.
          output: "html",
          trust: false,
          macros: { ...macros },
        });
        span.dataset.clRendered = "1";
      } catch {
        /* leave the raw TeX fallback in place on any render error */
      }
    });
  }, [macros]);

  return null;
}

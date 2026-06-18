"use client";

import { useMemo, useState } from "react";
import katex from "katex";
import { Check, Copy } from "lucide-react";
import { cn } from "@/lib/utils";

interface MathProps {
  children: string;
  block?: boolean;
  className?: string;
  /**
   * Explicit screen-reader label. Prefer `plain` for display formulas so the
   * same string also renders as a visible caption.
   */
  ariaLabel?: string;
  /**
   * Plain-English reading of the formula. For block math it renders as a
   * visible "In words:" caption (accessibility + SEO + LLM readability) and is
   * used as the screen-reader label. Highly recommended for every main formula.
   */
  plain?: string;
}

/**
 * Render math via KaTeX with accessibility + extraction hardening:
 *
 * - Output mode `htmlAndMathml`: KaTeX emits visual HTML plus a semantic MathML
 *   tree with `<annotation encoding="application/x-tex">` carrying the source.
 * - The visual `.katex-html` is made non-selectable in globals.css, so copy/
 *   paste, search engines and LLMs never pick up the spatially-garbled glyphs.
 * - `role="math"` with an `aria-label` of the plain-English reading when given
 *   (falling back to the TeX source), so assistive tech gets a sensible name.
 * - Display formulas additionally expose a "copy LaTeX" button (the source) and
 *   an optional visible plain-English caption.
 */
export function Math({
  children,
  block = false,
  className,
  ariaLabel,
  plain,
}: MathProps) {
  const html = useMemo(() => {
    try {
      return katex.renderToString(children, {
        displayMode: block,
        throwOnError: false,
        strict: "ignore",
        output: "htmlAndMathml",
        trust: false,
      });
    } catch {
      return children;
    }
  }, [children, block]);

  const label = ariaLabel ?? plain ?? children;

  if (block) {
    return (
      <div className={cn("my-2", className)}>
        <div className="group relative">
          <div
            role="math"
            aria-label={label}
            className="formula-scroll overflow-x-auto"
            dangerouslySetInnerHTML={{ __html: html }}
          />
          <CopyLatex tex={children} />
        </div>
        {plain && (
          <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
            <span className="font-semibold text-slate-500">In words: </span>
            {plain}
          </p>
        )}
      </div>
    );
  }

  return (
    <span
      role="math"
      aria-label={label}
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

/**
 * A subtle copy-to-clipboard button for the LaTeX source of a display formula.
 * Hidden until the formula is hovered or the button is focused (keyboard).
 */
function CopyLatex({ tex }: { tex: string }) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(tex);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard unavailable (e.g. insecure context) — no-op */
    }
  };

  return (
    <button
      type="button"
      onClick={copy}
      aria-label={copied ? "LaTeX copied to clipboard" : "Copy LaTeX source"}
      title={copied ? "Copied!" : "Copy LaTeX"}
      className="absolute right-1 top-1 rounded-md border border-slate-700/50 bg-slate-900/85 p-1 text-slate-400 opacity-50 backdrop-blur transition-opacity hover:text-slate-100 hover:opacity-100 focus:opacity-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400/40 group-hover:opacity-100"
    >
      {copied ? (
        <Check size={12} aria-hidden className="text-emerald-300" />
      ) : (
        <Copy size={12} aria-hidden />
      )}
    </button>
  );
}

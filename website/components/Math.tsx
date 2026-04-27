"use client";

import { useMemo } from "react";
import katex from "katex";
import { cn } from "@/lib/utils";

interface MathProps {
  children: string;
  block?: boolean;
  className?: string;
  /**
   * Optional plain-text label for screen readers. Falls back to the raw TeX
   * source when not provided; KaTeX also emits a `<annotation>` MathML node
   * containing the source so AT can pick it up directly.
   */
  ariaLabel?: string;
}

/**
 * Render math via KaTeX with accessibility hardening:
 *
 * - Output mode is `htmlAndMathml`: KaTeX emits both visual HTML and a
 *   semantic MathML tree (with `<annotation encoding="application/x-tex">`
 *   carrying the source). Screen readers prefer the MathML branch.
 * - The wrapper element is given `role="math"` and `aria-label` (or the raw
 *   TeX as fallback) so AT users get a spoken/bracketed form.
 * - Block math is wrapped in `formula-scroll` so the styled scrollbar rule
 *   in `globals.css` applies and print mode strips it.
 */
export function Math({
  children,
  block = false,
  className,
  ariaLabel,
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

  const label = ariaLabel ?? children;

  if (block) {
    return (
      <div
        role="math"
        aria-label={label}
        className={cn(
          "formula-scroll my-2 overflow-x-auto",
          className,
        )}
        dangerouslySetInnerHTML={{ __html: html }}
      />
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

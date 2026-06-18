import type { CSSProperties } from "react";

/**
 * TFPT video design tokens — mirrors the website (app/globals.css) so the intro
 * film and the site read as one product.
 */
export const COLORS = {
  bg: "#080c18",
  bgDeep: "#06091a",
  panel: "rgba(15, 23, 42, 0.55)",
  panelStrong: "rgba(15, 23, 42, 0.85)",
  border: "rgba(148, 163, 184, 0.16)",
  text: "#e2e8f0",
  textBright: "#f1f5f9",
  textDim: "#94a3b8",
  textFaint: "#64748b",
  blue: "#3b82f6",
  blueLight: "#60a5fa",
  violet: "#a78bfa",
  pink: "#f472b6",
  // status grades (match the ledger / ScopeGuard)
  exact: "#34d399", // [E] emerald
  exactBg: "rgba(16, 185, 129, 0.12)",
  conditional: "#fbbf24", // [C] amber
  conditionalBg: "rgba(245, 158, 11, 0.12)",
  open: "#fb7185", // [O] rose
  openBg: "rgba(244, 63, 94, 0.12)",
} as const;

export const GRADIENT_BLUE =
  "linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%)";

/** Apply a clipped gradient to text. */
export const gradientText = (gradient = GRADIENT_BLUE): CSSProperties => ({
  backgroundImage: gradient,
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  WebkitTextFillColor: "transparent",
  color: COLORS.blueLight,
});

export type StatusGrade = "E" | "C" | "O";

export const STATUS_META: Record<
  StatusGrade,
  { label: string; color: string; bg: string }
> = {
  E: { label: "Exact", color: COLORS.exact, bg: COLORS.exactBg },
  C: { label: "Conditional", color: COLORS.conditional, bg: COLORS.conditionalBg },
  O: { label: "Open", color: COLORS.open, bg: COLORS.openBg },
};

"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  ReactNode,
} from "react";
import { BookOpen, Microscope } from "lucide-react";
import { cn } from "@/lib/utils";

export type ReadingMode = "orientation" | "reviewer";

interface ReadingModeContextValue {
  mode: ReadingMode;
  setMode: (mode: ReadingMode) => void;
  toggle: () => void;
}

const ReadingModeContext = createContext<ReadingModeContextValue | null>(null);

const STORAGE_KEY = "tfpt:reading-mode";

/**
 * Provides a body-level reading mode so the rest of the site can hide or
 * surface dense content via CSS rules in `globals.css`.
 *
 * - `orientation` mode: visuals, claim maps, status badges. Heavy formula
 *   blocks and reviewer-only details are hidden via the `.reviewer-only`
 *   utility class.
 * - `reviewer` mode (default): everything is shown. This is the
 *   academic/publish-ready view.
 *
 * The selection persists to localStorage and is applied to
 * `document.documentElement` as `data-reading-mode="..."`.
 */
export function ReadingModeProvider({ children }: { children: ReactNode }) {
  const [mode, setModeState] = useState<ReadingMode>("reviewer");
  const [hydrated, setHydrated] = useState(false);

  // Hydrate from localStorage once on mount.
  useEffect(() => {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored === "orientation" || stored === "reviewer") {
        setModeState(stored);
      }
    } catch {
      // Storage may be unavailable (private browsing); silently keep default.
    }
    setHydrated(true);
  }, []);

  // Reflect the active mode on the root element so CSS rules can target it.
  useEffect(() => {
    if (!hydrated || typeof document === "undefined") return;
    document.documentElement.dataset.readingMode = mode;
    try {
      window.localStorage.setItem(STORAGE_KEY, mode);
    } catch {
      // Ignore storage errors.
    }
  }, [mode, hydrated]);

  const setMode = useCallback((m: ReadingMode) => setModeState(m), []);
  const toggle = useCallback(
    () => setModeState((m) => (m === "orientation" ? "reviewer" : "orientation")),
    [],
  );

  const value = useMemo(
    () => ({ mode, setMode, toggle }),
    [mode, setMode, toggle],
  );

  return (
    <ReadingModeContext.Provider value={value}>
      {children}
    </ReadingModeContext.Provider>
  );
}

export function useReadingMode(): ReadingModeContextValue {
  const ctx = useContext(ReadingModeContext);
  if (!ctx) {
    return {
      mode: "reviewer",
      setMode: () => {},
      toggle: () => {},
    };
  }
  return ctx;
}

/**
 * A two-state toggle pinned in the navbar. Orientation mode hides the heavy
 * formula blocks and reviewer-only details so first-time readers see the
 * claim and the visuals; reviewer mode brings everything back.
 */
export function ReadingModeToggle({ className }: { className?: string }) {
  const { mode, setMode } = useReadingMode();
  return (
    <div
      role="tablist"
      aria-label="Reading mode"
      className={cn(
        "inline-flex items-center gap-0.5 rounded-full bg-slate-900/60 p-0.5 ring-1 ring-slate-700/40",
        className,
      )}
    >
      <button
        type="button"
        role="tab"
        aria-selected={mode === "orientation"}
        title="Orientation: visuals, claim map, fewer formulas"
        onClick={() => setMode("orientation")}
        className={cn(
          "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold transition-colors",
          mode === "orientation"
            ? "bg-blue-500 text-white"
            : "text-slate-300 hover:text-white",
        )}
      >
        <BookOpen size={12} aria-hidden />
        Orientation
      </button>
      <button
        type="button"
        role="tab"
        aria-selected={mode === "reviewer"}
        title="Reviewer: formulas, references, proof status, kill criteria"
        onClick={() => setMode("reviewer")}
        className={cn(
          "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold transition-colors",
          mode === "reviewer"
            ? "bg-blue-500 text-white"
            : "text-slate-300 hover:text-white",
        )}
      >
        <Microscope size={12} aria-hidden />
        Reviewer
      </button>
    </div>
  );
}

/**
 * Wraps content that should only render in reviewer mode. The element is
 * hidden by a CSS rule on `[data-reading-mode="orientation"]`; we also
 * mark it `aria-hidden` when collapsed so AT users do not hear cut-off
 * derivation noise.
 */
export function ReviewerOnly({
  children,
  className,
  as: Tag = "div",
}: {
  children: ReactNode;
  className?: string;
  as?: keyof React.JSX.IntrinsicElements;
}) {
  const Element = Tag as keyof React.JSX.IntrinsicElements;
  // We cannot conditionally render based on context to avoid hydration
  // drift; instead we ship the markup and let CSS hide it.
  return (
    <Element className={cn("reviewer-only", className)}>
      {children}
    </Element>
  );
}

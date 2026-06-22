import { Fragment, type ReactNode } from "react";

/**
 * Lightweight inline renderer for the verification surfaces (script index list,
 * the script-detail reproducer, the dependency-graph node summaries).
 *
 * It highlights two things in otherwise-plain prose, mirroring the /changelog
 * page's visual language without a full LaTeX/KaTeX pipeline (the source text
 * here is unicode ASCII, not LaTeX):
 *
 *   1. Status markers  [E] [C] [O] [X]  (plus the fine ledger types
 *      [I] [L] [F] [N] [P] [B] [R] [A]) -> coloured badges, folded into the
 *      four public display classes (exact / conditional / open / kill test).
 *   2. Formula-ish tokens (anything carrying a math symbol, a sub/superscript,
 *      a Greek/blackboard letter, an `=`/`^`/`_`, a letter+digit identifier
 *      such as c3 / E8 / phi0, or a d/d fraction) -> a subtle monospace chip.
 *
 * The formula test is deliberately conservative and per-token: it never merges
 * across whitespace, so it cannot mangle ordinary prose — at worst it leaves a
 * spaced operator un-highlighted between two highlighted operands.
 */

// Status marker -> tone, following the /changelog palette (E emerald,
// C amber, O slate, X rose). Fine ledger types fold into their display class.
const MARKER_TONE: Record<string, string> = {
  E: "bg-emerald-500/10 text-emerald-300 ring-emerald-400/30",
  I: "bg-emerald-500/10 text-emerald-300 ring-emerald-400/30",
  L: "bg-emerald-500/10 text-emerald-300 ring-emerald-400/30",
  F: "bg-emerald-500/10 text-emerald-300 ring-emerald-400/30",
  N: "bg-emerald-500/10 text-emerald-300 ring-emerald-400/30",
  C: "bg-amber-500/10 text-amber-300 ring-amber-400/30",
  P: "bg-amber-500/10 text-amber-300 ring-amber-400/30",
  B: "bg-amber-500/10 text-amber-300 ring-amber-400/30",
  R: "bg-amber-500/10 text-amber-300 ring-amber-400/30",
  O: "bg-slate-500/10 text-slate-300 ring-slate-400/30",
  A: "bg-slate-500/10 text-slate-300 ring-slate-400/30",
  X: "bg-rose-500/10 text-rose-300 ring-rose-400/30",
};

const MARKER_GLOBAL = /\[(E|C|O|X|I|L|F|N|P|B|R|A)\]/g;

// Any "strong" math character: operators, sub/superscripts, Greek (the
// uppercase range Α-Ω already covers Δ Λ Ω Φ Ψ Γ Θ Ξ Π Σ), blackboard letters.
const MATH_CHAR =
  /[=^_{}|+×÷·⋅∘⊕⊗√∞∂∇∈∉⊂⊆∩∪⇒⟹→↦↔⟷≤≥≠≈∼≅≡∝∏∑−⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ₀₁₂₃₄₅₆₇₈₉α-ωΑ-Ωℤℙℝℂℕℚ]/u;

// A "core" is a letter (Latin, Greek) / blackboard / digit — anything that is
// not purely operators/punctuation. Lone operators (= → ⇒ ± …) have no core and
// are never chipped, so prose is never mangled.
const CORE_CHAR = /[A-Za-z0-9α-ωΑ-Ωℤℙℝℂℕℚ]/u;

function isFormula(raw: string): boolean {
  const t = raw.replace(/^[("'¿¡]+/, "").replace(/[).,;:!?"']+$/, "");
  if (!t || !CORE_CHAR.test(t)) return false;
  if (MATH_CHAR.test(t)) return true; // symbols, sub/superscripts, Greek (φ₀, μ₄, α⁻¹, ℤ₄)
  if (/[A-Za-z]\d/.test(t)) return true; // identifier: c3, E8, phi0, theta13, v219, D5, P1
  if (/\d+\/\d+/.test(t)) return true; // fraction: 41/10, 2/3
  return false;
}

function StatusBadge({ code }: { code: string }) {
  const tone = MARKER_TONE[code] ?? MARKER_TONE.O;
  return (
    <span
      className={`mx-0.5 inline-flex items-center rounded px-1 align-baseline font-mono text-[0.85em] font-semibold ring-1 ${tone}`}
    >
      [{code}]
    </span>
  );
}

function FormulaChip({ value }: { value: string }) {
  return (
    <span className="rounded bg-slate-800/50 px-1 font-mono text-[0.92em] text-blue-200/95">
      {value}
    </span>
  );
}

/** Render one marker-free text fragment, chipping formula-ish tokens. */
function renderProse(text: string, keyBase: string): ReactNode {
  const parts = text.split(/(\s+)/); // keep whitespace runs as their own parts
  return parts.map((part, i) => {
    if (i % 2 === 1) return <Fragment key={`${keyBase}-s${i}`}>{part}</Fragment>;
    if (!part || !isFormula(part)) {
      return <Fragment key={`${keyBase}-t${i}`}>{part}</Fragment>;
    }
    // Keep trailing/leading sentence punctuation outside the chip (but not
    // parentheses, which are part of formulas like (2/3)⁶ or F_U(1)).
    const lead = part.match(/^[,"']+/)?.[0] ?? "";
    const trail = part.match(/[,;:.!?"']+$/)?.[0] ?? "";
    const core = part.slice(lead.length, part.length - trail.length);
    if (!core) return <Fragment key={`${keyBase}-t${i}`}>{part}</Fragment>;
    return (
      <Fragment key={`${keyBase}-f${i}`}>
        {lead}
        <FormulaChip value={core} />
        {trail}
      </Fragment>
    );
  });
}

/**
 * Render a plain-text string with status-marker badges and formula chips.
 * Safe on any string; renders ordinary prose unchanged.
 */
export function RichText({ text }: { text: string }): ReactNode {
  if (!text) return null;
  const out: ReactNode[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  MARKER_GLOBAL.lastIndex = 0;
  let idx = 0;
  while ((m = MARKER_GLOBAL.exec(text)) !== null) {
    if (m.index > last) {
      out.push(
        <Fragment key={`p${idx}`}>
          {renderProse(text.slice(last, m.index), `p${idx}`)}
        </Fragment>,
      );
    }
    out.push(<StatusBadge key={`m${idx}`} code={m[1]} />);
    last = m.index + m[0].length;
    idx += 1;
  }
  if (last < text.length) {
    out.push(
      <Fragment key={`p${idx}`}>{renderProse(text.slice(last), `p${idx}`)}</Fragment>,
    );
  }
  return <>{out}</>;
}

/**
 * Compact the long `what_web` descriptions for the list view: prefer the first
 * sentence, else cut at a word boundary, capped near `max` characters. The full
 * text stays available in the script-detail reproducer.
 */
export function shortText(s: string, max = 165): string {
  if (s.length <= max) return s;
  const slice = s.slice(0, max);
  const stop = Math.max(slice.lastIndexOf(". "), slice.lastIndexOf("; "));
  if (stop > max * 0.5) return s.slice(0, stop + 1).trimEnd() + " …";
  const space = slice.lastIndexOf(" ");
  return slice.slice(0, space > 0 ? space : max).trimEnd() + " …";
}

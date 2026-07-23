/**
 * Mini SVG: axioms → discrete compiler → E₈ audit → SM readouts.
 */
export function CompilerDiagram() {
  return (
    <figure
      className="mt-6 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-5"
      aria-label="Compiler pipeline from two axioms to Standard Model readouts"
    >
      <svg
        viewBox="0 0 640 160"
        className="mx-auto h-auto w-full max-w-3xl"
        role="img"
        aria-label="c3 and g_car enter a discrete compiler; D5 plus A3 with mu4 close into E8; SM readouts exit"
      >
        {/* Axioms */}
        <rect
          x="8"
          y="28"
          width="118"
          height="104"
          rx="12"
          fill="rgba(59,130,246,0.08)"
          stroke="rgba(96,165,250,0.55)"
          strokeWidth="1.4"
        />
        <text x="67" y="52" textAnchor="middle" fontSize="11" fill="rgb(147,197,253)">
          axioms
        </text>
        <text
          x="67"
          y="82"
          textAnchor="middle"
          fontSize="13"
          fontFamily="ui-monospace, monospace"
          fill="rgb(226,232,240)"
        >
          c₃ = 1/(8π)
        </text>
        <text
          x="67"
          y="108"
          textAnchor="middle"
          fontSize="13"
          fontFamily="ui-monospace, monospace"
          fill="rgb(226,232,240)"
        >
          g_car = 5
        </text>

        <path
          d="M132 80 H168"
          stroke="rgba(148,163,184,0.7)"
          strokeWidth="1.6"
          markerEnd="url(#tourArrow)"
        />

        {/* Compiler */}
        <rect
          x="172"
          y="28"
          width="150"
          height="104"
          rx="12"
          fill="rgba(16,185,129,0.07)"
          stroke="rgba(52,211,153,0.5)"
          strokeWidth="1.4"
        />
        <text x="247" y="52" textAnchor="middle" fontSize="11" fill="rgb(110,231,183)">
          discrete compiler
        </text>
        <text
          x="247"
          y="84"
          textAnchor="middle"
          fontSize="13"
          fontFamily="ui-monospace, monospace"
          fill="rgb(226,232,240)"
        >
          D₅ ⊕ A₃
        </text>
        <text
          x="247"
          y="108"
          textAnchor="middle"
          fontSize="12"
          fontFamily="ui-monospace, monospace"
          fill="rgb(203,213,225)"
        >
          + μ₄ clock
        </text>

        <path
          d="M328 80 H364"
          stroke="rgba(148,163,184,0.7)"
          strokeWidth="1.6"
          markerEnd="url(#tourArrow)"
        />

        {/* E8 */}
        <rect
          x="368"
          y="40"
          width="110"
          height="80"
          rx="12"
          fill="rgba(234,88,12,0.08)"
          stroke="rgba(251,146,60,0.55)"
          strokeWidth="1.4"
        />
        <text x="423" y="72" textAnchor="middle" fontSize="11" fill="rgb(253,186,116)">
          audit hull
        </text>
        <text
          x="423"
          y="98"
          textAnchor="middle"
          fontSize="18"
          fontFamily="ui-monospace, monospace"
          fontWeight="600"
          fill="rgb(254,215,170)"
        >
          E₈
        </text>

        <path
          d="M484 80 H520"
          stroke="rgba(148,163,184,0.7)"
          strokeWidth="1.6"
          markerEnd="url(#tourArrow)"
        />

        {/* Outputs */}
        <rect
          x="524"
          y="28"
          width="108"
          height="104"
          rx="12"
          fill="rgba(99,102,241,0.08)"
          stroke="rgba(129,140,248,0.5)"
          strokeWidth="1.4"
        />
        <text x="578" y="58" textAnchor="middle" fontSize="11" fill="rgb(165,180,252)">
          readouts
        </text>
        <text
          x="578"
          y="86"
          textAnchor="middle"
          fontSize="12"
          fill="rgb(226,232,240)"
        >
          SM structure
        </text>
        <text
          x="578"
          y="108"
          textAnchor="middle"
          fontSize="11"
          fill="rgb(203,213,225)"
        >
          α, mixings…
        </text>

        <defs>
          <marker
            id="tourArrow"
            markerWidth="8"
            markerHeight="8"
            refX="6"
            refY="3"
            orient="auto"
          >
            <path
              d="M0,0 L6,3 L0,6"
              fill="none"
              stroke="rgba(148,163,184,0.9)"
              strokeWidth="1.2"
            />
          </marker>
        </defs>
      </svg>
      <figcaption className="mt-3 text-center font-mono text-[11px] text-slate-500">
        D5 ⊕ A3 + μ4 ⇒ E8 ⇒ SM readouts
      </figcaption>
    </figure>
  );
}

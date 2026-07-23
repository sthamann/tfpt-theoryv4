/**
 * Seam as a quarter-beat clock: circle, four marks, thermal label.
 */
export function SeamClock() {
  const cx = 160;
  const cy = 120;
  const r = 78;
  const marks = [
    { angle: -90, label: "0" },
    { angle: 0, label: "1" },
    { angle: 90, label: "2" },
    { angle: 180, label: "3" },
  ];

  return (
    <figure
      className="mt-6 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-5"
      aria-label="Seam clock with four marks and Hawking temperature"
    >
      <svg
        viewBox="0 0 320 240"
        className="mx-auto h-auto w-full max-w-md"
        role="img"
        aria-label="Circle with four quarter marks representing the seam clock; T seam equals 4 c3"
      >
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="rgba(59,130,246,0.06)"
          stroke="rgba(96,165,250,0.7)"
          strokeWidth="2"
        />

        {/* quarter arcs hint */}
        {[0, 90, 180, 270].map((start) => {
          const a0 = ((start - 90) * Math.PI) / 180;
          const a1 = ((start - 90 + 80) * Math.PI) / 180;
          const x0 = cx + Math.cos(a0) * (r - 14);
          const y0 = cy + Math.sin(a0) * (r - 14);
          const x1 = cx + Math.cos(a1) * (r - 14);
          const y1 = cy + Math.sin(a1) * (r - 14);
          return (
            <path
              key={start}
              d={`M ${x0} ${y0} A ${r - 14} ${r - 14} 0 0 1 ${x1} ${y1}`}
              fill="none"
              stroke="rgba(52,211,153,0.35)"
              strokeWidth="3"
              strokeLinecap="round"
            />
          );
        })}

        {marks.map((m) => {
          const rad = (m.angle * Math.PI) / 180;
          const x1 = cx + Math.cos(rad) * (r - 6);
          const y1 = cy + Math.sin(rad) * (r - 6);
          const x2 = cx + Math.cos(rad) * (r + 10);
          const y2 = cy + Math.sin(rad) * (r + 10);
          const lx = cx + Math.cos(rad) * (r + 26);
          const ly = cy + Math.sin(rad) * (r + 26);
          return (
            <g key={m.label}>
              <line
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke="rgba(251,146,60,0.9)"
                strokeWidth="2.4"
                strokeLinecap="round"
              />
              <text
                x={lx}
                y={ly + 4}
                textAnchor="middle"
                fontSize="12"
                fontFamily="ui-monospace, monospace"
                fill="rgb(253,186,116)"
              >
                {m.label}
              </text>
            </g>
          );
        })}

        {/* hand pointing to mark 1 */}
        <line
          x1={cx}
          y1={cy}
          x2={cx + r * 0.55}
          y2={cy}
          stroke="rgba(226,232,240,0.85)"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <circle cx={cx} cy={cy} r="5" fill="rgb(226,232,240)" />

        <text
          x={cx}
          y={cy - 18}
          textAnchor="middle"
          fontSize="12"
          fill="rgb(148,163,184)"
        >
          μ₄ clock
        </text>
        <text
          x={cx}
          y={cy + 28}
          textAnchor="middle"
          fontSize="13"
          fontFamily="ui-monospace, monospace"
          fill="rgb(110,231,183)"
        >
          T_seam = 4c₃
        </text>
      </svg>
      <figcaption className="mt-2 text-center text-xs leading-relaxed text-slate-400">
        Four marks · quarter-beat · temperature = Hawking normalisation (third leg of c₃)
      </figcaption>
    </figure>
  );
}

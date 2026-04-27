"use client";

import { motion } from "motion/react";
import { ArrowRight } from "lucide-react";
import { Math as Tex } from "./Math";

/**
 * Three roots of the transport polynomial P(z). Each is a zero of P, not a
 * zero of P′. The lower critical *point* (zero of P′) sits between the
 * lower transport root and the mid transport root and is plotted as a
 * separate triangular marker below.
 */
const ROOTS = [
  {
    label: "Upper transport root",
    value: "1",
    note: "Decoupled / trivial endpoint",
    accent: "from-slate-500 to-slate-400",
  },
  {
    label: "Mid transport root",
    value: "64/729",
    note: "Intermediate transport balance",
    accent: "from-cyan-500 to-blue-400",
  },
  {
    label: "Lower transport root",
    value: "1/729",
    note: "Anchor for δ_ph; the lower critical point of P′ sits just above it",
    accent: "from-violet-500 to-fuchsia-500",
  },
];

/**
 * Critical points of P′(z) for P(z) = (z − 1)(z − 64/729)(z − 1/729).
 * Computed once at build time so the plot can mark them as triangles
 * separate from the round root markers above. Numerical: P′(z) = 0 has two
 * real solutions, sandwiched between consecutive roots.
 */
const CUBIC_CRITICAL_POINTS = (() => {
  const r1 = 1 / 729;
  const r2 = 64 / 729;
  const r3 = 1;
  // P(z) = z³ - (r1+r2+r3) z² + (r1 r2 + r1 r3 + r2 r3) z - r1 r2 r3
  // P'(z) = 3 z² - 2(r1+r2+r3) z + (r1 r2 + r1 r3 + r2 r3)
  const a = 3;
  const b = -2 * (r1 + r2 + r3);
  const c = r1 * r2 + r1 * r3 + r2 * r3;
  const d = Math.sqrt(b * b - 4 * a * c);
  const cpLow = (-b - d) / (2 * a);
  const cpHigh = (-b + d) / (2 * a);
  return [cpLow, cpHigh];
})();

export function TransportPole() {
  return (
    <div className="glass rounded-2xl ring-1 ring-slate-700/40">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Cusp cubic — transport phase polynomial
        </span>
        <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-emerald-200 ring-1 ring-emerald-400/30">
          Bridge readout · not theorem core
        </span>
      </div>

      <div className="grid gap-8 p-6 md:p-8 lg:grid-cols-5">
        <div className="lg:col-span-2">
          <h3 className="font-serif text-lg font-semibold text-slate-50">
            Three transport roots, two critical points
          </h3>
          <p className="mt-2 text-sm leading-relaxed text-slate-300">
            The transport phase is governed by the cubic{" "}
            <Tex>{"P(z) = (z-1)\\!\\left(z-\\tfrac{64}{729}\\right)\\!\\left(z-\\tfrac{1}{729}\\right)"}</Tex>
            . Its three zeros — the <em>transport roots</em> — are
            structurally distinct from the two zeros of{" "}
            <Tex>{"P'(z) = 0"}</Tex>, the <em>critical points</em> that sit
            between consecutive roots. The <em>lower critical point</em>{" "}
            selects <Tex>{"\\delta_{\\mathrm{ph}}"}</Tex> on the retained
            branch.
          </p>

          <div className="mt-3 rounded-md border border-slate-700/40 bg-slate-950/50 px-3 py-2 text-[11px] leading-snug text-slate-300">
            <span className="font-semibold text-slate-200">
              Reading rule.
            </span>{" "}
            In the plot, transport roots of <Tex>{"P(z)"}</Tex> are drawn as
            filled circles. Critical points of <Tex>{"P'(z)"}</Tex> are drawn
            as triangles. The two are mathematically different objects.
          </div>

          <div className="mt-4 flex flex-wrap items-center gap-2 rounded-xl border border-violet-400/25 bg-violet-500/5 px-3 py-2 text-xs text-violet-100/90">
            <span className="rounded-full bg-violet-500/20 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-violet-200">
              Output flow
            </span>
            <span className="font-mono">
              <Tex>{"z_{\\mathrm{cp,low}}"}</Tex>
            </span>
            <ArrowRight size={12} aria-hidden className="text-violet-300" />
            <span className="font-mono">
              <Tex>{"\\delta_{\\mathrm{ph}}"}</Tex>
            </span>
            <ArrowRight size={12} aria-hidden className="text-violet-300" />
            <span className="font-mono">
              <Tex>{"\\delta_{\\mathrm{CKM}}"}</Tex>
            </span>
            <span className="text-violet-200/80">
              (lower critical point of P′, not the root z = 1/729)
            </span>
          </div>

          <div className="mt-6 space-y-3">
            {ROOTS.map((r, i) => (
              <motion.div
                key={r.label}
                initial={{ opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="relative overflow-hidden rounded-xl border border-slate-700/40 bg-slate-950/40 px-4 py-3"
              >
                <div
                  className={`absolute left-0 top-0 h-full w-1 bg-gradient-to-b ${r.accent}`}
                />
                <div className="flex items-baseline justify-between gap-3">
                  <div>
                    <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">
                      {r.label}
                    </div>
                    <div className="font-mono text-lg font-semibold text-slate-50">
                      z = {r.value}
                    </div>
                  </div>
                </div>
                <div className="mt-1 text-xs text-slate-400">{r.note}</div>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-3">
          <CubicChart />
        </div>
      </div>
    </div>
  );
}

function CubicChart() {
  const samples = 320;
  const xMin = -0.05;
  const xMax = 1.1;

  const data = Array.from({ length: samples }, (_, i) => {
    const z = xMin + (i / (samples - 1)) * (xMax - xMin);
    const y = (z - 1) * (z - 64 / 729) * (z - 1 / 729);
    return { z, y };
  });

  const yMin = Math.min(...data.map((d) => d.y));
  const yMax = Math.max(...data.map((d) => d.y));

  const w = 600;
  const h = 280;
  const pad = { top: 20, right: 20, bottom: 32, left: 40 };

  const xScale = (z: number) =>
    pad.left + ((z - xMin) / (xMax - xMin)) * (w - pad.left - pad.right);
  const yScale = (y: number) =>
    pad.top + ((yMax - y) / (yMax - yMin)) * (h - pad.top - pad.bottom);

  const pathData = data
    .map((d, i) => `${i === 0 ? "M" : "L"} ${xScale(d.z).toFixed(2)} ${yScale(d.y).toFixed(2)}`)
    .join(" ");

  const roots = [1 / 729, 64 / 729, 1];

  const xAxisY = yScale(0);

  return (
    <div className="relative">
      <svg
        viewBox={`0 0 ${w} ${h}`}
        className="block w-full"
        role="img"
        aria-label="Plot of the cusp cubic P(z) showing three roots at z = 1/729, 64/729, and 1"
      >
        <defs>
          <linearGradient id="cubicStroke" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#a78bfa" />
            <stop offset="50%" stopColor="#60a5fa" />
            <stop offset="100%" stopColor="#34d399" />
          </linearGradient>
          <linearGradient id="cubicFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#60a5fa" stopOpacity="0.25" />
            <stop offset="100%" stopColor="#60a5fa" stopOpacity="0" />
          </linearGradient>
        </defs>

        <g aria-hidden="true">
          {[0.2, 0.4, 0.6, 0.8, 1.0].map((t) => (
            <line
              key={t}
              x1={xScale(t)}
              x2={xScale(t)}
              y1={pad.top}
              y2={h - pad.bottom}
              stroke="rgba(148,163,184,0.08)"
              strokeWidth={1}
            />
          ))}
        </g>

        <line
          x1={pad.left}
          x2={w - pad.right}
          y1={xAxisY}
          y2={xAxisY}
          stroke="rgba(148,163,184,0.4)"
          strokeWidth={1}
        />
        <line
          x1={pad.left}
          x2={pad.left}
          y1={pad.top}
          y2={h - pad.bottom}
          stroke="rgba(148,163,184,0.4)"
          strokeWidth={1}
        />

        <motion.path
          initial={{ pathLength: 0, opacity: 0 }}
          whileInView={{ pathLength: 1, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 1.6, ease: [0.16, 1, 0.3, 1] }}
          d={pathData}
          fill="none"
          stroke="url(#cubicStroke)"
          strokeWidth={2.5}
          strokeLinecap="round"
        />

        {roots.map((r, i) => (
          <motion.g
            key={`root-${r}`}
            initial={{ opacity: 0, scale: 0 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{
              duration: 0.5,
              delay: 1.6 + i * 0.12,
              type: "spring",
            }}
          >
            <circle
              cx={xScale(r)}
              cy={xAxisY}
              r={6}
              fill={i === 0 ? "#a78bfa" : i === 1 ? "#60a5fa" : "#94a3b8"}
              stroke="#0f172a"
              strokeWidth={2}
            />
            <text
              x={xScale(r)}
              y={xAxisY + 18}
              fill="#cbd5e1"
              fontSize="10"
              fontFamily="JetBrains Mono, monospace"
              textAnchor="middle"
            >
              {i === 0 ? "1/729" : i === 1 ? "64/729" : "1"}
            </text>
          </motion.g>
        ))}

        {CUBIC_CRITICAL_POINTS.map((cp, i) => {
          const isLower = i === 0;
          const cpY = yScale(
            (cp - 1) * (cp - 64 / 729) * (cp - 1 / 729),
          );
          const triHalf = 6;
          const triPath = `M ${xScale(cp)} ${cpY - triHalf} L ${xScale(cp) - triHalf} ${cpY + triHalf} L ${xScale(cp) + triHalf} ${cpY + triHalf} Z`;
          return (
            <motion.g
              key={`cp-${i}`}
              initial={{ opacity: 0, scale: 0 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 2.0 + i * 0.15, type: "spring" }}
            >
              {isLower && (
                <>
                  <circle
                    cx={xScale(cp)}
                    cy={cpY}
                    r={14}
                    fill="#a78bfa"
                    opacity="0.18"
                  />
                  <line
                    x1={xScale(cp)}
                    x2={xScale(cp)}
                    y1={pad.top + 4}
                    y2={cpY - 8}
                    stroke="#a78bfa"
                    strokeWidth={1}
                    strokeDasharray="3 3"
                    opacity="0.55"
                  />
                </>
              )}
              <path
                d={triPath}
                fill={isLower ? "#c4b5fd" : "#fcd34d"}
                stroke="#0f172a"
                strokeWidth={1.5}
              />
              <text
                x={xScale(cp)}
                y={cpY - triHalf - 6}
                fill={isLower ? "#c4b5fd" : "#fde68a"}
                fontSize="10"
                fontFamily="JetBrains Mono, monospace"
                textAnchor="middle"
              >
                {isLower ? "z_cp,low" : "z_cp,high"}
              </text>
              {isLower && (
                <text
                  x={xScale(cp)}
                  y={pad.top - 2}
                  fill="#c4b5fd"
                  fontSize="10"
                  fontFamily="JetBrains Mono, monospace"
                  textAnchor="middle"
                >
                  selects δ_ph
                </text>
              )}
            </motion.g>
          );
        })}

        {/* Inline legend */}
        <g aria-hidden="true">
          <circle cx={pad.left + 12} cy={pad.top + 14} r={5} fill="#94a3b8" stroke="#0f172a" strokeWidth={2} />
          <text x={pad.left + 22} y={pad.top + 18} fill="#cbd5e1" fontSize="10" fontFamily="JetBrains Mono, monospace">
            roots of P(z)
          </text>
          <path
            d={`M ${pad.left + 130} ${pad.top + 9} L ${pad.left + 124} ${pad.top + 19} L ${pad.left + 136} ${pad.top + 19} Z`}
            fill="#c4b5fd"
            stroke="#0f172a"
            strokeWidth={1.5}
          />
          <text x={pad.left + 142} y={pad.top + 18} fill="#cbd5e1" fontSize="10" fontFamily="JetBrains Mono, monospace">
            critical points of P′(z)
          </text>
        </g>

        <text
          x={(w - pad.left - pad.right) / 2 + pad.left}
          y={h - 6}
          fill="#94a3b8"
          fontSize="10"
          textAnchor="middle"
        >
          z
        </text>
        <text
          x={pad.left - 28}
          y={pad.top + 12}
          fill="#94a3b8"
          fontSize="10"
        >
          P(z)
        </text>
      </svg>

      <p className="mt-3 text-center text-xs text-slate-400">
        Roots of <span className="font-mono text-slate-300">P(z)</span> and
        critical points of{" "}
        <span className="font-mono text-slate-300">P′(z)</span> are visually
        separated. The lower critical point selects{" "}
        <span className="font-mono text-slate-300">δ_ph</span> as a branch
        consequence, not a fit parameter.
      </p>
    </div>
  );
}

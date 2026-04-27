"use client";

import { motion } from "motion/react";

/**
 * Schematic plot of F_U(1)(α) crossing zero at the closed-branch root.
 *
 * The SVG is hand-shaped to be didactic, not numerically accurate: the
 * x-axis is a small interval around α⁻¹ ≈ 137.0359992, and the curve is
 * drawn so the unique positive root sits visibly between two reference
 * markers (the closed-branch root and the CODATA 2022 recommended value).
 *
 * The relative scale matters more than the absolute one — the residual
 * ≈ 3.98 × 10⁻⁸ is too small to render to scale without trickery.
 */
export function AlphaRootPlot() {
  // Schematic horizontal coordinates inside the SVG viewBox (0..600).
  const X_TFPT = 360;
  const X_CODATA = 320;
  const Y_AXIS = 200;
  const ROOT_X = X_TFPT;

  return (
    <div className="rounded-xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h4 className="font-serif text-base font-semibold text-slate-50">
          F<sub>U(1)</sub>(α) crosses zero exactly once
        </h4>
        <span className="rounded-full bg-blue-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-blue-200 ring-1 ring-blue-400/30">
          Schematic
        </span>
      </div>

      <svg
        viewBox="0 0 600 320"
        role="img"
        aria-label="Schematic plot of F_U(1)(alpha) crossing zero at the closed-branch root, with the CODATA 2022 recommended value marked nearby."
        className="mt-3 w-full"
      >
        <defs>
          <linearGradient id="rootCurve" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0" stopColor="#60a5fa" />
            <stop offset="1" stopColor="#a78bfa" />
          </linearGradient>
        </defs>

        {/* Axes */}
        <line
          x1="40"
          x2="580"
          y1={Y_AXIS}
          y2={Y_AXIS}
          stroke="#475569"
          strokeWidth="1"
        />
        <line
          x1="80"
          x2="80"
          y1="40"
          y2="290"
          stroke="#475569"
          strokeWidth="1"
        />

        {/* Axis labels */}
        <text
          x="585"
          y={Y_AXIS - 6}
          fill="#94a3b8"
          fontSize="11"
          fontFamily="ui-monospace, monospace"
        >
          α⁻¹
        </text>
        <text
          x="60"
          y="42"
          fill="#94a3b8"
          fontSize="11"
          fontFamily="ui-monospace, monospace"
        >
          F(α)
        </text>
        <text
          x="60"
          y={Y_AXIS + 4}
          fill="#94a3b8"
          fontSize="11"
          fontFamily="ui-monospace, monospace"
        >
          0
        </text>

        {/* The curve: monotone increasing through the root, slightly bent. */}
        <motion.path
          d="M 80 290
             C 180 285, 240 240, 300 220
             C 320 213, 350 207, 360 200
             C 380 192, 430 165, 480 110
             C 510 80, 540 60, 580 50"
          fill="none"
          stroke="url(#rootCurve)"
          strokeWidth="2.5"
          strokeLinecap="round"
          initial={{ pathLength: 0, opacity: 0 }}
          whileInView={{ pathLength: 1, opacity: 1 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
        />

        {/* CODATA marker — slightly to the left of the root */}
        <line
          x1={X_CODATA}
          x2={X_CODATA}
          y1={Y_AXIS - 60}
          y2={Y_AXIS + 60}
          stroke="#10b981"
          strokeWidth="1"
          strokeDasharray="3 3"
          opacity="0.7"
        />
        <circle cx={X_CODATA} cy={Y_AXIS} r="4" fill="#10b981" />
        <text
          x={X_CODATA}
          y={Y_AXIS + 80}
          fill="#34d399"
          fontSize="11"
          textAnchor="middle"
          fontFamily="ui-monospace, monospace"
        >
          CODATA 2022
        </text>
        <text
          x={X_CODATA}
          y={Y_AXIS + 95}
          fill="#94a3b8"
          fontSize="10"
          textAnchor="middle"
          fontFamily="ui-monospace, monospace"
        >
          137.035 999 177(21)
        </text>

        {/* TFPT root marker */}
        <line
          x1={ROOT_X}
          x2={ROOT_X}
          y1="40"
          y2={Y_AXIS}
          stroke="#a78bfa"
          strokeWidth="1.2"
          strokeDasharray="4 4"
          opacity="0.6"
        />
        <motion.circle
          cx={ROOT_X}
          cy={Y_AXIS}
          r="6"
          fill="#a78bfa"
          stroke="#0b1220"
          strokeWidth="2"
          initial={{ scale: 0 }}
          whileInView={{ scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 1, duration: 0.5, type: "spring" }}
        />
        <text
          x={ROOT_X}
          y="62"
          fill="#c4b5fd"
          fontSize="11"
          textAnchor="middle"
          fontFamily="ui-monospace, monospace"
        >
          α⋆⁻¹ = 137.035 999 216 8…
        </text>
        <text
          x={ROOT_X}
          y="77"
          fill="#94a3b8"
          fontSize="10"
          textAnchor="middle"
        >
          TFPT closed-branch root
        </text>

        {/* Residual bracket */}
        <g>
          <line
            x1={X_CODATA}
            x2={ROOT_X}
            y1={Y_AXIS + 30}
            y2={Y_AXIS + 30}
            stroke="#fb923c"
            strokeWidth="1.2"
          />
          <line
            x1={X_CODATA}
            x2={X_CODATA}
            y1={Y_AXIS + 26}
            y2={Y_AXIS + 34}
            stroke="#fb923c"
            strokeWidth="1.2"
          />
          <line
            x1={ROOT_X}
            x2={ROOT_X}
            y1={Y_AXIS + 26}
            y2={Y_AXIS + 34}
            stroke="#fb923c"
            strokeWidth="1.2"
          />
          <text
            x={(X_CODATA + ROOT_X) / 2}
            y={Y_AXIS + 22}
            fill="#fdba74"
            fontSize="10"
            textAnchor="middle"
            fontFamily="ui-monospace, monospace"
          >
            ≈ 3.98 × 10⁻⁸
          </text>
        </g>
      </svg>

      <p className="mt-2 text-[11px] leading-relaxed text-slate-400">
        Hand-shaped sketch — the residual is shown enlarged so it is visible.
        The actual numerical separation is 39.8 parts per billion in α⁻¹.
      </p>
    </div>
  );
}

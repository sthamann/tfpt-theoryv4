"use client";

import { motion } from "motion/react";

/**
 * The α⁻¹ fixed-point comparator — a deliberately honest σ-axis.
 *
 * At the true numeric scale (137.0359992…) the TFPT root and the CODATA value
 * are visually indistinguishable; the only meaningful axis is "distance in
 * units of the CODATA σ". So the axis IS that σ-axis, and the caption states
 * plainly that it is magnified — no fake "look how close" zoom that hides the
 * gap, and no fake "look how far" zoom that inflates it. All three numbers
 * mirror lib/predictions.ts and the AlphaVisualization comparison block.
 */
const SIGMA = 2.1e-8; // CODATA-2022 standard uncertainty on α⁻¹
const TFPT_SIGMA = 1.9; // residual in units of σ
const AXIS_MIN = -3;
const AXIS_MAX = 3;

function sigmaToPct(s: number): number {
  return ((s - AXIS_MIN) / (AXIS_MAX - AXIS_MIN)) * 100;
}

export function AlphaComparator() {
  const codataPct = sigmaToPct(0);
  const tfptPct = sigmaToPct(TFPT_SIGMA);
  const bandLeft = sigmaToPct(-1);
  const bandRight = sigmaToPct(1);

  return (
    <figure
      className="rounded-xl border border-slate-700/40 bg-slate-950/40 p-5 sm:p-6"
      aria-label="Comparator: the TFPT root sits 1.9 standard deviations above the CODATA-2022 value for the inverse fine-structure constant."
    >
      <figcaption className="flex flex-wrap items-baseline justify-between gap-2">
        <h4 className="font-serif text-base font-semibold text-slate-50">
          α⁻¹ comparator — distance in CODATA σ
        </h4>
        <span className="font-mono text-xs text-amber-200/90">Δ = +1.9σ</span>
      </figcaption>

      {/* The σ track */}
      <div className="mt-8 mb-10" role="img" aria-hidden="true">
        <div className="relative h-1.5 rounded-full bg-slate-800">
          {/* ±1σ band around CODATA */}
          <div
            className="absolute top-0 h-full rounded-full bg-emerald-500/30"
            style={{ left: `${bandLeft}%`, width: `${bandRight - bandLeft}%` }}
          />

          {/* CODATA marker */}
          <div
            className="absolute -top-1.5 h-4.5 w-0.5 -translate-x-1/2 bg-emerald-300"
            style={{ left: `${codataPct}%`, height: "1.125rem", top: "-0.375rem" }}
          />
          <div
            className="absolute -translate-x-1/2 whitespace-nowrap text-[10px] font-semibold text-emerald-200"
            style={{ left: `${codataPct}%`, top: "-1.75rem" }}
          >
            CODATA-2022
          </div>
          <div
            className="absolute -translate-x-1/2 whitespace-nowrap font-mono text-[10px] text-emerald-200/80"
            style={{ left: `${codataPct}%`, top: "0.9rem" }}
          >
            137.035 999 177(21)
          </div>

          {/* TFPT marker */}
          <motion.div
            initial={{ scaleY: 0 }}
            whileInView={{ scaleY: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            className="absolute -top-1.5 w-0.5 -translate-x-1/2 origin-bottom bg-blue-300"
            style={{ left: `${tfptPct}%`, height: "1.125rem", top: "-0.375rem" }}
          />
          <div
            className="absolute -translate-x-1/2 whitespace-nowrap text-[10px] font-semibold text-blue-200"
            style={{ left: `${tfptPct}%`, top: "-1.75rem" }}
          >
            TFPT root
          </div>
          <div
            className="absolute -translate-x-1/2 whitespace-nowrap font-mono text-[10px] text-blue-200/80"
            style={{ left: `${tfptPct}%`, top: "0.9rem" }}
          >
            137.035 999 216 8…
          </div>

          {/* σ ticks */}
          {[-3, -2, -1, 0, 1, 2, 3].map((s) => (
            <div
              key={s}
              className="absolute top-1/2 h-1 w-px -translate-x-1/2 -translate-y-1/2 bg-slate-600"
              style={{ left: `${sigmaToPct(s)}%` }}
            />
          ))}
        </div>

        {/* σ scale labels */}
        <div className="relative mt-9 h-3">
          {[-3, -2, -1, 0, 1, 2, 3].map((s) => (
            <span
              key={s}
              className="absolute -translate-x-1/2 font-mono text-[9px] text-slate-500"
              style={{ left: `${sigmaToPct(s)}%` }}
            >
              {s > 0 ? `+${s}σ` : `${s}σ`}
            </span>
          ))}
        </div>
      </div>

      <p className="text-[11px] leading-relaxed text-slate-400">
        <strong className="text-slate-300">Honest scale.</strong> The axis is in
        units of the CODATA-2022 standard uncertainty σ = 2.1 × 10⁻⁸. At the true
        numeric scale the two values are visually identical to ~10 significant
        figures; this axis is magnified about 3.4 × 10⁹× so the 1.9σ residual
        (Δα⁻¹ ≈ 3.98 × 10⁻⁸) is visible at all. It is a fixed point, not a fit —
        and the residual is the live kill test.
      </p>
    </figure>
  );
}

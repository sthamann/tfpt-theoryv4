"use client";

import { motion } from "motion/react";
import { Math } from "./Math";

/**
 * ThermalSeamLegs -- animated visual for v526 (SEAM.THERMAL.KMS.01):
 * the three legs of c3 -- geometry (v58), anomaly/modular normalisation (v208)
 * and the MEASURED seam temperature (v526) -- converge on c3 = 1/(8pi).
 * Design language mirrors GravityEmergence.
 */

const LEGS = [
  {
    id: "geo",
    label: "Geometry",
    sub: "one-sided Gauss–Bonnet",
    formula: "c_3 = \\frac{1}{|\\mathbb{Z}_2|\\cdot 2\\pi\\,\\chi(S^2)} = \\frac{1}{8\\pi}",
    note: "seam winding 8 = 2|μ₄|",
    ring: "ring-sky-400/40",
    badge: "bg-sky-500/15 text-sky-200",
    src: "v58",
  },
  {
    id: "anomaly",
    label: "Anomaly / modular",
    sub: "Bisognano–Wichmann KMS",
    formula: "T_H = \\frac{\\kappa}{2\\pi},\\quad \\frac{1}{2\\pi} = 4c_3",
    note: "Δ^{it} = e^{−2πtK_H}",
    ring: "ring-amber-400/40",
    badge: "bg-amber-500/15 text-amber-200",
    src: "v208",
  },
  {
    id: "temp",
    label: "Temperature — measured",
    sub: "detailed balance on the free OS quotient",
    formula: "\\beta_{\\mathrm{angle}} = 2\\pi\\ \\text{exact} \\;\\Rightarrow\\; T_{\\mathrm{seam}} = 4c_3",
    note: "β = N clock steps (N = 8 and 16)",
    ring: "ring-emerald-400/40",
    badge: "bg-emerald-500/15 text-emerald-200",
    src: "v526",
  },
];

export function ThermalSeamLegs() {
  return (
    <div className="mt-8 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h4 className="font-serif text-base font-semibold text-slate-50">
          The seam is thermal — three legs of <span className="font-mono">c₃</span>
        </h4>
        <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-emerald-200 ring-1 ring-emerald-400/30">
          v526 · [E]/[C]
        </span>
      </div>

      <p className="mt-2 text-xs leading-relaxed text-slate-400">
        The Hawking normalisation is no longer only postulated into the horizon sector: the
        reconstructed free seam OS quotient admits exactly <em>one</em> detailed-balance thermal
        representation, and its temperature comes out{" "}
        <span className="font-mono">T_seam = 4c₃</span> — the same{" "}
        <strong className="text-slate-200">Bisognano–Wichmann/Hawking normalisation</strong> the
        geometry and anomaly legs carry. Temperature is the{" "}
        <strong className="text-slate-200">third leg</strong> of{" "}
        <span className="font-mono">c₃ = 1/(8π)</span>.
      </p>

      {/* three legs */}
      <div className="mt-5 grid gap-3 sm:grid-cols-3">
        {LEGS.map((o, i) => (
          <motion.div
            key={o.id}
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.45, delay: i * 0.12 }}
            className={`rounded-xl border border-slate-700/40 bg-slate-950/60 p-3 ring-1 ${o.ring}`}
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-semibold uppercase tracking-widest text-slate-300">
                {o.label}
              </span>
              <span className={`rounded px-1.5 py-0.5 font-mono text-[9px] font-semibold ${o.badge}`}>
                {o.src}
              </span>
            </div>
            <div className="mt-0.5 text-[11px] text-slate-500">{o.sub}</div>
            <div className="mt-2 text-slate-100">
              <Math>{o.formula}</Math>
            </div>
            <div className="mt-1 font-mono text-[10px] text-slate-400">{o.note}</div>
          </motion.div>
        ))}
      </div>

      {/* converge arrow */}
      <motion.div
        initial={{ opacity: 0, scaleY: 0.4 }}
        whileInView={{ opacity: 1, scaleY: 1 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.4, delay: 0.45 }}
        className="mx-auto mt-3 flex flex-col items-center text-slate-500"
        aria-hidden
      >
        <div className="flex w-full max-w-md items-center justify-around text-lg">
          <span>↘</span>
          <span>↓</span>
          <span>↙</span>
        </div>
      </motion.div>

      {/* convergence node */}
      <motion.div
        initial={{ opacity: 0, scale: 0.85 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true, amount: 0.4 }}
        transition={{ duration: 0.5, delay: 0.6, type: "spring", stiffness: 120 }}
        className="mx-auto max-w-md rounded-xl border border-emerald-400/40 bg-emerald-500/5 p-3 text-center"
      >
        <div className="text-[10px] font-semibold uppercase tracking-widest text-emerald-200/90">
          geometry + anomaly + temperature
        </div>
        <div className="mt-1 text-emerald-50">
          <Math>{"c_3 = \\tfrac{1}{8\\pi}, \\qquad T_H = \\tfrac{c_3}{M} = \\tfrac{1}{8\\pi M}"}</Math>
        </div>
        <div className="mt-1.5 text-[11px] leading-snug text-emerald-100/80">
          the axiom <strong>is</strong> the Hawking coefficient — now derived from the seam KMS
          structure; SdS <Math>{"\\tfrac{1}{4\\pi} = 2c_3"}</Math>, Nariai{" "}
          <Math>{"T_N = 4c_3\\sqrt{\\Lambda}"}</Math>
        </div>
      </motion.div>

      <div className="mt-4 rounded-md border border-slate-700/40 bg-slate-950/60 p-3 text-[11px] leading-relaxed text-slate-300">
        <strong className="text-slate-100">Honest fences.</strong> The [C]-typed reading is
        &ldquo;seam euclidean circle = thermal circle of the reconstructed horizon dynamics&rdquo;;
        &ldquo;the seam <em>is</em> a horizon&rdquo; stays [C]. The temperature bridge closes, the
        entropy-<em>fraction</em> bridge (the v129 fractions {"{1/3, 2/3}"}, the v190 floor) honestly
        does not; the non-compact control has <span className="font-mono">T = 0</span> — the
        temperature hangs exactly on compactness of the euclidean circle (
        <span className="font-mono">v526</span>, no marker moves).
      </div>
    </div>
  );
}

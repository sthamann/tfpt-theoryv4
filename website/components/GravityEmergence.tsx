"use client";

import { motion } from "motion/react";
import { Math } from "./Math";

/**
 * GravityEmergence -- animated visual for v358 (GRAV.ENTROPY.EQUILIBRIUM.01):
 * the three independent origins of c3 converge to 1/(8pi), the thermodynamic and
 * geometric origins coincide via |mu4| = |Z2|*chi = 4, and the entanglement first
 * law delta S = delta<K> yields the parameter-free linearised Einstein equation.
 */

const ORIGINS = [
  {
    id: "anchor",
    label: "Anchor",
    sub: "a = (1,1,2)",
    formula: "c_3 = \\frac{1}{2\\,e_1(a)\\,\\pi}",
    note: "e₁(a) = 4",
    ring: "ring-amber-400/40",
    badge: "bg-amber-500/15 text-amber-200",
    src: "v23",
  },
  {
    id: "geo",
    label: "Geometry",
    sub: "one-sided Gauss–Bonnet",
    formula: "c_3 = \\frac{1}{|\\mathbb{Z}_2|\\,2\\pi\\,\\chi(S^2)}",
    note: "|Z₂|·χ = 2·2",
    ring: "ring-sky-400/40",
    badge: "bg-sky-500/15 text-sky-200",
    src: "v58",
  },
  {
    id: "thermo",
    label: "Thermodynamics",
    sub: "entanglement first law",
    formula: "c_3 = \\frac{\\eta}{2\\pi},\\ \\eta = \\frac{1}{|\\mu_4|}",
    note: "δS = δ⟨K⟩",
    ring: "ring-violet-400/40",
    badge: "bg-violet-500/15 text-violet-200",
    src: "v358",
  },
];

export function GravityEmergence() {
  return (
    <div className="mt-8 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h4 className="font-serif text-base font-semibold text-slate-50">
          Gravity is parameter-free — three origins of <span className="font-mono">c₃</span> converge
        </h4>
        <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-emerald-200 ring-1 ring-emerald-400/30">
          v358 / v359 · [E]
        </span>
      </div>

      <p className="mt-2 text-xs leading-relaxed text-slate-400">
        The entanglement first law <Math>{"\\delta S = \\delta\\langle K\\rangle"}</Math> (Jacobson;
        Faulkner et al.), run with TFPT&rsquo;s atoms, gives the <em>full covariant</em> Einstein equation
        (fixed-volume stationarity → the Einstein tensor, v359) with <strong className="text-slate-200">both
        coefficients fixed</strong> — no free dimensionless dial. The seam constant{" "}
        <span className="font-mono">c₃ = 1/(8π)</span> arrives by{" "}
        <strong className="text-slate-200">three independent routes</strong> that all agree.
      </p>

      {/* three origins */}
      <div className="mt-5 grid gap-3 sm:grid-cols-3">
        {ORIGINS.map((o, i) => (
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

      {/* convergence node: c3 = 1/(8pi) */}
      <motion.div
        initial={{ opacity: 0, scale: 0.85 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true, amount: 0.4 }}
        transition={{ duration: 0.5, delay: 0.6, type: "spring", stiffness: 120 }}
        className="mx-auto max-w-md rounded-xl border border-emerald-400/40 bg-emerald-500/5 p-3 text-center"
      >
        <div className="text-[10px] font-semibold uppercase tracking-widest text-emerald-200/90">
          triply over-determined
        </div>
        <div className="mt-1 text-emerald-50">
          <Math>{"c_3 = \\tfrac{1}{8\\pi}\\quad\\Longrightarrow\\quad c_3^{-1} = 8\\pi"}</Math>
        </div>
        <div className="mt-1.5 text-[11px] leading-snug text-emerald-100/80">
          thermo origin <Math>{"2\\pi/\\eta"}</Math> <strong>=</strong> geo origin{" "}
          <Math>{"|\\mathbb{Z}_2|\\,2\\pi\\,\\chi"}</Math> &nbsp;iff&nbsp;{" "}
          <span className="font-mono">|μ₄| = |Z₂|·χ = 4</span>
        </div>
      </motion.div>

      {/* result */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.4 }}
        transition={{ duration: 0.5, delay: 0.85 }}
        className="mt-4 rounded-xl border border-blue-400/30 bg-blue-500/5 p-4 text-center"
      >
        <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-200/90">
          parameter-free Einstein equation (full covariant)
        </div>
        <div className="mt-1 text-lg text-blue-50">
          <Math>{"G_{ab} + \\Lambda g_{ab} = c_3^{-1}\\, T_{ab} = 8\\pi\\, T_{ab}"}</Math>
        </div>
        <div className="mt-1 text-[11px] text-blue-100/75">
          no free dimensionless Newton dial — <span className="font-mono">G</span> is the one unit{" "}
          <span className="font-mono">v_geo</span>
        </div>
      </motion.div>

      <div className="mt-4 rounded-md border border-slate-700/40 bg-slate-950/60 p-3 text-[11px] leading-relaxed text-slate-300">
        <strong className="text-slate-100">Honest residual.</strong> This closes the{" "}
        <em>full covariant</em> equation parameter-free (v359: fixed-volume → the Einstein tensor, with
        Lovelock making matter conservation an output); the matter flux is assembled (the Casini–Huerta–Myers
        ball modular Hamiltonian, boost via Bisognano–Wichmann, <span className="font-mono">v323</span>) and
        the entropy density is atom-fixed (<span className="font-mono">1/4 = 1/|μ₄|</span>, central charge{" "}
        <span className="font-mono">c = g_car + N_fam = 8</span>). What remains is the Jacobson
        equation-of-state status (an external candidate action — Bianconi&apos;s entropic action, PRD 111, 066001
        (2025) — is quantified in <span className="font-mono">v473</span>–<span className="font-mono">v478</span>:{" "}
        <span className="font-mono">β′_B = c₃/6</span> pinned, the R² kill test executed and resolved as a
        scale-measure datum, the compression conjecture made well-posed — all without changing the typing), the
        global ambient measure (<span className="font-mono">QG.AMB.01</span>), and the absolute scale{" "}
        <span className="font-mono">v_geo</span>.
      </div>
    </div>
  );
}

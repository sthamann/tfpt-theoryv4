"use client";

import { useEffect, useRef, useState } from "react";
import { motion } from "motion/react";

/**
 * UniversalGapLab — an animated visualisation of the new (v383–v391) findings.
 *
 * Three linked views, every number grounded in a verification module (nothing
 * invented here):
 *
 *  A. "Every sector is the same gapped operator" — the contraction
 *     iterₙ = x* + rⁿ(x₀ − x*) racing to its attractor at the spectral-gap
 *     rate r = λ₂/λ₁. Seam-gapped sectors carry r = (2/3)⁶ (v303/v387/v388);
 *     the discrete compiler the golden (φ+2)/4 (v312/v387); a no-gap r = 1
 *     never forgets its start (the Lean theorem no_gap_no_forget,
 *     FORM.SPECTRALGAP.01). This is also the typed correction budget: the rate
 *     IS the first-correction size (v388).
 *  B. The entire-form-factor graviton (v386/v389): the dressed/GR ratio e^{-u}
 *     (u = p²/M²) falls faster than any power — finite, ghost-free, UV-soft.
 *  C. The residual is certification, not construction (v384): every open item
 *     is external (A math proof / B theorem-forbidden / C external physics);
 *     the "internal mechanisms" bin is empty.
 */

type Sector = {
  label: string;
  rate: number;
  rateLabel: string;
  facet: string;
  tone: string;
  dot: string;
};

const SECTORS: Sector[] = [
  {
    label: "Flavor (Koide F_pole)",
    rate: (2 / 3) ** 6,
    rateLabel: "(2/3)⁶ ≈ 0.088",
    facet: "prime-3 · family",
    tone: "text-emerald-200",
    dot: "#34d399",
  },
  {
    label: "Horizon recovery",
    rate: (2 / 3) ** 6,
    rateLabel: "(2/3)⁶ ≈ 0.088",
    facet: "prime-3 · family",
    tone: "text-emerald-200",
    dot: "#10b981",
  },
  {
    label: "QG decoupling bound",
    rate: (2 / 3) ** 6,
    rateLabel: "(2/3)⁶ · χ=729/665",
    facet: "prime-3 · family",
    tone: "text-teal-200",
    dot: "#2dd4bf",
  },
  {
    label: "Discrete compiler",
    rate: (5 + Math.sqrt(5)) / 8,
    rateLabel: "(φ+2)/4 ≈ 0.905",
    facet: "prime-5 · carrier",
    tone: "text-amber-200",
    dot: "#fbbf24",
  },
  {
    label: "No spectral gap (r = 1)",
    rate: 1,
    rateLabel: "r = 1 — no gap",
    facet: "start never forgotten",
    tone: "text-rose-200",
    dot: "#fb7185",
  },
];

const RESIDUALS: { id: string; kind: "A" | "B" | "C"; note: string }[] = [
  { id: "SEAM.EQUIV.01", kind: "A", note: "cited MMST/Adamo continuum theorem (v336)" },
  { id: "ALPHA.QUILLEN.EXACT.01", kind: "A", note: "Quillen ζ-functional (v382; reduced v391, grounded v433)" },
  { id: "QG.AMB.01", kind: "A", note: "constructive measure, a [C] redundancy (v369)" },
  { id: "v_geo", kind: "B", note: "the one metrology unit — No-Unit theorem (v153/v364)" },
  { id: "F_transfer", kind: "C", note: "QCD / Boltzmann / relic (v371–v374, firewall v187)" },
];

const KIND_META: Record<"A" | "B" | "C", { label: string; tone: string }> = {
  A: { label: "External math proof", tone: "border-blue-400/30 bg-blue-500/5 text-blue-200" },
  B: { label: "Theorem-forbidden", tone: "border-violet-400/30 bg-violet-500/5 text-violet-200" },
  C: { label: "External physics", tone: "border-amber-400/30 bg-amber-500/5 text-amber-200" },
};

/** View A: the convergence-to-attractor animation (the universal gap). */
function GapConvergence() {
  const [n, setN] = useState(0);
  const [playing, setPlaying] = useState(true);
  const raf = useRef<number | null>(null);
  const t0 = useRef<number | null>(null);

  useEffect(() => {
    if (!playing) return;
    const N_MAX = 10;
    const PERIOD = 7000; // ms for a full 0→N_MAX→reset cycle
    const step = (ts: number) => {
      if (t0.current === null) t0.current = ts;
      const elapsed = (ts - t0.current) % PERIOD;
      setN((elapsed / PERIOD) * N_MAX);
      raf.current = requestAnimationFrame(step);
    };
    raf.current = requestAnimationFrame(step);
    return () => {
      if (raf.current) cancelAnimationFrame(raf.current);
      t0.current = null;
    };
  }, [playing]);

  const W = 560;
  const trackLeft = 176;
  const trackRight = W - 28;
  const trackLen = trackRight - trackLeft;

  return (
    <div className="rounded-2xl border border-slate-700/40 bg-slate-950/50 p-5">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-[10px] font-semibold uppercase tracking-widest text-emerald-300/80">
            A · every sector is the same gapped operator
          </div>
          <div className="mt-1 font-serif text-lg text-slate-100">
            iterₙ = x⋆ + rⁿ(x₀ − x⋆) → the unique attractor
          </div>
        </div>
        <button
          type="button"
          onClick={() => setPlaying((p) => !p)}
          className="rounded-full border border-slate-600/60 bg-slate-900/60 px-3 py-1 text-xs font-semibold text-slate-200 transition-colors hover:bg-slate-800/80"
        >
          {playing ? "Pause" : "Play"}
        </button>
      </div>

      <svg viewBox={`0 0 ${W} 250`} className="mt-4 w-full" role="img" aria-label="Each sector contracts to its attractor at its spectral-gap rate; a gapless r=1 sector never converges.">
        {/* start (x₀) and attractor (x⋆) reference lines */}
        <line x1={trackLeft} y1={20} x2={trackLeft} y2={232} stroke="#475569" strokeDasharray="3 3" strokeWidth={1} />
        <text x={trackLeft} y={246} fill="#94a3b8" fontSize={10} textAnchor="start">x₀ (start)</text>
        <line x1={trackRight} y1={20} x2={trackRight} y2={232} stroke="#64748b" strokeDasharray="3 3" strokeWidth={1} />
        <text x={trackRight} y={246} fill="#94a3b8" fontSize={10} textAnchor="end">x⋆ (attractor)</text>
        {SECTORS.map((s, i) => {
          const y = 30 + i * 42;
          const dev = Math.pow(s.rate, n); // deviation rⁿ ∈ (0,1]
          // x₀ sits at the left (deviation 1); the attractor x⋆ at the right
          // (deviation 0). As n grows the dot converges rightward; r = 1 stays put.
          const cx = trackRight - trackLen * dev;
          return (
            <g key={s.label}>
              <text x={8} y={y + 4} fill="currentColor" fontSize={11} className={s.tone}>
                {s.label}
              </text>
              <text x={8} y={y + 17} fill="#64748b" fontSize={9}>
                {s.rateLabel} · {s.facet}
              </text>
              <line x1={trackLeft} y1={y} x2={trackRight} y2={y} stroke="#1e293b" strokeWidth={6} strokeLinecap="round" />
              <line x1={trackLeft} y1={y} x2={cx} y2={y} stroke={s.dot} strokeWidth={6} strokeLinecap="round" opacity={0.5} />
              <circle cx={cx} cy={y} r={6} fill={s.dot} />
            </g>
          );
        })}
      </svg>

      <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
        <span>
          step n = <span className="font-mono text-slate-200">{n.toFixed(1)}</span>
        </span>
        <span>
          the rate r <span className="text-slate-300">is</span> the first-correction size (v388); r = 1 never forgets x₀ (Lean <span className="font-mono">FORM.SPECTRALGAP.01</span>)
        </span>
      </div>
    </div>
  );
}

/** View B: the entire-form-factor graviton ratio e^{-u}. */
function FormFactor() {
  const [playing, setPlaying] = useState(true);
  const [u, setU] = useState(0);
  const raf = useRef<number | null>(null);
  const t0 = useRef<number | null>(null);
  const U_MAX = 8;

  useEffect(() => {
    if (!playing) return;
    const PERIOD = 6000;
    const step = (ts: number) => {
      if (t0.current === null) t0.current = ts;
      const e = (ts - t0.current) % PERIOD;
      setU((e / PERIOD) * U_MAX);
      raf.current = requestAnimationFrame(step);
    };
    raf.current = requestAnimationFrame(step);
    return () => {
      if (raf.current) cancelAnimationFrame(raf.current);
      t0.current = null;
    };
  }, [playing]);

  const W = 560;
  const H = 220;
  const padL = 40;
  const padR = 20;
  const padT = 16;
  const padB = 30;
  const x = (uu: number) => padL + ((W - padL - padR) * uu) / U_MAX;
  const y = (v: number) => padT + (H - padT - padB) * (1 - v);
  const dressed = (uu: number) => Math.exp(-uu); // dressed/GR ratio
  const power = (uu: number) => 1 / (1 + uu); // a 1/(1+u) power-law comparison
  const pts = (f: (uu: number) => number) =>
    Array.from({ length: 121 }, (_, k) => {
      const uu = (U_MAX * k) / 120;
      return `${x(uu).toFixed(1)},${y(f(uu)).toFixed(1)}`;
    }).join(" ");

  return (
    <div className="rounded-2xl border border-slate-700/40 bg-slate-950/50 p-5">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
            B · the entire-form-factor graviton (v386 / v389)
          </div>
          <div className="mt-1 font-serif text-lg text-slate-100">
            dressed / GR ratio e<sup>−u</sup>, u = p²/M²
          </div>
        </div>
        <button
          type="button"
          onClick={() => setPlaying((p) => !p)}
          className="rounded-full border border-slate-600/60 bg-slate-900/60 px-3 py-1 text-xs font-semibold text-slate-200 transition-colors hover:bg-slate-800/80"
        >
          {playing ? "Pause" : "Play"}
        </button>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className="mt-4 w-full" role="img" aria-label="The dressed/GR ratio e^-u falls faster than the power law 1/(1+u): UV-softened, ghost-free.">
        <line x1={padL} y1={y(0)} x2={W - padR} y2={y(0)} stroke="#334155" strokeWidth={1} />
        <line x1={padL} y1={padT} x2={padL} y2={y(0)} stroke="#334155" strokeWidth={1} />
        <text x={padL - 6} y={y(1) + 3} fill="#64748b" fontSize={9} textAnchor="end">1</text>
        <text x={padL - 6} y={y(0) + 3} fill="#64748b" fontSize={9} textAnchor="end">0</text>
        <text x={W - padR} y={H - 8} fill="#64748b" fontSize={9} textAnchor="end">u →</text>
        {/* power-law comparison */}
        <polyline points={pts(power)} fill="none" stroke="#64748b" strokeWidth={1.5} strokeDasharray="4 3" />
        <text x={x(6)} y={y(power(6)) - 6} fill="#94a3b8" fontSize={9}>1/(1+u) — power law</text>
        {/* dressed ratio */}
        <polyline points={pts(dressed)} fill="none" stroke="#60a5fa" strokeWidth={2.5} />
        <text x={x(2.4)} y={y(dressed(2.4)) - 8} fill="#93c5fd" fontSize={10}>e^(−u) — faster than any power</text>
        {/* single pole / GR limit at u=0 */}
        <circle cx={x(0)} cy={y(1)} r={4} fill="#a78bfa" />
        <text x={x(0) + 6} y={y(1) - 4} fill="#c4b5fd" fontSize={9}>single pole at u=0 (GR + −u)</text>
        {/* sweep marker */}
        <line x1={x(u)} y1={padT} x2={x(u)} y2={y(0)} stroke="#f8fafc" strokeOpacity={0.25} strokeWidth={1} />
        <circle cx={x(u)} cy={y(dressed(u))} r={4} fill="#f8fafc" />
      </svg>

      <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
        <span>
          u = <span className="font-mono text-slate-200">{u.toFixed(2)}</span>,{" "}
          e<sup>−u</sup> = <span className="font-mono text-slate-200">{Math.exp(-u).toExponential(2)}</span>
        </span>
        <span>ghost-free, UV-soft, finite at every loop order by power counting (v389)</span>
      </div>
    </div>
  );
}

/** View C: the residual is certification, not construction (v384). */
function ResidualCertification() {
  return (
    <div className="rounded-2xl border border-slate-700/40 bg-slate-950/50 p-5">
      <div className="text-[10px] font-semibold uppercase tracking-widest text-slate-300/80">
        C · the residual is certification, not construction (v384)
      </div>
      <div className="mt-1 font-serif text-lg text-slate-100">
        every open item is external — zero open internal mechanisms
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        {(["A", "B", "C"] as const).map((kind) => (
          <div key={kind} className={`rounded-xl border p-3 ${KIND_META[kind].tone}`}>
            <div className="flex items-center gap-2">
              <span className="font-mono text-sm font-semibold">{kind}</span>
              <span className="text-[10px] font-semibold uppercase tracking-widest opacity-80">
                {KIND_META[kind].label}
              </span>
            </div>
            <ul className="mt-2 space-y-2">
              {RESIDUALS.filter((r) => r.kind === kind).map((r, i) => (
                <motion.li
                  key={r.id}
                  initial={{ opacity: 0, y: 6 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.1 * i }}
                  className="rounded-lg bg-slate-900/50 px-2.5 py-1.5"
                >
                  <span className="font-mono text-[11px] text-slate-100">{r.id}</span>
                  <span className="block text-[10px] leading-snug text-slate-400">{r.note}</span>
                </motion.li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ delay: 0.5 }}
        className="mt-3 flex items-center justify-between rounded-xl border border-dashed border-rose-400/30 bg-rose-500/5 px-4 py-3"
      >
        <span className="text-[11px] font-semibold uppercase tracking-widest text-rose-200/80">
          Open internal TFPT mechanisms
        </span>
        <span className="font-serif text-2xl font-semibold text-rose-100">0 — none</span>
      </motion.div>
    </div>
  );
}

export function UniversalGapLab() {
  return (
    <div className="grid gap-5 lg:grid-cols-2">
      <div className="lg:col-span-2">
        <GapConvergence />
      </div>
      <FormFactor />
      <ResidualCertification />
    </div>
  );
}

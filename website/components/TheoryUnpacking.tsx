"use client";

import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, Pause, Play } from "lucide-react";
import { Math } from "./Math";
import { cn } from "@/lib/utils";

/**
 * Animated 6-frame "theory unpacking" diagram.
 *
 * The narrative shows what TFPT does to reality — geometrically — in six
 * tightly-coupled steps:
 *
 *   1. Boundary datum (one-sided half-manifold)
 *   2. Exact double via τ_dbl (mirror reflects, seam appears)
 *   3. Calderón polarization (positive / negative split)
 *   4. Carrier involution → 3 + 2 rank split
 *   5. Counting via [u_Σ] = 1 (3 families · 1 doublet)
 *   6. Closed branch T★ → bridge readouts (α⁻¹, λ_C, sin²θ_13, θ_eff = 0)
 *
 * The component runs an autoplay cycle but pauses when the user clicks a
 * step pip, the play/pause button, or hovers over the canvas. It also
 * respects `prefers-reduced-motion` and stays on the final frame in that
 * case.
 */

interface UnpackingStep {
  id: number;
  badge: string;
  title: string;
  body: string;
  formula: string;
}

const STEPS: UnpackingStep[] = [
  {
    id: 0,
    badge: "Frame 1",
    title: "One-sided boundary datum",
    body: "Reality enters as a single spectral datum on a seam-bounded half-space. No bulk, no carrier, no Standard Model yet — only the boundary primitive.",
    formula:
      "\\mathfrak{T}_\\partial = (\\mathcal{A}_+, \\mathcal{H}_+, D_+, J, \\Gamma, B_\\Sigma)",
  },
  {
    id: 1,
    badge: "Frame 2",
    title: "Exact double via τ_dbl",
    body: "The half-space is reflected across its boundary into an exact double. The shared edge becomes the seam Σ — the involution τ_dbl is the only structure carried across.",
    formula:
      "\\tau_{\\mathrm{dbl}}: \\mathfrak{T}_\\partial \\rightsquigarrow \\mathfrak{T}_{\\min}^{\\mathrm{cl}}",
  },
  {
    id: 2,
    badge: "Frame 3",
    title: "Calderón polarization ι_C",
    body: "The doubled datum splits canonically into positive and negative polarization sectors. The split is not chosen — it is the boundary projector of D acting on the double.",
    formula:
      "\\iota_C: \\mathcal{H} = \\mathcal{H}_+ \\oplus \\mathcal{H}_-",
  },
  {
    id: 3,
    badge: "Frame 4",
    title: "Carrier ε_car → 3 + 2",
    body: "The polarization induces a finite carrier involution. Compact Higgs index forces dim E₊ = 2; primitive Yukawa type forces dim E₋ = 3. The 3 + 2 split is derived, not assumed.",
    formula:
      "E = E_- \\oplus E_+, \\quad (\\dim E_-, \\dim E_+) = (3, 2)",
  },
  {
    id: 4,
    badge: "Frame 5",
    title: "Counting via [u_Σ] = 1",
    body: "The unit seam class fixes 3 chiral families on E₋ and exactly one weak doublet on E₊. The Standard-Model packet emerges as a counting consequence.",
    formula:
      "[u_\\Sigma] = 1 \\;\\Rightarrow\\; N_{\\mathrm{fam}} = 3,\\; N_\\Phi = 1",
  },
  {
    id: 5,
    badge: "Frame 6",
    title: "Closed branch T★ → observables",
    body: "The closed branch projects onto bridge readouts. α, λ_C, sin²θ_13, β_rad, and the strong-CP null θ_eff = 0 all read off the same admissibility data — none are fitted.",
    formula:
      "\\alpha^{-1}(0) = 137.035\\,999\\,217\\,\\ldots,\\;\\; \\theta_{\\mathrm{eff}} = 0",
  },
];

const FRAME_MS = 5500;

export function TheoryUnpacking() {
  const reduced = useReducedMotion();
  const [step, setStep] = useState(reduced ? STEPS.length - 1 : 0);
  const [playing, setPlaying] = useState(!reduced);
  const [hovered, setHovered] = useState(false);

  useEffect(() => {
    if (!playing || hovered || reduced) return;
    const id = window.setInterval(
      () => setStep((s) => (s + 1) % STEPS.length),
      FRAME_MS,
    );
    return () => window.clearInterval(id);
  }, [playing, hovered, reduced]);

  const current = STEPS[step];
  const next = () => {
    setPlaying(false);
    setStep((s) => (s + 1) % STEPS.length);
  };
  const prev = () => {
    setPlaying(false);
    setStep((s) => (s - 1 + STEPS.length) % STEPS.length);
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className="glass mx-auto mt-12 max-w-6xl overflow-hidden rounded-2xl ring-1 ring-slate-700/40"
      aria-label="Animated theory unpacking — six geometric frames"
      aria-roledescription="carousel"
    >
      <header className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Theory unpacking · how TFPT reconstructs reality, in 6 frames
        </span>
        <div className="flex items-center gap-1.5">
          <button
            type="button"
            onClick={prev}
            aria-label="Previous frame"
            className="rounded-full bg-slate-900/60 p-1.5 text-slate-300 ring-1 ring-slate-700/40 transition-colors hover:bg-slate-800/80 hover:text-white"
          >
            <ChevronLeft size={12} aria-hidden />
          </button>
          <button
            type="button"
            onClick={() => setPlaying((p) => !p)}
            aria-label={playing ? "Pause autoplay" : "Resume autoplay"}
            aria-pressed={playing}
            className="rounded-full bg-slate-900/60 p-1.5 text-slate-300 ring-1 ring-slate-700/40 transition-colors hover:bg-slate-800/80 hover:text-white"
            disabled={!!reduced}
            title={
              reduced
                ? "Autoplay disabled — prefers-reduced-motion"
                : playing
                  ? "Pause"
                  : "Play"
            }
          >
            {playing && !reduced ? (
              <Pause size={12} aria-hidden />
            ) : (
              <Play size={12} aria-hidden />
            )}
          </button>
          <button
            type="button"
            onClick={next}
            aria-label="Next frame"
            className="rounded-full bg-slate-900/60 p-1.5 text-slate-300 ring-1 ring-slate-700/40 transition-colors hover:bg-slate-800/80 hover:text-white"
          >
            <ChevronRight size={12} aria-hidden />
          </button>
        </div>
      </header>

      <div
        className="grid gap-0 lg:grid-cols-[3fr_2fr]"
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        <div className="border-b border-slate-800/60 lg:border-b-0 lg:border-r">
          <UnpackingCanvas step={step} />
        </div>

        <div className="p-6 lg:p-7">
          <AnimatePresence mode="wait">
            <motion.div
              key={current.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
            >
              <div className="flex items-center gap-2">
                <span className="rounded-full bg-blue-500/15 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-blue-200 ring-1 ring-blue-400/30">
                  {current.badge}
                </span>
                <span className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
                  {current.id + 1} / {STEPS.length}
                </span>
              </div>
              <h3 className="mt-3 font-serif text-xl font-semibold leading-snug text-slate-50">
                {current.title}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-300">
                {current.body}
              </p>
              <div className="mt-4 overflow-x-auto formula-scroll rounded-md border border-slate-700/40 bg-slate-950/60 p-3">
                <Math block>{current.formula}</Math>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      <div
        role="tablist"
        aria-label="Frame navigation"
        className="grid grid-cols-6 gap-1 border-t border-slate-800/60 bg-slate-950/40 px-3 py-3 sm:gap-1.5 sm:px-5"
      >
        {STEPS.map((s) => {
          const active = step === s.id;
          return (
            <button
              key={s.id}
              type="button"
              role="tab"
              aria-selected={active}
              aria-label={`${s.badge}: ${s.title}`}
              onClick={() => {
                setStep(s.id);
                setPlaying(false);
              }}
              className="group relative h-1.5 overflow-hidden rounded-full bg-slate-700/40 transition-colors hover:bg-slate-600/50"
            >
              <span
                aria-hidden="true"
                className={cn(
                  "block h-full origin-left rounded-full bg-gradient-to-r from-blue-400 to-violet-400 transition-transform duration-500 ease-out",
                  active ? "scale-x-100" : "scale-x-0",
                )}
              />
            </button>
          );
        })}
      </div>
    </motion.section>
  );
}

/* ---------- SVG canvas ----------------------------------------------- */

const CX = 480;
const CY = 270;
const R = 180;
const VIEW_W = 960;
const VIEW_H = 540;

/**
 * Helpful step gates. `from` is the smallest step at which the given layer
 * starts being visible; before that it is animated to opacity 0.
 */
const visible = (step: number, from: number) => step >= from;

function UnpackingCanvas({ step }: { step: number }) {
  return (
    <div className="relative aspect-[16/9] w-full">
      <svg
        viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
        className="absolute inset-0 h-full w-full"
        role="img"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="halfNeg" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stopColor="#60a5fa" stopOpacity="0.45" />
            <stop offset="1" stopColor="#60a5fa" stopOpacity="0.05" />
          </linearGradient>
          <linearGradient id="halfPos" x1="1" y1="0" x2="0" y2="0">
            <stop offset="0" stopColor="#a78bfa" stopOpacity="0.45" />
            <stop offset="1" stopColor="#a78bfa" stopOpacity="0.05" />
          </linearGradient>
          <radialGradient id="closedGlow" cx="0.5" cy="0.5" r="0.7">
            <stop offset="0" stopColor="#34d399" stopOpacity="0.35" />
            <stop offset="1" stopColor="#34d399" stopOpacity="0" />
          </radialGradient>
          <linearGradient id="seamGlow" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#a78bfa" stopOpacity="0" />
            <stop offset="0.4" stopColor="#a78bfa" stopOpacity="0.9" />
            <stop offset="0.6" stopColor="#60a5fa" stopOpacity="0.9" />
            <stop offset="1" stopColor="#60a5fa" stopOpacity="0" />
          </linearGradient>
          <pattern
            id="bgGrid"
            width="40"
            height="40"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M 40 0 L 0 0 0 40"
              fill="none"
              stroke="rgba(148,163,184,0.05)"
              strokeWidth="1"
            />
          </pattern>
        </defs>

        {/* Background grid */}
        <rect
          x="0"
          y="0"
          width={VIEW_W}
          height={VIEW_H}
          fill="url(#bgGrid)"
          opacity="0.7"
        />

        {/* Closed-branch glow (final frame) */}
        <motion.circle
          cx={CX}
          cy={CY}
          r={R + 80}
          fill="url(#closedGlow)"
          animate={{ opacity: visible(step, 5) ? 0.9 : 0 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
        />

        {/* ---- Layer 1: left half-disk (boundary datum) ---- */}
        <motion.g
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
        >
          {/* Polarization fill, negative side */}
          <motion.path
            d={`M ${CX} ${CY - R} A ${R} ${R} 0 0 0 ${CX} ${CY + R} L ${CX} ${CY - R} Z`}
            fill="url(#halfNeg)"
            stroke="none"
            animate={{ opacity: visible(step, 2) ? 1 : 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          />
          {/* Outline */}
          <motion.path
            d={`M ${CX} ${CY - R} A ${R} ${R} 0 0 0 ${CX} ${CY + R}`}
            fill="none"
            stroke="#60a5fa"
            strokeWidth="1.6"
            strokeLinecap="round"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
          />

          {/* Step-1 boundary edge highlight */}
          <motion.line
            x1={CX}
            x2={CX}
            y1={CY - R}
            y2={CY + R}
            stroke="#60a5fa"
            strokeWidth="2.5"
            strokeLinecap="round"
            animate={{
              opacity: step === 0 ? 1 : 0.35,
              strokeWidth: step === 0 ? 2.5 : 1.4,
            }}
            transition={{ duration: 0.5 }}
          />

          {/* Step-1 label */}
          <motion.g
            animate={{ opacity: step === 0 ? 1 : 0 }}
            transition={{ duration: 0.4 }}
          >
            <text
              x={CX - 220}
              y={CY - R - 20}
              fill="#bfdbfe"
              fontSize="14"
              fontFamily="ui-monospace, monospace"
            >
              Boundary datum
            </text>
            <text
              x={CX - 220}
              y={CY - R - 4}
              fill="#94a3b8"
              fontSize="11"
              fontFamily="ui-monospace, monospace"
            >
              one-sided · seam edge highlighted
            </text>
          </motion.g>
        </motion.g>

        {/* ---- Layer 2: right half-disk (exact double) ---- */}
        <motion.g
          initial={false}
          animate={{
            opacity: visible(step, 1) ? 1 : 0,
            scaleX: visible(step, 1) ? 1 : 0,
          }}
          style={{ transformOrigin: `${CX}px ${CY}px` }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
        >
          <path
            d={`M ${CX} ${CY - R} A ${R} ${R} 0 0 1 ${CX} ${CY + R} L ${CX} ${CY - R} Z`}
            fill="url(#halfPos)"
            stroke="none"
            opacity={visible(step, 2) ? 1 : 0}
          />
          <path
            d={`M ${CX} ${CY - R} A ${R} ${R} 0 0 1 ${CX} ${CY + R}`}
            fill="none"
            stroke="#a78bfa"
            strokeWidth="1.6"
            strokeLinecap="round"
          />
        </motion.g>

        {/* ---- Layer 3: seam line + label ---- */}
        <motion.g
          animate={{ opacity: visible(step, 1) ? 1 : 0 }}
          transition={{ duration: 0.6, delay: visible(step, 1) ? 0.4 : 0 }}
        >
          <line
            x1={CX}
            x2={CX}
            y1={CY - R - 10}
            y2={CY + R + 10}
            stroke="url(#seamGlow)"
            strokeWidth="2.5"
          />
          <text
            x={CX + 10}
            y={CY - R - 14}
            fill="#cbd5e1"
            fontSize="12"
            fontFamily="ui-monospace, monospace"
          >
            Σ · seam
          </text>
          <text
            x={CX + 10}
            y={CY + R + 24}
            fill="#94a3b8"
            fontSize="11"
            fontFamily="ui-monospace, monospace"
          >
            τ_dbl involution
          </text>
        </motion.g>

        {/* ---- Layer 4: polarization labels ---- */}
        <motion.g
          animate={{ opacity: step === 2 ? 1 : 0 }}
          transition={{ duration: 0.5 }}
        >
          <text
            x={CX - R + 18}
            y={CY - 8}
            fill="#bfdbfe"
            fontSize="32"
            fontFamily="ui-serif, serif"
            fontWeight="600"
          >
            −
          </text>
          <text
            x={CX - R + 18}
            y={CY + 18}
            fill="#94a3b8"
            fontSize="11"
            fontFamily="ui-monospace, monospace"
          >
            ℋ_−
          </text>
          <text
            x={CX + R - 32}
            y={CY - 8}
            fill="#ddd6fe"
            fontSize="32"
            fontFamily="ui-serif, serif"
            fontWeight="600"
          >
            +
          </text>
          <text
            x={CX + R - 32}
            y={CY + 18}
            fill="#94a3b8"
            fontSize="11"
            fontFamily="ui-monospace, monospace"
          >
            ℋ_+
          </text>
        </motion.g>

        {/* ---- Layer 5: carrier dots E₋ (3) + E₊ (2) ---- */}
        <CarrierDots step={step} />

        {/* ---- Layer 6: counting / family clustering ---- */}
        <CountingClusters step={step} />

        {/* ---- Layer 7: closed branch + observable readouts ---- */}
        <ObservableReadouts step={step} />
      </svg>
    </div>
  );
}

/* ---------- Sub-layers --------------------------------------------- */

const E_NEG: Array<{ x: number; y: number }> = [
  { x: CX - 110, y: CY - 90 },
  { x: CX - 130, y: CY + 10 },
  { x: CX - 110, y: CY + 100 },
];

const E_POS: Array<{ x: number; y: number }> = [
  { x: CX + 110, y: CY - 60 },
  { x: CX + 110, y: CY + 70 },
];

function CarrierDots({ step }: { step: number }) {
  return (
    <motion.g
      animate={{ opacity: visible(step, 3) ? 1 : 0 }}
      transition={{ duration: 0.5 }}
    >
      {E_NEG.map((p, i) => (
        <motion.g
          key={`neg-${i}`}
          initial={false}
          animate={{ scale: visible(step, 3) ? 1 : 0 }}
          style={{ transformOrigin: `${p.x}px ${p.y}px` }}
          transition={{ duration: 0.5, delay: 0.12 + i * 0.06, type: "spring" }}
        >
          <circle
            cx={p.x}
            cy={p.y}
            r="11"
            fill="#3b82f6"
            stroke="#dbeafe"
            strokeWidth="2"
          />
        </motion.g>
      ))}
      {E_POS.map((p, i) => (
        <motion.g
          key={`pos-${i}`}
          initial={false}
          animate={{ scale: visible(step, 3) ? 1 : 0 }}
          style={{ transformOrigin: `${p.x}px ${p.y}px` }}
          transition={{ duration: 0.5, delay: 0.3 + i * 0.06, type: "spring" }}
        >
          <circle
            cx={p.x}
            cy={p.y}
            r="11"
            fill="#a855f7"
            stroke="#ede9fe"
            strokeWidth="2"
          />
        </motion.g>
      ))}

      {/* Step-4 caption */}
      <motion.g
        animate={{ opacity: step === 3 ? 1 : 0 }}
        transition={{ duration: 0.4 }}
      >
        <text
          x={CX - R - 10}
          y={CY + R + 38}
          fill="#bfdbfe"
          fontSize="13"
          fontFamily="ui-monospace, monospace"
          textAnchor="end"
        >
          E₋ · dim 3
        </text>
        <text
          x={CX + R + 10}
          y={CY + R + 38}
          fill="#ddd6fe"
          fontSize="13"
          fontFamily="ui-monospace, monospace"
        >
          E₊ · dim 2
        </text>
      </motion.g>
    </motion.g>
  );
}

/* SU(3) triplet colour offsets around each E₋ dot */
const TRIPLET = [
  { dx: 0, dy: -14 },
  { dx: -12, dy: 10 },
  { dx: 12, dy: 10 },
];
const TRIPLET_COLOURS = ["#fb7185", "#34d399", "#60a5fa"];

function CountingClusters({ step }: { step: number }) {
  const fan = visible(step, 4);
  return (
    <motion.g
      animate={{ opacity: fan ? 1 : 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Each E₋ "family" splits into a colour triplet */}
      {E_NEG.map((p, i) => (
        <motion.g
          key={`fam-${i}`}
          initial={false}
          animate={{ opacity: fan ? 1 : 0 }}
          transition={{ duration: 0.4, delay: fan ? i * 0.07 : 0 }}
        >
          {TRIPLET.map((d, j) => (
            <motion.circle
              key={j}
              cx={p.x + d.dx}
              cy={p.y + d.dy}
              r="5"
              fill={TRIPLET_COLOURS[j]}
              stroke="#0f172a"
              strokeWidth="1"
              initial={{ scale: 0 }}
              animate={{ scale: fan ? 1 : 0 }}
              style={{ transformOrigin: `${p.x + d.dx}px ${p.y + d.dy}px` }}
              transition={{
                duration: 0.4,
                delay: fan ? 0.05 + i * 0.07 + j * 0.04 : 0,
                type: "spring",
              }}
            />
          ))}
          <text
            x={p.x - 28}
            y={p.y + 36}
            fill="#94a3b8"
            fontSize="10"
            fontFamily="ui-monospace, monospace"
          >
            family {i + 1}
          </text>
        </motion.g>
      ))}

      {/* E₊ stays a single weak doublet — connect the two dots with a brace */}
      <motion.g
        animate={{ opacity: fan ? 1 : 0 }}
        transition={{ duration: 0.4, delay: fan ? 0.3 : 0 }}
      >
        <path
          d={`M ${E_POS[0].x + 22} ${E_POS[0].y} Q ${E_POS[0].x + 36} ${(E_POS[0].y + E_POS[1].y) / 2} ${E_POS[1].x + 22} ${E_POS[1].y}`}
          fill="none"
          stroke="#c4b5fd"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <text
          x={E_POS[0].x + 48}
          y={(E_POS[0].y + E_POS[1].y) / 2 + 4}
          fill="#ddd6fe"
          fontSize="11"
          fontFamily="ui-monospace, monospace"
        >
          N_Φ = 1
        </text>
      </motion.g>

      {/* Step-5 caption */}
      <motion.g
        animate={{ opacity: step === 4 ? 1 : 0 }}
        transition={{ duration: 0.4 }}
      >
        <text
          x={CX}
          y={CY + R + 60}
          fill="#cbd5e1"
          fontSize="13"
          textAnchor="middle"
          fontFamily="ui-monospace, monospace"
        >
          [u_Σ] = 1 → 3 families · 1 weak doublet
        </text>
      </motion.g>
    </motion.g>
  );
}

const READOUTS = [
  {
    label: "α⁻¹(0)",
    value: "137.0360",
    x: CX + R + 60,
    y: CY - 100,
    accent: "#60a5fa",
  },
  {
    label: "λ_C",
    value: "0.22438",
    x: CX + R + 60,
    y: CY,
    accent: "#34d399",
  },
  {
    label: "θ_eff",
    value: "0",
    x: CX + R + 60,
    y: CY + 100,
    accent: "#f472b6",
  },
  {
    label: "sin²θ_13",
    value: "0.02311",
    x: CX - R - 60,
    y: CY - 100,
    accent: "#a78bfa",
    anchor: "end" as const,
  },
  {
    label: "β_rad",
    value: "0.2424°",
    x: CX - R - 60,
    y: CY + 100,
    accent: "#fbbf24",
    anchor: "end" as const,
  },
];

function ObservableReadouts({ step }: { step: number }) {
  const show = visible(step, 5);
  return (
    <motion.g
      animate={{ opacity: show ? 1 : 0 }}
      transition={{ duration: 0.6 }}
    >
      {READOUTS.map((r, i) => (
        <motion.g
          key={r.label}
          initial={false}
          animate={{
            opacity: show ? 1 : 0,
            scale: show ? 1 : 0.6,
          }}
          style={{ transformOrigin: `${r.x}px ${r.y}px` }}
          transition={{
            duration: 0.5,
            delay: show ? 0.2 + i * 0.08 : 0,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {/* Connector from center to readout */}
          <motion.line
            x1={CX}
            x2={r.x}
            y1={CY}
            y2={r.y}
            stroke={r.accent}
            strokeWidth="1"
            strokeOpacity="0.35"
            strokeDasharray="2 4"
          />
          <rect
            x={(r.anchor === "end" ? r.x - 110 : r.x - 4)}
            y={r.y - 22}
            rx="6"
            ry="6"
            width="114"
            height="40"
            fill="rgba(15, 23, 42, 0.85)"
            stroke={r.accent}
            strokeOpacity="0.55"
            strokeWidth="1"
          />
          <text
            x={r.anchor === "end" ? r.x - 96 : r.x + 10}
            y={r.y - 6}
            fill="#cbd5e1"
            fontSize="10"
            fontFamily="ui-monospace, monospace"
          >
            {r.label}
          </text>
          <text
            x={r.anchor === "end" ? r.x - 96 : r.x + 10}
            y={r.y + 12}
            fill={r.accent}
            fontSize="14"
            fontFamily="ui-monospace, monospace"
            fontWeight="600"
          >
            {r.value}
          </text>
        </motion.g>
      ))}

      {/* Closed-branch label */}
      <motion.g
        animate={{ opacity: show ? 1 : 0 }}
        transition={{ duration: 0.5, delay: show ? 0.6 : 0 }}
      >
        <text
          x={CX}
          y={CY + R + 64}
          fill="#6ee7b7"
          fontSize="14"
          textAnchor="middle"
          fontFamily="ui-monospace, monospace"
          fontWeight="600"
        >
          Closed branch T★
        </text>
        <text
          x={CX}
          y={CY + R + 82}
          fill="#94a3b8"
          fontSize="11"
          textAnchor="middle"
          fontFamily="ui-monospace, monospace"
        >
          observables emerge — none fitted
        </text>
      </motion.g>
    </motion.g>
  );
}

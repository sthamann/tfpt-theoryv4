"use client";

import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, Pause, Play } from "lucide-react";
import { Math } from "./Math";
import { cn } from "@/lib/utils";

/**
 * Animated 6-frame "theory unpacking" diagram.
 *
 * The narrative shows the compiler construction — geometrically — in six
 * tightly-coupled steps:
 *
 *   1. The two axioms (seam constant c₃, five-slot carrier g_car)
 *   2. The seam and its ℤ₂ sheet (Gauss–Bonnet normalisation)
 *   3. Carrier split → 3 + 2 (the D₅ half-spinor)
 *   4. The 3 + 2 carrier (hypercharge, dim S⁺ = 16)
 *   5. The μ₄ glue ⇒ E₈ (240 roots)
 *   6. The readouts + bootstrap (α⁻¹, θ_eff = 0)
 *
 * The component runs an autoplay cycle but pauses when the user clicks a
 * step pip, the play/pause button, or hovers over the canvas. It also
 * respects `prefers-reduced-motion` and stays on the final frame in that
 * case.
 */

interface UnpackingStep {
  id: number;
  badge: string;
  short: string;
  title: string;
  body: string;
  formula: string;
  /** Plain-English reading of the formula (caption + screen-reader label). */
  plain: string;
}

const STEPS: UnpackingStep[] = [
  {
    id: 0,
    badge: "Step 1",
    short: "Two numbers",
    title: "Two numbers in",
    body: "The Standard Model takes ~20 parameters as input. Here only two numbers enter: the seam constant c₃ = 1/(8π) on the boundary and a five-slot carrier g_car = 5. No gauge group, no families, no α is put in by hand — everything below is a consequence.",
    formula: "c_3 = \\tfrac{1}{8\\pi}, \\qquad g_{\\mathrm{car}} = 5",
    plain: "The seam constant c₃ equals one over eight pi; the carrier rank g_car equals five.",
  },
  {
    id: 1,
    badge: "Step 2",
    short: "The seam",
    title: "The seam and its sheet",
    body: "The seam carries a ℤ₂ sheet involution. The Gauss–Bonnet normalisation of the one-sided seam sphere fixes the seam constant — only π stays continuous.",
    formula:
      "c_3 = \\frac{1}{|\\mathbb{Z}_2|\\oint_{S^2}K\\,dA} = \\frac{1}{8\\pi}",
    plain: "The seam constant is one divided by the ℤ₂-halved total curvature of the seam sphere (Gauss–Bonnet) — which equals one over eight pi.",
  },
  {
    id: 2,
    badge: "Step 3",
    short: "Carrier 3+2",
    title: "Carrier split → 3 + 2",
    body: "The five carrier slots split into 3 colour + 2 weak. The even-Hamming code on the slots is the D₅ half-spinor — the split is arithmetic, not assumed.",
    formula:
      "g_{\\mathrm{car}} = 5 = 3 + 2 \\;\\Rightarrow\\; C^+ = D_5",
    plain: "The five carrier slots split as three colour plus two weak, giving the D₅ half-spinor.",
  },
  {
    id: 3,
    badge: "Step 4",
    short: "Spinor 16",
    title: "The 3 + 2 carrier",
    body: "The colour block (dim 3) and weak block (dim 2) carry the determinant-normalized hypercharge Y = −1/3, +1/2. The half-spinor packet is Λ^even of the carrier, dim 16.",
    formula:
      "(\\dim E_-, \\dim E_+) = (3, 2), \\quad \\dim S^+ = 16",
    plain: "The colour and weak blocks have dimensions three and two; the half-spinor packet has dimension sixteen.",
  },
  {
    id: 4,
    badge: "Step 5",
    short: "Glue ⇒ E₈",
    title: "Glue ⇒ E₈",
    body: "Three families and the four-puncture geometry ℙ¹∖μ₄ = A₃ glue with the D₅ spinor across the common discriminant ℤ₄: E₈ = (D₅ ⊕ A₃) + μ₄, 240 roots.",
    formula:
      "E_8 = (D_5 \\oplus A_3) + \\mu_4, \\quad |R(E_8)| = 240",
    plain: "E₈ is D₅ together with A₃, glued by μ₄, with 240 roots.",
  },
  {
    id: 5,
    badge: "Step 6",
    short: "Readouts",
    title: "What the compiler reads off",
    body: "From E₈ the compiler reads off the gauge group, three families and the hypercharges; α⁻¹ = 137.036 (1.9σ from CODATA); all nine masses, CKM and PMNS from one φ₀-ladder; the strong-CP null θ_eff = 0; and the scalaron, Λ and the cosmological readouts — about fifty status-graded results, none fitted. The bootstrap loop even re-derives the two inputs, so the discrete core is over-determined.",
    formula:
      "\\alpha^{-1}(0) = 137.035\\,999\\,217\\,\\ldots,\\;\\; \\theta_{\\mathrm{eff}} = 0",
    plain: "The inverse fine-structure constant is about 137.035999217, and the effective strong-CP phase is exactly zero.",
  },
];

const FRAME_MS = 5500;

export function TheoryUnpacking() {
  const reduced = useReducedMotion();
  // Deterministic initial state so the server and first client render match
  // (avoids a hydration mismatch); reduced-motion is applied after mount below.
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [hovered, setHovered] = useState(false);

  useEffect(() => {
    if (reduced) {
      setStep(STEPS.length - 1);
      setPlaying(false);
    }
  }, [reduced]);

  useEffect(() => {
    if (!playing || hovered || reduced) return;
    const id = window.setInterval(
      () => setStep((s) => (s + 1) % STEPS.length),
      FRAME_MS,
    );
    return () => window.clearInterval(id);
  }, [playing, hovered, reduced]);

  const current = STEPS[step];
  const autoplaying = playing && !hovered && !reduced;
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
      <header className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 px-5 py-3.5">
        <div className="flex min-w-0 flex-col gap-0.5">
          <span className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/70">
            How the compiler works · two axioms → E₈ → the observables
          </span>
          <span className="flex items-baseline gap-2">
            <span className="font-mono text-[11px] font-semibold text-violet-300/90">
              {String(step + 1).padStart(2, "0")}
            </span>
            <AnimatePresence mode="wait">
              <motion.span
                key={current.id}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.3 }}
                className="truncate font-serif text-base font-semibold text-slate-100"
              >
                {current.short}
              </motion.span>
            </AnimatePresence>
          </span>
        </div>
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

      {/* Autoplay progress: a live bar that fills over each frame's dwell time
          while playing, and otherwise shows overall progress through the arc. */}
      <div className="h-0.5 w-full bg-slate-800/60" aria-hidden="true">
        {autoplaying ? (
          <motion.div
            key={step}
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ duration: FRAME_MS / 1000, ease: "linear" }}
            className="h-full origin-left bg-gradient-to-r from-blue-400 to-violet-400"
          />
        ) : (
          <div
            className="h-full origin-left bg-gradient-to-r from-blue-400/70 to-violet-400/70 transition-transform duration-500"
            style={{ transform: `scaleX(${(step + 1) / STEPS.length})` }}
          />
        )}
      </div>

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
              <h3 className="font-serif text-xl font-semibold leading-snug text-slate-50">
                {current.title}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-300">
                {current.body}
              </p>
              <div className="mt-4 overflow-x-auto formula-scroll rounded-md border border-slate-700/40 bg-slate-950/60 p-3">
                <Math block plain={current.plain}>{current.formula}</Math>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      <div
        role="tablist"
        aria-label="Step navigation"
        className="flex gap-1 border-t border-slate-800/60 bg-slate-950/40 px-2 py-2.5 sm:gap-1.5 sm:px-3"
      >
        {STEPS.map((s) => {
          const active = step === s.id;
          const done = step > s.id;
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
              className={cn(
                "group flex min-w-0 flex-1 items-center justify-center gap-1.5 rounded-lg px-1.5 py-1.5 ring-1 transition-colors sm:justify-start sm:px-2.5",
                active
                  ? "bg-blue-500/15 ring-blue-400/40"
                  : "bg-slate-900/40 ring-slate-700/40 hover:bg-slate-800/70",
              )}
            >
              <span
                aria-hidden="true"
                className={cn(
                  "flex h-5 w-5 shrink-0 items-center justify-center rounded-full font-mono text-[10px] font-semibold transition-colors",
                  active
                    ? "bg-gradient-to-r from-blue-400 to-violet-400 text-slate-950"
                    : done
                      ? "bg-slate-600/70 text-slate-100"
                      : "bg-slate-800 text-slate-400 group-hover:text-slate-200",
                )}
              >
                {s.id + 1}
              </span>
              <span
                className={cn(
                  "hidden truncate text-[11px] font-medium sm:block",
                  active
                    ? "text-blue-100"
                    : "text-slate-400 group-hover:text-slate-200",
                )}
              >
                {s.short}
              </span>
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

        {/* ---- Layer 1: left half-disk (the seam) ---- */}
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
              Seam · c₃ = 1/(8π)
            </text>
            <text
              x={CX - 220}
              y={CY - R - 4}
              fill="#94a3b8"
              fontSize="11"
              fontFamily="ui-monospace, monospace"
            >
              the boundary normaliser
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
            ℤ₂ sheet involution
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
            colour
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
            weak
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
          g_car = 5 → D₅ spinor · 3 families · 1 doublet
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
          Compiler output
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

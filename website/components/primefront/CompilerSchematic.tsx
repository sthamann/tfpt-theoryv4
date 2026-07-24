"use client";

import { motion } from "motion/react";

/**
 * Two axiom blocks + μ4 glue arrow → E8 lattice completion.
 */
export function CompilerSchematic() {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-slate-700/50 bg-slate-950/60 p-4 sm:p-6">
      <svg
        viewBox="0 0 640 220"
        className="mx-auto h-auto w-full max-w-2xl"
        role="img"
        aria-label="Schematic: axioms c3 and g_car build D5 plus A3 with mu4 glue into E8"
      >
        <defs>
          <linearGradient id="pf-block" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#1e3a8a" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#0f172a" stopOpacity="0.95" />
          </linearGradient>
          <linearGradient id="pf-e8" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#047857" stopOpacity="0.85" />
            <stop offset="100%" stopColor="#0f172a" stopOpacity="0.95" />
          </linearGradient>
          <marker
            id="pf-arrow"
            markerWidth="8"
            markerHeight="8"
            refX="6"
            refY="3"
            orient="auto"
          >
            <path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8" />
          </marker>
        </defs>

        {/* Axiom P1 */}
        <motion.g
          initial={{ opacity: 0, x: -12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <rect
            x="16"
            y="36"
            width="150"
            height="72"
            rx="10"
            fill="url(#pf-block)"
            stroke="#3b82f6"
            strokeWidth="1.5"
          />
          <text x="91" y="66" textAnchor="middle" fill="#93c5fd" fontSize="11" fontFamily="ui-monospace, monospace">
            axiom P1
          </text>
          <text x="91" y="88" textAnchor="middle" fill="#e2e8f0" fontSize="14" fontFamily="Georgia, serif">
            c₃ = 1/(8π)
          </text>
        </motion.g>

        {/* Axiom P2 */}
        <motion.g
          initial={{ opacity: 0, x: -12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <rect
            x="16"
            y="124"
            width="150"
            height="72"
            rx="10"
            fill="url(#pf-block)"
            stroke="#3b82f6"
            strokeWidth="1.5"
          />
          <text x="91" y="154" textAnchor="middle" fill="#93c5fd" fontSize="11" fontFamily="ui-monospace, monospace">
            axiom P2
          </text>
          <text x="91" y="176" textAnchor="middle" fill="#e2e8f0" fontSize="14" fontFamily="Georgia, serif">
            g_car = 5
          </text>
        </motion.g>

        {/* Blocks D5 / A3 */}
        <motion.g
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.25 }}
        >
          <rect
            x="220"
            y="48"
            width="100"
            height="56"
            rx="8"
            fill="#0f172a"
            stroke="#64748b"
            strokeWidth="1.25"
          />
          <text x="270" y="82" textAnchor="middle" fill="#f8fafc" fontSize="16" fontFamily="Georgia, serif">
            D₅
          </text>
          <rect
            x="220"
            y="128"
            width="100"
            height="56"
            rx="8"
            fill="#0f172a"
            stroke="#64748b"
            strokeWidth="1.25"
          />
          <text x="270" y="162" textAnchor="middle" fill="#f8fafc" fontSize="16" fontFamily="Georgia, serif">
            A₃
          </text>
          <text x="270" y="118" textAnchor="middle" fill="#94a3b8" fontSize="18">
            ⊕
          </text>
        </motion.g>

        {/* Glue μ4 */}
        <motion.g
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.45, delay: 0.4 }}
        >
          <circle cx="390" cy="116" r="34" fill="#1e293b" stroke="#f59e0b" strokeWidth="1.75" />
          <text x="390" y="112" textAnchor="middle" fill="#fcd34d" fontSize="10" fontFamily="ui-monospace, monospace">
            glue
          </text>
          <text x="390" y="130" textAnchor="middle" fill="#fef3c7" fontSize="15" fontFamily="Georgia, serif">
            μ₄
          </text>
        </motion.g>

        {/* Arrow paths */}
        <motion.path
          d="M166 72 H210"
          stroke="#64748b"
          strokeWidth="1.5"
          fill="none"
          markerEnd="url(#pf-arrow)"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        />
        <motion.path
          d="M166 160 H210"
          stroke="#64748b"
          strokeWidth="1.5"
          fill="none"
          markerEnd="url(#pf-arrow)"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
        />
        <motion.path
          d="M320 116 H350"
          stroke="#f59e0b"
          strokeWidth="1.75"
          fill="none"
          markerEnd="url(#pf-arrow)"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.45 }}
        />
        <motion.path
          d="M430 116 H470"
          stroke="#34d399"
          strokeWidth="1.75"
          fill="none"
          markerEnd="url(#pf-arrow)"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.55 }}
        />

        {/* E8 */}
        <motion.g
          initial={{ opacity: 0, x: 12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.55, delay: 0.6 }}
        >
          <rect
            x="478"
            y="70"
            width="140"
            height="92"
            rx="12"
            fill="url(#pf-e8)"
            stroke="#34d399"
            strokeWidth="1.75"
          />
          <text x="548" y="108" textAnchor="middle" fill="#a7f3d0" fontSize="11" fontFamily="ui-monospace, monospace">
            lattice completion
          </text>
          <text x="548" y="138" textAnchor="middle" fill="#ecfdf5" fontSize="28" fontFamily="Georgia, serif">
            E₈
          </text>
        </motion.g>
      </svg>
      <p className="mt-3 text-center font-mono text-[11px] text-slate-500">
        D₅ ⊕ A₃ + μ₄ ⇒ E₈ — discrete compiler, not a continuum guess
      </p>
    </div>
  );
}

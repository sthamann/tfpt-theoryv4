"use client";

import { useEffect, useState } from "react";

const PRIMES = [
  { p: 3, lines: 1120, sigma3: 28, ap: -4, a: 448, b: 24 },
  { p: 5, lines: 19656, sigma3: 126, ap: -2, a: 4032, b: 124 },
  { p: 7, lines: 137600, sigma3: 344, ap: 24, a: 11008, b: 368 },
] as const;

/** Lattice graph nodes for a schematic neighbour step. */
const NODES = [
  { id: 0, x: 80, y: 100 },
  { id: 1, x: 160, y: 50 },
  { id: 2, x: 160, y: 150 },
  { id: 3, x: 250, y: 100 },
  { id: 4, x: 330, y: 55 },
  { id: 5, x: 330, y: 145 },
  { id: 6, x: 410, y: 100 },
] as const;

const EDGES: [number, number][] = [
  [0, 1],
  [0, 2],
  [1, 3],
  [2, 3],
  [3, 4],
  [3, 5],
  [4, 6],
  [5, 6],
];

export function NeighborStepping() {
  const [idx, setIdx] = useState(0);
  const [step, setStep] = useState(0);
  const row = PRIMES[idx];

  useEffect(() => {
    const id = window.setInterval(() => {
      setStep((s) => (s + 1) % 5);
    }, 900);
    return () => window.clearInterval(id);
  }, []);

  useEffect(() => {
    const id = window.setInterval(() => {
      setIdx((i) => (i + 1) % PRIMES.length);
    }, 4500);
    return () => window.clearInterval(id);
  }, []);

  const activeEdge = step % EDGES.length;

  return (
    <div className="rounded-2xl border border-slate-700/50 bg-slate-950/60 p-4 sm:p-5">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <p className="font-mono text-[10px] uppercase tracking-widest text-emerald-300/90">
          Kneser neighbour stepping · p = {row.p}
        </p>
        <p className="font-mono text-[11px] text-slate-400">
          #lines = {row.lines.toLocaleString("en-US")} = σ₃·#P³
        </p>
      </div>

      <svg
        viewBox="0 0 480 200"
        className="mx-auto h-auto w-full max-w-xl"
        role="img"
        aria-label="Animated lattice graph showing Kneser neighbour steps"
      >
        {EDGES.map(([u, v], i) => {
          const A = NODES[u];
          const B = NODES[v];
          const on = i === activeEdge;
          return (
            <line
              key={`${u}-${v}`}
              x1={A.x}
              y1={A.y}
              x2={B.x}
              y2={B.y}
              stroke={on ? "#34d399" : "#334155"}
              strokeWidth={on ? 2.5 : 1.25}
              style={{ transition: "stroke 0.35s ease, stroke-width 0.35s" }}
            />
          );
        })}
        {NODES.map((n) => (
          <g key={n.id}>
            <circle
              cx={n.x}
              cy={n.y}
              r={n.id === 3 ? 9 : 7}
              fill={n.id === 0 || n.id === 6 ? "#0f766e" : "#1e293b"}
              stroke="#94a3b8"
              strokeWidth="1.25"
            />
          </g>
        ))}
        <text x="80" y="185" textAnchor="middle" fill="#64748b" fontSize="10" fontFamily="ui-monospace, monospace">
          E₈
        </text>
        <text x="410" y="185" textAnchor="middle" fill="#64748b" fontSize="10" fontFamily="ui-monospace, monospace">
          neighbour
        </text>
      </svg>

      <div className="mt-4 overflow-x-auto rounded-xl border border-slate-700/40 bg-slate-900/60 p-3">
        <p className="mb-2 font-mono text-[10px] text-slate-500">
          Frozen marked operator · ν_p = a·Id + b·T_p · b = σ₃ + a_p
        </p>
        <div className="flex flex-wrap items-center gap-4">
          <MatrixDiag
            label={`T_${row.p}`}
            values={[row.sigma3, row.sigma3, row.sigma3, row.ap]}
          />
          <div className="font-mono text-xs text-slate-400">
            <div>
              (a, b) ={" "}
              <span className="text-slate-200">
                ({row.a}, {row.b})
              </span>
            </div>
            <div className="mt-1">
              a_p = b − σ₃ ={" "}
              <span className="text-emerald-300">{row.ap}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function MatrixDiag({
  label,
  values,
}: {
  label: string;
  values: readonly number[];
}) {
  return (
    <div className="font-mono text-[11px] text-slate-300">
      <span className="text-slate-500">{label} ≈ </span>
      <span className="inline-block border-y border-slate-600 px-1 py-0.5">
        diag(
        {values.map((v, i) => (
          <span key={i}>
            <span className={i === 3 ? "text-emerald-300" : "text-sky-300"}>
              {v}
            </span>
            {i < values.length - 1 ? ", " : ""}
          </span>
        ))}
        )
      </span>
    </div>
  );
}

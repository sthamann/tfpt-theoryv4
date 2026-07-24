"use client";

import { useEffect, useMemo, useState } from "react";

/** Root-shell glue census from Teil 11: classes (0,1,2,3) = (52,64,60,64). */
const ROOT_COUNTS = [52, 64, 60, 64] as const;
const COLORS = ["#38bdf8", "#a78bfa", "#f472b6", "#34d399"] as const;
const LABELS = ["deg 0", "deg 1", "deg 2", "deg 3"] as const;

type Point = { x: number; y: number; cls: number; id: number };

function buildPoints(shell: number): Point[] {
  const counts =
    shell === 1
      ? ROOT_COUNTS
      : ([40, 48, 44, 48] as const); // schematic higher shell
  const pts: Point[] = [];
  let id = 0;
  const R = 38 + shell * 28;
  counts.forEach((n, cls) => {
    for (let i = 0; i < Math.min(n, 28); i++) {
      const a = (i / Math.min(n, 28)) * Math.PI * 2 + cls * 0.15;
      const jitter = 4 + (i % 5);
      pts.push({
        x: 160 + Math.cos(a) * (R + jitter),
        y: 140 + Math.sin(a) * (R * 0.72 + jitter * 0.4),
        cls,
        id: id++,
      });
    }
  });
  return pts;
}

export function ShellCensus() {
  const [shell, setShell] = useState(1);
  const [phase, setPhase] = useState(0);
  const points = useMemo(() => buildPoints(shell), [shell]);

  useEffect(() => {
    const id = window.setInterval(() => {
      setPhase((p) => (p + 1) % 4);
    }, 1600);
    return () => window.clearInterval(id);
  }, []);

  useEffect(() => {
    const id = window.setInterval(() => {
      setShell((s) => (s % 3) + 1);
    }, 4800);
    return () => window.clearInterval(id);
  }, []);

  const signed =
    shell === 1
      ? ROOT_COUNTS[0] - ROOT_COUNTS[2]
      : 40 - 44;
  const highlight = phase < 2 ? "total" : "signed";

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-700/50 bg-slate-950/60 p-4 sm:p-5">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <p className="font-mono text-[10px] uppercase tracking-widest text-slate-400">
          Glue-coloured shells · shell n = {shell}
        </p>
        <p className="font-mono text-[11px] text-slate-300">
          {highlight === "total" ? (
            <>
              total roots ={" "}
              <span className="text-sky-300">
                {shell === 1 ? 240 : 180}
              </span>
            </>
          ) : (
            <>
              signed (0 − 2) ={" "}
              <span className="text-rose-300">{signed}</span>
              {shell === 1 && (
                <span className="text-slate-500"> = −rank(E₈)</span>
              )}
            </>
          )}
        </p>
      </div>
      <svg
        viewBox="0 0 320 280"
        className="mx-auto h-auto w-full max-w-md"
        role="img"
        aria-label="Animated E8 shell points coloured by glue class with signed difference"
      >
        {[1, 2, 3].map((r) => (
          <ellipse
            key={r}
            cx="160"
            cy="140"
            rx={38 + r * 28}
            ry={(38 + r * 28) * 0.72}
            fill="none"
            stroke="#334155"
            strokeWidth="1"
            opacity={r === shell ? 0.9 : 0.35}
          />
        ))}
        {points.map((p) => {
          const active =
            highlight === "total" || p.cls === 0 || p.cls === 2;
          const sign =
            highlight === "signed" && (p.cls === 0 || p.cls === 2);
          const op =
            highlight === "total"
              ? 0.85
              : p.cls === 0 || p.cls === 2
                ? 0.95
                : 0.15;
          return (
            <circle
              key={p.id}
              cx={p.x}
              cy={p.y}
              r={sign ? 3.2 : 2.4}
              fill={COLORS[p.cls]}
              opacity={active ? op : 0.12}
              style={{
                transition: "opacity 0.6s ease, r 0.4s ease",
              }}
            />
          );
        })}
        <text
          x="160"
          y="268"
          textAnchor="middle"
          fill="#94a3b8"
          fontSize="11"
          fontFamily="ui-monospace, monospace"
        >
          Θ₀ − Θ₂ = θ₃² · θ₄⁶
        </text>
      </svg>
      <ul className="mt-3 flex flex-wrap justify-center gap-3">
        {LABELS.map((lab, i) => (
          <li
            key={lab}
            className="flex items-center gap-1.5 font-mono text-[10px] text-slate-400"
          >
            <span
              className="inline-block h-2 w-2 rounded-full"
              style={{ background: COLORS[i] }}
              aria-hidden
            />
            {lab}
            {shell === 1 ? ` · ${ROOT_COUNTS[i]}` : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}

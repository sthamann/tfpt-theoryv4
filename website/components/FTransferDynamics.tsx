"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { RotateCw } from "lucide-react";

type Panel = {
  key: string;
  title: string;
  rate: string;
  color: string;
  highlight?: boolean;
  attractor: number;
  attractorLabel: string;
  yMin: number;
  yMax: number;
  curve: (tn: number) => number;
  envelope?: (tn: number) => number;
};

const GAP = 6 * Math.log(1.5); // seam gap = -ln (2/3)^6 ≈ 2.4328

const PANELS: Panel[] = [
  {
    key: "pole",
    title: "F_pole (Koide)",
    rate: "SEAM rate (2/3)⁶",
    color: "#fbbf24",
    highlight: true,
    attractor: 2,
    attractorLabel: "attractor q* = 2",
    yMin: 1.7,
    yMax: 5.3,
    curve: (tn) => 2 + 3 * Math.exp(-GAP * tn * 2.8),
  },
  {
    key: "boltz",
    title: "F_Boltzmann (η_B)",
    rate: "thermal washout κ_f",
    color: "#60a5fa",
    attractor: 1,
    attractorLabel: "balance S/W",
    yMin: 0,
    yMax: 1.12,
    curve: (tn) => 1 - Math.exp(-1.3 * tn * 6),
  },
  {
    key: "relic",
    title: "F_relic (axion)",
    rate: "cosmological freeze",
    color: "#34d399",
    attractor: 0,
    attractorLabel: "n·a³ → const",
    yMin: -1.08,
    yMax: 1.08,
    curve: (tn) => Math.exp(-0.16 * tn * 14) * Math.cos(2.2 * tn * 14),
    envelope: (tn) => Math.exp(-0.16 * tn * 14),
  },
  {
    key: "qcd",
    title: "F_QCD (m_p/m_e)",
    rate: "RG flow, b₃ = −7",
    color: "#f87171",
    attractor: 0,
    attractorLabel: "UV attractor α_s → 0",
    yMin: -0.012,
    yMax: 0.13,
    curve: (tn) => 0.118 / (1 + 0.118 * (7 / (2 * Math.PI)) * tn * 14),
  },
];

function drawPanel(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  p: Panel,
  progress: number,
) {
  const padL = 12;
  const padR = 12;
  const padT = 30;
  const padB = 16;
  const plotW = w - padL - padR;
  const plotH = h - padT - padB;
  const X = (tn: number) => padL + tn * plotW;
  const Y = (v: number) => padT + (1 - (v - p.yMin) / (p.yMax - p.yMin)) * plotH;

  ctx.clearRect(0, 0, w, h);

  // panel frame
  ctx.strokeStyle = p.highlight ? "rgba(251,191,36,0.55)" : "rgba(148,163,184,0.18)";
  ctx.lineWidth = p.highlight ? 1.5 : 1;
  ctx.strokeRect(0.5, 0.5, w - 1, h - 1);

  // attractor line (dashed)
  ctx.setLineDash([4, 4]);
  ctx.strokeStyle = "rgba(148,163,184,0.5)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padL, Y(p.attractor));
  ctx.lineTo(w - padR, Y(p.attractor));
  ctx.stroke();
  ctx.setLineDash([]);

  // envelope (relic)
  if (p.envelope) {
    ctx.strokeStyle = p.color + "66";
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let i = 0; i <= 240; i++) {
      const tn = (i / 240) * progress;
      const xx = X(tn);
      ctx.lineTo(xx, Y(p.envelope(tn)));
    }
    ctx.stroke();
  }

  // main curve, drawn up to `progress`
  ctx.strokeStyle = p.color;
  ctx.lineWidth = p.highlight ? 2.4 : 1.9;
  ctx.lineJoin = "round";
  ctx.beginPath();
  const N = 260;
  for (let i = 0; i <= N; i++) {
    const tn = (i / N) * progress;
    const xx = X(tn);
    const yy = Y(p.curve(tn));
    if (i === 0) ctx.moveTo(xx, yy);
    else ctx.lineTo(xx, yy);
  }
  ctx.stroke();

  // moving head dot
  const headTn = progress;
  ctx.fillStyle = p.color;
  ctx.beginPath();
  ctx.arc(X(headTn), Y(p.curve(headTn)), p.highlight ? 4 : 3, 0, Math.PI * 2);
  ctx.fill();

  // labels
  ctx.fillStyle = p.highlight ? "#fcd34d" : "#cbd5e1";
  ctx.font = "600 12px ui-sans-serif, system-ui, sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(p.title, padL, 14);
  ctx.fillStyle = p.highlight ? "rgba(252,211,77,0.85)" : "rgba(148,163,184,0.85)";
  ctx.font = "10px ui-monospace, monospace";
  ctx.fillText(p.rate, padL, 26);
  ctx.fillStyle = "rgba(148,163,184,0.7)";
  ctx.font = "9px ui-sans-serif, system-ui, sans-serif";
  ctx.textAlign = "right";
  ctx.fillText(p.attractorLabel, w - padR - 2, Y(p.attractor) - 4);
}

export function FTransferDynamics() {
  const canvasRefs = useRef<(HTMLCanvasElement | null)[]>([]);
  const wrapRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number | null>(null);
  const startRef = useRef<number>(0);
  const [reduced, setReduced] = useState(false);
  const [runKey, setRunKey] = useState(0);

  const sizeCanvas = useCallback((c: HTMLCanvasElement) => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = c.getBoundingClientRect();
    c.width = Math.max(1, Math.round(rect.width * dpr));
    c.height = Math.max(1, Math.round(rect.height * dpr));
    const ctx = c.getContext("2d");
    if (ctx) ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return rect;
  }, []);

  const render = useCallback(
    (progress: number) => {
      PANELS.forEach((p, i) => {
        const c = canvasRefs.current[i];
        if (!c) return;
        const rect = c.getBoundingClientRect();
        const ctx = c.getContext("2d");
        if (ctx) drawPanel(ctx, rect.width, rect.height, p, progress);
      });
    },
    [],
  );

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mq.matches);
    const onChange = () => setReduced(mq.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  useEffect(() => {
    canvasRefs.current.forEach((c) => c && sizeCanvas(c));
    const ro = new ResizeObserver(() => {
      canvasRefs.current.forEach((c) => c && sizeCanvas(c));
      render(reduced ? 1 : 1);
    });
    if (wrapRef.current) ro.observe(wrapRef.current);
    return () => ro.disconnect();
  }, [sizeCanvas, render, reduced]);

  useEffect(() => {
    if (reduced) {
      render(1);
      return;
    }
    startRef.current = 0;
    const DURATION = 4200;
    const HOLD = 1100;
    const step = (ts: number) => {
      if (!startRef.current) startRef.current = ts;
      const elapsed = ts - startRef.current;
      const cycle = DURATION + HOLD;
      const t = elapsed % cycle;
      const progress = t < DURATION ? easeOut(t / DURATION) : 1;
      render(progress);
      rafRef.current = requestAnimationFrame(step);
    };
    rafRef.current = requestAnimationFrame(step);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [render, reduced, runKey]);

  return (
    <figure className="my-4 rounded-xl border border-slate-700/40 bg-slate-950/40 p-4">
      <figcaption className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p className="text-sm font-semibold text-slate-100">
            F_transfer: one shape, four rates
          </p>
          <p className="text-xs text-slate-400">
            Every transfer instance is a gapped relaxation to a unique attractor — the same
            shape as the main-branch update to the E₈ marks.
          </p>
        </div>
        {!reduced && (
          <button
            type="button"
            onClick={() => setRunKey((k) => k + 1)}
            className="inline-flex items-center gap-1.5 rounded-lg border border-slate-700/50 bg-slate-900/60 px-2.5 py-1.5 text-xs font-medium text-slate-300 transition-colors hover:bg-slate-800/70 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400/40"
            aria-label="Replay the F_transfer relaxation animation"
          >
            <RotateCw size={13} aria-hidden /> Replay
          </button>
        )}
      </figcaption>

      <div ref={wrapRef} className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {PANELS.map((p, i) => (
          <canvas
            key={p.key}
            ref={(el) => {
              canvasRefs.current[i] = el;
            }}
            className="h-[150px] w-full rounded-lg bg-slate-900/40"
            role="img"
            aria-label={`${p.title}: a ${p.rate} relaxation converging to ${p.attractorLabel}`}
          />
        ))}
      </div>

      <p className="mt-3 text-xs leading-relaxed text-slate-400">
        <span className="font-semibold text-amber-300/90">Only F_pole (Koide)</span> runs at the{" "}
        <span className="font-mono">seam</span> rate — its Möbius multiplier is{" "}
        <span className="font-mono">(2/3)⁶ = λ₂</span>, the seam-clock eigenvalue. The other three
        share the <em>shape</em> with external rates (thermal washout, cosmological freeze, RG
        flow). So F_transfer is the readout end of the one discrete→dynamic principle, not a
        bolt-on (v303).
      </p>
    </figure>
  );
}

function easeOut(t: number) {
  return 1 - Math.pow(1 - t, 3);
}

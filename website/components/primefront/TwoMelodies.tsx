"use client";

import { useEffect, useMemo, useRef } from "react";

/**
 * Smooth Witt background + oscillating a_p² residual (Eichler layer).
 * Schematic: λ = λ_Eis + a_p².
 */
export function TwoMelodies() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const primes = useMemo(
    () => [
      { p: 3, ap2: 16 },
      { p: 5, ap2: 4 },
      { p: 7, ap2: 576 },
      { p: 11, ap2: 1936 },
      { p: 13, ap2: 484 },
      { p: 17, ap2: 1444 },
      { p: 19, ap2: 576 },
      { p: 23, ap2: 1936 },
      { p: 29, ap2: 400 },
      { p: 31, ap2: 1024 },
    ],
    [],
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let raf = 0;
    let t0 = performance.now();

    const draw = (now: number) => {
      const t = (now - t0) / 1000;
      const dpr = window.devicePixelRatio || 1;
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;
      if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
        canvas.width = w * dpr;
        canvas.height = h * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      }
      ctx.clearRect(0, 0, w, h);

      // grid
      ctx.strokeStyle = "rgba(51,65,85,0.55)";
      ctx.lineWidth = 1;
      for (let i = 1; i < 4; i++) {
        const y = (h * i) / 4;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }

      const pad = 16;
      const xs = primes.map((_, i) => pad + (i * (w - 2 * pad)) / (primes.length - 1));

      // Smooth background (schematic σ₃-scale curve)
      ctx.beginPath();
      ctx.strokeStyle = "rgba(56,189,248,0.85)";
      ctx.lineWidth = 2;
      xs.forEach((x, i) => {
        const p = primes[i].p;
        const smooth = 0.25 + 0.55 * Math.log(p) / Math.log(31);
        const y = h - pad - smooth * (h - 2 * pad);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();

      // Oscillating residual a_p² (normalised, with shimmer)
      ctx.beginPath();
      ctx.strokeStyle = "rgba(244,114,182,0.9)";
      ctx.lineWidth = 2;
      const maxAp2 = Math.max(...primes.map((r) => r.ap2));
      xs.forEach((x, i) => {
        const flicker = 0.08 * Math.sin(t * 3.2 + i * 1.1);
        const r = primes[i].ap2 / maxAp2 + flicker;
        const y = h * 0.55 - r * (h * 0.35);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();

      // points
      xs.forEach((x, i) => {
        const p = primes[i].p;
        const smooth = 0.25 + 0.55 * Math.log(p) / Math.log(31);
        const yS = h - pad - smooth * (h - 2 * pad);
        const flicker = 0.08 * Math.sin(t * 3.2 + i * 1.1);
        const r = primes[i].ap2 / maxAp2 + flicker;
        const yR = h * 0.55 - r * (h * 0.35);
        ctx.fillStyle = "#38bdf8";
        ctx.beginPath();
        ctx.arc(x, yS, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#f472b6";
        ctx.beginPath();
        ctx.arc(x, yR, 3, 0, Math.PI * 2);
        ctx.fill();
      });

      raf = requestAnimationFrame(draw);
    };

    raf = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(raf);
  }, [primes]);

  return (
    <div className="rounded-2xl border border-slate-700/50 bg-slate-950/60 p-4 sm:p-5">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <p className="font-mono text-[10px] uppercase tracking-widest text-slate-400">
          Two melodies · λ = λ_Eis + a_p²
        </p>
        <ul className="flex gap-4 font-mono text-[10px] text-slate-400">
          <li className="flex items-center gap-1.5">
            <span className="h-1.5 w-4 rounded-full bg-sky-400" aria-hidden />
            Witt / smooth
          </li>
          <li className="flex items-center gap-1.5">
            <span className="h-1.5 w-4 rounded-full bg-pink-400" aria-hidden />
            a_p² residual
          </li>
        </ul>
      </div>
      <canvas
        ref={canvasRef}
        className="h-44 w-full sm:h-52"
        aria-label="Animated chart of smooth background plus oscillating a_p squared residual"
      />
      <p className="mt-2 text-xs leading-relaxed text-slate-500">
        Schematic of the Eichler split (Teile 33, 36): elementary geometry plus
        exact cuspidal interference. Two-sided (no f₈ input) at p ≤ 5; closed
        forms to p ≤ 100.
      </p>
    </div>
  );
}

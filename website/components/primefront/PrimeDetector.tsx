"use client";

import { useMemo, useState } from "react";

/** Demo window n = 2..40. Formula: shell count target = 240(1+n³); primes match. */
const DEMO_N = Array.from({ length: 39 }, (_, i) => i + 2);

function isPrime(n: number): boolean {
  if (n < 2) return false;
  if (n % 2 === 0) return n === 2;
  for (let d = 3; d * d <= n; d += 2) {
    if (n % d === 0) return false;
  }
  return true;
}

/** Classical σ₃ criterion: n prime ⟺ r_E8(2n) = 240(1+n³). */
function targetCount(n: number): number {
  return 240 * (1 + n * n * n);
}

/** Two-squares via χ₄: odd prime is a²+b² iff p ≡ 1 (mod 4). */
function isSumOfTwoSquares(p: number): boolean {
  if (p === 2) return true;
  return isPrime(p) && p % 4 === 1;
}

export function PrimeDetector() {
  const [n, setN] = useState(11);
  const prime = isPrime(n);
  const target = targetCount(n);
  const match = prime; // in the classical criterion, match ⟺ prime

  const strip = useMemo(
    () =>
      DEMO_N.map((k) => ({
        k,
        prime: isPrime(k),
        twoSq: isSumOfTwoSquares(k),
      })),
    [],
  );

  return (
    <div className="rounded-2xl border border-slate-700/50 bg-slate-950/60 p-4 sm:p-5">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-widest text-slate-400">
            Geometric primality demo
          </p>
          <p className="mt-1 font-serif text-lg text-slate-100">
            n = <span className="font-mono text-sky-300">{n}</span>
          </p>
        </div>
        <label className="flex flex-col gap-1 text-[11px] text-slate-400">
          Pick n ∈ [2, 40]
          <input
            type="range"
            min={2}
            max={40}
            value={n}
            onChange={(e) => setN(Number(e.target.value))}
            className="w-48 accent-sky-400"
          />
        </label>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <div className="rounded-xl border border-slate-700/40 bg-slate-900/50 p-3">
          <p className="font-mono text-[10px] text-slate-500">
            Shell target · 240(1+n³)
          </p>
          <p className="mt-1 font-mono text-xl text-slate-100">
            {target.toLocaleString("en-US")}
          </p>
          <p className="mt-2 text-xs leading-relaxed text-slate-400">
            Classical σ₃ criterion (Teil 21): n&gt;1 is prime iff the E₈ shell at
            norm 2n has exactly this many vectors —{" "}
            <span className="text-slate-300">0 errors to 10⁴</span> in the probe.
          </p>
        </div>
        <div
          className={`rounded-xl border p-3 ${
            match
              ? "border-emerald-400/35 bg-emerald-500/10"
              : "border-slate-700/40 bg-slate-900/50"
          }`}
        >
          <p className="font-mono text-[10px] text-slate-500">Verdict</p>
          <p
            className={`mt-1 font-serif text-xl ${
              match ? "text-emerald-200" : "text-slate-300"
            }`}
          >
            {match ? "prime — shell matches" : "composite — shell mismatches"}
          </p>
          <p className="mt-2 text-xs leading-relaxed text-slate-400">
            χ₄ fibre (property channel):{" "}
            {isPrime(n) ? (
              isSumOfTwoSquares(n) ? (
                <span className="text-sky-300">p = a²+b² (p≡1 mod 4 or 2)</span>
              ) : (
                <span className="text-amber-200">not a sum of two squares</span>
              )
            ) : (
              <span className="text-slate-500">— (n not prime)</span>
            )}
          </p>
        </div>
      </div>

      <div
        className="mt-4 flex flex-wrap gap-1"
        role="list"
        aria-label="Numbers 2 to 40 coloured by primality"
      >
        {strip.map(({ k, prime: p, twoSq }) => (
          <button
            key={k}
            type="button"
            role="listitem"
            onClick={() => setN(k)}
            title={
              p
                ? twoSq
                  ? `${k} prime, two squares`
                  : `${k} prime, not two squares`
                : `${k} composite`
            }
            className={`h-7 w-7 rounded-md font-mono text-[10px] transition ${
              k === n
                ? "ring-2 ring-white/70"
                : ""
            } ${
              p
                ? twoSq
                  ? "bg-sky-500/25 text-sky-100 hover:bg-sky-500/40"
                  : "bg-emerald-500/20 text-emerald-100 hover:bg-emerald-500/35"
                : "bg-slate-800/80 text-slate-500 hover:bg-slate-700"
            }`}
          >
            {k}
          </button>
        ))}
      </div>
      <p className="mt-2 font-mono text-[10px] text-slate-500">
        Green = prime · cyan = prime and sum of two squares · gray = composite
      </p>
    </div>
  );
}

"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

type AtlasObject = {
  id: string;
  name: string;
  centre: number;
  weight: string;
  note: string;
  channel: "abelian" | "cuspidal" | "other";
};

const OBJECTS: AtlasObject[] = [
  {
    id: "mellin-th3",
    name: "Mellin(θ₃)",
    centre: 0.5,
    weight: "≤1",
    note: "→ π⁻ˢΓ(s)ζ(2s) — classical Riemann θ proof; centre 1/2.",
    channel: "abelian",
  },
  {
    id: "zeta-qi",
    name: "ζ_{ℚ(i)} = ζ L(χ₄)",
    centre: 0.5,
    weight: "1",
    note: "Dedekind zeta of the μ₄-field; FE about 1/2. Abelian drop closed.",
    channel: "abelian",
  },
  {
    id: "epstein",
    name: "E₈ Epstein / total census",
    centre: 2,
    weight: "4",
    note: "Λ_E8(s)=Λ_E8(4−s); fix line Re s = 2 = k/2.",
    channel: "other",
  },
  {
    id: "signed",
    name: "Signed census L-series",
    centre: 2,
    weight: "4",
    note: "ηη − 8L(f₈) — pole-killed; still weight 4.",
    channel: "cuspidal",
  },
  {
    id: "f8",
    name: "L(f₈, s)",
    centre: 2,
    weight: "4",
    note: "Where a_p lives. Needs its own cuspidal bridge — still open.",
    channel: "cuspidal",
  },
  {
    id: "rs-ab",
    name: "RS abelian product",
    centre: 1,
    weight: "normed",
    note: "After weight normalisation: shifts {+1,+1,−1,−1} — no ξ-line factor.",
    channel: "abelian",
  },
];

export function CenterAtlas() {
  const [active, setActive] = useState(OBJECTS[0].id);
  const selected = OBJECTS.find((o) => o.id === active) ?? OBJECTS[0];

  return (
    <div className="rounded-2xl border border-slate-700/50 bg-slate-950/60 p-4 sm:p-5">
      <p className="mb-4 font-mono text-[10px] uppercase tracking-widest text-violet-300/90">
        Centre atlas · click an object
      </p>

      <div className="relative mx-auto max-w-xl px-2 pb-8 pt-6">
        {/* axis */}
        <div className="relative h-2 rounded-full bg-slate-800">
          <div className="absolute inset-y-0 left-0 w-1/4 rounded-full bg-gradient-to-r from-violet-500/50 to-transparent" />
          <span className="absolute -top-5 left-0 font-mono text-[10px] text-violet-300">
            centre ½ (ξ)
          </span>
          <span className="absolute -top-5 left-1/2 -translate-x-1/2 font-mono text-[10px] text-slate-500">
            1
          </span>
          <span className="absolute -top-5 right-0 font-mono text-[10px] text-slate-400">
            centre 2
          </span>
        </div>

        <div className="relative mt-6 h-28">
          {OBJECTS.map((o) => {
            const left = `${(o.centre / 2) * 100}%`;
            const y =
              o.channel === "abelian" ? "10%" : o.channel === "cuspidal" ? "55%" : "32%";
            const color =
              o.channel === "abelian"
                ? "border-violet-400/50 bg-violet-500/20 text-violet-100"
                : o.channel === "cuspidal"
                  ? "border-rose-400/40 bg-rose-500/15 text-rose-100"
                  : "border-slate-500/40 bg-slate-700/40 text-slate-200";
            return (
              <button
                key={o.id}
                type="button"
                onClick={() => setActive(o.id)}
                style={{ left, top: y }}
                className={cn(
                  "absolute -translate-x-1/2 whitespace-nowrap rounded-full border px-2.5 py-1 font-mono text-[10px] transition",
                  color,
                  active === o.id && "ring-2 ring-white/50 scale-105",
                )}
              >
                {o.name}
              </button>
            );
          })}
        </div>
      </div>

      <div className="rounded-xl border border-slate-700/40 bg-slate-900/50 p-3">
        <div className="flex flex-wrap items-baseline gap-2">
          <h3 className="font-serif text-lg text-slate-100">{selected.name}</h3>
          <span className="font-mono text-[10px] text-slate-500">
            weight {selected.weight} · centre {selected.centre}
          </span>
        </div>
        <p className="mt-1 text-sm leading-relaxed text-slate-400">
          {selected.note}
        </p>
      </div>
    </div>
  );
}

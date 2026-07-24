import { PRIME_FRONT_UPDATES, type PrimeFrontVerdict } from "@/lib/primeFront";
import { StatusBadge } from "./StatusBadge";

const VERDICT_COLOR: Partial<Record<PrimeFrontVerdict, string>> = {
  PROMOTED: "text-emerald-300",
  EXACT: "text-sky-300",
  CLOSED: "text-violet-300",
  HARDENED: "text-teal-300",
  REPAIRED: "text-cyan-300",
  FOUNDED: "text-indigo-300",
  "TERRAIN-MAPPED": "text-slate-200",
  TYPED: "text-slate-300",
  PARTIAL: "text-amber-200",
  MIXED: "text-amber-200",
  BENCHMARK: "text-slate-300",
  DEFLATED: "text-rose-300",
  DEAD: "text-rose-300",
  "KILLED-AS-NAIVE": "text-rose-300",
  RUNNING: "text-sky-300",
};

export function UpdateFeed() {
  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-400">
        One entry per completed agent run. Newest first. To post a future update,
        prepend an object to{" "}
        <code className="rounded bg-slate-800/80 px-1.5 py-0.5 font-mono text-[11px] text-slate-300">
          website/lib/primeFront.ts
        </code>
        .
      </p>
      <ol className="space-y-3">
        {PRIME_FRONT_UPDATES.map((u, i) => (
          <li
            key={`${u.part}-${u.title}-${i}`}
            className="rounded-2xl border border-slate-700/45 bg-slate-950/50 p-4 sm:p-5"
          >
            <div className="flex flex-wrap items-center gap-2">
              <time
                dateTime={u.date}
                className="font-mono text-[11px] text-slate-500"
              >
                {u.date}
              </time>
              <span className="font-mono text-[11px] text-slate-400">
                Teil {u.part}
              </span>
              <StatusBadge badge={u.badge} />
              <span
                className={`ml-auto font-mono text-[10px] font-semibold uppercase tracking-wider ${
                  VERDICT_COLOR[u.verdict] ?? "text-slate-400"
                }`}
              >
                {u.verdict}
              </span>
            </div>
            <h3 className="mt-2 font-serif text-lg text-slate-100">{u.title}</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-slate-400">
              {u.summary}
            </p>
            {u.script && (
              <p className="mt-2 font-mono text-[10px] text-slate-600">
                {u.script}
              </p>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
}

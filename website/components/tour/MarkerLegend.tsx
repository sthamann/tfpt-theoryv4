import { STATUS_MARKERS } from "./tourData";

const META: Record<
  (typeof STATUS_MARKERS)[number],
  { meaning: string; tone: string }
> = {
  "[E]": {
    meaning: "exact / machine-proven",
    tone: "text-emerald-200 bg-emerald-500/15 ring-emerald-400/30",
  },
  "[C]": {
    meaning: "conditional under named hypotheses",
    tone: "text-amber-200 bg-amber-500/15 ring-amber-400/30",
  },
  "[O]": {
    meaning: "open / declared input",
    tone: "text-rose-200 bg-rose-500/15 ring-rose-400/30",
  },
  "[X]": {
    meaning: "falsifiable kill test",
    tone: "text-blue-200 bg-blue-500/15 ring-blue-400/30",
  },
};

export function MarkerLegend() {
  return (
    <ul className="mt-4 grid gap-2 sm:grid-cols-2">
      {STATUS_MARKERS.map((m) => (
        <li
          key={m}
          className={`flex items-start gap-2 rounded-xl px-3 py-2 text-xs ring-1 ${META[m].tone}`}
        >
          <span className="font-mono font-semibold">{m}</span>
          <span className="text-slate-300">{META[m].meaning}</span>
        </li>
      ))}
    </ul>
  );
}

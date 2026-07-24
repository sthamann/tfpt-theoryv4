import Link from "next/link";

export function HonestyBanner() {
  return (
    <aside
      role="note"
      aria-label="Research honesty notice"
      className="relative overflow-hidden rounded-2xl border border-amber-400/40 bg-gradient-to-br from-amber-500/15 via-slate-950/80 to-slate-950/90 p-5 sm:p-6"
    >
      <div
        aria-hidden
        className="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full bg-amber-400/10 blur-2xl"
      />
      <p className="font-mono text-[10px] font-semibold uppercase tracking-[0.2em] text-amber-300">
        Honesty first
      </p>
      <p className="mt-2 max-w-3xl text-sm leading-relaxed text-amber-50/95 sm:text-base">
        Research diary. Everything here is exploratory sandbox work unless
        explicitly marked as machine-verified (currently:{" "}
        <Link
          href="/verification"
          className="font-mono text-emerald-300 underline decoration-emerald-400/40 underline-offset-2 hover:text-emerald-200"
        >
          v535
        </Link>
        ). No claim of progress toward the Riemann Hypothesis is made.
      </p>
    </aside>
  );
}

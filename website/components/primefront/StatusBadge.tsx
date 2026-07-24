import { cn } from "@/lib/utils";
import type { PrimeFrontBadge } from "@/lib/primeFront";

const STYLES: Record<
  PrimeFrontBadge,
  { label: string; className: string }
> = {
  sandbox: {
    label: "sandbox",
    className:
      "border-amber-400/30 bg-amber-500/10 text-amber-200",
  },
  "machine-verified": {
    label: "machine-verified",
    className:
      "border-emerald-400/35 bg-emerald-500/10 text-emerald-200",
  },
  running: {
    label: "running",
    className:
      "border-sky-400/35 bg-sky-500/10 text-sky-200",
  },
};

export function StatusBadge({
  badge,
  className,
}: {
  badge: PrimeFrontBadge;
  className?: string;
}) {
  const s = STYLES[badge];
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-widest",
        s.className,
        className,
      )}
    >
      {badge === "running" && (
        <span
          className="h-1.5 w-1.5 animate-pulse rounded-full bg-sky-300"
          aria-hidden
        />
      )}
      [{s.label}]
    </span>
  );
}

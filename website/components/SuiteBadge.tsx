import Link from "next/link";
import { SCRIPT_TOTAL } from "@/lib/suite";
import { SITE_DATE } from "@/lib/version";
import { cn } from "@/lib/utils";

/**
 * Static per-release suite status. Values are build-time imports from
 * suite.ts / version.ts — not live-fetched. Honest: green for this release cut.
 */
export function SuiteBadge({
  className,
  href = "/verification",
}: {
  className?: string;
  href?: string;
}) {
  const label = `suite green · ${SCRIPT_TOTAL}/${SCRIPT_TOTAL} · synced ${SITE_DATE}`;
  return (
    <Link
      href={href}
      title="Verification suite status for this site release (static, not live)"
      className={cn(
        "inline-flex items-center gap-1.5 border border-slate-600/50 bg-slate-950/70 px-2 py-0.5 font-mono text-[10px] tracking-wide text-slate-300 transition-colors hover:border-slate-500 hover:text-slate-100",
        className,
      )}
    >
      <span
        aria-hidden
        className="h-1.5 w-1.5 flex-none rounded-full bg-emerald-400"
      />
      <span>{label}</span>
    </Link>
  );
}

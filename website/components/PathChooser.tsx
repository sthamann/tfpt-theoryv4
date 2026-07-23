import Link from "next/link";
import { ArrowRight, BookOpen, FlaskConical, ShieldAlert } from "lucide-react";
import { SectionHeader } from "./SectionHeader";

const PATHS: {
  role: string;
  title: string;
  body: string;
  href: string;
  cta: string;
  icon: typeof BookOpen;
}[] = [
  {
    role: "Curious?",
    title: "Tour or film",
    body: "Take the guided tour, or watch five and a half minutes of plain language — the claim stack without the jargon tax.",
    href: "/tour",
    cta: "Open the tour",
    icon: BookOpen,
  },
  {
    role: "Physicist?",
    title: "Verification + kill board",
    body: "Run a check in the browser, read the status ledger, and see exactly how the programme can fail.",
    href: "/verification#dag",
    cta: "Open verification",
    icon: ShieldAlert,
  },
  {
    role: "Want to reproduce?",
    title: "Clone, run, report",
    body: "One command to the suite green line. External replications: still zero — that is the invitation.",
    href: "/replication",
    cta: "Replication page",
    icon: FlaskConical,
  },
];

export function PathChooser() {
  return (
    <section
      id="path"
      className="relative scroll-mt-20 border-t border-slate-800/60 py-14 sm:py-16"
      aria-labelledby="path-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          id="path-heading"
          eyebrow="Next step"
          title="Choose your path"
          description="Three doors — pick the one that matches how you want to pressure-test the claim."
        />
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {PATHS.map((p) => {
            const Icon = p.icon;
            return (
              <Link
                key={p.role}
                href={p.href}
                className="group flex flex-col border border-slate-700/50 bg-slate-950/50 p-5 transition-colors hover:border-slate-500/60 hover:bg-slate-900/40"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-[11px] font-semibold uppercase tracking-widest text-slate-400">
                    {p.role}
                  </span>
                  <Icon size={16} className="text-slate-500" aria-hidden />
                </div>
                <h3 className="mt-3 font-serif text-lg font-semibold text-slate-50">
                  {p.title}
                </h3>
                <p className="mt-2 flex-1 text-sm leading-relaxed text-slate-400">
                  {p.body}
                </p>
                <span className="mt-4 inline-flex items-center gap-1.5 text-sm font-semibold text-blue-300 group-hover:text-blue-200">
                  {p.cta}
                  <ArrowRight
                    size={14}
                    className="transition-transform group-hover:translate-x-0.5"
                    aria-hidden
                  />
                </span>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SectionHeader } from "./SectionHeader";

const NEGATIVES: { title: string; body: string }[] = [
  {
    title: "RXTE HFQPO null",
    body: "Preregistered archival scan: no ×1.5 ladder tooth. 3σ sensitivity ~0.75% rms (best source).",
  },
  {
    title: "NICER recovery null",
    body: "Dense timing channel: no frozen recovery comb at detectable amplitude. Sensitivity ~0.93% rms.",
  },
  {
    title: "2DCS kill (toy)",
    body: "Interacting Fidkowski–Kitaev toy fails Kill-Test 2 — the straddle law (v529). Published, not buried.",
  },
  {
    title: "Ten side-blind bit tests",
    body: "Ten derivation attempts on the remaining input bit all failed — the bit stays an input (twist-class choice).",
  },
];

/**
 * Explicit non-claims + honest negatives — the anti-hype band.
 * Copy for the lead paragraph is fixed by the homepage redesign brief.
 */
export function HonestyBand() {
  return (
    <section
      id="honesty"
      className="relative scroll-mt-20 border-t border-slate-800/60 py-14 sm:py-16"
      aria-labelledby="honesty-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          id="honesty-heading"
          eyebrow="Honesty"
          title="What we do not claim"
          description="The strongest credibility move is naming the gaps before a reviewer finds them."
        />

        <div className="mt-8 grid gap-6 lg:grid-cols-[1.2fr_1fr]">
          <div className="border border-amber-500/25 bg-amber-500/[0.04] px-5 py-5 sm:px-6">
            <p className="text-sm leading-relaxed text-slate-200 sm:text-[15px]">
              <span className="font-semibold text-amber-100">
                What we do not claim.{" "}
              </span>
              SEAM.EQUIV is not closed as an unconditional theorem. One input
              bit stays an input (ten blind derivation attempts failed —
              that&rsquo;s the point). The first interacting toy fails our own
              kill test (v529) — published, not buried. Empirical HFQPO
              searches returned nulls; they are search targets, not claims. No
              external lab has reproduced the suite yet — we want that to
              change.
            </p>
            <div className="mt-4 flex flex-wrap gap-3 text-xs font-semibold">
              <Link
                href="/falsification"
                className="inline-flex items-center gap-1 text-rose-200 underline decoration-rose-400/40 underline-offset-2 hover:text-rose-100"
              >
                Kill board <ArrowRight size={12} aria-hidden />
              </Link>
              <Link
                href="/replication"
                className="inline-flex items-center gap-1 text-slate-300 underline decoration-slate-600 underline-offset-2 hover:text-white"
              >
                Replication status <ArrowRight size={12} aria-hidden />
              </Link>
            </div>
          </div>

          <aside
            aria-labelledby="honest-negatives-heading"
            className="border border-slate-700/50 bg-slate-950/60"
          >
            <div className="border-b border-slate-800/70 px-4 py-3">
              <h3
                id="honest-negatives-heading"
                className="font-mono text-[11px] font-semibold uppercase tracking-widest text-slate-400"
              >
                Honest negatives
              </h3>
            </div>
            <ul className="divide-y divide-slate-800/70">
              {NEGATIVES.map((n) => (
                <li key={n.title} className="px-4 py-3">
                  <div className="font-mono text-[11px] font-semibold text-slate-200">
                    {n.title}
                  </div>
                  <p className="mt-1 text-xs leading-relaxed text-slate-400">
                    {n.body}
                  </p>
                </li>
              ))}
            </ul>
          </aside>
        </div>
      </div>
    </section>
  );
}

"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  ExternalLink,
  Github,
  ShieldAlert,
  Terminal,
} from "lucide-react";
import { WoitBridgeProgress } from "@/components/WoitBridgeProgress";
import { REPO_URL } from "@/lib/utils";
import {
  ALPHA,
  AXIOMS,
  BRIDGES,
  COMPILER,
  EMPIRICAL_NULLS,
  INPUT_BIT,
  LINKS,
  OPEN,
  PREDICTIONS,
  SEAM,
  TOUR_AS_OF,
  TOUR_STEPS,
  TOY_KILL,
  VERIFICATION,
  type TourStepId,
} from "./tourData";
import { CompilerDiagram } from "./CompilerDiagram";
import { MarkerLegend } from "./MarkerLegend";
import { SeamClock } from "./SeamClock";
import { TourNav } from "./TourNav";
import { TourStepCard } from "./TourStepCard";

function stepIndexFromHash(): number {
  if (typeof window === "undefined") return 0;
  const raw = window.location.hash.replace(/^#/, "");
  if (!raw.startsWith("step-")) return 0;
  const id = raw.slice(5) as TourStepId;
  const idx = TOUR_STEPS.findIndex((s) => s.id === id);
  return idx >= 0 ? idx : 0;
}

function scrollToStep(index: number, updateHash: boolean) {
  const step = TOUR_STEPS[index];
  if (!step) return;
  const el = document.getElementById(`step-${step.id}`);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  if (updateHash) {
    const url = `${window.location.pathname}#step-${step.id}`;
    window.history.replaceState(null, "", url);
  }
}

export function TourShell() {
  const [activeIndex, setActiveIndex] = useState(0);
  const steps = TOUR_STEPS;

  const go = useCallback((index: number) => {
    const clamped = Math.max(0, Math.min(steps.length - 1, index));
    setActiveIndex(clamped);
    scrollToStep(clamped, true);
  }, [steps.length]);

  const onPrev = useCallback(() => go(activeIndex - 1), [activeIndex, go]);
  const onNext = useCallback(() => go(activeIndex + 1), [activeIndex, go]);

  // Hash deep-link on mount + back/forward
  useEffect(() => {
    const apply = () => {
      const idx = stepIndexFromHash();
      setActiveIndex(idx);
      // delay so layout is ready
      requestAnimationFrame(() => scrollToStep(idx, false));
    };
    apply();
    window.addEventListener("hashchange", apply);
    return () => window.removeEventListener("hashchange", apply);
  }, []);

  // Keyboard ← / →
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (
        t &&
        (t.tagName === "INPUT" ||
          t.tagName === "TEXTAREA" ||
          t.tagName === "SELECT" ||
          t.isContentEditable)
      ) {
        return;
      }
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        onPrev();
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        onNext();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onPrev, onNext]);

  // Scroll-spy: which section is in view
  useEffect(() => {
    const nodes = steps
      .map((s) => document.getElementById(`step-${s.id}`))
      .filter((n): n is HTMLElement => Boolean(n));
    if (nodes.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (visible[0]?.target?.id) {
          const id = visible[0].target.id.replace(/^step-/, "") as TourStepId;
          const idx = steps.findIndex((s) => s.id === id);
          if (idx >= 0) setActiveIndex(idx);
        }
      },
      { rootMargin: "-20% 0px -55% 0px", threshold: [0.15, 0.35, 0.55] },
    );

    nodes.forEach((n) => observer.observe(n));
    return () => observer.disconnect();
  }, [steps]);

  const stepById = useMemo(() => {
    const map = new Map(steps.map((s) => [s.id, s]));
    return map;
  }, [steps]);

  return (
    <div className="relative pb-20">
      <TourNav
        steps={steps}
        activeIndex={activeIndex}
        onGo={go}
        onPrev={onPrev}
        onNext={onNext}
      />

      {/* Intro band */}
      <header className="relative isolate overflow-hidden pt-10 pb-4 sm:pt-14">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div className="relative mx-auto max-w-3xl px-4 sm:px-6">
          <nav aria-label="Breadcrumb" className="mb-5">
            <Link
              href="/"
              className="text-sm text-slate-400 transition-colors hover:text-slate-200"
            >
              ← Back to overview
            </Link>
          </nav>
          <span className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/10 px-3 py-1 text-xs font-medium uppercase tracking-widest text-blue-200">
            Guided tour · 10 steps
          </span>
          <h1 className="mt-5 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl">
            What TFPT claims — and how to check it
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300 sm:text-lg">
            A distill-style walkthrough for curious non-specialists and skeptical
            physicists. Plain English first; technical depth on demand. Not a
            &ldquo;proven TOE&rdquo; pitch — an honest map of axioms, machine
            checks, open gates, and kill tests. Facts as of {TOUR_AS_OF}.
          </p>
          <p className="mt-3 text-xs text-slate-500">
            Tip: ← / → keys move between steps · deep links look like{" "}
            <span className="font-mono text-slate-400">#step-seam</span>
          </p>
        </div>
      </header>

      {/* 1 — Two numbers */}
      <TourStepCard
        step={stepById.get("two-numbers")!}
        visual={
          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            <div className="rounded-2xl border border-blue-400/25 bg-blue-500/5 p-5">
              <p className="text-[11px] font-semibold uppercase tracking-widest text-blue-300">
                {AXIOMS.c3.label}
              </p>
              <p className="mt-2 font-mono text-2xl text-slate-50">
                {AXIOMS.c3.symbol} = {AXIOMS.c3.value}
              </p>
            </div>
            <div className="rounded-2xl border border-emerald-400/25 bg-emerald-500/5 p-5">
              <p className="text-[11px] font-semibold uppercase tracking-widest text-emerald-300">
                {AXIOMS.gCar.label}
              </p>
              <p className="mt-2 font-mono text-2xl text-slate-50">
                {AXIOMS.gCar.symbol} = {AXIOMS.gCar.value}
              </p>
            </div>
          </div>
        }
        depth={
          <p>
            The public display markers are [E] / [C] / [O] / [X]; fine claim
            types live only in <span className="font-mono">status_ledger.csv</span>
            , which wins on any disagreement. The load-bearing chain is the
            discrete compiler {COMPILER.chain}. This tour never upgrades an open
            gate.
          </p>
        }
      />

      {/* 2 — Compiler */}
      <TourStepCard
        step={stepById.get("compiler")!}
        visual={<CompilerDiagram />}
        depth={
          <p>
            {COMPILER.plain} The E₈ layer is the audit hull (240-root projection
            / referee), not a free fitting manifold. Carrier rigidity is also
            Lean-formalised ({VERIFICATION.leanCarrier}).
          </p>
        }
      />

      {/* 3 — Outputs */}
      <TourStepCard
        step={stepById.get("outputs")!}
        visual={
          <ul className="mt-6 grid gap-3">
            {PREDICTIONS.examples.map((ex) => (
              <li
                key={ex.id}
                className="rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4"
              >
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <h3 className="font-serif text-lg text-slate-50">{ex.title}</h3>
                  <span className="font-mono text-sm text-emerald-200">
                    {ex.value}
                  </span>
                </div>
                <p className="mt-1.5 text-sm text-slate-400">{ex.note}</p>
              </li>
            ))}
            <li className="rounded-xl border border-dashed border-slate-700/50 px-4 py-3 text-sm text-slate-400">
              Plus {PREDICTIONS.frozenCount - 3} further frozen predictions in the
              registry — {PREDICTIONS.frozenCount} total, blind-committed.
            </li>
          </ul>
        }
        depth={
          <p>
            Headline EM line: {ALPHA.label} = {ALPHA.inverse} ({ALPHA.sigmaToCodata}{" "}
            to CODATA). Mass ratios and mixings are readouts of the residue /
            carrier structure, not independent knobs. See{" "}
            <Link href="/#predictions" className="text-blue-300 hover:text-blue-200">
              predictions
            </Link>{" "}
            and the freeze file for the full surface.
          </p>
        }
      />

      {/* 4 — Not numerology */}
      <TourStepCard
        step={stepById.get("not-numerology")!}
        visual={<MarkerLegend />}
        depth={
          <ul className="list-disc space-y-2 pl-5">
            <li>
              <strong className="text-slate-200">Frozen predictions:</strong>{" "}
              {PREDICTIONS.frozenCount} entries committed before decisive data
              (registry + freeze file).
            </li>
            <li>
              <strong className="text-slate-200">Null MCs / LEE discipline:</strong>{" "}
              look-elsewhere and null-model batteries sit with the empirical
              searches; proximity to data never upgrades a ledger marker.
            </li>
            <li>
              <strong className="text-slate-200">Honesty markers:</strong> every
              load-bearing claim is typed [E]/[C]/[O]/[X]; the ledger is the
              single source of truth.
            </li>
            <li>
              <strong className="text-slate-200">Triple stack:</strong>{" "}
              {VERIFICATION.pythonModules} Python modules; Wolfram mirror{" "}
              {VERIFICATION.wolfram}; Lean carrier {VERIFICATION.leanCarrier}.
            </li>
          </ul>
        }
      >
        <p className="mt-5 text-sm leading-relaxed text-slate-400">
          Empirics that returned nulls (e.g. {EMPIRICAL_NULLS.rxte};{" "}
          {EMPIRICAL_NULLS.nicer}) stay search targets — never quietly promoted
          to theory claims.
        </p>
      </TourStepCard>

      {/* 5 — Seam */}
      <TourStepCard
        step={stepById.get("seam")!}
        visual={<SeamClock />}
        depth={
          <p>
            Geometry and anomaly/modular routes already pinned{" "}
            <span className="font-mono">{AXIOMS.c3.symbol} = {AXIOMS.c3.value}</span>
            . The thermal leg measures{" "}
            <span className="font-mono">{SEAM.temperature}</span> on the free
            OS quotient — {SEAM.temperatureNote}. Metaphor: {SEAM.clockMetaphor}.
            See also the thermal-legs panel on the home and verification pages.
          </p>
        }
      />

      {/* 6 — Check yourself */}
      <TourStepCard
        step={stepById.get("check-yourself")!}
        visual={
          <div className="mt-6 space-y-3">
            <div className="rounded-2xl border border-slate-700/40 bg-slate-950/60 p-4 font-mono text-sm text-slate-200">
              <div className="mb-2 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-widest text-emerald-300">
                <Terminal size={14} aria-hidden />
                One-liner
              </div>
              <code className="block whitespace-pre-wrap break-all">
                {VERIFICATION.runCommand}
              </code>
              <p className="mt-2 text-xs text-slate-400">
                Expected terminus:{" "}
                <span className="text-emerald-300">
                  {VERIFICATION.runPassLine}
                </span>{" "}
                ({VERIFICATION.pythonModules} modules).
              </p>
            </div>
            <Link
              href={LINKS.verificationDag}
              className="inline-flex items-center gap-2 rounded-xl border border-blue-400/30 bg-blue-500/10 px-4 py-3 text-sm font-medium text-blue-100 transition-colors hover:bg-blue-500/20"
            >
              Open the Pyodide DAG on /verification
              <ArrowRight size={16} aria-hidden />
            </Link>
          </div>
        }
        depth={
          <p>
            Independent second path: Wolfram {VERIFICATION.wolfram}. Carrier
            algebra in Lean 4 with {VERIFICATION.leanCarrier}. You can also clone{" "}
            <a
              href={REPO_URL}
              className="text-blue-300 hover:text-blue-200"
              target="_blank"
              rel="noopener noreferrer"
            >
              the public repo
            </a>{" "}
            and audit the ledger row-by-row.
          </p>
        }
      />

      {/* 7 — How it dies */}
      <TourStepCard
        step={stepById.get("how-it-dies")!}
        visual={
          <div className="mt-6 space-y-3">
            <div className="rounded-2xl border border-rose-400/30 bg-rose-500/5 p-4">
              <p className="text-[11px] font-semibold uppercase tracking-widest text-rose-300">
                Toy kill · banked
              </p>
              <p className="mt-2 font-serif text-xl text-slate-50">
                {TOY_KILL.id} · {TOY_KILL.name}
              </p>
              <p className="mt-2 text-sm leading-relaxed text-slate-300">
                {TOY_KILL.plain} Status: {TOY_KILL.status}.
              </p>
            </div>
            <Link
              href={LINKS.falsification}
              className="inline-flex items-center gap-2 text-sm font-medium text-blue-300 hover:text-blue-200"
            >
              <ShieldAlert size={16} aria-hidden />
              Full kill board & freeze criteria
              <ArrowRight size={14} aria-hidden />
            </Link>
          </div>
        }
        depth={
          <p>
            Structural kills include JUNO on sin²θ₁₂ = 0.3067, CMB-S4 on the
            frozen r-band, neutrino ordering, the strong-CP null, and w = −1 —
            each committed in advance. A single satisfied freeze criterion kills
            the construction. Empirical nulls ({EMPIRICAL_NULLS.nicer}) remain
            search targets behind the experiments firewall.
          </p>
        }
      />

      {/* 8 — Still open */}
      <TourStepCard
        step={stepById.get("still-open")!}
        visual={
          <ul className="mt-6 space-y-3">
            <li className="rounded-2xl border border-rose-400/25 bg-rose-500/5 p-4">
              <div className="flex items-center justify-between gap-2">
                <span className="font-mono text-sm text-slate-50">
                  {OPEN.seamEquiv.id}
                </span>
                <span className="rounded-full bg-rose-500/15 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-200 ring-1 ring-rose-400/30">
                  {OPEN.seamEquiv.marker}
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-300">{OPEN.seamEquiv.plain}</p>
            </li>
            <li className="rounded-2xl border border-amber-400/25 bg-amber-500/5 p-4">
              <div className="flex items-center justify-between gap-2">
                <span className="font-mono text-sm text-slate-50">
                  the one input bit
                </span>
                <span className="rounded-full bg-rose-500/15 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-200 ring-1 ring-rose-400/30">
                  {INPUT_BIT.status}
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-300">
                {INPUT_BIT.failedDerivations} side-blind derivation attempts
                failed — that&apos;s the point. Now defined as the{" "}
                <strong className="font-medium text-slate-100">
                  {INPUT_BIT.definition}
                </strong>
                , {INPUT_BIT.measurable}. It remains an input.
              </p>
            </li>
            <li className="rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4">
              <p className="text-sm text-slate-300">{OPEN.interactingSeam.plain}</p>
            </li>
          </ul>
        }
        depth={
          <p>
            {INPUT_BIT.note} Parent SEAM.EQUIV closes only if a named route
            closes; unconditional status stays [O]. External replications to
            date: {VERIFICATION.externalReplications}.
          </p>
        }
      />

      {/* 9 — Two bridges */}
      <TourStepCard
        step={stepById.get("two-bridges")!}
        visual={
          <div className="mt-6 space-y-4">
            <div className="rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="font-serif text-base font-semibold text-slate-50">
                  {BRIDGES.celestial.name}
                </h3>
                <span className="rounded-full bg-sky-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-sky-200 ring-1 ring-sky-400/30">
                  {BRIDGES.celestial.steps} steps
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-300">
                {BRIDGES.celestial.progressLabel}. Measure chain:{" "}
                <span className="text-emerald-200">
                  {BRIDGES.celestial.measureChain}
                </span>
                .
              </p>
              <div
                className="mt-3 h-2 overflow-hidden rounded-full bg-slate-800"
                role="progressbar"
                aria-valuenow={90}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label="Celestial route progress indicator"
              >
                <div className="h-full w-[90%] rounded-full bg-sky-400/80" />
              </div>
              <p className="mt-1.5 text-[11px] text-slate-500">
                Progress cue only — not a ledger upgrade.
              </p>
            </div>
            <WoitBridgeProgress />
          </div>
        }
        depth={
          <p>
            Woit contract {BRIDGES.woit.contract}: executed stages{" "}
            {BRIDGES.woit.executed.join(" · ")}; open: {BRIDGES.woit.open}. The
            celestial measure-chain derivation is at probe level — do not read
            this bar as closure of SEAM.EQUIV.
          </p>
        }
      />

      {/* 10 — Join in */}
      <TourStepCard
        step={stepById.get("join-in")!}
        visual={
          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            <Link
              href={LINKS.replication}
              className="rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 transition-colors hover:border-blue-400/40 hover:bg-blue-500/5"
            >
              <p className="text-[11px] font-semibold uppercase tracking-widest text-blue-300">
                Reproduce
              </p>
              <p className="mt-2 font-serif text-lg text-slate-50">/replication</p>
              <p className="mt-1 text-xs text-slate-400">
                Self-verified scorecard · {VERIFICATION.externalReplications}{" "}
                external replications yet
              </p>
            </Link>
            <Link
              href={LINKS.review}
              className="rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 transition-colors hover:border-blue-400/40 hover:bg-blue-500/5"
            >
              <p className="text-[11px] font-semibold uppercase tracking-widest text-blue-300">
                Review
              </p>
              <p className="mt-2 font-serif text-lg text-slate-50">/review</p>
              <p className="mt-1 text-xs text-slate-400">
                Hostile-reviewer entry in five minutes
              </p>
            </Link>
            <a
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 transition-colors hover:border-emerald-400/40 hover:bg-emerald-500/5"
            >
              <p className="inline-flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-widest text-emerald-300">
                <Github size={12} aria-hidden />
                Falsify
              </p>
              <p className="mt-2 font-serif text-lg text-slate-50">GitHub</p>
              <p className="mt-1 inline-flex items-center gap-1 text-xs text-slate-400">
                Clone · run · open an issue
                <ExternalLink size={11} aria-hidden />
              </p>
            </a>
          </div>
        }
        depth={
          <p>
            Also useful:{" "}
            <Link href={LINKS.orientation} className="text-blue-300 hover:text-blue-200">
              /orientation
            </Link>{" "}
            (one-map reading guide) and{" "}
            <Link href={LINKS.falsification} className="text-blue-300 hover:text-blue-200">
              /falsification
            </Link>{" "}
            (kill board). We will record external reproductions and disputes on
            the replication page — including negative ones.
          </p>
        }
      />

      {/* End CTA strip */}
      <div className="mx-auto max-w-3xl px-4 pb-8 sm:px-6">
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-700/40 bg-slate-950/40 px-4 py-4">
          <p className="text-sm text-slate-400">
            Step {activeIndex + 1} of {steps.length}
          </p>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={onPrev}
              disabled={activeIndex <= 0}
              className="rounded-lg border border-slate-700/60 px-3 py-1.5 text-sm text-slate-200 disabled:opacity-30"
            >
              Previous
            </button>
            <button
              type="button"
              onClick={onNext}
              disabled={activeIndex >= steps.length - 1}
              className="rounded-lg border border-blue-400/40 bg-blue-500/15 px-3 py-1.5 text-sm text-blue-100 disabled:opacity-30"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

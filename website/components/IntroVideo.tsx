"use client";

import { useEffect, useRef, useState } from "react";
import { Play } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { cn, SITE_URL } from "@/lib/utils";

const VIDEO_SRC = "/intro/tfpt-intro.mp4";
const POSTER_SRC = "/intro/tfpt-intro-poster.jpeg";
const CAPTIONS_SRC = "/intro/tfpt-intro.en.vtt";

/** Chapter markers — seconds match the video's eight beats (script.ts). */
const CHAPTERS: { t: number; label: string }[] = [
  { t: 0, label: "The bet" },
  { t: 15, label: "The machine" },
  { t: 55, label: "The readout" },
  { t: 95, label: "One pattern" },
  { t: 120, label: "Gravity for free" },
  { t: 146, label: "Not numerology" },
  { t: 189, label: "How to kill it" },
  { t: 219, label: "What's open" },
];

/**
 * The transcript, grouped by chapter. Mirrored from the video's caption track
 * (captions.json). Rendered as visible (collapsible) text so it is accessible to
 * screen readers and indexable by search/answer engines (the video pixels are
 * not). Keep in sync with /intro/tfpt-intro.en.vtt.
 */
const TRANSCRIPT: { heading: string; body: string }[] = [
  {
    heading: "The bet (0:00)",
    body: "This is the fine-structure constant — how strongly light and matter interact. Physics measures it. TFPT computes it — the one answer a short equation allows, fixed by just two numbers, and nothing else. Bold claim. So I'll also show you exactly where it could break.",
  },
  {
    heading: "The machine (0:15)",
    body: "Think of TFPT as a compiler — not a table of lucky numbers, but a machine. Two inputs go in: a boundary constant, c₃ = 1/(8π) — the rule for an edge of space, and a carrier, g_car = 5 — how the building blocks plug together. From only those two, one shape is forced to assemble: the exceptional group E₈. But here's the twist — E₈ is not a force of nature. It's a scaffold: a consistency check you build, verify against, then step away from. The Standard Model isn't “everything is E₈” — it's what you read off after projecting back down.",
  },
  {
    heading: "The readout (0:55)",
    body: "So what does the machine print out? First, a discrete skeleton — exact and machine-checked, with no wiggle room: three generations of matter, the right charges, the 240 roots of E₈, and the same small numbers everywhere — two, three, five. Then the headline: the fine-structure constant is the single positive root of one cubic. Not chosen — forced. α⁻¹ = 137.0359992, less than two sigma from the measured value. Not a fit. A forced answer.",
  },
  {
    heading: "One pattern, not free knobs (1:35)",
    body: "The same discipline runs through the particle masses. They don't come from dozens of free dials — but from one pattern: a single seed, a fixed matrix, and whole-number steps. Mixing angles and the leading CP phase drop out of the same geometry. The one honest unit they still need, we flag — we don't hide it.",
  },
  {
    heading: "Gravity comes free (2:00)",
    body: "And that first input hides a gift. c₃ = 1/(8π) is the exact 8π sitting inside Einstein's equation for gravity. Run the same atoms through the heat of a horizon, and the full law of gravity falls out — both constants fixed, even the cosmological constant, set by α. The same 1/(8π) shows up three independent ways. Hard to call that an accident.",
  },
  {
    heading: "Why this isn't numerology (2:26)",
    body: "Small whole numbers raise a fair worry: is this just numerology? So we tried to break it ourselves. We froze thirteen predictions, then ran two hundred thousand random look-alike theories. TFPT hits all thirteen. The random ones top out at five. For α: of ninety-four thousand variants, exactly one lands in the measured window. Seven completely different number systems each rebuild the same skeleton. And we publish what E₈ does not use — five of its eight pieces carry no prediction. The odds a look-alike matches the whole scorecard: below ten to the minus thirty. Checked twice — independently in Wolfram and in Lean.",
  },
  {
    heading: "How to kill it (3:09)",
    body: "Now the honest part — how would you kill it? Every prediction was sealed in a registry before any comparison. sin²θ₁₂ ≈ 0.3067. sin²θ₁₃ ≈ 0.0231. A tiny gravitational-wave ratio. Normal neutrino ordering. Today, all of them sit within about one sigma. The near-term tests are real: neutrino mass from DESI and CMB-S4, and proton decay at Hyper-Kamiokande. One clean miss, and it's wrong.",
  },
  {
    heading: "What is actually open (3:39)",
    body: "So what is actually still open? Not a vague pile — three named, labelled handoffs. One published-theorem step from closing the central seam, the clearly-marked bridges to external physics, and one honest unit — because a theorem says pure numbers can never hand you a kilogram. Zero hidden mechanisms. Two inputs, one compiler — fully audited.",
  },
];

const fmt = (t: number) => `${Math.floor(t / 60)}:${String(t % 60).padStart(2, "0")}`;

const videoJsonLd = {
  "@context": "https://schema.org",
  "@type": "VideoObject",
  name: "TFPT — a 4-minute introduction",
  description:
    "A 4-minute introduction to Topological Fixed-Point Theory (TFPT): two inputs — the boundary constant c₃ = 1/(8π) and the carrier g_car = 5 — drive a discrete compiler with E₈ as a consistency scaffold, reading off the Standard-Model structure, the fine-structure constant α⁻¹ = 137.0359992, the particle-mass pattern, and a parameter-free law of gravity (c₃ = 1/(8π) is the 8π of Einstein's equation). It then shows why this isn't numerology — a frozen 13/13 scorecard against 200,000 random look-alike theories, α unique to 1 in 94,500, a richly over-determined integer skeleton, odds below 10⁻³⁰, checked independently in Wolfram and Lean — the near-term kill tests, and the honest residual: three named, typed interfaces with zero hidden mechanisms.",
  thumbnailUrl: [`${SITE_URL}${POSTER_SRC}`],
  uploadDate: "2026-06-25",
  duration: "PT4M10S",
  contentUrl: `${SITE_URL}${VIDEO_SRC}`,
  inLanguage: "en",
  isFamilyFriendly: true,
  transcript: TRANSCRIPT.map((s) => `${s.heading}\n${s.body}`).join("\n\n"),
  publisher: {
    "@type": "Organization",
    name: "TFPT Collaboration",
    url: SITE_URL,
  },
};

export function IntroVideo() {
  const ref = useRef<HTMLVideoElement>(null);
  const [started, setStarted] = useState(false);

  // Captions are burned into the video (open captions). Browsers remember a
  // user's prior "captions on" preference and would auto-show the <track>,
  // doubling the captions — so default the selectable track off; users can still
  // enable it from the native captions menu.
  const disableTracks = () => {
    const v = ref.current;
    if (!v) return;
    for (const t of Array.from(v.textTracks)) t.mode = "disabled";
  };
  useEffect(disableTracks, []);

  const play = () => {
    const v = ref.current;
    if (!v) return;
    setStarted(true);
    void v.play();
  };

  const seek = (t: number) => {
    const v = ref.current;
    if (!v) return;
    v.currentTime = t;
    setStarted(true);
    void v.play();
  };

  return (
    <section
      id="intro-video"
      className="relative scroll-mt-20 py-20 sm:py-24"
      aria-labelledby="intro-video-heading"
    >
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(videoJsonLd) }}
      />
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          id="intro-video-heading"
          align="center"
          eyebrow="Start here"
          title="The 4-minute introduction"
          description="Two inputs in, E₈ as a consistency scaffold, the Standard Model, the constants and even gravity out — plus why this isn't numerology, the near-term kill tests, and an honest residual of three named interfaces."
        />

        <figure className="mt-10">
          <div className="relative overflow-hidden rounded-2xl border border-slate-700/50 bg-slate-950/60 shadow-2xl shadow-blue-500/10">
            <video
              ref={ref}
              className="aspect-video w-full"
              controls
              playsInline
              preload="none"
              poster={POSTER_SRC}
              aria-label="TFPT — a 4-minute introduction (English, with subtitles)"
              onLoadedMetadata={disableTracks}
            >
              <source src={VIDEO_SRC} type="video/mp4" />
              {/* Captions are burned in (open captions); this selectable track
                  stays available for users who prefer browser-styled subtitles
                  and for indexing — not `default`, to avoid double captions. */}
              <track
                kind="subtitles"
                src={CAPTIONS_SRC}
                srcLang="en"
                label="English"
              />
              Your browser does not support the video tag. You can read the full
              transcript below.
            </video>

            {!started && (
              <button
                type="button"
                onClick={play}
                aria-label="Play the 4-minute introduction"
                className="group absolute inset-0 flex items-center justify-center bg-slate-950/30 transition-colors hover:bg-slate-950/15 focus-visible:outline-none"
              >
                <span className="flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-violet-500 text-white shadow-lg shadow-blue-500/40 ring-1 ring-white/20 transition-transform group-hover:scale-110 group-focus-visible:scale-110">
                  <Play size={34} className="ml-1" aria-hidden />
                </span>
              </button>
            )}
          </div>

          {/* chapter markers */}
          <nav
            aria-label="Video chapters"
            className="mt-4 flex flex-wrap justify-center gap-2"
          >
            {CHAPTERS.map((c) => (
              <button
                key={c.t}
                type="button"
                onClick={() => seek(c.t)}
                className={cn(
                  "inline-flex items-center gap-2 rounded-full border border-slate-700/50 bg-slate-900/60 px-3 py-1.5 text-xs font-medium text-slate-300 transition-colors hover:border-blue-400/40 hover:text-blue-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400/40",
                )}
              >
                <span className="font-mono text-blue-300/80">{fmt(c.t)}</span>
                {c.label}
              </button>
            ))}
          </nav>

          <figcaption className="mt-3 text-center text-xs text-slate-500">
            English narration with on-screen captions; a selectable subtitle
            track and the full transcript below are generated from the same
            source.
          </figcaption>
        </figure>

        {/* transcript — accessible + indexable */}
        <details className="group mt-8 rounded-2xl border border-slate-700/40 bg-slate-950/40 p-5 sm:p-6">
          <summary className="flex cursor-pointer list-none items-center justify-between text-sm font-semibold text-slate-200 transition-colors hover:text-white">
            <span>Read the full transcript</span>
            <span className="text-slate-500 transition-transform group-open:rotate-180">
              ⌄
            </span>
          </summary>
          <div className="prose-tfpt mt-5 space-y-5">
            {TRANSCRIPT.map((s) => (
              <div key={s.heading}>
                <h3 className="font-serif text-base font-semibold text-slate-100">
                  {s.heading}
                </h3>
                <p className="mt-1 text-sm leading-relaxed text-slate-300">
                  {s.body}
                </p>
              </div>
            ))}
          </div>
        </details>
      </div>
    </section>
  );
}

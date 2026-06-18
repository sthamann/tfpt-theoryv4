"use client";

import { useEffect, useRef, useState } from "react";
import { Play } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { cn, SITE_URL } from "@/lib/utils";

const VIDEO_SRC = "/intro/tfpt-intro.mp4";
const POSTER_SRC = "/intro/tfpt-intro-poster.jpeg";
const CAPTIONS_SRC = "/intro/tfpt-intro.en.vtt";

/** Chapter markers — seconds match the video's seven beats (script.ts). */
const CHAPTERS: { t: number; label: string }[] = [
  { t: 0, label: "The bet" },
  { t: 15, label: "The machine" },
  { t: 56, label: "The readout" },
  { t: 97, label: "One texture" },
  { t: 123, label: "How to kill it" },
  { t: 154, label: "The audit layer" },
  { t: 173, label: "The open knot" },
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
    body: "This is the fine-structure constant. Physics treats it as a measured input. TFPT claims it's the unique root of a short equation — fixed by two inputs, and nothing else. Big claim. So I'll also show you exactly where it could break.",
  },
  {
    heading: "The machine (0:15)",
    body: "TFPT isn't another table of nice numbers — it's a discrete compiler. Two operative inputs go in: a boundary constant, c₃ = 1/(8π), and a five-fold carrier, g_car = 5. From those, one structure is built: the carrier makes the D₅ side, four marked boundary points make the A₃ family geometry, and the μ₄ glue closes them into E₈. And this defuses the usual no-go theorems: E₈ is not a gauge group of nature. It's the audit hull — the consistency container. The Standard Model is a readout after projection, not “everything is E₈.”",
  },
  {
    heading: "The readout (0:56)",
    body: "What comes out splits cleanly. First, the discrete core — exact, or machine-checked: three families, hypercharges, the flavor matrix, sixteen carrier states, the recurring 2-3-5, the Coxeter number 30, the 240 roots of E₈. Then the boundary side: from c₃ comes one seed, φ₀ — and from it, the Cabibbo structure, the electromagnetic fixed point, and the scale grammar. The fine-structure constant lands as the unique positive root of a cubic: 137.0359992 — 1.9σ from the measured value. Not a fit. A forced root.",
  },
  {
    heading: "One texture, not free knobs (1:37)",
    body: "The Standard-Model part compresses hard. Masses and mixings don't come from free Yukawa numbers — they come from one texture: a seed, a fixed flavor matrix, integer word-lengths. The CKM angles and the leading CP phase fall out of the same holonomy; the reactor angle θ₁₃ comes straight from the seed. Absolute masses run through one typed bridge, v_geo, and standard RG. Dimensional analysis with a seatbelt.",
  },
  {
    heading: "How to kill it (2:03)",
    body: "Now the honest part — how do you kill it? The predictions were frozen in a blind registry before any comparison — machine-enforced. sin²θ₁₂ ≈ 0.3067. sin²θ₁₃ ≈ 0.0231. α⁻¹ as a fixed point. A small tensor ratio r between 0.0033 and 0.0048. Normal neutrino ordering, with a low mass floor. The closed core predictions sit within about one sigma today — every tension tracked in the open. The near-term kill tests are real: neutrino mass from DESI and CMB-S4, and proton decay at Hyper-Kamiokande.",
  },
  {
    heading: "The audit layer (2:34)",
    body: "How is this kept honest? Every statement carries a status — exact, conditional, open, or kill-test — in one machine-readable ledger: the single source of truth. A no-free-pattern rule on every load-bearing number. And a red team whose job is to break the theory, not confirm it — otherwise math becomes numerology with better typography.",
  },
  {
    heading: "The one open knot (2:53)",
    body: "So what's actually open? The discrete compiler is structurally closed. The one hard knot is a single theorem: the raw, reflection-positive seam state must be — canonically — the holomorphic (E₈)₁ net at τ = i. Both proof routes meet there. The sharpest remaining piece has a name: Flat-Away. Close it, and the structural core is done. What stays are deliberately typed interfaces.",
  },
];

const fmt = (t: number) => `${Math.floor(t / 60)}:${String(t % 60).padStart(2, "0")}`;

const videoJsonLd = {
  "@context": "https://schema.org",
  "@type": "VideoObject",
  name: "TFPT — a 3-minute introduction",
  description:
    "A 3-minute introduction to Topological Fixed-Point Theory (TFPT): two inputs — the seam constant c₃ = 1/(8π) and the carrier g_car = 5 — build a discrete compiler with E₈ as an audit hull, reading off the Standard-Model structure, the fine-structure constant α⁻¹ = 137.0359992, and the scale grammar. Ledger-typed, reproducible and falsifiable, with one open structural theorem (SEAM.EQUIV.01).",
  thumbnailUrl: [`${SITE_URL}${POSTER_SRC}`],
  uploadDate: "2026-06-18",
  duration: "PT3M18S",
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
          title="The 3-minute introduction"
          description="Two inputs in, E₈ as the consistency hull, Standard-Model structure and the constants out — with a ledger, a red team and kill tests. The open core isn't diffuse: it's a single seam-equivalence theorem."
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
              aria-label="TFPT — a 3-minute introduction (English, with subtitles)"
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
                aria-label="Play the 3-minute introduction"
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

"use client";

import { useEffect, useRef, useState } from "react";
import { Play } from "lucide-react";
import { SectionHeader } from "./SectionHeader";
import { cn, SITE_URL } from "@/lib/utils";

const VIDEO_SRC = "/intro/tfpt-intro.mp4";
const POSTER_SRC = "/intro/tfpt-intro-poster.jpeg";
const CAPTIONS_SRC = "/intro/tfpt-intro.en.vtt";

/** Chapter markers — seconds match the video's ten beats (script.ts). */
const CHAPTERS: { t: number; label: string }[] = [
  { t: 0, label: "Is reality compiled?" },
  { t: 20, label: "What comes out" },
  { t: 65, label: "From how little" },
  { t: 95, label: "The proof layer (E₈)" },
  { t: 135, label: "It computes itself" },
  { t: 165, label: "The beauty" },
  { t: 195, label: "Not numerology" },
  { t: 245, label: "Five breakthroughs" },
  { t: 302, label: "Honest gaps" },
  { t: 316, label: "The honest answer" },
];

/**
 * The transcript, grouped by chapter. Mirrored from the video's caption track
 * (captions.json). Rendered as visible (collapsible) text so it is accessible to
 * screen readers and indexable by search/answer engines (the video pixels are
 * not). Keep in sync with /intro/tfpt-intro.en.vtt.
 */
const TRANSCRIPT: { heading: string; body: string }[] = [
  {
    heading: "Is reality compiled? (0:00)",
    body: "A program begins as a few lines of source code — and unfolds into something huge and detailed. Here's an honest question, not a claim: could reality work the same way? Could the rules of our universe be the output of something tiny — compiled, not chosen? Let's look at where that idea leads — and how it could fail.",
  },
  {
    heading: "What comes out (0:20)",
    body: "Start at the end — with what this one idea actually produces. Almost the whole Standard Model — our rulebook for every known particle and force: the forces, why matter comes in three families, the single Higgs, the masses, how they mix. Gravity — Einstein's equation, with its constants fixed instead of assumed. Pieces of cosmology — the early universe, how much ordinary matter there is, dark energy. The strength of light — the famous one over one-thirty-seven — is just one line among many. And twenty-seven concrete, testable predictions. That's the output. The real question: from how much input?",
  },
  {
    heading: "From how little (1:05)",
    body: "Here's the surprising part: almost nothing goes in. Two numbers. A tempo — set by the edge of space. And a width: how many slots the building block has — five. And those two aren't even truly free. Strip it down, and what's left is one small whole-number pattern — and π. A huge, detailed result from a tiny source. That gap — between almost nothing and all of this — is the whole story.",
  },
  {
    heading: "The proof layer — E₈ (1:35)",
    body: "How can two numbers carry that much? Because they don't just get plugged in — they have to pass a test. The parts they build must fit into one rigid mathematical object: E₈. E₈ isn't a force of nature. It's a proof layer — the referee that certifies the pieces fit only one way. Two hundred and forty points, one perfect pattern. If anything were off, nothing would lock. Most possible universes simply don't compile.",
  },
  {
    heading: "It computes itself — the fixed point (2:15)",
    body: "Now turn it around. If the proof closes for only one tempo and one width… then the proof decides them. The inputs are forced by the structure they build. The thing works out its own starting point. The loop closes on itself. That's the fixed point the theory is named after. Not a model you tune until it fits — a structure that has to be what it is.",
  },
  {
    heading: "The beauty (2:45)",
    body: "Once you see it, the elegance is hard to miss. The same small numbers — two, three, five — run through every part, because it's all one object. And it isn't frozen. A simple clock gives the whole thing a single resting state. So the constants aren't dialled in by hand — they're where it settles. Almost no free choices, one connected picture.",
  },
  {
    heading: "Is this just numerology? (3:15)",
    body: "Now the fair objection: small whole numbers that fit reality — isn't that just numerology, like seeing faces in clouds? We took it seriously. Nobody drew this picture top-down. It assembled itself — out of hundreds of small, independent checks, each verified by computer, that slowly clicked into one whole. E₈ proves the pieces can fit. These checks prove we're not fooling ourselves — every load-bearing claim machine-verified twice, with a team tasked to break it. We froze predictions before the data, then ran two hundred thousand random look-alikes. They get at most five right; this gets all thirteen. By luck? Below one in 10³⁰ — effectively zero.",
  },
  {
    heading: "Five breakthroughs (4:05)",
    body: "And it hasn't stopped. Five new results — each machine-checked, each honestly labelled. One. The calculating engine of the deepest route used to be declared. Now it is derived — its key number, sixty-four, is computed three independent ways instead of put in. One global integral stays open. Two. The bridge from timeless Euclidean math back to real, physical time now stands — at the free level: the reflection structure exists, and the little clock returns as a genuine time operator. Three. The seam has a temperature — exactly the black-hole value its founding constant demands. Geometry, anomaly, and now temperature — all from c₃ = 1/(8π). The seam is a miniature horizon. Four. Ten blind tests prove the one remaining input bit cannot be derived — it is a genuine choice. But it is now physically defined — in principle readable by an interferometer. One axiom becomes one measurement. And five — reported just as loudly: the first interacting toy model fails one of our own kill tests. A real threat — and the first constructive filter for the one construction site left.",
  },
  {
    heading: "Honest gaps (5:02)",
    body: "So what's still open? The interacting seam. One global integral. One unit no pure number can give. Every gap labelled — and still killable: neutrino mass, proton decay, dark energy. One clean miss, and it's wrong.",
  },
  {
    heading: "The honest answer (5:16)",
    body: "So — is reality compiled? We still don't know. That's the honest answer. But the version you can test keeps getting sharper — more derived, less declared; every gap marked, every test named. Maybe the constants were never arbitrary. Maybe they simply had to add up.",
  },
];

const fmt = (t: number) => `${Math.floor(t / 60)}:${String(t % 60).padStart(2, "0")}`;

const videoJsonLd = {
  "@context": "https://schema.org",
  "@type": "VideoObject",
  name: "TFPT — Is reality compiled?",
  description:
    "A short film on Topological Fixed-Point Theory (TFPT) built around one honest question: is reality compiled? It opens with the output — almost the whole Standard Model (forces, three generations, one Higgs, the masses and mixings, strong-CP = 0), gravity (Einstein's equation with fixed constants), pieces of cosmology, the fine-structure constant α⁻¹ = 137.0359992 as just one line among many, and 27 testable predictions — including the derived measure chain and the thermal seam — then shows how little goes in: two numbers that reduce to one small whole-number pattern and π. E₈ is the proof layer: the referee (240-root projection) where the parts fit only one way, so the inputs are forced — a fixed point. The same 2·3·5 runs through every part, and a spectral-gap clock settles on one attractor (constants selected, not tuned). On numerology: hundreds of machine-checks assembled the picture bottom-up, verified twice (Wolfram + Lean) with a red team; 13 predictions were frozen before the data and beat 200,000 random look-alikes (≤5/13), odds below 10⁻³⁰. Five machine-checked breakthroughs sharpen the picture; the remaining gaps stay labelled and killable (neutrino mass, proton decay, dark energy). The verdict is humble: we still don't know — but here is a version you can test.",
  thumbnailUrl: [`${SITE_URL}${POSTER_SRC}`],
  uploadDate: "2026-07-23",
  duration: "PT5M30S",
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
      className="relative scroll-mt-20 py-12 sm:py-16"
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
          title="Is reality compiled?"
          description="A short film: the whole Standard Model, gravity and 27 predictions out of almost nothing — why E₈ is the proof layer, how the two inputs fix themselves, the beauty of one connected object, and how we keep it honest rather than numerology."
        />

        <figure className="mt-10">
          <div className="relative overflow-hidden border border-slate-700/50 bg-slate-950/60">
            <video
              ref={ref}
              className="aspect-video w-full"
              controls
              playsInline
              preload="none"
              poster={POSTER_SRC}
              aria-label="TFPT — Is reality compiled? (English, with subtitles)"
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
                aria-label="Play the film — Is reality compiled?"
                className="group absolute inset-0 flex items-center justify-center bg-slate-950/30 transition-colors hover:bg-slate-950/15 focus-visible:outline-none"
              >
                <span className="flex h-20 w-20 items-center justify-center rounded-full border border-blue-400/40 bg-blue-500/20 text-blue-100 ring-1 ring-white/10 transition-transform group-hover:scale-105 group-focus-visible:scale-105">
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
            English captions burned into the picture (silent track); a selectable
            subtitle track and the full transcript below are generated from the
            same source.
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

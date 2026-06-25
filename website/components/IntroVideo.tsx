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
  { t: 15, label: "The machine & E₈" },
  { t: 58, label: "The readout" },
  { t: 102, label: "The clocks" },
  { t: 134, label: "Gravity for free" },
  { t: 160, label: "Not numerology" },
  { t: 204, label: "23 predictions" },
  { t: 244, label: "What's open" },
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
    heading: "The machine & E₈ (0:15)",
    body: "Think of TFPT as a compiler — a machine, not a table of lucky numbers. Two inputs go in: a tempo, c₃ = 1/(8π) — the rate set by the edge of space, and a width, g_car = 5 — how many slots the carrier has. From those, the pieces build themselves: three families of matter, a sixteen-part block that is exactly one full generation, and the hypercharges. Then the key player — E₈. It isn't a force of nature; it's the auditor: the one rulebook where every piece locks together exactly one way, like a perfect crystal. And it closes for only that one tempo and width — so E₈ doesn't accept the inputs, it forces them. The axioms are outputs.",
  },
  {
    heading: "The readout — what comes out (0:58)",
    body: "So what does the machine actually print out? Almost the entire Standard Model — exact and machine-checked: the three forces and their charges, three generations, exactly one Higgs, all nine particle masses on a single ladder, the quark and neutrino mixings, both CP phases, and a built-in reason there's no neutron dipole — strong-CP is exactly zero. The headline: the fine-structure constant is the single positive root of one equation. Not chosen — forced. α⁻¹ = 137.0359992, under two sigma from experiment. Read the same edge as a horizon, and you also get cosmology — and gravity.",
  },
  {
    heading: "The clocks — discrete → dynamic (1:42)",
    body: "But a list of numbers isn't physics yet — what makes it move? Through a clock. Two gears mesh: one of size five, the carrier; one of size six, the families. Together they turn an order-thirty cycle — the same 2 · 3 · 5 that runs through everything. This clock has a gap: it always relaxes toward one single state, and never drifts back. So the constants aren't tuned — they're selected. The machine settles on exactly one attractor (Perron–Frobenius). That's the bridge: from frozen arithmetic to living dynamics.",
  },
  {
    heading: "Gravity comes free (2:14)",
    body: "And that first input hides a gift. c₃ = 1/(8π) is the exact 8π sitting inside Einstein's equation for gravity. Run the same atoms through the heat of a horizon, and the full law of gravity falls out — both constants fixed, even the cosmological constant, set by α. The same 1/(8π) shows up three independent ways. Hard to call that an accident.",
  },
  {
    heading: "Why this isn't numerology (2:40)",
    body: "Small whole numbers raise a fair worry: is this just numerology? So we tried to break it ourselves. Of all the predictions, thirteen were frozen before we ever looked at the data. Then two hundred thousand random look-alike theories. TFPT hits all thirteen; the random ones top out at five. For α alone: of ninety-four thousand variants, exactly one lands in the measured window. And the seven arithmetic “coincidences”? They're one object — the 2 · 3 · 5 of E₈ — seen seven ways, not seven flukes. The odds a look-alike matches the whole scorecard: below ten to the minus thirty. Checked twice — independently in Wolfram and in Lean.",
  },
  {
    heading: "23 predictions · how to kill it (3:24)",
    body: "The machine doesn't just explain — it predicts. Twenty-three falsifiable numbers. Today: nine already match, six are close, none miss, and eight are still waiting for data. sin²θ₁₂ ≈ 0.3067. sin²θ₁₃ ≈ 0.0231. A tiny gravitational-wave ratio. Normal neutrino ordering. The near-term tests are real: neutrino mass from DESI and CMB-S4, proton decay at Hyper-Kamiokande, and the dark-energy equation of state at DESI. Each one is a tripwire. One clean miss, and the theory is wrong.",
  },
  {
    heading: "What is actually open (4:04)",
    body: "So what is actually still open? Not a vague pile — three named, labelled handoffs. One published-theorem step from closing the central seam, the clearly-marked bridges to external physics, and one honest unit — because a theorem says pure numbers can never hand you a kilogram. Zero hidden mechanisms. Two inputs, one compiler — fully audited.",
  },
];

const fmt = (t: number) => `${Math.floor(t / 60)}:${String(t % 60).padStart(2, "0")}`;

const videoJsonLd = {
  "@context": "https://schema.org",
  "@type": "VideoObject",
  name: "TFPT — a 4-minute introduction",
  description:
    "A 4-minute introduction to Topological Fixed-Point Theory (TFPT): two inputs — the tempo c₃ = 1/(8π) and the carrier width g_car = 5 — drive a discrete compiler. E₈ is the auditor: the one rulebook where the pieces lock together exactly one way, so it pins the inputs (the axioms are outputs). The machine reads off almost the entire Standard Model (three forces and charges, three generations, exactly one Higgs, nine masses on one φ₀-ladder, CKM+PMNS, both CP phases, strong-CP = 0), the fine-structure constant α⁻¹ = 137.0359992, cosmology and a parameter-free law of gravity. An order-30 clock with a spectral gap turns the static structure into dynamics with a unique attractor (the constants are selected, not tuned). It makes 23 falsifiable predictions (9 match, 6 near, 0 miss, 8 pending; 13 frozen blind), shows why this isn't numerology (13/13 vs 200,000 random look-alikes ≤5, α unique to 1 in 94,500, the seven arithmetic witnesses are one 2·3·5/E₈ object, odds below 10⁻³⁰, checked in Wolfram and Lean), the near-term kill tests (DESI, CMB-S4, Hyper-K), and an honest residual of three named interfaces with zero hidden mechanisms.",
  thumbnailUrl: [`${SITE_URL}${POSTER_SRC}`],
  uploadDate: "2026-06-25",
  duration: "PT4M36S",
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
          description="Two inputs in; E₈ as the auditor that pins them; almost the whole Standard Model, the constants, the order-30 clocks that make it dynamical, gravity and 23 predictions out — plus why this isn't numerology, the kill tests, and an honest residual of three named interfaces."
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

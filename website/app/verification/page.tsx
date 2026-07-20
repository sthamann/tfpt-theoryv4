import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, Github, TerminalSquare } from "lucide-react";
import { SectionHeader } from "@/components/SectionHeader";
import { VerificationDag } from "@/components/VerificationDag";
import { ScriptIndex } from "@/components/ScriptIndex";
import { GravityEmergence } from "@/components/GravityEmergence";
import { UniversalGapLab } from "@/components/UniversalGapLab";
import { SuiteTimeline } from "@/components/SuiteTimeline";
import { ResidualChain } from "@/components/ResidualChain";
import { SCRIPT_TOTAL } from "@/lib/suite";
import { REPO_URL, SITE_URL } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Verification & Workflow — Every Number Machine-Checked",
  description:
    "How TFPT is verified: an interactive dependency graph showing exactly how each result is computed and on which inputs it depends (including the self-consistency loop), the four-path verification stack (Python suite, independent Wolfram mirror, Lean carrier proof, versioned status ledger), and the full script index linked to GitHub.",
  keywords: [
    "TFPT verification",
    "dependency graph",
    "reproducibility",
    "verification suite",
    "status ledger",
    "Wolfram",
    "Lean proof",
    "self-consistency",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/verification` },
  openGraph: {
    type: "article",
    title: "Verification & Workflow — Every Number Machine-Checked",
    description:
      "An interactive dependency graph of the TFPT compiler closure, the four-path verification stack, and the full script index — all linked to the public repository.",
    url: `${SITE_URL}/verification`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
    authors: ["Stefan Hamann", "Alessandro Rizzo"],
  },
  twitter: {
    card: "summary_large_image",
    title: "Verification & Workflow — TFPT",
    description:
      "Interactive dependency graph + four-path verification stack + full script index.",
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "WebPage",
  name: "TFPT — Verification & Workflow",
  url: `${SITE_URL}/verification`,
  inLanguage: "en",
  description:
    "Interactive dependency graph of the TFPT compiler closure and the full verification stack.",
  sameAs: [REPO_URL],
  isBasedOn: REPO_URL,
};

const authorsJsonLd = [
  { "@type": "Person", name: "Stefan Hamann" },
  { "@type": "Person", name: "Alessandro Rizzo" },
];

const softwareJsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareSourceCode",
  name: "TFPT verification suite",
  description: `${SCRIPT_TOTAL} numbered claim checks (Python), an independent Wolfram mirror, and a Lean 4 carrier-rigidity proof — every load-bearing TFPT result re-derived from the two axioms c₃ = 1/(8π) and g_car = 5.`,
  codeRepository: REPO_URL,
  url: `${SITE_URL}/verification`,
  programmingLanguage: ["Python", "Wolfram Language", "Lean 4"],
  runtimePlatform: "Python 3, Wolfram Engine, Lean 4",
  author: authorsJsonLd,
};

const datasetJsonLd = {
  "@context": "https://schema.org",
  "@type": "Dataset",
  name: "TFPT status ledger & frozen prediction registry",
  description:
    "The versioned status_ledger.csv (single source of truth for every typed claim: id, status, location, dependency, script) and predictions_frozen.json (the blind prediction registry, frozen 2026-06-09).",
  inLanguage: "en",
  url: `${SITE_URL}/verification`,
  isBasedOn: REPO_URL,
  sameAs: [REPO_URL],
  creator: authorsJsonLd,
};

const PATHS: { label: string; value: string; body: string }[] = [
  {
    label: "Python suite",
    value: `${SCRIPT_TOTAL} checks`,
    body: "One file per claim cluster; run_all.py ends ALL CHECKS PASSED. Exact sympy where possible, mpmath/numpy otherwise.",
  },
  {
    label: "Wolfram mirror",
    value: "116/116 + 378/378",
    body: "An independent second path for the exact algebraic / identity / lattice results, on the Wolfram Engine: the verified base file plus the v84+ extension file.",
  },
  {
    label: "Lean carrier",
    value: "0 sorry",
    body: "The P2 carrier algebra — hypercharge, anomaly-freedom, integer rigidity — formalised in Lean 4 with only kernel axioms.",
  },
  {
    label: "Status ledger",
    value: "1 source of truth",
    body: "status_ledger.csv types every claim (id, status, location, dependency, script) and is versioned. If the text and the ledger disagree, the ledger wins.",
  },
];

const MARKERS: { m: string; meaning: string; tone: string }[] = [
  { m: "[E]", meaning: "exact / machine-proven (fine types: identity, lattice/Lie, Lean-formalised, numerical fixed point)", tone: "text-emerald-200 bg-emerald-500/15 ring-emerald-400/30" },
  { m: "[C]", meaning: "conditional — holds under named hypotheses (fine type: physical bridge / readout)", tone: "text-amber-200 bg-amber-500/15 ring-amber-400/30" },
  { m: "[O]", meaning: "open / axiom — declared input or genuine gap", tone: "text-rose-200 bg-rose-500/15 ring-rose-400/30" },
  { m: "[X]", meaning: "falsifiable kill test (committed in advance)", tone: "text-blue-200 bg-blue-500/15 ring-blue-400/30" },
];

const REVIEWER_MAP: { label: string; marker: string; tone: string; items: string[] }[] = [
  {
    label: "Exact kernel",
    marker: "[E]",
    tone: "border-emerald-400/30 bg-emerald-500/5",
    items: [
      "Anchor a = (1,1,2); the E₈ glue D₅⊕A₃+μ₄ ⇒ E₈",
      "Gauge group, 3 families, hypercharge (Lean-formalised)",
      "α⁻¹ = 137.0359992 — unique root of the explicit cubic F_U(1)=0",
      "Flavor operator ladder (Q,K,R,L), quark/lepton ratios",
      "θ_QCD = 0, Higgs uniqueness, the order-30 Coxeter cycle",
    ],
  },
  {
    label: "Conditional physics",
    marker: "[C]",
    tone: "border-amber-400/30 bg-amber-500/5",
    items: [
      "Reflection positivity + gap (Decoupling Theorem, Δ_eff = 1.648)",
      "G_net algebra + AQFT machinery [E]; seam coupling [C] closed modulo cited theorems (v367/v368 + v376–v379, ground-state witnesses v489/v490)",
      "F_transfer: Koide, η_B, axion relic, m_p/m_e — runnable typed solvers (v371–v375)",
      "Scheme layer / QCD + EW matching for absolute masses",
    ],
  },
  {
    label: "Open premises",
    marker: "[O]",
    tone: "border-rose-400/30 bg-rose-500/5",
    items: [
      "P1, P2 — declared inputs, reduced to the anchor a=(1,1,2)+π (not free dials)",
      "v_geo — the one dimensionful scale (metrology primitive, No-Unit Theorem)",
      "SEAM.EQUIV.01 — [C] closed modulo cited theorems (lattice v367/v368 + S3 stack v376–v379, ground-state witnesses v489/v490, Lean FORM.SEAM.MMST.01); the only [O] residual is the cited continuum scaling-limit existence (v336; extension leg on the peer-reviewed crossed-product package, realisation at invariant level, v469; stays [O])",
    ],
  },
  {
    label: "Kill tests",
    marker: "[X]",
    tone: "border-blue-400/30 bg-blue-500/5",
    items: [
      "JUNO: sin²θ₁₂ ≈ 0.3067 (prediction of record, frozen)",
      "CMB tensor-to-scalar r ≈ 0.004 (Starobinsky); n_s vs DESI",
      "Normal neutrino ordering with small m_ββ; θ_eff = 0 (nEDM)",
      "A fourth chiral generation (N_fam ≠ 3) or w ≠ −1 breaks the core",
    ],
  },
];

const REPRODUCE = `# 1. Compile the active document set      ->  "10 ok, 0 failed"
bash build.sh notes

# 2. Run the Python verification suite    ->  "ALL CHECKS PASSED"
cd verification && python run_all.py

# 3. Independent Wolfram path (optional)  ->  "ALL WOLFRAM CHECKS PASSED"
wolframscript -file verification/wolfram/tfpt_readouts.wl

# 4. Lean carrier-rigidity proof (optional) ->  "AUDIT: PASS"
cd experiments/lean4-carrier-rigidity && lake exe cache get && bash scripts/audit.sh

# 5. The sync audit (papers <-> suite <-> ledger <-> website)  ->  "AUDIT OK"
bash build.sh audit

# 6. Regenerate the reproducibility manifests (run last)
python verification/make_manifest.py`;

export default function VerificationPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(softwareJsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(datasetJsonLd) }}
      />

      <section className="relative isolate overflow-hidden pt-12 pb-12 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[500px] w-[1000px] -translate-x-1/2 rounded-full opacity-30 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(16,185,129,0.35), rgba(99,102,241,0.25), transparent)",
          }}
        />
        <div className="relative mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Breadcrumb" className="mb-6">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
            >
              <ArrowLeft size={14} />
              Back to overview
            </Link>
          </nav>
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-500/10 px-4 py-1.5 text-xs font-medium tracking-wider text-emerald-200">
            <span className="uppercase">Verification &amp; workflow</span>
          </span>
          <h1 className="mt-6 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl md:text-6xl">
            Every number is{" "}
            <span className="text-gradient-blue">machine-checked</span>.
          </h1>
          <p className="mt-4 max-w-3xl text-base leading-relaxed text-slate-300 sm:text-lg">
            TFPT is built like a compiler, and verified like one. Nothing is
            marked closed that is not re-derived from the two axioms by an
            independent script, and no dimensionful quantity is claimed as a
            derivation from pure numbers. The graph below shows exactly how each
            result is computed, on which inputs it depends, and which scripts
            check it — including the self-consistency loop that fixes the inputs
            themselves. Every script is{" "}
            <span className="font-semibold text-slate-100">runnable live in your browser</span>{" "}
            — click one to execute the real Python (via Pyodide / WebAssembly)
            and watch the checks pass, step by step.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
            >
              <Github size={16} />
              Open the repository
            </Link>
            <Link
              href="#dag"
              className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
            >
              Jump to the dependency graph
            </Link>
          </div>
        </div>
      </section>

      {/* Four-path stack + markers */}
      <section className="relative py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="The discipline"
            title="Four independent paths, one ledger"
            description="A claim is only as strong as the way it is checked. The dimensionless skeleton is verified three independent ways and typed in a single versioned ledger, so the papers, the suite and the ledger stay in lock-step."
          />
          <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {PATHS.map((p) => (
              <div
                key={p.label}
                className="glass flex flex-col rounded-2xl p-5 ring-1 ring-slate-700/40"
              >
                <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                  {p.label}
                </div>
                <div className="mt-1 font-serif text-2xl font-semibold text-slate-50">
                  {p.value}
                </div>
                <p className="mt-2 text-xs leading-relaxed text-slate-400">
                  {p.body}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-6 flex flex-wrap items-center gap-2 rounded-2xl border border-slate-700/40 bg-slate-950/40 px-5 py-4">
            <span className="mr-1 text-[11px] font-semibold uppercase tracking-widest text-slate-300">
              Status markers
            </span>
            {MARKERS.map((x) => (
              <span
                key={x.m}
                className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[11px] font-medium ring-1 ${x.tone}`}
              >
                <span className="font-mono font-semibold">{x.m}</span>
                {x.meaning}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* External reviewer map: the attack surface at a glance */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="For the external reviewer"
            title="The attack surface, at a glance"
            description={`What is exact, what is conditional, what is an open premise, and how to kill it — so a reviewer can decide where to push without reading ${SCRIPT_TOTAL} scripts first. Nothing here is hidden: the exact kernel stands on its own; the conditional and open layers are explicitly typed.`}
          />
          <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {REVIEWER_MAP.map((box) => (
              <div
                key={box.label}
                className={`flex flex-col rounded-2xl border p-5 ${box.tone}`}
              >
                <div className="flex items-center gap-2">
                  <span className="font-mono text-sm font-semibold text-slate-100">
                    {box.marker}
                  </span>
                  <span className="text-[11px] font-semibold uppercase tracking-widest text-slate-300">
                    {box.label}
                  </span>
                </div>
                <ul className="mt-3 space-y-2">
                  {box.items.map((it) => (
                    <li key={it} className="break-words text-xs leading-relaxed text-slate-300">
                      {it}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <p className="mt-5 text-sm leading-relaxed text-slate-400">
            The honest one-line claim is conditional, not messianic:{" "}
            <span className="text-slate-200">
              a two-input discrete compiler whose algebraic kernel derives the Standard-Model skeleton
              and several dimensionless readouts, with every physical transfer layer explicitly typed
            </span>{" "}
            — and the keystone SEAM.EQUIV.01 (the raw RP seam = the holomorphic (E₈)₁ net at τ=i) is
            closed modulo cited theorems: the target net is pinned at every computable level (lattice
            v367/v368 + S3 stack v376–v379, ground-state witnesses v489/v490) and Lean-pinned (FORM.SEAM.MMST.01) to the published MMST/Adamo
            theorems, so the AQFT closure to (E₈)₁ follows modulo the cited continuum-existence residual
            (v336; extension leg on the peer-reviewed crossed-product package, realisation at invariant
            level, v469; stays [O]); its conformal-deck face QGEO.SYM.01 is a corollary.
          </p>
        </div>
      </section>

      {/* Origin Theory — the translation clock */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Origin Theory · one clock"
            title="The translation clock: discrete ↔ dynamic is 5 × 6"
            description="The bridge between the static (lattice/spectrum) data and the dynamic (recovery/relaxation) data is not a map but a clock — the order-30 Coxeter element — and, because gcd(5,6)=1, it factorizes into two coprime hands: a static carrier ring ℤ/5 = g_car (golden √5, no rate) and a dynamic family ring ℤ/6 = 2·N_fam (the recovery rate (2/3)⁶, exponent 6). The dynamic hand runs 0,1,2,3,4,5 — position 0 is the conserved law (the attractor, rate 0), 1..5 the live phases; the static hand runs 1,2,3,4,5. So '0,1,2,3,4,5' is the law-inclusive reading and '1,2,3,4,5' the live-only reading of the same clock (v319)."
          />
          <figure className="mt-8 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-6">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/figures/translation_clock.png"
              alt="Two concentric clock rings. The outer ring has six ticks labelled 0,1,2,3,4,5 — the dynamic family hand ℤ/6 = 2·N_fam carrying the recovery rate (2/3)^6 (exponent 6); the tick at position 0 is highlighted as the conserved law (rate 0, the attractor). The inner ring has five ticks labelled 1,2,3,4,5 — the static carrier hand ℤ/5 = g_car carrying the golden √5 and no rate. The centre reads ℤ/30 = 5 × 6, the order-30 Coxeter clock."
              className="mx-auto w-full max-w-md rounded-lg bg-white"
            />
            <figcaption className="mt-4 text-sm leading-relaxed text-slate-400">
              The order-30 Coxeter clock as two coprime hands:{" "}
              <span className="text-slate-200">dynamic</span>{" "}
              <span className="font-mono">ℤ/6 = 2·N_fam</span> (0..5, rate{" "}
              <span className="font-mono">(2/3)⁶</span>, position 0 = the law) and{" "}
              <span className="text-slate-200">static</span>{" "}
              <span className="font-mono">ℤ/5 = g_car</span> (1..5, golden{" "}
              <span className="font-mono">√5</span>, no rate). One full turn is{" "}
              <span className="font-mono">lcm(5,6) = 30 = h(E₈)</span> — the arithmetic is [E],
              the &ldquo;the bridge is one clock&rdquo; reading is [C] (v319).
            </figcaption>
          </figure>
        </div>
      </section>

      {/* Universal spectral gap — the animated lab (v383–v391) */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="One principle · animated"
            title="The universal spectral gap — one operator, many sectors"
            description="Every TFPT sector is the same object: a gapped operator with a unique attractor (the physics) and a spectral gap (the reason there is no free parameter). The same gap also sizes each sector's first correction — a typed budget, not a uniform band — and the gap rate is the prime-3 (2/3)⁶ or prime-5 golden facet of the order-30 Coxeter clock. Watch the sectors race to their attractor; the gapless r=1 track never forgets its start (the Lean theorem). Beside it: the entire-form-factor graviton (finite, ghost-free, UV-soft) and the residual matrix that is certification, not construction (v383–v391)."
          />
          <div className="mt-10">
            <UniversalGapLab />
          </div>
        </div>
      </section>

      {/* External cross-check figure (PyR@TE) */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="External cross-check"
            title="The F_transfer running — confirmed by an independent tool"
            description="The renormalization-group running that carries the boundary data to the observables, computed at two loops. The gauge β-functions are reproduced verbatim by the third-party generator PyR@TE 3 (v159); the strong coupling reaches confinement at Λ_QCD ≈ 0.4 GeV (v164); and the Higgs quartic falls to ≈0 with β_λ ≈ 0 at the Planck scale — the free-seam near-criticality that ties the Higgs mass to the boundary fixed point (v166)."
          />
          <figure className="mt-8 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-6">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/figures/rg_running.png"
              alt="Two-panel plot. Left: the inverse gauge couplings versus log10(energy) from the QCD confinement scale to the Planck mass — the U(1) line has slope b1 = 41/10, the strong coupling inverse goes to zero at about 0.4 GeV, and the three couplings do not unify. Right: the Higgs quartic coupling falls from 0.13 at the electroweak scale to about 0.002 near the reduced Planck mass with vanishing beta function — the Standard-Model near-criticality."
              className="mx-auto w-full max-w-4xl rounded-lg bg-white"
            />
            <figcaption className="mt-4 text-sm leading-relaxed text-slate-400">
              Two-loop Standard-Model running. <span className="text-slate-200">Left:</span>{" "}
              gauge couplings — the U(1)<sub>Y</sub> slope is the abelian index{" "}
              <span className="font-mono">b₁ = 41/10</span> (v159), confinement{" "}
              <span className="font-mono">α₃⁻¹ → 0</span> at{" "}
              <span className="font-mono">Λ_QCD ≈ 0.4 GeV</span> (v164), no SM unification.{" "}
              <span className="text-slate-200">Right:</span> the Higgs quartic reaches{" "}
              <span className="font-mono">λ(M̄_Pl) ≈ 0.002</span>,{" "}
              <span className="font-mono">β_λ ≈ 0</span> — the free-seam near-criticality (v166).
            </figcaption>
          </figure>
        </div>
      </section>

      {/* E8 slice compression figure */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Structural compression"
            title="The E₈ audit atlas is one projection of two alphabets"
            description="The seven maximal E₈ slices (each a way of cutting 248) are not seven separate hits: every block is built from just two typed alphabets — the anchor power sums P = (3,4,6,10) and the Sheet-Diamond operator determinants (3,4,8,14,20,32), which sum to 81 = N_fam⁴. The atlas is therefore a closed grammar over admissible invariants, exactly what the No-Free-Pattern discipline demands (v170)."
          />
          <figure className="mt-8 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/40 p-4 sm:p-6">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/figures/slice_compression.png"
              alt="Seven horizontal stacked bars, one per maximal E8 subalgebra (D8, D5xA3, E6xA2, E7xA1, F4xG2, A4xA4, A8), each summing to 248. Blocks are coloured by their alphabet source: blue for anchor power-sum blocks, gold for Sheet-Diamond determinant blocks (which sum to 81 = N_fam^4), green for symmetric or glue blocks."
              className="mx-auto w-full max-w-4xl rounded-lg bg-white"
            />
            <figcaption className="mt-4 text-sm leading-relaxed text-slate-400">
              Each of the seven E₈ slices is one projection of two alphabets —{" "}
              <span className="text-slate-200">blue</span> power-sum blocks{" "}
              <span className="font-mono">P=(3,4,6,10)</span> and{" "}
              <span className="text-slate-200">gold</span> determinant blocks{" "}
              <span className="font-mono">(3,4,8,14,20,32)</span> with{" "}
              <span className="font-mono">Σdet = 81 = N_fam⁴</span>; green = symmetric/glue.
              The full lemma (K₄ edge graph, row-budget cross, dim E₆ = 78 = p₂·Δ) is in
              the E₈-audit paper (v170).
            </figcaption>
          </figure>
        </div>
      </section>

      {/* The journey + the structural residual */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="The journey & what remains"
            title="From two axioms to one geometric premise"
            description={`The verification suite grew in phases — foundations, the Standard-Model readouts, the seam=horizon geometry, the reductions and external cross-checks, the AQFT closure, the icosahedral capstone, the seam-equivalence closing arc and the certification round (${SCRIPT_TOTAL} scripts today). The closure arc drives the whole remaining structural question down, step by machine-checked step, to a target pinned at every computable level — closed modulo a cited published theorem (MMST/Adamo), not solved. Both views below are live HTML, not images: every script chip runs the real Python in your browser.`}
          />
          <div className="mt-8">
            <SuiteTimeline />
          </div>
          <div className="mt-8">
            <ResidualChain />
          </div>
          <p className="mt-5 break-words text-sm leading-relaxed text-slate-400">
            The bedrock is closed modulo cited theorems via the Seam Equivalence Theorem
            (<span className="font-mono">SEAM.EQUIV.01</span>) — the raw RP seam IS the holomorphic (E₈)₁
            net at τ=i (its conformal-deck face <span className="font-mono">QGEO.SYM.01</span> is a
            corollary): the target is pinned at every computable level by an explicit lattice model
            (v367/v368) and the S3 closure stack (v376–v379, ground-state witnesses v489/v490), Lean-pinned (FORM.SEAM.MMST.01) to the
            published MMST/Adamo theorems, leaving [O] = the cited continuum scaling-limit existence only
            (v336; extension leg on the peer-reviewed crossed-product package, realisation at invariant
            level, v469; stays [O]). The emergent-QFT layer (<span className="font-mono">v258–v261</span>,
            the Modular Spectral Closure) collapses onto this <em>same</em> bedrock — the boundary QFT is
            one relative object that adds no new open item — and{" "}
            <span className="font-mono">v_geo</span> stays the one no-unit primitive.
          </p>
          <GravityEmergence />
        </div>
      </section>

      {/* The interactive DAG */}
      <section
        id="dag"
        className="relative scroll-mt-20 border-t border-slate-800/60 py-12 sm:py-16"
      >
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="The dependency graph"
            title="How each result is computed"
            description="Two axioms at the source, the E₈ compiler in the middle, the observables as sinks. Click any node to see what it is, its status marker, its inputs and outputs, how it can fail, and the scripts that machine-check it — then click a script to run it live in your browser. The dashed rose edges are the bootstrap: the E₈ closure feeds back and fixes the inputs."
          />
          <div className="mt-10">
            <VerificationDag />
          </div>
        </div>
      </section>

      {/* Reproduce */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Reproduce it yourself"
            title="Five commands, from the repository root"
            description="Dependencies: a LaTeX distribution, Python 3 with sympy / mpmath / numpy / matplotlib; optionally the Wolfram Engine and Lean 4. Every script cited in run_all.py is also cited inline in the documents, and the status heatmap is generated directly from the ledger."
          />
          <div className="mt-8 overflow-hidden rounded-2xl border border-slate-700/40 bg-slate-950/70">
            <div className="flex items-center gap-2 border-b border-slate-800/60 px-4 py-2.5">
              <TerminalSquare size={14} className="text-slate-400" aria-hidden />
              <span className="font-mono text-[11px] uppercase tracking-widest text-slate-400">
                reproduce / verify
              </span>
            </div>
            <pre className="overflow-x-auto px-5 py-4 text-[12px] leading-relaxed text-slate-200">
              <code className="font-mono">{REPRODUCE}</code>
            </pre>
          </div>
        </div>
      </section>

      {/* Script index */}
      <section className="relative border-t border-slate-800/60 py-12 sm:py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="The script index"
            title="What each script checks"
            description="The full verification suite, grouped by what it proves. Every script links to its source in the public repository."
          />
          <div className="mt-10">
            <ScriptIndex />
          </div>

          <div className="mt-10 flex flex-col items-center gap-3 rounded-2xl border border-blue-400/25 bg-gradient-to-br from-blue-500/10 to-violet-500/5 p-8 text-center">
            <h3 className="font-serif text-xl font-semibold text-slate-50">
              Independent scrutiny is the point
            </h3>
            <p className="max-w-2xl text-sm leading-relaxed text-slate-400">
              These checks are reproducible by anyone — that is what
              &ldquo;independent&rdquo; means here: the same result falls out on
              your machine, on an independent Wolfram path, and (for the carrier)
              in Lean. We do not claim external endorsements; we invite review.
              Open questions and known limitations are tracked openly in the
              research contracts and the status ledger — disagreements go in the
              issue tracker.
            </p>
            <div className="mt-1 flex flex-wrap items-center justify-center gap-3">
              <Link
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105"
              >
                <Github size={16} />
                Source, scripts &amp; ledger
              </Link>
              <Link
                href={`${REPO_URL}/issues`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-full border border-slate-600/60 bg-slate-900/60 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800/80"
              >
                Open an issue / review
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

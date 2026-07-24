import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { SITE_URL } from "@/lib/utils";
import { PRIME_FRONT_SECTIONS } from "@/lib/primeFront";
import { HonestyBanner } from "@/components/primefront/HonestyBanner";
import { DiarySection } from "@/components/primefront/DiarySection";
import { CompilerSchematic } from "@/components/primefront/CompilerSchematic";
import { ShellCensus } from "@/components/primefront/ShellCensus";
import { KillChainTimeline } from "@/components/primefront/KillChainTimeline";
import { PrimeDetector } from "@/components/primefront/PrimeDetector";
import { NeighborStepping } from "@/components/primefront/NeighborStepping";
import { TwoMelodies } from "@/components/primefront/TwoMelodies";
import { CenterAtlas } from "@/components/primefront/CenterAtlas";
import { UpdateFeed } from "@/components/primefront/UpdateFeed";
import { StatusBadge } from "@/components/primefront/StatusBadge";

export const metadata: Metadata = {
  title: "The Prime Front — Research Diary",
  description:
    "A plain-language research diary of TFPT's prime / zeta investigation: signed E8 census, kill-chain honesty, Hecke from geometry (v535), and the open distance to any Hilbert–Pólya carrier. Sandbox unless machine-verified.",
  keywords: [
    "TFPT prime front",
    "E8 census",
    "Hecke from geometry",
    "v535",
    "zeta research diary",
    "Kneser neighbours",
    "Stefan Hamann",
  ],
  alternates: { canonical: `${SITE_URL}/prime-front` },
  openGraph: {
    type: "article",
    title: "The Prime Front — TFPT research diary",
    description:
      "Primes, the E8 census, and one load-bearing result (v535). No claim of progress toward the Riemann Hypothesis.",
    url: `${SITE_URL}/prime-front`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "The Prime Front — TFPT",
    description:
      "Research diary of the prime / zeta line. Machine-verified today: v535 only.",
  },
};

export default function PrimeFrontPage() {
  return (
    <>
      <section className="relative isolate overflow-hidden pt-12 pb-8 sm:pt-16">
        <div aria-hidden className="absolute inset-0 grid-bg pointer-events-none" />
        <div
          aria-hidden
          className="absolute -top-40 left-1/2 -z-10 h-[520px] w-[1000px] -translate-x-1/2 rounded-full opacity-35 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(56,189,248,0.28), rgba(16,185,129,0.12), transparent)",
          }}
        />
        <div className="relative mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <nav aria-label="Breadcrumb" className="mb-6">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
            >
              <ArrowLeft size={14} aria-hidden />
              Back to overview
            </Link>
          </nav>

          <HonestyBanner />

          <p className="mt-8 font-mono text-[11px] uppercase tracking-[0.2em] text-sky-300/90">
            Research diary · Teile 11–40
          </p>
          <h1 className="mt-3 font-serif text-4xl font-semibold leading-tight text-slate-50 sm:text-5xl md:text-6xl">
            The Prime Front
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300 sm:text-lg">
            Primes are the simplest objects with the most complex behaviour.
            This page tells — in ordinary language — how a discrete physics
            compiler&apos;s bookkeeping kept speaking number theory, what
            survived preregistered kills, and what is still honestly open.
          </p>

          <nav
            aria-label="On this page"
            className="mt-8 flex flex-wrap gap-2"
          >
            {PRIME_FRONT_SECTIONS.map((s) => (
              <a
                key={s.id}
                href={`#${s.id}`}
                className="rounded-full border border-slate-700/50 bg-slate-900/40 px-3 py-1 font-mono text-[11px] text-slate-400 transition hover:border-slate-500 hover:text-slate-200"
              >
                {s.label}
              </a>
            ))}
          </nav>
        </div>
      </section>

      {/* 1 — Hook */}
      <DiarySection
        id="hook"
        eyebrow="01 · Hook"
        title="What if the bookkeeping secretly speaks number theory?"
        badge="sandbox"
      >
        <p>
          Prime numbers look elementary: indivisible integers. Their global
          pattern is anything but. The Riemann Hypothesis asks for a precise
          spectral order behind that pattern — and this diary does{" "}
          <em>not</em> claim to approach that hypothesis.
        </p>
        <p>
          TFPT is a discrete compiler: two axioms build an E₈ lattice and read
          off Standard-Model structure. While exploring that lattice&apos;s
          shell census, the suite found classical modular objects — thetas,
          Hecke eigenvalues, Apéry congruences — sitting inside compiler-native
          counts. The question became: which of those links are mechanism, and
          which are beautiful coincidence?
        </p>
        <p className="text-slate-400">
          What follows is the arc from first surprise (Teil 11) through a
          four-stage kill of the “archimedean-from-seam” slogan, to the one
          load-bearing promotion of the series:{" "}
          <Link
            href="/verification"
            className="text-emerald-300 underline decoration-emerald-400/30 underline-offset-2 hover:text-emerald-200"
          >
            v535 — Hecke from geometry
          </Link>
          .
        </p>
      </DiarySection>

      {/* 2 — Compiler */}
      <DiarySection
        id="compiler"
        eyebrow="02 · The compiler in one picture"
        title="Two axioms, one lattice completion"
        badge="sandbox"
        visual={<CompilerSchematic />}
      >
        <p>
          The discrete compiler starts with two numbers only: the seam constant{" "}
          <span className="font-mono text-slate-200">c₃ = 1/(8π)</span> and the
          carrier rank{" "}
          <span className="font-mono text-slate-200">g_car = 5</span>. From
          those, the theory forces a split{" "}
          <span className="font-mono text-slate-200">D₅ ⊕ A₃</span> completed by
          a four-element glue group{" "}
          <span className="font-mono text-slate-200">μ₄</span> to the unique even
          unimodular lattice in eight dimensions —{" "}
          <span className="font-mono text-slate-200">E₈</span>.
        </p>
        <p>
          Everything on this page is about what that lattice&apos;s point counts
          know — and what they do not know — about primes and L-functions.
          Classical theorems stay classical; the TFPT contribution is the
          in-suite mechanics that make those objects appear from frozen
          geometry.
        </p>
      </DiarySection>

      {/* 3 — Signed census */}
      <DiarySection
        id="census"
        eyebrow="03 · First discovery · Teil 11"
        title="The signed census: θ₃² · θ₄⁶ as a tensor factor"
        badge="sandbox"
        visual={<ShellCensus />}
      >
        <p>
          Colour every E₈ shell point by its μ₄ “glue class” (four colours).
          Ordinary counting recovers the classical Eisenstein series{" "}
          <span className="font-mono text-slate-200">
            1 + 240 Σ σ₃(n) qⁿ
          </span>
          . The surprise is the <em>signed</em> difference between opposite
          colours:
        </p>
        <p className="rounded-xl border border-slate-700/40 bg-slate-900/50 px-4 py-3 font-mono text-sm text-sky-200">
          Θ₀ − Θ₂ = θ₃(q)² · θ₄(q)⁶
        </p>
        <p>
          Here θ₃² is the theta series of the Gaussian integers ℤ[i] — the
          classical object whose L-value{" "}
          <span className="font-mono text-slate-200">L(1, χ₄) = π/4</span>{" "}
          produces π. It appears as a literal tensor factor of the
          compiler&apos;s signed glue census (classical Jacobi theta algebra;
          the probe content is the in-suite correlation).
        </p>
        <p>
          Three character channels sit on the same shells:{" "}
          <strong className="font-medium text-slate-200">total</strong> (all
          primes, ζ(s)ζ(s−3)),{" "}
          <strong className="font-medium text-slate-200">signed</strong> (entire
          L-series — the glue character kills the pole), and{" "}
          <strong className="font-medium text-slate-200">spinor</strong>{" "}
          (2-adic).
        </p>
      </DiarySection>

      {/* 4 — Bridges */}
      <DiarySection
        id="bridges"
        eyebrow="04 · Surprise bridges · Teil 12"
        title="The census “knows” the Apéry numbers"
        badge="sandbox"
      >
        <p>
          The cuspidal piece of the signed count is the weight-4 form{" "}
          <span className="font-mono text-slate-200">
            f₈ = η(2τ)⁴ η(4τ)⁴
          </span>{" "}
          — classically the Beukers / Ahlgren–Ono form tied to Apéry&apos;s
          proof that ζ(3) is irrational. For every odd prime p ≤ 97 the probe
          checks{" "}
          <span className="font-mono text-slate-200">
            A((p−1)/2) ≡ a_p mod p²
          </span>
          . Via Teil 11, the signed E₈ count at odd prime shells satisfies the
          same congruence. Placebos on nearby eta products fail.
        </p>
        <p className="text-slate-400">
          Beautiful, form-specific, and still sandbox: a correlation inside the
          suite, not a new proof of irrationality.
        </p>
      </DiarySection>

      {/* 5 — Kill chain */}
      <DiarySection
        id="kill-chain"
        eyebrow="05 · Honesty as a method · Teile 14, 19–25"
        title="The kill chain — presented as a feature"
        badge="sandbox"
        visual={<KillChainTimeline />}
      >
        <p>
          An early slogan said the seam&apos;s measured angle 2π was “the
          self-dual temperature.” Teil 14{" "}
          <strong className="font-medium text-rose-200">deflated</strong> that:
          the steps parameter is compiler-specific; the angle is universal
          Bisognano–Wichmann / Unruh conversion.
        </p>
        <p>
          Then the whole “archimedean term from the seam” route was killed in
          four preregistered stages: mode density → interval cut → dictionary →
          scattering phase. Lesson, typed and kept: the seam is a discrete μ₄
          clock, not a hidden Gamma factor. The archimedean piece of the
          explicit formula is treated as a classical externum for recovery
          work.
        </p>
        <p className="text-slate-400">
          Killing your own favourite story on purpose is the method. Null
          results are first-class outcomes.
        </p>
      </DiarySection>

      {/* 6 — Predict */}
      <DiarySection
        id="predict"
        eyebrow="06 · Can it predict primes? · Teil 21"
        title="Three honest channels — and one missing operator"
        badge="sandbox"
        visual={<PrimeDetector />}
      >
        <p>
          <strong className="font-medium text-slate-200">(a) Exact geometric
          primality.</strong>{" "}
          n&gt;1 is prime if and only if the E₈ shell at norm 2n has exactly{" "}
          <span className="font-mono text-slate-200">240(1+n³)</span> vectors —
          the classical σ₃ criterion, checked with zero false
          positives/negatives to 10⁴.
        </p>
        <p>
          <strong className="font-medium text-slate-200">(b) Per-prime
          properties.</strong>{" "}
          Glue characters predict arithmetic type: χ₄-fibre ⟺ p = a²+b²
          (100% for p&lt;1000 in the probe). The compiler says what a prime
          does, not where the next one sits.
        </p>
        <p>
          <strong className="font-medium text-slate-200">(c) Positional
          prediction</strong>{" "}
          needs the zero spectrum. Measured budget:{" "}
          <span className="font-mono text-slate-200">x_max ≈ 0.31 · T</span>.
          That Hilbert–Pólya operator does not exist in the suite — stated
          honestly, not as a near miss.
        </p>
      </DiarySection>

      {/* 7 — Hecke */}
      <DiarySection
        id="hecke"
        eyebrow="07 · The mechanism · Teile 27–32 · v535"
        title="Hecke from geometry — the one load-bearing result"
        badge="machine-verified"
        visual={<NeighborStepping />}
      >
        <p>
          Kneser p-neighbours — isotropic lines in E₈/pE₈ — carry the Hecke
          structure of the census. The count of lines is{" "}
          <span className="font-mono text-slate-200">σ₃(p) · #P³(𝔽_p)</span>{" "}
          (enumerated at p = 2, 3, 5, 7: 135 / 1120 / 19656 / 137600).
        </p>
        <p>
          The frozen marked neighbour-sum operator is an affine Hecke element{" "}
          <span className="font-mono text-slate-200">
            ν_p = a · Id + b · T_p
          </span>{" "}
          with <span className="font-mono text-slate-200">b = σ₃(p) + a_p</span>
          . Prime fingerprints fall out of geometry:{" "}
          <span className="font-mono text-emerald-300">
            a₃ = −4, a₅ = −2, a₇ = 24
          </span>
          . Census redundancy is purely 2-adic oldform structure (dim 7 = 5+2);
          recovery is newform projection.
        </p>
        <p>
          Promoted as{" "}
          <span className="font-mono text-emerald-300">
            verification/v535_hecke_from_geometry.py
          </span>{" "}
          (HECKE.GEOM.01, 25/25, AUDIT OK). Classical theorems (Kneser, Hecke,
          Atkin–Lehner, multiplicity one) are classical; the claim is the
          in-suite mechanics. No RH statement. Weight-4 → GL(1) stays open.
        </p>
      </DiarySection>

      {/* 8 — Eichler */}
      <DiarySection
        id="eichler"
        eyebrow="08 · The Eichler layer · Teile 33, 36"
        title="Smooth background + coherent interference"
        badge="sandbox"
        visual={<TwoMelodies />}
      >
        <p>
          Once the neighbour operator is frozen, the geometric count splits as
          an elementary Witt piece plus{" "}
          <span className="font-mono text-slate-200">exactly a_p²</span> — like
          a smooth melody with a coherent flicker on top. Two-sided
          confirmation (mod-p geometry on one side, eta-product on the other)
          holds at p ≤ 5; closed forms extend the identity to p ≤ 100.
        </p>
        <p className="text-slate-400">
          Still sandbox hardening around the promoted core — not a second
          ledger upgrade by itself.
        </p>
      </DiarySection>

      {/* 9 — Weight drop */}
      <DiarySection
        id="weight-drop"
        eyebrow="09 · Two-channel weight drop · Teile 35, 39"
        title="Abelian channel closed; cuspidal channel remains"
        badge="sandbox"
        visual={<CenterAtlas />}
      >
        <p>
          Rankin–Selberg translates{" "}
          <em>only</em> the abelian shadow into GL(1) products of{" "}
          <span className="font-mono text-slate-200">{"{1, χ₄}"}</span>. The
          centre atlas shows the ξ-line (centre 1/2) is reached exactly by
          weight ≤ 1 theta factors: Mellin(θ₃) → ζ(2s) and{" "}
          <span className="font-mono text-slate-200">
            ζ_ℚ(i) = ζ(s) L(s, χ₄)
          </span>
          . That abelian weight drop is factorisation + Mellin — typed closed.
        </p>
        <p>
          The cuspidal channel — where the{" "}
          <span className="font-mono text-slate-200">a_p</span> live — still
          sits at centre 2 and needs its own bridge. Possessing ζ as a{" "}
          <em>function</em> is not possessing its zeros as a{" "}
          <em>spectrum</em>.
        </p>
      </DiarySection>

      {/* 10 — Stage 4 */}
      <DiarySection
        id="stage-4"
        eyebrow="10 · Stage-4 map · Teil 40"
        title="Two-point spectrum; infinitely many still missing"
        badge="sandbox"
      >
        <p>
          Today&apos;s operator algebra on the census forms is commutative with
          a <em>two-point</em> Gelfand spectrum (the σ₃-system and the a_p-system,
          with oldform copies). A Hilbert–Pólya carrier would need an unbounded
          / non-commutative operator with infinitely many eigenvalues.
        </p>
        <p>
          Only two candidate classes remain inside the suite&apos;s vocabulary:
          seam modular flow, and adelic Bost–Connes-style completion. Each has
          preregistered kills. Distance to the Riemann Hypothesis — stated
          without theatre — is large.
        </p>
        <p className="rounded-xl border border-slate-700/40 bg-slate-900/40 px-4 py-3 text-sm text-slate-400">
          Verdict of the terrain map:{" "}
          <span className="font-mono text-slate-200">TERRAIN-MAPPED</span>.
          Cartography, not a proof attempt.
        </p>
      </DiarySection>

      {/* 11 — Meaning */}
      <DiarySection
        id="meaning"
        eyebrow="11 · What would it mean"
        title="Four calibrated levels — with caveats"
        badge="sandbox"
      >
        <ol className="space-y-3">
          <MeaningLevel
            level="Done"
            badge="machine-verified"
            title="Mechanism"
            body="Hecke structure of the census is lattice-native (v535). Prime fingerprints a_p can be read from a frozen neighbour operator."
          />
          <MeaningLevel
            level="Near"
            badge="sandbox"
            title="Signed / scalable cusp + cuspidal bridge"
            body="Independent evaluators that see signed a_p at scale, and a translation of the centre-2 cuspidal sector — Teile 37–38 are running."
          />
          <MeaningLevel
            level="Big if"
            badge="sandbox"
            title="A genuinely new functor"
            body="A compiler functor that is Hecke-translating, Euler-preserving, and ξ-carrying without smuggling ζ from outside. Kills are preregistered; classical named pieces stay classical."
          />
          <MeaningLevel
            level="Dream"
            badge="sandbox"
            title="Riemann Hypothesis"
            body="Not claimed. Not evidenced. Crypto unaffected. No magic prime oracle — positional prediction still requires a spectrum nobody has built here."
          />
        </ol>
      </DiarySection>

      {/* 12 — Live updates */}
      <section
        id="updates"
        aria-labelledby="updates-heading"
        className="scroll-mt-24 border-t border-slate-800/60 py-12 sm:py-16"
      >
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-slate-500">
              12 · Live updates
            </span>
            <StatusBadge badge="sandbox" />
          </div>
          <h2
            id="updates-heading"
            className="mt-3 font-serif text-2xl font-semibold text-slate-50 sm:text-3xl md:text-4xl"
          >
            Feed — one entry per completed agent run
          </h2>
          <div className="mt-8">
            <UpdateFeed />
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-800/60 py-10">
        <div className="mx-auto max-w-5xl px-4 text-sm text-slate-500 sm:px-6 lg:px-8">
          Numbers and verdicts are taken from{" "}
          <code className="font-mono text-slate-400">experiments/next.txt</code>{" "}
          (2026-07-23/24 diary) and{" "}
          <code className="font-mono text-slate-400">
            verification/v535_hecke_from_geometry.py
          </code>
          . Exploratory probes live under{" "}
          <code className="font-mono text-slate-400">
            experiments/tfpt-discovery/
          </code>
          .
        </div>
      </footer>
    </>
  );
}

function MeaningLevel({
  level,
  badge,
  title,
  body,
}: {
  level: string;
  badge: "sandbox" | "machine-verified";
  title: string;
  body: string;
}) {
  return (
    <li className="rounded-2xl border border-slate-700/45 bg-slate-950/40 p-4">
      <div className="flex flex-wrap items-center gap-2">
        <span className="font-mono text-[10px] uppercase tracking-widest text-slate-500">
          {level}
        </span>
        <StatusBadge badge={badge} />
      </div>
      <h3 className="mt-1 font-serif text-lg text-slate-100">{title}</h3>
      <p className="mt-1 text-sm leading-relaxed text-slate-400">{body}</p>
    </li>
  );
}

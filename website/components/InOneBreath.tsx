import { SectionHeader } from "./SectionHeader";

const LINES: { plain: string; technical?: string }[] = [
  {
    plain: "Two small inputs set the rules of a discrete compiler.",
    technical: "axioms",
  },
  {
    plain:
      "The compiler assembles a rigid mathematical shell that only closes one way.",
    technical: "E₈ audit hull",
  },
  {
    plain:
      "From that shell it reads off the Standard-Model skeleton — forces, three families, hypercharge — and a board of concrete predictions.",
  },
  {
    plain:
      "Every load-bearing step is machine-checked; what is still open or failed is published, not buried.",
  },
];

/**
 * Four-line plain-English mechanism — no μ₄ / seam jargon in the lead sentence.
 * Technical terms appear in parentheses after the everyday reading.
 */
export function InOneBreath() {
  return (
    <section
      id="in-one-breath"
      className="relative scroll-mt-20 border-t border-slate-800/60 py-14 sm:py-16"
      aria-labelledby="in-one-breath-heading"
    >
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          id="in-one-breath-heading"
          eyebrow="Mechanism"
          title="In one breath"
          description="The whole story in four lines — everyday language first, jargon only in parentheses."
        />
        <ol className="mt-8 space-y-0 border border-slate-700/50 bg-slate-950/50">
          {LINES.map((line, i) => (
            <li
              key={line.plain}
              className="flex gap-3 border-b border-slate-800/70 px-4 py-3.5 last:border-b-0 sm:gap-4 sm:px-5"
            >
              <span className="mt-0.5 font-mono text-[11px] font-semibold text-slate-500">
                {String(i + 1).padStart(2, "0")}
              </span>
              <p className="text-sm leading-relaxed text-slate-200 sm:text-[15px]">
                {line.plain}
                {line.technical ? (
                  <span className="text-slate-500">
                    {" "}
                    ({line.technical})
                  </span>
                ) : null}
              </p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

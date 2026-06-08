"use client";

import { papers } from "@/lib/papers";
import { PaperSection } from "./PaperSection";
import { CarrierVisualization } from "./CarrierVisualization";
import { AlphaVisualization } from "./AlphaVisualization";
import { SectionHeader } from "./SectionHeader";

export function PapersSection() {
  return (
    <section
      id="papers"
      className="relative scroll-mt-20 py-12 sm:py-16"
      aria-labelledby="papers-heading"
    >
      <div className="mx-auto max-w-7xl px-4 pb-12 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="The document set"
          title="8 documents: 1 reading guide, 4 core papers, 3 companions"
          description="Doc 0 is the reading guide (introduction). Docs 1–4 are the core papers — architecture & E₈, the Standard Model, the E₈ audit & bootstrap, the honest frontier. Docs 5–7 are the companions — Appendix H (horizon unit system), the Origin Theory synthesis, and the research contracts. Each opens with its inputs, contribution, what it does not claim, and its falsification surface."
        />
      </div>

      {papers
        .filter((p) => p.number > 0)
        .map((p) => (
          <div key={p.id}>
            <PaperSection paper={p} />
            {p.number === 1 && (
              <div className="mx-auto mb-16 max-w-7xl px-4 sm:px-6 lg:px-8">
                <AlphaVisualization />
              </div>
            )}
            {p.number === 2 && (
              <div className="mx-auto mb-16 max-w-7xl px-4 sm:px-6 lg:px-8">
                <CarrierVisualization />
              </div>
            )}
          </div>
        ))}
    </section>
  );
}

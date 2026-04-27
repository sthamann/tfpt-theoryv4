"use client";

import { papers } from "@/lib/papers";
import { PaperSection } from "./PaperSection";
import { CarrierVisualization } from "./CarrierVisualization";
import { AlphaVisualization } from "./AlphaVisualization";
import { TransportPole } from "./TransportPole";
import { CosmologyTimeline } from "./CosmologyTimeline";
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
          eyebrow="The paper series"
          title="Six papers, one staged proof"
          description="The TFPT 4.5 series is split by burden of proof. Each paper isolates one type of scrutiny — primitive kernel, carrier theorem, precision readout, conditional QFT closure, dimensionless metrology, and downstream cosmology — with explicit inputs, contributions, exclusions, and falsification surface."
        />
      </div>

      {papers
        .filter((p) => p.number > 0)
        .map((p) => (
          <div key={p.id}>
            <PaperSection paper={p} />
            {p.number === 2 && (
              <div className="mx-auto mb-16 max-w-7xl px-4 sm:px-6 lg:px-8">
                <CarrierVisualization />
              </div>
            )}
            {p.number === 3 && (
              <div className="mx-auto mb-16 max-w-7xl space-y-8 px-4 sm:px-6 lg:px-8">
                <AlphaVisualization />
                <TransportPole />
              </div>
            )}
            {p.number === 6 && (
              <div className="mx-auto mb-16 max-w-7xl px-4 sm:px-6 lg:px-8">
                <CosmologyTimeline />
              </div>
            )}
          </div>
        ))}
    </section>
  );
}

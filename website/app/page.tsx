import { Hero } from "@/components/Hero";
import { IntroVideo } from "@/components/IntroVideo";
import { TrustContract } from "@/components/TrustContract";
import { ClaimStack } from "@/components/ClaimStack";
import { Safeguards } from "@/components/Safeguards";
import { WhyThisMatters } from "@/components/WhyThisMatters";
import { Overview } from "@/components/Overview";
import { RosettaLexicon } from "@/components/RosettaLexicon";
import { OpenGates } from "@/components/OpenGates";
import { ReconstructionChain } from "@/components/ReconstructionChain";
import { HorizonStory } from "@/components/HorizonStory";
import { GravityEmergence } from "@/components/GravityEmergence";
import { ThermalSeamLegs } from "@/components/ThermalSeamLegs";
import { SectionHeader } from "@/components/SectionHeader";
import { PapersSection } from "@/components/PapersSection";
import { PredictionsSection } from "@/components/PredictionsSection";
import { EcosystemSection } from "@/components/EcosystemSection";
import { DownloadsSection } from "@/components/DownloadsSection";

export default function HomePage() {
  return (
    <>
      {/* Narrative arc: hook -> mechanism -> honesty discipline -> typed details
          -> translation -> what's open -> the dependency DAG -> the seam=horizon
          story -> gravity falls out parameter-free -> papers / predictions ->
          where the structure travels (adjacent projects) -> downloads. The
          motivation (WhyThisMatters) leads, so the fascination
          lands before the trust apparatus; the status discipline (TrustContract,
          ClaimStack) follows immediately to keep skeptical readers. */}
      <Hero />
      <IntroVideo />
      <WhyThisMatters />
      <Overview />
      <TrustContract />
      <ClaimStack />
      <Safeguards />
      <RosettaLexicon />
      <OpenGates />
      <ReconstructionChain />
      <HorizonStory />
      <section
        id="gravity"
        aria-labelledby="gravity-heading"
        className="relative border-t border-slate-800/60 py-16 sm:py-20"
      >
        <div className="mx-auto max-w-5xl px-4 sm:px-6">
          <SectionHeader
            id="gravity-heading"
            eyebrow="Gravity, parameter-free"
            title="The Einstein equation falls out — with no free dial"
            description="The entanglement first law, run with TFPT's atoms, gives the full covariant Einstein equation Gₐᵦ + Λgₐᵦ = c₃⁻¹Tₐᵦ; the seam constant c₃ arrives by three independent routes that all agree — and its temperature leg is now measured on the seam itself (T_seam = 4c₃, v526)."
          />
          <GravityEmergence />
          <ThermalSeamLegs />
        </div>
      </section>
      <PapersSection />
      <PredictionsSection />
      <EcosystemSection />
      <DownloadsSection />
    </>
  );
}

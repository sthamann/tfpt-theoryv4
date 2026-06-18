import { Hero } from "@/components/Hero";
import { TrustContract } from "@/components/TrustContract";
import { ClaimStack } from "@/components/ClaimStack";
import { WhyThisMatters } from "@/components/WhyThisMatters";
import { Overview } from "@/components/Overview";
import { RosettaLexicon } from "@/components/RosettaLexicon";
import { OpenGates } from "@/components/OpenGates";
import { ReconstructionChain } from "@/components/ReconstructionChain";
import { HorizonStory } from "@/components/HorizonStory";
import { PapersSection } from "@/components/PapersSection";
import { PredictionsSection } from "@/components/PredictionsSection";
import { DownloadsSection } from "@/components/DownloadsSection";

export default function HomePage() {
  return (
    <>
      {/* Narrative arc: hook -> mechanism -> honesty discipline -> typed details
          -> translation -> what's open -> the dependency DAG -> a gravity test
          -> papers / predictions / downloads. The motivation (WhyThisMatters)
          leads, so the fascination lands before the trust apparatus; the status
          discipline (TrustContract, ClaimStack) follows immediately to keep
          skeptical readers. */}
      <Hero />
      <WhyThisMatters />
      <Overview />
      <TrustContract />
      <ClaimStack />
      <RosettaLexicon />
      <OpenGates />
      <ReconstructionChain />
      <HorizonStory />
      <PapersSection />
      <PredictionsSection />
      <DownloadsSection />
    </>
  );
}

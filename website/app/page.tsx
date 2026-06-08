import { Hero } from "@/components/Hero";
import { TrustContract } from "@/components/TrustContract";
import { Overview } from "@/components/Overview";
import { OpenGates } from "@/components/OpenGates";
import { ReconstructionChain } from "@/components/ReconstructionChain";
import { PapersSection } from "@/components/PapersSection";
import { PredictionsSection } from "@/components/PredictionsSection";
import { DownloadsSection } from "@/components/DownloadsSection";

export default function HomePage() {
  return (
    <>
      <Hero />
      <TrustContract />
      <Overview />
      <OpenGates />
      <ReconstructionChain />
      <PapersSection />
      <PredictionsSection />
      <DownloadsSection />
    </>
  );
}

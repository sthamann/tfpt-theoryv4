import { Hero } from "@/components/Hero";
import { Overview } from "@/components/Overview";
import { ReconstructionChain } from "@/components/ReconstructionChain";
import { PapersSection } from "@/components/PapersSection";
import { PredictionsSection } from "@/components/PredictionsSection";
import { DownloadsSection } from "@/components/DownloadsSection";

export default function HomePage() {
  return (
    <>
      <Hero />
      <Overview />
      <ReconstructionChain />
      <PapersSection />
      <PredictionsSection />
      <DownloadsSection />
    </>
  );
}

import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { ReconstructionChain } from "@/components/ReconstructionChain";
import { HorizonStory } from "@/components/HorizonStory";
import { GravityEmergence } from "@/components/GravityEmergence";
import { ThermalSeamLegs } from "@/components/ThermalSeamLegs";
import { SectionHeader } from "@/components/SectionHeader";
import { SITE_URL } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Architecture — Compiler Pipeline, Horizon & Gravity",
  description:
    "The TFPT compiler pipeline (reconstruction chain), the seam=horizon story, and the parameter-free gravity emergence — narrative architecture pages moved off the homepage archive.",
  alternates: { canonical: `${SITE_URL}/architecture` },
  openGraph: {
    type: "website",
    title: "Architecture — TFPT",
    description:
      "Compiler pipeline, seam=horizon story, and parameter-free gravity emergence.",
    url: `${SITE_URL}/architecture`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
  },
};

export default function ArchitecturePage() {
  return (
    <>
      <div className="mx-auto max-w-5xl px-4 pt-10 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
        >
          <ArrowLeft size={14} aria-hidden />
          Back to start
        </Link>
        <div className="mt-6 mb-4">
          <SectionHeader
            eyebrow="Architecture"
            title="How the pieces lock"
            description="The dependency chain from two axioms to the Standard-Model skeleton, the seam=horizon identification, and the parameter-free Einstein equation — archived here so the homepage stays a narrative, not a museum."
          />
        </div>
      </div>
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
    </>
  );
}

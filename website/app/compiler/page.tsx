import type { Metadata } from "next";
import { ExternalLink } from "lucide-react";
import { SITE_URL } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Compiler in Action — Watch Two Numbers Build the Standard Model",
  description:
    "An interactive walkthrough of the TFPT compiler: from one boundary edge — the seam constant c₃ = 1/(8π) and the carrier rank g_car = 5 — E₈ validates the closure and the machine reads off the Standard Model, the constants (α⁻¹ = 137.0359992), the flavor sector and 23 falsifiable predictions. Turn the dials and watch every universe but ours fail to close.",
  keywords: [
    "TFPT compiler",
    "interactive Standard Model",
    "E8 audit hull",
    "c3 = 1/(8π)",
    "g_car = 5",
    "fine-structure constant 137",
    "ablation console",
    "TFPT machine",
    "Stefan Hamann",
    "Alessandro Rizzo",
  ],
  alternates: { canonical: `${SITE_URL}/compiler` },
  openGraph: {
    type: "website",
    title: "The Compiler in Action — TFPT",
    description:
      "Interactive: two numbers (c₃ = 1/(8π), g_car = 5) compile the Standard Model, the constants and 23 predictions. E₈ validates the closure; turn the dials and only the audited universe survives.",
    url: `${SITE_URL}/compiler`,
    siteName: "TFPT — Topological Fixed-Point Theory",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "The Compiler in Action — TFPT",
    description:
      "Watch two numbers build the Standard Model. Interactive E₈ compiler with a live ablation console.",
  },
};

export default function CompilerPage() {
  return (
    <section className="flex h-[calc(100vh-4rem)] flex-col">
      <div className="flex shrink-0 items-center justify-between gap-4 border-b border-slate-800/60 bg-slate-950/40 px-4 py-2.5 sm:px-6">
        <div className="min-w-0">
          <h1 className="truncate font-serif text-base font-semibold text-slate-100 sm:text-lg">
            The Compiler in Action
          </h1>
          <p className="truncate text-xs text-slate-400">
            Two numbers — <span className="font-mono text-slate-300">c₃ = 1/(8π)</span> and{" "}
            <span className="font-mono text-slate-300">g_car = 5</span> — compile the Standard
            Model, the constants and 23 predictions.{" "}
            <span className="hidden sm:inline">Click any part of the machine to inspect it.</span>
          </p>
        </div>
        <a
          href="/compiler/index.html?v=2"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-slate-700/60 bg-white/5 px-3 py-1.5 text-xs font-medium text-slate-200 transition-colors hover:bg-white/10 hover:text-white"
        >
          <ExternalLink size={13} aria-hidden />
          Full screen
        </a>
      </div>
      <iframe
        src="/compiler/index.html?v=2"
        title="TFPT Machine — the compiler in action: from one edge to the Standard Model"
        loading="lazy"
        className="w-full flex-1 border-0 bg-[#080c18]"
      />
    </section>
  );
}

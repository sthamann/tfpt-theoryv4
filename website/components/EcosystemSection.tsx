"use client";

import { motion } from "motion/react";
import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { SectionHeader } from "./SectionHeader";

interface EcosystemProject {
  name: string;
  href: string;
  domain: string;
  image: string;
  /** Descriptive alt text for the landing-page screenshot. */
  imageAlt: string;
  eyebrow: string;
  body: string;
  tags: string[];
}

/**
 * Adjacent projects that reuse TFPT's *structure* — deliberately not presented as
 * evidence for the physics. Field AI states it "takes the structure, not the
 * physics predictions"; Agentic Commerce is the co-author's applied research
 * track that lists TFPT and Field AI as its theoretical work. Every claim here is
 * grounded in the linked sites' own wording.
 */
const PROJECTS: EcosystemProject[] = [
  {
    name: "Field AI",
    href: "https://www.hylaean.ai/",
    domain: "hylaean.ai",
    image: "/ecosystem/hylaean.png",
    imageAlt:
      "Field AI landing page (hylaean.ai): the headline “Intelligence that grows like a landscape — not a lookup table” over a dark field visualization.",
    eyebrow: "Architecture · field-native intelligence",
    body: "A research architecture that treats intelligence as physics: knowledge is geometry (a valley / attractor), a question is a boundary condition, and the answer is the field relaxing into a single equilibrium. It explicitly builds on TFPT's structure and vocabulary — a field on a carrier, twist (K) and binding (L) operators, transport (T) between positions, and a spectral gap that guarantees one attractor — while taking the structure, not the physics predictions.",
    tags: ["Field on a carrier", "K · L · T operators", "Spectral-gap attractor"],
  },
  {
    name: "Agentic Commerce",
    href: "https://agentic-commerce.sh/",
    domain: "agentic-commerce.sh",
    image: "/ecosystem/agentic-commerce.png",
    imageAlt:
      "Agentic Commerce landing page (agentic-commerce.sh): the headline “Agentic Commerce” with the line that commerce is executed by intelligent agents acting on human intent.",
    eyebrow: "Applied · agent-driven commerce",
    body: "Stefan Hamann's (TFPT co-author, CEO of Shopware) work on the shift to agent-driven commerce — where intent becomes machine-readable and AI agents discover, negotiate and transact on behalf of people. Its “experimental work” research track sits explicitly alongside TFPT and Field AI, connecting the compiler's structural ideas to emergent intelligence and autonomous systems.",
    tags: ["Emergent intelligence", "Systems thinking", "Open agent protocols"],
  },
];

export function EcosystemSection() {
  return (
    <section
      id="ecosystem"
      className="relative scroll-mt-20 border-t border-slate-800/60 py-20 sm:py-24"
      aria-labelledby="ecosystem-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          id="ecosystem-heading"
          eyebrow="Where the structure travels"
          title="The same structure, applied beyond physics"
          description="TFPT's core objects — a field on a carrier, twist and binding operators, transport, and a spectral gap that forces a single attractor — also seed adjacent research. These are independent, author-adjacent projects that reuse the structure and vocabulary; they are not evidence for the physics claims on this site."
        />

        <div className="mt-12 grid gap-6 lg:grid-cols-2">
          {PROJECTS.map((p, i) => (
            <motion.article
              key={p.name}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.1 }}
              transition={{ duration: 0.5, delay: i * 0.08 }}
              className="group glass flex flex-col overflow-hidden rounded-2xl ring-1 ring-slate-700/40 transition-all hover:ring-blue-400/50"
            >
              <Link
                href={p.href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`Open ${p.name} (${p.domain}) in a new tab`}
                className="relative block overflow-hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400/60"
              >
                <Image
                  src={p.image}
                  width={1600}
                  height={1000}
                  alt={p.imageAlt}
                  sizes="(max-width: 1024px) 100vw, 50vw"
                  className="aspect-[16/10] w-full object-cover object-top transition-transform duration-500 group-hover:scale-[1.03]"
                />
                <div
                  className="pointer-events-none absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent"
                  aria-hidden
                />
                <span className="absolute left-3 top-3 inline-flex items-center gap-1.5 rounded-full border border-slate-600/40 bg-slate-950/70 px-2.5 py-1 font-mono text-[10px] font-medium tracking-wide text-slate-300 backdrop-blur">
                  {p.domain}
                </span>
              </Link>

              <div className="flex flex-1 flex-col p-5 sm:p-6">
                <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
                  {p.eyebrow}
                </span>
                <h3 className="mt-2 font-serif text-xl font-semibold text-slate-50">
                  {p.name}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-400">
                  {p.body}
                </p>

                <div className="mt-4 flex flex-wrap gap-2">
                  {p.tags.map((t) => (
                    <span
                      key={t}
                      className="rounded-full border border-slate-700/40 bg-slate-900/50 px-3 py-1 text-[11px] font-medium text-slate-300"
                    >
                      {t}
                    </span>
                  ))}
                </div>

                <Link
                  href={p.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-5 inline-flex items-center gap-1.5 self-start text-sm font-semibold text-blue-300 transition-colors hover:text-blue-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400/60 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950"
                >
                  Visit {p.domain}
                  <ArrowUpRight size={15} aria-hidden />
                </Link>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}

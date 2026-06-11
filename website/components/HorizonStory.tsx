"use client";

import { motion } from "motion/react";
import { Math } from "./Math";
import { SectionHeader } from "./SectionHeader";

/**
 * HorizonStory — a plain-language visual of the v101/v102 result:
 * put a black hole inside the de Sitter bulk; at the maximal (Nariai)
 * size the horizon roots form the anchor pattern (1,1,−2), the entropy
 * bound is exactly the Koide branch value 2/3, and the dynamics in both
 * sectors flows away from the anchor configuration (stationary repeller).
 * Everything shown is machine-checked in v101_horizon_anchor.py and
 * v102_seam_orientation.py; the carrier-in-the-bulk reading is typed [P].
 */

function BulkDiagram() {
  return (
    <svg viewBox="0 0 360 240" className="h-auto w-full" role="img"
      aria-label="A black hole growing inside the de Sitter bulk until its horizon meets the cosmological horizon at the Nariai point">
      {/* de Sitter bulk */}
      <circle cx="180" cy="120" r="104" fill="rgba(59,130,246,0.06)"
        stroke="rgba(96,165,250,0.65)" strokeWidth="1.6" />
      <text x="180" y="24" textAnchor="middle" fontSize="11"
        fill="rgb(147,197,253)">
        cosmological horizon (de Sitter bulk)
      </text>
      {/* growing black hole stages */}
      <circle cx="180" cy="120" r="22" fill="rgba(251,191,36,0.10)"
        stroke="rgba(251,191,36,0.5)" strokeWidth="1" strokeDasharray="3 3" />
      <circle cx="180" cy="120" r="58" fill="rgba(251,191,36,0.08)"
        stroke="rgba(251,191,36,0.6)" strokeWidth="1.2" strokeDasharray="4 3" />
      <circle cx="180" cy="120" r="104" fill="none"
        stroke="rgba(248,113,113,0.85)" strokeWidth="2" strokeDasharray="6 4" />
      <text x="180" y="124" textAnchor="middle" fontSize="10"
        fill="rgb(252,211,77)">
        black hole grows
      </text>
      {/* arrow outward */}
      <line x1="180" y1="96" x2="180" y2="44" stroke="rgba(252,211,77,0.7)"
        strokeWidth="1.4" markerEnd="url(#arrowOut)" />
      <defs>
        <marker id="arrowOut" markerWidth="8" markerHeight="8" refX="6"
          refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6" fill="none"
            stroke="rgba(252,211,77,0.9)" strokeWidth="1.2" />
        </marker>
      </defs>
      {/* Nariai label */}
      <text x="180" y="232" textAnchor="middle" fontSize="11"
        fill="rgb(252,165,165)">
        maximal case (Nariai): both horizons meet — roots (1, 1, −2) = the anchor
      </text>
    </svg>
  );
}

function OrientationDiagram() {
  // a simple "hilltop = anchor, valley = democratic" picture, valid in
  // both sectors (flavor potential / SdS entropy with sign flipped)
  const path =
    "M 16 64 C 70 150, 120 158, 168 110 C 216 62, 268 40, 336 36";
  return (
    <svg viewBox="0 0 360 200" className="h-auto w-full" role="img"
      aria-label="Dynamics rolls away from the anchor hilltop toward the democratic valley in both sectors">
      <path d={path} fill="none" stroke="rgba(96,165,250,0.8)"
        strokeWidth="2.2" />
      {/* anchor hilltop (right, repeller) */}
      <circle cx="336" cy="36" r="7" fill="rgb(248,113,113)"
        stroke="rgba(0,0,0,0.4)" />
      <text x="332" y="22" textAnchor="end" fontSize="11"
        fill="rgb(252,165,165)">
        anchor configuration (stationary repeller)
      </text>
      {/* democratic valley (left, attractor) */}
      <circle cx="96" cy="142" r="7" fill="rgb(52,211,153)"
        stroke="rgba(0,0,0,0.4)" />
      <text x="96" y="170" textAnchor="middle" fontSize="11"
        fill="rgb(110,231,183)">
        democratic endpoint (attractor)
      </text>
      {/* rolling ball + arrow */}
      <circle cx="252" cy="52" r="6" fill="rgb(226,232,240)"
        stroke="rgba(0,0,0,0.35)" />
      <line x1="240" y1="60" x2="180" y2="98" stroke="rgba(226,232,240,0.8)"
        strokeWidth="1.6" markerEnd="url(#arrowFlow)" />
      <defs>
        <marker id="arrowFlow" markerWidth="9" markerHeight="9" refX="7"
          refY="3.5" orient="auto">
          <path d="M0,0 L7,3.5 L0,7" fill="none"
            stroke="rgba(226,232,240,0.9)" strokeWidth="1.3" />
        </marker>
      </defs>
    </svg>
  );
}

const FACTS = [
  {
    title: "Nariai = the anchor",
    body: (
      <>
        At the maximal mass the horizon equation becomes{" "}
        <Math>{"t^3-3t+2=(t-1)^2(t+2)"}</Math> with roots{" "}
        <Math>{"(1,1,-2)"}</Math> — exactly the traceless form of the anchor{" "}
        <Math>{"a=(1,1,2)"}</Math> that generates the whole compiler grammar.
      </>
    ),
    marker: "[I]",
  },
  {
    title: "The Koide 2/3 is the entropy bound",
    body: (
      <>
        The maximal black hole carries exactly{" "}
        <Math>{"\\tfrac{2}{3}=|\\mathbb{Z}_2|/N_{\\mathrm{fam}}"}</Math> of the
        de Sitter entropy — the same constant that sits at the Koide branch
        point of the flavor sector. Zero adjustable parameters on either side.
      </>
    ),
    marker: "[I]",
  },
  {
    title: "One orientation in both sectors",
    body: (
      <>
        Flavor relaxation and black-hole evaporation both flow{" "}
        <em>away</em> from the anchor configuration — a stationary repeller
        with grammar-constant curvature (<Math>{"\\pm\\Delta"}</Math> in
        flavor, <Math>{"2/9=|\\mathbb{Z}_2|/N_{\\mathrm{fam}}^2"}</Math> in
        gravity). Reading it as one variational principle stays [P].
      </>
    ),
    marker: "[I] + [P]",
  },
];

export function HorizonStory() {
  return (
    <section
      aria-labelledby="horizon-story-heading"
      className="relative border-t border-white/5 bg-slate-950 py-20 sm:py-24"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <SectionHeader
          id="horizon-story-heading"
          eyebrow="Seam = horizon"
          title="Put a black hole into the bulk — the grammar answers"
          description="A structure test with zero free parameters: write classical black-hole mechanics inside the de Sitter bulk in seam units, and every coefficient lands on a compiler atom that is already load-bearing elsewhere. Machine-checked in v101/v102; the carrier-in-the-bulk reading is typed [P]."
        />
        <div className="mt-10 grid gap-6 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5 }}
            className="rounded-2xl border border-white/10 bg-white/[0.03] p-5"
          >
            <h3 className="text-sm font-semibold text-slate-200">
              The maximal black hole in the de Sitter bulk
            </h3>
            <div className="mt-3"><BulkDiagram /></div>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="rounded-2xl border border-white/10 bg-white/[0.03] p-5"
          >
            <h3 className="text-sm font-semibold text-slate-200">
              One orientation: away from the anchor, toward the democratic
              endpoint
            </h3>
            <div className="mt-3"><OrientationDiagram /></div>
          </motion.div>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {FACTS.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.4, delay: i * 0.08 }}
              className="rounded-xl border border-white/10 bg-white/[0.03] p-4"
            >
              <div className="flex items-center justify-between gap-2">
                <h4 className="text-sm font-semibold text-slate-200">
                  {f.title}
                </h4>
                <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] font-semibold text-emerald-200 ring-1 ring-emerald-400/30">
                  {f.marker}
                </span>
              </div>
              <p className="mt-2 text-[13px] leading-relaxed text-slate-400">
                {f.body}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

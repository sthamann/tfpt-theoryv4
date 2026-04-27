"use client";

import { motion } from "motion/react";
import { CheckCircle2, XCircle } from "lucide-react";
import { Math } from "@/components/Math";
import { SectionHeader } from "@/components/SectionHeader";

const CLAIMS = [
  "TFPT is a boundary-polarized spectral theory whose primitive input is a one-sided boundary datum.",
  "Boundary polarization induces a finite carrier involution; compact Higgs index and primitive Yukawa type force the ranks (dim E_-, dim E_+) = (3, 2) — the carrier polynomial 6Y² − Y − 1 = 0 is a corollary, not an entry assumption.",
  "The Standard-Model packet, α, the Cabibbo angle, and the PMNS reactor angle are forced by the same primitive datum, not fitted independently.",
  "The strong-CP null θ_eff = 0 is a theorem-level consequence of admissibility and determinant-line closure.",
];

const NOT_CLAIMS = [
  "The carrier polynomial is not invoked before the rank discharge — it appears only as the minimal polynomial of the derived eigenvalues.",
  "Minimality is not a wishlist over preferred physics — it is a presentation-invariant defect filtration on essentialized admissible bordisms.",
  "The CMB Stage 2 sky realization is not a theorem. A good CMB world is not automatically this CMB world.",
  "The full pole-mass ledger, detailed E8 stage atlas, and cosmological comparison rows (Ω_b, η_B, m_a) are downstream comparisons, not primitive selectors.",
];

export function WhatTfptClaims() {
  return (
    <section
      id="claims"
      className="relative scroll-mt-24 py-20 sm:py-24"
      aria-labelledby="claims-heading"
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="What TFPT claims"
          title="A staged reconstruction, not a list of fits"
          description="The orientation makes two things explicit: what TFPT does claim at the primitive level, and what it explicitly does not promote to theorem status. The split is what makes the falsification surface auditable."
        />

        <div className="mt-12 grid gap-5 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.6 }}
            className="rounded-2xl border border-emerald-400/20 bg-emerald-500/5 p-6"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/15 ring-1 ring-emerald-400/30">
                <CheckCircle2 size={18} className="text-emerald-300" />
              </div>
              <h3 className="font-serif text-xl font-semibold text-slate-50">
                Claimed at the primitive level
              </h3>
            </div>
            <ul className="mt-5 space-y-3 text-sm leading-relaxed text-slate-300">
              {CLAIMS.map((c, i) => (
                <li key={i} className="flex gap-3">
                  <span
                    className="mt-1.5 h-1.5 w-1.5 flex-none rounded-full bg-emerald-400"
                    aria-hidden
                  />
                  <span>{c}</span>
                </li>
              ))}
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.05 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="rounded-2xl border border-orange-400/20 bg-orange-500/5 p-6"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-orange-500/15 ring-1 ring-orange-400/30">
                <XCircle size={18} className="text-orange-300" />
              </div>
              <h3 className="font-serif text-xl font-semibold text-slate-50">
                Not claimed at this level
              </h3>
            </div>
            <ul className="mt-5 space-y-3 text-sm leading-relaxed text-slate-300">
              {NOT_CLAIMS.map((c, i) => (
                <li key={i} className="flex gap-3">
                  <span
                    className="mt-1.5 h-1.5 w-1.5 flex-none rounded-full bg-orange-400"
                    aria-hidden
                  />
                  <span>{c}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-10 rounded-2xl border border-slate-700/40 bg-slate-950/40 p-6 sm:p-8"
        >
          <h3 className="font-serif text-lg font-semibold text-slate-50">
            The primitive boundary datum
          </h3>
          <p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-300">
            Everything reconstructs from a single one-sided boundary datum. The
            primitive kernel is reconstructed canonically; carrier, gauge group,
            and the Standard-Model packet follow from a stabilizer theorem rather
            than from a list of inserted representations.
          </p>
          <div className="mt-5 grid gap-3 lg:grid-cols-2">
            <div className="rounded-lg border border-slate-700/40 bg-slate-950/60 p-4">
              <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                Primitive datum
              </div>
              <div className="mt-2 overflow-x-auto">
                <Math block>
                  {"\\mathfrak{T}_\\partial = (\\mathcal{A}_+,\\mathcal{H}_+,D_+,J,\\Gamma,B_\\Sigma)"}
                </Math>
              </div>
            </div>
            <div className="rounded-lg border border-slate-700/40 bg-slate-950/60 p-4">
              <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                Primitive kernel
              </div>
              <div className="mt-2 overflow-x-auto">
                <Math block>
                  {"\\mathfrak{T}_\\partial^{\\mathrm{ker}} = (\\mathcal{A},\\mathcal{H},D,J,\\Gamma,\\tau_{\\mathrm{dbl}},\\iota_C,P_{\\mathrm{prim}},[u_\\Sigma],c_3)"}
                </Math>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

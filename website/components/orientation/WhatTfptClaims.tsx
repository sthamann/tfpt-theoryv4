"use client";

import { motion } from "motion/react";
import { CheckCircle2, XCircle } from "lucide-react";
import { Math } from "@/components/Math";
import { SectionHeader } from "@/components/SectionHeader";

const CLAIMS = [
  "TFPT is a discrete compiler with two inputs: the seam constant c₃ = 1/(8π) and the five-slot carrier g_car = 5. Nothing else is inserted by hand.",
  "The carrier gives D₅, the family geometry gives A₃, and the μ₄ glue closes E₈ = (D₅ ⊕ A₃) + μ₄ as a lattice theorem — 240 = 16·5·3, 248 = 240 + 8 are carrier traces.",
  "α⁻¹ = 137.0359992168 is the unique root of a parameter-free cubic (existence + uniqueness proved), and the flavor matrix, masses and θ₁₂ = 1/3 − φ₀/2 follow from one φ₀-ladder.",
  "The bootstrap loop re-derives the inputs: g_car = 5 is forced three ways and the 8 in c₃ equals rank E₈ — the discrete core is overdetermined, with only π irreducible.",
];

const NOT_CLAIMS = [
  "E₈ is the unimodular audit/compiler hull, not an unbroken physical gauge group — so the no-go results against literal E₈ world-formulas do not apply.",
  "The dimensionful EW/QCD masses (m_W, m_Z, m_H, sin²θ_W, α_s) sit on the RG scheme layer; the absolute quark amplitude scale reduces to the U_point anchor.",
  "The frontier items — η_B, m_p/m_e, Koide, dark matter — are honest handles, not forced compiler powers; gravity's local field equation is now parameter-free (Gₐᵦ + Λgₐᵦ = c₃⁻¹Tₐᵦ, both coefficients fixed), with only the ambient measure left open.",
  "No strict physical TOE is certified: the ambient, non-perturbative quantum-gravity measure (G6 / QG.AMB.01) — decoupled from the now-closed local field equation — remains the open completion target.",
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
          title="One compiler, not a list of fits"
          description="The introduction makes two things explicit: what TFPT does claim at the compiler level, and what it explicitly does not promote past its grade. The split is what makes the falsification surface auditable."
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
            The two axioms
          </h3>
          <p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-300">
            Everything is generated from the seam constant and the five-slot
            carrier. They are not even independent: both are elementary symmetric
            polynomials of the single anchor a = (1,1,2), so the inputs collapse
            to the anchor plus the lone continuous primitive π.
          </p>
          <div className="mt-5 grid gap-3 lg:grid-cols-2">
            <div className="rounded-lg border border-slate-700/40 bg-slate-950/60 p-4">
              <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                P1 — seam constant
              </div>
              <div className="mt-2 overflow-x-auto">
                <Math block>
                  {"c_3 = \\frac{1}{|\\mathbb{Z}_2|\\oint_{S^2}K\\,dA} = \\frac{1}{8\\pi}"}
                </Math>
              </div>
            </div>
            <div className="rounded-lg border border-slate-700/40 bg-slate-950/60 p-4">
              <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                P2 — five-slot carrier
              </div>
              <div className="mt-2 overflow-x-auto">
                <Math block>
                  {"g_{\\mathrm{car}} = 5 = 3 + 2, \\quad \\dim S^+ = 2^{g-1} = 16"}
                </Math>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

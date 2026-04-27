"use client";

import { motion } from "motion/react";
import { ArrowDown } from "lucide-react";
import { Math } from "./Math";

const COLOR_TRIPLET = [
  { name: "1", colorClass: "from-orange-500 to-red-500" },
  { name: "2", colorClass: "from-emerald-500 to-teal-500" },
  { name: "3", colorClass: "from-blue-500 to-cyan-500" },
];

const WEAK_DOUBLET = [
  { name: "1", colorClass: "from-violet-500 to-purple-500" },
  { name: "2", colorClass: "from-fuchsia-500 to-pink-500" },
];

export function CarrierVisualization() {
  return (
    <div className="space-y-8">
      <div className="rounded-2xl border border-amber-400/25 bg-amber-500/5 p-5 sm:p-6">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-amber-500/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-amber-200 ring-1 ring-amber-400/30">
            Proof tree cut
          </span>
          <span className="text-[10px] font-semibold uppercase tracking-widest text-amber-200/80">
            Reading order matters
          </span>
        </div>
        <p className="mt-2 text-sm leading-relaxed text-amber-100/90">
          The carrier polynomial{" "}
          <Math>{"6Y^2 - Y - \\mathbf{1} = 0"}</Math> is{" "}
          <span className="font-semibold text-amber-200">not</span> an entry
          assumption. It is the algebraic shadow of a derived rank split{" "}
          <Math>{"(\\dim E_-, \\dim E_+) = (3, 2)"}</Math>. The four steps below
          show the order in which TFPT actually proves this.
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-2 xl:grid-cols-4">
        <ProofStep
          step={1}
          accent="from-blue-500 to-cyan-500"
          title="Boundary involution"
          subtitle="Calderón polarization"
          body="The Calderón polarization of the one-sided boundary datum induces a finite essential carrier involution. At this stage there is only a two-point algebra — no rank, no Standard Model."
          formula={"\\varepsilon_{\\mathrm{car}} = \\iota_C|_E,\\; E = E_- \\oplus E_+"}
          conclusion={"\\dim E = ?"}
        />
        <ProofStep
          step={2}
          accent="from-violet-500 to-purple-500"
          title="Compact Higgs index"
          subtitle="Riemann–Roch on S²"
          body="Unit seam winding selects the minimal nonnegative determinant class on the compactified normal sphere. The seam-even block carries 𝒪(1) on S²; Riemann–Roch gives a 2-dimensional space of holomorphic sections."
          formula={"H^0(S^2,\\mathcal{O}(1)) \\simeq \\mathbb{C}^2"}
          conclusion={"\\Rightarrow \\dim E_+ = 2"}
        />
        <ProofStep
          step={3}
          accent="from-emerald-500 to-teal-500"
          title="Primitive Yukawa type"
          subtitle="Indecomposable trilinear"
          body="The retained branch contains a nonzero primitive indecomposable local trilinear with two fermionic legs and one seam-even bosonic leg. Closure of the negative factor without a spectator forces Λ³E_- = det E_-."
          formula={"\\Lambda^3 E_- = \\det E_-"}
          conclusion={"\\Rightarrow \\dim E_- = 3"}
        />
        <ProofStep
          step={4}
          accent="from-fuchsia-500 to-pink-500"
          title="Determinant-normalized Y"
          subtitle="Polynomial as corollary"
          body="With (dim E_-, dim E_+) = (3, 2) the primitive integer determinant-preserving generator is unique. The carrier polynomial appears only as the minimal polynomial of its two derived roots."
          formula={"Y = -\\tfrac{1}{3} P_- + \\tfrac{1}{2} P_+"}
          conclusion={"6Y^2 - Y - \\mathbf{1} = 0"}
        />
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <div className="glass rounded-2xl ring-1 ring-slate-700/40">
          <div className="border-b border-slate-800/60 px-5 py-3">
            <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
              Derived rank split — visualized
            </span>
          </div>
          <div className="p-6">
            <div className="overflow-x-auto">
              <Math block>
                {String.raw`E = E_- \oplus E_+, \quad (\dim E_-, \dim E_+) = (3, 2)`}
              </Math>
            </div>

            <div className="mt-6 grid gap-5 sm:grid-cols-2">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.7 }}
                className="relative rounded-xl border border-orange-400/30 bg-gradient-to-br from-orange-500/10 to-red-500/5 p-5"
              >
                <div className="text-[10px] font-semibold uppercase tracking-widest text-orange-200/90">
                  E_- (negative polarization)
                </div>
                <div className="mt-2 font-serif text-3xl font-semibold text-slate-50">
                  dim 3
                </div>
                <div className="mt-1 text-xs text-slate-400">
                  forced by primitive Yukawa type
                </div>
                <div className="mt-4 flex gap-2">
                  {COLOR_TRIPLET.map((c, i) => (
                    <motion.div
                      key={c.name}
                      initial={{ scale: 0, opacity: 0 }}
                      whileInView={{ scale: 1, opacity: 1 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.2 + i * 0.1, type: "spring" }}
                      className={`flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br ${c.colorClass} font-mono text-xs font-semibold text-white ring-2 ring-white/10`}
                    >
                      {c.name}
                    </motion.div>
                  ))}
                </div>
                <div className="mt-3 text-[10px] font-mono uppercase tracking-widest text-orange-200/70">
                  Y = −1/3 (after determinant normalization)
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.7, delay: 0.15 }}
                className="relative rounded-xl border border-violet-400/30 bg-gradient-to-br from-violet-500/10 to-purple-500/5 p-5"
              >
                <div className="text-[10px] font-semibold uppercase tracking-widest text-violet-200/90">
                  E_+ (positive polarization)
                </div>
                <div className="mt-2 font-serif text-3xl font-semibold text-slate-50">
                  dim 2
                </div>
                <div className="mt-1 text-xs text-slate-400">
                  forced by compact Higgs index
                </div>
                <div className="mt-4 flex gap-2">
                  {WEAK_DOUBLET.map((c, i) => (
                    <motion.div
                      key={c.name}
                      initial={{ scale: 0, opacity: 0 }}
                      whileInView={{ scale: 1, opacity: 1 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.5 + i * 0.1, type: "spring" }}
                      className={`flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br ${c.colorClass} font-mono text-xs font-semibold text-white ring-2 ring-white/10`}
                    >
                      {c.name}
                    </motion.div>
                  ))}
                </div>
                <div className="mt-3 text-[10px] font-mono uppercase tracking-widest text-violet-200/70">
                  Y = +1/2 (after determinant normalization)
                </div>
              </motion.div>
            </div>

            <div className="mt-5 rounded-lg border border-emerald-400/25 bg-emerald-500/5 p-4 text-xs leading-relaxed text-emerald-100/90">
              <strong className="text-emerald-200">Trace, automatic.</strong>{" "}
              <Math>
                {"\\operatorname{tr}_E Y = 3 \\!\\cdot\\! (-1/3) + 2 \\!\\cdot\\! (1/2) = 0"}
              </Math>{" "}
              — not an additional constraint, just arithmetic on the derived
              eigenvalues.
            </div>
          </div>
        </div>

        <div className="glass rounded-2xl ring-1 ring-slate-700/40">
          <div className="border-b border-slate-800/60 px-5 py-3">
            <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
              Spinor packet S⁺ = Λ^even E (read off after carrier)
            </span>
          </div>
          <div className="p-6">
            <div className="overflow-x-auto">
              <Math block>
                {"S^+ = \\Lambda^{\\mathrm{even}} E, \\quad \\dim S^+ = 16"}
              </Math>
            </div>

            <div className="mt-6">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-700/60 text-slate-300">
                    <th className="py-2 font-semibold">Multiplet</th>
                    <th className="py-2 font-semibold">SU(3)×SU(2)×U(1)</th>
                    <th className="py-2 text-right font-semibold">Y</th>
                    <th className="py-2 text-right font-semibold">Dim</th>
                  </tr>
                </thead>
                <tbody className="text-slate-300">
                  {[
                    { mp: "Q_L", repr: "(3, 2, 1/6)", y: "1/6", dim: "6" },
                    { mp: "u_R", repr: "(3, 1, 2/3)", y: "2/3", dim: "3" },
                    { mp: "d_R", repr: "(3, 1, −1/3)", y: "−1/3", dim: "3" },
                    { mp: "L_L", repr: "(1, 2, −1/2)", y: "−1/2", dim: "2" },
                    { mp: "e_R", repr: "(1, 1, −1)", y: "−1", dim: "1" },
                    { mp: "ν_R", repr: "(1, 1, 0)", y: "0", dim: "1" },
                  ].map((row, i) => (
                    <motion.tr
                      key={row.mp}
                      initial={{ opacity: 0, x: -8 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true, amount: 0.05 }}
                      transition={{ duration: 0.4, delay: i * 0.05 }}
                      className="border-b border-slate-800/40 transition-colors hover:bg-slate-900/40"
                    >
                      <td className="py-2 font-mono">{row.mp}</td>
                      <td className="py-2 text-slate-400">{row.repr}</td>
                      <td className="py-2 text-right font-mono text-blue-300">
                        {row.y}
                      </td>
                      <td className="py-2 text-right font-mono">{row.dim}</td>
                    </motion.tr>
                  ))}
                  <tr className="text-slate-100">
                    <td className="py-2 font-semibold" colSpan={3}>
                      One chiral family (incl. ν_R)
                    </td>
                    <td className="py-2 text-right font-mono font-semibold text-emerald-300">
                      16
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="mt-5 grid gap-3 sm:grid-cols-3">
              {[
                { label: "Families", value: "3" },
                { label: "Higgs N_Φ", value: "1" },
                { label: "b₁", value: "41/10" },
              ].map((c) => (
                <div
                  key={c.label}
                  className="rounded-lg border border-slate-700/40 bg-slate-950/40 px-4 py-3 text-center"
                >
                  <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                    {c.label}
                  </div>
                  <div className="mt-1 font-serif text-lg font-semibold text-slate-50">
                    {c.value}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-700/40 bg-slate-950/40 p-6 sm:p-7">
        <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
          Why this coefficient is forced — not guessed
        </div>
        <h3 className="mt-1 font-serif text-lg font-semibold text-slate-50">
          The general split check
        </h3>
        <p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-300">
          For any essential split E_b ⊕ E_s with determinant-normalized roots
          −1/b and 1/s, the two-point generator satisfies the family
        </p>
        <div className="mt-3 overflow-x-auto rounded-lg border border-slate-700/40 bg-slate-950/60 p-3">
          <Math block>
            {"b s\\, Y^2 + (s - b)\\, Y - \\mathbf{1} = 0"}
          </Math>
        </div>
        <p className="mt-3 text-sm leading-relaxed text-slate-300">
          The boundary / Higgs / Yukawa rank arguments fix{" "}
          <Math>{"(b, s) = (3, 2)"}</Math>. The coefficient{" "}
          <span className="font-mono text-slate-100">6 = 3 · 2</span> is the
          determinant-periodized block normalization of the rigid 3+2 carrier
          — not phenomenologically tuned, not guessed.
        </p>
      </div>
    </div>
  );
}

function ProofStep({
  step,
  accent,
  title,
  subtitle,
  body,
  formula,
  conclusion,
}: {
  step: number;
  accent: string;
  title: string;
  subtitle: string;
  body: string;
  formula: string;
  conclusion: string;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.05 }}
      transition={{ duration: 0.6, delay: step * 0.06 }}
      className="group glass relative flex flex-col overflow-hidden rounded-2xl ring-1 ring-slate-700/40 transition-all hover:ring-slate-500/60"
    >
      <div
        aria-hidden
        className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${accent} opacity-70`}
      />
      <div className="flex flex-col gap-3 p-5">
        <div className="flex items-start gap-3">
          <span
            className={`flex h-9 w-9 flex-none items-center justify-center rounded-lg bg-gradient-to-br ${accent} font-mono text-sm font-semibold text-white shadow-md`}
          >
            {step}
          </span>
          <div>
            <h4 className="font-serif text-base font-semibold leading-tight text-slate-50">
              {title}
            </h4>
            <p className="text-[11px] font-medium uppercase tracking-widest text-slate-400">
              {subtitle}
            </p>
          </div>
        </div>
        <p className="text-xs leading-relaxed text-slate-300">{body}</p>

        <div className="rounded-lg border border-slate-700/40 bg-slate-950/40 p-3">
          <div className="text-[9px] font-semibold uppercase tracking-widest text-blue-300/70">
            Step formula
          </div>
          <div className="mt-1 overflow-x-auto">
            <Math block>{formula}</Math>
          </div>
        </div>

        <div className="flex items-center justify-center text-slate-500">
          <ArrowDown size={14} aria-hidden />
        </div>

        <div className="rounded-lg border border-emerald-400/25 bg-emerald-500/5 p-3">
          <div className="text-[9px] font-semibold uppercase tracking-widest text-emerald-300/80">
            Conclusion
          </div>
          <div className="mt-1 overflow-x-auto">
            <Math block>{conclusion}</Math>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

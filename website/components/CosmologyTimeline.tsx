"use client";

import { motion } from "motion/react";
import { Math } from "./Math";
import { Telescope, Wand2, Atom, Star } from "lucide-react";

type StageStatus = "fixed" | "downstream" | "programmatic" | "conjectural";

const STATUS_STYLE: Record<
  StageStatus,
  { label: string; className: string }
> = {
  fixed: {
    label: "Fixed before cosmology",
    className:
      "bg-blue-500/15 text-blue-200 ring-blue-400/30",
  },
  downstream: {
    label: "Downstream interface",
    className:
      "bg-violet-500/15 text-violet-200 ring-violet-400/30",
  },
  programmatic: {
    label: "Programmatic target",
    className:
      "bg-fuchsia-500/15 text-fuchsia-200 ring-fuchsia-400/30",
  },
  conjectural: {
    label: "Conjectural",
    className:
      "bg-rose-500/15 text-rose-200 ring-rose-400/30",
  },
};

const STAGES: Array<{
  icon: typeof Atom;
  title: string;
  body: string;
  accent: string;
  status: StageStatus;
}> = [
  {
    icon: Atom,
    title: "Closed branch T★",
    body: "All primitive structure — kernel, carrier, EM closure, admissibility, metrology — fixed before cosmology enters.",
    accent: "from-blue-500 to-violet-500",
    status: "fixed",
  },
  {
    icon: Wand2,
    title: "Seam transfer · determinant line",
    body: "Λ_IR = M̄_Pl⁴ [-log det_adm(1 - U_Σ)]. The infrared scale is read from the admissible determinant, not fitted.",
    accent: "from-violet-500 to-fuchsia-500",
    status: "downstream",
  },
  {
    icon: Telescope,
    title: "CMB Stage 1 — spectra",
    body: "Transfer functions, angular spectra, comparison rows. Falsification targets and benchmark rows.",
    accent: "from-fuchsia-500 to-pink-500",
    status: "programmatic",
  },
  {
    icon: Star,
    title: "CMB Stage 2 — sky realization",
    body: "A conjectural realization target. A good CMB world is not automatically this CMB world — programmatic, not theorem-level.",
    accent: "from-pink-500 to-rose-500",
    status: "conjectural",
  },
];

export function CosmologyTimeline() {
  return (
    <div className="glass rounded-2xl ring-1 ring-slate-700/40">
      <div className="border-b border-slate-800/60 px-5 py-3">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-blue-300/80">
          Cosmology — downstream interface, status-coded
        </span>
      </div>

      <div className="p-6 md:p-8">
        <div className="overflow-x-auto">
          <Math block>
            {"\\mathfrak{T}_\\star \\Rightarrow (U_\\Sigma, \\det_{\\mathrm{adm}}, \\text{scalaron}, \\nu) \\Rightarrow (\\Lambda_{\\mathrm{IR}}, S_\\Sigma, N_{\\mathrm{DW}}, \\theta_i, T_R, \\mathcal{I}_{\\mathrm{LG}}) \\Rightarrow \\text{CMB targets}"}
          </Math>
        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {STAGES.map((s, i) => {
            const Icon = s.icon;
            const statusStyle = STATUS_STYLE[s.status];
            return (
              <motion.div
                key={s.title}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.05 }}
                transition={{ duration: 0.6, delay: i * 0.1 }}
                className="relative overflow-hidden rounded-xl border border-slate-700/40 bg-slate-950/40 p-5"
              >
                <div
                  className={`mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br ${s.accent}`}
                >
                  <Icon size={18} className="text-white" />
                </div>
                <div className="flex items-center gap-2">
                  <h4 className="font-serif text-base font-semibold text-slate-50">
                    {s.title}
                  </h4>
                </div>
                <span
                  className={`mt-1 inline-block rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest ring-1 ${statusStyle.className}`}
                >
                  {statusStyle.label}
                </span>
                <p className="mt-3 text-xs leading-relaxed text-slate-300">
                  {s.body}
                </p>
              </motion.div>
            );
          })}
        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[
            { l: "Λ_IR", v: "Seam transfer", n: "−log det_adm(1 − U_Σ)" },
            { l: "Axion", v: "ν_a ≈ 15.764 GHz", n: "Haloscope window" },
            { l: "η_B", v: "5.97 × 10⁻¹⁰", n: "Leptogenesis interface" },
            { l: "β_BH(r)", v: "16 c₃⁴ Q_e^eff Q_m^eff / r²", n: "EHT/ngEHT achromatic residual intercept" },
          ].map((it) => (
            <div
              key={it.l}
              className="rounded-xl border border-slate-700/40 bg-slate-950/40 px-5 py-4"
            >
              <div className="math-label text-[10px] font-semibold tracking-widest text-blue-300/80">
                {it.l}
              </div>
              <div className="mt-1 font-serif text-lg font-semibold text-slate-50">
                {it.v}
              </div>
              <div className="text-xs text-slate-400">{it.n}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

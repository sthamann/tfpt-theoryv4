"use client";

import { ChevronDown, ExternalLink } from "lucide-react";
import { FAQ_ITEMS } from "@/lib/faq";

const SOURCES: { name: string; what: string; href: string }[] = [
  { name: "CODATA 2022", what: "fine-structure constant α⁻¹", href: "https://physics.nist.gov/cuu/Constants/" },
  { name: "NuFIT 6.0", what: "neutrino mixing angles & δ_CP", href: "http://www.nu-fit.org/" },
  { name: "ACT DR6", what: "cosmic birefringence β", href: "https://act.princeton.edu/" },
  { name: "Planck 2018", what: "n_s, A_s, Ω_b, baseline cosmology", href: "https://www.cosmos.esa.int/web/planck" },
  { name: "JUNO", what: "sub-percent solar angle sin²θ₁₂", href: "https://juno.ihep.cas.cn/" },
  { name: "DUNE", what: "atmospheric octant, δ_CP, ordering", href: "https://www.dunescience.org/" },
  { name: "CMB-S4", what: "tensor-to-scalar ratio r", href: "https://cmb-s4.org/" },
  { name: "BICEP/Keck", what: "current bound r < 0.036", href: "http://bicepkeck.org/" },
  { name: "PSI nEDM", what: "neutron electric dipole moment", href: "https://www.psi.ch/en/nedm" },
  { name: "PDG", what: "particle masses & mixing reference", href: "https://pdg.lbl.gov/" },
];

export function HostileRefereeFAQ() {
  return (
    <div>
      <div className="space-y-3">
        {FAQ_ITEMS.map((item) => (
          <details
            key={item.q}
            className="group glass rounded-2xl ring-1 ring-slate-700/40 [&_summary::-webkit-details-marker]:hidden"
          >
            <summary className="flex cursor-pointer list-none items-center justify-between gap-3 px-5 py-4 text-left">
              <span className="font-serif text-base font-semibold text-slate-50">
                {item.q}
              </span>
              <ChevronDown
                size={18}
                className="flex-none text-slate-400 transition-transform group-open:rotate-180"
                aria-hidden
              />
            </summary>
            <div className="border-t border-slate-800/60 px-5 py-4 text-sm leading-relaxed text-slate-300">
              {item.a}
            </div>
          </details>
        ))}
      </div>

      <div className="mt-10 rounded-2xl border border-slate-700/40 bg-slate-950/40 p-6">
        <h3 className="font-serif text-base font-semibold text-slate-50">
          Experimental comparison sources
        </h3>
        <p className="mt-1 text-xs leading-relaxed text-slate-400">
          These are comparison surfaces, not inputs. The closed branch is built
          only from the two axioms.
        </p>
        <ul className="mt-4 grid gap-2 sm:grid-cols-2">
          {SOURCES.map((s) => (
            <li key={s.name}>
              <a
                href={s.href}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center justify-between gap-2 rounded-lg border border-slate-800/50 bg-slate-950/40 px-3 py-2 transition-colors hover:border-blue-400/40 hover:bg-blue-500/5"
              >
                <span className="text-sm">
                  <span className="font-semibold text-slate-100">{s.name}</span>
                  <span className="text-slate-400"> — {s.what}</span>
                </span>
                <ExternalLink
                  size={13}
                  className="flex-none text-slate-600 transition-colors group-hover:text-blue-300"
                  aria-hidden
                />
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

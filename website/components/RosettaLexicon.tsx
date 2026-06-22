import { SectionHeader } from "./SectionHeader";

/**
 * The "Rosetta" lexicon: TFPT's discrete-mathematics nomenclature ("compiler",
 * "seam", "deck", "readout", "microcode") mapped heuristically onto standard
 * QFT / mathematical-physics language (Wilsonian RG, path integral, anomalies,
 * index theorems). This is a translation aid for mainstream physicists, not a
 * new claim — every row points to the orthodox concept the TFPT term plays the
 * role of. Recommended by external review (publication-accessibility).
 */
const LEXICON: { term: string; reading: string }[] = [
  {
    term: "Compiler",
    reading:
      "A deterministic boundary → IR map (a fixed renormalization-group endpoint read off by projection), not a parameter fit. ‘Compiles’ = evaluates the unique fixed point.",
  },
  {
    term: "Seam",
    reading:
      "The reflection-positive boundary / holographic screen — a Wilsonian UV boundary CFT (chiral conformal net) whose data the bulk reads off.",
  },
  {
    term: "Carrier (D₅ ⊕ A₃)",
    reading:
      "The boundary field content / chiral algebra: 16 free Majorana fermions, c = 8 = 5 + 3 (a free-fermion conformal net).",
  },
  {
    term: "μ₄ glue / deck",
    reading:
      "An orbifold deck transformation / simple-current (ℤ₄) extension — the standard ‘gauge a discrete symmetry’ / extension operation on a CFT.",
  },
  {
    term: "Clock",
    reading:
      "The Coxeter monodromy element of W(A₃) = S₄ (order h(A₃) = 4) — the orbifold rotation generating the ℤ₄.",
  },
  {
    term: "Audit hull (E₈)",
    reading:
      "An anomaly / consistency lattice — the even unimodular ‘checksum’ that the carrier must embed into. NOT a 4D gauge group (so Coleman–Mandula / Distler–Garibaldi do not apply).",
  },
  {
    term: "Readout / projection",
    reading:
      "An observable extracted as an index or intersection number — the value of an operator after projecting onto the physical sector (a Wilson-line/operator VEV).",
  },
  {
    term: "Microcode",
    reading:
      "The integer charge / index labels (hypercharges, Dynkin indices, Plücker coordinates) — the discrete, RG-invariant quantum numbers.",
  },
  {
    term: "Plücker readout",
    reading:
      "A topological intersection / Schubert index on a Grassmannian — a discrete, scheme-independent number (e.g. cᵤ/c_d = 55/117).",
  },
  {
    term: "Gap (2/3)⁶",
    reading:
      "The spectral gap of the boundary transfer operator = the RG-irrelevance rate of the leading deformation (a Perron–Frobenius subleading eigenvalue).",
  },
  {
    term: "Anchor a = (1,1,2)",
    reading:
      "The minimal generating datum — the role a renormalization scheme’s defining numbers play; its symmetric functions are (|μ₄|, g_car, |ℤ₂|) = (4,5,2).",
  },
  {
    term: "F_transfer",
    reading:
      "The (still-open) RG / threshold-matching functor: compiler source data → physical pole observable (Koide source→pole, η_B Boltzmann, m_p/m_e via QCD/EW). The missing dynamical action principle lives here.",
  },
  {
    term: "v_geo",
    reading:
      "The one dimensionful renormalization condition — a unit choice. After setting ℏ = c = 1 a single scale must still be fixed by hand; the No-Unit Theorem proves a dimensionless compiler cannot produce it.",
  },
  {
    term: "SEAM.EQUIV.01 (keystone)",
    reading:
      "The single named open theorem: the raw reflection-positive seam state IS the holomorphic (E₈)₁ net at τ=i. The role Einstein’s ‘c = const’ plays — TFPT’s one irreducible structural postulate; its conformal-deck face QGEO.SYM.01 (the seam’s conformal structure IS the carrier orbifold deck) is downstream.",
  },
];

export function RosettaLexicon() {
  return (
    <section
      id="rosetta"
      className="relative scroll-mt-20 border-t border-slate-800/60 py-20 sm:py-24"
      aria-labelledby="rosetta-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="A translation key"
          title="Compiler-speak → standard physics"
          description="TFPT’s vocabulary comes from discrete mathematics and computer science; a phenomenologist looks for Lagrangians and RG flows. This Rosetta maps each TFPT term onto the orthodox concept it plays the role of — a reading aid, not a new claim."
        />
        <div className="mt-10 overflow-hidden rounded-2xl border border-slate-700/40">
          <table className="w-full border-collapse text-left text-sm">
            <thead>
              <tr className="bg-slate-900/60 text-[11px] uppercase tracking-widest text-blue-300/80">
                <th className="w-1/3 px-4 py-3 font-semibold">TFPT term</th>
                <th className="px-4 py-3 font-semibold">Standard QFT / mathematical reading</th>
              </tr>
            </thead>
            <tbody>
              {LEXICON.map((row, i) => (
                <tr
                  key={row.term}
                  className={i % 2 === 0 ? "bg-slate-950/30" : "bg-slate-900/20"}
                >
                  <td className="px-4 py-3 align-top font-mono text-xs font-semibold text-slate-100">
                    {row.term}
                  </td>
                  <td className="px-4 py-3 align-top leading-relaxed text-slate-300">
                    {row.reading}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-5 text-sm leading-relaxed text-slate-400">
          The one honest gap a physicist will spot is{" "}
          <span className="font-mono text-slate-200">F_transfer</span>: the discrete kernel and the
          dimensionless readouts are exact, but the continuous dynamical principle that drives the
          source data to the physical pole is the open transfer layer — explicitly typed{" "}
          <span className="font-mono">[C]</span>, never sold as a derivation.
        </p>
      </div>
    </section>
  );
}

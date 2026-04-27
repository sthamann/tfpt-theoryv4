/**
 * Inline glossary used by the GlossTerm component to surface short, one-line
 * definitions for the technical TFPT vocabulary on hover/focus/tap. Keep
 * each definition under ~280 characters so the tooltip stays scannable.
 */
export interface GlossaryEntry {
  term: string;
  alias?: string[];
  short: string;
}

export const GLOSSARY: GlossaryEntry[] = [
  {
    term: "boundary datum",
    alias: ["one-sided boundary datum", "one sided boundary datum"],
    short:
      "Minimal one-sided spectral input from which the primitive kernel is reconstructed. The single primitive admissible object the rest of TFPT is built on.",
  },
  {
    term: "Calderón polarization",
    alias: ["Calderon polarization", "Calderón projector"],
    short:
      "The boundary projector that splits the doubled datum into positive and negative polarization sectors; supplies the carrier involution.",
  },
  {
    term: "primitive kernel",
    short:
      "The five-tuple (τ_dbl, ι_C, P_prim, [u_Σ], c₃) reconstructed from the boundary datum before any phenomenological input.",
  },
  {
    term: "carrier",
    alias: ["carrier rigidity", "carrier packet"],
    short:
      "Finite essential split E = E_- ⊕ E_+ carrying the determinant-normalized hypercharge generator Y. Polynomial 6Y² − Y − 1 = 0 is its corollary, not its assumption.",
  },
  {
    term: "joint discrete solve",
    short:
      "A single discrete admissibility solution that simultaneously fixes the rank split, the seam normalization, and the bridge seed — the source of the three decoders.",
  },
  {
    term: "admissibility selector",
    alias: ["admissibility", "P_adm", "selector"],
    short:
      "The composite projector P_adm = P_prim · P_sing · P_Θ that selects (does not evolve) the physical admissible sector of TFPT. Forces θ_eff = 0.",
  },
  {
    term: "closed branch",
    alias: ["T★", "T_star"],
    short:
      "The fully reconstructed admissible TFPT object after the selector and the closure dynamics have been applied. Inputs to all observable readouts.",
  },
  {
    term: "bridge readout",
    short:
      "An observable numerical output (α, λ_C, sin²θ_13, β, …) read off after theorem core and admissibility, with declared comparison map but no fitted constants.",
  },
  {
    term: "seam transfer",
    short:
      "The infrared map Λ_IR = M̄_Pl⁴[−log det_adm(1 − U_Σ)] connecting the admissible determinant line to the cosmological constant scale.",
  },
  {
    term: "determinant-line response",
    alias: ["determinant line", "Chern–Simons response"],
    short:
      "The Chern–Simons-type response sector that produces the cosmic birefringence amplitude β = φ₀/(4π) and, locally projected, the achromatic dyonic intercept β_BH(r).",
  },
  {
    term: "retained seed",
    alias: ["φ₀", "phi_0", "u = φ₀"],
    short:
      "The primitive bridge seed φ₀ = 1/(6π) + 3/(256π⁴) projecting to λ_C = √(φ₀(1−φ₀)), β_rad = φ₀/(4π), sin²θ_13 = φ₀ e^(−γ).",
  },
  {
    term: "seam opening",
    alias: ["φ_seam(α)"],
    short:
      "The α-dependent opening φ_seam(α) used inside the carrier-form electromagnetic closure equation. Different from the retained seed φ₀.",
  },
  {
    term: "compact Higgs index",
    short:
      "The Riemann–Roch readout H⁰(S², 𝒪(1)) ≅ ℂ² that fixes dim E_+ = 2 on the seam-even line bundle of the compactified normal sphere.",
  },
  {
    term: "primitive Yukawa type",
    short:
      "An indecomposable local trilinear with two fermionic legs and one seam-even bosonic leg; closes the negative factor and forces dim E_- = 3.",
  },
  {
    term: "cusp cubic",
    short:
      "The transport polynomial P(z) = (z − 1)(z − 64/729)(z − 1/729). Its lower critical point selects δ_ph on the rigid flavor branch.",
  },
  {
    term: "scheme projection",
    short:
      "Final mapping in the observable functor chain that sends physical observables into a chosen comparison scheme (e.g. MS̄ at M_Z). Conventions enter only here.",
  },
  {
    term: "downstream interface",
    short:
      "Cosmology / horizon / sky-realization comparison surface; status-coded as programmatic or conjectural. Cannot tune the primitive branch.",
  },
];

const NORMALISE = (s: string) => s.toLowerCase().trim();

export function findEntry(needle: string): GlossaryEntry | undefined {
  const norm = NORMALISE(needle);
  return GLOSSARY.find((entry) => {
    if (NORMALISE(entry.term) === norm) return true;
    return entry.alias?.some((a) => NORMALISE(a) === norm);
  });
}

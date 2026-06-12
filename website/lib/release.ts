/**
 * Release metadata for the published PDFs. The version, release date, byte
 * size, and SHA-256 hash are written here so reviewers can verify integrity
 * and tell two snapshots apart without opening the file.
 *
 * To regenerate these values after a re-build:
 *
 *   npm run release:write   (rewrites bytes + sha256 in place)
 *
 * which invokes scripts/release-hashes.mjs against website/public.
 */

export interface ReleaseAsset {
  /** Path under /public, including the leading slash. */
  href: string;
  /** Series version this snapshot was built against. */
  version: string;
  /** ISO-8601 release date for the artifact. */
  releaseDate: string;
  /** Byte size of the PDF (raw bytes). */
  bytes: number;
  /** SHA-256 hash of the PDF, lowercase hex. */
  sha256: string;
  /** Optional changelog entry — short, one-line. */
  changelog?: string;
}

const COMMON = {
  version: "TFPT 5.0",
  releaseDate: "2026-06-08",
};

export const RELEASE_ASSETS: Record<string, ReleaseAsset> = {
  "/papers/introduction.pdf": {
    href: "/papers/introduction.pdf",
    ...COMMON,
    bytes: 918742,
    sha256:
      "2525f3e28d68bdbc5125ec7f750394b0a425952d270783bd9b98095ff84ceb1f",
    changelog:
      "Compiler-closure reading guide: two axioms, the dependency DAG, the predictions and the proof ledger.",
  },
  "/papers/tfpt_1_architecture_e8.pdf": {
    href: "/papers/tfpt_1_architecture_e8.pdf",
    ...COMMON,
    bytes: 979727,
    sha256:
      "7fa3293077ecd57ac8817668c38dda581ef21a10be5e7a14dd416ff29b95674b",
    changelog:
      "Architecture: the two axioms, the D₅ × A₃ → E₈ construction, and the EM fixed point with existence + uniqueness.",
  },
  "/papers/tfpt_2_standard_model.pdf": {
    href: "/papers/tfpt_2_standard_model.pdf",
    ...COMMON,
    bytes: 1016638,
    sha256:
      "f4cc00e56d40198f9f1d3d1601859db49ffc2e85168b70f6d358dc2701f9272d",
    changelog:
      "The Standard Model in one φ₀-ladder, the flavor residue matrix, and the derived solar angle θ₁₂.",
  },
  "/papers/tfpt_3_e8_audit_bootstrap.pdf": {
    href: "/papers/tfpt_3_e8_audit_bootstrap.pdf",
    ...COMMON,
    bytes: 797592,
    sha256:
      "d181630cf796bbd29e845138c5e173494d102f3aad6055eadf1d0d1a63b0b175",
    changelog:
      "The seven E₈ slices as an audit raster, the cascade bridge, and the Möbius bootstrap.",
  },
  "/papers/tfpt_4_frontier.pdf": {
    href: "/papers/tfpt_4_frontier.pdf",
    ...COMMON,
    bytes: 537439,
    sha256:
      "11bb2cc70c729652f1c3e772dfa542227ea7c3811fab0fb3ad6ba9e4c48b79c6",
    changelog:
      "Honest status of η_B, m_p/m_e, Koide, dark matter and full quantum gravity — not forced onto the ladder.",
  },
  "/papers/tfpt_horizon_readouts.pdf": {
    href: "/papers/tfpt_horizon_readouts.pdf",
    ...COMMON,
    bytes: 717028,
    sha256:
      "9834bfad04fac6fa6617bc998f283054c7d3cb9183586f15505d81e9457789f0",
    changelog:
      "Appendix H — the horizon unit system: c₃ = 1/(8π) as the universal horizon thermal code.",
  },
  "/papers/origin_theory.pdf": {
    href: "/papers/origin_theory.pdf",
    ...COMMON,
    bytes: 733522,
    sha256:
      "e37357b065ec8c7471c12af5819c91fc68cc5c9127109a88b714a5b27e96c3f6",
    changelog:
      "Origin Theory: the (5,3) skeleton, the triply-forced 8, the order-30 Coxeter cycle, and the gapped unique attractor.",
  },
  "/papers/tfpt_research_contracts.pdf": {
    href: "/papers/tfpt_research_contracts.pdf",
    ...COMMON,
    bytes: 706726,
    sha256:
      "6f38ae85f03d7452b03f078613c27c0cc8a83a040da36134115e9b527ef3112b",
    changelog:
      "Research contracts for the two open gates: (U_wall) flavor wall-selection and (G_metric) the QG measure.",
  },
};

export function getReleaseAsset(href: string): ReleaseAsset | undefined {
  return RELEASE_ASSETS[href];
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export function formatHashShort(sha256: string): string {
  return `${sha256.slice(0, 8)}…${sha256.slice(-4)}`;
}

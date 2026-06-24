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
  version: "TFPT 5.3",
  releaseDate: "2026-06-24",
};

export const RELEASE_ASSETS: Record<string, ReleaseAsset> = {
  "/papers/introduction.pdf": {
    href: "/papers/introduction.pdf",
    ...COMMON,
    bytes: 2072025,
    sha256:
      "deaf7d02e66626bd4bf63a4996fca8a8dc45311fa8f2b01adc2af92b12e8c2aa",
    changelog:
      "Compiler-closure reading guide: two axioms, the dependency DAG, the predictions and the proof ledger.",
  },
  "/papers/tfpt_1_architecture_e8.pdf": {
    href: "/papers/tfpt_1_architecture_e8.pdf",
    ...COMMON,
    bytes: 1098530,
    sha256:
      "f6854471dff10b83e00985609956d3cc0760c0fb0c5f69a5b6635f6ece4ce300",
    changelog:
      "Architecture: the two axioms, the D₅ × A₃ → E₈ construction, and the EM fixed point with existence + uniqueness.",
  },
  "/papers/tfpt_2_standard_model.pdf": {
    href: "/papers/tfpt_2_standard_model.pdf",
    ...COMMON,
    bytes: 1176018,
    sha256:
      "2d039cc09c9bd48ff18075c3b0b2c3f73c4fb5762a1531c26f2719a6878660c5",
    changelog:
      "The Standard Model in one φ₀-ladder, the flavor residue matrix, and the derived solar angle θ₁₂.",
  },
  "/papers/tfpt_3_e8_audit_bootstrap.pdf": {
    href: "/papers/tfpt_3_e8_audit_bootstrap.pdf",
    ...COMMON,
    bytes: 917628,
    sha256:
      "2a8ac103461e65674d2d02e5d0bb5c38fa6f28e07759a4e1347f3b640a0ac46a",
    changelog:
      "The seven E₈ slices as an audit raster, the cascade bridge, and the Möbius bootstrap.",
  },
  "/papers/tfpt_4_frontier.pdf": {
    href: "/papers/tfpt_4_frontier.pdf",
    ...COMMON,
    bytes: 791574,
    sha256:
      "4028375bce778be5400f0a01615273e83e59154c5c6b966ae563a00dbcd4b10c",
    changelog:
      "Honest status of η_B, m_p/m_e, Koide, dark matter and full quantum gravity — not forced onto the ladder.",
  },
  "/papers/tfpt_horizon_readouts.pdf": {
    href: "/papers/tfpt_horizon_readouts.pdf",
    ...COMMON,
    bytes: 890523,
    sha256:
      "5e260b9ae58b69b81577be7f864b78c75cb9c587ee611a12f8ff195bd95582f6",
    changelog:
      "Appendix H — the horizon unit system: c₃ = 1/(8π) as the universal horizon thermal code.",
  },
  "/papers/origin_theory.pdf": {
    href: "/papers/origin_theory.pdf",
    ...COMMON,
    bytes: 1063420,
    sha256:
      "375435401d13432b4af86c64a257337f88117a61f389337133faeed425a3797b",
    changelog:
      "Origin Theory: the (5,3) skeleton, the triply-forced 8, the order-30 Coxeter cycle, and the gapped unique attractor.",
  },
  "/papers/tfpt_research_contracts.pdf": {
    href: "/papers/tfpt_research_contracts.pdf",
    ...COMMON,
    bytes: 1355082,
    sha256:
      "111161a314e80039e3bdd1a93195f06825d3729ba27d3174f55c8950781f10de",
    changelog:
      "Research contracts for the remaining interfaces: v_geo (scale anchor, [O]), G_net (metric inclusion, [C] closed modulo cited theorems), F_transfer (downstream transport, typed runnable solvers [C]).",
  },
  "/papers/tfpt_5_redteam.pdf": {
    href: "/papers/tfpt_5_redteam.pdf",
    ...COMMON,
    bytes: 776741,
    sha256:
      "d6031747a0648e70566d1492b9c9638ceedd33a99e4185aa3df2b0b2fea74792",
    changelog:
      "The adversarial audit: Targets A–E, what survives, what each target reduces to, and the kill tests.",
  },
  "/papers/changelog.pdf": {
    href: "/papers/changelog.pdf",
    ...COMMON,
    bytes: 1023116,
    sha256:
      "ea292bcfd60b4972412425db43dc06b898c29cf101530ea6dba1d035e6937546",
    changelog:
      "The canonical dated changelog of every change to the theory, the suite, the papers and the website.",
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

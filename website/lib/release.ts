/**
 * Release metadata for the published PDFs. The version, release date, byte
 * size, and SHA-256 hash are written here so reviewers can verify integrity
 * and tell two snapshots apart without opening the file.
 *
 * To regenerate these values after a re-build:
 *
 *   pnpm run release:hashes  (or)  npm run release:hashes
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
  version: "TFPT 4.5",
  releaseDate: "2026-04-27",
};

export const RELEASE_ASSETS: Record<string, ReleaseAsset> = {
  "/papers/00_orientation_note.pdf": {
    href: "/papers/00_orientation_note.pdf",
    ...COMMON,
    bytes: 291651,
    sha256:
      "3a4f9ed654c23427e0ac19ca9bf88c1099a536e032c437342ff454153dd7a552",
    changelog: "Orientation map updated to reflect 4.5 series terminology.",
  },
  "/papers/01_boundary_kernel.pdf": {
    href: "/papers/01_boundary_kernel.pdf",
    ...COMMON,
    bytes: 326384,
    sha256:
      "e5e17cd615088f3bf0b1ceff5b33bf6efb1556445ff038ffeab27a12240500f0",
  },
  "/papers/02_carrier_rigidity.pdf": {
    href: "/papers/02_carrier_rigidity.pdf",
    ...COMMON,
    bytes: 405267,
    sha256:
      "506437119d7f198118ac958cc78ec63b05894937ecddac0425648b21e4f0004f",
  },
  "/papers/03_em_closure.pdf": {
    href: "/papers/03_em_closure.pdf",
    ...COMMON,
    bytes: 387201,
    sha256:
      "d678e9d0fbb4edde6ed6136d5fdc72990f166d056ef7c5c20208fda0e20041ed",
    changelog:
      "Added UFE bridge for the birefringence seed and the achromatic dyonic intercept remark β_BH(r).",
  },
  "/papers/04_admissibility_qft.pdf": {
    href: "/papers/04_admissibility_qft.pdf",
    ...COMMON,
    bytes: 394606,
    sha256:
      "27ab3e60b3081d759ab12ebc7290d02bbf5beef0523e413383fc23a741aaf60d",
  },
  "/papers/05_metrology.pdf": {
    href: "/papers/05_metrology.pdf",
    ...COMMON,
    bytes: 326418,
    sha256:
      "595f63badbcf64ef74f43bf628ddd922c1d50a35a56325d471cf4a9a0ac30699",
    changelog:
      "Added the Einstein-limit normalizer ξ = c₃/φ₀ as a compression identity.",
  },
  "/papers/06_cosmology.pdf": {
    href: "/papers/06_cosmology.pdf",
    ...COMMON,
    bytes: 270246,
    sha256:
      "390307bcb5283f01e71dfe28d3ed8071e99cee0266ad4fb944ed8cbce293264e",
  },
  "/papers/coverage_audit.pdf": {
    href: "/papers/coverage_audit.pdf",
    ...COMMON,
    bytes: 102401,
    sha256:
      "179c709429ecbc5d42fd660b7956e161193fe264f5634855258628fe29f6d868",
  },
  "/papers/series_index.pdf": {
    href: "/papers/series_index.pdf",
    ...COMMON,
    bytes: 102428,
    sha256:
      "ba9cd6c801f20263deb27c60f39881400e27e5e3a1a186818819b608634e4f9d",
  },
  "/papers/technical_companion.pdf": {
    href: "/papers/technical_companion.pdf",
    ...COMMON,
    bytes: 516649,
    sha256:
      "ecf1ed4597efe622ee966c2487bf23e98945ee008f440f17f8cb610fc0534326",
    changelog:
      "Added the dyonic calibration lemma with horizon-shift sign correction and the external RG-fingerprint protocol.",
  },
  "/papers/theory_map.pdf": {
    href: "/papers/theory_map.pdf",
    ...COMMON,
    bytes: 123614,
    sha256:
      "83b99fea8ff088dffcfa956b532a0b7080389bcf898495a104ee13411089286c",
  },
  "/predictions/tfpt_prediction_alpha_em_closure.pdf": {
    href: "/predictions/tfpt_prediction_alpha_em_closure.pdf",
    ...COMMON,
    bytes: 137631,
    sha256:
      "38ab64ce33915f8ce8cb6502f2964885315a3756ed549319c3b4612e0cd78ac4",
  },
  "/predictions/tfpt_prediction_alpha_mz_scheme.pdf": {
    href: "/predictions/tfpt_prediction_alpha_mz_scheme.pdf",
    ...COMMON,
    bytes: 126262,
    sha256:
      "3372201bccbcc3dd0bb38d340d401945a0571ddc5cde786eaa615f5bb8b55699",
  },
  "/predictions/tfpt_prediction_axion_haloscope_window.pdf": {
    href: "/predictions/tfpt_prediction_axion_haloscope_window.pdf",
    ...COMMON,
    bytes: 135390,
    sha256:
      "bb3e4dcda20e332b89e55a8e88516fe7b32200bc5403605b39d46369f811065a",
  },
  "/predictions/tfpt_prediction_birefringence_beta.pdf": {
    href: "/predictions/tfpt_prediction_birefringence_beta.pdf",
    ...COMMON,
    bytes: 126201,
    sha256:
      "c001318c942e33a6b79bdaf167f762bc60963d56b914d37d421c9cfd46eb251d",
  },
  "/predictions/tfpt_prediction_ckm_phase.pdf": {
    href: "/predictions/tfpt_prediction_ckm_phase.pdf",
    ...COMMON,
    bytes: 127405,
    sha256:
      "e6ac37ab5e091262dab199724389a5dff52aae9ece025ebcdde6c11b4b731c6f",
  },
  "/predictions/tfpt_prediction_eht_achromatic_intercept.pdf": {
    href: "/predictions/tfpt_prediction_eht_achromatic_intercept.pdf",
    ...COMMON,
    bytes: 147739,
    sha256:
      "f435495e934b5539f9cd900eab7caf32ea44ffb3ffc80b0403a8b0fcf46b744e",
    changelog:
      "Initial release: achromatic residual intercept protocol for EHT/ngEHT polarimetry.",
  },
  "/predictions/tfpt_prediction_eta_b_leptogenesis.pdf": {
    href: "/predictions/tfpt_prediction_eta_b_leptogenesis.pdf",
    ...COMMON,
    bytes: 128766,
    sha256:
      "57aba21cc040b8d1215b9d1c1ee942698769bb281390c3d018ca8056500ef94c",
  },
  "/predictions/tfpt_prediction_lambda_c_cabibbo.pdf": {
    href: "/predictions/tfpt_prediction_lambda_c_cabibbo.pdf",
    ...COMMON,
    bytes: 135921,
    sha256:
      "9f1304ff8aaa2388a44ce95a8a2e9ed990a034cfee898acf2625956ca06a7f8b",
  },
  "/predictions/tfpt_prediction_neutrino_sum.pdf": {
    href: "/predictions/tfpt_prediction_neutrino_sum.pdf",
    ...COMMON,
    bytes: 124592,
    sha256:
      "ba062b9d6fc5c882f47389eba10bc9f0473a666a29857370d9693610dd649ebb",
  },
  "/predictions/tfpt_prediction_neutrinoless_double_beta.pdf": {
    href: "/predictions/tfpt_prediction_neutrinoless_double_beta.pdf",
    ...COMMON,
    bytes: 134103,
    sha256:
      "ec1fec5b68c6517c908060959686b4edfa79fd5329155b71f73e0bb69caa7135",
  },
  "/predictions/tfpt_prediction_no_second_higgs.pdf": {
    href: "/predictions/tfpt_prediction_no_second_higgs.pdf",
    ...COMMON,
    bytes: 125298,
    sha256:
      "36890b9f3e5e46b6d8cf826ebeb35280a42aa7f9414b1d8bbc7bc285d1393c56",
  },
  "/predictions/tfpt_prediction_omega_b_cosmology.pdf": {
    href: "/predictions/tfpt_prediction_omega_b_cosmology.pdf",
    ...COMMON,
    bytes: 127147,
    sha256:
      "912f6f168a642848064f9d567cdc1312a333d211561e5464fb9f6057291611d8",
  },
  "/predictions/tfpt_prediction_pi0_hadronic.pdf": {
    href: "/predictions/tfpt_prediction_pi0_hadronic.pdf",
    ...COMMON,
    bytes: 125842,
    sha256:
      "be5d57e18c4b175fd4590057c8a48452dbe2dec71c4a7ee94170f199df74604f",
  },
  "/predictions/tfpt_prediction_pmns_phase_octant.pdf": {
    href: "/predictions/tfpt_prediction_pmns_phase_octant.pdf",
    ...COMMON,
    bytes: 126325,
    sha256:
      "9f80a5514065e0e07405668daba20a7650f17f5f5c90dc29d65cacc92ef95f4c",
  },
  "/predictions/tfpt_prediction_rare_kaons.pdf": {
    href: "/predictions/tfpt_prediction_rare_kaons.pdf",
    ...COMMON,
    bytes: 124810,
    sha256:
      "28f6d147bdcab5be9bc5954d069da9acbb205c71798bdab07f4fd468f68f1f63",
  },
  "/predictions/tfpt_prediction_strong_cp_edm_null.pdf": {
    href: "/predictions/tfpt_prediction_strong_cp_edm_null.pdf",
    ...COMMON,
    bytes: 126293,
    sha256:
      "1a2422981a730f07751db64bc95da09d2e6bdf56b3a5d0c22ae14abd34dd7021",
  },
  "/predictions/tfpt_prediction_theta13_neutrino.pdf": {
    href: "/predictions/tfpt_prediction_theta13_neutrino.pdf",
    ...COMMON,
    bytes: 126613,
    sha256:
      "1ad92e70e901ab4e878421144fabdb9b12b3d39dc0d37551fd18e8c904a861f1",
  },
  "/predictions/tfpt_two_page_summary.pdf": {
    href: "/predictions/tfpt_two_page_summary.pdf",
    ...COMMON,
    bytes: 119855,
    sha256:
      "3db298e8bd8f34b399fb5360e35c334e040ba70b7296960a893f2a39747710b7",
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

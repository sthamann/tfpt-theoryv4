/**
 * Shared KaTeX macros for every math surface on the site (mirror of the
 * document-set macros in tfpt_style.tex / the changelog.tex standalone
 * preamble). Without these, any formula copied from the papers that uses
 * \gcar, \Nfam, \cthree, … renders as a red KaTeX error.
 *
 * Keep in sync with CHANGELOG_MACROS in the generated lib/changelog.ts
 * (verification/make_changelog_web.py) — this map exists separately so client
 * components do not have to import the multi-MB changelog data.
 */
export const TFPT_KATEX_MACROS: Record<string, string> = {
  "\\cthree": "c_3",
  "\\phiz": "\\varphi_0^{\\mathrm{ret}}",
  "\\gcar": "g_{\\mathrm{car}}",
  "\\Nfam": "N_{\\mathrm{fam}}",
  "\\Oadm": "\\Omega_{\\mathrm{adm}}",
  "\\ainv": "\\alpha^{-1}",
  "\\Mbar": "\\bar M_{\\mathrm{Pl}}",
  "\\Mpl": "M_{\\mathrm{Pl}}",
  "\\Z": "\\mathbb{Z}",
  "\\PP": "\\mathbb{P}",
};

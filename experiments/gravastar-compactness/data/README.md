# Data — gravastar / ECO compactness leg

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. Reproducible from `measurements.json` (no blobs).

## `measurements.json`

- **External result** — Jampolski & Rezzolla 2026, "Formation of gravastars"
  (arXiv:2509.15302): a dynamical Einstein solution in which a de Sitter core nucleates in a
  collapsing dust ball and balances gravity into a **gravastar**, with a **maximum initial
  compactness `C = 3/8`** above which collapse to a black hole is unavoidable; the
  Schwarzschild horizon is at `C = 1/2`.
- **TFPT prediction** — Nariai geometric quotient `Q_geom = 3/8` (Koide-form quotient of the
  three horizon roots at the maximal de Sitter–black-hole state, `horizon_readouts`/`v57`),
  pure de Sitter limit `1/2`. ECO echo amplitude bounded by the recovery reflectivity
  `(2/3)⁶ = 64/729` (same kernel as `gw-ringdown-echo`).
- **Compactness landmarks** — photon sphere `1/3` (light-trapping threshold), Buchdahl `4/9`,
  horizon `1/2`. Convention `C = GM/(Rc²)`.
- **Masses** — GW150914 / GW190521 remnants, a 30 M☉ template, plus M87\* and Sgr A\* (for
  the shadow note). `GM_sun/c³ = 4.9255×10⁻⁶ s`.

All values are published/derived constants; nothing is fit.

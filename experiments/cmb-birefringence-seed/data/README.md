# Data — CMB seed-line test

All values are **published summary statistics** transcribed from the cited
refereed papers / preprints (no raw map or chain is needed for a line test on
two scalar posteriors). `measurements.json` is the single source.

## Cosmic birefringence `β`

| experiment | β (deg) | reference |
|---|---|---|
| ACT DR6 (Diego-Palazuelos & Komatsu 2025) | 0.215 ± 0.074 | arXiv:2509.13654 |
| Planck PR4 (Eskilt & Komatsu 2022) | 0.30 ± 0.11 | arXiv:2205.13962 |

ACT DR6 is the primary (most recent, EB+TB with optics-model miscalibration priors;
2.9σ from zero). The authors explicitly flag unresolved systematics, so this is a
consistency input, not a clean detection.

## Baryon fraction `Ω_b`

| probe | Ω_b | reference |
|---|---|---|
| Planck 2018 (TT,TE,EE+lowE+lensing) | 0.0493 ± 0.0009 | Planck 2018 VI, A&A 641 A6 |
| BBN + primordial D/H | 0.0489 ± 0.0012 | PDG 2024 BBN review; Cooke+ 2018 |

`Ω_b` from `Ω_b h²` with `h = 0.6736`. The BBN value is independent of the CMB and
lands essentially on the TFPT prediction (0.04894).

## Provenance / refresh

The ACT DR6 and NA62/g-2 numbers were confirmed against the live sources on
2026-06-15 (web). No large data product is downloaded; the test consumes only the
two posterior summaries.

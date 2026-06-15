# Data — dark-energy w watchdog

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. No downloaded blobs — `measurements.json` holds published
DESI DR2 CPL `w0-wa` summary values. Reproducible from this file.

## `measurements.json` — DESI DR2 (2025) CPL combinations

DESI DR2 BAO + CMB + **one supernova compilation at a time** (arXiv:2503.14738):

| combination | w0 | wa | published σ vs ΛCDM | SN family |
|---|---|---|---|---|
| DESI+CMB+Pantheon+ | −0.838 ± 0.055 | −0.62 ± 0.205 | 2.8σ | Pantheon+ |
| DESI+CMB+Union3 | −0.667 ± 0.088 | −1.09 ± 0.29 | 3.8σ | Union3 |
| DESI+CMB+DES-SN5YR | −0.752 ± 0.057 | −0.86 ± 0.21 | 4.2σ | DES-SN5YR |

`rho_w0_wa ≈ −0.9` is the published-typical CPL correlation; with it the 2-D Mahalanobis
distance of the TFPT point `(w0,wa)=(−1,0)` reproduces the published significances to ~0.2σ.

## Overlap caveat (the whole point of the watchdog)

Pantheon+, Union3 and DES-SN5YR **share low-z supernovae** — they are *alternative*
datasets, not independent. The watchdog therefore reports the **strongest single**
overlap-aware combination as the headline and never multiplies/stacks the three (a naive
`sqrt(Σσ²)` would manufacture a spurious >5σ). Confirmed on 2026-06-15.

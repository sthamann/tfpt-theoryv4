# Data — shared-seed stress test

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. No downloaded blobs — `measurements.json` holds four
published values from **independent pipelines** (so the seed legs are not all the same
measurement). Reproducible from this file.

## `measurements.json` — the four seed legs

| leg | value | pipeline | source / where to get it |
|---|---|---|---|
| `β` (deg) | 0.215 ± 0.074 | CMB | ACT DR6, arXiv:2509.13654 |
| `Ω_b h²` (+ `h`=0.6736) | 0.02218 ± 0.00055 | BBN (CMB-independent) | PDG/Cooke+2018 D/H |
| `sin²θ13` | 0.02195 ± 0.00058 | reactor | NuFIT 6.0 |
| `λ` = \|V_us\| (Cabibbo) | 0.22431 ± 0.00085 | CKM | PDG 2024 |

Each leg is inverted to the implied seed `φ₀`; joint fit + leave-one-out + dominant pull
in `src/tfpt_seed/cli.py`. Confirmed on 2026-06-15.

# Data — GW ringdown spectroscopy (QNM ln3)

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. No downloaded blobs — `measurements.json` holds a few
published ringdown parameters of loud events. Reproducible from this file.

## `measurements.json` — ringdown events

| event | M_final (M☉) | spin a_f | f₂₂₀ (Hz) | source / where to get it |
|---|---|---|---|---|
| GW150914 | 62.0 | 0.67 | 251 | Abbott+ 2016; Isi+ 2019 ringdown |
| GW250114 | 63.0 | 0.68 | 248 | GWTC-5.0 (loudest BBH, SNR 78.6); f₂₂₀ indicative |

`f₂₂₀` is the **measured n=0 fundamental**; the TFPT/Hod signature `ω_R/T_H → ln3 = ln N_fam`
lives in the **high-overtone (n→∞)** limit, so the family-count test is **data-limited**
(needs high-overtone spectroscopy). Logic in `src/tfpt_ringdown/cli.py`. Confirmed 2026-06-15.

# Data — Higgs criticality

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. No downloaded blobs.

## `measurements.json` — Buttazzo et al. 2013 (arXiv:1307.3536) NNLO fit

The Planck-scale couplings are the published linear fits (eq. 61) in the input pole masses:

```
lambda(M_Pl) = -0.0143 - 0.0066 (M_t-173.34) + 0.0018 (alpha_s-0.1184)/0.0007 + 0.0029 (M_h-125.15)
g1(M_Pl)     =  0.6154 + ...     g2 = 0.5055     g3 = 0.4873 + ...     yt = 0.3825 + ...
```

Inputs (and 1σ): `M_t = 173.34 ± 0.76 ± 0.3`, `M_h = 125.15 ± 0.24`, `α_s(M_Z) = 0.1184 ±
0.0007`, `M_W = 80.384 ± 0.014` GeV. `β_λ(M_Pl)` is computed at 1-loop from these couplings
(`g1` GUT-normalised, `g_Y = √(3/5) g1`). Absolute stability is excluded at 2.8σ (eq. 65).
Confirmed 2026-06-15.

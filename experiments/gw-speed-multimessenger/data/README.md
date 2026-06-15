# Data — GW speed (v_GW = c)

`data/` is **gitignored** (`data/*`); only this `README.md` and the hand-authored
`measurements.json` are tracked. No downloaded blobs — `measurements.json` holds the
published GW170817 multimessenger numbers. Reproducible from this file.

## `measurements.json` — GW170817 + GRB170817A

| quantity | value | source / where to get it |
|---|---|---|
| `Δt` (GRB after merger) | 1.74 ± 0.05 s | Abbott+ 2017, ApJL 848 L13 |
| distance | ~40 Mpc | NGC 4993 (Abbott+ 2017) |
| emission window | [0, 10] s | Abbott+ 2017 modelling |
| published bound `(v_GW−c)/c` | [−3×10⁻¹⁵, +7×10⁻¹⁶] | Abbott+ 2017 (LIGO/Virgo + Fermi-GBM/INTEGRAL) |

TFPT predicts `(v_GW−c)/c = 0` exactly (single Lorentz cone); the test (in
`src/tfpt_gwspeed/cli.py`) checks 0 lies inside the bound. Confirmed on 2026-06-15.

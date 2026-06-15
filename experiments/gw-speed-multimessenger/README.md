# TFPT `v_GW = c` — multimessenger null test (GW170817)

TFPT predicts a **single Lorentz cone** shared by EM, gravity and massless modes, so
`(v_GW − c)/c = 0` exactly (`horizon_readouts`; a **named falsifier** — a measured
`v_GW ≠ c` would break the gravity closure). This is the gravity analog of FRB.01
(Type-5 null signature).

## Result

GW170817 + GRB170817A (Abbott+ 2017, ApJL 848 L13): the GRB arrived 1.74 s after the
BNS merger over ~40 Mpc → published bound `−3×10⁻¹⁵ ≤ (v_GW−c)/c ≤ +7×10⁻¹⁶`. The TFPT
value `0` sits inside the bound → **consistency (kill-test passed)**. Not a detection —
standard GR predicts the same; the value is its falsification surface.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-gwspeed analyze    # or: PYTHONPATH=src python -m tfpt_gwspeed.cli analyze
```

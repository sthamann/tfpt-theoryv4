# TFPT mixing angles — PMNS (θ12/θ13/θ23) + CKM δ

Compiler-level **predictions of record** (the most belastbar tier — sharper than the
FRB/GW search targets), all from `c₃`/`φ₀`:

```
sin²θ12 = 1/3 − φ0/2     = 0.306747      (TBM + seam misalignment)
sin²θ13 = φ0·e^(−5/6)    = 0.0231        (seed × carrier-trace)
sin²θ23 = 1/2                            (μτ-symmetric; octant not selected)
δ_CKM   = π/3 + 3λ²      = 68.65°        (CKM CP phase; frozen of record, canonical v88)
```

## Result (deterministic; published global fits in `data/measurements.json`)

| observable | TFPT | data | pull |
|---|---|---|---|
| sin²θ12 | 0.306747 | NuFIT 6.0 0.307±0.012 | **−0.02σ** |
| sin²θ12 | 0.306747 | JUNO 0.3092±0.0087 | −0.28σ |
| sin²θ13 | 0.0231 | NuFIT 6.0 0.02195±0.00058 | **+2.0σ** (mild tension) |
| sin²θ23 | 0.5 | NuFIT 6.0 0.470±0.017 | +1.76σ (octant open) |
| δ_CKM | 68.65° | LHCb γ 64.6°±2.8 | +1.45σ |

→ **θ12 is a sharp hit** (essentially on NuFIT/JUNO); **θ13 carries the known ~2σ
tension** (the one place TFPT is pulled); θ23 consistent with maximal (octant
ambiguous); the CKM δ is consistent with the LHCb γ. `θ12/θ13/θ23` are PMNS predictions
of record; `δ_CKM` is the CKM phase (different sector). θ13 shares the seed `φ0` with the
CMB birefringence (see `cmb-birefringence-seed` shared-seed test).

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-neutrino analyze    # or: PYTHONPATH=src python -m tfpt_neutrino.cli analyze
```

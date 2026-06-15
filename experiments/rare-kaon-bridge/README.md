# rare-kaon-bridge — the flavour bridge as a *geometry*

**Status: `consistent` (3/5 direct legs) + `data_limited` (R_K, BR(KL) wait for KOTO).**

Instead of celebrating one lucky `BR(K⁺→π⁺νν)` number, this tests the whole TFPT flavour
bridge as a geometric object:

| leg | TFPT | data | result |
|---|---|---|---|
| `BR(K⁺→π⁺νν)` | 9.45×10⁻¹¹ | NA62 (9.6⁺¹·⁹₋₁.₈)×10⁻¹¹ | −0.08σ ✓ |
| `BR(KL→π⁰νν)` | 3.33×10⁻¹¹ | KOTO < 2.2×10⁻⁹ (90% CL) | below limit (data_limited) |
| `R_K = BR(KL)/BR(K⁺)` | **0.35238** | (KOTO-II) | respects Grossman-Nir, near SM 0.40 (data_limited) |
| `δ_CKM / γ` | 68.65° (π/3+3λ²) | LHCb γ 64.6°±2.8° | +1.45σ ✓ |
| Jarlskog `J` | 3.03×10⁻⁵ | PDG (3.08±0.13)×10⁻⁵ | −0.07σ ✓ |

## Why a *geometry* test

`R_K` is the robust observable: the SM short-distance function `X_t` and `|Vcb|⁴` largely
cancel in the ratio, so `R_K` probes the flavour *structure* rather than the overall scale.
TFPT's `R_K = 0.35238` is **near the SM ratio (~0.40)** and **well below the Grossman-Nir
bound (4.3)** — i.e. the structure is consistent, but not a unique fingerprint.

## Firewall (the honest typing)

This is a **downstream flavour BRIDGE [C]**, not a primitive compiler output. Only `λ`
(Cabibbo) and `δ_CKM` are TFPT predictions; `|Vcb|`, `|Vub|` and the SM short-distance
functions are **external nuisances** (used here to isolate the phase in `J`). The real
discriminator is **KOTO measuring BR(KL) → R_K**, not another `BR(K⁺)`.

## Run

```bash
cd experiments/rare-kaon-bridge && PYTHONPATH=src python3 -m tfpt_kaon.cli analyze
```

Standalone search; not in the verification suite, ledger or website.

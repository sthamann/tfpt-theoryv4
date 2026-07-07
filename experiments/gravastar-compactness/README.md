# gravastar-compactness — TFPT Nariai `3/8` ↔ gravastar max compactness `C = 3/8`

**Status: `data_limited` (suggestive normal-form match; concrete ECO echo template).**

Two independent constructions land on the **same rational** and the **same de Sitter
endpoint**:

| | transition value | de Sitter endpoint |
|---|---|---|
| TFPT Nariai `Q_geom` (`v57`) | **3/8** | 1/2 |
| Jampolski–Rezzolla 2026 max compactness (arXiv:2509.15302) | **3/8** | 1/2 |

## What the runner checks

1. **Normal-form match (honest).** `Q_geom(Nariai) = 3/8 = C_max` and both share the de
   Sitter endpoint `1/2`. This is an **exact rational coincidence with a shared endpoint**,
   *not* a proven `C ↔ Q_geom` map → typed `[C]`, suggestive (a structural echo, not an
   identity). Promoting it to a formal `verification/vN` would require the explicit map.
2. **Compactness ladder.** `1/3 < 3/8 < 4/9 < 1/2`: a `C=3/8` object sits **above** the
   photon-sphere/light-trapping threshold (`1/3`, surface at `R = 8M/3 < 3M`) and **below**
   Buchdahl (`4/9`) and the horizon (`1/2`) → a **horizonless, light-trapping ECO** — exactly
   the regime that produces ringdown **echoes**.

   *Metallic-mean structure (theory-contract cross-ref, `[C]`).* Writing the ladder via the
   sheet-index form `C(k) = (k²−1)/(6k)`, the two **classical** thresholds land exactly on the
   two smallest metallic means: `C(1+√2) = 1/3` (photon sphere = **silver** mean, index
   `n=|Z₂|=2`) and `C((3+√13)/2) = 1/2` (horizon = **bronze** mean, index `n=N_fam=3`), since
   `C(μ_n) = n/6` for the n-th metallic mean `μ_n` (root of `x²−nx−1`). The physical window
   `C ≤ 1/2` is exactly `n ≤ 3 = N_fam`; Buchdahl `4/9` and Nariai `3/8` are the **non-metallic**
   rungs in between (`6C` non-integer). Exact-arithmetic contract:
   [`theory-contracts/metallic_compactness_ladder.py`](../theory-contracts/metallic_compactness_ladder.py)
   (5/5). This is an internal ordering principle typed `[C]` (fractional/metallic replica sheets
   need the same open continuation as the `3/8 ↔ Q_geom` map) — **no new prediction, no status change**.
3. **Echo template.** Tortoise-coordinate round-trip delay (surface ↔ photon sphere) plus the
   TFPT recovery-reflectivity amplitude bound `(2/3)⁶`:

   | remnant | echo delay (Δt = 2.288 M) | amplitude ratio |
   |---|---|---|
   | GW150914 (62 M☉) | ~0.70 ms | ≤ `(2/3)⁶ = 0.0878` |
   | GW190521 (142 M☉) | ~1.60 ms | ≤ `(2/3)⁶` |
   | 30 M☉ | ~0.34 ms | ≤ `(2/3)⁶` |

   This supplies the **time scale** that [`gw-ringdown-echo`](../gw-ringdown-echo/) (which
   fixes only the amplitude ratio) was missing → a concrete `(delay, amplitude)` injection
   template for the Stage-1 strain search.

## EHT side (honest limitation)

A `C=3/8` horizonless object still has a photon sphere, so its shadow critical impact
parameter `b_c = 3√3 M` is **degenerate with a Kerr black hole** — EHT **shadow size cannot
discriminate** it. The discriminator is the central brightness depth (horizonless → faint
inner flux) and, primarily, **GW echoes**.

## Frozen kill rule

```
a C=3/8 horizonless echo with amplitude damping (2/3)^6 and the predicted ms-scale delay,
excluded across high-ringdown-SNR events -> the ECO/gravastar reading of the seam falls.
```

## Run

```bash
cd experiments/gravastar-compactness && PYTHONPATH=src python3 -m tfpt_gravastar.cli analyze
```

## Firewall

Standalone search. Not in the verification suite, ledger, or website; no load-bearing claim.
The `3/8` match is `[C]` (suggestive), and the ECO echo is a search template, not a detection.

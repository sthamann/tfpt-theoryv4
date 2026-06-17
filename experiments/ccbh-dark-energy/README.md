# ccbh-dark-energy — TFPT `k = 3 → w = −1` cosmological-coupling leg

**Status: `data_limited` (consistent-but-contested downstream bridge).**

TFPT reads a black hole as the **local** realization of the seam and de Sitter as the
**global** one; the maximal de Sitter–black-hole (**Nariai**) state sits on the anchor
`(1,1,−2)` and obeys the exact identity `S_dS · ρ_Λ = 32π⁴`. So the seam black-hole
interior **is** the de Sitter vacuum — interior equation of state `w_in = −1`.

Croker & Weiner (2019) show a cosmologically coupled compact object gains mass
`M(a) ∝ a^k` with `k = −3 w_in`, so the population density scales `ρ ∝ a^(k−3)` with
`w_eff = −k/3`. Therefore:

```
w_in = −1   ⇒   k = −3·w_in = 3 (exactly)   ⇒   w_eff = −1   (true cosmological constant)
```

This is the **mechanism** behind the `w = −1` that [`dark-energy-w-watchdog`](../dark-energy-w-watchdog/)
confronts with DESI — the two are **alternative readings** of one question (is dark energy
a constant Λ?) and must **not** be double-counted (`alternative_group = w_de_eos`).

## Confrontation

| leg | TFPT | data | pull |
|---|---|---|---|
| coupling index `k` | `3` (exact) | Farrah+2023 `k = 3.11 ± 0.79` | **−0.14σ** |
| pop. EoS `w_eff = −k/3` | `−1` | `−1.04 ± 0.26` | +0.14σ |
| density closure `Ω_de` | `0.68` (CCBH, k=3) | Planck `Ω_Λ = 0.6889` | order-consistent (contested) |

## Why `data_limited`, not a hit

The coupling index agrees with TFPT `k=3` at face value, **but the CCBH-as-dark-energy
interpretation is disputed**: Lacy+2024, Amendola+2023, Andrae & El-Badry 2023 and
Mistele 2023 contest the required SMBH mass growth, whether `k=3` can be *all* of dark
energy under background-cosmology constraints, and the coupling derivation itself. So this
is a **downstream bridge**, never a confirmation; the deciding measurement is DESI `w(z)`.

## Frozen kill rule

```
a robust k != 3 at >= 3 sigma in a systematics-controlled SMBH-growth sample
-> the TFPT 'seam interior = de Sitter vacuum carrier' reading falls
   (NOT the compiler core; w=-1 can still hold via a plain Lambda).
```

## Run

```bash
cd experiments/ccbh-dark-energy && PYTHONPATH=src python3 -m tfpt_ccbh.cli analyze
```

## Firewall

Standalone search/watchdog. Not in the verification suite, ledger, or website; makes no
load-bearing TFPT claim. `k=3 ⇔ w=−1` is the TFPT cosmology branch under test, not the
compiler core.

# dark-energy-w-watchdog — TFPT `w = −1` kill watchdog

**Status: `data_limited` (watchdog armed, not triggered).**

TFPT predicts a *true* cosmological constant: `w = −1` exactly (the Λ/H₀ engine,
`S_dS · ρ_Λ = 32π⁴`). DESI DR2 (2025) reports a preference for **dynamical** dark energy in
the CPL `w0–wa` plane. This watchdog confronts the TFPT point `(w0, wa) = (−1, 0)` with the
published DESI DR2 combinations and decides whether the cosmology branch is in trouble.

## Why this is a watchdog, not a number-hunt

The reviewer's warning is baked in: **do not stack the three supernova compilations.**
Pantheon+, Union3 and DES-SN5YR overlap heavily (shared low-z SNe), so they are alternative
datasets. Combining them as if independent (`sqrt(Σσ²)`) manufactures a spurious >5σ
"discovery". The watchdog instead takes the **strongest single overlap-aware combination**
as the headline and prints the naive product only as a labelled anti-pattern.

## Method

`(w0,wa)=(−1,0)` distance from each CPL best fit via the 2-D Gaussian (Mahalanobis)
distance with the published `ρ(w0,wa) ≈ −0.9`. This reproduces the DESI DR2 significances to
~0.2σ, which validates the inputs.

## Result (2026-06-15)

| combination | 2-D distance from w=−1 | published σ |
|---|---|---|
| DESI+CMB+Pantheon+ | ~3.1σ | 2.8σ |
| DESI+CMB+Union3 | ~3.9σ | 3.8σ |
| DESI+CMB+DES-SN5YR | ~4.4σ | 4.2σ |

**Headline (overlap-aware): ~4.4σ** (DES-SN5YR). Naive product ≈ 6.6σ — *spurious, not used*.

## Frozen kill rule

```
w != -1 at >= 5 sigma in a single, systematics-controlled, overlap-aware combination
-> TFPT Lambda/H0 cosmology branch falls (NOT the compiler core).
```

Currently the strongest overlap-aware exclusion is ~4.4σ (< 5σ) and SN-sample dependent →
**armed, not triggered.** If DESI + a single controlled SN sample pushes past 5σ, the Λ/H₀
branch takes a real hit.

## Run

```bash
cd experiments/dark-energy-w-watchdog && PYTHONPATH=src python3 -m tfpt_w.cli analyze
```

## Firewall

Standalone search/watchdog. Not in the verification suite, ledger, or website. Makes no
load-bearing TFPT claim; `w=−1` is the TFPT cosmology branch under test, not the compiler core.

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

## Result (2026-06-15, frozen 2025 baseline)

| combination | 2-D distance from w=−1 | published σ |
|---|---|---|
| DESI+CMB+Pantheon+ | ~3.1σ | 2.8σ |
| DESI+CMB+Union3 | ~3.9σ | 3.8σ |
| DESI+CMB+DES-SN5YR | ~4.4σ | 4.2σ |

**Headline (overlap-aware): ~4.4σ** (DES-SN5YR). Naive product ≈ 6.6σ — *spurious, not used*.

## Status timeline — 2026-07-02 entry (recorded before DESI DR3)

TFPT predicts the evolving-DE preference **dissolves**, so the *direction* of each
update is the point of this watchdog. The 2026 status, ingested as a dated entry in
`data/measurements.json` (`status_timeline`):

1. **DES-Dovekie recalibration** (arXiv:2511.07517, MNRAS 2026): a full recalibration
   of DES-SN5YR found an input-file error — the 9 SALT3 calibration-variant weights
   were rounded to 0.3 instead of `1/√9 ≈ 0.33`, so the calibration-systematic weights
   summed to 0.81 instead of 1, **underestimating the total photometric uncertainty by
   ~20%**. With DES-Dovekie + CMB (Planck+ACT+SPT) + DESI DR2:
   `w0 = −0.803 ± 0.054`, `wa = −0.72 ± 0.21`, significance **3.2σ, down from 4.2σ**
   (≈ 5:1 Bayesian odds — the paper's own reading: *"only a weak preference for
   evolving dark energy"*).
2. **Bayesian model comparison** (Ong, Yallup & Handley, arXiv:2603.05472; Ockham /
   Jeffreys–Lindley penalty via nested-sampling evidences): the 3.1σ frequentist
   preference from **DESI DR2 + CMB alone is eliminated entirely** —
   `ln B = −0.57 ± 0.26`, modestly favouring ΛCDM. Adding the corrected Dovekie
   calibration keeps concordance (`ln B = −0.01 ± 0.27`); with the *original*
   DES-SN5YR calibration the preference survives (`ln B = +3.32`, 3.07σ) — i.e. it is
   traced to the calibration error. *"With the calibration corrected, the Bayesian
   evidence for dynamical dark energy vanishes."*
3. **What survives**: Union3-driven pulls — published frequentist 3.8σ
   (2.23σ Bayesian); Union3 has not been recalibrated.

The frozen 2025 baseline above is kept as-is (the kill machinery is unchanged); the
timeline records that its 4.2–4.4σ headline is now known to be calibration-inflated.

## Frozen kill rule

```
w != -1 at >= 5 sigma in a single, systematics-controlled, overlap-aware combination
-> TFPT Lambda/H0 cosmology branch falls (NOT the compiler core).
```

Currently the strongest overlap-aware exclusion is ~4.4σ (< 5σ) on the frozen 2025
baseline — and per the 2026 timeline entry it is known to be calibration-inflated
(corrected: 3.2σ) → **armed, not triggered.** If DESI + a single controlled SN sample
pushes past 5σ, the Λ/H₀ branch takes a real hit.

## Run

```bash
cd experiments/dark-energy-w-watchdog && PYTHONPATH=src python3 -m tfpt_w.cli analyze
```

## Firewall

Standalone search/watchdog. Not in the verification suite, ledger, or website. Makes no
load-bearing TFPT claim; `w=−1` is the TFPT cosmology branch under test, not the compiler core.

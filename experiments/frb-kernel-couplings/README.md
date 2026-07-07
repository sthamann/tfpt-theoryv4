# FRB kernel couplings — non-marginal and operator-proxy FRB axes (KC.01–06)

> **Firewall:** search targets / consistency checks on horizon-residual channels —
> **never** load-bearing, never `[E]`. A hit in any axis is escalate-only (universal-DSI
> / astrophysical coincidence stays the default reading). Preregistered in
> `hypotheses/kernel_couplings_v1.yaml` **before** any statistic ran.

The 2026-07-06 bird's-eye scan of the theory's geometry/topology found that all prior
FRB tests probed **marginals** (energy ratios alone, time structure alone),
**deck-blind** polarization invariants (PA is defined mod π — invariant under the Z₂
orientation flip; FRB.06 used |V|/I), or visible-number searches instead of operator
structure. Six structures are now tested here:

| axis | signature | derivation | status |
|---|---|---|---|
| **KC.01** | **joint energy–time tooth**: pairs on a time tooth `(3/2)^k` must sit on the partner energy tooth `(2/3)^k` (`E·t = const` along the ladder) | **forced** by the frozen kernel semantics (both ratios are eigenvalue readings of the same transfer `T`) | **NULL** (both sources) |
| **KC.02** | **V-handedness alternation**: the *sign* of circular polarization is the only deck-visible polarization observable; consecutive kernel steps flip it | exploratory (Z₂ deck reading; unforced observable coupling) | **NULL** |
| **KC.03** | **size-space DSI**: log-periodic decoration of the burst-*energy* distribution (FRB analog of pulsar PG.01) | standard DSI corollary of the mode ladder | **NULL** (both sources) |
| **KC.04** | **μ₄ phase–time helix**: `Φ = ω·ln(τ_j/τ_i) + q·2ΔPA ≈ const` for consecutive pairs, frozen ω = 2.583, q ∈ {1, 2} | exploratory (μ₄ deck reading; the deferred "Befund P3") | **NULL** |
| **KC.05** | **μ₄ block-leakage proxy**: PA-derived C4 transition operator should suppress off-character transitions | exploratory S8 proxy; transduction `B` unproven | **NULL** |
| **KC.06** | **multivariate S2a spectrum**: lag-1 operator on `(cos 2PA, sin 2PA, L/I, sign V)` should approach `{1,64/729,1/729}` | exploratory operator spectrum; not a tooth/comb scan | **NULL** |

## Data (all committed in sibling experiments; nothing fetched)

- **FRB 20121102A** — Li+2021 (Nature 598, 267), 1652 bursts, MJD + isotropic energy.
- **FRB 20220912A** — Zhang+2023 (ApJ 955, 142), 1076 bursts, barycentric MJD + energy.
- **FRB 20240114A** — FAST pol catalog v5 (Wang+2026), 6134 bursts with **signed**
  `DOC = V/I` (47% negative) — the handedness sign that FRB.04/06/08 never used.

## Results (seed 0, `results/results.json`)

- **KC.01 (2D ladder coupling): clean NULL in both sources.** 20121102A: 1569
  consecutive within-session pairs, 130 on a time tooth, **14 joint hits vs 19.5
  expected** under the energy-shuffle null (enrichment 0.72, p = 0.94); 20220912A:
  3 joint hits vs 4.4 (p = 0.84). The energy-shuffle null preserves *both* marginals
  exactly and destroys only the coupling — this is a well-powered absence of the
  ladder coupling at catalog statistics. Free-quotient control: >55% of arbitrary
  energy bases beat the kernel (nothing special at 2/3); placebo pairings comparable.
- **KC.02 (handedness alternation): NULL.** 3540 significant-handedness bursts, 3454
  consecutive pairs: alternation fraction **0.480 vs shuffle 0.497** (p = 0.98 — if
  anything, handedness *persists* slightly, consistent with magnetospheric
  propagation memory); net handedness +0.058 (balanced); tooth-gated subset too small
  (3 pairs, data-limited on that leg).
- **KC.03 (energy-distribution DSI): NULL in both sources after the 3-null battery.**
  20121102A (8.3 e-folds in ln E, 10/12 λ gated, GMM population null k=3): best member
  λ=8 raw p = 0.0185 → **Bonferroni global p = 0.185**; 20220912A (9.9 e-folds, k=2):
  global p = 0.68. The famous bimodality is fully absorbed by the population null —
  the PG.01 pulsar result replicates in the FRB energy domain.

- **KC.04 (phase–time helix, added as dated v1.1 prereg addendum before its run): NULL.**
  83 sessions, 5934 pairs with significant linear polarization (L/I ≥ 10%). The naive
  permutation null fires for q=1 (p = 0.0005) — but that is exactly the Faraday/drift
  trap the prereg anticipated: the **drift-robust circular-shift null** (preserves the
  PA autocorrelation) gives p = 0.12, and the off-kernel rank shows ω = 2.583 is **not
  special** (p = 0.37) — the concentration is slow PA drift coupled to burst clustering,
  present at *any* ω, not a kernel helix. q=2: same pattern (0.017 / 0.26 / 0.64).
  Documented limitation: PA is mod π and RM-uncorrected; an RM-corrected re-run would
  sharpen the (already null) statement.
- **KC.05 (μ₄ block-leakage proxy, v1.2 addendum): NULL.** On 6037 consecutive
  PA-class pairs from FAST 20240114A, the C4 off-character fraction is **0.4268**
  (shuffle median 0.4629, low-tail p=0.0045), but it is **not C4-specific**:
  Z3 gives 0.3677 and random unequal 4-mark partitions have median 0.3958 and
  minimum 0.015. The small shuffle p is therefore PA persistence/marking geometry,
  not a μ₄ block-protection signature.
- **KC.06 (multivariate S2a spectrum, v1.2 addendum): NULL.** The lag-1 operator on
  `(cos 2PA, sin 2PA, L/I, sign V)` uses 3447 consecutive significant-polarization
  pairs. Normalised eigenvalue magnitudes are **[1.0, 0.5066, 0.38444, 0.04781]**,
  far from `{1, 0.08779, 0.00137}`; distance 0.5676 is not unusually close relative
  to the within-session shuffle null (median 0.9305, p_close=0.1799).

**Audit note (bug caught during the run, on record):** the first pass showed a nominal
λ=8 "candidate" (global p = 0.01) in 20121102A. It was a **null-generator artefact**:
`sklearn`'s `GaussianMixture.sample()` re-seeds from its `random_state` on every call,
so all 2000 GMM null draws were *identical* (null median = null p95). The robustness
probe caught it (split-half unstable 38 vs 79; free-λ scan peaks at the range edge
λ≈56–60, not at 8). Fixed by drawing a fresh seed per null realisation; the candidate
dissolved. Exactly the failure mode the escalate-only discipline exists for.

## Reproduce

```bash
PYTHONPATH=src python -m tfpt_kc.cli     # shared venv: numpy/scipy/scikit-learn
```

## Layout

```
hypotheses/kernel_couplings_v1.yaml  # preregistered axes, nulls, controls, kill conditions
src/tfpt_kc/data.py                  # catalog loaders + sessionisation (gap > 0.2 d)
src/tfpt_kc/joint_tooth.py           # KC.01 (energy-shuffle null, placebo pairing, free-quotient LEE)
src/tfpt_kc/vsign.py                 # KC.02 (within-session sign permutation; tooth-gated secondary)
src/tfpt_kc/energy_dsi.py            # KC.03 (lognormal/KDE/GMM 3-null battery, Bonferroni)
src/tfpt_kc/helix.py                 # KC.04 (frozen-omega helix; permutation + circular-shift + off-kernel rank)
src/tfpt_kc/operator_proxy.py        # KC.05/KC.06 (mu4 block leakage + S2a lag spectrum)
results/results.json                 # committed run (seed 0)
```

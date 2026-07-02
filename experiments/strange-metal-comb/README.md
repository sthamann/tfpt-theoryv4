# Strange-metal comb — the first laboratory comb-ripple search

> **Firewall (read first):** strange metals have **no established boundary-recovery structure.**
> The `σ₁(ω/T)` master curve is a quantum-critical scaling function of a doped Mott insulator —
> **not** a horizon/boundary relaxation and **not** a geometric mode ladder — so there is **no
> a-priori reason** for `ω=2.583` here. Even a hit would be a **universal
> discrete-scale-invariance (DSI) coincidence, never TFPT confirmation** (repo firewall class).
> **A null is expected and informative.** This is a **search target / consistency check** —
> nothing here is load-bearing `[E]` or gets a `\veri{}`.

## Why strange metals (structural motivation, not a claim)

TFPT's seam temperature `T = 4c₃κ = κ/2π` is exactly the **KMS/Planckian bound**, and strange
metals dissipate at `τ = ħ/(k_B T)` **universally** — doping-independent (Michon+ 2023; the RMP
colloquium lists *why Planckian?* as an open question). That makes the strange-metal master curve
the first **laboratory** surface where the TFPT recovery comb can even be asked for. The
**discriminating question:** continuous quantum criticality predicts a **smooth** `σ₁(ω/T)`
master curve; a gapped-boundary-attractor reading would decorate it with a **log-periodic ripple
in `ln(ω/T)`** at the frozen frequency:

```
(smooth master curve) * (1 + eps cos(omega u + phi)),   u = ln(hbar*omega / k_B T)
omega = 2 pi / ln(lambda),  lambda = (3/2)^6   ->  omega = 2.5827
eps   = exp(-pi^2 / ln lambda) = 0.0173  (~1.7%, the QT.02 amplitude-suppression law)
ONE comb period = ln((3/2)^6) = 2.433 in u;  hard u-range gate >= 2.8 periods
```

All from the two axioms (`c3 = 1/(8π)`, `g_car = 5`); **no condensed-matter number enters.** The
detector (`comb.py`) is a verbatim port of the injection-validated recovery-comb detector from
`experiments/recovery-comb-domains` (kernel logic unchanged, guarded bit-for-bit by
`tests/test_frozen_kernel.py`). Preregistered in `hypotheses/strange_metal_comb_v1.yaml`
**before** any data was touched.

## Observable semantics (locked before the data pass)

- **Observable:** real optical conductivity `σ₁(ω,T)` of LSCO x=0.24, normal state.
- **Master curve:** `y = ln(T·σ₁)` vs `u = ln(ħω/k_BT)` — the paper's own Planckian ν=1 collapse
  (`σ₁ ~ T⁻¹F(ω/T)`), built with the paper's own conversion (`σ₁[kS/cm] = 0.13452·E[eV]·ε₂`),
  temperature window (T ≥ 40 K, normal state) and energy window (E ≤ 0.4 eV, below interband) —
  exactly the `fig02` analysis code shipped in the paper's open-data archive.
- **Recovery observable:** residuals `r(u) = y − smooth(u)`; the multiplicative ripple is
  **additive with amplitude ~eps** in `y` (amplitude-type observable; no energy/amplitude
  pairing ambiguity arises).
- **Detrend flexibility (documented):** primary = degree-2 polynomial in `u` (the frozen
  detector convention); variants = degree-3/4 polynomials, cubic spline with knots every 3.0 in
  `u` (wider than one comb period), and per-temperature degree-2 detrend (absorbs per-T
  calibration offsets / imperfect collapse). A hit surviving only one detrend choice would be an
  audit anomaly, not a candidate.

## Data (all public, provenance in file headers)

| Role | Dataset | Source | Status |
|---|---|---|---|
| PRIMARY | LSCO x=0.24 `ε(ω)` at 13 T (2.5 meV–5 eV) | Michon+ 2023 Nat. Commun. 14:3033 **open data**, Yareta DOI `10.26037/yareta:zvtvqwmbl5emvd3bxr6sluurqi` (CC-BY-4.0) | **obtained** (`data/lsco_x0p24_*.txt`) |
| Replication | Bi-2212 σ₁(ω,T) tables | van der Marel+ 2003 Nature 425:271 | **not publicly retrievable** (supplement has figures/methods only; underlying files were privately exchanged) → replication leg `data_limited` |
| Negative control | Au, Cu n,k tables (far-IR/IR, room T) | Ordal+ 1985/1987 via refractiveindex.info (CC0) | **obtained** (`data/{au,cu}_ordal_nk.csv`) |

## Method (preregistered tests SMC.01–SMC.07)

1. **SMC.01 kernel rank:** comb gain at `ω=2.5827` vs a dense off-kernel periodogram
   `ω ∈ [1,6]` (kernel ±10% excluded) over the detrended master curve, gated at ≥ 2.8 comb
   periods; frozen `detect_comb` rank reported alongside.
2. **SMC.02 amplitude + phase:** least-squares `ε̂, φ̂` at the fixed kernel `ω`.
3. **SMC.03 null batteries:** residual point-permutation **and** per-T cyclic-shift
   (block-style, preserves autocorrelation) — report both, use the **larger** p.
4. **SMC.04 TFPT λ-battery:** `λ ∈ {3/2, φ, 2, 3, 4, 5, 8, (3/2)⁶, 30}`, per-λ u-range+Nyquist
   gate, **Bonferroni** look-elsewhere.
5. **SMC.05 injection power:** `ε ∈ {0.0173, 0.05}` ripples injected into the **real** master
   curve (random phase), rerun per detrend variant; `ε=0` false alarm. Honest power statement.
6. **SMC.06 Drude negative control:** identical pipeline on Au/Cu — must stay quiet.
7. **SMC.07 replication:** Bi-2212 if retrievable (it is not → `data_limited`).

## Results (deterministic; `results/results.json`, seed 0)

- **Detector validated** (unchanged kernel): 96% detection at ≥2.8 periods, 0% false positive,
  range-blind below.
- **Master curve:** 11 227 points, T = 40–300 K (9 temperatures), `u` range 7.10 → **2.92 comb
  periods — clears the 2.8 gate** (barely; this is intrinsically a ~3-period surface).
- **SMC.01: `ω=2.583` is NOT special.** Primary p = **0.297**; frozen detector p = 0.248;
  variants p = 0.14–0.51 — **detrend-robust null**.
- **SMC.02/03:** `ε̂ = 0.067` at the kernel frequency, but the **conservative (per-T
  cyclic-shift) null puts the 95% amplitude floor at 0.186** — the master curve's own
  systematic wiggles (Kramers–Kronig + calibration + imperfect collapse) are **an order of
  magnitude above the predicted 1.7% ripple**. Conservative null p = 0.68. (The point-permutation
  p = 0.001 is the textbook anti-conservative artifact the prereg anticipated — autocorrelated
  smooth structure, not a comb.)
- **SMC.04 λ-battery: NULL after look-elsewhere** (Bonferroni global p = 0.063 over 8 gated
  ratios; best = the low-specificity atom λ=4 at raw p = 0.008; all idiosyncratic ratios quiet;
  λ=30 range-blind).
- **SMC.05 injection power (the honest answer):** predicted ε = 1.73% detected **0–25%**
  (best variant: spline), ε = 5% detected **0–30%**, false alarm 0% → **the published optical
  data is NOT precise enough for a 1.7% ripple test**; even 5% is marginal. The limiting factor
  is not point count (11k points) but **smooth systematic structure** in the residual field.
- **SMC.06: Drude controls quiet** (Au p = 0.33, Cu p = 0.14; both < 2.8 periods, rank
  reported) — pipeline valid.
- **SMC.07:** replication leg `data_limited` (no public Bi-2212 table).

**Verdict: `data_limited` (null at the detectable amplitude).** `ω=2.583` is not special in the
first laboratory master curve tested, robustly across detrend choices — but the search only
reliably constrains ripples well above ~5% (the conservative pooled 95% floor is ε ≈ 0.19; the
best variant detects ε = 5% only 30% of the time), far above the predicted 1.7%. The λ-battery is
a clean look-elsewhere NULL. This is exactly the prereg-expected outcome, and it is informative:
it is the **first laboratory bound on a log-periodic decoration of the Planckian ω/T master
curve at the TFPT frequency**, and it fixes what a decisive test needs — sub-% optical
calibration or a differential (multi-doping/multi-compound) collapse that cancels the
systematics. **No claim; nothing `[E]`.**

## Reproduce

```bash
source ../tfpt-discovery/.venv/bin/activate       # numpy + scipy (shared venv; do NOT pip install)
python scripts/fetch_michon2023.py                # Yareta open-data archive -> data/lsco_*
python scripts/fetch_drude_control.py             # Ordal Au/Cu n,k -> data/*_ordal_nk.csv
PYTHONPATH=src python -m tfpt_smc.cli analyze     # all tests -> results/results.json
PYTHONPATH=src python tests/test_frozen_kernel.py # kernel bit-identity guard
```

## Layout

```
hypotheses/strange_metal_comb_v1.yaml  # preregistered tests + kill conditions (frozen BEFORE data)
src/tfpt_smc/comb.py     # frozen kernel detector (verbatim port; guarded bit-for-bit)
src/tfpt_smc/master.py   # LSCO/Drude ingestion, master curve, detrends, nulls, battery, injections
src/tfpt_smc/cli.py      # `tfpt-smc analyze` -> results/results.json
scripts/fetch_michon2023.py     # Yareta DLCM API download with provenance headers
scripts/fetch_drude_control.py  # Ordal Au/Cu n,k (refractiveindex.info, CC0)
data/                    # fetched public data (provenance in each file header)
results/results.json     # committed deterministic summary
tests/test_frozen_kernel.py  # kernel + lambda-battery bit-identity vs recovery-comb-domains
```

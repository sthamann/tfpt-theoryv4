# Crust-cooling recovery comb — the floor-terminated 2nd data world

> **Firewall (read first):** neutron-star **crust cooling is surface heat diffusion**, the crust
> relaxing back to core equilibrium after an accretion outburst. It is **not** a horizon/boundary
> recovery and **not** a geometric mode ladder, so there is **no a-priori reason** for `ω=2.583`
> here. A hit would be a **universal discrete-scale-invariance (DSI) coincidence, never TFPT
> confirmation.** The sole value of this domain is as the independent **SECOND data world** the
> discriminating comb needs (`ω=2.583` replicated in ≥2 physically independent worlds). This is a
> **search target / consistency check** — nothing here is load-bearing `[E]` or gets a `\veri{}`.

The "new" TFPT dynamic signature is a **shape**: a system relaxing to a fixed point through the
frozen geometric mode ladder leaves a log-periodic (DSI) comb on its recovery curve,

```
R(t) = (smooth relaxation) * (1 + eps cos(omega ln t + phi))
omega = 2 pi / ln(lambda),  lambda = (3/2)^6   ->  omega = 2.583
eps  ~ exp(-pi^2 / ln lambda) ~ 0.017  (~2%, the QT.02 amplitude-suppression law)
ONE comb period = ln((3/2)^6) = 2.433 in ln t;  hard wall at N_fam = 3;  protected floor w0 > 0
```

All from the two axioms (`c3 = 1/(8π)`, `g_car = 5`); **no neutron-star number enters**. The
detector (`comb.py`) is a self-contained port of the injection-validated log-periodic comb detector
from `experiments/recovery-comb-domains` and `experiments/pulsar-glitch-recovery` (kernel logic
unchanged).

## Why crust cooling

Crust cooling is the **cleanest floor-terminated relaxation-to-attractor in nature outside the
horizon.** A quasi-persistent LMXB transient accretes for years–decades, heating the crust out of
thermal equilibrium; when the outburst ends the surface temperature `kT_eff(t)` relaxes back to the
**nonzero core-equilibrium floor** over ~5–30 yr, monitored by Chandra/XMM/NICER. That protected
floor (crust → nonzero core equilibrium, the well-known *"cooling curves cannot be fit without a
constant offset"* fact) is a natural — if generic — test of the TFPT protected floor `w0`.

## Observable semantics (locked before the data pass)

- **Observable:** redshift-corrected effective surface temperature `kT_eff∞(t)` (eV) vs **time since
  the end of the outburst** (relaxation onset `t0`). (Thermal luminosity `L_x` is equivalent up to a
  Stefan–Boltzmann power; not used.)
- **Recovery observable:** `y = ln(kT_eff)`. The comb is a **multiplicative** fractional ripple on
  the smooth cooling, so in `ln(kT)` it is **additive** with amplitude `~eps`, and the smooth
  exponential-to-floor trend is absorbed by the detector's **degree-2 polynomial-in-ln(t)** baseline
  (identical treatment to the recovery-comb-domains `y=ln(flux)` channels).
- Getting this pairing wrong (energy vs amplitude, etc.) is an audit anomaly, not a candidate.

## Method

1. **Per-curve kernel test (CC.01):** is `ω=2.583` special vs an off-kernel periodogram, gated at
   `≥2.8` comb periods? **Every** crust-cooling curve spans `< 2.8` periods (weeks..15 yr ⇒ ≲2.7
   periods, and real curves start months after `t0`), so all are individually **range-blind**.
2. **Superposed-epoch pooled stack (CC.02, primary KILL test):** pool all ≥6 cooling episodes into
   one `ln(t)` series (each aligned at its own `t0`, per-curve smooth trend + source offset removed),
   spanning the **union ln-range** (`≈3.1` periods) — which *clears* the gate no single curve can —
   then rank the kernel comb gain vs the off-kernel periodogram. *Assumption (optimistic):* the comb
   phase is common across sources (cascade clock anchored at `t0`); a phase-random washout control is
   run in the injection battery.
3. **TFPT λ-battery (CC.03):** phase-incoherent stack at every TFPT ratio `λ ∈ {3/2, φ, 2, 3, 4, 5,
   8, (3/2)⁶, 30}`, per-λ ln-range+Nyquist gate, **Bonferroni** look-elsewhere. Small-λ (large ω)
   entries need less ln-range, so they are testable where the `(3/2)⁶` kernel is range-blind — but a
   small-λ hit is **low specificity** (dense among any scaling story).
4. **Protected-floor test (CC.04):** fit `kT_eff(t) = b + A e^{-t/τ}`; report the core-equilibrium
   floor `b` (generic crust physics, consistency only).
5. **Null battery:** smooth-baseline surrogate; **injection-recovery on the real epoch sampling**
   (strong comb must be recovered, comb-free rejected, and the `eps~2%` power floor reported);
   phase-random washout control; off-kernel λ-battery with Bonferroni.

**KILL:** `ω=2.583` not special across the stacked cooling ensemble.

## Results (deterministic; `results/results.json`)

- **Data:** 8 cooling episodes across **6 distinct transients** (KS 1731−260, MXB 1659−29 ×2
  outbursts, XTE J1701−462, EXO 0748−676, MAXI J0556−332 ×2 outbursts, Aql X-1); **67** `kT_eff`
  epochs, all **transcribed from published spectral-fit tables** (see `data/README.md`).
- **Detector validated** (unchanged kernel): fires **96%** at ≥2.8 periods, **0%** false-positive,
  range-blind below; stack sharpening single 45% → stacked 100%.
- **Every curve is range-blind** (best = XTE J1701−462 at **2.46** < 2.8 periods) → the
  phase-incoherent kernel stack has **`n_used = 0`** (`ω=2.583` not testable that way).
- **Superposed-epoch pooled stack** (67 pts, **3.08** comb periods) clears the gate: **`ω=2.583` is
  NOT special, p ≈ 0.45 → clean NULL** (under the phase-aligned assumption).
- **TFPT λ-battery:** **NULL** after look-elsewhere (**Bonferroni global p = 1.0**; best atom `λ=5`,
  p≈0.28; the idiosyncratic `3/2, φ, (3/2)⁶` are all range-blind, 0 curves gated).
- **Protected floor:** **7/8** episodes show a significant nonzero core-equilibrium floor
  (consistent with the TFPT protected floor — but **generic crust physics**, not TFPT-specific).
- **Injection on the real sampling:** a strong comb (ε=15%) is recovered **100%**, the comb-free
  null false-alarm is **~5%**, **but the predicted ε~2% is detected only ~2%** → the stack is
  **underpowered on the intrinsic amplitude** (density-poor). Phase-random washout confirms the
  pooled test needs `t0`-aligned phases.

**Verdict: `data_limited`.** Crust cooling has the right **floor-terminated** character, but it is
**range/density-limited** for the discriminating ~2% `ω=2.583` comb: no single curve clears the
2.8-period gate, and even the superposed-epoch stack — which does clear it in ln-range — is
underpowered at the predicted amplitude. It serves as an honest 2nd world only via the
(low-specificity) λ-battery **NULL** and the (generic) protected floor. **No claim; nothing `[E]`.**

## Reproduce

```bash
source ../tfpt-discovery/.venv/bin/activate      # numpy + scipy (shared venv; do NOT pip install)
python scripts/fetch_crust_cooling.py            # regenerate the small derived CSVs from tables
PYTHONPATH=src python -m tfpt_crust.cli analyze   # detector+stack validation + all tests -> results/results.json
```

## Layout

```
src/tfpt_crust/comb.py     # frozen kernel detector + injection validation + stacked meta-test + lambda-battery helpers (self-contained port)
src/tfpt_crust/cooling.py  # CSV reader; superposed-epoch pooled stack; TFPT lambda-battery; protected-floor fit; injection-recovery on real sampling
src/tfpt_crust/cli.py      # `tfpt-crust analyze` -> results/results.json
scripts/fetch_crust_cooling.py  # transcribed published tables (cited) -> data/*.csv
data/*.csv                 # 8 derived cooling curves (t_days_since_outburst,kT_eff_eV,err); provenance in data/README.md
hypotheses/crust_cooling_comb_v1.yaml  # preregistered tests + kill conditions (frozen before data)
results/results.json       # committed deterministic summary
```

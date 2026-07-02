# DSI false-positive control — the frozen comb detector on known NON-TFPT cascades

> **Firewall (read first):** earthquake aftershock cascades and solar-flare sequences are
> **known non-TFPT relaxation systems** — crustal/critical and magnetic-reconnection cascades,
> **not** boundary/horizon recoveries. That is the point: this is a **CONTROL bed**, a detector
> calibration, not a TFPT search. **No outcome here can ever confirm TFPT.** A quiet detector
> calibrates the **specificity** of the existing channel nulls; a detector firing at `ω=2.583`
> on controls would quantify the **universal-DSI coincidence rate** the firewall names.
> Nothing here is `[E]`; no load-bearing claim in either direction.
>
> **Two textbook negative controls (v2)** extend the real-cascade bed with the cleanest
> non-TFPT discrete-scale-invariance nature offers — the **Efimov ladder** (an *exactly
> derived* scale factor `λ = e^(π/s₀) = 22.694`) — and the canonical **boundary-less two-step
> relaxation** — **glass/mode-coupling-theory** exponents. Same firewall: these calibrate the
> detector's specificity and the *distinctness* of the frozen scales; they can never confirm
> TFPT.

## The sceptic's question this bed answers

The TFPT comb channels (`recovery-comb-domains`, `pulsar-glitch-recovery`, `crust-cooling-comb`)
report **nulls** at the frozen kernel

```
omega = 2 pi / ln(lambda),  lambda = (3/2)^6   ->  omega = 2.583
eps   ~ exp(-pi^2 / ln lambda) ~ 0.017          (QT.02 amplitude-suppression law)
```

A sceptic asks: *"would this detector fire on ANY discrete-scale-invariant or generic relaxation
cascade?"* If yes, the nulls are weak (the detector is promiscuous) and any future hit would be
cheap. If no, the nulls are **specific**: the kernel frequency does not light up on generic
Omori/DSI cascades, so both the nulls and any eventual hit carry information. This bed measures
that false-positive rate **on real data** from the two canonical non-TFPT cascade worlds.

## Control data (public, no auth; fetched by `scripts/`)

| world | source | sequences |
|---|---|---|
| earthquake aftershocks | [USGS ComCat FDSN](https://earthquake.usgs.gov/fdsnws/event/1/query) | Landers 1992 M7.3, Hector Mine 1999 M7.1, Tohoku 2011 M9.1, Ridgecrest 2019 M7.1 — 3-yr windows, 17 654 events total; Omori `t^-p` decay, **Sornette-documented log-periodic DSI** in some sequences (the canonical non-TFPT DSI system) |
| solar flares | [NOAA NGDC GOES XRS flare reports](https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/) | sun-wide ≥C1 flares within 60 d after Halloween 2003 X17.2, Sep 2005 X17.0, Aug 2011 X6.9, Oct 2014 X3.1 — 1 076 flares total; Omori-like decaying flare rate (de Arcangelis et al. 2006) |

Raw downloads are cached in `data/raw/` (gitignored); the small normalised `(t_days,size)`
per-sequence CSVs in `data/sequences/` are committed. Aftershock window/radius/minmag mirror the
`recovery-comb-domains` quake channel so the two experiments see comparable sequences.

## Method — the SAME frozen statistic, vendored and guarded

`src/tfpt_dsicontrol/comb.py` is a **faithful minimal copy** of the injection-validated detector
from `experiments/recovery-comb-domains/src/tfpt_combdomains/comb.py` (kernel constants and gain
statistic unchanged). **`tests/test_frozen_kernel.py` asserts the vendored constants
(`ω = 2π/ln((3/2)⁶) = 2.5827`, `ε_pred ≈ 0.017`, the 2.8-period gate, the degree-2 detrend, the
0.05 threshold) and the statistic itself are bit-identical to the original** — any drift in
either file fails the guard.

Each sequence is a point process; the recovery observable is the same construction as the TFPT
quake channel: **equal-`ln(t)` bins of event counts, `y = ln(count)`** (Omori rate `~t^-p` →
per-bin count `~t^(1-p)`, near-flat in `ln t`; the detector's degree-2 poly-in-`ln t` baseline
absorbs the smooth decay). Per sequence:

1. **Frozen detector verdict** at `ω=2.583` (`run_comb` unchanged): off-kernel periodogram-rank
   `p` + the hard ≥2.8-comb-period `ln(t)`-range gate.
2. **Rate-preserving shuffle null:** surrogate event sets multinomially redistributed over the
   same `ln(t)` bins with probabilities from the fitted smooth (deg-2 in `ln t`) rate — Omori
   trend and total count preserved, ripple destroyed; `p_shuffle` = rank of the observed kernel
   gain over 500 surrogates.
3. **Off-kernel scan `ω ∈ [1,6]`** (501 points): the kernel's rank; the sequence's own best free
   `ω`; and the best **localisable** `ω` (frequencies the curve spans for ≥2.8 cycles — the same
   requirement the kernel must meet; the raw argmax otherwise pins at the low edge on trend
   residue).
4. **Fitted ripple amplitude** at the kernel, next to `ε_pred ≈ 0.017`.

Aggregate deliverable: the **kernel false-positive rate** over gated sequences — the frozen
criterion (`p < 0.05` + gate) and the strict double criterion (frozen AND shuffle `p < 0.05`) —
with Wilson 95% intervals. Protocol preregistered in
`hypotheses/dsi_false_positive_control_v1.yaml`.

## Results (deterministic, seed 0; `results/results.json`)

Vendored detector re-validated by injection: fires 96% on a real comb with sufficient range, 0%
on smooth decay, range-blind below 2.8 periods.

| sequence | kind | events | comb periods | p(ω=2.583) periodogram | p(ω=2.583) shuffle | kernel rank /449 | best localisable ω (λ) | ε_fit |
|---|---|---:|---:|---:|---:|---:|---|---:|
| Landers 1992 | aftershock | 4458 | **5.39** | 0.069 | 0.048 | 40 | 2.52 (12.1) | 0.23 |
| Hector Mine 1999 | aftershock | 1837 | **3.33** | 0.613 | 0.395 | 276 | 2.92 (8.6) | 0.09 |
| Tohoku 2011 | aftershock | 4333 | **4.94** | 0.882 | 0.904 | 396 | 1.62 (48.4) | 0.03 |
| Ridgecrest 2019 | aftershock | 7026 | **4.94** | 0.333 | 0.102 | 185 | 1.71 (39.4) | 0.26 |
| Halloween 2003 | flare | 274 | 1.79 ⊘ | 0.244 | 0.134 | 64 | 6.00 (2.9) | 0.22 |
| Sep 2005 | flare | 115 | 1.49 ⊘ | 0.125 | 0.014 | 63 | 4.85 (3.7) | 0.31 |
| Aug 2011 | flare | 253 | 1.56 ⊘ | 0.134 | 0.002 | 134 | 4.63 (3.9) | 0.77 |
| Oct 2014 | flare | 434 | 1.78 ⊘ | 0.855 | 0.800 | 378 | 5.77 (3.0) | 0.05 |

⊘ = range-blind (< 2.8 comb periods; a 60-day flare window cannot span the `(3/2)⁶` ladder) —
honestly excluded from the false-positive denominator, exactly as the TFPT channels exclude
range-blind curves.

**Aggregate kernel false-positive rate (4 gated sequences):**

- frozen criterion: **0/4 = 0.00** (Wilson 95% [0, 0.49]) — nominal rate at `p<0.05` is ~5%
- strict (frozen AND rate-preserving shuffle): **0/4 = 0.00** (Wilson 95% [0, 0.49])

The closest call is Landers 1992 (`p_periodogram ≈ 0.07–0.11` over seeds 0–2, never < 0.05;
notably its best localisable DSI scale `λ ≈ 12.1` sits near `(3/2)⁶ = 11.4` — a reminder of how
easily generic seismic DSI can *drift close to* the kernel, which is precisely why the frozen
threshold + look-elsewhere discipline matters). Meanwhile the controls do show their **own**
log-periodicity away from the kernel: 5/8 sequences have a best-localisable-ω shuffle
`p < 0.05` (uncorrected), and the flare sequences prefer `λ ≈ 2.9–3.9` — consistent with the
Sornette-type system-dependent DSI scales (`λ ~ 2–3.5`) reported for critical cascades. That is
**expected outcome (ii)**: the detector sees generic DSI where it exists, at *non-kernel*
frequencies.

**Verdict: `consistent` (control passed).** The kernel frequency `ω=2.583` fired on **zero of
four** gated real non-TFPT cascades (upper 95% bound 49% — limited by n=4, but with zero hits
under both nulls and every kernel `p ≥ 0.07`), while the same sequences visibly carry
*non-kernel* DSI. The existing TFPT-channel nulls are therefore **specific**: the detector is not
promiscuous on Omori/DSI-type relaxations, so a null at `ω=2.583` is informative and a future hit
would not be generically cheap. **Firewall:** this calibrates the detector only; it is **not**
evidence for TFPT, and nothing here is `[E]`.

## Control 1 — the Efimov ladder (nature's exactly-derived non-TFPT DSI)

The [Efimov effect](https://doi.org/10.1016/j.physrep.2006.03.001) is the one non-TFPT discrete
scale invariance whose scale factor is *derived from first principles*, not fitted: three
resonantly interacting bosons form a geometric ladder of trimer states with universal factor

```
lambda_Efimov = e^(pi/s0),  s0 = 1.00624  ->  lambda = 22.694,  ln(lambda) = 3.1221,
omega_Efimov  = 2 pi / ln(lambda_Efimov)  =   2.0125.
```

That is a **22.1 %** frequency separation from the kernel `ω = 2.583` — comfortably outside the
±10 % kernel neighbourhood the periodogram statistic already excludes, so the two ladders are
**resolvable by construction**. Two tests (`src/tfpt_dsicontrol/efimov.py`; data in
`data/efimov.json` with references):

- **EF.01 — measured ladder ratios.** Published cold-atom resonance-position ratios:
  ¹³³Cs `21.0 ± 1.3` (Huang+ 2014, PRL **112**, 190401), ⁷Li `21.1 ± 2.6` (Pollack+ 2009,
  Science **326**, 1683), ³⁹K `25 ± 4` (Zaccanti+ 2009, Nat. Phys. **5**, 586). Inverse-variance
  combined: **`21.33 ± 1.12`** — consistent with `λ_Efimov = 22.69` (`−1.2σ`) and **`8.9σ` from
  the TFPT `λ = (3/2)⁶ = 11.39`** (a one-parameter χ² scan over `λ ∈ [5,50]` prefers `21.35` and
  puts TFPT `8.9σ`-equivalent away). **Inverse statement (as requested):** ¹³³Cs alone is
  **`7.4σ`** from the TFPT `λ = 11.39` — the frozen kernel and the Efimov DSI are cleanly
  distinct scales.
- **EF.02 — frozen detector on the Efimov comb (gated).** The vendored `run_comb` on a realised
  Efimov comb (ripple at exactly `ω_Efimov`, validation-grade `ε = 0.30`, 25 noise seeds, ln-range
  = 3.7 kernel = 2.88 Efimov periods so both gates clear): kernel fired **0/25** (median
  `p = 0.20`), while detection *at* `ω_Efimov` is **100 %** and the free scan localises
  `ω = 2.01 (λ = 22.8)`. The Efimov ladder therefore enters the aggregate FP count as **one
  additional gated DSI control** on which the kernel does **not** fire.

## Control 2 — glass/MCT exponent spread (boundary-less two-step relaxation has no frozen bend)

Mode-coupling theory is the canonical theory of **boundary-less two-step relaxation** (β plateau
+ α decay). Its whole exponent structure hangs on the exponent parameter `λ_MCT` through the exact
relations `λ = Γ(1−a)²/Γ(1−2a) = Γ(1+b)²/Γ(1+2b)` and `γ = 1/(2a) + 1/(2b)`, and `λ_MCT` is an
explicit **functional of the static structure `S(q)`** — so `γ` is **system-dependent by
construction**. This is a *structural* control: **no comb run, no detector**, just the exponent
bookkeeping (`src/tfpt_dsicontrol/mct.py`; data in `data/mct_exponents.json`, cited per system).

| system | γ (measured/derived) | λ_MCT | reference |
|---|---:|---:|---|
| hard spheres (3D, PY) | 2.46 ± 0.10 | 0.735 | Franosch+ 1997; Sperl 2004 |
| binary hard disks (2D) | 2.497 ± 0.05 | 0.742 | Weysser & Hajnal, PRE **83**, 041503 (2011) |
| Kob–Andersen LJ (3D) | 2.80 ± 0.20 | 0.78 | Kob & Andersen, PRE **51**, 4626 (1995) |
| BKS silica | 2.35 ± 0.15 | 0.710 | Horbach & Kob, PRE **64**, 041503 (2001) |
| orthoterphenyl | 2.46 ± 0.20 | 0.735 | Singh+ 1998 (schematic MCT) |
| Gaussian core model | 2.70 ± 0.10 | 0.779 | Ikeda & Miyazaki 2011 |
| soft spheres (3D) | 2.20 ± 0.15 | 0.670 | compilation, Commun. Phys. **7** (2024) |

- **MCT.01 — exponent relations.** The exact Γ-function relations reproduce the textbook
  hard-sphere set (`λ = 0.735 → a = 0.312, b = 0.583, γ = 2.46`) and every data-file row is
  internally consistent (quoted-vs-derived `γ` guard).
- **MCT.02 — spread statistic.** Across 7 systems `γ` spans **`[2.20, 2.80]`**, std `0.20`,
  range width `0.60` = **`4.0×` the median per-system error `0.15`**. The frozen bend
  `ln3/ln(3/2) = 2.7095` **does sit inside** that spread — but a *locked universal* bend is
  **rejected at χ² = 43.4 / 7 dof (≈ 4.9σ, Wilson–Hilferty)**, while the weaker one-universal-γ
  hypothesis (χ² = 11.5 / 6 dof, ≈ 1.4σ) is reported as-is. The nearest system (Gaussian core
  model, `γ = 2.70`) lands `0.01` from the bend — a **proximity coincidence** named honestly, in
  exactly the spirit of Landers' `λ ≈ 12.1` near `(3/2)⁶` in the cascade bed. **Control passes:**
  boundary-less two-step relaxation shows **no frozen universal bend**, so the TFPT walled-clock
  bend is a falsifiable, informative feature — not a generic property of two-timescale decay.

## Aggregate false-positive statement (v2 — including the gated Efimov DSI control)

The Efimov ladder is a genuine, exactly-derived DSI that clears the range gate, so it joins the
kernel false-positive denominator:

- v1 cascade aggregate (unchanged): **frozen 0/4**, strict 0/4 (Wilson95 `[0, 0.49]`).
- **Combined over all 5 gated DSI controls (4 cascade sequences + the Efimov ladder): kernel
  fired `0/5 = 0.00` (Wilson95 `[0, 0.43]`).**

Across every gated discrete-scale-invariant relaxation the bed can reach — real Omori/Sornette
seismic cascades, real solar-flare cascades, and the textbook Efimov ladder — the frozen kernel
`ω = 2.583` fires **zero times**, while each system's *own* DSI (seismic `λ ≈ 2–3.5`, Efimov
`λ = 22.7`) is recovered where it exists, and the glassy relaxation bend is provably
system-dependent. The existing comb nulls are **specific**, and the frozen kernel/bend are
**distinct** from the nearest textbook non-TFPT scales. **Firewall:** calibration only; **not**
evidence for TFPT; nothing here is `[E]`.

## Reproduce

```bash
. ../tfpt-discovery/.venv/bin/activate            # shared venv (numpy); do NOT pip install
python scripts/fetch_aftershocks.py               # USGS ComCat -> data/sequences/*.csv
python scripts/fetch_flares.py                    # NGDC GOES XRS -> data/sequences/*.csv
PYTHONPATH=src python tests/test_frozen_kernel.py     # frozen-kernel guard (must ALL PASS)
PYTHONPATH=src python tests/test_negative_controls.py # Efimov + MCT control guards (ALL PASS)
PYTHONPATH=src python -m tfpt_dsicontrol.cli analyze   # -> results/results.json (all sections)
PYTHONPATH=src python -m tfpt_dsicontrol.cli efimov    # CONTROL 1 only (Efimov ladder)
PYTHONPATH=src python -m tfpt_dsicontrol.cli mct       # CONTROL 2 only (glass/MCT spread)
```

## Layout

```
src/tfpt_dsicontrol/comb.py       # VENDORED frozen detector (verbatim from recovery-comb-domains; guarded)
src/tfpt_dsicontrol/fetch.py      # USGS ComCat + NGDC GOES XRS fetchers (cached, normalised)
src/tfpt_dsicontrol/sequences.py  # rate curve, rate-preserving shuffle null, omega scan, FP aggregate + combined DSI aggregate
src/tfpt_dsicontrol/efimov.py     # CONTROL 1: exact Efimov ladder, EF.01 measured ratios, EF.02 detector resolvability
src/tfpt_dsicontrol/mct.py        # CONTROL 2: exact MCT exponent relations + honest spread statistic (structural, no comb)
src/tfpt_dsicontrol/cli.py        # `tfpt-dsicontrol {analyze, fetch, fetch-quakes, fetch-flares, validate, audit, efimov, mct}`
scripts/fetch_aftershocks.py      # documented download: 4 aftershock sequences
scripts/fetch_flares.py           # documented download: 4 flare sequences
tests/test_frozen_kernel.py       # constants + statistic bit-identical to the original kernel
tests/test_negative_controls.py   # Efimov exact constants/resolvability + MCT exponent relations/spread guards
hypotheses/dsi_false_positive_control_v1.yaml  # preregistered cascade protocol + expected outcomes
hypotheses/dsi_negative_controls_v2.yaml       # preregistered Efimov + MCT control protocol (extends v1)
data/sequences/*.csv              # normalised (t_days,size) control sequences (committed)
data/efimov.json                  # CONTROL 1: published Efimov resonance positions/ratios + references
data/mct_exponents.json           # CONTROL 2: per-system MCT exponent sets (lambda, a, b, gamma) + references
data/raw/                         # raw USGS/NGDC downloads (gitignored)
results/results.json              # committed deterministic summary (cascades + Efimov + MCT + combined aggregate)
```

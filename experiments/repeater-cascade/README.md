# Repeater cascade — the walled clock + frozen comb on FRB burst-time cascades

> **Firewall:** a **search target / consistency check**, never a load-bearing claim.
> Repeater burst-time cascades are tested as a *residual boundary-recovery pattern*;
> nothing here is upgraded to `[E]`. A hit would be a universal
> discrete-scale-invariance coincidence in the magnetar/FRB engine — **not** a horizon
> signature and **not** TFPT confirmation — until it recurs in ≥ 2 independent worlds.

## Why this experiment exists

The GW Stage-2 identifiability analysis machine-checked that the walled two-mode
clock bend `rate(2)/rate(1) = ln3/ln(3/2) = 2.7095` is **degenerate** within one
monotone recovery (two-mode R² gain ~1e-3 even noise-free). The discriminating
dynamic signatures are (a) the **log-periodic comb** `ω = 2π/ln((3/2)⁶) = 2.583`
(ripple `ε = exp(−π²/ln λ) ≈ 1.7%`) over **> ~2.8 ln-periods** (PG.06 machine
check), and (b) the time-resolved recovery **sequence** of a repeating source.

Every pulsar leg so far hit the **range wall**: Crab monthly (PG.05), J0537 ~1.9
periods (PG.06), Vela-2024 ~2.55 periods (PG.07). Hyperactive FRB repeaters are the
one astrophysical system with **thousands of time-stamped events per activity
episode**: a single FAST session spans τ from ~0.3 s to hours, i.e. **3–5 comb
periods in ln(t − t_onset)**. This experiment is the structurally most sensitive
TFPT dynamic search precisely because the range wall does not apply; the honest
remaining wall is the **amplitude** (see verdict).

Preregistered **before** any statistic ran: `hypotheses/repeater_cascade_v1.yaml`
(frozen kernel byte-guarded by `tests/test_frozen_kernel.py`, including identity
with the `pulsar-glitch-recovery` kernel).

## Data (all real, fetched by `scripts/fetch_data.py`)

| Committed file | Source | Bursts | Provenance |
|---|---|---|---|
| `data/frb20220912a_zhang2023.csv` | FRB 20220912A | 1,076 | Zhang Y.-K.+2023 ApJ 955,142 (FAST); VizieR `J/ApJ/955/142` table1.dat, barycentric MJD @1.5 GHz |
| `data/frb20201124a_fast.csv` | FRB 20201124A | 1,863 + 881 | Xu H.+2022 Nature 609,685 (spring-2021) + Zhang Y.-K.+2022 RAA 22,124002 (autumn-2021), via the committed Blinkverse export in `frb-tfpt-signatures` (rows keyed by reference DOI) |
| `data/frb20240114a_fast.csv` | FRB 20240114A | 6,134 | FAST polarization catalog v5 (ApJS 2025), MJD_topo at 1e-8 d |
| `data/chime_cat2_repeaters.csv` | 15 CHIME repeaters | 981 | CHIME/FRB Catalog 2 (ApJS 283,34). The portal (`chime-frb.ca/catalog2`) was **503**; fetched from the **CANFAR DOI archive** `doi:10.11570/25.0066` → `vault/.../data/table/chimefrbcat2.csv` (host via CADC registry) |

Anti double-counting: FRB 20220912A exists in Blinkverse *and* CHIME Cat2; the FAST
leg uses only the Zhang+2023 VizieR table and the CHIME leg only CHIME-detected
bursts — no burst enters twice. FRB 20201124A CHIME rows (34) are a separate,
instrument-independent series.

## What it checks (`src/repeater_cascade/`)

Sessions: gap > 0.2 d; onset proxy `t0` = first burst; `τ_i = t_i − t0` (s), gated
at `τ ≥ 30×` the dataset time resolution.

| Axis | Signature | Method + null battery | Result (seed 0) |
|---|---|---|---|
| **RC.01** | walled two-mode clock `R(t) = w0 + w1 e^{−rt} + w2 e^{−2.7095·rt}` (frozen bend, r profiled, NNLS weights) on per-session rate curves | ΔR² over single-exp null; rate-preserving surrogates; **free-bend placebo family** [1.5, 6] | **degenerate-null**: 37 rate curves, median ΔR² = 0.0000, 0/37 with p < 0.05, frozen bend beats the placebo family **0/37** times. The injection check shows even a TRUE frozen-bend session gives ΔR² ≈ 0.004 (p ≈ 0.8) — the machine-checked Stage-2 degeneracy, reproduced on real cascade sampling |
| **RC.02** | **frozen comb** `ω = 2.583` in `ln(t − t_onset)`: Rayleigh power of phases `ω·ln τ_i` | rate-preserving surrogates (smooth cubic log-density redraw); **off-kernel periodogram rank** (surrogate-standardised ζ(ω) vs 150 off-kernel frequencies); **off-kernel λ battery** (Bonferroni); KS cross-check; **reach gate > 2.8 periods enforced per session** | **null at detectable amplitude**: 9 gate-passing sessions across 2 sources (FRB 20201124A: 2, FRB 20240114A: 7; max reach **4.80 periods**); survive-all-nulls session p (= max of surrogate & rank p): Fisher p = 0.72 / 0.38, BH **q = 0.72** — ω is not special. One session (MJD 60676.32: p_sur 0.040, p_rank 0.022, battery-smallest) fires alone but dies in aggregation — a fluctuation, not a candidate |
| **RC.03** | waiting-time ratio ladder on the teeth `{log 3/2, log (3/2)³, log (3/2)⁶}` (the tooth set IS the step/amplitude/energy battery; PG.02/PG.03 mirror) | within-session shuffle of the RAW intervals, ratios recomputed; Bonferroni over sources | **null**: 20201124A p = 0.46 (2,593 ratios), 20220912A p = 0.71 (1,031), 20240114A raw p = 0.033 → **Bonferroni ×3 p = 0.10** (49/17/65 sessions) |

All TFPT numbers derive from the two axioms (`c₃ = 1/(8π)`, `g_car = 5`) in
`constants.py` — identical to the FRB/GW/pulsar kernels — frozen as targets, never
fitted.

## Injection validation (`tfpt-cascade validate`, seed 0)

FAST-like synthetic session (inhomogeneous Poisson, `rate ∝ τ^−0.8`, N ≈ 1000,
reach ≈ 4 periods), survive-all-nulls criterion:

- reference amplitude `ε = 0.30`: comb detected **94%** (15/16 seeds);
- smooth `ε = 0`: false-positive rate **0%**;
- **predicted** `ε = 0.0173`: detection rate **0%** — the honest amplitude wall
  (Rayleigh power scales as `n ε²/4`; a single-session 5σ detection at 1.7% needs
  ~1e5 bursts).

## Verdict (v1, 2026-07-02)

**`null` at detectable comb amplitude; `data_limited` at the predicted 1.7%.**
For the first time in the TFPT dynamic-search programme the **ln-range wall is
cleared** — 9 real sessions span > 2.8 comb periods (up to 4.8) — and the frozen
`ω = 2.583` is *not* a special log-frequency in any of them after surrogate
calibration, off-kernel ranking and the λ battery. The detector is
injection-validated at reference amplitude on exactly this session sampling, so
this is a real null for combs with `ε ≳ 0.1`, not a dead pipeline. At the
*predicted* `ε ≈ 1.7%` a single session has ~0 power (amplitude wall: ~1e5
bursts/session needed), so the predicted-amplitude comb is **not killed** — it
stays `data_limited`. RC.01 confirms the bend degeneracy on real data; RC.03
ladders are null after look-elsewhere. FRB 20220912A's FAST sessions top out at
2.73 periods (~1 h blocks) — just **below** the gate, so it contributes to
RC.01/RC.03 only. CHIME Cat2 contributes no within-session cascade (all transit
sessions n < 30) — `data_limited` for this axis, kept as the
instrument-independent cross-check for future hyperactive episodes.

**Decisive next step:** a super-session stack (phase-coherent in `ln τ` across
~50+ sessions of one source) would buy the missing amplitude sensitivity
(√N × session-N); requires modelling per-session onset offsets — a real analysis
project, preregister as RC.04 before running.

## Reproduce

```bash
. ../tfpt-discovery/.venv/bin/activate      # shared venv (numpy/scipy/matplotlib)
python scripts/fetch_data.py                # re-fetch / re-derive the committed tables
python tests/test_frozen_kernel.py          # frozen-kernel guard
PYTHONPATH=src python -m repeater_cascade.cli audit
PYTHONPATH=src python -m repeater_cascade.cli validate   # injection-recovery self-check
PYTHONPATH=src python -m repeater_cascade.cli analyze    # RC.01/02/03 -> results/results.json
```

## Layout

```
hypotheses/repeater_cascade_v1.yaml   # preregistered FROZEN hypothesis (before data pass)
scripts/fetch_data.py                 # VizieR + CANFAR + committed-catalog derivations
data/                                 # committed burst-time tables (see table above)
src/repeater_cascade/constants.py     # frozen kernel from the axioms (guarded)
src/repeater_cascade/data_io.py       # loaders -> BurstSeries
src/repeater_cascade/sessions.py      # sessionisation, tau gating, reach in comb periods
src/repeater_cascade/clock_template.py# RC.01 walled two-mode clock (frozen bend + placebos)
src/repeater_cascade/comb.py          # RC.02 frozen comb (surrogates, rank, lambda battery)
src/repeater_cascade/ladder.py        # RC.03 waiting-time ladders (PG.02/03 mirror)
src/repeater_cascade/validation.py    # injection-recovery on realistic session sampling
src/repeater_cascade/cli.py           # tfpt-cascade audit|validate|analyze
tests/test_frozen_kernel.py           # kernel byte-guard + cross-domain identity
results/results.json, validation.json, rc_comb.png
```

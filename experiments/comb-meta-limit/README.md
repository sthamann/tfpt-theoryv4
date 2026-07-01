# comb-meta-limit — a meta-analytic UPPER LIMIT on the recovery-comb amplitude `ε`

> **FIREWALL:** this is a **search-surface meta-analysis**, *not* a claim — nothing here is
> load-bearing (`[E]`) and nothing gets a `\veri{}`. It reads the *existing* per-channel
> recovery-comb results (read-only) and combines them. The **all-channel** limit is a
> **universal-DSI** statement, explicitly **NOT** a TFPT constraint; only the
> **boundary/horizon-scoped** limit is TFPT-relevant. Honest verdict language throughout.

The repo has a pile of clean per-channel *nulls* for the frozen dynamic recovery comb

```
R(t) = (power law) · (1 + ε cos(ω ln t + φ)),   ω = 2π/ln((3/2)⁶) = 2.583,
ε  ~ exp(−π²/ln λ) = 0.0173  (~2%, the QT.02 amplitude-suppression law, λ=(3/2)⁶)
```

Each channel said "the kernel ω is not special" — a *qualitative* null. This experiment turns that
pile into the first **quantitative** statement: a hierarchical / random-effects **95% upper limit**
on the common comb amplitude `ε` at the frozen ω, and asks whether the joint limit pushes **below
~2%** (which would be a genuine, if soft, constraint on the dynamic kernel — not just "another
null").

## Two limits — reported separately, never mixed

1. **Boundary/horizon-scoped** (the **TFPT-relevant** limit): only the channels where TFPT actually
   predicts a *universal* ε — the GW ringdown residual and the horizon-residual FRB tails
   (A3/A3b), plus the BH late-time tail (A2). This is the number that would matter for the theory.

2. **All-channel** (surface + horizon): additionally folds in the *surface* channels — A1 magnetar,
   A4 GRB plateau, A5 ENT/AGN-disk-TDE, PG.05 Crab (and PG.07 Vela / crust-cooling when their
   result files exist). This is legitimate **only** as a bound on a *universal discrete-scale-
   invariance* amplitude; a surface comb would be a universal-DSI coincidence, **never** a TFPT
   confirmation, so this number is **never** presented as a TFPT constraint.

## Honest costs (built into the method, not hidden)

- **ε is not guaranteed universal across surface vs horizon.** A surface relaxation
  (magnetosphere, accretion disk, crust) and a horizon recovery need not share one ε. Combining
  them under a single ε is therefore a **universal-DSI** statement only. The two limits are kept
  strictly separate and the all-channel number is **never** called a TFPT constraint.
- **Shared detector, independent sources.** Every channel runs the *same* comb detector
  (correlated method), but the astrophysical *sources* (a magnetar outburst, a GRB afterglow, an
  AGN-disk TDE) are physically independent. We model this honestly: a per-source ε̂ with a
  **red-noise-aware** uncertainty from that curve's own off-kernel periodogram, combined with a
  **random-effects** (DerSimonian–Laird + Hartung–Knapp) upper limit — **not** a naïve product,
  which would manufacture significance. The shared-detector correlation is additionally folded in
  as a conservative SE inflation `√(1+(k−1)ρ)` (default ρ=0.3), reported alongside.
- **This is an UPPER-LIMIT design, not a detection.** A null channel sits at ε̂≈0 with a proper
  uncertainty; we report where the *joint* 95% UL lands relative to 2%. No significance is claimed.

## What actually yields an absolute ε (and what doesn't)

| tier | channels | why |
|---|---|---|
| **A — absolute ε** (fed into the limit) | A1 magnetar, A4 GRB, A5 ENT | recovery observable is `y = ln(flux)`, so the fitted comb amplitude **is** the fractional ε the theory predicts; the curves are committed → reproduced locally |
| **B — normalised / no ε** (enumerated only) | A3, A3b FRB · PG.05 Crab · GW · A2 · PG.07 Vela · crust | raw curve gitignored/absent, **or** the observable is a linear intensity / nu-dot residual (not a fractional flux modulation), **or** a single ringdown is degenerate (the bend needs a many-event cascade). Only a *normalised* amplitude `√(2·gain)` is available — **not** comparable to the absolute 2%. |

The decisive, honest finding falls straight out of this table: **every channel where TFPT predicts
a universal ε (the horizon group) is amplitude-data-limited**, while the only channels that yield an
absolute ε are *surface* ones. So the TFPT-relevant limit is `data_limited`, and the all-channel
number is a surface-driven universal-DSI bound.

## Method

Per **gated** recovery curve (≥ 2.8 comb periods in ln t — the same hard range gate the siblings
use), fit

```
y(ln t) = poly₂(ln t) + A cos(ω ln t) + B sin(ω ln t),   a_hat = √(A²+B²)
```

(identical fit to `recovery-comb-domains/comb.py`; reproduced-gain cross-check passes for **30/30**
committed sources). The comb **power** is debiased by the mean **off-kernel** power (red-noise
aware): `ε²̂ = a_hat(ω)² − ⟨a_hat(f)²⟩_offkernel`, with a 1σ from the off-kernel power scatter.
Powers combine **sources → channel → group** by DerSimonian–Laird random-effects with a
**Hartung–Knapp–Sidik–Jonkman** robust SE (the recommended few-study fix; the plain z-based UL is
anti-conservative here — confirmed by the coverage check). The one-sided 95% UL is
`ε₉₅ = √(max(0, ε²̂ + t_{k−1}·se))`.

**Verdict enum:** `constrains` (UL < 2% → soft tension for the dynamic kernel), `data_limited`
(UL ≥ 2% → can't constrain), `consistent` (a positive ε within 1σ of 2%).

## Current result (`results/results.json`, deterministic, seed 0)

- **Boundary/horizon-scoped limit → `data_limited`.** No horizon/horizon-residual channel yields an
  absolute ε (GW single-event bend is degenerate; the FRB raw waterfalls are not on disk and the
  tail observable is linear intensity; A2 is below single-event SNR). The TFPT-relevant ε is **not
  yet constrainable** — the honest headline.
- **All-channel (universal-DSI) limit → `data_limited`.** Combining the three absolute-ε surface
  channels (A1, A4, A5): ε̂ = 0.0, **95% UL = 0.120 (12.0%)** (HKSJ, t₂=2.92; ρ=0.3-inflated
  0.137). That is **≈ 6.9× the ~2% prediction**, so the pile of surface nulls does **not** push
  below 2% — it cannot yet constrain the universal-DSI amplitude either.
- **Per-channel** ε̂ ± σ (absolute, Tier A): A4 GRB 0.027 ± 0.040 (17 curves, the anchor);
  A1 magnetar 0.00 ± 0.074 (2 curves); A5 ENT 0.00 ± 0.064 (1 curve). Tier-B normalised amplitudes
  `√(2g)`: A3 0.27, A3b 0.58, PG.05 0.76 (context only, not absolute ε).
- **Injection self-consistency:** inject a known common ε into mock channels and re-run the whole
  pipeline — ε=0→ε̂=0.016 (UL 0.027); ε=0.02→ε̂=0.015 (UL 0.030); **ε=0.05→ε̂=0.048 (UL 0.055)**.
  Coverage of the 95% UL ≈ **0.92** over 150 trials (target 0.95; within Monte-Carlo error — mildly
  anti-conservative, so a channel grazing the UL is "escalate", not "hard exclude").

**Bottom line:** the search space is genuinely narrow. The ~2% comb needs a *clean, wide-ln(t),
horizon* recovery, and no such curve exists yet; the surface channels that do exist bound only a
universal-DSI amplitude, and only to ~12%. No claim.

## Reproduce

```bash
source ../tfpt-discovery/.venv/bin/activate            # numpy + scipy
cd experiments/comb-meta-limit
PYTHONPATH=src python -m tfpt_metalimit.cli analyze     # -> results/results.json + printed summary
#   --seed N      change the off-kernel/injection seed
#   --rho R       shared-detector correlation for the conservative SE inflation (default 0.3)
#   --quick       fewer injection-coverage trials (fast smoke run)
```

Reads (read-only) the sibling results/data: `recovery-comb-domains/{results,data}`,
`pulsar-glitch-recovery/results`, `gw-ringdown-echo` (README-level), and
`crust-cooling-comb/results/*.json` if a parallel sibling has produced it (graceful skip if absent).

## Layout

```
src/tfpt_metalimit/kernel.py     # frozen kernel: omega=2.583, lambda=(3/2)^6, eps_predicted=1.7%
src/tfpt_metalimit/combfit.py    # harmonised comb-amplitude fit + red-noise-aware off-kernel null band
src/tfpt_metalimit/channels.py   # ingest every channel (Tier A reproduced locally; Tier B read-only)
src/tfpt_metalimit/metalimit.py  # DL + Hartung-Knapp random-effects 95% UL, correlation, verdict enum
src/tfpt_metalimit/selfcheck.py  # injection self-consistency + UL coverage calibration
src/tfpt_metalimit/cli.py        # `python -m tfpt_metalimit.cli analyze`
results/results.json             # both ULs + per-channel eps_hat + self-consistency (committed output)
```

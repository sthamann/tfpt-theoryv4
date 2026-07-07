# CMB primordial log-comb — the frozen ω against the Planck feature search

> **Firewall:** a consistency **typing** against published constraints — never
> load-bearing, never `[E]`. No raw likelihood is re-fit; the experiment
> machine-checks the confrontation and states the dated decider. Preregistered
> in `hypotheses/cmb_logcomb_v1.yaml`.

## Why this bed is categorically special

Every astrophysical comb search so far ran on observer time with an
**unjustified clock** (the S14 lesson — all those nulls are bridge nulls). The
primordial power spectrum is the **one natural-data bed where the log-clock is
motivated**: inflation e-folds *are* a log-clock (modes exit the horizon at
ln k ∝ N). If the seed epoch carried the seam recovery, its log-comb would be
imprinted **in ln k** — and Planck already searched exactly this template:

```
P(k) = P0(k) · [1 + A_log · cos(ω_log · ln(k/k*) + φ)]      (Planck 2018 X, Sect. 7)
```

The frozen TFPT frequency `ω = 2π/ln((3/2)⁶) = 2.5827` (log₁₀ω = 0.412) lies
**inside** the Planck search prior (log₁₀ω ∈ [0, 2.1]). What is *not* derived
(flagged bridge, S15): that the recovery comb transfers multiplicatively into
P(k), and that the amplitude is the QT.02 value ε = e^(−π²/lnΛ) = 0.0173.

## Result (machine-checked typing) — **data_limited**

| check | value |
|---|---|
| ω inside the published search band | yes (0.412 ∈ [0, 2.1]) |
| reach, full likelihood window (k = 10⁻⁴–0.2 Mpc⁻¹, ℓ = 2–2500) | **3.12 comb periods** (> 2.8 gate) |
| reach, conservative window (k = 0.005–0.2) | 1.52 periods (sub-gate; the gate passes only with the cosmic-variance-dominated low-ℓ leg) |
| published detection at any ω | none (Planck: Δχ² ~ 10 typed as noise/217-GHz artefact) |
| published 95 % amplitude bound | ≈ 0.03 (Planck 2018 X, Fig. 28); ≈ 0.029 combined Planck+SPT-3G+ACT |
| predicted amplitude | ε = 0.0173 — a factor **1.7 below** today's bound |

**Verdict: `data_limited`.** The predicted comb is currently invisible by a
factor ~1.7 in amplitude. **Dated decider:** CMB-S4-class combined bounds reach
the 0.017 level — a future 95 % bound `A_log(ω = 2.583) < 0.017` with no
detection **kills** the primordial-DSI bridge reading; a detection *at* the
frozen ω (phase-coherent across TT/TE/EE) escalates. Either way this is one of
the few dated, external, zero-parameter decision points of the program (the
frequency has no tunable freedom).

## Reproduce

```bash
cd experiments/cmb-primordial-logcomb
python tests/test_frozen_targets.py          # 6/6 guard
PYTHONPATH=src python -m tfpt_cmblog.analysis   # -> results/results.json
```

## References

Planck 2018 results X (A&A 641, A10), Sect. 7–8 + Fig. 28 (log-oscillation
template, priors, bounds); combined Planck+SPT-3G+ACT feature constraints
(A_log ≲ 0.029 at 95 %); Planck 2018 VI/IX for the underlying likelihoods.

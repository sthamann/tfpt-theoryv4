# FRB ontology — testing what FRBs could BE in TFPT (FO.01–FO.10)

> **Firewall:** search targets / consistency checks — **never** load-bearing, never `[E]`.
> A hit in any axis is escalate-only (universal DSI / astrophysical coincidence /
> selection systematics stay the default reading). Preregistered in
> `hypotheses/frb_ontology_v1.yaml` **before** any statistic ran (v1.1 addendum dated,
> see audit note below).

Six ontology hypotheses on the NATURE of FRBs in TFPT (research note
`experiments/next.txt` 2026-07-07 (I)), one level above the number tests. Hard
constraint from the catalog (SIGNATURES.md): the whole intensity/timing/polarization
surface is null (FRB.01–09, KC.01–06, RC.01–04), while two robust POSITIVE structures
exist (PA fundamental m=2, handedness persistence). A viable ontology must PREDICT
that null landscape. Typing per SIGNATURES.md 0b.1–0b.4 (S15 transduction gate, S14
clock-map gate, μ₄ = Galois gear without a pointer, prime 2 without a rate).

| axis | ontology under test | type | verdict (seed 0; seed 1 identical) |
|---|---|---|---|
| **FO.01** | intensity-blind amplifier: the coherent threshold readout projects the character structure out of ALL intensity/timing functionals (`B·P_r = 0`) — the null landscape as a prediction | theory contract (`theory-contracts/fo01_transduction_invisibility.py`, never scorecard) | **5/5 PASS** |
| **FO.02** | repeater system as natural EIT: bursts probe the medium; DM/RM are KNOWN linear line integrals (first FRB axis passing the S15 eligibility gate); all coupled observables share one two-rate set with ratio ln3/ln(3/2) = 2.7095 | search target (named B) | **data_limited** (AIC prefers single rates) |
| **FO.02b** | same reading at INTRA-session cadence (v1.2 addendum): within sessions the two rates are shared and their ratio is frozen; per-burst scatter without memory would type the RM variance as magnetospheric, not a medium state | search target (named B) | **data_limited — informative negative** (variance real, but NO temporal memory in either source) |
| **FO.03** | S14 clock map: the session cascade ticks in the medium state path `τ_mod = Σ\|ΔRM\|`, not observer time — first FRB comb test with a NAMED clock | search target (named clock, bridge) | **null** at detectable amplitude |
| **FO.04** | parity without rate: m=2 + handedness persistence ARE the only allowed Z₂ signature; no m=4 refinement, rate-free switches, persistent classes | diagnostic (prime-2) | **consistent** (all three predictions hold) |
| **FO.05** | episode as transfer unit: quiescence gaps / episode-integrated energies on the teeth — the last untested aggregation level | exploratory surface leakage (no named B) | **null** |
| **FO.06** | repeater/one-off = Z₂ leaf classes: exactly two morphological modes; morphology predicts repetition | diagnostic (prime-2; default astro) | **not_confirmed_not_refuted** |
| **FO.07** | S8 on data (v1.3): character classes as BLOCK structure of the burst-observable covariance | operator-structure probe | **consistent** (blocks real, Bonferroni p = 0.006 — but the partition IS the standard Faraday-vs-emission sector split, Rand 1.0) |
| **FO.08** | S15 hole search (v1.3): FORBIDDEN region in (DOL, DOC) instead of peaks | operator-structure probe | **null** (largest hole 0.30 vs marginal-preserving null 0.55, p = 1.0) |
| **FO.09** | rank drop (v1.3): delay-embedded dynamics on ≤ 3 modes ('rank 3, not 2, not 5') | operator-structure probe | **null** (median effective rank 0 in both energy sources — memoryless) |
| **FO.10** | causal asymmetry (v1.3): time arrow in within-session energy sequences | operator-structure probe | **null** (reversal-null Bonferroni p = 1.0 — arrow-free cascade) |

## Data (all committed in sibling experiments; nothing fetched)

- **FRB 20240114A** — FAST pol catalog v5 (Wang+2026), 6134 bursts: MJD, RM±err, DM,
  Weff, DOL, DOC, PA (FO.02/03/04, and FO.05 times).
- **Blinkverse export** — multi-source (FO.05; deduplicated by (source, MJD@1e-6 d);
  FRB 20240114A excluded there — anti double-counting).
- **CHIME Cat2 repeaters** (repeater-cascade) — FO.05 instrument-independent leg.
- **CHIME Cat1** (VizieR) — FO.06 (excluded_flag = 0, first sub-bursts, clean
  fitburst width; 474 events, 59 repeater bursts, 126 flagged out).

## Results (seed 0, `results/results.json`; seed 1 cross-checked, identical verdicts)

- **FO.01 (theory contract): 5/5 PASS.** (C1) the uniform functional is *exactly*
  blind: max |1·Tⁿp − 1| = 9.8e-15 — the trivial character is a left eigenvector of
  any stochastic transfer. (C2) the coherent threshold-intensity readout with uniform
  coupling produces burst trains statistically indistinguishable between the kernel
  seam {1, 64/729, 1/729} and a scrambled seam {1, 0.55, 0.30} (KS D = 0.006–0.009,
  p ≥ 0.47, 20k runs) — **the 20+ FRB intensity/timing nulls are what this ontology
  predicts.** (C3) a character-resolved readout recovers 64/729 to 1e-12. (C4) an
  unequal-weight coupling makes the *same* functional discriminating (KS D = 0.061,
  p = 5e-33) — invisibility is a property of B, not of the channel.
- **FO.02 (common-rate medium operator): data_limited.** 89 nightly sessions; ACF
  single rates RM 0.019/d, DM 0.016/d, log₁₀Weff 0.087/d, DOL 0.077/d. The joint
  shared two-rate fit lands at ratio 4.20, but **AIC prefers per-observable single
  rates (8.07 vs 12.54)** — the nightly medium state does not require a second rate;
  the kernel ratio is not the closest grid point (placebo 4.5 is), OU-null p = 0.55.
  The honest reading: at nightly sampling the relaxation is single-memory; a
  common-rate test needs intra-night injection events (RM jump + relaxation within
  hours) — a bespoke-data project, not available in the v5 nightly cadence.
- **FO.02b (intra-session common rate, v1.2 addendum): data_limited — but an
  informative negative that sharpens FO.02 decisively.** The data FO.02 v1 said it
  needed already exist in committed catalogs: per-burst RM *within* sessions
  (v5: all 35 sessions with ≥ 30 RM bursts reject constant RM at χ²_red 77–337;
  Blinkverse FRB 20201124A / Xu+2022: 1131 per-burst RM, 12 sessions, spans
  50–240 rad/m² over 2–3.5 h). The preregistered MEMORY gate (first ACF bin vs
  time-shuffle) is injection-validated on the real timestamps (OU relaxation at
  τ = 120/600/1800 s detected in 31–34/35 v5 sessions and 8–10/12 20201124A
  sessions; white-noise false-positive 3/35 and 0/12) — and the real data fail
  it: **33/35 (v5) and 12/12 (20201124A) sessions show NO temporal memory** in
  any medium observable; the 2 memory-passing v5 sessions need no second rate
  by AIC. Reading: the strong intra-session RM variance is **per-burst
  (magnetospheric/sightline), not a relaxing medium state** — the
  burst-sampled "medium" has nothing to relax on burst timescales, so the
  two-rate ratio is untestable at this cadence (per prereg kill (i)). Combined
  with FO.02 v1 (nightly: memory exists but single-rate), the
  'FRB-as-medium-measurement' ontology now survives only in the untested
  hours-to-days relaxation band or via a true tracked injection event
  (RM-jump source of the FRB 20190520B class with dense monitoring — that RM
  table is login-walled, documented in frb-tfpt-signatures/data/README). 3 sessions pass the
  2.8-period reach gate in ln τ_mod (2.82 / 2.85 / 3.16 periods; 32 sessions below
  gate); survive-all p per session 0.84 / 0.45 / 0.59; **Fisher p = 0.81**. The first
  named-clock FRB comb is null like every observer-time comb; the predicted
  ε = 1.7 % stays behind the amplitude wall (that leg remains data_limited).
- **FO.04 (parity without rate): consistent — all three predictions hold.**
  (a) **no μ₄ pointer**: the vm2-only first run fired nominally at m=4 (A4 = 0.0424
  vs null 0.0127, p = 0.0005) — the dated v1.1 specificity battery resolves it:
  the odd/even harmonic placebos fire equally (z3 = 3.6, z4 = 4.4, z6 = 4.2 — generic
  misfit: the two PA modes sit 60.2° apart, not 90°), and a 3-component smooth null
  absorbs m=4 completely (**p = 0.64**) ⇒ PA-distribution misfit, not a μ₄ class
  structure. (b) **switches are rate-free**: 376 waiting-time ratios, tooth
  enrichment 0.74, p = 1.0; no comb-gated session. (c) **classes persist**: 45/45
  sessions share the global dominant PA mode, binomial p = 2.8e-14. Diagnostic
  consistency — never support (the same phenomenology is standard magnetospheric
  physics).
- **FO.05 (episode transfer): null.** 8 sources clear the episode gates (5-d
  definition): quiescence-gap Bonferroni **p = 1.0** (7 sources), episode-energy
  Bonferroni **p = 0.44** (7 sources); the 10-d flagged secondary agrees. Largest
  single-source excursion: FRB20190520B energy enrichment 3.0 at p = 0.063 — not
  significant, single source. The last untested aggregation level closes null.
  (Known dominant systematic on record: observing-schedule selection.)
- **FO.06 (leaf classes): not_confirmed_not_refuted.** Morphology strongly predicts
  repetition (CV-AUC **0.833** vs label-permutation null 0.493, p = 0.001; repeater
  fraction per GMM mode 0.6 % vs 19.9 %, odds ratio 44.9 — replicates Pleunis+2021,
  default reading astro/selection), **but** BIC prefers **k = 3** (−1218.6) over
  k = 2 (−1182.3) — the "exactly two classes" prediction does not hold on the only
  uniform-survey catalog. Caveats on record: 400–800 MHz bandwidth censoring,
  exposure/beam selection uncorrected.

### v1.3 operator-structure round (FO.07–FO.10, seed 0; seed 1 identical)

The strategy shift from "where do we see 2/3, μ₄, comb?" to "where is an
operator forced not to mix states" (SIGNATURES.md 1b), run on data:

- **FO.07 (covariance character blocks): consistent — structure real, content
  standard.** 5694 complete 10-observable bursts (v5, within-session
  median/MAD-standardised). The correlation matrix IS strongly block-diagonal
  beyond a spectrum-preserving random-rotation null (k=2: S_off = 0.052 vs null
  median 0.273, p = 0.002; Bonferroni p = 0.006) — **but** the found partition
  is exactly `{DOC, cos2PA, sin2PA, RM_res}` vs the rest: the
  Faraday/geometry-vs-emission sector split every magnetospheric model
  predicts (Rand agreement 1.0 with the preregistered physics partition —
  v1.3.1 escalation gate; the first-run `hint_flag` stays on record). No
  character-class content beyond known physics.
- **FO.08 (polarimetric null space): null.** 6107 S/N ≥ 20 bursts; the largest
  empty disk in (DOL, DOC) has r = 0.302 (at DOL 30 %, DOC −57 %), while the
  marginal-preserving joint-permutation null reaches median 0.551 → p = 1.0.
  The visible voids are entirely marginal-driven; **no joint forbidden
  region** in the only full-Stokes catalog in hand.
- **FO.09 (rank drop): null.** Within-session log-energy Hankel rank (delay 8,
  shuffle-calibrated): median effective rank **0** in both sources (Li+2021:
  27 sessions, occasional storm-drift sessions up to 8; Zhang+2023: 10
  sessions, median 0) — memoryless, no 3-mode manifold. The multivariate v5
  medium leg (median 3) is flagged **descriptive only**: it conflates the
  static FO.07 sector correlations with dynamics and is not evidence of
  3-mode dynamics given the FO.02b no-memory result.
- **FO.10 (causal asymmetry): null — a genuinely new bound.** Increment
  skewness 0.048 / 0.002 and Pomeau asymmetry −0.051 / −0.006 (Li+2021 1582 /
  Zhang+2023 1032 increments), all reversal-null p ≥ 0.36, Bonferroni p = 1.0:
  **within-session energy sequences are time-reversible at catalog
  statistics.** An arrow-free cascade bounds every "directed recovery" reading
  of burst trains — and is exactly what the FO.01 amplifier predicts (the
  threshold readout of a hidden relaxation carries no visible arrow).
  Open control on record: earthquake aftershocks (known irreversible) not run
  — USGS data gitignored in recovery-comb-domains.

**Audit note (on record, the FRB.06/KC.03 lesson repeating):** the FO.04 m=4
statistic against the *vm2-only* bootstrap was a nominal hit on the first run. The
specificity battery (odd-harmonic placebos + 3-component smooth null) was added as a
**dated v1.1 prereg addendum** before re-running; it typed the excess as null-model
misfit. First-run verdict `tension` and the addendum are both preserved in
`hypotheses/frb_ontology_v1.yaml`.

## Bottom line

The ontology round sharpens the picture rather than softening it: the **only**
FO reading positively supported is the one that *predicts* invisibility (FO.01,
contract-level) plus the rate-free parity typing (FO.04). Both channels with a
named B or named clock — the two categorically new probes — come back
null/data_limited at today's data quality. FO.02b closes the intra-night leg
FO.02 asked for: the burst-sampled medium shows **variance without memory** in
both sources, so there is no relaxing state for the operator to act on at burst
cadence — the medium-measurement reading is disfavoured there and survives only
in the untested hours-to-days band or via a tracked RM-injection event. FO.03
is amplitude-walled like every comb. The episode level closes null (FO.05), and
the two-class ontology fails its sharpest morphological test (FO.06: three
modes, not two). No axis produces support; nothing is promotable.

## Reproduce

```bash
. ../tfpt-discovery/.venv/bin/activate      # shared venv (numpy/scipy/sklearn)
python tests/test_frozen_kernel.py          # 11/11 kernel guard
PYTHONPATH=src python -m tfpt_fo.cli audit
PYTHONPATH=src python -m tfpt_fo.cli analyze --seed 0    # -> results/results.json
python ../theory-contracts/fo01_transduction_invisibility.py   # FO.01 contract
```

## Layout

```
hypotheses/frb_ontology_v1.yaml   # preregistered axes + dated v1.1 addendum
src/tfpt_fo/constants.py          # frozen kernel from the axioms (guarded)
src/tfpt_fo/data.py               # committed-catalog loaders (anti double-counting)
src/tfpt_fo/fo02_common_rate.py   # FO.02 shared two-rate ACF fit + OU null + placebos
src/tfpt_fo/fo02b_intra_session.py # FO.02b intra-session common rate (memory gate, injection-validated)
src/tfpt_fo/fo03_state_clock.py   # FO.03 tau_mod comb (reach gate, perm + rank nulls)
src/tfpt_fo/fo04_parity.py        # FO.04 m=4 battery + switch teeth/comb + persistence
src/tfpt_fo/fo05_episodes.py      # FO.05 episode gaps/energies on the teeth
src/tfpt_fo/fo06_leaf_classes.py  # FO.06 GMM mode count + label AUC (CHIME Cat1)
src/tfpt_fo/fo07_covariance.py    # FO.07 covariance block structure (spectrum-preserving null)
src/tfpt_fo/fo08_nullspace.py     # FO.08 largest-empty-disk hole search (joint-permutation null)
src/tfpt_fo/fo09_rank.py          # FO.09 Hankel effective rank (shuffle-calibrated)
src/tfpt_fo/fo10_arrow.py         # FO.10 time-arrow statistics (reversal null)
tests/test_frozen_kernel.py       # kernel byte-guard (11 checks)
results/results.json              # committed run (seed 0)
```

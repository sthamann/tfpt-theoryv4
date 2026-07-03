# qpe-recurrence — the frozen recovery kernel on quasi-periodic eruption timings

**Verdict (v1.0, seed 0): QPE.01 `null` (2 sources, quantified sensitivity) ·
QPE.02 `data_limited` (triplet-starved) · QPE.03 `data_limited` (range-blind).**

> **Firewall:** QPEs are **not** direct Hawking emission and **not** new gravity. The
> eruption mechanism (disk collisions / EMRI / instabilities) is an **accretion /
> "horizon-adjacent surface" channel** — legitimacy typing identical to
> `recovery-comb-domains` A5 (AGN-disk TDE). Every result is a **search target, never a
> claim**; a hit would be a universal-DSI/ratio coincidence in the eruption engine, never
> TFPT confirmation, until it recurs in ≥2 independent worlds.

## Why QPEs

Quasi-periodic eruptions (GSN 069, eRO-QPE1–4, …) are a genuinely **unexplained
post-2019 phenomenon class** — repeating soft-X-ray eruptions from galactic nuclei, the
only known *repeating* transient located directly at an SMBH. Every published orbital
model has trouble (the eRO-QPE2 super-period paper concludes "no reliable solution").
Within the TFPT recovery-search program they are the closest horizon-*adjacent*
repeating system available — which is exactly why the firewall above matters: proximity
to a horizon does not make the eruption clock a boundary-recovery observable.

## Preregistration and data

- **Hypotheses frozen before analysis:** `hypotheses/qpe_tfpt_v1.yaml` (QPE.01–03,
  kernel values, nulls, gates, kill conditions, language rules). Kernel byte-guarded by
  `tests/test_frozen_kernel.py` (12 checks, incl. a data-token denylist).
- **eRO-QPE2:** 32 eruption arrival times, Table B.1 of arXiv:2604.09788 (XMM1–4
  campaign + XRT/NICER/EP; ~2.24 h recurrence), machine-extracted — 5 contiguous
  (`ΔN_QPE = 1`) blocks → 17 recurrence times.
- **GSN 069:** 9 recurrence times, Table A.1 of Miniutti et al. 2023, A&A 670, A93
  (XMM3–XMM6 + Chandra; ~9 h recurrence), curated with an explicit legibility rule
  (`data/README.md`).

## Results (deterministic, `--seed 0`)

| test | prediction | result |
|---|---|---|
| **QPE.01** recurrence-ratio ladder | pile-up at `{2/3, 8/27, 64/729}` (±0.10 dex, +inverses) | **null in both sources.** eRO-QPE2: 12 ratios, 0 hits, max\|log r\| = 0.022 dex, spread 0.009 dex — the step tooth (0.176 dex) is **>17× the observed spread** away: a kernel step in the QPE clock is *excluded*, not merely unobserved. GSN 069: 4 ratios; the single loose "hit" (XMM6 ratio 1.24 within 0.10 dex of the *inverse* step 3/2) is reproduced by the shuffle null with p = 1.0 → null by the preregistered rule. |
| **QPE.02** walled-clock gap ratio (bend 2.7095, wall N=3) | clock pile-up on monotone triplets | **data_limited**: only 3 monotone recurrence triplets exist (QPE clocks alternate long/short by construction) — underpowered, honestly reported. |
| **QPE.03** log-periodic comb (`ω = 2.583`) | comb *if* the >2.8-period ln-range gate passes | **data_limited (range-blind)**: best campaign reaches **0.80 periods** — quasi-periodic point processes have `ln`-range ~ `ln N`, far below the gate; stacking raises amplitude, never range (PG.06 machine check). |

The QPE.01 null is the informative product: the QPE recurrence clock is *precise
enough* (sub-percent timing) that a kernel step would have been unmissable — this is a
**well-powered null**, unlike the range-blind comb legs.

## What would change the verdict

1. A QPE source with secular recurrence-time *decay* spanning ≥1 decade in `ln(τ)`
   (e.g. a QPE turn-off like GSN 069's 2020 disappearance densely monitored) would
   activate QPE.03 for real.
2. ≥5 monotone recurrence triplets (e.g. the XMM6-style monotone drift epochs) would
   power QPE.02.
3. More sources (eRO-QPE1/3/4, Swift J0230) with published per-eruption timings extend
   QPE.01 replication.

## Reproduce

```bash
. experiments/tfpt-discovery/.venv/bin/activate
cd experiments/qpe-recurrence
python tests/test_frozen_kernel.py                       # 12 guard checks
PYTHONPATH=src python -m qpe_recurrence.cli analyze --seed 0
```

Deterministic at fixed seed; writes `results/results.json`.

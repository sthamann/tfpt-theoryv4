# hfqpo-ladder — BH high-frequency QPO 3:2 pairs vs the TFPT kernel step 3/2

> **Firewall (read first):** TFPT's 3/2 is a **relaxation-ladder step** (from `N_fam = 3`:
> `rate(n) = -6 ln(1 - n/3)`, consecutive scale factor `3/2`), **not** a two-oscillator
> frequency ratio. HFQPO pairs are conventionally two simultaneous oscillation modes
> (relativistic precession, or the Kluźniak–Abramowicz **3:2 parametric resonance** `ν_θ:ν_r`).
> Mapping a two-oscillator ratio onto a ladder step is **non-canonical** — TFPT derives no
> HFQPO production mechanism. A bare 3:2 match is therefore **coincidence-risk**: GR parametric
> resonance selects 3:2 on its own, and detection selection clusters ratios near 3:2 even with
> no resonance at all (H2). **Only the ladder test (H3) discriminates**, and even a ladder hit
> would be **`[C]`-tier** until the mapping is derived. The GR-resonance explanation is the
> standing favorite. This is a **search target, not a claim**; nothing here is `[E]`.

## What is tested

Four BH X-ray binaries show twin HFQPO pairs consistent with 3:2
(GRO J1655−40 441/298 Hz, XTE J1550−564 276/184 Hz, GRS 1915+105 168/113 Hz,
H1743−322 242/166 Hz). Two readings make **different third-frequency predictions**:

| reading | third frequency | integer lines (`ν₀ = ν_u/3 = ν_l/2`) |
|---|---|---|
| **TFPT geometric ladder** | tooth at `ν₃ = (3/2) ν_u` (661.5 / 414 / 252 / 363 Hz) | **forbidden** |
| **GR resonance / harmonics** | none required | expected (e.g. `4ν₀`, `ν_l/2`) |

The tooth and the nearest integer line (`4ν₀`) are `ν_u/6 ≥ 26 Hz` apart in every source —
resolvable at HFQPO widths. Everything (statistics, thresholds, MC design, verdict rules,
archival design) preregistered in `hypotheses/hfqpo_v1.yaml` **before** computing on the
table; the kernel is frozen and guarded (`tests/test_frozen_kernel.py`, all constants shared
bit-identically with `recovery-comb-domains`).

## Data (published tables only; `data/measurements.json` with full references)

Verified against the papers 2026-07-02: Motta+ 2014a (MNRAS 437, 2554), Remillard+ 2002
(ApJ 580, 1030), Remillard & McClintock 2006 (ARA&A 44, 49), Remillard+ 2006 (ApJ 637, 1002),
Belloni+ 2012 (MNRAS 426, 1701), Belloni & Altamirano 2013 (MNRAS 432, 10), Motta+ 2022
(MNRAS 517, 1469), plus dynamical masses (Beer & Podsiadlowski 2002; Orosz+ 2011; Reid+ 2014;
Yanes-Rizo+ 2022; GRAVITY 2022). The census **includes the counterexample** XTE J1859+226
(227.5/128.6 Hz, ratio 1.769 — a genuine published pair far from 3:2) and carries the
**anti-kernel record**: XTE J1550−564's marginal broad 92 Hz = 184/2 (Remillard+ 2002 modelled
92:184:276 as integer 1:2:3) and GRS 1915+105's 34/68 Hz integer pair. Sgr A* flare QPOs
(1.445/0.886 mHz, central ratio 1.63) are **contested** and preregistered as exploratory only.

## Results (deterministic, seed 0; `results/results.json`)

**H1 — exact-3/2 point test.** Pulls vs exactly 3/2: J1655 −0.96σ, J1550 ±0.00σ,
GRS 1915 −0.19σ, H1743 −0.89σ → combined χ² = 1.75 (dof 4), **p = 0.78**: the four pairs are
statistically consistent with exactly 3/2. But **XTE J1859+226 sits +9.2σ from 3/2** (and off
the ladder: log₁.₅ 1.769 = 1.41) — 3:2 is **not universal** among BH HFQPO pairs. Verdict:
**`consistent`** — and ambiguous by construction (see H2).

**H2 — selection null (the Belloni/Boutelier deflator).** Monte-Carlo (200 000 trials) of the
Boutelier+ 2010 mechanism: two linearly correlated frequencies whose joint detection is
weighted by an equal-rms window. With the window anchored at the 3/2 crossing (empirically
where it sits: Török 2009), **selection alone produces a ≥4-of-5 cluster within ±0.05 of 1.5
in 18.5% of trials** (per-source probability 0.50). Unanchored or unselected: ~0.05%. The
observed clustering **does not beat the anchored selection null**, so H1 consistency carries
no discriminating weight — for TFPT *or* for the resonance model.

**H3 — ladder discriminator (the decisive test; literature stage).** No published search ever
targeted `ν₃ = 1.5 ν_u`, although the teeth lie inside the band the RXTE PCA archive searches
covered (Belloni+ 2012 searched 100–1000 Hz over 7108 observations; 450 Hz was detected at
4.5% rms in the hard band, so the instrument reaches the teeth). Census per source: J1655 —
nothing above 450 Hz ever published; J1550 — closest existing constraint is a *generic*
1–1.8% rms (3σ) in-band limit on any additional HFQPO in the stacked ~275 Hz group
(Varniere & Rodriguez 2018), not tooth-targeted; GRS 1915 — systematic search found 49/51
detections at 58–72 Hz, nothing at 252 Hz; H1743 — 50–2000 Hz searched, no feature near
363 Hz reported, no limits given. Meanwhile the only published third-frequency structures are
**integer lines** (92 = 184/2; 34/68 Hz) — points to the harmonic side. Verdict:
**`data_limited`** — with the archival next stage fully specified in the YAML (HEASARC RXTE
PCA event data; ObsID groups per source: 10255-01-* J1655, 30188-06-*/30191-01-* J1550,
80138-06-* H1743, BA12 epochs GRS 1915; stacked PDS in the published state selections;
Lorentzian fits at tooth and integer line; ≥4σ after a 2-frequency × 4-source trials
correction, else 3σ % rms upper limits). Deliberately **not** run here.

**H4 — frozen-kernel guard.** ALL PASS: step = 3/2 exact from `N_fam = 3` (a `Fraction`, no
fit, no SI input); tooth arithmetic; geometric teeth provably disjoint from integer harmonics
(the discriminator is well-posed); `λ = (3/2)⁶`, `ω = 2.5827`, `ε ≈ 0.017` bit-identical to
the shared `recovery-comb-domains` detector; H2 design constants match the YAML.

**Overall verdict: `data_limited`.** The 3:2 cluster is real but cheap (H2); the one test that
could distinguish a TFPT-ladder reading from GR parametric resonance (H3) has never been done
in the literature and is specified as the next stage. The honest current standing: **GR
resonance favored**, TFPT reading unproven and non-canonical, decisive data reachable in the
public RXTE archive.

## Reproduce

```bash
. ../tfpt-discovery/.venv/bin/activate             # shared venv (numpy); do NOT pip install
PYTHONPATH=src python tests/test_frozen_kernel.py  # H4 guard (must ALL PASS)
PYTHONPATH=src python -m tfpt_hfqpo.cli analyze    # H1+H2+H3 -> results/results.json
PYTHONPATH=src python -m tfpt_hfqpo.cli audit      # print frozen kernel constants
```

## Layout

```
hypotheses/hfqpo_v1.yaml         # preregistered protocol (frozen before the data pass)
data/measurements.json           # published pair table + masses + full references (committed)
src/tfpt_hfqpo/constants.py      # frozen kernel: step 3/2 exact, ladder/harmonic arithmetic
src/tfpt_hfqpo/point_test.py     # H1 exact-3/2 point test (chi^2 across 4 sources)
src/tfpt_hfqpo/selection_null.py # H2 Boutelier/Barret/Torok selection-null Monte-Carlo
src/tfpt_hfqpo/ladder.py         # H3 ladder discriminator: literature census + verdict
src/tfpt_hfqpo/cli.py            # `tfpt-hfqpo {analyze, audit}`
tests/test_frozen_kernel.py      # H4 guard: axioms, arithmetic, shared-kernel bit-identity
results/results.json             # committed deterministic summary
```

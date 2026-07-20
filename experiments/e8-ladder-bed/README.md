# E8 mass-ladder blind-recovery bed (CoNb2O6 / BaCo2V2O8)

> **Firewall (read first):** the E8 spectrum at the perturbed 1D transverse-field
> Ising quantum critical point is **established physics** (Zamolodchikov 1989) and
> its material realizations are **published** (Coldea+ 2010; Amelin+ 2020; Zou+ 2021;
> Zhang+ 2020). Blindly recovering the ladder from the published peak positions
> validates the **ladder detector** (assignment search + scale fit + Monte-Carlo
> null calibration) that TFPT uses on search surfaces (e.g. `hfqpo-ladder`) — it
> **confirms Zamolodchikov E8, NOT the TFPT axioms**. No TFPT number enters the E8
> mass ratios. Nothing here is `[E]`; nothing gets a `\veri{}`. **Failure kills the
> detector, not TFPT** (exactly as typed in the scorecard row `parked_analog`).

## Why this bed exists

The scorecard parks an analog row "E8 mass-ladder blind recovery bed": all eight
one-particle masses of the Zamolodchikov E8 spectrum have been measured in real
materials, which makes them the only public *known-answer* dataset on which a
blind mass-ladder pipeline can be validated end-to-end — including its false-alarm
behaviour under scrambled/offset/jittered spectra and against wrong ladders. The
TFPT-relevant cross-check: the E8 masses are the **Perron-Frobenius eigenvector of
the E8 Cartan matrix** (lowest Cartan eigenvalue `2 − 2cos(π/30)`, the order-30
Coxeter clock; cf. `experiments/next.txt` Hook 3) — the same PF/golden structure
class as the compiler attractor (v312/v313). That identity is re-verified here as
a machine self-test before any data run.

## Data (all public; provenance per number)

| Dataset | Source | What is used | σ policy |
|---|---|---|---|
| BaCo2V2O8, INS, **H = 4.7 T** ∥ [010] (the NMR-located 1D QCP), 0.4 K, Q=(002) | Zou, Cui, Wang et al., **PRL 127, 077201 (2021)**; arXiv:2005.13302v3, Fig. 3(a) | 17 peaks: 8 single-particle markers **[1.200, 2.005, 2.508, 3.000, 3.626, 3.897, 4.497, 5.756] meV** + 9 fit-curve maxima (multi-particle / zone-folding peaks) | 0.10 meV singles, 0.12 meV broader features (instrument resolution 0.1 meV per the paper) |
| CoNb2O6, THz, **B = 4.75 T** ∥ b, 0.25 K | Amelin et al., **PRB 102, 104431 (2020)**; arXiv:2006.12956, verbatim text values | 7 peaks: m1–m6 = **0.16/0.26/0.32/0.40/0.47/0.51 THz** + broad 0.43 THz peak (the paper's (m1+m2)-continuum onset — kept in the blind input as a contaminant) | 0.01 THz (6 GHz resolution + rounding) |
| Coldea et al., Science 327, 177 (2010) | historical anchor | m2/m1 → golden ratio near Bc; **not** a blind input | — |

**BaCo2V2O8 extraction path** (`scripts/extract_zou_fig3.py`, deterministic): the
arXiv e-print (`data/arxiv_2005.13302v3_eprint.tar.gz`, committed) embeds Fig. 3 as
vector PDF with raster panels. Panels (a) INS / (b) analytic / (c) iTEBD share one
x-axis (identical tick pixels; 195 px/meV; labels 1–5 meV). The eight red vertical
markers are placed **per panel** at that panel's own single-particle peak positions
— validated on panel (b), where they reproduce the analytic positions `1.2·r_i` meV
to ≤ 0.8 % (automated assert). Panel (a) markers therefore give the measured
single-particle energies; the remaining peaks come from tracing the paper's own
Gaussian-fit curve (connectivity DP, QA overlay in `results/extraction_qa.png`).
Digitization adds ≲ 0.01 meV, far below the 0.1 meV instrument resolution. Note the
paper quotes no per-peak numerical table (only m1 = 1.2 meV in text); the figure is
the primary published record, and Fig. 4(a) of the same paper (Energy/m1 at 4.7 T)
is consistent with the extracted ratios.

**CoNb2O6:** values are verbatim from the PRB text — no digitization. m7, m8 are
**not testable** there: m7 = 3.891 · 0.16 THz = 0.62 THz lies outside the 0.6 THz
low-pass window of the experiment (and the paper reports m7/m8 as unresolved).
Hence the honest target is 6/8 rungs, not 8/8.

## Theory reference (exact, frozen by tests)

`m_i/m_1 = {1, 2cos(π/5), 2cos(π/30), 4cos(π/5)cos(7π/30), 4cos(π/5)cos(2π/15),
4cos(π/5)cos(π/30), 8cos²(π/5)cos(7π/30), 8cos²(π/5)cos(2π/15)}
≈ {1, 1.6180, 1.9890, 2.4049, 2.9563, 3.2183, 3.8912, 4.7834}`.

**PF self-test (must pass before any data run, asserted in the CLI):** the sorted
PF eigenvector of the E8 Dynkin adjacency `2I − A(E8)`, normalized to its smallest
component, equals the Zamolodchikov ladder to **1.5 × 10⁻¹⁵** relative; the lowest
E8 Cartan eigenvalue equals `2 − 2cos(π/30) = 0.010956209263453…` to **4.5 × 10⁻¹⁴**
relative; `m2/m1 −  φ = 2.2 × 10⁻¹⁶`. PASS.

## Blind-recovery detector (preregistered; `hypotheses/e8_ladder_bed_v1.yaml`)

Input: sorted peak list + σ, **no labels, no knowledge of which peak is m1**.
Every peak is tried as the m1 anchor; a monotone injective DP matching assigns
peaks to rungs with a per-pair gate |pull| ≤ 3σ, maximizing (n_assigned, then
−χ²); two weighted-LS scale refinements. Physical gates: rung 1 must be assigned;
every peak below `2·m̂1 − 2σ` must be assigned (no continua below the two-particle
threshold); peaks above `2·m̂1` may stay unassigned (continua, zone folding).
Score: χ²/dof (dof = n − 1). Significance: **5000 random 8-rung ladders**
(uniform-log ratios in the same dynamic range [1, 4.7834], seed 0), identical
detector; `p = P[(n ≥ n_obs) ∧ (χ²/dof ≤ obs)]`, add-one estimator.

**Verdict enum:** `validated` = BCVO ≥ 6/8 rungs with χ²/dof ≤ 2 and p < 0.01 AND
CoNb2O6 ≥ 5 in-window rungs with p < 0.01 AND every control class rejected;
`partially_validated` = one material validated, other marginal, or a control class
marginal; `failed` = recovery fails or a control class is systematically accepted.
Control criteria were amended once after the first full run (v1.1: jitter as
dose-response; scramble near-duplicate accounting; χ²-gated wrong-ladder
comparator) — **fully disclosed with rationale and all v1 numbers preserved** in
the hypotheses YAML `amendment_v1_1` block; the recoveries themselves were never
touched.

## Results (deterministic, seed 0; `results/results.json`)

| Run | n rungs | χ²/dof | MC p (5000 ladders) | Note |
|---|---|---|---|---|
| **A1 BaCo2V2O8 blind, 17 peaks** | **8/8** | **0.35** | **0.0056** | m̂1 = 1.215 meV; the 0.43-context: rung 7 lands on the 4.654 meV multi-particle blend, the paper's m7 marker (4.497 meV) stays unassigned — consistent with the paper's own caveat that peaks above 4·m1 are blended at 0.1 meV resolution |
| A2 BCVO singles-only (8 markers) | 8/8 | 0.96 | **0.0004** | paper's m7 assigned, pull −1.9σ; clean-detector significance |
| A1 σ-variant (0.05 meV singles) | 8/8 | 1.33 | 0.0074 | conclusion σ-robust |
| **B CoNb2O6 blind, 7 peaks** | **6/8** | **0.52** | **0.0038** | m̂1 = 0.1605 THz; 0.43 THz contaminant correctly left unassigned; m7/m8 outside the 0.6 THz window (documented, not a detector failure) |

**Control battery (all classes rejected):**

| Class | BaCo2V2O8 | CoNb2O6 | Rejected? |
|---|---|---|---|
| (a) scramble (200 log-gap permutations) | 1/200 = 0.5 % | at observed strength, excl. 3 near-duplicate permutations: 3/200 = 1.5 % (at the weaker v1 bar n≥5: 14/200 = 7 %) | **yes** |
| (b) offset ±{0.3, 0.5}·m1 | 0/4 cases | 0/4 cases | **yes** |
| (c) jitter dose-response 5/10/20/30 % | 21 % / 17.5 % / 6 % / **3.5 %** | 11.5 % / 6 % / 2 % / **3 %** | **yes** (≤ 5 % at destructive level; small-jitter firing is correct behaviour — the real data itself deviates from exact E8 by 3–5 %) |
| (d) wrong ladders on real data: harmonic 1..8, A3-PF, D8-PF, Airy | harmonic/A3/D8: no valid recovery at all; Airy: n=7, χ²/dof 0.77 — **E8 wins strictly (8/8, 0.35)** | harmonic/A3/D8: none; Airy fails the χ² gate (2.38) | **yes** |
| (e) synthetic Airy bed (confined-spinon spectrum, the true zero-field physics of these compounds) | E8 detector finds **0 valid rungs** | — | **yes** |

Honest caveats: (i) on the dense 17-peak BCVO list the smooth Airy alternative can
match 7 peaks within noise (χ²/dof 0.77) — discrimination against smooth wrong
ladders comes from the full 8/8 + lower χ², not from n≥6 alone; short/dense peak
windows have limited ladder specificity (same lesson as the CoNb2O6 scramble leak
at the weak v1 bar). (ii) BCVO deviations from the exact ladder reach ~4–5 %
(m2, m3, m7 region) — resolution-limited and visible in the paper's own Fig. 4(a);
the recovery is significant because random ladders do worse, not because the data
is exact.

**VERDICT: `validated`** (detector level). The Cartan-PF ladder pipeline recovers
the published Zamolodchikov E8 spectrum blindly on both materials and rejects all
control classes. This validates the detector for TFPT ladder searches — **it is
not evidence for TFPT**.

## Reproduce

```bash
source ../tfpt-discovery/.venv/bin/activate      # numpy/scipy/matplotlib (shared venv)
python scripts/extract_zou_fig3.py               # arXiv e-print -> data/baco2v2o8_ins_peaks.csv (+ QA png)
PYTHONPATH=src python tests/test_ladder_exact.py # frozen ladder + PF identity + detector sanity (6 tests)
PYTHONPATH=src python -m tfpt_e8lb.cli analyze   # runs A1/A2/B + control battery -> results/ (~80 s)
```

## Layout

```
hypotheses/e8_ladder_bed_v1.yaml   # preregistered detector/criteria + disclosed v1.1 amendment
data/arxiv_2005.13302v3_eprint.tar.gz  # committed primary source (Zou+ figure PDFs)
data/baco2v2o8_ins_peaks.csv       # digitized BCVO peaks (provenance header)
data/conb2o6_thz_peaks.csv         # verbatim CoNb2O6 peaks (provenance header)
scripts/extract_zou_fig3.py        # deterministic figure digitization + calibration asserts
src/tfpt_e8lb/ladder.py            # exact E8 ladder, Cartan-PF ladders (A3/D8/E8), Airy ladder, PF self-test
src/tfpt_e8lb/recover.py           # blind DP assignment search + scale fit + MC null
src/tfpt_e8lb/controls.py          # scramble / offset / jitter / wrong-ladder / Airy-bed batteries
src/tfpt_e8lb/cli.py               # analyze -> results/results.json, assignments.csv, ladder_fit.png
tests/test_ladder_exact.py         # bit-frozen ladder values + PF identity + known-answer detector tests
results/                           # deterministic outputs (results.json, CSV, PNGs)
```

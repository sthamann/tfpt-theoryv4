# TFPT lab-channel residuals — `F_transfer` from three independent experiments

`search.txt` §§7–9: stress the continuous transfer physics (`F_transfer`) from three
*completely different* laboratory systematics — a magnetic moment, a rare flavour
decay, and a dark-matter haloscope. A hit in one is interesting; hits in two with
unrelated systematics are hard to dismiss.

## Firewall / typing (all `[C]` — never upgraded to `[E]`)

- `Δaµ = 45/(2¹⁹π⁹)` is an **exact compiler number**; its reading as the muon
  anomalous-moment residual is a physical **bridge `[C]`**.
- The kaon branching ratios are a **downstream flavour bridge `[C]`** (external
  short-distance functions); the axion mass/relic is **frontier `[C]`** (dimensionful
  via `f_a`, relic-density model-dependent).

These are confrontations, **not** claims. Verdicts are deliberately **split** (per SM
baseline for g−2; per relic branch for the axion) so no single ampel hides a model
dependence.

## Results (deterministic; published values in `data/measurements.json`)

### Rare kaon K⁺→π⁺νν — **`[C]` downstream bridge, very strong consistency**
| release | data | TFPT | pull |
|---|---|---|---|
| NA62 2016–2022 (JHEP25) | (13.0 ⁺³·³₋₃.₀)×10⁻¹¹ | 9.45×10⁻¹¹ | −1.13σ |
| NA62 2016–2024 (La Thuile 26) | (9.6 ⁺¹·⁹₋₁.₈)×10⁻¹¹ | 9.45×10⁻¹¹ | **−0.08σ** |

TFPT 9.45×10⁻¹¹ is inside the bridge kill-window [7,12]×10⁻¹¹. KL→π⁰νν (3.33×10⁻¹¹) is
far below the KOTO 90%CL limit (2.2×10⁻⁹) → data-limited. This is the sharpest new
**consistency** point — but a downstream bridge, **not** a compiler hit.

### Muon g−2 Δaµ = 2.879×10⁻⁹ — **`[C]`, SM-baseline-dependent (no single verdict)**
| SM baseline | residual aexp−aSM | pull | status |
|---|---|---|---|
| WP2020 dispersive | (2.62±0.45)×10⁻⁹ | +0.58σ | **viable** |
| WP2025 lattice | (0.39±0.64)×10⁻⁹ | +3.92σ | **tension** |
| CMD-3-related | — | — | placeholder (data-limited) |
| future consensus | — | — | placeholder |

(Experiment: Fermilab final + BNL world average `116 592 071.5(14.5)×10⁻¹¹`, PRL 135,
101802 (2025). WP2025: `a_µ(SM) = 116 592 033(62)×10⁻¹¹`, arXiv:2505.21476 — the σ=62
supersedes the σ=63 previously carried here, moving the lattice pull 3.86σ → 3.92σ.)

The seam-vertex value sits on the *old* dispersive anomaly but is pushed to tension if
the 2025 lattice HVP holds — exactly the kill condition `search.txt §8` anticipated.
Reported per baseline; **no `confirmed`/`killed` ampel**.

**Kill condition (dated 2026-07-02):** if a data-driven (e⁺e⁻) HVP consensus emerges
consistent with the lattice/WP25 value (a CMD-3-side resolution), the TFPT g−2 bridge
is **dead** — the residual pins to ~0.4×10⁻⁹ and the seam-vertex reading sits at +3.9σ
today, hardening past 5σ as HVP errors shrink toward the 127-ppb experimental
precision. A KLOE-side dispersive consensus **restores the bridge to <1σ** (+0.58σ on
WP2020). **Watch:** MUonE first results (Phase-1 pilot run completed Jun–Aug 2025,
~5×10¹¹ events, Δα_had analysis underway; full run post-LS3); new e⁺e⁻→ππ data (BaBar
2009+2025 combination, arXiv:2601.16587, keeps the dispersive prediction in tension
with the FNAL measurement; BESIII/Belle II/CMD-3/SND remeasurements on 1–2 yr
timescales; KLOE vs CMD-3 tension >5σ at the ρ peak); Theory Initiative **WP-3,
announced for ~2027–28** — the next consensus SM HVP is the decision point.

### Axion — **`[C]` frontier; marker + two relic branches**
- haloscope marker `m_a = 23.8 µeV (≈5.76 GHz)`: inside the HAYSTAC/CAPP band but **not
  excluded at DFSZ** → data-limited (exclusion depends on the dataset + coupling model).
- `DM.AXION.HILLTOP.01` (θᵢ=170°): `Ωₐh² ≈ 0.66` → **tension** (overcloses ~5.5×).
- `DM.AXION.SPINE.01` (θᵢ=3π/5=108°, from the spine quotient `N_fam/g_car=3/5`):
  **exploratory, FROZEN** before any run, acceptance band `0.08 ≤ Ωₐh² ≤ 0.16`. Not a
  prediction of record; the full finite-T solve lives in `experiments/ftransfer/axion_relic`.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-lab analyze            # or: PYTHONPATH=src python -m tfpt_lab.cli analyze
```

## Layout

```
src/tfpt_lab/constants.py   # Δaµ (exact), K BRs, axion mass — frozen targets
src/tfpt_lab/tests.py       # g-2 (both HVP), kaons (NA62/KOTO), axion marker
src/tfpt_lab/cli.py         # `tfpt-lab analyze`
data/measurements.json      # published values + references
```

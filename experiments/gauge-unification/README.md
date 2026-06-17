# sin²θ_W = 3/8 — the spectral-action unification, run against PDG data

> **Firewall:** a **downstream bridge**, `discriminative_power = weak`. `sin²θ_W = 3/8` is the
> *standard* SU(5)/SO(10) GUT value, shared by every grand-unified model — TFPT **inherits** it
> (it does not improve, or specifically own, the Standard-Model unification gap).

The discrete→dynamic completion (`v244`/`v245`) predicts, via Connes' spectral action and the
NCG normalisation of the carrier `SO(10) 16`, the boundary relation at the spectral scale `Λ`:

```
sin²θ_W(Λ) = 3/8 ,    g3 = g2 = √(5/3) g1   (g1 GUT-normalised)
```

This experiment **confronts that with the measured couplings** (PDG 2024) by running the SM gauge
couplings from `M_Z` upward (1-loop, plus a gauge-only 2-loop cross-check).

## Result (1-loop SM RGE vs PDG)

| quantity | value |
|---|---|
| `α_i⁻¹(M_Z)` (GUT-norm) | `(59.0, 29.6, 8.5)` |
| `α1 = α2` unification scale | `Λ₁₂ ≈ 1.0×10¹³ GeV` |
| `α3⁻¹` there vs `α_GUT⁻¹` | `36.8` vs `42.4` → **misses by 13%** (SM does **not** unify exactly) |
| `3/8 → sin²θ_W(M_Z)` (GQW) | **`0.2076`** vs measured **`0.23122`** |

**Verdict:** `3/8` is the standard GUT value (TFPT reproduces it exactly at `Λ`), but the pure-SM
running gives the **well-known ~10% GQW gap** at `M_Z` and the three couplings miss unification by
~13% — the universal Standard-Model non-unification, closed only by SUSY/threshold corrections,
**not a TFPT-specific result**. So: **consistent at the GUT level, not a precision hit**; typed
`data_limited` / `weak` in the scorecard. A full 2-loop + threshold + SUSY analysis is the open
sharpening (it is the same physics every SU(5)/SO(10) model faces).

This is the honest data confrontation of the new `v244`/`v245` signature — the headline is that
TFPT does **not** buy a better Weinberg angle than standard grand unification.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .   # numpy only
tfpt-gut analyze        # or: PYTHONPATH=src python -m tfpt_gut.cli analyze
```

## Layout

```
src/tfpt_gut/rge.py    # PDG inputs + 1/2-loop SM RGE + unification solve + GQW sin^2 prediction
src/tfpt_gut/cli.py    # `tfpt-gut analyze`
results/results.json   # committed summary
```

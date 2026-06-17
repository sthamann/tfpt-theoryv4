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

## Pati–Salam extension — the carrier-native two-step unification

The carrier is `D5 ⊕ A3 = SO(10) × SU(4)` — i.e. the **Pati–Salam** group
`SU(4)_c × SU(2)_L × SU(2)_R` (Spin(6)=SU(4), Spin(4)=SU(2)×SU(2)). So the *native*
high-scale gauge structure is not the SM but Pati–Salam. `pati_salam.py` runs the
two-step chain `M_Z →(SM)→ M_PS →(PS)→ M_GUT (SO(10): α4=α2L=α2R)` and asks: at what
`M_PS` does the carrier's own gauge structure unify, and is it the TFPT scalaron
scale `M_s = c3^{7/2} M̄_Pl ≈ 3.06×10¹³ GeV`?

| scalar variant | M_PS | M_PS/M_s | M_GUT | α_GUT⁻¹ | τ_p(p→eπ⁰) | proton decay |
|---|---|---|---|---|---|---|
| fermions only | 5.1e13 | ×1.66 | 2.6e15 | 45 | 6e33 yr | excluded |
| minimal (bidbl+(4,1,2)) | 4.2e13 | ×1.38 | 2.4e15 | 45 | 4e33 yr | excluded |
| +2nd bidoublet | 4.3e13 | ×1.39 | 2.0e15 | 45 | 2e33 yr | excluded |
| **+(15,1,1) of SU(4)** | 4.0e13 | ×1.32 | 5.8e15 | 46 | 1.5e35 yr | **SAFE** |
| +extra (4,1,2) | 3.4e13 | ×1.12 | 2.6e15 | 45 | 6e33 yr | excluded |

**Two findings.** (1) The required PS-breaking scale `M_PS` lands on the TFPT
scalaron scale to a factor **1.1–1.7, robustly across all scalar choices** (M_PS is
fixed by the SM run below it) — two *independent* TFPT scales (the gravitational
scalaron `c3^{7/2}M̄_Pl` and the gauge-unification scale) coincide to ~40%. (2)
**Proton decay selects the scalar content:** minimal choices give `M_GUT ≈ 2×10¹⁵`
→ `τ_p ~ few×10³³ yr`, **excluded** by Super-K (`2.4×10³⁴ yr`); a higher-`M_GUT`
choice (`+(15,1,1)`, the SU(4) adjoint) gives `M_GUT ≈ 5.8×10¹⁵`, `τ_p ~ 1.5×10³⁵ yr`
— **safe**, within Hyper-K reach.

**Honest scope `[O]`** (exploratory, not a closure): this **presupposes the carrier
`SO(10)` is *gauged*** (intermediate PS gauge bosons — the open theory fork, vs the
strict "SM gauge content, no new state"); it is 1-loop; `τ_p` carries a ~×3
hadronic-matrix-element uncertainty. It is a genuine, *falsifiable* TFPT-native
coincidence plus a sharp proton-decay kill-test — **not** a proof of unification.
Full data in `results/pati_salam.json`.

### Two-loop, leptogenesis, and the ~40% deviation

- **The deviation is mostly the loop order.** Going 1-loop → 2-loop (2-loop SM below
  `M_PS`, 1-loop PS above) pulls the scale ratio from `M_PS/M_s = 1.1–1.7` to
  **`1.0–1.2`** — one scalar variant lands at **`×1.02` (essentially exact)**. The
  residual `≲20%` is within PS-threshold corrections and the O(1) ambiguity between
  the *scalaron mass* `c3^{7/2}M̄_Pl` and the actual PS-breaking *VEV*. So the
  coincidence is exact to within the theory's own resolution — no anomaly to explain.
- **Proton decay is the binding constraint, not the scale match.** Two-loop *lowers*
  `M_GUT` (~1–3×10¹⁵), so at face value all minimal variants are Super-K-excluded;
  survival needs `M_GUT` pushed up (larger reps / GUT thresholds) or the ~×3
  matrix-element headroom. **This — not the scalaron match — is where the gauged-SO(10)
  branch lives or dies.**
- **Leptogenesis works at `M_R = scalaron`.** Seesaw with `m₃~0.05 eV` implies a
  natural Dirac Yukawa `y_D = √(m₃ M_R)/v ≈ 0.22`; the needed CP asymmetry is `~0.02%`
  of the Davidson–Ibarra bound (`M₁` in the thermal window). The apparent `~20×` vs
  the `y_D=1` seesaw value `6×10¹⁴` is absorbed into the (free) Dirac Yukawa — **not a
  tension.** So the scalaron consistently sets the PS-breaking, B−L and ν_R-Majorana
  scale at once.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .   # numpy only
tfpt-gut analyze                                  # SM sin^2 confrontation
PYTHONPATH=src python -m tfpt_gut.pati_salam      # Pati-Salam two-step + proton decay
```

## Layout

```
src/tfpt_gut/rge.py    # PDG inputs + 1/2-loop SM RGE + unification solve + GQW sin^2 prediction
src/tfpt_gut/cli.py    # `tfpt-gut analyze`
results/results.json   # committed summary
```

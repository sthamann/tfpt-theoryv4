# proton-decay — the TFPT proton lifetime vs Super-K, Hyper-K, DUNE, JUNO

**Status: `kill` (minimal 16-content, both loop orders) + `tension` (the surviving `+(15,1,1)`
branch at 2-loop) + `data_limited` (the `p→ν̄K⁺` channel).**

> **Firewall (read first).** Proton decay here is **conditional on the OPTIONAL gauged
> carrier-Pati-Salam → SO(10) UV branch (branch B)**. The default TFPT reading **A is
> boundary-only**, so `τ_p` is a **downstream / branch prediction — never a primitive
> compiler output**. Nothing here is `[E]` or `\veri{}`. Generic proton decay is a
> *generic-GUT* signature; the **TFPT-specific** sharpening is only: (i) the PS-breaking
> scale `M_PS` coincides with the independent **scalaron scale** `M_s = c₃^{7/2} M̄`;
> (ii) the E8 hull **forbids the 126 and supplies only ONE 45** (`v247`), so proton-safety
> is *structurally marginal*; (iii) the **minimal 16-content is already excluded**. If only
> the minimal PS stage is gauged, its SU(4) leptoquarks mediate rare **LFV** (`K_L→μe`), **not**
> `p→e⁺π⁰` (`v385`) — the dim-6 mode needs the full SO(10) `X,Y` bosons at `M_GUT`.

This confronts the TFPT-computed proton lifetime — the number the suite calls the *binding
constraint* on branch B (`v266` PS.PROTON.02, `v249` PS.RGTEST.01) — against the real limits.
It scans the **E8-allowed Higgs content × {1-loop, 2-loop} × an O(3) hadronic band** and emits
a verdict ∈ `{consistent, tension, kill, data_limited}` per channel/branch.

## Result (golden channel `p→e⁺π⁰`)

| content | loop | M_GUT / GeV | α_GUT⁻¹ | M_PS/M_s | τ_p / yr | vs Super-K (2.4×10³⁴) | verdict |
|---|---|---|---|---|---|---|---|
| minimal 16H | 1-loop | 2.40×10¹⁵ | 45.1 | ×1.38 | 4.19×10³³ | −0.8 dex | **kill** |
| minimal 16H | 2-loop | 1.29×10¹⁵ | 44.5 | ×1.22 | 3.43×10³² | −1.8 dex | **kill** |
| **+(15,1,1)** | 1-loop | 5.80×10¹⁵ | 45.5 | ×1.32 | **1.46×10³⁵** | +0.8 dex | **consistent** |
| **+(15,1,1)** | 2-loop | 2.80×10¹⁵ | 44.9 | ×1.18 | **7.72×10³³** | −0.5 dex | **tension** |

- **The minimal 16-content is excluded** (`kill`) at *both* loop orders — even the optimistic
  edge of the O(3) hadronic band stays below Super-K. The renormalisable 126 that would rescue
  it is E8-**forbidden** (`v247`).
- **The single E8-allowed 45 `+(15,1,1)`** is the *only* surviving content: `τ_p ≈ 1.46×10³⁵ yr`
  at 1-loop (`consistent`), sitting **right at the Hyper-K reach** (~6×10³⁴ yr @10 yr → 10³⁵ @20 yr)
  — a **dated, decisive kill-test**, not open-ended hope.
- **Latent 2-loop tension.** 2-loop lowers `M_GUT`, so the same `+(15,1,1)` gives
  `τ_p ≈ 7.7×10³³ yr < Super-K`. The central value is **already excluded**; only the optimistic
  edge of the O(3) band (or GUT-threshold headroom) keeps it from a clean kill → **`tension`**.
  Because the hull supplies just one 45, there is no larger-rep escape → proton-safety is
  structurally marginal.

## Second channel `p→ν̄K⁺` (DUNE / JUNO / SUSY-favoured)

In the **non-SUSY** dim-6 gauge mechanism, `p→e⁺π⁰` is the golden dominant mode and `p→ν̄K⁺` is
**subdominant**: `Γ(ν̄K⁺) = R_νK · Γ(e⁺π⁰)`, with `R_νK ∈ [0.1, 1.0]` an **external** hadronic/
flavour nuisance (*not* a TFPT primitive — exactly like `|Vcb|,|Vub|` in the rare-kaon bridge).
For the surviving `+(15,1,1)` branch this puts `τ(ν̄K⁺) ~ 5×10³⁵ yr` — **above even the next-gen
reach** (DUNE 1.3×10³⁴, JUNO ~10³⁴, HK ~2×10³⁴) → **`data_limited`**. So `ν̄K⁺` does **not**
sharpen the TFPT constraint; the confrontation bites in `e⁺π⁰`.

## Preregistration (frozen before touching the limits)

- **Inputs:** axiom `c₃ = 1/(8π)` → scalaron `M_s = c₃^{7/2} M̄ ≈ 3.06×10¹³ GeV`; measured SM
  couplings at `M_Z` (PDG) as RGE boundary conditions; E8-allowed content `{minimal_16H,
  +(15,1,1)_45}` (`v247`). No fitted exponents.
- **Rate:** `τ(p→e⁺π⁰) = 10³⁶ (M_GUT/10¹⁶)⁴ (α_GUT⁻¹/40)² yr` (SU(5)/SO(10) benchmark).
- **Bands:** hadronic `HAD_BAND = 3` (O(3)); band-softness `1.3` (an optimistic edge within
  30 % of a limit is a *tension*, not a clean kill); `R_νK ∈ [0.1, 1.0]`.
- **Verdict rule** (`src/tfpt_proton/proton.py`, not tuned to data): `consistent` if the whole
  band clears the current limit; `kill` if even the optimistic edge is comfortably below it;
  `tension` in between; `data_limited` if `consistent` but above the best next-gen reach.
- **Kill conditions:** the branch dies if the golden `e⁺π⁰` channel is excluded for *every*
  E8-allowed content (minimal is already dead; `+(15,1,1)` is the last stand), or if Hyper-K
  reaches 10³⁵ yr with no signal.

## Reproduces

`verification/v266` (PS.PROTON.02), `v249` (PS.RGTEST.01) and
`experiments/gauge-unification/results/pati_salam.json` — same two-step RGE, same betas, same
`τ_p` benchmark. The M_PS/M_GUT/α_GUT/τ_p values match `pati_salam.json`'s two E8-allowed rows.

## Run

```bash
# shared venv (numpy); do NOT pip install into it
source ../tfpt-discovery/.venv/bin/activate
cd experiments/proton-decay
PYTHONPATH=src python -m tfpt_proton.cli analyze   # confrontation + results/results.json
PYTHONPATH=src python -m tfpt_proton.cli audit     # kernel-freeze guard (axioms/betas/content)
```

## Layout

```
src/tfpt_proton/rge.py           # PDG boundary conditions + SM 1/2-loop gauge RGE
src/tfpt_proton/unification.py   # two-step PS->SO(10) solve; scalaron scale; E8-allowed content
src/tfpt_proton/proton.py        # tau_p formulas, hadronic + R_nuK bands, verdict rule
src/tfpt_proton/confront.py      # builds the confrontation + per-branch summary + narrative
src/tfpt_proton/cli.py           # `analyze` / `audit`
data/limits.json                 # external limits + future reach, with provenance (committed)
results/results.json             # deterministic CLI output (scorecard source)
```

Standalone search / confrontation; **not** in the verification suite, ledger or website. See
`data/README.md` for the experimental-limit provenance.

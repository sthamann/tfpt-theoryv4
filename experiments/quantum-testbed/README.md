# TFPT quantum testbed — catch the algebra at work

> **Firewall:** **internal-consistency** check, **no external data**, never load-bearing.
> `evidence_class = internal_consistency`, `stage = not_applicable` — the same basket as
> `recovery-channel`/Page-curve, **not** the same as CMB/Kaon.

`problem_1.txt` calls the strongest *quantum* signature *"TFPT scales in the entanglement
spectrum and in quench recovery curves"* and frames the whole programme as
**Topology → operator algebra → QFT** ("catch the algebra at work, don't look for matter
first"). This experiment builds the frozen recovery kernel `{1, (2/3)⁶, (1/3)⁶}` as a
quantum object and checks the predicted patterns — and, taking up the **reconsideration**
("could the signature be something other than a static ratio?"), it shows the kernel is
carried **dynamically**, as *discrete scale invariance*, not as a number in a histogram.

## What it checks (`src/tfpt_qtest/`)

| Channel | Construction | Result |
|---|---|---|
| **QT.01 entanglement spectrum** | Gaussian (free-fermion `Γ(t)`) state whose occupation spectrum **is** the kernel `{1,(2/3)⁶,(1/3)⁶}` | **exact identities**: surprisals `−ln ζ = {6 ln(3/2)=Δ, 6 ln 3}`, ratio `ln3/ln(3/2)=2.7095` (= the FRB.09 recovery-clock `g1/g2`), a **protected zero-surprisal (decoherence-free) mode**, Schmidt recovery `I_n=(2/3)^{6n}` |
| **QT.02 quench DSI + suppression law** | open-system relaxation of a **geometric rate ladder** `γ_k = γ₀·λ^{−k}`; test log-periodic ripple at `ω = 2π/ln λ` | the kernel reappears as a **log-frequency**; amplitude `~ e^{−π²/ln λ}`, so detectable **only** for the coarse **energy gap `(3/2)⁶`** (p≈0.002) and exponentially **invisible** for the carrier `3/2` (p≈0.97); non-geometric control **null** |
| **QT.03 free-fermion OTOC** | single-particle `H_TFPT` with the kernel-ladder spectrum; squared-commutator `C_ij(t)=|G_ij(t)|²` | ballistic operator spreading + on-site-return DSI test (exploratory) |
| **QT.04 exact walled clock** | the verification suite's exact discrete→dynamic clock `rate(n)=−6 ln(1−n/3)` (v124/v126/v147), pole at `n=N_fam=3` | **det-clean bend** `rate(2)/rate(1)=ln3/ln(3/2)=2.7095`, **protected floor** (`λ=1`), **hard wall** (no 3rd mode), sheet slope `2=\|Z₂\|`; turned into a **matched-filter waveform discriminator** (kernel recovery → recovers 2.7095; non-kernel → rejected) |
| **QT.05 anyon MTC (statistics)** | the carrier discriminant MTC `Z4×Z4`, `q=(5x²+3y²)/8` (v241/v242/v243) — sectors = particle types, spins = statistics, monodromy = S-matrix | **16 sectors → 6 bosons / 2 fermions (`θ=−1`, phase `π` = m=2) / 8 anyons**; **statistical phase quanta `π/4` (spin, 8th roots) and `π/2` (braiding)**; `c=8` (Gauss–Milgram); integrable factorised S, trivial on `(E8)₁`. The FRB.08 "fundamental m=2" is the **predicted fermion sector**, not a null |

## The reconsidered signature (why this matters)

Every static-ratio search (FRB.02–09, pulsar PG.01–04) came back **null**. QT.02 explains
*why* and what to do instead. A system relaxing to its fixed point through a geometric ladder
of modes has a **complex critical exponent** `α + iω`, i.e. its recovery curve is

```
R(t) = (power law) · (1 + ε·cos(ω·ln t + φ)),    ω = 2π / ln λ,    ε ~ e^{−π²/ln λ}.
```

So the discrete kernel is **not** a ratio you read off a histogram — it is a *log-frequency in
the recovery dynamics* (the "discrete → dynamic" transition). The amplitude law `ε ~ e^{−π²/ln λ}`
is decisive:

| ladder ratio λ | ω = 2π/ln λ | amplitude ~ e^{−π²/ln λ} | detected? |
|---|---|---|---|
| `3/2` (carrier) | 15.50 | 3×10⁻¹¹ | no (invisible) |
| `(3/2)³` | 5.17 | 3×10⁻⁴ | no |
| **`(3/2)⁶` (energy gap)** | **2.58** | **2×10⁻²** | **yes (p≈0.002)** |
| `2⁶` | 1.51 | 9×10⁻² | yes (p≈0.002) |

i.e. only a **coarse** ladder (λ ≳ e²≈7) leaves a detectable ripple; the TFPT **energy gap
`(3/2)⁶≈11.4`** sits right at the ~2% threshold.

### The exact clock is *walled* — the sharper waveform signature (QT.04)

Reading the verification suite's exact discrete→dynamic reconstruction (`v124`/`v126`/`v147`)
sharpens this further. TFPT's recovery is **not** an infinite geometric ladder (which would give
sustained DSI) but the **resummed, walled clock** `rate(n) = −6 ln(1−n/3)` with a **pole at
`n = N_fam = 3`**. So a *single* recovery event is

```
R(t) = w₀ + w₁ e^{−6ln(3/2)·t/τ} + w₂ e^{−6ln3·t/τ}   (two modes + a protected floor, NO 3rd mode)
```

with three sharp, *new*, falsifiable signatures (different from any static ratio):

1. **det-clean bend** — the two decay rates are locked at `rate(2)/rate(1) = ln3/ln(3/2) = 2.7095`
   (exact, no determinant correction, v147), i.e. a **one-parameter** (`τ`) two-exponential, not two
   free rates;
2. **protected floor** `w₀` — recovery saturates at a non-zero "law" level, never returns to zero;
3. **hard wall** — no third decay timescale (`≥3` robust decay modes would be a *tension*).

QT.04 turns the bend into a **matched-filter waveform discriminator**: a kernel recovery is fit by
the fixed-ratio (2.7095) template (free fit recovers 2.71); a non-kernel recovery (e.g. ratio 5) is
rejected. **This is the concrete, more-sensitive data-side probe** — applied to recovery *waveforms*
(FRB post-burst tails, pulsar post-glitch `ν(t)`, GW ringdown residuals), **not** size/energy
histograms (which is why those are null). Sustained log-periodic DSI returns only across a *cascade*
of events (the E8 dimension cascade of scales), never within one walled recovery.

### A different signature class: anyon statistics (QT.05, from v241–v245)

The discrete→dynamic completion (v240–v245) reconstructs the *particle/statistics* layer: the seam
net's superselection sectors are the particle types (v241), spins are the exchange statistics (v242),
and the 2-particle S-matrix is the braiding monodromy (v243). Read as observables, this gives a
signature class **orthogonal** to the recovery dynamics — **discrete statistical phases**:

- **spin (exchange) phase in units of `π/4`** (the spins are 8th roots of unity, `q∈{0,⅛,⅜,½,⅝,⅞}`);
- **braiding (monodromy) phase in units of `π/2`** (`B∈{0,¼,½,¾}`);
- the 16 sectors split into **6 bosons, 2 fermions (`θ=−1`, phase `π`), 8 anyons**, so the *dominant*
  statistical structure is the **m=2 fermion mode** — which **reinterprets the FRB.08 polarisation
  result** ("fundamental m=2, not m=4") as the **predicted** fermion sector rather than a null
  (a *preregistered* m=2 / `π/4`-comb test on new polarisation data is the clean confirmation);
- `c = 8 = g_car + N_fam` falls out of the anyon data (Gauss–Milgram), tying statistics to the
  `(E8)₁` central charge.

Two further **new empirical hooks** from the spectral-action completion (v244/v245), now in the
scorecard: **`sin²θ_W = 3/8` at the spectral scale** (NCG/SU(5) unification `g3=g2=√(5/3)g1`, runs to
~0.231 at `M_Z`) and the carrier `16` = **one anomaly-free SM generation** (`ΣY=ΣY³=0`, one Higgs
doublet). These are genuinely *new, falsifiable* signatures of the completed discrete→dynamic chain —
beyond the recovery kernel.

## Result

QT.01 reproduces the kernel exactly in the entanglement spectrum (a protected DFS mode + the
gap `6 ln(3/2)` and `6 ln 3` as mode surprisals, recovery `I_n=(2/3)^{6n}`). QT.02 exhibits the
dynamical DSI and its `e^{−π²/ln λ}` suppression, validated with a non-geometric control. QT.04
shows the exact clock is **walled** (two modes + floor, bend `2.7095`, no 3rd mode) and builds the
matched-filter waveform discriminator (kernel→2.71, non-kernel→rejected). This is a **structural
confirmation** that the kernel lives in the algebra/dynamics, plus a sharp, honest statement of
where a real signature could still hide — **not** a new empirical result.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .   # numpy/scipy
tfpt-qtest audit       # frozen kernel + DSI ladder ratios (omega, suppression)
tfpt-qtest analyze     # QT.01/02/03 -> results/results.json
# or:  PYTHONPATH=src python -m tfpt_qtest.cli analyze
```

## Layout

```
src/tfpt_qtest/constants.py     # frozen kernel + DSI ladder ratios (mirrors recovery-channel)
src/tfpt_qtest/dsi.py           # discrete-scale-invariance predictor (omega, amplitude law, detector)
src/tfpt_qtest/entanglement.py  # QT.01: Gaussian-state entanglement spectrum = kernel + I_n + protected mode
src/tfpt_qtest/quench.py        # QT.02 recovery-DSI scan + control; QT.03 free-fermion OTOC
src/tfpt_qtest/clock.py         # QT.04 exact walled clock (v124) + matched-filter waveform discriminator
src/tfpt_qtest/mtc.py           # QT.05 carrier anyon MTC (v241/242/243): spin/braid phase quanta, c=8, integrable S
src/tfpt_qtest/cli.py           # `tfpt-qtest audit|analyze`
results/results.json            # committed summary
```

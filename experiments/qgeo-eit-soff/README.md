# QGEO S_off on a REAL measured boundary operator — the EIT analog channel

> **Firewall:** analog / **instrument validation** of the `S_off` observable — **never
> external evidence for TFPT**. `evidence_class = internal_consistency`, same basket as
> `qc-recovery-kernel` / `quantum-testbed`. A μ₄-symmetric tank returning to the
> instrument floor validates the *observable*, not the physics; a failure kills the
> analog *channel*, not the compiler.

The operator form of the QGEO seam premise (`QGEO.SYM.01`, research contracts;
v198/v201/v210) says the boundary energy form Λ_Σ of a μ₄-marked disk is
**block-diagonal in the four μ₄ character classes** `{n ≡ r mod 4}` — no off-character
matrix elements. The simulation side is certified
(`theory-contracts/qgeo_soff_reconstruction.py`: instrument requirement ~10⁻³ relative
spectral precision). **This experiment takes the step onto real hardware:** electrical
impedance tomography (EIT) *measures* the boundary Neumann-to-Dirichlet map of a
2-D body — the laboratory realisation of Λ_Σ.

## Data — KIT4 open 2D EIT archive (real measurements)

Hauptmann, Kolehmainen, Mach, Savolainen, Seppänen, Siltanen, *Open 2D Electrical
Impedance Tomography data archive* (arXiv:1704.01178), data DOI
[10.5281/zenodo.1203914](https://doi.org/10.5281/zenodo.1203914) (CC BY 4.0):
circular saline tank (⌀ 28 cm), **16 equidistant electrodes**, 79 pairwise current
injections × 16 adjacent voltage differences per case, **38 cases** (homogeneous,
plastic/metal inclusions, foam annuli, organic targets). 16 electrodes are ideal here:
the four μ₄ character classes are **exact** subspaces of the electrode Fourier basis and
the μ₄ clock ρ (rotation by π/2) is an exact 4-electrode permutation.

```bash
python scripts/fetch_eit.py     # data_mat_files.zip -> data/mat/*.mat (gitignored, ~24 MB)
python src/tfpt_qgeo_eit/analysis.py   # -> results/results.json
```

## Method (`src/tfpt_qgeo_eit/analysis.py`)

1. electrode potentials from the adjacent-difference data (least squares, zero-mean
   gauge); 2. mean-free electrode **ND matrix** `R` by least squares over all 79
   injections, symmetrised — the **reciprocity error** `‖R−Rᵀ‖/‖R‖` is the measured
   instrument floor (the σ dial of the simulation contract); 3. 16-point Fourier
   transform, `n=0` dropped, then the **harmonic split** of the off-circulant
   (rotation-breaking) weight into the μ₄-**allowed** channel (lag `≡ 0 mod 4`) and the
   **forbidden** channel (`S_off`, the leakage), plus the clock commutator `‖[ρ,R]‖/‖R‖`.

Geometry logic: a rotation-invariant target has *no* off-circulant weight at all; a
generic anisotropic target spreads it ~isotropically over the 15 harmonic lags
(12 forbidden : 3 allowed → forbidden fraction ≈ 0.8); a **μ₄-symmetric target** puts
everything into the allowed channel (forbidden fraction → floor) — that is the
discriminating signature.

## v1.2 — the difference-operator upgrade (frozen 2026-07-06, same day)

The v1 absolute metrics carry an H3 trap: the raw operator is dominated by the symmetric
tank, so `S_off` can look small while the target is barely visible. v1.2 therefore runs
everything on the **difference operator `Δ = R_case − R_hom`** and freezes the acceptance
protocol for the future lab run (full spec: `hypotheses/qgeo_eit_soff_v1.yaml`, v1.2 block):

- **Primary dial = absolute forbidden leakage over the split-half noise floor**
  `leak(m) = √(A_off_m(Δ)/A_off_m(Δ_noise))` — *not* the fraction `f_forbid` alone
  (v1.2 lesson, on record: a dominant rotation-invariant component dilutes the fraction
  while the anisotropic part still leaks). Fractions stay as atlas descriptors.
- **Group fingerprint C2/C4/C8/C16:** the H3 class is `Δ` visible **and** C4 holds
  **and C8 broken** — a centered ring passes C8 too and can never fake a positive;
  a generic target breaks C4 already.
- **Clock recovery:** leakage over all 15 electrode rotations — for H3 the minima must
  sit at k ∈ {4, 8, 12} (the π/2 orbit), read off the operator, not assumed.
- **D4 reflection score** (the `ΘρΘ = ρ⁻¹` face, v196): min over the 16 dihedral axes.
- **NtD/DtN robustness:** all profiles recomputed on the pseudoinverse difference
  (DtN proxy); the commutant transfers exactly in the ideal case (verified 1e-15), so a
  divergence flags pipeline artefacts, never physics. State-level test `ρCρᵀ = C` for
  `C = f(R)` is mathematically equivalent to `[ρ,R] = 0` (verified) — documented, not
  double-counted as a score.
- **Scaling law for the break-ladder:** forbidden energy leakage `∝ δ²` (verified on the
  simulation contract: exponent 1.998).

**v1.2 archive run (37 target cases vs homogeneous reference): 0 C4-positives — exactly
as required for an archive without a μ₄ target.** Geometry-blind classification:
26 generic-anisotropic, 1 rotation-invariant-like (7.1 centered pumpkin), 1
homogeneous-like (1.4 small centered tube), 9 ambiguous (leak 4–6× the split-half floor —
the **between-session systematics floor**, see caveat). Classifier vs documented geometry:
**34/37**; the 3 mismatches are physically real, not pipeline errors — the 6.1 boundary
foam annulus touches the electrodes with visible joints and four clamp pressure points
(photo-verified), i.e. genuinely not rotation-invariant where EIT is most sensitive.
**Floor caveat (drives the H3 protocol):** the split-half floor is injection-noise only;
refill/temperature/contact drift between sessions is not in it — the H3 run must include
repeat homogeneous measurements to calibrate the true reproducibility floor. Blind
protocol (20–40 unlabeled measurements, frozen scores, unblind after lock) and the
9-step symmetry-break ladder are specified in the YAML. Output: `results/results_v12.json`.

## Result (v1 run 2026-07-06, all 38 real cases): ANALOG CHANNEL VALIDATED (H1+H2); H3 preregistered

- **H1 floor (homogeneous tank, case 1.0): PASS.** The measured boundary operator is
  μ₄-block-diagonal at the instrument floor: `S_off = 7.6e-5`, clock commutator
  `1.5e-2`, reciprocity `5.3e-3` — KIT4-class hardware *realises* the σ~10⁻³ precision
  the simulation contract named as the requirement.
- **H2 controls (anisotropy-gated): PASS.** All **28** anisotropic (off-center) targets
  leak with the **generic isotropic signature** (forbidden harmonic fraction 0.87–1.00,
  expectation ~12/15 = 0.8; `S_off` up to 0.019 ≈ 250× floor), and **none fakes a μ₄
  positive**. The 9 centered/annular targets (e.g. 1.4 centered tube, 7.1 centered
  pumpkin ring, 8.x annuli) are rotation-invariant-like and correctly sit near the
  floor — **documented v1.1 refinement** of the too-coarse v1 wording "every inclusion
  must leak" (photo-verified; see the dated addendum in `hypotheses/qgeo_eit_soff_v1.yaml`).
- **H3 μ₄-positive: `data_limited` (preregistered future measurement).** The decisive
  configuration is *not* in the archive: **four identical inclusions at `j·π/2`** (same
  radius and center distance, aligned to electrodes 1/5/9/13) must show *large*
  anisotropy with forbidden fraction **at the floor**, while 1-, 2-, 3- and
  generic-4-inclusion placements leak. Any KIT4-class EIT lab can run it — the exact
  discriminator, floor and expected effect sizes are now calibrated on their own
  published hardware.

**No claim.** A future H3 pass would validate that the μ₄ block-diagonality is
*realisable and measurable* in an analog boundary system (escalate the analog program);
it would say nothing about whether nature's seam does it.

## Layout

```
hypotheses/qgeo_eit_soff_v1.yaml   # preregistered v1 + dated v1.1 addendum (anisotropy gate)
scripts/fetch_eit.py               # Zenodo 1203914 fetch (data gitignored)
src/tfpt_qgeo_eit/analysis.py      # ND reconstruction, harmonic split, S_off, clock commutator
data/mat/, data/photos/            # raw archive (gitignored)
results/results.json               # committed per-case table + verdict
```

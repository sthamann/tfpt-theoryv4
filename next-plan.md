# TFPT — next plan (forward directions after v358 / parameter-free gravity)

**Date:** 2026-06-23 · **Status at start:** v5.3 · `run_all` green · Wolfram 302/302 · AUDIT OK (355 scripts) · Zenodo draft 20808181

> Note: per the workspace rule all repo prose is English (only `next.txt` may be German); this plan is the English companion to the `next.txt` running notes.

## Where we stand
The bridge from the discrete compiler to the **dynamic world** has been instantiated on the gravity side:
`v358` derives the **linearised Einstein equation parameter-free** (`G_ab = c₃⁻¹ T_ab`, `c₃⁻¹ = 8π` fixed) from the
entanglement first law `δS = δ⟨K⟩`, and shows the **thermodynamic** and **geometric** origins of `c₃` coincide via
the atom identity `|μ₄| = |Z₂|·χ(S²) = 4` (so `c₃` is triply over-determined). The matter flux (J3) is assembled
and the entropy density is atom-fixed. **Residual:** the linear→non-linear extension and the one absolute scale
`v_geo`; no free dimensionless parameter remains in the gravity coupling.

The following directions are now **concretely reachable** (each was diffuse before v358). Listed with goal, why it is
reachable now, concrete next steps (modules to build / what to compute), honest difficulty, and the precise open part.

---

## Direction 1 — The full **non-linear** covariant Einstein equation
- **Goal:** extend `v358`'s linearised result to the full covariant `G_ab + Λ g_ab = 8π T_ab` (close the original B6).
- **Why reachable now:** the linearised version is in hand; the standard route (Jacobson 2015 small-ball
  *entanglement equilibrium* beyond first order; Wald entropy / the "all causal diamonds" quantifier) only needs the
  pieces we already have (modular Hamiltonian `v323`, area law `v59`, the atom-fixed coefficient).
- **Concrete steps:**
  1. `v359 GRAV.NONLINEAR.01` — compute the second-order small-ball entropy variation `δ²S|_V` on the
     reconstructible symmetric background (round S² × warped radial × modular time); verify the non-linear curvature
     terms assemble into `G_ab` (not just `R_ab`), with `Λ` appearing from the background-curvature piece.
  2. Verify the "all causal diamonds / all frames" quantifier promotes the (00)-component to the full tensor.
  3. Honest scope: the *equation of state* status (Jacobson) vs a *fundamental* equation is a known interpretive
     fork — type it `[C]`, do not over-claim.
- **Difficulty:** medium-high (a genuine GR computation, but on a fixed symmetric background). **Open part:** the
  background-independent / fully dynamical metric (still needs the continuum realisation).

## Direction 2 — Calculable **GR corrections from the seam gap** (a prediction channel)
- **Goal:** turn the seam transfer gap `(2/3)⁶` / the spectrum `{1,(2/3)⁶,(1/3)⁶}` into **calculable** higher-curvature
  corrections to GR (beyond the known `R²` scalaron), i.e. a falsifiable deviation at the seam scale.
- **Why reachable now:** the entropy density and the modular spectrum are atom-fixed; higher-derivative entropy
  corrections (Wald / the subleading heat-kernel terms) map to higher-curvature couplings whose coefficients are now
  gap-determined, not free.
- **Concrete steps:**
  1. `v360 GRAV.GAPCORR.01` — derive the leading correction coefficient from the subleading transfer eigenvalue
     `(2/3)⁶` (the first-law `δS` beyond the area term); express it in atoms.
  2. Translate to an observable: a correction to the scalaron sector or a seam-scale modification; pre-register a
     kill test (`[X]`) tied to a `freeze_file` row.
- **Difficulty:** medium. **Risk:** must pass the anti-numerology discriminator (a *forced* coefficient, not a fit) —
  decline if the coefficient is not atom-forced.

## Direction 3 — The QG **measure** (C7) as fluctuations around the parameter-free saddle
- **Goal:** complete `G_metric`'s *measure* side (C7), now that the classical saddle (the Einstein equation) is
  parameter-free.
- **Why reachable now:** `v76` already reduced the ambient measure to a finite seam-**boundary** (Calderón) measure;
  with a parameter-free saddle, the path integral is **fluctuations around a fixed classical solution**.
- **Concrete steps:**
  1. `v361 QGAMB.SADDLE.01` — set up the one-loop fluctuation determinant around the `v358` saddle on the seam-boundary
     measure; check the gap (`Δ_eff = 1.648 > 0`) controls convergence.
  2. Tie to the existing OS/clustering machinery (`v240`, `v398`) and the GHP contour (`v334`).
- **Difficulty:** high (constructive-QFT grade). **Open part:** the genuine non-perturbative boundary projective limit.

## Direction 4 — Cosmology: **Λ / S_dS as the equilibrium state**
- **Goal:** derive the cosmological constant `Λ` / de Sitter entropy `S_dS` as the **equilibrium state** of the seam
  thermodynamics (connect to dark energy).
- **Why reachable now:** the de Sitter background is the maximally-symmetric solution of the parameter-free equation;
  `δS = 0` (equilibrium) selects it, and TFPT already has `S_dS = 32π⁴ e^{2α⁻¹}` (`v54`/`v190`) + the Nariai anchor.
- **Concrete steps:**
  1. `v362 COSMO.EQUILIBRIUM.01` — show the dS background is the equilibrium (max-entropy at fixed volume) solution;
     read off `Λ` from the equilibrium condition + the seam vacuum number `δ_Σ` (`v206`).
  2. Cross-check against the existing `Λ ~ e^{−2α⁻¹}` and `H₀` readouts; keep the Hubble-tension honesty.
- **Difficulty:** medium. **Open part:** the absolute normalisation (= `v_geo`, Direction 6).

## Direction 5 — Matter–gravity **backreaction** (J3 explicit → the full Einstein eq with TFPT matter)
- **Goal:** with the matter boost flux J3 now assembled (CHM ball modular Hamiltonian × TFPT's `T_ab`), compute the
  **backreaction** of the SM content on the metric — gravitational read-outs of the carrier.
- **Why reachable now:** `δ⟨K_B⟩ = (8π²R⁴/15) δ⟨T₀₀⟩` is explicit; the SM stress tensor is the carrier's.
- **Concrete steps:**
  1. `v363 GRAV.BACKREACT.01` — feed the carrier stress tensor into the J3 flux; check the sourced linearised metric;
     look for any *forced* gravitational read-out of SM quantum numbers.
- **Difficulty:** medium. **Risk:** anti-numerology discipline on any "read-out".

## Direction 6 — The absolute scale **v_geo** (the single remaining dimensionful input)
- **Goal:** the one acknowledged unit. Either (a) derive the Planck-area / entropy unit from the seam, or (b) prove it
  is irreducibly the one unit (sharpen the No-Unit theorem `v153`).
- **Why reachable now:** after v358 it is provably the **only** dimensionful input in the gravity coupling — isolated.
- **Concrete steps:**
  1. `v364 VGEO.SHARPEN.01` — restate `v_geo` as the single Planck-area unit tying `1/G`, `U_point`, `m/μ`; test any
     Sakharov-style induced-scale relation; honest `[O]` if it stays primitive.
- **Difficulty:** conceptual (likely stays the one unit). **Value:** clarity — the last dimensionful anchor named.

## Direction 7 (complementary, matter side) — close the **(E8)₁ in-class** continuum realisation
- **Goal:** the matter-side bridge residual: prove the seam collar is in MMST's free-lattice-fermion class so the
  scaling limit IS `(E8)₁` (the SEAM.EQUIV.01 residual).
- **Why now:** the gravity side is done; this is the symmetric remaining half (matter side).
- **Concrete steps:** verify MMST's hypotheses for the explicit collar (`v336` + the wavelet/Koo-Saleur structure);
  `v365 SEAM.MMST.INCLASS.01`.
- **Difficulty:** high (functional analysis). **Open part:** the genuine scaling-limit theorem.

---

## Recommended order (highest value / most tractable first)
1. **Direction 1** (non-linear Einstein) — directly extends v358, closes B6 conceptually.
2. **Direction 4** (Λ as equilibrium) — high-impact (dark energy), medium difficulty, builds on existing dS readouts.
3. **Direction 2** (gap corrections) — the only *new falsifiable prediction* channel; do it with the strict discriminator.
4. **Direction 5** (backreaction) — explicit, uses J3.
5. **Direction 6** (v_geo) — cheap clarity.
6. **Direction 3 / 7** (QG measure / MMST in-class) — the two hard functional-analysis residuals; long-horizon.

## Discipline reminders (do not relax)
- Every new `vN` follows the full workflow: derive from `{c₃, g_car}`, `check()/summary()`, register in `run_all.py`
  + `script_registry.csv`, cite `\veri{}` in the affected paper **body**, mirror exact results in Wolfram, add a
  changelog entry, run `bash build.sh release` → `AUDIT OK`, refresh manifests.
- **Anti-numerology:** any new coefficient must be a *forced* identity (the v354/v355 discriminator), never a fit.
- **Honest scope:** mark `[E]/[C]/[O]` precisely; never promote a `[C]` bridge to `[E]`.

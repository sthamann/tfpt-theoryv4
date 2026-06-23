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

## Direction 2 — GR corrections from the seam gap — DONE (`v360`): the disciplined result is a DECLINE
- **RESULT (`v360 GRAV.GAPCORR.01`):** run with the strict discriminator, the answer is **no new near-term forced
  prediction**. The leading higher-curvature term IS the **R² scalaron** (`M_scal²/M̄² = c₃⁷`), which is the
  next-order term of the same entanglement-equilibrium route (Wald first law → f(R)=R+R²) and is **already** a live
  CMB-S4 kill test (`n_s = 1−2/N★`, `r = 12/N★²`). A *distinct* gap-induced curvature² term sits at the seam/Planck
  scale (`Δ = 6 ln(3/2)` is dimensionless → scale `ξ·v_geo`), and a new dimensionless coefficient there is **not
  atom-forced** (scalaron exponent 7=g+N−1  vs gap exponent 6=2N_fam; `c₃⁷` vs `(2/3)⁶` unrelated) → declined per
  v354/v355.
- **Takeaway:** the calculable GR deviation already exists (the scalaron); Direction 2 added no new dial — exactly the
  anti-numerology outcome. Closed.

## Direction 3 — The QG **measure** (C7) as fluctuations around the parameter-free saddle — DONE (`v365`): ADVANCED, not closed
- **RESULT (`v365 QGAMB.SADDLE.01`):** with the parameter-free saddle (`v358`/`v359`) the QG **measure**
  (gate C7/`QG.AMB.01`) organises as a **one-loop Gaussian fluctuation determinant** that is now *well-posed and
  convergent*:
  - **[E]** the fluctuation inverse-propagator **stiffness is fixed** `1/c₃ = 8π` (no free dial) — before `v358`
    this expansion wasn't even dimensionlessly well-posed (the Newton coupling was a dial);
  - **[E]** the fluctuation operator is **gapped** `M ≥ Δ_eff = 6 ln(3/2) − 31/(4π²) ≈ 1.648 > 0` (`v76`/`v337`)
    ⇒ mode-by-mode convergence; finite model log-det `Tr' log M = 6 ln(9/2)` on the OS spectrum;
  - **[C]** the wrong-sign conformal mode converges on the **GHP contour** `∫e^{−|c|φ²} = √(2π/3)` + IDG (`v334`);
  - **[E]** the **admissible projective limit exists** (tightness `χ = 729/665`, `v330`), with **0** new
    dimensionless dials (`v364`).
- **[O] Open part:** the genuine **non-perturbative** projective limit (G6 on the *ambient* sector). One-loop
  control around a fixed saddle **reduces** C7 to the non-perturbative limit; it does not close it.
- **Takeaway:** C7 is sharpened from "diffuse full QG" to "a one-loop-controlled Gaussian fluctuation problem
  around a parameter-free saddle." Cited in `tfpt_research_contracts`; Python-only.

## Direction 4 — Cosmology: Λ **consistency** (the VALUE is already done from α — DEMOTED)
- **CORRECTION:** Λ's value is **not open**. TFPT already derives it from α (`v60`):
  `ρ_Λ/M̄_Pl⁴ = (3/4π²)·e^{−2α⁻¹}`, and the famous "123 orders" = `2α⁻¹/ln10` (= 119.03, the EM fixed point) +
  `log₁₀(256π⁴/3)` (= 3.92, the seam-defect prefactor). So "derive Λ" is redundant — the original Direction 4 goal
  was an over-claim.
- **Reduced goal:** the only genuinely new item is a **consistency check** — that the Λ appearing as the
  background-curvature constant in the Direction-1 non-linear equation equals the already-derived `ρ_Λ`, i.e. the two
  gravity routes (the α-readout `v60` and the equilibrium/field-equation) agree. A confirmation, not a new derivation.
- **Difficulty:** low — fold into Direction 1 (one extra `check()`), do not spend a standalone effort on it.
- **Priority:** demoted (Λ is essentially done; this is housekeeping).

## Direction 5 — Matter–gravity backreaction — DONE (`v361`): finite & forced, no new dial
- **RESULT (`v361 GRAV.BACKREACT.01`):** two genuine forced facts + an honest decline.
  - **[E]** the carrier's gravitational anomaly is **forced**: `c_- = 16/2 = 8 = g_car + N_fam` (chiral central
    charge of the 16-Majorana content).
  - **[E]** the backreaction is **finite** → **Λ from α**: the matter vacuum energy through `G_ab = c₃⁻¹ T_ab` is
    gap-suppressed (Decoupling Thm v337) to `ρ_Λ = (3/4π²)e^{−2α⁻¹}` (v60), the 123 orders = 119.03 + 3.92 — **not**
    the `M_Pl⁴` catastrophe. The loop (v359 equation + v60 Λ + carrier vacuum) **closes**.
  - **[O]** decline: no new atom-forced read-out of individual SM quantum numbers (the backreaction is GR-with-the-SM;
    the forced pieces `c_-=8`, `Λ` are already established).
- **Takeaway:** the backreaction is finite and consistent (closes the CC-backreaction loop), but adds no new dial.
  Closed.

## Direction 6 — The absolute scale v_geo — DONE (`v364`): the single dimensionful input; 0 dials + 1 unit + π
- **RESULT (`v364 VGEO.SHARPEN.01`):** the No-Unit Theorem (`v153`) already made `v_geo` a forced metrology
  primitive; the **sharpening** after the parameter-free gravity (v358/v359/v361) is that the **gravity sector adds no
  new scale either** — `1/c₃ = 8π` and the `Λ` prefactor `(8π)²·48c₃⁴ = 3/(4π²)` are dimensionless, so `1/G ~ v_geo²`
  and `Λ ~ (dimensionless)·v_geo⁴` reduce to `v_geo` × atoms.
- **Final tally:** every dimensionful quantity = (dimensionless ratio) × (power of `v_geo`); TFPT's free content is
  `{v_geo, π}` with **ZERO dimensionless dials** — a ~26 → 1 reduction vs the SM. `v_geo` is irreducibly primitive
  (the one unit, not a gap); `1/G` is UV-sensitive (Sakharov, v68).
- **Takeaway:** the last dimensionful anchor is named and shown to be the **only** one. Closed.

## Direction 7 (complementary, matter side) — the **(E8)₁ in-class** continuum realisation — DONE (`v366`): ADVANCED, not closed
- **RESULT (`v366 SEAM.MMST.INCLASS.01`):** the seam collar is verified **IN MMST's free-lattice-fermion
  scaling-limit class**, hypothesis-by-hypothesis, so the chiral scaling limit is a chiral CFT pinned to `(E8)₁`:
  - **[E]** class arithmetic: `D = dim S⁺ = 2^(g_car−1) = 16` Majoranas, `c = g_car + N_fam = 8`, `rank E8 = 8`
    ⇒ MMST's range `rank ≤ c ≤ D` reads `8 ≤ 8 ≤ 16` (**in** range, saturating `rank = c = 8`);
  - **[E]** gapped (`Δ = 6 ln(3/2) > 0`, **derived** `v302`); **[E]** chiral (`c₋ = D/2 = 8 ≠ 0`);
  - **[C]** quasi-free CAR class (`v155`/`v160`) ⇒ the **MMST scaling-limit theorem applies** (`v336`);
  - **[E]** the target is pinned to `(E8)₁` (`det K = 1` vs `SO(16)` `det K = 4`) by the order-4 `μ₄` clock (`v351`).
- **[O] Open part:** the single **S3** input — the abstract collar realised as a genuine **lattice** chiral
  free-fermion invertible phase (the one-sidedness / "Flat-Away", `v297`/`v356`) = the seam one-sidedness that
  *defines* `c₃`. Given S3, MMST applies as a cited theorem.
- **Takeaway:** the continuum side of `SEAM.EQUIV.01` is reduced to **one named, theorem-bounded input** (S3).
  Verifies MMST in-class; **advances**, does not close. Cited in `tfpt_research_contracts`; Python-only.

---

## Recommended order (highest value / most tractable first)
1. ✅ **Direction 1** (non-linear Einstein) — DONE (`v359`): full covariant `G_ab + Λ g_ab = (1/c₃) T_ab`,
   both coefficients parameter-free; B6 closed at the local level. (Direction-4 Λ consistency folded in.)
2. ✅ **Direction 2** (gap corrections) — DONE (`v360`): disciplined DECLINE — the calculable GR deviation is the
   R² scalaron (already falsifiable); no new atom-forced coefficient.
3. ✅ **Direction 5** (backreaction) — DONE (`v361`): finite & forced (c_-=8 + Λ from α), no new dial.
4. ✅ **Direction 6** (v_geo) — DONE (`v364`): the single dimensionful input; 0 dials + 1 unit + π.
5. ✅ **Direction 3** (QG measure) — DONE (`v365`): C7 reduced to a one-loop-controlled Gaussian fluctuation
   problem around the parameter-free saddle (fixed stiffness `1/c₃=8π`, gap-controlled convergence, tight
   admissible projective limit, 0 dials); residual = the non-perturbative projective limit only.
6. ✅ **Direction 7** (MMST in-class) — DONE (`v366`): the seam collar verified in MMST's free-fermion class
   (`8 ≤ 8 ≤ 16`, gapped, chiral) ⇒ scaling limit pinned to `(E8)₁`; `SEAM.EQUIV.01` reduced to the single S3
   lattice-realisation input.
- (Direction 4 was folded into Direction 1: Λ's value is already done from α.)

### What now genuinely remains (both are single, named, *external/foundational* residuals)
- **C7 non-perturbative projective limit** (the constructive-QFT ambient measure; gap-decoupled, blocks no test).
- **SEAM.EQUIV.01 S3** (the lattice chiral free-fermion invertible realisation of the collar = the seam
  one-sidedness that *defines* `c₃`).
Both are now theorem-bounded reductions, not diffuse "full QG / continuum" gaps — every TFPT-internal lever has
been pulled; what is left is genuinely hard mathematics (constructive QFT / scaling-limit existence), not a free
dial or a missing TFPT mechanism.

---

## Forward plan v2 (2026-06-23) — Tracks toward QFT / Gravity / TOE completion

The Directions 1–7 above closed/sharpened the *internal* gravity and reduction work. What remains is organised as
**four tracks** with the precise completion target each unlocks. Definitions (the operational completion grammar,
consistent with `tfpt_research_contracts` and the No-Unit theorem `v153`/`v364`):

- **QFT-complete** = Modular Spectral Closure (`v261`) **+** `SEAM.EQUIV.01` discharged (the boundary relative
  object is one mathematical object, no residual premise).
- **Gravity-complete** = QFT-complete **+** *either* the ambient measure is built (C7) *or* the ambient sector is
  proved physically redundant (the holographic route).
- **TOE-complete (operational)** = Gravity-complete **+** `F_transfer` is a closed, dial-free solver suite **+**
  the frozen kill tests survive. (`v_geo` stays the one metrology unit — by theorem, not a gap.)

### Track 1 — close `SEAM.EQUIV.01` by attacking the single S3 input (highest leverage → QFT-complete)
- **Goal:** discharge S3 (`v356`/`v366`): the abstract 16-Majorana collar realised as a genuine **lattice chiral
  free-fermion invertible phase** (`c_- = 8`, gap `6 ln(3/2)`, `det K = 1`) — the seam one-sidedness that *defines*
  `c₃`. Given S3, MMST applies as a cited theorem and the scaling limit is `(E8)₁`.
- **Why reachable now:** the continuum chain S1→S6 is theorem-bounded except S3 (`v366`); the gap is *derived*
  (`v302`), the target *pinned* (`v351`), invertibility follows from gapped free fermions (`v301`).
- **Concrete steps:**
  1. `v367 SEAM.S3.LATTICE.01` — build the explicit Koo–Saleur lattice fermion model of the collar; verify on the
     lattice (numerically + class arithmetic) `c_- = 8`, transfer gap `= 6 ln(3/2)`, `det K = 1` vs `SO(16)` `= 4`.
  2. `v368 SEAM.S3.INFLOW.01` — harden the anomaly-inflow leg (S4): the chiral edge of the invertible bulk is
     non-gappable (`c_- ≠ 0` by bulk–edge), so edge existence follows from S2+S3, not a separate assumption.
- **Difficulty:** high (constructive lattice→continuum existence). **Open part:** the from-scratch lattice
  realisation; stays `[O]`/`[C]` (cited MMST), but reduces "continuum gap" to one lattice existence statement.

### Track 2 — `Gravity-complete` without building the ambient swamp (the holographic route)
- **Goal:** prove the **ambient redundancy** statement instead of constructing the general Euclidean QG measure —
  the strategically strongest move, since it sidesteps the conformal-factor swamp (`v332`/`v334`).
- **Why reachable now:** `(E8)₁` holomorphy gives `DHR((E8)₁) = Vec` (no anyons / superselection), `det K = 1`
  (no torus GSD), the Petz recovery rate `(2/3)⁶` (`v221`), and the gap-decoupling margin `Δ_eff ≈ 1.648 > 0`
  (`v76`/`v337`) are all in hand — the ingredients of a boundary-reconstruction theorem.
- **Concrete steps:**
  1. ✅ `v369 QGAMB.REDUNDANCY.01` — **DONE (this change):** assemble the ambient-redundancy statement
     `O_phys^bulk/Diff ≅ A_Σ^{μ4}` from the established `[E]` discriminators (`det K = 1` ⇒ `DHR = Vec`; no torus
     GSD; finite Petz recovery `(2/3)⁶`; gap margin `1.648 > 0`) + modular (Bisognano–Wichmann) covariance; so
     QG.AMB.01 is a non-fundamental **certification** object, not missing dynamics. `[C]` (conditional on
     `SEAM.EQUIV.01` + BW intrinsicality); residual `[O]` = those two premises. Python-only.
  2. `v370 KMS.HESSIAN.ENTIRE.01` — the perturbative companion (`list.txt` "Paper C"): evaluate the **untruncated**
     KMS spectral-action Hessian `Tr e^{−D²/Λ²}` as a *form factor* (not to `a₄`); target the spin-2 sector
     `Π₂(p) ∝ 1/(p² e^{p²/M²})` (entire, zero-free) ⇒ the Stelle ghost is a truncation artefact. `[C]` →
     perturbative graviton unitarity; mirror the exact pieces in Wolfram.
- **Difficulty:** `v369` low-medium (synthesis of established facts, like `v335`/`v365`); `v370` medium (a real
  heat-kernel form-factor computation). **Open part:** `v369` stays `[C]` on `SEAM.EQUIV.01`; `v370` is perturbative
  only (does not replace the non-perturbative measure).

### Track 3 — `TOE-complete (operational)`: `F_transfer` as a dial-free solver suite
- **Goal:** turn the frontier transfer interfaces into runnable, typed solvers — `F_transfer = F_pole ⊕ F_Boltzmann
  ⊕ F_relic ⊕ F_QCD` — so every "near-miss" either becomes algorithmically reproducible or dies honestly.
- **Why reachable now:** `v326` already assembles the suite as one harness; `v339` maps each external input
  precisely; the compiler fixes the source (CKM point, Koide `Q=2/3`), the solver does the QCD/thermal dirt.
- **Concrete steps:** `v371 F.POLE` (Koide source→pole via RG+QED dressing), `v372 F.BOLTZMANN` (`η_B` washout),
  `v373 F.RELIC` (finite-T axion relic), `v374 F.QCD` (`m_p/m_e` via carrier-`b₃` running). Each: compiler input +
  external standard physics → typed `[C]` output, **no free dial**. Feeds the freeze registry (rare kaons, `ε_K`,
  PMNS package, reheating map).
- **Difficulty:** medium (engineering + cited external physics). **Open part:** these stay `[C]` transfer bridges,
  never promoted to compiler powers (the firewall in `tfpt_4_frontier`).

### Track 4 — "and possibly more": the observatory stack (prediction machine, not a PDF)
- **Goal:** operationalise the compiler as a prediction machine: a machine-readable prediction registry (extend
  `freeze_file.csv`), a horizon-signature lab (`β_BH(r)` achromatic `1/r²`, echo templates, `(2/3)^{6n}` recovery —
  as a *search* tool, not a claim machine), and a status-typed CI for every observable.
- **Difficulty:** low-medium (tooling). **Open part:** none physical — this is infrastructure that makes the closed
  pieces usable and the open pieces honestly fenced.

### Recommended order (v2) — ALL DONE (2026-06-23)
1. ✅ `v369` (ambient redundancy) — done: the holographic route, QG.AMB.01 reframed as a certification object.
2. ✅ Track 1 (`v367`/`v368`, S3) — done: an explicit gapped p+ip lattice model (numerical Chern `|C|=1`, `c_-=8`,
   `det K` 4→1) + the anomaly-inflow edge existence on a strip; S3 reduced to a runnable lattice model.
3. ✅ Track 2 `v370` (spin-2 unitarity) — done: the Barnes–Rivers spin decomposition; the Stelle ghost is a spin-2
   state cured by the entire KMS form factor (`v304`), the spin-0 mode by the GHP contour (`v334`) ⇒ perturbative
   graviton unitarity sector-by-sector `[C]`.
4. ✅ Track 3 (`v371`–`v374`, `F_transfer`) — done: the four transfers promoted from contracts to typed runnable
   solvers with kill tests (Koide QED-excluded negative; `η_B` BDP ODE factor-1.1 near-hit; axion spine branch lands
   on `Ω_DM`; `m_p/m_e` band contains 1836.15).
5. ✅ Track 4 `v375` (observatory) — done: a status-typed CI over `freeze_file.csv` (falsifiability complete + the
   live JUNO/NuFIT/ACT/BK18 scorecard, `θ13` flagged at 2.0σ).

**Plus** the `list.txt` credibility/hygiene pass (claim-drift softened, `ε = c3 + 36 c3⁴` explicit, θ12
prediction-of-record vs diagnostics, JUNO first-data + ACT DR6 + CODATA caveats, "Complete solutions" → "Closure
status", null-model bound typed). What remains are only the two genuinely-hard external residuals: the **C7
non-perturbative projective limit** and **SEAM.EQUIV.01 S3** (now a single lattice-existence statement).

### Honest limits (hold even at full closure)
No absolute GeV from pure numbers (`v_geo` is metrology, `v153`/`v364`); QCD/nuclei/chemistry stay solver physics;
no antigravity/warp (gravity only via `T_ab`); experiments (JUNO, CMB-S4, EDM, …) remain the judges.

## Discipline reminders (do not relax)
- Every new `vN` follows the full workflow: derive from `{c₃, g_car}`, `check()/summary()`, register in `run_all.py`
  + `script_registry.csv`, cite `\veri{}` in the affected paper **body**, mirror exact results in Wolfram, add a
  changelog entry, run `bash build.sh release` → `AUDIT OK`, refresh manifests.
- **Anti-numerology:** any new coefficient must be a *forced* identity (the v354/v355 discriminator), never a fit.
- **Honest scope:** mark `[E]/[C]/[O]` precisely; never promote a `[C]` bridge to `[E]`.

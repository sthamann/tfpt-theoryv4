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

## Discipline reminders (do not relax)
- Every new `vN` follows the full workflow: derive from `{c₃, g_car}`, `check()/summary()`, register in `run_all.py`
  + `script_registry.csv`, cite `\veri{}` in the affected paper **body**, mirror exact results in Wolfram, add a
  changelog entry, run `bash build.sh release` → `AUDIT OK`, refresh manifests.
- **Anti-numerology:** any new coefficient must be a *forced* identity (the v354/v355 discriminator), never a fit.
- **Honest scope:** mark `[E]/[C]/[O]` precisely; never promote a `[C]` bridge to `[E]`.

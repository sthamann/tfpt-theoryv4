# What is genuinely open

> The honest frontier. If you want to *close* one of these, see the "Try to break TFPT" section
> of the [README](../README.md#try-to-break-tfpt) and open a claim challenge.

**Current status (v5.4).** The discrete/algebraic compiler is closed (`[E]`). The honest residual
is **three named interface problems** — not a diffuse list:

| Interface | Question | Status |
|---|---|---|
| `v_geo` | the one metrology unit (`=1/√G = m/μ`); No-Unit Thm: no compiler scale | primitive `[O]` |
| `G_net` | `SEAM.EQUIV.01`: the raw seam *is* the holomorphic `(E8)₁` net | `[C]` — closed modulo a cited theorem |
| `F_transfer` | one functor, four typed interfaces (Koide, `η_B`, axion, `m_p/m_e`) | `[C]` |

The remaining distance is therefore not a list but **one metrology unit** (`v_geo`, the No-Unit
Theorem, `v153`/`v364`) plus the **typed `F_transfer` interfaces** (Koide, `η_B`, axion, `m_p/m_e`
— deliberately `[C]`, never compiler outputs), above the **cited-theorem ceiling** on the seam
(`SEAM.EQUIV.01` closed modulo MMST + OS reconstruction, Lean `FORM.SEAM.MMST.01`) and with
**`QG.AMB.01` a `[C]` redundancy** (`v369`). The central theorem reads as a clean simple-current
extension, `(D₅)₁⊗(A₃)₁ ⋊ ⟨(1,1)⟩ ≅ (E₈)₁` (index 4, c = 8, μ = 1 ⇒ holomorphic ⇒ E₈, `v154`).

---

## Deep dive — parameter-free gravity, the all-orders perturbative leg, and `SEAM.EQUIV.01`

**Gravity is parameter-free.** The classical metric-sector field equation is no longer only an `R+R²`
readout. The entanglement first law `δS = δ⟨K⟩` (Jacobson; Faulkner et al.), run with TFPT's atoms,
gives the **full covariant** Einstein equation `G_ab + Λ g_ab = c₃⁻¹ T_ab` with **both** coefficients
fixed — `c₃⁻¹ = 8π` (no free dimensionless Newton dial; the thermodynamic origin `2π/η` *coincides*
with the geometric one `|Z₂|·2π·χ` via `|μ₄| = |Z₂|·χ(S²) = 4`, so `c₃` is triply over-determined —
anchor, geometry, thermodynamics, `v358`/`v359`) and `Λ` from `α` (`ρ_Λ = (3/4π²)e^{−2α⁻¹}`, `v60`);
the Einstein tensor (not Ricci) is forced by Lovelock, so matter conservation is an output (`v359`).
The residual here is only the equation-of-state interpretive fork and the one unit `v_geo`. An
**external candidate** for the missing action level — Bianconi's entropic action, *Gravity from
entropy*, PRD 111, 066001 (2025) — is quantified in `v473`: her free constant is pinned exactly
(`β′_B = c₃/6 = 1/(48π)`), her emergent `Λ` reproduces the `v60` branch with the exact target
`Tr Q² = 32c₃⁴`, and the `R²` sector misses the TFPT Starobinsky coefficient by exactly `3(8π)⁹ ≈ 10¹³`
(pre-registered kill test) — nothing closes, the typing stays `[O]`. The operator level is executed in
`v474`: the D₅ Clifford/spinor structure exhibited on the carrier Fock space `Λ•ℂ⁵` (ten exact gammas,
the 45-dim `so(10)` preserving the 16-dim even subspace), the Hodge fold identified as the `5 → 5̄`
conjugation (her `1+5+10` becomes the GUT `16 = 1+5̄+10`), and the `Q`-target decided — integer supports
exactly `{|ℤ₂|, rank E₈, 2^g_car}` with minimal uniform `q = c₃²`; the naive pair-block (`10`) reading is
killed. The `R²` kill test itself is executed in `v475`: with exact tensorial factors (vacuum action
`3βR + (17/24)β²R²` on the maximally symmetric background) the raw entropic scalaron comes out
**trans-Planckian** (`m² = 4608π²/17 M̄²`, ≈ 51.7 M̄), so the light-trace-mode reading is dead and
KMS-spectral renormalisation is the only surviving `R²` route; the Lorentzian-positivity caveat now has
an explicit timelike witness (`1 − αv² ≤ 0`). The compression conjecture (AP2) is made well-posed in
`v476`: the literal operator-side reading is ill-posed on a pure bulk, the state-side reading (build
`Δ_Σ` from the compressed relative metric) is forced, and the mismatch between the readings is exactly
second order in the cross-cut correlations and gap-suppressed — AP2 itself stays `[O]`. The surviving
`R²` route is typed as ONE moment condition in `v477`: the entropic action is the flat scale-integral of
relative heat-kernel actions, and demanding `m² = c₃⁷M̄²` forces exactly `μ₂/μ₁² = (72/17)(8π)⁹` — with
the closure identity `(4608π²/17)/((72/17)(8π)⁹) = c₃⁷` holding identically, the 13 orders are a
scale-measure datum which TFPT's own KMS moment (`v36` `f₀`) fixes correctly; zero new dials,
consistency not derivation `[C]`. First steps on the two remaining legs are in `v478`: the compressed
critical state's modular data flows to the CHM/Bisognano–Wichmann geometric form (`c_est → 1` at 2×10⁻⁴,
CHM parabola, even bands exactly zero) — meeting TFPT's Einstein-derivation input (`v323`/`v358`) — and
the measure condition reduces to one exact KMS time `t₀ = ln(72/17) + 9ln(8π) = 30.461` (the `h(E₈) = 30`
near-miss explicitly declined); both legs stay `[O]`. The global measure (`QG.AMB.01`) is now a
**`[C]` redundancy** (`v369`): a certification object rather than missing dynamics, conditional on
`SEAM.EQUIV.01` and Bisognano–Wichmann.

**The perturbative 4D leg closes to all orders.** The matter+gauge `S_pert` is a typed
Epstein–Glaser/BRST contract (`v381`, `QFT4D.EG.ALLORDER.01`): dimension-4 power-counting ⇒ a finite
counterterm space, BRST nilpotency `s²=0` for the carrier `su(3)×su(2)`, and the seam gap ⇒ the
adiabatic limit, with all-order `T_n` existence and the Slavnov–Taylor identity imported (the
`R²/Weyl²` Stelle ghost is fenced out as the resummed entire form factor, `v304`/`v370`/`v380`). The
EM-Ward functional origin — *why exactly that* `F_U(1)` — is named as the tracked target
`ALPHA.QUILLEN.EXACT.01` (`v382`), a face of `SEAM.EQUIV.01`; the `α⁻¹` value itself stays `[E]`. Four
honest steps narrow that target without closing it: a solvable 4D model reaches the `a₄` heat-kernel
order (`v433`); the matter factor `b₁` is the `U(1)_Y` `a₄` coefficient via the `β = a₄` theorem,
collapsing the three residuals to one `[C]` (the seam `F`-normalisation) + one `[O]` (`v434`); and a
`π`-power test isolates the cubic `α³` as the *unique* metric-independent (`π⁰`) topological rung, whose
coefficient is a conditional integer Chern–Simons level (`v435`). A fifth step (`v470`) upgrades both
leftovers: the `α³` level **equals the computed bulk Chern invariant** `|C| = 1` of the same p+ip collar
that realises S3, and the seam `F`-normalisation is retyped as the **affine embedding index**
`k_Y = tr(Y²)/tr(T3²) = 5/3` (Ginsparg 1987; `(3/5)·(41/6) = 41/10 = b₁` exactly). A sixth step (`v472`)
exhibits the bridge lemma at the finite level. What stays `[O]` is the **continuum** ζ-det identification
on the abstract seam (= the `SEAM.EQUIV.01` face), so `ALPHA.QUILLEN.EXACT.01` stays `[O]`.

**One principle behind "parameter-free", and the shape of what's left.** A bird's-eye synthesis
shows every TFPT sector is the *same* object — a gapped operator with a unique attractor (the physics)
and a spectral gap (the reason there is no free dial); so "parameter-freeness is a theorem" is **one**
spectral-gap statement, theory-wide, not a list of coincidences (`v383`). The residual matrix is now
**certification, not construction** (`v384`): every open item is an external math proof, theorem-forbidden
(the unit), or external physics — **zero** open internal mechanisms.

**`SEAM.EQUIV.01` is closed modulo a cited theorem.** The explicit lattice model (`v367`/`v368`) and
the S3 closure stack pin the target at every computable level — central charge `c=8` (`v376`), the
`(E8)₁` character with 248 currents and one primary (`v377`), genus-one torus GSD = 1 (`v378`) and
reflection positivity (`v379`) — and it is Lean-formalised as `FORM.SEAM.MMST.01`: the collar's MMST
hypotheses are kernel-proved, the MMST scaling-limit and Adamo–Moriwaki–Tanimoto OS-reconstruction
theorems enter as named cited axioms, and the `#print axioms` check is clean. The *only* residual that
stays `[O]` is the abstract continuum existence of the scaling limit (exactly those two cited published
theorems, `v336`). The post-F **G-block** narrows that residual on six more fronts (`v454`–`v464`,
`v469`), re-founding the `128`-spinor extension on 1995–2001 peer-reviewed subfactor theory (the
Longo–Rehren locality integer `h_s = 16/16 = 1 ∈ ℤ`) and reducing the realisation axiom to invariants
(R1′: quasi-free `[C]` + gap `[E]` + class D + `c₋ = 8` `[E]`, computed FHS `|C| = 1`, `ν = 16`, the
Kitaev 16-fold-way class whose edge *is* the bosonic `(E8)₁` state). Across the whole G-block the
residual is now *entirely certification* — a named, hypothesis-audited package of published theorems with
no open internal mechanism — yet `SEAM.EQUIV.01` stays `[O]` because it still rests on cited
continuum-existence theorems we do not re-prove. `QGEO.SYM.01` is its **corollary** (`v335`, Lean
`FORM.QGEO.BW.01`). `QG.AMB.01` is gap-decoupled from the general Euclidean-QG conformal-factor problem
(margin `Δ_eff ≈ 1.648 > 0`, `v76`/`v330`).

---

## Historical reduction (how we got here)

<details>
<summary><b>The full reduction chain and the forward plan</b></summary>

- **One condition, not many** (`v234`/`v235`): the whole *structural* residual — the metric inclusion
  `G_net`, the carrier `P2` and red-team Target A — is a single condition, *"the seam carries no
  nontrivial abelian sector"*, with three provably-equivalent faces that all force `E8`: holomorphy
  (`μ`-index 1), a homology-sphere seam link (`Γ` perfect `⟺ 2I`, `v232`), and exactly one 1-dim irrep
  (`v219`) — all equal `#(mark-1) = |H₁| = 1`, true only for `E8`. In abelian Chern–Simons language it is
  the single integer step `holomorphic ⟺ det K = 1`; the extension tower `D₅⊕A₃ (16) → D₈ (4) → E₈ (1)`
  is anyon condensation, i.e. the Kitaev `E8` quantum-Hall state.
- **Gravity is parameter-free** (`v358`/`v359`): the entanglement first law gives the **full covariant**
  Einstein equation `G_ab + Λ g_ab = c₃⁻¹ T_ab` with **both** coefficients fixed, and the **thermodynamic**
  origin of `c₃` **coincides** with the **geometric** one via `|μ₄| = |Z₂|·χ(S²) = 4`. So `c₃` is
  **triply over-determined** (anchor, geometry, thermodynamics). The only residual is the equation-of-state
  interpretive fork and the one unit `v_geo`.
- **The central theorem**: `1/(8π)` from the seam-determinant replica — structure closed, the
  Fursaev–Solodukhin factor machine-derived (`v90`), the mechanism exhibited at the gapped-model level
  (`v150`), the Calderón transfer answered (`v151`), the `q(A₃)` normalisation identified as the one
  dimensionful anchor in disguise (`v152`), and the whole chain exercised numerically on the discretized
  collar with the seam's own kernel and real replica sheets (`v471`).
- **Ambient QG measure** (`QG.AMB.01` / `G_metric`) — reframed as a **`[C]` redundancy** (`v369`).
- **Absolute amplitude normalisation** (`U_point`) — an anchor; the quark *ratios* are closed.
- **Frontier interfaces** (`m_p/m_e`, `η_B`, Koide, axion relic) — deliberately typed as interfaces,
  never quoted as compiler outputs.

**Forward plan v2 (2026-06-23) — all five tracks done.** Track 1 (`v367`/`v368` + S3 stack `v376`–`v379`):
an explicit gapped p+ip lattice model (numerical Chern `|C|=1`, `c_-=8`) pins the `(E8)₁` target at every
computable level; only the cited MMST continuum scaling limit stays external. Track 2 (`v369`): the ambient
QG measure is reframed as a **holographic redundancy**. Track 3 (`v371`–`v374`): the four `F_transfer`
interfaces promoted to typed runnable solvers. Track 4 (`v375`): a status-typed CI over the frozen
prediction registry with a live JUNO/NuFIT/ACT/BK18 scorecard. Plus `v380`: the KMS Entire Hessian — the
Stelle ghost is exactly a finite Seeley–DeWitt truncation.

A development timeline of all 472 modules is in [`introduction.tex`](../introduction.tex) (and on the
website verification page).

</details>

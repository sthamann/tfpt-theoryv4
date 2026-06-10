# TFPT computational verification suite

Every load-bearing numerical / arithmetic claim marked **[I]** (exact identity),
**[L]** (Lie/lattice theorem) or **[N]** (numerical fixed point) in the six TFPT
documents is re-derived here from the two axioms alone:

* **P1** — the boundary seam constant `c3 = 1/(8*pi)`
* **P2** — the five-slot carrier `g_car = 5`

Everything else (E8, the SM packet, `alpha^-1`, the flavor matrix, the cascade,
gravity/cosmology, horizon readouts) is produced as a consequence and checked
against the value quoted in the papers.

## How to run

```bash
cd verification
python3 -m venv .venv && source .venv/bin/activate   # or reuse an existing venv
pip install mpmath numpy sympy
python run_all.py            # runs v1..v13, exits 0 iff all pass
python v1_e8_glue.py         # any single module also runs standalone
```

Dependencies: `mpmath`, `numpy`, `sympy` for the claim suite (`run_all.py`,
`v1`..`v13`). The two helper generators need extra packages: `make_figures.py`
also needs `matplotlib` (writes `../figures/*.pdf`); `make_manifest.py` needs
only the standard library (writes `../manifest.sha256`).

## Script ↔ claim ↔ document map

| Script | Verifies | Referenced in |
|---|---|---|
| `v1_e8_glue.py` | **Glue theorem** `E8 = (D5⊕A3)+μ4`: `disc(D5)=disc(A3)=Z4`, `q(D5)+q(A3)=5/4+3/4=2`, `240=16·5·3`, `248=240+8` | intro, tfpt_1 (Part II), tfpt_3 |
| `v2_carrier_pascal.py` | **Carrier/Pascal closure**: `g_car=5` unique; `16=1+5+10`; `N_fam=3`, `rank E8=8`, `Ω_adm=48`, `b1=41/10` | tfpt_1, tfpt_2, intro |
| `v3_em_alpha.py` | **EM closure**: unique root of `F_{U(1)}(α)=0`, `α⁻¹=137.0359992168`, existence/uniqueness, inverse test, ablation | tfpt_1 (EM closure), tfpt_2, intro |
| `v4_flavor_matrix.py` | **Flavor residue matrix** `R`: `det R=8=h(D5)`, principal minors `{2,3,5}`, char.poly `t³−9t²+10t−8`, SNF `diag(1,1,8)`, `‖R‖²=78`, `∑L=40` | tfpt_1, tfpt_2, tfpt_3 |
| `v5_e8_cascade.py` | **E8 cascade spine** `D_n=60−2n`: endpoints `60,8`; exponent rungs sum `240`; IR tail product `46080=|W(D5)||W(A3)|`; variance `6552=78·84` | tfpt_3 (cascade bridge) |
| `v6_bootstrap.py` | **Self-consistency bootstrap**: reverse glue `μ²−5μ+4=0`; `g_car=5` forced three ways; `8=rank E8=h(D5)=φ(30)` | intro (back-channel), tfpt_3 (Part III) |
| `v7_gravity_cosmo.py` | **Gravity/cosmology**: scalaron exponent `7`; `M_scal²/M̄²=c3⁷` (`3.06e13 GeV`); `A_s`, `n_s`, `r`; `Ω_b`; `sin²θ12=1/3−φ0/2` | tfpt_1, tfpt_2, intro |
| `v8_horizon.py` | **Horizon readouts**: `1/(2π)=4c3`; `1920=|W(D5)|`; `S_dS=e^{2α⁻¹}/(128c3⁴)`; Page; `β_rad=φ0/4π=0.2424°` | tfpt_horizon_readouts |
| `v9_neutrino_texture.py` | **Solar angle θ₁₂**: explicit μτ-symmetric Majorana texture → `sin²θ12=1/3−φ0/2=0.30675`, `θ23=45°`, `θ13=0`; residual `ε=3φ0/4≈c3` (0.23%) | tfpt_3, tfpt_2 |
| `v10_projection_involution.py` | **Q,Σ algebra**: `K=R+QΣ`, `L=R+Q(I+Σ)`; `χ_Q=(t-1)(t²-5t+3)`, `χ_K=(t-1)(t²-8t+4)`; det ladder `(3,4,8,20)`, product `1920=|W(D5)|`; `Q±`,`K±`; `a^T K a=41` | tfpt_2 (Q,Σ section) |
| `v11_unique_KQ.py` | **Uniqueness**: `K` and `Q` are the *unique* nonneg-int matrices with their row/col sums, char.poly and monotone rows (exhaustive enumeration) | tfpt_2 |
| `v12_mass_generation_polynomials.py` | **Sector/generation polynomials** of `K` + anchor-block det ladder `(9,10,16,40)` | tfpt_2 |
| `v13_open_gates.py` | **Gate closures**: `M=41=10b1=ΣL+N_Φ`; `Q₊=A₃` exponents, `Q₋²=N_fam` | tfpt_2 |
| `v14_carrier_uniqueness.py` (A2) | **g_car=5 forced**: unique `g` with `N_fam∈Z⁺` and `g+N_fam=8`; split `(3,2)` from `b+s=5, b²+s²=13`; `Tr Y=Tr Y³=0` | tfpt_1 |
| `v15_bootstrap_classification.py` (A1) | **D5⊕A3 unique**: the only familyful cyclic-glue decomposition of E8 (16-spinor + 3 families), glue `Z4=|μ4|` | tfpt_1, tfpt_3 |
| `v16_solar_dual_anchor.py` (A3) | **Solar lemma**: `aᵀR⁻¹=aᵀL⁻¹=(-½,-½,1)`; `sin²θ12=⅓-φ0/2=0.3067`; full PMNS | tfpt_2 |
| `v17_hexagonal_resolvent.py` (A4) | **Resolvent backbone** `D_y⁻¹=(Σ y^{5-m}δ^m U₆^m)/(y⁶-δ⁶)`; quark c-digits = open `U_f*` step | tfpt_2 |
| `v18_quark_yukawa.py` (A4) | **Quark sector**: `y=λ_Y^L·Λ` reproduces source ratios (`mu/md=0.470085`, `mc/ms=13.61`, `mt/mb=40.80`) exactly + lepton `c=(16/7,4/3,7/6)`; full hierarchy; exact quark `c` need `U_f*` (open) | tfpt_2 |
| `v19_monodromy_moduli.py` (A4 deep) | **`U_f*` reduction**: exact pole `z_*=(794-7√9961)/2187` (`3⁷`); bare resolvent fails 3-11× (holonomy essential); required `Λ=(0.475,1.107,0.917)`, `Λ_μ>1`⇒non-unitary; D4-symmetric SU(3) monodromy constructible but **D4-fixed locus positive-dimensional** ⇒ exact quark `c` reduce to the `(U)` stable-point selection | tfpt_2 (H2) |
| `v20_lepton_c_derivation.py` | **Lepton c's DERIVED**: rational ⇒ from `δ=1/2` (not `δ_ph`). Non-anchor `c=\|μ4\|^w/(5/4−cos(rπ/3))` ⇒ `c_e=16/7, c_μ=4/3`; anchor via product `Π c=2^{g_car}/N_fam²=32/9` ⇒ `c_τ=7/6`. **Lepton-specific** (down sector forces `c_d/c_s=4` vs `0.94`) | tfpt_2 (leptons) |
| `v21_solar_product_quark.py` | **3 A-tasks**: solar coeff `= q(A3)=3/4` (the A3 glue-norm, `q(D5)+q(A3)=2`), `sin²θ12=1/3−φ0/2`; product `32/9=2^{g_car}/N_fam²` (full Clifford dim), `ΣL=16=dim S+`; quark non-extension (`c_c/c_s=1/7` vs `0.724`) | tfpt_2 |
| `v22_open_gates_audit.py` | **residual-gates audit contract** (A2,B3,B4,B5,B6,C7): machine-pins the exact reduction of each open gate (what is forced vs. the named residual). None closed — gates made explicit, not hidden | tfpt_2/4 |
| `v23_anchor_generator.py` | **anchor-first**: `a=(1,1,2)` → elem. sym. `(4,5,2)=(\|μ4\|,g_car,\|Z2\|)`, `c3=1/(2e₁π)`; power sums `p_n=2+2^n` → `\|R(E8)\|=240`, `dim E8=248`, binary ladder. Inputs reduce to `{a,π}` | introduction, tfpt_1 |
| `v24_quark_ratio_closure.py` | **quark RATIO closure**: `c_u/c_d=55/117`, `c_c/c_s=34/47`, `c_t/c_b=3/26` from TFPT blocks; mass ratios match `<0.03%`; rational `c` gauge, `Λ_q` in O(1) | tfpt_2 |
| `v25_frontier_conjectures.py` | **conjectures [P]**: Koide source→pole `Q_src+φ0/24≈2/3` (`\|W(A3)\|=24`); axion `f_a=M_scal/128→m_a≈23.8 μeV` | tfpt_4 |
| `v26_flavor_frontier_unification.py` | the **`11` is not uniquely forced** (≥5 readings; `55/117`=table ratio) ⇒ stays `[P]`; **unifies** the open flavor surface (c_u/c_d, Q-geometry, R-mod-(U), H2-equiv) into ONE `(U)` gate; sharpening: cusp config on the **parabolic stability wall** ⇒ polystable `∇_F*` | tfpt_2 (H2) |
| `v27_wall_representative.py` | **`(U_wall)` explicit**: balanced wall rep `W_wall` (cols=perm(0,1,2)/3, rows `w=(2,1,1)`, pardeg 0); selector `det R=8, SNF(1,1,8), Spec(Q+)={1,2,3}` ⇒ one `D4`-fixed polystable point gives `R,Q,U_f*,c_u/c_d,c_q,H2` together | tfpt_2 (H2) |
| `v28_gravity_fR.py` | **R+R² closed [I/P]**: `f(R)=R+R²/(6M²)`, `M=c3^{7/2}Mbar`=scalaron mass; `f(R)` field eq + trace; `N*=57`→`n_s=0.9649,r=0.0037,A_s=2.17e-9`; full metric measure `[A]`; `248c3²<6log(3/2)` | tfpt_2, tfpt_4 |
| `v29_research_contract_certs.py` | **research-contract certificates**: `C_U^(1)` wall enumeration (1296→144 walls→**5 orbits**, so symmetry alone does NOT pick `W_wall` — honest U1 correction); `G5` gap-dominance `2‖V‖=0.785<Δ=2.433`, `Δ_eff>1.647` | tfpt_research_contracts |
| `v30_d4_character_variety.py` | **C_U^(2)**: full `D4`-fixed `SU(3)` character variety is **positive-dimensional** (reflection does not isolate the point) ⇒ the selector must cut it, needing the `R(ρ)` parabolic↔residue dictionary (= H2) — the single remaining `(U_wall)` input | tfpt_research_contracts |
| `v31_R_dictionary.py` | **R(ρ) characterized**: case A alive (all `D4`-fixed monodromies irreducible ⇒ nontrivial mixing, U2 ≠ B); `R(ρ)` not algebraic (`R` integer, traces continuous) ⇒ it is the transcendental **non-abelian-Hodge** parabolic-degree map; `C_U^(3)` residual = the Hitchin solve | tfpt_research_contracts |
| `v32_rh_splitting.py` | **RH route (result-open)**: exponent collapse `ΣU^kA₀U^{-k}=4·diag(A₀)` exact ⇒ **splitting type made algebraic** `O(-2)⊕O(-1)²⟺diag(A₀)=(½,¼,¼)` (Schur-Horn); honest wall: `∏M_k=I` is path-ordered (not `exp`), `R`-extraction needs the H2 bridge — `c_u/c_d` not obtained (no fabrication) | tfpt_research_contracts |
| `v33_explicit_flat_bundle.py` | **explicit valid flat bundle (RH-solve output)**: hardcoded `A₀` realises cusp class + splitting `O(-2)⊕O(-1)²` + trivial ∞-monodromy `‖M_∞−I‖~1e-9` (⇒`∏M_k=I`) + **irreducible (case A)**. Existence + case A confirmed; unique `∇_F*` needs `det R=8`, `c_u/c_d` needs H2 | tfpt_research_contracts |
| `v34_h2_bridge_attempt.py` | **H2-bridge attempt (honest negative)**: explicit per-puncture `M_k` (cusp class, `∏M_k=I`); `\|diag M_k\|=(0,½,½)`, natural extraction does NOT reproduce the lepton amplitudes ⇒ the `Γ^min` geodesic-to-word dictionary is genuinely missing; `c_u/c_d` not obtained (no fabrication) | tfpt_research_contracts |

> **Scripts `v35`–`v91`.** The table above lists the original `v1`–`v34` core; the
> later scripts (`v35`–`v91`, including the operator-pencil sequence
> `v80`/`v81`/`v82`/`v85`) are each registered with a one-line description in
> `run_all.py` and typed in `status_ledger.csv` (**the source of truth**).
> `v82_koide_attractor_splitting.py` proves two structural results on top of
> the `v80`/`v81` anchor-block double cover: **(A)** the Koide source→pole RG attractor
> is *forced, not postulated* — a branch-divisor-preserving Möbius map fixing both
> branch points `q=2,5` is unique, and its multiplier `(2/3)⁶` is exactly the
> subleading eigenvalue `λ₂` of the already-established gapped transfer operator
> (`v54`/`v56`), with the Koide branch `−2/3=−|Z2|/N_fam` equal to that operator's cusp
> weight — so the three "Koide postulates" collapse to one `[P]` identification
> (`FR.KOIDE.04`); and **(B)** the clean rational double cover is *non-generic* — the
> splitting-type placements give discriminants `81=N_fam⁴`, `49=scalaron²`,
> `40=|R(D5)|`, only two of which split, hardening "anchor-first" (`FLAV.PENCIL.04`).
> The most recent, `v85_master_cover.py` (`FLAV.PENCIL.05`), answers `next.txt` P3:
> the anchor-block determinant is **GL(2)-covariant** on `span{K,Q}`, so there is
> exactly **one** double cover up to Möbius reparametrisation (`disc = N_fam⁴·det(G)²`)
> and the whole disc-81 family (incl. the `−8/3 = −rank(E8)/N_fam` rung = carrier −
> one transport period) is its orbit; P6 is answered **negatively** (`μ₄` is not a
> 4:1 cover of the line — the tower is a ladder of double covers); P4 is typed (the
> branch trace fixes only the scalaron *scale* exponent, the tilt stays `[P]` with
> external `N_star`); and `v86_nstar_reheating.py` (`COSMO.NSTAR.01`) computes that
> external `N_star` from the theory's own scalaron mass plus *standard* reheating
> physics: `Γ = 4M³/(48πM̄²) = 128 GeV`, `T_reh = 9.6e9 GeV`,
> `N_star(k=0.05/Mpc) = 51.4` ⇒ `n_s = 0.9611`, `r = 0.0045` — typed `[P]`,
> inside the frozen registry band (registry untouched), with the +0.9σ Planck
> `n_s` tension recorded as the kill criterion.
> The B-round adds three structural scripts: `v89_carrier_index_lemma.py`
> (`GATE.METRIC.06`) reframes the Gate-A theorem as an **index computation** —
> KLM `μ_A = [B:A]²μ_B` gives Jones index `[(E8)₁:(D5)₁×(A3)₁] = 4 = |μ₄|`
> (the glue-group order *is* the inclusion index; all three glue sectors are
> `h=1` currents; holomorphy then *follows* from μ-additivity `16/4² = 1`);
> `v90_conical_defect_chain.py` (`SEAM.AREACOEFF.03`) **derives** the
> Fursaev–Solodukhin factor `S = 4πkA` (smoothed-cone Gauss–Bonnet, exactly
> smoothing-independent; `S = A/4 ⇔ c₃ = 1/(8π)` sympy-solved) so the
> Seam–Horizon residual is isolated to the single step "seam determinant ⇒ EH
> form", with no Bekenstein–Hawking import anywhere; and `v86` (extended)
> records the **A_s dichotomy**: matching A_s at the slow-reheating point
> would need `M_scal × 1.092` — impossible at locked `c₃^{7/2}` — so either
> fast preheating `[P]` or the exponent-7 normalisation fails (decisive).
> `v91_spine_tetrahedron.py` (`ARCH.SPINE.01`) packages the spine `{2,3,4,5}`
> as one finite object (edges/faces/volume = the integer grammar, volume `120 =
> |R⁺(E8)|`, graph form `240 = |μ₄|·|E(K₄)|·|E(K₅)|` with a `K₆` negative
> control), with the dual cuts typed as tautological presentation and the
> sub-grammar incompleteness (`7,16,41,48,240,248` outside) stated honestly.
> Two red-team follow-ups complete the round: `v87_bulk_uniqueness_reduction.py`
> (`GATE.METRIC.05`) merges Target-A residual (ii) into (i) — for a holomorphic
> net the 2D bulk is unique (LR/KLM/BKLR), machine-contrasted against `SO(16)₁`
> whose `Z2×Z2` discriminant category admits **six** modular invariants (incl.
> both `E8`-extension pairings) — so **Target A = one residual**; and
> `v88_cp_phase_audit.py` (`FLAV.CP.01`) quantifies the Target-D CP residual:
> frozen `δ = π/3+3λ²` survives at `+0.98σ` vs `γ_PDG`, the data central value
> sits `0.07°` from the alternative `π/3+2λ²` (recorded as a look-elsewhere
> trap, **not** adopted), decision at `σ_γ ≤ 0.96°`.

**Freeze file.** `freeze_file.csv` registers the committed kill criteria for every
falsifiable prediction (solar angle, `r`, ordering, nEDM, `w`, ...), referenced by
the introduction's *Freeze file* box.

**Blind-prediction registry (frozen 2026-06-09, machine-enforced).**
`predictions_frozen.json` freezes every *dimensionless prediction of record* at
25 significant digits **before** the next decisive data releases (JUNO
`θ12`/`θ13`, CMB-S4/LiteBIRD `r` and `β`, DESI `n_s`). `v84_frozen_registry.py`
re-derives every frozen decimal from the two axioms on each suite run, so the
formula and the frozen value are locked together: changing either alone fails
the suite, and the file itself is covered by `manifest.sha256`. The registry
also *enforces* the `θ12` freeze convention of `tfpt_2`: exactly **one**
prediction of record (`sin²θ12 = 1/3 − φ0/2 = 0.306747…`), with the seam
(`0.306808`) and non-linear (`0.307020`) values typed as derived variants of the
*same* texture — they can never silently become alternative predictions
(look-elsewhere ambiguity machine-excluded). Conditional entries carry their
hypothesis by name; `r` and `n_s` are registered as *bands* over the declared
external `N_star ∈ [50, 60]`, never as point predictions. Ledger row:
`REG.FREEZE.01`.

`tfpt_constants.py` holds the shared primitives and the `check()` harness; it is
imported by every `v*` script and by `run_all.py`. **All carrier integers
(`N_fam`, `Ω_adm`, `b1`, `dim S⁺`, `rank E8`) are now computed from `{c3, g_car}`
in `tfpt_constants.py`, not hand-assigned** (reviewer point A6).

`v1_e8_glue.py` ships an **explicit E8 lattice certificate** (reviewer point A5):
it builds all 240 roots, the Bourbaki simple-root basis, and certifies the
lattice is *even* and *unimodular* (Gram det = 1) with every root integral over
the basis — i.e. the constructed overlattice **is** E8, not just a matching of
the arithmetic tail.

## Content manifest (stable identity)

`python make_manifest.py` writes `../manifest.sha256` (sorted `sha256  path` over
the six TeX sources, the figures, and the verification suite) plus a single
*manifest digest* that is the stable content identity of the project — use this,
not the Overleaf export-zip hash, as the canonical identity (reviewer point A3).

## Single status ledger (source of truth)

`status_ledger.csv` is the **single source of truth** for every claim: its
`claim_id` (e.g. `E8.GLU.01`, `EM.FP.01`, `QG.AMB.01`), `status`
(Axiom / Formal / Lattice / Numerical / Physical / Open), `location`,
`dependencies`, `script`, and `external_data`. The six PDFs are written against
it; if a document and the ledger ever disagree, **the ledger wins**.

## Lean provenance (the `Formal` rows)

**Shipped path.** In the reviewer package the Lean project ships at the package
root as `lean4-carrier-rigidity/`. In the source repository the same project
lives at `experiments/lean4-carrier-rigidity/`. A referee should follow the
**shipped** path; both contain identical content (toolchain
`leanprover/lean4:v4.29.1`). One command runs the hard audit gate:

```bash
cd lean4-carrier-rigidity        # source repo: experiments/lean4-carrier-rigidity
bash scripts/audit.sh            # ~7 s with cached .lake/build
```

It enforces and (this round) passes: `lake build` succeeds (1886 jobs);
no `sorry`/`admit`; no `axiom`/`constant`/`unsafe`/`opaque`/`partial`
declarations; and `#print axioms` on every headline theorem returns **only**
the three standard Lean kernel axioms (`propext`, `Classical.choice`,
`Quot.sound`). Use `--quick` for the static checks without a build. The full
transcript (toolchain version + `AUDIT: PASS` record) is saved at
`lean4-carrier-rigidity/AUDIT_TRANSCRIPT.txt` (reviewer point A4).

**Lean manifest.** `make_manifest.py` now also covers the Lean archive: it
writes a dedicated `lean_manifest.sha256` (sorted `sha256  relpath` over every
Lean source, `lakefile.lean`, `lake-manifest.json`, `lean-toolchain`, the audit
script and transcript) so the Lean layer has a stable content identity of its
own, separate from the TeX/Python `manifest.sha256`.

A *future* hardening target (not a blocker for the present script-certified
status): formalise the E8 lattice/glue certificate of `v1_e8_glue.py` in Lean.
Today the E8 glue is **script-certified** (240 roots, Gram evenness,
unimodularity, root integrality, glue index `Z4`); the Lean formalisation of
that certificate would be an additional, non-blocking layer.

## Status markers in the papers

`[I]` exact identity · `[L]` Lie/lattice theorem · `[F]` formalised (Lean/script)
· `[N]` numerical fixed point · `[P]` physical/conditional · `[A]` axiom/open.
Claims carrying `[I]`, `[L]` or `[N]` are the ones reproduced by this suite;
`[F]` Lean material lives in `lean4-carrier-rigidity/` (shipped) /
`experiments/lean4-carrier-rigidity/` (repo).

## Residual gates (explicitly open — do not silently promote)

The audit-visible residual gates (Alessandro 5.0 review). These stay `[A]`/`[P]`
and must not be rendered as closed:

| Gate | Status | What is missing |
|---|---|---|
| Geometric origin of `Q` | `[A]` | `Q±` not yet forced from the `D4`-equivariant parabolic geometry on `P¹∖μ4` (reduced to two finite statements; see `v13`, `v19`) |
| `R` modulo unitarity `(U)` | `[P]` | `R` derived up to the Mehta–Seshadri unitarity condition; the `D4`-fixed locus is positive-dimensional (`v19`), `(U)` selects the stable point |
| `N_star` | `[P]` | reheating input, **not** a compiler consequence |
| Covariant metric-sector eq. | `[A]` | full Einstein-side field equation open; `R+R²`/scalaron is a readout, not a closure |
| Wolfram `[C]` second path | — | `.wl`/`.wls` exports shipped in `verification/wolfram/` as an independent numerical path |

## Red Team / Stress Test layer (`redteam/`)

A **deliberately adversarial** layer that tries to *break* the five load-bearing
reductions instead of confirming them (the v78-review request). It is separate
from `run_all.py` on purpose: its checks assert adversarial facts (a
counterexample exists, a hidden assumption is needed, a firewall holds), and the
honest outcome of each target lives in a **status**, not a green pass.

```bash
cd redteam && python run_redteam.py     # runs targets A–E + writes redteam_table.txt
```

| Target | Script | Verdict |
|---|---|---|
| A — (E8)₁ boundary-net identification | `redteam/rt_A_e8net.py` | reduced, not closed (`c=8` underdetermines the net; holomorphy is the missing assumption). After `v83` + `v87`: **one** residual — holomorphy+`c=8` pins both the net (`v83`) *and* the unique 2D bulk (`v87`, LR/KLM/BKLR; `SO(16)₁` counter-model admits six modular invariants) |
| B — carrier rank / Pascal condition | `redteam/rt_B_pascal.py` | survives, narrowed (arithmetic `[F]` stands; the Pascal *selection* is typed `[A]/[P]`) |
| C — `k = c₃/2` seam-area coefficient | `redteam/rt_C_kc3.py` | survives (dimensional firewall: no naked `k_phys = c₃/2`) |
| D — `U_point → v_geo` bijection | `redteam/rt_D_upoint.py` | survives, narrowed (four hypotheses made explicit; CP phases residual) |
| E — `v_geo` dimensional floor | `redteam/rt_E_vgeo.py` | survives, narrowed (floor of the certified tiers; frontier scales stay typed) |

Verdicts are recorded as ledger rows `REDTEAM.A.01 … REDTEAM.E.01` and presented
in the note `tfpt_5_redteam.tex`. See `redteam/README.md` for the full protocol.

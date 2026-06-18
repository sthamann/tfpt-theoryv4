# TFPT — Wolfram independent verification path

This folder provides an **independent second computational path** (Wolfram
Language) for the core TFPT numerical readouts, requested in the 5.0 review
(point 3: the `.wl`/`.wls` exports for the `[C]` audit layer). It does **not**
replace the Python suite — it is a deliberately independent engine that
reproduces the same headline numbers, so a reviewer can cross-check the
`[N]`/`[C]` readouts without trusting a single toolchain.

## Run

```bash
wolframscript -file tfpt_readouts.wl
```

(or load `tfpt_readouts.wl` in a Mathematica notebook / kernel). It prints
`[PASS]`/`[FAIL]` per readout and a final `ALL WOLFRAM CHECKS PASSED` line.

### Local engine status (this machine)

`wolframscript` is installed (`brew install --cask wolfram-engine`, 14.3.0.0),
the kernel path is configured, and the free Wolfram Engine license is
**activated**. `wolframscript -file tfpt_readouts.wl` runs clean:

```
--- Wolfram readouts: 116 passed, 0 failed ---
ALL WOLFRAM CHECKS PASSED
```

So the independent Wolfram path is **verified to reproduce** the Python suite's
headline readouts (`α⁻¹`, E8 glue, `M=41`, K/Q ladder `1920=|W(D5)|`, lepton
`c=(16/7,4/3,7/6)`, solar `sin²θ12=1/3−φ0/2`, the G2 heat-kernel coefficients,
the anchor-plane Plücker apparatus, and the `(U_wall)` selectors) on a different
engine.

To reproduce on another machine: get a free license at
<https://www.wolfram.com/engine/free-license>, run `wolframscript -activate`
once (Wolfram ID + password), then `wolframscript -file tfpt_readouts.wl`.

## What it reproduces (mirrors `verification/v*.py`)

| Readout | Wolfram | Python counterpart |
|---|---|---|
| EM closure `α⁻¹ = 137.0359992168` (unique root of `F_{U(1)}=0`) | `FindRoot` | `v3_em_alpha.py` |
| E8 glue arithmetic `240=16·5·3`, `248=240+8`, `h=30` | exact | `v1_e8_glue.py` |
| carrier/Pascal `16=1+5+10`, `N_fam=3`, `rank E8=8` | exact | `v2_carrier_pascal.py` |
| EM budget `M=40+1=10 b1=41`, `aᵀKa=41` | exact | `v13`, `v10` |
| K/Q/Σ ladder `det(Q,K,R,L)=(3,4,8,20)`, product `1920=|W(D5)|` | exact | `v10_projection_involution.py` |
| lepton `c` from `δ=1/2` resolvent + product `32/9` → `16/7,4/3,7/6` | exact | `v20`, `v21` |
| solar `q(A3)=3/4`, `q(D5)+q(A3)=2`, `sin²θ12=1/3−φ0/2` | exact | `v16`, `v21` |
| anchor generator `e_k(a)=(4,5,2)`, `p_n=2+2^n` → `240,248` | exact | `v23` |
| quark ratios `55/117, 34/47, 3/26` | exact | `v24` |
| G2 spectral action `a2=−R/3`, `a4|R²=R²/72` → `R+R²` | symbolic | `v36_spectral_action_g2.py` |
| Plücker apparatus `‖Pl(K)‖₁=11`, `‖Pl_R(K)‖₁=26`, `ΣPl_R(L)=60`, pencil `det(K+xQ)=3x³+7x²+6x+4`, dualities, lepton ring | exact | `v37_plucker_anchor.py` |
| `(U_wall)` selectors `Spec(Q₊)={1,2,3}=3α+1`, `det R=8`, splitting `=a` | exact | `v39_uwall_selectors.py` |
| Exterior Leg Lemma: scalar leg → `c_u/c_d≡1`; anchor microcode `e₂(p₃+1)/(p₀²(2p₂+1))=55/117` | exact | `v42_exterior_leg.py` |
| carrier exterior grading `16=Λ^even(5)=1+10+5`; exterior degrees `(u,d)=(2,4)`, sum`=6`, diff`=2` | exact | `v44_carrier_exterior.py` |
| the `11` is Pascal: `\|Pl(K)\|₁=11=Σ_{k≤2}C(4,k)=16−g_car`; `15=dim su(4)=10+5=N_fam·g_car` | exact | `v45_family_exterior.py` |
| Grand Mass Volume: sector det exponents `=K`-row sums `(6,9,10)`, total `25=g_car²`; `Q`-rows `(4,5,6)` | exact | `v46_grand_mass_volume.py` |
| Selection (Thm A): `q(D5)+q(A3)=2`, glue `4=|μ4|`, only `n=5` gives 16-spinor | exact | `v47_selection_theorem.py` |
| EM Ward (Thm C): `8b1=(4/5)M=164/5`, `−5/4=q(D5)` | exact | `v48_em_ward.py` |
| Readout Rigidity (Thm U2): `c_u/c_d=55/117` stratum-constant | exact | `v49_readout_rigidity.py` |
| Q geometry (Thm Q): `χ(Q_+)=(t−1)(t−2)(t−3)`, `χ(Q_−)=t(t²−3)` | exact | `v50_q_geometry.py` |
| glue norms `=(g_car,N_fam)/|μ4|`; four ops forced `{2, 1/2=δ, 15/16, 5/3}`, reproduces `16/7,4/3` | exact | `v51_boundary_half_step.py` |
| pencil endpoints `P(−1)=2,P(0)=4,P(1)=20,P(2)=68=2p₅`; `det(K−Q)=2`, `tr=N_fam` | exact | `v52_pencil_endpoints.py` |
| compiler core from `(5,3)`: `rank E8=8`, `\|Z2\|=2`, Pythagorean `25=9+16=N_fam²+\|Z2\|·rank E8=dim S⁺`, anchor char-poly unique | exact | `v53_compiler_core.py` |
| seam=horizon keystones: `8` triply-forced (`2\|μ4\|=rank E8=h(D5)=φ(30)=8π` grav), one transfer op `(2/3)⁶` for flavor+horizon | exact | `v54_seam_horizon_keystones.py` |
| E8 Coxeter cycle: exponents `=`totatives(30), `φ(30)=8`, order `30=\|Z2\|·N_fam·g_car`; `S_dS·ρ_Λ=32π⁴`; `S_dS=2^g_car·π^\|μ4\|·e^{2α⁻¹}` | exact | `v55_coxeter_cycle.py` |
| unique attractor: gap `6log(3/2)>0`, Coxeter in `\|μ4\|=4` planes, sum exps `=120=\|R⁺(E8)\|`, `rank·h=240` | exact | `v56_unique_attractor.py` |
| horizon cross-links: `c3=`Einstein/Jacobson `8π`, `1/4=1/\|μ4\|`; Hod QNM `ln3=ln N_fam`; `1920=\|W(D5)\|` | exact | `v57_horizon_crosslinks.py` |
| seam-horizon chain: one-sided `S²` Gauss-Bonnet `c3=1/(2·4π)`, seam units `1/(2c3)=4π`, `1/(4c3)=2π` | exact | `v58_seam_horizon_chain.py` |
| area-law evidence: `8=\|Z2\|·\|μ4\|`, `2π=1/(4c3)` (the free-field EE area-law is numerical, Python-only) | exact | `v59_area_law_evidence.py` |
| Λ branch: `(8π)²δ_top=3/(4π²)`, mis-scale `2c3/δ_top=64π³/3` (G_N pinned); `(1,5,10)=K5` | exact | `v60_lambda_metrology_branch.py` |
| CFT bridge: WZW `c=(8,5,3)=(rank E8,g_car,N_fam)`, conformal embedding `c_coset=0`; `N_fam=\|μ4\|−1` | exact | `v61_cft_bridge.py` |
| Seam-Engineering Index `Ξ=2\|V\|/Δ=31/(24π²log(3/2))≈0.323`, `2\|V\|=31/(4π²)`, `Δ_eff≈1.648` | exact | `v63_seam_engineering_index.py` |
| compiler atoms `=` E8 Casimir degrees `{2,8,12,14,18,20,24,30}`; `Σ=128=2⁷`, `Σexp=120=\|R⁺(E8)\|` | exact | `v66_e8_casimir_degrees.py` |
| central theorem closure: Fursaev-Solodukhin `S=4πk A`, `k=c3/2` ⟹ `2πc3=1/4` ⟹ `S=A/4`; `c3=1/(8π)` unique | exact | `v67_area_law_coefficient.py` |
| residual resolved: Seeley-DeWitt `a₂=−d/(192π²)R`, `1/G` UV-sensitive ⟹ `k=c3/2` is normalization | symbolic | `v68_seeley_dewitt_residual.py` |
| D4-equivariant Q: Z4 eigenphases, `Q₊=3w+1=diag(1,2,3)`, `Q₋` E-coupling `√3` ⟹ `t(t²−3)` | exact | `v69_d4_q_geometry.py` |
| Q integer-lift: `R` unimodular (`{-1,i,-i}`), `det Q=3=N_fam`, SNF `diag(1,1,3)` | exact | `v70_q_integer_lift.py` |

The numerical `(U_wall)` results (kill-switch sampling `v38`, harmonic-metric
unitarisation `v40`, leg test `v41`) rest on `scipy` ODE/linear-algebra and are
the Python path; the Wolfram path mirrors their **algebraic** content (`v39`).

## Provenance note

As with the Lean archive (whose local reproduction is pending on the reviewer's
side), this Wolfram path is shipped as source; it was authored to match the
machine-checked Python results to the quoted precision. The two primitives
`c3 = 1/(8π)` and `g_car = 5` are the only inputs.

## Extension file (v84–v158) — verified running

`tfpt_readouts_extension.wl` mirrors the v84–v101 round (frozen registry,
master cover, reheating arithmetic, bulk uniqueness, carrier index, conical
defect chain, spine tetrahedron, glue uniqueness, Koide relaxation toy,
sheet diamond `v94`, centered diamond `v95`, branch-kernel selection `v96`,
sheet-conjugation bridge `v97`, discriminant dictionary `v98`, Koide flow
time `v99`, horizon anchor `v101`, seam orientation `v102`, trisection normal form `v103`, Nariai clock `v104`, residual inventory `v105`, review validation `v106`, quantum-clock target `v107`, Pascal ladder `v108`, sheet pairing `v109`, Calderón-sheet selection `v110`, quadratic transport `v111`, self-counting channel `v112`, quasi-free kernel `v113`, torsion delta `v114`, anchor residue `v115`, resonance theorem `v116`, monodromy = W(A₃) `v117`, hexagon-family dictionary `v118`, second review validation `v119`, address table `v120`, address pinning `v121`, margin theorem `v122`; the inventory-update `v123` is ledger bookkeeping, Python-only by nature; resummed clock `v124`, glue Q-system `v125`, clock-wall bridge `v126`, ring resummation `v127`, graded hull `v128`, entropy power law `v129`, Born square `v130`, measure-is-area `v131`, det-ratio anomaly `v132`, zeta budget `v133`, dual anchor `v134`, determinant surface `v135`, dual-normal selector `v136`, Q+ cohomology `v137`, VW firewall `v138`, selector triangle `v139`, canonical map `v140`, deck selection `v141`, frame integrality `v142`, graded Frobenius `v143`, det-ratio family cancellation `v144`, pairing atoms `v145`, Möbius D4 realisation `v146`, clock Gaussian model `v147`, NS/R sector census `v148`, cusp normal `v149`, replica EH model `v150`, BFK split `v151`, R3 normalisation = anchor `v152`, No-Unit Theorem `v153`, Simple-Current Extension `v154`, seam-net construction `v156`, rigid fixed point `v157`, fixed-point stability `v158`, PyR@TE gauge cross-check `v159`, QGEO rigidity `v168`, E8 slice compression `v170`, atomic OS moment + Sugawara `v171`, trace-anomaly seed `v172`, seam Fock readings `v174`, net existence + full-cone RP `v175`, Koide F-corner 53/54 `v183`, Riemann-Roch carrier `v189` (h⁰=5/rankH₁=3=rank(D5)/N_fam), Nariai entropy bound `v190` ((x−1)²≥0), universal branch line `v191` (affine relabeling + decoy negative control), QGEO.ENERGY.02 EH-rigidity `v193` (k selects q(A3)=3/4 family, not q(D5)=5/4 carrier), QGEO.MARKS.02 Lefschetz/character `v195` (Tr(ρ|H¹)=−1, free μ4 orbit forced), QGEO.VARI.01 `v196` (E_fail=0 on the μ4 block), ARCH.RRCAR.02 `v197` (Λ^even(C⁵)=16=D5 half-spinor), QGEO.MODULAR.01 `v198` (principal symbol |k|=diag(|n|) commutes exactly with the clock diag(i^n)), QGEO.STATE.01 `v199` ([ρ,H]=0 ⟺ H μ4-character-block-diagonal), QGEO.SUBPRIN.01 `v201` (a μ4-mark sum ∑_{j=0}^3 e^{−i m 2πj/4}=4·[m≡0 mod 4] is Z4-invariant ⟹ the sub-principal symbol M_f is character-block-diagonal — block-diagonality forced by the marks, not postulated), HOR.EHT.01 `v203` (the EHT achromatic polarization coupling 16 c₃⁴ = 1/(256π⁴) = δ_top/3, the same top-form coefficient as the α-kernel correction), and the 2026-06-15 archive-integration round FR.MUONG2.01 `v204` (the muon seam-vertex value a_μ = (5/4)(48 c₃⁴)²/(2π) = 45/(524288 π⁹)), GRAV.XI.01 `v205` (ξ = c₃/φ_tree = 3/4 = q(A₃) = ln(m/μ), the independent gravitational 3/4), HOR.BHTHERMO.01 `v208` (the scalaron Wald factor f_R = 1+R/(3M_s²) + the modular 2π = 1/(4c₃)) — their numerical/[P] siblings v206 (H₀ branch), v207 (asymptotic safety) and v209 (BH defect) stay Python-only — their [N] census/RH/ODE parts stay Python-only; and QGEO.PILLOW.01 `v214` (the pillowcase reduction: cross-ratio 2 => j=1728 => square modulus => order-4 CM clock, unifying the v180 isometry and v201 mark-locality residuals into one canonical flat-pillowcase-metric premise) is exact and mirrored, while its Klein-J modular values stay mpmath-numerical (Python-only); and QGEO.MARKS.03 `v216` (the four marks emerge from Gauss-Bonnet: `n = 2χ = 4` plus the Euclidean-orbifold uniqueness of the pillowcase) is exact and mirrored, while its numerical sibling `v217` (the free-`n`/free-positions emergence scan on the DtN/state) is Python-only; and the diamond axis geometry `v218` (DIAMOND.AXIS/PLUCKER/SPECTRAL.01: `det(C+xU)=14+6x` linear vs `det(C+yV)=14+14y+4y²` quadratic with curvatures `(8,6)=(rank E₈,|R⁺(A₃)|)`; the Plücker ladder `K→C→F` steps `(1,8,10),(1,8,16)`; the spectral ramification squares `(1,3,4,6)` kernels `(13,48,65,105)`) is exact and mirrored, while its anchor-defect/pair-sum audit blocks and the `F`=transfer-corner heuristic stay Python-only; `v155` (quasi-free boundary) is numerical/numpy, Python-only; the v160–v167, v163/v164/v166/v169 and v173 (Pfaffian CP) rounds are numerical/inventory, Python-only by nature; the v176 Seam Collar Realisation Theorem is an assembly/reduction certificate whose exact identities are already mirrored via v168/v156/v162/v154/v175, so it is Python-only; the v177 QGEO proof tree is Möbius/cohomology symbolic (uniformisation, ω_k characters, residues), Python-only; the v178 MARKS/KERNEL deeper-reduction attempt is Möbius/Schur symbolic + numeric, Python-only; the v179 conformal-realisation unification is arithmetic/bookkeeping (Gauss-Bonnet χ=2, h(A3)=4, rank/cohomology counts), Python-only; the v180/v181 Möbius reductions (uniformisation + Kerékjártó + finite-order Möbius / equivariant uniformisation) are symbolic + cited-theorem, Python-only; the v182 reviewer-residual map is reduction bookkeeping + arithmetic, Python-only; the v184–v188 F_transfer-firewall round (η_B honest test, axion relic estimate, ledger/prose guards) is numerical/bookkeeping, Python-only; the v192 energy-conserving-clock reformulation is a [O] structural restatement of the bedrock, Python-only; the v193 QGEO.ENERGY.02 energy-commutator contract is a [O] proof target whose sub-claims are structural/logical (Python-only) while its exact q(A3) EH-rigidity rider IS mirrored above); and the 2026-06-16 structural-finds round is mirrored exactly: McKay bedrock `v219` (the 2I irrep degrees `{1,2,2,3,3,4,4,5,6}` = the affine E₈ Kac marks via `A·marks=2 marks`, sums `30=h(E₈)` and `120=|R⁺(E₈)|`), CM-norm duality `v222` (`41=N_ℤ[i](5,4)`, `7=N_ℤ[ω](3,2)`, `13=N_ℤ[i](3,2)`), Coxeter totative clock `v223` (`(ℤ/30)ˣ`=E₈ exponents, `7` order 4), the `248=120+128` channel split `v227`, the Riemann-Roch index gate `v228` (degree-4 divisor ⟹ `(5,3)`, `Λ^even(C⁵)=16`), the lepton étale Frobenius algebra `v229` (ring closure + `Discriminant(m)≠0` + `C₆` charpoly `t⁶−1`), the center budget `v230` (`(7,11,13)` = hex/Fock/square norms), the diamond F_transfer path `v224` (sheet axis `4t²+14t+14` vs flat winding `6s+8`, Plücker steps `(1,8,10),(1,8,16)`), and the dual normal frame `v225` (`d=−½(1,1,−2)`, `n·R=(8,0,0)`, `det(1,d,n)=21`) — while the CP hexagonal modulus `v220` (Klein-J modular values) and the seam recoverability code `v221` (numerical contraction bound) stay Python-only; and the 2026-06-17 CP-reduction `v231` (both CP phases are `mu6` powers of one hexagonal unit `rho=e^{i pi/3}`: `delta_CKM,lead=arg(rho)=pi/3`, `delta_PMNS=arg(rho^4)=4pi/3`, `rho^4=-rho` so they differ by the `Z2` sheet `rho^3=-1`; `C6` charpoly `t^6-1`; sheet-flipped frame orientations `+/-21 sin(pi/3)`) is mirrored exactly; and the E8 Kleinian-seam model `v232` (finite E8 = affine E8 minus the trivial node = the 8 exceptional `P^1`'s of the resolution of `C^2/2I`, negated intersection form = E8 Cartan `det=1`, link = Poincare homology sphere `S^3/2I`, `pi1=2I` order `120`) is mirrored exactly; and the 2026-06-17 closing-shape round: `v233` (CP = the universal family/triality phase, `mu6=mu3 x mu2`, `rho=omega^2*(-1)`, quark/lepton share the triality class and differ only by the sheet) and `v234` (the Seam-Holomorphy selection: `#mark-1 = |Gamma^ab| = |H1(link)|` is `1` only for E8, so holomorphy = homology-sphere = one-1-dim-irrep is one E8-selector; holomorphic `c=8=g_car+N_fam` => unique even unimodular rank-8 = E8) and `v235` (the Chern-Simons realisation: a free gapped bosonic bulk = an even K-matrix, `#anyons=|det K|`, `c=signature`, holomorphic `<=> det 1`; the v92 tower `D5(+)A3`(det 16)`->D8`(det 4)`->E8`(det 1) is the anyon-condensation tower = the Kitaev E8 state) are mirrored exactly; and the 2026-06-17 capstone round: `v236` (the (2,3,5) Brieskorn singularity generates the skeleton — Milnor number `(2-1)(3-1)(5-1)=8`, monodromy eigenvalues = the E8 exponents/30 = the order-30 Coxeter cycle `Phi_30`, both clocks `mu3` in `<h>=Z/30` and `mu4` in the Galois `(Z/30)^x`) and `v237` (the closing step as physics — genus-g degeneracy `|det K|^g`, no topological degeneracy `<=> det K=1 <=>` the seam is SRE = the Kitaev E8 phase) are mirrored exactly; and the 2026-06-17 closure round `v259` (PS.SPECACT.02: the seam KMS cutoff `f(u)=e^{-u}` gives `f_2/f_0=f_4/f_2=1` exactly, vs a Gaussian control `sqrt(pi)/2`, so `kappa=sqrt(c_PS/c_grav)` loses its scheme factor) and `v260` (ARCH.K3.01: one Kummer/K3 carries seam + carrier-16 + E8 — E8 Cartan `det 1`/even/pos-def, K3 lattice `U^3(+)E8(-1)^2` rank 22/`det -1`/even/signature (3,19), 16 nodes `=|A[2]|=2^4=dim S+`, 4 marks) are mirrored exactly, while `v258` (PS.DIRAC.03, the Dirac-as-covariance-induction `log((1-C)C^-1)=H` matrix-log identity) and `v261` (QFT.MSC.01, the Modular-Spectral-Closure assembly/reduction certificate, whose exact sub-facts are already mirrored via v259/v260/v89/v197) are Python-only by the suite convention (like the rest of the v238–v257 NCG round and the v176 assembly certificate). It is kept **separate** from `tfpt_readouts.wl` so the
verified 116/116 base file is untouched.

**Status: verified.** First engine run 2026-06-11 (Wolfram Engine 14.3): the
v84–v93 block passed **45/45** on first run; the v94–v140 blocks were added
the same day, the v141–v144 block on 2026-06-12. Current state:

```
--- Wolfram extension v84-v237 + v259-v260: 267 passed, 0 failed ---
ALL WOLFRAM EXTENSION CHECKS PASSED
```

(ledger `GATE.WOLFRAM.02`). The scipy-only parts of the round (the `v86`
pivot ODE solve, the `v88` data pulls, the `v99` mpmath ODE probe of the
time-1 map — its exact symbolic form *is* mirrored) stay Python-only and
are flagged as such in the `.wl` comments. The statistical numerology null
test `v100_numerology_null_mc.py` (grammar census + Monte-Carlo + RNG
controls) is likewise Python-only by the suite's convention (like
`v62`/`v64`/`v65`) and flagged in the `.wl` comment.

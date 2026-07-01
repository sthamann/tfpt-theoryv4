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
time `v99`, horizon anchor `v101`, seam orientation `v102`, trisection normal form `v103`, Nariai clock `v104`, residual inventory `v105`, review validation `v106`, quantum-clock target `v107`, Pascal ladder `v108`, sheet pairing `v109`, Calderón-sheet selection `v110`, quadratic transport `v111`, self-counting channel `v112`, quasi-free kernel `v113`, torsion delta `v114`, anchor residue `v115`, resonance theorem `v116`, monodromy = W(A₃) `v117`, hexagon-family dictionary `v118`, second review validation `v119`, address table `v120`, address pinning `v121`, margin theorem `v122`; the inventory-update `v123` is ledger bookkeeping, Python-only by nature; resummed clock `v124`, glue Q-system `v125`, clock-wall bridge `v126`, ring resummation `v127`, graded hull `v128`, entropy power law `v129`, Born square `v130`, measure-is-area `v131`, det-ratio anomaly `v132`, zeta budget `v133`, dual anchor `v134`, determinant surface `v135`, dual-normal selector `v136`, Q+ cohomology `v137`, VW firewall `v138`, selector triangle `v139`, canonical map `v140`, deck selection `v141`, frame integrality `v142`, graded Frobenius `v143`, det-ratio family cancellation `v144`, pairing atoms `v145`, Möbius D4 realisation `v146`, clock Gaussian model `v147`, NS/R sector census `v148`, cusp normal `v149`, replica EH model `v150`, BFK split `v151`, R3 normalisation = anchor `v152`, No-Unit Theorem `v153`, Simple-Current Extension `v154`, seam-net construction `v156`, rigid fixed point `v157`, fixed-point stability `v158`, PyR@TE gauge cross-check `v159`, QGEO rigidity `v168`, E8 slice compression `v170`, atomic OS moment + Sugawara `v171`, trace-anomaly seed `v172`, seam Fock readings `v174`, net existence + full-cone RP `v175`, Koide F-corner 53/54 `v183`, Riemann-Roch carrier `v189` (h⁰=5/rankH₁=3=rank(D5)/N_fam), Nariai entropy bound `v190` ((x−1)²≥0), universal branch line `v191` (affine relabeling + decoy negative control), QGEO.ENERGY.02 EH-rigidity `v193` (k selects q(A3)=3/4 family, not q(D5)=5/4 carrier), QGEO.MARKS.02 Lefschetz/character `v195` (Tr(ρ|H¹)=−1, free μ4 orbit forced), QGEO.VARI.01 `v196` (E_fail=0 on the μ4 block), ARCH.RRCAR.02 `v197` (Λ^even(C⁵)=16=D5 half-spinor), QGEO.MODULAR.01 `v198` (principal symbol |k|=diag(|n|) commutes exactly with the clock diag(i^n)), QGEO.STATE.01 `v199` ([ρ,H]=0 ⟺ H μ4-character-block-diagonal), QGEO.SUBPRIN.01 `v201` (a μ4-mark sum ∑_{j=0}^3 e^{−i m 2πj/4}=4·[m≡0 mod 4] is Z4-invariant ⟹ the sub-principal symbol M_f is character-block-diagonal — block-diagonality forced by the marks, not postulated), HOR.EHT.01 `v203` (the EHT achromatic polarization coupling 16 c₃⁴ = 1/(256π⁴) = δ_top/3, the same top-form coefficient as the α-kernel correction), and the 2026-06-15 archive-integration round FR.MUONG2.01 `v204` (the muon seam-vertex value a_μ = (5/4)(48 c₃⁴)²/(2π) = 45/(524288 π⁹)), GRAV.XI.01 `v205` (ξ = c₃/φ_tree = 3/4 = q(A₃) = ln(m/μ), the independent gravitational 3/4), HOR.BHTHERMO.01 `v208` (the scalaron Wald factor f_R = 1+R/(3M_s²) + the modular 2π = 1/(4c₃)) — their numerical/[P] siblings v206 (H₀ branch), v207 (asymptotic safety) and v209 (BH defect) stay Python-only — their [N] census/RH/ODE parts stay Python-only; and QGEO.PILLOW.01 `v214` (the pillowcase reduction: cross-ratio 2 => j=1728 => square modulus => order-4 CM clock, unifying the v180 isometry and v201 mark-locality residuals into one canonical flat-pillowcase-metric premise) is exact and mirrored, while its Klein-J modular values stay mpmath-numerical (Python-only); and QGEO.MARKS.03 `v216` (the four marks emerge from Gauss-Bonnet: `n = 2χ = 4` plus the Euclidean-orbifold uniqueness of the pillowcase) is exact and mirrored, while its numerical sibling `v217` (the free-`n`/free-positions emergence scan on the DtN/state) is Python-only; and the diamond axis geometry `v218` (DIAMOND.AXIS/PLUCKER/SPECTRAL.01: `det(C+xU)=14+6x` linear vs `det(C+yV)=14+14y+4y²` quadratic with curvatures `(8,6)=(rank E₈,|R⁺(A₃)|)`; the Plücker ladder `K→C→F` steps `(1,8,10),(1,8,16)`; the spectral ramification squares `(1,3,4,6)` kernels `(13,48,65,105)`) is exact and mirrored, while its anchor-defect/pair-sum audit blocks and the `F`=transfer-corner heuristic stay Python-only; `v155` (quasi-free boundary) is numerical/numpy, Python-only; the v160–v167, v163/v164/v166/v169 and v173 (Pfaffian CP) rounds are numerical/inventory, Python-only by nature; the v176 Seam Collar Realisation Theorem is an assembly/reduction certificate whose exact identities are already mirrored via v168/v156/v162/v154/v175, so it is Python-only; the v177 QGEO proof tree is Möbius/cohomology symbolic (uniformisation, ω_k characters, residues), Python-only; the v178 MARKS/KERNEL deeper-reduction attempt is Möbius/Schur symbolic + numeric, Python-only; the v179 conformal-realisation unification is arithmetic/bookkeeping (Gauss-Bonnet χ=2, h(A3)=4, rank/cohomology counts), Python-only; the v180/v181 Möbius reductions (uniformisation + Kerékjártó + finite-order Möbius / equivariant uniformisation) are symbolic + cited-theorem, Python-only; the v182 reviewer-residual map is reduction bookkeeping + arithmetic, Python-only; the v184–v188 F_transfer-firewall round (η_B honest test, axion relic estimate, ledger/prose guards) is numerical/bookkeeping, Python-only; the v192 energy-conserving-clock reformulation is a [O] structural restatement of the bedrock, Python-only; the v193 QGEO.ENERGY.02 energy-commutator contract is a [O] proof target whose sub-claims are structural/logical (Python-only) while its exact q(A3) EH-rigidity rider IS mirrored above); and the 2026-06-16 structural-finds round is mirrored exactly: McKay bedrock `v219` (the 2I irrep degrees `{1,2,2,3,3,4,4,5,6}` = the affine E₈ Kac marks via `A·marks=2 marks`, sums `30=h(E₈)` and `120=|R⁺(E₈)|`), CM-norm duality `v222` (`41=N_ℤ[i](5,4)`, `7=N_ℤ[ω](3,2)`, `13=N_ℤ[i](3,2)`), Coxeter totative clock `v223` (`(ℤ/30)ˣ`=E₈ exponents, `7` order 4), the `248=120+128` channel split `v227`, the Riemann-Roch index gate `v228` (degree-4 divisor ⟹ `(5,3)`, `Λ^even(C⁵)=16`), the lepton étale Frobenius algebra `v229` (ring closure + `Discriminant(m)≠0` + `C₆` charpoly `t⁶−1`), the center budget `v230` (`(7,11,13)` = hex/Fock/square norms), the diamond F_transfer path `v224` (sheet axis `4t²+14t+14` vs flat winding `6s+8`, Plücker steps `(1,8,10),(1,8,16)`), and the dual normal frame `v225` (`d=−½(1,1,−2)`, `n·R=(8,0,0)`, `det(1,d,n)=21`) — while the CP hexagonal modulus `v220` (Klein-J modular values) and the seam recoverability code `v221` (numerical contraction bound) stay Python-only; and the 2026-06-17 CP-reduction `v231` (both CP phases are `mu6` powers of one hexagonal unit `rho=e^{i pi/3}`: `delta_CKM,lead=arg(rho)=pi/3`, `delta_PMNS=arg(rho^4)=4pi/3`, `rho^4=-rho` so they differ by the `Z2` sheet `rho^3=-1`; `C6` charpoly `t^6-1`; sheet-flipped frame orientations `+/-21 sin(pi/3)`) is mirrored exactly; and the E8 Kleinian-seam model `v232` (finite E8 = affine E8 minus the trivial node = the 8 exceptional `P^1`'s of the resolution of `C^2/2I`, negated intersection form = E8 Cartan `det=1`, link = Poincare homology sphere `S^3/2I`, `pi1=2I` order `120`) is mirrored exactly; and the 2026-06-17 closing-shape round: `v233` (CP = the universal family/triality phase, `mu6=mu3 x mu2`, `rho=omega^2*(-1)`, quark/lepton share the triality class and differ only by the sheet) and `v234` (the Seam-Holomorphy selection: `#mark-1 = |Gamma^ab| = |H1(link)|` is `1` only for E8, so holomorphy = homology-sphere = one-1-dim-irrep is one E8-selector; holomorphic `c=8=g_car+N_fam` => unique even unimodular rank-8 = E8) and `v235` (the Chern-Simons realisation: a free gapped bosonic bulk = an even K-matrix, `#anyons=|det K|`, `c=signature`, holomorphic `<=> det 1`; the v92 tower `D5(+)A3`(det 16)`->D8`(det 4)`->E8`(det 1) is the anyon-condensation tower = the Kitaev E8 state) are mirrored exactly; and the 2026-06-17 capstone round: `v236` (the (2,3,5) Brieskorn singularity generates the skeleton — Milnor number `(2-1)(3-1)(5-1)=8`, monodromy eigenvalues = the E8 exponents/30 = the order-30 Coxeter cycle `Phi_30`, both clocks `mu3` in `<h>=Z/30` and `mu4` in the Galois `(Z/30)^x`) and `v237` (the closing step as physics — genus-g degeneracy `|det K|^g`, no topological degeneracy `<=> det K=1 <=>` the seam is SRE = the Kitaev E8 phase) are mirrored exactly; and the 2026-06-17 closure round `v259` (PS.SPECACT.02: the seam KMS cutoff `f(u)=e^{-u}` gives `f_2/f_0=f_4/f_2=1` exactly, vs a Gaussian control `sqrt(pi)/2`, so `kappa=sqrt(c_PS/c_grav)` loses its scheme factor) and `v260` (ARCH.K3.01: one Kummer/K3 carries seam + carrier-16 + E8 — E8 Cartan `det 1`/even/pos-def, K3 lattice `U^3(+)E8(-1)^2` rank 22/`det -1`/even/signature (3,19), 16 nodes `=|A[2]|=2^4=dim S+`, 4 marks) are mirrored exactly, while `v258` (PS.DIRAC.03, the Dirac-as-covariance-induction `log((1-C)C^-1)=H` matrix-log identity) and `v261` (QFT.MSC.01, the Modular-Spectral-Closure assembly/reduction certificate, whose exact sub-facts are already mirrored via v259/v260/v89/v197) are Python-only by the suite convention (like the rest of the v238–v257 NCG round and the v176 assembly certificate); and the 2026-06-18 frontier-closure round `v262`–`v266` (alpha_s RG, the D_F seesaw, the DtN FFT, the fork freeze + text guard, the proton-decay RG) is numerical/text → Python-only, while `v267` (QGEO.SYM.02: the rigidity / minimal-axiom form — cross-ratio 2 of the order-4 orbit, `j=1728 ⟺ λ∈{-1,1/2,2}`, hexagonal `j=0`) is exact and mirrored (its DtN/FFT part stays Python-only); and `v268` (FLAV.TH13.01: the theta_13 exponent `5/6 = tr_E Y^2`, the carrier hypercharge trace) is exact and mirrored; and the 2026-06-18 4D-QFT round `v269` (QFT4D.SPERT.01, the S_pert pAQFT existence skeleton) + `v270` (FLAV.PMNS.03, the PMNS Jarlskog CP strength, numerical) are Python-only, while `v271` (QFT4D.SPERT.02: the concrete Epstein-Glaser one-loop quartic — the bubble scaling degree `sd=4=d ⟹ ω=0 ⟹` exactly one logarithmic counterterm, the loop factor `Ω₃/(2(2π)⁴)=1/(16π²)`, the φ⁴ one-loop `β=3λ²/(16π²)`) is exact and mirrored; and `v273` (QFT4D.SPERT.03: the EG one-loop gauge self-energy → the SM beta coefficients from the carrier/SM content, `b3=-7`, `b2=-19/6`, `b1=41/10`) is exact and mirrored, while the 2026-06-18 scale round `v272` (ν-scale, numerical), `v274` (over-determination, numerical) and `v275` (QG.AMB.01 roadmap) are Python-only; and `v277` (QGAMB.TIERB.01: the seam-Calderón → (E8)₁ matching certificate — the discriminator det Cartan(E8)=1 vs det Cartan(D8=SO(16))=4, and the (E8)₁ character `1+248q+…` with 248=dim E8 currents) is exact and mirrored, and `v278` (QFT4D.SPERT.04: the one-loop optical theorem — the bubble discontinuity `(x₊−x₋)²=1−4m²/s`, the two-body phase space) is exact and mirrored, and the 2026-06-18 self-investigation round `v281` (QGAMB.MODULAR.01: #anyons=|det Gram| tower 16→4→1 + Gauss-Milgram c=8) and `v282` (QGAMB.UNIFY.01: the E8-at-τ=i unification, j=1728 and χ_E8(i)=1728^{1/3}=12) are exact and mirrored, while `v276` (flat-pillowcase commutator), `v280` (pillowcase DtN) and `v283` (kill-test scorecard) are numerical Python-only. It is kept **separate** from `tfpt_readouts.wl` so the
   verified 116/116 base file is untouched.

**Status: verified.** First engine run 2026-06-11 (Wolfram Engine 14.3): the
v84–v93 block passed **45/45** on first run; the v94–v140 blocks were added
the same day, the v141–v144 block on 2026-06-12. Current state:

```
--- Wolfram extension v84-v237 + v259-v260 + v267-v268 + v271 + v273 + v277 + v278 + v281 + v282 + v313-v320 + v325 + v327 + v337 + v341 + v342 + v344 + v345 + v347 + v348 + v349 + v350 + v351 + v352 + v354 + v355 + v358 + v359 + v410-v419 + v422 + v429 + v430 + v431 + v437 + v445 + v450-v454 + v456 + v457 + v459 + v461 + v462 + v463: 365 passed, 0 failed ---
ALL WOLFRAM EXTENSION CHECKS PASSED
```

The 2026-06-30 G-block round (the post-F "next options", `v454`–`v459`) adds 6
exact mirrors: `v454` (the level-1 Sugawara central charge `c = dim G/(1+h^v) = 8`
for **both** `SO(16)_1` `120/15` and `(E8)_1` `248/31`; the Casimir and Kac–Moody
`<J_n J_-n>=n` fits are Python-only), `v456` (S3 from P1 — `c3`'s `8` is the
one-sided count `|Z2|·(∮K/π)=2·4`, and a reflection sends the Chern integer
`C → −C`, so a two-sided boundary forces `C = 0`; the Chern computation is
Python-only), `v457` (the `(E8)_1` character tower `{1,248,4124,34752}` from
`E4/η^8`, and the kill-test discriminators `248 = 120 + 128`, `|det Cartan E8| = 1`
vs `|det Cartan D8| = 4`), and `v459` (E8 even unimodular, the 240 roots split
`112 + 128`, and `248 = 8 + 240 = 120 + 128` — the lattice-VOA route supplying the
128-spinor extension MMST leaves open). `v455` (uniform Tomita–Takesaki tower) and
`v458` (the MMST citation audit) are Python-only/structural.

The 2026-06-30 `v461`/`v462` round adds 3 more exact mirrors (total `363/363`):
`v461` (the Kapustin–Fidkowski strict-locality obstruction as integer logic — the
Wilson-loop/Wannier winding `= |C| = 1 ≠ 0` and `c_- = 8 ≠ 0`, and a strict
finite-range commuting projector would force winding `0 ⟹ C = −C ⟹ C = 0`, so it is
forbidden; the Wilson-loop winding/Chern themselves are numerical, Python-only), and
`v462` (the 128-spinor extension at character level — the Jacobi/E8 theta identity
`θ₂⁸+θ₃⁸+θ₄⁸ = 2E₄` so `χ_{(E8)₁} = E4/η⁸ = χ_o^{SO16} + χ_s^{SO16}`, and the
`(E8)_1` weight-1 `248 = 120 + 128` with the finite 16-Majorana Fock counts
`C(16,2)=120`, `2^{16/2}=256=128+128`; the finite-`L`→continuum convergence is
Python-only).

The 2026-06-30 `v463`/`v464` round adds 2 more exact mirrors (total `365/365`):
`v463` (the `c=8` holomorphic-uniqueness pin — `c=8` has **three** level-1
candidates `A8` (dim 80), `D8=SO(16)` (dim 120), `E8` (dim 248), all
`dim = 8·(1+h^v)`, so `c=8` is necessary but **not** sufficient; holomorphy forces
`dim V_1 = E4/η^8` `q^1` coeff `= 248 = dim E8`, excluding the gleich-`c` rivals
`A8`/`D8`; the tower `{1,248,4124,34752,213126}` are the `E4/η^8` coefficients).
`v464` (the one-particle realization rigidity — symbol idempotency, Cauchy kernel
convergence, entanglement `c`-fit) is numerical, Python-only.

(ledger `GATE.WOLFRAM.02`). The scipy-only parts of the round (the `v86`
pivot ODE solve, the `v88` data pulls, the `v99` mpmath ODE probe of the
time-1 map — its exact symbolic form *is* mirrored) stay Python-only and
are flagged as such in the `.wl` comments. The statistical numerology null
test `v100_numerology_null_mc.py` (grammar census + Monte-Carlo + RNG
controls) is likewise Python-only by the suite's convention (like
`v62`/`v64`/`v65`) and flagged in the `.wl` comment. The 2026-06-21
adversarial-review follow-ups — `v305_witness_independence.py` (the structural
generator-economy firewall), `v306_seed_crossval.py` (the leave-one-out seed
cross-validation) and `v307_data_watchdog.py` (the decision pipeline over the
frozen registry) — are structural/statistical/data-confrontation modules and
are therefore Python-only by the same convention (no exact algebraic result is
added, so the Wolfram exact-check count is unchanged). The 2026-07-01 cross-sector
seed slice `v465_seed_crosssector_joint.py` (the θ13-independent β + λ_C
back-solve, a subset of `v306`) is likewise a statistical consistency module,
Python-only (no exact algebraic result added; the Wolfram exact-check count stays
unchanged). The 2026-07-01 sixth-channel `v466_seed_leptonmass_channel.py` (the
charged-lepton mass ratio `m_e/m_μ = (12/7) φ0²` back-solving the same seed to
−0.11%, a new measurement sector extending the `v306`/`v465` over-determination) is
the same kind of statistical consistency module, Python-only (no exact algebraic
result added; the Wolfram exact-check count stays unchanged).

The 2026-06-22 **cyclotomic/Galois arithmetic arc** added ten exact checks
(275 → 285): `v313_golden_atoms_spectral.py` (the affine-E8 charpoly factors
`x(x²−4)(x²−1)(x²−x−1)(x²+x−1)` with the golden minimal polynomial `x²−x−1`,
the `(2,3,5)` atoms as the spectral angles `2cos(π/k)`, and the `31/30`
icosahedral selection), `v314_rate_translation.py` (the rational kernel vs the
`Q(√5)` dynamic-rate split, translation acting only on `Q`), `v315_coxeter_coupling.py`
(`30=5·6`, `φ(30)=8=rank E8`, the Galois group `μ4×Z2`, and `√5` as the
quadratic Gauss sum in `Q(ζ₅)`), `v316_galois_readout.py` (`ρ=ζ₆=ζ₃₀⁵`,
`ρ⁴=−ρ`, and `Gal(Q(ζ₆)/Q)=Z2` as CP conjugation), `v317_galois_family.py`
(`N_fam=3` as the `μ3` orbit with the Galois-refined `1+2` split),
`v318_arithmetic_capstone.py` (`φ₀=(4/3)c₃+48c₃⁴` as a pure function of `π`) and
`v320_galois_cp_relation.py` (the CP lock `δ_PMNS=4π/3=δ_CKM,lead+π=240°`). The
translation clock `v319_translation_clock.py` is a structural reading and stays
Python-only.

The 2026-06-22 **next-steps round** added three more exact checks (285 → 288):
`v325_pillowcase_keystone.py` (the keystone orbifold `S²(2,2,2,2)` has
`χ_orb = 2 − 4(1−1/2) = 0`, i.e. flat at `τ=i`; the other keystone pieces —
`marks=4`, `j=1728`, `det Cartan(E₈)=1` — were already mirrored via v216/v214/v277)
and `v327_hypergraph_rewrite.py` (the minimal branching rule `M` has spectrum
`{0,2/3,1}`, the survival `2/3=(N_fam−1)/N_fam` with `(2/3)^6=64/729`, and the proof
that `2/3` is **not** a root of the affine-E₈ characteristic polynomial). The
`F_transfer` solver suite `v326_ftransfer_suite.py` (numerical ODE/RG relaxations) and
the `θ13` pressure-point `v328_theta13_pressure.py` (data confrontation) are Python-only.

The 2026-06-22 **α-Quillen round** added one more exact check (289 → 290):
`v341_alpha_quillen.py` (the `F_U(1)` seam-form discriminant identities — `φ_base=(4/3)c₃` so
`c₃/φ_base=3/4=q(A3)`, `−5/4=−q(D5)`, `q(D5)+q(A3)=2`, and the counterterm `(4/5)M=8b₁`).
The Quillen-form split at the root is the numerical α solve (Python-only, v3).

The 2026-06-22 **EM-Ward heat-kernel round** added one more exact check (290 → 291):
`v342_em_ward_heatkernel.py` (the heat-kernel origin — `c₃=1/(|Z₂|∮K)=1/(8π)` Gauss–Bonnet,
the Gilkey `a₄` gauge-curvature coefficient `30Ω²/360=1/12`, the `c₃`-ladder `{0,3,6}`, and
`2c₃³=1/(256π³)` carrying `π³` = three boundary insertions). The textbook Gilkey coefficient
is cited, not re-derived; the cubic Maxwell moment stays the `EM.WARD.01` residual.

The 2026-06-22 **det K=1 synthesis round** added one more exact check (291 → 292):
`v344_detk_synthesis.py` (the ADE `|det Cartan| = |H₁(link)| = #(1-dim irreps)` sequence
`A_n→n+1, D_n→4, E6→3, E7→2, E8→1` — only `E8→1`, the binary icosahedral `2I` being the
unique perfect ADE group). The four-routes analysis `v343_four_routes_analysis.py` is a
Python-only roadmap (its de Sitter / gap facts are already mirrored via v54/v337).

The 2026-06-22 **R3 execution round** added one more exact check (292 → 293):
`v345_hypergraph_homotopy.py` (the plumbing link `H₁ = coker(Cartan)` via the Smith normal
form — `|coker(E8)| = 1` so the E8 plumbing boundary is an integral homology sphere, vs
`|coker(D5)| = 4`; only E8). The companion perfectness of `2I = SL(2,5)` (the link's `π₁`)
is a direct finite-group commutator computation, Python-only.

The 2026-06-22 **L2 closure-modes round** added one more exact check (293 → 294):
`v347_seam_closure_modes.py` (the precise locus of the one open arrow — the seam pillowcase
base `S²(2,2,2,2)` has `χ_orb = 0` (Euclidean/flat) while the 2I/E8 Seifert base `S²(2,3,5)`
has `χ_orb = 1/30` (spherical), so L2 bridges two geometric types). The geometric-bridge
capstone `v346_seam_geometric_bridge.py` is a Python-only chain-bookkeeping roadmap (its
arithmetic is already mirrored via v344/v345).

The 2026-06-22 **Route B (rigidity) round** added one more exact check (294 → 295):
`v348_seam_rigidity_route.py` (the crystallographic restriction `{1,2,3,4,6}` — the 5-fold
absent — so `φ = 2cos(π/5)` is what extends the crystallographic `μ4` to the non-crystallographic
icosahedral `2I`, and `E8 = the icosian ring` (Conway–Sloane, rank 8) makes `2I→E8` a lattice
identity; the keystone reduces to "does the raw seam carry `φ`?").

The 2026-06-22 **golden-ratio test round** added one more exact check (295 → 296):
`v349_raw_seam_golden_test.py` (the honest negative — the raw carrier is NOT golden: `D5`
(`h=8`) gives `2cos(2π/8)=√2`, `A3` (`h=4`) gives `0`; golden needs `5|h`, which holds only on
the output side `{SU(5) h=5, H3 h=10, E8 h=30}`. So `φ` is the icosahedral *input*, not a hidden
raw feature; `L2` reduces to "is `g_car=5` a pentagon or a count?").

The 2026-06-22 **bootstrap-correction round** added one more exact check (296 → 297):
`v350_bootstrap_inputs_correction.py` (the correction of v349 — `g_car=5` is the bootstrap
fixed point, the largest prime of `h(E8)=30`, and `FactorInteger[30]={2,3,5}` ARE the
icosahedral axes; the golden ratio is EMERGENT from the `μ4`-glue `D5⊕A3→E8` (`h=30`, golden),
not external. So the inputs are over-determined fixed points, not free axioms, and the
residual is the physical continuum realisation, not the golden ratio).

The 2026-06-22 **continuum + framework round** added two more exact checks (297 → 299):
`v351_continuum_realisation_sharpened.py` (the `c=8` which-net ambiguity `E8` (det 1) vs
`SO(16)=D8` (det 4) is resolved by the seam's order-4 `μ4` clock — index-4 → `E8`, index-2 →
`SO(16)` — with the bootstrap agreeing `h(E8)=30` (max prime 5) vs `h(D8)=14` (max prime 7)),
and `v352_framework_irreducible.py` (both axioms bootstrap-forced — the `8` over-determined
`rank E8 = h(D5) = φ(30) = 8`, `g_car=5` the Coxeter-match — so the only irreducibles are the
framework + `π`). (`v353_selfloop_capstone.py`, the self-consistent-loop rethink, is Python-only.)

The 2026-06-22 **reverse-audit round** added two more exact checks (299 → 301):
`v354_e8_reverse_audit.py` (the reverse numerology audit — of E8's 8 Casimir degrees
`{2,8,12,14,18,20,24,30}` exactly 3 feed a primary readout (`2,8,30`) and 5 are hull overhead
(`{12,14,18,20,24}`); the golden ratio is in the unmapped structure, so it is not numerology),
and `v355_e8_unmapped_bandwidth.py` (the disciplined bandwidth search — the unmapped region's
forced content is *collective*: `sum(degrees)=128=dim S⁺`, `product(degrees)=|W(E8)|`,
`exponents = totatives of 30`; the per-degree atom matches are unforced and declined, so the
search finds no new physical hit — reconciling `v66` and `v354`).

The 2026-06-23 **entanglement-gravity round** added two exact checks (301 → 303):
`v358_grav_entropy_equilibrium.py` (the entanglement first law `δS=δ⟨K⟩` with TFPT's atoms gives
the *linearised* Einstein equation parameter-free — `1/c3 = 8π`; the thermodynamic (`2π/η`) and
geometric (`|Z2|·2π·χ`) origins of `c3` coincide via `|μ4|=|Z2|·χ=4`; the CHM 3-ball weight
integral `∫w d³x = 4π R⁴/15` assembles the matter boost flux J3), and
`v359_grav_nonlinear_einstein.py` (the *full* covariant `G_ab + Λ g_ab = (1/c3) T_ab` via the
fixed-volume equilibrium — the Einstein tensor `g^{ab}G_ab = (1−d/2)R = −R` in d=4, both
coefficients parameter-free: `8π = 1/c3` and the `Λ` prefactor `(8π)²·48c3⁴ = 3/(4π²)`).

The 2026-06-24 **sheet-generator round** added five exact checks (303 → 308):
`v410_sheet_generator_binary.py` (the sheet axis `V = Q diag(0,1,1)` is a binary internal
compiler — `V^n = {{0,2^(n-1),0},{0,2^n,0},{0,2^(n+1)-2,1}}` so `V^n·1 = (2^(n-1),2^n,2^(n+1)-1)`,
the bilinears `1ᵀV^n1 = 7·2^(n-1)-1`, `1ᵀV^na = 7·2^(n-1)`, `aᵀV^na = 11·2^(n-1)`,
`aᵀV^n1 = 11·2^(n-1)-2`, and the theta cross-link `σ₃(2)=9=aᵀV1`, `σ₃(3)=28=1ᵀV³a=det(I+R)`,
`σ₃(5)=126`), `v411_ud_ratio_vpower.py` (`c_u/c_d = (1ᵀV⁴1)/((aᵀV1)(1ᵀV²1)) = 55/117`, a
re-encoding of `5·11/(9·13)`), `v412_sheet_source_corner_J.py` (the Z₂-wall corner
`J = M(1,-2) = C-2V` with `χ_J = λ³-6λ²+3λ-2`, `aᵀJa=30=h(E₈)`, `det(I+J)=12`, `det(2I+J)=40`),
`v413_sheet_characteristic_calculus.py` (`e₁=3t+12`, `e₂=2t²+15t+25`, `e₃=4t²+14t+14` ⟹
`Δe₁=3`, `Δ²e₂=4`, `Δ²e₃=8`, and the anchor energy `aᵀM_t a = 52+11t`) and
`v414_center_resolvent_portal.py` (the resolvent ladder `det(C)=14`, `det(I+C)=52`,
`det(2I+C)=120` = `G₂ → F₄ → E₈⁺`). The binary-spine / Lie-dimension readings stay `[C]`,
audit-typed.

The 2026-06-25 **Gaussian-operator / atom-trichotomy round** added seven exact
checks (308 → 315): `v415_gaussian_operator.py` (the square CM-norm dictionary of
`v222`/`v230` lifted from numbers to OPERATORS via `J = [U,V]/3`, the integer `μ₄`
quarter-turn born from the commutator of the binary `V` and ternary `U` compilers —
`J² = -I` on the rank-2 image, the Gaussian integers `3+2i`/`5+4i` are eigenvalues of
`3I+2J`/`5I+4J` with norms `13=Δ_Q`/`41=10b₁`, `(aI+bJ)(aI-bJ)` reads `(a²+b²)` on the
`μ₄`-plane and the real part² on the kernel, and the intrinsic order-4 deck
`D=-I+J-J²` with `χ₂`-line `ker[U,V]=a-1`) and `v416_atom_trichotomy.py` (the atoms
`{2,3,5}` are ramified/inert/split in `ℤ[i]` vs `ℤ[ω]`, the ramified prime of each ring
is its own atom, and each atom is the unique ramified prime of one quadratic facet of
`K=ℚ(i,√-3,√5)`, product `2·3·5=30=h(E₈)`). This round also corrected a one-character
sign bug in the pre-existing `v412` `CharacteristicPolynomial` check (Wolfram returns
`-(χ)` for odd rank `n=3`), so the extension now runs genuinely clean at `315/315`.

The 2026-06-25 **Eisenstein/CP-operator round** added three exact checks (315 → 318):
`v417_eisenstein_cp_operator.py` — the hexagonal dual of `v415`. The family rotation
`P=(1 2 3)` is the order-3 Eisenstein deck (`P²+P+I=ONES`) and realises the hex CM norm
`7=N_ℤ[ω](3+2ω)` as `(3I+2P)(3I+2P²)=7I+6·ONES` with `Spec {7,7,25}` (the dual of `v415`'s
`{13,13,9}`); the CP clock `W=-P²` (order 6, `W²=P`, `W³=-I`, `Spec {-1,ζ₆,ζ₆⁻¹}`) gives the
two CP phases `δ_CKM=arg ζ₆=π/3` and `δ_PMNS=arg ζ₆⁴=4π/3`; and all flavor-side clocks are
powers of `ζ₃₀` (`ζ₃₀¹⁵=-1`, `ζ₃₀¹⁰=ω`, `ζ₃₀⁶=ζ₅`, `ζ₃₀⁵=ζ₆`) while the seam `μ₄=i` is the
Galois side `(ℤ/30)^×` of order `φ(30)=8=rank E₈` — so `ℚ(ζ₃₀)` carries both `E₈` invariants
(`h=30` and `rank=8`).

The 2026-06-25 **cyclotomic-norm-triple round** added three exact checks (318 → 321):
`v418_cyclotomic_norm_triple.py` — it finds the missing carrier-5 clock of `v417` as the `4×4`
`Φ₅`-companion `C₅` (`C₅⁵=I`, golden ratio in its `2cos` values), shows the carrier norm
`N_ℤ[ζ₅](3+2ζ₅)=det(3I+2C₅)=55=5·11=` the quark numerator, and assembles the norm triple
`det(3I+2·Comp(Φ_{3,4,5}))=(7,13,55)=`(scalaron, `Δ_Q`, quark numerator) over the three atom-rings
`ℤ[ω],ℤ[i],ℤ[ζ₅]` (atoms `3,2,5`). Negative control: the anchor `(5,4)→(21,41,461)` reaches named
values only in the `ω`- and `i`-rings (`21=N_ω(5,4)`, `41=10b₁`, `v222`) but `461` (prime) in the
carrier ring, so the carrier ring separates `(3,2)→55` from `(5,4)→461`; and honestly the scan shows
`(3,2)` is the **forced** carrier split (`v14`), not the unique clean one (`(2,1)→(3,5,11)` is a
secondary rung).

The 2026-06-25 **seam-Galois round** added three exact checks (321 → 324):
`v419_seam_galois_carrier.py` — a positive resolution of the `v409`/`RES.COXETER.SYMMETRY.01` cyclic/Galois
asymmetry. Because `h(E₈)=30` is squarefree the cyclic clock `ℤ/30` has **no order-4 element**, so the seam
`μ₄` is forced onto the Galois side `(ℤ/30)^× = (ℤ/2)^××(ℤ/3)^××(ℤ/5)^× = μ₄×ℤ₂` (order `φ(30)=8=rank E₈`);
the `μ₄` (`ℤ/4`) factor **is** `(ℤ/5)^×` — the carrier prime 5 — so the seam `μ₄ = Gal(ℚ(ζ₅))`, realised on
the carrier clock `C₅` by the explicit Frobenius operator `G` with `G C₅ G⁻¹ = C₅²`, `G⁴=I`. So the square
seam (atom 2) is the carrier pentagon's (atom 5) Galois group, and `ℚ(ζ₃₀)` carries both `E₈` invariants.
Figure `coxeter_galois.pdf`.

The 2026-06-25 **Galois↔Net bridge round** added three exact checks (324 → 327):
`v422_galois_net_bridge.py` — the seam `μ₄ = Gal(ℚ(ζ₅))` is the **same cyclic `ℤ/4`** as the `(E₈)₁`
simple-current glue, not a mere order-4 coincidence. `disc(A₃)=disc(D₅)=ℤ/4` (one Smith invariant factor 4
= cyclic; `D_n` disc is `ℤ/4` for `n` odd, `ℤ₂×ℤ₂` for `n` even, so the carrier `D₅` (rank 5, odd) is cyclic
while `D₈` (rank 8, even) is Klein); `(ℤ/5)^×=⟨2⟩` is cyclic order 4 (only the carrier prime 5 gives order
4); the glue `⟨(1,1)⟩` in `ℤ₄×ℤ₄` (16=dim S⁺) is order 4 with Lagrangian quotient `16/4²=1=(E₈)₁`. Negative
control: the Klein/order-2 `⟨(2,2)⟩` gives `16/2²=4=disc(D₈)=SO(16)` (det 4), **not** `E₈` (det 1) — so the
cyclic `ℤ/4` (forced by 5) selects `E₈`, bridging the Galois gearbox (v419) to `G_net`/`SEAM.EQUIV.01`.

The 2026-06-26 **pentagon/golden round** added three exact checks (327 → 330):
`v429_axion_pentagon_phi.py` — the otherwise-"unmapped" icosahedral/golden `E₈` structure (`v354`/`v313`)
surfaces in the **one external cosmological input** `θ_i`. Because `N_fam=g_car−2`, the axion spine angle
`θ_i = π N_fam/g_car = (g_car−2)π/g_car` is **exactly the interior angle of the regular `g_car`-gon** — for
`g_car=5` the pentagon, `θ_i=3π/5=108°`; its cosine is golden `cos(3π/5)=(1−√5)/4=−1/(2φ)` (partner
`2cos(2π/5)=1/φ`, `φ=2cos(π/5)`); and the golden character is **unique to `g_car=5`** (among small `n`-gons
only `n=5` has an irrational interior-angle cosine; `n=3,4,6` give `1/2,0,−1/2`). A `[C]` re-reading that
refines `v354` ("`φ` in no readout" → "`φ` touches only the `[C]` spine angle") and gives a geometric motive
for the spine branch over the hilltop `~170°`; it does **not** upgrade `DM.AXION.SPINE.01` (stays `[C]`).

The 2026-06-27 **other-side audit round** added three exact checks (330 → 333):
`v430_other_side_reverse_audit.py` — the sheet/deck complement of the reverse audit (`v354`/`v355`). The
double cover's "other side" (the one-sided `ℤ₂` collar / conjugate half-spinor `S⁻`) is **forced-disjoint**
from `E₈`'s five unmapped Casimir degrees `{12,14,18,20,24}`: the deck is the matched degree-2 invariant
(`|ℤ₂|=2=Min(deg)`, the metric, one of the matched `{2,8,30}`); the two sheets are the `128`-spinor
(`128=8·16=2^(rank−1)=Total[deg]`, the spinor half of `248=120+128`, `S⁻` the conjugate `(16̄,4̄)`,
`128=2·64`); and the sheet/deck set `{2,16,32,128}` meets `{12,14,18,20,24}` in `∅` (only degree contact the
matched `2`). A clean structural negative consolidating the `S⁻`-dark-matter downgrade (`v227`) and the WIMP
no-go; no status change.

The 2026-06-27 **degree-ladder round** added six exact checks (333 → 339):
`v431_e8_degree_ladder.py` — the structural complement of the reverse audit (`v354`/`v355`/`v430`). `E₈`'s
five "unmapped" Casimir degrees are **not** diffuse overhead but the forced two-family decomposition
`deg(E₈) = 6·spine{2,3,4,5} ⊔ ({2}∪det-ladder{8,14,20})`: the exponents are the `φ(30)=8` totatives of
`h=30=2·3·5`, so the degrees occupy only the residue classes `{0,2} mod 6`; the `6k` family `/6` is the
`v91` spine `{2,3,4,5}`, the `6k+2` family `{8,14,20}=(det R,det C,det L)` is the winding line `6s+8`
(`v135`); `18=6·N_fam` is spine-family, not a holdout; the clean split is special to `E₈` (`E₆/E₇/D₅` fail).
The arithmetic decomposition is exact `[E]/[I]`; the **functorial** flavour identification stays `[P]`
(`12,24` admit two readings each) — a structure theorem, not a forced flavour map; no status change.

The 2026-06-29 **degree-joint round** added three exact checks (339 → 342):
`v437_e8_degree_joint.py` — a consolidation of `v6`/`v66`/`v355`/`v431` that derives more from the `E₈`
Casimir degrees without crossing the `v354`/`v355` anti-numerology line. All of `E₈`'s combinatorics is fixed
by its degree multiset alone (`rank=8`, `h=30`, `120/240` roots, `dim=248`, `|W|=696729600`, `Σdeg=128`); and
the two TFPT structural integers `(g_car,N_fam)=(5,3)` are the **unique** root pair of
`x²−(rank E₈)x+(h/2) = x²−8x+15 = (x−3)(x−5)` (sum of roots `=rank E₈=8`, product `=h/2=15=g_car·N_fam`), so
both are forced together by two degree-invariants; the three mapped degrees `{2,8,30}=min/rank/max`. No new
per-degree mining; no status change.

The 2026-06-30 **rigidity-forcing round** added three exact checks (342 → 345):
`v445_seam_rigidity_forcing.py` — the converse of `v442`, upgrading rigidity from "block-diagonal PERMITS
commuting" to "commuting with the order-4 clock FORCES block-diagonal". (i) the ENTRYWISE forcing
`[ρ,E_{ab}]=(iᵃ−iᵇ)E_{ab}=0 ⟺ a≡b (mod 4)`, verified for all `a,b∈0..31` (residue-only ⇒ uniform in `N`, the
v442 uniformity); (ii) the exact commutant dimension `Σ nₛ² = 4·4² = 64` is a PROPER subspace of `N²=256`
(`N=16`); (iii) THE ORDER IS THE DISCRIMINATOR — the order-2 commutant (`128`) is strictly larger than the
order-4 (`64`), swept `N=4..64`, so the four marks `|μ₄|=4=h(A₃)` force strictly more structure than two (only
index-4 is `(E₈)₁`, det 1 vs `SO(16)` det 4, already mirrored via v281/v344). Also Lean-kernel-hardened
(`SeamRigidityForcing.lean`, `FORM.SEAM.RIGIDITY.FORCING.01`). The clock-invariance derivation `v446`, the
topological edge `v447` and the four-point `v448` are numerical (numpy BdG / OS reconstruction) and stay
Python-only by the suite convention.

The 2026-06-30 **edge-CFT / modular round** added nine exact checks (345 → 354):
`v452_seam_e8_modular.py` — the `(E₈)₁` torus modular data (4 checks): (i) S-invariance
`χ(−1/τ)=χ(τ)` for `χ=E₄/η⁸` (weight 0 ⇒ one primary, `S=[1]`); (ii) T-phase
`χ(τ+1)/χ(τ)=e^{−2πi/3}=e^{−2πi c/24}` (`c=8`); (iii) leading power `χ·q^{1/3}→1` ⇒
`q^{−c/24}=q^{−1/3}` ⇒ `c=8=g_car+N_fam`; (iv) holomorphic `c=8≡0 (mod 8)` and T-phase order
`24/gcd(8,24)=3`. (`E₄` is evaluated via its `q`-series `1+240·Σσ₃(n)qⁿ` because Wolfram's
`EisensteinE` stays symbolic for complex `τ`.) `v450_seam_edge_entanglement.py` — the
Calabrese-Cardy reading `c per Majorana = 1/2`, `N_Maj=2^{g_car−1}=16`, `c₋=16·½=8`.
`v451_seam_edge_cardy_tower.py` — the edge is the Ising minimal model `M(3,4)`:
`c=1−6(p−q)²/(pq)=1/2`, Kac weights `h_{2,2}=1/16` (σ) and `h_{1,3}=1/2` (ε), so
`{c,h_σ,h_ε}={½,1/16,½}` uniquely names the free-Majorana CFT. `v453_seam_mu4_from_marks.py`
— the four Gauss-Bonnet marks ARE `μ₄` (roots of `z⁴−1`), the form basis `ω_k` is `μ₄`-graded
(`→iᵏω_k`) and the cross-ratio `λ=2` is preserved by `z→iz`, so `QGEO.SYM.01` follows from
`marks=μ₄` + the existing `QGEO.REALIZE.01`. Also Lean-kernel-hardened (`SeamEdgeChern.lean`,
`FORM.SEAM.EDGE.CHERN.01`). The numerical edge readings `v449` (uniform-in-N) and `v447`
(topological Chern) stay Python-only (numpy BdG / FHS lattice).

The 2026-06-22 **next-steps round (A/C/D/B)** added one more exact check (288 → 289):
`v337_decoupling_theorem.py` (the ambient back-reaction scale `2·dim(E₈)·c₃² = 31/(4π²)`
exactly, so the decoupling margin `6 ln(3/2) − 31/(4π²) > 0` with finite susceptibility
`χ = 1/(1−(2/3)⁶) = 729/665`). The keystone-unification `v335_seam_equiv_unify.py`
(reduction/inventory; its arithmetic `c=8`, `det E₈=1` is already mirrored), the
continuum-limit literature map `v336_continuum_limit.py` (the `c=8`/`det` facts are already
mirrored, the rest is citation mapping) and the `θ13` budget `v338_theta13_budget.py` (data
confrontation) are Python-only. The Lean `D₈`/holomorphy-discriminator hardening
(`CartanDeterminants.lean`) mirrors the already-present Wolfram `det E₈=1` / `det D₈=4`.

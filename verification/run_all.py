"""Run the whole TFPT verification suite and report PASS/FAIL.

    $ cd verification && python run_all.py

Exit code 0 iff every claim in v1..v8 passes.  Each module is also runnable on
its own (e.g. `python v1_e8_glue.py`).
"""
import importlib

MODULES = [
    ("v1_e8_glue", "mu4 glue theorem"),
    ("v2_carrier_pascal", "carrier / Pascal closure"),
    ("v3_em_alpha", "electromagnetic closure (alpha)"),
    ("v4_flavor_matrix", "flavor residue matrix"),
    ("v5_e8_cascade", "E8 cascade spine"),
    ("v6_bootstrap", "self-consistency bootstrap"),
    ("v7_gravity_cosmo", "gravity / cosmology readouts"),
    ("v8_horizon", "horizon thermodynamics"),
    ("v9_neutrino_texture", "neutrino Majorana texture (theta_12)"),
    ("v10_projection_involution", "Q,Sigma projection-involution algebra"),
    ("v11_unique_KQ", "uniqueness of K and Q"),
    ("v12_mass_generation_polynomials", "sector/generation polynomials"),
    ("v13_open_gates", "closing/sharpening the open audit gates"),
    ("v14_carrier_uniqueness", "carrier rank g=5 and 3+2 split forced"),
    ("v15_bootstrap_classification", "D5+A3 unique familyful E8 glue"),
    ("v16_solar_dual_anchor", "solar angle from the dual anchor"),
    ("v17_hexagonal_resolvent", "finite hexagonal resolvent backbone"),
    ("v18_quark_yukawa", "charged-fermion Yukawa sector + quark c-readout"),
    ("v19_monodromy_moduli", "U_f* holonomy reduction: why exact quark c's need (U)"),
    ("v20_lepton_c_derivation", "lepton c's derived: delta=1/2 resolvent + product rule"),
    ("v21_solar_product_quark", "solar coefficient q(A3), product rule, quark scope"),
    ("v22_open_gates_audit", "residual-gates audit contract (A2,B3,B4,B5,B6,C7)"),
    ("v23_anchor_generator", "anchor a=(1,1,2) generates the axioms and E8"),
    ("v24_quark_ratio_closure", "quark ratio closure 55/117, 34/47, 3/26 + c gauge"),
    ("v25_frontier_conjectures", "Koide source->pole + axion f_a (conjectures)"),
    ("v26_flavor_frontier_unification", "the '11' reduces to the single (U) gate"),
    ("v27_wall_representative", "(U)_wall: balanced wall representative + selector"),
    ("v28_gravity_fR", "R+R^2 covariant field equation closed; full measure open"),
    ("v29_research_contract_certs", "U_wall enumeration (5 orbits) + G5 gap-dominance"),
    ("v30_d4_character_variety", "C_U^(2): D4-fixed variety is positive-dimensional"),
    ("v31_R_dictionary", "R(rho) is the non-abelian-Hodge map (case A alive)"),
    ("v32_rh_splitting", "RH route: splitting type made algebraic; product=I wall stays"),
    ("v33_explicit_flat_bundle", "explicit valid (U_wall) flat bundle (RH-solve output, case A)"),
    ("v34_h2_bridge_attempt", "H2 bridge: explicit M_k; honest dictionary gap (no c_u/c_d)"),
    ("v35_quark_qcd_boundary", "the gates are the discrete<->continuous boundary"),
    ("v36_spectral_action_g2", "G2: spectral action -> R+R^2 ; gap-decoupling QG resolution"),
    ("v37_plucker_anchor", "anchor-plane Plücker apparatus + K+xQ pencil + flavor dualities"),
    ("v38_uwall_killswitch", "(U_wall) U2 kill-switch hardened: irreducible across the locus (case A robust)"),
    ("v39_uwall_selectors", "(U_wall) selector side closed on the explicit point: det R=8 + Spec(Q_+) from bundle"),
    ("v40_harmonic_metric", "(U_wall) harmonic metric = finite linear algebra (polystable=unitary, no Hitchin PDE)"),
    ("v41_leg_assignment", "(U_wall) final leg test: holonomy supplies delta=1/2, amplitudes are the resolvent (honest negative on literal reproduction)"),
    ("v42_exterior_leg", "(U_wall) Exterior Leg Lemma: the quark u/d leg is a Lambda^2 F area (Plücker), not a scalar"),
    ("v43_exterior_bridge", "(U_wall) Lambda^2 F bridge: exterior leg = 3-bar conjugate rep; integer Pl(K) is the discrete invariant, not the continuous action"),
    ("v44_carrier_exterior", "(U_wall) exterior leg = carrier Lambda^2 grading (u^c in Lambda^2(5)): Lie-level, no special math"),
    ("v45_family_exterior", "(U_wall) the '11' = exterior algebra of the family fundamental mu4 (Pascal; no special math)"),
    ("v46_grand_mass_volume", "Grand Mass Volume: absolute mass-scaling = det M_SM ~ u^25 = u^{g_car^2} [I] (not a product rule)"),
    ("v47_selection_theorem", "Boundary Carrier Selection Theorem: (D5+A3)+mu4=E8 unique; alternatives excluded"),
    ("v48_em_ward", "EM boundary Ward decomposition: F_U(1) = Maxwell + Calderon + transport; 8b1=(4/5)M, -5/4=q(D5)"),
    ("v49_readout_rigidity", "Readout Rigidity (Thm U2): c_u/c_d constant on the discrete selector stratum; (U_wall) 4-way split"),
    ("v50_q_geometry", "Q geometry (Thm Q): Q_+/Q_- char-polys + unique normal form; D4-equivariant origin [P]"),
    ("v51_boundary_half_step", "glue norms=(g_car,N_fam)/|mu4|; four ops forced: sum=2,diff=1/2=delta,prod=15/16,ratio=5/3"),
    ("v52_pencil_endpoints", "K+xQ pencil endpoints P(-1)=2,P(0)=4,P(1)=20,P(2)=68=2p5; det(K-Q)=2 (audit ext. of v37)"),
    ("v53_compiler_core", "compiler core from (g_car,N_fam)=(5,3): rank E8=8, |Z2|=2; Pythagorean 25=9+16; anchor char-poly unique"),
    ("v54_seam_horizon_keystones", "seam=horizon [I] keystones: 8 triply-forced (2|mu4|=rank E8=h(D5)=phi(30)=8pi grav); one transfer op (2/3)^6 for flavor+horizon"),
    ("v55_coxeter_cycle", "computed E8 Coxeter element order 30=|Z2|*N_fam*g_car, phases=exponents=totatives(30), rank=phi(30)=8; S_dS*rho_L=32pi^4"),
    ("v56_unique_attractor", "gapped boundary transport (gap 6log(3/2)>0) => UNIQUE attractor, rate (2/3)^6; Coxeter in |mu4|=4 planes; entropy reset=rank-1 projector"),
    ("v57_horizon_crosslinks", "horizon cross-links [I]: c3=Jacobson/Einstein 8pi coeff, 1/4=1/|mu4|; Hod QNM omega_R/T_H=ln(3)=ln(N_fam) [P]; P_H denom 1920=|W(D5)|"),
    ("v58_seam_horizon_chain", "seam-horizon chain (precise): c3=1/(8pi) from one-sided S^2 Gauss-Bonnet, KMS=4c3 kappa, S_BH=M^2/2c3, RT in seam units; Seam-Horizon Theorem OPEN [A]"),
    ("v59_area_law_evidence", "area-law necessary condition met: RP Gaussian kernel => area law (gapped EE saturates), same gap as the attractor; c3 coefficient still open [A]"),
    ("v60_lambda_metrology_branch", "Lambda branch selection (2c3/dtop=64pi^3/3=661.5 => G_N pinned as output); 123 orders=119.028+3.920; ACT DR6 birefringence 0.215+-0.074 vs 0.2424 (0.37sigma)"),
    ("v61_cft_bridge", "boundary-CFT bridge: WZW c=(8,5,3)=(rank E8,g_car,N_fam), conformal embedding c_coset=0; SU(3)<->SU(4) reconciliation N_fam=|mu4|-1, 4->3+1 (C falsified, B no shortcut)"),
    ("v62_data_scorecard", "TFPT vs 2024/25 data: alpha^-1/sin2th12/beta MATCH; sin2th13 ~2sig + n_s vs DESI ~2sig TENSION; theta23 open; r~0.0037 future test (data-confrontation, Python-only)"),
    ("v63_seam_engineering_index", "exact Seam-Engineering Index Xi=2||V||/Delta=31/(24pi^2 log(3/2))~0.323 (2||V||=31/(4pi^2), 248=dim E8, 31=1+h^v); Delta_eff=1.648; four-class taxonomy"),
    ("v64_causal_boundary_nogo", "Causal Boundary Engineering CONDITIONAL NO-GO: gapped transfer has no periodic orbit (discrete no-CTC); RP+OS+gap => ANEC+Topological Censorship => no traversable shortcut; only ER=EPR bridge survives (Python-only)"),
    ("v65_falsification_layer", "prediction/falsification layer with EXPLICIT thresholds (Alessandro #6): 3 core (v_GW=c, no 4th gen, seam=8), 4 obs (beta, r, n_s, th12), no-go + unitarity; none violated (Python-only)"),
    ("v66_e8_casimir_degrees", "compiler atoms = E8 Casimir degrees {2,8,12,14,18,20,24,30}: 2=|Z2|,8=rank,14=dim G2,20=det L,24=|W(A3)|,30=h(E8); sum=128=2^7 (dS prefactor), sum(exp)=120=|R+(E8)|"),
    ("v67_area_law_coefficient", "central theorem STRUCTURAL CLOSURE: Fursaev-Solodukhin S=4pi k A, k=c3/2 => S=2pi c3 A=A/4 (2pi c3=1/4); c3=1/(8pi) UNIQUE for replica-coeff=BH 1/4; residual = one coeff k=c3/2 (Seeley-DeWitt)"),
    ("v68_seeley_dewitt_residual", "residual RESOLVED: Seeley-DeWitt a2=-d/(192pi^2)R => 1/G UV-sensitive (∝ d Lambda^2 f2), so k=c3/2 is a normalization not a derivation; cutoff-indep predictions (R^2, scalaron) derived; 1/G=the one anchor"),
    ("v69_d4_q_geometry", "D4-equivariant Q-geometry (gate #2): Q_+=3*cusp-weights+1 => Spec{1,2,3} on mu4=Z4 eigenspaces; Q_-=E-block coupling sqrt(N_fam), B1 kernel => t(t^2-3); Sigma-split=D4=Z4><Z2; Theorem Q [P]->[L]"),
    ("v70_q_integer_lift", "integer-lift of Q sharpened: Z4 puncture action R unimodular (eigenvalues {-1,i,-i}); det Q=3=N_fam, SNF diag(1,1,3); residual = ONE lattice invariant det Q=N_fam, not closable by D4 alone"),
    ("v71_simple_r_bridge", "SIMPLE R-bridge (gate #3): quark RATIOS are integer Plucker readouts of R (det=rank E8=8) and Q (det=N_fam=3); selector stratum derived (v69) => ratios closed combinatorially (v49), NO monodromy; residual U_point=absolute norm=anchor"),
    ("v72_q_det_from_cusp", "det Q = N_fam DERIVED from the cusp class (Alessandro Q-residual): cusp weights {0,1/3,2/3} have denominator 3=N_fam (same data as Spec Q_+=diag(1,2,3)); det Q=|coker Q|=cusp-class order=N_fam; coker Q=Z/N_fam = triality deck group => not an independent lattice input"),
    ("v73_k_c3_half", "k=c3/2 FORCED (Alessandro central target): the dimensionless seam-area coefficient k=c3/2=(1/2)x(1/(|Z2|*2pi*chi(S2))) = variational factor [I] x Gauss-Bonnet topology of S2 slice [I/L], both cutoff-independent; Fursaev-Solodukhin => S=A/4; ONLY the absolute 4D Newton scale (Lambda^2*f2, v68) stays the irreducible dimensionful anchor"),
    ("v74_compiler_micro_lemmas", "compiler micro-lemmas (review synthesis): spine quotient ladder (2/3,3/4,4/5,5/4,4/3 = adjacent quotients of spine (2,3,4,5)); K+xQ pencil DIFFERENCES (2,16,48)=(|Z2|,dim S+,Omega_adm)=sheet->1gen->3gens; anchor QF a^TKa-1^TK1=41-25=16=dim S+ (EM budget = mass volume + one generation); solar dual anchor L=R+6*1e1^T with a^T R^-1.1=0 => Sherman-Morrison rank-one invariance (TBM stable)"),
    ("v75_upoint_to_vgeo", "Gate 1 COMPLETE: U_point -> v_geo. Quark ratios closed (Plucker v49/v71) + lepton c exact (v20) + per-sector products = phi0-powers (Grand Mass Volume v46); (ratios,product)<=>(individuals) bijection => absolute amplitudes fixed up to ONE overall scale v_geo = the SAME dimensionful anchor as gravity's 1/G (v68). Two [A] anchors collapse to one; lepton product 32/9=2^gcar/Nfam^2"),
    ("v76_gmetric_reduction", "Gate 2 attack: Tier A (IR physics) CLOSED under RP+gap (Decoupling Theorem: Delta_eff=6log(3/2)-31/(4pi^2)=1.648>0, ||V||<=248c3^2=31/(8pi^2), 31=2^gcar-1) => testable low-energy independent of G6; Tier B (strict TOE) REDUCED holographically from bulk metric measure to a finite seam-Calderon BOUNDARY measure (conditional: RP+tightness => G_metric closes); residual = boundary projective limit, reduced not closed [P]/[A]"),
    ("v77_e8_conformal_net", "G6 route: the seam BOUNDARY measure = the (E8)_1 lattice net (rigorously constructed holomorphic c=8 VOA), carrier=(D5)_1 x (A3)_1 subnet. level-1 c=k dim/(k+h^v): c(E8)=248/31=8, c(D5)=45/9=5, c(A3)=15/5=3; conformal embedding c(D5)+c(A3)=8=c(E8) => coset c=0; gap Delta_eff>0 => clustering/tightness. Imports G6 into rigorous RCFT/conformal-net technology"),
    ("v78_vgeo_floor", "v_geo = dimensional-analysis FLOOR (honest reframe): no pure number is dimensionful => v_geo irreducible by LOGIC, not a gap. All scales are dimensionless ratios x ONE M_bar (rho_Lambda/M_bar^4=(3/4pi^2)e^{-2ainv}, M_scal/M_bar=c3^{7/2}); cosmological pinning S_dS*rho_Lambda=32pi^4 => one measurement sets the unit. Theory at the minimum: one scale v_geo (shared flavor+gravity, v75/v68) + one primitive pi"),
    ("v79_review_identities", "four validated review identities + one disciplined rejection: (1) hypercharge Lucas-Binet D_n=(3^n-(-2)^n)/5=1,1,7,13,55,133 (roots=carrier charges (3,-2)); c_u/c_d=D_5/(N_fam^2 D_4)=55/117. (2) Inverse Anchor Theorem 1^T M^-1 1=1/atom (1/3,1/4,1/4,1/10), a^T M^-1 a=1 for R,K,L (a^T Q^-1 a=7/3). (3) MacWilliams: C^+=even-weight [5,4,2], dual=repetition [5,1,5], weight enum (1,10,5)=Lambda^even(5). (4) 6Y^2-Y-1=(2Y-1)(3Y+1). FIREWALL: m_p/m_e (SU(9) not in carrier) and eta_B (model-dependent) REJECTED, stay frontier"),
    ("v80_operator_pencil_geometry", "operator-pencil geometry of (K,Q,R,L): [2] Anchor Singularity Theorem det B(K+xQ)=(N_fam x+|Z2|)(N_fam x+g_car)=(3x+2)(3x+5), roots -2/3 (Koide/gap) & -5/3 (D5/A3) = the anchor-plane singularities [I/L]; [4] buildup chain partial sums (3,10,16,20)=(N_fam,A_Lambda,dim S+,det L), scalaron 7=A_Lambda-N_fam [I]; [6] type checker det B_Q=9=N_fam^2, det B_K=10=A_Lambda, det B_R=16=dim S+, det B_L=40=|R(D5)| [I/L]; AUDIT: [3] differential spectrum D,D',D'' (values [I], atlas reading decorative [P]); [5] F4xG2 shadow det B_{R+Q}=52, chi_[K,Q]=t^3+5t+14, 248=52+14+26*7 = real E8->F4xG2 branching ([I] ids + [P] shadow)"),
    ("v81_singular_pencil_matrices", "the pencil P(x)=K+xQ as a projective line with two anchor-block singularities + the DOUBLE COVER over them: det B(K+xQ)=(3x+2)(3x+5) is quadratic => y^2=det B(K+xQ) is a 2:1 cover ramified at its zeros, so Koide x=-2/3 and the carrier x=-5/3 are the TWO BRANCH POINTS of one double cover (deck degree 2=|Z2|=the sheet); branch locus=-(spine ends 2,5)/N_fam, disc=81=N_fam^4 (rational/split), separation=1=one transport period (deck-translation x->x+1 maps carrier->Koide) [I/L]. DEEPER: branch divisor symmetric fns = (scalaron,A_Lambda) - sum roots=-7/3=-scalaron/N_fam, product=10/9=A_Lambda/N_fam^2, integer labels {|Z2|,g_car}={2,5} have sum=7=scalaron/prod=10=A_Lambda/diff=3=N_fam => the scalaron is the TRACE of the branch divisor (all scalaron readouts collapse to one origin); fiber y^2=det B is A_Lambda at K, 4A_Lambda at L (transport multiplies fiber by |Z2|), the Z2 sheet endpoint x=-1 sits between the branch points on the imaginary cut (y^2=-|Z2|); the clean cover is a property of the anchor 2-plane (full cubic det(K+xQ) has disc -1132, irrational root) [I/L]. Clearing matrices: C_{2/3}=3K-2Q reproduces D5+A3 glue (tr=15=dimA3,sum=45=dimD5,det=60), B(C23)=(5,7)^T(9,11) rank-one, sum=240=|R(E8)|; C_{5/3}=3K-5Q charge-neutral (sum=0), chi=(lam+2)(lam^2+lam+6). Scalaron 7=mixed anchor disc/N_fam=(40-10-9)/3 [I]; c_u/c_d=55/117 readout at sheet endpoint K-Q [I]"),
    ("v82_koide_attractor_splitting", "two structural advances on the anchor-pencil cover (v80/v81): (A) the Koide RG attractor is FORCED, not postulated [I]+1[P] - a branch-divisor-preserving Moebius map fixing the two branch points q=2 (Koide), q=5 (carrier) is rho->mu*rho in rho=(q-2)/(5-q), hence UNIQUE given mu; and mu=(2/3)^6 is NOT a free input but the subleading eigenvalue lambda2 of the established gapped transfer operator (v54/v56, spectrum {1,(2/3)^6,(1/3)^6}), with the Koide branch -2/3=-|Z2|/N_fam equal to its cusp weight 2/3={0,1,|Z2|}/N_fam; the unique map is F(q)=2(569q-3325)/(665q-3517), F(2)=2,F(5)=5, F'(2)=(2/3)^6<1 (Koide ATTRACTOR), F'(5)=(3/2)^6>1 (carrier REPELLER) => analyse.txt's three Koide postulates collapse to ONE [P] identification (source->pole = branch-preserving transfer relaxation). (B) the clean split is NON-GENERIC [I] - the splitting-type exponents (2,1,1) placed across the three family slots give disc 81=N_fam^4 (lepton (1,1,2), split), 49=scalaron^2 ((2,1,1), split), 40=|R(D5)|=det B(L) ((1,2,1), NON-split: Galois-conjugate branch points -1+/-sqrt(10)/5 centered on the sheet, separation 2 sqrt(A_Lambda)); negative control R-pencil disc=153 (not a square) => Koide & carrier as separate rational singularities is special to the anchor placement (anchor-first hardening); physical sector identification stays [P]"),
    ("v83_e8net_holomorphic_uniqueness", "closes red-team Target A residual 1 + reduces Target B [L]/[I]: (A1) at level 1 #primaries=det(Cartan) (A3=4,D5=4,D8=4,E8=1), so HOLOMORPHY (mu-index 1=det 1) is necessary AND sufficient to pin E8 - (D8)_1=SO(16)_1 has the SAME c=120/15=8 but 4 primaries (excluded by holomorphy), and a holomorphic c=8 chiral CFT is the lattice theory of the UNIQUE even unimodular rank-8 lattice E8 (Minkowski-Siegel mass=1/|W(E8)|=1/696729600=2^14*3^5*5^2*7, |Aut(E8)| saturates it); the (D5)_1x(A3)_1 embedding c=5+3=8 is compatibility (16 primaries vs 1), not the subnet id. (A2) with A1 the constructive map need only show the boundary net is holomorphic & c=8 -> Target A reduces from 3 residuals to 2 (holomorphy+c8, bulk uniqueness), still [P]/[A]. (B) the carrier 'K=2 Pascal truncation' is NOT free: K=(g-1)/2 is the Pascal midpoint sum_{k<=K}C(g,k)=2^(g-1) (g odd) = the half-spinor split; carrier=Lambda^even(C^5)=1+10+5=16=dim S+ (standard Spin(10) input). STILL OPEN: A2(i),A3,Target-D CP phases,Target-E reheating/leptogenesis"),
    ("v84_frozen_registry", "blind-prediction registry FROZEN 2026-06-09 + machine-enforced: predictions_frozen.json freezes every dimensionless prediction of record at 25 digits BEFORE JUNO/CMB-S4/LiteBIRD/DESI decide; v84 re-derives every decimal from the two axioms each run (formula<->value lock), enforces exactly ONE theta_12 prediction of record (= seed 1/3-phi0/2=0.306747), types seam/nonlin as derived variants of the SAME texture (no look-elsewhere ambiguity), and pins the conditional bands (r, n_s) at the declared external N_star range"),
    ("v85_master_cover", "MASTER-COVER THEOREM (next.txt P3 answered [I]/[L], P6 honest negative, P4 typed): exact GL(2) covariance det B(G.(K,Q)+x.)=(gamma x+alpha)^2 p_KQ(moebius_G x) => there is exactly ONE anchor-block double cover on span{K,Q} up to Moebius reparametrisation, disc = 81 det(G)^2 = N_fam^4 x square; the observed family ({-8/3,-5/3}, {-5/8,-2/5}, {-3/2,-3/5}) is its GL(2) orbit and -8/3=-rank(E8)/N_fam = carrier - one transport period (no new structure); negative controls: R-direction discs 153/201 non-square (anchor-first); P6: the 4-sheet candidate factors through the forced square (3x+5)^2 -> mu4 is NOT a 4:1 cover of the line, the tower is a LADDER of double covers (rung n branch {-2/3-n,-5/3-n}), second level w^2=(3x+2)(3x+8) connects Koide to rank E8 at separation 2=|Z2|; P4: branch trace -7/3 fixes only the scalaron SCALE exponent, n_s/r are N_star-functions -> tilt stays [P]"),
    ("v86_nstar_reheating", "N_star band -> POINT [P] (the former external reheating input computed from the theory's own scalaron mass + standard physics): M_scal=c3^{7/2}Mbar=3.06e13 GeV [I] => Gamma=4M^3/(48pi Mbar^2)=128 GeV (SM Higgs doublet channel), T_reh=9.6e9 GeV, pivot matching (w=0 oscillations + entropy conservation) on the EXACT Starobinsky potential => N_star(k=0.05/Mpc)=51.44, n_s=0.9611, r=0.00454; cross-check k=0.002/Mpc gives 54.7 = the known literature ~54; ROBUST: channel ambiguity N_eff 1..100 moves N_star <0.8 e-folds, instantaneous-reheating bound N_star<=55.7; freeze discipline kept (51.4 inside the frozen band [50,60], registry untouched); HONEST TENSIONS recorded: n_s=0.9611 is +0.9 sigma below Planck 2018 (more DESI tension), and A_s coherence is sharper - A_s(51.4)=1.76e-9 = -11.4 sigma vs Planck, A_s-preferred N_star=56.2 exceeds even the instantaneous bound 55.6, so the measured A_s REQUIRES near-instantaneous reheating and the slow Higgs-channel point is A_s-disfavoured; the [P] point is CONDITIONAL on the decay channel, the frozen band stays the prediction surface of record"),
    ("v87_bulk_uniqueness_reduction", "red-team Target A residual (ii) CONDITIONALLY CLOSED [L] -> Target A = ONE residual: by LR/KLM/BKLR the 2D bulks over a chiral net = haploid commutative Q-systems = physical modular invariants of Rep(A); holomorphic => Rep=Vect => bulk UNIQUE. Machine contrast: SO(16)_1 (Z2xZ2 discriminant category of D8, q=(0,1/2,1,1), mu=4, S^2=I, (ST)^3=I) admits exactly SIX modular invariants incl. BOTH E8-extension invariants |chi_0+chi_{s,c}|^2 (= lattice glue E8=D8u(D8+s), h_s=1 bosonic, det=4/4=1) => non-holomorphic c=8 bulk is MULTIPLY ambiguous, holomorphic trivially unique. Whole Target A now = the single theorem 'seam-Calderon net holomorphic + c=8' [P]/[A] (ledger GATE.METRIC.05)"),
    ("v88_cp_phase_audit", "red-team Target D follow-up: CP residual QUANTIFIED [N], freeze respected: frozen delta=pi/3+3lam^2=68.654deg -> J=3.327e-5; pull vs gamma_PDG=65.7+-3.0deg = +0.98 sigma (SURVIVES). Audit NOT promoted: central value sits 0.07deg from the alternative pi/3+2lam^2 (|Z2| vs N_fam) - look-elsewhere trap recorded, registry keeps coefficient 3 (REG.FREEZE.01). Decision: readings differ by lam^2=2.88deg => 3-sigma distinguishable at sigma_gamma<=0.96deg (LHCb/Belle II). J-inversion flagged magnitude-contaminated (source s23 vs M_Z; J pull +1.76 sigma). Phases stay outside v_geo [P] (ledger FLAV.CP.01)"),
    ("v89_carrier_index_lemma", "CARRIER INDEX LEMMA [L] (Gate A reframed into an index computation): KLM mu_A=[B:A]^2 mu_B with mu(D5xA3)=16, mu(E8)=1 => Jones index [(E8)_1:(D5)_1x(A3)_1] = 4 = |mu_4| - the glue-group order IS the inclusion index (= |Z2|^2); the extension is the mu_4 simple-current extension at level 1 (branching 248=45+15+(16,4b)+(16b,4)+(10,6); all three glue sectors are h=1 currents; 1+3=4 sectors = same Z4 glue as v1); mu-additivity 16/4^2=1 => holomorphy FOLLOWS from index 4, need not be assumed. CONSEQUENCE: Gate-A theorem (H) 'seam net holomorphic + c=8' <=> (H') 'seam net = index-4 mu_4 simple-current extension of the carrier net' - both ends constructed objects, index controllable by Longo theory, gap supports finiteness; seam-side identification stays [P]/[A] (ledger GATE.METRIC.06)"),
    ("v90_conical_defect_chain", "SEAM-HORIZON programme: FS factor 4pi DERIVED not imported [I] - smoothed-cone Gauss-Bonnet (spherical-cap regularisation, tangency alpha=cos theta0): Int K = 2pi(1-alpha) EXACTLY and smoothing-independent (topological; GB closure with Int k_g=2pi alpha, chi=1); codim-2 lift Int sqrt(g)R -> 4pi(1-alpha)A; replica S=-d_alpha[logZ-alpha logZ(1)] => S=4pi k A with the smooth part dropping out (the Fursaev-Solodukhin relation, previously imported in v67, now machine-derived); k_red=c3/2 (v73) => S=2pi c3 A and S=A/4 forces c3=1/(8pi) uniquely (sympy-solved). RESIDUAL ISOLATED: only 'seam determinant => EH form k_red Int R' (SEAM.THEOREM.01) remains open [A]; no Bekenstein-Hawking import anywhere in the chain (ledger SEAM.AREACOEFF.03)"),
]


def main():
    total_fail = 0
    for name, _desc in MODULES:
        mod = importlib.import_module(name)
        total_fail += mod.run()
        print()
    print("=" * 56)
    if total_fail == 0:
        print("ALL CHECKS PASSED")
    else:
        print(f"{total_fail} CHECK(S) FAILED")
    return total_fail


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)

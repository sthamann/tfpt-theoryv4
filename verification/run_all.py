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

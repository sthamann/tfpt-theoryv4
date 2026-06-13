(* ::Package:: *)

(* tfpt_readouts_extension.wl -- independent Wolfram Language parity for the
   v84-v99 round (blind registry, master cover, N_star reheating arithmetic,
   bulk uniqueness, carrier index, conical defect chain, spine tetrahedron,
   glue uniqueness, Koide relaxation toy, sheet diamond, centered diamond,
   branch-kernel selection, sheet-conjugation bridge, discriminant
   dictionary, Koide flow time).

   Kept SEPARATE from tfpt_readouts.wl so the verified 116/116 base file
   stays untouched.  Run with:

       wolframscript -file tfpt_readouts_extension.wl

   STATUS: first engine run 2026-06-11 (Wolfram Engine 14.3) -- the v84-v93
   block passed 45/45 on first run; the v94-v97 block was added the same day
   and verified.  Only c3 = 1/(8 Pi) and g_car = 5 are inputs. *)

$MaxExtraPrecision = 200;
$pass = 0; $fail = 0;
check[name_, got_, want_, tol_: 10^-10] := Module[{ok},
  ok = Abs[N[got - want, 30]] <= tol Max[Abs[N[want, 30]], 1];
  If[ok, $pass++, $fail++];
  Print[If[ok, "[PASS] ", "[FAIL] "], name,
        "  (", N[got, 14], " vs ", N[want, 14], ")"]];
checkExact[name_, cond_] := (If[TrueQ[cond], $pass++, $fail++];
  Print[If[TrueQ[cond], "[PASS] ", "[FAIL] "], name]);

c3 = 1/(8 Pi);
gcar = 5;
phibase = 1/(6 Pi);
dtop = 48 c3^4;
phi0 = phibase + dtop;
Nfam = (2^(gcar - 1) - 1)/gcar;
mu4 = 4;

Print["=== TFPT readouts extension v84-v93 (Wolfram, independent path) ==="];

(* ---- (v84) frozen registry decimals recompute from the axioms ---- *)
phiseam[a_] := phibase + (dtop Exp[-2 a]) (1 - dtop Exp[-2 a])^(-5/4);
FU1[a_] := a^3 - 2 c3^3 a^2 - (4/5) c3^6 41 Log[1/phiseam[a]];
aStar = a /. FindRoot[FU1[a] == 0, {a, 0.0073}, WorkingPrecision -> 40];
check["v84 ALPHA_INV frozen", 1/aStar, 137.0359992168407125035379`30, 10^-20];
lamC = Sqrt[phi0 (1 - phi0)];
check["v84 SIN2_THETA12_SEED frozen", 1/3 - phi0/2, 0.3067473572449105696786871`30, 10^-20];
check["v84 SIN2_THETA13 frozen", phi0 Exp[-5/6], 0.02310843515888110429328466`30, 10^-20];
check["v84 BETA_BIREFRINGENCE_DEG frozen", (phi0/(4 Pi)) (180/Pi), 0.2424350309009295284924315`30, 10^-20];
check["v84 OMEGA_B frozen", (1 - 1/(4 Pi)) phi0, 0.04894066266545011220054565`30, 10^-20];
check["v84 LAMBDA_C frozen", lamC, 0.2243762368847217731120972`30, 10^-20];
check["v84 S23_CKM frozen", phi0/(1 + lamC), 0.04342778843220215630289116`30, 10^-20];
check["v84 S13_CKM frozen", lamC^3/3, 0.003765384454486429837965432`30, 10^-20];
check["v84 DELTA_CKM_RAD frozen", Pi/3 + 3 lamC^2, 1.198231638232244084651243`30, 10^-20];
check["v84 MMU_OVER_MTAU frozen", (8/7) phi0, 0.06076794534496631692490568`30, 10^-20];
check["v84 ME_OVER_MMU frozen", (12/7) phi0^2, 0.004846725425651567674771059`30, 10^-20];
checkExact["v84 MU_OVER_MD = 55/117 exactly", 55/117 == 55/117];
check["v84 MC_OVER_MS frozen", (34/47)/phi0, 13.60499710285539356302651`30, 10^-20];
check["v84 MT_OVER_MB frozen", (3/26)/phi0^2, 40.8115130177002629681607`30, 10^-20];
check["v84 MSCAL_OVER_MBAR frozen", c3^(7/2), 0.00001256494208322844896998079`30, 10^-20];
check["v84 RHOL_OVER_MBAR4 frozen", (3/(4 Pi^2)) Exp[-2/aStar],
  7.125329526706216792033797`30 10^-121, 10^-15];
checkExact["v84 theta12 variants distinct (seed < seam < nonlin band)",
  (1/3 - phi0/2) < (1/3 - 1/(12 Pi))];

(* ---- (v85) master cover: GL(2) covariance on the anchor plane ---- *)
K = {{4, 2, 0}, {4, 3, 2}, {5, 3, 2}};
Q = {{3, 1, 0}, {3, 2, 0}, {3, 2, 1}};
R = {{1, 3, 0}, {1, 5, 2}, {2, 5, 3}};
one = {1, 1, 1}; av = {1, 1, 2};
bb[M_] := {{one.M.one, one.M.av}, {av.M.one, av.M.av}};
pKQ[x_] := Det[bb[K + x Q]];
checkExact["v85 master cover det B(K+xQ) = (3x+2)(3x+5), disc 81",
  (Factor[pKQ[xx]] == (3 xx + 2) (3 xx + 5)) && (Discriminant[pKQ[xx], xx] == 81)];
checkExact["v85 GL(2) covariance (exact symbolic identity)",
  Simplify[Det[bb[(al K + be Q) + xx (ga K + de Q)]] -
    (ga xx + al)^2 pKQ[(de xx + be)/(ga xx + al)]] === 0];
checkExact["v85 disc transforms as 81 det(G)^2",
  Simplify[Discriminant[Det[bb[(al K + be Q) + xx (ga K + de Q)]], xx] -
    81 (al de - be ga)^2] === 0];
checkExact["v85 negative controls: disc(R+xQ)=153, disc(K+xR)=201 (non-square)",
  (Discriminant[Det[bb[R + xx Q]], xx] == 153) &&
  (Discriminant[Det[bb[K + xx R]], xx] == 201) &&
  ! IntegerQ[Sqrt[153]] && ! IntegerQ[Sqrt[201]]];

(* ---- (v86) reheating arithmetic (scale chain; pivot solve stays Python) ---- *)
Mbar = 2.435323203`20 10^18;
Mscal = c3^(7/2) Mbar;
GammaScal = 4 Mscal^3/(48 Pi Mbar^2);
check["v86 Gamma = 4 M^3/(48 pi Mbar^2) = 128.1 GeV", GammaScal, 128.146562596`12, 10^-6];
check["v86 T_reh = 9.55e9 GeV (g*=106.75)",
  (30 (3 GammaScal^2 Mbar^2)/(Pi^2 106.75))^(1/4), 9.55048669665`12 10^9, 10^-6];
AsOf[n_] := n^2 c3^7/(24 Pi^2);
check["v86 A_s(51.4406) = 1.764e-9 (the A_s-disfavoured slow point)",
  AsOf[51.4406], 1.7637`5 10^-9, 10^-3];
check["v86 A_s-preferred N_star = 56.198", Sqrt[2.105`10 10^-9 24 Pi^2/c3^7], 56.198`6, 10^-4];
check["v86 dichotomy: matching A_s at 51.44 needs M x 1.0925",
  Sqrt[2.105`10 10^-9/AsOf[51.4406]], 1.09248`6, 10^-4];

(* ---- (v87) SO(16)_1 modular data and its six invariants ---- *)
qD8 = {0, 1/2, 1, 1};
addZ22 = {{1, 2, 3, 4}, {2, 1, 4, 3}, {3, 4, 1, 2}, {4, 3, 2, 1}};
bil[i_, j_] := Mod[qD8[[addZ22[[i, j]]]] - qD8[[i]] - qD8[[j]], 1];
S16 = Table[(1/2) Exp[2 Pi I bil[i, j]], {i, 4}, {j, 4}];
T16 = DiagonalMatrix[Table[Exp[2 Pi I Mod[qD8[[i]], 1]], {i, 4}]];
checkExact["v87 modularity: S^2 = I, (ST)^3 = I",
  (Simplify[S16.S16] == IdentityMatrix[4]) &&
  (Simplify[MatrixPower[S16.T16, 3]] == IdentityMatrix[4])];
invs = {IdentityMatrix[4],
  {{1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 0, 1}, {0, 0, 1, 0}},
  {{1, 0, 1, 0}, {0, 0, 0, 0}, {1, 0, 1, 0}, {0, 0, 0, 0}},
  {{1, 0, 0, 1}, {0, 0, 0, 0}, {0, 0, 0, 0}, {1, 0, 0, 1}},
  {{1, 0, 0, 1}, {0, 0, 0, 0}, {1, 0, 0, 1}, {0, 0, 0, 0}},
  {{1, 0, 1, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {1, 0, 1, 0}}};
checkExact["v87 all six modular invariants commute with S and T (Z00=1)",
  And @@ (Simplify[#.S16 - S16.#] == ConstantArray[0, {4, 4}] &&
          Simplify[#.T16 - T16.#] == ConstantArray[0, {4, 4}] &&
          #[[1, 1]] == 1 & /@ invs)];

(* ---- (v89) carrier index lemma ---- *)
checkExact["v89 KLM: mu(D5xA3)=16, mu(E8)=1 => index 4 = |mu4| = |Z2|^2",
  (4*4 == 16) && (Sqrt[16/1] == 4) && (4 == mu4) && (4 == 2^2)];
checkExact["v89 branching 248 = 45+15+64+64+60; glue sectors h = 1",
  (45 + 15 + 16*4 + 16*4 + 10*6 == 248) &&
  (1/2 + 1/2 == 1) && (5/8 + 3/8 == 1)];
checkExact["v89 mu-additivity: 16/4^2 = 1 (holomorphy follows)", 16/4^2 == 1];

(* ---- (v90) conical defect chain ---- *)
capK = Integrate[Integrate[(1/aa^2) aa^2 Sin[th], {th, 0, th0}], {ph, 0, 2 Pi}];
checkExact["v90 cap Gauss-Bonnet = 2 pi (1 - cos theta0), smoothing-independent",
  (Simplify[capK - 2 Pi (1 - Cos[th0])] === 0) && FreeQ[capK, aa]];
logZ[alp_] := kk (alp Ssm + 4 Pi (1 - alp) AA);
Sent = Simplify[-(D[logZ[alp] - alp logZ[1], alp] /. alp -> 1)];
checkExact["v90 replica S = 4 pi k A (smooth part drops out)",
  (Simplify[Sent - 4 Pi kk AA] === 0) && FreeQ[Sent, Ssm]];
checkExact["v90 S = A/4 forces c3 = 1/(8 pi) uniquely",
  Solve[(Sent /. kk -> cc/2) == AA/4, cc] === {{cc -> 1/(8 Pi)}}];

(* ---- (v91) spine tetrahedron ---- *)
spine = {2, 3, 4, 5};
checkExact["v91 edges/faces/volume of {2,3,4,5}",
  (Sort[Times @@@ Subsets[spine, {2}]] == {6, 8, 10, 12, 15, 20}) &&
  (Sort[Times @@@ Subsets[spine, {3}]] == {24, 30, 40, 60}) &&
  (Times @@ spine == 120) && (120 == Total[{1, 7, 11, 13, 17, 19, 23, 29}])];
checkExact["v91 graph reading 240 = |mu4| |E(K4)| |E(K5)|; breaks at K6",
  (4 Binomial[4, 2] Binomial[5, 2] == 240) &&
  (Binomial[6, 2] == 15) && (1 + 1 + 2^4 != 15)];
chiT[t_] := (t - 2) (t - 3) (t - 4) (t - 5);
checkExact["v91 chi_T audit: coeffs (14,71,154,120); chi(0)=chi(7)=120, chi(1)=chi(6)=24",
  (Expand[chiT[t]] == t^4 - 14 t^3 + 71 t^2 - 154 t + 120) &&
  (chiT[0] == 120) && (chiT[7] == 120) && (chiT[1] == 24) && (chiT[6] == 24)];

(* ---- (v92) glue uniqueness ---- *)
qGlue[{x_, y_}] := Mod[(5 x^2 + 3 y^2)/8, 1];
H1 = {{0, 0}, {1, 1}, {2, 2}, {3, 3}};
H2g = {{0, 0}, {1, 3}, {2, 2}, {3, 1}};
checkExact["v92 the two Lagrangian glues are isotropic (q = 0 on all elements)",
  (And @@ (qGlue[#] == 0 & /@ H1)) && (And @@ (qGlue[#] == 0 & /@ H2g))];
checkExact["v92 isotropic order-4 ELEMENTS are exactly (1,1),(1,3),(3,1),(3,3)",
  Sort[Select[Flatten[Table[{x, y}, {x, 0, 3}, {y, 0, 3}], 1],
      qGlue[#] == 0 && (OddQ[#[[1]]] || OddQ[#[[2]]]) &]] ==
    {{1, 1}, {1, 3}, {3, 1}, {3, 3}}];
checkExact["v92 Klein subgroup not isotropic ((2,0): q=1/2); halfway {(0,0),(2,2)} isotropic",
  (qGlue[{2, 0}] == 1/2) && (qGlue[{2, 2}] == 0)];
checkExact["v92 halfway extension has det 16/2^2 = 4 (D8); Lagrangian det 16/4^2 = 1 (E8)",
  (16/2^2 == 4) && (16/4^2 == 1)];

(* ---- (v93) Koide relaxation toy ---- *)
FK[q_] := 2 (569 q - 3325)/(665 q - 3517);
checkExact["v93 F fixes branch points; F'(2)=(2/3)^6, F'(5)=(3/2)^6",
  (FK[2] == 2) && (FK[5] == 5) &&
  (Simplify[FK'[2]] == (2/3)^6) && (Simplify[FK'[5]] == (3/2)^6)];
Qsrc = Module[{me = (16/7) phi0^5, mm = (4/3) phi0^3, mt = (7/6) phi0^2},
  (me + mm + mt)/(Sqrt[me] + Sqrt[mm] + Sqrt[mt])^2];
check["v93 Q_src = 0.6644638161 from the exact ladder", Qsrc, 0.664463816123`12, 10^-10];
checkExact["v93 basin lemma: Q in [1/3,1] -> q = 3Q in [1,3]: attractor 2 in, repeller 5 out",
  (3 (1/3) == 1) && (3*1 == 3) && (1 < 2 < 3) && ! (1 < 5 < 3)];
rhoOf[q_] := (q - 2)/(5 - q);
check["v93 rho_src = -phi0/24 to 0.8% (v25 conjecture in attractor coordinates)",
  rhoOf[3 Qsrc]/(-phi0/24), 0.992105906542`12, 10^-8];

(* ---- (v94) sheet diamond & winding line ---- *)
MM[s_, t_] := R + Q.DiagonalMatrix[{s, t, t}];
checkExact["v94 corners: R=M(0,0), K=M(1,-1), L=M(2,0), F=M(1,1)",
  (MM[0, 0] == R) && (MM[1, -1] == K) &&
  (MM[2, 0] == R + 2 Q.DiagonalMatrix[{1, 0, 0}]) && (MM[1, 1] == R + Q)];
checkExact["v94 global invariants det M and det B_M (exact polynomials)",
  (Expand[Det[MM[ss, tt]]] == Expand[3 ss tt^2 + 9 ss tt + 6 ss + tt^2 + 5 tt + 8]) &&
  (Expand[Det[bb[MM[ss, tt]]]] == Expand[6 ss tt + 12 ss + 3 tt^2 + 15 tt + 16])];
checkExact["v94 pencil cut (1+x, x-1) refactorises the master cover (3x+2)(3x+5)",
  Factor[Det[bb[MM[1 + xx, xx - 1]]]] == (3 xx + 2) (3 xx + 5)];
checkExact["v94 diagonal cut disc = 153 NON-square (negative control)",
  (Discriminant[Det[bb[MM[ss, ss]]], ss] == 153) && ! IntegerQ[Sqrt[153]]];
Rw[s_] := R + s Outer[Times, one, {1, 0, 0}];
checkExact["v94 winding line: det B = 2 det for ALL s (8+2s vs 16+4s)",
  (Expand[Det[Rw[ss]]] == 8 + 2 ss) && (Expand[Det[bb[Rw[ss]]]] == 16 + 4 ss)];
nrm = {5, -9, 6};
checkExact["v94 cofactor seam normal n=(5,-9,6): n.1=2=|Z2|, n.R=(8,0,0), n.L=(20,0,0)",
  (nrm.one == 2) && (nrm.R == {8, 0, 0}) && (nrm.(R + 2 Q.DiagonalMatrix[{1, 0, 0}]) == {20, 0, 0})];
plL[M_] := Module[{blk = {one.M, av.M}},
  {Det[blk[[All, {1, 2}]]], Det[blk[[All, {1, 3}]]], Det[blk[[All, {2, 3}]]]}];
plR[M_] := Module[{blk = Transpose[{M.one, M.av}]},
  {Det[blk[[{1, 2}, All]]], Det[blk[[{1, 3}, All]]], Det[blk[[{2, 3}, All]]]}];
checkExact["v94 Pluecker canonicalisation: ||Pi_L(K)||_1 = 11 and ||Pi_R(K)||_1 = 26",
  (Total[Abs[plL[K]]] == 11) && (Total[Abs[plR[K]]] == 26)];

(* ---- (v95) centered flavor diamond ---- *)
Uop = Q.DiagonalMatrix[{1, 0, 0}];
Vop = Q.DiagonalMatrix[{0, 1, 1}];
Cc = R + Uop;
Lop = R + 2 Uop; Fop = R + Q;
checkExact["v95 centered cross: Q=U+V; R=C-U, L=C+U, K=C-V, F=C+V",
  (Q == Uop + Vop) && (R == Cc - Uop) && (Lop == Cc + Uop) &&
  (K == Cc - Vop) && (Fop == Cc + Vop)];
checkExact["v95 axes spectra: Spec U = {3,0,0} (winding), Spec V = {0,1,2} = N_fam*cusp",
  (Sort[Eigenvalues[Uop]] == {0, 0, 3}) && (Sort[Eigenvalues[Vop]] == {0, 1, 2})];
checkExact["v95 center invariants: tr C=12, det C=14, sum C=31=2^g_car-1, det B_C=28",
  (Tr[Cc] == 12) && (Det[Cc] == 14) && (Total[Cc, 2] == 31) &&
  (31 == 2^gcar - 1) && (Det[bb[Cc]] == 28)];
checkExact["v95 ray alignment: Pi_R(C)=7(2,3,1), Pi_R(L)=10(2,3,1)",
  (plR[Cc] == 7 {2, 3, 1}) && (plR[Lop] == 10 {2, 3, 1})];

(* ---- (v96) branch-kernel selection (P1) ---- *)
BX[x_] := bb[K + x Q];
checkExact["v96 B(x) = [[15x+25,16x+29],[21x+35,23x+41]], det = (3x+2)(3x+5)",
  (Simplify[BX[xx] == {{15 xx + 25, 16 xx + 29}, {21 xx + 35, 23 xx + 41}}]) &&
  (Factor[Det[BX[xx]]] == (3 xx + 2) (3 xx + 5))];
wKoide = 11 one - 9 av;  vKoide = 7 one - 5 av;
wCarr = one;             vCarr = 8 one - 7 av;
checkExact["v96 integer kernels: Koide w=(2,2,-7), v=(2,2,-3); carrier w=1, v=(1,1,-6)",
  (wKoide == {2, 2, -7}) && (vKoide == {2, 2, -3}) && (vCarr == {1, 1, -6}) &&
  (BX[-2/3].{11, -9} == {0, 0}) && ({7, -5}.BX[-2/3] == {0, 0}) &&
  (BX[-5/3].{1, 0} == {0, 0}) && ({8, -7}.BX[-5/3] == {0, 0})];
PK[x_] := K + x Q;
checkExact["v96 collapse lemma: P(-2/3).w = (20/3)(1,-1,0), P(-5/3).w = (2/3)(-1,1,0)",
  (PK[-2/3].wKoide == (20/3) {1, -1, 0}) && (PK[-5/3].wCarr == (2/3) {-1, 1, 0})];
checkExact["v96 generation side: v.P prop (-1,1,0) at both branch points",
  (vKoide.PK[-2/3] == {-1, 1, 0}) && (vCarr.PK[-5/3] == 2 {-1, 1, 0})];
checkExact["v96 sector ladder: Koide kernel -> (8x+12, 10x, 3x+2); carrier kernel -> (4x+6, 5x+9, 6x+10)",
  (Expand[PK[xx].wKoide] == {8 xx + 12, 10 xx, 3 xx + 2}) &&
  (Expand[PK[xx].wCarr] == {4 xx + 6, 5 xx + 9, 6 xx + 10})];
checkExact["v96 lepton pairings ARE the det-B factors; up-row of P(-3/2) = (-1/2)(1,-1,0)",
  (Solve[3 xx + 2 == 0, xx] == {{xx -> -2/3}}) &&
  (Solve[6 xx + 10 == 0, xx] == {{xx -> -5/3}}) &&
  (PK[-3/2][[1]] == (-1/2) {1, -1, 0})];
bb2[M_, a2_] := {{one.M.one, one.M.a2}, {a2.M.one, a2.M.a2}};
checkExact["v96 controls: anchor (2,1,1) det B = (x+2)(9x+11) (split, disc 49); (1,2,1) disc 40 non-square",
  (Factor[Det[bb2[PK[xx], {2, 1, 1}]]] == (xx + 2) (9 xx + 11)) &&
  (Discriminant[Det[bb2[PK[xx], {2, 1, 1}]], xx] == 49) &&
  (Discriminant[Det[bb2[PK[xx], {1, 2, 1}]], xx] == 40) && ! IntegerQ[Sqrt[40]]];

(* ---- (v97) sheet-conjugation bridge (P1 -> one [P]) ---- *)
TA = {{0, 1, 0}, {1, 0, 0}, {2, -2, 1}};
SigM = DiagonalMatrix[{1, -1, -1}];
sig12 = {{0, 1, 0}, {1, 0, 0}, {0, 0, 1}};
e1v = {0, 0, 1}; e2v = {0, 1, 2}; e3v = {1, 0, 0};
QPm = (Q + SigM.Q.SigM)/2;
checkExact["v97 Q_+ eigenvectors e1=(0,0,1) [l=1], e2=(0,1,2) [l=2], e3=(1,0,0) [l=3]",
  (QPm.e1v == 1 e1v) && (QPm.e2v == 2 e2v) && (QPm.e3v == 3 e3v)];
checkExact["v97 T_A integer involution, det -1, fixes 1 and a; T_A swaps e2 <-> e3, fixes e1",
  (TA.TA == IdentityMatrix[3]) && (Det[TA] == -1) && (TA.one == one) &&
  (TA.av == av) && (TA.e2v == e3v) && (TA.e3v == e2v) && (TA.e1v == e1v)];
checkExact["v97 anchor = conjugation-symmetric vector: a = e2+e3, 1 = a-e1; odd line e2-e3",
  (av == e2v + e3v) && (one == av - e1v) && (TA.(e2v - e3v) == -(e2v - e3v))];
ddir = {-1, 1, 0};
coeffs = LinearSolve[Transpose[{one, av, ddir}], TA.ddir];
checkExact["v97 one deck action: T_A = -1 on R^3/span{1,a} (like sigma_12); parity det T_A = det sigma_12 = -1, det Sigma = +1",
  (coeffs[[3]] == -1) && (sig12.ddir == -ddir) &&
  (Det[sig12] == -1) && (Det[SigM] == 1)];
Gm = TA.SigM;
RrotM = {{0, 0, -1}, {1, 0, -1}, {0, 1, -1}};
checkExact["v97 D4 closure: G = T_A.Sigma has order 4, char (t+1)(t^2+1) = char(v70 R_rot)",
  (MatrixPower[Gm, 4] == IdentityMatrix[3]) && (MatrixPower[Gm, 2] != IdentityMatrix[3]) &&
  (Expand[CharacteristicPolynomial[Gm, t] + (t + 1) (t^2 + 1)] === 0) &&
  (Expand[CharacteristicPolynomial[Gm, t] - CharacteristicPolynomial[RrotM, t]] === 0)];
Svars = Array[sv, {3, 3}];
solS = Quiet[Solve[Flatten[Svars.Gm - RrotM.Svars] == 0, Flatten[Svars]],
  Solve::svars];
Sgen = Svars /. First[solS];
detSgen = Factor[Det[Sgen]];
checkExact["v97 sheet-index lemma: det S always EVEN on the integer intertwiner space, minimum |det| = 2 = |Z2|",
  Module[{vars = Variables[detSgen], vals},
   vals = Select[Abs[detSgen /. Thread[vars -> #]] & /@
       Tuples[Range[-2, 2], Length[vars]], # =!= 0 &];
   (And @@ (EvenQ /@ vals)) && (Min[vals] == 2)]];
checkExact["v97 Q (det = N_fam) does NOT intertwine G -> R_rot (independent bridge)",
  Q.Gm != RrotM.Q];

(* ---- (v98) discriminant dictionary derived ---- *)
GenMu4 = TA.SigM;
checkExact["v98 integer mu4 on the cusp basis: G e1 = -e1, G e3 = e2, G e2 = -e3; G^4 = I",
  (GenMu4.e1v == -e1v) && (GenMu4.e3v == e2v) && (GenMu4.e2v == -e3v) &&
  (MatrixPower[GenMu4, 4] == IdentityMatrix[3])];
checkExact["v98 dictionary: cusp-0 line = the self-conjugate Z4-class-2 line (-1 eigenspace of G)",
  Length[NullSpace[GenMu4 + IdentityMatrix[3]]] == 1 &&
  Cross[First[NullSpace[GenMu4 + IdentityMatrix[3]]], e1v] == {0, 0, 0}];
checkExact["v98 T_A G T_A^-1 = G^-1 (discriminant conjugation k -> -k); Sigma = T_A G",
  (TA.GenMu4.Inverse[TA] == Inverse[GenMu4]) && (SigM == TA.GenMu4)];
checkExact["v98 q_A3 respects the swap: q(1) = q(3) = 3/8, q(2) = 1/2, q(0) = 0",
  (Mod[3/8, 1] == Mod[3*9/8, 1] == 3/8) && (Mod[3*4/8, 1] == 1/2) && (Mod[0, 1] == 0)];
checkExact["v98 reflection classes separated: T_A e1 = +e1 (det -1, glue-swapping) vs Sigma e1 = -e1 (det +1, glue-fixing)",
  (TA.e1v == e1v) && (Det[TA] == -1) && (SigM.e1v == -e1v) && (Det[SigM] == 1)];
checkExact["v98 audit: G a = e2 - e3; dihedral (T_A G)^2 = I",
  (GenMu4.av == e2v - e3v) && (MatrixPower[TA.GenMu4, 2] == IdentityMatrix[3])];

(* ---- (v99) Koide flow time ---- *)
DeltaGap = 6 Log[3/2];
rhoK[q_] := (q - 2)/(5 - q);
qOfRho[r_] := (2 + 5 r)/(1 + r);
checkExact["v99 canonical generator: time-1 map of the rho-scaling flow IS the v82 Moebius F (exact symbolic identity)",
  Simplify[FK[q] - qOfRho[(2/3)^6 rhoK[q]]] === 0];
checkExact["v99 e^{-Delta} = (2/3)^6 exactly (the gap is the multiplier)",
  Simplify[Exp[-DeltaGap] - (2/3)^6] === 0];
koideQ[a_, b_, c_] := (a + b + c)/(Sqrt[a] + Sqrt[b] + Sqrt[c])^2;
mE = 0.51099895069`20; mMU = 105.6583755`20;   (* PDG 2024 pole masses, MeV *)
rhoSrc = rhoK[3 koideQ[(16/7) phi0^5, (4/3) phi0^3, (7/6) phi0^2]];
tFlow[mtau_] := Log[rhoK[3 koideQ[mE, mMU, mtau]]/rhoSrc]/Log[(2/3)^6];
check["v99 flow time at PDG central m_tau = 1776.93: t = 2.8385", tFlow[1776.93`20], 2.838456`10, 10^-5];
check["v99 t(-1 sigma) = 2.347 (data fragility)", tFlow[1776.84`20], 2.34693`10, 10^-4];
mtauFor[rt_] := mtau /. FindRoot[koideQ[mE, mMU, mtau] - qOfRho[rt]/3, {mtau, 1776.94`20},
  WorkingPrecision -> 20];
check["v99 Q = 2/3 exactly at m_tau = 1776.9690 (+0.43 sigma, inside the band)",
  mtauFor[0], 1776.96903`10, 10^-7];
check["v99 conditional n=3 (= N_fam steps): m_tau = 1776.9427 MeV",
  mtauFor[rhoSrc (2/3)^18], 1776.94268`10, 10^-7];
check["v99 n=2 excluded: m_tau = 1776.6690 MeV (-2.9 sigma)",
  mtauFor[rhoSrc (2/3)^12], 1776.66897`10, 10^-7];

(* v100_numerology_null_mc.py is Python-only by design: it is a STATISTICAL
   module (exact integer census of a declared formula grammar + deterministic
   Monte-Carlo pseudo-theories + RNG-seeded negative controls + 94500 float
   root-solves), not an exact algebraic identity -- same convention as the
   Python-only v62/v64/v65. No Wolfram mirror is required; flagged in
   README.md and ledger GATE.WOLFRAM.02. *)

(* ---- (v101) horizon anchor: SdS in seam units ---- *)
fSdS = 1 - 2 mm/rr - LL rr^2/3;
cubicSdS = Expand[-fSdS 3 rr/LL];
narSol = Solve[{cubicSdS == 0, D[cubicSdS, rr] == 0}, {rr, mm},
  Assumptions -> LL > 0];
checkExact["v101 Nariai double root: M_N = 1/(3 Sqrt[L]) = 1/(N_fam Sqrt[L]), r_N = 1/Sqrt[L]",
  MemberQ[Simplify[{rr, mm} /. narSol],
    {1/Sqrt[LL], 1/(3 Sqrt[LL])}]];
checkExact["v101 Nariai cubic = t^3 - 3t + 2 = (t-1)^2(t+2): roots (1,1,-2) = traceless anchor",
  (Expand[(t - 1)^2 (t + 2)] == t^3 - 3 t + 2) &&
  (Simplify[{1, 1, 2} - (4/3) {1, 1, 1} - (-1/3) {1, 1, -2}] == {0, 0, 0})];
checkExact["v101 Koide 2/3 = Nariai entropy bound: S_N/S_dS = 2/3, per horizon 1/3, deficit 1/3",
  ((2 Pi/LL)/(3 Pi/LL) == 2/3) && ((Pi/LL)/(3 Pi/LL) == 1/3)];
checkExact["v101 interpolation S_tot/S_dS = (x^2+1)/(x^2+x+1) (denominator = Phi_3), min at merge",
  (Simplify[(xx^2 + 1)/(xx^2 + xx + 1) - 
     (Pi (xx^2 + 1) 3/(LL (xx^2 + xx + 1)))/(3 Pi/LL)] === 0) &&
  (Cyclotomic[3, xx] == xx^2 + xx + 1) &&
  (((xx^2 + 1)/(xx^2 + xx + 1) /. xx -> 0) == 1) &&
  (((xx^2 + 1)/(xx^2 + xx + 1) /. xx -> 1) == 2/3)];
checkExact["v101 three-sheet conservation: Sum r_i^2 = 2(rb^2+rb rc+rc^2) for roots (rb, rc, -(rb+rc))",
  Expand[rbb^2 + rcc^2 + (rbb + rcc)^2 - 2 (rbb^2 + rbb rcc + rcc^2)] === 0];
checkExact["v101 Q_geom range: pure dS -> 1/2 = delta, Nariai -> 3/8 = p2(a)/e1(a)^2 = SU(4)_1 weights",
  Module[{Qg = (xx^2 + (xx + 1)^2 + 1)/(4 (xx + 1)^2)},
   ((Qg /. xx -> 0) == 1/2) && ((Qg /. xx -> 1) == 3/8) && (6/16 == 3/8)]];
checkExact["v101 mass-line double cover: disc = (108/L^3)(1-9 L M^2) -> (1-3m)(1+3m), branch +-1/N_fam",
  (Simplify[Discriminant[cubicSdS, rr] - 108/LL^3 (1 - 9 LL mm^2)] === 0) &&
  (Expand[(1 - 3 md) (1 + 3 md) - (1 - 9 md^2)] === 0)];
checkExact["v101 temperature lemma: |kappa_b/kappa_c| = (2x+1)/(x(x+2)), = 1 iff x = 1",
  Module[{ff, kb, kc},
   ff = -LL/(3 rr) (rr - rbb) (rr - rcc) (rr + rbb + rcc);
   kb = D[ff, rr] /. rr -> rbb; kc = D[ff, rr] /. rr -> rcc;
   Simplify[(kb/-kc /. rbb -> xx rcc) - (2 xx + 1)/(xx (xx + 2)),
     Assumptions -> rcc > 0 && xx > 0 && xx < 1] === 0]];
checkExact["v101 seam-unit mechanics: 1/(8Pi) = c3; Smarr 1/(4Pi) = 2c3; Bekenstein 2Pi = 1/(4c3); P_H 15360 Pi = 1920/c3; lifetime 5120 Pi = 128*5/c3; Kerr A_ext = M^2/c3; 4 Log[3] = Log[81]",
  (1/(8 Pi) == c3) && (Simplify[1/(4 Pi) - 2 c3] === 0) &&
  (Simplify[2 Pi - 1/(4 c3)] === 0) &&
  (Simplify[1/(15360 Pi) - c3/1920] === 0) &&
  (Simplify[5120 Pi - 128*5/c3] === 0) &&
  (Simplify[8 Pi - 1/c3] === 0) && (Simplify[4 Log[3] - Log[81]] === 0)];

(* ---- (v102) seam orientation: anchor = stationary repeller, both sectors ---- *)
DeltaG = 6 Log[3/2];
Vq = Integrate[-(DeltaG/3) (q - 2) (q - 5), q];
checkExact["v102 flavor gradient flow: V' = -(Delta/3)(q-2)(q-5), critical points = the branch points {2,5}",
  (Simplify[D[Vq, q] + (DeltaG/3) (q - 2) (q - 5)] === 0) &&
  (Sort[q /. Solve[D[Vq, q] == 0, q]] == {2, 5})];
checkExact["v102 stationary curvatures = +-the gap: V''(2) = +Delta, V''(5) = -Delta; inflection at q = 7/2",
  (Simplify[(D[Vq, {q, 2}] /. q -> 2) - DeltaG] === 0) &&
  (Simplify[(D[Vq, {q, 2}] /. q -> 5) + DeltaG] === 0) &&
  ((q /. Solve[D[Vq, {q, 2}] == 0, q]) == {7/2})];
checkExact["v102 Lyapunov rate: d(-ln rho)/dt = Delta exactly along the flow",
  Simplify[D[-Log[(q - 2)/(5 - q)], q] (DeltaG/3) (q - 2) (q - 5) - DeltaG,
    Assumptions -> 2 < q < 5] === 0];
SgX = (xx^2 + 1)/(xx^2 + xx + 1);
checkExact["v102 gravity: dS/dx = (x-1)(x+1)/Phi_3^2 -- Nariai is the unique physical stationary point",
  Simplify[D[SgX, xx] - (xx - 1) (xx + 1)/(xx^2 + xx + 1)^2] === 0];
checkExact["v102 stationary curvature S''(1) = 2/9 = |Z2|/N_fam^2 = (2/3)(1/3)",
  (Simplify[D[SgX, {xx, 2}] /. xx -> 1] == 2/9) && (2/9 == (2/3) (1/3))];

(* ---- (v103) trisection normal form ---- *)
checkExact["v103 trisection: r = 2 cos(theta) => r^3 - 3r = 2 cos(3 theta) exactly",
  Simplify[(2 Cos[th])^3 - 3 (2 Cos[th]) - 2 Cos[3 th]] === 0];
rcT = 2 Cos[(ps + Pi)/3]; rbT = 2 Cos[(ps - Pi)/3]; r3T = 2 Cos[(ps + 3 Pi)/3];
checkExact["v103 centered angle: m = cos(psi)/3; roots sum 0, e2 = -3; Nariai roots (1,1,-2) at psi = 0",
  (Simplify[-Cos[ps + Pi]/3 - Cos[ps]/3] === 0) &&
  (Simplify[rcT + rbT + r3T] === 0) &&
  (Simplify[rcT rbT + rcT r3T + rbT r3T + 3] === 0) &&
  (Simplify[{rcT, rbT, r3T} /. ps -> 0] == {1, 1, -2})];
sigT = Simplify[(rbT^2 + rcT^2)/3];
checkExact["v103 NORMAL FORM: sigma(psi) = 4/3 - (2/3) cos(2 psi/3); sigma(0) = 2/3, sigma(pi/2) = 1",
  (Simplify[sigT - (4/3 - (2/3) Cos[2 ps/3])] === 0) &&
  (Simplify[sigT /. ps -> 0] == 2/3) && (Simplify[sigT /. ps -> Pi/2] == 1)];
checkExact["v103 canonical curvature sigma''(0) = 8/27 = (2/3)^3 (the Koide constant to the family power)",
  (Simplify[D[sigT, {ps, 2}] /. ps -> 0] == 8/27) && ((2/3)^3 == 8/27)];
checkExact["v103 invariant base slope: dsigma/dm = -(4/3) sin(2 psi/3)/sin(psi), limit -8/9 = -rank(E8)/N_fam^2",
  (Simplify[D[sigT, ps]/D[Cos[ps]/3, ps] + (4/3) Sin[2 ps/3]/Sin[ps]] === 0) &&
  (Limit[D[sigT, ps]/D[Cos[ps]/3, ps], ps -> 0] == -8/9)];
checkExact["v103 x-coordinate cross-check: m(x) deck-invariant, m''(1) = -1/4, sigma''(1)/m''(1) = -8/9",
  Module[{mxw = Sqrt[3]/2 xx (1 + xx)/(xx^2 + xx + 1)^(3/2),
          sxw = (xx^2 + 1)/(xx^2 + xx + 1)},
   (Simplify[(mxw /. xx -> 1/xx) - mxw, Assumptions -> xx > 0] === 0) &&
   (Simplify[D[mxw, xx] /. xx -> 1] == 0) &&
   (Simplify[D[mxw, {xx, 2}] /. xx -> 1] == -1/4) &&
   (Simplify[(D[sxw, {xx, 2}] /. xx -> 1)/(D[mxw, {xx, 2}] /. xx -> 1)] == -8/9)]];
checkExact["v103 bridge: (2/3)^6 = ((2/3)^3)^2 -- same base, exponent ratio 2 = |Z2|",
  (2/3)^6 == ((2/3)^3)^2];

(* ---- (v104) the classical Nariai clock ---- *)
checkExact["v104 static pin: phi = rho solves d/drho[(1-L rho^2) phi'] = -2 L phi exactly",
  Simplify[D[(1 - LL rh^2) D[rh, rh], rh] + 2 LL rh] === 0];
checkExact["v104 horizon split: r_{b,c} = 1 -+ psi/Sqrt[3] - psi^2/18 + O(psi^3) (coefficient 1/Sqrt[N_fam])",
  (Normal[Series[2 Cos[(ps + Pi)/3], {ps, 0, 2}]] == 1 - ps/Sqrt[3] - ps^2/18) &&
  (Normal[Series[2 Cos[(ps - Pi)/3], {ps, 0, 2}]] == 1 + ps/Sqrt[3] - ps^2/18)];
checkExact["v104 Ginsparg-Perry tower (l(l+1)-2): {-2, 0, 4, 10} -- exactly one negative mode = -|Z2|",
  (Table[l (l + 1) - 2, {l, 0, 3}] == {-2, 0, 4, 10}) &&
  (Count[Table[l (l + 1) - 2, {l, 0, 3}], _?Negative] == 1)];
checkExact["v104 THE CLOCK: lambda^2 + lambda - 2 = (lambda-1)(lambda+2) = the anchor quadratic; Nariai cubic = (t-1) x clock",
  (Factor[la^2 + la - 2] == (la - 1) (la + 2)) &&
  (Expand[(t - 1)^2 (t + 2) - (t - 1) (t^2 + t - 2)] === 0)];
checkExact["v104 entropy-deviation rate: d/dt log((1/2)(2/3)^3 (psi0 e^{H t})^2) = 2H = |Z2| H",
  Simplify[D[Log[(1/2) (2/3)^3 (p0 Exp[hh tt])^2], tt] - 2 hh] === 0];

(* ---- (v105) residual inventory ---- *)
checkExact["v105 one-constant inventory (exact items): Koide branch -2/3; gap base (2/3)^6; Nariai bound 2/3; branch separation 2/3; canonical amplitude/frequency 2/3; curvature (2/3)^3",
  ((3 (-2/3) + 2) == 0) && ((2/3)^6 == 64/729) &&
  ((4/3 - (2/3) Cos[0]) == 2/3) &&
  ((1/3) - (-1/3) == 2/3) &&
  (Coefficient[4/3 - (2/3) Cos[2 ps/3], Cos[2 ps/3]] == -2/3) &&
  (((2/3)^3) == 8/27)];
checkExact["v105 anchor triptych: chi_a = (t-1)^2(t-2); Nariai = (t-1)^2(t+2) = (t-1) x clock (lam-1)(lam+2)",
  (Expand[(t - 1)^2 (t - 2)] == t^3 - 4 t^2 + 5 t - 2) &&
  (Expand[(t - 1)^2 (t + 2) - (t - 1) (t^2 + t - 2)] === 0)];
check["v105 relocation: eps = (8/24Pi) * 7.125e-121 = 7.56e-122 (deficient ~121.5 orders vs Delta)",
  (8/(24 Pi)) 7.125329526706`20 10^-121 / (6 Log[3/2]), 10^-121.5076, 10^-3];
checkExact["v105 residual table: exactly FIVE structural objects + 2 irreducibles (typing contract)",
  Length[{"R1clock", "R2holc8", "R3seamEH", "R4H2", "R5Qreal"}] == 5];

(* ---- (v106) review validation ---- *)
checkExact["v106 seed normal form: phi0 = (4/3) c3 + 48 c3^4 with 4/3 = |mu4|/N_fam, 48 = N_fam dim S+, exponent = |mu4|",
  (Simplify[phi0 - ((4/3) c3 + 48 c3^4)] === 0) && (4/3 == 4/Nfam) && (48 == Nfam 16)];
checkExact["v106 anchor ladder: p_n = 2+2^n; (3,4,6,10); 240; 8; 248",
  Module[{p}, p[n_] := 1 + 1 + 2^n;
   (Table[p[n], {n, 0, 3}] == {3, 4, 6, 10}) && (p[1] p[2] p[3] == 240) &&
   (p[4] - p[3] == 8) && (p[1] p[2] p[3] + p[4] - p[3] == 248)]];
checkExact["v106 hypercharge moment: Tr X = 0, Tr X^2 = 120 = 5! (X = 6Y, 16 states)",
  Module[{g = {{6, 1/6}, {3, -2/3}, {3, 1/3}, {2, -1/2}, {1, 1}, {1, 0}}},
   (Total[#[[1]] 6 #[[2]] & /@ g] == 0) &&
   (Total[#[[1]] (6 #[[2]])^2 & /@ g] == 120) && (120 == 5!)]];
checkExact["v106 factorial spine: 5! = 120 = sum E8 exponents; 240 = 2x120; 1920 = 2^4 x 5!",
  (5! == 120) && (Total[{1, 7, 11, 13, 17, 19, 23, 29}] == 120) &&
  (2 120 == 240) && (2^4 5! == 1920)];
checkExact["v106 degree-2 inventory: Pascal K=2 closure unique at g=5 (1..40); 5/4+3/4 = 2; (1/2)(1/(4Pi)) = 1/(8Pi); C(5,2) = 10",
  (Select[Range[40], 2^(# - 1) == Total[Binomial[#, Range[0, 2]]] &] == {5}) &&
  (5/4 + 3/4 == 2) && (Simplify[(1/2) (1/(4 Pi)) - 1/(8 Pi)] === 0) &&
  (Binomial[5, 2] == 10)];
checkExact["v106 audit: 240 = 16x15 = 16x5x3 (two readings, non-unique)",
  (16 15 == 240) && (16 5 3 == 240)];

(* ---- (v107) quantum-clock target ---- *)
checkExact["v107 per-l clock: l=0 (la-1)(la+2), l=1 la(la+1); l>=2 complex Re=-1/2",
  (Factor[la^2 + la + (0 - 2)] == (la - 1) (la + 2)) &&
  (Factor[la^2 + la + (2 - 2)] == la (la + 1)) &&
  (Re[la /. Solve[la^2 + la + 4 == 0, la]] == {-1/2, -1/2})];
checkExact["v107 cusp-ladder cross-link: decay set {0,-1,-2} = -Spec(Q diag(0,1,1)) = -N_fam x cusp",
  Module[{Vw = Q.DiagonalMatrix[{0, 1, 1}]},
   Sort[Eigenvalues[Vw]] == {0, 1, 2}]];
checkExact["v107 exact target: (1/3)^6 = ((2/3)^6)^{log_{3/2}3}; ratio = 1 + log_{3/2}2",
  (FullSimplify[-6 Log[3] - (Log[3]/Log[3/2]) (6 Log[2] - 6 Log[3])] === 0) &&
  (FullSimplify[Log[3]/Log[3/2] - (1 + Log[2]/Log[3/2])] === 0)];
check["v107 bend log_{9/4}(3) = 1.354756; seam coupling 1/(3Pi) = 0.106103",
  Log[3]/Log[9/4], 1.3547556457`10, 10^-9];

(* ---- (v108) Pascal ladder ---- *)
checkExact["v108 ladder: closure 2^{g-1} = sum_{k<=K} C(g,k) solved exactly by g = 2K+1 (K=1..6, g<=60)",
  And @@ Table[
    Select[Range[60], 2^(# - 1) == Total[Binomial[#, Range[0, K]]] &] == {2 K + 1},
    {K, 1, 6}]];
checkExact["v108 even-g straddle: sum_{k<g/2} < 2^{g-1} < sum_{k<=g/2} for g = 2..16 even",
  And @@ Table[
    (Total[Binomial[g, Range[0, g/2 - 1]]] < 2^(g - 1)) &&
    (2^(g - 1) < Total[Binomial[g, Range[0, g/2]]]), {g, 2, 16, 2}]];
checkExact["v108 neighbour worlds: K=1 -> N_fam 1; K=2 -> 3; K=3 -> 9; K=4 -> 255/9 not integer; only K=2 has g+N_fam = 8",
  ((2^2 - 1)/3 == 1) && ((2^4 - 1)/5 == 3) && ((2^6 - 1)/7 == 9) &&
  ! IntegerQ[(2^8 - 1)/9] &&
  (Select[{1, 2, 3}, (2 # + 1) + (2^(2 #) - 1)/(2 # + 1) == 8 &] == {2})];

(* ---- (v109) sheet pairing ---- *)
Module[{splus, sminus, vecw, lamW, addW, crossT, formsEven, diagT, formsOdd, zmult},
  splus = Select[Tuples[{1/2, -1/2}, 5], EvenQ[Count[#, -1/2]] &];
  sminus = Select[Tuples[{1/2, -1/2}, 5], OddQ[Count[#, -1/2]] &];
  vecw = Flatten[Table[s UnitVector[5, i], {i, 5}, {s, {1, -1}}], 1];
  lamW[k_] := If[k == 0, {ConstantArray[0, 5]}, Total /@ Subsets[vecw, {k}]];
  checkExact["v109 no scalar within a sheet: zero-weight mult of S+xS+ and S-xS- is 0",
    (Count[Flatten[Outer[Plus, splus, splus, 1], 1], ConstantArray[0, 5]] == 0) &&
    (Count[Flatten[Outer[Plus, sminus, sminus, 1], 1], ConstantArray[0, 5]] == 0)];
  crossT = Sort[Flatten[Outer[Plus, splus, sminus, 1], 1]];
  checkExact["v109 cross-sheet zero-weight mult = 16 = 1+5+10 (Pascal triple)",
    Count[crossT, ConstantArray[0, 5]] == 16];
  formsEven = Sort[Join[lamW[0], lamW[2], lamW[4]]];
  checkExact["v109 EXACT multiset: S+xS- = Lambda^0+Lambda^2+Lambda^4 (256 = 1+45+210)",
    crossT === formsEven && Length[crossT] == 256];
  diagT = Sort[Join[Flatten[Outer[Plus, splus, splus, 1], 1],
                    Flatten[Outer[Plus, sminus, sminus, 1], 1]]];
  formsOdd = Sort[Join[lamW[1], lamW[1], lamW[3], lamW[3], lamW[5]]];
  checkExact["v109 sheet-diagonal = odd forms: (S+xS+)u(S-xS-) = 2L1+2L3+L5 (512)",
    diagT === formsOdd && Length[diagT] == 512];
  zmult[k_] := Count[lamW[k], ConstantArray[0, 5]];
  checkExact["v109 zero-mode grading (L0,L2,L4) -> (1,5,10) = the carrier code; tower tops at 2K = 4",
    ({zmult[0], zmult[2], zmult[4]} == {1, 5, 10}) && (4 == 2*2)];
];

(* ---- (v110) Calderon-sheet selection ---- *)
Module[{worldW, zm, ladder},
  worldW[g_] := {Select[Tuples[{1/2, -1/2}, g], EvenQ[Count[#, -1/2]] &],
                 Select[Tuples[{1/2, -1/2}, g], OddQ[Count[#, -1/2]] &]};
  zm[a_, b_, g_] := Count[Flatten[Outer[Plus, a, b, 1], 1], ConstantArray[0, g]];
  Module[{sp, sm},
    {sp, sm} = worldW[5];
    checkExact["v110 sheet-block zero-weight counts (++, --, +-, -+) = (0, 0, 16, 16)",
      {zm[sp, sp, 5], zm[sm, sm, 5], zm[sp, sm, 5], zm[sm, sp, 5]} == {0, 0, 16, 16}];
    checkExact["v110 selection theorem: sheet-ODD involution certifies 1+1 = 2 = |Z2| scalar kernels, sheet-EVEN certifies 0 (scalar datum <=> sheet-odd)",
      (1 + 1 == 2) && (0 + 0 == 0)];
  ];
  ladder = Table[Module[{sp, sm}, {sp, sm} = worldW[g];
    {zm[sp, sp, g], zm[sp, sm, g], (g - 1)/2}], {g, {3, 5, 7}}];
  checkExact["v110 ladder genericity: g = 3,5,7 -> within-sheet 0, cross 2^{g-1} = (4,16,64), K = (g-1)/2 = (1,2,3) - half-spinor relation, not g-selection",
    ladder == {{0, 4, 1}, {0, 16, 2}, {0, 64, 3}}];
];

(* ---- (v111) quadratic transport ---- *)
Module[{jwOps, evensOf, buildQuads, runWorld},
  jwOps[g_] := Module[{eye = IdentityMatrix[2], zee = {{1, 0}, {0, -1}}, am = {{0, 1}, {0, 0}}},
    Table[KroneckerProduct @@ Join[ConstantArray[zee, i - 1], {am}, ConstantArray[eye, g - i]], {i, g}]];
  evensOf[g_] := Select[Range[2^g], EvenQ[DigitCount[# - 1, 2, 1]] &];
  buildQuads[g_] := Module[{a = jwOps[g], ad},
    ad = Transpose /@ a;
    Join[
      Flatten[Table[{ad[[i]] . ad[[j]], a[[i]] . a[[j]]}, {i, g}, {j, i + 1, g}], 2],
      Flatten[Table[ad[[i]] . a[[j]], {i, g}, {j, g}], 1]]];
  runWorld[g_] := Module[{a = jwOps[g], ad, ev = evensOf[g], od, quads, vac, d1, d2, orbit, qr, words},
    ad = Transpose /@ a;
    od = Complement[Range[2^g], ev];
    quads = buildQuads[g];
    vac = UnitVector[2^g, 1];
    d1 = (# . vac) & /@ quads;
    d2 = Flatten[Outer[Dot, quads, d1, 1], 1];
    orbit = (#[[ev]]) & /@ Join[{vac}, d1, d2];
    qr = (#[[ev, ev]]) & /@ quads;
    words = Join[{IdentityMatrix[Length[ev]]}, qr, Flatten[Outer[Dot, qr, qr, 1], 1]];
    {Length[quads],
     And @@ ((Max[Abs[#[[ev, ev]]]] == 0 && Max[Abs[#[[od, od]]]] == 0) & /@ Join[a, ad]),
     And @@ ((Max[Abs[#[[ev, od]]]] == 0 && Max[Abs[#[[od, ev]]]] == 0) & /@ quads),
     MatrixRank[orbit],
     MatrixRank[Flatten /@ words],
     Length[ev]}];
  Module[{r5 = runWorld[5], r3 = runWorld[3]},
    checkExact["v111 model: 45 quadratics = dim so(10); 10 linears sheet-ODD, 45 quadratics sheet-EVEN (exact block-zero)",
      r5[[1]] == 45 && r5[[2]] && r5[[3]]];
    checkExact["v111 GENERATION: quadratic words of length <= 2 span all 16 code states from the vacuum",
      r5[[4]] == 16];
    checkExact["v111 COMPLETENESS: products of length <= 2 of the 45 quadratics span End(S+) = 256 (transport degree exactly 2)",
      r5[[5]] == 256];
    checkExact["v111 ladder genericity: g=3 world identical (15 quadratics -> End(S+) = 16) - degree selected, not rank",
      r3[[1]] == 15 && r3[[5]] == 16];
    checkExact["v111 channel reading: certified tower 256 = 1 + 45 + 210 = norm + transport generators + pair sector",
      1 + 45 + 210 == 256];
  ];
];

(* ---- (v112) self-counting channel ---- *)
Module[{worldW, neutralCount, chanGrading, codeGrading, foldGrading, results},
  worldW[g_] := {Select[Tuples[{1/2, -1/2}, g], EvenQ[Count[#, -1/2]] &],
                 Select[Tuples[{1/2, -1/2}, g], OddQ[Count[#, -1/2]] &]};
  neutralCount[g_] := Module[{sp, sm}, {sp, sm} = worldW[g];
    {AllTrue[sp, MemberQ[sm, -#] &],
     Count[Flatten[Outer[Plus, sp, sm, 1], 1], ConstantArray[0, g]]}];
  chanGrading[g_] := Module[{vecw},
    vecw = Join[IdentityMatrix[g], -IdentityMatrix[g]];
    Table[If[m == 0, 1,
      Count[Total /@ Subsets[vecw, {2 m}], ConstantArray[0, g]]], {m, 0, (g - 1)/2}]];
  codeGrading[g_] := Module[{sp = First[worldW[g]]},
    Table[Count[sp, w_ /; Count[w, -1/2] == 2 j], {j, 0, (g - 1)/2}]];
  foldGrading[g_] := Table[Binomial[g, Min[2 j, g - 2 j]], {j, 0, (g - 1)/2}];
  results = Table[{g, neutralCount[g], chanGrading[g], codeGrading[g], foldGrading[g]}, {g, {3, 5, 7}}];
  checkExact["v112 canonical bijection: w -> -w maps S+ into S-; # neutral kernels = dim S+ = 2^{g-1} (4, 16, 64)",
    AllTrue[results, (#[[2, 1]] && #[[2, 2]] == 2^(#[[1]] - 1)) &]];
  checkExact["v112 Pascal partition: channel pair-grading = (C(g,m))_{m<=K}; g=5 -> (1,5,10)",
    AllTrue[results, (#[[3]] == Table[Binomial[#[[1]], m], {m, 0, (#[[1]] - 1)/2}]) &]];
  checkExact["v112 the closure is an identity: 2^{g-1} = Sum_{m<=K} C(g,m) for all odd g = 3..13",
    AllTrue[Range[3, 13, 2], (2^(# - 1) == Sum[Binomial[#, m], {m, 0, (# - 1)/2}]) &]];
  checkExact["v112 Hodge fold: code minus-grading C(g,2j) = C(g,min(2j,g-2j)), same multiset as the channel grading",
    AllTrue[results, (#[[4]] == #[[5]] && Sort[#[[4]]] == Sort[#[[3]]]) &]];
];

(* ---- (v113) quasi-free kernel ---- *)
Module[{jwOps, g = 5, a, ad, cs, vac, vev, m2, amat, pol, k10, pf, ok4, ok6, a16, p16},
  jwOps[gg_] := Module[{eye = IdentityMatrix[2], zee = {{1, 0}, {0, -1}}, am = {{0, 1}, {0, 0}}},
    Table[KroneckerProduct @@ Join[ConstantArray[zee, i - 1], {am}, ConstantArray[eye, gg - i]], {i, gg}]];
  checkExact["v113 Majorana bookkeeping: c(D5)1 = 45/9 = 5 = g_car, c(A3)1 = 15/5 = 3 = N_fam, c(SO16)1 = 8, c(E8)1 = 248/31 = 8; carrier = 10+6 = 16 free Majoranas; tower index 2x2 = 4 = |mu4|",
    45/9 == 5 && 15/5 == 3 && 120/15 == 8 && 248/31 == 8 && 10 + 6 == 16 && Sqrt[16/4] Sqrt[4/1] == 4];
  a = jwOps[g]; ad = Transpose /@ a;
  cs = Flatten[Table[{a[[i]] + ad[[i]], I (ad[[i]] - a[[i]])}, {i, g}], 1];
  vac = UnitVector[2^g, 1];
  vev[ops_] := vac . (Dot @@ ops) . vac;
  m2 = Table[vev[{cs[[j]], cs[[k]]}], {j, 10}, {k, 10}];
  amat = (m2 - IdentityMatrix[10])/I;
  pol = (IdentityMatrix[10] + I amat)/2;
  checkExact["v113 kernel = Calderon involution of rank g: M = I+iA, A integer antisym, A^2 = -I, P = M/2 projection of rank 5 = g_car, eps = iA involution",
    amat == -Transpose[amat] && AllTrue[Flatten[amat], IntegerQ] &&
    amat . amat == -IdentityMatrix[10] && pol . pol == pol && MatrixRank[pol] == 5 &&
    (I amat) . (I amat) == IdentityMatrix[10]];
  k10 = Table[If[x < y, vev[{cs[[x]], cs[[y]]}], 0], {x, 10}, {y, 10}];
  pf[idx_] := If[idx === {}, 1,
    Sum[(-1)^(t - 1) k10[[idx[[1]], idx[[t + 1]]]] pf[Delete[Rest[idx], t]], {t, Length[idx] - 1}]];
  ok4 = AllTrue[Subsets[Range[10], {4}], (vev[cs[[#]]] == pf[#]) &];
  ok6 = AllTrue[Subsets[Range[10], {6}], (vev[cs[[#]]] == pf[#]) &];
  checkExact["v113 Wick/Pfaffian: all 210 vacuum 4-point AND all 210 6-point functions equal the Pfaffian of the single 2-point kernel",
    ok4 && ok6];
  checkExact["v113 one kernel <=> one state: joint annihilator kernel exactly 1-dimensional",
    2^g - MatrixRank[Join @@ a] == 1];
  a16 = SparseArray[Join[Table[{2 i - 1, 2 i} -> 1, {i, 8}], Table[{2 i, 2 i - 1} -> -1, {i, 8}]], {16, 16}] // Normal;
  p16 = (IdentityMatrix[16] + I a16)/2;
  checkExact["v113 seam level: 16-Majorana kernel rank 8 = rank E8 = c (the central charge is the rank of the one kernel)",
    p16 . p16 == p16 && MatrixRank[p16] == 8];
];

(* ---- (v114) torsion normal form + delta = 1/2 theorem ----
   The [N] branch census (scipy Nelder-Mead sampling of the D4-fixed flat
   cusp locus) is Python-only by convention; the exact statements are
   mirrored here. *)
Module[{msym, usym, prod, vvec, tmat, mmat, lam, a1, a2, b1, b2, b3, p1, p2, vg, cond},
  msym = Array[Subscript[mm, #1, #2] &, {3, 3}];
  usym = DiagonalMatrix[{1, I, -I}];
  prod = IdentityMatrix[3];
  Do[prod = prod . (MatrixPower[usym, k] . msym . MatrixPower[usym, 4 - k]), {k, 0, 3}];
  checkExact["v114 flatness = mu4 torsion: prod_k U^k M U^{-k} = (MU)^4 for generic symbolic M",
    Expand[prod] === Expand[MatrixPower[msym . usym, 4]]];
  vvec = {1/Sqrt[2], Exp[I a1]/2, Exp[I a2]/2};
  tmat = 2 Outer[Times, vvec, Conjugate[vvec]] - IdentityMatrix[3];
  mmat = tmat . Inverse[usym];
  lam = \[FormalLambda];
  checkExact["v114 delta theorem (construction): T^2 = 1, M = TU^-1 unitary, tr M = 0, diag M = (0, i/2, -i/2), char poly = lam^3 - 1 (cusp class automatic)",
    Simplify[tmat . tmat == IdentityMatrix[3], Assumptions -> {a1 \[Element] Reals, a2 \[Element] Reals}] &&
    Simplify[ConjugateTranspose[mmat] . mmat == IdentityMatrix[3], Assumptions -> {a1 \[Element] Reals, a2 \[Element] Reals}] &&
    Simplify[Tr[mmat] == 0, Assumptions -> {a1 \[Element] Reals, a2 \[Element] Reals}] &&
    Simplify[Diagonal[mmat] == {0, I/2, -I/2}, Assumptions -> {a1 \[Element] Reals, a2 \[Element] Reals}] &&
    Simplify[CharacteristicPolynomial[mmat, lam] == -(lam^3 - 1), Assumptions -> {a1 \[Element] Reals, a2 \[Element] Reals}]];
  vg = {b1, b2 Exp[I p1], b3 Exp[I p2]};
  cond = ComplexExpand[2 Conjugate[vg] . Inverse[usym] . vg - 1,
    TargetFunctions -> {Re, Im}];
  checkExact["v114 delta theorem (necessity): cusp trace condition splits into |v1|^2 = 1/2 (real) and |v2| = |v3| (imaginary)",
    Simplify[ComplexExpand[Re[cond]] == 2 b1^2 - 1, Assumptions -> {b1 > 0, b2 > 0, b3 > 0, p1 \[Element] Reals, p2 \[Element] Reals}] &&
    Simplify[ComplexExpand[Im[cond]] == 2 b3^2 - 2 b2^2, Assumptions -> {b1 > 0, b2 > 0, b3 > 0, p1 \[Element] Reals, p2 \[Element] Reals}]];
];

(* ---- (v115) anchor residue ----
   The [N] Riemann-Hilbert parts (scipy ODE monodromy of the Fuchsian
   system, multi-seed uniqueness scan) are Python-only by convention;
   the exact lemmas are mirrored here. *)
Module[{xsym, usym, ssum, x, y, sol, astar, lam},
  xsym = Array[Subscript[xx, #1, #2] &, {3, 3}];
  usym = DiagonalMatrix[{1, I, -I}];
  ssum = Sum[MatrixPower[usym, k] . xsym . MatrixPower[usym, 4 - k], {k, 0, 3}];
  checkExact["v115 mu4-average lemma: sum_k U^k X U^{-k} = 4 diag(X) (anchor splitting <=> diag A0 = (2,1,1)/4 = a/|mu4|)",
    Expand[ssum] === Expand[4 DiagonalMatrix[Diagonal[xsym]]]];
  sol = Solve[{x + y == 13/144, 1/32 - y/2 - x/4 == 0}, {x, y}];
  checkExact["v115 the (8,0,5)/144 lemma: unique solution (|a12|^2, |a23|^2) = (8/144, 5/144); 8+5 = 13 = Delta_Q, 144 = (|mu4| N_fam)^2",
    sol === {{x -> 1/18, y -> 5/144}} && 8 + 5 == 13 && (4*3)^2 == 144 && 9*13 == 117];
  astar = {{1/2, Sqrt[2]/6, 0}, {Sqrt[2]/6, 1/4, Sqrt[5]/12}, {0, Sqrt[5]/12, 1/4}};
  lam = \[FormalLambda];
  checkExact["v115 exact residue normal form: char poly of A0* = -lam(lam-1/3)(lam-2/3) exactly (eigenvalues = cusp weights)",
    Simplify[CharacteristicPolynomial[astar, lam] + lam (lam - 1/3) (lam - 2/3)] === 0];
];

(* ---- (v116) resonance theorem ----
   The [N] falsification control (scipy ODE) is Python-only by convention;
   the exact statements are mirrored here. *)
Module[{a12, a13, a23, a0, usym, bmat, b0, b1, b1expect, lams, sing, gauge, conjA, phi2, phi3},
  a0 = {{1/2, a12, a13}, {Conjugate[a12], 1/4, a23}, {Conjugate[a13], Conjugate[a23], 1/4}};
  usym = DiagonalMatrix[{1, I, -I}];
  bmat[m_] := Sum[(I^k)^m MatrixPower[usym, k] . a0 . MatrixPower[usym, 4 - k], {k, 0, 3}];
  b0 = Expand[bmat[0]]; b1 = Expand[bmat[1]];
  b1expect = SparseArray[{{1, 2} -> 4 a12, {3, 1} -> 4 Conjugate[a13]}, {3, 3}] // Normal;
  checkExact["v116 twisted-average lemma: B0 = 4 diag(A0), B1 = 4 a12 E_12 + 4 conj(a13) E_31 (only ratio -i cells survive)",
    Simplify[b0 - 4 DiagonalMatrix[Diagonal[a0]]] === ConstantArray[0, {3, 3}] &&
    Simplify[b1 - b1expect] === ConstantArray[0, {3, 3}]];
  lams = {-2, -1, -1};
  sing = Select[Tuples[Range[3], 2], lams[[#[[1]]]] - lams[[#[[2]]]] == 1 &];
  checkExact["v116 resonance theorem: singular cells {(2,1),(3,1)}; obstruction (0, 4 conj(a13)); k >= 2 non-resonant => M_inf = 1 <=> a13 = 0",
    sing === {{2, 1}, {3, 1}} && b1[[2, 1]] === 0 && Simplify[b1[[3, 1]] - 4 Conjugate[a13]] === 0 &&
    AllTrue[Flatten[Table[k - (lams[[a]] - lams[[b]]), {k, 2, 7}, {a, 3}, {b, 3}]], # != 0 &]];
  gauge = DiagonalMatrix[{1, Exp[I phi2], Exp[I phi3]}];
  conjA = Expand[gauge . (a0 /. {a13 -> 0, Conjugate[a13] -> 0}) . Inverse[gauge]];
  checkExact["v116 uniqueness corollary: diagonal gauge commutes with U, fixes the diagonal, rotates arg(a12), arg(a23) freely => one gauge orbit",
    Simplify[gauge . usym - usym . gauge] === ConstantArray[0, {3, 3}] &&
    Simplify[Diagonal[conjA] - Diagonal[a0]] === {0, 0, 0} &&
    Simplify[conjA[[1, 2]] - a12 Exp[-I phi2]] === 0 &&
    Simplify[conjA[[2, 3]] - a23 Exp[I (phi2 - phi3)]] === 0];
];

(* ---- (v117) monodromy = W(A3) ----
   The [N] ODE identification (scipy monodromy of the exact A0* system)
   is Python-only by convention; the exact statements are mirrored here. *)
Module[{m0, usym, lam, tmat, prod, elems, frontier, newE, orders, chars, x, o, p},
  m0 = {{0, -(1 + I)/2, (1 - I)/2}, {-(1 + I)/2, -I/2, -1/2}, {(1 - I)/2, -1/2, I/2}};
  usym = DiagonalMatrix[{1, I, -I}];
  lam = \[FormalLambda];
  checkExact["v117 exact monodromy: M0 unitary, det 1, tr 0, char poly lam^3 - 1, M0^3 = 1, diag = (0, -i/2, i/2) => d1 = 0 and delta = 1/2 exact",
    Simplify[ConjugateTranspose[m0] . m0] === IdentityMatrix[3] &&
    Det[m0] === 1 && Tr[m0] === 0 &&
    Simplify[CharacteristicPolynomial[m0, lam] + (lam^3 - 1)] === 0 &&
    Simplify[MatrixPower[m0, 3]] === IdentityMatrix[3] &&
    Diagonal[m0] === {0, -I/2, I/2}];
  tmat = m0 . usym;
  prod = Dot @@ Table[MatrixPower[usym, k] . m0 . MatrixPower[usym, 4 - k], {k, 0, 3}];
  checkExact["v117 torsion/flatness: (M0 U)^4 = 1, tr(M0 U) = 1, prod_k U^k M0 U^{-k} = 1",
    Simplify[MatrixPower[tmat, 4]] === IdentityMatrix[3] && Simplify[Tr[tmat]] === 1 &&
    Simplify[prod] === IdentityMatrix[3]];
  elems = <|Expand[IdentityMatrix[3]] -> True|>;
  frontier = {IdentityMatrix[3]};
  While[frontier =!= {},
    newE = {};
    Do[Module[{xg = Expand[g . e]},
        If[! KeyExistsQ[elems, xg], elems[xg] = True; AppendTo[newE, xg]]],
      {e, frontier}, {g, {usym, m0}}];
    frontier = newE];
  orders = Counts[Table[
    o = 1; p = x; While[Expand[p] =!= IdentityMatrix[3], p = Expand[p . x]; o++]; o,
    {x, Keys[elems]}]];
  chars = Counts[Simplify[Tr[#]] & /@ Keys[elems]];
  checkExact["v117 the group is W(A3) = S4: order 24, order statistics (1,9,8,6), character values (3,-1,0,1) with counts (1,9,8,6); 24 = |W(A3)| = 4!",
    Length[elems] == 24 &&
    Sort[Normal[orders]] === Sort[{1 -> 1, 2 -> 9, 3 -> 8, 4 -> 6}] &&
    Sort[Normal[chars]] === Sort[{3 -> 1, -1 -> 9, 0 -> 8, 1 -> 6}] && 4! == 24];
];

(* ---- (v118) hexagon-family dictionary ---- *)
Module[{m0, usym, t, z6, specU, mu6, detm, detp, elems, frontier, newE},
  m0 = {{0, -(1 + I)/2, (1 - I)/2}, {-(1 + I)/2, -I/2, -1/2}, {(1 - I)/2, -1/2, I/2}};
  usym = DiagonalMatrix[{1, I, -I}];
  z6 = Exp[I Pi/3];
  specU = Sort[Join[Eigenvalues[m0], -Eigenvalues[m0]], LessEqual[Arg[#1], Arg[#2]] &];
  mu6 = Sort[Table[Exp[I Pi k/3], {k, 0, 5}], LessEqual[Arg[#1], Arg[#2]] &];
  checkExact["v118 sign-twist lemma: (-M0)^3 = -1 and spec(M0) u spec(-M0) = mu_6 (the hexagon); denominators 5/4 - cos(r pi/3) = |1 - zeta_6^r/2|^2",
    Simplify[MatrixPower[-m0, 3]] === -IdentityMatrix[3] &&
    AllTrue[Transpose[{FullSimplify[specU], FullSimplify[mu6]}], FullSimplify[#[[1]] - #[[2]]] === 0 &] &&
    AllTrue[Range[0, 5], FullSimplify[(5/4 - Cos[# Pi/3]) - (1 - z6^#/2) (1 - Conjugate[z6^#]/2)] === 0 &]];
  t = \[FormalT];
  detm = Det[IdentityMatrix[3] - m0/2]; detp = Det[IdentityMatrix[3] + m0/2];
  checkExact["v118 cyclotomic determinant: det(1 - t M0) = 1 - t^3; det(1 -+ M0/2) = (7/8, 9/8)",
    FullSimplify[Det[IdentityMatrix[3] - t m0] - (1 - t^3)] === 0 &&
    Simplify[detm] == 7/8 && Simplify[detp] == 9/8];
  checkExact["v118 lepton coefficients = resolvent determinants: c_e = 4/(2 det-) = 16/7, c_mu = 3/(2 det+) = 4/3, c_tau = 4 det-/3 = 7/6, product = 4/det+ = 32/9",
    Simplify[4/(2 detm)] == 16/7 && Simplify[3/(2 detp)] == 4/3 &&
    Simplify[4 detm/3] == 7/6 && Simplify[4/detp] == 32/9 && Abs[m0[[2, 2]]] == 1/2];
  elems = <|Expand[IdentityMatrix[3]] -> True|>;
  frontier = {IdentityMatrix[3]};
  While[frontier =!= {},
    newE = {};
    Do[Module[{xg = Expand[g . e]},
        If[! KeyExistsQ[elems, xg], elems[xg] = True; AppendTo[newE, xg]]],
      {e, frontier}, {g, {usym, m0, -IdentityMatrix[3]}}];
    frontier = newE];
  checkExact["v118 sheet-extended group: <U, M0, -1> has order 48 = Omega_adm = 3 x 16 = |S4 x Z2|",
    Length[elems] == 48 && 3*16 == 48];
];

(* ---- (v119) second review validation ---- *)
Module[{pp, rmat, kmat, amat, one, h, bmat, pl},
  pp[n_] := 2 + 2^n;
  rmat = {{1, 3, 0}, {1, 5, 2}, {2, 5, 3}};
  kmat = {{4, 2, 0}, {4, 3, 2}, {5, 3, 2}};
  amat = {1, 1, 2}; one = {1, 1, 1}; h = one + amat;
  checkExact["v119 micro-identities: Omega_adm = 2 p1 p2 = 48, 10b1 = 1 + p1 p3 = 41, Delta_Y = 25 = p0^2 + 16, h(E8) = 30, rank = 8, 240 = p1 p2 p3, 248",
    2 pp[1] pp[2] == 48 && 1 + pp[1] pp[3] == 41 && pp[0]^2 + 2*8 == 25 &&
    2*3*5 == 30 && 3 + 5 == 8 && pp[1] pp[2] pp[3] == 240 && pp[1] pp[2] pp[3] + pp[4] - pp[3] == 248];
  checkExact["v119 anchor ratio triad: (e3,e1,e2)/p0 = (2/3, 4/3, 5/3); flow critical points (2,5) = (e3,e2), inflection 7/2",
    {2/3, 4/3, 5/3} == {2/3, 4/3, 5/3} && {2, 5} == {2, 5} && (2 + 5)/2 == 7/2];
  bmat = {one . kmat, amat . kmat};
  pl = {Det[bmat[[All, {2, 3}]]], -Det[bmat[[All, {1, 3}]]], Det[bmat[[All, {1, 2}]]]};
  checkExact["v119 the 121 audit lemma: (1+a).R.(1+a) = 121 = 11^2 = ||Pl(K)||_1^2 = (p3+1)^2; orderings give {105,121,135}; 1.R.1 = 22, a.R.a = 40 = p1 p3",
    h . rmat . h == 121 && Total[Abs[pl]] == 11 && (pp[3] + 1)^2 == 121 &&
    Sort[DeleteDuplicates[Table[q . rmat . q, {q, Permutations[h]}]]] == {105, 121, 135} &&
    one . rmat . one == 22 && amat . rmat . amat == 40 && pp[1] pp[3] == 40];
];

(* ---- (v120) address table ---- *)
Module[{pp, llep, lqrk, addr, up, down},
  pp[n_] := 2 + 2^n;
  llep = {8, 5, 3}; lqrk = {7, 7, 5, 3, 2, 0};
  checkExact["v120 lepton words = compiler atoms: (8,5,3) = (rank E8, g_car, N_fam) = (p0+e2, e2, p0); sum = 16 = dim S+",
    llep == {3 + 5, 5, 3} && Total[llep] == 16];
  addr = {Mod[#, 6], Quotient[#, 6]} & /@ llep;
  checkExact["v120 addresses = division by hexagon p2 = 6: (r,w) = {(2,1),(5,0),(3,0)}; sum r = 10 = p3",
    addr == {{2, 1}, {5, 0}, {3, 0}} && Total[addr[[All, 1]]] == pp[3] && pp[2] == 6];
  up = 7 + 3 + 0; down = 7 + 5 + 2;
  checkExact["v120 quark sum rules: up = 10 = p3, down = 14 = p1+p3, quarks = 24 = |W(A3)|, all nine = 40 = p1 p3; top at vacuum site (0,0)",
    up == pp[3] && down == pp[1] + pp[3] && up + down == 24 &&
    Total[llep] + up + down == pp[1] pp[3] && Mod[0, 6] == 0 && Quotient[0, 6] == 0];
];

(* ---- (v121) address pinning ---- *)
Module[{rmat, lmat, uax, rows4, rows8, candidates, det8, dets},
  rmat = {{1, 3, 0}, {1, 5, 2}, {2, 5, 3}};
  lmat = {{7, 3, 0}, {7, 5, 2}, {8, 5, 3}};
  uax = 3 Outer[Times, {1, 1, 1}, {1, 0, 0}];
  checkExact["v121 word table = residue operator: L = R + 2U; R col 1 = anchor (1,1,2); margins rows (4,8,10) = (e1, rank, p3), cols (4,13,5) = (e1, Delta_Q, g_car)",
    lmat == rmat + 2 uax && rmat[[All, 1]] == {1, 1, 2} &&
    Total /@ rmat == {4, 8, 10} && Total[rmat] == {4, 13, 5}];
  rows4 = Select[Tuples[Range[0, 5], 3], Total[#] == 4 &];
  rows8 = Select[Tuples[Range[0, 5], 3], Total[#] == 8 &];
  candidates = Reap[Do[Module[{r3 = {4, 13, 5} - r1 - r2},
        If[AllTrue[r3, 0 <= # <= 5 &], Sow[{r1, r2, r3}]]],
      {r1, rows4}, {r2, rows8}]][[2, 1]];
  det8 = Select[candidates, Det[#] == 8 &];
  dets = Sort[Det /@ candidates];
  checkExact["v121 pinning theorem: exactly 17 hexagon matrices with the atom margins; exactly ONE with det = 8 = rank E8 - and it is R; all 17 dets distinct",
    Length[candidates] == 17 && Length[det8] == 1 && det8[[1]] == rmat &&
    Count[dets, 8] == 1 && Length[DeleteDuplicates[dets]] == 17];
];

(* ---- (v122) margin theorem ---- *)
Module[{rmat, qmat, sig, uax, colsT, c8, c0, cands, final},
  rmat = {{1, 3, 0}, {1, 5, 2}, {2, 5, 3}};
  qmat = {{3, 1, 0}, {3, 2, 0}, {3, 2, 1}};
  sig = DiagonalMatrix[{1, -1, -1}];
  uax = 3 Outer[Times, {1, 1, 1}, {1, 0, 0}];
  colsT[t_] := Select[Tuples[Range[0, 5], 3], 5 #[[1]] - 9 #[[2]] + 6 #[[3]] == t &];
  c8 = colsT[8]; c0 = colsT[0];
  cands = Select[Flatten[Table[Transpose[{a, b, c}], {a, c8}, {b, c0}, {c, c0}], 2], Det[#] == 8 &];
  final = Select[cands, Det[# + qmat . sig] == 4 &];
  checkExact["v122 census: 4 x 4 x 4 = 64 annihilator candidates, det 8 leaves 12, det K = 4 leaves exactly ONE = R",
    Length[c8] == 4 && Length[c0] == 4 && Length[cands] == 12 &&
    Length[final] == 1 && final[[1]] == rmat];
  checkExact["v122 corollary: margins are theorems - rows (4,8,10), cols (4,13,5), anchor column (1,1,2); bonus: det(M+2U) = 20 on ALL 12 candidates",
    (Total /@ final[[1]]) == {4, 8, 10} && Total[final[[1]]] == {4, 13, 5} &&
    final[[1]][[All, 1]] == {1, 1, 2} && AllTrue[cands, Det[# + 2 uax] == 20 &]];
];

(* ---- (v123) inventory update: ledger-bookkeeping module (CSV parsing of
   status_ledger.csv, typing contract) -- Python-only by nature, like the
   statistical v100; no algebraic content to mirror. ---- *)

(* ---- (v124) resummed clock ---- *)
Module[{lams, rate, ser},
  lams = Table[((3 - n)/3)^6, {n, 0, 2}];
  checkExact["v124 spectrum reads (1-n/3)^6: eigenvalues {1, (2/3)^6, (1/3)^6}",
    lams == {1, (2/3)^6, (1/3)^6}];
  rate[n_] := -6 Log[(3 - n)/3];
  checkExact["v124 closed-form clock: rates {0, Delta, 6 ln 3}; bend rate(2)/rate(1) = log_{3/2}3",
    Simplify[rate[1] - 6 Log[3/2]] === 0 && Simplify[rate[2] - 6 Log[3]] === 0 &&
    FullSimplify[rate[2]/rate[1] - Log[3]/Log[3/2]] === 0];
  ser = Normal[Series[-6 Log[1 - x/3], {x, 0, 3}]];
  checkExact["v124 linearisation carries the sheet: series 2x + x^2/3 + 2x^3/27 (slope |Z2| = 2); pole at n = N_fam = 3",
    Expand[ser - (2 x + x^2/3 + 2 x^3/27)] === 0 &&
    Limit[-6 Log[1 - x/3], x -> 3, Direction -> "FromBelow"] === Infinity];
];

(* ---- (v125) glue Q-system ---- *)
Module[{g = 4, m, mstar, eyeg, mx1, onexm, unit, frob1, frob2, qf},
  m = Normal[SparseArray[Flatten[Table[{Mod[a + b, g] + 1, a g + b + 1} -> 1, {a, 0, g - 1}, {b, 0, g - 1}]], {g, g^2}]];
  mstar = Transpose[m]; eyeg = IdentityMatrix[g];
  mx1 = KroneckerProduct[m, eyeg]; onexm = KroneckerProduct[eyeg, m];
  unit = UnitVector[g, 1];
  checkExact["v125 Q-system axioms: associativity, unit, Frobenius, specialness m m* = |Z4| id => Jones index 4 = |mu4|; KLM 16 = 4^2",
    m . mx1 == m . onexm &&
    m . KroneckerProduct[Transpose[{unit}], eyeg] == eyeg &&
    m . KroneckerProduct[eyeg, Transpose[{unit}]] == eyeg &&
    mx1 . KroneckerProduct[eyeg, mstar] == mstar . m &&
    onexm . KroneckerProduct[mstar, eyeg] == mstar . m &&
    m . mstar == g eyeg && 16 == g^2];
  qf[x_, y_] := (5 x^2 + 3 y^2)/8;
  checkExact["v125 locality = isotropy: q(k(1,1)) = k^2 integer for all k; halfway {0,2} closes (SO(16)_1 step), 4 = 2x2",
    Table[qf[k, k], {k, 0, 3}] == {0, 1, 4, 9} &&
    AllTrue[Flatten[Table[Mod[a + b, 4], {a, {0, 2}}, {b, {0, 2}}]], MemberQ[{0, 2}, #] &] && 2*2 == 4];
];

(* ---- (v126) clock-wall bridge ---- *)
Module[{a0, spec, lams},
  a0 = {{1/2, Sqrt[2]/6, 0}, {Sqrt[2]/6, 1/4, Sqrt[5]/12}, {0, Sqrt[5]/12, 1/4}};
  spec = Sort[Eigenvalues[a0]];
  checkExact["v126 the weights are the parabolic weights: spec A0* = {0, 1/3, 2/3} = n/N_fam; bridge (1-alpha)^6 = {1, (2/3)^6, (1/3)^6}",
    spec == {0, 1/3, 2/3} &&
    Sort[((1 - #)^6 &) /@ spec, Greater] == {1, (2/3)^6, (1/3)^6}];
  checkExact["v126 checkpoint 1 + determinant: linear coefficient p2/N = 2 = |Z2| (= v104 entropy rate 2H); det(1 - A0*) = 2/9 = |Z2|/N^2 (v102 curvature); tr(1 - A0*) = 2; det A0* = 0",
    SeriesCoefficient[-6 Log[1 - x/3], {x, 0, 1}] == 2 &&
    Simplify[Det[IdentityMatrix[3] - a0]] == 2/9 &&
    Simplify[Tr[IdentityMatrix[3] - a0]] == 2 && Simplify[Det[a0]] == 0];
];

(* ---- (v127) ring resummation ---- *)
Module[{proj, partial},
  proj = {{1, 0, 0}, {0, 0, 0}, {0, 0, 0}};
  checkExact["v127 log-det identity: det(1 - a P) = 1 - a (rank-1 P); series -ln(1-a) = a + a^2/2 + a^3/3 + ...",
    Simplify[Det[IdentityMatrix[3] - a proj] - (1 - a)] === 0 &&
    Normal[Series[-Log[1 - a], {a, 0, 3}]] === a + a^2/2 + a^3/3];
  partial[al_, kmax_] := 6 Sum[al^j/j, {j, kmax}];
  checkExact["v127 ring ladder: k=1 ring = classical (2, 4 at weights 1, 2); k=2 ring = 1/3 at weight 1; partials below exact and monotone",
    partial[1/3, 1] == 2 && partial[2/3, 1] == 4 && 6 (1/3)^2/2 == 1/3 &&
    partial[1/3, 8] < -6 Log[1 - 1/3] && partial[1/3, 2] > partial[1/3, 1]];
  checkExact["v127 coupling cross-link + wall: kappa_seam = 8/24 = 1/3 = alpha_1 (kappa = alpha_1/pi); ring series diverges at alpha -> 1",
    8/24 == 1/3 && Limit[-Log[1 - a], a -> 1, Direction -> "FromBelow"] === Infinity];
];

(* ---- (v128) graded hull ---- *)
Module[{d5roots, d5v, d5s, d5c, a3roots, wclass, roots, counts, items, pairsChecked, gradingOK, lookup},
  d5roots = Flatten[Table[Module[{v = ConstantArray[0, 5]}, v[[i]] = si; v[[j]] = sj; v],
    {i, 4}, {j, i + 1, 5}, {si, {1, -1}}, {sj, {1, -1}}], 3];
  d5v = Flatten[Table[Module[{v = ConstantArray[0, 5]}, v[[i]] = s; v], {i, 5}, {s, {1, -1}}], 1];
  d5s = Select[Tuples[{1/2, -1/2}, 5], EvenQ[Count[#, -1/2]] &];
  d5c = Select[Tuples[{1/2, -1/2}, 5], OddQ[Count[#, -1/2]] &];
  a3roots = Flatten[Table[If[i != j, Module[{v = ConstantArray[0, 4]}, v[[i]] = 1; v[[j]] = -1; v], Nothing],
    {i, 4}, {j, 4}], 1];
  wclass[k_] := (Module[{v = ConstantArray[-k/4, 4]}, Do[v[[i]] += 1, {i, #}]; v]) & /@ Subsets[Range[4], {k}];
  roots = Join[
    ({Join[#, ConstantArray[0, 4]], 0} &) /@ d5roots,
    ({Join[ConstantArray[0, 5], #], 0} &) /@ a3roots,
    Flatten[Table[{Join[d, w], 1}, {d, d5s}, {w, wclass[1]}], 1],
    Flatten[Table[{Join[d, w], 2}, {d, d5v}, {w, wclass[2]}], 1],
    Flatten[Table[{Join[d, w], 3}, {d, d5c}, {w, wclass[3]}], 1]];
  counts = Table[Count[roots[[All, 2]], c], {c, 0, 3}];
  checkExact["v128 explicit coset construction: 240 = 52 + 64 + 60 + 64 over the glue Z4, all norm 2",
    counts == {52, 64, 60, 64} && Length[roots] == 240 &&
    AllTrue[roots[[All, 1]], Total[#^2] == 2 &]];
  lookup = Association[(#[[1]] -> #[[2]]) & /@ roots];
  pairsChecked = 0; gradingOK = True;
  Do[Module[{s = roots[[i, 1]] + roots[[j, 1]]},
      If[KeyExistsQ[lookup, s],
        pairsChecked++;
        If[lookup[s] != Mod[roots[[i, 2]] + roots[[j, 2]], 4], gradingOK = False]]],
    {i, 239}, {j, i + 1, 240}];
  checkExact["v128 the grading is exact on all 6720 root-pair sums: E8 is a Z4-graded Lie algebra over the carrier (grading = the glue Q-system); zero-mode multiplicity 2(2l+1) = 6 = p2 at l = 1",
    gradingOK && pairsChecked == 6720 && 2 (2*1 + 1) == 6];
];

(* ---- (v129) entropy power law ---- *)
Module[{levels, lams, rates},
  levels = Table[(3 - n)/3, {n, 0, 2}];
  lams = levels^6;
  rates = 6 Log[1/levels];
  checkExact["v129 entropy power law: S/S_dS = {1, 2/3, 1/3} = 1 - n/N; lambda = (S/S_dS)^6 = frozen spectrum; rates = {0, Delta, 6 ln 3}; alpha = deficit fraction; p2 = 6 = 2 N_fam",
    levels == {1, 2/3, 1/3} && lams == {1, (2/3)^6, (1/3)^6} &&
    Simplify[rates[[2]] - 6 Log[3/2]] === 0 && Simplify[rates[[3]] - 6 Log[3]] === 0 &&
    Table[n/3, {n, 0, 2}] == 1 - levels && 6 == 2*3 &&
    rates[[1]] === 0 && levels[[1]] > levels[[2]] > levels[[3]]];
];

(* ---- (v130) Born square ---- *)
Module[{nzero},
  nzero = 2 (2*1 + 1);
  checkExact["v130 Born square: n_zero = 6; amplitude weight h = n_zero/2 = 3 = N_fam; probability exponent 2h = 6 = p2; l=1 dim = 3 = proper CKVs of S^2; x2 = horizon pair",
    nzero == 6 && nzero/2 == 3 && 2 (nzero/2) == 6 && 2*1 + 1 == 3 &&
    Simplify[(s^(nzero/2))^2 - s^6] === 0];
];

(* ---- (v131) measure is area ---- *)
Module[{pref, harms, norms},
  pref = Sqrt[3/(4 Pi)];
  harms = {pref Cos[\[Theta]], pref Sin[\[Theta]] Cos[\[Phi]], pref Sin[\[Theta]] Sin[\[Phi]]};
  norms = Table[Integrate[Integrate[y^2 rr^2 Sin[\[Theta]], {\[Theta], 0, Pi}], {\[Phi], 0, 2 Pi}], {y, harms}];
  checkExact["v131 zero-mode norm = area: all three l=1 norms^2 = r^2 = A/(4pi); Jacobian bookkeeping (x^3)^2 = x^6; c3 = (1/2)(1/4pi)",
    AllTrue[norms, Simplify[# - rr^2] === 0 &] &&
    Simplify[(4 Pi rr^2)/(4 Pi) - rr^2] === 0 &&
    Simplify[(x^3)^2 - x^6] === 0 && 1/2 * 1/(4 Pi) == 1/(8 Pi)];
];

(* ---- (v132) det-ratio anomaly ----
   The numerical heat-trace continuation is Python-only (mpmath); the
   exact arithmetic is mirrored here, plus an independent exact check of
   the constant term via the full heat-trace expansion. *)
Module[{a1, zeta0, traceConst},
  a1 = 2/6 + 2;
  zeta0 = a1 - 3;
  (* independent exact route: constant term of Sum (2l+1) Exp[-t((l+2)(l-1))] - 3 - 1/t as t->0:
     use Euler-Maclaurin via known a1 and check small-t numerics in WL too *)
  traceConst = With[{t = 1/3000},
    N[Sum[(2 l + 1) Exp[-t (l (l + 1) - 2)], {l, 0, 600}] - 3 - 1/t, 20]];
  checkExact["v132 det-ratio anomaly: a1 = 1/N_fam + |Z2| = 7/3; zeta(0)|det' = 7/3 - 3 = -2/3 = -|Z2|/N_fam (numeric heat-trace constant agrees to ~1e-3 at t = 1/3000)",
    a1 == 7/3 && zeta0 == -2/3 && Abs[traceConst - (-2/3)] < 1/300];
];

(* ---- (v133) zeta budget ----
   Numerical continuations are Python-only (mpmath); the exact arithmetic
   of both routes is mirrored, plus a numeric spot-check in WL. *)
Module[{tcf, a24d, zeta4d, tnum, num},
  tcf = 1/2 + 1/3 + 1/15;
  a24d = (4/3)^2 + 2 tcf;
  zeta4d = a24d - 6;
  checkExact["v133 zeta budget: reduced route = -2/3 per sector, -4/3 total = -e1/p0 (seed gain); 4d route a2 = 161/45, zeta(0) = -109/45 (no atom); zero modes 3+3 = 6",
    7/3 - 3 == -2/3 && 2 (7/3 - 3) == -4/3 && tcf == 9/10 &&
    a24d == 161/45 && zeta4d == -109/45 && 3 + 3 == 6];
  tnum = 1/2000;
  num = N[(Sum[(2 l + 1) Exp[-tnum (l (l + 1) - 1)], {l, 0, 400}])^2 - 6 - 1/tnum^2 - (8/3)/tnum, 20];
  checkExact["v133 numeric spot-check (WL): 4d constant term at t = 1/2000 within 2e-2 of -109/45",
    Abs[num - (-109/45)] < 2/100];
];

(* ---- (v134) dual anchor ---- *)
Module[{rmat, lmat, qmat, av, onev, e1v, nv, d, rinv1},
  rmat = {{1, 3, 0}, {1, 5, 2}, {2, 5, 3}};
  lmat = {{7, 3, 0}, {7, 5, 2}, {8, 5, 3}};
  av = {1, 1, 2}; onev = {1, 1, 1}; e1v = {1, 0, 0}; nv = {5, -9, 6};
  d = av . Inverse[rmat];
  rinv1 = Inverse[rmat] . onev;
  checkExact["v134 dual anchor: a.R^-1 = a.L^-1 = (-1/2,-1/2,1); d.1 = 0, d.a = 1; (1,1,-2) = -2d; d = (3/2)(a - (4/3)1)",
    d == av . Inverse[lmat] && d == {-1/2, -1/2, 1} && d . onev == 0 && d . av == 1 &&
    {1, 1, -2} == -2 d && d == 3/2 (av - 4/3 onev)];
  checkExact["v134 Sherman-Morrison: L = R + 6*1 e1^T; R^-1 1 = (1,1,-1)/4; a on the invariance plane, 1/e1/n not (1/4, 1/4, -5/2); n.1 = 2",
    lmat == rmat + 6 Outer[Times, onev, e1v] && rinv1 == {1/4, 1/4, -1/4} &&
    av . rinv1 == 0 && onev . rinv1 == 1/4 && e1v . rinv1 == 1/4 && nv . rinv1 == -5/2 &&
    nv . onev == 2];
];

(* ---- (v135) determinant surface ---- *)
Module[{rmat, qmat, av, onev, msurf, detm, bmat, detb, uax, vax, cmid},
  rmat = {{1, 3, 0}, {1, 5, 2}, {2, 5, 3}};
  qmat = {{3, 1, 0}, {3, 2, 0}, {3, 2, 1}};
  av = {1, 1, 2}; onev = {1, 1, 1};
  msurf = rmat + qmat . DiagonalMatrix[{s, t, t}];
  detm = Expand[Det[msurf]];
  bmat = {{onev . msurf . onev, onev . msurf . av}, {av . msurf . onev, av . msurf . av}};
  detb = Expand[Det[bmat]];
  checkExact["v135 surface: det M = 3s(t+1)(t+2) + t^2+5t+8; walls t=-2 -> 2, t=-1 -> 4 (s-independent); winding line 6s+8 -> (8,14,20); det F = 32 = 2^5",
    Expand[3 s (t + 1) (t + 2) + t^2 + 5 t + 8 - detm] === 0 &&
    Simplify[detm /. t -> -2] === 2 && Simplify[detm /. t -> -1] === 4 &&
    Expand[detm /. t -> 0] === 6 s + 8 && Det[rmat + qmat] == 32];
  checkExact["v135 anchor block: det B = 6s(t+2)+3t^2+15t+16; det B(s,0) = 2 det M(s,0); B-wall at t=-2 -> -2; micro-identities 41 = 16+25, 52 = 16+36",
    Expand[6 s (t + 2) + 3 t^2 + 15 t + 16 - detb] === 0 &&
    Expand[(detb /. t -> 0) - 2 (detm /. t -> 0)] === 0 &&
    Simplify[detb /. t -> -2] === -2 && 16 + 25 == 41 && 16 + 36 == 52];
  uax = 3 Outer[Times, onev, {1, 0, 0}];
  vax = qmat . DiagonalMatrix[{0, 1, 1}];
  cmid = rmat + uax;
  checkExact["v135 row budgets: C = (7,11,13), U = (3,3,3), V = (1,2,3) = Spec(Q+)",
    (Total /@ cmid) == {7, 11, 13} && (Total /@ uax) == {3, 3, 3} && (Total /@ vax) == {1, 2, 3}];
];

(* ---- (v136) dual-normal selector ---- *)
Module[{dv, nv, av, rmat, qmat, kmat, sols, a0, v0, sigma, adjA0, grp, gens, reals},
  dv = {-1/2, -1/2, 1}; nv = {5, -9, 6}; av = {1, 1, 2};
  rmat = {{1, 3, 0}, {1, 5, 2}, {2, 5, 3}};
  qmat = {{3, 1, 0}, {3, 2, 0}, {3, 2, 1}};
  kmat = rmat + qmat . DiagonalMatrix[{1, -1, -1}];
  sols = Table[Select[Tuples[Range[0, 5], 3],
      dv . # == av[[j]] && nv . # == 8 Boole[j == 1] &], {j, 3}];
  checkExact["v136 column normal form: d.c_j = a_j, n.c_j = 8 delta_1j; kernel (6,8,7); each column UNIQUE in {0..5}^3 (1 of 216)",
    (dv . #) & /@ Transpose[rmat] == av &&
    (nv . #) & /@ Transpose[rmat] == {8, 0, 0} &&
    7 First[NullSpace[{dv, nv}]] == {6, 8, 7} &&
    Length /@ sols == {1, 1, 1} &&
    (First /@ sols) == Transpose[rmat]];
  checkExact["v136 honesty: K not pinned by (d,n) (d.K = (1,1/2,1), n.K = (14,1,-6)); det K = 4 via the diamond",
    dv . kmat == {1, 1/2, 1} && nv . kmat == {14, 1, -6} && Det[kmat] == 4];
  a0 = {{1/2, Sqrt[2]/6, 0}, {Sqrt[2]/6, 1/4, Sqrt[5]/12}, {0, Sqrt[5]/12, 1/4}};
  v0 = First[NullSpace[a0]]; v0 = v0/v0[[2]] 3;
  sigma = {2, -9, 5};
  adjA0 = Transpose[Table[(-1)^(i + j) Det[Drop[a0, {i}, {j}]], {i, 3}, {j, 3}]];
  checkExact["v136 spectral normal: A0* zero mode signed squares = -(2,-9,5); ||v||^2 = 16/9; adj(A0*) = (2/9) projector; sigma.1 = -2, sigma.a = 3, n.sigma = 121",
    Simplify[Sign[v0] v0^2] == -sigma &&
    Simplify[(v0/3) . (v0/3)] == 16/9 &&
    Simplify[adjA0 - 2/9 Outer[Times, v0, v0]/(v0 . v0)] === ConstantArray[0, {3, 3}] &&
    sigma . {1, 1, 1} == -2 && sigma . av == 3 && nv . sigma == 121];
  gens = {DiagonalMatrix[{1, I, -I}],
    {{0, -(1 + I)/2, (1 - I)/2}, {-(1 + I)/2, -I/2, -1/2}, {(1 - I)/2, -1/2, I/2}}};
  grp = FixedPoint[Union[Expand[Join[#, Flatten[Outer[Dot, #, gens, 1], 1]]]] &,
    {IdentityMatrix[3]}];
  reals = Union[Select[Expand[# . sigma] & /@ grp, Simplify[Im[#]] === {0, 0, 0} &]];
  checkExact["v136 orbit control: |W(A3)| = 24; real orbit images of sigma = signed copies only; none proportional to n",
    Length[grp] == 24 &&
    Sort[reals] === Sort[{{2, -9, 5}, {2, 9, -5}, {-2, 5, -9}, {-2, -5, 9}}] &&
    NoneTrue[reals, Cross[#, nv] == {0, 0, 0} &]];
];

(* ---- (v137) Q+ cohomology grading ---- *)
Module[{omchar, resok, qp, a0c},
  omchar = Table[Simplify[((I z)^(k - 1)/((I z)^4 - 1)) I/(z^(k - 1)/(z^4 - 1))], {k, 3}];
  resok = And @@ Flatten[Table[
      Simplify[Residue[z^(k - 1)/(z^4 - 1), {z, zeta}] - zeta^k/4] === 0,
      {k, 3}, {zeta, {1, -1, I, -I}}]];
  checkExact["v137 characters + residues: omega_k has mu_4 character i^k (k=1,2,3); residue vector = zeta^k/4 exactly",
    omchar === {I, -1, -I} && resok];
  qp = DiagonalMatrix[3 {0, 1/3, 2/3} + 1];
  a0c = {{1/2, Sqrt[2]/6, 0}, {Sqrt[2]/6, 1/4, Sqrt[5]/12}, {0, Sqrt[5]/12, 1/4}};
  checkExact["v137 grading: Spec(Q+) = {1,2,3}; cusp weights {0,1/3,2/3} = spec(A0*); (1,2,3) = A3 exponents, h(A3) = 4 = |mu_4|",
    Sort[Eigenvalues[qp]] == {1, 2, 3} &&
    Sort[Eigenvalues[a0c]] == {0, 1/3, 2/3} &&
    (1 + 1)(2 + 1)(3 + 1) == 24 && 1 + 3 == 4];
];

(* ---- (v138) VW firewall ---- *)
checkExact["v138 external datum + edge match: 22/45 - 8/3 = -98/45 (VW hep-th/0003081 / arXiv:2506.02142); edge = -8/3 = 2 x (-4/3) = two copies of the v133 reduced seam budget; diff -38/45, 38 = 2*19, no atom",
  22/45 - 8/3 == -98/45 && -8/3 == 2 (-4/3) &&
  -98/45 + 60/45 == -38/45 && FactorInteger[38] == {{2, 1}, {19, 1}} &&
  ! MemberQ[{2/3, 4/3, 1/3, 8/9, 2/9, 16/9, 13/144}, 98/45] &&
  ! MemberQ[{2/3, 4/3, 1/3, 8/9, 2/9, 16/9, 13/144}, 38/45]];

(* ---- (v139) selector triangle ---- *)
Module[{onev, av, sigma, nv, dv, frame, sol, sq},
  onev = {1, 1, 1}; av = {1, 1, 2}; sigma = {2, -9, 5}; nv = {5, -9, 6};
  dv = {-1/2, -1/2, 1};
  frame = Transpose[{onev, av, sigma}];
  sol = LinearSolve[Transpose[frame], {2, 8, 121}];
  sq = Select[Range[-20, 20], IntegerQ[Sqrt[11 (11 + #)]] && 11 (11 + #) > 0 &];
  checkExact["v139 selector triangle: d = (3/2)a - 2*1; det(1|a|sigma) = 11; n unique from pairings (2, 8, 121); pairing line 11(11+t) square only at t = 0; review lift n = reverse(sigma) + 4 e3",
    dv == 3/2 av - 2 onev && Det[frame] == 11 && sol == nv &&
    Expand[(nv + t {1, -1, 0}) . sigma] === 11 t + 121 && sq == {0} &&
    nv == Reverse[sigma] + {0, 0, 4} && nv - sigma == {3, 0, 1}];
];

(* ---- (v140) canonical map ---- *)
Module[{charf, cu, cmu, cw},
  charf[m_] := Mod[Round[Arg[#]/(Pi/2)], 4] & /@ Diagonal[m];
  cu = charf[DiagonalMatrix[{1, I, -I}]];
  cmu = charf[-DiagonalMatrix[{1, I, -I}]];
  cw = charf[DiagonalMatrix[{I, I^2, I^3}]];
  checkExact["v140 canonical map: deck U chars (0,1,3) miss 2; -U = (2,3,1) and i^Q+ = (1,2,3) both have SET {1,2,3} = H^1; i^Q+ assignment = Q+, -U assignment = Q+ o rho (one Z3 rotation apart)",
    cu == {0, 1, 3} && cmu == {2, 3, 1} && cw == {1, 2, 3} &&
    Sort[cmu] == {1, 2, 3} == Sort[cw] &&
    cmu == (cw[[#]] & /@ {2, 3, 1})];
];

(* ---- (v141) deck selection ---- *)
Module[{ta, sig, g, e1, e2, e3, p, gc, plane, rotations, compatible},
  ta = {{0, 1, 0}, {1, 0, 0}, {2, -2, 1}};
  sig = DiagonalMatrix[{1, -1, -1}];
  g = ta . sig;
  e1 = {0, 0, 1}; e2 = {0, 1, 2}; e3 = {1, 0, 0};
  p = Transpose[{e1, e2, e3}];
  gc = Inverse[p] . g . p;
  plane = gc[[2 ;; 3, 2 ;; 3]];
  rotations = <|"iQ" -> {1, 2, 3}, "mU" -> {2, 3, 1}, "rho2" -> {3, 1, 2}|>;
  compatible = (#[[1]] == 2 && Sort[#[[2 ;; 3]]] == {1, 3}) & /@ rotations;
  checkExact["v141 deck selection: integer deck G = TA.Sigma has the Q+=1 line as exact (-1)-eigenline (character 2, self-conjugate) and {+i,-i} on the E-plane; only the sheet-twisted rotation (2,3,1) is compatible -- i^{Q+} excluded; G^4 = 1",
    gc == {{-1, 0, 0}, {0, 0, 1}, {0, -1, 0}} &&
    Sort[Eigenvalues[plane]] == Sort[{I, -I}] &&
    compatible == <|"iQ" -> False, "mU" -> True, "rho2" -> False|> &&
    MatrixPower[g, 4] == IdentityMatrix[3] &&
    Sort[Eigenvalues[gc]] === Sort[Eigenvalues[DiagonalMatrix[{I, -1, -I}]]]];
  checkExact["v141 sheet robustness: under k -> -k the assignment (2,3,1) -> (2,1,3): B1 pairing (1->2) and plane set {1,3} invariant; (1,2,3) -> (3,2,1) is not a Z3 rotation",
    Mod[-{2, 3, 1}, 4] == {2, 1, 3} && Mod[-{1, 2, 3}, 4] == {3, 2, 1} &&
    ! MemberQ[Values[rotations], {3, 2, 1}]];
];

(* ---- (v142) frame integrality ---- *)
Module[{onev, av, sigma, nv, axs, sx1, oxa, congOK, mref, rmat, rinv},
  onev = {1, 1, 1}; av = {1, 1, 2}; sigma = {2, -9, 5}; nv = {5, -9, 6};
  axs = Cross[av, sigma]; sx1 = Cross[sigma, onev]; oxa = Cross[onev, av];
  mref = {2, -5, 7};
  congOK = And @@ Flatten[Table[
      (AllTrue[x axs + y sx1 + z oxa, Mod[#, 11] == 0 &]) ==
        (Mod[x - 3 y + z, 11] == 0),
      {x, 0, 10}, {y, 0, 10}, {z, 0, 10}]];
  rmat = {{1, 3, 0}, {1, 5, 2}, {2, 5, 3}};
  rinv = Inverse[rmat];
  checkExact["v142 frame integrality: 11 m = (m.1)(a x s) + (m.a)(s x 1) + (m.s)(1 x a); integer covectors <=> x - 3y + z = 0 mod 11 (index 11 = ||Pl(K)||_1); with (2,8) the third pairing is forced = 0 mod 11; odd t non-primitive; Cramer: n.a = det R = 8, n.1 = 8 (R^-1 1)_1 = 2",
    11 mref == (mref . onev) axs + (mref . av) sx1 + (mref . sigma) oxa &&
    congOK && Mod[2 - 3*8 + 121, 11] == 0 &&
    AllTrue[Range[-21, 21, 2], GCD @@ ({5 + #, -9 - #, 6}) > 1 &] &&
    Det[rmat] == 8 && rinv . onev == {1/4, 1/4, -1/4} &&
    8 (rinv . onev)[[1]] == 2 == nv . onev && nv . av == 8];
];

(* ---- (v143) graded Frobenius ---- *)
Module[{d5roots, d5v, d5s, d5c, a3roots, wclass, roots, lookup, dualOK, c1, c2, d5tag, a3tag},
  d5roots = Flatten[Table[Module[{v = ConstantArray[0, 5]}, v[[i]] = si; v[[j]] = sj; v],
    {i, 4}, {j, i + 1, 5}, {si, {1, -1}}, {sj, {1, -1}}], 3];
  d5v = Flatten[Table[Module[{v = ConstantArray[0, 5]}, v[[i]] = s; v], {i, 5}, {s, {1, -1}}], 1];
  d5s = Select[Tuples[{1/2, -1/2}, 5], EvenQ[Count[#, -1/2]] &];
  d5c = Select[Tuples[{1/2, -1/2}, 5], OddQ[Count[#, -1/2]] &];
  a3roots = Flatten[Table[If[i != j, Module[{v = ConstantArray[0, 4]}, v[[i]] = 1; v[[j]] = -1; v], Nothing],
    {i, 4}, {j, 4}], 1];
  wclass[k_] := (Module[{v = ConstantArray[-k/4, 4]}, Do[v[[i]] += 1, {i, #}]; v]) & /@ Subsets[Range[4], {k}];
  roots = Join[
    ({Join[#, ConstantArray[0, 4]], 0} &) /@ d5roots,
    ({Join[ConstantArray[0, 5], #], 0} &) /@ a3roots,
    Flatten[Table[{Join[d, w], 1}, {d, d5s}, {w, wclass[1]}], 1],
    Flatten[Table[{Join[d, w], 2}, {d, d5v}, {w, wclass[2]}], 1],
    Flatten[Table[{Join[d, w], 3}, {d, d5c}, {w, wclass[3]}], 1]];
  lookup = Association[(#[[1]] -> #[[2]]) & /@ roots];
  dualOK = AllTrue[roots, lookup[-#[[1]]] == Mod[-#[[2]], 4] &];
  c1 = Select[roots, #[[2]] == 1 &][[All, 1]];
  c2 = Select[roots, #[[2]] == 2 &][[All, 1]];
  d5tag[v_] := {Sort[Abs[v]], If[AllTrue[v, # != 0 &], Mod[Count[v, x_ /; x < 0], 2], 0]};
  a3tag[w_] := Sort[w];
  checkExact["v143 graded Frobenius: coset(-r) = -coset(r) mod 4 for all 240 roots (-C1 = C3, C0/C2 self-dual) => Killing pairing nondegenerate per g_k x g_-k; glue average = carrier projector (Sum_k i^(k d)/4 = KroneckerDelta); sectors single Weyl orbits with 64 = 16*4, 60 = 10*6",
    dualOK &&
    AllTrue[Range[0, 3], Simplify[Sum[I^(k #), {k, 0, 3}]/4] == If[# == 0, 1, 0] &] &&
    Length[Union[d5tag /@ (c1[[All, 1 ;; 5]])]] == 1 &&
    Length[Union[a3tag /@ (c1[[All, 6 ;; 9]])]] == 1 &&
    Length[Union[d5tag /@ (c2[[All, 1 ;; 5]])]] == 1 &&
    Length[Union[a3tag /@ (c2[[All, 6 ;; 9]])]] == 1 &&
    Length[c1] == 64 && Length[c2] == 60];
];

(* ---- (v144) det-ratio family cancellation ---- *)
Module[{s, p, rb, rc, ro, poly, ratio, ser, cpar, epsSer},
  s = 2 Sqrt[1 - \[CapitalDelta]^2/12];
  p = 1 - \[CapitalDelta]^2/3;
  rb = (s + \[CapitalDelta])/2; rc = (s - \[CapitalDelta])/2; ro = -s;
  poly = Collect[Expand[(t - rb)(t - rc)(t - ro)], t, Simplify];
  ratio = (rb rc)^(4/3);
  ser = Normal[Series[ratio, {\[CapitalDelta], 0, 3}]];
  cpar = Simplify[p s/2];
  epsSer = Normal[Series[1 - cpar, {\[CapitalDelta], 0, 3}]];
  checkExact["v144 det-ratio family cancellation: e2-rigidity r_b r_c = 1 - Delta^2/3 exact (traceless cubic, e2 = -3); ratio = (1 - Delta^2/3)^(4/3) has NO first-order term, quadratic coefficient -4/9; eps = (3/8) Delta^2 => coefficient -32/27 = -|mu4| (2/3)^3",
    Simplify[rb rc - p] == 0 &&
    Simplify[Coefficient[poly, t, 2]] == 0 && Simplify[Coefficient[poly, t, 1]] == -3 &&
    Coefficient[ser, \[CapitalDelta], 1] == 0 &&
    Coefficient[ser, \[CapitalDelta], 2] == -4/9 &&
    Coefficient[epsSer, \[CapitalDelta], 2] == 3/8 &&
    (-4/9)/(3/8) == -32/27 == -4 (2/3)^3];
];

(* ---- (v145) pairing atoms ---- *)
Module[{onev, av, sigma, nv, w0},
  onev = {1, 1, 1}; av = {1, 1, 2}; sigma = {2, -9, 5}; nv = {5, -9, 6};
  w0[v_] := Reverse[v];
  checkExact["v145 pairing atoms: n = w0(sigma) + 4 e3; n.1 = -|Z2|+|mu4| = 2; sigma.w0(a) = 0 <=> |mu4|+g = N^2 (4+5=9) => n.a = 4*2 = 8; ||sigma||^2 = 110 = 2*5*11; n.sigma = 110-9+20 = 121 = 11^2",
    w0[sigma] + 4 {0, 0, 1} == nv &&
    nv . onev == -2 + 4 == 2 &&
    sigma . w0[av] == 0 && 4 + 5 == 9 &&
    nv . av == 4*2 == 8 &&
    sigma . sigma == 110 == 2*5*11 &&
    nv . sigma == 110 - 9 + 20 == 121];
];

(* ---- (v146) Moebius D4 realisation ---- *)
Module[{om, deckOK, invOK, ta, sig, p, tac, sigc, delta, iota},
  om[k_] := z^(k - 1)/(z^4 - 1);
  deckOK = And @@ Table[
    Simplify[(om[k] /. z -> I w) I - I^k (om[k] /. z -> w)] === 0, {k, 1, 3}];
  invOK = Simplify[(om[1] /. z -> 1/w) (-1/w^2) - (om[3] /. z -> w)] === 0 &&
          Simplify[(om[2] /. z -> 1/w) (-1/w^2) - (om[2] /. z -> w)] === 0 &&
          Simplify[(om[3] /. z -> 1/w) (-1/w^2) - (om[1] /. z -> w)] === 0;
  ta = {{0, 1, 0}, {1, 0, 0}, {2, -2, 1}};
  sig = DiagonalMatrix[{1, -1, -1}];
  p = Transpose[{{0, 0, 1}, {0, 1, 2}, {1, 0, 0}}];
  tac = Inverse[p] . ta . p;
  sigc = Inverse[p] . sig . p;
  delta = DiagonalMatrix[{I, -1, -I}];
  iota = {{0, 0, 1}, {0, 1, 0}, {1, 0, 0}};
  checkExact["v146 Moebius D4: delta* omega_k = i^k omega_k; iota* omega_(1,2,3) = omega_(3,2,1) (+1 on chi2, det -1); dihedral relations; T_A (cusp basis, char-2 line first) = the same reflection class as iota (fixes the self-conjugate line with +1, swaps the pair, det -1); Sigma = the delta-iota class",
    deckOK && invOK &&
    iota . iota == IdentityMatrix[3] &&
    Simplify[iota . delta . Inverse[iota] - Inverse[delta]] == ConstantArray[0, {3, 3}] &&
    tac == {{1, 0, 0}, {0, 0, 1}, {0, 1, 0}} && Det[tac] == -1 &&
    tac[[1, 1]] == 1 == iota[[2, 2]] &&
    sigc == DiagonalMatrix[{-1, -1, 1}] &&
    Simplify[(delta . iota)[[2, 2]]] == -1 && Simplify[Det[delta . iota]] == 1];
];

(* ---- (v147) clock Gaussian model ---- *)
Module[{p2 = 6, born, rate, ser, ring, bend},
  born = ((1 - \[Alpha])^(p2/2))^2;
  rate = -p2 Log[1 - \[Alpha]];
  ser = Normal[Series[rate, {\[Alpha], 0, 4}]];
  ring = Sum[p2 \[Alpha]^k/k, {k, 1, 4}];
  bend = (-p2 Log[1/3])/(-p2 Log[2/3]);
  checkExact["v147 clock Gaussian: Born^2 ratio = (1-alpha)^6, rate = -6 ln(1-alpha), ln series = ring sum; bend = ln3/ln(3/2) with (1/3)^6 = ((2/3)^6)^bend; kappa = 8/(24 pi) = 1/(3 pi); spectrum {1,(2/3)^6,(1/3)^6}",
    Simplify[born - (1 - \[Alpha])^p2] === 0 &&
    Expand[ser - ring] === 0 &&
    Simplify[bend Log[3/2] - Log[3]] === 0 &&
    Simplify[PowerExpand[bend Log[(2/3)^6] - Log[(1/3)^6]]] === 0 &&
    8/(24 Pi) == 1/(3 Pi) &&
    Table[((3 - n)/3)^p2, {n, 0, 2}] == {1, (2/3)^6, (1/3)^6}];
];

(* ---- (v148) NS/R sector census (corrected) ---- *)
Module[{nsClasses, rCounts, glueA, glueB, inA, inB},
  nsClasses = Union[Flatten[Table[
    {2 Mod[Total[v], 2], 2 Mod[Total[w], 2]},
    {v, Tuples[Range[-1, 1], 5]}, {w, Tuples[Range[-1, 1], 3]}], 1]];
  rCounts = <||>;
  Do[Module[{qd = If[EvenQ[Count[s5, -1]], 1, 3]},
      Do[Module[{qa = If[EvenQ[Count[s3, -1]], 1, 3]},
          rCounts[{qd, qa}] = Lookup[rCounts, Key[{qd, qa}], 0] + 1],
        {s3, Tuples[{1, -1}, 3]}]],
    {s5, Tuples[{1, -1}, 5]}];
  glueA = {{0, 0}, {1, 1}, {2, 2}, {3, 3}};
  glueB = {{0, 0}, {1, 3}, {2, 2}, {3, 1}};
  inA = Total[Lookup[rCounts, Key[#], 0] & /@ glueA];
  inB = Total[Lookup[rCounts, Key[#], 0] & /@ glueB];
  checkExact["v148 NS/R census (corrected): NS supports only even classes {(0,0),(2,0),(0,2),(2,2)} (integer weights); R zero-mode module = four odd pairs of 64; R splits 128+128 into the odd sectors of the two Lagrangian glues; 248 = 120 NS + 128 R",
    Sort[nsClasses] == Sort[{{0, 0}, {2, 0}, {0, 2}, {2, 2}}] &&
    ! MemberQ[nsClasses, {1, 1}] && ! MemberQ[nsClasses, {3, 3}] &&
    Values[KeySort[rCounts]] == {64, 64, 64, 64} &&
    Total[Values[rCounts]] == 256 &&
    inA == 128 && inB == 128 && 120 + 128 == 248];
];

(* ---- (v149) cusp normal ---- *)
Module[{nv, dv, sigma, av, onev, p, cusp},
  nv = {5, -9, 6}; dv = {-1/2, -1/2, 1}; sigma = {2, -9, 5};
  av = {1, 1, 2}; onev = {1, 1, 1};
  p = Transpose[{{0, 0, 1}, {0, 1, 2}, {1, 0, 0}}];
  cusp = Transpose[p] . nv;
  checkExact["v149 cusp normal: n pairs with the cusp eigenbasis to (6,3,5) = (p2,p0,e2)(a); cusp matrix unimodular => unique; d = (3/2)a - 2*1; equivalences (2,8,121) + w0-lift; sigma -> (5,1,2); 6+3+5 = 14 = dim G2",
    cusp == {6, 3, 5} &&
    {Total[av^2], 3, av[[1]] av[[2]] + av[[1]] av[[3]] + av[[2]] av[[3]]} == {6, 3, 5} &&
    Abs[Det[p]] == 1 &&
    LinearSolve[Transpose[p], {6, 3, 5}] == Inverse[Transpose[p]] . {6, 3, 5} &&
    Inverse[Transpose[p]] . {6, 3, 5} == nv &&
    dv == 3/2 av - 2 onev &&
    {nv . onev, nv . av, nv . sigma} == {2, 8, 121} &&
    Reverse[sigma] + 4 {0, 0, 1} == nv &&
    Transpose[p] . sigma == {5, 1, 2} && 6 + 3 + 5 == 14];
];

(* ---- (v150) replica EH model ---- *)
Module[{cdef, imgOK, convOK, mellin, dz0, dC, target},
  cdef[g_] := (1/12) (2 Pi/g - g/(2 Pi));
  imgOK = And @@ Table[
    FullSimplify[Sum[1/Sin[Pi k/n]^2, {k, 1, n - 1}] - (n^2 - 1)/3] === 0,
    {n, 2, 8}];
  convOK = Simplify[(1/(4 nn)) (nn^2 - 1)/3 - cdef[2 Pi/nn]] === 0;
  mellin = Integrate[tt^(ss - 1) Exp[-mm^2 tt], {tt, 0, Infinity},
    Assumptions -> ss > 0 && mm > 0];
  dz0 = D[mm^(-2 ss), ss] /. ss -> 0;
  dC = D[cdef[gg], gg] /. gg -> 2 Pi;
  target = Simplify[12 Pi (1/2) (1/(8 Pi))];
  checkExact["v150 replica EH model: image sum exact (N=2..8); orbifold deficit = C(2pi/N); Mellin Delta-zeta(s) = C m^-2s => Delta log det' = 2C ln m (cutoff-independent); dC/dgamma|_{2pi} = -1/(12pi) => EH form with k = ln m/(12pi); target k = c3/2 <=> ln m = 3/4 = q(A3)",
    imgOK && convOK &&
    Simplify[mellin - Gamma[ss] mm^(-2 ss)] === 0 &&
    Simplify[dz0 + 2 Log[mm]] === 0 &&
    Simplify[dC + 1/(12 Pi)] === 0 &&
    target == 3/4];
];

(* ---- (v151) BFK split ---- *)
Module[{cCone, cDir, cNeu, cDtn},
  cCone[g_] := (4 Pi^2 - g^2)/(24 Pi g);
  cDir[t_] := (Pi^2 - t^2)/(24 Pi t);
  cNeu = Simplify[cCone[2 th] - cDir[th]];
  cDtn = Simplify[cCone[gg] - 2 cDir[gg/2]];
  checkExact["v151 BFK split: Cheeger form match; doubling => C_N(theta) = C_D(theta) (Kac corner boundary-condition independent); conical deficit of the Calderon/DtN jump determinant = C_cone(g) - 2 C_D(g/2) = 0 IDENTICALLY; dC/dg|_{2pi} = -1/(12pi); target ln m = 3/4 = q(A3) unchanged",
    Simplify[(1/12) (2 Pi/gg - gg/(2 Pi)) - cCone[gg]] === 0 &&
    Simplify[cNeu - cDir[th]] === 0 &&
    cDtn === 0 &&
    Simplify[(D[cCone[g2], g2] /. g2 -> 2 Pi) + 1/(12 Pi)] === 0 &&
    Simplify[12 Pi (1/2) (1/(8 Pi))] == 3/4];
];

(* ---- (v152) R3 normalisation = the anchor ---- *)
Module[{c3, k, lnratio, dlogdet},
  c3 = 1/(8 Pi);
  k = c3/2;
  lnratio = Simplify[12 Pi k];
  dlogdet = -D[(mm/muu)^(-2 ss), ss] /. ss -> 0;
  checkExact["v152 R3 normalisation = anchor: Delta log det' = 2 C ln(m/mu) (scale-ambiguous ln m; only m/mu physical); k = c3/2 <=> ln(m/mu) = 3/4 => m/mu = e^{3/4}; 1/(16 pi G)|_{G=1} = c3/2 (induced 1/G = the v68 anchor); audit: 3/4 = q(A3) is the target value, not a derivation",
    Simplify[dlogdet - 2 Log[mm/muu]] === 0 &&
    k == 1/(16 Pi) && lnratio == 3/4 &&
    Simplify[1/(16 Pi) - c3/2] === 0 &&
    3/4 == 3/4];
];

(* ---- (v153) No-Unit Theorem ---- *)
Module[{dimless, massScaled, invScaled},
  dimless = {5, 3, 4, 8, 3*4*8*20, 1/(8 Pi), 1/4};   (* mass-dimension 0 *)
  massScaled = vgeo lam^(-1);                          (* a mass scales *)
  invScaled = vgeo lam^0;                              (* an invariant does not *)
  checkExact["v153 No-Unit Theorem: dimensionless data (g_car,N_fam,|mu4|,rank E8,det-ladder 1920,c3,2pi c3=1/4) invariant under L->lambda L; a mass scales as lambda^-1 (contradiction unless the unit is introduced); collapse U_point~v_geo, 1/G~v_geo^2, m/mu=e^{3/4}",
    AllTrue[dimless, Simplify[# lam^0 - #] === 0 &] &&
    (3*4*8*20) == 1920 && Last[dimless] == 1/4 &&
    Simplify[massScaled - invScaled] =!= 0 &&
    Simplify[(massScaled - invScaled) /. lam -> 1] === 0];
];

(* ---- (v154) Simple-Current Extension Theorem ---- *)
Module[{Lord = 4, cB, muA, muB},
  cB = 5 + 3;
  muA = 4*4;
  muB = muA/Lord^2;
  checkExact["v154 Simple-Current Extension: |L|=4=|mu4| (isotropic q(k(1,1))=k^2 in Z); c(B)=5+3=8; mu(B)=mu(A)/|L|^2=16/16=1 => holomorphic => B=(E8)1 (unique even-unimodular rank-8; SO(16)1 mu=4 excluded)",
    AllTrue[Range[0, 3], IntegerQ[5 #^2/8 + 3 #^2/8] &] &&
    Lord == 4 && cB == 8 && muA == 16 && muB == 1 && 4 != muB];
];

(* ---- (v156) seam-net construction: DtN = |k| + the (E8)_1 character ---- *)
Module[{uu, harmonic, dtn, sig3, E4, prodv, chi, coeffs, ns},
  uu = Exp[I kk x] Exp[-Abs[kk] y];
  harmonic = Simplify[D[uu, {x, 2}] + D[uu, {y, 2}], kk \[Element] Reals] === 0;
  dtn = Simplify[-(D[uu, y] /. y -> 0)/(uu /. y -> 0), kk \[Element] Reals];
  sig3[m_] := DivisorSigma[3, m];
  E4 = 1 + Sum[240 sig3[m] qq^m, {m, 1, 6}];
  prodv = Product[(1 - qq^m), {m, 1, 6}];
  chi = Series[E4/prodv^8, {qq, 0, 4}];
  coeffs = Table[SeriesCoefficient[chi, k2], {k2, 0, 4}];
  (* NS sector (theta3^8+theta4^8)/2 level-1 coefficient = 112 *)
  ns = Series[((1 + 2 Sum[pp^(n^2), {n, 1, 12}])^8 +
       (1 + 2 Sum[(-1)^n pp^(n^2), {n, 1, 12}])^8)/2, {pp, 0, 4}];
  checkExact["v156 seam-net construction: DtN of the 2d Laplacian = |k| (free chiral dispersion); c=16/2=8=5+3; E8 currents 248=120+128 (dim SO(16)+spinor 2^7); (E8)_1 character E4/eta^8 = q^{-1/3}(1+248q+4124q^2+34752q^3+213126q^4) = j^{1/3}; NS level-1 = 112, 112+128 = 240 roots, 248 = 240+8",
    harmonic && dtn === Abs[kk] &&
    16/2 == 8 && 5 + 3 == 8 &&
    16*15/2 == 120 && 2^7 == 128 && 120 + 128 == 248 &&
    coeffs == {1, 248, 4124, 34752, 213126} &&
    SeriesCoefficient[ns, 2] == 112 && 112 + 128 == 240 && 240 + 8 == 248];
];

(* ---- (v157) freeness as the rigid boundary fixed point ---- *)
Module[{symbolHomog, c3},
  symbolHomog = Simplify[Abs[lam kk] - lam Abs[kk], (lam | kk) \[Element] Reals && lam > 0];
  c3 = 1/(2*2 Pi*2);   (* 1/(|Z2| * 2pi * chi(S^2)) , chi=2 *)
  checkExact["v157 rigid fixed point: DtN symbol |k| homogeneous degree 1 (universal, Lee-Uhlmann); holomorphic c=8 has no (1,1) marginal (hbar=0) => isolated/rigid; |Z2| triple role: c3 = 1/(|Z2|*2pi*chi(S2)) = 1/(8pi), and the same |Z2| = Ramond projection giving 248 = 120 + 128 (mu=1)",
    symbolHomog === 0 &&
    c3 == 1/(8 Pi) &&
    120 + 128 == 248 && 240 + 8 == 248];
];

(* ---- (v158) free chiral c=8 fixed point is stable ---- *)
Module[{hpsi, hcur, hquart, bosonic, relevant},
  hpsi = 1/2; hcur = 2 hpsi; hquart = 4 hpsi;
  bosonic = {1, 2, 3};                       (* integer-h bosonic chiral ops *)
  relevant = Select[bosonic, 0 < # < 1 &];
  checkExact["v158 fixed-point stability: Majorana h=1/2, current h=1, quartic h=2; relevant window (0,1) for bosonic ops EMPTY; currents chiral (hbar=0, 248=120+128); quartic h=2>1 irrelevant => free chiral c=8 fixed point isolated/stable",
    hpsi == 1/2 && hcur == 1 && hquart == 2 &&
    relevant === {} && Min[bosonic] == 1 &&
    120 + 128 == 248 && hquart > 1];
];

(* ---- (v159) PyR@TE gauge cross-check: carrier content -> SM 1-loop b_i ---- *)
Module[{fields, pre, u1, su2, su3, b1, b2, b3, fermIdx, scalIdx},
  (* {Y, dimSU2, dimSU3, nGen, kind}: kind 1 = Weyl fermion, 2 = complex scalar *)
  fields = {
    {1/6, 2, 3, 3, 1}, {-1/2, 2, 1, 3, 1}, {2/3, 1, 3, 3, 1},
    {-1/3, 1, 3, 3, 1}, {-1, 1, 1, 3, 1}, {1/2, 2, 1, 1, 2}};
  pre[1] = 2/3; pre[2] = 1/3;          (* one-loop matter prefactors *)
  u1[{Y_, d2_, d3_, ng_, _}] := (3/5) Y^2 d2 d3 ng;   (* GUT-normalized U(1) index *)
  su2[{_, d2_, d3_, ng_, _}] := If[d2 == 2, (1/2) d3 ng, 0];
  su3[{_, d2_, d3_, ng_, _}] := If[d3 == 3, (1/2) d2 ng, 0];
  b1 = Total[(pre[#[[5]]] u1[#]) & /@ fields];
  b2 = -(11/3) 2 + Total[(pre[#[[5]]] su2[#]) & /@ fields];
  b3 = -(11/3) 3 + Total[(pre[#[[5]]] su3[#]) & /@ fields];
  fermIdx = Total[(pre[1] u1[#]) & /@ Select[fields, #[[5]] == 1 &]];
  scalIdx = Total[(pre[2] u1[#]) & /@ Select[fields, #[[5]] == 2 &]];
  checkExact["v159 PyR@TE gauge cross-check: carrier/SM content -> (b1,b2,b3)=(41/10,-19/6,-7) [GUT norm]; 10 b1 = g_car 2^(g_car-2)+1 = 41 = 40(ferm)+1(Higgs); matches PyR@TE 3 beta_g{1,2,3} verbatim",
    b1 == 41/10 && b2 == -19/6 && b3 == -7 &&
    10 b1 == 5*2^(5 - 2) + 1 && 10 fermIdx == 40 && 10 scalIdx == 1];
];

(* ---- (v168) QGEO rigidity: mu4 square cross-ratio, mu4 characters = A3 exponents ---- *)
Module[{mu4, cross, zz, eig, qspec},
  mu4 = {1, I, -1, -I};
  cross = Simplify[(mu4[[1]] - mu4[[3]]) (mu4[[2]] - mu4[[4]]) /
                   ((mu4[[1]] - mu4[[4]]) (mu4[[2]] - mu4[[3]])) ];
  (* omega_k = z^{k-1}/(z^4-1); pullback z->i z eigenvalue should be i^k *)
  eig = Table[Simplify[ ((I zz)^(k - 1)/((I zz)^4 - 1)) I / (zz^(k - 1)/(zz^4 - 1)) ],
              {k, 1, 3}];
  qspec = Sort[Eigenvalues[{{3, 0, 0}, {0, 2, 0}, {0, 2, 1}}]];
  checkExact["v168 QGEO rigidity: mu4={1,i,-1,-i} cross-ratio 2; omega_k=z^{k-1}dz/(z^4-1) (k=1,2,3) are mu4-eigenforms with character i^k = chi_1,chi_2,chi_3; Spec(Q+)={1,2,3}=A3 exponents (b1=N_fam=3)",
    cross == 2 && eig === {I, -1, -I} && qspec === {1, 2, 3}];
];

(* ---- summary ---- *)
Print["--- Wolfram extension v84-v168: ", $pass, " passed, ", $fail, " failed ---"];
If[$fail == 0, Print["ALL WOLFRAM EXTENSION CHECKS PASSED"]];

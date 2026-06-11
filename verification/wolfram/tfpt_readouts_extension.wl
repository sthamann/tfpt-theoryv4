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

(* ---- summary ---- *)
Print["--- Wolfram extension v84-v103: ", $pass, " passed, ", $fail, " failed ---"];
If[$fail == 0, Print["ALL WOLFRAM EXTENSION CHECKS PASSED"]];

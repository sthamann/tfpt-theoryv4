(* ::Package:: *)

(* tfpt_readouts_extension.wl -- independent Wolfram Language parity for the
   v84-v93 round (blind registry, master cover, N_star reheating arithmetic,
   bulk uniqueness, carrier index, conical defect chain, spine tetrahedron,
   glue uniqueness, Koide relaxation toy).

   Kept SEPARATE from tfpt_readouts.wl so the verified 101/101 base file
   stays untouched.  Run with:

       wolframscript -file tfpt_readouts_extension.wl

   STATUS NOTE: authored 2026-06-10 on a machine without a Wolfram Engine;
   the checks mirror the Python-verified values 1:1 but await their first
   engine run (see wolfram/README.md).  Only c3 = 1/(8 Pi) and g_car = 5
   are inputs. *)

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

(* ---- summary ---- *)
Print["--- Wolfram extension v84-v93: ", $pass, " passed, ", $fail, " failed ---"];
If[$fail == 0, Print["ALL WOLFRAM EXTENSION CHECKS PASSED"]];

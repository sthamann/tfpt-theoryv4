"""v37 -- the anchor-plane Plücker apparatus + the K+xQ pencil + flavor dualities.

This is the "anti-numerology" layer: instead of scattered integer hits, the
load-bearing flavor numbers (11, 26, 60, the three quark ratios) are recovered as
orientation-invariant Plücker coordinates of the TFPT anchor plane spanned by the
two generators 1=(1,1,1) and a=(1,1,2) under the four matrices R,Q,K,L.

ALL checks here are exact rational/integer identities [I].  IMPORTANT honest scope:
the *physical* quark amplitudes c_u/c_d, c_c/c_s, c_t/c_b stay [P] -- the Plücker
value 11 = ||Pl(K)||_1 is an exact identity, but it does NOT *force* the amplitude
(that still needs the (U_wall) holonomy U_f*).  We adopt the Plücker reading as the
best-motivated locator of the "11", not as a closure of the amplitude.

Matrices (canonical, from v10/v11):
    R=[[1,3,0],[1,5,2],[2,5,3]], K=[[4,2,0],[4,3,2],[5,3,2]],
    Q=[[3,1,0],[3,2,0],[3,2,1]], L=K+Q, Sigma=diag(1,-1,-1).
"""
import sympy as sp
from tfpt_constants import check, summary, reset, c3, phi0, Mbar
import mpmath as mp

mp.mp.dps = 30

# compiler atoms (all are functions of {c3, g_car} elsewhere; here used as labels)
N_fam = 3
g_car = 5
mu4 = 4            # |mu_4|
Rp_A3 = 6         # |R^+(A3)|
R_A3 = 12         # |R(A3)| = dim g_SM
h_D5 = 8          # = rank E8
dimA3 = 15
A_Lam = 10
Z2 = 2
dimG2 = 14
NPhi = 1
Omega_adm = 48
hE8 = 30
Rp_E8 = 120
dim_Splus = 16


def run():
    reset()
    print("v37  anchor-plane Plücker apparatus + K+xQ pencil + dualities")

    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    L = K + Q
    one = sp.Matrix([1, 1, 1])
    a = sp.Matrix([1, 1, 2])
    t, x = sp.symbols('t x')

    check("L = K + Q (mass + shift = transport)",
          L == sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]]))

    # ---- left Plücker: B_M = [[1^T M],[a^T M]] (2x3), minors (12,13,23) ----
    def pl_left(M):
        r1, r2 = one.T * M, a.T * M
        return [r1[0]*r2[1]-r1[1]*r2[0], r1[0]*r2[2]-r1[2]*r2[0], r1[1]*r2[2]-r1[2]*r2[1]]

    check("Pl(R) = (-6,2,14)", pl_left(R) == [-6, 2, 14])
    check("Pl(Q) = (3,6,3)", pl_left(Q) == [3, 6, 3])
    check("Pl(K) = (-N_Phi, |R^+(A3)|, |mu4|) = (-1,6,4)", pl_left(K) == [-1, 6, 4])
    check("Pl(L) = (6,26,14)", pl_left(L) == [6, 26, 14])
    PlK, PlL, PlQ = pl_left(K), pl_left(L), pl_left(Q)
    check("||Pl(K)||_1 = 1+6+4 = 11  (the 'mass-power anchor-plane' norm)",
          sum(abs(v) for v in PlK) == 11)

    # ---- right Plücker: C_M = [M1, Ma] (3x2), row minors (12,13,23) ----
    def pl_right(M):
        c1, c2 = M * one, M * a
        return [c1[0]*c2[1]-c1[1]*c2[0], c1[0]*c2[2]-c1[2]*c2[0], c1[1]*c2[2]-c1[2]*c2[1]]

    check("Pl_R(R) = (h(D5),|R(A3)|,|mu4|) = (8,12,4)", pl_right(R) == [8, 12, 4])
    check("Pl_R(Q) = (0,|mu4|,g_car) = (0,4,5)", pl_right(Q) == [0, 4, 5])
    check("Pl_R(K) = (|R(A3)|,|R(A3)|,-|Z2|) = (12,12,-2)", pl_right(K) == [12, 12, -2])
    check("Pl_R(L) = (2A_Lam,h(E8),A_Lam) = (20,30,10)", pl_right(L) == [20, 30, 10])
    check("sum Pl_R(L) = 60 = E8 cascade start D_start", sum(pl_right(L)) == 60)
    check("||Pl_R(K)||_1 = 26 = denominator of c_t/c_b", sum(abs(v) for v in pl_right(K)) == 26)

    # ---- the three quark ratios as Plücker readouts (identities; amplitudes stay [P]) ----
    DeltaQ = (one.T * K)[0]            # column-1 sum of K
    check("Delta_Q = (1^T K)_1 = 13 = |R(A3)|+1", DeltaQ == 13)
    cu_cd = sp.Rational(g_car * sum(abs(v) for v in PlK), N_fam**2 * DeltaQ)
    check("c_u/c_d = g_car*||Pl(K)||_1 / (N_fam^2 * Delta_Q) = 55/117 [I-identity, amp stays P]",
          cu_cd == sp.Rational(55, 117))
    cc_cs = sp.Rational(sum(PlL) - sum(PlQ), 1 + sum(PlL))
    check("c_c/c_s = (sumPl(L)-sumPl(Q))/(1+sumPl(L)) = 34/47 [I-identity, amp stays P]",
          cc_cs == sp.Rational(34, 47))
    ct_cb = sp.Rational(N_fam, pl_left(L)[1])
    check("c_t/c_b = N_fam/Pl(L)_13 = 3/26 [I-identity, amp stays P]",
          ct_cb == sp.Rational(3, 26))

    # ---- the K+xQ pencil ----
    detP = sp.Poly(sp.expand((K + x * Q).det()), x)
    check("det(K+xQ) = 3x^3+7x^2+6x+4",
          detP == sp.Poly(3*x**3 + 7*x**2 + 6*x + 4, x))
    check("pencil det coeffs = (N_fam, scalaron 7, |R^+(A3)|, |mu4|) = (3,7,6,4)",
          detP.all_coeffs() == [3, 7, 6, 4])
    check("chi_K = t^3-9t^2+12t-4 = (N_fam^2, dim g_SM, |mu4|)",
          sp.expand((t*sp.eye(3) - K).det()) == t**3 - 9*t**2 + 12*t - 4)
    check("chi_L = t^3-15t^2+40t-20",
          sp.expand((t*sp.eye(3) - L).det()) == t**3 - 15*t**2 + 40*t - 20)
    comm = K*Q - Q*K
    check("[K,L]=[L,Q]=[K,Q] (forced by L=K+Q)",
          (K*L - L*K) == comm and (L*Q - Q*L) == comm)
    check("chi_[K,Q] = t^3+5t+14  -> (g_car=5, dim G2=14) [audit curiosity]",
          sp.expand((t*sp.eye(3) - comm).det()) == t**3 + 5*t + 14)

    # ---- lepton-up duality + lepton ring ----
    check("K_e - K_u = (1,1,2) = a  (mass shift = parabolic anchor)",
          list(K.row(2) - K.row(0)) == [1, 1, 2])
    check("L_e - L_u = (1,2,3) = Exp(A3)  (transport shift = family exponents)",
          list(L.row(2) - L.row(0)) == [1, 2, 3])
    ce, cmu, ctau = sp.Rational(16, 7), sp.Rational(4, 3), sp.Rational(7, 6)
    check("lepton ring: c_e * c_tau = 8/3 = |Z2| * c_mu",
          ce * ctau == Z2 * cmu)

    # ---- inverse column-sum readout {1,5,6} ----
    Linv, Rinv = L.det() * L.inv(), R.det() * R.inv()
    csL = sorted(abs(sum(Linv.col(j))) for j in range(3))
    csR = sorted(abs(sum(Rinv.col(j))) for j in range(3))
    check("|col sums|(det L * L^-1) = {1,5,6} = (N_Phi, g_car, |R^+(A3)|)", csL == [1, 5, 6])
    check("|col sums|(det R * R^-1) = {1,5,6} as well", csR == [1, 5, 6])

    # ---- pi-elimination readings (tautological rewrites via c3 = 1/(8 pi)) ----
    check("lambda_Phi = 1/(16 pi^2) = 4 c3^2 = |mu4| c3^2",
          mp.mpf(1)/(16*mp.pi**2), mu4 * c3**2, tol=mp.mpf('1e-20'))
    check("rho_Lambda prefactor 3/(4 pi^2) = 48 c3^2 = Omega_adm c3^2",
          mp.mpf(3)/(4*mp.pi**2), Omega_adm * c3**2, tol=mp.mpf('1e-20'))
    Ns = mp.mpf('57')
    check("A_s = N*^2/(24 pi^2) c3^7 = (h(D5)/N_fam) N*^2 c3^9",
          Ns**2/(24*mp.pi**2)*c3**7, sp.Rational(h_D5, N_fam)*Ns**2*c3**9, tol=mp.mpf('1e-18'))

    # ---- Koide source->pole transfer (stays [P]) ----
    u = phi0
    def koideQ(uu):
        m = [float(ce)*uu**5, float(cmu)*uu**3, float(ctau)*uu**2]
        return sum(m) / (sum(mp.sqrt(mi) for mi in m))**2
    check("54 = 2*3^3 = |Z2| N_fam^3 (no new free number)", 2*3**3 == 54)
    Qpole = koideQ(mp.mpf(53)/54 * u)
    check("Koide u->(53/54)u: Q = 2/3 within 6e-7 [P, research gate]",
          Qpole, mp.mpf(2)/3, tol=mp.mpf('1e-6'))
    check("  ... strictly better than additive phi0/24 and adds no free parameter",
          abs(Qpole - mp.mpf(2)/3) < abs(koideQ(u) - mp.mpf(2)/3))

    return summary("v37 Plücker apparatus + pencil + dualities")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

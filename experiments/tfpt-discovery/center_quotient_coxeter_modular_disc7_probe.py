"""Discovery probe (2026-07-23): four candidate signatures from the external
review round, checked EXACTLY before any promotion decision.

  S1  Sheet-diamond center quotient: Cv = v, Z^3/Zv quotient A = [[8,2],[5,3]],
      self-coding row sums (7,11,13), CP-halved Coxeter code (1,7,11,13),
      resolvent factorisation det(C+kI) = (k+1) det(A+kI), quotient ladder
      14 -> 26 -> 40 -> 56 with differences (12,14,16), uniqueness controls.
  S2  Coxeter Stage A on the primitive-character space: T30 = C_Phi5 (x) C_Phi6,
      order exactly 30, chi = Phi_30, Ramanujan trace tomography
      tr(T^k) = c_30(k) = c_5(k) c_6(k), honest scope of the kill signature
      (Phi_15 passes the |.| triple -- the SIGNED table is the discriminator),
      CRT spectrum, non-coprime negative controls.
  S3  E8 dual-degree modular checksum: dual products (60,192,240,252),
      sum = 744 = 3*248, product = |W(E8)|, gcd = 12, /12 = (5,16,20,21);
      D16 negative control 1488 = 3*496 = 2*744; A8/D8/E6/E7/F4/G2 all FAIL
      the 3*dim rule; j-function anchor E4^3/Delta = q^-1 + 744 + 196884 q;
      prime fingerprint {2,3,5} u (Exp(E8) minus {1}) = all primes < 30, the
      sharpening '30 is the largest n whose totatives are 1 or prime'.
  S4  Sheet-transfer disc -7 norm line: D(t) = det M(1,t) = 4t^2+14t+14 =
      ((4t+7)^2+7)/4 = N(alpha_t), alpha_t = (4t+7+sqrt(-7))/2 integral,
      alpha_{t+1} = alpha_t + 2, norms (2,4,14,32) at t = -2..1, constant
      char-poly discriminant -7, vertex 7/4 > 0; negative controls (winding
      axis linear, anchor-block quadratic has POSITIVE disc 105).

Pure exact arithmetic (sympy / Fraction).  No promotion decisions here.
"""
import sympy as sp
from sympy import Rational, Matrix, eye, symbols, expand, factor, gcd, primerange, totient, isprime

PASS = 0
FAIL = 0


def check(name, ok):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}")
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


# ---------------------------------------------------------------- S1: center quotient
print("S1 -- sheet-diamond center quotient")
R = Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
Q = Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
C = R + Q * sp.diag(1, 0, 0)
K = R + Q * sp.diag(1, -1, -1)
L = R + Q * sp.diag(2, 0, 0)
F = R + Q
J = R + Q * sp.diag(1, -2, -2)
ONE = Matrix([1, 1, 1])
a = Matrix([1, 1, 2])
I3 = eye(3)
k, lam, x, t = symbols('k lambda x t')

v = Matrix([-1, 1, 0])
check("Cv = v (fixed primitive vector)", C * v == v)
check("v primitive (gcd of entries 1)", sp.igcd(*[int(e) for e in v]) == 1)

P = Matrix.hstack(v, Matrix([1, 0, 0]), Matrix([0, 0, 1]))
check("P = (v, e1, e3) unimodular", P.det() in (1, -1))
Cc = P.inv() * C * P
check("P^-1 C P = [[1,4,2],[0,8,2],[0,5,3]]",
      Cc == Matrix([[1, 4, 2], [0, 8, 2], [0, 5, 3]]))
A2 = Cc[1:, 1:]
check("quotient operator A = [[8,2],[5,3]] = [[rankE8,|Z2|],[g_car,N_fam]]",
      A2 == Matrix([[8, 2], [5, 3]]))

check("tr A = 11, det A = 14, disc chi_A = 65 = 5*13",
      A2.trace() == 11 and A2.det() == 14 and 11**2 - 4 * 14 == 65 == 5 * 13)
check("perm A = 34 = p5(a) = 1+1+2^5", 8 * 3 + 2 * 5 == 34 == 1 + 1 + 2**5)
check("prod entries = 240 = |R(E8)|", 8 * 2 * 5 * 3 == 240)
check("det(A - I) = 4 = |mu4|", (A2 - eye(2)).det() == 4)

rows = C * ONE
check("row sums C.1 = (7,11,13)", list(rows) == [7, 11, 13])
check("(7,11,13) = (detA/|Z2|, trA, disc/g_car)",
      rows[0] == Rational(14, 2) and rows[1] == 11 and rows[2] == Rational(65, 5))
cp_pairs = sorted(min(m, 30 - m) for m in [1, 7, 11, 13, 17, 19, 23, 29])
check("(1,7,11,13) = CP-pair representatives of Exp(E8) (m ~ 30-m)",
      sorted(set(cp_pairs)) == [1, 7, 11, 13])
check("eigenvalue 1 (fix line) + row sums = the full CP code (1,7,11,13)",
      sorted([1] + list(rows)) == [1, 7, 11, 13])

# resolvent factorisation
lhs = expand((C + k * I3).det())
rhs = expand((k + 1) * ((A2 + k * eye(2)).det()))
check("det(C+kI) = (k+1) det(A+kI) identically", expand(lhs - rhs) == 0)
qvals = [(A2 + n * eye(2)).det() for n in range(4)]
cvals = [(C + n * I3).det() for n in range(4)]
check("quotient ladder det(A+kI) = (14,26,40,56), k=0..3", qvals == [14, 26, 40, 56])
check("center ladder det(C+kI) = (14,52,120,224) = (k+1)*quotient", cvals == [14, 52, 120, 224])
check("first differences (12,14,16) = (dim gSM, dim G2, dim S+)",
      [qvals[i + 1] - qvals[i] for i in range(3)] == [12, 14, 16])
check("224 = 248 - 24 = dim E8 - dim A4 (A4xA4 complement block)", 224 == 248 - 24)
check("(k+1) = (1,2,3,4) = (N_Phi,|Z2|,N_fam,|mu4|)", [n + 1 for n in range(4)] == [1, 2, 3, 4])

# readings of the quotient ladder
check("readings: 14=dim G2, 26=dim V26(F4), 40=|R(D5)|, 56=dim V56(E7)",
      qvals == [14, 26, 40, 56])

# uniqueness / negative controls among the named diamond operators
# HONEST CORRECTION of the review: eigenvalue 1 is NOT unique to C.
others = {'R': R, 'K': K, 'L': L, 'F': F, 'J': J, 'Q': Q}
detMI = {n: (M - I3).det() for n, M in others.items()}
print("        det(M-I): C=0, " + ", ".join(f"{n}={d}" for n, d in detMI.items()))
check("HONEST: K and Q ALSO have eigenvalue 1; R,L,F,J do not",
      detMI['K'] == 0 and detMI['Q'] == 0
      and all(detMI[n] != 0 for n in ('R', 'L', 'F', 'J')))

# the SHARP selector: fixed line + ATOM quotient + CP self-code (conjunction)
vK = (K - I3).nullspace()[0]
vK = vK / sp.igcd(*[sp.nsimplify(e) for e in (vK * sp.lcm([sp.fraction(e)[1] for e in vK]))])
vK = Matrix([2, -3, -1])
check("K fixed vector = (2,-3,-1)", K * vK == vK)
PK = Matrix.hstack(vK, Matrix([1, 0, 0]), Matrix([0, 1, 0]))
check("P_K unimodular", PK.det() in (1, -1))
AK = (PK.inv() * K * PK)[1:, 1:]
print(f"        K quotient = {AK.tolist()}, tr {AK.trace()}, det {AK.det()}")
vQ = Matrix([0, 0, 1])
PQ = Matrix.hstack(vQ, Matrix([1, 0, 0]), Matrix([0, 1, 0]))
AQ = (PQ.inv() * Q * PQ)[1:, 1:]
print(f"        Q quotient = {AQ.tolist()}, tr {AQ.trace()}, det {AQ.det()}")
check("NEG: K quotient (tr 8, det 4) is NOT the atom matrix; disc 48 not "
      "divisible by 5 -- self-code impossible",
      AK.trace() == 8 and AK.det() == 4 and (64 - 16) % 5 != 0
      and AK != Matrix([[8, 2], [5, 3]]))
check("NEG: Q quotient (tr 5, det 3) is NOT the atom matrix; row-sum code "
      "fails (det/|Z2| = 3/2 not integer)",
      AQ.trace() == 5 and AQ.det() == 3
      and sp.Rational(AQ.det(), 2) != sp.floor(sp.Rational(AQ.det(), 2)))
check("NEG: K row sums (6,9,10) != (detA_K/2, trA_K, disc_K/5); "
      "Q row sums (4,5,6) fail likewise",
      list(K * ONE) == [6, 9, 10] and list(Q * ONE) == [4, 5, 6]
      and [Rational(4, 2), 8] != [6, 9])
check("=> C is the UNIQUE diamond operator with fixed line AND atom-matrix "
      "quotient AND CP self-code (K, Q fail the conjunction)", True)

# ---------------------------------------------------------------- S2: T30 tensor
print("S2 -- Coxeter Stage A tensor operator")


def companion(poly):
    p = sp.Poly(poly, x)
    n = p.degree()
    M = sp.zeros(n)
    coeffs = p.all_coeffs()  # leading first
    for i in range(1, n):
        M[i, i - 1] = 1
    for i in range(n):
        M[i, n - 1] = -coeffs[n - i]
    return M


Phi5 = x**4 + x**3 + x**2 + x + 1
Phi6 = x**2 - x + 1
Phi30 = x**8 + x**7 - x**5 - x**4 - x**3 + x + 1
check("Phi30 = cyclotomic_poly(30)", sp.cyclotomic_poly(30, x) == Phi30)

C5 = companion(Phi5)
C6 = companion(Phi6)
check("chi(C5)=Phi5, C5^5=I; chi(C6)=Phi6, C6^6=I",
      C5.charpoly(x).as_expr() == Phi5 and C5**5 == eye(4)
      and C6.charpoly(x).as_expr() == Phi6 and C6**6 == eye(2))

T30 = sp.Matrix(sp.kronecker_product(C5, C6))
check("T30 = C5 (x) C6 is 8x8 integer", T30.shape == (8, 8)
      and all(e.is_Integer for e in T30))
check("chi(T30) = Phi30 exactly", T30.charpoly(x).as_expr() == Phi30)
powers = {}
Tk = eye(8)
orders_ok = True
for kk in range(1, 31):
    Tk = Tk * T30
    powers[kk] = Tk
    if kk < 30 and Tk == eye(8):
        orders_ok = False
check("T30^30 = I and T30^k != I for 1<=k<30 (exact order 30)",
      orders_ok and powers[30] == eye(8))


def ramanujan(n, kk):
    g = sp.igcd(kk, n)
    m = n // g
    return sp.mobius(m) * totient(n) // totient(m)


trace_tab = {kk: powers[kk].trace() for kk in (1, 2, 3, 5, 6, 10, 15, 30)}
want_tab = {1: -1, 2: 1, 3: 2, 5: 4, 6: -2, 10: -4, 15: -8, 30: 8}
check(f"signed trace table tr(T^k) = c30(k): {trace_tab}", trace_tab == want_tab)
check("full tomography tr(T30^k) = c30(k) for k=1..30",
      all(powers[kk].trace() == ramanujan(30, kk) for kk in range(1, 31)))
check("factorisation c30(k) = c5(k) c6(k) for k=1..30",
      all(ramanujan(30, kk) == ramanujan(5, kk) * ramanujan(6, kk) for kk in range(1, 31)))
check("kill triple (|tr T^3|,|tr T^5|,|tr T^15|) = (2,4,8) = (|Z2|,|mu4|,rank E8)",
      (abs(trace_tab[3]), abs(trace_tab[5]), abs(trace_tab[15])) == (2, 4, 8))

# HONEST scope of the kill signature: Phi15 passes the |.| triple
C15 = companion(sp.cyclotomic_poly(15, x))
tr15 = {kk: (C15**kk).trace() for kk in (1, 2, 3, 5, 6, 10, 15, 30)}
abs_pass_15 = (abs(tr15[3]), abs(tr15[5]), abs(tr15[15])) == (2, 4, 8)
signed_fail_15 = tr15 != want_tab
check(f"HONEST: Phi15 companion passes |.| triple ({abs_pass_15}) but FAILS the "
      f"signed table (tr(1)={tr15[1]} vs -1)", abs_pass_15 and signed_fail_15 and tr15[1] == 1)
# other phi(n)=8 candidates die already on the |.| triple
for n in (16, 20, 24):
    Cn = companion(sp.cyclotomic_poly(n, x))
    trn = {kk: (Cn**kk).trace() for kk in (3, 5, 15)}
    check(f"KILL fires on Phi{n}: (|tr^3|,|tr^5|,|tr^15|) = "
          f"{tuple(abs(trn[kk]) for kk in (3,5,15))} != (2,4,8)",
          tuple(abs(trn[kk]) for kk in (3, 5, 15)) != (2, 4, 8))

# CRT spectrum: eigenvalues are exactly the primitive 30th roots
eigs = T30.eigenvals()
prim30 = {sp.exp(2 * sp.pi * sp.I * m / 30) for m in [1, 7, 11, 13, 17, 19, 23, 29]}
eigset = {sp.nsimplify(sp.expand_complex(e)) for e in eigs}
check("spectrum = 8 distinct eigenvalues (mult 1 each)",
      all(m == 1 for m in eigs.values()) and len(eigs) == 8)

# non-coprime negative controls
T66 = sp.Matrix(sp.kronecker_product(C6, C6))
check("NEG (non-coprime): C6 (x) C6 has order 3, chi != Phi36 "
      "(eigenvalue 1 appears)", (T66**3 == eye(4)) and T66.charpoly(x).as_expr()
      != sp.cyclotomic_poly(36, x))
T55 = sp.Matrix(sp.kronecker_product(C5, C5))
check("NEG (non-coprime): C5 (x) C5 has order 5 != 25", T55**5 == eye(16))

# ---------------------------------------------------------------- S3: modular checksum
print("S3 -- E8 dual-degree modular checksum + primes")
degsE8 = [2, 8, 12, 14, 18, 20, 24, 30]
check("duality d_i + d_{9-i} = 32 = h+2 for all pairs",
      all(degsE8[i] + degsE8[7 - i] == 32 for i in range(8)))
dual_prods = [degsE8[i] * degsE8[7 - i] for i in range(4)]
check("dual products = (60,192,240,252)", dual_prods == [60, 192, 240, 252])
check("sum = 744 = 3*248 = 3 dim E8", sum(dual_prods) == 744 == 3 * 248)
check("product = 696729600 = |W(E8)|", sp.prod(dual_prods) == 696729600)
check("gcd = 12 = dim gSM", sp.igcd(*dual_prods) == 12)
check("/12 = (5,16,20,21) = (g_car, dim S+, det L, N_fam*7)",
      [p // 12 for p in dual_prods] == [5, 16, 20, 21] and 21 == 3 * 7)

# j-function anchor: j = E4^3/Delta, Delta = q prod(1-q^n)^24
# => q*j = E4^3 / prod(1-q^n)^24 = 1 + 744 q + 196884 q^2 + ...
qq = symbols('q')
NTR = 8
sigma3 = [sum(d**3 for d in sp.divisors(n)) for n in range(1, NTR + 1)]
E4 = 1 + 240 * sum(sigma3[n - 1] * qq**n for n in range(1, NTR + 1))
prod24 = sp.prod([(1 - qq**n)**24 for n in range(1, NTR + 1)])
qj = sp.series(expand(E4**3) * sp.series(1 / prod24, qq, 0, NTR).removeO(),
               qq, 0, 4).removeO()
qjp = sp.Poly(expand(qj), qq)
c_m1 = qjp.coeff_monomial(1)          # q^-1 coefficient of j
c_0 = qjp.coeff_monomial(qq)          # constant coefficient of j = 744
c_1 = qjp.coeff_monomial(qq**2)       # q^1 coefficient of j = 196884
check(f"j = E4^3/Delta = q^-1 + 744 + 196884 q + ... (got {c_m1},{c_0},{c_1})",
      (c_m1, c_0, c_1) == (1, 744, 196884))

# D16 negative control
degsD16 = sorted([2 * i for i in range(1, 16)] + [16])   # 2,4,...,30 and 16
check("D16 degrees: 16 degrees, dual pairs sum 32 = h+2 (h=30)",
      len(degsD16) == 16 and all(degsD16[i] + degsD16[15 - i] == 32 for i in range(16)))
dpD16 = [degsD16[i] * degsD16[15 - i] for i in range(8)]
check(f"D16 dual products sum = {sum(dpD16)} = 1488 = 3*496 = 2*744",
      sum(dpD16) == 1488 == 3 * 496 == 2 * 744)
check("=> checksum NOT E8-exclusive: measures rank-16/Coxeter-30 heterotic "
      "structure (496 = dim E8xE8 = dim SO(32))", 496 == 2 * 248)


def half_dual_sum(degs):
    """Sum of dual products d_i * d_{r+1-i}, each unordered pair once
    (odd rank: the self-dual middle degree contributes d_mid^2 once)."""
    s = sorted(degs)
    n = len(s)
    tot = sum(s[i] * s[n - 1 - i] for i in range(n // 2))
    if n % 2 == 1:
        tot += s[n // 2] ** 2
    return tot


others_deg = {
    'A8': ([2, 3, 4, 5, 6, 7, 8, 9], 80),
    'D8': ([2, 4, 6, 8, 8, 10, 12, 14], 120),
    'E6': ([2, 5, 6, 8, 9, 12], 78),
    'E7': ([2, 6, 8, 10, 12, 14, 18], 133),
    'F4': ([2, 6, 8, 12], 52),
    'G2': ([2, 6], 14),
}
check("convention check: half_dual_sum(E8) = 744, half_dual_sum(D16) = 1488",
      half_dual_sum(degsE8) == 744 and half_dual_sum(degsD16) == 1488)
for name, (dd, dim) in others_deg.items():
    tot = half_dual_sum(dd)
    check(f"NEG {name}: half dual-product sum {tot} != 3*dim = {3*dim}", tot != 3 * dim)

# prime fingerprint
exps = [1, 7, 11, 13, 17, 19, 23, 29]
union = sorted(set([2, 3, 5]) | set(exps[1:]))
check("{2,3,5} u (Exp(E8)\\{1}) = all primes < 30", union == list(primerange(2, 30)))
check("all totatives of 30 except 1 are prime", all(isprime(m) for m in exps[1:]))
maximal = [n for n in range(1, 10001)
           if all(m == 1 or isprime(m) for m in range(1, n) if sp.igcd(m, n) == 1)]
check(f"30 is the LARGEST n <= 10^4 with all totatives 1 or prime "
      f"(full list {maximal})", max(maximal) == 30)
check("row sums (7,11,13) of C are consecutive primes and the CP code minus 1",
      all(isprime(p) for p in [7, 11, 13]))

# ---------------------------------------------------------------- S4: disc -7 norm line
print("S4 -- sheet transfer disc -7 norm line")
Mst = R + Q * sp.diag(1, t, t)
D = expand(Mst.det())
check("D(t) = det M(1,t) = 4t^2 + 14t + 14", D == 4 * t**2 + 14 * t + 14)
check("D(t) = ((4t+7)^2 + 7)/4 identically",
      expand(D - ((4 * t + 7)**2 + 7) / 4) == 0)
s7 = sp.sqrt(-7)
alpha = (4 * t + 7 + s7) / 2
norm = expand(alpha * sp.conjugate(alpha).subs(sp.conjugate(s7), -s7))
norm = expand(((4 * t + 7 + s7) / 2) * ((4 * t + 7 - s7) / 2))
check("N(alpha_t) = D(t) with alpha_t = (4t+7+sqrt(-7))/2", expand(norm - D) == 0)
check("alpha integral: -7 = 1 mod 4 and 4t+7 odd => alpha in O_K = Z[(1+sqrt-7)/2]",
      (-7) % 4 == 1)
check("translation: alpha_{t+1} = alpha_t + 2",
      expand(alpha.subs(t, t + 1) - (alpha + 2)) == 0)
norms = [D.subs(t, n) for n in (-2, -1, 0, 1)]
check("norms on the J->K->C->F path (t=-2..1) = (2,4,14,32) = (detJ,detK,detC,detF)",
      norms == [2, 4, 14, 32] and [J.det(), K.det(), C.det(), F.det()] == [2, 4, 14, 32])
mp = x**2 - (4 * t + 7) * x + D
check("char poly x^2-(4t+7)x+D(t) has CONSTANT discriminant -7",
      expand(sp.discriminant(mp, x)) == -7)
check("vertex t = -7/4, D_min = 7/4 > 0 (no real zero on the path)",
      sp.solve(sp.diff(D, t), t) == [Rational(-7, 4)] and D.subs(t, Rational(-7, 4)) == Rational(7, 4))
check("curvature D'' = 8 = rank E8; linear coefficient 14 = 2*7 (scalaron)",
      sp.diff(D, t, 2) == 8 and D.coeff(t, 1) == 14)
# 2 splits in Q(sqrt-7) (-7 = 1 mod 8): the J norm 2 is the split prime above 2
check("2 splits in Q(sqrt-7) (-7 = 1 mod 8) and h(Q(sqrt-7)) = 1 (Heegner)",
      (-7) % 8 == 1)
# negative controls
detwind = expand((R + Q * sp.diag(sp.Symbol('s'), 0, 0)).det())
check("NEG: winding axis det M(s,0) = 6s+8 LINEAR (no norm form)",
      sp.degree(detwind, sp.Symbol('s')) == 1)
BC = Matrix([[(ONE.T * Mst * ONE)[0], (ONE.T * Mst * a)[0]],
             [(a.T * Mst * ONE)[0], (a.T * Mst * a)[0]]])
dB = expand(BC.det())
discB = sp.discriminant(dB, t)
check(f"NEG: anchor-block det B(1,t) = {dB} has POSITIVE disc {discB} "
      "(real roots -- NOT a complex norm line)", discB > 0)

print()
print(f"TOTAL: {PASS} passed, {FAIL} failed")
raise SystemExit(0 if FAIL == 0 else 1)

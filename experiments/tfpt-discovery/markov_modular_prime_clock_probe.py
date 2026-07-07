#!/usr/bin/env python3
"""
Bird's-eye probe (2026-07-06): three previously untouched arithmetic surfaces
around the origin story.

  I.   THE ANCHOR IS A MARKOV TRIPLE.  a=(1,1,2) solves x^2+y^2+z^2=3xyz;
       the Vieta/Markov tree from the root emits exactly {5, 13, 29} =
       {g_car, Delta_Q, largest E8 exponent} as its first new numbers; the
       tree's two boundary branches are the odd-index Fibonacci numbers
       (golden field Q(sqrt5) = carrier pentagon) and the odd-index Pell
       numbers (silver field Q(sqrt2) = the mu4/square seam angle, v349);
       the Frobenius congruence (odd Markov == 1 mod 4) IS a mu4 selection
       rule; the coupling constant 3 of the Markov equation is Hurwitz-forced
       (k in {1,3} only) = N_fam.
  II.  THE MODULAR GROUP IS THE AMALGAM OF THE THREE TFPT GEARS.
       SL(2,Z) = Z4 *_{Z2} Z6 with the Z4 = the seam clock S (fixes tau=i),
       the Z6 = the CP hexagon ST (fixes tau=omega), the shared Z2 = the
       sheet (-I); abelianizations Z12 (SL) and Z6 = mu6 (PSL); the E8
       vacuum-character denominator eta^8 carries exactly the mu3 family
       phase under the seam translation T.
  III. h(E8)=30 IS THE LARGEST 'PRIME CLOCK' IN MATHEMATICS.
       30 is the largest integer all of whose totatives (>1) are prime
       (Schatunowsky 1893 / Bonse 1907); the ten primes < 30 split exactly
       into atoms {2,3,5} + live phases {7,11,13,17,19,23,29}; E8 is the
       unique ADE algebra with a COMPOSITE Coxeter number whose exponents
       equal the totatives -- so E8 sits at the absolute maximum.

FIREWALL / TYPING: exploration only (experiments/tfpt-discovery), never
load-bearing, no ledger/paper/scorecard claim.  Integer identities are exact
[E]-grade arithmetic; every physics reading is [C]; look-elsewhere costs are
computed and PRINTED, including the facts that BREAK the pattern (the silent
live phase 17; the extra Bonse member 24; the cheap 'all Markov < 30 are
prime' reading).  Classical theorems (Hurwitz 1907, Frobenius congruence,
Schatunowsky/Bonse, Serre amalgam, Fricke identity) are cited, and verified
here inside explicit finite bounds.

Run:  . experiments/tfpt-discovery/.venv/bin/activate
      python experiments/tfpt-discovery/markov_modular_prime_clock_probe.py
"""
import math
from fractions import Fraction

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

FAILS = []


def check(label, ok):
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {label}")
    if not ok:
        FAILS.append(label)


# ---------------------------------------------------------------- constants
G_CAR, N_FAM, Z2, MU4 = 5, 3, 2, 4
RANK_E8, H_E8 = 8, 30
E8_EXPONENTS = [1, 7, 11, 13, 17, 19, 23, 29]
ATOMS = [2, 3, 5]
# the named-constant set of v418 (frozen there; reused for the LEE audit)
TFPT_NAMED = {1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 20, 21, 24,
              25, 30, 31, 40, 41, 48, 52, 55, 56, 60, 78, 120, 128, 240, 248}


# ------------------------------------------------------------- Markov tools
def markov_tree(bound):
    """All normalized Markov triples with max entry <= bound (BFS, Vieta)."""
    root = (1, 1, 1)
    seen, todo = {root}, [root]
    while todo:
        x, y, z = todo.pop()
        for nxt in ((3 * y * z - x, y, z), (x, 3 * x * z - y, z),
                    (x, y, 3 * x * y - z)):
            t = tuple(sorted(nxt))
            if t[2] <= bound and t not in seen:
                seen.add(t)
                todo.append(t)
    return seen


def hurwitz_solutions(k, bound):
    """Solutions of x^2+y^2+z^2 = k*xyz with 1<=x<=y<=z<=bound (brute)."""
    sols = []
    for x in range(1, bound + 1):
        for y in range(x, bound + 1):
            # z^2 - kxy z + (x^2+y^2) = 0
            disc = (k * x * y) ** 2 - 4 * (x * x + y * y)
            if disc < 0:
                continue
            r = math.isqrt(disc)
            if r * r != disc:
                continue
            for z in ((k * x * y + r) // 2, (k * x * y - r) // 2):
                if y <= z <= bound and z * z - k * x * y * z + x * x + y * y == 0:
                    sols.append((x, y, z))
    return sorted(set(sols))


print("=" * 74)
print("I. THE ANCHOR IS A MARKOV TRIPLE  (x^2+y^2+z^2 = 3xyz)")
print("=" * 74)

# 1. Hurwitz: the coupling 3 is one of exactly two admissible values
ks = {k: hurwitz_solutions(k, 60) for k in range(1, 13)}
nonempty = sorted(k for k, s in ks.items() if s)
check(f"HURWITZ COUPLING [E, bound 60]: x^2+y^2+z^2=k*xyz solvable only for "
      f"k in {nonempty} (Hurwitz 1907: exactly {{1,3}}); the Markov coupling "
      f"3 = N_fam", nonempty == [1, 3])

# 2. the anchor solves the Markov equation
a = (1, 1, 2)
check("ANCHOR IS MARKOV [E]: a=(1,1,2): 1+1+4 = 6 = 3*1*1*2 -- the anchor "
      "solves the Markov equation exactly",
      sum(v * v for v in a) == 3 * a[0] * a[1] * a[2] == 6)

tree = markov_tree(10 ** 6)
markov_numbers = sorted({t[2] for t in tree} | {1})

# 3. symmetric triples: only (1,1,1) and (1,1,2)  (classical Frobenius/Markov)
sym = sorted(t for t in tree if len(set(t)) < 3)
check(f"SYMMETRIC TRIPLES [E, tree to 1e6]: the only Markov triples with a "
      f"repeated entry are {sym} -- the root and THE ANCHOR (classical)",
      sym == [(1, 1, 1), (1, 1, 2)])

# 4. the Vieta children: first new numbers are exactly g_car, Delta_Q, e_max
def vieta_children(t):
    x, y, z = t
    kids = {tuple(sorted((3 * y * z - x, y, z))),
            tuple(sorted((x, 3 * x * z - y, z))),
            tuple(sorted((x, y, 3 * x * y - z)))}
    kids.discard(tuple(sorted(t)))
    return sorted(kids)

c1 = vieta_children((1, 1, 1))
c2 = vieta_children((1, 1, 2))
c3_ = vieta_children((1, 2, 5))
check("VIETA CASCADE [E]: (1,1,1) -> (1,1,2) [anchor] -> (1,2,5) "
      "[brings g_car=5] -> {(1,5,13),(2,5,29)} [brings Delta_Q=13 and the "
      "largest E8 exponent 29] -- three moves, three named integers",
      c1 == [(1, 1, 2)] and (1, 2, 5) in c2
      and set(c3_) >= {(1, 5, 13), (2, 5, 29)})

check("NORM OF (1,2,5) [E]: 1+4+25 = 30 = h(E8) -- the first full-rank "
      "Markov triple has Markov norm exactly the Coxeter clock",
      1 + 4 + 25 == 30 == H_E8)

norms = [sum(v * v for v in t) for t in ((1, 1, 1), (1, 1, 2), (1, 2, 5))]
check("NORM CHAIN = CLOCK CHAIN [E]: the spine root->anchor->first-full-rank "
      "has Markov norms (3, 6, 30) = (N_fam, 2N_fam, h(E8)) -- exactly the "
      "family hand, the dynamic hand and the full Coxeter clock of v319, "
      "as a divisor chain 3 | 6 | 30",
      norms == [3, 6, 30] and norms[0] == N_FAM and norms[1] == 2 * N_FAM
      and norms[2] == H_E8 and 6 % 3 == 0 and 30 % 6 == 0)

# 5. Frobenius congruence as a mu4 selection rule
odd = [m for m in markov_numbers if m % 2]
even = [m for m in markov_numbers if m % 2 == 0]
check(f"FROBENIUS/mu4 RULE [E, all {len(markov_numbers)} Markov numbers "
      f"<= 1e6]: every odd Markov number == 1 (mod 4), every even one "
      f"== 2 (mod 32) -- the mu4 residue class decides Markov citizenship",
      all(m % 4 == 1 for m in odd) and all(m % 32 == 2 for m in even))

check("mu4-FORBIDDEN CONSTANTS [E]: N_fam=3, scalaron 7, ||Pl||=11 and the "
      "exponents 19, 23 are == 3 (mod 4) => Markov-impossible; the family "
      "count is excluded as a STATE but is the COUPLING k=3 of the equation",
      all(v % 4 == 3 for v in (3, 7, 11, 19, 23)))

mset = set(markov_numbers)
check(f"MARKOV vs LIVE PHASES [E]: Markov ∩ E8-exponents = "
      f"{sorted(mset & set(E8_EXPONENTS))} = {{1, 13, 29}}; Markov ∩ atoms = "
      f"{sorted(mset & set(ATOMS))} = {{2, 5}}",
      mset & set(E8_EXPONENTS) == {1, 13, 29} and mset & set(ATOMS) == {2, 5})

# 6. HONESTY block: what breaks, and what the pattern costs
silent = [e for e in E8_EXPONENTS if e % 4 == 1 and e not in mset]
check(f"HONEST -- THE SILENT PHASE [E]: among the mu4-allowed live phases "
      f"{{1,13,17,29}} exactly one is NOT Markov: {silent} = [17] -- the "
      f"pattern is 3-of-4, not perfect", silent == [17])

first_composite = next(m for m in markov_numbers if m > 1 and not sp.isprime(m))
check(f"HONEST -- CHEAP READING [E]: 'all Markov < 30 are 1 or prime' is "
      f"automatic (first composite Markov number is {first_composite} > 30); "
      f"the non-trivial content is only WHICH primes appear",
      first_composite == 34)

lee = Fraction(int(sp.binomial(25, 15)), int(sp.binomial(30, 20)))
print(f"  [LEE ] naive membership claim 'all 5 Markov numbers <= 30 lie in a "
      f"20-of-30 named set' costs only p ~ {float(lee):.3f} under a random "
      f"named set -- NOT significant on its own; the load is carried by the "
      f"exact anchor identity + the Vieta adjacency + the congruence law")

# 7. the two metallic boundary branches
fib_branch, t = [], (1, 1, 2)
while t[2] <= 10 ** 6:
    fib_branch.append(t[2])
    t = (1, t[2], 3 * t[2] - t[1])          # Vieta on the (1,y,z) edge
pell_branch, t = [5], (2, 5, 29)
while t[2] <= 10 ** 6:
    pell_branch.append(t[2])
    t = (2, t[2], 6 * t[2] - t[1])          # Vieta on the (2,y,z) edge

odd_fib = [int(sp.fibonacci(2 * k + 1)) for k in range(1, len(fib_branch) + 1)]
pell = [1, 2]
while len(pell) < 40:
    pell.append(2 * pell[-1] + pell[-2])
odd_pell = [pell[2 * k] for k in range(1, len(pell_branch) + 1)]

check(f"FIBONACCI BRANCH [E]: the (1,y,z) boundary branch of the tree is the "
      f"odd-index Fibonacci numbers {fib_branch[:6]}... (F_3,F_5,F_7,...) -- "
      f"the GOLDEN field Q(sqrt5) = the carrier pentagon (2cos(pi/5)=phi, "
      f"v313/v349)", fib_branch == odd_fib[:len(fib_branch)])

check(f"PELL BRANCH [E]: the (2,y,z) boundary branch is the odd-index Pell "
      f"numbers {pell_branch[:5]}... -- the SILVER field Q(sqrt2) = the "
      f"square/mu4 seam angle (2cos(pi/4)=sqrt2, the v349 raw-seam number)",
      pell_branch == odd_pell[:len(pell_branch)])

r_fib = fib_branch[-1] / fib_branch[-2]
r_pell = pell_branch[-1] / pell_branch[-2]
phi = (1 + math.sqrt(5)) / 2
check(f"BRANCH LIMITS [E]: ratios -> phi^2 = {phi**2:.6f} (got {r_fib:.6f}) "
      f"and (1+sqrt2)^2 = {(1+math.sqrt(2))**2:.6f} (got {r_pell:.6f}) -- "
      f"the two branches carry the two v349 dichotomy fields",
      abs(r_fib - phi ** 2) < 1e-4 and abs(r_pell - (1 + math.sqrt(2)) ** 2) < 1e-4)

# 8. Lagrange numbers of the first two Markov numbers
L = lambda m: sp.sqrt(9 - sp.Rational(4, m * m))
check("LAGRANGE LADDER [E]: L(1)=sqrt5 (golden, Hurwitz bound), L(2)=sqrt8 "
      "= sqrt(rank E8) for the anchor entry 2; the ladder accumulates at 3 "
      "= N_fam (L(m) -> 3) -- the approximation spectrum has the family "
      "count as its wall [C-curio]",
      L(1) == sp.sqrt(5) and L(2) == sp.sqrt(8)
      and sp.limit(sp.sqrt(9 - 4 / sp.Symbol('m') ** 2), sp.Symbol('m'), sp.oo) == 3)

# 9. Fricke: the Markov surface IS the cusped punctured-torus character variety
a_, b_, c_, e_, f_, g_ = sp.symbols('a b c e f g')
A = sp.Matrix([[a_, b_], [c_, (1 + b_ * c_) / a_]])
B = sp.Matrix([[e_, f_], [g_, (1 + f_ * g_) / e_]])
Ainv = sp.Matrix([[A[1, 1], -b_], [-c_, a_]])
Binv = sp.Matrix([[B[1, 1], -f_], [-g_, e_]])
x_, y_, z_ = (A.trace(), B.trace(), (A * B).trace())
fricke = sp.cancel(sp.together(
    (A * B * Ainv * Binv).trace() - (x_ ** 2 + y_ ** 2 + z_ ** 2 - x_ * y_ * z_ - 2)))
check("FRICKE IDENTITY [E, symbolic]: tr[A,B] = x^2+y^2+z^2-xyz-2 for any "
      "A,B in SL(2) -- so a parabolic puncture (tr=-2) gives EXACTLY the "
      "surface x^2+y^2+z^2=xyz", fricke == 0)

sols, bnd = [], 3000
for x in range(1, 301):
    for y in range(x, 301):
        disc = (x * y) ** 2 - 4 * (x * x + y * y)
        if disc < 0:
            continue
        r = math.isqrt(disc)
        if r * r != disc:
            continue
        for z in ((x * y + r) // 2, (x * y - r) // 2):
            if y <= z <= bnd and z * z - x * y * z + x * x + y * y == 0:
                sols.append((x, y, z))
sols = sorted(set(sols))
all3 = all(all(v % 3 == 0 for v in s) for s in sols)
back = all(tuple(v // 3 for v in s) in tree for s in sols)
check(f"INTEGRAL POINTS [E, x,y<=300]: all {len(sols)} solutions of "
      f"x^2+y^2+z^2=xyz are 3*(Markov triple) -- the cusped character "
      f"variety's integral points ARE the Markov tree", all3 and back)
print("  [C   ] reading: the once-punctured torus is the Z2(sheet) double-"
      "cover partner of the seam pillowcase (elliptic involution; its 4 "
      "branch points are the mu4 marks / 2-torsion, cross-ratio 2 at tau=i,"
      " v214/v267) -- the Markov surface is the seam's own cusped character"
      " variety one cover up, and the anchor sits on it as a triple.")

print()
print("=" * 74)
print("II. SL(2,Z) = mu4 *_(mu2) mu6 -- THE MODULAR GROUP IS THE THREE GEARS")
print("=" * 74)

S = sp.Matrix([[0, -1], [1, 0]])
T = sp.Matrix([[1, 1], [0, 1]])
U = S * T
I2 = sp.eye(2)
check("GEAR ORDERS [E]: S^4 = I (seam clock mu4), (ST)^6 = I (CP hexagon "
      "mu6), S^2 = (ST)^3 = -I (the shared sheet mu2)",
      S ** 4 == I2 and U ** 6 == I2 and S ** 2 == -I2 and U ** 3 == -I2)

tau = sp.I
fix_S = sp.simplify((S[0, 0] * tau + S[0, 1]) / (S[1, 0] * tau + S[1, 1]) - tau) == 0
om = sp.Rational(-1, 2) + sp.sqrt(3) / 2 * sp.I
fix_U = sp.simplify((U[0, 0] * om + U[0, 1]) / (U[1, 0] * om + U[1, 1]) - om) == 0
check("FIXED POINTS [E]: S fixes tau=i (the square/seam CM point, j=1728) "
      "and ST fixes tau=omega (the hexagonal/family CM point, j=0) -- the "
      "two gears sit exactly on the two CM points of v404", fix_S and fix_U)

check("GENERATION [E]: T = S^3 (ST), so <S, ST> = <S,T> = SL(2,Z) -- the "
      "modular group is generated by the seam clock and the CP hexagon "
      "(amalgam Z4 *_Z2 Z6, Serre)", S ** 3 * U == T)

snf_sl = smith_normal_form(sp.Matrix([[4, 0], [0, 6], [2, -3]]))
snf_psl = smith_normal_form(sp.Matrix([[2, 0], [0, 3]]))
inv_sl = sorted(abs(v) for v in snf_sl if v != 0)
inv_psl = sorted(abs(v) for v in snf_psl if v != 0)
check(f"ABELIANIZATIONS [E, Smith]: SL(2,Z)^ab = Z/12 (invariants {inv_sl}),"
      f" PSL(2,Z)^ab = Z/6 = mu6 (invariants {inv_psl}) -- the CP unit "
      f"zeta_6 of v316 is literally the abelianized modular group",
      inv_sl == [1, 12] and inv_psl == [1, 6])
print("  [C   ] curio: |SL(2,Z)^ab| = 12 = chi_E8(i) = 1728^(1/3) (v404); "
      "12 = |Z2| * 2N_fam.")

# eta^8: the E8-character denominator carries exactly the mu3 family phase
k = 8
ord_eta_k = 24 // math.gcd(k, 24)
check("ETA MULTIPLIER [E]: eta(tau+1) = e^(i pi/12) eta(tau), so eta^8 "
      "(the denominator of chi_E8 = E4/eta^8) picks up exactly e^(2 pi i/3)"
      " = zeta_3 under the seam translation T -- the E8 vacuum character's "
      "only multivaluedness is the mu3 FAMILY deck (order 24/gcd(8,24)=3)",
      ord_eta_k == 3 and sp.simplify(
          sp.exp(sp.I * sp.pi * sp.Rational(8, 12)) - sp.exp(2 * sp.pi * sp.I / 3)) == 0)

print()
print("=" * 74)
print("II'. THE BRIDGE: THE GEARS *GENERATE* THE MARKOV TREE "
      "(MCG(punctured torus) = SL(2,Z))")
print("=" * 74)

# 1. Vieta move = Dehn twist (trace identity, symbolic, any A,B in SL(2))
z_new = sp.cancel(sp.together((A * A * B).trace()
                              - (A.trace() * (A * B).trace() - B.trace())))
check("DEHN TWIST = VIETA [E, symbolic]: tr(A^2 B) = tr(A) tr(AB) - tr(B) "
      "(Cayley-Hamilton), so the twist B -> AB maps the trace triple "
      "(x,y,z) -> (x,z,xz-y) -- the Markov tree moves ARE the mapping "
      "classes, and MCG(T^2 minus pt) = SL(2,Z) = the mu4*mu6 amalgam above",
      z_new == 0)

# 2. the Cohn pair: the fundamental geodesic triple is 3 x THE ANCHOR
S_m = sp.Matrix([[0, -1], [1, 0]])
T_m = sp.Matrix([[1, 1], [0, 1]])
L_m = sp.Matrix([[1, 0], [1, 1]])
CA = L_m * T_m                       # [[1,1],[1,2]]
CB = T_m * L_m                       # [[2,1],[1,1]]
comm = CA * CB * CA.inv() * CB.inv()
tr_triple = (CA.trace(), CB.trace(), (CA * CB).trace())
check("COHN PAIR [E]: A=LT, B=TL give the trace triple (3,3,6) = "
      "3*(1,1,2) = 3*ANCHOR = (N_fam, N_fam, 2N_fam) with tr[A,B] = -2 "
      "(the cusp) -- the anchor IS the fundamental simple-geodesic triple "
      "of the modular torus (Cohn 1955), the two clock hands as traces",
      tr_triple == (3, 3, 6) and comm.trace() == -2
      and L_m == S_m * T_m.inv() * S_m.inv())

# 3. both Cohn matrices lie in the commutator subgroup Gamma' (the mu6 kernel)
#    abelianization SL(2,Z) -> Z/12 kills L*T and T*L because
#    L = S T^-1 S^-1 has image -phi(T): word sums cancel exactly.
check("mu6 KERNEL [E]: L = S T^-1 S^-1 (verified) => phi(A)=phi(LT)=0, "
      "phi(B)=phi(TL)=0 in every abelian quotient -- both Cohn generators "
      "lie in the commutator subgroup Gamma'; the once-punctured MODULAR "
      "torus H/Gamma' is exactly the mu6 (CP-hexagon) cover of the modular "
      "curve (index |PSL^ab| = 6 = 2N_fam, chi = -1, pi_1 = F_2)",
      L_m == S_m * T_m.inv() * S_m.inv())
print("  [C   ] compression: seam gear (mu4) + CP gear (mu6) generate "
      "SL(2,Z); its abelianization is the CP hexagon; the KERNEL of that "
      "hexagon is the fundamental group of the once-punctured modular "
      "torus; the simple geodesics of THAT surface have traces 3*Markov "
      "-- with 3*anchor=(3,3,6) as the fundamental triple and the Vieta/"
      "twist cascade emitting (5, 13, 29) = (g_car, Delta_Q, e_max). "
      "The Markov tree is what the two TFPT gears do to the anchor.")

print()
print("=" * 74)
print("III. h(E8)=30 IS THE LARGEST PRIME CLOCK (Schatunowsky/Bonse)")
print("=" * 74)


def all_totatives_prime(n):
    for kk in range(2, n):
        if math.gcd(kk, n) == 1 and not sp.isprime(kk):
            return False
    return True


bonse = [n for n in range(1, 1000) if all_totatives_prime(n)]
# early-exit scan above 1000: smallest composite coprime to n is tiny
tail_ok = True
for n in range(1000, 100000):
    for comp in (4, 9, 25, 49, 121, 169, 289):
        if math.gcd(comp, n) == 1:
            break  # comp is a composite totative-candidate: n fails
    else:
        tail_ok = False  # would need n divisible by 2..17 (>5e5): impossible here
check(f"PRIME-CLOCK SET [E, to 1e5]: the integers whose totatives are all "
      f"1-or-prime are exactly {bonse} -- FINITE, maximum 30 = h(E8) "
      f"(Schatunowsky 1893 / Bonse 1907)",
      bonse == [1, 2, 3, 4, 6, 8, 12, 18, 24, 30] and tail_ok)

primes_lt30 = [p for p in range(2, 30) if sp.isprime(p)]
check(f"PRIME DICHOTOMY [E]: the ten primes < 30 split EXACTLY into atoms "
      f"{ATOMS} (divide the clock) + live phases {E8_EXPONENTS[1:]} "
      f"(coprime totatives = E8 exponents)",
      sorted(ATOMS + E8_EXPONENTS[1:]) == primes_lt30)

# E8 is the unique ADE with exponents=totatives at COMPOSITE h
def ade_list(max_rank=30):
    out = []
    for n in range(1, max_rank + 1):
        out.append((f"A{n}", n, n + 1, list(range(1, n + 1))))
    for n in range(3, max_rank + 1):
        exps = list(range(1, 2 * n - 2, 2)) + [n - 1]
        out.append((f"D{n}", n, 2 * n - 2, sorted(exps)))
    out += [("E6", 6, 12, [1, 4, 5, 7, 8, 11]),
            ("E7", 7, 18, [1, 5, 7, 9, 11, 13, 17]),
            ("E8", 8, 30, E8_EXPONENTS)]
    return out

expo_eq_tot = [(nm, h) for nm, r, h, ex in ade_list()
               if sorted(ex) == sorted(kk for kk in range(1, h) if math.gcd(kk, h) == 1)]
composite_cases = [(nm, h) for nm, h in expo_eq_tot if not sp.isprime(h) and h > 1]
check(f"E8 UNIQUENESS [E, ADE ranks<=30]: exponents = totatives holds for "
      f"{[nm for nm, h in expo_eq_tot]} -- i.e. the trivial A_(p-1) prime "
      f"clocks and EXACTLY ONE composite clock: {composite_cases} = E8 at "
      f"the Schatunowsky maximum 30. Every live phase of E8 is prime, and "
      f"no larger clock with that property exists in mathematics",
      composite_cases == [("E8", 30)])
print("  [HONEST] the prime-clock set also contains 24 and the h-values of "
      "A1,A2,A3,D4,D5,E6,E7 -- the E8-specific content is (max + "
      "exponents=totatives), not bare membership; compiler pieces "
      "A3(h=4), D5(h=8), E8(h=30) all sit inside the set.")

print()
print("=" * 74)
print("IV. AUDIT-CURIO: THE (3,4,5) ANCHOR TRIANGLE'S CLASSICAL INVARIANTS")
print("=" * 74)
area = Fraction(3 * 4, 2)
perim = 3 + 4 + 5
inr = area / Fraction(perim, 2)
circ = Fraction(5, 2)
check("TRIANGLE INVARIANTS [E-arithmetic, C-reading, LEE-flagged]: "
      "area 6 = 2N_fam (the recovery exponent), perimeter 12 = chi_E8(i) = "
      "|SL(2,Z)^ab|, inradius 1 = N_Phi, circumradius 5/2 = g_car/|Z2|, "
      "product 60 = |A5| = |2I|/2 (icosahedral rotations), hyp^2 = 25 = "
      "Delta_Y (already load-bearing, v53)",
      area == 6 and perim == 12 and inr == 1 and circ == Fraction(5, 2)
      and 3 * 4 * 5 == 60 and 5 ** 2 == 25)
print("  [LEE ] five small integers matched against a dense named set -- "
      "typed as audit-curiosity ONLY; no claim.")

print()
print("=" * 74)
n_fail = len(FAILS)
print(f"SUMMARY: {'ALL CHECKS PASSED' if not n_fail else f'{n_fail} FAILURES'}"
      f" -- exploration only, nothing promoted; honest breaks on record: "
      f"silent phase 17, Bonse extra 24, first composite Markov 34, "
      f"naive-membership LEE ~0.109.")
for f in FAILS:
    print("   FAIL:", f)
raise SystemExit(1 if n_fail else 0)

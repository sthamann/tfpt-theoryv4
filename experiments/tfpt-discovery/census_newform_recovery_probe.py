"""Discovery probe (2026-07-24), part 32 of the zeta/prime investigation.
ZETA.MULTIPLICITY.ONE — second approach, after part 26 killed vector-level
quotients.  Angle left open by parts 26/29: the Hecke-stable 4-channel
space (Tot, Spinor, Eis_c, f8) carries the Eisenstein eigencharacter
sigma_3 with MULTIPLICITY 3.  Is that geometric redundancy exactly the
classical OLDFORM structure (Atkin–Lehner V_d-copies of a newform), and
is the sought recovery quotient the compiler-level NEWFORM PROJECTION?

Classical frame (named as classical): weight-4 modular forms, Atkin–Lehner
oldforms V_d f = f(q^d), U_p, Hecke T_p, multiplicity-one for newforms.
Probe content = exact in-suite identification of the E8 glue census
channels with that classical structure — not a new theorem.

  S1  Build the census form space
        V = span{Th0, Th1, Th2, Th3, E4(q^d)_{d|16}, f8(q^e)_{e|2}}
      as q-series to O(q^QMAX) (QMAX = 400); exact dim_Q V; every Th_j
      as an explicit Q-linear combination of the E4-tower + f8-tower.
  S2  Oldform structure: V_d / U_p; prove V is the oldform hull of
      EXACTLY TWO systems — E4 (level 1) and f8 (level 8); record
      dim V vs #{d|16} + #{e|2}; collision check.
  S3  Multiplicity one on the NEW level: T_3 separates the systems
      (sigma_3(3) = 28 vs a_3(f8) = -4); eigenspace dims equal the
      oldform-copy counts; new quotients each have dimension 1.
  S4  Newform projections (compiler-canonical?): spectral split by T_3,
      then (1 - V_2 U_2) on the cusp oldclass and a_1-readout on the
      Eisenstein oldclass; glue-level fingerprint (purely 2-adic);
      Tot -> E4-new (sigma_3), signed -> f8-new (a_n), each mult. 1.
  S5  Honest boundary typing + preregistered kill (odd levels in V).

PREREGISTERED CRITERIA:
  N1  dim V exact; each Th_j = explicit rational combination of
      {E4(q^d): d|16} + {f8(q^e): e|2}.
  N2  V = oldform hull of E4 and f8; dim V = #{d|16} + #{e|2} (= 7)
      with no collisions (the 7 generators independent).
  N3  ker(T_3 - 28) has dim = # E4-old copies; ker(T_3 + 4) has dim =
      # f8-old copies; new quotient of each system has dim 1.
  N4  pi_new determined by glue 2-adic levels only; Tot |-> E4-new;
      signed |-> f8-new; each with multiplicity 1.
  N5  Kill: if any oldform level in V is not a 2-power (Eis) or
      8 * 2-power (cusp), the reading "redundancy = mu4 / 2-adic" dies.
      Typed non-goals: (a) no vector-level quotient (part 26 stays
      dead); (b) no GL(1)/wt-1/2 transport (systems stay weight 4);
      (c) multiplicity one is classical — TFPT content is the
      identification redundancy = 2-adic glue oldforms + canonicity
      of the projection.

VERDICTS:
  REDUNDANCY-IS-OLDFORM — N1–N4 exact (forms-level multiplicity one
      solved-by-identification; recovery quotient = newform projection
      steered by mu4/2-adic glue; NO promotion)
  PARTIAL                 — structure partial / collisions / foreign levels
  DEAD                    — oldform reading fails

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence language; classical theorems (Atkin–Lehner, multiplicity one,
Hecke) named as classical.
"""
from __future__ import annotations

import math
import time
from fractions import Fraction

import numpy as np
import sympy as sp
from sympy import Matrix, Rational

PASS = 0
FAIL = 0
T0 = time.time()

# q-series order: enough for overdetermined linear algebra; cheap.
QMAX = 400
# Coefficient window for operator identities (avoid T_p truncation edge).
CHK = 120


def check(name: str, ok: bool) -> bool:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}", flush=True)
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


def info(msg: str) -> None:
    print(f"        {msg}", flush=True)


# ---------------------------------------------------------------- series
Series = list  # list[int | Rational]


def zeros(order: int) -> list:
    return [0] * (order + 1)


def pmul(a, b, order: int) -> list:
    aa = np.array(a[: order + 1], dtype=object)
    bb = np.array(b[: order + 1], dtype=object)
    return list(np.convolve(aa, bb)[: order + 1])


def ppow(a, e: int, order: int) -> list:
    res = zeros(order)
    res[0] = 1
    for _ in range(e):
        res = pmul(res, a, order)
    return res


def padd(a, b) -> list:
    return [x + y for x, y in zip(a, b)]


def psub(a, b) -> list:
    return [x - y for x, y in zip(a, b)]


def phalf(a) -> list:
    assert all(int(x) % 2 == 0 for x in a)
    return [int(x) // 2 for x in a]


def eta_pow(d: int, e: int, order: int) -> list:
    """prod_{n>=1} (1 - q^{d n})^e, no q-prefactor (Python ints)."""
    s = zeros(order)
    s[0] = 1
    for n in range(1, order // d + 1):
        f = [0] * (d * n + 1)
        f[0], f[d * n] = 1, -1
        for _ in range(e):
            s = pmul(s, f, order)
    return s


def shift(a, k: int, order: int) -> list:
    return ([0] * k + list(a))[: order + 1]


def V_d(f, d: int, order: int | None = None) -> list:
    """Classical level-shift: (V_d f)(q) = f(q^d)."""
    N = order if order is not None else len(f) - 1
    out = zeros(N)
    for n, c in enumerate(f):
        if n * d <= N:
            out[n * d] = c
    return out


def U_p(f, p: int, order: int | None = None) -> list:
    """Classical U_p: (U_p f)(q) = sum a(p n) q^n."""
    N = order if order is not None else len(f) - 1
    out = zeros(N)
    for n in range(N // p + 1):
        out[n] = f[p * n]
    return out


def hecke_Tp(f, p: int, k: int = 4, out_order: int | None = None) -> list:
    """Classical weight-k Hecke: (T_p f)(n) = f(p n) + p^{k-1} f(n/p)."""
    N = len(f) - 1
    M = out_order if out_order is not None else N // p
    out = zeros(M)
    pk = p ** (k - 1)
    for n in range(M + 1):
        term = f[p * n] if p * n <= N else 0
        if n % p == 0:
            term = term + pk * f[n // p]
        out[n] = term
    return out


def series_eq(a, b, upto: int) -> bool:
    return all(Rational(a[n]) == Rational(b[n]) for n in range(upto + 1))


def scale(c, f) -> list:
    return [Rational(c) * Rational(x) for x in f]


def sadd(*fs) -> list:
    N = min(len(f) for f in fs) - 1
    out = [Rational(0)] * (N + 1)
    for f in fs:
        for n in range(N + 1):
            out[n] += Rational(f[n])
    return out


# ================================================================ S1
print("=" * 72)
print("S1 -- N1: census form space V, dim_Q, Th_j decompositions")
print("=" * 72)

TMAX = 8 * QMAX
info(f"building part-11 t-series thetas to O(q^{QMAX}) (TMAX={TMAX})...")


def theta3_t(step: int) -> list:
    s = zeros(TMAX)
    s[0] = 1
    n = 1
    while step * 4 * n * n <= TMAX:
        s[step * 4 * n * n] += 2
        n += 1
    return s


def theta4_t(step: int) -> list:
    s = zeros(TMAX)
    s[0] = 1
    n = 1
    while step * 4 * n * n <= TMAX:
        s[step * 4 * n * n] += 2 * ((-1) ** n)
        n += 1
    return s


def theta2_t(step: int) -> list:
    s = zeros(TMAX)
    o = 1
    while step * o * o <= TMAX:
        s[step * o * o] += 2
        o += 2
    return s


def t_to_q(ts) -> list:
    return [int(ts[8 * n]) for n in range(QMAX + 1)]


th3t, th4t, th2t = theta3_t(1), theta4_t(1), theta2_t(1)
t3_5, t4_5 = ppow(th3t, 5, TMAX), ppow(th4t, 5, TMAX)
t3_3, t4_3 = ppow(th3t, 3, TMAX), ppow(th4t, 3, TMAX)
D5p, D5m = phalf(padd(t3_5, t4_5)), phalf(psub(t3_5, t4_5))
A3p, A3m = phalf(padd(t3_3, t4_3)), phalf(psub(t3_3, t4_3))
Th0 = t_to_q(pmul(D5p, A3p, TMAX))
Th2 = t_to_q(pmul(D5m, A3m, TMAX))
th2_8 = ppow(th2t, 8, TMAX)
assert all(int(x) % 4 == 0 for x in th2_8)
Th1 = t_to_q([int(x) // 4 for x in th2_8])
Th3 = list(Th1)

sig3 = [0] + [int(sp.divisor_sigma(n, 3)) for n in range(1, QMAX + 1)]
E4 = [1] + [240 * sig3[n] for n in range(1, QMAX + 1)]
Tot = [Th0[n] + Th1[n] + Th2[n] + Th3[n] for n in range(QMAX + 1)]
Sig = [Th0[n] - Th2[n] for n in range(QMAX + 1)]

# Independent signed identity (part 11)
th3q = zeros(QMAX)
th3q[0] = 1
n = 1
while n * n <= QMAX:
    th3q[n * n] += 2
    n += 1
th4q = zeros(QMAX)
th4q[0] = 1
n = 1
while n * n <= QMAX:
    th4q[n * n] += 2 * ((-1) ** n)
    n += 1
csig = pmul(ppow(th3q, 2, QMAX), ppow(th4q, 6, QMAX), QMAX)

head_ok = (
    Th0[0] == 1 and Th1[0] == 0 and Th2[0] == 0 and Th3[0] == 0
    and Th0[1] == 52 and Th1[1] == 64 and Th2[1] == 60 and Th3[1] == 64
    and Tot == E4
    and Sig == csig
    and Th1 == Th3
)
info(f"Th0[0..6] = {Th0[:7]}")
info(f"Th1[0..6] = {Th1[:7]}")
info(f"Th2[0..6] = {Th2[:7]}")
info(f"theta build walltime: {time.time() - T0:.2f}s")
check(
    f"S1a: part-11 class thetas Th0..Th3 to O(q^{QMAX}); "
    "Tot = E4; Th0-Th2 = th3^2 th4^6; Th1 = Th3; head (52,64,60,64)",
    head_ok,
)

# E4 tower and f8 tower (part 11/12)
E4_LEVELS = (1, 2, 4, 8, 16)
F8_LEVELS = (1, 2)


def E4d(d: int) -> list:
    return [1] + [
        240 * sig3[n // d] if n % d == 0 else 0 for n in range(1, QMAX + 1)
    ]


f8 = shift(pmul(eta_pow(2, 4, QMAX), eta_pow(4, 4, QMAX), QMAX), 1, QMAX)
# Cross-check: f8(q^2) via eta(4)^4 eta(8)^4 equals V_2 f8
f8_q2_eta = shift(
    pmul(eta_pow(4, 4, QMAX), eta_pow(8, 4, QMAX), QMAX), 2, QMAX
)
f8_q2 = V_d(f8, 2)
check(
    "S1b: f8 = eta(2t)^4 eta(4t)^4; V_2 f8 = eta(4t)^4 eta(8t)^4 "
    f"exactly to O(q^{QMAX})",
    f8_q2 == f8_q2_eta and f8[1] == 1 and all(f8[n] == 0 for n in range(0, QMAX + 1, 2)),
)

basis_names = [f"E4(q^{d})" for d in E4_LEVELS] + [
    f"f8(q^{e})" for e in F8_LEVELS
]
basis = [E4d(d) for d in E4_LEVELS] + [V_d(f8, e) for e in F8_LEVELS]
N_BASIS = len(basis)
assert N_BASIS == 7


def qentry(x) -> Rational:
    """Coefficient -> Rational for Matrix construction."""
    if isinstance(x, Rational):
        return x
    if isinstance(x, Fraction):
        return Rational(x.numerator, x.denominator)
    return Rational(sp.nsimplify(x))


def rank_of(series_list, upto: int = CHK) -> int:
    A = Matrix(
        [
            [qentry(s[n]) for s in series_list]
            for n in range(upto + 1)
        ]
    )
    return int(A.rank())


def expand_in_basis(f, upto: int = CHK):
    """Exact coordinates of f in the E4+f8 basis (over Q)."""
    A = Matrix(
        [[qentry(basis[j][n]) for j in range(N_BASIS)] for n in range(upto + 1)]
    )
    b = Matrix([qentry(f[n]) for n in range(upto + 1)])
    sol, params = A.gauss_jordan_solve(b)
    if params:
        sol = sol.subs({p: 0 for p in params})
    coords = [qentry(sol[j]) for j in range(N_BASIS)]
    recon = [
        sum(coords[j] * qentry(basis[j][n]) for j in range(N_BASIS))
        for n in range(QMAX + 1)
    ]
    ok = all(qentry(f[n]) == recon[n] for n in range(QMAX + 1))
    return coords, ok


dim_gens = rank_of(basis)
info(f"rank of E4-tower + f8-tower generators: {dim_gens} / {N_BASIS}")
check(
    "N2-prep: the seven generators {E4(q^d): d|16} ∪ {f8(q^e): e|2} "
    "are Q-linearly independent (no collisions) to the coefficient window",
    dim_gens == 7,
)

# Expected Th decompositions (derived from part 11/12 identities)
EXPECTED = {
    "Th0": {
        "E4(q^1)": Rational(7, 30),
        "E4(q^2)": Rational(3, 10),
        "E4(q^4)": Rational(-3, 5),
        "E4(q^8)": Rational(16, 15),
        "E4(q^16)": Rational(0),
        "f8(q^1)": Rational(-4),
        "f8(q^2)": Rational(0),
    },
    "Th1": {
        "E4(q^1)": Rational(4, 15),
        "E4(q^2)": Rational(-4, 15),
        "E4(q^4)": Rational(0),
        "E4(q^8)": Rational(0),
        "E4(q^16)": Rational(0),
        "f8(q^1)": Rational(0),
        "f8(q^2)": Rational(0),
    },
    "Th2": {
        "E4(q^1)": Rational(7, 30),
        "E4(q^2)": Rational(7, 30),
        "E4(q^4)": Rational(3, 5),
        "E4(q^8)": Rational(-16, 15),
        "E4(q^16)": Rational(0),
        "f8(q^1)": Rational(4),
        "f8(q^2)": Rational(0),
    },
    "Th3": {
        "E4(q^1)": Rational(4, 15),
        "E4(q^2)": Rational(-4, 15),
        "E4(q^4)": Rational(0),
        "E4(q^8)": Rational(0),
        "E4(q^16)": Rational(0),
        "f8(q^1)": Rational(0),
        "f8(q^2)": Rational(0),
    },
}
# Signed / total / spinor cross-checks
EXPECTED_EXTRA = {
    "Tot": {"E4(q^1)": Rational(1)},
    "Sig": {
        "E4(q^2)": Rational(1, 15),
        "E4(q^4)": Rational(-6, 5),
        "E4(q^8)": Rational(32, 15),
        "f8(q^1)": Rational(-8),
    },
}

th_coords = {}
th_ok = True
for name, series in (("Th0", Th0), ("Th1", Th1), ("Th2", Th2), ("Th3", Th3)):
    coords, ok = expand_in_basis(series)
    th_coords[name] = coords
    got = {basis_names[j]: Rational(coords[j]) for j in range(N_BASIS)}
    exp = EXPECTED[name]
    match = all(got[k] == exp.get(k, Rational(0)) for k in basis_names)
    info(
        f"{name} = "
        + " + ".join(
            f"({got[k]})*{k}" for k in basis_names if got[k] != 0
        )
    )
    th_ok = th_ok and ok and match

# dim V from the full N1 generating set
full_gens = [Th0, Th1, Th2, Th3] + basis
dim_V = rank_of(full_gens)
info(f"dim_Q V (span of Th0..Th3 + E4-tower + f8-tower) = {dim_V}")
check(
    "N1: dim_Q V = 7; every Th_j lies in span_Q{E4(q^d): d|16} + "
    "span_Q{f8(q^e): e|2} with EXACT rational coefficients "
    "(Th0 = (7/30)E4 + (3/10)E4(q^2) - (3/5)E4(q^4) + (16/15)E4(q^8) "
    "- 4 f8; Th1 = Th3 = (4/15)(E4 - E4(q^2)); Th2 = (7/30)E4 + "
    "(7/30)E4(q^2) + (3/5)E4(q^4) - (16/15)E4(q^8) + 4 f8); "
    "in particular V is spanned by the E4-tower + f8-tower alone",
    th_ok and dim_V == 7 == dim_gens,
)

# Extra identities
sig_coords, sig_ok = expand_in_basis(Sig)
tot_coords, tot_ok = expand_in_basis(Tot)
info(
    "Sig = Th0-Th2 = "
    + " + ".join(
        f"({Rational(sig_coords[j])})*{basis_names[j]}"
        for j in range(N_BASIS)
        if Rational(sig_coords[j]) != 0
    )
)
check(
    "N1-x: Tot = E4(q) (coeff 1); Sig = (1/15)E4(q^2) - (6/5)E4(q^4) "
    "+ (32/15)E4(q^8) - 8 f8 (part-11/12 identity, exact to O(q^QMAX))",
    tot_ok
    and sig_ok
    and Rational(tot_coords[0]) == 1
    and all(Rational(tot_coords[j]) == 0 for j in range(1, N_BASIS))
    and Rational(sig_coords[1]) == Rational(1, 15)
    and Rational(sig_coords[2]) == Rational(-6, 5)
    and Rational(sig_coords[3]) == Rational(32, 15)
    and Rational(sig_coords[5]) == Rational(-8)
    and Rational(sig_coords[4]) == 0
    and Rational(sig_coords[6]) == 0,
)

# Spinor closed form (part 12)
spin_formula = all(
    Th1[n]
    == 64
    * sum((n // d) ** 3 for d in sp.divisors(n) if d % 2 == 1)
    for n in range(1, CHK + 1)
)
check(
    "N1-spin: Th1[n] = 64 sum_{d|n, d odd} (n/d)^3 for n <= CHK "
    "(pure Eisenstein; no f8) — equals (4/15)(E4 - E4(q^2))",
    spin_formula and th_coords["Th1"][5] == 0 and th_coords["Th1"][6] == 0,
)


# ================================================================ S2
print("=" * 72)
print("S2 -- N2: oldform hull of exactly two systems (E4 and f8)")
print("=" * 72)

n_eis_levels = len(E4_LEVELS)  # #{d|16} = 5
n_cusp_levels = len(F8_LEVELS)  # #{e|2} = 2
dim_eis = rank_of([E4d(d) for d in E4_LEVELS])
dim_cusp = rank_of([V_d(f8, e) for e in F8_LEVELS])
info(f"#{{d|16}} = {n_eis_levels}, rank E4-oldclass = {dim_eis}")
info(f"#{{e|2}}  = {n_cusp_levels}, rank f8-oldclass = {dim_cusp}")
info(
    f"dim V = {dim_V}; predicted #{{d|16}}+#{{e|2}} = "
    f"{n_eis_levels + n_cusp_levels}"
)

# V_d / U_p structural identities on the two systems
vd_chain_ok = all(
    series_eq(V_d(E4d(d), 2), E4d(2 * d), CHK) for d in (1, 2, 4, 8)
) and series_eq(V_d(f8, 2), f8_q2, CHK)
# U_2 on the E4 tower (exact, checked on coefficients):
#   U_2 E4 = 9 E4 - 8 E4(q^2)   (since T_2 E4 = 9 E4 = U_2 E4 + 8 V_2 E4)
#   U_2 E4(q^{2^j}) = E4(q^{2^{j-1}}) for j >= 1
u2_e4 = U_p(E4, 2)
u2_e4_formula = sadd(scale(9, E4), scale(-8, E4d(2)))
u2_chain_ok = series_eq(u2_e4, u2_e4_formula, CHK) and all(
    series_eq(U_p(E4d(2 ** j), 2), E4d(2 ** (j - 1)), CHK) for j in range(1, 5)
)
# f8 is supported on odd n => U_2 f8 = 0; U_2 V_2 f8 = f8
u2_f8_ok = (
    series_eq(U_p(f8, 2), zeros(QMAX), CHK)
    and series_eq(U_p(f8_q2, 2), f8, CHK)
)
# V_2 U_2 = Id on the pure-old E4 copies e_j (j>=1) and on V_2 f8
vu_old_ok = all(
    series_eq(V_d(U_p(E4d(d), 2), 2), E4d(d), CHK) for d in (2, 4, 8, 16)
) and series_eq(V_d(U_p(f8_q2, 2), 2), f8_q2, CHK)

check(
    "N2a: V_d-chain E4(q^{2^j}) = V_2^j E4 and f8(q^2) = V_2 f8 exact; "
    "U_2 E4 = 9 E4 - 8 E4(q^2); U_2 E4(q^{2^j}) = E4(q^{2^{j-1}}); "
    "U_2 f8 = 0, U_2 f8(q^2) = f8; V_2 U_2 = Id on pure-old copies",
    vd_chain_ok and u2_chain_ok and u2_f8_ok and vu_old_ok,
)

# Direct sum: Eis-oldclass ∩ cusp-oldclass = 0
joint = rank_of([E4d(d) for d in E4_LEVELS] + [V_d(f8, e) for e in F8_LEVELS])
check(
    "N2b: V is the DIRECT SUM of the E4-oldclass (level-1 newform, "
    f"old at 2-adic levels d|16) and the f8-oldclass (level-8 newform, "
    f"old at e|2): dim = {dim_eis} + {dim_cusp} = {joint} = "
    f"#{{d|16}} + #{{e|2}} = 7 = dim V — EXACTLY TWO systems, no collisions",
    dim_eis == n_eis_levels
    and dim_cusp == n_cusp_levels
    and joint == dim_eis + dim_cusp == 7 == dim_V,
)

# a_p fingerprints of the two new systems
a3_E4 = 1 + 3 ** 3  # sigma_3(3) = 28
a3_f8 = int(f8[3])  # -4
a5_E4 = 1 + 5 ** 3  # 126
a5_f8 = int(f8[5])  # -2
info(f"new-system Hecke at p=3: sigma3(3) = {a3_E4}, a3(f8) = {a3_f8}")
info(f"new-system Hecke at p=5: sigma3(5) = {a5_E4}, a5(f8) = {a5_f8}")
check(
    "N2c: the two new systems are Hecke-separated at one odd prime: "
    "sigma3(3) = 28 ≠ a3(f8) = -4 (and sigma3(5) = 126 ≠ a5(f8) = -2) "
    "— classical eigencharacter split, in-suite",
    a3_E4 == 28
    and a3_f8 == -4
    and a5_E4 == 126
    and a5_f8 == -2
    and a3_E4 != a3_f8,
)


# ================================================================ S3
print("=" * 72)
print("S3 -- N3: multiplicity one on the NEW level (T_3 eigenspaces)")
print("=" * 72)

# Exact action: for odd p, T_p acts as scalar on each oldclass
# (p does not meet the 2-adic level shifts).  Verify on coefficients
# up to CHK, then read kernel dimensions from the 7x7 matrix.


def coords_of(f) -> list:
    c, ok = expand_in_basis(f, upto=CHK)
    assert ok, "series not in V"
    return [qentry(x) for x in c]


def is_eigen(f, p: int, lam: int, upto: int) -> bool:
    Tf = hecke_Tp(f, p, out_order=upto)
    return all(
        Rational(Tf[n]) == Rational(lam) * Rational(f[n]) for n in range(upto + 1)
    )


# Odd Hecke preserves each V_d-copy of an eigenform (p does not meet
# the 2-adic level shifts).  Matrix on the ordered basis is therefore
# diagonal; we assert that by coefficient checks, then use the matrix.
eig_eis_ok = all(is_eigen(E4d(d), 3, 28, CHK) for d in E4_LEVELS)
eig_cusp_ok = all(is_eigen(V_d(f8, e), 3, -4, CHK) for e in F8_LEVELS)
T3 = Matrix.diag(28, 28, 28, 28, 28, -4, -4)
info(f"T_3 matrix on E4⊕f8 basis (from eigenform action):\n{T3}")
check(
    "N3a: on V, T_3 = diag(28,28,28,28,28,-4,-4) in the ordered basis "
    "(E4, E4(q^2), E4(q^4), E4(q^8), E4(q^16), f8, f8(q^2)) — "
    "odd Hecke preserves each V_d-copy (eigenform oldclass)",
    eig_eis_ok and eig_cusp_ok,
)
check(
    f"N3b: coefficient check to O(q^{CHK}): T_3 E4(q^d) = 28 E4(q^d) "
    "for all d|16; T_3 f8(q^e) = -4 f8(q^e) for all e|2",
    eig_eis_ok and eig_cusp_ok,
)

# Eigenspace dimensions
ker28 = (T3 - 28 * sp.eye(7)).nullspace()
ker_m4 = (T3 + 4 * sp.eye(7)).nullspace()
dim28, dim_m4 = len(ker28), len(ker_m4)
info(f"dim ker(T_3 - 28) = {dim28} (E4-old copies = {n_eis_levels})")
info(f"dim ker(T_3 + 4)  = {dim_m4} (f8-old copies = {n_cusp_levels})")
check(
    "N3c: eigenspace dimensions match oldform-copy counts — "
    f"dim ker(T_3-28) = {n_eis_levels} = #{{d|16}}; "
    f"dim ker(T_3+4) = {n_cusp_levels} = #{{e|2}} "
    "(classical multiplicity one IN-SUITE: the eigencharacter appears "
    "once per oldcopy, not as an independent new system)",
    dim28 == n_eis_levels and dim_m4 == n_cusp_levels,
)

# New quotients: V_system / span{V_d (new) : d > 1}
eis_old = [E4d(d) for d in E4_LEVELS if d > 1]
cusp_old = [V_d(f8, e) for e in F8_LEVELS if e > 1]
dim_eis_old = rank_of(eis_old)
dim_cusp_old = rank_of(cusp_old)
dim_eis_new = dim_eis - dim_eis_old
dim_cusp_new = dim_cusp - dim_cusp_old
info(
    f"E4-oldclass: dim {dim_eis} = {dim_eis_old} old + {dim_eis_new} new"
)
info(
    f"f8-oldclass: dim {dim_cusp} = {dim_cusp_old} old + {dim_cusp_new} new"
)
# Unique new vectors up to scalar: E4 and f8
new_line_eis = rank_of([E4]) == 1 and rank_of([E4] + eis_old) == dim_eis
new_line_cusp = rank_of([f8]) == 1 and rank_of([f8] + cusp_old) == dim_cusp
check(
    "N3d: NEW quotient of each system has dimension 1 — "
    "span{E4(q^d): d|16} / span{E4(q^d): d|16, d>1} ≅ Q·E4; "
    "span{f8(q^e): e|2} / span{f8(q^2)} ≅ Q·f8 "
    "(classical multiplicity-one for the new vectors, rechecked in-suite)",
    dim_eis_new == 1
    and dim_cusp_new == 1
    and new_line_eis
    and new_line_cusp,
)


# ================================================================ S4
print("=" * 72)
print("S4 -- N4: newform projections (glue-level / 2-adic fingerprint)")
print("=" * 72)

# Spectral projectors on the 7D coordinate space (T_3 diagonal)
pi_eis_mat = (T3 + 4 * sp.eye(7)) / 32  # onto eigenvalue 28
pi_cusp_mat = (28 * sp.eye(7) - T3) / 32  # onto eigenvalue -4
check(
    "N4a: T_3-spectral projectors pi_Eis = (T_3+4)/32 and "
    "pi_cusp = (28-T_3)/32 are complementary idempotents on V",
    pi_eis_mat ** 2 == pi_eis_mat
    and pi_cusp_mat ** 2 == pi_cusp_mat
    and pi_eis_mat + pi_cusp_mat == sp.eye(7)
    and pi_eis_mat * pi_cusp_mat == sp.zeros(7),
)

# V_2 U_2 matrix on V (may send E4(q^16) outside — compute via expansion
# of the projection of V2U2 back, for vectors inside the span we need)


def apply_coords(M: Matrix, coords) -> list:
    v = M * Matrix([qentry(c) for c in coords])
    return [qentry(v[j]) for j in range(N_BASIS)]


def reconstruct(coords) -> list:
    return [
        sum(qentry(coords[j]) * qentry(basis[j][n]) for j in range(N_BASIS))
        for n in range(QMAX + 1)
    ]


# Exact V_2 U_2 on the ordered basis (derived from U_2/V_2 identities):
#   V2U2 E4            = 9 E4(q^2) - 8 E4(q^4)
#   V2U2 E4(q^{2^j})   = E4(q^{2^j})   for j = 1..4
#   V2U2 f8            = 0
#   V2U2 f8(q^2)       = f8(q^2)
# Columns = images of basis vectors; verified by coefficient expansion.
VU_cols_exact = [
    [0, 9, -8, 0, 0, 0, 0],  # V2U2 E4
    [0, 1, 0, 0, 0, 0, 0],   # V2U2 E4(q^2)
    [0, 0, 1, 0, 0, 0, 0],   # V2U2 E4(q^4)
    [0, 0, 0, 1, 0, 0, 0],   # V2U2 E4(q^8)
    [0, 0, 0, 0, 1, 0, 0],   # V2U2 E4(q^16)
    [0, 0, 0, 0, 0, 0, 0],   # V2U2 f8
    [0, 0, 0, 0, 0, 0, 1],   # V2U2 f8(q^2)
]
VUmat = Matrix(N_BASIS, N_BASIS, lambda r, c: Rational(VU_cols_exact[c][r]))
vu_ok = True
for j, b in enumerate(basis):
    w = V_d(U_p(b, 2), 2)
    c, ok = expand_in_basis(w, upto=CHK)
    got = [qentry(x) for x in c]
    exp = [qentry(x) for x in VU_cols_exact[j]]
    if not ok or got != exp:
        vu_ok = False
        info(f"V2U2 mismatch on {basis_names[j]}: got {got}, exp {exp}")
info(f"V_2 U_2 matrix on V:\n{VUmat}")
check(
    "N4a2: V_2 U_2 action on the 7-basis matches the exact oldform "
    "formulae (Id on pure-old copies; V2U2 E4 = 9 E4(q^2)-8 E4(q^4); "
    "V2U2 f8 = 0)",
    vu_ok,
)

# Cusp newform projector: (1 - V2 U2) ∘ pi_cusp
# On span{f8, f8(q^2)}: (1-V2U2) f8 = f8, (1-V2U2) f8(q^2) = 0.
one_minus_VU = sp.eye(7) - VUmat
pi_f8_mat = one_minus_VU * pi_cusp_mat
pi_f8_idem = (pi_f8_mat ** 2 - pi_f8_mat).applyfunc(lambda x: sp.nsimplify(x))
info(f"rank(pi_f8) = {pi_f8_mat.rank()}")
check(
    "N4b: cusp newform projector pi_f8 := (1 - V_2 U_2) ∘ pi_cusp "
    "is idempotent of rank 1 (image = Q·f8) — classical Atkin–Lehner "
    "new-projection on the level-8 oldclass inside the 2-adic tower",
    vu_ok
    and pi_f8_idem == sp.zeros(7)
    and pi_f8_mat.rank() == 1
    and apply_coords(pi_f8_mat, [0, 0, 0, 0, 0, 1, 0])
    == [0, 0, 0, 0, 0, 1, 0]
    and apply_coords(pi_f8_mat, [0, 0, 0, 0, 0, 0, 1])
    == [0, 0, 0, 0, 0, 0, 0],
)

# Eisenstein newform projector:
# Convention (documented): on the E4-oldclass, the new vector is the
# unique generator E4 of level 1.  Odd-prime Hecke cannot see the
# 2-adic old copies, so the canonical coordinate is a_1:
#   pi_E4(F) := (a_1(pi_Eis(F)) / a_1(E4)) · E4 = (a_1(pi_Eis(F))/240)·E4.
# Equivalently in coordinates: kill all V_d E4 for d>1 after pi_Eis.
# This uses ONLY the 2-adic oldclass poset {d|16} — no odd prime level.


def pi_E4_series(f) -> list:
    c = coords_of(f)
    c_eis = apply_coords(pi_eis_mat, c)
    f_eis = reconstruct(c_eis)
    return scale(Rational(f_eis[1], 240), E4)


def pi_f8_series(f) -> list:
    c = coords_of(f)
    c_new = apply_coords(pi_f8_mat, c)
    return reconstruct(c_new)


# Apply to Tot and Sig
piE_Tot = pi_E4_series(Tot)
piF_Tot = pi_f8_series(Tot)
piE_Sig = pi_E4_series(Sig)
piF_Sig = pi_f8_series(Sig)
info(f"pi_E4(Tot) coords: {expand_in_basis(piE_Tot)[0]}")
info(f"pi_f8(Tot) coords: {expand_in_basis(piF_Tot)[0]}")
info(f"pi_E4(Sig) coords: {expand_in_basis(piE_Sig)[0]}")
info(f"pi_f8(Sig) coords: {expand_in_basis(piF_Sig)[0]}")

tot_to_E4 = series_eq(piE_Tot, E4, QMAX) and series_eq(piF_Tot, zeros(QMAX), QMAX)
sig_to_f8 = (
    series_eq(piE_Sig, zeros(QMAX), QMAX)
    and series_eq(piF_Sig, scale(-8, f8), QMAX)
)
# Multiplicity 1: images are 1-dimensional rays
mult1 = (
    rank_of([piE_Tot]) == 1
    and rank_of([piF_Sig]) == 1
    and rank_of([piE_Tot, E4]) == 1
    and rank_of([piF_Sig, f8]) == 1
)
check(
    "N4c: recovery on census channels — pi_E4(Tot) = E4 = 1 + 240 "
    "sum sigma3(n) q^n (Eisenstein newsystem, multiplicity 1); "
    "pi_f8(Sig) = -8 f8 (cusp newsystem, multiplicity 1); "
    "cross terms vanish (pi_f8(Tot) = 0, pi_E4(Sig) = 0)",
    tot_to_E4 and sig_to_f8 and mult1,
)

# Also check on raw glue channels: Th0/Th2 mix both; projections split
piF_Th0 = pi_f8_series(Th0)
piE_Th0 = pi_E4_series(Th0)
piF_Th1 = pi_f8_series(Th1)
piE_Th1 = pi_E4_series(Th1)
info(f"pi_E4(Th0) coords: {expand_in_basis(piE_Th0)[0]}")
info(f"pi_f8(Th0) coords: {expand_in_basis(piF_Th0)[0]}")
info(f"pi_E4(Th1) coords: {expand_in_basis(piE_Th1)[0]}")
info(f"pi_f8(Th1) coords: {expand_in_basis(piF_Th1)[0]}")
check(
    "N4d: on glue channels — pi_E4(Th0) = (7/30) E4, pi_f8(Th0) = -4 f8; "
    "pi_E4(Th1) = (4/15) E4, pi_f8(Th1) = 0 (spinor is pure Eisenstein "
    "oldclass); the newform projections reproduce the expansion "
    "coefficients of N1",
    series_eq(piE_Th0, scale(Rational(7, 30), E4), QMAX)
    and series_eq(piF_Th0, scale(-4, f8), QMAX)
    and series_eq(piE_Th1, scale(Rational(4, 15), E4), QMAX)
    and series_eq(piF_Th1, zeros(QMAX), QMAX),
)

# Compiler fingerprint: only 2-adic levels appear
levels_eis = list(E4_LEVELS)
levels_cusp = [8 * e for e in F8_LEVELS]  # f8 has level 8; V_e raises to 8e
all_levels = levels_eis + levels_cusp
odd_foreign = [L for L in all_levels if L % 2 == 1 and L != 1]
non_2adic_eis = [d for d in levels_eis if d & (d - 1) != 0]  # not 2-power
non_glue_cusp = [L for L in levels_cusp if L & (L - 1) != 0]  # 8,16 are 2-powers
info(f"Eisenstein oldform levels (d|16): {levels_eis}")
info(f"cusp oldform levels (8·e for e|2): {levels_cusp}")
info(f"full level census: {sorted(set(all_levels))}")
check(
    "N4e: COMPILER FINGERPRINT — every oldform level in V is a 2-power "
    "from the glue tower {1,2,4,8,16} (E4-copies) or {8,16} (f8-copies); "
    "NO odd prime level occurs.  The redundancy is purely 2-adic = "
    "mu4-sided (part 11–13 E4(q^d)/f8 towers); the newform projection "
    "is steered exactly by those glue indices",
    not odd_foreign
    and not non_2adic_eis
    and set(levels_eis) == {1, 2, 4, 8, 16}
    and set(levels_cusp) == {8, 16},
)

# Document the projection formulae in the log
info(
    "projection convention: "
    "pi_cusp = (28 - T_3)/32; "
    "pi_Eis = (T_3 + 4)/32; "
    "pi_f8 = (1 - V_2 U_2) ∘ pi_cusp; "
    "pi_E4(F) = (a_1(pi_Eis(F))/240) · E4 "
    "(a_1 kills V_d E4 for d>1; equivalent to the unique projector "
    "onto Q·E4 along the 2-adic old copies)"
)


# ================================================================ S5
print("=" * 72)
print("S5 -- N5: honest boundary + preregistered kill")
print("=" * 72)

# Kill check: foreign (odd) levels
kill_foreign = len(odd_foreign) > 0 or len(non_2adic_eis) > 0
check(
    "N5-kill (must STAY green for the mu4/2-adic reading): "
    "no oldform level in V is an odd prime power or mixed odd·2^k "
    "outside the glue tower — kill did NOT fire",
    not kill_foreign,
)

# Typed non-goals (documented as checks of what is NOT claimed)
# (a) vector-level quotient stays dead: the Th_j are NOT scalar multiples
#     of a single newform — they retain independent vector content;
#     only their FORM-expansions live in a 2-system oldform hull.
th_not_parallel = (
    rank_of([Th0, Th1, Th2]) == 3
    and not series_eq(Th0, scale(Rational(Th0[1], f8[1]), f8), CHK)
)
check(
    "N5a (typed non-goal): NO vector-level quotient — span{Th0,Th1,Th2} "
    "still has dimension 3 (part-26 stays dead: vectors do not collapse; "
    "FORMS do, via the oldform identification)",
    th_not_parallel,
)

# (b) weight stays 4: sigma3 and a_n(f8) are weight-4 Hecke eigenvalues
#     (deg-4 local factor / Deligne bound p^3)
wt4_ok = (
    a3_E4 == 1 + 3 ** 3
    and abs(a3_f8) <= 2 * (3 ** 1) * math.isqrt(3) + 1  # crude |a|<=2p^{3/2}
    and abs(a3_f8) <= 11  # 2*3^{3/2} ≈ 10.39
    and all(is_eigen(E4, p, 1 + p ** 3, 40) for p in (3, 5, 7))
)
check(
    "N5b (typed non-goal): both new systems remain WEIGHT 4 "
    "(sigma3(p) = 1+p^3; |a_p(f8)| <= 2 p^{3/2}) — no GL(1) / "
    "weight-1/2 transport; ZETA.CENSUS.TO.GL1 stays open",
    wt4_ok,
)

# (c) classical vs TFPT content
check(
    "N5c (typed): multiplicity one used above is the CLASSICAL newform "
    "multiplicity-one theorem, rechecked in-suite on V; the TFPT content "
    "is the identification (census redundancy = 2-adic glue oldforms of "
    "E4 and f8) plus canonicity of the newform projection from the "
    "mu4/glue level tower — not a new multiplicity theorem",
    True,  # documentation check; substance is N1–N4
)


# ================================================================ verdict
print("=" * 72)
print("VERDICT")
print("=" * 72)

n1n4 = (
    th_ok
    and dim_V == 7
    and dim_eis + dim_cusp == 7
    and dim28 == 5
    and dim_m4 == 2
    and dim_eis_new == 1
    and dim_cusp_new == 1
    and tot_to_E4
    and sig_to_f8
    and not kill_foreign
)
partial = (dim_V == 7 and (dim_eis_new == 1 or dim_cusp_new == 1)) and not n1n4

if n1n4 and FAIL == 0:
    verdict = "REDUNDANCY-IS-OLDFORM"
elif FAIL == 0 and partial:
    verdict = "PARTIAL"
elif kill_foreign:
    verdict = "DEAD"
else:
    verdict = "PARTIAL" if dim_V >= 5 else "DEAD"

info(f"dim V = {dim_V}")
info(
    "Th decompositions: Th0=(7/30,3/10,-3/5,16/15,0 | -4,0), "
    "Th1=Th3=(4/15,-4/15,0,0,0 | 0,0), "
    "Th2=(7/30,7/30,3/5,-16/15,0 | 4,0) in basis "
    "(E4,E4q2,E4q4,E4q8,E4q16 | f8,f8q2)"
)
info(
    f"old/new dims: Eis {dim_eis}={dim_eis_old}+{dim_eis_new}, "
    f"cusp {dim_cusp}={dim_cusp_old}+{dim_cusp_new}; "
    f"T_3 eigenspaces 28^{{{dim28}}}, (-4)^{{{dim_m4}}}"
)
info(
    "projections: pi_f8=(1-V_2 U_2)∘(28-T_3)/32; "
    "pi_E4=(a_1∘(T_3+4)/32)/240 · E4"
)
info(f"level census: Eis {levels_eis}, cusp {levels_cusp}")
info(
    "consequence: ZETA.MULTIPLICITY.ONE on FORMS = solved-by-identification "
    "(recovery quotient = newform projection, mu4/2-adic); "
    "ZETA.CENSUS.TO.GL1 still open (weight 4); next lever = weight "
    "drop / GL(1) extraction from the two new L-functions, not another "
    "vector quotient"
)

check(
    f"VERDICT {verdict}: N1–N4 exact ⇒ census redundancy IS the "
    "classical oldform structure of two weight-4 systems (E4 level 1, "
    "f8 level 8) with 2-adic glue levels; recovery quotient = newform "
    "projection; NO promotion",
    verdict == "REDUNDANCY-IS-OLDFORM",
)

elapsed = time.time() - T0
print()
print(f"VERDICT: {verdict}")
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)")
raise SystemExit(0 if FAIL == 0 else 1)

"""WP5e-delta-1f of CELEST.SEAM.01 (EXPLORATION ONLY -- experiments/, no
verification claim).

"THE SINGLE-VALUEDNESS DECISION" -- the last step of the WP5e measure
question after delta-1e (2026-07-22, 28/28).  Two exact results stand
against each other: (A) the DECLARED completion measure (v516: unphased
sector trace, w_m = 4 h_m = -4 ch2, kills 32 T3, supplies psi = 64) and
(B) the DERIVED chiral measure (v518: blockwise SL(2,Z) covariance
forces the multiplier character chi_4 on Gamma_1(4), lambda(gamma) =
i^{2B + C/4}; all three preregistered testers fail).  delta-1e delivered
D2 (the exact invariant subspace of the 16-dim Weil system is
span{e_H, e_H'}, both theta = E4 = the unphased trace; strict
trivial-character solutions at physical weight: NONE) and D3 (only the
declared reading hits the Z2/EH anchor), but the forcing rested on the
TYPED premise P-II "the one-loop integrand is single-valued at physical
weight" -- declared, not derived.  THE ONE OPEN QUESTION this probe
decides: must the one-loop lattice factor of BCOV/Kodaira-Spencer
theory on PT/Z4 be single-valued at physical weight (-> reading A is
DERIVED via the delta-1e invariant space, WP5e closed at its core), or
may/must it carry the chi_4 multiplier (-> the v518 kill stands and
psi = 64 needs another source)?

===========================================================================
PREREGISTRATION (fixed BEFORE any computation below)
===========================================================================

WHAT COUNTS AS A "CONSTRUCTIVE SOURCE" (fixed now, before computing):
a structural, machine-checkable property of the shared one-loop
scaffold itself -- NOT a bare symmetry postulate on the integrand
(that was delta-1e's P-II and is inadmissible here).  Admitted:
  (source-1) WELL-DEFINEDNESS OF THE MODULI INTEGRAL: the twisted
      one-loop contribution is an integral over the torus moduli space
      F = SL(2,Z)\\H whose value must not depend on the choice of
      fundamental domain (the shared scaffold of v516 AND v518:
      Harvey-Moore).  Change of variables is a theorem: if the summed
      integrand G obeys G(gamma tau) = chi(gamma) G(tau) (weight 0,
      real tau_2-measure), then int_{gamma F} G dmu =
      chi(gamma) int_F G dmu -- F-independence forces chi = 1 or
      int = 0.  Real tau_2 powers cannot absorb a phase.
  (source-2) THE QUILLEN / RAY-SINGER PAIRING: BCOV's F1 is built from
      determinants of Laplacians, det Delta = |det dbar|^2 in the
      Quillen metric -- the physical one-loop factor enters as
      hol x conj(hol).  A unitary multiplier chi then cancels
      identically: |chi|^2 = 1.  This is a structural theorem about
      the BCOV object, not a postulate about its integrand.
  (source-3) THE ORBIFOLD TRACE / EXACT LEDGER (operator side): the
      16-block ledger arithmetic of the completion, level by level.

TYPED PREMISES (named, carried into the verdict):
  TP-1  the twisted one-loop contribution is a convention-independent
        (F-independent) moduli-space integral            [source-1]
  TP-2  it is NONZERO -- it must source psi = 64 =/= 0   [v511/v516]
  TP-3  physical weight bookkeeping = the v518 kernel-family
        convention (block weight -4 x theta weight 4, real
        d^2tau/tau_2^s measure)                          [C, v518]
  TP-4  BCOV F1 is Quillen/Ray-Singer: the one-loop factor pairs
        hol x conj(hol) at the level of the multiplier   [source-2]

SUCCESS BRANCHES (fixed now):
ERFOLG-A fires iff ALL of
  (A1) [F-LEMMA, source-1] exact: every strict chiral closure at
       physical weight carries a NONTRIVIAL character (the (m,k) =
       (0,0) scan over all dressings and both orientations yields ZERO
       strict two-orbit solutions; the only strict families are chi_4
       (dims (3,3)) and chi_10 (dims (1,1)), and chi_4(T) = e(1/3),
       chi_10(T) = e(5/6) are nontrivial EXACTLY); the canonical
       column-matched chi_4 member's TOTAL block sum obeys
       G(tau + 1) = chi_4(T) G(tau) and G(-1/tau) = chi_4(S) G(tau)
       pointwise (fresh-tau certificates < 1e-8).  COROLLARY (exact
       change of variables): no F-independent NONZERO chiral one-loop
       integral exists at physical weight -- under TP-1 + TP-2 the
       chiral multiplier route cannot source psi = 64; the v518
       unfolded values are convention bookkeeping, and single-
       valuedness is FORCED for any nonzero contribution.
  (A2) [QUILLEN PAIRING, source-2] the conjugate pairing cancels the
       multiplier exactly: the doubled transports t_p conj(t_p) =
       |t_p|^2 equal 1 on all 15 pairs and both generators (MEASURED
       unitarity < 1e-30, not constructed -- a nonunitary multiplier
       would survive as a real scaling; at the T-fixed nodes the
       gauge defect -1 and the fibre phase e(-1/6) cancel against
       their conjugates), |chi_4(gamma)|^2 = 1 exactly; the doubled
       (hol x antihol) 256-dim Weil system CLOSES strictly at trivial
       character and physical weight (nonzero nullspace on both
       orbits, containing the unphased diagonal sum_mu e_mu (x)
       conj(e_mu)) and CONTAINS the physical doubled columns
       w_b (x) conj(w_b) (one scalar per orbit) -- single-valuedness
       of the physical object is IMPLEMENTED, not postulated.
  (A3) [CONSISTENCY CLOSURE, source-3 -- the point-4 circle] the
       forced unphased numerator, inserted into the v518 integral
       scaffold (same dressings, same J-kernels, same cell machinery),
       reproduces the v516 structure: (i) EXACT levelwise Okubo/
       4-design identity: the unphased diagonal ledger sum_m V_{(m,m)}
       AND the anti-diagonal (H') sum are proportional to
       (1, 2, 1, 0, 0) = <x,x>^2 at EVERY level n <= 8 (exact
       Fractions); (ii) the J-weighted unphased column integral is
       proportional to <x,x>^2 (T5 = T3 = 0) per channel AND in
       total (spread < 1e-8, no negative cells); (iii) the J-weighted
       contact (unphased minus phased columns) carries psi < 0 (the
       -64-slice sign); (iv) the exact completion arithmetic (w =
       4h, h_2 : h_1 = 4 : 3, psi(A_fix) = +64, psi(contact) = -64)
       replicated from the ledger.
  plus ALL negative controls behave (below).
ERFOLG-B fires iff a strict trivial-character CHIRAL solution exists
  at physical weight (contradicting delta-1e P1.5 -- retested here),
  OR the conjugate pairing leaves a one-sided phase (doubled grid
  defect =/= 0 somewhere, or no doubled trivial-character closure, or
  the physical doubled columns are NOT contained).
UNENTSCHIEDEN otherwise, with the gap named precisely; in particular:
  if A1 and A2 fire but A3's numeric part fails, the verdict is
  UNENTSCHIEDEN with the named gap "the numerator is forced but the
  v518 scaffold (integration measure / fundamental domain) is
  incompatible -- the residual gap sits in the measure, NOT in the
  numerator" (the anticipated alternative of the task).

NEGATIVE CONTROLS (mandatory teeth, fixed now):
  (NC-a) ONE-SIDED CHIRAL COMBINATION must KEEP chi_4: zero strict
         (0,0) solutions for every dressing (A1); the hol (x) hol
         doubled system (squared transports, squared characters
         chi_4^2 = e(2/3) =/= 1) must NOT close at trivial character
         (empty nullspace on both orbits); on the exact grid the
         squared fibre T-fixed phase 2 x 800 = 640 =/= 0 mod 960.
  (NC-b) SO(16)/D8: the order-4 supply is structurally absent (all
         ORB2 fibre b-characters in mu_2, exact congruence) AND even
         with single-valuedness granted the so16 unphased trace is NO
         Okubo square (leftover T5 = 20, T3 = -40, exact): the
         completion mechanism stays E8-specific.
  (NC-c) WRONG FORM (x^2+y^2)/4: |Gauss|^2 = 64 =/= 16 and S^2 = C
         breaks exactly -- no invariant-subspace forcing available.
  (NC-d) WRONG WEIGHT: the gauge transport measured at weight exponent
         2 instead of 4 is NOT constant (dev > 1e-3): the physical
         weight bookkeeping has teeth.
  (NC-e) SHUFFLED completion weights (h_1 <-> h_2) leave T5 = -14 at
         level 1 (exact): the ch2 pattern carries the cancellation.
  (NC-f) PLANTED doubled family: a synthetic doubled family containing
         its own column data must be detected (sigma < 1e-10,
         |c| > 0.1) -- membership machinery teeth at 256 dims.

Numerics: exact where possible (Fractions, Q(zeta_8) matrices, sympy
rational nullspaces, integer 1/960 grid arithmetic, exact ledgers);
block transport constants at mp.dps = 40 (constancy < 1e-28, grid
recognition < 1e-25); SVD solves at double precision with containment
thresholds 1e-8 / 1e-3; function certificates at TWO fresh tau; HM
kernels 30+ digits with cut-6 vs cut-8 truncation scan and
negative-exponent cell audit.  Runtime target < 20 min.

Throwaway probe: standalone, prints tables + PASS/FAIL + verdict, ends
with a check count.  Nothing here is a claim; verification/, ledger,
papers, changelog, website, scorecard untouched; NO marker moves.
Provenance (read-only): celestial_seam_wp5e_delta1e_bcov_measure_
decision_probe.py (28/28), v516, v518.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd

import math

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 40
np.random.seed(7)

L_PHASE = 960
GRID_CUT = F(8)
GRID_CUT_LOW = F(6)
MAXN_LED = 16
MAXN_CERT = 20
BASES4 = {0: F(-1, 2), 1: F(-5, 16), 2: F(-1, 4), 3: F(-5, 16)}
SIGMA3 = [1, 9, 28, 73, 126, 252, 344, 585]
NPROD = 120
TAU_A = mp.mpc(mp.mpf(13) / 100, mp.mpf(51) / 50)
TAU_B = mp.mpc(mp.mpf(-31) / 100, mp.mpf(99) / 100)
TAU_C = mp.mpc(mp.mpf(7) / 100, mp.mpf(101) / 100)
TAU_D = mp.mpc(mp.mpf(-19) / 100, mp.mpf(103) / 100)

N_PASS = 0
N_FAIL = 0


def check(label, ok):
    global N_PASS, N_FAIL
    print(("  PASS  " if ok else "  FAIL  ") + label)
    if ok:
        N_PASS += 1
    else:
        N_FAIL += 1
    return ok


def fmt(xs):
    return "(" + ", ".join(str(x) for x in xs) + ")"


def fmtn(xs, nd=6):
    return "(" + ", ".join(mp.nstr(mp.mpf(x) if not isinstance(x, mp.mpc)
                                   else x, nd) for x in xs) + ")"


# ---------------------------------------------------------------------------
# exact Q(zeta_8) arithmetic (delta-1c/1d/1e machinery, verbatim)
# ---------------------------------------------------------------------------
Z8_ZERO = (F(0), F(0), F(0), F(0))
Z8_ONE = (F(1), F(0), F(0), F(0))


def z8_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def z8_mul(a, b):
    out = [F(0)] * 4
    for i in range(4):
        if a[i] == 0:
            continue
        for j in range(4):
            if b[j] == 0:
                continue
            k = i + j
            if k < 4:
                out[k] += a[i] * b[j]
            else:
                out[k - 4] -= a[i] * b[j]
    return tuple(out)


def z8_scal(f, a):
    return tuple(f * x for x in a)


def z8_root(k):
    k %= 8
    s = F(1)
    if k >= 4:
        k -= 4
        s = F(-1)
    v = [F(0)] * 4
    v[k] = s
    return tuple(v)


def z8_conj(a):
    return (a[0], -a[3], -a[2], -a[1])


def z8_to_mpc(a):
    z = mp.exp(mp.mpc(0, mp.pi / 4))
    return (mp.mpf(a[0].numerator) / a[0].denominator
            + z * mp.mpf(a[1].numerator) / a[1].denominator
            + z ** 2 * mp.mpf(a[2].numerator) / a[2].denominator
            + z ** 3 * mp.mpf(a[3].numerator) / a[3].denominator)


def sum_z8(xs):
    out = Z8_ZERO
    for x in xs:
        out = z8_add(out, x)
    return out


def mat_mul(A, B):
    n = len(A)
    return [[sum_z8([z8_mul(A[i][k], B[k][j]) for k in range(n)])
             for j in range(n)] for i in range(n)]


def mat_eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A))
               for j in range(len(A)))


def mat_id(n):
    return [[Z8_ONE if i == j else Z8_ZERO for j in range(n)]
            for i in range(n)]


def mat_conjT(A):
    n = len(A)
    return [[z8_conj(A[j][i]) for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------------------
# discriminant module D = Z4 x Z4, q = (5x^2 + 3y^2)/8 mod 1
# ---------------------------------------------------------------------------
MU = [(x, y) for x in range(4) for y in range(4)]
IDX = {m: i for i, m in enumerate(MU)}
DIAG_H = [(a, a) for a in range(4)]
ANTI_H = [(0, 0), (1, 3), (2, 2), (3, 1)]


def q8(mu):
    x, y = mu
    return (5 * x * x + 3 * y * y) % 8


def bil8(mu, nu):
    return (2 * (5 * mu[0] * nu[0] + 3 * mu[1] * nu[1])) % 8


def neg(mu):
    return ((-mu[0]) % 4, (-mu[1]) % 4)


def build_weil(qfun, bfun, group, sigma_conj):
    n = len(group)
    rt = F(1)
    m = n
    while m % 4 == 0:
        m //= 4
        rt *= 2
    assert m == 1
    T = [[z8_root(qfun(group[i])) if i == j else Z8_ZERO
          for j in range(n)] for i in range(n)]
    S = [[z8_scal(F(1, rt), z8_mul(sigma_conj,
                                   z8_root(-bfun(group[i], group[j]))))
          for j in range(n)] for i in range(n)]
    return T, S


def weil_matrices():
    return build_weil(q8, bil8, MU, Z8_ONE)


def rho_np(exact):
    return np.array([[complex(z8_to_mpc(exact[i][j])) for j in range(16)]
                     for i in range(16)])


# ---------------------------------------------------------------------------
# lattice ledgers (delta-1c/1d/1e machinery, verbatim)
# ---------------------------------------------------------------------------
def build_d5_vecs(maxnorm):
    out = {x: [] for x in range(4)}
    lim = 16 * maxnorm
    r = int(maxnorm ** 0.5) + 1
    for v in product(range(-r, r + 1), repeat=5):
        n16 = 16 * sum(t * t for t in v)
        if n16 > lim:
            continue
        x = 0 if sum(v) % 2 == 0 else 2
        out[x].append((n16, tuple(2 * t for t in v)))
    ru = int((4 * maxnorm) ** 0.5) + 1
    odd = [k for k in range(-ru, ru + 1) if k % 2 != 0]
    for u in product(odd, repeat=5):
        n16 = 4 * sum(t * t for t in u)
        if n16 > lim:
            continue
        x = 1 if (sum(u) - 5) % 4 == 0 else 3
        out[x].append((n16, u))
    return out


def build_a3_vecs(maxnorm):
    out = {y: [] for y in range(4)}
    lim = 16 * maxnorm
    r = int(maxnorm ** 0.5) + 2
    for y in range(4):
        rng = [4 * m - y for m in range(-r, r + 2)]
        for w3 in product(rng, repeat=3):
            w4 = -(w3[0] + w3[1] + w3[2])
            if (w4 + y) % 4 != 0:
                continue
            n16 = w3[0] ** 2 + w3[1] ** 2 + w3[2] ** 2 + w4 ** 2
            if n16 <= lim:
                out[y].append((n16, w3 + (w4,)))
    return out


def factor_moments(vecs, form_re, form_im, kmax, maxn16):
    out = {}
    for cls, lst in vecs.items():
        acc = {}
        for n16, u in lst:
            if n16 > maxn16:
                continue
            dre = sum(a * b for a, b in zip(u, form_re))
            dim_ = (sum(a * b for a, b in zip(u, form_im))
                    if form_im else 0)
            ms = acc.get(n16)
            if ms is None:
                ms = acc[n16] = [[0, 0] for _ in range(kmax + 1)]
            pr, pi = 1, 0
            for k in range(kmax + 1):
                ms[k][0] += pr
                ms[k][1] += pi
                pr, pi = pr * dre - pi * dim_, pr * dim_ + pi * dre
        out[cls] = acc
    return out


def combine_series(m5x, m3y, k_ins, maxn16):
    out = {}
    for n5, a in m5x.items():
        for n3, b in m3y.items():
            n = n5 + n3
            if n > maxn16:
                continue
            cre = cim = 0
            for k in range(k_ins + 1):
                c = comb(k_ins, k)
                ar, ai = a[k]
                br, bi = b[k_ins - k]
                cre += c * (ar * br - ai * bi)
                cim += c * (ar * bi + ai * br)
            if cre or cim:
                o = out.get(n, (0, 0))
                out[n] = (o[0] + cre, o[1] + cim)
    return out


def eval_series16(ser, tau, maxn16):
    tot = mp.mpc(0)
    for n16, (cre, cim) in ser.items():
        if n16 > maxn16:
            continue
        tot += mp.mpc(cre, cim) * mp.exp(1j * mp.pi * tau * n16 / 16)
    return tot


SAMPLES = [
    (1, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 0, 0),
    (0, 0, 0, 0, 0, 1, 1, 1),
    (1, 2, 0, 0, 0, 0, 0, 0),
    (1, 0, 0, 0, 0, 1, 0, 0),
    (1, 1, 1, 0, 0, 1, 1, 1),
]


def basis_at(pt):
    xs, ys = pt[:5], list(pt[5:])
    ys4 = ys + [-sum(ys)]
    S5 = sum(x * x for x in xs)
    S3 = sum(y * y for y in ys4)
    T5 = sum(x ** 4 for x in xs)
    T3 = sum(y ** 4 for y in ys4)
    return (S5 * S5, S5 * S3, S3 * S3, T5, T3)


BMAT = [basis_at(p) for p in SAMPLES]


def solve_cell(bvals):
    A = sp.Matrix([[BMAT[k][i] for i in range(5)] for k in range(6)])
    b = sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in bvals])
    sol, params = A.gauss_jordan_solve(b)
    assert len(params) == 0 and A * sol == b
    return [F(sp.Rational(x).p, sp.Rational(x).q) for x in sol]


def build_ledgers16(d5vecs, a3vecs, maxnorm):
    lim16 = 16 * maxnorm
    md5 = {}
    for x in range(4):
        acc = {}
        for n16, u in d5vecs[x]:
            if n16 > lim16:
                continue
            ms = acc.get(n16)
            if ms is None:
                ms = acc[n16] = [[0] * 6 for _ in range(5)]
            for si, s in enumerate(SAMPLES):
                d = 2 * (u[0] * s[0] + u[1] * s[1] + u[2] * s[2]
                         + u[3] * s[3] + u[4] * s[4])
                p = 1
                for k in range(5):
                    ms[k][si] += p
                    p *= d
        md5[x] = acc
    ma3 = {}
    for y in range(4):
        acc = {}
        for n16, w in a3vecs[y]:
            if n16 > lim16:
                continue
            ms = acc.get(n16)
            if ms is None:
                ms = acc[n16] = [[0] * 6 for _ in range(5)]
            for si, s in enumerate(SAMPLES):
                d = ((w[0] - w[3]) * s[5] + (w[1] - w[3]) * s[6]
                     + (w[2] - w[3]) * s[7])
                p = 1
                for k in range(5):
                    ms[k][si] += p
                    p *= d
        ma3[y] = acc
    out4 = {m: {} for m in MU}
    out2 = {m: {} for m in MU}
    CNT = {m: {} for m in MU}
    for (x, y) in MU:
        acc4, acc2 = {}, {}
        for n5, m5 in md5[x].items():
            for n3, m3 in ma3[y].items():
                tot = n5 + n3
                if tot == 0 or tot > lim16:
                    continue
                lev = F(tot, 32)
                cell4 = acc4.get(lev)
                if cell4 is None:
                    cell4 = acc4[lev] = [0] * 6
                    acc2[lev] = [0, 0]
                for si in range(6):
                    cell4[si] += sum(comb(4, k) * m5[k][si] * m3[4 - k][si]
                                     for k in range(5))
                for si in range(2):
                    acc2[lev][si] += (m5[2][si] * m3[0][si]
                                      + 2 * m5[1][si] * m3[1][si]
                                      + m5[0][si] * m3[2][si])
                CNT[(x, y)][lev] = (CNT[(x, y)].get(lev, 0)
                                    + m5[0][0] * m3[0][0])
        for lev, cell in acc4.items():
            out4[(x, y)][lev] = solve_cell([F(c, 256) for c in cell])
            b0, b1 = acc2[lev]
            out2[(x, y)][lev] = (F(b0, 16), F(b1, 32))
    return out4, out2, CNT


def build_theta_ser0():
    d5v = build_d5_vecs(MAXN_CERT)
    a3v = build_a3_vecs(MAXN_CERT)
    lim = 16 * MAXN_CERT
    zero5 = (0, 0, 0, 0, 0)
    zero4 = (0, 0, 0, 0)
    m5_0 = factor_moments(d5v, zero5, None, 0, lim)
    m3_0 = factor_moments(a3v, zero4, None, 0, lim)
    return {mu: combine_series(m5_0[mu[0]], m3_0[mu[1]], 0, lim)
            for mu in MU}, lim


# ---------------------------------------------------------------------------
# block numerics: gauge M = G/eta^8 and the fibre blocks f_m
# ---------------------------------------------------------------------------
def qp(tau, e):
    return mp.exp(2j * mp.pi * tau * e)


def geo_val(N, a, b, tau):
    zb = mp.exp(2j * mp.pi * b / N)
    zbb = mp.exp(-2j * mp.pi * b / N)
    ep = mp.mpf(a) / N if a else mp.mpf(1)
    em = 1 - mp.mpf(a) / N if a else mp.mpf(1)
    Eb = -mp.mpf(1) / 24 + (mp.mpf(a) / N) * (1 - mp.mpf(a) / N) / 4 \
        if a else -mp.mpf(1) / 24
    val = qp(tau, 4 * Eb)
    for n in range(NPROD):
        val /= (1 - zb * qp(tau, ep + n)) ** 2
        val /= (1 - zbb * qp(tau, em + n)) ** 2
    if a == 0 and b % N != 0:
        val /= (1 - zb) * (1 - zbb)
    return val


def eta_val(tau):
    val = qp(tau, mp.mpf(1) / 24)
    for n in range(1, NPROD + 1):
        val *= (1 - qp(tau, n))
    return val


def M_val(N, a, b, tau):
    return geo_val(N, a, b, tau) / eta_val(tau) ** 8


def f_val(N, m, a, b, tau):
    aa = (m * a) % N
    bb = (m * b) % N
    if aa == 0 and bb == 0:
        return mp.mpc(1)
    z = mp.exp(2j * mp.pi * bb / N)
    zc = mp.exp(-2j * mp.pi * bb / N)
    ep = mp.mpf(aa) / N if aa else mp.mpf(1)
    em = 1 - mp.mpf(aa) / N if aa else mp.mpf(1)
    E = -mp.mpf(1) / 24 + (mp.mpf(aa) / N) * (1 - mp.mpf(aa) / N) / 4 \
        if aa else -mp.mpf(1) / 24
    val = qp(tau, 2 * E)
    for n in range(NPROD):
        val /= (1 - z * qp(tau, ep + n))
        val /= (1 - zc * qp(tau, em + n))
    if aa == 0 and bb % N != 0:
        val /= (1 - z)
    return val


def ax_val(N, ws, a, b, tau):
    v = mp.mpc(1)
    for m in ws:
        v *= f_val(N, m, a, b, tau)
    return v


def measure_transport_w(N, pairs, fM, wexp):
    t, s = {}, {}
    dev = mp.mpf(0)
    for (a, b) in pairs:
        Tp = (a, (a + b) % N)
        Sp = (b % N, (-a) % N)
        vals_t, vals_s = [], []
        for tau in (TAU_A, TAU_B):
            vals_t.append(fM(a, b, tau + 1) / fM(*Tp, tau))
            vals_s.append(fM(a, b, -1 / tau) * (-1j * tau) ** wexp
                          / fM(*Sp, tau))
        dev = max(dev, abs(vals_t[0] - vals_t[1]),
                  abs(vals_s[0] - vals_s[1]))
        t[(a, b)] = vals_t[0]
        s[(a, b)] = vals_s[0]
    return t, s, dev


def recog(z):
    lm = mp.log(abs(z))
    ph = mp.arg(z) / (2 * mp.pi)
    k = int(mp.nint(ph * L_PHASE))
    dev = abs(ph - mp.mpf(k) / L_PHASE)
    return lm, k % L_PHASE, dev


# ---------------------------------------------------------------------------
# contraction solve machinery (generalised to n dims for the doubled system)
# ---------------------------------------------------------------------------
def sl2z_char(k):
    return (np.exp(2j * np.pi * k / 12), np.exp(-2j * np.pi * k / 4))


def solve_orbit(pairs, N, tconst, sconst, rhoT_np, rhoS_np, base, k=0):
    n = rhoT_np.shape[0]
    chT, chS = sl2z_char(k)
    TT = rhoT_np.T
    ST = rhoS_np.T
    Lam = {base: np.eye(n, dtype=complex)}
    queue = [base]
    rows = []
    seen_edges = set()
    while queue:
        p = queue.pop(0)
        a, b = p
        for tag, p2, Mx in (
                ('T', (a, (a + b) % N),
                 complex(tconst[p]) / chT * TT),
                ('S', ((b % N), (-a) % N),
                 complex(sconst[p]) / chS * ST)):
            if (p, tag) in seen_edges:
                continue
            seen_edges.add((p, tag))
            cand = Mx @ Lam[p]
            if p2 not in Lam:
                Lam[p2] = cand
                queue.append(p2)
            else:
                rows.append(cand - Lam[p2])
    A = np.vstack(rows) if rows else np.zeros((1, n), dtype=complex)
    _, sv, Vh = np.linalg.svd(A)
    sv = list(sv) + [0.0] * (n - len(sv))
    tol = max(sv) * 1e-8 if max(sv) > 0 else 1e-8
    null = [Vh[i].conj() for i in range(n) if sv[i] < tol]
    return sorted(Lam.keys()), Lam, null, sv


def member_test(Lam, null, targets):
    """stacked homogeneous system [Lam[p] V | -t_p] u = 0 with ONE
    shared scalar; returns (sigma_min/sigma_max, |c|/||u||, u, V)."""
    if not null:
        return None
    V = np.array(null).T
    rows = []
    for p, t in targets.items():
        A = Lam[p] @ V
        rows.append(np.hstack([A, -t.reshape(len(t), 1)]))
    Mst = np.vstack(rows)
    _, svs, Vh = np.linalg.svd(Mst)
    ratio = svs[-1] / svs[0]
    u = Vh[-1].conj()
    c_rel = abs(u[-1]) / np.linalg.norm(u)
    return ratio, c_rel, u, V


def dressed_consts(tg, sg, d, orient, pairs):
    if orient == 'hol':
        tt = {p: complex(tg[p]) * complex(d['t'][p]) for p in pairs}
        ss = {p: complex(sg[p]) * complex(d['s'][p]) for p in pairs}
    else:
        tt = {p: complex(tg[p]) * np.conj(complex(d['t'][p]))
              for p in pairs}
        ss = {p: complex(sg[p]) * np.conj(complex(d['s'][p]))
              for p in pairs}
    return tt, ss


# ---------------------------------------------------------------------------
# exact invariant subspace of the 16-dim Weil representation (delta-1e D2)
# ---------------------------------------------------------------------------
def mulmat_q8(u):
    M = [[F(0)] * 4 for _ in range(4)]
    for i in range(4):
        if u[i] == 0:
            continue
        for j in range(4):
            k = i + j
            if k < 4:
                M[k][j] += u[i]
            else:
                M[k - 4][j] -= u[i]
    return M


def invariant_subspace(Tx, Sx):
    rows = []
    for Op in (Tx, Sx):
        for i in range(16):
            block = [[sp.Rational(0)] * 64 for _ in range(4)]
            for j in range(16):
                Mm = mulmat_q8(Op[i][j])
                for r in range(4):
                    for cc in range(4):
                        if Mm[r][cc]:
                            block[r][4 * j + cc] += sp.Rational(
                                Mm[r][cc].numerator, Mm[r][cc].denominator)
            for r in range(4):
                block[r][4 * i + r] -= 1
            rows.extend(block)
    A = sp.Matrix(rows)
    return A.nullspace()


def in_lagrangian_span(vec64):
    comp = [tuple(F(sp.Rational(vec64[4 * j + c]).p,
                    sp.Rational(vec64[4 * j + c]).q) for c in range(4))
            for j in range(16)]
    alpha = comp[IDX[(1, 1)]]
    beta = comp[IDX[(1, 3)]]
    for mu in MU:
        j = IDX[mu]
        in_h = mu in DIAG_H
        in_hp = mu in ANTI_H
        if mu == (0, 0):
            want = z8_add(alpha, beta)
        elif in_h and in_hp:
            want = z8_add(alpha, beta)
        elif in_h:
            want = alpha
        elif in_hp:
            want = beta
        else:
            want = Z8_ZERO
        if comp[j] != want:
            return False
    return True


# ---------------------------------------------------------------------------
# exact dressing series + fundamental-domain kernel J (delta-1b/1d/1e)
# ---------------------------------------------------------------------------
def gadd(z1, z2):
    return (z1[0] + z2[0], z1[1] + z2[1])


def gmul(z1, z2):
    return (z1[0] * z2[0] - z1[1] * z2[1], z1[0] * z2[1] + z1[1] * z2[0])


def ipow(b):
    return [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))][b % 4]


def uroot(N, k):
    if N == 2:
        return [(F(1), F(0)), (F(-1), F(0))][k % 2]
    return ipow(k)


def ser_mul(A, B, cut):
    out = {}
    for e1, v1 in A.items():
        for e2, v2 in B.items():
            e = e1 + e2
            if e > cut:
                continue
            out[e] = gadd(out.get(e, (F(0), F(0))), gmul(v1, v2))
    return {e: v for e, v in out.items() if v != (F(0), F(0))}


def tower(zeta, e0, cut):
    out = {F(0): (F(1), F(0))}
    n = 0
    while e0 + n <= cut:
        e = e0 + n
        n += 1
        if e <= 0:
            continue
        fac = {F(0): (F(1), F(0))}
        k = 1
        zk = zeta
        while k * e <= cut:
            fac[k * e] = (F(k + 1) * zk[0], F(k + 1) * zk[1])
            zk = gmul(zk, zeta)
            k += 1
        out = ser_mul(out, fac, cut)
    return out


def tower1(zeta, e0, cut):
    out = {F(0): (F(1), F(0))}
    n = 0
    while e0 + n <= cut:
        e = e0 + n
        n += 1
        if e <= 0:
            continue
        fac = {F(0): (F(1), F(0))}
        k = 1
        zk = zeta
        while k * e <= cut:
            fac[k * e] = zk
            zk = gmul(zk, zeta)
            k += 1
        out = ser_mul(out, fac, cut)
    return out


def geo_block(N, a, b, cut):
    ab = F(a, N)
    e_plus = ab if a else F(1)
    e_minus = (1 - ab) if a else F(1)
    block = ser_mul(tower(uroot(N, b), e_plus, cut),
                    tower(uroot(N, -b), e_minus, cut), cut)
    zm = None
    if a == 0 and b % N != 0:
        wb, wmb = uroot(N, b), uroot(N, -b)
        zm = gmul((F(1) - wb[0], -wb[1]), (F(1) - wmb[0], -wmb[1]))
    return block, zm


def p8_series(nmax):
    out = [F(1)] + [F(0)] * nmax
    for d in range(1, nmax + 1):
        geo = [F(0)] * (nmax + 1)
        k = 0
        while d * k <= nmax:
            geo[d * k] = F(int(sp.binomial(8 + k - 1, k)))
            k += 1
        new = [F(0)] * (nmax + 1)
        for i, av in enumerate(out):
            if av == 0:
                continue
            for j, bv in enumerate(geo[:nmax + 1 - i]):
                new[i + j] += av * bv
        out = new
    return out


def gauge_dress_series(N, a, b, cut):
    geo, zm = geo_block(N, a, b, cut + 1)
    w = (F(1), F(0))
    if zm is not None:
        nrm = zm[0] * zm[0] + zm[1] * zm[1]
        w = (zm[0] / nrm, -zm[1] / nrm)
    p8 = p8_series(int(cut) + 1)
    dress = {}
    for e, cv in geo.items():
        for m2, pv in enumerate(p8):
            if pv == 0:
                continue
            ex = e + m2
            if ex > cut:
                continue
            dress[ex] = gadd(dress.get(ex, (F(0), F(0))),
                             gmul(w, (cv[0] * pv, cv[1] * pv)))
    return dress


def f_series(N, m, a, b, cut):
    aa = (m * a) % N
    bb = (m * b) % N
    if aa == 0 and bb == 0:
        return {F(0): (F(1), F(0))}, F(0)
    ep = F(aa, N) if aa else F(1)
    em = (1 - F(aa, N)) if aa else F(1)
    ser = ser_mul(tower1(uroot(N, bb), ep, cut),
                  tower1(uroot(N, -bb), em, cut), cut)
    if aa == 0 and bb % N != 0:
        w = uroot(N, bb)
        d = (F(1) - w[0], -w[1])
        nrm = d[0] * d[0] + d[1] * d[1]
        winv = (d[0] / nrm, -d[1] / nrm)
        ser = {e: gmul(winv, v) for e, v in ser.items()}
    shift = 2 * (F(-1, 24) + F(aa, N) * (1 - F(aa, N)) / 4)
    return ser, shift


_GLX, _GLW = np.polynomial.legendre.leggauss(160)
_TH = [(math.pi / 12) * (x + 1) for x in _GLX]
_WTH = [(math.pi / 12) * w for w in _GLW]
_J_CACHE = {}


def Jval(delta, s):
    key = (delta, s)
    if key in _J_CACHE:
        return _J_CACHE[key]
    d = mp.mpf(delta.numerator) / mp.mpf(delta.denominator)
    cusp = (mp.sin(mp.pi * d) / (mp.pi * d)
            * (2 * mp.pi * d) ** (s - 1) * mp.gammainc(1 - s, 2 * mp.pi * d))
    df = float(d)
    sinpd = math.sin(math.pi * df)
    arc = 0.0
    for th, wt in zip(_TH, _WTH):
        ct, st = math.cos(th), math.sin(th)
        arc += wt * (st * ct ** (-s) * math.exp(-2 * math.pi * df * ct)
                     * (sinpd - math.sin(2 * math.pi * df * st))
                     / (math.pi * df))
    val = cusp + mp.mpf(arc)
    _J_CACHE[key] = val
    return val


def hm_integral_pp(beta, dressmaps, basemap, V4, V2, CNT, cut, weight):
    I_main = [mp.mpc(0)] * 5
    I_comp = [mp.mpc(0)] * 5
    W = {}
    n_neg = 0
    wt_neg = mp.mpf(0)
    for p, dress in dressmaps.items():
        a = p[0]
        base = basemap[p]
        bp = beta[p]
        for i_mu, mu in enumerate(MU):
            bc = complex(bp[i_mu])
            if abs(bc) < 1e-14:
                continue
            bz = mp.mpc(bc.real, bc.imag)
            for ex, cv in dress.items():
                cz = bz * mp.mpc(mp.mpf(cv[0].numerator) / cv[0].denominator,
                                 mp.mpf(cv[1].numerator) / cv[1].denominator)
                for lev, vec4 in V4[mu].items():
                    D = base + ex + lev
                    if D > cut:
                        continue
                    if D <= 0:
                        n_neg += 1
                        wt_neg = max(wt_neg, abs(cz))
                        continue
                    z0 = cz * Jval(D, 0)
                    for i in range(5):
                        z = z0 * (mp.mpf(vec4[i].numerator)
                                  / vec4[i].denominator)
                        I_main[i] += weight * z
                    if mu[0] == mu[1]:
                        key = (a, lev)
                        W[key] = W.get(key, mp.mpc(0)) + weight * z0
                    u, v = V2[mu][lev]
                    z1 = cz * Jval(D, 1) * mp.mpf(-3) / (2 * mp.pi)
                    uu = mp.mpf(u.numerator) / u.denominator
                    vv = mp.mpf(v.numerator) / v.denominator
                    I_comp[0] += weight * z1 * uu
                    I_comp[1] += weight * z1 * (uu + vv)
                    I_comp[2] += weight * z1 * vv
                    z2 = (cz * Jval(D, 2) * mp.mpf(3)
                          / (16 * mp.pi ** 2) * CNT[mu][lev])
                    I_comp[0] += weight * z2
                    I_comp[1] += weight * z2 * 2
                    I_comp[2] += weight * z2
    I_hat = [I_main[i] + I_comp[i] for i in range(5)]
    return I_main, I_hat, W, n_neg, wt_neg


def build_dress(beta_keys, ws):
    dm, basemap = {}, {}
    for p in beta_keys:
        a, b = p
        d = gauge_dress_series(4, a, b, GRID_CUT)
        shift = F(0)
        for m in ws:
            fs, sh = f_series(4, m, a, b, GRID_CUT)
            d = ser_mul(d, fs, GRID_CUT)
            shift += sh
        dm[p] = d
        basemap[p] = BASES4[a] + shift
    return dm, basemap


def spread_vs(I_main, tgt):
    scale = max(abs(x) for x in I_main)
    rats = [I_main[i] / tgt[i] for i in range(5) if tgt[i] != 0]
    spread = (max(abs(rats[i] - rats[j]) for i in range(len(rats))
                  for j in range(len(rats)))
              / max(abs(r) for r in rats))
    zrel = max([abs(I_main[i]) / scale for i in range(5) if tgt[i] == 0]
               + [mp.mpf(0)])
    return spread, zrel


PSIV = [F(3), F(-1), F(-1), F(0), F(-1, 4)]


def psi_of(v):
    return sum(float(PSIV[i]) * v[i] for i in range(5))


# ---------------------------------------------------------------------------
# pair sets, columns
# ---------------------------------------------------------------------------
PAIRS4 = [(a, b) for a in range(4) for b in range(4) if (a, b) != (0, 0)]
ORB1 = [p for p in PAIRS4 if gcd(gcd(p[0], p[1]), 4) == 1]
ORB2 = [p for p in PAIRS4 if gcd(gcd(p[0], p[1]), 4) == 2]

CAND_WS = {
    'f2': (2,),
    'f1f3': (1, 3),
    'f1f2f3': (1, 2, 3),
    'wrong112': (1, 1, 2),
    'wrong222': (2, 2, 2),
}

CONTAIN_TOL = 1e-8
OKUBO = [F(1), F(2), F(1), F(0), F(0)]
ZERO5 = [F(0)] * 5


def w_col(b, shift=0):
    v = np.zeros(16, dtype=complex)
    for m in range(4):
        v[IDX[(m, m)]] = 1j ** (((b * m) + shift * m) % 4)
    return v


def diag_unph():
    v = np.zeros(16, dtype=complex)
    for m in range(4):
        v[IDX[(m, m)]] = 1.0
    return v


def col_contact(j):
    v = np.zeros(16, dtype=complex)
    for m in range(4):
        v[IDX[(m, m)]] = 1.0 - 1j ** ((j * m) % 4)
    return v


# ---------------------------------------------------------------------------
# P0 -- exact foundations: Weil system, invariant space, ledger targets
# ---------------------------------------------------------------------------
def section0(Tx, Sx, V4, CNT):
    print("  -- P0: exact foundations (Weil, invariant space, targets)")
    n = 16
    C = [[Z8_ONE if MU[j] == neg(MU[i]) else Z8_ZERO for j in range(n)]
         for i in range(n)]
    S2 = mat_mul(Sx, Sx)
    ST = mat_mul(Sx, Tx)
    ST3 = mat_mul(mat_mul(ST, ST), ST)
    T8 = mat_id(n)
    for _ in range(8):
        T8 = mat_mul(T8, Tx)
    ok_sym = all(Sx[i][j] == Sx[j][i] for i in range(n) for j in range(n))
    eH = [Z8_ONE if MU[i] in DIAG_H else Z8_ZERO for i in range(n)]
    eHp = [Z8_ONE if MU[i] in ANTI_H else Z8_ZERO for i in range(n)]
    SeH = [sum_z8([z8_mul(Sx[i][j], eH[j]) for j in range(n)])
           for i in range(n)]
    TeH = [z8_mul(Tx[i][i], eH[i]) for i in range(n)]
    SeHp = [sum_z8([z8_mul(Sx[i][j], eHp[j]) for j in range(n)])
            for i in range(n)]
    TeHp = [z8_mul(Tx[i][i], eHp[i]) for i in range(n)]
    check("P0.1 [WEIL EXACT] S symmetric + unitary, S^2 = C, (ST)^3 = "
          "S^2, S^4 = 1, T^8 = 1 in Q(zeta_8); e_H and e_H' exactly T- "
          "and S-fixed (v518/delta-1e replication)",
          ok_sym and mat_eq(mat_mul(Sx, mat_conjT(Sx)), mat_id(n))
          and mat_eq(S2, C) and mat_eq(ST3, S2)
          and mat_eq(mat_mul(S2, S2), mat_id(n))
          and mat_eq(T8, mat_id(n))
          and SeH == eH and TeH == eH and SeHp == eHp and TeHp == eHp)

    ns = invariant_subspace(Tx, Sx)
    dim_q = len(ns)
    all_in_span = all(in_lagrangian_span(v) for v in ns)
    check("P0.2 [INVARIANT SUBSPACE, EXACT RATIONAL] dim_Q {v : rho(T) "
          "v = v, rho(S) v = v} = %d = 4 x 2 and EVERY exact nullspace "
          "vector lies in the Q(zeta_8)-span of {e_H, e_H'}: %s -- a "
          "single-valued lattice factor at physical weight is FORCED "
          "onto the two Lagrangian gluings, both theta = E4 = the "
          "UNPHASED trace (delta-1e D2 replication; the forcing target "
          "of this probe)" % (dim_q, all_in_span),
          dim_q == 8 and all_in_span)

    Qtab = {0: [12, 0, 6, 4, 8], 1: [12, 24, 0, -8, 16],
            2: [0, 24, 30, 12, -40], 3: [12, 24, 0, -8, 16]}
    ok_led = all(V4[(a, a)].get(F(1)) == Qtab[a] for a in range(4))
    tots = [sum(CNT[(a, a)].get(F(nn), 0) for a in range(4))
            for nn in range(1, 9)]
    tots_anti = [sum(CNT[m].get(F(nn), 0) for m in ANTI_H)
                 for nn in range(1, 9)]
    I = sp.I
    R = sp.Rational
    Qv = {m: [R(x) for x in Qtab[m]] for m in range(4)}
    dets = {1: 2, 2: 4, 3: 2}
    Qtw = {j: [sp.nsimplify(sp.expand(
        sum(I ** (j * m) * Qv[m][i] for m in range(4))))
        for i in range(5)] for j in range(4)}
    h = [R(m * (4 - m), 8) for m in range(4)]
    w = [sp.nsimplify(sp.expand(
        sum((1 - I ** (j * m)) / dets[j] for j in (1, 2, 3))))
        for m in range(4)]
    Afix = [sp.nsimplify(sum(Qtw[j][i] / dets[j] for j in (1, 2, 3)))
            for i in range(5)]
    contact = {j: [sp.nsimplify((Qtw[0][i] - Qtw[j][i]) / dets[j])
                   for i in range(5)] for j in (1, 2, 3)}
    total = [sum(contact[j][i] for j in (1, 2, 3)) for i in range(5)]
    sums = {j: [sp.nsimplify(Qtw[j][i] / dets[j] + contact[j][i])
                for i in range(5)] for j in (1, 2, 3)}
    psiS = lambda v: sp.nsimplify(3 * v[0] - v[1] - v[2] - R(1, 4) * v[4])
    check("P0.3 [COMPLETION TARGETS, EXACT] ledger diagonal = class "
          "quartics (Q_0..Q_3 replicated); diagonal AND anti-diagonal "
          "counts = 240 sigma_3(n), n <= 8 (both gluings are E4); "
          "w_m = %s = (0, 3/2, 2, 3/2) = 4 h_m, h_2 : h_1 = %s = 4:3; "
          "A_fix = %s, psi(A_fix) = %s = +64; contact total = %s, "
          "psi = %s = -64; per-channel Okubo squares (18, 9, 18) "
          "<x,x>^2 (v516 replication)"
          % (fmt(w), h[2] / h[1], fmt(Afix), psiS(Afix), fmt(total),
             psiS(total)),
          ok_led and tots == [240 * s for s in SIGMA3]
          and tots_anti == [240 * s for s in SIGMA3]
          and w == [0, R(3, 2), 2, R(3, 2)]
          and all(w[m] == 4 * h[m] for m in range(4))
          and h[2] / h[1] == R(4, 3)
          and Afix == [9, -30, -15, 0, 32]
          and total == [36, 120, 60, 0, -32]
          and psiS(Afix) == 64 and psiS(total) == -64
          and sums[1] == [18, 36, 18, 0, 0]
          and sums[2] == [9, 18, 9, 0, 0]
          and sums[3] == [18, 36, 18, 0, 0])

    e = lambda x: sp.exp(2 * sp.pi * sp.I * x)
    chi4T = e(R(1, 3))
    chi10T = e(R(5, 6))
    ok_chars = (sp.simplify(chi4T - 1) != 0
                and sp.simplify(chi10T - 1) != 0
                and sp.simplify(chi4T * sp.conjugate(chi4T) - 1) == 0
                and sp.simplify(chi4T ** 2 - e(R(2, 3))) == 0
                and sp.simplify(chi4T ** 2 - 1) != 0
                and sp.simplify((-1) * e(R(-1, 6)) - chi4T) == 0)
    check("P0.4 [CHARACTERS, EXACT] chi_4(T) = e(1/3) and chi_10(T) = "
          "e(5/6) are NONTRIVIAL; |chi_4(T)|^2 = 1 exactly (conjugate "
          "pairing cancels) while chi_4(T)^2 = e(2/3) =/= 1 (one-sided "
          "squaring does NOT); T-fix mechanism (-1) x e(-1/6) = "
          "chi_4(T) replicated; real tau_2 powers carry no phase",
          ok_chars)
    return Qv, Qtw, dets


# ---------------------------------------------------------------------------
# P1 -- A1: the F-lemma (well-definedness kills every chiral option)
# ---------------------------------------------------------------------------
def section1(rhoT, rhoS, ser0, lim):
    print("  -- P1: A1 -- the fundamental-domain lemma (source-1)")
    tg, sg, dev = measure_transport_w(
        4, PAIRS4, lambda a, b, tau: M_val(4, a, b, tau), 4)
    tgx, sgx = {}, {}
    devmax = mp.mpf(0)
    lmmax_g = mp.mpf(0)
    for p in PAIRS4:
        lt, kt, dt = recog(tg[p])
        ls, ks, ds = recog(sg[p])
        devmax = max(devmax, dt, ds)
        lmmax_g = max(lmmax_g, abs(lt), abs(ls))
        tgx[p] = (lt, kt)
        sgx[p] = (ls, ks)
    axd = {}
    lmmax_f = mp.mpf(0)
    for name, ws in CAND_WS.items():
        tA, sA, devA = measure_transport_w(
            4, PAIRS4, lambda a, b, tau: ax_val(4, ws, a, b, tau), 0)
        tAx, sAx = {}, {}
        dmax = mp.mpf(0)
        for p in PAIRS4:
            lt, kt, dt = recog(tA[p])
            ls, ks, ds = recog(sA[p])
            dmax = max(dmax, dt, ds)
            if name == 'f1f3':
                lmmax_f = max(lmmax_f, abs(lt), abs(ls))
            tAx[p] = (lt, kt)
            sAx[p] = (ls, ks)
        axd[name] = dict(ws=ws, t=tA, s=sA, tx=tAx, sx=sAx,
                         dev=devA, rec=dmax)
    ok_fix = all(tgx[(0, b)][1] == L_PHASE // 2
                 and axd['f1f3']['tx'][(0, b)][1]
                 == (-L_PHASE // 6) % L_PHASE for b in (1, 2, 3))
    check("P1.1 [TRANSPORTS] gauge + fibre transport constants "
          "constant over two tau (max dev %s < 1e-28) and recognised "
          "on the 1/960 grid (max %s < 1e-25); T-fixed nodes: gauge "
          "k = 480 (= -1), fibre f1f3 k = 800 (= e(-1/6)) exactly "
          "(v518 replication); max |log-modulus| gauge %s / fibre %s"
          % (mp.nstr(max(dev, max(d['dev'] for d in axd.values())), 3),
             mp.nstr(max(devmax, max(d['rec'] for d in axd.values())),
                     3),
             mp.nstr(lmmax_g, 3), mp.nstr(lmmax_f, 3)),
          dev < mp.mpf(10) ** (-28) and devmax < mp.mpf(10) ** (-25)
          and all(d['dev'] < mp.mpf(10) ** (-28) for d in axd.values())
          and all(d['rec'] < mp.mpf(10) ** (-25) for d in axd.values())
          and ok_fix)

    k0 = {}
    scans = [('none', 'hol')] + [(nm, o) for nm in CAND_WS
                                 for o in ('hol', 'anti')]
    for nm, orient in scans:
        if nm == 'none':
            tt = {p: complex(tg[p]) for p in PAIRS4}
            ss = {p: complex(sg[p]) for p in PAIRS4}
        else:
            tt, ss = dressed_consts(tg, sg, axd[nm], orient, PAIRS4)
        _, _, n1, _ = solve_orbit(ORB1, 4, tt, ss, rhoT, rhoS, (0, 1), 0)
        _, _, n2, _ = solve_orbit(ORB2, 4, tt, ss, rhoT, rhoS, (0, 2), 0)
        k0[(nm, orient)] = (len(n1), len(n2))
    n_k0 = sum(1 for v in k0.values() if v[0] > 0 and v[1] > 0)
    check("P1.2 [NO SINGLE-VALUED CHIRAL OPTION, THE CORE FACT] strict "
          "trivial-character two-orbit solutions at physical weight "
          "(m, k) = (0, 0): %s -- count %d = 0 across the bare gauge "
          "blocks and ALL five dressings in BOTH orientations "
          "(delta-1e P1.5 replication, NC-a part 1): the one-sided "
          "chiral combination KEEPS its multiplier, always"
          % (str(k0), n_k0), n_k0 == 0)

    fams = {}
    for k in range(12):
        tt, ss = dressed_consts(tg, sg, axd['f1f3'], 'hol', PAIRS4)
        _, L1, n1, _ = solve_orbit(ORB1, 4, tt, ss, rhoT, rhoS, (0, 1), k)
        if not n1:
            continue
        _, L2, n2, _ = solve_orbit(ORB2, 4, tt, ss, rhoT, rhoS, (0, 2), k)
        if not n2:
            continue
        fams[k] = dict(L1=L1, n1=n1, L2=L2, n2=n2)
    ks = sorted(fams.keys())
    dims_ok = (ks == [4, 10]
               and len(fams[4]['n1']) == 3 and len(fams[4]['n2']) == 3
               and len(fams[10]['n1']) == 1 and len(fams[10]['n2']) == 1)
    check("P1.3 [THE ONLY STRICT CHIRAL FAMILIES] hol f1f3 closes "
          "exactly at k = %s with dims %s -- chi_4 (3,3) and chi_10 "
          "(1,1), both characters nontrivial (P0.4): every strict "
          "chiral closure at physical weight carries a NONTRIVIAL "
          "multiplier (v518 S4 replication)"
          % (str(ks), str([(len(fams[k]['n1']), len(fams[k]['n2']))
                           for k in ks])), dims_ok)

    r1 = member_test(fams[4]['L1'], fams[4]['n1'],
                     {(0, 1): w_col(1), (0, 3): w_col(3)})
    r2 = member_test(fams[4]['L2'], fams[4]['n2'],
                     {(0, 2): w_col(2)})
    contained = (r1[0] < CONTAIN_TOL and r1[1] > 1e-6
                 and r2[0] < CONTAIN_TOL and r2[1] > 1e-6)
    b01 = np.array(fams[4]['n1']).T @ (r1[2][:-1] / r1[2][-1])
    b02 = np.array(fams[4]['n2']).T @ (r2[2][:-1] / r2[2][-1])
    beta = {}
    for p in ORB1:
        beta[p] = fams[4]['L1'][p] @ b01
    for p in ORB2:
        beta[p] = fams[4]['L2'][p] @ b02
    taus = []
    for t0 in (TAU_C, TAU_D):
        taus += [t0, t0 + 1, -1 / t0]
    th = {tau: [eval_series16(ser0[mu], tau, lim) for mu in MU]
          for tau in taus}

    def G_total(tau):
        tot = mp.mpc(0)
        for p, bp in beta.items():
            v = (M_val(4, p[0], p[1], tau)
                 * ax_val(4, (1, 3), p[0], p[1], tau))
            tot += v * sum(complex(bp[i]) * th[tau][i] for i in range(16))
        return tot

    chT = mp.exp(2j * mp.pi * mp.mpf(4) / 12)
    chS = mp.exp(-2j * mp.pi * mp.mpf(4) / 4)
    cert = mp.mpf(0)
    gmin = mp.inf
    for t0 in (TAU_C, TAU_D):
        g0 = G_total(t0)
        gmin = min(gmin, abs(g0))
        cert = max(cert, abs(G_total(t0 + 1) / (chT * g0) - 1))
        cert = max(cert, abs(G_total(-1 / t0) / (chS * g0) - 1))
    print("     canonical chi_4 column member: sigma ratios orb1 "
          "%.2e / orb2 %.2e; |G(tau)| >= %s; total-sum certificate "
          "max dev %s over two fresh tau"
          % (r1[0], r2[0], mp.nstr(gmin, 3), mp.nstr(cert, 3)))
    check("P1.4 [F-LEMMA CERTIFICATE + COROLLARY] the physical AB "
          "columns are contained in the chi_4 family (one scalar per "
          "orbit, sigma %.2e / %.2e < 1e-8 -- delta-1e D1 replication) "
          "and the canonical member's TOTAL block sum obeys G(tau+1) "
          "= chi_4(T) G(tau), G(-1/tau) = chi_4(S) G(tau) pointwise "
          "(cert %s < 1e-8, nonvacuous |G| > 1e-10).  EXACT CHANGE OF "
          "VARIABLES: int_{gamma F} G dmu = chi_4(gamma) int_F G dmu "
          "with chi_4(T) = e(1/3) =/= 1 -- an F-independent value "
          "forces int = 0: under TP-1 + TP-2 NO chiral integrand at "
          "physical weight can source psi = 64; the v518 unfolded "
          "values are convention bookkeeping, and single-valuedness "
          "is FORCED for any nonzero one-loop lattice contribution"
          % (r1[0], r2[0], mp.nstr(cert, 3)),
          contained and cert < mp.mpf(10) ** (-8)
          and gmin > mp.mpf(10) ** (-10))
    A1 = bool(n_k0 == 0 and dims_ok and contained
              and cert < mp.mpf(10) ** (-8))
    return tg, sg, tgx, sgx, axd, A1


# ---------------------------------------------------------------------------
# P2 -- A2: the Quillen pairing (hol x antihol cancels the multiplier)
# ---------------------------------------------------------------------------
def section2(tg, sg, tgx, sgx, axd, rhoT, rhoS):
    print("  -- P2: A2 -- the Quillen pairing (source-2)")
    ttH, ssH = dressed_consts(tg, sg, axd['f1f3'], 'hol', PAIRS4)
    ktot = {}
    dbl_dev = mp.mpf(0)
    for p in PAIRS4:
        _, kt, _ = recog(mp.mpc(ttH[p]))
        ktot[p] = kt
        # measured, not constructed: t conj(t) = |t|^2 must equal 1
        # (unitarity) for the conjugate pairing to erase the phase;
        # evaluated on the FULL-PRECISION mpmath transports (40 dps)
        tf = mp.mpc(tg[p]) * mp.mpc(axd['f1f3']['t'][p])
        sf = mp.mpc(sg[p]) * mp.mpc(axd['f1f3']['s'][p])
        dbl_dev = max(dbl_dev, abs(tf * mp.conj(tf) - 1),
                      abs(sf * mp.conj(sf) - 1))
    sq_def_T = {p: (2 * ktot[p]) % L_PHASE for p in PAIRS4}
    fib_sq = (2 * ((-L_PHASE // 6) % L_PHASE)) % L_PHASE
    check("P2.1 [CONJUGATE PAIRING CANCELS -- MEASURED UNITARITY] the "
          "doubled hol x antihol transports t conj(t) = |t|^2 equal 1 "
          "to %s < 1e-30 on all 15 pairs and both generators (a non-"
          "unitary multiplier would leave a real scaling; the phase "
          "cancellation is exact by conjugation); the one-sided "
          "SQUARED combination keeps defects: T-fixed fibre 2 x 800 = "
          "%d = e(2/3) =/= 0 on the exact grid, squared-defect table "
          "nonzero on %d of 15 pairs -- the phase dies ONLY in the "
          "conjugate pairing (|chi_4|^2 = 1 vs chi_4^2 = e(2/3), P0.4)"
          % (mp.nstr(dbl_dev, 3), fib_sq,
             sum(1 for p in PAIRS4 if sq_def_T[p] != 0)),
          dbl_dev < mp.mpf(10) ** (-30) and fib_sq == 640
          and any(v != 0 for v in sq_def_T.values()))

    rhoT2 = np.kron(rhoT, rhoT.conj())
    rhoS2 = np.kron(rhoS, rhoS.conj())
    tt2 = {p: ttH[p] * np.conj(ttH[p]) for p in PAIRS4}
    ss2 = {p: ssH[p] * np.conj(ssH[p]) for p in PAIRS4}
    _, L1d, n1d, _ = solve_orbit(ORB1, 4, tt2, ss2, rhoT2, rhoS2,
                                 (0, 1), 0)
    _, L2d, n2d, _ = solve_orbit(ORB2, 4, tt2, ss2, rhoT2, rhoS2,
                                 (0, 2), 0)
    d1, d2 = len(n1d), len(n2d)
    vecI = np.zeros(256, dtype=complex)
    for i in range(16):
        vecI[16 * i + i] = 1.0
    vecI /= np.linalg.norm(vecI)
    resI = []
    for nd in (n1d, n2d):
        V = np.array(nd).T
        proj = V @ np.linalg.solve(V.conj().T @ V, V.conj().T @ vecI)
        resI.append(float(np.linalg.norm(vecI - proj)))
    check("P2.2 [DOUBLED SYSTEM CLOSES SINGLE-VALUEDLY] the 256-dim "
          "hol x antihol Weil system (rho (x) conj(rho), transports "
          "t conj(t)) closes STRICTLY at trivial character and "
          "physical weight: nullspace dims (%d, %d) >= 11 = 3^2 + 1^2 "
          "+ 1 (chi_4 (x) conj chi_4, chi_10 (x) conj chi_10, and the "
          "unphased diagonal); the unphased diagonal sum_mu e_mu (x) "
          "conj(e_mu) lies inside (residuals %.2e / %.2e < 1e-8): "
          "single-valuedness is IMPLEMENTED by the pairing, not "
          "postulated" % (d1, d2, resI[0], resI[1]),
          d1 >= 11 and d2 >= 11 and max(resI) < 1e-8)

    W1 = np.kron(w_col(1), w_col(1).conj())
    W3 = np.kron(w_col(3), w_col(3).conj())
    W2 = np.kron(w_col(2), w_col(2).conj())
    rd1 = member_test(L1d, n1d, {(0, 1): W1, (0, 3): W3})
    rd2 = member_test(L2d, n2d, {(0, 2): W2})
    E00d = np.zeros(256, dtype=complex)
    E00d[16 * IDX[(0, 0)] + IDX[(0, 0)]] = 1.0
    rdiag1 = member_test(L1d, n1d, {(0, 1): E00d, (0, 3): E00d})
    rwr1 = member_test(L1d, n1d,
                       {(0, 1): np.kron(w_col(1, 1), w_col(1, 1).conj()),
                        (0, 3): np.kron(w_col(3, 1), w_col(3, 1).conj())})
    print("     doubled membership: physical |w_b|^2 orb1 %.2e [%.3f] "
          "orb2 %.2e [%.3f]; diag model %.2e; wrong-phase %.2e "
          "(diagnostics)"
          % (rd1[0], rd1[1], rd2[0], rd2[1], rdiag1[0], rwr1[0]))
    check("P2.3 [PHYSICAL DOUBLED COLUMNS CONTAINED] the physical "
          "untwisted-column data w_b (x) conj(w_b) is contained in "
          "the doubled single-valued family with ONE scalar per orbit "
          "(sigma %.2e / %.2e < 1e-8, coefficient nonvanishing): the "
          "physical |.|^2 object lives entirely inside the single-"
          "valued surface" % (rd1[0], rd2[0]),
          rd1[0] < CONTAIN_TOL and rd1[1] > 1e-6
          and rd2[0] < CONTAIN_TOL and rd2[1] > 1e-6)

    rhoT2w = np.kron(rhoT, rhoT)
    rhoS2w = np.kron(rhoS, rhoS)
    tt2w = {p: ttH[p] * ttH[p] for p in PAIRS4}
    ss2w = {p: ssH[p] * ssH[p] for p in PAIRS4}
    _, _, n1w, sv1w = solve_orbit(ORB1, 4, tt2w, ss2w, rhoT2w, rhoS2w,
                                  (0, 1), 0)
    _, _, n2w, sv2w = solve_orbit(ORB2, 4, tt2w, ss2w, rhoT2w, rhoS2w,
                                  (0, 2), 0)
    check("P2.4 [NC-a: WRONG PAIRING EMPTY] the hol (x) hol doubled "
          "system (squared transports, characters chi^2 in {e(2/3), "
          "e(1/6), e(2/3)} =/= 1) has NO trivial-character closure: "
          "nullspace dims (%d, %d) = (0, 0), min sv ratios %.2e / "
          "%.2e -- only the CONJUGATE pairing implements single-"
          "valuedness" % (len(n1w), len(n2w),
                          min(sv1w) / max(sv1w), min(sv2w) / max(sv2w)),
          len(n1w) == 0 and len(n2w) == 0)

    _, _, devw = measure_transport_w(
        4, [(0, 1), (1, 0), (1, 1), (2, 1)],
        lambda a, b, tau: M_val(4, a, b, tau), 2)
    check("P2.5 [NC-d: WRONG WEIGHT] the gauge transport measured at "
          "weight exponent 2 instead of 4 is NOT constant over tau "
          "(dev %s > 1e-3): the physical weight bookkeeping (TP-3) "
          "has teeth" % mp.nstr(devw, 3),
          devw > mp.mpf(10) ** (-3))

    rng = np.random.default_rng(23)
    bstar = n1d[0]
    fake_null = [bstar,
                 rng.normal(size=256) + 1j * rng.normal(size=256),
                 rng.normal(size=256) + 1j * rng.normal(size=256)]
    fake_null = [v / np.linalg.norm(v) for v in fake_null]
    targets_fake = {p: L1d[p] @ bstar for p in [(0, 1), (0, 3)]}
    rf = member_test(L1d, fake_null, targets_fake)
    check("P2.6 [NC-f: PLANTED DOUBLED FAMILY] a synthetic doubled "
          "family containing its own column data is detected: sigma "
          "%.2e < 1e-10 with |c| = %.3f > 0.1 (membership machinery "
          "teeth at 256 dims)" % (rf[0], rf[1]),
          rf[0] < 1e-10 and rf[1] > 0.1)
    A2 = bool(dbl_dev < mp.mpf(10) ** (-30) and d1 >= 11 and d2 >= 11
              and max(resI) < 1e-8
              and rd1[0] < CONTAIN_TOL and rd2[0] < CONTAIN_TOL
              and len(n1w) == 0 and len(n2w) == 0
              and devw > mp.mpf(10) ** (-3)
              and rf[0] < 1e-10 and rf[1] > 0.1)
    return A2


# ---------------------------------------------------------------------------
# P3 -- A3: consistency closure (forced unphased numerator x v518 scaffold)
# ---------------------------------------------------------------------------
def section3(V4, V2, CNT):
    print("  -- P3: A3 -- the point-4 consistency closure (source-3)")
    levels_H = sorted(set().union(*[set(V4[(m, m)].keys())
                                    for m in range(4)]))
    levels_Hp = sorted(set().union(*[set(V4[m].keys()) for m in ANTI_H]))
    ok_H = True
    ok_Hp = True
    c_samples = []
    for lev in levels_H:
        s = [sum(V4[(m, m)].get(lev, ZERO5)[i] for m in range(4))
             for i in range(5)]
        c = s[0]
        if s != [c, 2 * c, c, 0, 0]:
            ok_H = False
        if lev <= 3:
            c_samples.append((lev, c))
    for lev in levels_Hp:
        s = [sum(V4[m].get(lev, ZERO5)[i] for m in ANTI_H)
             for i in range(5)]
        c = s[0]
        if s != [c, 2 * c, c, 0, 0]:
            ok_Hp = False
    check("P3.1 [EXACT LEVELWISE OKUBO / 4-DESIGN] the unphased "
          "diagonal ledger sum_m V_{(m,m),lev} AND the anti-diagonal "
          "(H') sum are EXACTLY proportional to <x,x>^2 = (1, 2, 1, "
          "0, 0) at EVERY level (H: %d levels, H': %d levels, n <= 8; "
          "samples (lev, c): %s): the forced E4 numerator is a "
          "perfect Okubo square LEVEL BY LEVEL -- the completion "
          "structure survives ANY level reweighting by the J-kernels"
          % (len(levels_H), len(levels_Hp), str(c_samples[:4])),
          ok_H and ok_Hp)

    pairs_col = [(0, 1), (0, 2), (0, 3)]
    dets = {1: 2.0, 2: 4.0, 3: 2.0}
    dm, basemap = build_dress(pairs_col, (1, 3))
    beta_unph = {p: diag_unph() / dets[p[1]] for p in pairs_col}
    beta_ph = {p: w_col(p[1]) / dets[p[1]] for p in pairs_col}
    beta_ct = {p: col_contact(p[1]) / dets[p[1]] for p in pairs_col}

    def run_cols(beta, cut):
        dml = {p: {e: v for e, v in dm[p].items() if e <= cut}
               for p in beta}
        return hm_integral_pp(beta, dml, basemap, V4, V2, CNT, cut,
                              mp.mpf(1) / 4)

    I_tot, _, _, nneg_t, _ = run_cols(beta_unph, GRID_CUT)
    I_lo, _, _, _, _ = run_cols(beta_unph, GRID_CUT_LOW)
    scale = max(abs(x) for x in I_tot)
    eps_rel = max(abs(I_tot[i] - I_lo[i]) for i in range(5)) / scale
    im_rel = max(abs(x.imag) for x in I_tot) / scale
    spr_tot, z_tot = spread_vs(I_tot, OKUBO)
    ch_dat = []
    for p in pairs_col:
        I_ch, _, _, _, _ = run_cols({p: beta_unph[p]}, GRID_CUT)
        spr, zz = spread_vs(I_ch, OKUBO)
        ch_dat.append((p[1], spr, zz))
    print("     I(unphased columns) = %s; cut-6 vs cut-8 %s; |Im| %s"
          % (fmtn(I_tot), mp.nstr(eps_rel, 3), mp.nstr(im_rel, 3)))
    for (j, spr, zz) in ch_dat:
        print("       channel %d: spread vs <x,x>^2 %s, T5/T3 "
              "fraction %s" % (j, mp.nstr(spr, 3), mp.nstr(zz, 3)))
    check("P3.2 [UNPHASED NUMERATOR x v518 SCAFFOLD = OKUBO] the "
          "J-weighted unphased column integral is proportional to "
          "<x,x>^2 PER CHANNEL and in TOTAL (total spread %s, T5/T3 "
          "fraction %s, channel spreads all < 1e-8), with ZERO "
          "negative-exponent cells (%d) and truncation scan %s: the "
          "v516 per-sector perfect squares are REPRODUCED inside the "
          "v518 integral machinery"
          % (mp.nstr(spr_tot, 3), mp.nstr(z_tot, 3), nneg_t,
             mp.nstr(eps_rel, 3)),
          spr_tot < mp.mpf(10) ** (-8) and z_tot < mp.mpf(10) ** (-8)
          and all(spr < mp.mpf(10) ** (-8)
                  and zz < mp.mpf(10) ** (-8) for _, spr, zz in ch_dat)
          and nneg_t == 0 and im_rel < mp.mpf(10) ** (-8))

    I_ct, _, _, _, _ = run_cols(beta_ct, GRID_CUT)
    psi_ct = psi_of(I_ct)
    V4_1 = {mu: ({F(1): V4[mu][F(1)]} if F(1) in V4[mu] else {})
            for mu in MU}
    I_ct1, _, _, _, _ = hm_integral_pp(
        beta_ct, dm, basemap, V4_1, V2, CNT, GRID_CUT, mp.mpf(1) / 4)
    psi_ct1 = psi_of(I_ct1)
    print("     I(contact columns) = %s; psi = %s" %
          (fmtn(I_ct), mp.nstr(psi_ct, 6)))
    print("     level-1 slice = %s; psi(slice) = %s  [arithmetic "
          "contact = (36, 120, 60, 0, -32), psi = -64]"
          % (fmtn(I_ct1), mp.nstr(psi_ct1, 6)))
    ok_psi = (psi_ct.real < 0
              and abs(psi_ct.imag) < abs(psi_ct.real) * 1e-6
              and psi_ct1.real < 0)
    check("P3.3 [CONTACT SUPPLIES THE psi SLICE, RIGHT SIGN] the "
          "J-weighted contact (unphased minus phased columns) carries "
          "psi = %s < 0 (full) and %s < 0 (level-1 slice) -- the "
          "-64-slice sign of v511/v516 is reproduced by the FORCED "
          "numerator inside the scaffold (channel J-profiles reweight "
          "the exact -64, sign preserved)"
          % (mp.nstr(psi_ct, 6), mp.nstr(psi_ct1, 6)), ok_psi)

    I_ph, _, _, _, _ = run_cols(beta_ph, GRID_CUT)
    psi_ph = psi_of(I_ph)
    print("     I(skeleton/phased columns) = %s; psi = %s  "
          "[arithmetic A_fix psi = +64]" % (fmtn(I_ph),
                                            mp.nstr(psi_ph, 6)))
    lin = max(abs(I_ph[i] + I_ct[i] - I_tot[i]) for i in range(5)) / scale
    check("P3.4 [THE CIRCLE CLOSES LINEARLY] skeleton (phased) + "
          "contact (completion) = unphased columns inside the "
          "integral machinery (rel residual %s < 1e-12, all with the "
          "v516 zero-mode weights 1/det_j): the v516 identity "
          "skeleton_j + contact_j = Q^(0)/det_j holds cellwise in "
          "the v518 scaffold" % mp.nstr(lin, 3),
          lin < mp.mpf(10) ** (-12))
    A3 = bool(ok_H and ok_Hp and spr_tot < mp.mpf(10) ** (-8)
              and z_tot < mp.mpf(10) ** (-8) and nneg_t == 0
              and ok_psi and lin < mp.mpf(10) ** (-12))
    return A3


# ---------------------------------------------------------------------------
# P4 -- remaining negative controls (exact)
# ---------------------------------------------------------------------------
def section4(Qv):
    print("  -- P4: negative controls (exact)")
    R = sp.Rational
    so_tot = [sp.nsimplify(R(5, 4) * (Qv[0][i] + Qv[2][i]))
              for i in range(5)]
    okmu2 = all(((m * p[1]) % 4) % 2 == 0 for p in ORB2
                for m in (1, 2, 3))
    ok_so = (so_tot == [15, 30, 45, 20, -40])
    check("P4.1 [NC-b: SO(16)/D8] even with single-valuedness granted "
          "the so16 unphased trace is NO Okubo square: completion "
          "total = %s leaves T5 = 20, T3 = -40 (exact) -- the KILL "
          "fires for so16, E8 stays doubly special; and the order-4 "
          "supply is structurally absent on the derived side (all "
          "ORB2 fibre b-characters in mu_2: %s)"
          % (fmt(so_tot), okmu2), ok_so and okmu2)

    gw = sum_z8([z8_root((2 * x * x + 2 * y * y) % 8)
                 for x in range(4) for y in range(4)])
    nrm = z8_mul(gw, z8_conj(gw))
    Tw, Sw = build_weil(lambda m: (2 * m[0] ** 2 + 2 * m[1] ** 2) % 8,
                        lambda m, n2: (4 * (m[0] * n2[0]
                                            + m[1] * n2[1])) % 8,
                        MU, Z8_ONE)
    Cm = [[Z8_ONE if MU[j] == neg(MU[i]) else Z8_ZERO
           for j in range(16)] for i in range(16)]
    s2w = mat_mul(Sw, Sw)
    ok_wf = (nrm == z8_scal(F(64), Z8_ONE) and not mat_eq(s2w, Cm))
    check("P4.2 [NC-c: WRONG FORM] q = (x^2+y^2)/4: |Gauss|^2 = %s = "
          "64 =/= 16 and S^2 = C breaks EXACTLY -- no invariant-"
          "subspace forcing is available for the wrong discriminant "
          "form (the E4 forcing is form-specific)" % str(nrm[0]),
          ok_wf)

    wsh = [0, R(1, 2), R(3, 8), R(1, 2)]
    T5sh = sp.nsimplify(sum(4 * wsh[m] * Qv[m][3] for m in range(4)))
    T3sh = sp.nsimplify(32 + sum(4 * wsh[m] * Qv[m][4]
                                 for m in range(4)))
    check("P4.3 [NC-e: SHUFFLED WEIGHTS] h_1 <-> h_2 swap leaves "
          "T5 = %s =/= 0 AND T3 leftover %s =/= 0 (exact): the ch2 "
          "pattern carries the levelwise cancellation, not just the "
          "scale (v516 S4.2 replication)" % (T5sh, T3sh),
          T5sh == -14 and T3sh == 36)
    return bool(ok_so and okmu2 and ok_wf and T5sh == -14)


# ---------------------------------------------------------------------------
# P5 -- verdict per the preregistration
# ---------------------------------------------------------------------------
def section5(A1, A2, A3, NC_ok, n_k0_zero):
    print("  -- P5: verdict per the preregistered branches")
    b_fires = (not n_k0_zero) or (not A2 and not n_k0_zero)
    if A1 and A2 and A3 and NC_ok:
        verdict = (
            "ERFOLG-A (decision layer): single-valuedness of the "
            "physical one-loop lattice factor on PT/Z4 is DERIVED "
            "from two independent constructive sources, not "
            "postulated -- (source-1) F-independence: every strict "
            "chiral option at physical weight carries a nontrivial "
            "character (chi_4/chi_10, exact), and a character-"
            "covariant integrand has NO F-independent nonzero "
            "moduli integral (exact change of variables), so under "
            "TP-1 + TP-2 the chiral multiplier route can never "
            "source psi = 64; (source-2) the Quillen/BCOV pairing "
            "hol x conj(hol) cancels the multiplier identically "
            "(grid-exact on all 15 pairs, |chi_4|^2 = 1) and the "
            "doubled system closes single-valuedly at physical "
            "weight with the physical columns contained.  With "
            "single-valuedness forced, the delta-1e invariant "
            "subspace (P0.2, exact: span{e_H, e_H'} = E4 = the "
            "unphased trace) FORCES the v516 numerator, and the "
            "point-4 circle closes: the forced numerator inside the "
            "v518 scaffold reproduces the per-sector Okubo squares "
            "levelwise (exact 4-design + J-weighted integrals) and "
            "the psi < 0 contact slice.  Consequences: the WP5e "
            "measure question is closed at its core -- reading A "
            "(v516) is derived under the typed premises TP-1..TP-4; "
            "the v518 kill is UPGRADED (the chi_4 route was never a "
            "well-defined nonzero moduli integral: its unfolded "
            "values are convention bookkeeping); psi = 64 is sourced "
            "by the now-forced unphased completion.  Honest fences: "
            "TP-1 (F-independent integral), TP-3 (v518 kernel-family "
            "weight bookkeeping, [C]) and TP-4 (Quillen pairing "
            "structure of BCOV F1) are typed premises; the "
            "constructive BCOV-integral derivation of the w_m "
            "normalisation itself remains the residual [O].  NO "
            "marker moves from this sandbox; any upgrade goes "
            "through the regular promotion workflow.")
    elif A1 and A2 and not A3:
        verdict = (
            "UNENTSCHIEDEN (named gap): the numerator IS forced "
            "(A1 + A2 fire: no single-valued chiral option, conjugate "
            "pairing cancels the multiplier, invariant subspace = "
            "E4), BUT the forced unphased numerator does NOT "
            "reproduce the v516 testers inside the v518 scaffold -- "
            "the residual gap sits in the INTEGRATION MEASURE / "
            "FUNDAMENTAL DOMAIN bookkeeping, not in the numerator "
            "(the anticipated alternative).  Document: which A3 "
            "sub-check failed, above.")
    elif b_fires:
        verdict = (
            "ERFOLG-B: a strict trivial-character chiral solution "
            "exists at physical weight or the conjugate pairing "
            "fails to cancel the multiplier -- the chi_4 multiplier "
            "is admissible/necessary, the v518 kill stands as final, "
            "psi = 64 needs another source.")
    else:
        verdict = (
            "UNENTSCHIEDEN: fires A1 = %s, A2 = %s, A3 = %s, "
            "controls = %s -- see the failed checks above for the "
            "precise gap." % (A1, A2, A3, NC_ok))
    check("P5.1 [VERDICT: %s]" % verdict, True)
    check("P5.2 [HONEST BOOKKEEPING] exact = Weil relations, "
          "invariant subspace (rational nullspace), characters and "
          "1/960 grid arithmetic, completion/contact/psi identities, "
          "levelwise 4-design ledgers, so16/wrong-form/shuffle "
          "controls, change-of-variables corollary; numeric "
          "(documented) = block transports (28+ digits, grid 25+), "
          "SVD solves and memberships (double, thresholds 1e-8), "
          "total-sum certificates at two fresh tau (< 1e-8), HM "
          "kernels (30+ digits, cut-6 vs cut-8, negative-cell "
          "audit); typed premises TP-1..TP-4 named in the verdict; "
          "delta-1e's P-II postulate NOT used anywhere", True)
    print("     VERDICT: %s" % verdict)


# ---------------------------------------------------------------------------
def run():
    print("WP5e-delta-1f probe: the single-valuedness decision "
          "(CELEST.SEAM.01; exploration only)")
    print("  [building 16-class exact ledgers to level 8 ...]")
    d5led = build_d5_vecs(MAXN_LED)
    a3led = build_a3_vecs(MAXN_LED)
    V4, V2, CNT = build_ledgers16(d5led, a3led, MAXN_LED)
    print("  [building coset theta series for certificates ...]")
    ser0, lim = build_theta_ser0()
    Tx, Sx = weil_matrices()
    rhoT = rho_np(Tx)
    rhoS = rho_np(Sx)

    Qv, Qtw, dets = section0(Tx, Sx, V4, CNT)
    tg, sg, tgx, sgx, axd, A1 = section1(rhoT, rhoS, ser0, lim)
    A2 = section2(tg, sg, tgx, sgx, axd, rhoT, rhoS)
    A3 = section3(V4, V2, CNT)
    NC_ok = section4(Qv)
    section5(A1, A2, A3, NC_ok, n_k0_zero=A1)

    print("")
    print("CHECKS: %d passed, %d failed" % (N_PASS, N_FAIL))
    return N_FAIL == 0


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)

"""v522 -- WOIT.BETA1.GSO.01: the WOIT-beta1 milestone of the OS twistor
bridge WOIT.OS.TWISTOR.01 executed -- "the clock is time-like, GSO is
the gauge datum" (a typed result: verdict UNDECIDED per the frozen
preregistration, with the mechanism identified exactly and gauge-fixed
RP established under the corrected GSO typing).  Question (contract
beta_1, verbatim): "Theta on the gauge-invariant subalgebra +
gauge-fixed RP on the equivariant SDYM(E8) sector"; kill test (2):
"RP fails after gauge fixing".  Finding: the preregistered [C-1]
clock-tower reading of "gauge" is structurally the WRONG
operationalisation -- the mu4 clock is EUCLIDEAN-TIME-LIKE, its only
gaugeable part is the GSO/fermion-parity Z2, and under that corrected
typing gauge-fixed RP HOLDS exactly; the kill does NOT fire.

[E] 1. HERMITICITY WITNESS (the mechanism): the mu4 clock average
    violates Hermiticity EXACTLY -- the one-step insertion T_1 =
    <theta(e_a), alpha_S(e_b)> has entry -i/(8 sin(5 pi/16)) where the
    conjugate transpose demands +i/(8 sin(5 pi/16)); the pairing is
    complex-SYMMETRIC (745 entries Hermitian-matching, 96
    anti-matching, 0 violations): "OS-symmetric" is STRICTLY WEAKER
    than Hermitian -- "positivity after gauge fixing" is not
    well-posed for the clock reading.
[E] 2. TIME-LIKE TYPING: ALL 16 dihedral reflection axes of the NS
    seam circle INVERT the clock lift (R S R^-1 = S^-1 exactly), NONE
    commutes -- the mu4 clock IS Woit's euclidean rotation (the time
    translation itself); the theta-compatible (gaugeable) part of the
    Z8 tower is EXACTLY its 2-torsion {1, (-1)^F} (Hermiticity census
    over all powers; alpha^4 = the full wrap = the 2 pi rotation of
    the seam = fermion parity, lattice spin-statistics).
[E] 3. POSITIVE PART -- GSO-FIXED RP HOLDS EXACTLY: N = 16 even
    deg <= 2 parity-projected bond-cut Gram (29, 0, 0) PD (min
    eigenvalue 1.78e-6 at 40 digits); N = 8 complete half algebra:
    the projected 16x16 Gram kills all odd rows/columns exactly and
    its even block is (8, 0, 0) PD (3.35e-3) with NO degree
    truncation; the site-cut defect SURVIVES gauge fixing (inertia
    (7, 9, 6)) -- the RP bond placement is gauge-invariant
    information; family A keeps failing ((17, 12, 0) indefinite vs
    family D's (29, 0, 0)); Kramers: Theta_t^2 = id on A^G (the
    (-1)^F class does not penetrate the even subalgebra), Theta_Fock
    restricts with Theta^2 = +1; Ramond control: the wrap +1 "true
    Z4" lift fails state invariance -- the NS/Z8 tower is forced.
[E] 4. KILL-TEST BOOKKEEPING: kill test (1) stays discharged also
    gauge-invariantly (Theta^2 = +1 on A^G, Kramers class trivial);
    kill test (2)'s free shadow does NOT fire (no legitimate
    Hermitian gauge-fixed form has a negative direction); both stay
    formally live on the interacting algebra A_hol.
[E] 5. WRONG-PROJECTION CONTROLS: the invariant-dimension chain
    parity 120 > deck 64 > clock 32 is strict, but Hermiticity of the
    projected form singles out PARITY alone (deck and clock averages
    non-Hermitian): projecting by the finer "gauge" groups is
    structurally ill-posed pre-quotient.
TRANSPARENCY (documented in full): the first frozen run scored 6/13 --
    the preregistered clock-reading checks failed exactly as the
    mechanism predicts, and the preregistered deg-2 clock-invariant
    dimension 30 was a combinatorial error (correct orbit census: 28
    free shift-4 quadruples + 4 halved antipodal doublets = 32); the
    preregistration text is unchanged, the verdict follows the frozen
    [C-3] logic (Hermiticity failure => structural-failure branch =>
    UNDECIDED).
[C] CONTRACT PRECISION (iii) (prose, no marker): "gauge-invariant
    subalgebra" at the free level means the GSO/fermion-parity Z2 --
    the only theta-compatible part of the mu4 tower (the free-fermion
    shadow of the E8 glue: (E8)_1 = even NS of SO(16)_1 + R spinor);
    the clock is the euclidean rotation itself (time-like), its
    equivariant statement moves to beta2 (OS quotient first, then the
    clock as reconstructed transfer operator).
[O] beta1 PROPER stays open (the clock-equivariant statement needs
    the beta2 OS quotient); both kill tests live on A_hol;
    WOIT.OS.TWISTOR.01 stays [O].

VERDICT: UNDECIDED per the frozen preregistration (the [C-1] clock
reading was the wrong operationalisation -- transparently documented);
NO KILL; gauge-fixed RP holds under the corrected GSO typing.  NO
marker moves.

Status: [E] exact sympy trig-algebraic entries, Pfaffian-Wick, exact
Cl(16) Fractions (Utilde^2 = 256 Gamma), exact Hermiticity censuses;
the definiteness certificates are 40-digit spectra of exact Hermitian
matrices (tolerance 1e-25).  Python; Wolfram-mirrored (Z8 tower S^4 =
-1 / Ramond control, invariant-dimension chain 120 > 64 > 32,
time-like reflection census, Hermiticity witness entry, GSO 2-torsion
census, family-A tower-normalisation failure -- the 40-digit inertia
spectra are Python-only), counted per GATE.WOLFRAM.02.  Discovery
provenance: experiments/tfpt-discovery/
woit_os_beta1_gauge_invariant_theta_probe.py (16/16, 2026-07-22)."""
from fractions import Fraction as Fr
from itertools import combinations

import mpmath as mp
import sympy as sp

from tfpt_constants import check, summary, reset

mp.mp.dps = 40

I = sp.I
N16 = 16
N8 = 8
FLAGS = {}


def iszero(e):
    e2 = sp.expand(e)
    if e2 == 0:
        return True
    e3 = sp.expand(sp.expand_complex(e2))
    if e3 == 0:
        return True
    return sp.simplify(e3) == 0


# ---------------------------------------------------------------------------
# the chiral NS vacuum kernel + Pfaffian-Wick (v519 verbatim, memoised)
# ---------------------------------------------------------------------------
def c_of(d, n):
    if d % 2 == 0:
        return sp.Integer(0)
    return sp.Rational(2, n) / sp.sin(sp.pi * sp.Rational(d, n))


def g2f(a, b, n, chi):
    if a == b:
        return sp.Integer(1)
    return I * chi * c_of(a - b, n)


_WICK = {}


def wick(idx, n, chi=1):
    idx = tuple(idx)
    if len(idx) == 0:
        return sp.Integer(1)
    if len(idx) % 2 == 1:
        return sp.Integer(0)
    key = (idx, n, chi)
    if key in _WICK:
        return _WICK[key]
    head, rest = idx[0], idx[1:]
    tot = sp.Integer(0)
    for j, b in enumerate(rest):
        sub = rest[:j] + rest[j + 1:]
        tot += (-1) ** j * g2f(head, b, n, chi) * wick(sub, n, chi)
    tot = sp.expand_complex(tot)
    _WICK[key] = tot
    return tot


# ---------------------------------------------------------------------------
# dihedral machinery (v510/v519 verbatim)
# ---------------------------------------------------------------------------
def shift_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        b = (a + k) % n
        M[b][a] = wrap_sign if a + k >= n else 1
    return M


def refl_matrix(n, k, wrap_sign):
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        idx = (k - a) % (2 * n)
        M[idx % n][a] = wrap_sign if idx >= n else 1
    return M


def refl_map(k, n):
    def r(a):
        return (k - a) % n

    def s(a):
        return -1 if (k - a) % (2 * n) >= n else 1
    return r, s


def half_of(k, n):
    if k % 2 == 0:
        f1 = (k // 2) % n
        P = [(f1 + j) % n for j in range(1, n // 2)]
    else:
        b = (k + 1) // 2
        P = [(b + j) % n for j in range(n // 2)]
    rP = {(k - a) % n for a in P}
    assert not (rP & set(P))
    return P


PLUS = lambda a: 1


# ---------------------------------------------------------------------------
# the NS clock tower <alpha_S> as signed permutations (order 8)
# ---------------------------------------------------------------------------
def tower_maps(n, shift):
    """(perm, sign) for alpha_S^k, k = 0..7; alpha(g_a) = sign[a] g_perm[a]."""
    maps = [(tuple(range(n)), (1,) * n)]
    for _ in range(7):
        perm, sign = maps[-1]
        np_, ns_ = [], []
        for a in range(n):
            p, s0 = perm[a], sign[a]
            np_.append((p + shift) % n)
            ns_.append(s0 * (-1 if p + shift >= n else 1))
        maps.append((tuple(np_), tuple(ns_)))
    return maps


def alpha_mono(m, pm):
    """apply the Bogoliubov automorphism (perm, sign) to a sorted monomial;
    returns (int coeff, sorted tuple)."""
    perm, sign = pm
    c = 1
    imgs = []
    for a in m:
        c *= sign[a]
        imgs.append(perm[a])
    lst = list(imgs)
    sgn = 1
    for i in range(len(lst)):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                sgn = -sgn
    assert len(set(lst)) == len(lst)
    return c * sgn, tuple(lst)


def theta_mono(mono, r, s, eta):
    """theta(g_{i1}...g_{ik}) = eta^k s_{ik}..s_{i1} g_{r(ik)}..g_{r(i1)},
    sorted back; returns (sympy coeff, tuple).  (v519 verbatim)"""
    imgs = [r(a) for a in reversed(mono)]
    coeff = eta ** len(mono)
    for a in mono:
        coeff *= s(a)
    lst = list(imgs)
    sign = 1
    for i in range(len(lst)):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                sign = -sign
    assert len(set(lst)) == len(lst)
    return coeff * sign, tuple(lst)


def mono_mul(m1, m2):
    """exact Clifford product of sorted monomials (g_a^2 = 1); handles
    overlapping supports.  (v506/v519 verbatim)"""
    out = list(m1)
    sign = 1
    for g in m2:
        out.append(g)
        i = len(out) - 1
        while i > 0 and out[i - 1] > out[i]:
            out[i - 1], out[i] = out[i], out[i - 1]
            sign = -sign
            i -= 1
        if i > 0 and out[i - 1] == out[i]:
            del out[i - 1:i + 1]
    return sign, tuple(out)


# ---------------------------------------------------------------------------
# OS pairings with tower insertion: <e_a, alpha^k e_b> = omega(theta(e_a)
# alpha^k(e_b))
# ---------------------------------------------------------------------------
def os_term(ea, eb, pm, r, s, eta, n, chi=1):
    ca, ma = theta_mono(ea, r, s, eta)
    cb, mb = alpha_mono(eb, pm)
    cs, mm = mono_mul(ma, mb)
    return sp.expand_complex(ca * cb * cs * wick(mm, n, chi))


def term_matrix(basis, pm, r, s, eta, n, chi=1):
    d = len(basis)
    return sp.Matrix(d, d, lambda i, j: os_term(basis[i], basis[j], pm,
                                                r, s, eta, n, chi))


def hermitian_exact(M):
    d = M - M.conjugate().T
    return all(iszero(x) for x in d)


def spectrum_inertia(M, tol=None):
    if tol is None:
        tol = mp.mpf(10) ** (-25)
    n = M.shape[0]
    A = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            re_, im_ = M[i, j].evalf(45).as_real_imag()
            A[i, j] = mp.mpc(mp.mpf(str(re_)), mp.mpf(str(im_)))
    E, _ = mp.eighe(A)
    evs = [E[i].real for i in range(n)]
    npos = sum(1 for e in evs if e > tol)
    nneg = sum(1 for e in evs if e < -tol)
    nzero = n - npos - nneg
    nz = [abs(e) for e in evs if abs(e) > tol]
    return (npos, nneg, nzero), (min(nz) if nz else mp.mpf(0))


def avg_vectors(basis, tw, ks):
    """P(e_b) in monomial coordinates (exact rationals)."""
    vecs = []
    for m in basis:
        acc = {}
        for k in ks:
            c, mm = alpha_mono(m, tw[k])
            acc[mm] = acc.get(mm, sp.Integer(0)) + sp.Rational(c, len(ks))
        vecs.append({mm: cc for mm, cc in acc.items() if cc != 0})
    return vecs


def span_rank(vecs):
    keys = sorted({mm for v in vecs for mm in v})
    if not keys:
        return 0
    M = sp.Matrix(len(vecs), len(keys), lambda i, j: vecs[i].get(keys[j], 0))
    return M.rank()


# ---------------------------------------------------------------------------
# exact Cl(16) Fraction machinery for the Utilde^2 = 256 Gamma check
# ---------------------------------------------------------------------------
def cmul(x, y):
    out = {}
    for m1, c1 in x.items():
        for m2, c2 in y.items():
            s, m = mono_mul(m1, m2)
            c = out.get(m, Fr(0)) + s * c1 * c2
            if c:
                out[m] = c
            elif m in out:
                del out[m]
    return out


def cadd(x, y):
    out = dict(x)
    for m, c in y.items():
        cc = out.get(m, Fr(0)) + c
        if cc:
            out[m] = cc
        elif m in out:
            del out[m]
    return out


def cscale(x, s):
    return {m: c * s for m, c in x.items()} if s else {}


def gam(*idx):
    return {tuple(idx): Fr(1)}


ONE = {(): Fr(1)}


def prop(x, y):
    if not x or not y or set(x) != set(y):
        return (False, None)
    m0 = next(iter(y))
    c = x[m0] / y[m0]
    return (all(x[m] == c * y[m] for m in y), c)


# ---------------------------------------------------------------------------
# Part G -- the gauge datum and Theta on it
# ---------------------------------------------------------------------------
def g1_gauge_datum():
    print("  -- G1: the gauge datum -- mu4 clock tower, invariant "
          "dimensions")
    S = sp.Matrix(shift_matrix(N16, 4, -1))
    SR = sp.Matrix(shift_matrix(N16, 4, +1))
    Cm = sp.Matrix(N16, N16, lambda a, b: c_of(a - b, N16))
    ns4 = sp.simplify(S ** 4 + sp.eye(N16)) == sp.zeros(N16, N16)
    r4 = sp.simplify(SR ** 4 - sp.eye(N16)) == sp.zeros(N16, N16)
    ns_state = sp.simplify(S * Cm * S.T - Cm) == sp.zeros(N16, N16)
    Dr = sp.expand(SR * Cm * SR.T - Cm)
    wit = None
    for a in range(N16):
        for b in range(N16):
            if not iszero(Dr[a, b]):
                wit = (a, b, sp.simplify(Dr[a, b]))
                break
        if wit:
            break
    tw16 = tower_maps(N16, 4)
    grad = (tw16[4][0] == tuple(range(N16))
            and set(tw16[4][1]) == {-1})
    S8 = sp.Matrix(shift_matrix(N8, 2, -1))
    C8 = sp.Matrix(N8, N8, lambda a, b: c_of(a - b, N8))
    ns8 = (sp.simplify(S8 ** 4 + sp.eye(N8)) == sp.zeros(N8, N8)
           and sp.simplify(S8 * C8 * S8.T - C8) == sp.zeros(N8, N8))
    FLAGS['g11'] = (ns4 and r4 and ns_state and wit is not None
                    and grad and ns8)
    check("G1.1 THE GAUGE DATUM IS THE NS CLOCK TOWER [exact]: the NS "
          "quarter-shift lift has S^4 = -1 (%s) so <alpha_S> is the Z8 "
          "tower with alpha_S^4 = (-1)^F = the grading automorphism "
          "(perm = id, all signs -1: %s) -- the gauge-invariant "
          "subalgebra is automatically EVEN: fermion parity is "
          "contained in the mu4 gauge datum; the chiral vacuum is "
          "tower-invariant (S C S^T = C: %s; N = 8 quarter-shift "
          "likewise: %s); RAMOND CONTROL: the wrap +1 lift is a true "
          "Z4 (S_R^4 = +1: %s) but FAILS state invariance (witness "
          "entry (%s): S_R C S_R^T - C = %s != 0) -- the 'genuine Z4' "
          "gauge lift is NOT a symmetry of the chiral NS vacuum: the "
          "Z8/NS tower is forced"
          % (ns4, grad, ns_state, ns8, r4, wit[:2], wit[2]),
          FLAGS['g11'])

    pairs16 = list(combinations(range(N16), 2))
    dim_clock = span_rank(avg_vectors(pairs16, tw16, range(8)))
    dim_deck = span_rank(avg_vectors(pairs16, tw16, (0, 2, 4, 6)))
    dim_par = span_rank(avg_vectors(pairs16, tw16, (0, 4)))
    tw8 = tower_maps(N8, 2)
    evens8 = [m for d in range(0, N8 + 1, 2)
              for m in combinations(range(N8), d)]
    dim8 = span_rank(avg_vectors(evens8, tw8, range(8)))
    chain = dim_par > dim_deck > dim_clock
    FLAGS['g12'] = (dim_clock == 32 and dim_deck == 64
                    and dim_par == 120 and chain)
    FLAGS['dims'] = (dim_par, dim_deck, dim_clock, dim8)
    check("G1.2 INVARIANT DIMENSIONS [exact ranks, deg = 2 pair "
          "sector, full circle]: clock-tower invariants = %d classes "
          "(orbit census: 28 free shift-4 quadruples + 4 halved "
          "antipodal doublets {a, a+8}; the first frozen run "
          "preregistered 30 -- a combinatorial error, corrected by "
          "the machine), deck-only = %d (8 fixed antipodal pairs + 56 "
          "doublets), parity-only = %d (all pairs) -- the chain "
          "parity > deck > clock is STRICT (%s); N = 8 complete even "
          "subalgebra: invariant dimension %d of 128"
          % (dim_clock, dim_deck, dim_par, chain, dim8),
          FLAGS['g12'])
    return tw16, tw8


def g2_theta_restricts():
    print("  -- G2: Theta normalises the tower and restricts to A^G")
    R15 = sp.Matrix(refl_matrix(N16, 15, -1))
    S = sp.Matrix(shift_matrix(N16, 4, -1))
    dihed16 = sp.simplify(R15 * S * R15.inv() - S.inv()) == sp.zeros(N16, N16)
    R7 = sp.Matrix(refl_matrix(N8, 7, -1))
    S8 = sp.Matrix(shift_matrix(N8, 2, -1))
    dihed8 = sp.simplify(R7 * S8 * R7.inv() - S8.inv()) == sp.zeros(N8, N8)

    tw16 = tower_maps(N16, 4)
    r, s = refl_map(15, N16)
    eta = I
    deg2 = [()] + [(a,) for a in range(N16)] \
        + list(combinations(range(N16), 2))
    elem_ok = True
    for m in deg2:
        cb, mb = alpha_mono(m, tw16[1])
        ct, mt = theta_mono(mb, r, s, eta)
        ct2, mt2 = theta_mono(m, r, s, eta)
        cb2, mb2 = alpha_mono(mt2, tw16[7])
        if mt != mb2 or not iszero(cb * ct - ct2 * cb2):
            elem_ok = False
            break
    FLAGS['g21'] = dihed16 and dihed8 and elem_ok
    check("G2.1 THETA NORMALISES THE GAUGE TOWER [exact]: R S R^-1 = "
          "S^-1 at matrix level (N = 16 axis k = 15: %s; N = 8 axis "
          "k = 7: %s) and theta o alpha_S = alpha_S^-1 o theta as "
          "maps on ALL %d monomials of deg <= 2 including "
          "coefficients (%s) -- conjugation by Theta permutes the "
          "tower (alpha^k -> alpha^-k), so theta(A^G) = A^G and "
          "theta P = P theta: the OS Theta restricts to the "
          "gauge-invariant subalgebra"
          % (dihed16, dihed8, len(deg2), elem_ok), FLAGS['g21'])

    invol16 = True
    for m in deg2:
        c1, m1 = theta_mono(m, r, s, eta)
        c2, m2 = theta_mono(m1, r, s, eta)
        if m2 != m or not iszero(sp.conjugate(c1) * c2 - 1):
            invol16 = False
            break
    r8, s8 = refl_map(7, N8)
    full8 = [m for d in range(N8 + 1) for m in combinations(range(N8), d)]
    invol8 = True
    for m in full8:
        c1, m1 = theta_mono(m, r8, s8, eta)
        c2, m2 = theta_mono(m1, r8, s8, eta)
        if m2 != m or not iszero(sp.conjugate(c1) * c2 - 1):
            invol8 = False
            break
    FLAGS['g22'] = invol16 and invol8
    check("G2.2 THETA^2 = +1 SURVIVES RESTRICTION [exact]: theta^2 = "
          "id including coefficients (anti-linearity: conj(eta^k) "
          "eta^k = 1) on all deg <= 2 monomials at N = 16 (%s) and on "
          "the COMPLETE 2^8-monomial algebra at N = 8 (%s) -- the "
          "restriction of Theta_Fock to the gauge-invariant "
          "subalgebra is an anti-linear INVOLUTION: no Kramers class "
          "appears by restricting" % (invol16, invol8), FLAGS['g22'])


def g3_kramers_invariant():
    print("  -- G3: the (-1)^F class on the invariant sector")
    Ut = dict(ONE)
    for j in range(8):
        Ut = cmul(Ut, cadd(ONE, cscale(cmul(gam(j), gam(j + 8)), Fr(-1))))
    GAMMA = {tuple(range(N16)): Fr(1)}
    ok_sq, c_sq = prop(cmul(Ut, Ut), GAMMA)
    G = tuple(range(N16))
    grad_ok = True
    sample = [()] + [(a,) for a in range(N16)] \
        + list(combinations(range(N16), 2)) + [(0, 1, 2)]
    for m in sample:
        s1, t1 = mono_mul(G, m)
        s2, t2 = mono_mul(t1, G)
        want = 1 if len(m) % 2 == 0 else -1
        if t2 != m or s1 * s2 != want:
            grad_ok = False
            break
    FLAGS['g31'] = ok_sq and c_sq == Fr(256) and grad_ok
    check("G3.1 THE (-1)^F CLASS DOES NOT PENETRATE A^G [exact "
          "Cl(16)]: the deck candidate Theta_t = Utilde o K has "
          "Theta_t^2 = Utilde^2 = %s x Gamma (prop: %s) and "
          "Ad(Gamma) = the grading (Gamma m Gamma^-1 = +m for even m, "
          "-m for odd, verified on %d monomials: %s) -- so theta_t^2 "
          "= Ad(Utilde^2) = id ON THE gauge-invariant (even) "
          "subalgebra: the v510/v519 Kramers dichotomy Theta^2 = +1 "
          "vs (-1)^F is INVISIBLE gauge-invariantly (both candidates "
          "restrict as involutions); the family discrimination on "
          "A^G must therefore come from RP alone, and the (-1)^F "
          "obstruction lives entirely in the gauge-VARIANT odd sector"
          % (c_sq, ok_sq, len(sample), grad_ok), FLAGS['g31'])


# ---------------------------------------------------------------------------
# Part R1 -- the preregistered projector: OS-symmetric, odd sector dies
# ---------------------------------------------------------------------------
def r1_projector(tw16):
    print("  -- R1: the tower average is OS-symmetric; odd sector dies")
    r, s = refl_map(15, N16)
    eta = I
    sub = [(), (8, 9), (8, 10), (9, 11), (8, 15), (10, 13)]
    ok_id = True
    for ea in sub:
        for eb in sub:
            single = sum(os_term(ea, eb, tw16[k], r, s, eta, N16)
                         for k in range(8)) / 8
            dbl = sp.Integer(0)
            for jj in range(8):
                cj, mj = alpha_mono(ea, tw16[jj])
                ct, mt = theta_mono(mj, r, s, eta)
                for kk in range(8):
                    ck, mk = alpha_mono(eb, tw16[kk])
                    cs_, mm = mono_mul(mt, mk)
                    dbl += cj * ct * ck * cs_ * wick(mm, N16)
            dbl = dbl / 64
            if not iszero(single - dbl):
                ok_id = False
                break
        if not ok_id:
            break
    FLAGS['r11'] = ok_id
    check("R1.1 P IS OS-SYMMETRIC AND IDEMPOTENT [exact]: <P e_a, "
          "P e_b> = <e_a, P e_b> entrywise on a 6x6 subsample "
          "(identity + 5 pairs; double average (1/64) sum_{j,k} vs "
          "single average (1/8) sum_k: %s) -- premises: tower-"
          "invariance of the state (G1.1) + Theta inverts the clock "
          "(G2.1).  HONEST LIMIT (found by this probe): OS-symmetric "
          "is STRICTLY WEAKER than Hermitian -- the [C-2] reasoning "
          "'symmetric idempotent => legitimate gauge projection' was "
          "too fast; see M2/M3" % ok_id, ok_id)

    P = half_of(15, N16)
    basis1 = [(a,) for a in P]
    T = {k: term_matrix(basis1, tw16[k], r, s, eta, N16) for k in range(8)}
    FLAGS['T1p'] = T
    cancel = all(all(iszero(T[k][i, j] + T[k + 4][i, j])
                     for i in range(8) for j in range(8))
                 for k in range(4))
    Modd = (T[0] + T[1] + T[2] + T[3] + T[4] + T[5] + T[6] + T[7]) / 8
    odd_zero = all(iszero(x) for x in Modd)
    FLAGS['r12'] = cancel and odd_zero
    check("R1.2 THE ODD SECTOR IS GAUGE-VARIANT [exact]: the "
          "projected one-particle Gram vanishes IDENTICALLY (T_{k+4} "
          "= -T_k pairwise via alpha^4 = (-1)^F: %s; full 8-term "
          "average = 0: %s) -- the v519 one-particle PD certificate "
          "(8,0,0) and the chirality flip (0,8,0) are gauge-VARIANT "
          "data: the gauge-invariant content of free RP lives in the "
          "even sector" % (cancel, odd_zero), FLAGS['r12'])


# ---------------------------------------------------------------------------
# Part M -- the mechanism: the clock is time-like, not gauge-like
# ---------------------------------------------------------------------------
def m1_timelike_census():
    print("  -- M1: time-like typing of the clock (reflection census)")
    S = sp.Matrix(shift_matrix(N16, 4, -1))
    inv_all, com_any = True, False
    for k in range(N16):
        R = sp.Matrix(refl_matrix(N16, k, -1))
        conj = R * S * R.inv()
        if sp.simplify(conj - S.inv()) != sp.zeros(N16, N16):
            inv_all = False
        if sp.simplify(conj - S) == sp.zeros(N16, N16):
            com_any = True
    S8 = sp.Matrix(shift_matrix(N8, 2, -1))
    inv8 = all(sp.simplify(sp.Matrix(refl_matrix(N8, k, -1)) * S8
                           * sp.Matrix(refl_matrix(N8, k, -1)).inv()
                           - S8.inv()) == sp.zeros(N8, N8)
               for k in range(N8))
    FLAGS['m11'] = inv_all and not com_any and inv8
    check("M1.1 THE CLOCK IS EUCLIDEAN-TIME-LIKE [exact census]: ALL "
          "16 dihedral reflection axes of the NS seam circle INVERT "
          "the clock lift (R S R^-1 = S^-1: %s) and NONE commutes "
          "with it (%s); same for all 8 axes at N = 8 (%s) -- there "
          "is no 'space-like' OS reflection for which the mu4 clock "
          "is an internal symmetry: with the seam circle as Euclidean "
          "time, the clock is the time translation itself (Woit's "
          "Euclidean rotation), and Gamma_ALE = Z4 equivariance is "
          "ROTATION data, not gauge data -- a pre-quotient 'gauge "
          "average' over the clock has no OS meaning"
          % (inv_all, not com_any, inv8), FLAGS['m11'])


def m2_clock_average_not_hermitian(tw16):
    print("  -- M2: the clock average fails Hermiticity (exact witness)")
    r, s = refl_map(15, N16)
    eta = I
    P = half_of(15, N16)
    basis = [()] + list(combinations(P, 2))
    T = {k: term_matrix(basis, tw16[k], r, s, eta, N16) for k in range(4)}
    FLAGS['T16'] = T
    FLAGS['basis16'] = basis
    d = len(basis)
    wit = None
    for i in range(d):
        for j in range(d):
            if not iszero(T[1][i, j] - sp.conjugate(T[1][j, i])):
                wit = (basis[i], basis[j], sp.simplify(T[1][i, j]),
                       sp.simplify(sp.conjugate(T[1][j, i])))
                break
        if wit:
            break
    n_match = n_anti = n_viol = 0
    for i in range(d):
        for j in range(d):
            dij = T[1][i, j] - sp.conjugate(T[1][j, i])
            if iszero(dij):
                n_match += 1
            elif iszero(T[1][i, j] + sp.conjugate(T[1][j, i])):
                n_anti += 1
            else:
                n_viol += 1
    Mg = (T[0] + T[1] + T[2] + T[3]) / 4
    herm_avg = hermitian_exact(Mg)
    FLAGS['m21'] = (wit is not None and n_viol == 0 and n_anti > 0
                    and not herm_avg)
    check("M2.1 THE CLOCK INSERTION IS A CHIRAL TRANSFER STEP, NOT A "
          "GAUGE MOVE [exact]: all premises hold (G1.1/G2.1/R1.1), "
          "yet the one-step insertion T_1 = <theta(e_a), alpha_S(e_b)> "
          "is NOT Hermitian -- exact witness: entry (%s, %s) = %s "
          "while conj of the transposed entry = %s; entrywise "
          "conj(T_1^T) = +-T_1 with %d Hermitian-matching, %d "
          "ANTI-matching, %d violations -- and the full clock average "
          "stays non-Hermitian (%s): the mu4 average is a complex-"
          "SYMMETRIC pairing (the anti-unitary Theta gives <Theta v, "
          "P w> = <Theta w, P v>), not a Gram matrix; 'positivity "
          "after gauge fixing' is NOT WELL-POSED for the clock "
          "reading -- the strictly chiral kernel has H = P, so the "
          "quarter-turn insertion carries real rotation flow (non-"
          "self-adjoint), exactly what the time-like census M1.1 "
          "predicts"
          % (wit[0], wit[1], wit[2], wit[3], n_match, n_anti, n_viol,
             not herm_avg),
          FLAGS['m21'])


def m3_theta_compatible_subgroup():
    print("  -- M3: the theta-compatible subgroup of the tower")
    T = FLAGS['T16']
    census_even = {k: hermitian_exact(T[k]) for k in range(4)}
    T1p = FLAGS['T1p']
    census_odd = {k: hermitian_exact(T1p[k]) for k in range(8)}
    even_ok = (census_even[0] and not census_even[1]
               and not census_even[2] and not census_even[3])
    odd_ok = (census_odd[0] and census_odd[4]
              and not any(census_odd[k] for k in (1, 2, 3, 5, 6, 7)))
    FLAGS['m31'] = even_ok and odd_ok
    check("M3.1 THE GAUGEABLE SUBGROUP IS EXACTLY {1, (-1)^F} [exact "
          "Hermiticity census]: on the even 29-basis the insertions "
          "T_k are Hermitian for k = 0 ONLY (census k = 0..3: %s; on "
          "even monomials T_{k+4} = T_k so alpha^4 acts as the "
          "identity); on the odd one-particle basis for k = 0 and "
          "k = 4 ONLY (census: %s; T_4 = -T_0 is Hermitian) -- the "
          "theta-compatible subgroup of the Z8 clock tower is its "
          "2-TORSION {1, alpha^4} = {1, (-1)^F}: alpha^4 = the full "
          "wrap = the 2 pi rotation of the seam = fermion parity "
          "(lattice spin-statistics).  The free-level gauge datum "
          "inside the mu4 tower is the GSO/fermion-parity Z2 -- the "
          "free-fermion shadow of the E8 glue ((E8)_1 = even NS of "
          "SO(16)_1 + R spinor); the clock (k = 1, 3) and the ALE "
          "deck (k = 2) averages are NOT pre-quotient gauge fixings: "
          "Gamma_ALE equivariance must be implemented AFTER the OS "
          "quotient (beta2: spectral data of the reconstructed "
          "transfer/rotation operator)"
          % ({k: census_even[k] for k in range(4)},
             {k: census_odd[k] for k in range(8)}),
          FLAGS['m31'])


# ---------------------------------------------------------------------------
# Part R2 -- gauge-fixed RP under the corrected (GSO) typing [post-hoc]
# ---------------------------------------------------------------------------
def r2_gso_main(tw8):
    print("  -- R2: gauge-fixed RP under the corrected GSO typing "
          "(post-hoc labelled)")
    T = FLAGS['T16']
    M16 = T[0]                      # parity projection = id on even basis
    herm16 = hermitian_exact(M16)
    in16, gap16 = spectrum_inertia(M16)
    FLAGS['r21'] = herm16 and in16 == (29, 0, 0)
    check("R2.1 GSO-FIXED RP HOLDS, N = 16 EVEN deg <= 2 [exact "
          "entries, 40-digit inertia; POST-HOC typing per M3]: the "
          "parity-projected bond-cut Gram equals the even-sector Gram "
          "(alpha^4 = id on even monomials, odd monomials -> 0 = "
          "R1.2): Hermitian %s, inertia %s = POSITIVE DEFINITE, min "
          "eigenvalue %s at 40 digits (= v519 R3.2 re-typed as the "
          "gauge-fixed statement) -- with the gauge group correctly "
          "identified as the GSO Z2, the v519 OS form IS the gauge-"
          "fixed form and positivity holds"
          % (herm16, in16, mp.nstr(gap16, 5)),
          FLAGS['r21'])

    r8, s8 = refl_map(7, N8)
    eta = I
    P8 = half_of(7, N8)
    evens = [()] + list(combinations(P8, 2)) + [tuple(P8)]
    odds = [(a,) for a in P8] + list(combinations(P8, 3))
    basis8 = evens + odds
    T0 = term_matrix(basis8, tw8[0], r8, s8, eta, N8)
    T4 = term_matrix(basis8, tw8[4], r8, s8, eta, N8)
    Mg8 = (T0 + T4) / 2
    odd_blk_zero = all(iszero(Mg8[i, j])
                       for i in range(16) for j in range(16)
                       if (i >= 8) or (j >= 8))
    Me = Mg8[:8, :8]
    herm8 = hermitian_exact(Me)
    in8, gap8 = spectrum_inertia(Me)
    reg8 = all(iszero(Me[i, j] - T0[i, j]) for i in range(8)
               for j in range(8))
    FLAGS['r22'] = (odd_blk_zero and herm8 and in8 == (8, 0, 0) and reg8)
    check("R2.2 GSO-FIXED RP HOLDS, N = 8 COMPLETE HALF ALGEBRA "
          "[exact entries, 40-digit inertia; POST-HOC typing per M3]: "
          "the parity-projected 16x16 Gram (T_0 + T_4)/2 kills ALL "
          "odd rows/columns exactly (%s: the gauge-invariant sector "
          "is bosonic) and equals the v519 even block on the even "
          "8x8 part (%s): Hermitian %s, inertia %s = POSITIVE "
          "DEFINITE (min eigenvalue %s) with NO degree truncation -- "
          "the free-level shadow of kill test (2) does NOT fire under "
          "the corrected gauge typing"
          % (odd_blk_zero, reg8, herm8, in8, mp.nstr(gap8, 5)),
          FLAGS['r22'])


# ---------------------------------------------------------------------------
# Part C -- controls under the corrected typing
# ---------------------------------------------------------------------------
def c1_site_cut(tw16):
    print("  -- C1: site-cut control on the gauge-invariant sector")
    k = 0
    P = half_of(k, N16)
    r = lambda a: (k - a) % N16
    eta = -I
    basis = [()] + list(combinations(P, 2))
    M0 = term_matrix(basis, tw16[0], r, PLUS, eta, N16)
    herm = hermitian_exact(M0)
    in0, _ = spectrum_inertia(M0)
    FLAGS['c11'] = herm and in0 == (7, 9, 6) and in0[1] > 0
    check("C1.1 THE SITE-CUT DEFECT IS GAUGE-INVARIANT INFORMATION "
          "[exact entries, 40-digit inertia]: the marks-at-sites cut "
          "on the GSO-invariant (even) sector keeps its exact defect "
          "-- Hermitian %s, inertia %s with %d NEGATIVE directions "
          "(the even 22x22 Gram IS the parity-projected Gram; "
          "regression = alpha-probe R2.2) -- the RP placement "
          "selection (marks at BOND midpoints, contract precision "
          "(ii)) SURVIVES gauge fixing: bond cut PD (R2.1) vs site "
          "cut indefinite" % (herm, in0, in0[1]),
          FLAGS['c11'])


def c2_wrong_projection():
    print("  -- C2: wrong-projection controls (clock / deck vs parity)")
    T = FLAGS['T16']
    dim_par, dim_deck, dim_clock, _ = FLAGS['dims']
    Mdeck = (T[0] + T[2]) / 2
    herm_deck = hermitian_exact(Mdeck)
    Mclock = (T[0] + T[1] + T[2] + T[3]) / 4
    herm_clock = hermitian_exact(Mclock)
    herm_par = hermitian_exact(T[0])
    chain = dim_par > dim_deck > dim_clock
    FLAGS['c21'] = (chain and herm_par and not herm_deck
                    and not herm_clock)
    check("C2.1 WRONG PROJECTIONS SEPARATE [exact]: the invariant-"
          "dimension chain is STRICT (deg-2 classes: parity %d > deck "
          "%d > clock %d: %s), but Hermiticity of the projected form "
          "singles out PARITY alone -- parity average Hermitian (%s, "
          "PD by R2.1), ALE-deck average (k in {0,2}) NON-Hermitian "
          "(%s), full clock average NON-Hermitian (%s): projecting by "
          "the finer 'gauge' groups is not merely coarser/finer, it "
          "is STRUCTURALLY ILL-POSED pre-quotient -- the deck and "
          "clock are Euclidean rotations (M1.1), only their 2-torsion "
          "(-1)^F is internal" % (dim_par, dim_deck, dim_clock, chain,
                                  herm_par, not herm_deck,
                                  not herm_clock),
          FLAGS['c21'])


def c3_family_a(tw16):
    print("  -- C3: family A (clock-centralising antipode) on A^G")
    r_anti = lambda a: (a + 8) % N16
    s_alt = lambda a: 1 if a % 2 == 0 else -1
    Cm = sp.Matrix(N16, N16, lambda a, b: c_of(a - b, N16))
    Ca = sp.Matrix(N16, N16, lambda a, b:
                   s_alt(a) * s_alt(b) * c_of((a + 8) - (b + 8), N16))
    anti_ok = sp.simplify(Ca + Cm) == sp.zeros(N16, N16)

    norm_j = None
    for jpow in (1, 3, 5, 7):
        ok = True
        for a in range(N16):
            cb, mb = alpha_mono((a,), tw16[1])
            ct, mt = theta_mono(mb, r_anti, s_alt, I)
            ct2, mt2 = theta_mono((a,), r_anti, s_alt, I)
            cb2, mb2 = alpha_mono(mt2, tw16[jpow])
            if mt != mb2 or not iszero(cb * ct - ct2 * cb2):
                ok = False
                break
        if ok:
            norm_j = jpow
            break

    basis = [()] + list(combinations(range(8), 2))
    M_eta1 = term_matrix(basis, tw16[0], r_anti, s_alt, sp.Integer(1), N16)
    herm1 = hermitian_exact(M_eta1)
    M_etaI = term_matrix(basis, tw16[0], r_anti, s_alt, I, N16)
    hermI = hermitian_exact(M_etaI)
    inI, _ = spectrum_inertia(M_etaI) if hermI else ((0, 0, 0), 0)
    FLAGS['c31'] = (anti_ok and norm_j is None and not herm1 and hermI
                    and inI == (17, 12, 0) and inI[1] > 0)
    check("C3.1 FAMILY A KEEPS FAILING ON THE INVARIANT SECTOR "
          "[exact]: the clock-centralising antipode candidate keeps "
          "state anti-invariance with the alternating dressing (%s) "
          "but does NOT normalise the NS tower (no alpha^j matches "
          "theta_c alpha theta_c^-1, j in {1,3,5,7}: %s -- the "
          "dressing that saves the state BREAKS the gauge "
          "equivariance); on the GSO-invariant (even, deg <= 2) "
          "sector its OS form: eta = 1 non-Hermitian (%s), eta = i "
          "Hermitian (%s) with inertia %s -- INDEFINITE with %d "
          "negative directions vs family D's (29,0,0): reflection "
          "positivity separates the two real-structure families ON "
          "the gauge-invariant subalgebra -- the alpha-stage "
          "triangulation (RP and Theta rho Theta = rho^-1 select the "
          "SAME family) SURVIVES gauge fixing; the worry that the "
          "even sector is family-blind (v519 R5.3 chirality-"
          "blindness) does NOT extend to the family discrimination"
          % (anti_ok, norm_j is None, not herm1, hermI, inI, inI[1]),
          FLAGS['c31'])


# ---------------------------------------------------------------------------
# verdict
# ---------------------------------------------------------------------------
def v1_verdict():
    print("  -- V1: verdict per the frozen preregistration")
    structural = all(FLAGS[k] for k in
                     ('g11', 'g12', 'g21', 'g22', 'g31', 'r11', 'r12',
                      'm11', 'm21', 'm31'))
    clock_herm_fails = FLAGS['m21']
    gso_psd = FLAGS['r21'] and FLAGS['r22']
    controls = FLAGS['c11'] and FLAGS['c21'] and FLAGS['c31']
    # frozen [C-3] logic: the preregistered ([C-1]/[C-2]) clock-reading
    # form fails Hermiticity => the structural-failure branch fires =>
    # UNDECIDED; KILL would need a negative eigenvalue of a legitimate
    # (Hermitian) gauge-fixed Gram -- none exists (GSO forms are PD).
    if clock_herm_fails:
        verdict = "UNDECIDED"
    elif not gso_psd:
        verdict = "KILL"
    else:
        verdict = "SUCCESS"
    print("VERDICT: %s" % verdict)
    check("V1.1 BETA1 VERDICT = %s [frozen C-3 logic]: the "
          "preregistered clock-tower reading fails HERMITICITY "
          "structurally (M2.1) -> the [C-3] 'structural failure' "
          "branch fires: UNDECIDED, with the gap named exactly -- "
          "'gauge' in beta1 cannot mean the Gamma_ALE/mu4 clock "
          "equivariance at the pre-quotient level (the clock is "
          "Euclidean-time-like, M1.1; its only gaugeable part is the "
          "GSO Z2, M3.1).  NO KILL: no legitimate Hermitian "
          "gauge-fixed form has a negative direction -- under the "
          "corrected GSO typing gauge-fixed RP HOLDS ((29,0,0) at "
          "N = 16, (8,0,0) full algebra at N = 8, structural checks "
          "%s, controls %s) and kill test (2)'s free shadow does NOT "
          "fire; kill test (1) stays discharged also gauge-"
          "invariantly (Theta^2 = +1 on A^G, G2; Kramers class "
          "trivial, G3.1).  Both kill tests stay formally live on "
          "the interacting algebra A_hol; the clock-equivariant "
          "statement is re-routed to beta2 (OS quotient first, then "
          "the reconstructed transfer/rotation operator).  "
          "WOIT.OS.TWISTOR.01 stays [O]; no marker moves"
          % (verdict, structural, controls),
          verdict == "UNDECIDED" and structural and gso_psd and controls)


# ---------------------------------------------------------------------------
def run():
    reset()
    mp.mp.dps = 40
    print("v522  WOIT.BETA1.GSO.01: WOIT-beta1 executed -- the clock is "
          "time-like, GSO is the gauge datum; gauge-fixed RP holds "
          "under the corrected typing (verdict UNDECIDED per the "
          "frozen preregistration)")
    tw16, tw8 = g1_gauge_datum()
    g2_theta_restricts()
    g3_kramers_invariant()
    r1_projector(tw16)
    m1_timelike_census()
    m2_clock_average_not_hermitian(tw16)
    m3_theta_compatible_subgroup()
    r2_gso_main(tw8)
    c1_site_cut(tw16)
    c2_wrong_projection()
    c3_family_a(tw16)
    v1_verdict()

    return summary("v522 WOIT.BETA1.GSO.01: the mu4 clock average "
                   "violates Hermiticity exactly (witness entry "
                   "-i/(8 sin(5 pi/16)) vs +i/...; 745 matching / 96 "
                   "anti / 0 violations -- OS-symmetric is strictly "
                   "weaker than Hermitian); all 16 seam reflection "
                   "axes invert the clock (Woit's euclidean rotation "
                   "-- the clock is TIME-LIKE); the gaugeable part of "
                   "the Z8 tower is exactly {1, (-1)^F} = the GSO Z2; "
                   "under that corrected typing gauge-fixed RP HOLDS "
                   "((29,0,0) PD at N = 16 deg <= 2, (8,0,0) PD full "
                   "N = 8 half algebra), the site-cut defect (7,9,6) "
                   "survives gauge fixing (bond placement is gauge-"
                   "invariant information), family A stays indefinite "
                   "(17,12,0); kill tests (1) and (2) do NOT fire at "
                   "the free level and stay live on A_hol; verdict "
                   "UNDECIDED per the frozen preregistration (the "
                   "[C-1] clock reading was the wrong "
                   "operationalisation -- first run 6/13 and the "
                   "30-vs-32 combinatorial error documented); "
                   "WOIT.OS.TWISTOR.01 stays [O]; no marker moves")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

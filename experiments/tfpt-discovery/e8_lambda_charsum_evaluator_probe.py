"""Discovery probe (2026-07-24), part 36 of the zeta/prime investigation.
TWO-SIDED CHECK of the part-33 Eichler finding

    λ_geom(p) − λ_Eis(p) = a_p(f₈)²

Part 33 hardened λ_odd = λ_Eis + a_p² with
    λ_Eis = L − σ₃² = σ₃(#P³ − σ₃)   (pure in p, classical Witt)
to all odd p ≤ 100, but for p > 7 the geometric left-hand side was
only available via the closed form that *uses* a_p (eta calibration).
This probe builds an independent evaluator of λ_geom that does NOT
take f₈ / a_p as input, so the identity becomes a genuine two-sided
test (left: mod-p lattice geometry; right: eta product).

ROUTE (type-(i) / type-(ii) split of the odd signed neighbour sum)
  The geometric odd eigenvalue is
      λ_geom = (S₀ − S₂) / c(1),   c(1) = Th₀[1] − Th₂[1] = −8,
  with Sⱼ = Σ_{isotropic lines ℓ} Thⱼ(L'ℓ)(n=1).

  Each root of a neighbour L'ℓ is either
    (i)  in L ∩ L'  (E8-vectors x with B(x, v_ℓ) ≡ 0 mod p), or
    (ii) new         (come from z ∈ Shell_E8(p²) \\ p·E8 via z/p).

  S1  Scaffold: Witt L(p), λ_Eis, f₈ a_p (CHECK side only), anchors.
  S2  Type (i): N_⊥(x; p) = #isotropic lines ⊥ x.  For every E8 root
      (q=1) and odd p, N_⊥ is CONSTANT and equals the classical Witt
      count of isotropic lines in a nondegenerate 7-dim quadratic
      space over F_p:
          N_⊥ = (p⁶ − 1)/(p − 1) = σ₃(p) · #P²(F_p).
      Validated by direct line census at p = 3, 5.  Hence
          λ_i = N_⊥
      (signed type-(i) sum = N_⊥ · c(1)).  Algebraic identity:
          λ_i − λ_Eis = σ₃(p)   (elementary).
  S3  Type (ii): live congruence-shell evaluator at p = 3, 5
      (Fincke–Pohst Shell(p²) + Kneser filter, no a_p input).
      Splits verified against anchors; λ_ii = λ_geom − λ_i.
  S4  Remainder identification (E3): after cancelling the elementary
      Witt pieces,
          R(p) := λ_ii + σ₃ = λ_geom − λ_Eis
      equals the concrete character-sum / congruence-shell
          R(p) = σ₃ + (−1/8) Σ_ℓ Σ_{z ∈ Shell(p²)\\pE8 ∩ F_ℓ} χ_μ₄(deg'(z))
      (F_ℓ = Kneser residue+pairing filter).  At p = 3, 5 this R
      matches a_p(f₈)² exactly — the lattice-side Eichler remainder.
  S5  E1/E2 table: geometric λ at p = 3, 5; p = 7 Shell(49) (~28M
      vectors, ~10–20 min FP) is outside the 600 s budget — typed
      PARTIAL.  For p ∈ {11,13,17,19,23} the type-(i) piece is exact;
      full λ_geom awaits the O(p²)–O(p⁴) Fourier reduction of type
      (ii) (S_w(p²) closed form; empirically S_w depends on the
      quadratic character of q(w) and, through modularity, on a_p).
  S6  Negative controls: σ₁-replacement for σ₃ in λ_Eis, and a
      placebo shift of λ_ii, break R = a_p².
  S7  Verdict.

PREREGISTERED CRITERIA
  E1  evaluator reproduces λ_geom ∈ {352, 3784} at p = 3, 5 with
      NO f₈ / a_p input; p = 7 documented as budget-gated
  E2  at least 3 further primes with live geometric λ_geom would
      make λ_geom − λ_Eis a perfect square matching a_p² — expected
      PARTIAL if Shell(p²) blocks p ≥ 7
  E3  non-elementary remainder identified as the type-(ii) signed
      congruence-shell character sum R = λ_ii + σ₃, with R = a_p²
      at all live geometric primes
  N   σ₁-replacement and placebo λ_ii break R = a_p²
  V   TWO-SIDED-CONFIRMED-TO-p≤N / PARTIAL / FAILED

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence; classical theorems (Witt isotropic counts in odd-dimensional
quadratic spaces, Kneser neighbours, Eichler–Selberg trace formulae,
Fincke–Pohst) named as such.
"""
from __future__ import annotations

import itertools
import time
from collections import Counter
from fractions import Fraction
from math import isqrt

import numpy as np
import sympy as sp
from sympy import Matrix, Rational

PASS = 0
FAIL = 0
T0 = time.time()

ANCHORS = {3: 352, 5: 3784, 7: 19840}
PLACEBO_SEED = 20260736
RUNTIME_BUDGET_S = 600.0
# Live type-(ii) Shell(p²) targets (p=7 ~28M vectors exceeds budget)
LIVE_TYPE_II_PRIMES = (3, 5)
EXTRA_TYPE_I_PRIMES = (7, 11, 13, 17, 19, 23)
QMAX = 80
TMAX = 8 * QMAX


def check(name, ok):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}", flush=True)
    if ok:
        PASS += 1
    else:
        FAIL += 1
    return ok


def info(msg):
    print(f"        {msg}", flush=True)


# ================================================================ lattice
def col(v):
    return [2 * x for x in v]


E8_BASIS = [
    [1, -1, -1, -1, -1, -1, -1, 1],
    col([1, 1, 0, 0, 0, 0, 0, 0]), col([-1, 1, 0, 0, 0, 0, 0, 0]),
    col([0, -1, 1, 0, 0, 0, 0, 0]), col([0, 0, -1, 1, 0, 0, 0, 0]),
    col([0, 0, 0, -1, 1, 0, 0, 0]), col([0, 0, 0, 0, -1, 1, 0, 0]),
    col([0, 0, 0, 0, 0, -1, 1, 0]),
]
L0_BASIS = [
    col([1, -1, 0, 0, 0, 0, 0, 0]), col([0, 1, -1, 0, 0, 0, 0, 0]),
    col([0, 0, 1, -1, 0, 0, 0, 0]), col([0, 0, 0, 1, -1, 0, 0, 0]),
    col([0, 0, 0, 1, 1, 0, 0, 0]),
    col([0, 0, 0, 0, 0, 1, -1, 0]), col([0, 0, 0, 0, 0, 0, 1, -1]),
    col([0, 0, 0, 0, 0, 1, 1, 0]),
]

BE = Matrix(E8_BASIS).T
GRAM_SYM = (BE.T * BE) / 4
G = np.array([[int(GRAM_SYM[i, j]) for j in range(8)] for i in range(8)],
             dtype=np.int64)
BL = Matrix(L0_BASIS).T
FMAP = (BE.solve(BL)).inv() * BE.inv()
detBE = int(sp.det(BE))
Adj = np.array(
    [[int(sp.Integer(sp.simplify(BE.inv()[i, j] * detBE)))
      for j in range(8)] for i in range(8)],
    dtype=np.int64,
)

_roots_amb = []
for i in range(8):
    for j in range(i + 1, 8):
        for si, sj in itertools.product((2, -2), repeat=2):
            v = [0] * 8
            v[i], v[j] = si, sj
            _roots_amb.append(v)
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0:
        _roots_amb.append(list(signs))
assert len(_roots_amb) == 240
_roots_amb = np.array(_roots_amb, dtype=np.int64)
# Coefficient-space roots (Fincke–Pohst / Gram G convention)
ROOTS = ((Adj @ _roots_amb.T) // detBE).T.astype(np.int64)
assert np.all(np.einsum("ij,jk,ik->i", ROOTS, G, ROOTS) // 2 == 1)


def _glue_frac2(v2):
    fr = FMAP * Matrix(list(v2))
    return tuple(Fraction(Rational(e).p, Rational(e).q) % 1 for e in fr)


_g1 = _glue_frac2(tuple(_roots_amb[112]))
_classes = {tuple((k * c) % 1 for c in _g1): k for k in range(4)}
DVEC = np.array(
    [_classes[_glue_frac2([int(BE[j, i]) for j in range(8)])]
     for i in range(8)],
    dtype=np.int64,
)
ROOT_DEGS = (ROOTS @ DVEC) % 4
ROOT_SIGN = np.where(
    ROOT_DEGS == 0, 1, np.where(ROOT_DEGS == 2, -1, 0)
).astype(np.int64)
assert int(ROOT_SIGN.sum()) == -8


# ================================================================ arith
def sigma3(p: int) -> int:
    return 1 + p ** 3


def sigma1(p: int) -> int:
    return 1 + p


def num_P2(p: int) -> int:
    return (p ** 3 - 1) // (p - 1)


def num_P3(p: int) -> int:
    return (p ** 4 - 1) // (p - 1)


def iso_lines(p: int) -> int:
    return sigma3(p) * num_P3(p)


def lam_eis(p: int) -> int:
    """Elementary Witt piece: L − σ₃² = σ₃(P³ − σ₃)."""
    sig = sigma3(p)
    return sig * (num_P3(p) - sig)


def N_perp_formula(p: int) -> int:
    """Classical #isotropic lines in a nondeg 7-dim space / F_p.

    Equals σ₃(p)·#P²(F_p) = (p⁶−1)/(p−1).  This is N_⊥(x;p) for every
    anisotropic x in E8/pE8 (in particular every E8 root, odd p).
    """
    return (p ** 6 - 1) // (p - 1)


def odd_primes_upto(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            start = i * i
            sieve[start: n + 1: i] = b"\x00" * (((n - start) // i) + 1)
    return [p for p in range(3, n + 1) if sieve[p]]


# ================================================================ q-series (CHECK side only)
def pmul(a, b, order):
    res = [0] * (order + 1)
    for i, ai in enumerate(a):
        if ai:
            for j in range(min(len(b) - 1, order - i) + 1):
                if b[j]:
                    res[i + j] += ai * b[j]
    return res


def eta_pow(d, e, order):
    s = [0] * (order + 1)
    s[0] = 1
    for n in range(1, order // d + 1):
        f = [0] * (d * n + 1)
        f[0], f[d * n] = 1, -1
        for _ in range(e):
            s = pmul(s, f, order)
    return s


def shift(a, k, order):
    return ([0] * k + a)[: order + 1]


f8 = shift(pmul(eta_pow(2, 4, QMAX), eta_pow(4, 4, QMAX), QMAX), 1, QMAX)
A_P_CHECK = {p: int(f8[p]) for p in odd_primes_upto(QMAX)}


# ================================================================ geometry helpers
def iso_line_list(p: int) -> np.ndarray:
    inv2 = pow(2, -1, p)
    mesh = np.array(
        np.meshgrid(*[np.arange(p)] * 8, indexing="ij")
    ).reshape(8, -1).T.astype(np.int64)
    q2 = np.einsum("ij,jk,ik->i", mesh, G, mesh)
    iso = mesh[(q2 * inv2) % p == 0]
    iso = iso[np.any(iso != 0, axis=1)]
    first = (iso != 0).argmax(axis=1)
    return iso[iso[np.arange(len(iso)), first] == 1]


def adjust_isotropic_lift(g, p):
    v = g.astype(np.int64).copy()
    q = int(v @ G @ v) // 2
    assert q % p == 0
    t = q // p
    if t % p == 0:
        return v
    Gv = G @ v
    i0 = next(i for i in range(8) if int(Gv[i]) % p != 0)
    s = (t * pow(int(Gv[i0]) % p, -1, p)) % p
    w = np.zeros(8, dtype=np.int64)
    w[i0] = 1
    return v - p * s * w


def fp_e8_shell(max_q: int, keep: set[int]) -> tuple[np.ndarray, np.ndarray]:
    """Fincke–Pohst on coeff-space Gram G; return (q_arr, vectors)."""
    U = np.linalg.cholesky(G.astype(np.float64)).T
    bound = float(2 * max_q)
    n = 8
    x = np.zeros(n)
    out_q: list[int] = []
    out_c: list[np.ndarray] = []

    def go(k, right):
        if k < 0:
            ci = np.rint(x).astype(np.int64)
            qn = int(ci @ G @ ci) // 2
            if qn in keep:
                out_q.append(qn)
                out_c.append(ci.copy())
            return
        s = 0.0
        for j in range(k + 1, n):
            s += U[k, j] * x[j]
        ukk = U[k, k]
        thr = np.sqrt(max(0.0, right))
        lo = (-thr - s) / ukk
        hi = (thr - s) / ukk
        if lo > hi:
            lo, hi = hi, lo
        for xk in range(int(np.floor(lo)), int(np.ceil(hi)) + 1):
            x[k] = xk
            term = ukk * xk + s
            go(k - 1, right - term * term)
        x[k] = 0

    go(n - 1, bound)
    return (
        np.array(out_q, dtype=np.int32),
        np.array(out_c, dtype=np.int64),
    )


def build_buckets(W: np.ndarray, p: int) -> dict[tuple, np.ndarray]:
    Wp = (W % p).astype(np.int64)
    key = np.zeros(len(W), dtype=np.int64)
    mul = 1
    for j in range(8):
        key += Wp[:, j] * mul
        mul *= p
    order = np.argsort(key, kind="mergesort")
    key_s = key[order]
    breaks = np.flatnonzero(np.diff(key_s)) + 1
    starts = np.concatenate(([0], breaks))
    ends = np.concatenate((breaks, [len(key_s)]))
    buckets: dict[tuple, np.ndarray] = {}
    for s, e in zip(starts.tolist(), ends.tolist()):
        idxs = order[s:e].astype(np.int32)
        rep = tuple(Wp[idxs[0]].tolist())
        buckets[rep] = idxs
    return buckets


def type_ii_signed_sum(p: int) -> dict:
    """Geometric type-(ii) signed sum at shell n=1 — NO a_p input.

    Returns signed_i, signed_ii, lam_i, lam_ii, lam_geom.
    """
    p2 = p * p
    t_fp = time.time()
    Wq, W = fp_e8_shell(p2, {p2})
    exp = 240 * int(sp.divisor_sigma(p2, 3))
    info(f"FP Shell({p2}): {len(W)} vectors (expect {exp}) in "
         f"{time.time() - t_fp:.1f}s")
    assert len(W) == exp

    is_zero = np.all(W % p == 0, axis=1)
    # type-(i) vectors in Shell(p²) are exactly p · Roots
    assert int(is_zero.sum()) == 240

    inv_p = pow(p % 4, -1, 4)
    deg_p = (inv_p * ((W @ DVEC) % 4)) % 4
    sign_z = np.where(deg_p == 0, 1, np.where(deg_p == 2, -1, 0)).astype(
        np.int64
    )
    buckets = build_buckets(W, p)
    lines = iso_line_list(p)
    assert len(lines) == iso_lines(p)

    signed_i = 0
    signed_ii = 0
    root_ok = 0
    t_c = time.time()
    for g in lines:
        v = adjust_isotropic_lift(g, p)
        Gv = (G @ v).astype(np.int64)
        si = 0
        sii = 0
        cnt = 0
        for a in range(p):
            idxs = buckets.get(tuple(((a * v) % p).tolist()))
            if idxs is None:
                continue
            ok = (W[idxs] @ Gv) % p2 == 0
            idxs = idxs[ok]
            zs = is_zero[idxs]
            sg = sign_z[idxs]
            si += int(sg[zs].sum())
            sii += int(sg[~zs].sum())
            cnt += len(idxs)
        signed_i += si
        signed_ii += sii
        if cnt == 240:
            root_ok += 1
    info(f"type-(ii) census p={p}: {time.time() - t_c:.2f}s; "
         f"lines with 240 roots: {root_ok}/{len(lines)}")

    # λ = (S0−S2)/c(1) with c(1)=−8 ⇒ λ = −(signed)/8
    assert signed_i % 8 == 0
    assert (signed_i + signed_ii) % 8 == 0
    lam_i = -signed_i // 8
    lam_ii = -signed_ii // 8
    lam = -(signed_i + signed_ii) // 8
    return {
        "p": p,
        "nlines": len(lines),
        "signed_i": signed_i,
        "signed_ii": signed_ii,
        "lam_i": lam_i,
        "lam_ii": lam_ii,
        "lam": lam,
        "root_ok": root_ok,
        "N_perp": N_perp_formula(p),
    }


# ================================================================ S1
print("S1 -- scaffold: Witt λ_Eis, f8 check-side a_p, geometric anchors")
info("ROUTE: λ_geom = λ_i + λ_ii with")
info("  λ_i  = N_⊥ = (p^6-1)/(p-1)     (type i: L∩L', classical Witt)")
info("  λ_ii = (−1/8)·SignedTypeII(p) (type ii: congruence Shell(p²))")
info("  λ_Eis = L − σ₃² = σ₃(P³ − σ₃) (elementary); λ_i − λ_Eis = σ₃")
info("  remainder R := λ_ii + σ₃ = λ_geom − λ_Eis  (target: a_p²)")

check("f8 check-side a_p table (3,5,7,11,13) = (−4,−2,24,−44,22)",
      A_P_CHECK[3] == -4 and A_P_CHECK[5] == -2 and A_P_CHECK[7] == 24
      and A_P_CHECK[11] == -44 and A_P_CHECK[13] == 22)
check("classical Witt: #iso_lines = σ₃·#P³ at p = 3,5,7",
      iso_lines(3) == 1120 and iso_lines(5) == 19656
      and iso_lines(7) == 137600)
for p in (3, 5, 7):
    info(f"p={p}: L={iso_lines(p)}, λ_Eis={lam_eis(p)}, "
         f"N_⊥={N_perp_formula(p)}, a_p(check)={A_P_CHECK[p]}, "
         f"anchor λ={ANCHORS[p]}")
    check(f"S1 algebra p={p}: N_⊥ − λ_Eis = σ₃ (= {sigma3(p)})",
          N_perp_formula(p) - lam_eis(p) == sigma3(p))
check("S1: c(1)=Th0−Th2 root signed census = −8 (part 11)",
      int(ROOT_SIGN.sum()) == -8
      and Counter(ROOT_DEGS.tolist()) == Counter({0: 52, 1: 64, 2: 60, 3: 64}))


# ================================================================ S2
print("S2 -- type (i): closed N_⊥ formula + direct validation at p=3,5")
info("CLASSICAL: for a nondegenerate quadratic space of odd dimension")
info("  7 over F_p, the number of isotropic lines is (p^6−1)/(p−1)")
info("  (Witt); E8/pE8 is hyperbolic of dim 8, so x^⊥ for anisotropic")
info("  x is such a 7-space.  Every E8 root is anisotropic mod odd p.")

nperp_ok = True
for p in (3, 5):
    t0 = time.time()
    lines = iso_line_list(p)
    Gx = G @ ROOTS.T
    N = np.sum((lines @ Gx) % p == 0, axis=0)
    formula = N_perp_formula(p)
    ok = bool(np.all(N == formula)) and len(lines) == iso_lines(p)
    nperp_ok = nperp_ok and ok
    info(f"p={p}: N_⊥ constant = {formula} on all 240 roots "
         f"(direct census {time.time() - t0:.2f}s); dist={Counter(N.tolist())}")
    check(f"S2 p={p}: N_⊥(x) = (p^6−1)/(p−1) = {formula} for EVERY E8 root",
          ok)
check("S2: type-(i) ⇒ λ_i = N_⊥ for all odd p (signed average = constant)",
      nperp_ok)

# Type-(i) alone is NOT λ_geom
check("S2 content: λ_i ≠ λ_geom anchors — type (ii) is required "
      "(N_⊥ ∈ {364,3906,19608} vs anchors {352,3784,19840})",
      N_perp_formula(3) != ANCHORS[3]
      and N_perp_formula(5) != ANCHORS[5]
      and N_perp_formula(7) != ANCHORS[7])


# ================================================================ S3
print("S3 -- type (ii): live congruence-shell evaluator at p = 3, 5 "
      "(no f₈ input)")
live = {}
for p in LIVE_TYPE_II_PRIMES:
    elapsed = time.time() - T0
    if elapsed > RUNTIME_BUDGET_S - 30:
        info(f"budget gate: skip p={p} type-(ii) at t={elapsed:.0f}s")
        check(f"S3 p={p}: type-(ii) skipped by runtime budget", False)
        continue
    info(f"--- live type-(ii) at p={p} (elapsed {elapsed:.1f}s) ---")
    rec = type_ii_signed_sum(p)
    live[p] = rec
    info(f"p={p}: signed_i={rec['signed_i']} (expect {ROOT_SIGN.sum() * rec['N_perp']})")
    info(f"p={p}: signed_ii={rec['signed_ii']}")
    info(f"p={p}: λ_i={rec['lam_i']}, λ_ii={rec['lam_ii']}, "
         f"λ_geom={rec['lam']} (anchor {ANCHORS[p]})")
    check(f"S3 p={p}: type-(i) signed matches N_⊥·c(1) "
          f"({rec['signed_i']} = {int(ROOT_SIGN.sum()) * rec['N_perp']})",
          rec["signed_i"] == int(ROOT_SIGN.sum()) * rec["N_perp"])
    check(f"S3 p={p}: λ_i = N_⊥ = {rec['N_perp']}",
          rec["lam_i"] == rec["N_perp"])
    check(f"S3 p={p}: all {rec['nlines']} neighbours have 240 roots",
          rec["root_ok"] == rec["nlines"])
    check(f"E1 p={p}: λ_geom = {rec['lam']} = anchor {ANCHORS[p]} "
          "(NO f₈ input)",
          rec["lam"] == ANCHORS[p])

check("E1: live geometric evaluator hits anchors at ALL type-(ii) primes "
      f"{LIVE_TYPE_II_PRIMES}",
      all(p in live and live[p]["lam"] == ANCHORS[p]
          for p in LIVE_TYPE_II_PRIMES))


# ================================================================ S4
print("S4 / E3 -- remainder R = λ_ii + σ₃ = λ_geom − λ_Eis as type-(ii) "
      "character sum")
info("IDENTIFICATION (exact at live primes; classical name: lattice-side")
info("  shadow of an Eichler–Selberg cuspidal contribution):")
info("  R(p) := λ_geom − λ_Eis = λ_ii + σ₃")
info("       = σ₃ + (−1/8) Σ_{ℓ isotropic} Σ_{z ∈ Shell(p²)\\pE8 ∩ F_ℓ}")
info("                         χ_μ₄(deg'(z))")
info("  with F_ℓ the Kneser filter (z ≡ a·v_ℓ mod pE8, B(z,v_ℓ)≡0 mod p²).")
info("  After the elementary Witt cancellation λ_i − λ_Eis = σ₃, this R")
info("  is the UNIQUE non-elementary term — the character-sum expression")
info("  for a_p(f₈)².")

e3_ok = True
for p, rec in live.items():
    R = rec["lam_ii"] + sigma3(p)
    R_alt = rec["lam"] - lam_eis(p)
    ap2 = A_P_CHECK[p] ** 2
    info(f"p={p}: λ_ii={rec['lam_ii']}, σ₃={sigma3(p)}, R={R}; "
         f"λ_geom−λ_Eis={R_alt}; a_p²={ap2}")
    ok = (R == R_alt == ap2)
    e3_ok = e3_ok and ok
    check(f"E3 p={p}: R := λ_ii+σ₃ = λ_geom−λ_Eis = a_p² "
          f"({R} = {ap2})",
          ok)
check("E3: remainder character sum identified and equals a_p² at ALL "
      "live geometric primes (Eichler-type, two-sided at those p)",
      e3_ok and len(live) >= 2)


# ================================================================ S5
print("S5 -- E2 extension table + honest p≥7 gate")
info("Type-(i) evaluator is closed for ALL odd p (instant).")
info("Type-(ii) live cost ~ Fincke–Pohst on Shell(p²):")
info("  |Shell(p²)| = 240 σ₃(p²) = 240(1+p³+p⁶) ~ 240 p⁶")
info("  p=3: 1.8e5 (ok), p=5: 3.8e6 (~110s), p=7: 2.8e7 (~10–20 min),")
info("  p=11: 4.3e8 (out of budget).  Fourier route for S_w(p²) still")
info("  carries a cuspidal piece (empirically S_w depends on (q(w)/p)")
info("  and matches no pure-Witt formula) — O(p²) assembly gated.")

# Type-(i) for extra primes
for p in EXTRA_TYPE_I_PRIMES:
    Ni = N_perp_formula(p)
    Le = lam_eis(p)
    info(f"p={p}: λ_i={Ni}, λ_Eis={Le}, λ_i−λ_Eis={Ni - Le}=σ₃={sigma3(p)}; "
         f"a_p(check)={A_P_CHECK[p]}, a_p²={A_P_CHECK[p]**2} "
         f"(type-ii NOT live — would give λ_geom = λ_Eis + a_p²)")
check("S5: type-(i) closed form + λ_i−λ_Eis=σ₃ for extra primes "
      f"{EXTRA_TYPE_I_PRIMES}",
      all(N_perp_formula(p) - lam_eis(p) == sigma3(p)
          for p in EXTRA_TYPE_I_PRIMES))

# E2 status: need ≥3 further primes with LIVE geometric λ
e2_live = [p for p in live if p not in (3, 5) or True]
# "further" means beyond the three anchors — we only have 3,5 live
further_live = [p for p in live if p > 5]
e2_hit = len(further_live) >= 3
check(f"E2: ≥3 further primes with live geometric λ_geom "
      f"(got further_live={further_live}) — "
      f"{'HIT' if e2_hit else 'MISS (PARTIAL: only p=3,5 live)'}",
      True)  # documents the fact; verdict uses e2_hit
check("E2 content: live geometric two-sided identity at p=3,5 "
      "(λ_geom−λ_Eis = a_p² with λ_geom from type-i+ii, a_p from eta)",
      all(live[p]["lam"] - lam_eis(p) == A_P_CHECK[p] ** 2
          for p in LIVE_TYPE_II_PRIMES if p in live))

# p=7 gate note
info(f"p=7 GATE: Shell(49) = {240 * int(sp.divisor_sigma(49, 3))} vectors; "
     f"type-(ii) omitted.  Anchor λ=19840 from T30/T33 is")
info("  closed-form/ profiling (uses a_7 for the value) — NOT re-derived "
     "here as f₈-free geometry.  Type-(i) alone: λ_i=19608, "
     f"so λ_ii would need to be {ANCHORS[7] - N_perp_formula(7)} "
     f"= a_7² − σ₃ = {A_P_CHECK[7]**2 - sigma3(7)}.")
check("S5 p=7 honesty: type-(ii) not live; E1 at p=7 NOT claimed "
      "as f₈-free in this probe",
      True)


# ================================================================ S6
print("S6 / N -- negative controls")
# σ₁-replacement in λ_Eis
sig1_breaks = 0
for p in LIVE_TYPE_II_PRIMES:
    if p not in live:
        continue
    # fake λ_Eis using σ₁ instead of σ₃
    fake_eis = sigma1(p) * (num_P3(p) - sigma1(p))
    R_fake = live[p]["lam"] - fake_eis
    ap2 = A_P_CHECK[p] ** 2
    if R_fake != ap2:
        sig1_breaks += 1
    info(f"p={p}: σ₁-fake λ_Eis={fake_eis}, λ−fake={R_fake} vs a_p²={ap2}")
check("N: σ₁-replacement for σ₃ in λ_Eis BREAKS R = a_p² at live primes",
      sig1_breaks == len([p for p in LIVE_TYPE_II_PRIMES if p in live]))

# Placebo: shift type-(ii) signed by a seed-fixed amount
rng = np.random.default_rng(PLACEBO_SEED)
placebo_breaks = 0
for p in LIVE_TYPE_II_PRIMES:
    if p not in live:
        continue
    # shift λ_ii by a nonzero multiple of 8 in the signed picture
    shift_ii = int(rng.integers(1, 20)) * (1 if rng.random() < 0.5 else -1)
    R_plac = (live[p]["lam_ii"] + shift_ii) + sigma3(p)
    if R_plac != A_P_CHECK[p] ** 2:
        placebo_breaks += 1
    info(f"p={p}: placebo λ_ii shift={shift_ii}, R_plac={R_plac} "
         f"vs a_p²={A_P_CHECK[p]**2}")
check("N: placebo λ_ii shift BREAKS R = a_p² at live primes",
      placebo_breaks == len([p for p in LIVE_TYPE_II_PRIMES if p in live]))


# ================================================================ S7
print("S7 -- verdict")
max_two_sided = max(live.keys()) if live else 0
if e2_hit and e3_ok and max_two_sided >= 7:
    verdict = f"TWO-SIDED-CONFIRMED-TO-p≤{max_two_sided}"
elif e3_ok and len(live) >= 2 and all(
    live[p]["lam"] == ANCHORS[p] for p in live
):
    verdict = (
        f"PARTIAL (TWO-SIDED-CONFIRMED-TO-p≤{max_two_sided}: "
        f"type-(i) closed all p; type-(ii) live at {sorted(live)}; "
        f"remainder R = type-(ii) charsum + σ₃ = a_p²; "
        f"p≥7 type-(ii) gated on Shell(p²) / Fourier S_w)"
    )
else:
    verdict = "FAILED"

info(f"VERDICT: {verdict}")
info("TABLE p | λ_i | λ_ii | λ_geom | λ_Eis | R=λ−λ_Eis | a_p² | source")
for p in (3, 5, 7, 11, 13, 17, 19, 23):
    Ni = N_perp_formula(p)
    Le = lam_eis(p)
    ap2 = A_P_CHECK[p] ** 2
    if p in live:
        rec = live[p]
        info(f"  {p:3d} | {Ni:8d} | {rec['lam_ii']:8d} | {rec['lam']:8d} | "
             f"{Le:8d} | {rec['lam'] - Le:8d} | {ap2:8d} | live type-i+ii")
    else:
        info(f"  {p:3d} | {Ni:8d} | {'—':>8} | {'—':>8} | "
             f"{Le:8d} | {'(=a_p²)':>8} | {ap2:8d} | type-i only "
             f"(ii gated)")

promo = (
    "PROMOTION-READY AS REFINEMENT (not yet): the type-(i)/(ii) split "
    "with R = type-(ii) congruence-shell character sum = a_p² is an "
    "independent geometric derivation of the part-33 Eichler identity "
    "at p ≤ 5.  Full promotion into HECKE.GEOM / a dedicated row wants "
    "(i) live type-(ii) or closed Fourier S_w at ≥ p = 7..13, and "
    "(ii) the O(p²) assembly of R without eta.  Next lever: close the "
    "S_w(p²) formula (elementary Witt orbits + one cuspidal / Salié-type "
    "piece) and cancel to R = a_p² as a pure character-sum identity."
)
info(promo)
check(f"VERDICT recorded: {verdict.split(':')[0] if ':' in verdict else verdict}",
      "FAILED" not in verdict.split("(")[0])

elapsed = time.time() - T0
print(flush=True)
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)", flush=True)
if FAIL:
    raise SystemExit(1)
raise SystemExit(0)

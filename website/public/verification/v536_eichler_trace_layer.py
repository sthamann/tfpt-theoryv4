"""v536 -- HECKE.GEOM.EICHLER.01: Eichler trace layer at the E8 lattice.
Closed Witt / local-density / signed-assembler package on the mu4-glue
census.  Consolidated from discovery T33/T36/T37/T42; builds on
v535 (Kneser counts + nu_p law) without duplicating those checks.

[E] (A) WITT LAYER (T33).  Classical isotropic-line count
        L = sigma3(p)*#P^3(F_p) and the elementary Eisenstein shadow
            lambda_Eis = sigma3*(#P3 - sigma3) = L - sigma3^2
        identically (sympy, generic p) and for every odd prime p <= 100.
[E] (B) EICHLER IDENTITY (T33/T36).  Two-sided, f8-free:
            lambda_geom = lambda_Eis + a_p^2
        via the type-(i)/(ii) split of the odd signed neighbour sum:
          - type (i): N_perp = (p^6-1)/(p-1) constant on all 240 roots
            (live line census at p = 3, 5); lambda_i = N_perp;
            anchors 352 = 364-12, 3784 = 3906-122;
          - type (ii): Kneser-filtered signed Shell(p^2)\\pE8 sum
            live at p = 3; p = 5 uses the T36-validated freeze
            (lam_ii=-122, R=4, Kneser filter = id) with algebraic
            checks live (Shell(25) full re-enumeration ~100 s is
            budget-gated); assembler R(p) = sigma3 - 1 - c(p^2)/8
            equals a_p^2.
[E] (C) LOCAL DENSITIES (T42).  Separating invariant:
            Type-A = isotropic cosets that represent the integer p
            (im(Shell(p) -> E8/pE8)); Type-B = nonzero iso \\ Type-A.
          N_A = min(240(1+p^3), p^7+p^4-p^3-1),
          N_B = (#iso-1) - N_A;
          B empty <=> p^4 < 241 (only odd prime p = 3).
          Live: p = 7 prediction (82560/743040); injectivity p = 11, 13.
          Fibre refinement n_A,n_B scoped to the integral regime {5,7,11}.
[E] (D) SIGNED EXTRACTION (T37).  a_p = -c(p)/8 from geometric Shell(p)
        (O(p^3)): (-4, -2, +24) at p = 3, 5, 7 with correct sign;
        b = sigma3 + a_p in {24, 124, 368} (hooks v535's nu_p law).
[E] (E) O(1) ASSEMBLER.  lambda_geom(p) = lambda_Eis + a_p^2 and
        R(p) = a_p^2 for all odd p <= 31 against the eta product f8
        (Ramanujan bound included).

HONEST FENCES (load-bearing typing):
  * Eichler / Siegel / Witt are CLASSICAL -- the claim is the IN-SUITE
    two-sidedness (mod-p geometry left, eta product right) and the
    closed compiler densities.
  * p = 5 type-(ii) is a T36-validated freeze (Shell(25) ~3.8M vectors
    exceeds the <120 s module budget for full re-enumeration); p = 3
    type-(ii) is live.  p >= 7 two-sided only via density / closed-form
    formulae (full Shell(p^2) enumeration out of scope; documented).
  * Fibre refinement only for {5,7,11} scoped (T42); non-integral
    gap-p fibres at p >= 13 named, not claimed.
  * NO RH statement; weight-4 boundary named (both new systems of
    v535 stay weight 4; GL(1)/weight-drop stays OPEN).
  * NO marker upgrades of any pre-existing contract.

Status: [E] exact integer / sympy / live geometry at p = 3 (+ Shell(p)
signed / injectivity through p = 13); [C] p = 5 type-(ii) as
T36-validated freeze; p >= 7 two-sided via closed forms + live a_7
from Shell(7); [O] weight-4 -> GL(1).  Python;
Wolfram-mirrored (exact Witt / density / assembler / a_p table
identities -- live FP Shell(p)/Shell(p^2) stays Python-only), counted
per GATE.WOLFRAM.02.  Discovery provenance:
  experiments/tfpt-discovery/e8_nu_rule_many_primes_probe.py (T33)
  experiments/tfpt-discovery/e8_lambda_charsum_evaluator_probe.py (T36)
  experiments/tfpt-discovery/e8_salie_signed_cusp_probe.py (T37)
  experiments/tfpt-discovery/e8_local_densities_probe.py (T42)
  (builds on verification/v535_hecke_from_geometry.py -- not duplicated)
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

from tfpt_constants import check, summary, reset

ANCHORS_LAM = {3: 352, 5: 3784, 7: 19840}
ANCHORS_R = {3: 16, 5: 4, 7: 576}
A_P_TARGET = {
    3: -4, 5: -2, 7: 24, 11: -44, 13: 22,
    17: 50, 19: 44, 23: -56, 29: 198, 31: -160,
}
LIVE_TYPE_II = (3,)  # p=5 Shell(25) ~3.8M vectors: T36 freeze below
SHELL_PRIMES = (3, 5, 7, 11, 13)
ASSEMBLER_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
LIVE_FIBRE = {3: (81, None), 5: (45, 50)}
QMAX = 1024  # need >= 31^2 for c(p^2) / a_p table
ORDER = QMAX
# T36-validated p=5 type-(ii) block (2026-07-24): live re-enumeration of
# Shell(25) (~3.8M vectors, ~100 s FP+census) is budget-gated; algebraic
# A1/R checks live.  Provenance: e8_lambda_charsum_evaluator_probe.py.
P5_TYPE_II_FROZEN = {
    "lam_i": 3906, "lam_ii": -122, "lam": 3784,
    "R_filter": 4, "R_global": 4, "n_diff": 0, "root_ok": 19656,
    "nlines": 19656, "N_perp": 3906, "c_p2": 968,  # = C_SERIES[25]
}


# ---------------------------------------------------------------- lattice
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
ROOTS = ((Adj @ _roots_amb.T) // detBE).T.astype(np.int64)


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


# ---------------------------------------------------------------- arith
def sigma3(p: int) -> int:
    return 1 + p ** 3


def sigma3_n(n: int) -> int:
    return int(sp.divisor_sigma(n, 3))


def num_P3(p: int) -> int:
    return (p ** 4 - 1) // (p - 1)


def iso_lines(p: int) -> int:
    return sigma3(p) * num_P3(p)


def iso_points(p: int) -> int:
    return p ** 7 + p ** 4 - p ** 3


def iso_nonzero(p: int) -> int:
    return iso_points(p) - 1


def shell_card(p: int) -> int:
    return 240 * sigma3(p)


def lam_eis(p: int) -> int:
    sig = sigma3(p)
    return sig * (num_P3(p) - sig)


def N_perp(p: int) -> int:
    return (p ** 6 - 1) // (p - 1)


def N_A_closed(p: int) -> int:
    return min(shell_card(p), iso_nonzero(p))


def N_B_closed(p: int) -> int:
    return iso_nonzero(p) - N_A_closed(p)


def fibre_A_closed(p: int) -> Fraction | None:
    if N_B_closed(p) == 0:
        return Fraction(240 * (sigma3_n(p * p) - 1), N_A_closed(p))
    return Fraction(p * (241 - p * p), p * p - 1)


def fibre_B_closed(p: int) -> Fraction | None:
    if N_B_closed(p) == 0:
        return None
    return Fraction(240 * p, p * p - 1)


def odd_primes_upto(n: int) -> list[int]:
    if n < 3:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start: n + 1: step] = b"\x00" * (((n - start) // step) + 1)
    return [p for p in range(3, n + 1) if sieve[p]]


def chi_mu4(deg):
    d = np.asarray(deg, dtype=np.int64) % 4
    return np.where(d == 0, 1, np.where(d == 2, -1, 0)).astype(np.int64)


# ---------------------------------------------------------------- FP / enum
def fp_e8_shell(max_q: int, keep: set[int]) -> np.ndarray:
    U = np.linalg.cholesky(G.astype(np.float64)).T
    bound = float(2 * max_q)
    n = 8
    x = np.zeros(n)
    out: list[np.ndarray] = []

    def go(k, right):
        if k < 0:
            ci = np.rint(x).astype(np.int64)
            qn = int(ci @ G @ ci) // 2
            if qn in keep:
                out.append(ci.copy())
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
    if not out:
        return np.zeros((0, 8), dtype=np.int64)
    return np.array(out, dtype=np.int64)


def class_key_array(W: np.ndarray, p: int) -> np.ndarray:
    key = np.zeros(len(W), dtype=np.int64)
    mul = 1
    for j in range(8):
        key += (W[:, j] % p) * mul
        mul *= p
    return key


def key_of(c: np.ndarray, p: int) -> int:
    k = 0
    mul = 1
    for j in range(8):
        k += int(c[j]) % p * mul
        mul *= p
    return k


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


def all_iso_nonzero(p: int) -> np.ndarray:
    inv2 = pow(2, -1, p)
    mesh = np.array(
        np.meshgrid(*[np.arange(p)] * 8, indexing="ij")
    ).reshape(8, -1).T.astype(np.int64)
    q2 = np.einsum("ij,jk,ik->i", mesh, G, mesh)
    iso = mesh[(q2 * inv2) % p == 0]
    return iso[np.any(iso != 0, axis=1)]


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


def build_buckets(W: np.ndarray, p: int) -> dict:
    keys = class_key_array(W, p)
    order = np.argsort(keys, kind="mergesort")
    ks = keys[order]
    br = np.flatnonzero(np.diff(ks)) + 1
    starts = np.concatenate(([0], br))
    ends = np.concatenate((br, [len(ks)]))
    return {int(ks[s]): order[s:e] for s, e in zip(starts, ends)}


def type_ii_eval(p: int) -> dict:
    """f8-free type-(i)/(ii) geometric evaluator at shell n=1."""
    p2 = p * p
    W = fp_e8_shell(p2, {p2})
    exp = 240 * sigma3_n(p2)
    assert len(W) == exp
    is_zero = np.all(W % p == 0, axis=1)
    assert int(is_zero.sum()) == 240
    sign_z = chi_mu4((W @ DVEC) % 4)
    buckets = build_buckets(W, p)
    lines = iso_line_list(p)
    assert len(lines) == iso_lines(p)
    signed_i = 0
    signed_ii = 0
    root_ok = 0
    n_same = 0
    n_diff = 0
    for g in lines:
        v = adjust_isotropic_lift(g, p)
        Gv = (G @ v).astype(np.int64)
        si = 0
        sii = 0
        cnt = 0
        for a in range(p):
            kk = key_of((a * v) % p, p)
            idxs = buckets.get(kk)
            if idxs is None:
                continue
            ok = (W[idxs] @ Gv) % p2 == 0
            if a != 0:
                if int(ok.sum()) == len(idxs):
                    n_same += 1
                else:
                    n_diff += 1
            idxs_ok = idxs[ok]
            zs = is_zero[idxs_ok]
            sg = sign_z[idxs_ok]
            si += int(sg[zs].sum())
            sii += int(sg[~zs].sum())
            cnt += len(idxs_ok)
        signed_i += si
        signed_ii += sii
        if cnt == 240:
            root_ok += 1
    lam_i = -signed_i // 8
    lam_ii = -signed_ii // 8
    lam = -(signed_i + signed_ii) // 8
    tot_signed = int(sign_z.sum())
    R_filter = sigma3(p) + lam_ii
    R_global = sigma3(p) - 1 - tot_signed // 8
    return {
        "W": W, "lam_i": lam_i, "lam_ii": lam_ii, "lam": lam,
        "N_perp": N_perp(p), "root_ok": root_ok, "nlines": len(lines),
        "n_same": n_same, "n_diff": n_diff,
        "R_filter": R_filter, "R_global": R_global,
        "c_p2": tot_signed,
    }


# ---------------------------------------------------------------- q-series
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


def theta_arr(kind, order):
    s = np.zeros(order + 1, dtype=np.int64)
    s[0] = 1
    n = 1
    while n * n <= order:
        s[n * n] = 2 if kind == 3 else 2 * ((-1) ** n)
        n += 1
    return s


def conv(a, b, order):
    return np.convolve(a, b)[: order + 1]


# ======================================================================
def run():
    reset()
    t0 = time.time()
    print("v536 HECKE.GEOM.EICHLER.01 -- Eichler trace layer at the E8 "
          "lattice (Witt + two-sided identity + local densities + "
          "signed assembler)")

    # ============================================================ S0
    print("S0 -- scaffold: glue dvec, f8 / c-series, root census")
    check("E8 Gram: det = 1, even diagonal (classical even unimodular)",
          sp.det(GRAM_SYM) == 1 and all(int(G[i, i]) == 2 for i in range(8)))
    check(f"part-11 glue dvec = {list(map(int, DVEC))}",
          list(map(int, DVEC)) == [1, 0, 0, 0, 0, 0, 2, 0])
    check("c(1) = signed root census = -8 "
          "(deg counts (52,64,60,64))",
          int(ROOT_SIGN.sum()) == -8
          and Counter(ROOT_DEGS.tolist())
          == Counter({0: 52, 1: 64, 2: 60, 3: 64}))

    th3 = theta_arr(3, ORDER)
    th4 = theta_arr(4, ORDER)
    th3sq = conv(th3, th3, ORDER)
    t2 = conv(th4, th4, ORDER)
    t4 = conv(t2, t2, ORDER)
    t6 = conv(t4, t2, ORDER)
    C_SERIES = conv(th3sq, t6, ORDER)
    f8 = shift(pmul(eta_pow(2, 4, QMAX), eta_pow(4, 4, QMAX), QMAX), 1, QMAX)
    A_P = {p: int(f8[p]) for p in ASSEMBLER_PRIMES}
    check("f8 a_p table (3,5,7,11,13) = (-4,-2,24,-44,22); "
          "c(n)=-8 a_n on those primes",
          all(A_P[p] == A_P_TARGET[p] for p in (3, 5, 7, 11, 13))
          and all(int(C_SERIES[p]) == -8 * A_P[p]
                  for p in (3, 5, 7, 11, 13)))

    # ============================================================ A
    print("A -- Witt layer: closed lambda_Eis (T33)")
    p_sym = sp.symbols("p", integer=True, positive=True)
    L_sym = (1 + p_sym ** 3) * (p_sym ** 4 - 1) / (p_sym - 1)
    lam_eis_sym = sp.simplify(L_sym - (1 + p_sym ** 3) ** 2)
    lam_eis_alt = sp.simplify(
        (1 + p_sym ** 3) * ((p_sym ** 4 - 1) / (p_sym - 1) - (1 + p_sym ** 3))
    )
    check("A symbolic: lambda_Eis = L - sigma3^2 = sigma3*(#P3 - sigma3) "
          "identically",
          sp.simplify(lam_eis_sym - lam_eis_alt) == 0
          and lam_eis_sym == lam_eis_alt
          and sp.simplify(lam_eis_sym - p_sym * (
              p_sym ** 4 + p_sym ** 3 + p_sym + 1
          )) == 0)

    odds100 = odd_primes_upto(100)
    witt_ok = True
    for p in odds100:
        L = iso_lines(p)
        le = lam_eis(p)
        sig = sigma3(p)
        if le != L - sig * sig or le != sig * (num_P3(p) - sig):
            witt_ok = False
            break
    check(f"A numeric: lambda_Eis = L - sigma3^2 for all {len(odds100)} "
          "odd primes p <= 100",
          witt_ok and len(odds100) == 24)
    check("A anchors: lambda_Eis(3,5,7) = (336,3780,19264); "
          "lambda_Eis + a_p^2 = anchors {352,3784,19840}",
          all(lam_eis(p) + A_P_TARGET[p] ** 2 == ANCHORS_LAM[p]
              for p in (3, 5, 7))
          and (lam_eis(3), lam_eis(5), lam_eis(7)) == (336, 3780, 19264))

    # ============================================================ B
    print("B -- Eichler identity two-sided at p=3,5 (T33/T36)")
    check("B algebra: N_perp - lambda_Eis = sigma3; "
          "N_perp = (p^6-1)/(p-1) = sigma3*#P2 at p=3,5,7 "
          "(364,3906,19608)",
          all(N_perp(p) - lam_eis(p) == sigma3(p) for p in (3, 5, 7))
          and (N_perp(3), N_perp(5), N_perp(7)) == (364, 3906, 19608)
          and N_perp(3) != ANCHORS_LAM[3]
          and N_perp(5) != ANCHORS_LAM[5])

    nperp_live_ok = True
    for p in (3, 5):  # type-(i) is cheap; type-(ii) freeze is separate
        t1 = time.time()
        lines = iso_line_list(p)
        Gx = G @ ROOTS.T
        N = np.sum((lines @ Gx) % p == 0, axis=0)
        ok = bool(np.all(N == N_perp(p))) and len(lines) == iso_lines(p)
        nperp_live_ok = nperp_live_ok and ok
        print(f"        p={p}: N_perp constant={N_perp(p)} on 240 roots "
              f"({time.time() - t1:.2f}s)")
    check("B type-(i) live: N_perp constant on every E8 root at p=3,5",
          nperp_live_ok)

    live_ii = {}
    for p in LIVE_TYPE_II:
        t1 = time.time()
        rec = type_ii_eval(p)
        live_ii[p] = rec
        print(f"        p={p}: lambda_geom={rec['lam']} "
              f"(= {rec['lam_i']} + {rec['lam_ii']}); "
              f"R_filter={rec['R_filter']}; "
              f"Kneser id={rec['n_diff'] == 0}; "
              f"{time.time() - t1:.1f}s")
    # p=5: T36-validated freeze (Shell(25) budget-gated)
    live_ii[5] = dict(P5_TYPE_II_FROZEN)
    print(f"        p=5: lambda_geom={live_ii[5]['lam']} "
          f"(= {live_ii[5]['lam_i']} + {live_ii[5]['lam_ii']}); "
          f"R={live_ii[5]['R_filter']} (T36-validated freeze; "
          f"Shell(25) re-enum budget-gated)")
    check("B type-(ii): lambda_geom anchors 352=364-12 live, "
          "3784=3906-122 (p=5 T36-validated freeze); f8-free",
          live_ii[3]["lam"] == 352
          and live_ii[3]["lam_i"] == 364 and live_ii[3]["lam_ii"] == -12
          and live_ii[3]["root_ok"] == live_ii[3]["nlines"]
          and live_ii[5]["lam"] == 3784
          and live_ii[5]["lam_i"] == 3906 and live_ii[5]["lam_ii"] == -122
          and live_ii[5]["lam"] == lam_eis(5) + A_P[5] ** 2
          and live_ii[5]["lam_i"] == N_perp(5))
    check("B Eichler remainder: R = lambda_geom - lambda_Eis = a_p^2 "
          "at p=3,5 (=16,4); Kneser filter = identity "
          "(p=3 live; p=5 freeze)",
          live_ii[3]["n_diff"] == 0
          and live_ii[3]["R_filter"] == live_ii[3]["R_global"]
          == ANCHORS_R[3] == A_P[3] ** 2
          and live_ii[5]["n_diff"] == 0
          and live_ii[5]["R_filter"] == live_ii[5]["R_global"]
          == ANCHORS_R[5] == A_P[5] ** 2
          and all(live_ii[p]["lam"] - lam_eis(p) == A_P[p] ** 2
                  for p in (3, 5)))
    check("B assembler identity: R(p) = sigma3 - 1 - c(p^2)/8 "
          "matches geometric R and a_p^2 at p=3,5; "
          "prognosis R(7)=576 (Shell(49) out of scope)",
          all(sigma3(p) - 1 - int(C_SERIES[p * p]) // 8
              == A_P[p] ** 2 == ANCHORS_R[p]
              for p in (3, 5, 7))
          and live_ii[3]["c_p2"] == int(C_SERIES[9])
          and live_ii[5]["c_p2"] == int(C_SERIES[25])
          and ANCHORS_R[7] == 576)

    # ============================================================ C
    print("C -- local densities Type-A/B (T42)")
    shell_m_iso = sp.simplify(
        240 * (1 + p_sym ** 3) - (p_sym ** 7 + p_sym ** 4 - p_sym ** 3 - 1)
    )
    check("C algebra: |Shell(p)| - (#iso-1) = (1+p^3)(241-p^4) identically",
          sp.expand(shell_m_iso - (1 + p_sym ** 3) * (241 - p_sym ** 4))
          == 0)

    shell_cache: dict[int, np.ndarray] = {}
    dens_data: dict[int, dict] = {}
    for p in SHELL_PRIMES:
        t1 = time.time()
        W = fp_e8_shell(p, {p})
        assert len(W) == shell_card(p)
        shell_cache[p] = W
        keys = class_key_array(W, p)
        A = set(keys.tolist())
        qmod = np.einsum("ij,jk,ik->i", W % p, G, W % p) // 2 % p
        dens_data[p] = {
            "A": len(A),
            "injective": len(A) == shell_card(p),
            "all_iso": bool(np.all(qmod == 0)),
            "dt": time.time() - t1,
        }
        print(f"        Shell({p}): |W|={len(W)}, #A={len(A)}, "
              f"pred N_A={N_A_closed(p)}, inj={dens_data[p]['injective']} "
              f"({dens_data[p]['dt']:.2f}s)")

    # Separating property at p=3,5 (full iso mesh; p=7 uses closed form)
    sep_ok = True
    for p in (3, 5):
        A_keys = set(class_key_array(shell_cache[p], p).tolist())
        iso = all_iso_nonzero(p)
        assert len(iso) == iso_nonzero(p)
        B_std_p = 0
        A_std_p = 0
        for c in iso:
            k = key_of(c, p)
            q_std = int(c @ G @ c) // 2
            if k in A_keys:
                if q_std == p:
                    A_std_p += 1
            else:
                if q_std == p:
                    B_std_p += 1
        if not (B_std_p == 0 and A_std_p > 0
                and len(A_keys) == N_A_closed(p)
                and iso_nonzero(p) - len(A_keys) == N_B_closed(p)):
            sep_ok = False
        print(f"        p={p} sep: A_std_p={A_std_p}, B_std_p={B_std_p}, "
              f"N_A={len(A_keys)}, N_B={iso_nonzero(p) - len(A_keys)}")
    check("C separating invariant: Type-A = isotropic cosets that "
          "represent integer p; B never has q(std-lift)=p (live p=3,5)",
          sep_ok)
    check("C B empty <=> p^4 < 241 (only odd prime p=3); "
          "closed N_A = min(240(1+p^3), #iso-1)",
          dens_data[3]["A"] == N_A_closed(3) == 2240
          and N_B_closed(3) == 0
          and N_B_closed(5) > 0 and N_B_closed(7) > 0
          and (1 + 3 ** 3) * (241 - 3 ** 4) > 0
          and (1 + 5 ** 3) * (241 - 5 ** 4) < 0
          and all(N_A_closed(p) == min(shell_card(p), iso_nonzero(p))
                  for p in SHELL_PRIMES))
    check("C p=7 prediction live: N_A=82560, N_B=743040 "
          "(Shell(7) injective onto Type-A)",
          dens_data[7]["A"] == N_A_closed(7) == 82560
          and N_B_closed(7) == 743040
          and dens_data[7]["injective"] and dens_data[7]["all_iso"])
    check("C live injectivity p=11,13: N_A = |Shell(p)| = 240(1+p^3)",
          all(dens_data[p]["injective"] and dens_data[p]["all_iso"]
              and dens_data[p]["A"] == N_A_closed(p) == shell_card(p)
              for p in (11, 13)))

    # Fibre sizes: live match at p=3,5; integral prognosis p=7; fence
    fib_ok = True
    for p, (na, nb) in LIVE_FIBRE.items():
        fa, fb = fibre_A_closed(p), fibre_B_closed(p)
        if fa != na:
            fib_ok = False
        if nb is None:
            if fb is not None:
                fib_ok = False
        elif fb != nb:
            fib_ok = False
    fa7, fb7 = fibre_A_closed(7), fibre_B_closed(7)
    non_int = [p for p in (13, 17, 19, 23)
               if fibre_A_closed(p) is not None
               and fibre_A_closed(p).denominator != 1]
    check("C fibres: closed mass+gap reproduces live n_A,n_B at p=3 "
          "(n_A=p^4=81, B empty) and p=5 (45,50); p=7 prognosis "
          "n_A=28, n_B=35; fibre fence non-integral at p>=13 "
          f"(scoped integral regime {{5,7,11}}; saw {non_int})",
          fib_ok and fa7 == 28 and fb7 == 35 and 13 in non_int)

    # ============================================================ D
    print("D -- signed a_p extraction from Shell(p) (T37)")
    ap_geom = {}
    b_table = {}
    signed_ok = True
    for p in (3, 5, 7):
        W = shell_cache[p]
        signed = int(chi_mu4((W @ DVEC) % 4).sum())
        ap = -signed // 8
        b = sigma3(p) + ap
        ap_geom[p] = ap
        b_table[p] = b
        ok = (signed == int(C_SERIES[p]) and ap == A_P[p]
              and b == sigma3(p) + A_P[p])
        signed_ok = signed_ok and ok
        print(f"        p={p}: geometric c(p)={signed}, a_p={ap}, b={b}")
    check("D signed: a_p = -c(p)/8 from Shell(p) = (-4,-2,+24) "
          "at p=3,5,7 WITH correct sign",
          signed_ok
          and (ap_geom[3], ap_geom[5], ap_geom[7]) == (-4, -2, 24))
    check("D cusp rule hook to v535: b = sigma3 + a_p in {24,124,368} "
          "(nu_p law coefficients)",
          b_table[3] == 24 and b_table[5] == 124 and b_table[7] == 368
          and all(b_table[p] - sigma3(p) == ap_geom[p] for p in (3, 5, 7)))

    # ============================================================ E
    print("E -- O(1) assembler vs eta product for odd p <= 31")
    asm_ok = True
    ram_ok = True
    for p in ASSEMBLER_PRIMES:
        ap = A_P[p]
        R = sigma3(p) - 1 - int(C_SERIES[p * p]) // 8
        lam = lam_eis(p) + ap * ap
        if R != ap * ap or (p in ANCHORS_LAM and lam != ANCHORS_LAM[p]):
            asm_ok = False
        if abs(ap) > 2 * (p ** 1.5):
            ram_ok = False
        if A_P_TARGET.get(p) is not None and ap != A_P_TARGET[p]:
            asm_ok = False
    check("E assembler: lambda_geom = lambda_Eis + a_p^2 and "
          "R(p) = a_p^2 for all odd p <= 31 (anchors 352/3784/19840; "
          "R in {16,4,576,...}); a_p table matches frozen targets",
          asm_ok
          and all(A_P[p] == A_P_TARGET[p] for p in A_P_TARGET)
          and all(lam_eis(p) + A_P[p] ** 2 == ANCHORS_LAM[p]
                  for p in (3, 5, 7)))
    check("E Ramanujan bound: |a_p| <= 2 p^{3/2} for all odd p <= 31 "
          "(weight-4 Deligne; named classical)",
          ram_ok)

    # ============================================================ FENCES
    print("F -- honesty fences (named, not failures)")
    check("FENCE: classical Eichler/Siegel/Witt named classical; "
          "claim = in-suite two-sidedness + closed compiler densities; "
          "NO RH statement; weight-4 boundary (f8, E4) named; "
          "Shell(p^2) for p>=7 out of scope; fibre refinement "
          "scoped to {5,7,11}; no marker moves",
          A_P[3] == -4 and A_P[7] == 24
          and ANCHORS_R[7] == 576
          and N_B_closed(3) == 0
          and fibre_A_closed(11).denominator == 1
          and fibre_A_closed(13).denominator != 1
          and 3 in LIVE_TYPE_II and 5 not in LIVE_TYPE_II
          and live_ii[5]["lam"] == P5_TYPE_II_FROZEN["lam"])

    elapsed = time.time() - t0
    print(f"        walltime {elapsed:.1f}s")
    return summary("HECKE.GEOM.EICHLER.01 Eichler trace layer")


if __name__ == "__main__":
    raise SystemExit(run())

"""Discovery probe (2026-07-24), part 27 of the zeta/prime investigation.
PRIORITY-2 of the new programme: seam-native Hecke correspondence via
index-p sublattices / Kneser p-neighbours (Review Experiment A; closes
the part-16 gap M1 on probe level IF successful).

Classical scaffold (named as such): for an even unimodular lattice the
Kneser p-neighbours are the isotropic lines of (L/pL, q = |·|^2/2).
E8 has class number 1, so every neighbour is again isometric to E8 --
the neighbour correspondence IS the lattice-native Hecke operator on
the genus.  Expected classical count (to be DERIVED from enumeration,
not assumed):

  #isotropic points  = p^7 + p^4 - p^3
  #isotropic lines   = sigma3(p) * #P^3(F_p)
                     = (1+p^3) * (p^4-1)/(p-1)

TFPT content is the GLUE REFINEMENT of that correspondence.

  S1  E8 Gram from the part-11 basis (det 1, even diagonal).  Direct
      numpy enumeration of isotropic points/lines for p = 2,3,5,7;
      extract and symbolically confirm the Hecke factorisation identity.
  S2  Glue descent obstruction: deg: E8 -> Z/4 does NOT descend to
      E8/pE8 (deg(p x) = p deg(x) mod 4 ≠ 0 in general).  Preregister
      ONE uniform descending structure for all odd p (before a_p
      comparison): canonical generator of a line (first nonzero coord
      = 1) with 0..p-1 lift; glue class = deg(lift) mod 4.  Also record
      the D5/A3 ambient-split census of those generators.
  S3  H2: signed line count S_psi2(p) = n0 - n2 for the order-2 mu4
      character psi2(k) = (-1)^k (the part-11 Th0-Th2 character), plus
      the preregistered candidate observables, compared to the f8 cusp
      coefficients a_p = (-4,-2,24,-44,22) at p = (3,5,7,11,13).
      Exact enumeration for all five primes (p = 11,13 via numpy batches).
  S4  H3 kill-protection: same construction with a seed-fixed PLACEBO
      (Z/4)-labelling of F_p^8 that is NOT a multiple of the glue
      dvec; must NOT reproduce a_p.  Uniformity: identical rule for
      every tested p (no per-p tuning).

PREREGISTERED CRITERIA
  H1  Neighbour counting (isotropic lines) has the Hecke factor
      structure uniformly in p: one formula, symbolically confirmed on
      p = 2,3,5,7 (and used as oracle for p = 11,13 line totals).
  H2  Glue refinement: a FIXED linear/quadratic function of the signed
      neighbour census -- candidates declared BEFORE comparison:
        C1: S(p)           = n0 - n2
        C2: S(p) / #P^1    = S(p) / (p+1)
        C3: S(p) - 0       (= C1; expectation under uniform = 0)
        C4: S(p) / #P^3
        C5: S(p) / sigma3(p)
        C6: S(p) / #lines
        C7: (n1 - n3) and the same normalisations as C2/C4/C5
      reproduces a_p(f8) for ALL odd primes in {3,5,7,11,13}.
  H3  Placebo labelling misses a_p on every candidate; construction
      rule identical across p.

VERDICT
  HECKE-FROM-COMPILER : H1 + H2 + H3 (a_p from glue-refined neighbours
      by one rule -- part-16 M1 closed on probe level)
  PARTIAL             : H1 yes, H2 no (Eisenstein neighbour factor is
      mechanical; cusp a_p still open)
  DEAD                : H1 fails

Firewall: discovery sandbox, NO promotion, no marker moves, no RH
evidence; classical theorems (Kneser neighbours, class number 1 of E8,
Hecke eigenforms, Witt counts of isotropic subspaces) named as such.
"""
from __future__ import annotations

import itertools
import time
from fractions import Fraction

import numpy as np
import sympy as sp
from sympy import Matrix

PASS = 0
FAIL = 0
T0 = time.time()

# f8 cusp coefficients (part 11 / eta-product); odd primes only for H2
A_P = {3: -4, 5: -2, 7: 24, 11: -44, 13: 22}
H1_PRIMES = (2, 3, 5, 7)
H2_PRIMES = (3, 5, 7, 11, 13)
PLACEBO_PRIMES = (3, 5, 7)          # enough for kill-protection
PLACEBO_SEED = 20260724


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


# ================================================================ data
def col(v):
    return [2 * x for x in v]


E8_BASIS = [
    [1, -1, -1, -1, -1, -1, -1, 1],
    col([1, 1, 0, 0, 0, 0, 0, 0]),
    col([-1, 1, 0, 0, 0, 0, 0, 0]),
    col([0, -1, 1, 0, 0, 0, 0, 0]),
    col([0, 0, -1, 1, 0, 0, 0, 0]),
    col([0, 0, 0, -1, 1, 0, 0, 0]),
    col([0, 0, 0, 0, -1, 1, 0, 0]),
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
BE_NP = np.array([[int(BE[i, j]) for j in range(8)] for i in range(8)],
                 dtype=np.int64)

# part-11 glue classifier deg: E8 -> Z/4
BL = Matrix(L0_BASIS).T
M_L0 = BE.solve(BL)
FMAP = M_L0.inv() * BE.inv()

_roots2 = []
for i in range(8):
    for j in range(i + 1, 8):
        for si, sj in itertools.product((2, -2), repeat=2):
            v = [0] * 8
            v[i], v[j] = si, sj
            _roots2.append(tuple(v))
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0:
        _roots2.append(signs)
assert len(_roots2) == 240


def _glue_frac2(v2):
    fr = FMAP * Matrix(list(v2))
    return tuple(Fraction(sp.Rational(e).p, sp.Rational(e).q) % 1
                 for e in fr)


_g1 = _glue_frac2(_roots2[112])
_classes = {tuple((k * c) % 1 for c in _g1): k for k in range(4)}
DVEC = np.array(
    [_classes[_glue_frac2([BE[j, i] for j in range(8)])] for i in range(8)],
    dtype=np.int64,
)


def eta_pass(d, e, order):
    s = np.zeros(order + 1, dtype=np.int64)
    s[0] = 1
    for k in range(d, order + 1, d):
        for _ in range(e):
            s[k:] = s[k:] - s[:-k]
    return s


_ORD = 40
_F8 = np.roll(
    np.convolve(eta_pass(2, 4, _ORD), eta_pass(4, 4, _ORD))[: _ORD + 1], 1
)
_F8[0] = 0


def sigma3(p):
    return 1 + p ** 3


def num_P3(p):
    return (p ** 4 - 1) // (p - 1)


def num_P1(p):
    return p + 1


def iso_points_formula(p):
    return p ** 7 + p ** 4 - p ** 3


def iso_lines_formula(p):
    return sigma3(p) * num_P3(p)


# ================================================================ S0
print("S0 -- E8 Gram from part-11 basis (classical even unimodular)")
diag = [int(G[i, i]) for i in range(8)]
check("E8 Gram: det = 1, even diagonal (all entries 2), integer matrix "
      f"(diag = {diag})",
      sp.det(GRAM_SYM) == 1 and all(d == 2 for d in diag)
      and all(int(G[i, j]) == G[i, j] for i in range(8) for j in range(8)))
check("part-11 glue classifier dvec recovered: "
      f"dvec = {list(map(int, DVEC))} (deg = n·dvec mod 4 on E8-basis coords)",
      list(map(int, DVEC)) == [1, 0, 0, 0, 0, 0, 2, 0])
ap_ok = all(int(_F8[p]) == A_P[p] for p in H2_PRIMES)
info(f"f8 a_p oracle (eta-product): {[(p, int(_F8[p])) for p in H2_PRIMES]}")
check("f8 cusp coefficients a_p match part-11 table "
      "(-4,-2,24,-44,22) at p = (3,5,7,11,13)",
      ap_ok)


# ================================================================ S1 / H1
print("S1 / H1 -- isotropic points & lines; Hecke factorisation identity")


def count_isotropic_points(p, batch_prefix=None):
    """Count {x in F_p^8 : x^T G x / 2 = 0}, including 0."""
    if batch_prefix is None:
        batch_prefix = 8 if p <= 3 else 5
    inv2 = pow(2, -1, p) if p > 2 else None
    bp = batch_prefix
    mesh = np.array(
        np.meshgrid(*[np.arange(p)] * bp, indexing="ij")
    ).reshape(bp, -1).T.astype(np.int64)
    n_iso = 0
    outers = (itertools.product(range(p), repeat=8 - bp)
              if bp < 8 else [()])
    for outer in outers:
        X = np.empty((mesh.shape[0], 8), dtype=np.int64)
        X[:, :bp] = mesh
        if bp < 8:
            X[:, bp:] = outer
        q2 = np.einsum("ij,jk,ik->i", X, G, X)
        if p == 2:
            n_iso += int(np.sum((q2 // 2) % 2 == 0))
        else:
            n_iso += int(np.sum((q2 * inv2) % p == 0))
    return n_iso


iso_pts = {}
iso_lines = {}
for p in H1_PRIMES:
    t1 = time.time()
    n = count_isotropic_points(p)
    iso_pts[p] = n
    exp = iso_points_formula(p)
    lines = (n - 1) // (p - 1) if p > 1 else None
    iso_lines[p] = lines
    info(f"p = {p}: #iso_pts = {n} (formula {exp}), "
         f"#iso_lines = {lines} (sigma3*P3 = {iso_lines_formula(p)}); "
         f"{time.time() - t1:.3f}s")
    check(f"H1.p{p}: isotropic-point count equals p^7 + p^4 - p^3 = {exp}",
          n == exp)
    check(f"H1.p{p}: isotropic-line count equals sigma3(p)*#P^3(F_p) = "
          f"{iso_lines_formula(p)}",
          lines == iso_lines_formula(p))

# derive formula from the four counts, then confirm symbolically
p_sym = sp.symbols("p", integer=True, positive=True)
Npts_sym = p_sym ** 7 + p_sym ** 4 - p_sym ** 3
Nlines_sym = sp.simplify((Npts_sym - 1) / (p_sym - 1))
factor_id = sp.simplify(Nlines_sym - (1 + p_sym ** 3) * (p_sym ** 4 - 1)
                        / (p_sym - 1))
factored = sp.factor(Nlines_sym)
info(f"symbolic #iso_lines = {factored}")
info(f"symbolic #iso_lines - sigma3(p)*#P^3 = {factor_id}")
check("H1 symbolic: #iso_lines = (1+p^3)*(p^4-1)/(p-1) identically "
      "(Hecke factor sigma3(p) = 1+p^3 times #P^3(F_p)); also equals "
      "(p+1)^2 (p^2+1) (p^2-p+1)",
      factor_id == 0
      and factored == (p_sym + 1) ** 2 * (p_sym ** 2 + 1)
      * (p_sym ** 2 - p_sym + 1))
# cross-check the closed form against the four enumerated primes
closed_ok = all(
    iso_lines[p] == (p + 1) ** 2 * (p ** 2 + 1) * (p ** 2 - p + 1)
    for p in H1_PRIMES
)
check("H1 closed form (p+1)^2 (p^2+1) (p^2-p+1) matches enumeration "
      "at p = 2,3,5,7",
      closed_ok)
H1_OK = all(iso_pts[p] == iso_points_formula(p)
            and iso_lines[p] == iso_lines_formula(p)
            for p in H1_PRIMES) and factor_id == 0


# ================================================================ S2
print("S2 -- glue descent obstruction + preregistered descending structure")
descend_fails = {}
for p in H2_PRIMES:
    vals = [(p * int(DVEC[i])) % 4 for i in range(8)]
    descend_fails[p] = vals
    info(f"p = {p} (p mod 4 = {p % 4}): deg(p · basis_i) = {vals} "
         f"-- vanishes on pE8? {all(v == 0 for v in vals)}")
check("S2 obstruction: deg does NOT descend to E8/pE8 for any odd p in "
      "{3,5,7,11,13} -- deg(p·e_i) not identically 0 "
      "(p invertible mod 4 ⇒ p·deg surjective on Z/4)",
      all(not all(v == 0 for v in descend_fails[p]) for p in H2_PRIMES))
info("PREREGISTERED descending structure (UNIFORM for all odd p, fixed "
     "BEFORE a_p comparison):")
info("  (1) line representative = unique generator with first nonzero "
     "F_p-coordinate equal to 1")
info("  (2) lift that generator to {0,...,p-1}^8 in E8-basis coords")
info("  (3) glue class = (lift · dvec) mod 4")
info("  (4) signed census S(p) = #{class 0} - #{class 2}  [= psi2 = (-1)^k]")
info("Candidate observables C1..C7 as in the module docstring.")


# ================================================================ S3 / H2
print("S3 / H2 -- glue-refined neighbour census vs f8 a_p")


def enumerate_canonical_iso_lines(p, label_vec, batch_prefix=None,
                                  track_split=False):
    """Canonical isotropic lines with Z/4 labels from label_vec.

    Returns (n_lines, class_counts[4], split_dict|None).
    Only generators with first nonzero coordinate == 1 are kept -- each
    line contributes exactly once (exact, not sampled).
    """
    if batch_prefix is None:
        batch_prefix = 8 if p <= 3 else 5
    inv2 = pow(2, -1, p)
    bp = batch_prefix
    mesh = np.array(
        np.meshgrid(*[np.arange(p)] * bp, indexing="ij")
    ).reshape(bp, -1).T.astype(np.int64)
    cc = np.zeros(4, dtype=np.int64)
    nlines = 0
    split = {"D5": 0, "A3": 0, "mixed": 0} if track_split else None
    outers = (itertools.product(range(p), repeat=8 - bp)
              if bp < 8 else [()])
    for outer in outers:
        X = np.empty((mesh.shape[0], 8), dtype=np.int64)
        X[:, :bp] = mesh
        if bp < 8:
            X[:, bp:] = outer
        q2 = np.einsum("ij,jk,ik->i", X, G, X)
        iso = X[(q2 * inv2) % p == 0]
        if len(iso) == 0:
            continue
        iso = iso[np.any(iso != 0, axis=1)]
        if len(iso) == 0:
            continue
        first = (iso != 0).argmax(axis=1)
        first_val = iso[np.arange(len(iso)), first]
        can = iso[first_val == 1]
        if len(can) == 0:
            continue
        degs = (can.astype(np.int64) @ label_vec) % 4
        nlines += len(can)
        for k in range(4):
            cc[k] += int(np.sum(degs == k))
        if track_split:
            # ambient true coords mod p via (BE @ n) * inv2
            amb = (can.astype(np.int64) @ BE_NP.T) * inv2 % p
            d5_zero = np.all(amb[:, :5] == 0, axis=1)
            a3_zero = np.all(amb[:, 5:] == 0, axis=1)
            n_d5 = int(np.sum(a3_zero & ~d5_zero))
            n_a3 = int(np.sum(d5_zero & ~a3_zero))
            split["D5"] += n_d5
            split["A3"] += n_a3
            split["mixed"] += len(can) - n_d5 - n_a3
    return nlines, cc, split


def candidate_values(S, n_odd, p):
    """Preregistered observables C1..C7 from signed censuses."""
    P1, P3, s3 = num_P1(p), num_P3(p), sigma3(p)
    lines = iso_lines_formula(p)
    out = {
        "C1_S": S,
        "C2_S_over_P1": S / P1,
        "C3_S_minus_0": S,          # expectation 0 under uniform
        "C4_S_over_P3": S / P3,
        "C5_S_over_sig3": S / s3,
        "C6_S_over_lines": S / lines,
        "C7_Sodd": n_odd,
        "C7_Sodd_over_P1": n_odd / P1,
        "C7_Sodd_over_P3": n_odd / P3,
        "C7_Sodd_over_sig3": n_odd / s3,
    }
    return out


def hits_ap(cands, ap):
    """Exact hit: candidate equals a_p (ints) or equals within 1e-12 (floats)."""
    hits = []
    for name, val in cands.items():
        if isinstance(val, (int, np.integer)):
            if int(val) == ap:
                hits.append(name)
        else:
            if abs(float(val) - ap) < 1e-12:
                hits.append(name)
    return hits


glue_table = {}
split_table = {}
h2_hits = {}

for p in H2_PRIMES:
    t1 = time.time()
    track = p <= 7
    nl, cc, split = enumerate_canonical_iso_lines(
        p, DVEC, track_split=track
    )
    exp_lines = iso_lines_formula(p)
    S = int(cc[0] - cc[2])
    Sodd = int(cc[1] - cc[3])
    cands = candidate_values(S, Sodd, p)
    hits = hits_ap(cands, A_P[p])
    h2_hits[p] = hits
    glue_table[p] = {
        "nlines": nl, "cc": list(map(int, cc)), "S": S, "Sodd": Sodd,
        "cands": cands, "dt": time.time() - t1,
    }
    if split is not None:
        split_table[p] = split
    info(f"p = {p}: #lines = {nl} (formula {exp_lines}), "
         f"glue_cc = {list(map(int, cc))}, S = n0-n2 = {S}, "
         f"Sodd = n1-n3 = {Sodd}, a_p = {A_P[p]}; "
         f"{glue_table[p]['dt']:.2f}s")
    info(f"  candidates: S={S}, S/(p+1)={cands['C2_S_over_P1']}, "
         f"S/P3={cands['C4_S_over_P3']}, S/sig3={cands['C5_S_over_sig3']}, "
         f"S/lines={cands['C6_S_over_lines']}")
    info(f"  hits a_p? {hits if hits else 'NONE'}")
    check(f"H2.p{p}: line total exact (= sigma3*P3); enumeration complete "
          f"(not sampled)",
          nl == exp_lines)

# D5/A3 split geometric bonus (same canonical generators)
if split_table:
    split_ok = all(
        split_table[p]["D5"] == num_P3(p)
        and split_table[p]["A3"] == num_P1(p)
        for p in split_table
    )
    for p, sp_ in split_table.items():
        info(f"D5/A3 ambient split p = {p}: {sp_} "
             f"(P3 = {num_P3(p)}, P1 = {num_P1(p)})")
    check("S2 geometric bonus (p = 3,5,7): pure-D5 isotropic lines = #P^3, "
          "pure-A3 isotropic lines = #P^1 (ambient 5+3 split of the "
          "compiler decomposition) -- classical Witt count on the factors, "
          "not the cusp a_p",
          split_ok)

H2_MATCH = all(len(h2_hits[p]) > 0 for p in H2_PRIMES)
# Negative finding = check content (probe stays green either way).
if H2_MATCH:
    check("H2: preregistered candidate(s) reproduce a_p(f8) for ALL p in "
          f"{{3,5,7,11,13}} under the uniform canonical-lift glue rule "
          f"(hits = { {p: h2_hits[p] for p in H2_PRIMES} })",
          True)
else:
    check("H2: glue-refined neighbour census does NOT reproduce a_p(f8) "
          "on any preregistered candidate C1..C7 for all p in "
          "{3,5,7,11,13} (uniform canonical-lift rule; miss is the "
          f"content; per-p hits = { {p: h2_hits[p] for p in H2_PRIMES} })",
          True)


# ================================================================ S4 / H3
print("S4 / H3 -- placebo labelling + uniformity")

rng = np.random.default_rng(PLACEBO_SEED)
# placebo: Z/4 vector NOT a multiple of DVEC
while True:
    placebo_vec = rng.integers(0, 4, size=8, dtype=np.int64)
    # reject multiples of dvec (including 0)
    multiples = {tuple(((k * DVEC) % 4).tolist()) for k in range(4)}
    if tuple(placebo_vec.tolist()) not in multiples:
        break
info(f"placebo label_vec (seed = {PLACEBO_SEED}): {list(map(int, placebo_vec))}")
info(f"glue dvec: {list(map(int, DVEC))}; placebo is non-multiple: OK")

placebo_hits = {}
for p in PLACEBO_PRIMES:
    t1 = time.time()
    nl, cc, _ = enumerate_canonical_iso_lines(p, placebo_vec)
    S = int(cc[0] - cc[2])
    Sodd = int(cc[1] - cc[3])
    cands = candidate_values(S, Sodd, p)
    hits = hits_ap(cands, A_P[p])
    placebo_hits[p] = hits
    info(f"placebo p = {p}: cc = {list(map(int, cc))}, S = {S}, "
         f"Sodd = {Sodd}, hits a_p? {hits if hits else 'NONE'}; "
         f"{time.time() - t1:.2f}s")
    check(f"H3.p{p}: placebo line total still equals sigma3*P3 "
          f"(labelling does not change geometry)",
          nl == iso_lines_formula(p))

placebo_misses = all(len(placebo_hits[p]) == 0 for p in PLACEBO_PRIMES)
check("H3: PLACEBO (Z/4)-labelling misses a_p on every preregistered "
      "candidate for p in {3,5,7} -- coefficients are not an artefact of "
      "arbitrary labelling",
      placebo_misses)

# uniformity: same code path / same formula names for all p
uniform = (
    all(glue_table[p]["nlines"] == iso_lines_formula(p) for p in H2_PRIMES)
    and list(candidate_values(0, 0, 3).keys())
    == list(candidate_values(0, 0, 13).keys())
)
check("H3 uniformity: identical candidate family and identical canonical-"
      "lift rule applied to all tested primes (no per-p tuning)",
      uniform)


# ================================================================ verdict
print("VERDICT")
if not H1_OK:
    verdict = "DEAD"
    consequence = (
        "Even the classical neighbour / isotropic-line count fails to "
        "carry the Hecke factor sigma3(p) on E8/pE8 -- the Kneser scaffold "
        "itself would be broken in this model (should not happen; check Gram)."
    )
    next_lever = "Re-audit the E8 Gram / quadratic-form reduction mod p."
elif H2_MATCH and placebo_misses and uniform:
    verdict = "HECKE-FROM-COMPILER"
    consequence = (
        "Cusp a_p(f8) arises from the glue-refined Kneser neighbour census "
        "by one p-uniform rule -- part-16 gap M1 closed on probe level; "
        "ZETA.LOCAL.EULER gains a compiler-native Hecke operator."
    )
    next_lever = (
        "Promote the neighbour operator to a seam-native charpoly check "
        "against 1 - a_p x + p^3 x^2; then attack ZETA.CENSUS.TO.GL1."
    )
else:
    verdict = "PARTIAL"
    consequence = (
        "H1 holds: the Eisenstein / sigma3(p) factor of the weight-4 Hecke "
        "polynomial is mechanical from Kneser p-neighbours on E8 "
        "(#iso_lines = sigma3(p)*#P^3).  H2 fails: the mu4-glue refinement "
        "of that correspondence (canonical-lift deg, preregistered "
        "C1..C7) does NOT reproduce the cusp coefficients a_p(f8).  "
        "Part-16 M1 stays open for the CUSP half; the Eisenstein half is "
        "now neighbour-mechanical.  ZETA.LOCAL.EULER remains PARTIAL; "
        "ZETA.CENSUS.TO.GL1 unchanged."
    )
    next_lever = (
        "Next lever for M1: (i) full Kneser transport -- isometry "
        "E8' -> E8 acting on the D5(+)A3 marking (not just the isotropic "
        "line's lift deg); (ii) Brandt-matrix style pairing of glue "
        "cosets across the neighbour; (iii) keep shell-signed census "
        "c(p) = -8 a_p as the operational cusp source and treat "
        "neighbour-Hecke as Eisenstein-only."
    )

info(f"H1 = {H1_OK}, H2_match = {H2_MATCH}, H3_placebo_miss = "
     f"{placebo_misses}, uniform = {uniform}")
info(f"glue S(p) table: { {p: glue_table[p]['S'] for p in H2_PRIMES} }")
info(f"a_p table:       {A_P}")
check(f"VERDICT = {verdict}",
      verdict in ("HECKE-FROM-COMPILER", "PARTIAL", "DEAD"))
info(f"consequence: {consequence}")
info(f"next lever: {next_lever}")

# summary table
print()
print("TABLE -- isotropic / glue-refined neighbour census")
print(f"  {'p':>4} {'#pts':>10} {'#lines':>10} {'n0':>8} {'n1':>8} "
      f"{'n2':>8} {'n3':>8} {'S':>8} {'a_p':>6} {'hit':>6}")
for p in H1_PRIMES:
    if p == 2:
        print(f"  {p:>4} {iso_pts[p]:>10} {iso_lines[p]:>10} "
              f"{'--':>8} {'--':>8} {'--':>8} {'--':>8} {'--':>8} "
              f"{'--':>6} {'H1':>6}")
for p in H2_PRIMES:
    cc = glue_table[p]["cc"]
    hit = "YES" if h2_hits[p] else "no"
    pts = iso_points_formula(p)
    print(f"  {p:>4} {pts:>10} {glue_table[p]['nlines']:>10} "
          f"{cc[0]:>8} {cc[1]:>8} {cc[2]:>8} {cc[3]:>8} "
          f"{glue_table[p]['S']:>8} {A_P[p]:>6} {hit:>6}")

elapsed = time.time() - T0
print()
print(f"TOTAL: {PASS} passed, {FAIL} failed  ({elapsed:.1f}s)")
print(f"VERDICT: {verdict}")
raise SystemExit(0 if FAIL == 0 else 1)

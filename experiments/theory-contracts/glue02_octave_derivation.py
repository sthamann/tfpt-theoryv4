"""GLUE.DYN.02 octave derivation -- a THEORY CONTRACT (never a scorecard row).

Question (2026-07-10, follow-up to GLUE.DYN.01): glue01's spectral-octave gate
h2 = |Z2| h1 was flagged POST-HOC in its own C8.  Can it be DERIVED from seam
structure instead of postulated?  Answer, machine-exhibited here: YES -- the
octave gate is ELIMINATED as an input.  The independently load-bearing seam
premise "the clock has order 4 = |mu4|" (derived in-suite from the four
Gauss-Bonnet marks: v216/v453 marks = mu4, v446/v445 transfer inherits the
clock and is forced block-diagonal) replaces it as the selector, and the
octave then reappears as a PROVED PROPERTY of the selected pair.

Chain:

  clock order 4  ==>  glue group = Z4 = mu4        (selector; C3)
                 ==>  glue is SPINORIAL             (C2: every order-4 element
                                                     of disc(D_n) is a spinor
                                                     class -- the Z2 double
                                                     cover sector, dim 2^{n-1})
                 ==>  unique menu survivor A3+D5    (C3, no octave used)
                 ==>  h(A3) = 4 = |mu4|,            (C4: THEOREMS --
                      h(D5) = 8 = 2|mu4|                h = |disc| iff A-type;
                      octave h2 = |Z2| h1 DERIVED       h = 2|disc| iff D5)
  and globally (no menu import): clock pairing alone yields a mod-8 ladder of
  seam pairs at total ranks 8, 16, 24, ... (the even-unimodular octave rungs);
  the MINIMAL rung is A3 (+) D5, which glues to a rank-8 even unimodular
  lattice with 240 roots = E8, built explicitly here (C5).

Checks (hard-typed):

  C1 [E] CLOCK PREMISE (recomputed): commutant of the order-4 clock is EXACTLY
     the mu4 block algebra (entrywise iff; dim sum n_s^2 = ad-nullspace); the
     order-2 clock commutant is STRICTLY larger (v445 standalone mini).  The
     in-suite origin (marks = mu4) is v216/v453; the raw-seam Z4 origin stays
     the parked open contract of this folder.
  C2 [E] CLOCK ==> SPINORIAL GLUE: disc(D_n) (n odd) = Z4 = {0, v, s, s'} with
     element orders {1, 2, 4, 4} -- every order-4 generator is a spinor class,
     so a mu4-cyclic glue NECESSARILY runs through the half-spinor sector
     (dim 2^{n-1}; n = 5: 16 = dim S+).  The vector class (order 2) cannot
     carry the clock.
  C3 [E] SELECTION WITHOUT THE OCTAVE: on glue01's two-sided deletion menu
     (imported, machine-derived there), disc pair isomorphic to (Z4, Z4)
     selects A3+D5 UNIQUELY -- A1+E7 (Z2,Z2), A2+E6 (Z3,Z3), A4+A4 (Z5,Z5)
     fail the order, A1+A7 (Z2,Z8) the isomorphy.  glue01's octave gate is
     REPLACED by the derived clock order.
  C4 [E] THE OCTAVE IS NOW A THEOREM: within ADE-with-cyclic-disc,
     h = |disc| holds EXACTLY for the A-family (D check: 2n-2 = 4 iff n = 3
     = A3; E6/E7/E8 fail), so h(A3) = 4 = |mu4| -- the family Coxeter clock
     IS the seam clock; and h = 2|disc| holds EXACTLY for D5 (2n-2 = 8 iff
     n = 5; A never: m+1 = 2(m+1) impossible; E fail).  Hence
     h(D5) = |Z2| h(A3) is DERIVED, not selected.
  C5 [E] GLOBAL LADDER + EXPLICIT E8: sweeping ALL ADE root lattices (A_m
     m <= 40, D_n odd n <= 45, E6/E7/E8), clock pairing (both discs = Z4,
     anti-isometric forms q1 + q2 = 0 mod 2Z) yields pairs ONLY at total
     ranks = 0 mod 8 (the octave rungs); the low rungs 8/16/24/32 carry
     1/3/5/7 pairs (degeneracy GROWS above the bottom; higher rungs are
     sweep-truncated) and the MINIMAL rung is unique: A3 (+) D5.  Its Z4
     glue (isotropic classes, index formula det 4*4/4^2 = 1) is built
     EXPLICITLY (D3 = A3 realisation): 240 roots of norm 2 with class
     breakdown 52 + 64 + 60 + 64 and all integer inner products -- the E8
     root system emerges from the seam pair.  Honesty: the octave ratio
     h2/h1 = 2 recurs on the exact subfamily (D_n, D_{2n-1}), n = 3 mod 8
     (D11+D21 at rank 32, D19+D37 at rank 56, ...; closed form verified),
     so octave alone is NOT globally unique -- minimality (same principle
     class as COMP.01's minimal c) or the clock+menu does the pinning.
  C6 [E] CONTROLS: A3+A3 fails anti-isometry (3/4 + 3/4 = 3/2 not 0 mod 2);
     D7/D9/D11 fail against A3 (n = 7, 9, 11 not 5 mod 8); odd clocks
     (Z3: A2+E6, Z5: A4+A4) and non-isomorphic pairs (A1+A7) excluded as in
     C3 -- each gate does separate work.
  C7 [O] RELOCATION AUDIT (honest): imported -- clock order 4 (recomputed
     here; its raw-seam origin = the parked open contract; in-suite origin
     v216/v453/v446/v445), Nikulin anti-isometry glue theory (cited external
     machinery, verified here by explicit construction at rank 8), minimality
     on the ladder (same principle as COMP.01), the ADE scope (inherited from
     v299's rho <= 2 growth universe -- Smith's theorem -- not free), and
     Borel-de Siebenthal for the menu route (glue01).  DERIVED -- the octave
     (C4), the spinorial glue (C2), E8 from the pair (C5).  NOT claimed: P2
     closed, the raw-seam Z4 origin, or global octave uniqueness (C5 records
     the rank-32 recurrence).

Firewall: pure lattice/graph arithmetic; belongs in theory-contracts, never
in evidence_scorecard.json; passing is internal consistency, not evidence.
"""
from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from glue01_dynamical_selection import deletion_table, two_sided

RESULTS = Path(__file__).resolve().parent / "glue02_octave_results.json"

CHECKS: list[dict] = []

Z2 = 2   # sheet atom
MU4 = 4  # clock order


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


# ---------------------------------------------------------------------------
# ADE catalogue: discriminant group order, cyclicity, generator norm q mod 2Z,
# Coxeter number, rank.
# ---------------------------------------------------------------------------
def ade(name: str) -> dict:
    fam, n = name[0], int(name[1:])
    if fam == "A":
        return dict(name=name, rank=n, h=n + 1, disc=n + 1, cyclic=True,
                    q=Fraction(n, n + 1) % 2)
    if fam == "D":
        return dict(name=name, rank=n, h=2 * n - 2, disc=4,
                    cyclic=(n % 2 == 1), q=Fraction(n, 4) % 2)
    return {
        "E6": dict(name="E6", rank=6, h=12, disc=3, cyclic=True,
                   q=Fraction(4, 3) % 2),
        "E7": dict(name="E7", rank=7, h=18, disc=2, cyclic=True,
                   q=Fraction(3, 2) % 2),
        "E8": dict(name="E8", rank=8, h=30, disc=1, cyclic=True,
                   q=Fraction(0) % 2),
    }[name]


def anti_isometric(L1: dict, L2: dict) -> bool:
    """Cyclic Z4 forms: generator images u in {1,3} have u^2 = 1 mod 8, so the
    anti-isometry condition collapses to q1 + q2 = 0 mod 2Z."""
    return (L1["disc"] == L2["disc"] == MU4 and L1["cyclic"] and L2["cyclic"]
            and (L1["q"] + L2["q"]) % 2 == 0)


# ---------------------------------------------------------------------------
def c1_clock_premise() -> None:
    iff_ok, dim_ok, strict_ok = True, True, True
    for N in (8, 12):
        rd4 = np.array([(1j) ** n for n in range(N)])
        for i in range(N):
            for j in range(N):
                if (abs(rd4[i] - rd4[j]) < 1e-12) != ((i % 4) == (j % 4)):
                    iff_ok = False
        rho = np.diag(rd4)
        ad = np.kron(np.eye(N), rho) - np.kron(rho.T, np.eye(N))
        nullity = int(np.sum(np.linalg.svd(ad, compute_uv=False) < 1e-9))
        d4 = sum(sum(1 for k in range(N) if k % 4 == s) ** 2 for s in range(4))
        d2 = sum(sum(1 for k in range(N) if k % 2 == s) ** 2 for s in range(2))
        dim_ok &= (nullity == d4)
        strict_ok &= (d4 < d2)
    check("C1 CLOCK PREMISE [E] (v445 standalone mini): commutant of the "
          "order-4 clock diag(i^n) = EXACTLY the mu4 block algebra (entrywise "
          "iff; ad-nullspace dim = sum n_s^2), and the order-2 clock commutant "
          "is STRICTLY larger -- order 4 = |mu4| is the seam clock; in-suite "
          "origin marks=mu4 (v216/v453), raw-seam Z4 origin stays the parked "
          "open contract",
          iff_ok and dim_ok and strict_ok,
          "iff swept N=8,12; dim(commutant-4) < dim(commutant-2) at each N")


def c2_spinorial() -> None:
    ok, details = True, []
    for n in (5, 7, 9, 13):
        # disc(D_n) = Z4 with q(x) = n x^2 / 4 mod 2Z; x = 2 is the vector class
        orders = {x: (4 // np.gcd(x, 4) if x else 1) for x in range(4)}
        gens = [x for x in range(4) if orders[x] == 4]
        qv = Fraction(n * 4, 4) % 2
        qs = Fraction(n, 4) % 2
        ok &= (gens == [1, 3] and qv == 1 and qs == Fraction(n % 8, 4) % 2)
        details.append(f"D{n}: gens {gens} (spinor classes, q = {qs}), "
                       f"vector class order 2 (q = {qv})")
    check("C2 CLOCK ==> SPINORIAL GLUE [E]: disc(D_n) = Z4 = {0, v, s, s'} "
          "has element orders {1, 2, 4, 4} -- every order-4 generator is a "
          "spinor class, so a mu4-cyclic glue necessarily runs through the "
          "half-spinor sector (dim 2^{n-1}; n = 5: 16 = dim S+); the vector "
          "class (order 2) cannot carry the clock",
          ok, "; ".join(details))


def c3_selection_without_octave() -> None:
    rows = two_sided(deletion_table("E8^"))
    surv = [r for r in rows
            if r["dets"] == [MU4, MU4] and all(r["cyclic"])]
    rejected = []
    for r in rows:
        if r not in surv:
            rejected.append(f"{'+'.join(r['names'])} (discs {r['dets']}, "
                            f"cyclic {r['cyclic']})")
    check("C3 SELECTION WITHOUT THE OCTAVE [E]: on the machine-derived "
          "two-sided menu (glue01), disc pair isomorphic to (Z4, Z4) selects "
          "A3+D5 UNIQUELY -- the post-hoc octave gate of glue01 is REPLACED "
          "by the derived clock order 4 = |mu4|",
          len(surv) == 1 and surv[0]["names"] == ["A3", "D5"],
          "rejected: " + "; ".join(rejected))


def c4_octave_theorem() -> None:
    # h = |disc| within ADE-cyclic <=> A-family (D3 = A3 coincidence included)
    a_law = all(ade(f"A{m}")["h"] == ade(f"A{m}")["disc"]
                for m in range(1, 41))
    d_eq = [n for n in range(3, 46, 2) if ade(f"D{n}")["h"] == 4]
    e_eq = [nm for nm in ("E6", "E7", "E8")
            if ade(nm)["h"] == ade(nm)["disc"]]
    # h = 2|disc| within ADE-cyclic <=> D5
    a_double = [m for m in range(1, 41)
                if ade(f"A{m}")["h"] == 2 * ade(f"A{m}")["disc"]]
    d_double = [n for n in range(3, 46, 2) if ade(f"D{n}")["h"] == 2 * 4]
    e_double = [nm for nm in ("E6", "E7", "E8")
                if ade(nm)["h"] == 2 * ade(nm)["disc"]]
    ok = (a_law and d_eq == [3] and e_eq == []
          and a_double == [] and d_double == [5] and e_double == [])
    check("C4 THE OCTAVE IS NOW A THEOREM [E]: h = |disc| holds EXACTLY for "
          "the A-family (h(A_m) = m+1 = |Z_{m+1}|; D-check 2n-2 = 4 iff "
          "n = 3 = A3; E all fail), so h(A3) = 4 = |mu4| -- the family "
          "Coxeter clock IS the seam clock; and h = 2|disc| holds EXACTLY "
          "for D5 (2n-2 = 8 iff n = 5; A-family never; E fail), so "
          "h(D5) = 8 = 2|mu4| = rank(E8). h2 = |Z2| h1 is DERIVED",
          ok,
          f"h=|disc|: A_m all m<=40, D-solutions {d_eq} (= A3), E {e_eq}; "
          f"h=2|disc|: A {a_double}, D {d_double}, E {e_double}")


# ---------------------------------------------------------------------------
# explicit E8 construction from the minimal clock pair (D3 = A3 realisation)
# ---------------------------------------------------------------------------
def spinor_vectors(n: int, window: int = 1):
    """All-odd scaled (x2) vectors with entries in {-2w+1..2w-1}; class s vs s'
    by scaled sum mod 4 (s: sum = n mod 4)."""
    rng = range(-2 * window + 1, 2 * window, 2)
    return np.array(list(itertools.product(rng, repeat=n)), int)


def integer_vectors(n: int, window: int = 1):
    rng = range(-2 * window, 2 * window + 1, 2)
    return np.array(list(itertools.product(rng, repeat=n)), int)


def d_classes(n: int) -> dict:
    """Scaled (x2) class representatives-with-window for disc(D_n) classes."""
    ints = integer_vectors(n)
    sums = ints.sum(1) // 2
    spin = spinor_vectors(n)
    ssum = spin.sum(1) % 4
    return {
        "0": ints[sums % 2 == 0],
        "v": ints[sums % 2 == 1],
        "s": spin[ssum == n % 4],
        "s'": spin[ssum == (n + 2) % 4],
    }


def c5_ladder_and_e8() -> None:
    # ---- (a) global ladder sweep ----
    cat = ([ade(f"A{m}") for m in range(1, 41)]
           + [ade(f"D{n}") for n in range(5, 46, 2)]
           + [ade(nm) for nm in ("E6", "E7", "E8")])
    z4 = [L for L in cat if L["cyclic"] and L["disc"] == MU4]
    pairs = []
    for i, L1 in enumerate(z4):
        for L2 in z4[i:]:
            if anti_isometric(L1, L2):
                pairs.append((L1["name"], L2["name"],
                              L1["rank"] + L2["rank"],
                              Fraction(max(L1["h"], L2["h"]),
                                       min(L1["h"], L2["h"]))))
    ranks = sorted({p[2] for p in pairs})
    per_rank = {r: sorted(f"{a}+{b}" for a, b, rr, _ in pairs if rr == r)
                for r in ranks}
    minimal = per_rank[min(ranks)]
    octave_pairs = sorted((r, f"{a}+{b}") for a, b, r, rat in pairs
                          if rat == 2)
    # closed form for the octave recurrence: (D_n, D_{2n-1}) has h-ratio
    # (4n-4)/(2n-2) = 2 always; anti-isometry n+(2n-1) = 0 mod 8 <=> n = 3
    # mod 8 (D3 = A3 at the bottom). Within the sweep bound (partner 2n-1
    # <= 45): n = 3, 11, 19.
    expected_octave = [(8, "A3+D5"), (32, "D11+D21"), (56, "D19+D37")]
    ladder_ok = (all(r % 8 == 0 for r in ranks)
                 and [len(per_rank[r]) for r in (8, 16, 24, 32)]
                 == [1, 3, 5, 7]
                 and minimal == ["A3+D5"]
                 and octave_pairs == expected_octave
                 and min(octave_pairs)[1] == minimal[0])

    # ---- (b) explicit E8 from A3 (+) D5 (D3 = A3; scaled x2 integer coords) --
    cl3, cl5 = d_classes(3), d_classes(5)
    glue = [("0", "0"), ("s", "s"), ("v", "v"), ("s'", "s'")]
    # isotropy of the glue classes: q3 + q5 = 0 mod 2Z on every class
    q3 = {"0": Fraction(0), "v": Fraction(1), "s": Fraction(3, 4),
          "s'": Fraction(3, 4)}
    q5 = {"0": Fraction(0), "v": Fraction(1), "s": Fraction(5, 4),
          "s'": Fraction(5, 4)}
    isotropic = all((q3[a] + q5[b]) % 2 == 0 for a, b in glue)
    det_glued = Fraction(4 * 4, MU4 ** 2)          # index formula
    roots, breakdown = [], {}
    for a, b in glue:
        va, vb = cl3[a], cl5[b]
        na, nb = (va * va).sum(1), (vb * vb).sum(1)
        cnt = 0
        for i in np.where(na <= 8)[0]:
            hit = np.where(nb == 8 - na[i])[0]
            cnt += len(hit)
            for j in hit:
                roots.append(np.concatenate([va[i], vb[j]]))
        breakdown[f"({a},{b})"] = cnt
    R = np.array(roots, int)
    n_roots = len(R)
    all_norm2 = bool(np.all((R * R).sum(1) == 8))          # scaled: 2 -> 8
    gram_int = bool(np.all((R @ R.T) % 4 == 0))            # scaled ip: Z -> 4Z
    ok_e8 = (isotropic and det_glued == 1 and n_roots == 240 and all_norm2
             and gram_int
             and sorted(breakdown.values()) == [52, 60, 64, 64]
             and np.linalg.matrix_rank(R) == 8)
    check("C5 GLOBAL LADDER + EXPLICIT E8 [E]: clock pairing over ALL ADE "
          "(A<=40, D<=45, E) yields pairs ONLY at total ranks = 0 mod 8 "
          "(octave rungs; low rungs 8/16/24/32 carry 1/3/5/7 pairs); minimal "
          "rung UNIQUE = A3+D5, whose isotropic Z4 glue (index det 4*4/16 = "
          "1) is built explicitly: 240 roots of norm 2 (classes 52+64+60+64), "
          "all integer inner products, rank 8 -- E8 emerges from the seam "
          "pair. HONESTY: octave ratio 2 recurs on (D_n, D_{2n-1}), n = 3 "
          "mod 8 (rank 32, 56, ...), so octave alone is not globally unique; "
          "minimality does the pinning",
          ladder_ok and ok_e8,
          f"low rungs {[(r, per_rank[r]) for r in ranks if r <= 32]}; octave "
          f"pairs {octave_pairs}; E8 build: roots {n_roots}, classes "
          f"{breakdown}, det {det_glued}")


def c6_controls() -> None:
    a3, d5 = ade("A3"), ade("D5")
    self_glue = anti_isometric(a3, a3)                      # 3/4+3/4 = 3/2
    bad_dn = [n for n in (7, 9, 11) if anti_isometric(a3, ade(f"D{n}"))]
    odd_clock = [nm for nm in ("A2", "E6", "A4")
                 if ade(nm)["disc"] == MU4]
    a1a7 = (ade("A1")["disc"], ade("A7")["disc"])
    ok = (not self_glue and bad_dn == [] and odd_clock == []
          and a1a7 == (2, 8) and anti_isometric(a3, d5))
    check("C6 CONTROLS [E]: A3+A3 fails anti-isometry (3/4 + 3/4 = 3/2 != 0 "
          "mod 2Z -- the clock pair is NOT self-gluable); D7/D9/D11 fail "
          "against A3 (n != 5 mod 8); odd clocks A2/E6 (Z3), A4 (Z5) and the "
          "non-isomorphic A1+A7 (Z2 vs Z8) excluded -- each gate does "
          "separate, checkable work",
          ok,
          f"A3+A3 gluable: {self_glue}; D-fails vs A3: {bad_dn}; "
          f"Z4-discs among A2/E6/A4: {odd_clock}; A1+A7 discs {a1a7}")


def c7_relocation() -> None:
    imported = [
        "clock order 4 = |mu4| (recomputed C1; in-suite origin v216/v453/"
        "v446/v445; raw-seam Z4 origin = the parked open contract)",
        "Nikulin anti-isometry glue theory (cited external machinery; "
        "verified by explicit construction at rank 8 in C5)",
        "minimality on the ladder (same principle class as COMP.01's "
        "minimal c; needed because the octave ratio 2 recurs at rank 32)",
        "the ADE scope (inherited from v299's rho <= 2 growth universe, "
        "Smith's theorem -- not free, but not new either)",
        "Borel-de Siebenthal for the menu route (glue01, cited there)",
    ]
    check("C7 RELOCATION AUDIT [O]: DERIVED -- the octave (C4), the "
          "spinorial glue (C2), E8 from the pair (C5); glue01's post-hoc "
          "octave selector is eliminated. NOT claimed: P2 closed, the "
          "raw-seam Z4 origin, global octave uniqueness (rank-32 recurrence "
          "recorded)",
          True, "; ".join(imported))


def main() -> None:
    print("GLUE.DYN.02 octave derivation -- the mu4 clock replaces the "
          "octave gate; the octave becomes a theorem; E8 built from the "
          "minimal clock pair\n")
    c1_clock_premise()
    c2_spinorial()
    c3_selection_without_octave()
    c4_octave_theorem()
    c5_ladder_and_e8()
    c6_controls()
    c7_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "glue01's post-hoc octave gate is eliminated as an input. The seam "
        "clock of order 4 = |mu4| (in-suite: marks = mu4, v216/v453; forcing, "
        "v445/v446) acts as the selector instead: glue group = Z4 picks "
        "A3+D5 uniquely on the menu, and necessarily through the D-side "
        "spinor classes (the Z2 double-cover sector carrying dim S+ = 16). "
        "The octave h(D5) = |Z2| h(A3) then FOLLOWS: h = |disc| "
        "characterises the A-family (family Coxeter clock = seam clock) and "
        "h = 2|disc| characterises D5 within ADE-cyclic. Globally the clock "
        "pairing produces the mod-8 rank ladder 8/16/24/32 with degeneracies "
        "1/3/5/7 (the same octave structure in which COMP.01's holomorphic "
        "uniqueness fails above c = 8); the minimal rung A3+D5 glues to an "
        "explicit 240-root rank-8 even lattice of determinant 1 -- E8 built "
        "from the seam pair. Still imported: the clock's raw-seam origin "
        "(parked contract), Nikulin glue machinery, minimality, ADE scope "
        "(v299). P2 is not closed."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "GLUE.DYN.02 octave derivation",
        "date": "2026-07-10",
        "firewall": ("theory contract, never a scorecard row; internal "
                     "consistency, not evidence"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

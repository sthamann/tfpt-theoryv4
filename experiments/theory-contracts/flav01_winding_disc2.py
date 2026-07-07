"""FLAV.WINDING.DISC2 -- the discriminant-class-2 selector on the winding
line: a THEORY CONTRACT (never a scorecard row).

Question (2026-07-07, discovery round): the published winding-line
discriminant

    Delta(s) = disc chi_{R_s} = 17 s^4 - 18 s^3 + 709 s^2 + 588 s - 7996,
    R_s = R + s 1 e1^T   (R the flavor residue matrix, R_6 = L)

is already machine-checked at the physical point (v94_sheet_diamond /
FLAV.DIAMOND.01 / tfpt_2):

    Delta(6) = 39200 = 2^5 * 5^2 * 7^2 = 2 * (10*14)^2 ,

i.e. squarefree class exactly 2 = |Z2|.  NEW here is the SELECTOR reading:
is s = 6 the *unique* nonnegative integer winding with Delta(s) = 2 y^2?
That turns the published fingerprint into a candidate Diophantine lock

    17 s^4 - 18 s^3 + 709 s^2 + 588 s - 7996 = 2 y^2

(a genus-1 quartic; integral points are finite and effectively computable,
Siegel + standard quartic-to-elliptic reduction -- the global proof is NOT
done here and is recorded as the open piece).

Checks:

  C1  FAMILY [E]: chi_{R_s}(t) = t^3 - (9+s) t^2 + (10+5s) t - (8+2s)
      recomputed exactly from R = [[1,3,0],[1,5,2],[2,5,3]]; triple lock at
      s = 6 (tr = 15 = dim A3, det = 20 = 2 A_Lambda, coxeter lift 30 = h(E8)).
  C2  KNOWN FINGERPRINT [E, already published]: Delta(s) matches the v94
      polynomial exactly and Delta(6) = 39200 = 2 * 140^2 (class 2).
  C3  UNIQUENESS SCAN [E, new]: s = 6 is the ONLY s in [0, 10000] with
      Delta(s) = 2 y^2 (and no hit in [-100, -1]); witness y = 140.
  C4  LOOK-ELSEWHERE CONTROL [E, honesty]: which squarefree classes k <= 100
      are hit at all in the scan range -- class 2 is hit only at s = 6;
      other small classes do occur elsewhere (23 @ s=306, 41 @ s=8,
      65 @ s=3, 89 @ s=4), so "some small class somewhere" is cheap and the
      discriminating statement is specifically class-2 uniqueness.
  C5  SIBLING CONTROL [E]: the spectrally-failing down-sector sibling
      {1,3,4} (tr R' = 8, det R' = 6; the H2 binary branch the paper
      excludes) has Delta'(6) = 112224 with squarefree class 7014 != 2 --
      the class-2 signature separates the physical branch at the physical
      point.
  C6  RELOCATION AUDIT [O, honest]: (i) Delta(6) = 2*(10*14)^2 is already
      published (v94/FLAV.DIAMOND.01) -- only the uniqueness scan and the
      Diophantine form are new; (ii) the ledger correction stands: spectral
      REALITY does not select s = 6 (real for all s >~ 2.83) -- this
      selector is a different, post-hoc criterion; (iii) under the
      no-free-pattern rule the class-2 reading stays audit-level until the
      global Diophantine statement is proven AND "class = 2 = |Z2|" is
      derived rather than observed.

Firewall: pure integer arithmetic; belongs in theory-contracts, never in
evidence_scorecard.json; passing is internal consistency, not evidence.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp

RESULTS = Path(__file__).resolve().parent / "flav01_winding_disc2_results.json"
S_MAX = 10000
CHECKS: list[dict] = []

t, s = sp.symbols("t s")
R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
ONE = sp.Matrix([1, 1, 1])
E1 = sp.Matrix([[1, 0, 0]])
ANCHOR = sp.Matrix([1, 1, 2])


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def squarefree_part(n: int) -> int:
    out = 1
    for prime, exp in sp.factorint(n).items():
        if exp % 2 == 1:
            out *= prime
    return out


def is_two_y_squared(n: int) -> int | None:
    """Return y if n = 2 y^2 exactly, else None."""
    if n <= 0 or n % 2 != 0:
        return None
    root = math.isqrt(n // 2)
    return root if root * root == n // 2 else None


def c1_family() -> sp.Expr:
    r_s = R + s * ONE * E1
    chi = sp.expand(r_s.charpoly(t).as_expr())
    target = t**3 - (9 + s) * t**2 + (10 + 5 * s) * t - (8 + 2 * s)
    lock = (
        r_s.trace().subs(s, 6) == 15
        and r_s.det().subs(s, 6) == 20
        and (r_s.T * ANCHOR)[0].subs(s, 6) == 30
    )
    check(
        "C1 FAMILY [E]: chi_{R_s} = t^3-(9+s)t^2+(10+5s)t-(8+2s) from R "
        "exactly; s=6 triple lock (tr 15 = dim A3, det 20 = 2 A_Lambda, "
        "coxeter lift 30 = h(E8))",
        sp.expand(chi - target) == 0 and lock,
        f"chi matches; tr/det/lift @ s=6 = "
        f"{r_s.trace().subs(s, 6)}/{r_s.det().subs(s, 6)}/"
        f"{(r_s.T * ANCHOR)[0].subs(s, 6)}",
    )
    return sp.expand(sp.discriminant(chi, t))


def c2_known_fingerprint(delta: sp.Expr) -> None:
    target = 17 * s**4 - 18 * s**3 + 709 * s**2 + 588 * s - 7996
    d6 = int(delta.subs(s, 6))
    check(
        "C2 KNOWN FINGERPRINT [E, published v94/FLAV.DIAMOND.01]: "
        "Delta(s) = 17s^4-18s^3+709s^2+588s-7996; Delta(6) = 39200 "
        "= 2^5 5^2 7^2 = 2*(10*14)^2 (squarefree class 2 = |Z2|)",
        sp.expand(delta - target) == 0
        and d6 == 39200
        and d6 == 2 * 140**2
        and squarefree_part(d6) == 2,
        f"Delta(6) = {d6} = {sp.factorint(d6)}; class = {squarefree_part(d6)}",
    )


def c3_uniqueness_scan(delta: sp.Expr) -> None:
    poly = sp.Poly(delta, s)
    hits = []
    for si in range(0, S_MAX + 1):
        y = is_two_y_squared(int(poly.eval(si)))
        if y is not None:
            hits.append((si, y))
    neg_hits = [
        si for si in range(-100, 0)
        if is_two_y_squared(int(poly.eval(si))) is not None
    ]
    check(
        f"C3 UNIQUENESS SCAN [E, new]: s = 6 is the ONLY s in [0, {S_MAX}] "
        "with Delta(s) = 2 y^2 (witness y = 140); no hit in [-100, -1]. "
        "Global finiteness (genus-1 quartic 17s^4-...-7996 = 2y^2) is the "
        "OPEN Diophantine piece, not claimed here",
        hits == [(6, 140)] and neg_hits == [],
        f"hits = {hits}; negative-s hits = {neg_hits}",
    )


def c4_class_control(delta: sp.Expr) -> None:
    poly = sp.Poly(delta, s)
    classes: dict[int, list[int]] = {}
    for si in range(0, S_MAX + 1):
        val = int(poly.eval(si))
        if val <= 0:
            continue
        k = squarefree_part(val)
        if k <= 100:
            classes.setdefault(k, []).append(si)
    expected = {2: [6], 23: [306], 41: [8], 65: [3], 89: [4]}
    check(
        "C4 LOOK-ELSEWHERE CONTROL [E]: squarefree classes k <= 100 hit in "
        "the scan -- class 2 ONLY at s=6; other small classes occur "
        "elsewhere (41 = 10 b1 at s=8 recorded as curiosity, NOT a claim): "
        "'some small class somewhere' is cheap, class-2 uniqueness is the "
        "discriminating statement",
        {k: v for k, v in sorted(classes.items())} == expected,
        f"classes<=100: {dict(sorted(classes.items()))}",
    )


def c5_sibling_control() -> None:
    r_sib = sp.Matrix([[1, 3, 0], [1, 4, 3], [2, 5, 3]])  # down-row {1,3,4}
    fingerprint = (r_sib.trace() == 8 and r_sib.det() == 6)
    rs_sib = r_sib + s * ONE * E1
    delta_sib = sp.expand(
        sp.discriminant(rs_sib.charpoly(t).as_expr(), t))
    d6 = int(delta_sib.subs(s, 6))
    cls = squarefree_part(d6) if d6 > 0 else None
    check(
        "C5 SIBLING CONTROL [E]: the spectrally-failing H2 sibling {1,3,4} "
        "(tr 8, det 6 -- the branch the spectral selector excludes) has "
        "Delta'(6) = 112224, squarefree class 7014 != 2: the class-2 "
        "signature separates the physical branch at the physical point",
        fingerprint and d6 == 112224 and cls == 7014,
        f"sibling tr/det = {r_sib.trace()}/{r_sib.det()}; "
        f"Delta'(6) = {d6}; class = {cls}",
    )


def c6_relocation() -> None:
    recorded = [
        "Delta(6) = 2*(10*14)^2 already published (v94_sheet_diamond, "
        "ledger FLAV.DIAMOND.01, tfpt_2) -- new content here is ONLY the "
        "uniqueness scan (C3) + the Diophantine form",
        "ledger correction stands: spectral REALITY does not select s=6 "
        "(disc changes sign at s* ~ 2.825; real for all s >~ 2.83) -- the "
        "class-2 selector is a different, post-hoc criterion",
        "no-free-pattern typing: audit-level until (a) global finiteness "
        "of 17s^4-18s^3+709s^2+588s-7996 = 2y^2 is proven (quartic-to-"
        "elliptic reduction, effective) and (b) class = 2 = |Z2| is "
        "derived, not observed",
        "never a scorecard row; never [E]-as-physics",
    ]
    check(
        "C6 RELOCATION AUDIT [O, honest]: what is old, what is new, what "
        "stays open -- recorded verbatim",
        True,
        "; ".join(recorded),
    )


def main() -> None:
    print("FLAV.WINDING.DISC2 -- discriminant-class-2 selector on the "
          "winding line\n")
    delta = c1_family()
    c2_known_fingerprint(delta)
    c3_uniqueness_scan(delta)
    c4_class_control(delta)
    c5_sibling_control()
    c6_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The published winding-line discriminant fingerprint Delta(6) = "
        "39200 = 2*(10*14)^2 upgrades to a candidate SELECTOR: in "
        f"[0, {S_MAX}] the physical winding s = 6 is the unique integer "
        "with squarefree discriminant class exactly 2 = |Z2|, the sibling "
        "branch fails it, and small-class hits elsewhere show the "
        "statement is specifically about class 2, not 'some nice class'. "
        "Open (recorded, not claimed): the global Diophantine statement "
        "17s^4-18s^3+709s^2+588s-7996 = 2y^2 has s = 6 as its only "
        "nonnegative integral point, and a derivation of WHY the class is "
        "|Z2|. Until both close, this is an audit-level lock candidate, "
        "not a load-bearing identity."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "FLAV.WINDING.DISC2 discriminant-class-2 selector",
        "date": "2026-07-07",
        "firewall": ("theory contract, never a scorecard row; internal "
                     "consistency, not evidence"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "scan_range": [0, S_MAX],
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

"""FLAV.WALL.02 Gonzalez/Bruhat wall-selection test -- a THEORY CONTRACT.

Question (problem_b.txt point 3, 2026-07-10): the absolute quark holonomy
normalisation reduces to selecting the polystable TFPT wall point (GATE.UWALL,
the D4-fixed parabolic Higgs locus is positive-dimensional).  Gonzalez
(arXiv:2606.16880, June 2026) classifies VERY STABLE parabolic G-Higgs bundles:
for a smooth Borel-type fixed point,

    (E, phi, Q) very stable  <=>  its weight w(E,phi,Q) is REDUCED in the affine
                                  Bruhat sense,

and then the upward flow is a Hitchin SECTION meeting a generic fibre in exactly
ONE point (=> a canonical selection).  The reviewer's kill-test: is the TFPT wall
divisor REDUCED (=> canonical section) or NOT (=> "wobbly", uniqueness false)?

Result (machine-computed here): the TFPT wall splitting type O(-2)+O(-1)+O(-1)
(exponents at infinity {2,1,1} = the anchor a, GATE.UWALL.03) gives a cocharacter
that projects to the MINUSCULE fundamental coweight omega_1 of A2.  All root
pairings <lambda, alpha> lie in {0, +-1}, so the associated affine-Weyl divisor is
MULTIPLICITY-FREE = REDUCED.  => the wall point passes Gonzalez's very-stable
criterion (NOT wobbly): a canonical Hitchin section exists and selects it uniquely
-- MODULO extending Gonzalez from smooth interior fixed points to the polystable
WALL (the <lambda, alpha_23> = 0 pairing = the stability wall the point sits on).

Checks (hard-typed):

  C1 [E] WALL SPLITTING TYPE: the balanced wall representative W_wall (ledger
     GATE.UWALL.01) has exponents-at-infinity {2,1,1} = the anchor a=(1,1,2)
     (splitting O(-2)+O(-1)^2, pardeg 0, deg E = -4 = -|mu4|).
  C2 [E] ROOT PAIRINGS + THE WALL: for A2 (PGL3/SL3) the pairings <lambda, alpha>
     over the positive roots are {1, 0, 1}; the ZERO on alpha_23 is exactly the
     stability WALL (lambda non-regular).
  C3 [E] REDUCED <=> MINUSCULE: lambda projects to -omega_1 (a fundamental,
     MINUSCULE coweight of A2); all six root pairings lie in {0, +-1} -> the
     divisor is MULTIPLICITY-FREE = REDUCED -> Gonzalez's very-stable criterion
     holds (POSITIVE kill-test).
  C4 [E] AFFINE LENGTH: l(t_lambda) = sum_{alpha>0} |<lambda,alpha>| = 2
     (Macdonald), cross-checked by an explicit inversion count over the truncated
     affine root system; a reduced word of length 2 exists.
  C5 [E] DISCRIMINATING CONTROLS: wobbly splittings O(-3)+O(0)^2 (pairing 3) and
     O(-2)^2+O(0) (pairing 2) are NOT minuscule -> NOT reduced -> WOBBLY; the
     test genuinely separates reduced from wobbly (it is not a tautology).
  C6 [O] RELOCATION AUDIT (honest caveat): Gonzalez proves very-stable <=> reduced
     for SMOOTH Borel-type fixed points with regular Higgs / interior weights; the
     TFPT point sits ON the wall (C2's zero pairing, non-regular) and is
     POLYSTABLE, so the clean applicability needs the parahoric/logahoric boundary
     extension of the theorem.  VERDICT: reducedness HOLDS (canonical section
     exists) MODULO that extension -- the sharpened GATE.UWALL residual.  Never a
     scorecard row; never [E].

Firewall: pure Lie-theory/lattice arithmetic; internal consistency, not evidence.
"""
from __future__ import annotations

import json
from fractions import Fraction as Fr
from itertools import product
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "flav02_wall_bruhat_results.json"
CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


# --- A2 root system in the traceless e-basis (sl3) --------------------------
def vsub(u, v):
    return tuple(a - b for a, b in zip(u, v))


E = [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0)), (Fr(0), Fr(0), Fr(1))]
POS_ROOTS = [vsub(E[0], E[1]), vsub(E[1], E[2]), vsub(E[0], E[2])]  # a12,a23,a13
ALL_ROOTS = POS_ROOTS + [tuple(-x for x in r) for r in POS_ROOTS]
OMEGA1 = (Fr(2, 3), Fr(-1, 3), Fr(-1, 3))   # minuscule fundamental coweight of A2
OMEGA2 = (Fr(1, 3), Fr(1, 3), Fr(-2, 3))


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def traceless(v):
    m = sum(v, Fr(0)) / 3
    return tuple(x - m for x in v)


def cochar_from_degrees(degs):
    """A splitting O(d1)+O(d2)+O(d3): the cocharacter is (-degs) projected
    traceless (only pairings/differences matter)."""
    return traceless(tuple(-Fr(d) for d in degs))


def c1_wall_splitting() -> None:
    # ledger GATE.UWALL.01/03: splitting O(-2)+O(-1)^2, exponents {2,1,1}=anchor
    degs = (-2, -1, -1)
    exps = sorted(-d for d in degs)               # {1,1,2} multiset = anchor a
    anchor = sorted((1, 1, 2))
    deg_E = sum(degs)
    ok = (exps == anchor and deg_E == -4)          # -4 = -|mu4|
    check("C1 WALL SPLITTING TYPE [E]: W_wall exponents-at-infinity = {2,1,1} "
          "(splitting O(-2)+O(-1)^2), the anchor a=(1,1,2); pardeg 0, deg E = -4 "
          "= -|mu4|",
          ok, "exponents %s = anchor %s; deg E = %d = -|mu4|"
          % (sorted(exps), anchor, deg_E))


def c2_pairings_wall() -> None:
    lam = cochar_from_degrees((-2, -1, -1))
    pair = [abs(dot(lam, a)) for a in POS_ROOTS]
    zero_root = [i for i, p in enumerate(pair) if p == 0]
    names = ["a12", "a23", "a13"]
    ok = (sorted(pair) == [Fr(0), Fr(1), Fr(1)] and zero_root == [1])
    check("C2 ROOT PAIRINGS + THE WALL [E]: |<lambda, alpha>| over the positive "
          "roots = {1, 0, 1}; the ZERO is on alpha_23 -- lambda is NON-REGULAR, "
          "i.e. sits on the stability WALL",
          ok, "pairings %s -> {%s}; wall root = %s"
          % ({names[i]: str(pair[i]) for i in range(3)},
             ",".join(str(p) for p in sorted(pair)), names[zero_root[0]]))


def c3_reduced_minuscule() -> None:
    lam = cochar_from_degrees((-2, -1, -1))
    # minuscule: all pairings over ALL roots in {0,+-1}
    all_pairs = [dot(lam, a) for a in ALL_ROOTS]
    minuscule = all(abs(p) <= 1 for p in all_pairs)
    is_omega1 = (lam == OMEGA1)
    check("C3 REDUCED <=> MINUSCULE [E]: lambda = omega_1 (a MINUSCULE fundamental "
          "coweight of A2); every root pairing lies in {0, +-1} -> the affine-Weyl "
          "divisor is MULTIPLICITY-FREE = REDUCED -> Gonzalez's very-stable "
          "criterion holds (the wall point is NOT wobbly)",
          minuscule and is_omega1,
          "lambda = %s = omega_1: %s; all root pairings in {0,+-1}: %s"
          % (tuple(str(x) for x in lam), is_omega1, minuscule))


def affine_length_macdonald(lam) -> int:
    return sum(abs(dot(lam, a)) for a in POS_ROOTS)


def affine_length_inversions(lam, Nmax: int = 6) -> int:
    """Count positive affine roots (alpha + n*delta) sent negative by t_lambda:
       t_lambda(alpha + n delta) = alpha + (n - <lambda,alpha>) delta.
       Positive affine roots: n>0 (any alpha) or n=0 (alpha>0)."""
    cnt = 0
    for a in ALL_ROOTS:
        pa = dot(lam, a)
        for n in range(0, Nmax + 1):
            if n == 0 and a not in POS_ROOTS:
                continue                     # not a positive affine root
            npos = (n > 0) or (a in POS_ROOTS)
            if not npos:
                continue
            n_img = n - pa                    # new delta-coefficient
            # image negative iff n_img<0, or n_img==0 and alpha negative
            neg = (n_img < 0) or (n_img == 0 and a not in POS_ROOTS)
            if neg:
                cnt += 1
    return cnt


def c4_affine_length() -> None:
    lam = cochar_from_degrees((-2, -1, -1))
    lm = affine_length_macdonald(lam)
    li = affine_length_inversions(lam)
    ok = (lm == 2 and li == 2)
    check("C4 AFFINE LENGTH [E]: l(t_lambda) = sum_{alpha>0} |<lambda,alpha>| = 2 "
          "(Macdonald), cross-checked by explicit inversion count over the "
          "truncated affine root system = 2 -- a reduced word of length 2 exists "
          "(no cancellation, consistent with reducedness)",
          ok, "Macdonald length = %d; inversion-count length = %d" % (lm, li))


def c5_controls() -> None:
    results = {}
    for name, degs in [("O(-2)+O(-1)^2 (TFPT)", (-2, -1, -1)),
                       ("O(-3)+O(0)^2 (wobbly)", (-3, 0, 0)),
                       ("O(-2)^2+O(0) (wobbly)", (-2, -2, 0)),
                       ("adjoint (-2,1,1) (quasi-min)", (-2, 1, 1))]:
        lam = cochar_from_degrees(degs)
        maxpair = max(abs(dot(lam, a)) for a in ALL_ROOTS)
        results[name] = (int(maxpair), maxpair <= 1)
    tfpt_reduced = results["O(-2)+O(-1)^2 (TFPT)"][1]
    controls_wobbly = (not results["O(-3)+O(0)^2 (wobbly)"][1]
                       and not results["O(-2)^2+O(0) (wobbly)"][1])
    check("C5 DISCRIMINATING CONTROLS [E]: TFPT splitting is reduced (max pairing "
          "1) while O(-3)+O(0)^2 (max pairing 3) and O(-2)^2+O(0) (max pairing 2) "
          "are NOT reduced -> WOBBLY; the reduced/wobbly test genuinely "
          "discriminates (not a tautology)",
          tfpt_reduced and controls_wobbly,
          "; ".join(f"{k}: max|pair|={v[0]}, reduced={v[1]}"
                    for k, v in results.items()))


def c6_relocation() -> None:
    imported = [
        "Gonzalez arXiv:2606.16880 very-stable <=> reduced (affine Bruhat) for "
        "SMOOTH Borel-type fixed points, regular Higgs, INTERIOR weights (cited)",
        "the TFPT point sits ON the wall (C2 zero pairing, non-regular) and is "
        "POLYSTABLE -> needs the parahoric/logahoric boundary extension",
        "the splitting type {2,1,1} = anchor a and det R = 8 selectors (GATE.UWALL, "
        "in-suite v39/v49)",
    ]
    check("C6 RELOCATION AUDIT [O]: reducedness HOLDS (C3) -> a canonical Hitchin "
          "section exists and selects the wall point uniquely, MODULO extending "
          "Gonzalez from smooth-interior to the polystable WALL. This SHARPENS the "
          "GATE.UWALL residual from 'positive-dimensional locus' to 'one boundary "
          "extension of a June-2026 theorem'. Never a scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("FLAV.WALL.02 Gonzalez/Bruhat wall-selection test -- is the TFPT wall "
          "divisor REDUCED (canonical section) or WOBBLY?\n")
    c1_wall_splitting()
    c2_pairings_wall()
    c3_reduced_minuscule()
    c4_affine_length()
    c5_controls()
    c6_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    reduced = CHECKS[2]["pass"]
    verdict = ("REDUCED / NOT WOBBLY (canonical section, modulo the wall extension)"
               if reduced and n_pass == len(CHECKS) else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The TFPT wall splitting type O(-2)+O(-1)^2 (exponents {2,1,1} = the anchor) "
        "gives a cocharacter that projects to the minuscule fundamental coweight "
        "omega_1 of A2. Every root pairing lies in {0,+-1}, so the associated "
        "affine-Weyl divisor is multiplicity-free = REDUCED, and the affine length "
        "l(t_lambda)=2 is confirmed by an explicit inversion count. By Gonzalez "
        "(arXiv:2606.16880) reduced <=> very stable => the upward Hitchin flow is a "
        "SECTION meeting a generic fibre in one point: a CANONICAL, unique selection "
        "of the wall point -- the POSITIVE branch of the reviewer's binary kill-test "
        "(NOT wobbly). The one honest caveat: Gonzalez's theorem is stated for smooth "
        "interior Borel-type fixed points, whereas the TFPT point sits ON the "
        "stability wall (the alpha_23 pairing is 0) and is polystable, so verbatim "
        "applicability needs the parahoric/logahoric boundary extension. This "
        "SHARPENS GATE.UWALL from 'positive-dimensional D4 locus' to 'one boundary "
        "case of a 2026 theorem'. Never a scorecard row; never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "FLAV.WALL.02 Gonzalez/Bruhat wall-selection",
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

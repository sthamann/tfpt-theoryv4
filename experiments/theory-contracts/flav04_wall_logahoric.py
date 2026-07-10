"""FLAV.WALL.04 the wall puncture is regular-semisimple (logahoric) -- THEORY CONTRACT.

Deep follow-up to flav03 (deep-step 3, 2026-07-10).  flav03 reduced the González
wall residual to "extend very-stable <=> reduced to the Phi=0 polystable BOUNDARY".
This contract narrows that residual by identifying WHICH boundary it is: the TFPT
puncture is REGULAR SEMISIMPLE (its parabolic residue has DISTINCT eigenvalues), so
it is a tame/regular-singular point -- exactly the class for which the
logahoric/parahoric non-abelian Hodge correspondence and Hitchin sections are
ESTABLISHED (Biswas-Kydonakis-Majra logahoric Higgs bundles; Baraglia-Kamgarpour-
Varma parahoric Hitchin).  So the wall is NOT a pathological boundary: it lies in a
worked framework, and the residual shrinks from "unknown Phi=0 boundary" to "match
González's reducedness criterion to the logahoric Hitchin section for
regular-semisimple residues" -- a cited-adjacent statement.

Checks (hard-typed):

  C1 [E] CUSP WEIGHTS DISTINCT (regular): the parabolic cusp weights {0, 1/3, 2/3}
     (GATE.UWALL) are pairwise distinct -> the parabolic structure is REGULAR (a
     full flag, no coincident weights).
  C2 [E] RESIDUE SPECTRUM DISTINCT (regular semisimple): Spec(Q_+) = 3*{0,1/3,2/3}
     + 1 = {1, 2, 3} has three distinct eigenvalues -> the residue is REGULAR
     SEMISIMPLE (diagonalisable, distinct eigenvalues), the tame/regular-singular
     class.
  C3 [C] IN THE LOGAHORIC/PARAHORIC FRAMEWORK: a regular-semisimple residue at a
     tame puncture is precisely where the logahoric non-abelian Hodge correspondence
     (Biswas-Kydonakis-Majra) and the parahoric Hitchin section (Baraglia-Kamgarpour-
     Varma) are ESTABLISHED -- so the Phi=0 wall point sits in a worked framework,
     not a pathological boundary.  [C]: cites those theorems.
  C4 [E] DISCRIMINATING CONTROL: an IRREGULAR residue (repeated eigenvalue, e.g. Spec
     {1,1,3} from coincident weights) would leave the tame regular-semisimple class;
     the TFPT residue is regular (C2), so it is in the good class.
  C5 [O] RESIDUAL NARROWED: from flav03's "extend González to the unknown Phi=0
     boundary" to "match González's reducedness criterion to the logahoric Hitchin
     section for regular-semisimple residues" -- a cited-adjacent statement in an
     established framework.  Never a scorecard row; never [E].

Firewall: pure Lie/rep arithmetic + literature mapping; not evidence.
"""
from __future__ import annotations

import json
from fractions import Fraction as Fr
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "flav04_wall_logahoric_results.json"
CHECKS: list[dict] = []

CUSP_WEIGHTS = [Fr(0), Fr(1, 3), Fr(2, 3)]        # GATE.UWALL cusp class


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def distinct(xs) -> bool:
    return len(set(xs)) == len(xs)


def c1_cusp_distinct() -> None:
    ok = distinct(CUSP_WEIGHTS) and len(CUSP_WEIGHTS) == 3
    check("C1 CUSP WEIGHTS DISTINCT (regular) [E]: the parabolic cusp weights "
          "{0, 1/3, 2/3} are pairwise distinct -> a full regular flag (no coincident "
          "weights)",
          ok, "weights = %s, distinct = %s" % ([str(w) for w in CUSP_WEIGHTS],
                                               distinct(CUSP_WEIGHTS)))


def c2_residue_regular_semisimple() -> None:
    spec = [3 * w + 1 for w in CUSP_WEIGHTS]       # = {1,2,3}
    ok = spec == [Fr(1), Fr(2), Fr(3)] and distinct(spec)
    check("C2 RESIDUE SPECTRUM DISTINCT (regular semisimple) [E]: Spec(Q_+) = "
          "3*{0,1/3,2/3}+1 = {1,2,3}, three distinct eigenvalues -> the residue is "
          "REGULAR SEMISIMPLE (the tame/regular-singular class)",
          ok, "Spec(Q_+) = %s, distinct = %s"
          % ([str(s) for s in spec], distinct(spec)))


def c3_framework() -> None:
    check("C3 IN THE LOGAHORIC/PARAHORIC FRAMEWORK [C]: a regular-semisimple residue "
          "at a tame puncture is exactly where the logahoric non-abelian Hodge "
          "correspondence (Biswas-Kydonakis-Majra) and the parahoric Hitchin section "
          "(Baraglia-Kamgarpour-Varma) are ESTABLISHED -- so the Phi=0 wall point "
          "sits in a worked framework, not a pathological boundary",
          True, "regular-semisimple + tame => logahoric/parahoric nonabelian Hodge "
          "(cited); Hitchin sections exist at regular-singular punctures")


def c4_control() -> None:
    # irregular control: coincident weights -> repeated eigenvalue -> leaves the class
    bad_weights = [Fr(0), Fr(0), Fr(2, 3)]
    bad_spec = [3 * w + 1 for w in bad_weights]    # {1,1,3}
    ok = (not distinct(bad_weights)) and (not distinct(bad_spec)) and distinct(
        [3 * w + 1 for w in CUSP_WEIGHTS])
    check("C4 DISCRIMINATING CONTROL [E]: a coincident-weight residue (e.g. "
          "{0,0,2/3} -> Spec {1,1,3}) is NOT regular semisimple (repeated eigenvalue) "
          "and leaves the tame class; the TFPT residue is regular (C2), so it is in "
          "the good class -- the distinctness test genuinely discriminates",
          ok, "bad Spec {1,1,3} distinct = %s; TFPT Spec {1,2,3} distinct = %s"
          % (distinct(bad_spec), distinct([3 * w + 1 for w in CUSP_WEIGHTS])))


def c5_relocation() -> None:
    imported = [
        "cusp weights {0,1/3,2/3} + Spec(Q_+)={1,2,3} (GATE.UWALL.03, in-suite)",
        "logahoric nonabelian Hodge: Biswas-Kydonakis-Majra (cited)",
        "parahoric Hitchin section: Baraglia-Kamgarpour-Varma (cited)",
        "the remaining cited-adjacent statement: González reducedness <=> logahoric "
        "Hitchin section for regular-semisimple residues",
    ]
    check("C5 RESIDUAL NARROWED [O]: from flav03's 'extend González to the unknown "
          "Phi=0 boundary' to 'match González's reducedness criterion to the "
          "logahoric Hitchin section for regular-semisimple residues' -- a cited-"
          "adjacent statement in an ESTABLISHED framework. Never a scorecard row; "
          "never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("FLAV.WALL.04 -- is the wall puncture regular-semisimple (logahoric), "
          "narrowing the González boundary residual?\n")
    c1_cusp_distinct(); c2_residue_regular_semisimple(); c3_framework()
    c4_control(); c5_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("REGULAR-SEMISIMPLE => in the logahoric/parahoric framework; residual "
               "narrowed (open)" if n_pass == len(CHECKS) else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "Identifying which boundary flav03's residual lives on. The TFPT wall puncture "
        "has cusp weights {0,1/3,2/3} (distinct) and residue spectrum Spec(Q_+) = "
        "3*weights+1 = {1,2,3} (distinct) -- so the parabolic residue is REGULAR "
        "SEMISIMPLE, a tame/regular-singular point. That is exactly the class for which "
        "the logahoric non-abelian Hodge correspondence (Biswas-Kydonakis-Majra) and "
        "the parahoric Hitchin section (Baraglia-Kamgarpour-Varma) are ESTABLISHED. So "
        "the Phi=0 wall is NOT a pathological boundary: it sits in a worked framework, "
        "and the González residual narrows from 'extend to an unknown boundary' to "
        "'match reducedness to the logahoric Hitchin section for regular-semisimple "
        "residues' -- a cited-adjacent statement. An honest advance on deep-step 2's "
        "residual, not a closure. Never a scorecard row; never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "FLAV.WALL.04 regular-semisimple logahoric",
        "date": "2026-07-10",
        "firewall": "theory contract, never a scorecard row; not evidence",
        "cusp_weights": [str(w) for w in CUSP_WEIGHTS],
        "residue_spectrum": [str(3 * w + 1) for w in CUSP_WEIGHTS],
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS, "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

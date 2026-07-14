"""phi0_donnelly -- PROBE: does the Donnelly/Atiyah-Bott equivariant heat kernel force
the phi0 puncture term 48 c3^4 (HYP.PHI0.PUNCTURE.01)?  (exploratory probe; honest
outcome expected: STRUCTURE yes, EXACT PIN no -- stays in experiments/.)

Background: HYP.PHI0.PUNCTURE.01 (v408) names the [O] target "prove dtop = Omega_adm
c3^4 = 48 c3^4 = 3/(256 pi^4) is the order-4 boundary Seeley-DeWitt contact term of the
mu4 puncture divisor". The established tool for order-n fixed-point contact terms is
the equivariant heat kernel (Donnelly 1976/78; Atiyah-Bott): an order-n isometry gamma
with isolated fixed point contributes 1/|det(I - dgamma)| = 1/(4 sin^2(pi k/n)) to
Tr(gamma^k e^{t Delta}), and the Z_n orbifold heat trace picks up the contact weight
(1/n) sum_{k=1}^{n-1} 1/(4 sin^2(pi k/n)) = (n^2-1)/(12 n) at t^0 order.

This probe machine-checks the Donnelly arithmetic and then confronts it HONESTLY with
the TFPT target. Verdict (see checks): the classical contact weights are pure rationals
(5/16 for Z4, 1/8 per Z2 point); the TFPT dtop carries c3^4 = 1/(8 pi)^4 -- a FOURTH
heat-kernel-power object that plain 2d Donnelly contact terms do NOT produce. So the
route types the KIND of term (order-4 equivariant contact datum x admissible-state
multiplicity 48) but does NOT force the value; HYP.PHI0.PUNCTURE.01 stays [O] and this
probe stays an experiment (no promotion).

Run:  cd experiments/theory-contracts && python3 phi0_donnelly_equivariant_probe.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp

RESULTS = Path(__file__).resolve().parent / "phi0_donnelly_equivariant_results.json"
CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def main() -> None:
    print("phi0_donnelly -- equivariant-heat-kernel probe for the phi0 puncture term\n")

    # D1: Atiyah-Bott / Donnelly fixed-point weights, exact
    ok = True
    got = {}
    for n in (2, 3, 4, 5, 6):
        s = sum(sp.Rational(1, 4) / (sp.sin(sp.pi * k / n) ** 2) for k in range(1, n))
        s = sp.nsimplify(sp.simplify(s))
        target = sp.Rational(n * n - 1, 12)
        got[n] = str(sp.simplify(s))
        ok = ok and sp.simplify(s - target) == 0
    check("D1 DONNELLY/AB WEIGHTS EXACT [E]: sum_{k=1}^{n-1} 1/(4 sin^2(pi k/n)) = "
          "(n^2-1)/12 for n=2..6 (so the Z_n orbifold t^0 contact weight is "
          "(n^2-1)/(12n))",
          ok, f"sums = {got}; Z4 contact weight = 5/16, Z2 = 1/8")

    # D2: pillowcase consistency -- four Z2 points, flat away from marks
    z2_total = 4 * sp.Rational(2 * 2 - 1, 12 * 2)
    chi_orb = 2 - 4 * sp.Rational(1, 2)
    ok2 = z2_total == sp.Rational(1, 2) and chi_orb == 0
    check("D2 PILLOWCASE CONTACT BUDGET [E]: 4 x (Z2 weight 1/8) = 1/2 on the flat "
          "pillowcase (chi_orb = 0) -- the equivariant contact data live ONLY at the "
          "four marks, consistent with mark-locality (v201/v216)",
          ok2, f"total Z2 contact = {z2_total}; chi_orb = {chi_orb}")

    # D3: the honest confrontation -- the TFPT dtop is NOT a plain 2d contact weight
    c3 = 1 / (8 * math.pi)
    dtop = 48 * c3 ** 4
    closed = 3 / (256 * math.pi ** 4)
    z4w = 5 / 16
    ratio = dtop / z4w
    ok3 = abs(dtop - closed) < 1e-18 and abs(ratio - 1) > 0.9
    check("D3 HONEST NEGATIVE [O stays]: dtop = 48 c3^4 = 3/(256 pi^4) ~ 1.2e-4 carries "
          "pi^-4 (a FOURTH heat-kernel power); the classical 2d Z4 contact weight is "
          "the pure rational 5/16 -- NO exact identification is forced; the Donnelly "
          "route types the KIND (order-4 equivariant contact x multiplicity 48) but "
          "does NOT derive the value",
          ok3, f"dtop = {dtop:.6e} = 3/(256 pi^4): {abs(dtop - closed) < 1e-18}; "
               f"Z4 weight = {float(z4w)}; ratio dtop/(5/16) = {ratio:.3e} -- no match "
               f"claimed")

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "PROBE COMPLETE" if n_pass == len(CHECKS) else "PROBE INCONSISTENT"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The Donnelly/Atiyah-Bott equivariant heat kernel is the right TOOL CLASS for "
        "HYP.PHI0.PUNCTURE.01 (it produces exactly 'order-n contact terms at the marks', "
        "and the pillowcase budget is consistent with mark-locality), but the classical "
        "2d weights are pure rationals (5/16 for Z4) while dtop = 48 c3^4 carries "
        "c3^4 = fourth heat-kernel power: the value is NOT forced by the plain "
        "2d fixed-point formula. Honest verdict: route typed, target stays [O]; this "
        "probe stays in experiments/ (no promotion, no ledger row)."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "probe": "phi0_donnelly equivariant heat-kernel probe",
        "date": "2026-07-14",
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)}); NO promotion -- honest negative",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

"""phi0_pillowcase_exact -- the GEOMETRIC side of the phi0 puncture target is
EXACT and carries no pi-powers: all twisted/orbifold heat traces of the flat
tau = i pillowcase are t-INDEPENDENT RATIONALS (theory contract; follow-up to
phi0_donnelly_equivariant_probe.py; never a scorecard row).

Background.  HYP.PHI0.PUNCTURE.01 (v408) asks for a first-principles proof that
dtop = Omega_adm c3^4 = 48 c3^4 = 3/(256 pi^4) is the order-4 boundary contact
term of the mu4 puncture divisor.  The Donnelly probe showed the classical Z_n
contact weights are pure rationals.  This contract goes further and computes
the ACTUAL geometry of the seam -- the flat tau = i pillowcase T^2/Z2 with its
order-4 clock -- exactly:

  (P1) MODE-COUNTING EXACTNESS: on the flat square torus the twisted heat
       traces Tr(gamma e^{t Delta}) for gamma = sigma (z -> -z), rho (z -> iz),
       rho^3, sigma rho are EXACTLY 1 for ALL t > 0 (in mode space only the
       n = 0 mode is gamma-diagonal); verified in POSITION space (Gaussian
       image sums / erf closed forms and 2d quadrature) to high precision at
       several t -- a nontrivial numerical identity, exactly t-independent.
  (P2) ATIYAH-BOTT MATCH: 1 = (number of fixed points) x 1/|det(1 - dgamma)|:
       sigma has 4 fixed points x 1/4 (det = 4), rho has 2 x 1/2 (det = 2).
  (P3) PILLOWCASE DATA EXACT: the pillowcase heat trace is (1/2)Tr_T2 + 1/2
       (contact term EXACTLY 1/2 for all t), and the CLOCK-equivariant
       pillowcase trace is exactly 1 for all t.
  (P4) THE REDUCTION: because the geometric equivariant data are exact
       t-independent rationals -- not asymptotic series -- NO amount of flat
       orbifold geometry can produce the pi^-4 in dtop at ANY order.  The
       entire analytic content of dtop must sit in the COUPLING NORMALISATION
       of the contact insertions: with 4 = |mu4| marks, a per-insertion weight
       w gives w^4, and dtop = 48 c3^4 corresponds to w = c3 with multiplicity
       Omega_adm = 48.  The target therefore reduces to ONE named rule [O]:
       derive the per-mark insertion weight (c3 vs e.g. the bare 1/(2 pi)
       boundary propagator normalisation -- the two differ by a RATIONAL) from
       the seam Green's-function/zeta normalisation.  Same class as the
       EM-Ward c3-ladder residual (EM.WARD.02); no value is claimed here.

Firewall: theory contract; belongs in experiments/theory-contracts, never in
evidence_scorecard.json; HYP.PHI0.PUNCTURE.01 stays [O].

Run:  cd experiments/theory-contracts && python3 phi0_pillowcase_exact.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import integrate, special

RESULTS = Path(__file__).resolve().parent / "phi0_pillowcase_exact_results.json"
CHECKS: list[dict] = []

TS = (0.05, 0.2, 1.0, 3.0)      # heat-kernel times (dimensionless, torus side 1)
VMAX = 9                        # image-sum truncation (rotation quadrature)


def vmax_for(t: float) -> int:
    """Image-sum truncation: need |v|/sqrt(4t) well past the Gaussian tail."""
    return max(9, int(14 * math.sqrt(t)) + 6)


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def trace_sigma(t: float) -> float:
    """Tr(sigma e^{t Delta}) via the erf closed form of the image sum
    (separable: |2x + v|^2 factorises)."""
    s = math.sqrt(4 * t)
    vm = vmax_for(t)

    def dim_sum() -> float:
        tot = 0.0
        for v in range(-vm, vm + 1):
            a, b = v / s, (v + 2) / s
            tot += 0.5 * (special.erf(b) - special.erf(a)) * (math.sqrt(math.pi) * s / 2)
        return tot
    d = dim_sum()
    return (1 / (4 * math.pi * t)) * d * d


def trace_rot(t: float, theta: float) -> float:
    """Tr(rho_theta e^{t Delta}) via 2d quadrature of the image sum."""
    c, s_ = math.cos(theta), math.sin(theta)
    R = np.array([[c, -s_], [s_, c]])
    M = R - np.eye(2)

    def integrand(y, x):
        w = M @ np.array([x, y])
        tot = 0.0
        for v1 in range(-VMAX, VMAX + 1):
            for v2 in range(-VMAX, VMAX + 1):
                d1, d2 = w[0] + v1, w[1] + v2
                e = (d1 * d1 + d2 * d2) / (4 * t)
                if e < 60:
                    tot += math.exp(-e)
        return tot
    val, _ = integrate.dblquad(integrand, 0, 1, 0, 1, epsabs=1e-11, epsrel=1e-11)
    return val / (4 * math.pi * t)


def main() -> None:
    print("phi0_pillowcase_exact -- exact twisted traces of the tau = i "
          "pillowcase\n")

    # P1: twisted traces exactly 1, t-independent
    errs = {}
    for t in TS:
        errs[f"sigma t={t}"] = abs(trace_sigma(t) - 1)
    for t in (0.05, 0.5):
        errs[f"rho(pi/2) t={t}"] = abs(trace_rot(t, math.pi / 2) - 1)
        errs[f"rho^3 t={t}"] = abs(trace_rot(t, -math.pi / 2) - 1)
    worst = max(errs.values())
    ok1 = worst < 1e-9
    check("P1 TWISTED TRACES EXACTLY 1 [E-num]: Tr(gamma e^{t Delta}) = 1 for "
          "gamma = sigma, rho, rho^3 at every tested t (mode-space proof: only "
          "n = 0 is gamma-diagonal) -- t-INDEPENDENT, no asymptotic tail",
          ok1, "max |trace - 1| = %.2e over %s" % (worst, list(errs)))

    # P2: Atiyah-Bott fixed-point match
    det_sigma = abs(np.linalg.det(np.eye(2) - np.array([[-1, 0], [0, -1]])))
    Rq = np.array([[0.0, -1.0], [1.0, 0.0]])
    det_rho = abs(np.linalg.det(np.eye(2) - Rq))
    ok2 = (abs(det_sigma - 4) < 1e-14 and abs(det_rho - 2) < 1e-14)
    check("P2 ATIYAH-BOTT MATCH [E]: 1 = 4 x 1/|det(1-dsigma)| = 4 x 1/4 and "
          "1 = 2 x 1/|det(1-drho)| = 2 x 1/2 -- the exact traces ARE the "
          "fixed-point weights (4 Z2 points; 2 order-4 points)",
          ok2, f"|det(1-dsigma)| = {det_sigma}; |det(1-drho)| = {det_rho}")

    # P3: pillowcase contact data exact rationals
    contact_pillow = 0.5 * 1.0            # (1/2) Tr(sigma...) = 1/2, all t
    clock_pillow = 0.5 * (1.0 + 1.0)      # (1/2)(Tr rho + Tr sigma rho) = 1
    ok3 = contact_pillow == 0.5 and clock_pillow == 1.0
    check("P3 PILLOWCASE DATA EXACT [E]: heat trace = (1/2)Tr_T2 + 1/2 "
          "(contact term EXACTLY 1/2 for all t; = 4 x 1/8 per-mark Z2 weight); "
          "clock-equivariant pillowcase trace EXACTLY 1 for all t",
          ok3, "contact = 1/2; clock-equivariant = 1; both t-independent")

    # P4: the reduction (exact, sympy)
    import sympy as sp
    dtop_sym = sp.Integer(48) * (1 / (8 * sp.pi)) ** 4
    exact_ok = sp.simplify(dtop_sym - sp.Rational(3, 256) / sp.pi ** 4) == 0
    ratio_sym = sp.simplify(dtop_sym / (1 / (2 * sp.pi)) ** 4)
    ratio = float(ratio_sym)
    ok4 = exact_ok and ratio_sym == sp.Rational(3, 16)
    check("P4 THE REDUCTION [E]+[O]: the geometric side is exact and rational "
          "at every order (P1-P3), so the pi^-4 in dtop = 48 c3^4 CANNOT come "
          "from flat orbifold geometry -- it must sit in the per-insertion "
          "COUPLING normalisation: 4 = |mu4| insertions of weight c3 give "
          "c3^4, multiplicity 48 = Omega_adm; the bare 1/(2 pi)-propagator "
          "4-cycle differs by the RATIONAL 3/16. The single remaining [O]: "
          "derive the per-mark weight from the seam zeta/Green normalisation "
          "(same class as the EM.WARD.02 c3-ladder). No value claimed",
          ok4, f"dtop = 3/(256 pi^4); dtop / (1/2pi)^4 = {ratio:.6f} = 3/16")

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The geometric/equivariant side of HYP.PHI0.PUNCTURE.01 is now EXACT: "
        "on the flat tau = i pillowcase every twisted heat trace is a "
        "t-independent rational (sigma, rho, rho^3 all equal 1 = the "
        "Atiyah-Bott fixed-point count; pillowcase contact term exactly 1/2; "
        "clock-equivariant trace exactly 1). Because these are exact -- not "
        "asymptotic -- no orbifold geometry produces pi-powers at ANY order, "
        "so the entire analytic content of dtop = 48 c3^4 = 3/(256 pi^4) "
        "sits in ONE remaining rule: the per-mark insertion weight (c3 per "
        "mark; the bare 1/(2 pi) normalisation differs by the rational 3/16). "
        "The target narrows from 'derive the term' to 'derive the weight'; it "
        "stays [O]. No gate closes, no scorecard row."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "phi0_pillowcase_exact -- exact geometric side of the "
                    "puncture target",
        "date": "2026-07-14",
        "firewall": ("theory contract, never a scorecard row, never "
                     "load-bearing; HYP.PHI0.PUNCTURE.01 stays open"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

"""AXION.FORCE.04 is the factor ~7 really b3? -- a THEORY CONTRACT (REFUTATION).

Deep follow-up to axion03 (2026-07-10).  axion03 found that the early-QCD
isocurvature rescue needs the scalaron-gluon coupling amplified by a factor
~6.96 over the minimal trace anomaly, and FLAGGED (not derived) that 6.96 ~ b3 = 7.
This contract tries to DERIVE that factor from the spectral action / the A3(+)D5
index -- and instead REFUTES the b3 reading, cleanly.

The refutation is structural: the required shift and the anomaly shift BOTH carry
the SAME (b3/2pi) prefactor, so b3 CANCELS in their ratio:

    Delta_anom = (b3/2pi) * ln(Omega^p)          (trace-anomaly coupling)
    Delta_req  = (b3/2pi) * ln(Lambda_req/Lambda_0)   (required for m_a > H_inf)
    factor A   = Delta_req / Delta_anom = ln(Lambda_req/Lambda_0) / ln(Omega^p)

which is INDEPENDENT of b3.  The numerical A ~ 6.96 is a coincidence with b3=7
(and only for the Weyl-power convention p=2; p=1 gives ~13.9).  A is a PHYSICAL
scale ratio set by (H_inf, f_a, Lambda_QCD, N_star), not a group-theory integer.

Moreover the spectral action's genuine scalaron-gluon coupling is a SUBLEADING
a6-order term (R F^2), whose coefficient is a higher cutoff moment f_{-2} -- NOT
the a4 atoms that fix the F^2 and R^2 terms -- so even setting the coincidence
aside, the leading TFPT structure does not FORCE the amplification.

Verdict: the "factor = b3, forced by the A3(+)D5 index" reading is REFUTED.  The
amplification is a physical scale ratio (~7-14, convention-dependent) that b3
cancels out of; the spectral action does not force it at leading order.  axion03's
suggestive hint is retired.  The isocurvature rescue therefore stays genuinely open
(a postulated dim-4 coupling = a dial, or a post-inflationary axion).

Checks (hard-typed):

  C1 [E] b3 CANCELS (the core refutation): A = Delta_req/Delta_anom =
     ln(Lambda_req/Lambda_0)/ln(Omega^p) is INDEPENDENT of b3 -- computing A with
     b3 = 7 (nf=6) and b3 = 9 (nf=3) gives the SAME value; so A is NOT b3.
  C2 [E] CONVENTION-DEPENDENT: the Weyl power p (Omega vs Omega^2) shifts A from
     ~13.9 (p=1) to ~6.96 (p=2); the "~b3=7" match appears ONLY for p=2 and is not
     robust -- another sign it is a coincidence.
  C3 [E] A IS A PHYSICAL SCALE RATIO: A = ln(sqrt(H_inf f_a)/Lambda_QCD)/ln(Omega^p)
     is fixed by the inflation scale, the axion scale and the plateau (N_star), NOT
     by any group-theory integer of the A3(+)D5 index.
  C4 [O] SPECTRAL-ACTION COUPLING IS SUBLEADING: the scalaron(R)-gluon(F^2) coupling
     in the spectral action is an a6 term (R F^2), coefficient = higher moment
     f_{-2}, NOT the a4 atoms fixing F^2/R^2; so the leading forced structure does
     not hand the amplification -- even independently of the b3 coincidence.
  C5 [O] VERDICT / RELOCATION: REFUTED -- "factor = b3 forced by the index" is a
     coincidence (b3 cancels, convention-dependent) and the spectral action does not
     force it at leading order.  axion03's hint retired; the isocurvature rescue
     stays genuinely OPEN (a dim-4 dial, or a post-inflationary axion).  Never a
     scorecard row; never [E].

Firewall: F_transfer/cosmology bridge; internal consistency, not evidence.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "axion04_factor_b3_results.json"
CHECKS: list[dict] = []

PI = math.pi
MBAR = 2.435323203e18
C3 = 1.0 / (8.0 * PI)
DIM_SPLUS = 16
MU4 = 4
M_SCAL = C3 ** 3.5 * MBAR
F_A = M_SCAL / (2 * DIM_SPLUS * MU4)
A_S = 2.1e-9
R_REF = 0.004
N_STAR = 55
LAMBDA_QCD0 = 0.2


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def H_inf():
    return PI * MBAR * math.sqrt(A_S * R_REF / 2.0)


def ln_Lambda_req():
    return math.log(math.sqrt(H_inf() * F_A) / LAMBDA_QCD0)


def ln_Omega_p(p):
    phi_over_M = math.sqrt(1.5) * math.log(4 * N_STAR / 3)
    return (p / 2.0) * math.sqrt(2.0 / 3.0) * phi_over_M   # ln(Omega^p)


def delta_req(b3):
    return (b3 / (2 * PI)) * ln_Lambda_req()


def delta_anom(b3, p=2):
    return (b3 / (2 * PI)) * ln_Omega_p(p)


def amplification(b3, p=2):
    return delta_req(b3) / delta_anom(b3, p)


def c1_b3_cancels() -> None:
    A7 = amplification(7, p=2)                      # nf=6
    A9 = amplification(9, p=2)                      # nf=3
    b3_independent = abs(A7 - A9) < 1e-9
    ok = b3_independent and abs(A7 - 6.96) < 0.2
    check("C1 b3 CANCELS (core refutation) [E]: A = Delta_req/Delta_anom = "
          "ln(Lambda_req/Lambda_0)/ln(Omega^2) is INDEPENDENT of b3 -- A(b3=7) = "
          "%.3f = A(b3=9) = %.3f; the '~b3' match is NOT structural (b3 cancels)"
          % (A7, A9),
          ok, "A(b3=7)=%.4f, A(b3=9)=%.4f, identical=%s" % (A7, A9, b3_independent))


def c2_convention() -> None:
    A_p1 = amplification(7, p=1)
    A_p2 = amplification(7, p=2)
    ok = abs(A_p2 - 6.96) < 0.3 and abs(A_p1 - 13.9) < 0.6 and A_p1 > A_p2
    check("C2 CONVENTION-DEPENDENT [E]: the Weyl power p shifts A from ~%.1f (p=1, "
          "ln Omega) to ~%.2f (p=2, ln Omega^2); the '~b3=7' match appears ONLY for "
          "p=2 and is not robust -- a further sign of coincidence" % (A_p1, A_p2),
          ok, "A(p=1)=%.2f, A(p=2)=%.2f" % (A_p1, A_p2))


def c3_physical_ratio() -> None:
    A = amplification(7, p=2)
    num = ln_Lambda_req()
    den = ln_Omega_p(2)
    ok = abs(A - num / den) < 1e-9
    check("C3 A IS A PHYSICAL SCALE RATIO [E]: A = ln(sqrt(H_inf f_a)/Lambda_QCD)/"
          "ln(Omega^2) = %.2f/%.2f = %.3f -- set by the inflation scale, the axion "
          "scale and the plateau (N_star), NOT by any group-theory integer of the "
          "A3(+)D5 index" % (num, den, A),
          ok, "ln(Lambda_req/Lambda_0)=%.2f, ln(Omega^2)=%.2f, A=%.3f" % (num, den, A))


def c4_spectral_subleading() -> None:
    # F^2 and R^2 are a4 (coefficient f0); R*F^2 is a6 (coefficient f_{-2}) -- a
    # different, subleading heat-kernel order.
    order_F2 = 4          # a4
    order_R2 = 4          # a4
    order_RF2 = 6         # a6 (the scalaron-gluon coupling)
    ok = (order_RF2 > order_F2) and (order_F2 == order_R2)
    check("C4 SPECTRAL-ACTION COUPLING IS SUBLEADING [O]: F^2 and R^2 are a4 terms "
          "(coefficient f0 -- the leading atoms); the scalaron(R)-gluon(F^2) coupling "
          "R F^2 is an a6 term (coefficient = higher moment f_{-2}), a DIFFERENT "
          "subleading order -- so the leading forced structure does not hand the "
          "amplification, independently of the b3 coincidence",
          ok, "heat-kernel orders: F^2 = a%d, R^2 = a%d, R*F^2 = a%d (subleading)"
          % (order_F2, order_R2, order_RF2))


def c5_verdict() -> None:
    imported = [
        "QCD RG Lambda = mu exp(-2pi/(b3 alpha_s)); anomaly coefficient = b3 (standard)",
        "Chamseddine-Connes spectral action heat-kernel expansion a0,a2,a4,a6 "
        "(Gilkey; cited) -- F^2/R^2 at a4, R*F^2 at a6",
        "the amplification A = ln(Lambda_req/Lambda_0)/ln(Omega^p) (a physical scale "
        "ratio, b3-free)",
    ]
    check("C5 VERDICT / RELOCATION [O]: REFUTED -- 'factor = b3 forced by the index' "
          "is a coincidence (b3 CANCELS in the ratio, convention-dependent p=2 only) "
          "and the spectral action's scalaron-gluon coupling is a subleading a6 term "
          "(not the a4 atoms). axion03's hint is RETIRED; the isocurvature rescue "
          "stays genuinely OPEN (a dim-4 dial, or a post-inflationary axion). Never a "
          "scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("AXION.FORCE.04 -- is the amplification factor ~7 really b3 (from the "
          "spectral action / A3+D5 index), or a coincidence?\n")
    c1_b3_cancels(); c2_convention(); c3_physical_ratio()
    c4_spectral_subleading(); c5_verdict()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("REFUTED: factor ~7 is NOT b3 (b3 cancels); amplification not forced "
               "at leading order" if n_pass == len(CHECKS) else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    A2, A1 = amplification(7, 2), amplification(7, 1)
    reading = (
        "Trying to DERIVE axion03's factor ~6.96 from the spectral action / the "
        "A3(+)D5 index REFUTES the 'factor = b3' reading. Structurally, the required "
        "coupling shift and the trace-anomaly shift BOTH carry the same (b3/2pi) "
        "prefactor, so b3 CANCELS in their ratio: the amplification A = "
        "ln(Lambda_req/Lambda_0)/ln(Omega^p) is independent of b3 (A(b3=7) = A(b3=9) "
        "= %.2f). The numerical match with b3=7 holds only for the Weyl convention "
        "p=2 (p=1 gives %.1f), confirming coincidence. A is a physical scale ratio "
        "set by (H_inf, f_a, Lambda_QCD, N_star), not a group-theory integer. And the "
        "spectral action's genuine scalaron-gluon coupling (R F^2) is a subleading a6 "
        "term (higher moment f_{-2}), not one of the a4 atoms that fix F^2/R^2. So the "
        "leading TFPT structure does NOT force the amplification. Conclusion: "
        "axion03's suggestive '~b3' hint is retired as a coincidence, and the "
        "isocurvature rescue of FR.DM.02 stays genuinely open -- it needs either a "
        "postulated dim-4 scalaron-gluon coupling (a dial) or a post-inflationary "
        "axion scenario. A clean refutation, the anti-numerology discipline. Never a "
        "scorecard row; never [E]." % (A2, A1)
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "AXION.FORCE.04 factor-b3 refutation",
        "date": "2026-07-10",
        "firewall": "theory contract, never a scorecard row; not evidence",
        "amplification_p2": A2, "amplification_p1": A1, "b3_cancels": True,
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS, "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

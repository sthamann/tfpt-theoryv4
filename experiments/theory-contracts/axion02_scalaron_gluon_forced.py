"""AXION.FORCE.02 scalaron-gluon coupling: forced or a dial? -- a THEORY CONTRACT.

Follow-up to axion01 (next-step 1, 2026-07-10).  axion01 showed the FR.DM.02
fixed-angle scenario needs the early-QCD rescue of arXiv:2605.15192: a scalaron
(inflaton)-dependent QCD scale that lifts m_a(phi) > H_inf during inflation.  The
reviewer's condition for this to preserve parameter-freedom: the scalaron-gluon
coupling must be FORCED by a TFPT atom (c3 / spectral action / the A3(+)D5 index),
never a free dial.  This contract QUANTIFIES the required coupling and tests it
against the atoms -- honestly reporting that the target is now sharply defined and
VIABLE, but is NOT yet uniquely forced (so it is the precise open target, not a
closure).

Physics (all from TFPT's own frozen numbers + standard QCD RG):
  * m_a(0) = sqrt(chi(0))/f_a with chi(0)^(1/4) = 75.5 MeV (lattice) -> ~24 ueV today.
  * suppress isocurvature <=> m_a(inf) > H_inf, i.e. Lambda_inf > sqrt(H_inf f_a).
  * Lambda = mu exp(-2pi/(|b3| alpha_s)) with |b3| = 7 (SM QCD); so raising Lambda
    from 0.2 GeV to Lambda_inf needs a shift Delta(1/alpha_s) during inflation.

Checks (hard-typed):

  C1 [E] REQUIRED SCALE: Lambda_inf > sqrt(H_inf f_a) ~ 1.9e12 GeV (reproduces
     axion01 C4), i.e. a ln-enhancement ln(Lambda_inf/Lambda_0) ~ 30.
  C2 [E] REQUIRED COUPLING SHIFT: with |b3| = 7, Delta(1/alpha_s) = -|b3|/(2pi) *
     ln(Lambda_inf/Lambda_0) ~ -33 -- i.e. 1/alpha_s must drop by ~33 during
     inflation (alpha_s grows).
  C3 [E] VIABILITY (order of magnitude): the required |Delta(1/alpha_s)| ~ 33 is
     O(1/alpha_s) itself and O(the TFPT atoms c3^-1 = 8pi ~ 25, 4pi^2 ~ 39, |b3|*... );
     it is NOT trans-Planckian or fine-tuned -- the mechanism is quantitatively
     open, not excluded.
  C4 [O] NOT FORCED (honest): the map coupling -> Delta(1/alpha_s) also carries
     phi_inf/Mbar (the plateau field value, N_star-dependent = external reheating),
     and no single atom hits 33 EXACTLY (closest: 4pi^2 = 39.5, +18%; c3^-1 = 8pi
     = 25.1, -25%).  The repo's EXISTING fixed axion-GLUON coupling g_agg = -4 c3
     (GRAV.ASYMP.01) is a DIFFERENT operator (a G Gtilde/f_a), not the SCALARON-gluon
     kinetic coupling this needs.  So the coupling is NOT yet forced.
  C5 [E] NEGATIVE CONTROL / POWER: with NO coupling (Delta = 0) m_a(inf) ~ 24 ueV
     << H_inf ~ 1.6e13 GeV (ratio ~1e-27) -- the catastrophe axion01 found; and the
     required enhancement scales as sqrt(H_inf) ~ r^(1/4), so a smaller r shrinks it
     (the target tracks the frozen r).
  C6 [O] RELOCATION AUDIT: sharpens next-step 1 to a NUMBER -- "derive a
     scalaron-gluon kinetic coupling giving Delta(1/alpha_s)^inf ~ -33 (at the
     frozen r, N_star band) from c3 / the spectral-action a-coefficients / the
     A3(+)D5 index".  VERDICT: mechanism VIABLE, target DEFINED, coupling NOT yet
     forced.  Never a scorecard row; never [E].

Firewall: F_transfer/cosmology bridge; internal consistency, not evidence.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "axion02_scalaron_gluon_results.json"
CHECKS: list[dict] = []

PI = math.pi
C3 = 1.0 / (8.0 * PI)
MBAR = 2.435323203e18
DIM_SPLUS = 16
MU4 = 4
M_SCAL = C3 ** 3.5 * MBAR
F_A = M_SCAL / (2 * DIM_SPLUS * MU4)          # 2.39e11 GeV
A_S = 2.1e-9
R_REF = 0.004
B3 = 7                                          # |b3| SM QCD one-loop
LAMBDA_QCD0 = 0.2                                # GeV, today
CHI0_QUARTER = 0.0755                            # GeV, chi(0)^(1/4) lattice


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def H_inf(As=A_S, r=R_REF):
    return PI * MBAR * math.sqrt(As * r / 2.0)


def m_a_today():
    return CHI0_QUARTER ** 2 / F_A            # sqrt(chi0)/f_a in GeV


def c1_required_scale() -> None:
    H = H_inf()
    Lam_req = math.sqrt(H * F_A)
    ln_enh = math.log(Lam_req / LAMBDA_QCD0)
    ok = 1e12 < Lam_req < 5e12 and 25 < ln_enh < 35
    check("C1 REQUIRED SCALE [E]: Lambda_inf > sqrt(H_inf f_a) = %.2e GeV (m_a>H_inf), "
          "ln-enhancement ln(Lambda_inf/Lambda_0) = %.1f" % (Lam_req, ln_enh),
          ok, "H_inf=%.2e, f_a=%.2e -> Lambda_inf=%.2e GeV (~1e%d x today)"
          % (H, F_A, Lam_req, round(math.log10(Lam_req / LAMBDA_QCD0))))


def required_dinv():
    ln_enh = math.log(math.sqrt(H_inf() * F_A) / LAMBDA_QCD0)
    return -(B3 / (2 * PI)) * ln_enh


def c2_required_shift() -> None:
    d = required_dinv()
    ok = -40 < d < -28
    check("C2 REQUIRED COUPLING SHIFT [E]: Delta(1/alpha_s) = -|b3|/(2pi) * "
          "ln(Lambda_inf/Lambda_0) = %.1f (1/alpha_s must drop by ~33 during "
          "inflation; alpha_s grows)" % d,
          ok, "|b3|=%d -> Delta(1/alpha_s) = %.1f" % (B3, d))


def c3_viability() -> None:
    d = abs(required_dinv())
    atoms = {"c3^-1 = 8pi": 8 * PI, "4pi^2": 4 * PI ** 2,
             "2/c3 = 16pi": 16 * PI, "|b3|*2pi/... ": B3}
    # viability = O(1/alpha_s), same order as the atoms (10..40), not Planckian
    ok = 10 < d < 60
    check("C3 VIABILITY [E]: required |Delta(1/alpha_s)| = %.1f is O(1/alpha_s) and "
          "O(the atoms c3^-1=%.1f, 4pi^2=%.1f) -- natural, not fine-tuned or "
          "trans-Planckian; the mechanism is quantitatively OPEN, not excluded"
          % (d, 8 * PI, 4 * PI ** 2),
          ok, "closest atoms: " + ", ".join("%s=%.1f" % (k, v)
                                             for k, v in atoms.items() if 5 < v < 60))


def c4_not_forced() -> None:
    d = abs(required_dinv())
    cands = {"4pi^2": 4 * PI ** 2, "c3^-1=8pi": 8 * PI}
    devs = {k: (v - d) / d for k, v in cands.items()}
    none_exact = all(abs(x) > 0.1 for x in devs.values())
    g_agg = -4 * C3                            # the EXISTING axion-gluon coupling
    check("C4 NOT FORCED [O]: no single atom hits %.1f exactly (4pi^2 %.0f%%, "
          "c3^-1 %.0f%%); and the coupling->Delta map also carries phi_inf/Mbar "
          "(N_star-dependent, external). The repo's fixed axion-GLUON g_agg = -4c3 = "
          "%.3f is a DIFFERENT operator (a G Gtilde/f_a), not the scalaron-gluon "
          "kinetic term -- so the needed coupling is NOT yet forced"
          % (d, 100 * devs["4pi^2"], 100 * devs["c3^-1=8pi"], g_agg),
          none_exact, "deviations from atoms: " +
          ", ".join("%s %.0f%%" % (k, 100 * x) for k, x in devs.items()))


def c5_control() -> None:
    H = H_inf()
    ratio_off = m_a_today() / H               # no coupling
    # smaller r -> smaller H_inf -> smaller required enhancement
    d_lowr = -(B3 / (2 * PI)) * math.log(math.sqrt(H_inf(r=1e-4) * F_A) / LAMBDA_QCD0)
    ok = ratio_off < 1e-20 and abs(d_lowr) < abs(required_dinv())
    check("C5 NEGATIVE CONTROL / POWER [E]: with NO coupling m_a(inf)/H_inf = %.1e "
          "<< 1 (the isocurvature catastrophe); and the required |Delta| tracks the "
          "frozen r (r=1e-4 -> |Delta|=%.1f < %.1f) -- the target scales as r^(1/4), "
          "so it is data-anchored, not tunable" % (ratio_off, abs(d_lowr),
                                                    abs(required_dinv())),
          ok, "m_a(0)=%.1e GeV, H_inf=%.1e GeV" % (m_a_today(), H))


def c6_relocation() -> None:
    imported = [
        "single-field slow roll H_inf = pi Mbar sqrt(A_s r/2) (standard)",
        "chi(0)^(1/4) = 75.5 MeV lattice topological susceptibility (cited)",
        "QCD one-loop Lambda = mu exp(-2pi/(|b3| alpha_s)), |b3|=7 (standard)",
        "the early-QCD mechanism arXiv:2605.15192 (cited, not adopted)",
        "phi_inf/Mbar depends on N_star (external reheating, band [50,60])",
    ]
    check("C6 RELOCATION AUDIT [O]: next-step 1 sharpened to a NUMBER -- derive a "
          "scalaron-gluon kinetic coupling giving Delta(1/alpha_s)^inf ~ -33 (at the "
          "frozen r + N_star band) from c3 / spectral-action a-coefficients / the "
          "A3(+)D5 index. VERDICT: mechanism VIABLE, target DEFINED, coupling NOT "
          "yet forced. Never a scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("AXION.FORCE.02 -- is the scalaron-gluon coupling forced by a TFPT atom, "
          "or still a dial?\n")
    c1_required_scale(); c2_required_shift(); c3_viability()
    c4_not_forced(); c5_control(); c6_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("VIABLE + TARGET DEFINED, coupling NOT yet forced (open)"
               if n_pass == len(CHECKS) else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "Quantifying next-step 1: to lift m_a > H_inf during inflation (killing the "
        "axion01 isocurvature catastrophe) the QCD scale must reach Lambda_inf ~ "
        "1.9e12 GeV, a ln-enhancement ~30, i.e. Delta(1/alpha_s) ~ -33 during "
        "inflation. That shift is O(1/alpha_s) itself and of the same order as the "
        "TFPT atoms (c3^-1 = 8pi ~ 25, 4pi^2 ~ 39), so the mechanism is quantitatively "
        "VIABLE -- but no single atom hits 33 exactly, the map to the coupling also "
        "carries the N_star-dependent plateau field value, and the repo's only fixed "
        "gluon coupling (g_agg = -4c3) is a different operator. So the scalaron-gluon "
        "coupling is NOT yet forced; this contract turns next-step 1 into a sharp, "
        "data-anchored target rather than a closure. Never a scorecard row; never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "AXION.FORCE.02 scalaron-gluon forced?",
        "date": "2026-07-10",
        "firewall": "theory contract, never a scorecard row; not evidence",
        "required": {"Lambda_inf_GeV": math.sqrt(H_inf() * F_A),
                     "delta_inv_alpha_s": required_dinv(),
                     "H_inf_GeV": H_inf()},
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS, "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

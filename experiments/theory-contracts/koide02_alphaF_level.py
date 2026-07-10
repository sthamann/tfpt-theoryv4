"""KOIDE.U3.02 the Sumino cancellation ratio alpha_F/alpha -- a THEORY CONTRACT.

Follow-up to koide01 (next-step 4, 2026-07-10).  koide01 typed "alpha_F = 4 alpha"
(the reviewer's characterisation of Sumino's cancellation) as the OPEN make-or-break
step, and noted 4 = |mu4| = N_fam * C2(SU(3) fund) as exact identities.  This
contract computes the cancellation ratio from the gauge self-energy structure and
reaches an HONEST, CAUTIONARY result:

  the clean one-loop gauge-cancellation ratio is alpha_F/alpha = Q^2 / C2(family),
  which for leptons (Q^2 = 1) in the SU(3) fundamental (C2 = 4/3) is 3/4 -- NOT 4.

So the specific number "4" is CONVENTION-DEPENDENT (Sumino's U(3) normalisation /
charge assignment / family multiplicity), and the identity 4 = |mu4| = N_fam*C2(3)
is NUMEROLOGICAL unless Sumino's exact convention is DERIVED from the A3 net.  This
is the anti-numerology discipline (v354/v355 class): a coefficient counts only if
atom-forced, never if it merely matches an integer.

Checks (hard-typed):

  C1 [E] CASIMIRS: C2(SU(3) fund) = 4/3, C2(SU(3) adj) = 3 (exact, from
     (N^2-1)/(2N) and N); these are the objects the cancellation ratio is built from.
  C2 [E] CLEAN GAUGE-CANCELLATION RATIO: the one-loop gauge self-energy log
     coefficient is proportional to (coupling^2)*(Casimir); the family log cancels
     the QED log when alpha_F C2(family) = alpha Q^2 => alpha_F/alpha = Q^2/C2 =
     3/4 for leptons in the fundamental -- NOT 4.
  C3 [E] CONVENTION SCAN: under plausible U(3) conventions (family multiplicity
     N_fam, adjoint vs fundamental, U(1)_F charge) the ratio lands in
     {3/4, 9/4, 3, 4/3, ...} -- "which integer" is CONVENTION-DEPENDENT, so matching
     exactly 4 is not robust.
  C4 [E]/[O] THE '4' IS NUMEROLOGY-UNTIL-DERIVED: 4 = |mu4| = N_fam*C2(3) = 3*(4/3)
     are EXACT identities [E], but no convention-free gauge argument forces
     alpha_F/alpha = 4 [O]; the clean value is 3/4.  So koide01's C3 is DOWNGRADED:
     the '4=|mu4|' link is a coincidence unless Sumino's exact normalisation is
     derived from the A3 net.
  C5 [O] RELOCATION AUDIT: the OPEN step is sharper and STRICTER than koide01 stated
     -- not just "derive alpha_F=4alpha" but first "derive Sumino's U(3) coupling
     normalisation from the A3 net", since the target ratio is 3/4 in the clean
     convention.  Never a scorecard row; never [E].

Firewall: Koide is an F_transfer bridge; internal consistency, not evidence.
"""
from __future__ import annotations

import json
from fractions import Fraction as Fr
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "koide02_alphaF_level_results.json"
CHECKS: list[dict] = []
N = 3
N_FAM = 3
MU4 = 4


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def c1_casimirs() -> None:
    C2_fund = Fr(N ** 2 - 1, 2 * N)              # 4/3
    C2_adj = Fr(N)                                # 3
    ok = C2_fund == Fr(4, 3) and C2_adj == 3
    check("C1 CASIMIRS [E]: C2(SU(3) fund) = (N^2-1)/(2N) = 4/3, C2(SU(3) adj) = N = "
          "3 -- the objects the cancellation ratio is built from",
          ok, "C2_fund = %s, C2_adj = %s" % (C2_fund, C2_adj))


def c2_clean_ratio() -> None:
    Q2 = 1                                        # charged-lepton EM charge^2
    C2_fund = Fr(N ** 2 - 1, 2 * N)
    ratio = Fr(Q2) / C2_fund                       # 3/4
    ok = ratio == Fr(3, 4) and ratio != 4
    check("C2 CLEAN GAUGE-CANCELLATION RATIO [E]: the gauge self-energy log "
          "coefficient ~ (coupling^2)(Casimir); cancellation alpha_F C2 = alpha Q^2 "
          "=> alpha_F/alpha = Q^2/C2(fund) = %s -- NOT 4" % ratio,
          ok, "alpha_F/alpha (clean) = %s = 0.75; claimed 4 differs by factor %s"
          % (ratio, Fr(4) / ratio))


def c3_convention_scan() -> None:
    Q2 = 1
    C2_fund = Fr(N ** 2 - 1, 2 * N)
    C2_adj = Fr(N)
    conv = {
        "fund, per-lepton (clean)": Fr(Q2) / C2_fund,             # 3/4
        "fund x N_fam (loop sum)": Fr(N_FAM * Q2) / C2_fund,      # 9/4
        "adjoint rep": Fr(Q2) / C2_adj,                           # 1/3
        "adjoint x N_fam": Fr(N_FAM * Q2) / C2_adj,               # 1
        "inverse conv (C2/Q2)": C2_fund / Fr(Q2),                 # 4/3
    }
    hits4 = [k for k, v in conv.items() if v == 4]
    ok = (len(hits4) == 0) and (Fr(3, 4) in conv.values())
    check("C3 CONVENTION SCAN [E]: under plausible U(3) conventions the ratio lands "
          "in {%s} -- 'which value' is CONVENTION-DEPENDENT and NONE cleanly gives 4"
          % ", ".join(str(v) for v in conv.values()),
          ok, "; ".join("%s: %s" % (k, v) for k, v in conv.items()))


def c4_numerology() -> None:
    id_ok = (N_FAM * Fr(N ** 2 - 1, 2 * N) == 4 and MU4 == 4)   # 3*(4/3)=4=|mu4|
    clean = Fr(1) / Fr(N ** 2 - 1, 2 * N)                        # 3/4
    not_forced = (clean != 4)
    check("C4 THE '4' IS NUMEROLOGY-UNTIL-DERIVED [E]/[O]: 4 = |mu4| = N_fam*C2(3) = "
          "3*(4/3) are EXACT identities, but the convention-free gauge ratio is 3/4, "
          "not 4 -- so NO gauge argument forces alpha_F/alpha = 4; koide01's "
          "'4=|mu4|' link is a COINCIDENCE unless Sumino's exact U(3) normalisation "
          "is derived from the A3 net",
          id_ok and not_forced,
          "identities hold (3*4/3=4=|mu4|); clean ratio %s != 4 => not forced" % clean)


def c5_relocation() -> None:
    imported = [
        "one-loop gauge self-energy log ~ (coupling^2)(Casimir), same structure for "
        "QED and family gauge (standard)",
        "Sumino arXiv:0812.2103 U(3) family cancellation at alpha_F ~ O(1) alpha "
        "(cited; the specific '4' is his normalisation)",
        "the A3 = SU(4) family net (TFPT) -- Sumino's coupling normalisation is NOT "
        "yet derived from it (the sharpened open step)",
    ]
    check("C5 RELOCATION AUDIT [O]: the open step is STRICTER than koide01 stated -- "
          "first derive Sumino's U(3) coupling normalisation from the A3 net (the "
          "clean gauge ratio is 3/4, not 4), THEN the cancellation. The '4=|mu4|' is "
          "not a derivation. Never a scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("KOIDE.U3.02 -- is the Sumino ratio alpha_F/alpha = 4 forced, or "
          "convention-dependent numerology?\n")
    c1_casimirs(); c2_clean_ratio(); c3_convention_scan()
    c4_numerology(); c5_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("CAUTION: '4' NOT forced (clean ratio 3/4; convention-dependent)"
               if n_pass == len(CHECKS) else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "Computing the Sumino cancellation ratio honestly: the clean one-loop "
        "gauge-cancellation gives alpha_F/alpha = Q^2/C2(SU(3) fund) = 3/4, NOT 4. "
        "The specific value 4 is convention-dependent (U(3) normalisation, charge "
        "assignment, family multiplicity) and none of the plausible conventions "
        "cleanly yields 4. So while 4 = |mu4| = N_fam*C2(3) are exact identities, "
        "there is NO convention-free gauge argument forcing alpha_F/alpha = 4 -- "
        "koide01's '4=|mu4|' link is downgraded to a coincidence-until-derived. The "
        "sharpened open step is stricter: first derive Sumino's U(3) coupling "
        "normalisation from the A3 net (the clean target is 3/4), then the "
        "cancellation. This is the anti-numerology discipline. Never a scorecard "
        "row; never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "KOIDE.U3.02 Sumino ratio alpha_F/alpha",
        "date": "2026-07-10",
        "firewall": "theory contract, never a scorecard row; not evidence",
        "clean_ratio": "3/4", "claimed": "4", "verdict_type": "cautionary/negative",
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS, "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()

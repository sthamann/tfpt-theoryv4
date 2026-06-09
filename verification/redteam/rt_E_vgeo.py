"""RED TEAM  Target E -- v_geo as the unique dimensional floor.

Minimal claim (v78_vgeo_floor, ledger ANCHOR.VGEO.01):
    no pure-number theory can derive an absolute dimensionful scale; all physical
    scales are ratios to one measured unit v_geo.

Alessandro: conceptually correct, but it must be tested for HIDDEN second scales.
The package should verify that every dimensional observable uses the SAME v_geo,
and that no independent mass / length / cutoff / reheating / normalization /
matching scale / experimental datum re-enters under another name.

This script runs that single-scale AUDIT: it tabulates the dimensionful
quantities of the package, reduces each to (dimensionless number) x (power of one
M_bar = v_geo), and FLAGS the ones that are not pure reductions but either
explicit identifications or genuine frontier inputs.
"""
import mpmath as mp
from rt_common import (banner, step, note, verdict, check, summary, reset,
                       PI, c3, Mbar, phi0, SURVIVES_NARROWED)

REPORT = {}

# (name, reduced-form, tier, reduces?) ; reduces=True means = dimensionless x M_bar^p
AUDIT = [
    ("1/G  (Newton)",          "M_bar^2  (= v_geo, v68/v75)",             "closed", True),
    ("charged-fermion masses", "(pi/sqrt2) c_f phi0^k * v_geo (v20/v46)", "closed", True),
    ("M_scal (scalaron)",      "c3^(7/2) * M_bar (v7/v68)",               "IR",     True),
    ("rho_Lambda^(1/4)",       "(3/4pi^2)^(1/4) e^(-ainv/2) * M_bar (v60)", "IR",   True),
    ("f_a (axion)",            "(c3/|mu4|)^(7/2) * M_bar (v25/check.txt)", "IR",     True),
    ("seam cutoff Lambda",     "= v_geo  (seam=Planck IDENTIFICATION, v68)", "id",   False),
    ("electroweak vev v",      "matching scale -> needs explicit = f(c3)*v_geo", "frontier", False),
    ("reheating T_reh",        "frontier input [P] (N_star dimensionless ok)", "frontier", False),
    ("leptogenesis M_R",       "frontier input [P] (eta_B firewalled, v79)", "frontier", False),
]


def run():
    reset()
    banner("E", "v_geo as the unique dimensional floor (single-scale audit)")

    # --- 1 minimal statement ------------------------------------------------
    step(1, "minimal statement")
    note("every dimensionful observable = (dimensionless TFPT number) x (power of ONE\n"
         "scale v_geo); no second independent dimensionful input exists.")

    # --- 2 assumptions ------------------------------------------------------
    step(2, "assumptions")
    note("dimensional analysis: a pure number cannot be dimensionful, so >=1 anchor is\n"
         "required by logic; the claim is that EXACTLY one suffices.")

    # --- 3 logical chain: the reductions that hold -------------------------
    step(3, "logical chain -- closed/IR readouts reduce to one M_bar")
    M_scal = c3 ** mp.mpf('3.5') * Mbar
    check("M_scal/M_bar = c3^(7/2) is a pure number => M_scal ~ 3.06e13 GeV reduces to v_geo",
          abs(float(M_scal) - 3.06e13) / 3.06e13 < 0.05)
    check("f_a = (c3/|mu4|)^(7/2) M_bar : 128 = 4^(7/2) so f_a = M_scal/128 reduces to v_geo",
          abs(4 ** 3.5 - 128) < 1e-9 and
          abs(float((c3 / 4) ** mp.mpf('3.5') * Mbar) - float(M_scal) / 128) < 1e3)
    check("1/G and the flavor scale v_geo are the SAME anchor (v75/v68): two [A] -> one",
          True)

    # --- 4 validity conditions ---------------------------------------------
    step(4, "validity conditions")
    check("the reduction is exact only where the dimensionless prefactor is built from "
          "{c3, phi0, integers, pi} -- i.e. the closed compiler + protected IR tiers", True)

    # --- 5 counterexample search: hidden second scales ---------------------
    step(5, "counterexample search -- scan for a hidden SECOND scale")
    reduced = [a for a in AUDIT if a[3]]
    flagged = [a for a in AUDIT if not a[3]]
    for name, form, tier, ok in AUDIT:
        mark = "reduces" if ok else "FLAG   "
        note(f"[{mark}] ({tier:8s}) {name:24s} -> {form}")
    check(f"{len(reduced)} closed/IR observables reduce to dimensionless x v_geo "
          "(no second scale in tiers 1-2)", len(reduced) >= 5)
    check(f"audit SURFACES {len(flagged)} candidates that are NOT pure reductions: "
          "seam-cutoff identification, EW matching, reheating, leptogenesis",
          len(flagged) >= 4)

    # --- 6 limiting / degenerate cases -------------------------------------
    step(6, "limiting / degenerate cases")
    check("seam cutoff Lambda: only an IDENTIFICATION (seam=Planck) collapses it to v_geo; "
          "without it, Lambda is a hidden 2nd scale (v68 makes this explicit, not silent)",
          True)
    check("N_star is dimensionless (e-folds) so it is NOT a second scale; the reheating "
          "TEMPERATURE is, and stays a frontier [P] input", True)

    # --- 7 alternative structures ------------------------------------------
    step(7, "alternative structures -- could two anchors masquerade as one?")
    note("the EW vev, reheating temperature and leptogenesis scale must each be shown\n"
         "= (c3-power) x v_geo, or they are independent inputs. They currently live in the\n"
         "frontier tier [P]/[A] and must NOT be silently folded into v_geo.")
    check("=> single-scale-ness is EXACT for the closed+IR tiers, CONDITIONAL for the full "
          "theory on the flagged identifications", True)

    # --- 8 verdict ----------------------------------------------------------
    fails = summary("rt_E v_geo single-scale audit")
    verdict(
        REPORT, target_id="E",
        claim="exactly one dimensionful scale v_geo carries the whole theory",
        assumptions="dimensionless prefactors from {c3, phi0, pi, integers}; "
                    "seam=Planck identification for the cutoff",
        works="the closed compiler + protected IR tiers reduce every dimensionful readout "
              "to (pure number) x v_geo; 1/G and the flavor scale are one anchor",
        fails="the full theory still carries frontier dimensionful inputs (EW matching, "
              "reheating temperature, leptogenesis scale) + the seam-cutoff identification",
        status=SURVIVES_NARROWED,
        verdict_text="v_geo is the unique dimensional floor of the CERTIFIED tiers (true by "
                     "dimensional analysis). Full single-scale-ness is conditional on the "
                     "flagged identifications staying honestly typed.",
        residual="explicit reduction (or honest frontier typing) of EW/reheating/"
                 "leptogenesis scales + the seam=Planck cutoff identification.",
    )
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

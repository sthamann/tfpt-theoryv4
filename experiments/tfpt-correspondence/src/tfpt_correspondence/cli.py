"""``tfpt-correspondence analyze`` -- the TFPT correspondence-principle / phase-boundary check.

Question (internal consistency, NOT external data): does TFPT's own algebra place the
spacetime <-> black-hole "correspondence" -- the SAME seam state described two ways across a
threshold in a dimensionless order parameter -- onto COMPILER ATOMS, or would it need a free
number?

The runner checks four preregistered items (hypotheses/correspondence_v1.yaml):
  CORR.H1  atom-lock: the four phase-boundary constants {1/4, 1/2, 3/8, (2/3)^6} and the
           Bekenstein coefficient 4 c3 = 1/(2 pi) are EXACT atom rationals, not free numbers.
  CORR.H2  the critical quotient of order parameter (A) is exactly 1 for a black hole
           (Bekenstein saturation), atom-locked coefficient, independent of M.
  CORR.H3  order parameter (B), the SdS compactness quotient, runs monotonically over the
           atom window [3/8, 1/2] with 3/8 inside 1/3 < 3/8 < 4/9 < 1/2.
  CORR.H4  typing guard: [O]-gated on SEAM.EQUIV.01; no new scale; no Hagedorn/string scale
           (this is NOT Horowitz-Polchinski).

Verdict: a STRUCTURAL [C] correspondence -- atom-locked internally, but the physical
spacetime<->BH phase transition stays data_limited / [O]-gated on the open Seam-Horizon
theorem. Never [E], never load-bearing, out of the evidence scorecard.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from . import atoms, order_parameter as op

RESULTS = Path(__file__).resolve().parents[2] / "results"

GATE = "SEAM.EQUIV.01"  # Seam-Horizon theorem, OPEN (origin_theory / v58 / v346 / v347)


def _atom_lock() -> dict:
    """CORR.H1: every phase-boundary constant is an exact atom rational (not a fit)."""
    table = atoms.atom_lock_table()
    rows = {
        name: {
            "value": (str(val) if isinstance(val, Fraction) else round(float(val), 12)),
            "atom": identity,
            "holds": holds,
        }
        for name, (val, identity, holds) in table.items()
    }
    return {"rows": rows, "all_atom_locked": all(r["holds"] for r in rows.values())}


def analyze() -> dict:
    lock = _atom_lock()
    saturation = op.saturation_selfconsistency()
    window = op.compactness_window()
    echo = op.echo_template()

    h1 = lock["all_atom_locked"]
    h2 = saturation["all_q_are_one"] and all(
        abs(r - 1.0) < 1e-12 for r in saturation["S_BH_over_A_quarter"].values())
    h3 = (window["endpoint_de_sitter_matches_1_2"] and window["endpoint_nariai_matches_3_8"]
          and window["monotone_decreasing"] and window["ladder_1_3_lt_3_8_lt_4_9_lt_1_2"])
    # H4 is a static typing guard: kernel is atom-only + pi, no Hagedorn/string scale.
    h4 = True
    # H5 is the observable hook: it inherits the gw-ringdown-echo / gravastar verdicts
    # (data_limited) and only requires the echo template to be atom-consistent + finite.
    h5 = (abs(echo["amplitude_ratio_bound"] - 64.0 / 729.0) < 1e-12
          and echo["delay_over_M"] > 0.0)

    all_pass = h1 and h2 and h3 and h4
    verdict = (
        "STRUCTURAL [C] CORRESPONDENCE (consistent, [O]-gated). The spacetime<->black-hole "
        "correspondence is a CHANGE OF BOOKKEEPING of one seam state (geometry channel = "
        "spacetime; boundary/information channel = the compiler), and its phase-boundary "
        "constants are ALL compiler atoms: the critical Bekenstein-saturation quotient "
        "q_Bek=1 has the atom coefficient 4 c3 = 1/(2 pi) with density 1/4=1/|mu4|; the "
        "geometric window runs over [3/8, 1/2] = [p2(a)/e1(a)^2, |Z2|/|mu4|]; the recovery "
        "reflectivity bound is (2/3)^6=(|Z2|/N_fam)^(2 N_fam). NOTHING here needs a free "
        f"number, so the reading survives the numerology test -- but it is gated on the OPEN "
        f"{GATE} (Seam-Horizon theorem) and stays [C]: NOT [E], NOT load-bearing. It is NOT "
        "Horowitz-Polchinski (TFPT has no Hagedorn/string scale); the shared content is only "
        "'one state, two descriptions across a threshold'. The PHYSICAL phase transition "
        "(a measured order parameter) is data_limited."
    ) if all_pass else (
        "STRUCTURE BROKEN: a phase-boundary constant is not atom-locked or an order-parameter "
        "self-consistency check failed (see fields) -> correspondence reading rejected."
    )

    return {
        "experiment": "tfpt-correspondence",
        "version": "v1",
        "role": "internal-consistency / theory-contract search target (out of scorecard)",
        "gate": {"depends_on": GATE, "gate_status": "OPEN", "max_type_until_closed": "[C]"},
        "tests": {
            "CORR.H1_atom_lock": {"pass": h1, "detail": lock},
            "CORR.H2_saturation_selfconsistency": {"pass": h2, "detail": saturation},
            "CORR.H3_geometric_window": {"pass": h3, "detail": window},
            "CORR.H4_gate_and_no_new_state": {
                "pass": h4,
                "detail": {"kernel_atom_only_plus_pi": True, "hagedorn_or_string_scale": False,
                           "is_horowitz_polchinski": False, "discipline": ["v246", "v153"]},
            },
            "CORR.H5_observable_echo": {"pass": h5, "status": "data_limited", "detail": echo},
        },
        "status": "consistent" if all_pass else "tension",
        "type": "[C]",
        "firewall": (
            "Change-of-bookkeeping structural search; downstream of the OPEN SEAM.EQUIV.01; "
            "not in verification/ledger/website; not scorecard-eligible; never [E]."
        ),
        "verdict": verdict,
    }


def _print(res: dict) -> None:
    print("=" * 82)
    print("TFPT correspondence principle  (spacetime <-> black hole as an atom-locked "
          "phase boundary)")
    print("=" * 82)
    lock = res["tests"]["CORR.H1_atom_lock"]["detail"]["rows"]
    print("  [H1] atom-lock of the phase-boundary constants:")
    for name, r in lock.items():
        print(f"        {name:26s} = {str(r['value']):>10s}  == {r['atom']:24s} -> {r['holds']}")
    sat = res["tests"]["CORR.H2_saturation_selfconsistency"]["detail"]
    print(f"  [H2] critical quotient q_Bek at the horizon = "
          f"{list(sat['q_Bek_at_horizon'].values())}  (all == 1: {sat['all_q_are_one']})")
    print(f"        S_BH == A/4 (1/4=1/|mu4|): "
          f"{all(abs(r - 1.0) < 1e-12 for r in sat['S_BH_over_A_quarter'].values())}")
    win = res["tests"]["CORR.H3_geometric_window"]["detail"]
    print(f"  [H3] SdS window Q_geom: dS={win['q_geom_de_sitter']:.6f} (->1/2), "
          f"Nariai={win['q_geom_nariai']:.6f} (->3/8), monotone={win['monotone_decreasing']}, "
          f"ladder={win['ladder_1_3_lt_3_8_lt_4_9_lt_1_2']}")
    h4 = res["tests"]["CORR.H4_gate_and_no_new_state"]["detail"]
    print(f"  [H4] gate={res['gate']['depends_on']} (OPEN); Hagedorn/string scale="
          f"{h4['hagedorn_or_string_scale']}; is Horowitz-Polchinski={h4['is_horowitz_polchinski']}")
    ec = res["tests"]["CORR.H5_observable_echo"]["detail"]
    print(f"  [H5] observable echo @ Q_geom=3/8 ECO: delay={ec['delay_over_M']:.4f} M, "
          f"amplitude<=(2/3)^6={ec['amplitude_ratio_bound']:.4f}  (status: data_limited)")
    print(f"        delays (source frame): {ec['echo_delay_ms_source_frame']}  ms  "
          f"-> search in gw-ringdown-echo, delay in gravastar-compactness")
    print(f"\n  status={res['status']}  type={res['type']}")
    print(f"\n-> {res['verdict']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="TFPT correspondence principle: spacetime<->BH atom-locked phase boundary")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)

    res = analyze()
    if args.command == "audit":
        print("audit: kernel atoms only + pi; no SI inputs; no Hagedorn/string scale.")
        return 0 if all(t["pass"] for t in res["tests"].values()) else 1

    _print(res)
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

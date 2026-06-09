"""Shared harness for the TFPT Red Team / Stress Test layer.

This layer is DELIBERATELY ADVERSARIAL.  Unlike the confirmatory suite
(`verification/v*.py`), whose checks are designed to pass, every script here
tries to BREAK a load-bearing reduction of the package along Alessandro's five
targets (A-E).  A red-team `check(...)` therefore asserts an *adversarial* fact:
that a counterexample really exists, that a hidden assumption is really needed,
or that a firewall really holds.  The honest outcome of each target is carried
by an explicit VERDICT + RESIDUAL RISK, not by a green "PASS".

The fixed per-target protocol (Alessandro):
    1 minimal statement   2 assumptions          3 logical chain
    4 validity conditions 5 counterexample search 6 limiting/degenerate cases
    7 alternative structures                      8 provisional verdict

Each `rt_*` module exposes `run()` (prints the protocol, runs the adversarial
checks, returns the failed-check count) and fills a module-level `REPORT` dict
that `rt_table.py` aggregates into Alessandro's red-team table.
"""

import os
import sys

# --- make the parent verification/ importable for tfpt_constants ----------
_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_HERE)
_ROOT = os.path.dirname(_PARENT)
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from tfpt_constants import (  # noqa: E402  (re-exported for the rt_* modules)
    check, summary, reset,
    PI, c3, g_car, N_fam, dim_Splus, rankE8, Omega_adm, b1, Mbar, phi0,
)

PARENT_DIR = _PARENT          # verification/
ROOT_DIR = _ROOT              # repository root (where the .tex notes live)

# verdict vocabulary used in the aggregated table -------------------------
SURVIVES = "SURVIVES"                 # claim stands as worded
SURVIVES_NARROWED = "SURVIVES (narrowed)"   # stands only after an assumption is made explicit
REDUCED_OPEN = "REDUCED, not closed"  # honest open boundary; keep conservative wording
BROKEN = "BROKEN"                     # the worded claim fails the attack


def banner(target_id, title):
    """Print the per-target header."""
    bar = "=" * 78
    print(bar)
    print(f"  RED TEAM  Target {target_id}:  {title}")
    print(bar)


def step(n, name):
    """Print a numbered protocol step heading."""
    print(f"\n  [{n}] {name}")


def note(text):
    """Print a narrow protocol note (indented)."""
    for line in text.splitlines():
        print(f"      {line}")


def verdict(report_obj, *, target_id, claim, assumptions, works, fails,
            status, verdict_text, residual):
    """Record + print the provisional verdict and fill the REPORT dict.

    `status` is one of SURVIVES / SURVIVES_NARROWED / REDUCED_OPEN / BROKEN.
    """
    report_obj.update(
        target=target_id, claim=claim, assumptions=assumptions,
        works=works, fails=fails, status=status,
        verdict=verdict_text, residual=residual,
    )
    print("\n  [8] PROVISIONAL VERDICT")
    print(f"      status     : {status}")
    print(f"      verdict    : {verdict_text}")
    print(f"      works where: {works}")
    print(f"      fails where: {fails}")
    print(f"      residual   : {residual}")
    return report_obj


def read_text(path):
    """Best-effort file read for the firewall/audit scans (never raises)."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""

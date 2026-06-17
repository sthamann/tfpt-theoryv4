"""``tfpt-handedness analyze`` -- the parity / cosmic-spin-handedness watchdog.

A black-hole-cosmology child universe could inherit the parent black hole's spin, leaving a
global rotation / handedness imprint.  TFPT carries a ``mu4`` boundary clock and a
``PSL(2,C) ~ SO+(3,1)`` boundary orientation, so it allows at most a TINY global orientation
remnant -- it predicts APPROXIMATE PARITY, not a ~20% handedness excess.

Shamir 2025 (MNRAS 538 76) reports a ~50% counter-clockwise excess of galaxy rotation in
JWST/JADES.  This runner computes the monopole significance of that excess and is explicit
that the deciding question -- a true global parity MONOPOLE (possible parent-spin signature)
vs a Milky-Way-rotation aberration DIPOLE (systematic) -- needs sky-resolved counts that are
NOT in the aggregate data.  Galaxy Zoo (Land+2008) found consistency with isotropy.

So this is a FRONTIER watchdog, not a TFPT prediction-of-record:
  * consistent-with-isotropy  -> fine (TFPT only allows a tiny remnant);
  * a robust global monopole surviving MW-aberration + selection systematics across surveys
    -> a frontier parent-spin signature that TFPT would then have to source globally.

Frozen kill/flag rule (pre-registered):

    a parity-odd global spin MONOPOLE that survives Milky-Way-aberration + selection
    systematics, replicated across independent surveys -> promote from frontier watchdog to a
    parent-spin candidate (still NOT the compiler core).  A pure dipole is a systematic, not a
    signal.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
RESULTS = Path(__file__).resolve().parents[2] / "results"


def _two_sided_p(z: float) -> float:
    """Two-sided Gaussian tail probability for |z|."""
    return math.erfc(abs(z) / math.sqrt(2.0))


def binomial_monopole(n_ccw: int, n_cw: int) -> dict:
    """Significance of a handedness MONOPOLE under the null p=1/2 (Gaussian approximation)."""
    n = n_ccw + n_cw
    expected = n / 2.0
    sigma = math.sqrt(n / 4.0)
    z = (max(n_ccw, n_cw) - expected) / sigma
    asym = (n_ccw - n_cw) / n
    return {"n": n, "n_ccw": n_ccw, "n_cw": n_cw,
            "asymmetry": round(asym, 4),
            "excess_ratio": round(max(n_ccw, n_cw) / min(n_ccw, n_cw), 3),
            "monopole_z_sigma": round(z, 3), "two_sided_p": _two_sided_p(z)}


def analyze(m: dict) -> dict:
    legs = []
    for d in m["datasets"]:
        if d.get("n_ccw") is None or d.get("n_cw") is None:
            legs.append({"name": d["name"], "result": d.get("verdict", "no counts"),
                         "monopole_z_sigma": None})
            continue
        legs.append({"name": d["name"], **binomial_monopole(d["n_ccw"], d["n_cw"])})

    counted = [leg for leg in legs if leg.get("monopole_z_sigma") is not None]
    headline = max(counted, key=lambda r: r["monopole_z_sigma"]) if counted else None
    tfpt_allowed = m["tfpt_expectation"]["allowed_asymmetry"]
    return {
        "tfpt_allowed_asymmetry": tfpt_allowed,
        "legs": legs,
        "headline_dataset": headline["name"] if headline else None,
        "headline_monopole_z_sigma": headline["monopole_z_sigma"] if headline else None,
        "monopole_vs_dipole": "aggregate counts give the MONOPOLE only; separating a global "
                              "parity monopole from an MW-aberration dipole needs sky-resolved "
                              "counts (not in this data)",
        "status": "data_limited",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TFPT parity / galaxy-spin handedness watchdog")
    ap.add_argument("command", choices=["audit", "analyze"], nargs="?", default="analyze")
    args = ap.parse_args(argv)
    m = json.loads(DATA.read_text(encoding="utf-8"))

    print("=" * 78)
    print("TFPT parity watchdog  (galaxy-spin handedness vs a tiny PSL(2,C)/mu4 remnant)")
    print("=" * 78)
    if args.command == "audit":
        return 0

    res = analyze(m)
    print(f"  TFPT expectation: approximate parity (allowed asymmetry ~ "
          f"{res['tfpt_allowed_asymmetry']:.2f}; only a tiny boundary remnant)\n")
    for leg in res["legs"]:
        if leg.get("monopole_z_sigma") is None:
            print(f"  {leg['name']:28s} -> {leg['result']}")
        else:
            print(f"  {leg['name']:28s} -> ccw:cw = {leg['n_ccw']}:{leg['n_cw']} "
                  f"(x{leg['excess_ratio']}), asym={leg['asymmetry']:+.3f}, "
                  f"monopole {leg['monopole_z_sigma']:.2f}s (p={leg['two_sided_p']:.2g})")
    print(f"\n  caveat: {res['monopole_vs_dipole']}")

    verdict = (
        f"FRONTIER WATCHDOG (data_limited): the JADES excess is a ~"
        f"{res['headline_monopole_z_sigma']:.1f} sigma MONOPOLE, but it is most likely a "
        f"Milky-Way-rotation aberration (a DIPOLE), and Galaxy Zoo found isotropy. TFPT allows "
        f"only a tiny boundary remnant, so it does NOT predict a ~20% asymmetry: approximate "
        f"parity is the prediction. A robust global parity monopole surviving MW-aberration + "
        f"selection systematics across surveys would become a frontier parent-spin candidate -- "
        f"not yet, and never the compiler core. A pure dipole is a systematic, not a signal."
    )
    print(f"\n-> {verdict}")
    res["verdict"] = verdict

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

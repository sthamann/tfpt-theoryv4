"""Guard: the two textbook negative controls report honestly and stay distinct.

CONTROL 1 (Efimov ladder): the constants are the exactly-derived values (lambda = e^(pi/s0),
s0 = 1.00624 — not copied numbers), the Efimov and kernel frequencies are resolvable (>20%
apart, outside the detector's +-10% kernel-exclusion window), the measured 133Cs ratio puts
the TFPT lambda = (3/2)^6 more than 7 sigma away, and the frozen detector does NOT fire at
the kernel on a gated realisation of the Efimov comb.

CONTROL 2 (MCT exponent spread): the exact Gamma-function exponent relations reproduce the
canonical hard-sphere values (lambda = 0.735 -> a = 0.312, b = 0.583, gamma = 2.46), every
data-file row is internally consistent, and the spread statistic is reported honestly — the
locked-bend hypothesis (gamma == ln3/ln(3/2) = 2.7095 for all glass formers) must be rejected
while the bend still lies INSIDE the observed range (that is the structural point).

Run (no pytest needed):  PYTHONPATH=src python tests/test_negative_controls.py
Or, if pytest is available:  PYTHONPATH=src pytest tests/
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "src"))

from tfpt_dsicontrol import efimov, mct  # noqa: E402
from tfpt_dsicontrol.comb import LAMBDA, OMEGA  # noqa: E402


def test_efimov_constants_exactly_derived():
    """lambda_Efimov and omega_Efimov ARE e^(pi/s0) and 2pi/ln(lambda), s0 = 1.00624."""
    assert efimov.S0_EFIMOV == 1.00624
    assert efimov.LAMBDA_EFIMOV == math.exp(math.pi / 1.00624)
    assert abs(efimov.LAMBDA_EFIMOV - 22.694) < 5e-3
    assert efimov.OMEGA_EFIMOV == 2.0 * math.pi / math.log(efimov.LAMBDA_EFIMOV)
    assert abs(efimov.OMEGA_EFIMOV - 2.013) < 5e-3


def test_efimov_kernel_resolvable():
    """>20% frequency separation — outside the +-10% kernel window detect_comb excludes."""
    sep = (OMEGA - efimov.OMEGA_EFIMOV) / OMEGA
    assert sep > 0.20
    assert abs(efimov.OMEGA_EFIMOV - OMEGA) > 0.1 * OMEGA


def test_efimov_ladder_ratios_reject_tfpt_scale():
    """133Cs alone is >7 sigma from lambda = (3/2)^6; combined is Efimov-consistent."""
    ratios = efimov.ladder_ratio_test(efimov.load_ladders())
    cs = next(r for r in ratios["per_system"] if r["system"] == "133Cs")
    assert cs["z_tfpt"] > 7.0
    assert abs(cs["z_efimov"]) < 2.0
    assert ratios["sigma_equiv_tfpt"] > 7.0
    assert abs(ratios["combined_z_efimov"]) < 2.0
    assert LAMBDA == 1.5 ** 6   # the rejected scale is the axiom-derived one


def test_efimov_detector_quiet_at_kernel():
    """The frozen detector must NOT fire at omega=2.583 on a gated Efimov-comb realisation
    (fast 5-seed version of EF.02; the full 25-seed run lives in the CLI/results)."""
    r = efimov.detector_resolvability(n_seeds=5)
    assert r["periods_kernel"] >= 2.8 and r["periods_efimov"] >= 2.8   # gated both ways
    assert r["kernel_fired"] == 0
    assert r["efimov_detect_rate"] >= 0.6
    w = r["scan"]["best_localisable_omega"]
    assert w is not None and abs(w - efimov.OMEGA_EFIMOV) < 0.05 * efimov.OMEGA_EFIMOV


def test_mct_exponent_relations_canonical():
    """The exact Gamma relations reproduce the textbook hard-sphere exponent set."""
    assert abs(mct.a_from_lambda(0.735) - 0.312) < 2e-3
    assert abs(mct.b_from_lambda(0.735) - 0.583) < 2e-3
    assert abs(mct.gamma_from_lambda(0.735) - 2.46) < 1e-2
    assert abs(mct.lambda_from_gamma(2.46) - 0.735) < 2e-3
    assert mct.BEND_TFPT == math.log(3.0) / math.log(1.5)


def test_mct_rows_internally_consistent():
    """Every quoted (lambda, gamma) pair in the data file obeys the exponent relations."""
    rows = [mct.complete_row(r) for r in mct.load_systems()]
    assert len(rows) >= 5
    for r in rows:
        if r["lambda_quoted"]:
            assert abs(r["consistency_delta_gamma"]) < 0.35, r["system"]


def test_mct_spread_honest():
    """The spread statistic: bend inside the range, locked bend rejected, spread >> error —
    and the weaker one-universal-gamma number is reported as-is (not inflated)."""
    rec = mct.run_mct_control()
    sp = rec["spread"]
    assert sp["bend_inside_spread"]                      # the sceptic's premise is honoured
    assert sp["locked_bend_test"]["sigma_equiv_wh"] >= 3.0
    assert sp["spread_over_error_range"] >= 3.0
    assert sp["universality_test"]["chi2"] > 0           # reported, whatever its size
    assert rec["passed"]


if __name__ == "__main__":
    for fn in (test_efimov_constants_exactly_derived, test_efimov_kernel_resolvable,
               test_efimov_ladder_ratios_reject_tfpt_scale,
               test_efimov_detector_quiet_at_kernel,
               test_mct_exponent_relations_canonical, test_mct_rows_internally_consistent,
               test_mct_spread_honest):
        fn()
        print(f"  PASS {fn.__name__}")
    print("negative-controls guard: ALL PASS")

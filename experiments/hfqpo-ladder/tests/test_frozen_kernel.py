"""Guard: the hfqpo-ladder kernel is frozen, axiom-derived, and shared (H4).

Asserts (a) the ladder step is EXACTLY the rational 3/2 derived from N_fam = 3 (no fitted
exponent, no SI input), (b) the ladder/harmonic tooth arithmetic is what the preregistration
says, (c) the geometric tooth set is DISJOINT from the integer-harmonic set (the two
predictions never collide, so the discriminator is well-posed), and (d) the derived comb
constants are bit-identical to the shared frozen detector in recovery-comb-domains.

Run (no pytest needed):  PYTHONPATH=src python tests/test_frozen_kernel.py
"""

from __future__ import annotations

import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "src"))

ORIGINAL_COMB = (HERE.parents[0] / "recovery-comb-domains" / "src" / "tfpt_combdomains"
                 / "comb.py")

from tfpt_hfqpo import constants as k  # noqa: E402


def _load_original_comb():
    spec = importlib.util.spec_from_file_location("tfpt_combdomains_comb_original",
                                                  ORIGINAL_COMB)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_step_exact_rational_from_axioms():
    """step = N_fam/(N_fam-1) = 3/2 EXACT — a rational from the carrier, not a fit."""
    assert k.N_FAM == 3
    assert k.STEP == Fraction(3, 2)
    assert k.STEP_F == 1.5
    assert k.STEP == Fraction(k.N_FAM, k.N_FAM - 1)
    assert k.C3 == 1.0 / (8.0 * math.pi) and k.G_CAR == 5


def test_ladder_arithmetic():
    """Tooth and harmonic-fundamental arithmetic match the preregistration."""
    assert k.ladder_tooth(441.0) == 661.5
    assert k.ladder_tooth(276.0) == 414.0
    assert k.ladder_tooth(168.0) == 252.0
    assert k.ladder_tooth(242.0) == 363.0
    assert k.harmonic_fundamental(441.0) == 147.0          # = 294/2 ~ nu_l for a true 3:2 pair
    assert k.harmonic_fundamental(276.0) == 92.0           # the observed marginal subharmonic


def test_tooth_sets_disjoint():
    """Geometric teeth (3/2)^k never coincide with integer harmonics k*nu_0: the only
    solution of (3/2)^a = m/3 (integer m) is none for a >= 1 — so the discriminator is
    well-posed at any resolvable line separation."""
    for a in range(1, 7):
        tooth_over_nu0 = 3.0 * 1.5 ** a          # (3/2)^a * nu_u / (nu_u/3)
        assert abs(tooth_over_nu0 - round(tooth_over_nu0)) > 0.09, a
    # and concretely: tooth - 4 nu_0 = nu_u/6 >= 26 Hz for every source in the census
    for nu_u in (441.0, 276.0, 168.0, 242.0):
        sep = k.ladder_tooth(nu_u) - 4.0 * k.harmonic_fundamental(nu_u)
        assert math.isclose(sep, nu_u / 6.0, rel_tol=1e-12)
        assert nu_u / 6.0 >= 26.0


def test_comb_constants_match_shared_kernel():
    """lambda/omega/eps equal the shared frozen recovery-comb detector bit-for-bit."""
    orig = _load_original_comb()
    assert k.LAMBDA == orig.LAMBDA == 1.5 ** 6
    assert k.OMEGA == orig.OMEGA == 2.0 * math.pi / math.log(1.5 ** 6)
    assert k.EPS_PREDICTED == orig.EPS_PREDICTED
    assert abs(k.OMEGA - 2.5827) < 5e-4
    assert abs(k.EPS_PREDICTED - 0.017) < 1e-3


def test_h2_design_frozen():
    """The H2 Monte-Carlo design constants match hypotheses/hfqpo_v1.yaml."""
    assert k.H2_N_MC == 200_000 and k.H2_SEED == 0 and k.H2_N_SOURCES == 5
    assert k.H2_WINDOW == 0.05 and k.H2_CLUSTER_K == 4
    assert k.H2_SEL_WIDTH_X == 0.06 and k.H2_MEAS_SIGMA_R == 0.044
    assert k.H2_RATIO_AT_0 == 2.2 and k.H2_RATIO_SLOPE == -1.0
    assert k.H2_X_EQ_ANCHORED == 0.7
    # the anchored point IS the 3/2 crossing of the frozen ratio curve
    assert math.isclose(k.H2_RATIO_AT_0 + k.H2_RATIO_SLOPE * k.H2_X_EQ_ANCHORED, k.STEP_F,
                        rel_tol=1e-12)


if __name__ == "__main__":
    for fn in (test_step_exact_rational_from_axioms, test_ladder_arithmetic,
               test_tooth_sets_disjoint, test_comb_constants_match_shared_kernel,
               test_h2_design_frozen):
        fn()
        print(f"  PASS {fn.__name__}")
    print("frozen-kernel guard: ALL PASS")

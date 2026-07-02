"""Guard tests: the frozen kernel must equal the exact axioms-derived values.

The preregistration (hypotheses/repeater_cascade_v1.yaml) forbids any refitted
omega, bend, epsilon or exponent; these tests pin the constants byte-for-byte
against independent recomputations so a silent edit fails CI, and pin them to
the SAME frozen objects used in pulsar-glitch-recovery (cross-domain identity).
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from repeater_cascade import constants as c  # noqa: E402


def test_axioms():
    assert c.C3 == 1.0 / (8.0 * math.pi)
    assert c.G_CAR == 5
    assert c.N_FAM == 3
    assert c.P2_EXP == 6


def test_clock_bend_and_wall():
    # rate(n) = -6 ln(1 - n/3) == 6 ln(3/2), 6 ln 3 (exact identity; float ulp tol)
    assert c.RECOVERY_RATE_1 == 6.0 * math.log(1.5)
    assert c.RECOVERY_RATE_2 == 6.0 * math.log(3.0)
    assert abs(c.RECOVERY_RATE_1 - (-6.0 * math.log(1.0 - 1.0 / 3.0))) < 1e-14
    assert abs(c.RECOVERY_RATE_2 - (-6.0 * math.log(1.0 - 2.0 / 3.0))) < 1e-14
    assert c.BEND == math.log(3.0) / math.log(1.5)
    assert abs(c.BEND - 2.70951129135145) < 1e-12
    assert c.WALL == 3


def test_comb_kernel():
    lam = (3.0 / 2.0) ** 6
    assert c.LAMBDA_CASCADE == lam
    assert c.OMEGA == 2.0 * math.pi / math.log(lam)
    assert abs(c.OMEGA - 2.5827069463082895) < 1e-12
    assert c.ONE_PERIOD_DLN_T == math.log(lam)
    assert abs(c.EPS_PREDICTED - math.exp(-math.pi**2 / math.log(lam))) < 1e-15
    assert abs(c.EPS_PREDICTED - 0.0173025) < 5e-6
    assert c.REACH_GATE_PERIODS == 2.8


def test_ladder_teeth():
    assert c.LADDER_TEETH_DEX == (math.log10(1.5), math.log10(1.5**3), math.log10(1.5**6))
    assert c.LADDER_TOL_DEX == 0.05


def test_cross_domain_identity_with_pulsar_leg():
    """The cascade kernel must be the SAME frozen object as tfpt_pulsar's."""
    pulsar_src = Path(__file__).resolve().parents[2] / "pulsar-glitch-recovery" / "src"
    if not pulsar_src.exists():
        return  # standalone checkout: skip silently
    sys.path.insert(0, str(pulsar_src))
    from tfpt_pulsar import constants as pc
    from tfpt_pulsar.nu_recovery import LAMBDA_CASCADE, OMEGA

    assert c.BEND == pc.RECOVERY_BEND
    assert c.LAMBDA_CASCADE == LAMBDA_CASCADE
    assert c.OMEGA == OMEGA


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok {name}")
    print("frozen-kernel guard: ALL OK")

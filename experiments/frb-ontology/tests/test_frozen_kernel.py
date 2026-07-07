"""Guard: the FO kernel constants are exact axiom-derived rationals, frozen.

Run: python tests/test_frozen_kernel.py
"""

import math
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from tfpt_fo import constants as c  # noqa: E402

CHECKS = []


def check(name, ok):
    CHECKS.append((name, bool(ok)))


check("step 2/3 exact", c.STEP == Fraction(2, 3))
check("lambda_T 64/729 exact", c.LAMBDA_T == Fraction(64, 729))
check("lambda_DSI 729/64 exact", c.LAMBDA_DSI == Fraction(729, 64))
check("omega = 2pi/ln(729/64)", abs(c.OMEGA - 2 * math.pi / math.log(729 / 64)) < 1e-15)
check("omega value", abs(c.OMEGA - 2.5827069) < 1e-6)
check("epsilon = exp(-pi^2/lnL)", abs(c.EPSILON_PRED - math.exp(-math.pi ** 2 / math.log(729 / 64))) < 1e-15)
check("epsilon value ~1.73%", abs(c.EPSILON_PRED - 0.0173025) < 1e-6)
check("bend ln3/ln(3/2)", abs(c.BEND - 2.709511) < 1e-6)
check("teeth k=1,3,6", set(c.TIME_TEETH) == {1, 3, 6}
      and abs(c.TIME_TEETH[6] - 729 / 64) < 1e-12
      and abs(c.ENERGY_TEETH[6] - 64 / 729) < 1e-12)
check("no fitted exponents in module", not any(
    "fit_exponent" in n for n in dir(c)))
check("kernel not among placebos", all(abs(p - c.BEND) > 0.2 for p in c.PLACEBO_RATIOS)
      and all(abs(p - 1.5) > 0.2 and abs(p - 3.375) > 0.3 for p in c.PLACEBO_TEETH))

failed = [n for n, ok in CHECKS if not ok]
for n, ok in CHECKS:
    print(("PASS" if ok else "FAIL"), n)
print(f"{len(CHECKS) - len(failed)}/{len(CHECKS)} pass")
if failed:
    raise SystemExit(1)

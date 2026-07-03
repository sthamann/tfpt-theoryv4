"""Guard tests: the kernel is frozen from the axioms; no QPE number leaks in."""

import math
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from qpe_recurrence import kernel  # noqa: E402

FAILS = []


def check(name, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


check("attractor 2/3 exact", kernel.ATTRACTOR == Fraction(2, 3))
check("teeth exact fractions",
      kernel.TEETH["step"] == Fraction(2, 3)
      and kernel.TEETH["amplitude"] == Fraction(8, 27)
      and kernel.TEETH["energy"] == Fraction(64, 729))
check("clock bend = ln3/ln(3/2)",
      abs(kernel.CLOCK_BEND - math.log(3) / math.log(1.5)) < 1e-15)
check("comb omega = 2pi/ln((3/2)^6)",
      abs(kernel.COMB_OMEGA - 2 * math.pi / (6 * math.log(1.5))) < 1e-15)
check("comb eps = exp(-pi^2/ln lambda) ~ 1.727%",
      abs(kernel.COMB_EPS - math.exp(-math.pi ** 2 / (6 * math.log(1.5)))) < 1e-15
      and 0.017 < kernel.COMB_EPS < 0.018)
check("wall N_fam = 3", kernel.N_FAM == 3)

# no QPE magic numbers in the prediction layer
src = (pathlib.Path(__file__).resolve().parents[1] / "src" / "qpe_recurrence"
       / "kernel.py").read_text(encoding="utf-8")
for denied in ("8055", "29757", "33089", "60489", "GSN", "QPE2"):
    check(f"kernel.py contains no data token '{denied}'", denied not in src)

if FAILS:
    raise SystemExit(f"{len(FAILS)} guard test(s) failed: {FAILS}")
print("ALL GUARD TESTS PASS")

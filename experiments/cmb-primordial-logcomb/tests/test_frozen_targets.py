"""Guard: frozen targets + published-bound values (typing cannot drift)."""

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from tfpt_cmblog import analysis as a  # noqa: E402

checks = [
    ("omega frozen", abs(a.OMEGA - 2.0 * math.pi / math.log((3 / 2) ** 6)) < 1e-15),
    ("log10 omega in Planck prior", 0.0 <= math.log10(a.OMEGA) <= 2.1),
    ("epsilon value", abs(a.EPS_PRED - 0.0173025) < 1e-6),
    ("bounds on record", a.BOUND_95 == {"planck2018_x": 0.03, "combined_2024plus": 0.029}),
    ("windows frozen", a.K_FULL == (1e-4, 0.2) and a.K_CONSERVATIVE == (0.005, 0.2)),
    ("prediction below tightest bound", a.EPS_PRED < min(a.BOUND_95.values())),
]
for n, ok in checks:
    print(("PASS" if ok else "FAIL"), n)
print(f"{sum(ok for _, ok in checks)}/{len(checks)} pass")
if not all(ok for _, ok in checks):
    raise SystemExit(1)

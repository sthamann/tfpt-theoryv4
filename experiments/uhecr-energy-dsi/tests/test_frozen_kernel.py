"""Guard: frozen kernel constants + frozen selection/knots (byte-level intent)."""

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from tfpt_uhecr import analysis as a  # noqa: E402

checks = [
    ("omega frozen", abs(a.OMEGA - 2.0 * math.pi / math.log((3 / 2) ** 6)) < 1e-15),
    ("omega value", abs(a.OMEGA - 2.5827069) < 1e-6),
    ("epsilon value", abs(a.EPS_PRED - 0.0173025) < 1e-6),
    ("knots frozen at published features", a.KNOTS_EEV == (0.16, 5.0, 12.6, 45.7)),
    ("thresholds frozen", a.SEL["sd1500"]["thr"] == 2.5 and a.SEL["sd750"]["thr"] == 0.1),
    ("zenith cuts frozen", a.SEL["sd1500"]["zen"] == 60.0 and a.SEL["sd750"]["zen"] == 55.0),
    ("reach gate 2.8", a.REACH_GATE == 2.8),
    ("no fitted exponent symbols", not any("fit_exponent" in n for n in dir(a))),
]
for name, ok in checks:
    print(("PASS" if ok else "FAIL"), name)
print(f"{sum(ok for _, ok in checks)}/{len(checks)} pass")
if not all(ok for _, ok in checks):
    raise SystemExit(1)

"""Guard: the vendored comb kernel must match the original bit-for-bit.

The control experiment is only meaningful if it runs the SAME frozen detector as the TFPT
channels. This test loads the original ``recovery-comb-domains/src/tfpt_combdomains/comb.py``
directly by file path and asserts (a) the axiom-derived constants (omega = 2 pi / ln((3/2)^6),
eps_pred = exp(-pi^2/ln((3/2)^6)) ~ 0.017, the 2.8-period gate, the degree-2 detrend, the 0.05
threshold) are identical, and (b) the comb-gain statistic and the full detector return identical
numbers on a fixed input. Any drift in either file makes this fail — an audit anomaly.

Run (no pytest needed):  PYTHONPATH=src python tests/test_frozen_kernel.py
Or, if pytest is available:  PYTHONPATH=src pytest tests/
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "src"))

ORIGINAL = (HERE.parents[0] / "recovery-comb-domains" / "src" / "tfpt_combdomains" / "comb.py")

from tfpt_dsicontrol import comb as vendored  # noqa: E402


def _load_original():
    spec = importlib.util.spec_from_file_location("tfpt_combdomains_comb_original", ORIGINAL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod   # dataclasses (py>=3.12) resolve __module__ via sys.modules
    spec.loader.exec_module(mod)
    return mod


original = _load_original()


def test_constants_axiom_values():
    """The kernel constants ARE the axiom-derived values (not just copied numbers)."""
    assert vendored.LAMBDA == (3.0 / 2.0) ** 6
    assert vendored.OMEGA == 2.0 * math.pi / math.log((3.0 / 2.0) ** 6)
    assert abs(vendored.OMEGA - 2.5827) < 5e-4
    assert vendored.EPS_PREDICTED == math.exp(-math.pi ** 2 / math.log((3.0 / 2.0) ** 6))
    assert abs(vendored.EPS_PREDICTED - 0.017) < 1e-3


def test_constants_match_original():
    """Every frozen constant equals the original recovery-comb-domains value exactly."""
    for name in ("N_FAM", "P2", "LAMBDA", "OMEGA", "EPS_PREDICTED", "MIN_COMB_PERIODS",
                 "DETREND_DEG", "P_THRESHOLD"):
        assert getattr(vendored, name) == getattr(original, name), name


def _fixture():
    rng = np.random.default_rng(42)
    t = np.logspace(0.0, 3.2, 90)
    y = np.log(t ** -0.9 * (1.0 + 0.05 * np.cos(vendored.OMEGA * np.log(t) + 0.7)))
    return t, y + rng.normal(0.0, 0.05, len(t))


def test_comb_gain_identical():
    """The gain statistic returns bit-identical numbers on a fixed curve."""
    t, y = _fixture()
    lt = np.log(t)
    for omega in (vendored.OMEGA, 1.3, 3.7, 5.9):
        assert vendored._comb_gain(lt, y, omega) == original._comb_gain(lt, y, omega)


def test_detect_comb_identical():
    """The full detector (gain, periodogram-rank p) is bit-identical at fixed seed."""
    t, y = _fixture()
    assert vendored.detect_comb(t, y, seed=3) == original.detect_comb(t, y, seed=3)
    assert vendored.comb_periods(t) == original.comb_periods(t)
    assert vendored.run_comb(t, y, seed=3) == original.run_comb(t, y, seed=3)


if __name__ == "__main__":
    for fn in (test_constants_axiom_values, test_constants_match_original,
               test_comb_gain_identical, test_detect_comb_identical):
        fn()
        print(f"  PASS {fn.__name__}")
    print("frozen-kernel guard: ALL PASS")

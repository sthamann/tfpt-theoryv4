"""Guard tests that freeze the TFPT recovery kernel and keep the prediction
layer free of FRB data constants.

Runnable two ways:
    python tests/test_recovery_kernel_constants.py     # standalone (no pytest)
    pytest tests/                                       # if pytest is installed
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from frb_tfpt import recovery_kernel as K  # noqa: E402

PRED_LAYER = [SRC / "frb_tfpt" / "recovery_kernel.py", SRC / "frb_tfpt" / "tfpt_ladder.py"]


def test_energy_kernel_exact():
    f = K.kernel_fractions()
    assert f["energy_2"] == Fraction(64, 729)
    assert f["energy_3"] == Fraction(1, 729)


def test_field_roots_exact():
    f = K.kernel_fractions()
    assert f["field_2"] == Fraction(8, 27)
    assert f["field_3"] == Fraction(1, 27)


def test_step_exact():
    f = K.kernel_fractions()
    assert f["step_2"] == Fraction(2, 3)
    assert f["step_3"] == Fraction(1, 3)


def test_floats_match_fractions():
    f = K.kernel_fractions()
    assert K.LAMBDA2 == float(f["energy_2"])
    assert K.LAMBDA3 == float(f["energy_3"])
    assert K.SQRT_LAMBDA2 == float(f["field_2"])
    assert K.SQRT_LAMBDA3 == float(f["field_3"])


def test_no_fitted_exponents():
    # no public symbol may hint at a fitted/free exponent
    for name in dir(K):
        assert "fit_exponent" not in name.lower()
        assert "free_exponent" not in name.lower()
    for p in PRED_LAYER:
        src = p.read_text()
        assert "fit_exponent" not in src
        assert "data_io" not in src           # prediction layer must not import data
        for ext in (".tsv", ".csv", ".fits"):
            assert ext not in src             # no dataset references


def test_no_frb_data_constants():
    # no FRB measurement magic numbers may leak into the prediction layer
    forbidden = ["16.35", "528.9", "1652", "6131", "1539", "20180916",
                 "20121102", "20240114", "20240619", "rad m", "Jy"]
    for p in PRED_LAYER:
        src = p.read_text()
        for tok in forbidden:
            assert tok not in src, f"{tok!r} leaked into {p.name}"


def test_preregistration_matches_kernel():
    import yaml  # noqa: PLC0415  (test-only optional dependency)
    yml = Path(__file__).resolve().parents[1] / "hypotheses" / "frb_tfpt_v1.yaml"
    spec = yaml.safe_load(yml.read_text())["kernel"]
    f = K.kernel_fractions()
    assert Fraction(spec["energy"][0]) == f["energy_2"]
    assert Fraction(spec["energy"][1]) == f["energy_3"]
    assert Fraction(spec["field"][0]) == f["field_2"]
    assert Fraction(spec["field"][1]) == f["field_3"]
    assert Fraction(spec["step"][0]) == f["step_2"]
    assert Fraction(spec["step"][1]) == f["step_3"]


def _run() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  [PASS] {t.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  [FAIL] {t.__name__}: {exc}")
    print(f"--- recovery-kernel guard: {len(tests) - failed} passed, {failed} failed ---")
    return failed


if __name__ == "__main__":
    raise SystemExit(1 if _run() else 0)

"""Guard tests for the observable-semantics layer (FRB.02 channel mapping).

The decisive rule: an *energy* column may be tested against the energy ratios
{64/729,1/729} directly, or against the amplitude ratios {8/27,1/27} ONLY after a
sqrt transform. Testing a raw energy ratio against 8/27 is a channel mismatch and
must be flagged ``audit``.

Run: python tests/test_observable_semantics.py   (pytest optional)
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from frb_tfpt import observable_semantics as S  # noqa: E402


def test_energy_column_identity_is_energy_channel():
    assert S.is_theory_valid(True, "identity", "energy") is True
    assert S.is_theory_valid(True, "none", "energy") is True


def test_energy_column_sqrt_is_amplitude_channel():
    assert S.is_theory_valid(True, "sqrt", "amplitude") is True


def test_energy_ratio_vs_amplitude_numbers_is_illegal():
    # E_{n+1}/E_n vs 8/27 is NOT theory-valid (must sqrt first)
    assert S.is_theory_valid(True, "identity", "amplitude") is False
    assert S.is_theory_valid(True, "sqrt", "energy") is False


def test_non_energy_column_has_no_valid_channel():
    assert S.is_theory_valid(False, "identity", "energy") is False
    assert S.is_theory_valid(False, "sqrt", "amplitude") is False


def test_channels_have_correct_targets_and_audit_flag():
    chans = {c.name: c for c in S.energy_ratio_channels(raw_is_energy=True)}
    assert chans["energy"].audit is False and chans["energy"].transform == "identity"
    assert set(chans["energy"].targets) == {"64/729", "1/729"}
    assert chans["amplitude"].audit is False and chans["amplitude"].transform == "sqrt"
    assert set(chans["amplitude"].targets) == {"8/27", "1/27"}
    audit = chans["audit_energy_vs_amplitude_numbers"]
    assert audit.audit is True and set(audit.targets) == {"8/27", "1/27"}


def test_amplitude_hit_equals_energy_squared():
    # sqrt(E) ~ 8/27  <=>  E ~ (8/27)^2 = 64/729  (the core identity)
    assert math.isclose(S.AMPLITUDE_TARGETS["8/27"] ** 2, S.ENERGY_TARGETS["64/729"], rel_tol=1e-12)
    assert math.isclose(S.AMPLITUDE_TARGETS["1/27"] ** 2, S.ENERGY_TARGETS["1/729"], rel_tol=1e-12)


def _run() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t(); print(f"  [PASS] {t.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1; print(f"  [FAIL] {t.__name__}: {exc}")
    print(f"--- observable-semantics: {len(tests) - failed} passed, {failed} failed ---")
    return failed


if __name__ == "__main__":
    raise SystemExit(1 if _run() else 0)

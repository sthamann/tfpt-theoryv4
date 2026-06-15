"""Guard tests for the post-results language rules and verdict consistency.

Run: python tests/test_language_rules_current.py   (pytest optional)
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _yaml():
    return yaml.safe_load((ROOT / "hypotheses" / "frb_tfpt_v1.yaml").read_text())


def test_frb02_clean_null_phrasing_removed():
    allowed = _yaml()["language"]["allowed"]
    assert not any("clean null" in a.lower() for a in allowed), \
        "stale 'FRB.02 clean null' language must be removed"


def test_frb02_audit_candidate_language_present():
    allowed = " ".join(_yaml()["language"]["allowed"]).lower()
    assert "8/27" in allowed and "audit" in allowed


def test_language_patch_flagged():
    assert _yaml()["language"].get("language_patch_after_results") is True


def test_kernel_still_frozen_in_yaml():
    k = _yaml()["kernel"]
    assert k["energy"] == ["64/729", "1/729"]
    assert k["field"] == ["8/27", "1/27"]
    assert k["step"] == ["2/3", "1/3"]


def test_results_verdict_consistent_if_present():
    rj = ROOT / "results" / "results.json"
    if not rj.exists():
        print("  (results.json absent — skipping verdict check)")
        return
    d = json.loads(rj.read_text())
    assert d["overall"]["verdict"] in ("not_confirmed_not_refuted", "confirmed", "refuted")
    # FRB.02 must NOT be a support axis (single source + audit-only excess)
    assert "FRB02_echo_ratio" not in d["overall"]["support_axes"]


def _run() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t(); print(f"  [PASS] {t.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1; print(f"  [FAIL] {t.__name__}: {exc}")
    print(f"--- language-rules: {len(tests) - failed} passed, {failed} failed ---")
    return failed


if __name__ == "__main__":
    raise SystemExit(1 if _run() else 0)

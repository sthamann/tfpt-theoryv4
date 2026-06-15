"""Guard tests for FRB 20240114A burst-count accounting (no 6131/6134 drift).

Run: python tests/test_n_accounting.py   (pytest optional)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import numpy as np  # noqa: E402

from frb_tfpt import load_fast_20240114A_pol  # noqa: E402


def test_loader_n_matches_rows():
    s = load_fast_20240114A_pol()
    if not s.available:
        print("  (FRB 20240114A catalog absent — skipping)")
        return
    # the loader's own source string declares n_raw; it must equal len(series)
    assert "6134" in s.source
    assert len(s) == 6134


def test_results_n_accounting_separated():
    rj = ROOT / "results" / "results.json"
    if not rj.exists():
        print("  (results.json absent — skipping)")
        return
    na = json.loads(rj.read_text())["search_targets"]["FRB04_markov_spectrum"]["n_accounting"]
    for key in ("n_raw", "n_used_pa", "n_used_rm"):
        assert key in na, f"missing {key}"
    assert na["n_raw"] == 6134
    assert na["n_used_pa"] <= na["n_raw"] and na["n_used_rm"] <= na["n_raw"]


def test_no_stale_6131_claim_in_results():
    rj = ROOT / "results" / "results.json"
    if not rj.exists():
        return
    blob = rj.read_text()
    # the only allowed mention of 6131 would be in prose; the loader/source uses 6134
    assert "6131 bursts" not in blob


def _run() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t(); print(f"  [PASS] {t.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1; print(f"  [FAIL] {t.__name__}: {exc}")
    print(f"--- n-accounting: {len(tests) - failed} passed, {failed} failed ---")
    return failed


if __name__ == "__main__":
    raise SystemExit(1 if _run() else 0)

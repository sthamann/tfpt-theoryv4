#!/usr/bin/env python3
"""Frozen-kernel guard: exact E8 ladder values + Cartan-PF identity + detector
sanity on a synthetic known-answer spectrum. Run:
    PYTHONPATH=src python tests/test_ladder_exact.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tfpt_e8lb.ladder import E8_LADDER, pf_ladder, pf_selftest  # noqa: E402
from tfpt_e8lb.recover import recover, random_ladders  # noqa: E402

GOLDEN = (1 + 5 ** 0.5) / 2

# bit-frozen reference values (sympy N(..., 20), see hypotheses YAML)
E8_REF = [1.0, 1.6180339887498948482, 1.9890437907365466738,
          2.4048671723720653480, 2.9562952014676112759, 3.2183404585236657636,
          3.8911568233268538181, 4.7833861167528130669]


def test_exact_values():
    assert np.allclose(E8_LADDER, E8_REF, rtol=0, atol=1e-14), "E8 ladder drifted"
    assert abs(E8_LADDER[1] - GOLDEN) < 1e-14, "m2/m1 != golden ratio"


def test_pf_identity():
    st = pf_selftest()
    assert st["pass"], f"PF self-test failed: {st}"
    assert st["max_rel_dev_vs_zamolodchikov"] < 1e-12
    assert st["rel_dev_eigenvalue"] < 1e-12


def test_pf_alt_ladders_shapes():
    assert len(pf_ladder("A3")) == 3
    assert len(pf_ladder("D8")) == 8


def test_detector_known_answer():
    # synthetic exact E8 spectrum + two contaminant peaks above 2*m1
    m1 = 1.7
    peaks = list(m1 * E8_LADDER) + [2 * m1 * 1.02, m1 * 3.55]
    sigmas = [0.02 * p for p in peaks]
    rec = recover(peaks, sigmas, E8_LADDER)
    assert rec.ok and rec.n_assigned == 8, f"known-answer recovery failed: {rec}"
    assert abs(rec.scale - m1) / m1 < 0.01
    assert rec.chi2_dof < 0.5


def test_detector_rejects_harmonic_spectrum():
    peaks = 1.3 * np.arange(1.0, 9.0)
    sigmas = np.full(8, 0.02)
    rec = recover(peaks, sigmas, E8_LADDER)
    # a harmonic spectrum must not look like a full tight E8 ladder
    assert (not rec.ok) or rec.n_assigned <= 5 or rec.chi2_dof > 2.0


def test_null_ladders_deterministic():
    a = random_ladders(10, 8, 4.78, seed=0)
    b = random_ladders(10, 8, 4.78, seed=0)
    assert np.array_equal(a, b)
    assert np.all(a[:, 0] == 1.0)
    assert np.all(np.diff(a, axis=1) >= 0)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"ALL {len(fns)} TESTS PASSED")

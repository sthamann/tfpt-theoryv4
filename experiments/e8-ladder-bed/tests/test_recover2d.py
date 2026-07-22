#!/usr/bin/env python3
"""Known-answer + sanity tests for the amendment-v2 2D (2DCS) detector. Run:
    PYTHONPATH=src python tests/test_recover2d.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tfpt_e8lb.ladder import E8_LADDER  # noqa: E402
from tfpt_e8lb.recover2d import (build_catalog, mc_pvalue2d,  # noqa: E402
                                 recover2d)
from tfpt_e8lb.synth2d import ka2d_map, neg2d_map  # noqa: E402


def test_catalog_shape_and_content():
    cat = build_catalog(E8_LADDER)
    assert len(cat.xy) == 8 + 56 + 56 == 120
    assert cat.family.count("F1") == 8
    assert cat.family.count("F2") == 56
    assert cat.family.count("F3") == 56
    # F1 entries are exact diagonals
    for k in range(8):
        assert cat.xy[k, 0] == cat.xy[k, 1] == E8_LADDER[k]
        assert cat.rungs[k] == frozenset({k})
    # spot-check one F3 entry: (m6, |m6-m7|)
    i = cat.label.index("F3(6,|6-7|)")
    assert np.isclose(cat.xy[i, 0], E8_LADDER[5])
    assert np.isclose(cat.xy[i, 1], abs(E8_LADDER[5] - E8_LADDER[6]))
    assert cat.rungs[i] == frozenset({5, 6})


def test_known_answer_exact_map():
    """Noise-free E8 2D map -> full coverage, chi2 ~ 0, exact scale."""
    m1 = 0.16
    m = m1 * E8_LADDER
    peaks = [(m[a], m[a]) for a in range(6)]                # F1 diagonals 1..6
    peaks += [(m[1], m[0]),                                 # F2(2,1)
              (m[5], abs(m[5] - m[6])),                     # F3(6,|6-7|)
              (m[4], abs(m[4] - m[7]))]                     # F3(5,|5-8|)
    sigmas = np.full(len(peaks), 0.01)
    rec = recover2d(peaks, sigmas, E8_LADDER)
    assert rec.ok and rec.n_rungs == 8, f"exact-map coverage failed: {rec}"
    assert rec.n_matched == len(peaks)
    assert abs(rec.scale - m1) / m1 < 1e-9
    assert rec.chi2 < 1e-12


def test_known_answer_folding():
    """Negative omega_tau coordinates must fold to the positive quadrant."""
    m1 = 1.0
    peaks = [(-E8_LADDER[a], E8_LADDER[a]) for a in range(4)]
    sigmas = np.full(len(peaks), 0.02)
    rec = recover2d(peaks, sigmas, E8_LADDER)
    assert rec.ok and rec.n_rungs >= 4
    assert abs(rec.scale - m1) < 0.01


def test_ka2d_generator_deterministic():
    a, b = ka2d_map(), ka2d_map()
    assert np.array_equal(a["peaks"], b["peaks"])
    assert len(a["peaks"]) == 11          # 9 catalog peaks + 2 contaminants
    assert np.all(np.abs(a["peaks"]) <= a["window"])


def test_neg2d_generator():
    n = neg2d_map()
    # 18 unique folded coordinates after dedup: many Lehmann pathways coincide
    # exactly (eps_- + eps_+ = 2J = lambda_3, |eps - 2eps| = eps = |eps - GS|,
    # t3 cross peaks coincide with t1/t2 entries)
    assert len(n["peaks"]) == 18
    # eps_pm = J +/- sqrt(2) * J * alpha_yz with J = 2.48, alpha_yz = 0.226
    assert np.isclose(n["eps_minus_mev"], 2.48 - np.sqrt(2) * 2.48 * 0.226)
    assert np.isclose(n["eps_plus_mev"], 2.48 + np.sqrt(2) * 2.48 * 0.226)
    # tetraquark lambda_1 = 2J - sqrt(3) h+
    assert np.isclose(n["q_states_mev"]["lambda_1"],
                      2 * 2.48 - np.sqrt(3) * 2.48 * 0.226)


def test_detector_rejects_harmonic_2d_map():
    """A harmonic 2D map must not look like a tight full E8 catalog."""
    m1 = 0.2
    peaks = [(m1 * k, m1 * k) for k in range(1, 7)]
    peaks += [(m1 * 2, m1 * 1), (m1 * 6, m1 * 1)]
    sigmas = np.full(len(peaks), 0.004)
    rec = recover2d(peaks, sigmas, E8_LADDER)
    assert (not rec.ok) or rec.n_rungs <= 6 or rec.chi2_dof > 2.0, \
        f"harmonic map looked E8-like: {rec}"


def test_null_pruning_consistency():
    """Pruned MC null (coverage bound) must equal the unpruned scan."""
    from tfpt_e8lb.recover import random_ladders
    ka = ka2d_map()
    rec = recover2d(ka["peaks"], ka["sigmas"], E8_LADDER)
    assert rec.ok
    ladders = random_ladders(60, 8, float(E8_LADDER[-1]), seed=0)
    for lad in ladders:
        full = recover2d(ka["peaks"], ka["sigmas"], lad)
        pruned = recover2d(ka["peaks"], ka["sigmas"], lad,
                           min_n_rungs=rec.n_rungs)
        full_good = (full.ok and full.n_rungs >= rec.n_rungs
                     and full.chi2_dof <= rec.chi2_dof)
        pruned_good = (pruned.ok and pruned.n_rungs >= rec.n_rungs
                       and pruned.chi2_dof <= rec.chi2_dof)
        assert full_good == pruned_good, \
            f"pruning changed null outcome for ladder {lad}"


def test_mc_pvalue2d_deterministic():
    ka = ka2d_map()
    rec = recover2d(ka["peaks"], ka["sigmas"], E8_LADDER)
    a = mc_pvalue2d(ka["peaks"], ka["sigmas"], rec, float(E8_LADDER[-1]),
                    n_ladders=100, seed=0)
    b = mc_pvalue2d(ka["peaks"], ka["sigmas"], rec, float(E8_LADDER[-1]),
                    n_ladders=100, seed=0)
    assert a == b


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"ALL {len(fns)} TESTS PASSED")

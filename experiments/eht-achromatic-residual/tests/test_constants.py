"""Audit tests for the TFPT constants.

These tests are the algebraic safety net: every prediction in the EHT
pipeline traces back to phi0 and c3, so any drift between the four
equivalent expressions of the TFPT coupling immediately invalidates
the no-knobs claim.
"""

from __future__ import annotations

import math

import pytest

from tfpt_eht.constants import (
    BETA_DEG,
    BETA_RAD,
    C3,
    DELTA_TOP,
    PHI0,
    TFPT_COUPLING,
    audit_self_consistency,
)


def test_c3_is_one_over_eight_pi():
    assert C3 == pytest.approx(1.0 / (8.0 * math.pi), rel=1e-15)


def test_phi0_matches_paper_value():
    # phi0 = 1/(6 pi) + 3/(256 pi^4) ~ 5.31719522e-2
    expected = 1.0 / (6.0 * math.pi) + 3.0 / (256.0 * math.pi**4)
    assert PHI0 == pytest.approx(expected, rel=1e-15)
    assert PHI0 == pytest.approx(0.0531719522, rel=1e-9)


def test_beta_rad_matches_paper_value():
    # beta_rad = phi0 / (4 pi) ~ 4.2312895e-3 rad
    assert BETA_RAD == pytest.approx(0.0042312895, rel=1e-7)


def test_beta_in_degrees_is_paper_value():
    # beta ~ 0.2424 deg (Paper 3 / Komatsu 2020 comparison value)
    assert BETA_DEG == pytest.approx(0.2424350, rel=1e-5)


def test_delta_top_equals_48_c3_to_the_fourth():
    assert DELTA_TOP == pytest.approx(48.0 * C3**4, rel=1e-15)


def test_tfpt_coupling_three_expressions_agree():
    audit = audit_self_consistency()
    base = audit["TFPT_COUPLING"]
    for name, value in audit.items():
        assert value == pytest.approx(base, rel=1e-14), f"{name} drift: {value}"


def test_tfpt_coupling_equals_one_over_256_pi_fourth():
    assert TFPT_COUPLING == pytest.approx(1.0 / (256.0 * math.pi**4), rel=1e-15)


def test_tfpt_coupling_equals_sixteen_c3_to_fourth():
    assert TFPT_COUPLING == pytest.approx(16.0 * C3**4, rel=1e-15)


def test_tfpt_coupling_equals_delta_top_over_three():
    assert TFPT_COUPLING == pytest.approx(DELTA_TOP / 3.0, rel=1e-15)

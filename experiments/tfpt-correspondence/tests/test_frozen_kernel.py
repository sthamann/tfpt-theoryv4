"""Guard: the correspondence kernel is frozen, axiom-derived, and atom-only (CORR.H4).

Asserts that every phase-boundary constant is EXACTLY the atom rational the preregistration
(hypotheses/correspondence_v1.yaml) names -- no fitted numbers, no SI inputs -- and that the
two order parameters put the critical quotient / window endpoints exactly on those atoms.

Run (no pytest needed):  PYTHONPATH=src python tests/test_frozen_kernel.py
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "src"))

from tfpt_correspondence import atoms as a          # noqa: E402
from tfpt_correspondence import order_parameter as op  # noqa: E402


def test_axioms_and_derived_atoms():
    assert a.C3 == 1.0 / (8.0 * math.pi) and a.G_CAR == 5
    assert a.MU4 == 4 and a.Z2 == 2 and a.N_FAM == 3
    assert a.ANCHOR == (1, 1, 2)
    assert a.E1_ANCHOR == 4 and a.P2_ANCHOR == 6


def test_phase_boundary_constants_are_exact_atoms():
    """CORR.H1: the four boundary constants are exact atom fractions."""
    assert a.BEKENSTEIN_DENSITY == Fraction(1, 4) == Fraction(1, a.MU4)
    assert a.DE_SITTER_ENDPOINT == Fraction(1, 2) == Fraction(a.Z2, a.MU4)
    assert a.NARIAI_THRESHOLD == Fraction(3, 8) == Fraction(a.P2_ANCHOR, a.E1_ANCHOR ** 2)
    assert a.GAP6 == Fraction(64, 729) == Fraction(a.Z2, a.N_FAM) ** (2 * a.N_FAM)
    assert math.isclose(a.FOUR_C3, 1.0 / (2.0 * math.pi), rel_tol=1e-15)
    assert all(holds for _, _, holds in a.atom_lock_table().values())


def test_bekenstein_saturation_is_one_for_all_masses():
    """CORR.H2: the critical quotient q_Bek=1 at the horizon, atom coefficient, any M."""
    for mass in (1.0, 3.7, 1.0e6, 1.0e-3):
        assert math.isclose(op.q_bekenstein_schwarzschild(mass), 1.0, rel_tol=1e-14)
        assert math.isclose(op.schwarzschild_entropy(mass), op.area_over_four(mass), rel_tol=1e-14)


def test_sds_window_endpoints_and_monotone():
    """CORR.H3: Q_geom endpoints hit the atoms 1/2 and 3/8, monotone, ladder ordering."""
    assert math.isclose(op.q_geom(0.0), 0.5, abs_tol=1e-9)          # de Sitter -> |Z2|/|mu4|
    assert math.isclose(op.q_geom(1.0 / 3.0), 0.375, abs_tol=1e-9)  # Nariai -> p2(a)/e1(a)^2
    win = op.compactness_window()
    assert win["monotone_decreasing"] and win["ladder_1_3_lt_3_8_lt_4_9_lt_1_2"]
    # ladder ordering with the atoms as exact fractions
    assert a.PHOTON_SPHERE < a.NARIAI_THRESHOLD < a.BUCHDAHL < a.HORIZON


def test_no_hagedorn_or_string_scale():
    """CORR.H4: kernel exposes no dimensionful new scale (not Horowitz-Polchinski)."""
    names = dir(a)
    assert not any(k.lower().startswith(("hagedorn", "string", "alpha_prime", "ls_"))
                   for k in names)


def test_echo_template_atom_locked():
    """CORR.H5: the observable echo uses the atom amplitude (2/3)^6 and the 3/8 ECO surface;
    delay matches the gravastar-compactness value 2.288 M."""
    echo = op.echo_template()
    assert math.isclose(echo["amplitude_ratio_bound"], 64.0 / 729.0, rel_tol=1e-15)
    assert math.isclose(echo["surface_radius_over_M"], 8.0 / 3.0, rel_tol=1e-12)  # C=3/8
    assert math.isclose(echo["delay_over_M"], 2.288, abs_tol=2e-3)  # cross-check gravastar
    # GW150914 (62 Msun, source frame) ~ 0.70 ms
    assert math.isclose(echo["echo_delay_ms_source_frame"]["GW150914_62Msun"], 0.70, abs_tol=0.02)


if __name__ == "__main__":
    for fn in (test_axioms_and_derived_atoms,
               test_phase_boundary_constants_are_exact_atoms,
               test_bekenstein_saturation_is_one_for_all_masses,
               test_sds_window_endpoints_and_monotone,
               test_no_hagedorn_or_string_scale,
               test_echo_template_atom_locked):
        fn()
        print(f"  PASS {fn.__name__}")
    print("frozen-kernel guard: ALL PASS")

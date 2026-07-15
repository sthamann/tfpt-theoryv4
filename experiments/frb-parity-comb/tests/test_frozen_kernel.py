"""Byte-guard: the frozen kernel constants must match the preregistered YAML."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tfpt_pc import constants as C  # noqa: E402


def test_frozen_tones():
    assert abs(C.OMEGA_1 - 2.0 * math.pi / math.log(1.5 ** 6)) < 1e-15
    assert abs(C.OMEGA_1 - 2.582706946308289) < 1e-12
    assert abs(C.OMEGA_2 - 2.0 * math.pi / math.log(3.0 ** 6)) < 1e-15
    assert abs(C.OMEGA_2 - 0.953200289126709) < 1e-12
    assert abs(C.OMEGA_3 - 2.0 * math.pi / math.log(2.0 ** 6)) < 1e-15


def test_frozen_budget_and_gates():
    assert abs(C.EPS_BASE - math.exp(-math.pi ** 2 / math.log(1.5 ** 6))) < 1e-15
    assert C.COMB2_FADING_PER_PERIOD == 2.0 ** -6 == 1 / 64
    assert C.REACH_GATE_PERIODS == 2.8 and C.MIN_BURSTS_USED == 30
    assert C.SESSION_GAP_D == 0.2 and C.TAU_GATE_S == 0.5
    assert C.VSIGN_MIN_ABS_PCT == 5.0 and C.VSIGN_MIN_SIGMA == 2.0


def test_no_fitted_numbers():
    assert C.C3 == 1.0 / (8.0 * math.pi) and C.G_CAR == 5 and C.N_FAM == 3


if __name__ == "__main__":
    test_frozen_tones()
    test_frozen_budget_and_gates()
    test_no_fitted_numbers()
    print("frozen-kernel guard: ALL PASS")

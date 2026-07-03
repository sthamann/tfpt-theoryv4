"""FROZEN recovery kernel — exact values from the two axioms; no QPE number
enters this module (guarded by tests/test_frozen_kernel.py).

Identical to the repeater-cascade / pulsar-glitch-recovery kernels.
"""

from __future__ import annotations

import math
from fractions import Fraction

ATTRACTOR = Fraction(2, 3)                      # |Z2| / N_fam
TRANSPORT_EXPONENT = 6                          # Z6/A3 cycle
N_FAM = 3

TEETH = {
    "step": Fraction(2, 3),                     # 2/3
    "amplitude": Fraction(2, 3) ** 3,           # 8/27
    "energy": Fraction(2, 3) ** 6,              # 64/729
}

CLOCK_BEND = math.log(3.0) / math.log(1.5)      # 2.709511291351...
COMB_LAMBDA = 1.5 ** 6
COMB_OMEGA = 2.0 * math.pi / math.log(COMB_LAMBDA)          # 2.582993...
COMB_EPS = math.exp(-math.pi ** 2 / math.log(COMB_LAMBDA))  # 0.01727...
RANGE_GATE_PERIODS = 2.8                        # hard ln-range gate (PG.06)

TOLERANCE_DEX = 0.10
PLACEBO_RATIOS = (1.7, 2.2, 3.3, 4.5)

"""FROZEN kernel constants from the two TFPT axioms (c3 = 1/(8*pi), g_car = 5).

Identical to the FRB/GW/pulsar kernels in the sibling experiments; frozen as
targets, never fitted. Guarded by tests/test_frozen_kernel.py.
"""

from __future__ import annotations

import math
from fractions import Fraction

N_FAM = 3
Z2 = 2

STEP = Fraction(Z2, N_FAM)                    # 2/3
LAMBDA_T = STEP ** 6                          # 64/729  (transfer contraction)
LAMBDA_DSI = Fraction(N_FAM, Z2) ** 6         # 729/64  (log scale factor)

LN_LAMBDA = math.log(float(LAMBDA_DSI))       # 6 ln(3/2) = 2.4327902
OMEGA = 2.0 * math.pi / LN_LAMBDA             # 2.5830 (comb frequency)
EPSILON_PRED = math.exp(-math.pi ** 2 / LN_LAMBDA)   # 0.01734 (comb amplitude)
BEND = math.log(N_FAM) / math.log(N_FAM / Z2)        # ln3/ln(3/2) = 2.709511

TIME_TEETH = {k: (N_FAM / Z2) ** k for k in (1, 3, 6)}      # 1.5, 3.375, 11.39
ENERGY_TEETH = {k: (Z2 / N_FAM) ** k for k in (1, 3, 6)}    # partner teeth

TOL_DEX = 0.10
REACH_GATE_PERIODS = 2.8

PLACEBO_RATIOS = (1.5, 2.0, 3.5, 4.5)         # FO.02 bend placebos
PLACEBO_TEETH = (1.8, 2.5, 4.0)               # FO.05 tooth placebos

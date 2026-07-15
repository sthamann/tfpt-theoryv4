"""Frozen prediction layer for the parity-comb search (byte-matches
hypotheses/parity_comb_v1.yaml; guarded in tests/).

Everything derives from the two TFPT axioms; no SI value, no FRB number.
The NEW ingredient vs repeater-cascade is the v486 parity assignment:
lambda_2 = (2/3)^6 on the Z2-EVEN pair eigenvector (1,1) -> intensity comb
omega_1; lambda_3 = (1/3)^6 on the Z2-ODD eigenvector (1,-1) -> handedness
comb omega_2; relative comb-2 amplitude fades 2^-6 per period (S-b budget).
"""
from __future__ import annotations

import math

PI = math.pi
C3 = 1.0 / (8.0 * PI)                                    # P1
G_CAR = 5                                                # P2
N_FAM = 3
P2_EXP = 6                                               # |R^+(A_3)|

LAMBDA_EVEN = 1.5 ** P2_EXP                              # (3/2)^6 = 729/64
OMEGA_1 = 2.0 * PI / math.log(LAMBDA_EVEN)               # 2.5827069...
LAMBDA_ODD = 3.0 ** P2_EXP                               # 3^6 = 729
OMEGA_2 = 2.0 * PI / math.log(LAMBDA_ODD)                # 0.9531628...
LAMBDA_RATIO = 2.0 ** P2_EXP                             # 2^6 = 64
OMEGA_3 = 2.0 * PI / math.log(LAMBDA_RATIO)              # 1.5108406...

EPS_BASE = math.exp(-PI ** 2 / math.log(LAMBDA_EVEN))    # 0.0173042...
COMB2_FADING_PER_PERIOD = 2.0 ** (-P2_EXP)               # 1/64 (S-b)

REACH_GATE_PERIODS = 2.8
RELAXED_GATE_PERIODS = 1.2          # PC.02 secondary (exploratory, labelled)
MIN_BURSTS_USED = 30
RELAXED_MIN_BURSTS = 60
SESSION_GAP_D = 0.2
TAU_GATE_S = 0.5
VSIGN_MIN_ABS_PCT = 5.0
VSIGN_MIN_SIGMA = 2.0

N_SIGN_PERM = 2000
N_SURROGATE = 200
OFFTONE_LO, OFFTONE_HI, N_OFFTONE = 0.3, 6.5, 150


def summary() -> dict[str, float]:
    return {
        "c3": C3, "g_car": float(G_CAR), "N_fam": float(N_FAM),
        "omega_1": OMEGA_1, "omega_2": OMEGA_2, "omega_3": OMEGA_3,
        "eps_base": EPS_BASE, "comb2_fading": COMB2_FADING_PER_PERIOD,
        "reach_gate_periods": REACH_GATE_PERIODS,
    }

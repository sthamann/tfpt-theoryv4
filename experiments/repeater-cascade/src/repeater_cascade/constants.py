"""Frozen TFPT prediction layer for the repeater-cascade search.

Everything here is *derived* from the two TFPT axioms (identical to
``verification/tfpt_constants.py`` and the FRB/GW/pulsar experiments):

    P1   c3    = 1 / (8*pi)          seam / boundary constant
    P2   g_car = 5                   carrier rank

No SI value and no FRB number is hard-coded.  The dynamic kernel is the *same*
frozen object tested in PG.04c/PG.05/PG.07 (pulsar-glitch-recovery), FRB.09
(frb-tfpt-signatures) and the GW Stage-2 identifiability analysis:

  * the resummed recovery clock  rate(n) = -6 ln(1 - n/3)  (v124/v126/v147)
    with the det'-clean two-mode BEND rate(2)/rate(1) = ln3/ln(3/2) = 2.7095
    and the WALL at n = N_fam = 3 (at most two decay modes + floor);
  * the log-periodic recovery COMB at omega = 2*pi/ln((3/2)^6) = 2.583 with
    predicted ripple eps = exp(-pi^2/ln lambda) ~ 1.7% -- the one signature the
    GW Stage-2 analysis proved is NOT degenerate with a monotone recovery,
    PROVIDED the ln(t) reach exceeds ~2.8 comb periods (PG.06 machine check);
  * the static ladder teeth {log 3/2, log (3/2)^3, log (3/2)^6} -- the tooth set
    IS the step/amplitude/energy semantics battery (PG.02/PG.03 convention).

These are *targets to test against*, never fitted parameters.  The values must
match ``hypotheses/repeater_cascade_v1.yaml`` byte-for-byte (guarded in tests/).
"""

from __future__ import annotations

import math

PI: float = math.pi
C3: float = 1.0 / (8.0 * PI)                              # P1
G_CAR: int = 5                                            # P2

N_FAM: int = 3
P2_EXP: int = 6                                           # |R^+(A_3)|, transport-cycle exponent

# --- the resummed recovery clock (v124): rate(n) = -P2_EXP * ln(1 - n/N_FAM) ---
RECOVERY_RATE_1: float = P2_EXP * math.log(1.5)           # 6 ln(3/2) = 2.4328
RECOVERY_RATE_2: float = P2_EXP * math.log(3.0)           # 6 ln 3    = 6.5917
BEND: float = math.log(3.0) / math.log(1.5)               # rate(2)/rate(1) = 2.70951...
WALL: int = N_FAM                                         # >= 3 robust decay modes is a tension

# --- the log-periodic cascade comb -------------------------------------------
LAMBDA_CASCADE: float = 1.5**P2_EXP                       # (3/2)^6 = 729/64
OMEGA: float = 2.0 * PI / math.log(LAMBDA_CASCADE)        # 2.58270693...
ONE_PERIOD_DLN_T: float = math.log(LAMBDA_CASCADE)        # 2.43279... per comb period
EPS_PREDICTED: float = math.exp(-PI**2 / math.log(LAMBDA_CASCADE))   # 0.01730...
REACH_GATE_PERIODS: float = 2.8                           # PG.06 machine-checked gate
EPS_REFERENCE: float = 0.30                               # injection reference amplitude (PG.06/07)

# --- the static ladder teeth (PG.02/PG.03 semantics battery) ------------------
LADDER_TEETH_DEX: tuple[float, float, float] = (
    math.log10(1.5),                                      # step  3/2
    math.log10(1.5**3),                                   # amplitude reading (3/2)^3
    math.log10(1.5**6),                                   # energy reading (3/2)^6
)
LADDER_TOL_DEX: float = 0.05


def summary() -> dict[str, float]:
    """Numeric snapshot printed by ``tfpt-cascade audit``."""
    return {
        "c3": C3, "g_car": float(G_CAR), "N_fam": float(N_FAM), "p2_exp": float(P2_EXP),
        "rate(1)=6ln(3/2)": RECOVERY_RATE_1, "rate(2)=6ln3": RECOVERY_RATE_2,
        "bend=ln3/ln(3/2)": BEND, "wall_N_fam": float(WALL),
        "lambda=(3/2)^6": LAMBDA_CASCADE, "omega=2pi/ln(lambda)": OMEGA,
        "one_period_dln_t": ONE_PERIOD_DLN_T, "eps_predicted": EPS_PREDICTED,
        "reach_gate_periods": REACH_GATE_PERIODS,
        "tooth_3/2_dex": LADDER_TEETH_DEX[0], "tooth_(3/2)^3_dex": LADDER_TEETH_DEX[1],
        "tooth_(3/2)^6_dex": LADDER_TEETH_DEX[2],
    }

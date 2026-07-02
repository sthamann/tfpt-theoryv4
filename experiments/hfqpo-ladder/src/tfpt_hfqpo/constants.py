"""Frozen TFPT prediction layer for the hfqpo-ladder search.

Everything here is *derived* from the two TFPT axioms (P1: c3 = 1/(8 pi), P2: g_car = 5),
identical to the constants layer of the FRB / pulsar / repeater-cascade experiments. No SI
value and no QPO number is hard-coded.

The tested object is the RELAXATION-LADDER step

    step = N_fam / (N_fam - 1) = 3/2        (N_fam = 3)

i.e. the consecutive scale factor of the frozen geometric mode ladder whose 6-fold transport
cycle gives the shared comb scale lambda = (3/2)^6 and omega = 2 pi / ln(lambda) = 2.5827
tested in recovery-comb-domains / pulsar-glitch-recovery / FRB.09 / repeater-cascade.

Semantics warning (the firewall in code): mapping a two-oscillator HFQPO frequency RATIO onto
this ladder step is NON-CANONICAL — TFPT derives no HFQPO production mechanism. The kernel
reading is only discriminated from the GR 3:2 parametric resonance by the LADDER prediction:

    geometric ladder:  nu_l -> nu_u = (3/2) nu_l -> nu_3 = (3/2)^2 nu_l   and NO integer lines
    integer harmonics: nu_0 = nu_u/3 = nu_l/2; lines at k * nu_0          (the resonance world)

These values must match ``hypotheses/hfqpo_v1.yaml`` (guarded in tests/).
"""

from __future__ import annotations

import math
from fractions import Fraction

PI: float = math.pi
C3: float = 1.0 / (8.0 * PI)                          # P1
G_CAR: int = 5                                        # P2

N_FAM: int = 3
P2_EXP: int = 6                                       # |R^+(A_3)|, transport-cycle exponent

# --- the ladder step, EXACT rational from N_fam (no fitted exponent) --------------------
STEP: Fraction = Fraction(N_FAM, N_FAM - 1)           # 3/2 exact
STEP_F: float = float(STEP)                           # 1.5

# --- consistency with the shared dynamic kernel ------------------------------------------
LAMBDA: float = STEP_F ** P2_EXP                      # (3/2)^6 = 11.390625
OMEGA: float = 2.0 * PI / math.log(LAMBDA)            # 2.58270693...
EPS_PREDICTED: float = math.exp(-PI ** 2 / math.log(LAMBDA))   # ~0.0173 (QT.02 law)

# --- H2 selection-null frozen design (hypotheses/hfqpo_v1.yaml) --------------------------
H2_N_MC: int = 200_000
H2_N_SOURCES: int = 5
H2_SEED: int = 0
H2_WINDOW: float = 0.05          # cluster criterion: within +-0.05 of 3/2
H2_CLUSTER_K: int = 4            # ">= 4 of 5 sources"
H2_SEL_WIDTH_X: float = 0.06     # equal-rms detection window along the correlation
H2_MEAS_SIGMA_R: float = 0.044   # median published sigma_r of the five measured pairs
H2_NU_L_LO: float = 100.0        # nu_l = 100 + 400 x  (GR-like span of lower HFQPOs)
H2_NU_L_SPAN: float = 400.0
H2_RATIO_AT_0: float = 2.2       # r(x) = 2.2 - x: monotone ratio decrease toward ISCO,
H2_RATIO_SLOPE: float = -1.0     # crossing 3/2 at x_eq = 0.7 (the Torok-2009 equal-rms point)
H2_X_EQ_ANCHORED: float = 0.7


def ladder_tooth(nu_upper: float) -> float:
    """The preregistered third-tooth frequency nu_3 = (3/2) * nu_upper."""
    return STEP_F * nu_upper


def harmonic_fundamental(nu_upper: float) -> float:
    """The integer-harmonic fundamental nu_0 = nu_upper / 3 (= nu_lower / 2 for a 3:2 pair)."""
    return nu_upper / 3.0


def summary() -> dict[str, float]:
    """Numeric snapshot printed by ``tfpt-hfqpo audit``."""
    return {
        "c3": C3, "g_car": float(G_CAR), "N_fam": float(N_FAM), "p2_exp": float(P2_EXP),
        "step=3/2": STEP_F, "lambda=(3/2)^6": LAMBDA,
        "omega=2pi/ln(lambda)": OMEGA, "eps_predicted": EPS_PREDICTED,
    }

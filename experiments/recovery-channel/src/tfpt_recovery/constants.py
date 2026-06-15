"""Frozen TFPT boundary-recovery kernel (the channel spectrum).

The recovery transport is, in the suite (v160/v161/v155), the Bogoliubov second
quantisation Gamma(t) of a one-particle contraction t whose spectrum is the frozen
Page/flavor kernel. Energy channel:

    spec(t)        = { 1, (2/3)^6, (1/3)^6 }        (information / energy survival)
    amplitude      = { 1, (2/3)^3, (1/3)^3 } = {1, 8/27, 1/27}
    gap Delta      = 6 ln(3/2)
    2/3 = |Z2|/N_fam,  exponent 6 = |R^+(A_3)| (the Z6/A3 cycle)

All from c3 = 1/(8pi), g_car = 5 (no fit). This module turns that spectrum into an
explicit CPTP map and checks the channel axioms / Page curve (channel.py, page_curve.py).
"""

from __future__ import annotations

import math

N_FAM: int = 3
P2: int = 6                                   # |R^+(A_3)|, the transport-cycle exponent
TWO_THIRDS: float = 2.0 / 3.0

LAMBDA = (1.0, TWO_THIRDS**P2, (1.0 / 3.0) ** P2)          # 1, 64/729, 1/729
AMPLITUDE = (1.0, TWO_THIRDS ** (P2 // 2), (1.0 / 3.0) ** (P2 // 2))  # 1, 8/27, 1/27
DELTA_GAP: float = P2 * math.log(1.5)         # 6 ln(3/2) ~ 2.4328
C3: float = 1.0 / (8.0 * math.pi)             # seam constant (Hawking law, Page time)


def summary() -> dict[str, float]:
    return {
        "lambda_1": LAMBDA[0], "lambda_2_(2/3)^6": LAMBDA[1], "lambda_3_(1/3)^6": LAMBDA[2],
        "amp_2_(8/27)": AMPLITUDE[1], "amp_3_(1/27)": AMPLITUDE[2],
        "delta_gap": DELTA_GAP, "c3": C3, "N_fam": float(N_FAM), "p2": float(P2),
    }

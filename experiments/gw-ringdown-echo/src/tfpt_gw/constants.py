"""Frozen TFPT ringdown-echo constants.

search.txt sec.5 / horizon readouts: IF post-merger boundary recovery imprints
echoes on the ringdown, their amplitude ratio is bounded by the SAME recovery
eigenvalue that governs FRBs and flavour,

    A_{n+1} / A_n  <=  lambda2 = (2/3)^6 = 64/729 ~ 0.08779 .

This is an UPPER bound (echoes may be absent or smaller), so the GW channel is a
consistency / upper-limit test: a detected echo with ratio >> (2/3)^6 would be
against TFPT; a non-detection is consistent. The lag is free (object-dependent);
only the ratio is frozen.
"""

from __future__ import annotations

STAGE: str = "catalog_feasibility"              # NOT a strain-level echo test
RATIO: float = (2.0 / 3.0) ** 6                 # 64/729, the frozen echo amplitude bound
# geometric echo train sum_{n>=1} ratio^(2n) -> total echo power factor
ECHO_POWER_FACTOR: float = RATIO / (1.0 - RATIO**2) ** 0.5    # ~ratio (small)
# typical fraction of the network matched-filter SNR carried by the ringdown for
# comparable-mass BBH (order-of-magnitude; Berti+ 2006, Kamaretsos+ 2012)
RINGDOWN_FRACTION: float = 0.3
DET_THRESHOLD: float = 5.0                       # nominal single/stacked detection SNR


def summary() -> dict[str, float]:
    return {
        "ratio_(2/3)^6": RATIO,
        "echo_power_factor": ECHO_POWER_FACTOR,
        "ringdown_fraction": RINGDOWN_FRACTION,
        "det_threshold": DET_THRESHOLD,
    }

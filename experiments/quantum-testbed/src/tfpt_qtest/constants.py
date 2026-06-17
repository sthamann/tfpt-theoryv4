"""Frozen TFPT kernel for the quantum testbed (identical to recovery-channel).

Derived from the two axioms ``c3 = 1/(8 pi)``, ``g_car = 5``; no fit.  The recovery
transport is the Bogoliubov second quantisation ``Gamma(t)`` of a one-particle
contraction whose spectrum is the frozen Page/flavor kernel (suite v155/160/161):

    energy spectrum    {1, (2/3)^6, (1/3)^6}     (the correlation/occupation eigenvalues)
    amplitude          {1, (2/3)^3, (1/3)^3}
    gap                Delta = 6 ln(3/2)
    wall               N_fam = 3   (the recovery clock stops at 3 = rank A3)

This module supplies the kernel + the candidate *ladder ratios* whose dynamical
(discrete-scale-invariance) fingerprint the quench tests probe.
"""

from __future__ import annotations

import math

PI: float = math.pi
C3: float = 1.0 / (8.0 * PI)
G_CAR: int = 5
PHI0: float = 1.0 / (6.0 * PI) + 3.0 / (256.0 * PI**4)
N_FAM: int = 3
P2_EXP: int = 6
TWO_THIRDS: float = 2.0 / 3.0

LAMBDA = (1.0, TWO_THIRDS**P2_EXP, (1.0 / 3.0) ** P2_EXP)            # 1, 64/729, 1/729
AMPLITUDE = (1.0, TWO_THIRDS ** (P2_EXP // 2), (1.0 / 3.0) ** (P2_EXP // 2))  # 1, 8/27, 1/27
DELTA_GAP: float = P2_EXP * math.log(1.5)                            # 6 ln(3/2) ~ 2.4328


def ladder_ratios() -> dict[str, float]:
    """Kernel-derived geometric ladder ratios whose DSI log-frequency the quench
    tests.  Spans the carrier step up to the energy gap (the coarsest natural ratio)."""
    return {
        "3/2 (carrier)": 1.5,
        "(3/2)^3 (amplitude gap)": 27 / 8,
        "(3/2)^6 (energy gap)": 729 / 64,
        "2^6 (mode-2/mode-3 ratio)": 64.0,
    }


def summary() -> dict[str, float]:
    return {
        "c3": C3, "g_car": float(G_CAR), "phi0": PHI0, "N_fam": float(N_FAM),
        "kernel_energy_(2/3)^6": LAMBDA[1], "kernel_energy_(1/3)^6": LAMBDA[2],
        "kernel_amp_(2/3)^3": AMPLITUDE[1], "delta_gap_6ln(3/2)": DELTA_GAP,
        "(3/2)^6": 729 / 64,
    }

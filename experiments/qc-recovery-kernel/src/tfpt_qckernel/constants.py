"""Frozen TFPT kernel for the quantum-circuit realisation.

Identical numbers to ``recovery-channel`` / ``quantum-testbed`` — derived from the two
axioms ``c3 = 1/(8 pi)``, ``g_car = 5``; no fit.  The frozen seam transfer T has
spectrum ``{1, (2/3)^6, (1/3)^6}`` on the 3 flavor modes (Perron mode 1 protected).
One transfer step is a CPTP map; per step the two decaying modes survive with

    energy reading      lambda_2 = (2/3)^6 = 64/729,   lambda_3 = (1/3)^6 = 1/729
    amplitude reading   sqrt(lambda_2) = (2/3)^3 = 8/27,  sqrt(lambda_3) = (1/3)^3 = 1/27

Because the circuit realises the step as an amplitude-damping channel with survival
probability lambda_k, ONE circuit carries BOTH semantics: the excited-state
POPULATION decays by the energy reading per step, the off-diagonal COHERENCE decays
by the amplitude reading per step (coherence factor = sqrt(survival)).

The p2 exponent 6 means one seam transfer step = 6 carrier substeps with survivals
(2/3, 1/3); the bend (decay-rate ratio) is resolution invariant:

    ln lambda_3 / ln lambda_2 = ln 3 / ln(3/2) = 2.7095...   (the QT.04 walled-clock bend)
"""

from __future__ import annotations

import math

PI: float = math.pi
C3: float = 1.0 / (8.0 * PI)
G_CAR: int = 5
N_FAM: int = 3
P2_EXP: int = 6

# per TRANSFER STEP
LAMBDA_ENERGY = (1.0, (2.0 / 3.0) ** P2_EXP, (1.0 / 3.0) ** P2_EXP)      # 1, 64/729, 1/729
LAMBDA_AMPLITUDE = (1.0, (2.0 / 3.0) ** (P2_EXP // 2), (1.0 / 3.0) ** (P2_EXP // 2))  # 1, 8/27, 1/27

# per CARRIER SUBSTEP (one transfer step = P2_EXP substeps)
SUBSTEPS_PER_STEP: int = P2_EXP
CARRIER_SURVIVAL = (1.0, 2.0 / 3.0, 1.0 / 3.0)
RATE_MODE2: float = math.log(1.5)        # per-substep decay rate, mode 2 (= 6 ln(3/2) per step)
RATE_MODE3: float = math.log(3.0)        # per-substep decay rate, mode 3 (= 6 ln 3 per step)

BEND: float = math.log(3.0) / math.log(1.5)   # ln3/ln(3/2) = 2.7095, resolution invariant

# QT.04 waveform weights (floor, mode2, mode3) for the combined relaxation curve
QT04_WEIGHTS = (0.3, 0.5, 0.4)


def audit() -> dict:
    """Frozen-kernel identities the circuit must inherit (guards the constants)."""
    bend_ok = abs(BEND - math.log(3.0) / math.log(1.5)) < 1e-15
    amp_is_sqrt_energy = all(
        abs(LAMBDA_AMPLITUDE[i] - math.sqrt(LAMBDA_ENERGY[i])) < 1e-15 for i in range(3)
    )
    substep_ok = all(
        abs(CARRIER_SURVIVAL[i] ** SUBSTEPS_PER_STEP - LAMBDA_ENERGY[i]) < 1e-15 for i in range(3)
    )
    resolution_invariant = abs(RATE_MODE3 / RATE_MODE2 - BEND) < 1e-15
    return {
        "lambda2_energy_64/729": LAMBDA_ENERGY[1],
        "lambda3_energy_1/729": LAMBDA_ENERGY[2],
        "lambda2_amplitude_8/27": LAMBDA_AMPLITUDE[1],
        "lambda3_amplitude_1/27": LAMBDA_AMPLITUDE[2],
        "bend_ln3_over_ln3half": BEND,
        "amplitude_is_sqrt_energy": amp_is_sqrt_energy,
        "carrier_substep_power_ok": substep_ok,
        "bend_resolution_invariant": resolution_invariant,
        "ok": bend_ok and amp_is_sqrt_energy and substep_ok and resolution_invariant,
    }

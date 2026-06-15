"""Observable-semantics layer — which kernel channel a measured ratio may target.

The TFPT kernel has three readouts (see `recovery_kernel`):

    energy / information :  { 64/729, 1/729 }     reads  lambda      (~ E)
    amplitude / visibility: { 8/27,  1/27 }       reads  sqrt(lambda) (~ A = sqrt(E))
    sub-burst step        : { 2/3,   1/3 }        reads  the unpowered step

This module enforces the mapping so a test can never silently compare the wrong
quantity to the wrong number. The decisive example: a FAST burst catalogue gives
*energy* `E` (erg). Then

    E_{n+1}/E_n      may target only the ENERGY ratios   {64/729, 1/729},
    sqrt(E_{n+1}/E_n) may target only the AMPLITUDE ratios {8/27,   1/27}.

Because `A = sqrt(E)`, an amplitude hit at 8/27 is *identical* to an energy hit
at (8/27)^2 = 64/729. Testing an energy ratio directly against 8/27 is a channel
mismatch and is only ever reported as an explicitly-flagged ``audit`` result.
"""

from __future__ import annotations

from dataclasses import dataclass

from .recovery_kernel import (
    LAMBDA2,
    LAMBDA3,
    ONE_THIRD,
    SQRT_LAMBDA2,
    SQRT_LAMBDA3,
    TWO_THIRDS,
)

ENERGY_TARGETS: dict[str, float] = {"64/729": LAMBDA2, "1/729": LAMBDA3}
AMPLITUDE_TARGETS: dict[str, float] = {"8/27": SQRT_LAMBDA2, "1/27": SQRT_LAMBDA3}
STEP_TARGETS: dict[str, float] = {"2/3": TWO_THIRDS, "1/3": ONE_THIRD}


@dataclass(frozen=True)
class RatioChannel:
    """A legitimate (transform, target-set) pairing for a *consecutive ratio*
    of a raw quantity, plus an ``audit`` flag for theory-illegal pairings."""

    name: str
    transform: str            # how the raw energy ratio R_E is mapped: "identity" | "sqrt"
    targets: dict[str, float]
    audit: bool               # True => not theory-justified, never feeds support
    note: str


def energy_ratio_channels(raw_is_energy: bool = True) -> list[RatioChannel]:
    """The channels to run on a *consecutive energy ratio* `R_E = E_{n+1}/E_n`.

    With an energy column the only theory-valid pairings are
    (identity -> energy targets) and (sqrt -> amplitude targets). Testing the raw
    energy ratio against the amplitude numbers is included but flagged ``audit``.
    """
    if not raw_is_energy:
        raise ValueError("energy_ratio_channels expects an energy-like column")
    return [
        RatioChannel("energy", "identity", ENERGY_TARGETS, False,
                     "E_{n+1}/E_n vs {64/729,1/729} (energy readout)"),
        RatioChannel("amplitude", "sqrt", AMPLITUDE_TARGETS, False,
                     "sqrt(E_{n+1}/E_n) vs {8/27,1/27} (amplitude readout; "
                     "== energy ratio vs (8/27)^2=64/729)"),
        RatioChannel("audit_energy_vs_amplitude_numbers", "identity", AMPLITUDE_TARGETS, True,
                     "E_{n+1}/E_n vs {8/27,1/27} -- CHANNEL MISMATCH, not theory; "
                     "reported only as an audit anomaly"),
    ]


def is_theory_valid(raw_is_energy: bool, transform: str, target_channel: str) -> bool:
    """Guard used by tests/fingerprint: is this (column, transform, channel) legal?"""
    if not raw_is_energy:
        return False
    if target_channel == "energy":
        return transform in ("identity", "none")
    if target_channel == "amplitude":
        return transform == "sqrt"
    return False

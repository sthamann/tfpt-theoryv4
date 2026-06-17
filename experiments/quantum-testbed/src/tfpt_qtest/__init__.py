"""TFPT quantum testbed -- catch the algebra at work.

Internal-consistency companion to `recovery-channel`: build the frozen kernel as a
quantum object (entanglement spectrum + quench dynamics) and check the predicted
patterns.  The headline is the *reconsidered* signature class: the kernel shows up
**dynamically** as discrete scale invariance (log-periodic recovery at omega=2pi/ln
lambda), with an exp(-pi^2/ln lambda)-suppressed amplitude that is detectable only for
the coarse energy-gap ratio (3/2)^6 -- explaining the static-ratio nulls and pointing
to recovery *waveforms* as the next probe.  No external data.
"""

from __future__ import annotations

from . import constants, dsi
from .clock import (
    clock_identities,
    clock_rate,
    matched_filter_discriminate,
    recovery_curve,
)
from .entanglement import EntanglementReport, entanglement_spectrum
from .mtc import MTCReport, mtc_signatures, monodromy, theta
from .quench import (
    freefermion_otoc,
    kernel_ladder_hamiltonian,
    nongeometric_control,
    recovery_dsi_scan,
)

__all__ = [
    "constants",
    "dsi",
    "EntanglementReport",
    "entanglement_spectrum",
    "recovery_dsi_scan",
    "nongeometric_control",
    "freefermion_otoc",
    "kernel_ladder_hamiltonian",
    "clock_identities",
    "clock_rate",
    "recovery_curve",
    "matched_filter_discriminate",
    "MTCReport",
    "mtc_signatures",
    "monodromy",
    "theta",
]

__version__ = "0.1.0"

"""Cross-domain TFPT recovery-kernel search in pulsar glitches.

Completes the ``problem_1.txt`` cross-domain triangle (FRB recovery + GW ringdown
residual + **pulsar-glitch recovery**) by testing the *same* frozen boundary
kernel ``{1,(2/3)^6,(1/3)^6}`` (step ``3/2``) against the real Jodrell Bank Glitch
Catalogue.  Honest by construction: discreteness is calibrated against a
shape-preserving smooth null, and the recovery-parameter ``Q`` channel that needs
data not in the size catalogue is typed ``data_limited`` rather than assumed.
"""

from __future__ import annotations

from . import constants, dsi
from .catalog import (
    GlitchRecord,
    RecoveryRecord,
    by_pulsar,
    glitch_sizes,
    load_catalog,
    load_recovery,
    parse_jbo_html,
    parse_yu2013_recovery,
    recovery_by_glitch,
)
from .discreteness import (
    discreteness_report,
    gmm_multimodality,
    log_periodicity,
    targeted_ratio_tests,
)
from .dsi import detect_dsi, geometric_rate_relaxation, log_frequency, log_periodic_relaxation
from .ratios import prolific_glitchers, size_ratio_ladder, waiting_ratio_ladder
from .recovery import bend_wall_test, q_cluster_test, tau_component_ladder
from .validation import injection_recovery

__all__ = [
    "constants",
    "dsi",
    "GlitchRecord",
    "RecoveryRecord",
    "load_catalog",
    "load_recovery",
    "parse_jbo_html",
    "parse_yu2013_recovery",
    "recovery_by_glitch",
    "glitch_sizes",
    "by_pulsar",
    "discreteness_report",
    "log_periodicity",
    "gmm_multimodality",
    "targeted_ratio_tests",
    "size_ratio_ladder",
    "waiting_ratio_ladder",
    "prolific_glitchers",
    "q_cluster_test",
    "tau_component_ladder",
    "bend_wall_test",
    "log_frequency",
    "log_periodic_relaxation",
    "geometric_rate_relaxation",
    "detect_dsi",
    "injection_recovery",
]

__version__ = "0.1.0"

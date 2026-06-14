"""TFPT-signature search in real Fast Radio Burst data.

A reproducible pipeline that tests the FRB hypotheses of ``problem_b.txt``
against two real public datasets (CHIME/FRB Catalogue 1 and the FRB 20121102A
burst sample of Aggarwal et al. 2021) and reports a TFPT FRB fingerprint score.

The analysis is intentionally honest: the decisive, model-independent TFPT
signature (a discrete / log-periodic energy cascade) is calibrated against
smooth-null surrogates, and axes without data are reported as "no data" rather
than assumed.
"""

from __future__ import annotations

from . import cosmology, recovery_kernel, tfpt_ladder
from .activity_windows import activity_window_test
from .data_io import (
    BurstTable,
    DMzTable,
    PolTable,
    RepeaterSeries,
    load_chime_catalog1,
    load_dmz_sharma,
    load_dmz_table4,
    load_fast_20240114A_pol,
    load_fast_121102_1652,
    load_frb20240619D,
    load_frb121102_aggarwal,
    load_pandhi_pol,
    repeater_subsets,
)
from .dmz_baryon import baryon_test
from .drift_freq import drift_score
from .echo_ratio import echo_ratio_test, evaluate_echo_ratios_by_session
from .energy_clusters import energy_cluster_score, fit_spacing_ladder
from .fingerprint import (
    EvidenceAxis,
    FingerprintWeights,
    aggregate_axes,
    compute_fingerprint,
)
from .markov_spectrum import markov_spectrum_test
from .no_native_dispersion import no_native_dispersion_test
from .periodic_population import evaluate_periodic_windows
from .polarization import pa_angle_classes
from .recovery_observable_model import shared_kernel_search
from .rm_steps import rm_staircase
from .timing import folded_rayleigh, waiting_time_structure

__all__ = [
    "tfpt_ladder",
    "recovery_kernel",
    "cosmology",
    "BurstTable",
    "DMzTable",
    "PolTable",
    "load_chime_catalog1",
    "load_frb121102_aggarwal",
    "load_dmz_table4",
    "load_dmz_sharma",
    "load_pandhi_pol",
    "repeater_subsets",
    "RepeaterSeries",
    "load_fast_121102_1652",
    "load_fast_20240114A_pol",
    "load_frb20240619D",
    "energy_cluster_score",
    "fit_spacing_ladder",
    "drift_score",
    "waiting_time_structure",
    "folded_rayleigh",
    "rm_staircase",
    "pa_angle_classes",
    "baryon_test",
    "activity_window_test",
    "evaluate_periodic_windows",
    "echo_ratio_test",
    "evaluate_echo_ratios_by_session",
    "markov_spectrum_test",
    "shared_kernel_search",
    "no_native_dispersion_test",
    "EvidenceAxis",
    "aggregate_axes",
    "FingerprintWeights",
    "compute_fingerprint",
]

__version__ = "0.3.0"

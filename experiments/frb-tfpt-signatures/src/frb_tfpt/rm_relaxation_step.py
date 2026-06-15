"""FRB.04b (v2, EXPLORATORY) -- RM step-relaxation spectrum.

Motivation (post-v1, after seeing the FRB 20240114A result): the v1 strong test
compares the RM-residual transition spectrum to the *energy* kernel
{1, (2/3)^6, (1/3)^6} and is a clean null (RM is a smooth magneto-ionic drift,
not a discrete mu4 staircase). But the measured RM transition eigenvalues
(~0.62, 0.31) sit close to the *unpowered step* spectrum {1, 2/3, 1/3}, i.e. RM
may read environmental relaxation rather than the sixth-power information channel.

This is an **exploratory** hypothesis only. It was not preregistered against the
step kernel, so it can never retro-actively rescue v1; promotion requires
external replication in a second repeater. The kernel itself is still frozen
(2/3, 1/3 from the axioms) — only the *channel assignment* for RM is the new,
clearly-labelled exploratory choice.
"""

from __future__ import annotations

from .data_io import RepeaterSeries
from .markov_spectrum import MarkovSpectrumResult, markov_spectrum_test
from .recovery_kernel import ONE_THIRD, TWO_THIRDS


def rm_step_relaxation_test(series: RepeaterSeries, n_states: int = 4,
                            seed: int = 0) -> MarkovSpectrumResult:
    """RM-residual transition spectrum vs the unpowered step kernel {2/3, 1/3}."""
    return markov_spectrum_test(series, channel="rm", n_states=n_states, seed=seed,
                                kernel=(TWO_THIRDS, ONE_THIRD))

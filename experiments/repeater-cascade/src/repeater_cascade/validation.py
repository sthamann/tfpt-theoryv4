"""Injection-recovery validation of the RC detectors on realistic session sampling.

Preregistered recipe (hypotheses/repeater_cascade_v1.yaml `validation`):

  * synthetic session = inhomogeneous Poisson process, rate A * tau^-0.8 on
    [0.3 s, 5400 s] (a FAST-like hour with ~1000 bursts, reach ~4 comb periods);
  * RC.02: multiply the rate by (1 + eps cos(omega ln tau)).  At the REFERENCE
    amplitude eps = 0.30 the detector must fire (surrogate p < 0.05) and a
    smooth eps = 0 session must not; the detection rate at the PREDICTED
    eps = 0.01727 is the honest power statement (the amplitude wall);
  * RC.01: an injected frozen-bend two-mode rate must lift delta R^2 above the
    surrogate null; a single-exponential session must not.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .clock_template import clock_test_session
from .comb import comb_test_session
from .constants import BEND, EPS_PREDICTED, EPS_REFERENCE, OMEGA
from .sessions import Session

TAU_LO, TAU_HI = 0.3, 5400.0
N_TARGET = 1000


def _sample_inhomogeneous(rng: np.random.Generator, rate_fn, n_target: int
                          ) -> np.ndarray:
    """Thinning sampler on [TAU_LO, TAU_HI] with a tau^-0.8 majorant envelope."""
    alpha = 0.8
    # draw from the power-law envelope by inverse CDF, then thin
    n_prop = int(n_target * 4)
    q = rng.uniform(size=n_prop)
    a, b = TAU_LO ** (1 - alpha), TAU_HI ** (1 - alpha)
    tau = (a + q * (b - a)) ** (1.0 / (1 - alpha))
    env = tau ** (-alpha)
    acc = rng.uniform(size=n_prop) < rate_fn(tau) / (env * (1.0 + 0.35))
    tau = tau[acc]
    if len(tau) > n_target:                     # random subsample keeps the envelope
        tau = rng.choice(tau, size=n_target, replace=False)
    return np.sort(tau)


def _session_from(tau: np.ndarray) -> Session:
    return Session("synthetic", "SYNTH", 0.0, len(tau) + 1,
                   float(tau[-1]), tau, TAU_LO)


def make_comb_session(rng: np.random.Generator, eps: float) -> Session:
    rate = lambda t: t ** (-0.8) * (1.0 + eps * np.cos(OMEGA * np.log(t)))  # noqa: E731
    return _session_from(_sample_inhomogeneous(rng, rate, N_TARGET))


def make_two_mode_session(rng: np.random.Generator, *, frozen: bool) -> Session:
    """Burst rate = the walled two-mode clock (or a single exp for the null)."""
    r = 3.0 / TAU_HI * 50.0                        # both modes decay inside the window
    if frozen:
        rate = lambda t: 0.05 + np.exp(-r * t) + np.exp(-BEND * r * t)       # noqa: E731
    else:
        rate = lambda t: 0.05 + np.exp(-r * t)                               # noqa: E731
    n_prop = N_TARGET * 60
    tau = rng.uniform(TAU_LO, TAU_HI, n_prop)
    acc = rng.uniform(size=n_prop) < rate(tau) / rate(np.array([TAU_LO]))[0]
    tau = tau[acc]
    if len(tau) > N_TARGET:
        tau = rng.choice(tau, size=N_TARGET, replace=False)
    return _session_from(np.sort(tau))


@dataclass
class InjectionReport:
    # RC.02 comb -- detection RATES over seeds (survive-all-nulls criterion),
    # mirroring PG.06's synthetic_validation semantics
    comb_ref_eps: float
    comb_ref_rate: float          # eps=0.30: should be high (>= 0.6)
    false_positive_rate: float    # eps=0:    should be low  (<= 0.12)
    pred_eps: float
    pred_detection_rate: float    # eps=0.0173: the honest amplitude-wall number
    n_seeds: int
    # RC.01 clock
    clock_frozen_delta_r2: float
    clock_frozen_p: float
    clock_smooth_p: float
    passed: bool


def run_validation(*, n_seeds: int = 16, seed: int = 0) -> InjectionReport:
    rng = np.random.default_rng(seed)

    def fires(r) -> bool:
        # the same survive-all-nulls criterion the analysis marks 'qualified':
        # surrogate p AND off-kernel rank AND Bonferroni-smallest in the battery
        return bool(r.gate_passed and r.p_surrogate < 0.05 and r.p_rank < 0.05
                    and r.kernel_smallest_p)

    def rate(eps: float, base: int) -> tuple[float, object]:
        hits, last = 0, None
        for k in range(n_seeds):
            s = make_comb_session(np.random.default_rng(seed + base + k), eps)
            last = comb_test_session(s, seed=seed + k)
            hits += int(fires(last))
        return hits / n_seeds, last

    ref_rate, _ = rate(EPS_REFERENCE, 100)
    fp_rate, _ = rate(0.0, 300)
    pred_rate, _ = rate(EPS_PREDICTED, 500)

    s_clock = make_two_mode_session(rng, frozen=True)
    r_clock = clock_test_session(s_clock, seed=seed)
    s_single = make_two_mode_session(rng, frozen=False)
    r_single = clock_test_session(s_single, seed=seed)

    passed = bool(ref_rate >= 0.6 and fp_rate <= 0.12)
    return InjectionReport(
        EPS_REFERENCE, ref_rate, fp_rate,
        EPS_PREDICTED, pred_rate, n_seeds,
        r_clock.delta_r2_frozen, r_clock.p_surrogate, r_single.p_surrogate,
        passed)

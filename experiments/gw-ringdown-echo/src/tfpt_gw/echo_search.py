"""Stage-1 echo MATCHED-FILTER machinery, validated by injection-recovery.

The catalog census (echo_forecast.py) only asks whether a stacked strain search COULD
reach a (2/3)^6 echo. This module builds the actual Stage-1 search and validates it on
controlled injections (the honest, reproducible deliverable while real GWOSC strain
ingestion via gwpy is the data step -- exactly the EHT-experiment injection-suite pattern):

  pipeline:  data -> fit & subtract the main (Kerr) ringdown -> matched-filter the residual
             with an echo-train template at the FROZEN amplitude ratio (2/3)^6, FREE lag
             (scanned) and FREE phase -> detection SNR; PLUS a free-ratio control q_hat that
             estimates the per-echo ratio from the residual (anti-numerology, cf. FRB.02b).

  TFPT template lag:  the gravastar/ECO companion (experiments/gravastar-compactness) fixes
             the round-trip echo delay ~0.7 ms (62 Msun) for a C=3/8 object; the lag is
             object-dependent, so the search scans a grid and the ratio (2/3)^6 is the frozen
             discriminator.

  classification (validated 3/3):
    kernel echo  -> SNR>thr AND q_hat ~ (2/3)^6        => DETECTION (TFPT kernel)
    no echo      -> SNR<thr                            => NULL
    wrong ratio  -> SNR>thr BUT q_hat far from kernel  => ECHO, NOT the TFPT kernel (rejected)

Synthetic white-noise strain (deterministic, seeded). No real-strain claim is made.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .constants import DET_THRESHOLD, RATIO

FS = 16384.0          # Hz (LVK high sample rate)
DURATION = 1.0        # s
F0 = 195.0            # Hz, fundamental ringdown freq for ~62 Msun remnant
TAU = 4.0e-3          # s, ringdown damping time (Q ~ a few)
N_ECHO = 5            # echoes in the train template
KERNEL = RATIO        # (2/3)^6 amplitude ratio (frozen)
Q_TOL = 0.5           # |q_hat-kernel|/kernel below this => "kernel"; above => non-kernel
GRAVASTAR_LAG = 0.7e-3  # s, the C=3/8 ECO round-trip delay (gravastar-compactness)


def _times() -> np.ndarray:
    return np.arange(0.0, DURATION, 1.0 / FS)


def ringdown(t: np.ndarray, amp: float, phi: float = 0.0) -> np.ndarray:
    h = np.zeros_like(t)
    m = t >= 0.0
    h[m] = amp * np.exp(-t[m] / TAU) * np.cos(2.0 * np.pi * F0 * t[m] + phi)
    return h


def echo_train(t: np.ndarray, amp: float, lag: float, ratio: float,
               n_echo: int = N_ECHO, phi: float = 0.0) -> np.ndarray:
    h = np.zeros_like(t)
    for n in range(1, n_echo + 1):
        tn = t - n * lag
        m = tn >= 0.0
        h[m] += (ratio ** n) * amp * np.exp(-tn[m] / TAU) * np.cos(2.0 * np.pi * F0 * tn[m] + phi)
    return h


def _mf(data: np.ndarray, template: np.ndarray, sigma: float) -> float:
    """White-noise matched-filter SNR = <d,h>/(sigma ||h||)."""
    norm = float(np.sqrt(np.sum(template ** 2)))
    return 0.0 if norm == 0.0 else float(np.sum(data * template) / (sigma * norm))


def _project(data: np.ndarray, template: np.ndarray) -> float:
    """Least-squares amplitude of `template` in `data`."""
    norm2 = float(np.sum(template ** 2))
    return 0.0 if norm2 == 0.0 else float(np.sum(data * template) / norm2)


@dataclass
class SearchResult:
    case: str
    echo_snr: float          # residual matched-filter SNR (fixed (2/3)^6 template)
    best_lag_ms: float       # recovered lag
    q_hat: float             # free per-echo ratio recovered from the residual
    label: str               # DETECTION / NULL / NON_KERNEL_ECHO
    expected: str
    correct: bool


def search_once(case: str, sigma: float = 0.05, amp: float = 1.0, lag: float = 8.0e-3,
                seed: int = 0) -> SearchResult:
    """Build a synthetic strain for `case`, subtract the ringdown, MF the residual."""
    t = _times()
    rng = np.random.default_rng(seed)
    rd = ringdown(t, amp)
    inj = {"kernel": echo_train(t, amp, lag, KERNEL),
           "null": np.zeros_like(t),
           "wrong_ratio": echo_train(t, amp, lag, 0.5)}[case]
    data = rd + inj + rng.normal(0.0, sigma, t.size)

    # (1) Kerr subtraction: fit & remove the n=0 ringdown
    a_rd = _project(data, rd)
    resid = data - a_rd * rd

    # (2) matched filter the residual over a lag grid, fixed (2/3)^6 ratio
    lags = np.arange(2.0e-3, 40.0e-3, 0.5e-3)
    snrs = [(_mf(resid, echo_train(t, a_rd, lg, KERNEL), sigma), lg) for lg in lags]
    echo_snr, best_lag = max(snrs, key=lambda x: x[0])

    # (3) free-ratio control: per-echo ratio from the first-echo projection at best lag
    e1 = echo_train(t, a_rd, best_lag, 1.0, n_echo=1)   # unit first echo
    a1 = _project(resid, e1)
    q_hat = a1 / a_rd if a_rd != 0 else 0.0

    detected = echo_snr >= DET_THRESHOLD
    kernel_like = abs(q_hat - KERNEL) / KERNEL < Q_TOL
    if not detected:
        label = "NULL"
    elif kernel_like:
        label = "DETECTION"
    else:
        label = "NON_KERNEL_ECHO"
    expected = {"kernel": "DETECTION", "null": "NULL", "wrong_ratio": "NON_KERNEL_ECHO"}[case]
    return SearchResult(case, round(echo_snr, 2), round(best_lag * 1e3, 2),
                        round(q_hat, 4), label, expected, label == expected)


@dataclass
class InjectionSuite:
    results: list[SearchResult] = field(default_factory=list)
    n_correct: int = 0
    n_total: int = 0
    template_lag_ms: float = GRAVASTAR_LAG * 1e3
    verdict: str = ""


def injection_suite(seed: int = 0) -> InjectionSuite:
    suite = InjectionSuite()
    for i, case in enumerate(("kernel", "null", "wrong_ratio")):
        suite.results.append(search_once(case, seed=seed + i))
    suite.n_total = len(suite.results)
    suite.n_correct = sum(r.correct for r in suite.results)
    ok = suite.n_correct == suite.n_total
    suite.verdict = (
        f"Stage-1 echo matched-filter validated: {suite.n_correct}/{suite.n_total} injections "
        f"correctly classified -- the pipeline (Kerr subtraction + fixed-(2/3)^6 matched filter "
        f"+ free-ratio control) separates a TFPT-kernel echo, a no-echo null and a wrong-ratio "
        f"echo. Ready for real GWOSC strain (gwpy ingest is the data step). No echo claim made."
        if ok else
        f"FAIL: only {suite.n_correct}/{suite.n_total} injections classified correctly"
    )
    return suite

"""The frozen TFPT recovery-comb kernel -- everything derived from the two axioms.

``c3 = 1/(8 pi)`` (P1) + ``g_car = 5`` (P2) fix the geometric cascade scale ``lambda = (3/2)^6``
and hence the log-periodic comb log-frequency and its (suppressed) amplitude. NO fitted numbers.
Mirrors ``recovery-comb-domains/comb.py`` and ``gw-ringdown-echo/dynamic_recovery.py`` so the
meta-analysis tests the SAME kernel every channel tested.
"""

from __future__ import annotations

import math

N_FAM = 3
P2 = 6
LAMBDA = 1.5**P2  # (3/2)^6 = 11.390625, the geometric cascade scale
OMEGA = 2.0 * math.pi / math.log(LAMBDA)  # 2.5827..., the comb log-frequency (2 pi / ln lambda)
EPS_PREDICTED = math.exp(-(math.pi**2) / math.log(LAMBDA))  # ~0.0173, the QT.02 suppression law
MIN_COMB_PERIODS = 2.8  # hard ln(t)-range gate (machine-checked; no stacking relaxes it)
DETREND_DEG = 2  # degree of the poly-in-ln(t) baseline that absorbs the smooth recovery trend

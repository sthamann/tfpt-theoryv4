"""Meta-analytic upper limit on the TFPT recovery-comb amplitude eps at omega = 2.583.

Search-surface meta-analysis (FIREWALL: nothing here is load-bearing / [E]). It turns the
existing pile of clean per-channel recovery-comb NULLs into a QUANTITATIVE upper limit on the
common comb amplitude ``eps`` at the frozen kernel log-frequency, kept in TWO explicitly
separated groups:

  1. boundary/horizon-scoped  -- the TFPT-relevant limit (where TFPT predicts a universal eps);
  2. all-channel (surface+horizon) -- a universal-DSI bound only, explicitly NOT TFPT-specific.
"""

from .kernel import EPS_PREDICTED, LAMBDA, MIN_COMB_PERIODS, OMEGA

__all__ = ["OMEGA", "LAMBDA", "EPS_PREDICTED", "MIN_COMB_PERIODS"]

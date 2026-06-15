"""Page curve from the TFPT Hawking law + the island/unitary min-prescription.

With the TFPT evaporation law P_H = c3/(1920 M^2) (horizon_readouts), mass shrinks as
M(t) = M0 (1 - t/tau)^{1/3}, so the Bekenstein-Hawking entropy S_BH = M^2/(2 c3)
scales as

    S_BH(t)/S0 = (1 - t/tau)^{2/3} .

Energy/entropy conservation gives the coarse radiation entropy S_rad = S0 - S_BH, and
the unitary (island/Page) fine-grained entropy is the min of the two:

    S_page(t) = min( S_BH(t), S_rad(t) ).

The turnover (S_BH = S_rad = S0/2) is at (1 - t/tau)^{2/3} = 1/2, i.e.

    t_Page / tau = 1 - (1/2)^{3/2} = 0.6464...,

which is EXACTLY the TFPT Page time t_Page = (1 - 1/(2 sqrt2)) tau (horizon_readouts).
So the unitary Page turnover sits at the TFPT Page time with no extra input; the
boundary-recovery eigenvalue (2/3)^6 is the rate at which information returns after it.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .constants import LAMBDA


def s_bh(t_over_tau: np.ndarray) -> np.ndarray:
    return np.clip(1.0 - t_over_tau, 0.0, 1.0) ** (2.0 / 3.0)


def page_curve(n: int = 400):
    t = np.linspace(0.0, 1.0, n)
    sbh = s_bh(t)
    srad = 1.0 - sbh
    spage = np.minimum(sbh, srad)
    return t, sbh, srad, spage


@dataclass
class PageResult:
    t_page_over_tau: float
    t_page_theory: float
    turnover_matches: bool
    recovery_rate: float
    note: str = ""


def analyse() -> PageResult:
    t, sbh, srad, spage = page_curve()
    t_turn = float(t[int(np.argmax(spage))])
    t_theory = 1.0 - 1.0 / (2.0 * np.sqrt(2.0))     # 0.6464...
    ok = bool(abs(t_turn - t_theory) <= 2.0 / len(t))   # within grid resolution
    return PageResult(t_turn, float(t_theory), ok, float(LAMBDA[1]),
                      "unitary island min-prescription turnover sits at the TFPT Page "
                      "time 1-1/(2 sqrt2)=0.6464 tau; recovery rate after the Page time "
                      "is the boundary eigenvalue (2/3)^6")

"""Two-step carrier-native Pati-Salam -> SO(10) unification (the E8-allowed contents).

The TFPT carrier is D5 (+) A3 = SO(10) x SU(4). IF the carrier SO(10)/Pati-Salam is
gauged (the OPTIONAL UV branch B; NOT the default boundary-only reading A), the couplings
run in two steps

    M_Z --(SM)--> M_PS --(PS: SU(2)_L x SU(2)_R x SU(4)_c)--> M_GUT  (SO(10): a4=a2L=a2R)

with matching at M_PS:  a4 = a3,  a2L = a2,  a2R^-1 = (5/3) a1^-1 - (2/3) a3^-1  (v248).

Higgs content is NOT free: the E8 audit hull (v247, E8 -> SO(10) x SU(4)) supplies exactly
{1, 10, 16, 45} -- ONE 45 and ONE 15 -- and FORBIDS the 126. So only two contents are
E8-allowed:

  * ``minimal_16H``   -- the minimal renormalisable 16-Higgs (bidoublet + (4,1,2)),
  * ``+(15,1,1)_45``  -- plus the single SU(4)-adjoint (15,1,1) = the one E8-allowed 45.

This module reproduces verification/v266 (PS.PROTON.02) and v249 (PS.RGTEST.01); see also
experiments/gauge-unification/results/pati_salam.json.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from tfpt_proton.rge import B1L, M_Z, alpha_inv_at_MZ, run_2loop

# --- TFPT scalaron scale: flows from the axiom c3 = 1/(8 pi) + the Planck anchor --------
C3 = 1.0 / (8.0 * math.pi)          # axiom P1 (seam constant)
MBAR = 2.435323203e18               # reduced Planck mass (GeV) -- the gravitational anchor
M_SCALARON = C3 ** 3.5 * MBAR       # M_s = c3^{7/2} Mbar ~ 3.06e13 GeV (R+R^2 / spectral action)

# --- the two E8-allowed PS 1-loop beta coefficients b = (b4, b2L, b2R) (v247/v248/v266) --
E8_CONTENTS: dict[str, tuple[float, float, float]] = {
    "minimal_16H":  (-31 / 3, -3.0, -7 / 3),   # bidoublet + (4,1,2): minimal E8 10 + 16
    "+(15,1,1)_45": (-9.0, -3.0, -7 / 3),       # + SU(4)-adjoint (15,1,1) = the single E8 45
}


@dataclass
class UnifPoint:
    content: str
    loop: str                # "1loop" | "2loop"
    b_ps: tuple[float, float, float]
    M_PS_GeV: float
    M_GUT_GeV: float
    alpha_gut_inv: float
    ratio_to_scalaron: float
    valid: bool              # scales ordered M_PS < M_GUT < M_Pl


def _matching_rows(a: np.ndarray, Bsm: np.ndarray, C: np.ndarray):
    """The three PS matching lines a4 = a3, a2L = a2, a2R^-1 = (5/3)a1 - (2/3)a3.

    Each returned tuple (a0, ba, bg) is alpha^-1(M_PS) = a0 - ba*L_PS, then above M_PS the
    slope is C (the PS beta) over the second leg L_GUT.
    """
    def lin(i: int):
        if i == 0:
            return (a[2], -Bsm[2], -C[0])                       # SU(4)_c <- SU(3)_c
        if i == 1:
            return (a[1], -Bsm[1], -C[1])                       # SU(2)_L <- SU(2)_L
        return ((5 / 3) * a[0] - (2 / 3) * a[2],
                -((5 / 3) * Bsm[0] - (2 / 3) * Bsm[2]), -C[2])  # SU(2)_R reconstructed
    return lin(0), lin(1), lin(2)


def solve_1loop(b_ps: tuple[float, float, float]) -> tuple[float, float, float, bool]:
    """1-loop analytic two-step solve. Returns (M_PS, M_GUT, alpha_GUT^-1, valid).

    Identical machinery to v266.ps_solve / v249.ps_solve.
    """
    a = np.array(alpha_inv_at_MZ())
    Bsm = np.array(B1L) / (2 * math.pi)
    C = np.array(b_ps) / (2 * math.pi)
    c4, c2l, c2r = _matching_rows(a, Bsm, C)
    A = np.array([[c4[1] - c2l[1], c4[2] - c2l[2]],
                  [c4[1] - c2r[1], c4[2] - c2r[2]]])
    rhs = np.array([-(c4[0] - c2l[0]), -(c4[0] - c2r[0])])
    LPS, LG = np.linalg.solve(A, rhs)
    a_gut = c4[0] + c4[1] * LPS + c4[2] * LG
    M_PS = M_Z * math.exp(LPS)
    M_GUT = M_Z * math.exp(LPS + LG)
    return M_PS, M_GUT, a_gut, (LPS > 0 and LG > 0 and M_GUT < MBAR)


def solve_2loop(b_ps: tuple[float, float, float]) -> tuple[float, float, float, bool]:
    """2-loop SM below M_PS + 1-loop PS above; root-find M_PS so a4 = a2L = a2R meet.

    Identical machinery to gauge-unification's pati_salam.solve_2loop.
    """
    a0 = alpha_inv_at_MZ()
    C = np.array(b_ps) / (2 * math.pi)

    def residual(lnMps: float):
        t = lnMps - math.log(M_Z)
        a = run_2loop(a0, t, n=3000)
        a4, a2l = a[2], a[1]
        a2r = (5 / 3) * a[0] - (2 / 3) * a[2]
        t12 = (a4 - a2l) / (C[0] - C[1])
        t13 = (a4 - a2r) / (C[0] - C[2])
        Mps = math.exp(lnMps)
        return t12 - t13, Mps, t12, a4 - C[0] * t12

    lo, hi = math.log(1e12), math.log(1e15)
    rlo = residual(lo)[0]
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        rm = residual(mid)[0]
        if (rlo < 0) != (rm < 0):
            hi = mid
        else:
            lo, rlo = mid, rm
    _, Mps, tg, ag = residual(0.5 * (lo + hi))
    M_GUT = Mps * math.exp(tg)
    return Mps, M_GUT, ag, (tg > 0 and M_GUT < MBAR)


def solve(content: str, loop: str) -> UnifPoint:
    b = E8_CONTENTS[content]
    solver = solve_1loop if loop == "1loop" else solve_2loop
    M_PS, M_GUT, a_gut, ok = solver(b)
    return UnifPoint(content, loop, b, float(M_PS), float(M_GUT), float(a_gut),
                     float(M_PS / M_SCALARON), bool(ok))


def scan() -> list[UnifPoint]:
    return [solve(c, loop) for c in E8_CONTENTS for loop in ("1loop", "2loop")]

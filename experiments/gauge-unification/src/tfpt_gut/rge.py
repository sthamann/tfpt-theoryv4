"""sin^2 theta_W = 3/8 spectral-unification test against PDG data (1- and 2-loop SM RGE).

The discrete->dynamic completion (v244/v245) predicts, via Connes' spectral action / the
NCG normalisation of the carrier SO(10) 16, the GUT relation at the spectral scale Lambda

    sin^2 theta_W(Lambda) = 3/8,    g3 = g2 = sqrt(5/3) g1     (g1 GUT-normalised).

This module CONFRONTS that with the measured couplings: it runs the Standard-Model gauge
couplings from M_Z upward with the 1-loop (and gauge-only 2-loop) RGEs and asks

  (a) do the three couplings unify (meet at one scale)?  -- the SM is known NOT to,
  (b) imposing unification, what sin^2 theta_W(M_Z) does the 3/8 boundary predict?  --
      the Georgi-Quinn-Weinberg value, ~0.207 at 1 loop, vs measured 0.23122.

Honest: 3/8 is the standard SU(5)/SO(10) GUT value; TFPT *inherits* it (it does not improve
the SM unification gap). The result is "consistent at GUT level, NOT a precision hit".
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# PDG 2024 inputs at M_Z (MSbar)
M_Z = 91.1876
ALPHA_EM_INV = 127.951        # alpha_em^-1(M_Z)
SIN2_W_MEAS = 0.23122         # sin^2 theta_W^MSbar(M_Z)
SIN2_W_ERR = 0.00004
ALPHA_S = 0.1179              # alpha_s(M_Z)

# SU(5)/GUT normalisation: alpha_1 = (5/3) alpha_Y ; sin^2 theta_W(Lambda) = 3/8
GUT_NORM = 5.0 / 3.0
SIN2_W_GUT = 3.0 / 8.0

# 1-loop SM beta coefficients b=(b1,b2,b3), b1 GUT-normalised
B1L = (41.0 / 10.0, -19.0 / 6.0, -7.0)

# 2-loop SM gauge beta matrix b_ij (gauge sector; Yukawa neglected -- small for this test)
B2L = np.array([
    [199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
    [9.0 / 10.0, 35.0 / 6.0, 12.0],
    [11.0 / 10.0, 9.0 / 2.0, -26.0],
])


def alpha_inv_at_MZ() -> tuple[float, float, float]:
    """(alpha1,alpha2,alpha3)^-1 at M_Z from the measured (alpha_em, sin^2, alpha_s)."""
    cos2 = 1.0 - SIN2_W_MEAS
    a1 = (3.0 / 5.0) * cos2 * ALPHA_EM_INV    # GUT-normalised U(1)
    a2 = SIN2_W_MEAS * ALPHA_EM_INV
    a3 = 1.0 / ALPHA_S
    return a1, a2, a3


def run_1loop(a0: tuple[float, float, float], t: float) -> tuple[float, float, float]:
    """alpha_i^-1(mu) at t = ln(mu/M_Z), 1-loop."""
    return tuple(a0[i] - B1L[i] / (2 * math.pi) * t for i in range(3))


def run_2loop(a0: tuple[float, float, float], t: float, n: int = 2000) -> tuple[float, ...]:
    """Integrate the 2-loop gauge RGE for alpha_i^-1(mu); d(a_i^-1)/dt =
    -b_i/2pi - sum_j b_ij/(8 pi^2) * (1/a_j^-1)."""
    ainv = np.array(a0, dtype=float)
    dt = t / n
    for _ in range(n):
        alpha = 1.0 / ainv
        d = np.array([-B1L[i] / (2 * math.pi)
                      - sum(B2L[i, j] / (8 * math.pi**2) * alpha[j] for j in range(3))
                      for i in range(3)])
        ainv = ainv + d * dt
    return tuple(ainv)


@dataclass
class UnificationResult:
    a_MZ: tuple[float, float, float]
    t_12: float                 # ln(Lambda_12/M_Z) where a1=a2
    Lambda_12_GeV: float
    a_gut_inv: float            # common a1=a2 inverse coupling there
    a3_inv_at_12: float         # a3 at that scale (the unification miss)
    unify_miss_pct: float       # |a3 - a_gut|/a_gut at Lambda_12
    sin2_pred_1loop: float      # sin^2 theta_W(M_Z) predicted by imposing unification (GQW)
    sin2_meas: float
    pull_sigma: float
    verdict: str


def gqw_sin2(loop: str = "1loop") -> tuple[float, float, float]:
    """Impose full unification a1(Lambda)=a2=a3 and solve for sin^2 theta_W(M_Z) and Lambda,
    using the measured alpha_em, alpha_s as inputs (Georgi-Quinn-Weinberg)."""
    Ae = ALPHA_EM_INV
    As = 1.0 / ALPHA_S
    b1, b2, b3 = B1L
    # a1^-1(MZ) = (3/5)(1-s)Ae ; a2^-1 = s Ae ; a3^-1 = As. Unify all three:
    #   a1^-1(MZ) - a2^-1(MZ) = (b1-b2)L/2pi ;  a2^-1(MZ) - a3^-1(MZ) = (b2-b3)L/2pi
    # two eqns, unknowns s,L. Eliminate L.
    #   (3/5)(1-s)Ae - s Ae = (b1-b2)/(b2-b3) * (s Ae - As)
    k = (b1 - b2) / (b2 - b3)
    # (3/5)Ae - (3/5)Ae s - s Ae = k(s Ae - As)
    # (3/5)Ae + k As = s [ (3/5)Ae + Ae + k Ae ]
    s = ((3.0 / 5.0) * Ae + k * As) / ((3.0 / 5.0) * Ae + Ae + k * Ae)
    L = (s * Ae - As) / ((b2 - b3) / (2 * math.pi))
    return s, L, math.exp(L) * M_Z


def analyse() -> UnificationResult:
    a0 = alpha_inv_at_MZ()
    b1, b2, b3 = B1L
    # scale where a1 = a2 (1-loop): a0[0]-b1 t/2pi = a0[1]-b2 t/2pi
    t12 = (a0[0] - a0[1]) / ((b1 - b2) / (2 * math.pi))
    a_gut = a0[0] - b1 / (2 * math.pi) * t12
    a3_12 = a0[2] - b3 / (2 * math.pi) * t12
    miss = abs(a3_12 - a_gut) / a_gut

    sin2_pred, _, _ = gqw_sin2()
    pull = (sin2_pred - SIN2_W_MEAS) / SIN2_W_ERR
    verdict = (
        f"sin^2 theta_W = 3/8 is the standard SU(5)/SO(10) GUT value (TFPT inherits it via "
        f"the carrier 16). Running the measured SM couplings 1-loop: alpha1=alpha2 meet at "
        f"Lambda~{math.exp(t12)*M_Z:.1e} GeV but alpha3 misses by {100*miss:.0f}% (the known "
        f"SM non-unification). Imposing unification, the 3/8 boundary predicts "
        f"sin^2 theta_W(M_Z)={sin2_pred:.4f} vs measured {SIN2_W_MEAS:.5f} -- the classic ~"
        f"{100*abs(sin2_pred-SIN2_W_MEAS)/SIN2_W_MEAS:.0f}% GQW gap. CONSISTENT at GUT level, "
        "NOT a precision hit; closing the gap needs SUSY/thresholds (beyond TFPT's tree relation)."
    )
    return UnificationResult(a0, t12, math.exp(t12) * M_Z, a_gut, a3_12, miss,
                             sin2_pred, SIN2_W_MEAS, pull, verdict)

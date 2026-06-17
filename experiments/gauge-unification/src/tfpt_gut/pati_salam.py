"""Carrier-native Pati-Salam / SO(10) two-step unification + proton-decay test.

The SM-only run (rge.py) does NOT unify -- TFPT inherits the standard GUT value
sin^2 theta_W = 3/8 but buys no better Weinberg angle (the universal SM gap).

BUT the TFPT carrier is D5(+)A3 = SO(10) x SU(4) (Pati-Salam SU(4)_c x SU(2)_L x
SU(2)_R after Spin(6)=SU(4), Spin(4)=SU(2)xSU(2)).  So the *native* high-scale
gauge structure is NOT the SM but Pati-Salam.  This module asks the honest,
TFPT-specific question:

  IF the carrier SO(10)/Pati-Salam is GAUGED, at what scale M_PS must it break to
  the SM so the couplings unify into SO(10) -- and does that scale coincide with
  TFPT's INDEPENDENT scalaron scale M_s = c3^{7/2} Mbar (~3.06e13 GeV)?  And does
  the resulting M_GUT survive the Super-K proton-decay bound?

Two-step running   M_Z --(SM)--> M_PS --(PS)--> M_GUT (SO(10): a4=a2L=a2R), with
matching at M_PS:  a4=a3, a2L=a2, a2R^-1=(5/3)a1^-1-(2/3)a3^-1.

HONEST SCOPE (exploratory [O], not a closure):
  * PRESUPPOSES the carrier SO(10)/SU(4) is gauged -> intermediate PS gauge bosons
    (leptoquarks, W_R) at M_PS.  A theory FORK vs the strict "SM content, no new
    state" reading -- not established here.
  * 1-loop; the PS scalar (Higgs) content is a CHOICE.  M_PS is robust to it
    (fixed mostly by the SM run); M_GUT is not, and proton decay then SELECTS the
    admissible scalar content.
  * proton lifetime carries an order-of-magnitude hadronic-matrix-element factor.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

from tfpt_gut.rge import M_Z, B1L, alpha_inv_at_MZ

# TFPT scalaron scale  M_s = c3^{7/2} * Mbar  (independent: from R+R^2 / spectral action)
C3 = 1.0 / (8.0 * math.pi)
MBAR = 2.435323203e18
M_SCALARON = C3 ** 3.5 * MBAR                      # ~ 3.06e13 GeV

# proton decay p -> e+ pi0 bounds (years)
TAU_P_SK = 2.4e34          # Super-Kamiokande 2020 lower bound
TAU_P_HK = 1.0e35          # Hyper-Kamiokande projected reach (order of magnitude)
TAU16 = 1.0e36            # benchmark tau at M_X=1e16, alpha_GUT=1/40 (factor ~3 uncertainty)

# One-loop Pati-Salam beta coefficients b=(b4, b2L, b2R), 3 gens [(4,2,1)+(4bar,1,2)]
# plus a chosen scalar sector.  b = -11/3 C2 + 2/3 sum T_f + 1/3 sum T_s.
PS_SCALAR_VARIANTS: dict[str, tuple[float, float, float]] = {
    "fermions_only":                 (-32 / 3, -10 / 3, -10 / 3),
    "minimal (bidoublet + (4,1,2))": (-31 / 3, -3.0, -7 / 3),
    "+second bidoublet":             (-31 / 3, -8 / 3, -2.0),
    "+(15,1,1) of SU(4)":            (-9.0, -3.0, -7 / 3),
    "+extra (4,1,2)":                (-10.0, -3.0, -5 / 3),
}


def proton_lifetime(M_GUT: float, alpha_gut_inv: float, tau16: float = TAU16) -> float:
    """tau(p->e+pi0) ~ tau16 * (M_GUT/1e16)^4 * ((1/40)/alpha_GUT)^2.

    tau16 is the standard SU(5)/SO(10) benchmark at M_X=1e16, alpha_GUT=1/40
    (order-of-magnitude; lattice hadronic matrix elements carry a ~x3 uncertainty)."""
    alpha_gut = 1.0 / alpha_gut_inv
    return tau16 * (M_GUT / 1e16) ** 4 * ((1.0 / 40.0) / alpha_gut) ** 2


@dataclass
class PSResult:
    variant: str
    b_ps: tuple[float, float, float]
    M_PS_GeV: float
    M_GUT_GeV: float
    alpha_gut_inv: float
    ratio_to_scalaron: float
    tau_p_yr: float
    proton_safe: bool                # tau_p > Super-K bound
    valid: bool                      # scales ordered + sub-Planckian


def _solve(b_ps: tuple[float, float, float]) -> tuple[float, float, float, bool]:
    a = np.array(alpha_inv_at_MZ())
    Bsm = np.array(B1L) / (2 * math.pi)
    C = np.array(b_ps) / (2 * math.pi)

    def lin(idx: int) -> tuple[float, float, float]:
        if idx == 0:
            return (a[2], -Bsm[2], -C[0])                      # SU(4) <- SU(3)
        if idx == 1:
            return (a[1], -Bsm[1], -C[1])                      # SU(2)_L <- SU(2)
        return ((5 / 3) * a[0] - (2 / 3) * a[2],
                -((5 / 3) * Bsm[0] - (2 / 3) * Bsm[2]), -C[2])  # SU(2)_R reconstructed

    c4, c2l, c2r = lin(0), lin(1), lin(2)
    A = np.array([[c4[1] - c2l[1], c4[2] - c2l[2]],
                  [c4[1] - c2r[1], c4[2] - c2r[2]]])
    rhs = np.array([-(c4[0] - c2l[0]), -(c4[0] - c2r[0])])
    LPS, LG = np.linalg.solve(A, rhs)
    a_gut = c4[0] + c4[1] * LPS + c4[2] * LG
    return M_Z * math.exp(LPS), M_Z * math.exp(LPS + LG), a_gut, (LPS > 0 and LG > 0)


def _result(name: str, b: tuple[float, float, float]) -> PSResult:
    M_PS, M_GUT, a_gut, ok = _solve(b)
    tau = float(proton_lifetime(M_GUT, a_gut))
    return PSResult(name, tuple(float(x) for x in b), float(M_PS), float(M_GUT),
                    float(a_gut), float(M_PS / M_SCALARON), tau,
                    bool(tau > TAU_P_SK), bool(ok and M_GUT < MBAR))


def scan() -> list[PSResult]:
    return [_result(n, b) for n, b in PS_SCALAR_VARIANTS.items()]


def verdict() -> str:
    res = scan()
    ratios = [r.ratio_to_scalaron for r in res]
    safe = [r for r in res if r.proton_safe and r.valid]
    return (
        "Carrier-native Pati-Salam/SO(10) two-step unification: the carrier's own "
        "SU(4)xSU(2)xSU(2) above M_PS DOES unify, and the required PS-breaking scale "
        f"lands at M_PS = ({min(ratios):.1f}-{max(ratios):.1f}) x the TFPT scalaron scale "
        f"M_s = {M_SCALARON:.2e} GeV across ALL scalar choices (robust: M_PS is fixed by "
        "the SM run below it). So the gauge-unification scale and the gravitational "
        "scalaron scale -- two INDEPENDENT TFPT structures -- coincide to ~40%. "
        "PROTON DECAY then SELECTS the scalar content: minimal choices give M_GUT~2e15 GeV "
        f"-> tau_p ~ few x 10^33 yr, EXCLUDED by Super-K ({TAU_P_SK:.1e} yr); but a higher-"
        f"M_GUT choice (e.g. +(15,1,1), M_GUT~5.8e15) gives tau_p ~ 1e35 yr -- SAFE and "
        f"within Hyper-K reach. {len(safe)}/{len(res)} variants survive. CAVEATS [O]: "
        "presupposes the carrier SO(10) is GAUGED (the open fork); 1-loop; tau_p carries a "
        "~x3 matrix-element uncertainty. A genuine, falsifiable TFPT-native coincidence "
        "with a sharp proton-decay kill-test -- NOT a proof."
    )


def write_results(path: Path | None = None) -> dict:
    res = scan()
    out = {
        "scalaron_scale_GeV": M_SCALARON,
        "tau_p_superK_yr": TAU_P_SK,
        "tau_p_hyperK_yr": TAU_P_HK,
        "variants": [asdict(r) for r in res],
        "verdict": verdict(),
    }
    if path is None:
        path = Path(__file__).resolve().parents[2] / "results" / "pati_salam.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    print("scalaron M_s = %.3e GeV  (= c3^3.5 * Mbar, independent of gauge running)\n"
          % M_SCALARON)
    hdr = "%-32s %-10s %-10s %-6s %-9s %-11s %s"
    print(hdr % ("scalar variant", "M_PS/GeV", "M_GUT/GeV", "aG^-1", "M_PS/M_s",
                 "tau_p/yr", "p-decay"))
    for r in scan():
        print(hdr % (r.variant, "%.2e" % r.M_PS_GeV, "%.2e" % r.M_GUT_GeV,
                     "%.1f" % r.alpha_gut_inv, "x%.2f" % r.ratio_to_scalaron,
                     "%.1e" % r.tau_p_yr,
                     "SAFE" if r.proton_safe else "excluded"))
    write_results()
    print("\n" + verdict())
    print("\nwrote results/pati_salam.json")

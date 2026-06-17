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

from tfpt_gut.rge import M_Z, B1L, B2L, alpha_inv_at_MZ, run_2loop

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
    r1 = [r.ratio_to_scalaron for r in res]
    r2 = [solve_2loop(b)[0] / M_SCALARON for b in PS_SCALAR_VARIANTS.values()]
    return (
        "Carrier-native Pati-Salam/SO(10) two-step unification: the carrier's own "
        "SU(4)xSU(2)xSU(2) above M_PS DOES unify. (1) SCALE MATCH: the required "
        f"PS-breaking scale M_PS lands on the TFPT scalaron scale M_s = {M_SCALARON:.2e} GeV "
        f"-- 1-loop M_PS/M_s = {min(r1):.2f}-{max(r1):.2f}, and 2-loop SHRINKS this to "
        f"{min(r2):.2f}-{max(r2):.2f} (one variant ~1.02, essentially exact). So the ~40% "
        "1-loop gap was mostly the loop order; the residual <=20% is within PS-threshold + "
        "O(1) (scalaron-mass vs breaking-VEV) ambiguity. Two INDEPENDENT TFPT scales "
        "(gravitational scalaron, gauge unification) coincide. (2) PROTON DECAY is now the "
        "BINDING constraint: M_GUT ~ 1-6e15 GeV gives tau_p(p->e pi0) ~ 10^33-10^35 yr; the "
        f"minimal reps are EXCLUDED by Super-K ({TAU_P_SK:.1e} yr), only large-M_GUT content "
        "(e.g. +(15,1,1) at 1-loop) is safe, and 2-loop lowers M_GUT so survival needs "
        "M_GUT pushed up (larger reps / GUT thresholds) or the ~x3 matrix-element headroom. "
        "(3) LEPTOGENESIS: M_R = scalaron is viable (implied y_D~0.22, needed CP asymmetry "
        "~0.02% of the Davidson-Ibarra bound). CAVEATS [O]: presupposes the carrier SO(10) "
        "is GAUGED (the open fork); the binding risk is proton decay, NOT the scale match. "
        "A falsifiable TFPT-native coincidence with a sharp proton-decay kill-test, NOT a proof."
    )


def solve_2loop(b_ps: tuple[float, float, float]) -> tuple[float, float, float]:
    """Two-loop SM below M_PS + 1-loop PS above (the PS run is short, ~1.5 dec).
    Root-find M_PS so the two SO(10) conditions a4=a2L and a4=a2R meet at one M_GUT."""
    a0 = alpha_inv_at_MZ()
    C = np.array(b_ps) / (2 * math.pi)

    def residual(lnMps: float):
        t = lnMps - math.log(M_Z)
        a = run_2loop(a0, t, n=3000)                       # 2-loop SM a_i^-1 at M_PS
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
    return Mps, Mps * math.exp(tg), ag


def leptogenesis(M_R: float = M_SCALARON, m3_eV: float = 0.05) -> dict:
    """Is M_R = scalaron viable for thermal leptogenesis?  m3 ~ sqrt(dm^2_atm).
    Seesaw fixes the implied Dirac Yukawa y_D = sqrt(m3 M_R)/v; the washout anchor
    m~1 = m3/A_Lambda = m3/10 (FR.ETAB.03) sets the efficiency; compare the needed
    CP asymmetry to the Davidson-Ibarra bound."""
    v = 174.0
    m3 = m3_eV * 1e-9                                      # GeV
    y_D = math.sqrt(m3 * M_R) / v
    eps_max = (3 / (16 * math.pi)) * M_R * m3 / v**2       # Davidson-Ibarra
    mtil_eV = m3_eV / 10.0                                 # m~1 = m3/A_Lambda
    mstar = 1.08e-3
    kappa = min((2e-2 / mtil_eV) * (mtil_eV / (mtil_eV + mstar))**1.16, 0.1)
    eps_need = 6.1e-10 / (0.96e-2 * kappa)
    return {
        "M_R_GeV": M_R, "implied_y_D": y_D, "eps_DI_max": eps_max,
        "mtilde1_eV": mtil_eV, "efficiency_kappa": kappa, "eps_needed": eps_need,
        "headroom_eps_need_over_max": eps_need / eps_max,
        "viable": eps_need < eps_max,
        "note": ("M_R = scalaron is consistent with seesaw (natural y_D~0.22) and "
                 "thermal leptogenesis (needed CP asymmetry ~0.02% of the DI bound; "
                 "M_1 in the thermal window). The apparent ~20x vs the y_D=1 seesaw "
                 "value 6e14 is absorbed into the (free) Dirac Yukawa -- NOT a tension."),
    }


def write_results(path: Path | None = None) -> dict:
    res = scan()
    two_loop = []
    for name, b in PS_SCALAR_VARIANTS.items():
        M_PS, M_GUT, ag = solve_2loop(b)
        tau = proton_lifetime(M_GUT, ag)
        two_loop.append({"variant": name, "M_PS_GeV": M_PS, "M_GUT_GeV": M_GUT,
                         "alpha_gut_inv": ag, "ratio_to_scalaron": M_PS / M_SCALARON,
                         "tau_p_yr": tau, "proton_safe": bool(tau > TAU_P_SK)})
    out = {
        "scalaron_scale_GeV": M_SCALARON,
        "tau_p_superK_yr": TAU_P_SK,
        "tau_p_hyperK_yr": TAU_P_HK,
        "variants_1loop": [asdict(r) for r in res],
        "variants_2loop": two_loop,
        "leptogenesis": leptogenesis(),
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
    print("\n2-loop SM + 1-loop PS (root-found M_PS):")
    for name, b in PS_SCALAR_VARIANTS.items():
        M_PS, M_GUT, ag = solve_2loop(b)
        tau = proton_lifetime(M_GUT, ag)
        print("  %-28s M_PS=%.2e (x%.2f Ms)  M_GUT=%.2e  aG^-1=%.1f  tau_p=%.1e  %s"
              % (name, M_PS, M_PS / M_SCALARON, M_GUT, ag, tau,
                 "SAFE" if tau > TAU_P_SK else "excluded"))
    lp = leptogenesis()
    print("\nleptogenesis (M_R = scalaron = %.2e GeV): y_D=%.3f, eps_need/eps_max=%.1e -> %s"
          % (lp["M_R_GeV"], lp["implied_y_D"], lp["headroom_eps_need_over_max"],
             "VIABLE" if lp["viable"] else "fails"))
    write_results()
    print("\n" + verdict())
    print("\nwrote results/pati_salam.json")

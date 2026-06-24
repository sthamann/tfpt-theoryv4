"""Horizon compiler fingerprints: scrambling, Hawking 1920, area 4 ln3, turnaround radius.

These are structural identities / catalog-feasibility targets from tfpt_horizon_readouts.
No load-bearing claim -- documents what future data would test and checks internal consistency.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .constants import (
    AREA_LN3,
    C3,
    HAWKING_DENOM,
    LN3,
    MU4,
    N_FAM,
    PHI0,
    W_D5,
)


@dataclass
class HorizonPrint:
    name: str
    tfpt_value: str
    data_status: str
    decisive_experiment: str
    kill_condition: str


@dataclass
class HorizonResult:
    prints: list[HorizonPrint] = field(default_factory=list)
    identities_ok: bool = False
    verdict: str = ""


def run_horizon() -> HorizonResult:
    res = HorizonResult()

    # internal consistency
    ok_wd5 = W_D5 == 1920
    ok_area = abs(AREA_LN3 - math.log(N_FAM**4)) < 1e-12
    ok_ln3 = abs(LN3 - math.log(N_FAM)) < 1e-12
    ok_c3 = abs(C3 - 1.0 / (8.0 * math.pi)) < 1e-15
    res.identities_ok = ok_wd5 and ok_area and ok_ln3 and ok_c3

    m_sun = 1.989e30
    m_bh = 10.0 * m_sun
    s_bh = (m_bh ** 2)  # in Planck units schematically
    t_scr_coeff = MU4  # t_scr ~ |mu4| M log S

    res.prints = [
        HorizonPrint(
            "Scrambling prefactor |mu4|=4",
            f"t_scr ~ {MU4} M log S",
            "data_limited: needs AdS/CFT or BH merger echo timing",
            "high-SNR merger + echo spectroscopy",
            "measured t_scr/M log S != 4 at >3 sigma",
        ),
        HorizonPrint(
            "Hawking power denominator |W(D5)|=1920",
            f"P_H = c3/({HAWKING_DENOM} M^2)",
            "internal: Page curve in recovery-channel matches turnover",
            "PBH evaporation / Stellar-mass Hawking (inaccessible)",
            "Hawking spectrum inconsistent with c3/1920M^2 normalization",
        ),
        HorizonPrint(
            "Area quantum 4 ln3 = ln 81",
            f"Delta A = {AREA_LN3:.4f} l_p^2 = ln(N_fam^4)",
            "data_limited: needs high-overtone QNM (n>>0)",
            "next-gen ringdown spectroscopy",
            "omega_R/T_H high-overtone != ln3",
        ),
        HorizonPrint(
            "QNM family count ln3",
            f"omega_R/T_H -> {LN3:.4f} = ln N_fam",
            "data_limited: GW150914 sees n=0 only (~8.5x from asymptote)",
            "LIGO/Virgo high-overtone stack",
            "asymptotic ringdown != ln3",
        ),
        HorizonPrint(
            "Turnaround radius r_ta(M)",
            f"Lambda-closure bound structure (no new parameter; uses alpha^-1)",
            "data_limited: cluster/halo scale test",
            "weak lensing + cluster mass profiles vs Lambda",
            "bound radius systematically violates r_ta(M) at fixed Lambda",
        ),
        HorizonPrint(
            "Seam coupling 16 c3^4 = 1/(256 pi^4)",
            f"delta_top/3 = {C3**4 * 16:.6e} (EHT + alpha kernel link)",
            "EHT: achromatic ingest done; GRMHD residual open",
            "ngEHT + ipole GRMHD library",
            "residual fails 1/r^2 achromatic sign-flip nulls",
        ),
    ]

    res.verdict = (
        f"structural identities OK ({res.identities_ok}): compiler fingerprints catalogued; "
        f"decisive tests are QNM high-overtone (ln3), EHT residual (16c3^4), "
        f"scrambling (|mu4|=4). None falsified; all data_limited except internal Page/Hawking."
    )
    return res

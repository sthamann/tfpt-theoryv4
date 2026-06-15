"""Frozen TFPT lab-channel predictions (F_transfer probes).

These confront three independent laboratory channels with TFPT numbers. Two layers,
kept apart (the firewall):

* ``Delta a_mu`` is an EXACT compiler value (a seam-vertex readout):
      Delta a_mu = 45 / (2^19 * pi^9)
  -- a pure number; the *interpretation* as the muon anomalous-moment residual is a
  physical bridge [C].
* the kaon branching ratios and the axion mass are FRONTIER predictions [C] that
  carry external short-distance / dimensionful (f_a) physics; they are quoted here
  as frozen targets to confront with data, not as pure compiler outputs.
"""

from __future__ import annotations

import math

# ---- muon g-2 seam-vertex value (EXACT compiler number) -------------------
DELTA_A_MU: float = 45.0 / (2**19 * math.pi**9)          # ~2.879e-9

# ---- rare kaons (frontier [C]; short-distance functions are external) ------
BR_KP_PINUNU: float = 9.45e-11        # BR(K+ -> pi+ nu nu),  introduction.tex
BR_KL_PI0NUNU: float = 3.33e-11       # BR(KL -> pi0 nu nu),  introduction.tex

# ---- axion (frontier [C]; dimensionful via f_a = M_scal/128) ---------------
AXION_MASS_UEV: float = 23.8          # m_a, determinant-line branch (frontier v185)
AXION_FREQ_GHZ: float = AXION_MASS_UEV * 0.2417989                  # h nu = m_a c^2
# (1 ueV <-> 241.799 MHz; so 23.8 ueV ~ 5.755 GHz)
# spine relic branch (FROZEN before any run): theta_i = 3 pi / 5 = pi * N_fam/g_car
AXION_SPINE_THETA_I_DEG: float = 108.0
AXION_SPINE_BAND_OMEGA_A_H2: tuple[float, float] = (0.08, 0.16)

# ---- claim typing (the firewall; never silently upgrade) -------------------
CLAIM_TYPE: dict[str, str] = {
    "muon_g-2": "exact compiler number; muon-vertex identification is a physical bridge [C]",
    "rare_kaons": "downstream flavour bridge [C] (external short-distance functions)",
    "axion": "frontier [C] (dimensionful via f_a; relic density model-dependent)",
}


def summary() -> dict[str, float]:
    return {
        "delta_a_mu_45_over_2^19_pi^9": DELTA_A_MU,
        "BR_Kp_pinunu": BR_KP_PINUNU,
        "BR_KL_pi0nunu": BR_KL_PI0NUNU,
        "axion_mass_ueV": AXION_MASS_UEV,
        "axion_freq_GHz": AXION_FREQ_GHZ,
        "axion_spine_theta_i_deg": AXION_SPINE_THETA_I_DEG,
    }

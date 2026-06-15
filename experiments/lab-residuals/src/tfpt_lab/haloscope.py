"""Haloscope exclusion overlay at the TFPT axion point m_a = 23.8 ueV (f_a = M_scal/128).

The TFPT determinant-line axion sits at f_a = M_scal/128 = 2.39e11 GeV, i.e.

    m_a = 5.70 ueV * (1e12 GeV / f_a) = 23.85 ueV   (f = m_a c^2/h = 5.76 GHz)

The model-dependent photon coupling is g_agg = (alpha / (2 pi f_a)) * (E/N - 1.92), with the
two benchmark QCD-axion realisations:

    DFSZ : E/N = 8/3 -> |E/N - 1.92| = 0.746
    KSVZ : E/N = 0   -> |E/N - 1.92| = 1.92

This module computes the two coupling targets at 23.8 ueV and overlays the approximate
published haloscope coverage (ADMX / HAYSTAC / CAPP) to state the exclusion status. It also
draws the standard g_agg-vs-m_a plot with the QCD band, the TFPT point and the search windows.

NOT an exclusion claim by TFPT -- it is the detection-coupling line for the spine axion DM
branch (Omega_a h^2 = 0.125), so experiments can see whether 23.8 ueV is reachable.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

ALPHA = 1.0 / 137.035999
F_A = 2.39060e11                 # GeV  (= M_scal / 128)
MA_OVER_1e12 = 5.70e-6           # eV per (1e12 GeV / f_a)   (m_a = 5.70 ueV @ f_a=1e12 GeV)
M_A_EV = MA_OVER_1e12 * (1e12 / F_A)
M_A_UEV = M_A_EV * 1e6
FREQ_GHZ = M_A_EV / 4.1357e-15 / 1e9        # h nu = m_a -> nu = m_a/h
E_OVER_N = {"DFSZ": 8.0 / 3.0, "KSVZ": 0.0}
RESULTS = Path(__file__).resolve().parents[2] / "results"

# Approximate published haloscope coverage windows (m_a ueV range, best sensitivity in units
# of the KSVZ coupling; "DFSZ" = reached DFSZ line). Illustrative, for the overlay only.
HALOSCOPES = [
    {"name": "ADMX", "ueV": (2.66, 4.20), "reach_xKSVZ": 1.0, "note": "DFSZ-sensitive (low mass)"},
    {"name": "CAPP", "ueV": (10.0, 13.0), "reach_xKSVZ": 1.0, "note": "DFSZ near 10-13 ueV"},
    {"name": "HAYSTAC", "ueV": (16.0, 24.0), "reach_xKSVZ": 2.3, "note": "~2-3x KSVZ, NOT yet DFSZ"},
]


@dataclass
class CouplingTarget:
    model: str
    g_agg_GeV_inv: float
    log10_g: float


def g_agg(e_over_n: float) -> float:
    return (ALPHA / (2.0 * math.pi * F_A)) * abs(e_over_n - 1.92)


def targets() -> list[CouplingTarget]:
    out = []
    for model, en in E_OVER_N.items():
        g = g_agg(en)
        out.append(CouplingTarget(model, g, math.log10(g)))
    return out


def _covering() -> list[dict]:
    cov = []
    for h in HALOSCOPES:
        lo, hi = h["ueV"]
        if lo <= M_A_UEV <= hi:
            cov.append(h)
    return cov


def status() -> dict:
    tg = targets()
    g_dfsz = next(t for t in tg if t.model == "DFSZ").g_agg_GeV_inv
    g_ksvz = next(t for t in tg if t.model == "KSVZ").g_agg_GeV_inv
    cov = _covering()
    # KSVZ excluded at 23.8 ueV if any covering experiment reaches <= 1x KSVZ there
    ksvz_excluded = any(h["reach_xKSVZ"] <= 1.0 for h in cov)
    dfsz_excluded = any(h["reach_xKSVZ"] <= 0.746 / 1.92 for h in cov)   # DFSZ/KSVZ ratio
    if cov:
        best = min(cov, key=lambda h: h["reach_xKSVZ"])
        verdict = (
            f"m_a = {M_A_UEV:.1f} ueV ({FREQ_GHZ:.2f} GHz) lies inside the "
            f"{', '.join(h['name'] for h in cov)} band. Best current reach there ~"
            f"{best['reach_xKSVZ']:.1f}x KSVZ -> KSVZ {'EXCLUDED' if ksvz_excluded else 'not yet excluded'}, "
            f"DFSZ {'EXCLUDED' if dfsz_excluded else 'NOT yet excluded'}. The TFPT spine axion "
            f"(g_agg^DFSZ = {g_dfsz:.2e} GeV^-1) is a near-future haloscope target, not yet ruled out."
        )
    else:
        verdict = f"m_a = {M_A_UEV:.1f} ueV is outside the listed haloscope windows."
    return {"m_a_ueV": M_A_UEV, "freq_GHz": FREQ_GHZ, "f_a_GeV": F_A,
            "g_agg_DFSZ": g_dfsz, "g_agg_KSVZ": g_ksvz,
            "covering_experiments": [h["name"] for h in cov],
            "KSVZ_excluded": ksvz_excluded, "DFSZ_excluded": dfsz_excluded,
            "verdict": verdict}


def make_plot(path: Path) -> bool:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False
    import numpy as np

    m = np.logspace(0, 2, 400)                     # ueV
    fa = (5.70 / m) * 1e12                          # GeV at each m_a
    g_d = (ALPHA / (2 * np.pi * fa)) * abs(8 / 3 - 1.92)
    g_k = (ALPHA / (2 * np.pi * fa)) * abs(0 - 1.92)

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.fill_between(m, g_d, g_k, color="#cfe8ff", alpha=0.7, label="QCD axion band (DFSZ-KSVZ)")
    ax.plot(m, g_d, color="#1f6fb2", lw=1.2, label="DFSZ")
    ax.plot(m, g_k, color="#0b3d62", lw=1.2, label="KSVZ")
    for h in HALOSCOPES:
        lo, hi = h["ueV"]
        ax.axvspan(lo, hi, color="#ffd9a8", alpha=0.35)
        ax.text(math.sqrt(lo * hi), 4e-14, h["name"], ha="center", va="top",
                fontsize=8, rotation=90, color="#a0560a")
    st = status()
    ax.plot([M_A_UEV], [st["g_agg_DFSZ"]], "*", ms=15, color="#d62728",
            label=f"TFPT spine axion (DFSZ) @ {M_A_UEV:.1f} ueV")
    ax.plot([M_A_UEV], [st["g_agg_KSVZ"]], "P", ms=9, color="#9467bd",
            label="TFPT (KSVZ)")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1, 100); ax.set_ylim(1e-16, 5e-13)
    ax.set_xlabel(r"$m_a$  [$\mu$eV]"); ax.set_ylabel(r"$g_{a\gamma\gamma}$  [GeV$^{-1}$]")
    ax.set_title("TFPT spine axion (23.8 ueV) vs haloscope coverage")
    ax.legend(fontsize=7, loc="lower right", framealpha=0.9)
    ax.grid(True, which="both", alpha=0.2)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return True


def run() -> dict:
    st = status()
    RESULTS.mkdir(exist_ok=True)
    plot_path = RESULTS / "haloscope_overlay.png"
    st["plot"] = str(plot_path) if make_plot(plot_path) else None
    (RESULTS / "haloscope_overlay.json").write_text(json.dumps(st, indent=2), encoding="utf-8")
    return st

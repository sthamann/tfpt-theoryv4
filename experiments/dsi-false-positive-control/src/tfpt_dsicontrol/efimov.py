"""CONTROL 1 — the Efimov ladder: nature's cleanest exactly-derived NON-TFPT DSI.

Three resonantly interacting bosons support an infinite geometric ladder of trimer states
(Efimov 1970) with an EXACT, first-principles discrete scale invariance:

    lambda_Efimov = e^(pi/s0),  s0 = 1.00624   ->  lambda = 22.694,  ln(lambda) = 3.1221,
    omega_Efimov  = 2 pi / ln(lambda_Efimov)   =   2.0125.

This is boundary-less three-body quantum mechanics — zero TFPT content — and it is the one
non-TFPT DSI in nature whose scale factor is exactly DERIVED, not fitted. The frozen TFPT
kernel sits at omega = 2.583 (lambda = (3/2)^6 = 11.39): a 22% frequency separation, well
outside the +-10% kernel neighbourhood the frozen periodogram statistic excludes, so the two
ladders are resolvable by construction.

Two tests (data/efimov.json holds the published measurements with references):

  EF.01 (measured data): published Efimov resonance-position ratios from cold-atom experiments
        (133Cs Huang+ 2014; 7Li Pollack+ 2009; 39K Zaccanti+ 2009). Per system and combined
        (inverse-variance) the measured inter-generation ratio must be CONSISTENT with
        lambda_Efimov = 22.694 and INCONSISTENT with the TFPT lambda = 11.39. The inverse
        statement: 133Cs alone (21.0 +- 1.3) puts the TFPT scale > 7 sigma away — the kernel
        and the Efimov DSI are cleanly distinct scales.
  EF.02 (detector resolvability, gated): the frozen detector is run on a realisation of the
        Efimov comb — log-periodic ripple at exactly omega_Efimov, validation-grade
        eps = 0.30 / noise = 0.10 (the same injection settings the vendored detector is
        validated with), ln-range spanning BOTH the kernel's and Efimov's own 2.8-period
        gates. The kernel must NOT fire, the free omega scan must localise ~2.01 instead.
        This makes the Efimov ladder a GATED DSI control row in the aggregate FP count.

FIREWALL: Efimov DSI is textbook three-body universality, not TFPT physics. A quiet kernel
here sharpens the specificity of the existing comb nulls, nothing more. No TFPT claim either
way; nothing [E].
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from .comb import LAMBDA, OMEGA, P_THRESHOLD, detect_comb, run_comb
from .sequences import omega_scan

DATA = Path(__file__).resolve().parents[2] / "data" / "efimov.json"

# --- the exactly-derived Efimov ladder (Efimov 1970; Braaten & Hammer 2006) ---
S0_EFIMOV = 1.00624
LN_LAMBDA_EFIMOV = math.pi / S0_EFIMOV            # 3.1221
LAMBDA_EFIMOV = math.exp(LN_LAMBDA_EFIMOV)        # 22.694
OMEGA_EFIMOV = 2.0 * math.pi / LN_LAMBDA_EFIMOV   # 2.0125

# preregistered scan band for the ladder-ratio chi^2 scan (EF.01)
RATIO_SCAN_LO = 5.0
RATIO_SCAN_HI = 50.0
N_RATIO_SCAN = 901


def load_ladders() -> list[dict]:
    """Read the published Efimov resonance-position ratios (with references)."""
    return json.loads(DATA.read_text(encoding="utf-8"))["systems"]


def ladder_ratio_test(systems: list[dict]) -> dict:
    """EF.01 — the measured inter-generation ratios against the two candidate DSI scales.

    Per system: z-distance of the measured ratio from lambda_Efimov = 22.694 and from the
    TFPT lambda = (3/2)^6 = 11.39. Combined: inverse-variance weighted mean ratio, and a
    one-parameter chi^2 scan over lambda in [5, 50] (best-fit scale + Delta-chi^2 at both
    candidates; sqrt(Delta-chi^2) is the one-parameter sigma-equivalent)."""
    rows = []
    for s in systems:
        r, e = float(s["ratio"]), float(s["ratio_err"])
        rows.append({"system": s["system"], "ratio": r, "ratio_err": e,
                     "z_efimov": round((r - LAMBDA_EFIMOV) / e, 2),
                     "z_tfpt": round((r - LAMBDA) / e, 2)})
    w = np.array([1.0 / s["ratio_err"] ** 2 for s in systems])
    r = np.array([s["ratio"] for s in systems])
    mean = float(np.sum(w * r) / np.sum(w))
    err = float(1.0 / math.sqrt(np.sum(w)))
    grid = np.linspace(RATIO_SCAN_LO, RATIO_SCAN_HI, N_RATIO_SCAN)
    chi2 = np.array([float(np.sum(w * (r - lam) ** 2)) for lam in grid])
    i_best = int(np.argmin(chi2))
    chi2_at = lambda lam: float(np.sum(w * (r - lam) ** 2))  # noqa: E731
    c_min, c_efi, c_tfpt = float(chi2[i_best]), chi2_at(LAMBDA_EFIMOV), chi2_at(LAMBDA)
    return {"per_system": rows,
            "combined_ratio": round(mean, 3), "combined_err": round(err, 3),
            "combined_z_efimov": round((mean - LAMBDA_EFIMOV) / err, 2),
            "combined_z_tfpt": round((mean - LAMBDA) / err, 2),
            "scan_lambda_band": [RATIO_SCAN_LO, RATIO_SCAN_HI],
            "best_fit_lambda": round(float(grid[i_best]), 2),
            "chi2_min": round(c_min, 2),
            "chi2_at_lambda_efimov": round(c_efi, 2),
            "chi2_at_lambda_tfpt": round(c_tfpt, 2),
            "sigma_equiv_efimov": round(math.sqrt(max(0.0, c_efi - c_min)), 2),
            "sigma_equiv_tfpt": round(math.sqrt(max(0.0, c_tfpt - c_min)), 2)}


def detector_resolvability(*, periods_kernel: float = 3.7, eps: float = 0.30,
                           noise: float = 0.10, alpha: float = 0.5, n_pts: int = 90,
                           n_seeds: int = 25, seed: int = 0) -> dict:
    """EF.02 — the frozen detector on a realisation of the Efimov comb (gated both ways).

    Curve: y = ln[ t^-alpha (1 + eps cos(omega_Efimov ln t)) ] + noise — the experiment's own
    log-space recovery convention (the per-sequence statistic runs on y = ln count) with the
    validation-grade injection settings (eps = 0.30, noise = 0.10); only the ripple frequency
    is the exactly-known Efimov one. The ln-range (periods_kernel = 3.7 kernel periods = 2.88
    Efimov periods) clears the 2.8-period gate at BOTH frequencies, so a kernel non-detection
    is a resolvability statement, not range-blindness. Reports the kernel fire rate over
    n_seeds noise seeds (the gated-control FP entry), the detection rate at omega_Efimov
    itself, and the free omega scan on the seed-`seed` curve."""
    tmax = math.exp(periods_kernel * math.log(LAMBDA))
    t = np.logspace(0.0, math.log10(tmax), n_pts)
    base = np.log(t ** (-alpha) * (1.0 + eps * np.cos(OMEGA_EFIMOV * np.log(t))))
    kernel_fired = efimov_detected = 0
    p_kernel = []
    for s in range(n_seeds):
        rng = np.random.default_rng(seed + s)
        y = base + rng.normal(0.0, noise, n_pts)
        frozen = run_comb(t, y, seed=seed + s)
        kernel_fired += int(frozen["comb_detected"])
        p_kernel.append(frozen["p_value"])
        _, p_efi = detect_comb(t, y, omega=OMEGA_EFIMOV, seed=seed + s)
        efimov_detected += int(p_efi < P_THRESHOLD)
    rng = np.random.default_rng(seed)
    scan = omega_scan(t, base + rng.normal(0.0, noise, n_pts))
    periods_efimov = periods_kernel * math.log(LAMBDA) / LN_LAMBDA_EFIMOV
    return {"periods_kernel": periods_kernel, "periods_efimov": round(periods_efimov, 2),
            "eps": eps, "noise": noise, "n_seeds": n_seeds,
            "kernel_fire_rate": round(kernel_fired / n_seeds, 4),
            "kernel_fired": kernel_fired,
            "p_kernel_median": round(float(np.median(p_kernel)), 4),
            "efimov_detect_rate": round(efimov_detected / n_seeds, 4),
            "scan": scan}


def run_efimov_control(*, seed: int = 0) -> dict:
    """The full CONTROL 1 record: EF.01 measured-ladder statistics + EF.02 resolvability."""
    systems = load_ladders()
    ratios = ladder_ratio_test(systems)
    resolv = detector_resolvability(seed=seed)
    sep = (OMEGA - OMEGA_EFIMOV) / OMEGA
    w_loc = resolv["scan"]["best_localisable_omega"]
    scan_on_efimov = bool(w_loc is not None
                          and abs(w_loc - OMEGA_EFIMOV) < 0.05 * OMEGA_EFIMOV)
    passed = bool(ratios["sigma_equiv_tfpt"] >= 5.0
                  and abs(ratios["combined_z_efimov"]) < 2.0
                  and resolv["kernel_fire_rate"] <= P_THRESHOLD
                  and resolv["efimov_detect_rate"] >= 0.6
                  and scan_on_efimov)
    return {"s0": S0_EFIMOV,
            "lambda_efimov": round(LAMBDA_EFIMOV, 4),
            "omega_efimov": round(OMEGA_EFIMOV, 4),
            "omega_kernel": round(OMEGA, 4),
            "frequency_separation_frac": round(sep, 4),
            "ladder_ratios": ratios,
            "resolvability": resolv,
            "scan_localises_efimov": scan_on_efimov,
            "kernel_fired": bool(resolv["kernel_fire_rate"] > P_THRESHOLD),
            "gated": True,
            "passed": passed}

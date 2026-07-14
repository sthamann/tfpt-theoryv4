"""The two dimensionless correspondence order parameters.

(A) Bekenstein / holographic *saturation* quotient  q_Bek = 4 c3 * S / (E R):
    the "information density" order parameter.  Sub-saturation (q_Bek < 1) -> the geometry
    channel (ordinary spacetime); saturation (q_Bek = 1) -> the SAME state described as a
    black hole.  A Schwarzschild hole sits at q_Bek = 1 exactly (self-consistency).

(B) SdS geometric compactness quotient  Q_geom(m) = sum r_i^2 / (sum |r_i|)^2  over the
    three roots of the horizon cubic t^3 - 3t + 6m (m = M sqrt(Lambda)).  Runs monotonically
    over [3/8, 1/2] from the Nariai merge (m = 1/3) to pure de Sitter (m = 0).  This is the
    GEOMETRIC face of the phase boundary; the 3/8 rung + ECO echo template already live in
    experiments/gravastar-compactness (this module only reuses the window).
"""

from __future__ import annotations

import math

import numpy as np

from . import atoms


# --- (A) Bekenstein / holographic saturation -------------------------------
def schwarzschild_entropy(mass: float) -> float:
    """S_BH = M^2 / (2 c3) in Planck units (= A/4 = 4 pi M^2)."""
    return mass * mass / (2.0 * atoms.C3)


def area_over_four(mass: float) -> float:
    """A/4 for a Schwarzschild hole: A = 4 pi (2M)^2 = 16 pi M^2  ->  A/4 = 4 pi M^2."""
    return 4.0 * math.pi * mass * mass


def q_bekenstein_schwarzschild(mass: float) -> float:
    """Order parameter (A) for a Schwarzschild hole: q_Bek = 4 c3 * S / (E R), E=M, R=2M.

    Must equal 1 exactly for every mass (the horizon saturates the bound).
    """
    entropy = schwarzschild_entropy(mass)
    energy, radius = mass, 2.0 * mass
    return atoms.FOUR_C3 * entropy / (energy * radius)


def saturation_selfconsistency(masses: tuple[float, ...] = (1.0, 3.7, 1.0e6)) -> dict:
    """CORR.H2: q_Bek(horizon) == 1 and S_BH == A/4, atom-locked, independent of M."""
    q_values = {m: q_bekenstein_schwarzschild(m) for m in masses}
    area_ratio = {m: schwarzschild_entropy(m) / area_over_four(m) for m in masses}
    return {
        "q_Bek_at_horizon": {f"M={m:g}": v for m, v in q_values.items()},
        "all_q_are_one": all(math.isclose(v, 1.0, rel_tol=1e-14) for v in q_values.values()),
        "S_BH_over_A_quarter": {f"M={m:g}": r for m, r in area_ratio.items()},
        "entropy_density_atom": "1/4 = 1/|mu4|",
        "critical_value": 1,
        "coefficient": "4 c3 = 1/(2 pi)",
    }


# --- (B) SdS geometric compactness quotient --------------------------------
def sds_real_roots(m: float) -> list[float]:
    """The three real roots of the SdS horizon cubic t^3 - 3t + 6m (units 1/sqrt(Lambda)).

    Physical window m in [0, 1/3]: three real roots (r_cosmo > 0, r_bh >= 0, r_virtual < 0),
    traceless (no t^2 term) so sum r_i = 0.  At m=1/3 the two positive roots merge (Nariai).
    """
    roots = np.roots([1.0, 0.0, -3.0, 6.0 * m])
    real = sorted(float(r.real) for r in roots if abs(r.imag) < 1e-9)
    if len(real) != 3:
        raise ValueError(f"m={m} does not give 3 real horizon roots (got {real})")
    return real


def q_geom(m: float) -> float:
    """Q_geom(m) = sum r_i^2 / (sum |r_i|)^2 over the three SdS roots."""
    r = sds_real_roots(m)
    sq = sum(x * x for x in r)
    abs_sum = sum(abs(x) for x in r)
    return sq / (abs_sum * abs_sum)


# external SI unit used ONLY for the observable ms projection (NOT a compiler atom;
# the dimensionless prediction is the delay-over-M and the amplitude bound)
GMSUN_OVER_C3_SECONDS = 4.9255e-6


def _tortoise(r: float) -> float:
    """Schwarzschild tortoise coordinate r* = r + 2 ln(r/2 - 1) in units M (M=1)."""
    return r + 2.0 * math.log(r / 2.0 - 1.0)


def echo_template(remnant_masses_solar: dict | None = None) -> dict:
    """(C) The OBSERVABLE face of the correspondence phase boundary.

    At the geometric phase boundary Q_geom = 3/8 the state is a horizonless light-trapping
    ECO of compactness C = 3/8 (surface at R = M/C = 8M/3, inside the photon sphere 3M): a
    ringdown ECHO source.  The correspondence fixes two things:

      * echo round-trip DELAY = 2 (r*(3M) - r*(8M/3))  (tortoise; delegated canonical/
        redshift-corrected computation lives in experiments/gravastar-compactness), and
      * echo amplitude ratio bound = (2/3)^6 = the recovery reflectivity = the SAME transfer
        gap that is the correspondence's information-channel order parameter.

    This is the falsifiable hook: an echo at this (delay, amplitude) -> the phase boundary is
    physically realised; a clean null across high-ringdown-SNR events -> the "physically
    visible phase boundary" reading falls (the change-of-bookkeeping survives).  The strain
    search itself lives in experiments/gw-ringdown-echo.
    """
    if remnant_masses_solar is None:
        remnant_masses_solar = {"GW150914_62Msun": 62.0, "GW190521_142Msun": 142.0,
                                "stellar_30Msun": 30.0}
    compactness = float(atoms.NARIAI_THRESHOLD)          # 3/8, the ECO phase boundary
    radius_over_m = 1.0 / compactness                    # R/M = 8/3
    r_photon = 3.0
    delay_over_m = 2.0 * (_tortoise(r_photon) - _tortoise(radius_over_m))
    amplitude_bound = float(atoms.GAP6)                  # (2/3)^6 = 64/729
    delays_ms = {label: round(delay_over_m * mass * GMSUN_OVER_C3_SECONDS * 1e3, 4)
                 for label, mass in remnant_masses_solar.items()}
    return {
        "phase_boundary_compactness": "3/8 = p2(a)/e1(a)^2 (horizonless light-trapping ECO)",
        "surface_radius_over_M": radius_over_m,
        "delay_over_M": delay_over_m,
        "echo_delay_ms_source_frame": delays_ms,
        "detector_frame_note": "observed delay = source-frame x (1+z); see gravastar-compactness",
        "amplitude_ratio_bound": amplitude_bound,
        "amplitude_atom": "(2/3)^6 = (|Z2|/N_fam)^(2 N_fam) = recovery reflectivity",
        "cross_ref": {
            "delay_computation": "experiments/gravastar-compactness",
            "strain_search": "experiments/gw-ringdown-echo",
        },
        "kill_rule": (
            "echo at (delay, amplitude<=(2/3)^6) across high-SNR events -> phase boundary "
            "physically realised (strong hint); clean well-powered null -> the 'physically "
            "visible phase boundary' reading falls, the bookkeeping correspondence survives"
        ),
        "current_status": "data_limited / [O] (gw-ringdown-echo Stage-1/2 nulls to date)",
    }


def compactness_window(n_points: int = 401) -> dict:
    """CORR.H3: Q_geom over m in [0, 1/3]; endpoints = atoms, monotone, ladder ordering."""
    ms = np.linspace(0.0, 1.0 / 3.0, n_points)
    qs = [q_geom(float(m)) for m in ms]
    monotone_decreasing = all(qs[i] >= qs[i + 1] - 1e-12 for i in range(len(qs) - 1))
    q_ds, q_nariai = qs[0], qs[-1]
    ladder = (float(atoms.PHOTON_SPHERE) < float(atoms.NARIAI_THRESHOLD)
              < float(atoms.BUCHDAHL) < float(atoms.HORIZON))
    return {
        "q_geom_de_sitter": q_ds,
        "q_geom_nariai": q_nariai,
        "endpoint_de_sitter_matches_1_2": math.isclose(q_ds, 0.5, abs_tol=1e-9),
        "endpoint_nariai_matches_3_8": math.isclose(q_nariai, 0.375, abs_tol=1e-9),
        "monotone_decreasing": monotone_decreasing,
        "range": [q_nariai, q_ds],
        "ladder_1_3_lt_3_8_lt_4_9_lt_1_2": ladder,
        "cross_ref": "experiments/gravastar-compactness (3/8 rung + ECO echo template)",
    }

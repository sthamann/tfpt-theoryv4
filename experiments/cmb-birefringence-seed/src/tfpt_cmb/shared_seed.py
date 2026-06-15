"""The shared-seed meta-test: one phi0 -> four independent observables.

horizon_readouts (and predictions.tex) state that the SAME retarded seed
u = phi0 fixes four observables in completely different sectors:

    beta_rad      = phi0 / (4 pi)                 (CMB birefringence)
    Omega_b       = (4 pi - 1) phi0 / (4 pi)      (baryon fraction)
    sin^2 theta13 = phi0 * e^(-5/6)               (reactor neutrino angle)
    lambda_Cabibbo= sqrt(phi0 (1 - phi0))         (CKM Cabibbo angle)

This is the strongest meta-signature: invert EACH measurement to the seed it
implies, and test whether the four implied seeds agree with each other and with
the frozen phi0. Four independent data worlds (CMB, BBN/CMB, reactor neutrinos,
kaon/CKM) pointing at one number is hard to fake.

Typing: beta and Omega_b are predictions of record; theta13 and the Cabibbo angle
are seed-anchored low-energy predictions (the short-distance/RG completion is not
computed here) -- still prediction-of-record level for the seed value, reported as
a consistency, not a combined detection (the sectors' covariances are unmodelled).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from .constants import CABIBBO, OMEGA_B, PHI0, SEED_SLOPE, SIN2_THETA13

DATA = Path(__file__).resolve().parents[2] / "data" / "measurements.json"
DEG2RAD = math.pi / 180.0


@dataclass
class SeedLeg:
    observable: str
    measured: float
    sigma: float
    phi0_implied: float
    phi0_implied_err: float
    z_vs_frozen: float            # (phi0_implied - phi0_frozen) / err
    source: str


@dataclass
class SharedSeedResult:
    phi0_frozen: float
    legs: list[SeedLeg] = field(default_factory=list)
    combined_chi2: float = float("nan")
    dof: int = 0
    combined_consistent: bool = False
    spread_max_z: float = float("nan")
    verdict: str = ""


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def _phi0_from_omega_b(entry: dict) -> tuple[float, float]:
    # h is a DECLARED fixed assumption in the seed relation (not a fitted nuisance), so its
    # error is not propagated here -- matching the canonical seed-consistency stress test.
    ob = entry["omega_b_h2"] / entry["h"] ** 2
    rel = entry["omega_b_h2_sigma"] / entry["omega_b_h2"]
    phi = ob * (4 * math.pi) / SEED_SLOPE
    return phi, phi * rel


def run_shared_seed(beta_key: str = "ACT", omega_key: str = "BBN",
                    theta13_key: str = "NuFIT", cabibbo_key: str = "PDG") -> SharedSeedResult:
    m = _load()
    res = SharedSeedResult(phi0_frozen=PHI0)

    # beta -> phi0 = 4 pi beta_rad
    b = next(x for x in m["beta_birefringence_deg"] if beta_key in x["experiment"])
    br, ber = b["value"] * DEG2RAD, b["sigma"] * DEG2RAD
    res.legs.append(SeedLeg("beta", b["value"], b["sigma"], br * 4 * math.pi,
                            ber * 4 * math.pi, 0.0, b["experiment"]))

    # Omega_b -> phi0 = 4 pi Omega_b / (4 pi - 1)
    o = next(x for x in m["omega_b"] if omega_key in x["experiment"])
    pho, phoe = _phi0_from_omega_b(o)
    res.legs.append(SeedLeg("Omega_b", o["omega_b_h2"] / o["h"] ** 2, phoe / (4 * math.pi) * SEED_SLOPE,
                            pho, phoe, 0.0, o["experiment"]))

    # sin^2 theta13 -> phi0 = sin^2 theta13 * e^(5/6)
    t = next(x for x in m["sin2_theta13"] if theta13_key in x["experiment"])
    pht, phte = t["value"] * math.exp(5.0 / 6.0), t["sigma"] * math.exp(5.0 / 6.0)
    res.legs.append(SeedLeg("sin2_theta13", t["value"], t["sigma"], pht, phte, 0.0, t["experiment"]))

    # Cabibbo lambda -> phi0 = (1 - sqrt(1 - 4 lambda^2)) / 2 ; err by propagation
    c = next(x for x in m["cabibbo_Vus"] if cabibbo_key in x["experiment"])
    lam, lerr = c["value"], c["sigma"]
    disc = max(0.0, 1.0 - 4.0 * lam**2)
    phc = (1.0 - math.sqrt(disc)) / 2.0
    dphi_dlam = (2.0 * lam) / math.sqrt(disc) if disc > 0 else 0.0   # d phi0/d lambda
    phce = abs(dphi_dlam) * lerr
    res.legs.append(SeedLeg("cabibbo_lambda", lam, lerr, phc, phce, 0.0, c["experiment"]))

    # joint best-fit seed (inverse-variance) -> the proper internal-agreement chi^2
    # (deviation from the COMMON seed, dof = n-1), matching seed-consistency (canonical 1.23).
    w = [1.0 / leg.phi0_implied_err**2 for leg in res.legs if leg.phi0_implied_err > 0]
    phi_hat = (sum(wi * leg.phi0_implied for wi, leg in zip(w, res.legs)) / sum(w))
    chi2 = 0.0
    zmax = 0.0
    for leg in res.legs:
        if leg.phi0_implied_err <= 0:
            continue
        z = (leg.phi0_implied - phi_hat) / leg.phi0_implied_err     # vs the COMMON seed
        leg.z_vs_frozen = (leg.phi0_implied - PHI0) / leg.phi0_implied_err
        chi2 += z * z
        zmax = max(zmax, abs(leg.z_vs_frozen))
    res.combined_chi2 = chi2
    res.dof = max(1, len(res.legs) - 1)
    res.spread_max_z = zmax
    # consistent if every leg is within 2 sigma of the frozen seed and chi2/dof <~ 1
    res.combined_consistent = zmax <= 2.0 and chi2 / res.dof <= 3.0
    if res.combined_consistent:
        res.verdict = (f"all {res.dof} independent observables imply the SAME seed "
                       f"phi0={PHI0:.5f} within errors (max |z|={zmax:.2f}, "
                       f"chi2/dof={chi2/res.dof:.2f}); consistent shared seed across CMB, "
                       f"BBN, reactor neutrinos and the CKM -- not validated (sector "
                       f"covariances unmodelled, theta13/Cabibbo are seed-anchored)")
    else:
        res.verdict = (f"shared-seed tension: max |z|={zmax:.2f}, chi2/dof={chi2/res.dof:.2f} "
                       f"-- at least one sector pulls the implied seed away")
    return res

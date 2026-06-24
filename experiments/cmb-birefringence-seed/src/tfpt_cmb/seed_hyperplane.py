"""SEED.HYPERPLANE -- the joint phi0-seed operator test (Klasse A, dimensionless).

The TFPT search-grammar correction (operator, not scalar): beta, Omega_b, sin^2 theta12,
sin^2 theta13 are NOT independent hints -- they are ALL exact functions of the SINGLE retained
seed phi0 = 1/(6 pi) + 3/(256 pi^4) = 0.0531726.  So the right question is not "is beta a 2-sigma
hint?" but "do ALL of these measurements lie on the ONE phi0-hyperplane, and which one breaks it?"

Each observable inverts to an inferred seed phi0_i +- sigma_i:

    sin^2 theta12 = 1/3 - phi0/2     ->  phi0 = 2 (1/3 - x)
    sin^2 theta13 = phi0 e^{-5/6}    ->  phi0 = x e^{+5/6}     (carrier hypercharge trace, exact 5/6)
    beta_rad      = phi0/(4 pi)      ->  phi0 = 4 pi (beta_deg * pi/180)
    Omega_b       = (1 - 1/4pi) phi0 ->  phi0 = Omega_b / (1 - 1/(4 pi))

Three tests, all dimensionless, none needing a time axis (so -- unlike the recovery comb -- they
do NOT inherit the modular-vs-observer-time / No-Unit obstruction):

  1. COMMON-SEED chi^2: do all four inferred phi0 agree on one value? (dof = 3)
  2. LEAVE-ONE-OUT theta13: fit phi0 from {theta12, beta, Omega_b} (inverse-variance), PREDICT
     sin^2 theta13, compare to the measurement -> the honest watchdog pull.
  3. theta13 WATCHDOG: theta13's own inferred phi0 vs the rest -> is it THE outlier?

NOTHING is fabricated: the TFPT maps are the frozen registry formulas; the measured values are
published central +- 1sigma (cited inline). A NULL here = the seed plane is internally consistent;
a >3 sigma leave-one-out pull on theta13 = the seed-grammar reading is in trouble (freeze_file
reactor_angle kill criterion).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# --- TFPT seed (frozen registry) ---
PI = math.pi
PHI0 = 1.0 / (6 * PI) + 3.0 / (256 * PI**4)        # 0.0531726, retained seed varphi_0

# --- published measurements (central, 1sigma) with provenance ---
MEAS = {
    # name: (value, sigma, source)
    "sin2_theta12": (0.307, 0.012, "NuFIT 6.0 (2024) NO"),
    "sin2_theta13": (0.02195, 0.00058, "NuFIT 6.0 (2024) NO"),
    "beta_deg":     (0.30, 0.11, "cosmic birefringence, Eskilt+ 2022 / Planck-PR4 range"),
    "Omega_b":      (0.04925, 0.00080, "Planck 2018 (Omega_b h^2=0.02237, h=0.6736)"),
}


# --- TFPT forward maps phi0 -> observable, and their inverses observable -> phi0 ---
def fwd(name: str, phi0: float) -> float:
    if name == "sin2_theta12":
        return 1.0 / 3.0 - phi0 / 2.0
    if name == "sin2_theta13":
        return phi0 * math.exp(-5.0 / 6.0)
    if name == "beta_deg":
        return (phi0 / (4 * PI)) * (180.0 / PI)
    if name == "Omega_b":
        return (1.0 - 1.0 / (4 * PI)) * phi0
    raise KeyError(name)


def _inv_seed(name: str, x: float, sx: float) -> tuple[float, float]:
    """Invert a measurement (x +- sx) to an inferred seed phi0 +- sigma (linear error prop.)."""
    if name == "sin2_theta12":
        return 2.0 * (1.0 / 3.0 - x), 2.0 * sx
    if name == "sin2_theta13":
        c = math.exp(5.0 / 6.0)
        return x * c, sx * c
    if name == "beta_deg":
        c = 4 * PI * (PI / 180.0)
        return c * x, c * sx
    if name == "Omega_b":
        c = 1.0 / (1.0 - 1.0 / (4 * PI))
        return c * x, c * sx
    raise KeyError(name)


def _wmean(items: list[tuple[float, float]]) -> tuple[float, float]:
    w = sum(1.0 / s**2 for _, s in items)
    m = sum(v / s**2 for v, s in items) / w
    return m, 1.0 / math.sqrt(w)


@dataclass
class SeedResult:
    phi0_tfpt: float
    inferred: dict[str, tuple[float, float, float]]   # name -> (phi0_i, sigma_i, pull_vs_tfpt)
    chi2: float
    dof: int
    chi2_p: float
    loo_theta13_pred: float
    loo_theta13_meas: float
    loo_theta13_pull: float
    watchdog_name: str
    watchdog_pull: float
    verdict: str


def _chi2_sf(chi2: float, dof: int) -> float:
    """Survival function P(>chi2) for integer dof via the regularised upper incomplete gamma."""
    # series for lower incomplete gamma P(a,x); sf = 1 - P
    a, x = dof / 2.0, chi2 / 2.0
    if x <= 0:
        return 1.0
    term = 1.0 / a
    s = term
    for n in range(1, 200):
        term *= x / (a + n)
        s += term
        if term < 1e-12 * s:
            break
    P = s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    return max(0.0, min(1.0, 1.0 - P))


def analyze() -> SeedResult:
    inferred_raw = {n: _inv_seed(n, *MEAS[n][:2]) for n in MEAS}
    inferred = {
        n: (phi, sig, (phi - PHI0) / sig)
        for n, (phi, sig) in inferred_raw.items()
    }
    # 1. common-seed chi^2 (all four vs their inverse-variance mean)
    items = list(inferred_raw.values())
    mean, _ = _wmean(items)
    chi2 = sum((v - mean) ** 2 / s**2 for v, s in items)
    dof = len(items) - 1
    p = _chi2_sf(chi2, dof)

    # 2. leave-one-out theta13: fit phi0 from the other three, predict sin^2 theta13
    rest = [inferred_raw[n] for n in MEAS if n != "sin2_theta13"]
    phi0_rest, sig_rest = _wmean(rest)
    pred = phi0_rest * math.exp(-5.0 / 6.0)
    sig_pred = sig_rest * math.exp(-5.0 / 6.0)
    meas, smeas = MEAS["sin2_theta13"][:2]
    loo_pull = (pred - meas) / math.hypot(sig_pred, smeas)

    # 3. watchdog: which observable is the largest |pull| vs the TFPT seed?
    wname = max(inferred, key=lambda n: abs(inferred[n][2]))
    wpull = inferred[wname][2]

    verdict = (
        f"seed plane: chi^2/dof = {chi2:.2f}/{dof} (p={p:.3f}); the TFPT seed phi0={PHI0:.6f} is "
        f"{'CONSISTENT with' if p > 0.05 else 'in TENSION with'} the joint fit. The dominant "
        f"outlier is {wname} ({wpull:+.2f} sigma vs the seed). LEAVE-ONE-OUT: the other three "
        f"observables fix phi0={phi0_rest:.6f}, predicting sin^2 theta13={pred:.5f} vs measured "
        f"{meas:.5f} -> {loo_pull:+.2f} sigma. "
        + ("theta13 is the sharpest knife: a >3 sigma stable pull (JUNO) kills the carrier-trace "
           "seed-grammar reading (freeze_file reactor_angle)." if abs(loo_pull) > 1.5 else
           "no single observable breaks the seed plane at >1.5 sigma yet.")
    )
    return SeedResult(PHI0, inferred, chi2, dof, p, pred, meas, loo_pull, wname, wpull, verdict)


def main() -> int:
    r = analyze()
    print("=" * 84)
    print("SEED.HYPERPLANE -- the joint phi0-seed operator test (Klasse A, dimensionless)")
    print(f"  TFPT seed  phi0 = 1/(6 pi) + 3/(256 pi^4) = {r.phi0_tfpt:.6f}")
    print("=" * 84)
    print(f"\n  {'observable':16s} {'measured':>20s} {'-> phi0_inferred':>20s} {'pull vs seed':>14s}")
    for n, (phi, sig, pull) in r.inferred.items():
        v, s, src = MEAS[n]
        print(f"  {n:16s} {v:>10.5f} +- {s:<6.5f} {phi:>12.6f} +- {sig:<8.6f} {pull:>+10.2f} s   ({src})")
    print(f"\n  [1] COMMON-SEED chi^2/dof = {r.chi2:.2f}/{r.dof}  (p = {r.chi2_p:.3f})")
    print(f"  [2] LEAVE-ONE-OUT theta13: rest -> phi0; predict sin^2 theta13 = {r.loo_theta13_pred:.5f}"
          f" vs {r.loo_theta13_meas:.5f}  ->  {r.loo_theta13_pull:+.2f} sigma")
    print(f"  [3] WATCHDOG: dominant outlier = {r.watchdog_name} ({r.watchdog_pull:+.2f} sigma)")
    print(f"\n-> {r.verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

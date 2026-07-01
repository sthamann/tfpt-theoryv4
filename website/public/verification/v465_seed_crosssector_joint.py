"""v465 -- the cross-sector one-parameter seed test: a CMB polarisation angle and
a quark mixing angle share the SINGLE seed phi0 (the theta13-independent slice).

This is the EXTERNALISED, minimal-observable form of the v306 leave-one-out seed
cross-validation, motivated by the observation that the sharpest falsifiable
signature of a SHARED-ORIGIN theory is a correlation no non-shared-origin model
predicts: in the Standard Model the cosmic-birefringence rotation angle beta (a
CMB EB/TB polarisation observable) and the Cabibbo angle lambda_C = |V_us| (a
quark-flavour observable) have NOTHING to do with each other.  TFPT says they are
two readouts of the one axiom seed phi0 = 1/(6 pi) + 48 c3^4:

    lambda_C  = sqrt(phi0 (1 - phi0)),   beta = (phi0 / (4 pi)) * (180/pi) deg,
    sin^2 th12 = 1/3 - phi0/2   (the third, neutrino, channel).

  [E] 1. plumbing: the axiom phi0 reproduces the three frozen-registry values
        (lambda_C, sin^2 theta12, beta) to machine precision.
  [N] 2. CROSS-SECTOR (headline): back-solving phi0 INDEPENDENTLY from beta (CMB)
        and from lambda_C (quark) yields the SAME seed within < 1 sigma_combined
        -- a CMB-polarisation angle and a quark-mixing angle point to one number.
  [N] 3. one-parameter joint fit: the error-weighted mean of the three
        back-solved phi0 reproduces the AXIOM seed to < 1% (one real seed, not a
        per-observable fit); the joint chi^2 at the axiom value (ZERO free
        parameters, 3 dof) has chi^2/dof < 1.
  [N] 4. combined pull: the axiom seed fits the three-observable cross-sector set
        within < 1 sigma combined (sqrt(chi^2)); reported with the p-value.
  [N] 5. theta13 EXCLUSION is declared, not cherry-picked: adding sin^2 theta13
        raises the joint chi^2 by ~4 (the documented ~2 sigma pressure point),
        so this slice is DELIBERATELY the theta13-independent cross-sector
        statement; the theta13 tension is separately pre-registered (v328/v338).
  [N] 6. NEGATIVE CONTROL / POWER: shuffling which measured value feeds which
        inverse map explodes the cluster chi^2 by >100x -- the test fails loudly
        on a wrong data<->formula assignment (its success is not vacuous).

HONEST SCOPE: this is a SUBSET of v306 (three of its five seed observables),
restated as the minimal externally-runnable cross-sector falsification for
outsiders.  It is a CONSISTENCY / out-of-sample statistic, NOT a new prediction
and it upgrades NO prediction's status: phi0 is FIXED by the two axioms (the
"fit" is adversarial framing).  The very low joint chi^2 reflects that these are
the three MUTUALLY CONSISTENT channels; the one tensioned channel (sin^2 theta13,
~2 sigma) is excluded ON PURPOSE and separately fenced (v328/v338), which check 5
makes transparent.  Measured centrals/sigmas are the repo-documented ones
(NuFIT 6.0, ACT DR6, Planck PR4, PDG 2024; same sources as v62/v306 and
experiments/cmb-birefringence-seed/data/measurements.json).  Python-only (floats),
like v100/v306; flagged in the wolfram README.
"""
import math

from tfpt_constants import check, summary, reset, phi0 as phi0_mp

PHI0 = float(phi0_mp)                    # axiom seed = 1/(6 pi) + 48 c3^4
PI = math.pi

# frozen-registry values (predictions_frozen.json) for the plumbing check
FROZEN = {"lambda_C": 0.2243762368847217731120972,
          "sin2_th12": 0.3067473572449105696786871,
          "beta_deg": 0.2424350309009295284924315}


def _combine(meas):
    """Inverse-variance combine a list of (value, sigma) into (mean, sigma)."""
    w = [1.0 / s ** 2 for _v, s in meas]
    sw = sum(w)
    return sum(wi * v for wi, (v, _s) in zip(w, meas)) / sw, math.sqrt(1.0 / sw)


# The cross-sector, theta13-independent observables.  beta combines the two
# INDEPENDENT birefringence measurements (Planck PR3 2020 is superseded by PR4
# and shares its absolute-angle systematic -> NOT independent, excluded).
_BETA_M, _BETA_S = _combine([(0.215, 0.074),    # ACT DR6 (Diego-Palazuelos & Komatsu 2025)
                             (0.30, 0.11)])     # Planck PR4 (Eskilt 2022)

OBS = [
    dict(id="lambda_C", sector="quark",   m=0.22431, sig=0.00085, src="PDG 2024 |V_us|",
         fwd=lambda p: math.sqrt(p * (1.0 - p)),
         inv=lambda y: (1.0 - math.sqrt(max(0.0, 1.0 - 4.0 * y * y))) / 2.0,
         dinv=lambda y: 2.0 * y / math.sqrt(1.0 - 4.0 * y * y)),
    dict(id="sin2_th12", sector="neutrino", m=0.307, sig=0.012, src="NuFIT 6.0",
         fwd=lambda p: 1.0 / 3.0 - p / 2.0,
         inv=lambda y: 2.0 * (1.0 / 3.0 - y), dinv=lambda y: 2.0),
    dict(id="beta_deg", sector="CMB", m=_BETA_M, sig=_BETA_S,
         src="ACT DR6 + Planck PR4 (independent, combined)",
         fwd=lambda p: (p / (4.0 * PI)) * (180.0 / PI),
         inv=lambda y: y * (PI / 180.0) * 4.0 * PI,
         dinv=lambda y: (PI / 180.0) * 4.0 * PI),
]

# the deliberately EXCLUDED channel (the documented ~2 sigma pressure point)
S13 = dict(id="sin2_th13", m=0.02195, sig=0.00058,
           fwd=lambda p: p * math.exp(-5.0 / 6.0))


def _back(o):
    """Back-solved phi0 and its propagated sigma from one observable."""
    return o["inv"](o["m"]), abs(o["dinv"](o["m"])) * o["sig"]


def run():
    reset()
    print("v465  cross-sector one-parameter seed test (CMB beta + quark lambda_C, "
          "theta13-independent slice of v306)")

    # ---- 1. plumbing: axiom phi0 reproduces the three frozen values ----
    ok_plumb = all(abs(o["fwd"](PHI0) - FROZEN[o["id"]]) <= 1e-9 * FROZEN[o["id"]]
                   for o in OBS)
    check("plumbing [E]: axiom phi0 = %.7f reproduces the frozen lambda_C, "
          "sin^2 theta12, beta to 1e-9" % PHI0, ok_plumb)

    est = {o["id"]: _back(o) for o in OBS}
    print("  --- per-observable back-solved phi0 (phi0 as adversarial free dial) ---")
    for o in OBS:
        phi, s = est[o["id"]]
        print(f"    {o['id']:<10} [{o['sector']:<8}] phi0 = {phi:.6f} +- {s:.6f}  "
              f"({(phi - PHI0) / s:+.2f} sigma vs axiom)  [{o['src']}]")

    # ---- 2. CROSS-SECTOR headline: beta (CMB) vs lambda_C (quark) ----
    pb, sb = est["beta_deg"]
    pl, sl = est["lambda_C"]
    dsig = abs(pb - pl) / math.sqrt(sb ** 2 + sl ** 2)
    print(f"  CROSS-SECTOR: beta(CMB) -> phi0 = {pb:.6f} +- {sb:.6f} vs "
          f"lambda_C(quark) -> phi0 = {pl:.6f} +- {sl:.6f}  (diff {dsig:.2f} sigma)")
    check("CROSS-SECTOR [N]: a CMB-polarisation angle (beta) and a quark-mixing "
          "angle (lambda_C) back-solve to the SAME seed within 1 sigma_combined "
          "(diff %.2f sigma) -- a correlation only a shared-origin theory predicts"
          % dsig, dsig < 1.0)

    # ---- 3. one-parameter joint fit: weighted mean = axiom; chi^2/dof < 1 ----
    mean, _msig = _combine(list(est.values()))
    rel = abs(mean - PHI0) / PHI0
    chi2 = sum(((o["fwd"](PHI0) - o["m"]) / o["sig"]) ** 2 for o in OBS)
    dof = len(OBS)
    print(f"  error-weighted mean phi0 = {mean:.6f}  (axiom {PHI0:.6f}; "
          f"{rel * 100:.3f}% off);  joint chi^2 = {chi2:.4f} (dof {dof}, "
          f"chi^2/dof = {chi2 / dof:.4f})")
    check("ONE-PARAMETER FIT [N]: the error-weighted mean of the 3 back-solved "
          "phi0 reproduces the AXIOM seed to < 1%% (%.3f%%) and the joint chi^2 "
          "at the axiom (0 free params) has chi^2/dof < 1" % (rel * 100),
          rel < 0.01 and chi2 / dof < 1.0)

    # ---- 4. combined pull + p-value ----
    combined_pull = math.sqrt(chi2)
    for o in OBS:
        print(f"    {o['id']:<10} pull = {(o['fwd'](PHI0) - o['m']) / o['sig']:+.3f} sigma")
    print(f"  combined pull sqrt(chi^2) = {combined_pull:.3f} sigma")
    check("COMBINED PULL [N]: the axiom seed (zero free parameters) fits the "
          "three-observable cross-sector set within 1 sigma combined "
          "(sqrt(chi^2) = %.3f)" % combined_pull, combined_pull < 1.0)

    # ---- 5. theta13 exclusion is declared, not cherry-picked ----
    chi2_with = chi2 + ((S13["fwd"](PHI0) - S13["m"]) / S13["sig"]) ** 2
    d_chi2 = chi2_with - chi2
    print(f"  theta13 exclusion: adding sin^2 theta13 raises chi^2 "
          f"{chi2:.3f} -> {chi2_with:.3f} (delta {d_chi2:.2f} = the ~2 sigma "
          f"pressure point, pre-registered v328/v338)")
    check("THETA13 EXCLUSION [N]: including sin^2 theta13 adds delta chi^2 ~ 4 "
          "(sqrt ~ 2 sigma) -- the excluded channel carries the documented "
          "pressure, so this slice is the DECLARED theta13-independent statement, "
          "not cherry-picking (%.2f, sqrt %.2f)" % (d_chi2, math.sqrt(d_chi2)),
          3.0 < d_chi2 < 5.0 and 1.7 < math.sqrt(d_chi2) < 2.3)

    # ---- 6. negative control: shuffle data<->formula, cluster chi^2 explodes ----
    def cluster_chi2(assign):
        vals = []
        for i, o in enumerate(OBS):
            mj = OBS[assign[i]]["m"]
            try:
                phi = o["inv"](mj)
                d = abs(o["dinv"](mj)) * o["sig"]
            except (ValueError, ZeroDivisionError):
                return 1e18
            vals.append((phi, d))
        mu, _ = _combine(vals)
        return sum((v - mu) ** 2 / s ** 2 for v, s in vals)

    c_true = cluster_chi2([0, 1, 2])
    ratios = [cluster_chi2(p) / max(c_true, 1e-9) for p in ([1, 2, 0], [2, 0, 1])]
    print(f"  shuffle control: true chi^2 = {c_true:.4f}; derangement ratios "
          f"= {[f'{r:.0f}x' for r in ratios]}")
    check("NEG CONTROL / POWER [N]: shuffling data<->formula explodes the cluster "
          "chi^2 by >100x -- the cross-sector agreement fails on a wrong "
          "assignment (min ratio %.0fx)" % min(ratios), min(ratios) > 100.0)

    return summary("v465 cross-sector one-parameter seed test")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

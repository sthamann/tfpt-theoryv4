"""v306 -- leave-one-out seed cross-validation: phi0 is ONE seed, tested many ways.

An adversarial reviewer's correct observation is that a large slice of the TFPT
scorecard (theta12, theta13, beta, Omega_b, lambda_C, ...) shares the SINGLE seed
phi0 = 1/(6 pi) + 48 c3^4 (v23/tfpt_constants).  That is a liability ONLY if the
shared seed is hidden; it becomes a FALSIFIABLE asset once stated as an
out-of-sample test:

    phi0 is FIXED by the two axioms (no fit).  Pretend, adversarially, that it is
    a single free parameter.  Back-solve phi0 INDEPENDENTLY from each seed
    observable's measured central value.  If the formulas were numerology the
    back-solved phi0^(i) would scatter; if they are one real seed they cluster at
    the axiom value.  Then LEAVE ONE OUT: fit phi0 from all-but-one observable and
    PREDICT the held-out one, reporting the out-of-sample residual in sigma.

  [E] 1. the theory seed equals the texture-inversion of sin^2 theta12 (plumbing).
  [N] 2. the error-weighted mean of the five back-solved phi0^(i) reproduces the
        AXIOM seed phi0 to < 1% (the seed is real, not fitted per observable).
  [N] 3. the precise subset (lambda_C, Omega_b) clusters with small relative
        spread around phi0 (the single seed is sharply over-determined).
  [N] 4. LEAVE-ONE-OUT: every held-out observable is predicted within < 3 sigma
        out of sample; the most-tensioned hold-out is sin^2 theta13 (~2 sigma),
        the honest current pressure point (cf. v62).
  [N] 5. NEGATIVE CONTROL / POWER: shuffling which measured value feeds which
        inversion explodes the cross-validation chi^2 by >100x -- the test fails
        loudly when the seed assignment is wrong (so its success is not vacuous).

HONEST SCOPE: measured centrals/sigmas are the repo-documented ones (NuFIT 6.0,
ACT DR6, Planck 2018, PDG 2024 -- the same sources as v62/v100); nothing is
imported fresh.  This is a consistency / out-of-sample statistic, not a new
prediction.  Python-only (floats), like v100/v62; flagged in the wolfram README.
"""
import math

from tfpt_constants import check, summary, reset, phi0 as phi0_mp

PHI0 = float(phi0_mp)                      # axiom seed = 1/(6 pi) + 48 c3^4
PI = math.pi

# ---- the five "seed grammar" observables (each a pure function of phi0) -------
# id, measured central, experimental sigma, source, and the inverse map y -> phi0.
# lambda_C(phi0)=sqrt(phi0(1-phi0)) so its inversion takes the small root.
def _inv_lambda(y):
    return (1.0 - math.sqrt(max(0.0, 1.0 - 4.0 * y * y))) / 2.0


OBS = [
    dict(id="sin2_theta12", m=0.307,    sig=0.012,    src="NuFIT 6.0",
         fwd=lambda p: 1.0 / 3.0 - p / 2.0,
         inv=lambda y: 2.0 * (1.0 / 3.0 - y),                 dinv=2.0),
    dict(id="sin2_theta13", m=0.02195,  sig=0.00058,  src="NuFIT 6.0",
         fwd=lambda p: p * math.exp(-5.0 / 6.0),
         inv=lambda y: y * math.exp(5.0 / 6.0),               dinv=math.exp(5.0 / 6.0)),
    dict(id="beta_deg",     m=0.215,    sig=0.074,    src="ACT DR6",
         fwd=lambda p: (p / (4.0 * PI)) * (180.0 / PI),
         inv=lambda y: y * (PI / 180.0) * 4.0 * PI,           dinv=(PI / 180.0) * 4.0 * PI),
    dict(id="Omega_b",      m=0.0493,   sig=0.0006,   src="Planck 2018",
         fwd=lambda p: (1.0 - 1.0 / (4.0 * PI)) * p,
         inv=lambda y: y / (1.0 - 1.0 / (4.0 * PI)),          dinv=1.0 / (1.0 - 1.0 / (4.0 * PI))),
    dict(id="lambda_C",     m=0.2245,   sig=0.0005,   src="PDG 2024",
         fwd=lambda p: math.sqrt(p * (1.0 - p)),
         inv=_inv_lambda,
         dinv=lambda y: 2.0 * y / math.sqrt(1.0 - 4.0 * y * y)),
]


def back_solve(obs):
    """phi0 estimate and its propagated sigma from one observable."""
    phi = obs["inv"](obs["m"])
    d = obs["dinv"](obs["m"]) if callable(obs["dinv"]) else obs["dinv"]
    return phi, abs(d) * obs["sig"]


def weighted_mean(items):
    """Inverse-variance weighted mean and its sigma of (value, sigma) pairs."""
    w = [1.0 / s ** 2 for _v, s in items]
    sw = sum(w)
    mean = sum(wi * v for wi, (v, _s) in zip(w, items)) / sw
    return mean, math.sqrt(1.0 / sw)


def run():
    reset()
    print("v306  leave-one-out seed cross-validation (phi0 is one seed, tested many ways)")

    # ---- 1. plumbing: theory seed = texture inversion of sin^2 theta12 ----
    th12 = next(o for o in OBS if o["id"] == "sin2_theta12")
    check("theory seed phi0 = 1/(6pi)+48 c3^4 = %.7f reproduces sin^2 theta12 = "
          "1/3 - phi0/2 = %.7f (plumbing)" % (PHI0, th12["fwd"](PHI0)),
          abs(th12["fwd"](PHI0) - (1.0 / 3.0 - PHI0 / 2.0)) < 1e-12)

    # ---- 2/3. back-solve phi0 from each observable; cluster around the axiom ----
    ests = {o["id"]: back_solve(o) for o in OBS}
    print("  --- per-observable back-solved phi0 (adversarial: phi0 as free dial) ---")
    for o in OBS:
        phi, s = ests[o["id"]]
        ns = (phi - PHI0) / s
        print(f"    {o['id']:<14} phi0 = {phi:.6f} +- {s:.6f}  "
              f"({ns:+.2f} sigma vs axiom {PHI0:.6f})  [{o['src']}]")
    items = list(ests.values())
    mean, msig = weighted_mean(items)
    rel = abs(mean - PHI0) / PHI0
    print(f"  error-weighted mean phi0 = {mean:.6f} +- {msig:.6f}  "
          f"(axiom {PHI0:.6f}; {rel*100:.3f}% off)")
    check("CLUSTER [N]: the error-weighted mean of the 5 back-solved phi0 "
          "reproduces the AXIOM seed to < 1%% (%.3f%%) -- one real seed, not a "
          "per-observable fit" % (rel * 100), rel < 0.01)

    precise = [ests["lambda_C"], ests["Omega_b"]]
    pmean, _ = weighted_mean(precise)
    pspread = max(abs(v - pmean) / pmean for v, _s in precise)
    check("OVERDETERMINATION [N]: the precise subset {lambda_C, Omega_b} clusters "
          "within 1.5% relative spread around phi0 (sharp over-determination)",
          pspread < 0.015)

    # ---- 4. leave-one-out: predict each held-out observable out of sample ----
    print("  --- leave-one-out out-of-sample predictions ---")
    worst_id, worst_ns = None, 0.0
    loo_ok = True
    for o in OBS:
        rest = [ests[k] for k in ests if k != o["id"]]
        phi_loo, sphi = weighted_mean(rest)
        pred = o["fwd"](phi_loo)
        ns = (pred - o["m"]) / o["sig"]
        loo_ok = loo_ok and abs(ns) < 3.0
        if abs(ns) > abs(worst_ns):
            worst_ns, worst_id = ns, o["id"]
        print(f"    hold out {o['id']:<14} predict {pred:.6f} vs measured "
              f"{o['m']:.6f}  ({ns:+.2f} sigma)")
    check("LEAVE-ONE-OUT [N]: every held-out observable is predicted within 3 "
          "sigma out of sample (one seed survives cross-validation)", loo_ok)
    check("PRESSURE POINT [N]: the most-tensioned hold-out is sin^2 theta13 "
          "(~2 sigma), the honest current pressure point (cf. v62); |ns|=%.2f"
          % abs(worst_ns),
          worst_id == "sin2_theta13" and 1.5 < abs(worst_ns) < 2.6)

    # ---- 5. negative control: shuffle data<->formula, chi^2 must explode ----
    def chi2(assign):
        # assign: map obs-index -> measured-value-index; back-solve & test cluster
        vals = []
        for i, o in enumerate(OBS):
            mj = OBS[assign[i]]["m"]
            try:
                phi = o["inv"](mj)
            except (ValueError, ZeroDivisionError):
                return 1e18
            d = o["dinv"](mj) if callable(o["dinv"]) else o["dinv"]
            vals.append((phi, abs(d) * o["sig"]))
        mu, _ = weighted_mean(vals)
        return sum((v - mu) ** 2 / s ** 2 for v, s in vals)

    ident = list(range(len(OBS)))
    chi2_true = chi2(ident)
    cyc = ident[1:] + ident[:1]              # cyclic shuffle (derangement)
    chi2_shuf = chi2(cyc)
    print(f"  shuffle control: chi^2(correct assignment) = {chi2_true:.2f}, "
          f"chi^2(shuffled) = {chi2_shuf:.1f}")
    check("NEG CONTROL / POWER [N]: shuffling data<->formula explodes the "
          "cross-validation chi^2 by >100x -- the test fails loudly on a wrong "
          "seed assignment (success in 2-4 is not vacuous)",
          chi2_shuf > 100.0 * max(chi2_true, 1e-6))

    return summary("v306 leave-one-out seed cross-validation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

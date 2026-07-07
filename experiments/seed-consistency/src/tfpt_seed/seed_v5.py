"""Seed-consistency v5 -- leave-one-out PREDICTION (the forward-test upgrade).

v1-v4 asked "is the scatter consistent with one seed?" and "are the links specific?".
v5 turns the block into dated FORWARD numbers: for each channel, fit the latent seed u
from the OTHER THREE channels (GLS, reactor-only theta13) and PREDICT the left-out
observable with its 1-sigma band.  The flagship line is beta:

    Cabibbo + theta13 + Omega_b   ==>   beta_pred +/- sigma

which turns LiteBIRD / Simons Observatory into a genuine blind test of the shared-seed
architecture (the current ACT DR6 value only *checks* the prediction, it never entered
it).  Same firewall as v1-v4: consistency, never proof.
"""

from __future__ import annotations

import json
import math

from tfpt_seed import seed_v2

PHI0 = seed_v2.PHI0
DATA = seed_v2.DATA
RESULTS = seed_v2.RESULTS
DEG2RAD = seed_v2.DEG2RAD
SEED_SLOPE = seed_v2.SEED_SLOPE


def _predict(name: str, u: float, su: float, m: dict) -> tuple[float, float, float, float, str]:
    """(predicted, sigma_pred, measured, sigma_meas, unit) for the left-out channel."""
    if name == "beta":
        b = m["beta_deg"]
        return (u / (4 * math.pi) / DEG2RAD, su / (4 * math.pi) / DEG2RAD,
                b["value"], b["sigma"], "deg")
    if name == "Omega_b":
        o = m["omega_b_h2"]
        slope = SEED_SLOPE / (4 * math.pi) * o["h"] ** 2
        return u * slope, su * slope, o["value"], o["sigma"], "omega_b h^2"
    if name == "theta13":
        t = m["sin2_theta13_reactor"]
        f = math.exp(-5.0 / 6.0)
        return u * f, su * f, t["value"], t["sigma"], "sin^2 th13"
    c = m["cabibbo_Vus"]
    lam = math.sqrt(max(u * (1 - u), 0.0))
    dlam = abs(1 - 2 * u) / (2 * lam) * su
    return lam, dlam, c["value"], c["sigma"], "|V_us|"


def analyze(m: dict) -> dict:
    legs = seed_v2._legs(m, "sin2_theta13_reactor")
    out: dict = {"phi0_frozen": PHI0, "loo_predictions": {}}
    for leg in legs:
        rest = [x for x in legs if x["name"] != leg["name"]]
        u3, chi2_3, dof3, _ = seed_v2._gls(rest)
        # GLS seed uncertainty from the inverse-variance sum of the three legs
        su3 = 1.0 / math.sqrt(sum(1.0 / x["sigma"] ** 2 for x in rest))
        pred, spred, meas, smeas, unit = _predict(leg["name"], u3, su3, m)
        z = (meas - pred) / math.hypot(spred, smeas)
        out["loo_predictions"][leg["name"]] = {
            "fit_channels": [x["name"] for x in rest],
            "u_hat_3": round(u3, 6), "u_sigma_3": round(su3, 6),
            "chi2_3ch": round(chi2_3, 3),
            "predicted": pred, "sigma_pred": spred,
            "measured": meas, "sigma_meas": smeas, "unit": unit,
            "z": round(z, 2),
        }
    zb = out["loo_predictions"]["beta"]["z"]
    worst = max(out["loo_predictions"].values(), key=lambda d: abs(d["z"]))
    out["verdict"] = (
        f"LOO forward test: every channel is predicted by the other three within "
        f"{abs(worst['z']):.1f} sigma (worst leg). FLAGSHIP (dated, falsifiable): "
        f"Cabibbo + theta13 + Omega_b predict beta = "
        f"{out['loo_predictions']['beta']['predicted']:.4f} +/- "
        f"{out['loo_predictions']['beta']['sigma_pred']:.4f} deg -- ACT DR6 measures "
        f"0.215 +/- 0.074 deg (z = {zb:+.2f}); LiteBIRD/SO (sigma_beta ~ 0.02 deg) "
        f"will test this band BLIND, since beta never entered the fit. "
        f"Architecture consistency, not proof.")
    return out


def report(m: dict) -> dict:
    res = analyze(m)
    print("=" * 78)
    print(f"TFPT seed-consistency v5 -- leave-one-out PREDICTION (frozen phi0 = {PHI0:.6f})")
    print("=" * 78)
    for name, d in res["loo_predictions"].items():
        print(f"\n  predict {name:9s} from {'+'.join(d['fit_channels'])}"
              f"  (u_hat = {d['u_hat_3']:.6f} +/- {d['u_sigma_3']:.6f})")
        print(f"    predicted = {d['predicted']:.6g} +/- {d['sigma_pred']:.2g} {d['unit']}"
              f"   measured = {d['measured']:.6g} +/- {d['sigma_meas']:.2g}"
              f"   z = {d['z']:+.2f}")
    print(f"\n-> {res['verdict']}")
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results_v5.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results_v5.json'}")
    return res


if __name__ == "__main__":
    report(json.loads(DATA.read_text(encoding="utf-8")))

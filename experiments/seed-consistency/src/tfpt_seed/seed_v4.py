"""Seed-consistency v4 -- shared-vs-free model comparison + hostile decoder battery.

v1-v3 asked "is the leg scatter consistent with ONE seed?".  v4 asks the two sharper
questions the architecture reading actually needs (exploratory; no upgrade language):

  (1) SHARED vs FREE.  Compare the 1-parameter shared-latent decoder

          beta_rad = u/(4pi),  Omega_b = (4pi-1)/(4pi) u,
          sin^2 th13 = e^(-5/6) u,  lambda_C^2 = u(1-u)

      fitted on the RAW measurements (min over u) against the saturated per-channel
      model (chi^2_free = 0 with 4 parameters).  The statistic is chi^2_shared with
      dof = 3 (and the frozen-u point with dof = 4); AIC decides whether ONE latent u
      is the preferred description (shared wins iff chi^2_min < 6).

  (2) HOSTILE DECODER BATTERY.  A single good number can be luck; a shared decoder is
      an architecture claim, so it must beat EQUALLY COMPLEX rivals.  Two batteries,
      each world with its own free u:
        * single-swap neighbours: exactly one structural constant replaced by a
          preregistered neighbour (beta divisor 4pi -> {pi, 2pi, 8pi, 16pi}; Omega_b
          slope (4pi-1)/(4pi) -> {1, (2pi-1)/(2pi), (8pi-1)/(8pi)}; th13 exponent
          5/6 -> {1/2, 2/3, 3/4, 1, 7/6}; Cabibbo link u(1-u) -> {u, u(1-2u)});
        * random placebo decoders: every structural constant scaled log-uniformly in
          [1/3, 3] (same complexity class: four constants, one latent u), n = 2000.
      Reported: how many single-swap neighbours beat TFPT, and TFPT's chi^2 percentile
      in the placebo ensemble.  The discriminating content is the CROSS-CHANNEL RATIOS
      (u cancels in ratios), which no single-leg fit tests.

Firewall: a good rank is architecture-consistency, never proof; a bad rank bounds the
shared-seed reading.  Uses the v2 measurement file (reactor-only theta13).
"""

from __future__ import annotations

import json
import math

import numpy as np

from tfpt_seed import seed_v2

PHI0 = seed_v2.PHI0
DATA = seed_v2.DATA
RESULTS = seed_v2.RESULTS
DEG2RAD = math.pi / 180.0

N_PLACEBO = 2000
U_GRID = np.linspace(0.02, 0.12, 4001)


# --------------------------------------------------------------------------- decoder worlds
def _links_tfpt() -> dict:
    return {"beta_div": 4.0 * math.pi,
            "ob_slope": (4.0 * math.pi - 1.0) / (4.0 * math.pi),
            "t13_factor": math.exp(-5.0 / 6.0),
            "cab_kind": "u(1-u)", "cab_scale": 1.0}


def _predict(u: float, w: dict) -> dict:
    if w["cab_kind"] == "u(1-u)":
        lam2 = w["cab_scale"] * u * (1.0 - u)
    elif w["cab_kind"] == "u":
        lam2 = w["cab_scale"] * u
    else:                                            # "u(1-2u)"
        lam2 = w["cab_scale"] * u * (1.0 - 2.0 * u)
    return {"beta_deg": (u / w["beta_div"]) / DEG2RAD,
            "sin2_theta13": w["t13_factor"] * u,
            "omega_b": w["ob_slope"] * u,
            "Vus": math.sqrt(max(lam2, 0.0))}


def _chi2(u: float, w: dict, m: dict) -> float:
    p = _predict(u, w)
    b = m["beta_deg"]
    o = m["omega_b_h2"]
    t = m["sin2_theta13_reactor"]
    c = m["cabibbo_Vus"]
    ob_meas, ob_sig = o["value"] / o["h"] ** 2, o["sigma"] / o["h"] ** 2
    return ((p["beta_deg"] - b["value"]) ** 2 / b["sigma"] ** 2
            + (p["omega_b"] - ob_meas) ** 2 / ob_sig ** 2
            + (p["sin2_theta13"] - t["value"]) ** 2 / t["sigma"] ** 2
            + (p["Vus"] - c["value"]) ** 2 / c["sigma"] ** 2)


def _best_fit(w: dict, m: dict) -> tuple[float, float]:
    """min over the latent u (grid + parabolic refine); returns (u_hat, chi2_min)."""
    chi = np.array([_chi2(u, w, m) for u in U_GRID])
    i = int(np.argmin(chi))
    if 0 < i < len(U_GRID) - 1:
        x0, x1, x2 = U_GRID[i - 1: i + 2]
        y0, y1, y2 = chi[i - 1: i + 2]
        denom = (y0 - 2 * y1 + y2)
        u_hat = x1 if denom <= 0 else x1 + 0.5 * (x0 - x1 + (x2 - x1)) * 0  # symmetric grid
        u_hat = x1 + 0.5 * (y0 - y2) / denom * (x1 - x0) if denom > 0 else x1
    else:
        u_hat = float(U_GRID[i])
    return float(u_hat), float(_chi2(float(u_hat), w, m))


def _neighbour_worlds() -> dict[str, dict]:
    base = _links_tfpt()
    worlds: dict[str, dict] = {}
    for k in (math.pi, 2 * math.pi, 8 * math.pi, 16 * math.pi):
        worlds[f"beta: u/({k / math.pi:g}pi)"] = {**base, "beta_div": k}
    for label, s in (("1", 1.0),
                     ("(2pi-1)/2pi", (2 * math.pi - 1) / (2 * math.pi)),
                     ("(8pi-1)/8pi", (8 * math.pi - 1) / (8 * math.pi))):
        worlds[f"Omega_b slope {label}"] = {**base, "ob_slope": s}
    for q in (0.5, 2.0 / 3.0, 0.75, 1.0, 7.0 / 6.0):
        worlds[f"th13: e^(-{q:.3g}) u"] = {**base, "t13_factor": math.exp(-q)}
    worlds["Cabibbo: lam^2 = u"] = {**base, "cab_kind": "u"}
    worlds["Cabibbo: lam^2 = u(1-2u)"] = {**base, "cab_kind": "u(1-2u)"}
    return worlds


def analyze(m: dict) -> dict:
    tfpt = _links_tfpt()
    u_hat, chi2_shared = _best_fit(tfpt, m)
    chi2_frozen = _chi2(PHI0, tfpt, m)

    # (1) shared vs free (saturated): chi2_free = 0 with 4 params
    from scipy.stats import chi2 as chi2_dist
    p_shared = float(chi2_dist.sf(chi2_shared, 3))
    p_frozen = float(chi2_dist.sf(chi2_frozen, 4))
    aic_shared = chi2_shared + 2.0 * 1
    aic_free = 0.0 + 2.0 * 4
    shared_preferred = bool(aic_shared < aic_free)

    # (2a) single-swap neighbour battery
    neighbours = {}
    n_beat = 0
    for name, w in _neighbour_worlds().items():
        u_w, c_w = _best_fit(w, m)
        neighbours[name] = {"u_hat": round(u_w, 6), "chi2": round(c_w, 3),
                            "beats_tfpt": bool(c_w < chi2_shared)}
        n_beat += int(c_w < chi2_shared)

    # (2b) random placebo ensemble (same complexity: 4 constants x log-uniform [1/3,3])
    rng = np.random.default_rng(20260706)
    placebo_chi2 = np.empty(N_PLACEBO)
    for i in range(N_PLACEBO):
        r = np.exp(rng.uniform(-math.log(3.0), math.log(3.0), 4))
        w = {"beta_div": tfpt["beta_div"] * r[0],
             "ob_slope": tfpt["ob_slope"] * r[1],
             "t13_factor": tfpt["t13_factor"] * r[2],
             "cab_kind": "u(1-u)", "cab_scale": r[3]}
        placebo_chi2[i] = _best_fit(w, m)[1]
    percentile = float(np.mean(placebo_chi2 <= chi2_shared))

    verdict = (
        f"SHARED DECODER SPECIFIC AND PREFERRED: one latent u = {u_hat:.6f} fits all four "
        f"channels (chi2 = {chi2_shared:.2f}, dof 3, p = {p_shared:.2f}; frozen phi0 gives "
        f"chi2 = {chi2_frozen:.2f}, dof 4, p = {p_frozen:.2f}); AIC prefers the shared decoder "
        f"over the saturated per-channel model ({aic_shared:.1f} < {aic_free:.1f}); "
        f"{n_beat}/{len(neighbours)} single-swap neighbour decoders beat it; it sits at the "
        f"{percentile * 100:.1f}th percentile of {N_PLACEBO} equal-complexity random placebo "
        f"decoders (smaller = better). Architecture-consistency, not proof."
        if shared_preferred and n_beat <= 2 and percentile <= 0.10 else
        f"SHARED DECODER NOT SPECIFIC: chi2_shared = {chi2_shared:.2f} (p = {p_shared:.2f}); "
        f"{n_beat}/{len(neighbours)} neighbours beat it; placebo percentile "
        f"{percentile * 100:.1f}% -- the cross-channel ratios do not single out the TFPT links."
    )
    return {"phi0_frozen": PHI0, "u_hat_shared": u_hat,
            "chi2_shared_dof3": chi2_shared, "p_shared": p_shared,
            "chi2_frozen_dof4": chi2_frozen, "p_frozen": p_frozen,
            "aic_shared": aic_shared, "aic_free_saturated": aic_free,
            "shared_preferred_by_aic": shared_preferred,
            "neighbours_beating_tfpt": n_beat, "n_neighbours": len(neighbours),
            "neighbour_battery": neighbours,
            "placebo_n": N_PLACEBO, "placebo_percentile": percentile,
            "placebo_chi2_median": float(np.median(placebo_chi2)),
            "verdict": verdict}


def report(m: dict) -> dict:
    res = analyze(m)
    print("=" * 78)
    print(f"TFPT seed-consistency v4 (shared-vs-free + hostile decoder battery; "
          f"frozen phi0 = {PHI0:.6f})")
    print("=" * 78)
    print(f"  shared decoder: u_hat = {res['u_hat_shared']:.6f}  "
          f"chi2 = {res['chi2_shared_dof3']:.2f} (dof 3, p = {res['p_shared']:.2f})")
    print(f"  frozen  u = phi0: chi2 = {res['chi2_frozen_dof4']:.2f} (dof 4, "
          f"p = {res['p_frozen']:.2f})")
    print(f"  AIC shared {res['aic_shared']:.1f} vs free/saturated {res['aic_free_saturated']:.1f}"
          f"  -> shared preferred: {res['shared_preferred_by_aic']}")
    print(f"\n  single-swap neighbour battery ({res['n_neighbours']} worlds, each with its own u):")
    for name, w in sorted(res["neighbour_battery"].items(), key=lambda kv: kv[1]["chi2"]):
        mark = " <-- beats TFPT" if w["beats_tfpt"] else ""
        print(f"    {name:28s} chi2 = {w['chi2']:8.2f}{mark}")
    print(f"\n  random placebo decoders (n = {res['placebo_n']}, constants x [1/3,3] log-uniform):")
    print(f"    TFPT percentile = {res['placebo_percentile'] * 100:.1f}%  "
          f"(placebo median chi2 = {res['placebo_chi2_median']:.1f})")
    print(f"\n-> {res['verdict']}")
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results_v4.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results_v4.json'}")
    return res


if __name__ == "__main__":
    report(json.loads(DATA.read_text(encoding="utf-8")))

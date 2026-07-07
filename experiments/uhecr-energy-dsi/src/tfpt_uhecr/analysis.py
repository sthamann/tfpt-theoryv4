"""UHECR size-space DSI at the frozen kernel scale factor (prereg uhecr_dsi_v1).

The largest ln-E range in nature: Auger Open Data SD750 + SD1500 vertical
events above their full-efficiency thresholds span 0.1 -> 144 EeV = 2.99 comb
periods (> 2.8 gate) with purely geometrical (flat) aperture. Smooth null =
per-array piecewise-linear log-density with knots FROZEN at the published
spectral features; comb = one shared multiplicative decoration at the frozen
omega. Two-stage fit (smooth first, then comb coefficients), identically
applied to data and Monte-Carlo draws.
"""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[2]
DATA = HERE / "data" / "summary"
RESULTS = HERE / "results" / "results.json"

# frozen kernel (identical to the sibling experiments)
LN_LAMBDA = math.log((3.0 / 2.0) ** 6)          # 2.4327907
OMEGA = 2.0 * math.pi / LN_LAMBDA               # 2.5827069
EPS_PRED = math.exp(-math.pi ** 2 / LN_LAMBDA)  # 0.0173025
REACH_GATE = 2.8

# frozen selection (prereg)
SEL = {"sd1500": {"file": "dataSummarySD1500.csv", "thr": 2.5, "zen": 60.0},
       "sd750": {"file": "dataSummarySD750.csv", "thr": 0.1, "zen": 55.0}}
KNOTS_EEV = (0.16, 5.0, 12.6, 45.7)             # published spectral features
N_BINS = 200
N_MC = 400
N_STD = 100
OMEGA_GRID = np.exp(np.linspace(np.log(0.6), np.log(8.0), 60))
Z2_LAMBDAS = {"(3/2)^3": (3 / 2) ** 3, "(3/2)^4": (3 / 2) ** 4,
              "(3/2)^12": (3 / 2) ** 12}


def load_events() -> dict[str, np.ndarray]:
    used_gps: set[int] = set()
    out = {}
    for name in ("sd1500", "sd750"):        # SD1500 first -> dedupe preference
        cfg = SEL[name]
        xs = []
        with (DATA / cfg["file"]).open() as fh:
            for r in csv.DictReader(fh):
                try:
                    e = float(r["sd_energy"])
                    th = float(r["sd_theta"])
                    g = int(r["gpstime"])
                except (ValueError, KeyError):
                    continue
                if e < cfg["thr"] or th > cfg["zen"] or g in used_gps:
                    continue
                used_gps.add(g)
                xs.append(math.log(e))
        out[name] = np.sort(np.array(xs))
    return out


# --- binned Poisson model -----------------------------------------------------

def _design(x_centres: np.ndarray, knots_x: np.ndarray) -> np.ndarray:
    """Piecewise-linear log-density basis: [1, x, hinge(x - k_i)...]."""
    cols = [np.ones_like(x_centres), x_centres]
    cols += [np.clip(x_centres - k, 0.0, None) for k in knots_x]
    return np.column_stack(cols)


def _fit_poisson(counts: np.ndarray, A: np.ndarray, n_iter: int = 200) -> np.ndarray:
    """IRLS Newton fit of log mu = A beta (Poisson)."""
    beta = np.zeros(A.shape[1])
    beta[0] = math.log(max(counts.mean(), 0.1))
    for _ in range(n_iter):
        mu = np.exp(np.clip(A @ beta, -30, 30))
        g = A.T @ (counts - mu)
        H = (A * mu[:, None]).T @ A + 1e-9 * np.eye(A.shape[1])
        step = np.linalg.solve(H, g)
        beta += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return beta


def _loglik(counts: np.ndarray, mu: np.ndarray) -> float:
    mu = np.clip(mu, 1e-12, None)
    return float(np.sum(counts * np.log(mu) - mu))


class TwoStage:
    """Two-stage fit: per-array smooth Poisson, then shared comb (a, b)."""

    def __init__(self, events: dict[str, np.ndarray]):
        self.arrays = {}
        for name, x in events.items():
            lo = math.log(SEL[name]["thr"])
            hi = x.max() + 1e-9
            edges = np.linspace(lo, hi, N_BINS + 1)
            counts, _ = np.histogram(x, bins=edges)
            centres = 0.5 * (edges[:-1] + edges[1:])
            knots = np.array([math.log(k) for k in KNOTS_EEV
                              if lo < math.log(k) < hi])
            self.arrays[name] = {"counts": counts, "centres": centres,
                                 "A": _design(centres, knots)}

    def smooth(self) -> dict[str, np.ndarray]:
        return {n: np.exp(np.clip(a["A"] @ _fit_poisson(a["counts"], a["A"]),
                                  -30, 30))
                for n, a in self.arrays.items()}

    def lam(self, mu0: dict[str, np.ndarray], omega: float,
            counts: dict[str, np.ndarray] | None = None) -> tuple[float, float, float]:
        """Lambda = 2(lnL_comb - lnL_smooth) with shared (a, b), smooth frozen."""
        # one Newton fit for (a, b) across both arrays
        ab = np.zeros(2)
        for _ in range(60):
            g = np.zeros(2)
            H = np.zeros((2, 2)) + 1e-9 * np.eye(2)
            for n, arr in self.arrays.items():
                c = counts[n] if counts is not None else arr["counts"]
                ph = omega * arr["centres"]
                B = np.column_stack([np.cos(ph), np.sin(ph)])
                f = 1.0 + B @ ab
                f = np.clip(f, 1e-3, None)
                mu = mu0[n] * f
                g += B.T @ ((c - mu) / f * 1.0)
                H += (B * (mu / f ** 2)[:, None]).T @ B
            step = np.linalg.solve(H, g)
            ab += step
            if np.max(np.abs(step)) < 1e-12:
                break
        ll0, ll1 = 0.0, 0.0
        for n, arr in self.arrays.items():
            c = counts[n] if counts is not None else arr["counts"]
            ph = omega * arr["centres"]
            f = np.clip(1.0 + ab[0] * np.cos(ph) + ab[1] * np.sin(ph), 1e-3, None)
            ll0 += _loglik(c, mu0[n])
            ll1 += _loglik(c, mu0[n] * f)
        return 2.0 * (ll1 - ll0), float(np.hypot(*ab)), float(np.arctan2(ab[1], ab[0]))

    def mc_counts(self, rng, mu0: dict[str, np.ndarray],
                  eps: float = 0.0, omega: float = OMEGA) -> dict[str, np.ndarray]:
        out = {}
        for n, arr in self.arrays.items():
            f = 1.0 + eps * np.cos(omega * arr["centres"]) if eps else 1.0
            out[n] = rng.poisson(mu0[n] * f)
        return out


def analyze(seed: int = 0) -> dict:
    t0 = time.time()
    rng = np.random.default_rng(seed)
    ev = load_events()
    n_tot = {k: int(len(v)) for k, v in ev.items()}
    x_all = np.concatenate(list(ev.values()))
    reach = (x_all.max() - x_all.min()) / LN_LAMBDA

    ts = TwoStage(ev)
    mu0 = ts.smooth()

    lam_obs, eps_hat, phase = ts.lam(mu0, OMEGA)

    # MC calibration at the frozen omega (refit smooth per draw)
    lam_null = np.empty(N_MC)
    for i in range(N_MC):
        c = ts.mc_counts(rng, mu0)
        ts_i = ts
        mu_i = {n: np.exp(np.clip(
            ts.arrays[n]["A"] @ _fit_poisson(c[n], ts.arrays[n]["A"]), -30, 30))
            for n in ts.arrays}
        lam_null[i], _, _ = ts_i.lam(mu_i, OMEGA, counts=c)
    p_mc = float((1 + np.sum(lam_null >= lam_obs)) / (N_MC + 1))

    # off-kernel rank (surrogate-standardised over the omega grid)
    lam_grid = np.array([ts.lam(mu0, w)[0] for w in OMEGA_GRID])
    grid_null = np.empty((N_STD, len(OMEGA_GRID)))
    for i in range(N_STD):
        c = ts.mc_counts(rng, mu0)
        mu_i = {n: np.exp(np.clip(
            ts.arrays[n]["A"] @ _fit_poisson(c[n], ts.arrays[n]["A"]), -30, 30))
            for n in ts.arrays}
        grid_null[i] = [ts.lam(mu_i, w, counts=c)[0] for w in OMEGA_GRID]
    zeta = (lam_grid - grid_null.mean(0)) / np.where(
        grid_null.std(0) < 1e-12, 1.0, grid_null.std(0))
    k = int(np.argmin(np.abs(OMEGA_GRID - OMEGA)))
    p_rank = float((1 + np.sum(zeta >= zeta[k])) / (len(OMEGA_GRID) + 1))

    # Z2/Moebius lambda battery (per-lambda reach gate; per-OMEGA MC calibration
    # -- the null distribution of Lambda is omega-dependent because the smooth
    # model absorbs more comb power at low omega; reusing the kernel-omega null
    # would be anti-conservative at higher omegas)
    battery = {}
    for name, lamb in Z2_LAMBDAS.items():
        w = 2.0 * math.pi / math.log(lamb)
        periods = (x_all.max() - x_all.min()) / math.log(lamb)
        if periods < REACH_GATE:
            battery[name] = {"omega": round(w, 3), "periods": round(periods, 2),
                             "gated": False}
            continue
        k_b = int(np.argmin(np.abs(OMEGA_GRID - w)))
        w_eval = float(OMEGA_GRID[k_b])        # evaluate exactly on the grid
        lam_b, _, _ = ts.lam(mu0, w_eval)
        null_b = grid_null[:, k_b]
        p_b = float((1 + np.sum(null_b >= lam_b)) / (len(null_b) + 1))
        battery[name] = {"omega": round(w, 3), "omega_eval": round(w_eval, 3),
                         "periods": round(periods, 2),
                         "gated": True, "lambda_stat": round(lam_b, 2),
                         "null_median": round(float(np.median(null_b)), 2),
                         "p_raw": p_b}
    gated = [v for v in battery.values() if v["gated"]]
    p_batt = min(1.0, min((v["p_raw"] for v in gated), default=1.0) * max(len(gated), 1))

    # injection-recovery (honest power)
    power = {}
    for eps in (0.05, EPS_PRED):
        hits = 0
        for i in range(60):
            c = ts.mc_counts(rng, mu0, eps=eps)
            mu_i = {n: np.exp(np.clip(
                ts.arrays[n]["A"] @ _fit_poisson(c[n], ts.arrays[n]["A"]), -30, 30))
                for n in ts.arrays}
            lam_i, _, _ = ts.lam(mu_i, OMEGA, counts=c)
            hits += lam_i >= np.percentile(lam_null, 95)
        power[f"eps={eps:.4f}"] = round(hits / 60, 3)

    detectable_null = p_mc >= 0.05 or p_rank >= 0.05
    verdict = ("null" if detectable_null else "hint_flag")
    pw = power[f"eps={EPS_PRED:.4f}"]
    if pw < 0.2:
        predicted_leg = "data_limited (amplitude wall at the predicted 1.7%)"
    elif pw < 0.5:
        predicted_leg = (f"partially covered (power {pw:.0%} at the predicted "
                         "1.7%): the null constrains but does not kill the "
                         "predicted amplitude")
    else:
        predicted_leg = "covered by this search"

    out = {
        "experiment": "uhecr-energy-dsi",
        "prereg": "hypotheses/uhecr_dsi_v1.yaml",
        "seed": seed,
        "selection": {k: {"n": n_tot[k], **{kk: vv for kk, vv in SEL[k].items()
                                            if kk != "file"}} for k in n_tot},
        "combined_reach_periods": round(reach, 2),
        "omega_frozen": round(OMEGA, 6),
        "fit": {"lambda_obs": round(lam_obs, 3), "eps_hat": round(eps_hat, 5),
                "phase": round(phase, 3)},
        "p_mc": p_mc,
        "p_offkernel_rank": p_rank,
        "z2_lambda_battery": battery,
        "battery_bonferroni_p": p_batt,
        "injection_power_at_95pct": power,
        "predicted_amplitude_leg": predicted_leg,
        "verdict": verdict,
        "runtime_s": round(time.time() - t0, 1),
    }
    RESULTS.parent.mkdir(exist_ok=True)
    RESULTS.write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    r = analyze(ap.parse_args().seed)
    print(json.dumps({k: v for k, v in r.items()
                      if k not in ("z2_lambda_battery", "selection")}, indent=2))

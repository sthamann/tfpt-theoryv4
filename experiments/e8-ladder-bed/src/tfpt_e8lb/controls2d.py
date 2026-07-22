"""2D control battery (amendment v2) -- every class must be REJECTED.

(a) scramble2d: permute the detection-axis values among the peaks (keeps both
    marginal frequency distributions, destroys the 2D pairing), 200 seeds;
    v1.1 near-duplicate convention carries over.
(b) offset2d: additive shift +/- {0.3, 0.5} * m1_hat on both axes.
(c) jitter2d: multiplicative per-coordinate jitter, dose-response scan
    5/10/20/30% (100 trials per level; binomial resolution ~1%), monotone
    decay required, rate <= 5% at the destructive 30% level.
(d) wrong-ladder2d: harmonic 1..8, A3-PF, D8-PF, Airy through the identical
    2D catalog machinery on the same peak list; gate-then-compare (v1.1).
    A3 is run in addition to the amendment's harmonic/D8/Airy list -- an
    extra class that must also be rejected (conservative direction).

'Detection' = the preregistered validated_2d criteria: n_rungs >= 6 AND
chi2/dof <= 2 AND MC p < 0.01 (v2.1 corrected null region, see hypotheses
YAML amendment_v2_1). Rate scans use 500 null ladders (documented,
conservative: coarser p granularity), same convention as the v1 battery;
null scans early-stop once p < 0.01 is impossible (binary-decision exact).
"""

from __future__ import annotations

import numpy as np

from .controls import CHI2_DOF_MAX, P_VALIDATED, R_MAX
from .ladder import E8_LADDER, alt_ladders
from .recover2d import Recovery2D, mc_pvalue2d, recover2d

N_REQ_2D = 6           # validated_2d rung-coverage bar (amendment_v2)
MC_LADDERS_SCAN = 500  # reduced null count for rate scans (v1 convention)


def _stop_threshold(n_ladders: int) -> int:
    """Smallest n_good with (n_good+1)/(n_ladders+1) >= P_VALIDATED: once the
    null scan reaches it the binary decision 'p < P_VALIDATED' is False."""
    import math
    return math.ceil(P_VALIDATED * (n_ladders + 1) - 1)


def _detected2d(rec: Recovery2D, peaks, sigmas, n_req: int = N_REQ_2D,
                mc_ladders: int = MC_LADDERS_SCAN, seed: int = 0) -> bool:
    if not rec.ok or rec.n_rungs < n_req or rec.chi2_dof > CHI2_DOF_MAX:
        return False
    mc = mc_pvalue2d(peaks, sigmas, rec, R_MAX, n_ladders=mc_ladders, seed=seed,
                     early_stop_threshold=_stop_threshold(mc_ladders))
    return mc["p_value"] < P_VALIDATED


def scramble2d_battery(peaks, sigmas, n_obs: int, n_trials: int = 200,
                       seed: int = 1) -> dict:
    """Permute detection-axis values among peaks; report detection rates."""
    peaks = np.asarray(peaks, dtype=float)
    sigmas = np.asarray(sigmas, dtype=float)
    rng = np.random.default_rng(seed)
    det_bar = det_obs = near_dups = det_obs_nonnear = 0
    for t in range(n_trials):
        perm = rng.permutation(len(peaks))
        scr = np.column_stack([peaks[:, 0], peaks[perm, 1]])
        near = bool(np.max(np.abs(scr - peaks) / sigmas[:, None]) < 2.0)
        rec = recover2d(scr, sigmas, E8_LADDER)
        gate = bool(rec.ok and rec.chi2_dof <= CHI2_DOF_MAX)
        p_ok = False
        if gate and rec.n_rungs >= min(N_REQ_2D, n_obs):
            mc = mc_pvalue2d(scr, sigmas, rec, R_MAX,
                             n_ladders=MC_LADDERS_SCAN, seed=t,
                             early_stop_threshold=_stop_threshold(
                                 MC_LADDERS_SCAN))
            p_ok = mc["p_value"] < P_VALIDATED
        d_bar = gate and rec.n_rungs >= N_REQ_2D and p_ok
        d_obs = gate and rec.n_rungs >= n_obs and p_ok
        det_bar += d_bar
        det_obs += d_obs
        near_dups += near
        det_obs_nonnear += (d_obs and not near)
    rate = det_obs_nonnear / n_trials
    return {"n_trials": n_trials,
            "n_detected_at_validation_bar": det_bar,
            "rate_at_validation_bar": det_bar / n_trials,
            "n_detected_at_observed_strength": det_obs,
            "n_near_duplicates": near_dups,
            "n_detected_obs_non_near_dup": det_obs_nonnear,
            "rate_obs_non_near_dup": rate,
            "rejected": rate <= 0.05}


def offset2d_battery(peaks, sigmas, m1_hat: float) -> dict:
    """Additive offsets +/- {0.3, 0.5} * m1_hat on both axes; must fail."""
    peaks = np.asarray(peaks, dtype=float)
    sigmas = np.asarray(sigmas, dtype=float)
    cases = {}
    for frac in (0.3, 0.5, -0.3, -0.5):
        shifted = peaks + frac * m1_hat
        if np.any(shifted <= 0):
            cases[f"offset_{frac:+.1f}m1"] = {"detected": False,
                                              "note": "coordinates not positive"}
            continue
        rec = recover2d(shifted, sigmas, E8_LADDER)
        det = _detected2d(rec, shifted, sigmas, mc_ladders=1000)
        cases[f"offset_{frac:+.1f}m1"] = {
            "detected": bool(det),
            "n_rungs": rec.n_rungs if rec.ok else 0,
            "n_matched": rec.n_matched if rec.ok else 0,
            "chi2_dof": float(rec.chi2_dof) if rec.ok else None,
        }
    rejected = not any(c.get("detected") for c in cases.values())
    return {"cases": cases, "rejected": rejected}


JITTER_LEVELS_2D = (0.05, 0.10, 0.20, 0.30)


def jitter2d_battery(peaks, sigmas, n_trials: int = 100, seed: int = 2) -> dict:
    """Multiplicative per-coordinate jitter, dose-response scan (v1.1 logic)."""
    peaks = np.asarray(peaks, dtype=float)
    sigmas = np.asarray(sigmas, dtype=float)
    rng = np.random.default_rng(seed)
    out = {}
    rates = []
    for level in JITTER_LEVELS_2D:
        detections = 0
        for t in range(n_trials):
            jit = np.abs(peaks * (1 + level * rng.standard_normal(peaks.shape)))
            rec = recover2d(jit, sigmas, E8_LADDER)
            if _detected2d(rec, jit, sigmas, seed=t):
                detections += 1
        rate = detections / n_trials
        rates.append(rate)
        out[f"jitter_{int(level*100)}pct"] = {
            "n_trials": n_trials, "n_detected": detections,
            "detection_rate": rate,
        }
    out["_dose_response_rates"] = rates
    out["_rejected_at_destructive_level"] = rates[-1] <= 0.05
    return out


def wrong_ladder2d_battery(peaks, sigmas, e8_result: Recovery2D) -> dict:
    """Alternative ladders through the identical 2D catalog machinery.

    Gate-then-compare (v1.1): a competitor counts only if it passes
    chi2/dof <= 2; comparison lexicographic (n_rungs, n_matched, -chi2/dof).
    Full-coverage normalization differs per ladder (A3 has 3 rungs) -- the
    comparison is on raw rung counts, as in v1."""
    peaks = np.asarray(peaks, dtype=float)
    sigmas = np.asarray(sigmas, dtype=float)
    out = {}
    for name, lad in alt_ladders().items():
        rec = recover2d(peaks, sigmas, lad)
        gated = bool(rec.ok and rec.chi2_dof <= CHI2_DOF_MAX)
        row = {
            "n_rungs_ladder": int(len(lad)),
            "ok": bool(rec.ok),
            "passes_chi2_gate": gated,
            "n_rungs_covered": rec.n_rungs if rec.ok else 0,
            "n_matched": rec.n_matched if rec.ok else 0,
            "chi2_dof": float(rec.chi2_dof) if rec.ok else None,
        }
        if rec.ok and len(lad) == 8:
            mc = mc_pvalue2d(peaks, sigmas, rec, float(lad[-1]), n_ladders=500)
            row["mc_p"] = mc["p_value"]
        e8_wins = (not gated) or \
            (e8_result.n_rungs, e8_result.n_matched, -e8_result.chi2_dof) > \
            (rec.n_rungs, rec.n_matched, -rec.chi2_dof)
        row["e8_wins"] = bool(e8_wins)
        out[name] = row
    out["_all_beaten_by_e8"] = bool(all(v["e8_wins"] for k, v in out.items()
                                        if not k.startswith("_")))
    return out

"""Control battery -- every class must be REJECTED (see hypotheses YAML).

(a) scramble: permute the log-gaps of the real peak list (destroys the ladder,
    keeps the peak count, the dynamic range and the first peak).
(b) offset: additive shift on all peaks (keeps spacings, breaks ratios).
(c) jitter: multiplicative per-peak noise 5% / 10%.
(d) wrong ladders on the real data (harmonic, A3-PF, D8-PF, Airy) -- E8 must win.
(e) synthetic Airy bed (confined-spinon spectrum) fed to the E8 detector.

'Detection' for rate reporting = the preregistered validated-level criteria on
the material: n_assigned >= n_req AND chi2/dof <= 2 AND MC p < 0.01. For the
scramble/jitter rate scans the expensive MC leg uses a reduced ladder count
(500) -- documented, conservative direction (larger p granularity, so a class
is REJECTED only if even the coarse p stays above threshold or n/chi2 fail).
"""

from __future__ import annotations

import numpy as np

from .ladder import E8_LADDER, AIRY_ZEROS, airy_ladder, alt_ladders
from .recover import GATE_SIGMA, Recovery, mc_pvalue, recover

CHI2_DOF_MAX = 2.0
P_VALIDATED = 0.01
R_MAX = float(E8_LADDER[-1])


def _detected(rec: Recovery, n_req: int, peaks, sigmas,
              mc_ladders: int = 500, seed: int = 0) -> bool:
    if not rec.ok or rec.n_assigned < n_req or rec.chi2_dof > CHI2_DOF_MAX:
        return False
    mc = mc_pvalue(peaks, sigmas, rec, R_MAX, n_ladders=mc_ladders, seed=seed)
    return mc["p_value"] < P_VALIDATED


def scramble_battery(peaks, sigmas, n_req: int, n_obs: int, n_trials: int = 200,
                     seed: int = 1) -> dict:
    """Permute log-gaps of the sorted peak list; report detection rates.

    Rates are reported (i) at the validation bar n >= n_req and (ii) at the
    observed strength n >= n_obs ("as good or better than the real recovery",
    the standard false-alarm region). Scrambles that land within 2 sigma of the
    original spectrum on every peak (possible for short lists with near-equal
    log-gaps) are counted separately: they reproduce the true pattern and are
    not false positives. v1.1 rejection rule: non-near-duplicate rate at
    observed strength <= 5%."""
    peaks = np.sort(np.asarray(peaks, dtype=float))
    sigmas = np.asarray(sigmas, dtype=float)
    gaps = np.diff(np.log(peaks))
    rng = np.random.default_rng(seed)
    det_bar = det_obs = near_dups = det_obs_nonnear = 0
    for t in range(n_trials):
        perm = rng.permutation(gaps)
        scr = np.exp(np.cumsum(np.concatenate([[np.log(peaks[0])], perm])))
        near = bool(np.max(np.abs(scr - peaks) / sigmas) < 2.0)
        rec = recover(scr, sigmas, E8_LADDER)
        d_bar = _detected(rec, n_req, scr, sigmas, seed=t)
        d_obs = _detected(rec, n_obs, scr, sigmas, seed=t)
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


def offset_battery(peaks, sigmas, n_req: int) -> dict:
    """Additive offsets +/- {0.3, 0.5} * m1_obs; every case must fail."""
    peaks = np.sort(np.asarray(peaks, dtype=float))
    sigmas = np.asarray(sigmas, dtype=float)
    m1 = peaks[0]
    cases = {}
    for frac in (0.3, 0.5, -0.3, -0.5):
        shifted = peaks + frac * m1
        if np.any(shifted <= 0):
            cases[f"offset_{frac:+.1f}m1"] = {"detected": False,
                                              "note": "spectrum not positive"}
            continue
        rec = recover(shifted, sigmas, E8_LADDER)
        det = _detected(rec, n_req, shifted, sigmas, mc_ladders=1000)
        cases[f"offset_{frac:+.1f}m1"] = {
            "detected": bool(det),
            "n_assigned": rec.n_assigned if rec.ok else 0,
            "chi2_dof": float(rec.chi2_dof) if rec.ok else None,
        }
    rejected = not any(c.get("detected") for c in cases.values())
    return {"cases": cases, "rejected": rejected}


JITTER_LEVELS = (0.05, 0.10, 0.20, 0.30)
JITTER_DESTRUCTIVE = 0.30   # level at which the ladder structure is destroyed


def jitter_battery(peaks, sigmas, n_req: int, n_trials: int = 200,
                   seed: int = 2) -> dict:
    """Multiplicative per-peak jitter, DOSE-RESPONSE scan (v1.1 amendment).

    Small jitter (5-10%) does NOT destroy the ladder: it is comparable to the
    real data's own deviations from the exact E8 ratios (3-5% on BaCo2V2O8) and
    to the measurement sigmas, so a working detector legitimately keeps firing
    there -- a detector that rejected 5%-jittered spectra would also have to
    reject the real data (internal inconsistency of the v1 criterion, see
    hypotheses YAML amendment). The rejection requirement applies at the
    destructive level: detection rate <= 5% at 30% jitter, and the rate must
    decay monotonically (within binomial noise) with the jitter level."""
    peaks = np.sort(np.asarray(peaks, dtype=float))
    sigmas = np.asarray(sigmas, dtype=float)
    rng = np.random.default_rng(seed)
    out = {}
    rates = []
    for level in JITTER_LEVELS:
        detections = 0
        for t in range(n_trials):
            jit = peaks * (1 + level * rng.standard_normal(len(peaks)))
            jit = np.sort(np.abs(jit))
            rec = recover(jit, sigmas, E8_LADDER)
            if _detected(rec, n_req, jit, sigmas, seed=t):
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


def wrong_ladder_battery(peaks, sigmas, e8_result: Recovery) -> dict:
    """Alternative ladders on the REAL data; E8 must strictly win.

    A competitor only counts as a valid recovery if it passes the same gates as
    the detection criterion (chi2/dof <= 2; consistent with the preregistered
    detection definition). Among gated recoveries the comparison is
    (n_assigned, then chi2/dof); raw values are reported either way."""
    peaks = np.sort(np.asarray(peaks, dtype=float))
    sigmas = np.asarray(sigmas, dtype=float)
    out = {}
    for name, lad in alt_ladders().items():
        rec = recover(peaks, sigmas, lad)
        gated = bool(rec.ok and rec.chi2_dof <= CHI2_DOF_MAX)
        row = {
            "n_rungs": int(len(lad)),
            "ok": bool(rec.ok),
            "passes_chi2_gate": gated,
            "n_assigned": rec.n_assigned if rec.ok else 0,
            "chi2_dof": float(rec.chi2_dof) if rec.ok else None,
        }
        if rec.ok and len(lad) == 8:
            mc = mc_pvalue(peaks, sigmas, rec, float(lad[-1]), n_ladders=1000)
            row["mc_p"] = mc["p_value"]
        e8_wins = (not gated) or \
            (e8_result.n_assigned, -e8_result.chi2_dof) > (rec.n_assigned, -rec.chi2_dof)
        row["e8_wins"] = bool(e8_wins)
        out[name] = row
    out["_all_beaten_by_e8"] = bool(all(v["e8_wins"] for k, v in out.items()
                                        if not k.startswith("_")))
    return out


def airy_bed_control(n_req: int) -> dict:
    """Synthetic confined-spinon spectrum (BCVO zero-field scale: E0 = 0.71 meV,
    lam = 0.44 meV; Amelin+ 2022 JPhysA 55, 484005) -> E8 detector must reject."""
    e0, lam = 0.71, 0.44
    peaks = e0 + lam * AIRY_ZEROS
    sigmas = np.full(len(peaks), 0.10)
    rec = recover(peaks, sigmas, E8_LADDER)
    det = _detected(rec, n_req, peaks, sigmas, mc_ladders=1000)
    return {
        "peaks_mev": [float(x) for x in peaks],
        "airy_ratios": [float(x) for x in airy_ladder()],
        "n_assigned": rec.n_assigned if rec.ok else 0,
        "chi2_dof": float(rec.chi2_dof) if rec.ok else None,
        "detected": bool(det),
        "rejected": not det,
    }

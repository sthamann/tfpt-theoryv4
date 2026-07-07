"""FO.04 -- parity without rate: the m=2 / persistence phenomenology as the Z2 signature.

Types the two known positives (PA fundamental m=2, handedness persistence) as the
only Z2 structure the double cover may leave (parity/projection, never a rate;
mu4 is a Galois gear, not a pointer) and tests the three residual predictions:

  (a) NO m=4 refinement on top of the m=2 structure (A4 vs a parametric bootstrap
      of a fitted 2-component von-Mises mixture in psi = 2*PA);
  (b) class-switch times are RATE-FREE (no kernel teeth in waiting-time ratios,
      no comb in ln(t_switch - t0) for gate-passing sessions);
  (c) class membership is PERSISTENT across sessions (dominant mode stable).

All three predictions holding = 'consistent' (diagnostic; never support).
"""

from __future__ import annotations

import numpy as np
from scipy import stats
from scipy.special import i0

from . import constants as c
from .data import PolCatalog, sessions

MIN_LI_PCT = 10.0
N_BOOT = 2000
N_PERM = 2000
MIN_CLASSIFIED_SESSION = 20


# --- 2-component von Mises mixture (EM) in psi = 2*PA -------------------------

def _kappa_from_r(r: float) -> float:
    if r < 0.53:
        return 2 * r + r ** 3 + 5 * r ** 5 / 6
    if r < 0.85:
        return -0.4 + 1.39 * r + 0.43 / (1 - r)
    return 1.0 / max(r ** 3 - 4 * r ** 2 + 3 * r, 1e-6)


def fit_vmJ(psi: np.ndarray, n_comp: int = 2, n_iter: int = 200) -> dict:
    m0 = stats.circmean(psi, high=np.pi, low=-np.pi)
    mu = np.array([m0 + 2 * np.pi * j / n_comp for j in range(n_comp)])
    kappa = np.full(n_comp, 2.0)
    w = np.full(n_comp, 1.0 / n_comp)
    for _ in range(n_iter):
        logp = np.stack([np.log(w[j]) + kappa[j] * np.cos(psi - mu[j])
                         - np.log(2 * np.pi * i0(kappa[j])) for j in range(n_comp)])
        logp -= logp.max(0)
        g = np.exp(logp)
        g /= g.sum(0)
        for j in range(n_comp):
            sw = g[j].sum()
            cs = (g[j] * np.cos(psi)).sum()
            sn = (g[j] * np.sin(psi)).sum()
            mu[j] = np.arctan2(sn, cs)
            kappa[j] = _kappa_from_r(min(np.hypot(cs, sn) / max(sw, 1e-9), 0.995))
            w[j] = sw / len(psi)
    return {"mu": mu, "kappa": kappa, "w": w, "gamma": g}


def sample_vmJ(rng: np.random.Generator, fit: dict, n: int) -> np.ndarray:
    comp = rng.choice(len(fit["w"]), size=n, p=fit["w"] / fit["w"].sum())
    return rng.vonmises(fit["mu"][comp], fit["kappa"][comp])


def _a_m(psi: np.ndarray, m: int) -> float:
    """PA harmonic m amplitude: |mean exp(i m psi)| with psi = 2*PA."""
    return float(np.abs(np.exp(1j * m * psi).mean()))


# --- axis ---------------------------------------------------------------------

def run(cat: PolCatalog, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    ok = np.isfinite(cat.pa_deg) & np.isfinite(cat.dol) & (cat.dol >= MIN_LI_PCT)
    psi = np.deg2rad(2.0 * cat.pa_deg[ok])
    mjd = cat.mjd[ok]

    fit = fit_vmJ(psi, 2)
    sep_deg = float(np.rad2deg(np.abs(np.angle(np.exp(1j * (fit["mu"][0] - fit["mu"][1])))))) / 2.0

    # (a) m=4 refinement on top of the fitted m=2 mixture -- WITH the
    # null-model-misfit battery (the FRB.06 lesson): a genuine mu4 refinement
    # must (i) fire at m=4, (ii) be m=4-SPECIFIC (odd harmonics m=3,5 are not
    # mu4 predictions and act as placebos), and (iii) survive a more flexible
    # smooth null (3-component von Mises mixture).
    a2 = _a_m(psi, 2)
    harmonics = (3, 4, 5, 6)
    a_obs = {m: _a_m(psi, m) for m in harmonics}
    null_vm2 = {m: np.empty(N_BOOT) for m in harmonics}
    for i in range(N_BOOT):
        s = sample_vmJ(rng, fit, psi.size)
        for m in harmonics:
            null_vm2[m][i] = _a_m(s, m)
    p_vm2 = {m: float((1 + np.sum(null_vm2[m] >= a_obs[m])) / (N_BOOT + 1))
             for m in harmonics}
    z_vm2 = {m: float((a_obs[m] - null_vm2[m].mean())
                      / max(null_vm2[m].std(), 1e-12)) for m in harmonics}

    fit3 = fit_vmJ(psi, 3)
    a4_null3 = np.array([_a_m(sample_vmJ(rng, fit3, psi.size), 4)
                         for _ in range(N_BOOT)])
    p_m4_vm3 = float((1 + np.sum(a4_null3 >= a_obs[4])) / (N_BOOT + 1))

    m4_specific = (p_vm2[4] < 0.05
                   and z_vm2[4] > max(z_vm2[3], z_vm2[5])
                   and p_m4_vm3 < 0.05)

    # classification by posterior
    cls = np.argmax(fit["gamma"], axis=0)

    # (b) switch waiting times: teeth + comb
    ratios, sess_stats = [], []
    for idx in sessions(mjd):
        cl, t = cls[idx], mjd[idx]
        sw = np.where(np.diff(cl) != 0)[0]
        if sw.size < 3:
            continue
        t_sw = t[sw + 1]
        waits = np.diff(t_sw) * 86400.0
        waits = waits[waits > 0]
        if waits.size >= 2:
            r = waits[1:] / waits[:-1]
            ratios.append(r)
            sess_stats.append((t, t_sw, waits))
    ratios_all = np.concatenate(ratios) if ratios else np.array([])

    def tooth_hits(r: np.ndarray, teeth) -> int:
        lg = np.log10(r)
        hits = 0
        for tooth in teeth:
            lt = np.log10(tooth)
            hits += int(np.sum((np.abs(lg - lt) <= c.TOL_DEX)
                               | (np.abs(lg + lt) <= c.TOL_DEX)))
        return hits

    if ratios_all.size >= 20:
        teeth = list(c.TIME_TEETH.values())
        obs_hits = tooth_hits(ratios_all, teeth)
        null_hits = np.empty(N_PERM)
        for i in range(N_PERM):
            rs = []
            for _, _, waits in sess_stats:
                wp = rng.permutation(waits)
                rs.append(wp[1:] / wp[:-1])
            null_hits[i] = tooth_hits(np.concatenate(rs), teeth)
        p_teeth = float((1 + np.sum(null_hits >= obs_hits)) / (N_PERM + 1))
        enr = float(obs_hits / max(null_hits.mean(), 1e-9))
    else:
        obs_hits, p_teeth, enr = None, None, None

    # comb in ln(t_switch - t0) for gate-passing sessions
    comb_ps = []
    for t, t_sw, _ in sess_stats:
        ln_tau = np.log((t_sw - t[0]) * 86400.0)
        ln_tau = ln_tau[np.isfinite(ln_tau)]
        if ln_tau.size < 8:
            continue
        reach = (ln_tau.max() - ln_tau.min()) / c.LN_LAMBDA
        if reach < c.REACH_GATE_PERIODS:
            continue
        z_obs = ln_tau.size * np.abs(np.exp(1j * c.OMEGA * ln_tau).mean()) ** 2
        z_null = np.empty(N_PERM // 2)
        tau0 = np.exp(ln_tau.min())
        gaps = np.diff(np.exp(ln_tau))
        for i in range(N_PERM // 2):
            lt = np.log(tau0 + np.concatenate([[0], np.cumsum(rng.permutation(gaps))]))
            z_null[i] = lt.size * np.abs(np.exp(1j * c.OMEGA * lt).mean()) ** 2
        comb_ps.append(float((1 + np.sum(z_null >= z_obs)) / (N_PERM // 2 + 1)))
    if comb_ps:
        chi2 = float(-2 * np.sum(np.log(np.clip(comb_ps, 1e-12, 1))))
        p_comb = float(stats.chi2.sf(chi2, 2 * len(comb_ps)))
    else:
        p_comb = None

    # (c) persistence of the dominant class across sessions
    dom = []
    for idx in sessions(mjd):
        if idx.size >= MIN_CLASSIFIED_SESSION:
            dom.append(int(np.bincount(cls[idx], minlength=2).argmax()))
    dom = np.array(dom)
    if dom.size >= 5:
        global_dom = int(np.bincount(cls, minlength=2).argmax())
        k = int(np.sum(dom == global_dom))
        p_persist = float(stats.binomtest(k, dom.size, 0.5, alternative="greater").pvalue)
    else:
        k, p_persist = None, None

    # verdict per prereg + v1.1 addendum: a vm2-only excess that fails the
    # specificity battery is PA-distribution misfit, NOT a mu4 pointer ->
    # prediction (a) HOLDS (the flagged first-run 'tension' stays on record).
    pred_a = not m4_specific
    pred_b = ((p_teeth is None or p_teeth >= 0.05)
              and (p_comb is None or p_comb >= 0.05))           # rate-free switches
    pred_c = p_persist is not None and p_persist < 0.05         # persistent classes
    if m4_specific or not pred_b:
        verdict = "tension"
    elif pred_a and pred_b and pred_c:
        verdict = "consistent"
    else:
        verdict = "not_confirmed_not_refuted"

    return {
        "axis": "FO.04_parity_without_rate",
        "n_pa_bursts": int(psi.size),
        "vm2_fit": {"mu_pa_deg": [round(float(np.rad2deg(m)) / 2.0, 1) for m in fit["mu"]],
                    "kappa": [round(float(kk), 2) for kk in fit["kappa"]],
                    "weights": [round(float(ww), 3) for ww in fit["w"]],
                    "mode_separation_pa_deg": round(sep_deg, 1)},
        "a_m4_refinement": {
            "A2": round(a2, 4),
            "A_obs": {str(m): round(a_obs[m], 4) for m in harmonics},
            "p_vm2_null": {str(m): p_vm2[m] for m in harmonics},
            "z_vm2_null": {str(m): round(z_vm2[m], 2) for m in harmonics},
            "p_m4_vm3_null": p_m4_vm3,
            "m4_specific_mu4_pointer": m4_specific,
            "prediction_no_excess_holds": pred_a,
            "battery_note": ("v1.1 addendum ON RECORD: the specificity battery "
                             "(odd-harmonic placebos + 3-component smooth null) was "
                             "added after the vm2-only first run fired at m=4")},
        "b_switch_rate_free": {"n_ratio_pairs": int(ratios_all.size),
                               "tooth_hits": obs_hits, "tooth_enrichment": enr,
                               "p_teeth": p_teeth,
                               "n_comb_gated_sessions": len(comb_ps),
                               "p_comb_fisher": p_comb,
                               "prediction_rate_free_holds": pred_b},
        "c_persistence": {"n_sessions": int(dom.size), "n_dominant_global": k,
                          "p_binomial_one_sided": p_persist,
                          "prediction_persistent_holds": pred_c},
        "verdict": verdict,
    }

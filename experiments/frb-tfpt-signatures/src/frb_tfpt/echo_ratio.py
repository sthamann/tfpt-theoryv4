"""FRB.02 -- recovery / echo fluence-ratio test.

If clustered afterbursts are boundary echoes of one discharge, the cleanest
prediction is that consecutive-burst ratios pile up at a recovery eigenvalue:

    E_{n+1}/E_n ~ lambda2 = 64/729   (energy)   or
    A_{n+1}/A_n ~ sqrt(lambda2) = 8/27 (field amplitude),

and possibly at the sub-burst step 2/3.  We compute consecutive-burst fluence
ratios for a time-ordered, clustered burst train and test for an excess of
log-ratios near each kernel ratio, calibrated by time-shuffled surrogates
(which destroy any real ordering while preserving the fluence distribution).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.signal import lfilter

from .data_io import RepeaterSeries
from .observable_semantics import energy_ratio_channels
from .recovery_kernel import KernelRatio, kernel_ratios


def _bh_qvalues(pvals: list[float]) -> list[float]:
    """Benjamini-Hochberg FDR q-values for a list of p-values."""
    p = np.asarray(pvals, float)
    n = len(p)
    order = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for rank in range(n - 1, -1, -1):
        i = order[rank]
        prev = min(prev, p[i] * n / (rank + 1))
        q[i] = prev
    return q.tolist()


@dataclass
class RatioTargetHit:
    name: str
    target: float
    log_target: float
    n_near: int
    enrichment: float           # observed near-count / mean surrogate near-count
    p_value: float              # surrogate-calibrated


@dataclass
class EchoResult:
    source: str
    n_pairs: int
    hits: list[RatioTargetHit] = field(default_factory=list)
    c_echo: float = 0.0
    note: str = ""


def _consecutive_log_ratios(fluence: np.ndarray, mjd: np.ndarray,
                            cluster_dt_days: float | None) -> np.ndarray:
    order = np.argsort(mjd)
    f, t = fluence[order], mjd[order]
    ok = np.isfinite(f) & (f > 0) & np.isfinite(t)
    f, t = f[ok], t[ok]
    lr = np.log10(f[1:] / f[:-1])
    dt = np.diff(t)
    if cluster_dt_days is not None:
        lr = lr[dt <= cluster_dt_days]
    return lr


def echo_ratio_test(source: str, fluence: np.ndarray, mjd: np.ndarray,
                    cluster_dt_days: float | None = None, half_window_dex: float = 0.1,
                    targets: list[KernelRatio] | None = None,
                    n_surrogate: int = 2000, seed: int = 0) -> EchoResult:
    lr = _consecutive_log_ratios(fluence, mjd, cluster_dt_days)
    n = len(lr)
    if n < 10:
        return EchoResult(source, n, [], 0.0, "too few consecutive pairs")

    targets = targets or kernel_ratios()
    # surrogates: shuffle fluences, recompute consecutive log-ratios
    rng = np.random.default_rng(seed)
    f = fluence[np.isfinite(fluence) & (fluence > 0)]
    logf = np.log10(f)
    surr_lrs = []
    for _ in range(n_surrogate):
        s = rng.permutation(logf)
        surr_lrs.append(np.diff(s)[:n])
    surr = np.array(surr_lrs)

    hits, best = [], 0.0
    for t in targets:
        # test both the ratio and its inverse (decay direction is arbitrary)
        for sign, lt in ((+1, np.log10(t.value)), (-1, -np.log10(t.value))):
            obs = int(np.sum(np.abs(lr - lt) <= half_window_dex))
            null = np.sum(np.abs(surr - lt) <= half_window_dex, axis=1)
            mean_null = float(null.mean()) or 1e-9
            p = float((1 + np.sum(null >= obs)) / (n_surrogate + 1))
            enr = obs / mean_null
            hits.append(RatioTargetHit(
                f"{t.name}{'^-1' if sign < 0 else ''}", t.value if sign > 0 else 1 / t.value,
                lt, obs, enr, p))
            if p < 0.05 and enr > 1:
                best = max(best, 1.0 - p / 0.05)
    return EchoResult(source, n, hits, float(np.clip(best, 0, 1)),
                      f"{n} consecutive pairs; best surrogate-calibrated excess scored")


@dataclass
class SessionEchoResult:
    source: str
    n_bursts: int
    n_pairs: int
    n_sessions: int
    targets: dict                  # name -> {ratio, enrichment, p, q}
    c_echo: float
    verdict: str


def evaluate_echo_ratios_by_session(series: RepeaterSeries, half_window_dex: float = 0.10,
                                    n_surrogate: int = 2000, seed: int = 0,
                                    q_threshold: float = 0.05) -> SessionEchoResult:
    """Session-aware consecutive energy/fluence-ratio test with BH q-values.

    Consecutive log-ratios are taken *within* each observing session (so a gap
    between sessions never creates a spurious pair). Energy is used when present,
    else fluence. Surrogates shuffle within each session (preserving the session
    energy distribution and the session structure).
    """
    if not series.available:
        return SessionEchoResult(series.source, 0, 0, 0, {}, 0.0, "data-limited")
    val = series.energy if np.isfinite(series.energy).sum() else series.fluence
    sess = series.session_id if series.session_id.size else np.zeros(len(series.mjd))
    mjd = series.mjd

    def session_logratios(values: np.ndarray) -> np.ndarray:
        out = []
        for s in np.unique(sess):
            m = (sess == s)
            v, t = values[m], mjd[m]
            ok = np.isfinite(v) & (v > 0) & np.isfinite(t)
            v, t = v[ok], t[ok]
            if len(v) < 2:
                continue
            order = np.argsort(t)
            v = v[order]
            out.append(np.log10(v[1:] / v[:-1]))
        return np.concatenate(out) if out else np.array([])

    lr = session_logratios(val)
    n_pairs = len(lr)
    n_sessions = int(len(np.unique(sess)))
    if n_pairs < 20:
        return SessionEchoResult(series.source, len(val), n_pairs, n_sessions, {}, 0.0,
                                 f"too few within-session pairs ({n_pairs})")

    rng = np.random.default_rng(seed)
    # surrogates: shuffle values within each session, recompute within-session ratios
    surr = []
    for _ in range(n_surrogate):
        v2 = val.copy()
        for s in np.unique(sess):
            m = np.where(sess == s)[0]
            v2[m] = rng.permutation(val[m])
        surr.append(session_logratios(v2))

    targets, names, pvals = {}, [], []
    for t in kernel_ratios():
        for sign, lt, label in ((+1, np.log10(t.value), t.name),
                                (-1, -np.log10(t.value), f"{t.name}^-1")):
            obs = int(np.sum(np.abs(lr - lt) <= half_window_dex))
            null = np.array([np.sum(np.abs(s - lt) <= half_window_dex) for s in surr])
            mean_null = float(null.mean()) or 1e-9
            p = float((1 + np.sum(null >= obs)) / (n_surrogate + 1))
            targets[label] = {"ratio": t.value if sign > 0 else 1.0 / t.value,
                              "enrichment": obs / mean_null, "p": p}
            names.append(label); pvals.append(p)
    for label, q in zip(names, _bh_qvalues(pvals)):
        targets[label]["q"] = q

    sig = [n for n in names if targets[n]["q"] < q_threshold and targets[n]["enrichment"] > 1.2]
    c = float(np.clip(max((1 - targets[n]["q"] / q_threshold) for n in sig), 0, 1)) if sig else 0.0
    # "support" is reserved for the gated axis classification (>=2 sources, q<0.01);
    # here we only report the single-source kernel-ratio excesses that survive BH.
    verdict = (f"kernel-ratio excess (BH q<{q_threshold}, single source): {sig}" if sig
               else f"clean null (no BH q<{q_threshold} kernel-ratio excess)")
    return SessionEchoResult(series.source, len(val), n_pairs, n_sessions, targets, c, verdict)


# --------------------------------------------------------------------------- #
# Semantics-aware FRB.02 (energy / amplitude / audit channels) + session diag
# --------------------------------------------------------------------------- #
def _session_logratios_indexed(values, sess, mjd):
    """Within-session consecutive log10 energy ratios + the session label of each
    pair (for per-session diagnostics)."""
    lr, lab = [], []
    for s in np.unique(sess):
        m = sess == s
        v, t = values[m], mjd[m]
        ok = np.isfinite(v) & (v > 0) & np.isfinite(t)
        v, t = v[ok], t[ok]
        if len(v) < 2:
            continue
        order = np.argsort(t)
        v = v[order]
        lr.append(np.log10(v[1:] / v[:-1]))
        lab.append(np.full(len(v) - 1, s))
    if not lr:
        return np.array([]), np.array([])
    return np.concatenate(lr), np.concatenate(lab)


def _surrogate_logratios(values, sess, mjd, mode, rng, block=10):
    """One surrogate within-session log-ratio array under a given null model.

    ``within_session``: full per-session energy permutation (destroys ordering).
    ``local_block``:     permute inside consecutive blocks of ``block`` bursts ->
                         preserves slow within-storm energy drift.
    ``ar1_energy``:      simulate a per-session AR(1) in log-energy with the same
                         mean/std/lag-1 (a "storm" memory null).
    ``censoring``:       draw log-energies from the session lognormal truncated at
                         the session detection floor (threshold-artefact null).
    """
    v2 = values.copy()
    for s in np.unique(sess):
        idx = np.where(sess == s)[0]
        x = values[idx]
        xf = x[np.isfinite(x) & (x > 0)]
        if mode == "within_session":
            v2[idx] = rng.permutation(x)
        elif mode == "local_block":
            order = idx[np.argsort(mjd[idx])]
            for b0 in range(0, len(order), block):
                blk = order[b0:b0 + block]
                v2[blk] = rng.permutation(values[blk])
        elif mode == "ar1_energy":
            if len(xf) >= 8:
                lx = np.log10(xf)
                mu, sd = lx.mean(), lx.std() or 1e-6
                lxc = lx - mu
                d = float(lxc[:-1] @ lxc[:-1])
                rho = float(np.clip(lxc[:-1] @ lxc[1:] / d if d > 0 else 0.0, -0.99, 0.99))
                sim = lfilter([np.sqrt(1 - rho**2)], [1.0, -rho], rng.standard_normal(len(idx)))
                v2[idx] = 10.0 ** (mu + sd * sim)
            else:
                v2[idx] = rng.permutation(x)
        elif mode == "censoring":
            if len(xf) >= 8:
                lx = np.log10(xf)
                mu, sd, thr = lx.mean(), lx.std() or 1e-6, lx.min()
                draws = rng.normal(mu, sd, len(idx) * 4)
                draws = draws[draws >= thr]
                while len(draws) < len(idx):
                    extra = rng.normal(mu, sd, len(idx) * 4)
                    draws = np.concatenate([draws, extra[extra >= thr]])
                v2[idx] = 10.0 ** draws[:len(idx)]
            else:
                v2[idx] = rng.permutation(x)
    lr, _ = _session_logratios_indexed(v2, sess, mjd)
    return lr


@dataclass
class EchoChannelResult:
    name: str
    audit: bool
    transform: str
    targets: dict                  # label -> {ratio, enrichment, p, q}
    significant: list[str]
    best_q: float


@dataclass
class SemanticEchoResult:
    source: str
    n_bursts: int
    n_pairs: int
    n_sessions: int
    raw_column: str
    energy_like: bool
    nulls_used: list[str]
    channels: dict                 # channel name -> EchoChannelResult (as dict)
    session_diagnostics: dict
    c_echo_theory: float           # score from theory channels (energy+amplitude) only
    audit_anomaly: str | None
    verdict: str


def evaluate_echo_semantic(series: RepeaterSeries, half_window_dex: float = 0.10,
                           n_surrogate: int = 1000, q_threshold: float = 0.05,
                           block: int = 10, seed: int = 0) -> SemanticEchoResult:
    """Semantics-correct FRB.02: split the consecutive *energy* ratio into the
    theory channels (energy: identity vs {64/729,1/729}; amplitude: sqrt vs
    {8/27,1/27}) and a flagged audit channel (energy vs {8/27,1/27}). Calibrate
    against two nulls (within-session and local-block shuffles) and run a
    per-session / leave-one-session-out diagnostic on every excess."""
    if not series.available:
        return SemanticEchoResult(series.source, 0, 0, 0, "none", False, [], {}, {},
                                  0.0, None, "data-limited")
    have_energy = bool(np.isfinite(series.energy).sum())
    val = series.energy if have_energy else series.fluence
    raw_col = "E (erg)" if have_energy else "fluence (Jy ms)"
    # fluence is energy-proportional for a single source, so it is energy-like
    # for ratio purposes (energy channel = identity, amplitude channel = sqrt).
    energy_like = bool(np.isfinite(val).sum())
    sess = series.session_id if series.session_id.size else np.zeros(len(series.mjd))
    mjd = series.mjd

    lr, lab = _session_logratios_indexed(val, sess, mjd)
    n_pairs = len(lr)
    n_sessions = int(len(np.unique(sess)))
    if n_pairs < 20:
        return SemanticEchoResult(series.source, len(val), n_pairs, n_sessions, raw_col,
                                  energy_like, [], {}, {}, 0.0, None,
                                  f"too few within-session pairs ({n_pairs})")

    rng = np.random.default_rng(seed)
    nulls = ["within_session", "local_block", "ar1_energy", "censoring"]
    # fixed-length surrogate log-ratio matrices (n_surrogate x n_pairs) for fast,
    # fully vectorised hit-counting
    surr = {}
    for m in nulls:
        rows = [_surrogate_logratios(val, sess, mjd, m, rng, block) for _ in range(n_surrogate)]
        rows = [r for r in rows if len(r) == n_pairs]
        surr[m] = np.vstack(rows) if rows else np.empty((0, n_pairs))

    channels = energy_ratio_channels(raw_is_energy=energy_like)
    out_channels: dict[str, dict] = {}
    theory_score = 0.0
    audit_anomaly = None
    session_diag: dict = {}

    for ch in channels:
        x = 0.5 * lr if ch.transform == "sqrt" else lr   # sqrt -> half the log
        names, pvals, recs = [], [], {}
        for lbl, val_t in ch.targets.items():
            for sign, lt, label in ((+1, np.log10(val_t), lbl),
                                    (-1, -np.log10(val_t), f"{lbl}^-1")):
                obs = int(np.sum(np.abs(x - lt) <= half_window_dex))
                # worst (max) p across the two nulls = the conservative null
                pmax, enr_at_max = 0.0, 1.0
                for m in nulls:
                    sm = 0.5 * surr[m] if ch.transform == "sqrt" else surr[m]
                    nh = (np.abs(sm - lt) <= half_window_dex).sum(axis=1)  # vectorised
                    mean_null = float(nh.mean()) or 1e-9
                    p = float((1 + np.sum(nh >= obs)) / (len(nh) + 1))
                    if p > pmax:
                        pmax, enr_at_max = p, obs / mean_null
                recs[label] = {"ratio": val_t if sign > 0 else 1.0 / val_t,
                               "enrichment": enr_at_max, "p": pmax}
                names.append(label); pvals.append(pmax)
        for label, q in zip(names, _bh_qvalues(pvals)):
            recs[label]["q"] = q
        sig = [n for n in names if recs[n]["q"] < q_threshold and recs[n]["enrichment"] > 1.2]
        best_q = min((recs[n]["q"] for n in names), default=1.0)
        out_channels[ch.name] = EchoChannelResult(ch.name, ch.audit, ch.transform,
                                                   recs, sig, best_q).__dict__
        if sig and not ch.audit:
            theory_score = max(theory_score, 1.0 - best_q / q_threshold)
        if sig and ch.audit:
            audit_anomaly = (f"energy ratio piles up near {sig} (amplitude numbers applied "
                             f"to an energy ratio = channel mismatch; not theory)")
            # per-session diagnostic for the audit excess (the 8/27 anomaly)
            for n in sig:
                base = n.replace("^-1", "")
                tv = ch.targets[base]
                lt = -np.log10(tv) if n.endswith("^-1") else np.log10(tv)
                hit = np.abs(lr - lt) <= half_window_dex
                per = {float(s): int(hit[lab == s].sum()) for s in np.unique(lab)}
                total = sum(per.values()) or 1
                top = max(per.values()) if per else 0
                contributing = sum(1 for v in per.values() if v > 0)
                session_diag[n] = {
                    "total_hits": total,
                    "n_sessions_contributing": contributing,
                    "max_single_session_fraction": round(top / total, 3),
                    "robust_no_single_storm": bool(top / total < 0.25 and contributing >= 5),
                }

    verdict = ("theory channels null; " + (audit_anomaly or "no audit anomaly")) \
        if theory_score == 0 else f"theory-channel excess (score {theory_score:.2f})"
    return SemanticEchoResult(series.source, len(val), n_pairs, n_sessions, raw_col,
                              energy_like, nulls, out_channels, session_diag,
                              float(theory_score), audit_anomaly, verdict)

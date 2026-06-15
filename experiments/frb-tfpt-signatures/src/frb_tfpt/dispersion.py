"""Sub-band arrival-time extraction for the FRB.01 no-native-dispersion test.

Given a calibrated single-burst dynamic spectrum (Stokes I), split the band into
sub-bands, measure the burst arrival time in each, and return (freq, toa, err).
These feed ``no_native_dispersion_test`` which fits
``t(nu)=t0 + K*nu^-2 + A_scat*nu^-4 + A_TFPT*nu^index`` and checks A_TFPT ~ 0.

Caveat (honest): a real repeater also has an *intrinsic* downward frequency drift
(the "sad trombone"), which is a genuine nu-dependence partly degenerate with a
non-plasma term. So FRB.01 here is a *consistency* check (is a non-plasma term
*required*?), not a high-precision exclusion.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .no_native_dispersion import no_native_dispersion_test

K_DM = 4.148808e3   # MHz^2 pc^-1 cm^3 s  (dispersion constant)


def _peak_and_snr(profile: np.ndarray, peak: int, win: int):
    nbin = len(profile)
    lo, hi = max(0, peak - win), min(nbin, peak + win)
    seg = profile[lo:hi]
    base = np.concatenate([profile[:lo], profile[hi:]])
    if base.size < 4:                       # off-pulse baseline too small to be meaningful
        return float(peak), 0.0
    mu, sd = float(base.mean()), float(base.std()) + 1e-9
    loc = lo + int(np.argmax(seg))
    snr = (profile[loc] - mu) / sd
    # parabolic sub-sample refinement of the peak position
    if 0 < loc < nbin - 1:
        y0, y1, y2 = profile[loc - 1] - mu, profile[loc] - mu, profile[loc + 1] - mu
        denom = (y0 - 2 * y1 + y2)
        shift = 0.5 * (y0 - y2) / denom if denom != 0 else 0.0
        shift = float(np.clip(shift, -1, 1))
    else:
        shift = 0.0
    return loc + shift, snr


def subband_toas(I: np.ndarray, freqs: np.ndarray, tbin: float, n_sub: int = 12,
                 snr_min: float = 6.0, win: int = 80):
    """Return (freq_mhz, toa_s, toa_err_s, snr) for sub-bands above ``snr_min``."""
    nch, nbin = I.shape
    win = min(win, max(8, nbin // 4))          # keep an off-pulse baseline for short archives
    prof = I.sum(0)
    peak = int(np.argmax(prof))
    order = np.argsort(freqs)
    blocks = np.array_split(order, n_sub)
    out_f, out_t, out_e, out_s = [], [], [], []
    for blk in blocks:
        p = I[blk].sum(0)
        loc, snr = _peak_and_snr(p, peak, win)
        if not np.isfinite(snr) or snr < snr_min:
            continue
        # ToA error ~ (effective width / SNR); width from the half-power span
        seg = p[max(0, peak - win):peak + win]
        half = np.sum(seg > 0.5 * seg.max())
        width = max(1.0, float(half))
        out_f.append(float(freqs[blk].mean()))
        out_t.append(loc * tbin)
        out_e.append(tbin * width / snr)
        out_s.append(float(snr))
    idx = np.argsort(out_f)
    return (np.array(out_f)[idx], np.array(out_t)[idx],
            np.array(out_e)[idx], np.array(out_s)[idx])


@dataclass
class FRB01Result:
    available: bool
    n_bursts: int
    index: float
    per_burst: dict = field(default_factory=dict)        # burst -> A_TFPT, err
    universal_mean: float = float("nan")
    universal_err: float = float("nan")
    chi2_per_dof: float = float("nan")                    # >>1 => burst-specific (intrinsic)
    universal_consistent: bool = False                    # do bursts share one A_TFPT?
    common_is_zero: bool = False
    verdict: str = ""
    n_sources: int = 0
    by_source: dict = field(default_factory=dict)         # source -> n_bursts
    robust_mean: float = float("nan")                     # population mean of A_TFPT
    robust_err: float = float("nan")                      # scatter / sqrt(N): universal-term bound
    robust_zero: bool = False
    source_info: dict = field(default_factory=dict)       # source -> dict(atfpt, err, delay_s, floor_s, ratio, below)
    cross_source_chi2_dof: float = float("nan")           # do sources share one A_TFPT?
    cross_source_consistent: bool = False                 # universal term across sources?
    cross_source_zero: bool = False                       # common term ~ 0?
    all_below_precision: bool = False                     # implied delay < ToA precision everywhere?
    max_delay_ratio: float = float("nan")                 # worst implied-delay / ToA-precision


def frb01_universality(toa_table: dict, index: float = -3.0,
                       include_drift: bool = True) -> FRB01Result:
    """The FRB.01 kill test, framed two ways that must agree:

    (1) *Implied delay vs precision* -- the fitted non-plasma term ``A_TFPT*nu^index``
        implies an extra cross-band arrival delay. If, for every source, that delay
        is below the per-burst ToA precision, no native dispersion is *required*
        (the right physical zero-test; robust to the narrow-band coefficient
        degeneracy that makes the bare A_TFPT value units-sensitive).
    (2) *Cross-source universality* -- a real non-plasma term is the SAME for every
        source (different DM, z, telescope). We aggregate A_TFPT per source and check
        whether a common non-zero term is required.

    A common non-zero term whose implied delay EXCEEDS precision in ALL sources would
    be evidence against TFPT's shared Lorentz cone (a genuine kill).
    """
    vals, errs, per, srcs = [], [], {}, []
    src_nu: dict = {}        # source -> [nu arrays]
    src_floor: dict = {}     # source -> [toa_err arrays]
    for bid, b in toa_table.items():
        r = no_native_dispersion_test(b["freq"], b["toa"], b["toa_err"],
                                      extra_index=index, include_drift=include_drift)
        if not r.available or not np.isfinite(r.a_tfpt_err) or r.a_tfpt_err == 0:
            continue
        s = b.get("source") or "unknown"
        vals.append(r.a_tfpt); errs.append(r.a_tfpt_err); srcs.append(s)
        src_nu.setdefault(s, []).append(np.asarray(b["freq"], float))
        src_floor.setdefault(s, []).append(np.asarray(b["toa_err"], float))
        per[bid] = {"source": s, "n_sub": int(len(b["freq"])),
                    "a_tfpt": r.a_tfpt, "a_tfpt_err": r.a_tfpt_err}
    n = len(vals)
    if n == 0:
        return FRB01Result(False, 0, index, verdict="data-limited: no usable bursts")
    vals, errs, srcs = np.array(vals), np.array(errs), np.array(srcs)
    by_source = {s: int(np.sum(srcs == s)) for s in sorted(set(srcs.tolist()))}
    n_sources = len(by_source)
    w = 1.0 / errs**2
    mean = float(np.sum(w * vals) / np.sum(w))
    err_mean = float(1.0 / np.sqrt(np.sum(w)))
    chi2_dof = float(np.sum((vals - mean) ** 2 * w)) / max(1, n - 1)
    universal = chi2_dof < 3.0
    zero = abs(mean) <= 2 * err_mean
    robust_mean = float(np.mean(vals))
    robust_err = float(np.std(vals, ddof=1) / np.sqrt(n)) if n > 1 else float(errs[0])
    robust_zero = abs(robust_mean) <= 2 * robust_err

    # ---- per-source A_TFPT + implied cross-band delay vs ToA precision ----------
    source_info: dict = {}
    for s in by_source:
        m = srcs == s
        vs, es = vals[m], errs[m]
        ws = 1.0 / es**2
        ms = float(np.sum(ws * vs) / np.sum(ws))
        scatter = float(np.std(vs, ddof=1) / np.sqrt(len(vs))) if len(vs) > 1 else float(es[0])
        es_eff = max(scatter, float(1.0 / np.sqrt(np.sum(ws))))
        nu_all = np.concatenate(src_nu[s])
        nu_lo, nu_hi = float(nu_all.min()), float(nu_all.max())
        basis_pp = abs(nu_lo**index - nu_hi**index)            # peak-to-peak of nu^index
        delay_s = abs(ms) * basis_pp                            # implied extra cross-band delay
        floor_s = float(np.median(np.concatenate(src_floor[s])))  # ToA precision
        ratio = delay_s / floor_s if floor_s > 0 else float("inf")
        source_info[s] = {"n": by_source[s], "atfpt": ms, "err": es_eff,
                          "delay_s": delay_s, "floor_s": floor_s, "ratio": ratio,
                          "below": ratio <= 1.0}
    ratios = [d["ratio"] for d in source_info.values()]
    max_ratio = float(max(ratios))
    all_below = all(d["below"] for d in source_info.values())

    # ---- cross-source homogeneity (universal-term presence) --------------------
    cs_chi2_dof, cs_consistent, cs_zero, grand = float("nan"), False, False, float("nan")
    if n_sources >= 2:
        sm = np.array([source_info[s]["atfpt"] for s in source_info])
        se = np.array([source_info[s]["err"] for s in source_info])
        wsrc = 1.0 / se**2
        grand = float(np.sum(wsrc * sm) / np.sum(wsrc))
        cs_chi2_dof = float(np.sum((sm - grand) ** 2 * wsrc)) / max(1, n_sources - 1)
        cs_consistent = cs_chi2_dof < 3.0
        cs_zero = abs(grand) <= 2 * float(np.sqrt(1.0 / np.sum(wsrc)))

    # ---- verdict: the implied-delay test is the physical arbiter ---------------
    if all_below:
        verdict = (f"no native dispersion required: the fitted non-plasma nu^{index:g} term "
                   f"implies an extra cross-band delay BELOW the ToA precision in all "
                   f"{n_sources} source(s) (worst delay/precision = {max_ratio:.1e}) -> "
                   f"consistent with TFPT's shared Lorentz cone; FRB.01 not falsified")
    elif n_sources >= 2 and not cs_consistent:
        verdict = (f"per-source A_TFPT mutually INCONSISTENT (cross-source chi2/dof="
                   f"{cs_chi2_dof:.0f}) => no universal non-plasma delay; the above-precision "
                   f"residuals are source-specific (intrinsic drift / DM-fit leakage)")
    elif n_sources >= 2 and cs_consistent and not cs_zero:
        verdict = (f"a COMMON non-zero non-plasma term (A_TFPT={grand:.2e}) with implied delay "
                   f"ABOVE precision -> tension with the shared Lorentz cone (kill-test flag)")
    else:
        verdict = (f"single source, implied non-plasma delay above precision but universality "
                   f"untestable with one source -> data-limited")
    return FRB01Result(True, n, index, per, mean, err_mean, chi2_dof, universal, zero, verdict,
                       n_sources, by_source, robust_mean, robust_err, robust_zero,
                       source_info, cs_chi2_dof, cs_consistent, cs_zero, all_below, max_ratio)

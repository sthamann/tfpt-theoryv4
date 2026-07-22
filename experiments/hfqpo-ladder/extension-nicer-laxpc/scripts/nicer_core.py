#!/usr/bin/env python3
"""NICER loader + line fit for the hfqpo-ladder extension scan.

Everything statistical is inherited bit-identically from the parent experiment's
scripts/pds_core.py (SEG_S = 16 s, DT = 1/4096 s, Leahy normalisation, Lorentzian
fit convention, injection thinning). The only new code is:

  - load_nicer_events(): read TIME/PI from a merged-MPU cleaned event file
    (ni*_0mpu7_cl.evt.gz) and apply a PI band cut (PI is in units of 10 eV);
  - build_segment_cache(): per-obsid per-band 16-s light-curve segments cached
    as uint16 (NBIN bins each) so stack/sanity/inject/scan never re-read raw;
  - fit_line_range(): the parent fit_line statistic with an EXPLICIT fit window
    (the parent's geometric window x/1.6 would place the strong 55 Hz anchor
    inside the 82.7 Hz tooth window; frozen windows in hypotheses/hfqpo_ext_v1.yaml).

Barycentring is skipped as in the parent (<= 0.011 Hz at 110 Hz, negligible).
NICER dead time (~20 us/event/FPM, 52 FPMs) is < 1% at ~2e4 c/s: no co-spectrum
needed; the local continuum fit absorbs the small Leahy noise deficit.
"""
import os
import sys

import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
EXT_ROOT = os.path.dirname(HERE)
PARENT_SCRIPTS = os.path.join(os.path.dirname(EXT_ROOT), "scripts")
sys.path.insert(0, PARENT_SCRIPTS)

from pds_core import DT, FREQ, NBIN, SEG_S, Stack, local_rebin, thin_lightcurve  # noqa: E402

RAW = os.path.join(EXT_ROOT, "data", "raw")
CACHE = os.path.join(EXT_ROOT, "results", "cache")
os.makedirs(CACHE, exist_ok=True)

MIN_PH_PER_SEG = 200          # same threshold as parent obsid_pds

BANDS = {                     # frozen in hypotheses/hfqpo_ext_v1.yaml
    "tot":  (30, 1000),       # PI 30-1000  = 0.3-10 keV (primary)
    "hard": (300, 1200),      # PI 300-1200 = 3-12 keV  (secondary)
}


def load_nicer_events(path, pi_lo, pi_hi):
    """Merged-MPU cleaned event file -> (sorted times in band, merged GTIs)."""
    with fits.open(path) as h:
        ev = None
        gtis = []
        for hdu in h[1:]:
            if hdu.name == "EVENTS":
                ev = hdu
            elif hdu.name.startswith("GTI") and hdu.data is not None \
                    and len(hdu.data):
                for a, b in zip(hdu.data.field(0), hdu.data.field(1)):
                    gtis.append((float(a), float(b)))
        t = np.asarray(ev.data.field("TIME"), dtype=np.float64)
        pi = np.asarray(ev.data.field("PI"))
    sel = (pi >= pi_lo) & (pi <= pi_hi)
    t = np.sort(t[sel])
    gtis.sort()
    merged = [list(gtis[0])]
    for a, b in gtis[1:]:
        if a <= merged[-1][1] + 1e-6:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return t, merged


def segments_from_events(times, gtis):
    """16-s segments fully inside GTIs -> list of uint16 count arrays (NBIN,)."""
    segs = []
    for a, b in gtis:
        n = int((b - a) / SEG_S)
        for i in range(n):
            t0 = a + i * SEG_S
            i0 = np.searchsorted(times, t0)
            i1 = np.searchsorted(times, t0 + SEG_S)
            if i1 - i0 < MIN_PH_PER_SEG:
                continue
            idx = ((times[i0:i1] - t0) / DT).astype(np.int64)
            idx = idx[(idx >= 0) & (idx < NBIN)]
            lc = np.bincount(idx, minlength=NBIN)
            if lc.max() >= 65535:
                continue          # uint16 overflow guard (never expected)
            segs.append(lc.astype(np.uint16))
    return segs


def build_segment_cache(obsid, band):
    """Cache per-segment light curves for one obsid+band; returns npz path."""
    tag = f"{obsid}__{band}"
    npz = os.path.join(CACHE, tag + ".npz")
    if os.path.exists(npz):
        return npz
    path = os.path.join(RAW, obsid, f"ni{obsid}_0mpu7_cl.evt.gz")
    pi_lo, pi_hi = BANDS[band]
    t, gtis = load_nicer_events(path, pi_lo, pi_hi)
    segs = segments_from_events(t, gtis)
    arr = np.array(segs, dtype=np.uint16) if segs else \
        np.zeros((0, NBIN), dtype=np.uint16)
    np.savez_compressed(npz, segs=arr)
    return npz


def load_segments(obsids, band):
    """Concatenate cached segments over obsids -> (n_seg, NBIN) uint16."""
    parts = []
    for obsid in obsids:
        npz = build_segment_cache(obsid, band)
        d = np.load(npz)
        if len(d["segs"]):
            parts.append(d["segs"])
    if not parts:
        return np.zeros((0, NBIN), dtype=np.uint16)
    return np.concatenate(parts, axis=0)


def stack_from_segments(segs, thin=None, rng=None):
    """Leahy stack from uint16 segments; optional QPO injection by thinning."""
    st = Stack()
    acc = np.zeros(len(FREQ))
    nph_tot = 0
    for lc in segs:
        lc = lc.astype(np.float64)
        if thin is not None:
            f0, rms, q = thin
            lc = thin_lightcurve(lc, f0, rms, q, rng)
        nph = lc.sum()
        ft = np.fft.rfft(lc)[1:]
        acc += (2.0 / nph) * np.abs(ft) ** 2
        nph_tot += int(nph)
    st.add(acc, len(segs), nph_tot)
    return st


def fit_line_range(stack, f0_target, f0_tol, f_lo, f_hi,
                   q_lo=4.0, q_hi=25.0, df=None):
    """Parent fit_line statistic with an explicit fit window [f_lo, f_hi].

    Identical model, Q grid, significance convention (norm/sigma_norm) and
    3-sigma rms upper-limit grid (Q = 5, 8, 12, 20) as pds_core.fit_line."""
    if df is None:
        df = max(0.25, f0_target / 150.0)
    f, p, sig = local_rebin(stack, f_lo, f_hi, df)
    if len(f) < 10 or stack.nseg == 0:
        return None
    rate = stack.mean_rate

    def leahy_int_to_rms(norm):
        return np.sqrt(max(norm, 0.0) / rate) if rate > 0 else np.nan

    def model(x, c0, c1, norm, f0, fwhm):
        lor = norm * (fwhm / (2 * np.pi)) / ((x - f0) ** 2 + (fwhm / 2) ** 2)
        return c0 + c1 * (x / f0_target - 1.0) + lor

    best = None
    for q0 in (5.0, 8.0, 15.0):
        p0 = [float(np.median(p)), 0.0,
              max((p.max() - np.median(p)) * f0_target / q0, 1e-3),
              f0_target, f0_target / q0]
        lb = [0.0, -np.inf, 0.0, f0_target - f0_tol, f0_target / q_hi]
        ub = [np.inf, np.inf, np.inf, f0_target + f0_tol, f0_target / q_lo]
        try:
            popt, pcov = curve_fit(model, f, p, p0=p0, sigma=sig,
                                   bounds=(lb, ub), maxfev=30000)
        except Exception:
            continue
        resid = (p - model(f, *popt)) / sig
        chi2 = float((resid ** 2).sum())
        if best is None or chi2 < best["chi2"] - 1e-9:
            best = {"chi2": chi2, "dof": len(f) - 5,
                    "popt": popt, "perr": np.sqrt(np.abs(np.diag(pcov)))}
    if best is None:
        return None

    ul_norm_max = 0.0
    for q0 in (5.0, 8.0, 12.0, 20.0):
        fwhm0 = f0_target / q0

        def model_fq(x, c0, c1, norm, f0):
            return model(x, c0, c1, norm, f0, fwhm0)

        try:
            popt, pcov = curve_fit(
                model_fq, f, p, p0=[float(np.median(p)), 0.0, 1e-3, f0_target],
                sigma=sig,
                bounds=([0.0, -np.inf, 0.0, f0_target - f0_tol],
                        [np.inf, np.inf, np.inf, f0_target + f0_tol]),
                maxfev=30000)
            perr = np.sqrt(np.abs(np.diag(pcov)))
            ul_norm_max = max(ul_norm_max, popt[2] + 3.0 * perr[2])
        except Exception:
            continue

    c0, c1, norm, f0, fwhm = best["popt"]
    en = best["perr"][2]
    signif = norm / en if en > 0 else 0.0
    return {
        "f0_hz": float(f0), "fwhm_hz": float(fwhm), "q": float(f0 / fwhm),
        "norm_leahy": float(norm), "norm_err": float(en),
        "significance_sigma": float(signif),
        "rms_frac": float(leahy_int_to_rms(norm)),
        "rms_pct": float(100 * leahy_int_to_rms(norm)),
        "rms_ul3sig_pct": float(100 * leahy_int_to_rms(ul_norm_max)),
        "chi2": best["chi2"], "dof": best["dof"],
        "fit_window_hz": [f_lo, f_hi],
        "mean_rate_cps": float(stack.mean_rate), "n_seg": int(stack.nseg),
    }

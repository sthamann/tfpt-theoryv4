#!/usr/bin/env python3
"""Core PDS machinery for the H3 archival RXTE PCA scan.

Leahy-normalised power density spectra straight from PCA high-time-resolution
science files (processed SE event files, single-bit and fine binned XTE_SA
modes). No HEASoft, no barycentring:

    Barycentring is deliberately skipped. The largest frequency modulation the
    solar-system barycentre motion can imprint is v/c ~ 1e-4; at the highest
    target frequency (661.5 Hz) that is <= 0.07 Hz, negligible against HFQPO
    widths of 5-40 Hz and the 1/16 s = 0.0625 Hz Fourier resolution used here.

Segmenting: 16-s segments, dt = 1/4096 s (Nyquist 2048 Hz), segments must lie
entirely inside a GTI of their file. Stacked per (source, group, band).
"""
import glob
import json
import os
import re

import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit

SEG_S = 16.0
DT = 1.0 / 4096.0
NBIN = int(SEG_S / DT)          # 65536
NYQ = 0.5 / DT                  # 2048 Hz
FREQ = np.fft.rfftfreq(NBIN, DT)[1:]   # drop DC


# ---------------------------------------------------------------------------
# file -> (event times | binned counts) in a chosen channel band
# ---------------------------------------------------------------------------
def _tddes_channels(tddes):
    m = re.search(r"C\[(\d+)~(\d+)\]", tddes or "")
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def _gtis(hdul):
    gt = []
    for hdu in hdul[2:]:
        if hdu.name == "GTI" and hdu.data is not None and len(hdu.data):
            for a, b in zip(hdu.data.field(0), hdu.data.field(1)):
                gt.append((float(a), float(b)))
    if not gt:
        h = hdul[1].header
        gt = [(float(h["TSTART"]), float(h["TSTOP"]))]
    # merge overlapping
    gt.sort()
    merged = [list(gt[0])]
    for a, b in gt[1:]:
        if a <= merged[-1][1] + 1e-6:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return merged


def _tevtb2_bins(tevtb2):
    """Parse the C[a~b,c~d,...] channel-bin list of a TEVTB2 descriptor.
    Returns list of (abs_lo, abs_hi) per PHA bin index, or None."""
    m = re.search(r"C\[([^\]]+)\]", tevtb2 or "")
    if not m:
        return None
    bins = []
    for part in m.group(1).split(","):
        part = part.strip()
        mm = re.match(r"^\(?(\d+)~(\d+)", part)
        if mm:
            bins.append((int(mm.group(1)), int(mm.group(2))))
        elif part.isdigit():
            bins.append((int(part), int(part)))
        else:
            mm = re.match(r"^(\d+)", part)
            if mm:
                bins.append((int(mm.group(1)), int(mm.group(1))))
    return bins or None


def load_se_events(path, abs_lo=None, abs_hi=249):
    """Processed SE*.evt file -> (times, gtis, mode, file_chan_range).

    abs_lo/abs_hi select ABSOLUTE channels. The PHA column of processed SE
    files holds the mode's binned channel index; TEVTB2 maps bin -> absolute
    channels. Files entirely inside the requested range are used uncut."""
    with fits.open(path) as h:
        hdr = h[1].header
        mode = hdr.get("DATAMODE", "?")
        crange = _tddes_channels(hdr.get("TDDES2"))
        cols = [c.upper() for c in h[1].columns.names]
        t = np.asarray(h[1].data.field(0), dtype=np.float64)
        pha = None
        for cname in ("PHA", "CHANNEL"):
            if cname in cols:
                pha = np.asarray(h[1].data.field(h[1].columns.names[cols.index(cname)]))
                break
        tevtb2 = hdr.get("TEVTB2", "")
        gt = _gtis(h)
    if abs_lo is not None and crange is not None:
        if crange[0] >= abs_lo and crange[1] <= abs_hi:
            pass  # whole file inside band
        elif crange[1] < abs_lo or crange[0] > abs_hi:
            t = t[:0]  # entirely outside
        elif pha is not None:
            bins = _tevtb2_bins(tevtb2)
            if bins is not None and pha.max() < len(bins):
                keep_bins = {i for i, (a, b) in enumerate(bins)
                             if a >= abs_lo and b <= abs_hi}
                sel = np.isin(pha, list(keep_bins))
                t = t[sel]
            else:
                t = t[:0]  # cannot cut safely -> exclude from this band
    return t, gt, mode, crange


def load_sa_counts(path):
    """Fine binned / single-bit XTE_SA file -> (tstart_rows, dt_bin, counts2d,
    gtis, mode, chan_range). counts2d: one row of nbin bins per table row."""
    with fits.open(path) as h:
        hdr = h[1].header
        mode = hdr.get("DATAMODE", "?")
        tddes = hdr.get("TDDES2", "")
        m = re.search(r"T\[[\d.]+;([\d.eE+-]+);(\d+)\]", tddes)
        if not m:
            return None
        dtb = float(m.group(1))
        nb = int(m.group(2))
        crange = _tddes_channels(tddes)
        t0 = np.asarray(h[1].data.field(0), dtype=np.float64)
        cnt = h[1].data.field(1)
        cnt = np.asarray(cnt, dtype=np.float64)
        gt = _gtis(h)
    if cnt.ndim == 1:
        cnt = cnt.reshape(len(t0), -1)
    if cnt.ndim == 3:  # (rows, nchan, nbin) or (rows, nbin, nchan)
        # sum over the channel axis (the one whose length != nb)
        ax = 1 if cnt.shape[1] != nb else 2
        cnt = cnt.sum(axis=ax)
    return t0, dtb, cnt, gt, mode, crange


# ---------------------------------------------------------------------------
# segments -> Leahy PDS
# ---------------------------------------------------------------------------
def segments_from_gti(gtis, tref=None):
    segs = []
    for a, b in gtis:
        t = a if tref is None else max(a, tref)
        n = int((b - t) / SEG_S)
        for i in range(n):
            segs.append(t + i * SEG_S)
    return segs


def pds_from_events(times, gtis):
    """-> (sum_leahy, n_seg, n_photons_used, sum_rate). Leahy per segment."""
    acc = np.zeros(len(FREQ))
    nseg = 0
    nph_tot = 0
    times = np.sort(times)
    for t0 in segments_from_gti(gtis):
        i0 = np.searchsorted(times, t0)
        i1 = np.searchsorted(times, t0 + SEG_S)
        nph = i1 - i0
        if nph < 100:      # essentially empty segment (detector off)
            continue
        idx = ((times[i0:i1] - t0) / DT).astype(np.int64)
        idx = idx[(idx >= 0) & (idx < NBIN)]
        lc = np.bincount(idx, minlength=NBIN).astype(np.float64)
        ft = np.fft.rfft(lc)[1:]
        acc += (2.0 / nph) * np.abs(ft) ** 2
        nseg += 1
        nph_tot += nph
    return acc, nseg, nph_tot


def pds_from_binned(t0_rows, dtb, counts, gtis):
    """Binned/single-bit rows -> Leahy PDS accumulated over 16-s segments."""
    acc = np.zeros(len(FREQ))
    nseg = 0
    nph_tot = 0
    row_len = counts.shape[1] * dtb
    # build a contiguous series per GTI
    for a, b in gtis:
        sel = (t0_rows >= a - 1e-6) & (t0_rows + row_len <= b + 1e-6)
        if not sel.any():
            continue
        rows = np.where(sel)[0]
        # split into contiguous row runs
        run_start = rows[0]
        prev = rows[0]
        runs = []
        for r in rows[1:]:
            if abs(t0_rows[r] - (t0_rows[prev] + row_len)) > dtb:
                runs.append((run_start, prev))
                run_start = r
            prev = r
        runs.append((run_start, prev))
        for r0, r1 in runs:
            series = counts[r0:r1 + 1].ravel()
            # rebin to DT if finer
            fac = DT / dtb
            if abs(fac - round(fac)) > 1e-9 or fac < 1:
                # dtb coarser than DT or non-integer factor: skip (mode unusable)
                if dtb > DT * (1 + 1e-9):
                    continue
                continue
            fac = int(round(fac))
            n_dt = len(series) // fac
            series = series[:n_dt * fac].reshape(n_dt, fac).sum(axis=1)
            nseg_here = n_dt // NBIN
            for i in range(nseg_here):
                lc = series[i * NBIN:(i + 1) * NBIN]
                nph = lc.sum()
                if nph < 100:
                    continue
                ft = np.fft.rfft(lc)[1:]
                acc += (2.0 / nph) * np.abs(ft) ** 2
                nseg += 1
                nph_tot += int(nph)
    return acc, nseg, nph_tot


# ---------------------------------------------------------------------------
# stacked PDS container
# ---------------------------------------------------------------------------
class Stack:
    def __init__(self):
        self.acc = np.zeros(len(FREQ))
        self.nseg = 0
        self.nph = 0

    def add(self, acc, nseg, nph):
        self.acc += acc
        self.nseg += nseg
        self.nph += nph

    @property
    def mean_rate(self):
        return self.nph / (self.nseg * SEG_S) if self.nseg else 0.0

    def leahy(self):
        return self.acc / self.nseg

    def rebin_log(self, f_min=10.0, dlogf=0.01):
        """log-rebinned (f, P, sigma_P, n_raw_bins)."""
        P = self.leahy()
        edges = [f_min]
        while edges[-1] < NYQ:
            edges.append(edges[-1] * (1 + dlogf * 4.6))  # ~1.047 factor
        edges = np.array(edges)
        idx = np.digitize(FREQ, edges)
        out = []
        for k in range(1, len(edges)):
            m = idx == k
            n = m.sum()
            if n == 0:
                continue
            pm = P[m].mean()
            out.append((FREQ[m].mean(), pm, pm / np.sqrt(n * self.nseg), n))
        return np.array(out)


# ---------------------------------------------------------------------------
# Lorentzian fitting near a target frequency (linear-grid, fine)
# ---------------------------------------------------------------------------
def local_rebin(stack, f_lo, f_hi, df=2.0):
    P = stack.leahy()
    m = (FREQ >= f_lo) & (FREQ <= f_hi)
    f = FREQ[m]
    p = P[m]
    nfac = max(1, int(round(df / (FREQ[1] - FREQ[0]))))
    n = len(f) // nfac
    f = f[:n * nfac].reshape(n, nfac).mean(axis=1)
    p = p[:n * nfac].reshape(n, nfac).mean(axis=1)
    sig = p / np.sqrt(nfac * stack.nseg)
    return f, p, sig


def fit_line(stack, f0_target, f0_tol, q_lo=4.0, q_hi=25.0,
             window=1.6, df=None):
    """Fit continuum + Lorentzian around f0_target (free FWHM within
    published HFQPO coherences Q in [q_lo, q_hi]; f0 free within +-f0_tol).

    Significance = norm / sigma_norm (Belloni et al. 2012 convention).
    rms_ul3sig_pct: 3-sigma upper limit on fractional rms, taken as the max
    over a fixed-Q grid (5, 8, 12, 20) so narrow AND broad teeth are covered."""
    if df is None:
        df = max(0.25, f0_target / 150.0)
    f, p, sig = local_rebin(stack, f0_target / window, f0_target * window, df)
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

    # 3-sigma upper limits on the line integral over a fixed-Q grid
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
        "mean_rate_cps": float(stack.mean_rate), "n_seg": int(stack.nseg),
    }


# ---------------------------------------------------------------------------
# injection: thin real events with a Lorentzian-coherence oscillation
# ---------------------------------------------------------------------------
def inject_qpo_events(times, f0, rms_frac, q, rng):
    """Return a thinned copy of `times` carrying a QPO with fractional rms
    `rms_frac`, centroid f0, quality q. Piecewise-coherent oscillator:
    coherence segments of exponential length tau = Q/(pi f0) with fresh
    random phase produce a Lorentzian of FWHM = f0/Q. Acceptance-rejection:
    p(t) = (1 + a cos phi(t)) / (1 + a), a = sqrt(2) * rms_frac / thinned."""
    a = np.sqrt(2.0) * rms_frac
    if a >= 1.0:
        raise ValueError("rms too large for thinning")
    t = np.sort(times)
    if len(t) == 0:
        return t
    tau = q / (np.pi * f0)
    t0, t1 = t[0], t[-1]
    # build phase-jump boundaries
    bounds = [t0]
    while bounds[-1] < t1:
        bounds.append(bounds[-1] + rng.exponential(tau))
    bounds = np.array(bounds)
    phases = rng.uniform(0, 2 * np.pi, len(bounds))
    seg_idx = np.searchsorted(bounds, t, side="right") - 1
    phi = 2 * np.pi * f0 * t + phases[seg_idx]
    p = (1.0 + a * np.cos(phi)) / (1.0 + a)
    keep = rng.uniform(size=len(t)) < p
    return t[keep]


def thin_lightcurve(lc, f0, rms_frac, q, rng):
    """Binomial-thin a binned light curve (counts per DT bin) with the same
    piecewise-coherent Lorentzian oscillator. Statistically equivalent to
    per-event thinning at the DT resolution the PDS uses; works for summed
    event + single-bit streams alike. Fresh phase per 16-s segment is fine
    since the coherence time Q/(pi f0) << SEG_S for all targets."""
    a = np.sqrt(2.0) * rms_frac
    n = len(lc)
    tb = (np.arange(n) + 0.5) * DT
    tau = q / (np.pi * f0)
    # phase-jump boundaries across the segment
    n_jump = max(int(SEG_S / tau * 2 + 10), 4)
    gaps = rng.exponential(tau, n_jump)
    bounds = np.concatenate([[0.0], np.cumsum(gaps)])
    while bounds[-1] < SEG_S:
        bounds = np.concatenate([bounds, [bounds[-1] + rng.exponential(tau)]])
    phases = rng.uniform(0, 2 * np.pi, len(bounds))
    seg_idx = np.searchsorted(bounds, tb, side="right") - 1
    phi = 2 * np.pi * f0 * tb + phases[seg_idx]
    p = (1.0 + a * np.cos(phi)) / (1.0 + a)
    return rng.binomial(lc.astype(np.int64), p).astype(np.float64)

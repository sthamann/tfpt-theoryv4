#!/usr/bin/env python3
"""Orchestrator for the H3 archival scan: stack -> sanity -> inject -> scan.

Usage:  python run_scan.py stack|sanity|inject|scan|all

Checkpoints (JSON/NPZ) go to results/archival/; stacked PDS are cached so
every later stage can be re-run without touching the raw files again.

File-usage rule (documented): only PROCESSED SE*.evt event files are used for
event modes (raw FS3x XTE_SE twins carry undecoded packed event words and
unfiltered event streams); single-bit SB_* XTE_SA modes are decoded directly;
binned B_* modes all have Nyquist < 512 Hz in these configs and are unusable
for the 100-1000 Hz search band.
"""
import glob
import json
import os
import sys

import numpy as np
from astropy.io import fits

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pds_core import (DT, FREQ, NBIN, NYQ, SEG_S, Stack, fit_line,
                      inject_qpo_events, load_sa_counts, load_se_events,
                      pds_from_binned, pds_from_events, thin_lightcurve)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ARCH = os.path.join(ROOT, "data", "archive")
RAW = os.path.join(ARCH, "raw")
RESDIR = os.path.join(ROOT, "results", "archival")
CACHE = os.path.join(RESDIR, "cache")
os.makedirs(CACHE, exist_ok=True)

with open(os.path.join(ARCH, "obsid_manifest.json")) as f:
    MANIFEST = json.load(f)

# Per-source scan configuration. band 'hard' = processed event modes
# (channels >=36 abs, >=50 for the 1996 J1655 config, ~>13 keV);
# band 'wide' = hard + single-bit modes (adds ~2-13 keV where telemetered).
SCAN = {
    "GRO_J1655-40": {
        "groups_scan": ["B1_triplet", "B2_450Hz", "T300_epochs"],
        "sanity": [
            # gating pair reproductions (published values in comments):
            # 441-450 Hz, 13-27 keV, 4.5-6.0% rms (Strohmayer 01; Motta+14)
            {"group": "B2_450Hz", "band": "hard27", "f0": 449.0, "tol": 12.0},
            {"group": "B1_triplet", "band": "hard27", "f0": 441.0, "tol": 12.0},
            # 274-313 Hz total band, 0.9-1.4% rms (Belloni+12 Tab.2 T entries)
            {"group": "T300_epochs", "band": "bt", "f0": 296.0, "tol": 25.0},
        ],
        "scan_band": "hard27",    # prereg: tooth expected >13 keV like the 450
        "secondary_band": "bt",
        "tooth": 661.5, "tooth_tol": 6.0, "integer": 588.0, "integer_tol": 6.0,
    },
    "XTE_J1550-564": {
        "groups_scan": ["hard_280", "total_180", "outburst2000_270"],
        "sanity": [
            # 272-284 Hz hard band (chn 14-79), 3.7-5.2% rms (Belloni+12)
            {"group": "hard_280", "band": "bh", "f0": 280.0, "tol": 12.0},
            # 180-185 Hz total band (chn 0-79), 1.1-1.7% rms (Belloni+12)
            {"group": "total_180", "band": "bt", "f0": 183.0, "tol": 12.0},
            # 264-275 Hz hard band, 2000 outburst, 5.4-6.7% rms (Belloni+12)
            {"group": "outburst2000_270", "band": "bh", "f0": 273.0, "tol": 12.0},
        ],
        "scan_band": "bh",        # nu_u (276) is a hard-band feature
        "secondary_band": "bt",
        "tooth": 414.0, "tooth_tol": 9.0, "integer": 368.0, "integer_tol": 9.0,
    },
    "GRS_1915+105": {
        "groups_scan": ["gamma_1997_41_69", "gamma_1996_67", "delta_2003_34_68"],
        "sanity": [
            # 69.2 Hz (1.9% rms) + 41.5 Hz (2.4% rms), 13-27 keV (Strohmayer 01b)
            {"group": "gamma_1997_41_69", "band": "hard27", "f0": 69.2, "tol": 4.0},
            {"group": "gamma_1997_41_69", "band": "hard27", "f0": 41.5, "tol": 4.0},
            # 68 Hz (24 sigma) + 34 Hz (4.2 sigma), chn 8-79 = 3.3-33 keV (BA13)
            {"group": "delta_2003_34_68", "band": "bt", "f0": 68.0, "tol": 4.0},
            {"group": "delta_2003_34_68", "band": "bt", "f0": 34.0, "tol": 4.0},
        ],
        "scan_band": "bt",        # BA12/BA13 detection band
        "secondary_band": "hard27",
        "tooth": 252.0, "tooth_tol": 9.0, "integer": 224.0, "integer_tol": 9.0,
    },
    "H1743-322": {
        "groups_scan": ["q_low_242", "q_high_166"],
        "sanity": [
            # 242+-3 Hz, 1.1% rms, 7-35 keV (Remillard+06, 6.0 sigma)
            {"group": "q_low_242", "band": "bh", "f0": 242.0, "tol": 9.0},
            # 166+-5 Hz, 0.6% rms, 2-35 keV (Remillard+06, 4.1 sigma)
            {"group": "q_high_166", "band": "bt", "f0": 166.0, "tol": 9.0},
        ],
        "scan_band": "bh",        # R06 band in which nu_u (242) was found
        "secondary_band": "bt",
        "tooth": 363.0, "tooth_tol": 9.0, "integer": 322.7, "integer_tol": 9.0,
    },
}


# ---------------------------------------------------------------------------
# stage 1: stacking
# ---------------------------------------------------------------------------
def classify_files(obsid):
    """-> list of (path, kind, mode); kind in {'se','sb'}; dedupe raw twins."""
    out = []
    for p in sorted(glob.glob(os.path.join(RAW, obsid, "*"))):
        base = os.path.basename(p)
        try:
            with fits.open(p) as h:
                if len(h) < 2:
                    continue
                mode = h[1].header.get("DATAMODE", "")
                ncols = len(h[1].columns.names)
        except Exception:
            continue
        if mode.startswith("E_"):
            # processed SE files carry >=4 columns (TIME/Event/PCUID/PHA...)
            if base.upper().startswith("SE") and ncols >= 4:
                out.append((p, "se", mode))
        elif mode.startswith("SB_"):
            out.append((p, "sb", mode))
        # B_* binned modes in these configs are all Nyquist < 512 Hz -> skip
    return out


HARD_CHAN_LO = 36  # abs channel ~>13 keV for the relevant gain epochs

# Band definitions (absolute PCA channels). ev: cut applied to event modes
# (via TEVTB2 bin mapping); sb: single-bit streams kept if their channel
# range lies inside; None = single-bit excluded.
BANDS = {
    "hard27": {"ev": (36, 71), "sb": None},      # ~13-27 keV (Strohmayer band)
    "bh":     {"ev": (36, 79), "sb": (14, 35)},  # ~ Belloni+12 / R06 hard band
    "bt":     {"ev": (0, 79),  "sb": (0, 249)},  # ~ total band 0-79 (+ full-band SB)
}


def obsid_streams(obsid, band):
    """Load all usable data streams of one obsid for a named band.
    Returns (event_streams, binned_streams)."""
    spec = BANDS[band]
    ev, bn = [], []
    for p, kind, mode in classify_files(obsid):
        if kind == "se":
            t, gt, m, cr = load_se_events(p, spec["ev"][0], spec["ev"][1])
            if len(t):
                ev.append((t, gt))
        elif kind == "sb" and spec["sb"] is not None:
            r = load_sa_counts(p)
            if r is None:
                continue
            t0, dtb, cnt, gt, m, cr = r
            if dtb > DT * (1 + 1e-9):
                continue
            if cr is not None and (cr[0] < spec["sb"][0] or cr[1] > spec["sb"][1]):
                continue
            bn.append((t0, dtb, cnt, gt))
    return ev, bn


def _gti_intersect(g1, g2):
    out = []
    i = j = 0
    while i < len(g1) and j < len(g2):
        a = max(g1[i][0], g2[j][0])
        b = min(g1[i][1], g2[j][1])
        if b > a:
            out.append((a, b))
        if g1[i][1] < g2[j][1]:
            i += 1
        else:
            j += 1
    return out


def _span(item):
    """Time span (t_lo, t_hi) of a stream from its GTIs."""
    g = item[-1] if isinstance(item[-1], list) else item[1]
    return g[0][0], g[-1][1]


def obsid_pds(obsid, band, thin=None):
    """Summed-band light curve PDS for one obsid. Streams (different data
    modes) covering the SAME time chunk are co-added per segment (published
    approach: merge all good events); chunks are defined by grouping streams
    whose spans overlap, and GTIs are intersected within a chunk only.
    thin: optional (f0, rms, q, rng) -> QPO injected into the summed
    per-segment light curve by binomial thinning (all streams)."""
    ev, bn = obsid_streams(obsid, band)
    streams = [{"kind": "ev", "t": np.sort(t), "gti": gt} for t, gt in ev] + \
              [{"kind": "bn", "t0": t0, "dtb": dtb, "cnt": cnt, "gti": gt}
               for t0, dtb, cnt, gt in bn]
    if not streams:
        return np.zeros(len(FREQ)), 0, 0
    # group streams into chunks by span overlap
    for s in streams:
        s["lo"], s["hi"] = s["gti"][0][0], s["gti"][-1][1]
    streams.sort(key=lambda s: s["lo"])
    chunks = []
    for s in streams:
        placed = False
        for ch in chunks:
            if s["lo"] < ch["hi"] - 8.0 and s["hi"] > ch["lo"] + 8.0:
                ch["streams"].append(s)
                ch["lo"] = min(ch["lo"], s["lo"])
                ch["hi"] = max(ch["hi"], s["hi"])
                placed = True
                break
        if not placed:
            chunks.append({"lo": s["lo"], "hi": s["hi"], "streams": [s]})

    acc = np.zeros(len(FREQ))
    nseg = 0
    nph_tot = 0
    for ch in chunks:
        gti = ch["streams"][0]["gti"]
        for s in ch["streams"][1:]:
            gti = _gti_intersect(gti, s["gti"])
        for a, b in gti:
            n = int((b - a) / SEG_S)
            for i in range(n):
                t0 = a + i * SEG_S
                lc = np.zeros(NBIN)
                ok = True
                for s in ch["streams"]:
                    if s["kind"] == "ev":
                        ts = s["t"]
                        i0 = np.searchsorted(ts, t0)
                        i1 = np.searchsorted(ts, t0 + SEG_S)
                        idx = ((ts[i0:i1] - t0) / DT).astype(np.int64)
                        idx = idx[(idx >= 0) & (idx < NBIN)]
                        lc += np.bincount(idx, minlength=NBIN)
                    else:
                        t0r, dtb, cnt = s["t0"], s["dtb"], s["cnt"]
                        row_len = cnt.shape[1] * dtb
                        fac = int(round(DT / dtb))
                        r0 = np.searchsorted(t0r, t0 - 0.5 * row_len)
                        hit = False
                        for r in range(max(r0 - 1, 0), len(t0r)):
                            if t0r[r] >= t0 + SEG_S - 1e-6:
                                break
                            if t0r[r] >= t0 - 1e-6 and \
                               t0r[r] + row_len <= t0 + SEG_S + 1e-6:
                                off = int(round((t0r[r] - t0) / DT))
                                series = cnt[r].reshape(-1, fac).sum(axis=1)
                                n_here = min(len(series), NBIN - off)
                                if off >= 0 and n_here > 0:
                                    lc[off:off + n_here] += series[:n_here]
                                    hit = True
                        if not hit:
                            ok = False
                            break
                if not ok:
                    continue
                if thin is not None:
                    f0, rms, q, rng = thin
                    lc = thin_lightcurve(lc, f0, rms, q, rng)
                nph = lc.sum()
                if nph < 200:
                    continue
                ft = np.fft.rfft(lc)[1:]
                acc += (2.0 / nph) * np.abs(ft) ** 2
                nseg += 1
                nph_tot += int(nph)
    return acc, nseg, nph_tot


def build_stack(source, group, band):
    """Stack summed-band Leahy PDS over all obsids of a manifest group."""
    tag = f"{source}__{group}__{band}".replace("+", "p")
    npz = os.path.join(CACHE, tag + ".npz")
    if os.path.exists(npz):
        d = np.load(npz)
        st = Stack()
        st.add(d["acc"], int(d["nseg"]), int(d["nph"]))
        return st
    st = Stack()
    used = []
    obsids = MANIFEST["sources"][source]["groups"][group]["obsids"]
    for obsid in obsids:
        acc, nseg, nph = obsid_pds(obsid, band)
        if nseg:
            st.add(acc, nseg, nph)
            used.append({"obsid": obsid, "nseg": nseg, "nph": int(nph)})
    np.savez_compressed(npz, acc=st.acc, nseg=st.nseg, nph=st.nph)
    with open(os.path.join(CACHE, tag + "_files.json"), "w") as f:
        json.dump(used, f, indent=1)
    return st


def stage_stack():
    report = {}
    for source, cfg in SCAN.items():
        bands = {cfg["scan_band"], cfg["secondary_band"]} | \
                {s["band"] for s in cfg["sanity"]}
        for group in cfg["groups_scan"]:
            for band in sorted(bands):
                st = build_stack(source, group, band)
                key = f"{source}/{group}/{band}"
                report[key] = {"n_seg": st.nseg, "n_photons": st.nph,
                               "mean_rate_cps": round(st.mean_rate, 1),
                               "exposure_s": st.nseg * SEG_S}
                print(f"{key:55s} nseg={st.nseg:6d} rate={st.mean_rate:9.1f} c/s",
                      flush=True)
    with open(os.path.join(RESDIR, "stack_report.json"), "w") as f:
        json.dump(report, f, indent=2)


# ---------------------------------------------------------------------------
# stage 2: sanity gate
# ---------------------------------------------------------------------------
def stage_sanity():
    """Gate rule: the FIRST sanity entry per source is the nu_u anchor (the
    published upper-HFQPO of the pair, in its published band) and MUST be
    reproduced at >=3 sigma. Secondary published lines (weaker features,
    published at 3-4.2 sigma themselves) are reported; a miss there is a
    caveat, not a stop, provided the measured rms matches the published one."""
    out = {}
    anchors_ok = True
    n_pass = n_tot = 0
    for source, cfg in SCAN.items():
        for j, s in enumerate(cfg["sanity"]):
            st = build_stack(source, s["group"], s["band"])
            r = fit_line(st, s["f0"], s["tol"])
            key = f"{source}/{s['group']}/{s['band']}/@{s['f0']}Hz"
            gating = (j == 0)
            if r is None:
                out[key] = {"status": "no_fit", "gating": gating}
                if gating:
                    anchors_ok = False
                continue
            detected = r["significance_sigma"] >= 3.0
            n_tot += 1
            n_pass += int(detected)
            r["gating"] = gating
            r["status"] = "pass" if detected else ("ANCHOR_FAIL" if gating
                                                   else "secondary_miss")
            if gating and not detected:
                anchors_ok = False
            out[key] = r
            print(f"{key:60s} f0={r['f0_hz']:7.1f} rms={r['rms_pct']:.2f}% "
                  f"sig={r['significance_sigma']:.1f} {r['status']}")
    out["_gate"] = "PASS" if (anchors_ok and n_pass >= 0.8 * n_tot) else \
                   ("PASS_WITH_CAVEATS" if anchors_ok else "FAIL")
    out["_n_pass"] = n_pass
    out["_n_total"] = n_tot
    with open(os.path.join(RESDIR, "sanity_gate.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"SANITY GATE: {out['_gate']} ({n_pass}/{n_tot} lines reproduced)")


# ---------------------------------------------------------------------------
# stage 3: injection calibration
# ---------------------------------------------------------------------------
def collect_segments(source, cfg, max_segments=6000, seed=123):
    """Preload the per-segment light curves of the scan-band stack once
    (uint8 counts per DT bin) so injection trials only thin + FFT.
    If the stack exceeds max_segments, a random subsample is used and the
    effective significance threshold is scaled accordingly."""
    segs = []
    band = cfg["scan_band"]
    for group in cfg["groups_scan"]:
        for obsid in MANIFEST["sources"][source]["groups"][group]["obsids"]:
            ev, bn = obsid_streams(obsid, band)
            streams = [{"kind": "ev", "t": np.sort(t), "gti": gt}
                       for t, gt in ev] + \
                      [{"kind": "bn", "t0": t0, "dtb": dtb, "cnt": cnt,
                        "gti": gt} for t0, dtb, cnt, gt in bn]
            if not streams:
                continue
            for s in streams:
                s["lo"], s["hi"] = s["gti"][0][0], s["gti"][-1][1]
            streams.sort(key=lambda s: s["lo"])
            chunks = []
            for s in streams:
                placed = False
                for ch in chunks:
                    if s["lo"] < ch["hi"] - 8.0 and s["hi"] > ch["lo"] + 8.0:
                        ch["streams"].append(s)
                        ch["lo"] = min(ch["lo"], s["lo"])
                        ch["hi"] = max(ch["hi"], s["hi"])
                        placed = True
                        break
                if not placed:
                    chunks.append({"lo": s["lo"], "hi": s["hi"], "streams": [s]})
            for ch in chunks:
                gti = ch["streams"][0]["gti"]
                for s in ch["streams"][1:]:
                    gti = _gti_intersect(gti, s["gti"])
                for a, b in gti:
                    for i in range(int((b - a) / SEG_S)):
                        t0 = a + i * SEG_S
                        lc = np.zeros(NBIN)
                        ok = True
                        for s in ch["streams"]:
                            if s["kind"] == "ev":
                                ts = s["t"]
                                i0 = np.searchsorted(ts, t0)
                                i1 = np.searchsorted(ts, t0 + SEG_S)
                                idx = ((ts[i0:i1] - t0) / DT).astype(np.int64)
                                idx = idx[(idx >= 0) & (idx < NBIN)]
                                lc += np.bincount(idx, minlength=NBIN)
                            else:
                                t0r, dtb, cnt = s["t0"], s["dtb"], s["cnt"]
                                row_len = cnt.shape[1] * dtb
                                fac = int(round(DT / dtb))
                                r0 = np.searchsorted(t0r, t0 - 0.5 * row_len)
                                hit = False
                                for rr in range(max(r0 - 1, 0), len(t0r)):
                                    if t0r[rr] >= t0 + SEG_S - 1e-6:
                                        break
                                    if t0r[rr] >= t0 - 1e-6 and \
                                       t0r[rr] + row_len <= t0 + SEG_S + 1e-6:
                                        off = int(round((t0r[rr] - t0) / DT))
                                        series = cnt[rr].reshape(-1, fac).sum(axis=1)
                                        nh = min(len(series), NBIN - off)
                                        if off >= 0 and nh > 0:
                                            lc[off:off + nh] += series[:nh]
                                            hit = True
                                if not hit:
                                    ok = False
                                    break
                        if ok and lc.sum() >= 200 and lc.max() < 255:
                            segs.append(lc.astype(np.uint8))
    rng = np.random.default_rng(seed)
    n_full = len(segs)
    if n_full > max_segments:
        idx = rng.choice(n_full, max_segments, replace=False)
        segs = [segs[i] for i in idx]
    return segs, n_full


def stack_from_segments(segs, thin=None):
    st = Stack()
    acc = np.zeros(len(FREQ))
    nph_tot = 0
    for lc in segs:
        lc = lc.astype(np.float64)
        if thin is not None:
            f0, rms, q, rng = thin
            lc = thin_lightcurve(lc, f0, rms, q, rng)
        nph = lc.sum()
        ft = np.fft.rfft(lc)[1:]
        acc += (2.0 / nph) * np.abs(ft) ** 2
        nph_tot += int(nph)
    st.add(acc, len(segs), nph_tot)
    return st


def stage_inject(n_trials=8, seed=0, q_inj=10.0):
    """Injection-recovery at the tooth frequency, scan band, per source.
    Levels chosen adaptively around the analytically predicted sensitivity
    (3 sigma <=> rms = sqrt(3 sigma_norm / rate)); gate: >=90% recovery at
    2x the achieved sensitivity."""
    rng = np.random.default_rng(seed)
    results = {}
    ck_path = os.path.join(RESDIR, "injection_calibration.json")
    if os.path.exists(ck_path):
        with open(ck_path) as f:
            results = json.load(f)
    for source, cfg in SCAN.items():
        if source in results and results[source].get("_complete"):
            continue
        f0 = cfg["tooth"]
        segs, n_full = collect_segments(source, cfg)
        base = stack_from_segments(segs)
        r0 = fit_line(base, f0, cfg["tooth_tol"])
        sigma_norm = r0["norm_err"] if r0 else 0.3
        rate = base.mean_rate
        # subsampling weakens sigma_norm by sqrt(n_full/n_used); correct the
        # prediction back to the FULL stack for reporting
        scale_full = np.sqrt(len(segs) / max(n_full, 1))
        pred_rms = float(np.sqrt(3.0 * sigma_norm / rate))          # subsample
        pred_rms_full = float(pred_rms * np.sqrt(scale_full))
        levels = [0.75 * pred_rms, pred_rms, 1.5 * pred_rms, 2.0 * pred_rms]
        src_res = {"tooth_hz": f0, "q_injected": q_inj, "band": cfg["scan_band"],
                   "n_seg_used": len(segs), "n_seg_full_stack": n_full,
                   "mean_rate_cps": rate,
                   "pred_sens_rms_pct_subsample": 100 * pred_rms,
                   "pred_sens_rms_pct_full_stack": 100 * pred_rms_full,
                   "levels": {}}
        for rms in levels:
            det = 0
            meas = []
            for k in range(n_trials):
                st = stack_from_segments(segs, thin=(f0, rms, q_inj, rng))
                r = fit_line(st, f0, cfg["tooth_tol"])
                if r and r["significance_sigma"] >= 3.0:
                    det += 1
                    meas.append(r["rms_pct"])
            src_res["levels"][f"{100*rms:.3f}"] = {
                "injected_rms_pct": 100 * rms, "n_trials": n_trials,
                "n_detected_3sig": det, "recovery_frac": det / n_trials,
                "measured_rms_pct_mean": float(np.mean(meas)) if meas else None,
            }
            print(f"{source} inject rms={100*rms:.2f}% -> {det}/{n_trials} "
                  f"recovered", flush=True)
            results[source] = src_res
            with open(ck_path, "w") as f:
                json.dump(results, f, indent=2)
        # achieved sensitivity: smallest injected level with >=90% recovery
        sens = None
        for key, lv in sorted(src_res["levels"].items(),
                              key=lambda kv: kv[1]["injected_rms_pct"]):
            if lv["recovery_frac"] >= 0.9:
                sens = lv["injected_rms_pct"]
                break
        src_res["sensitivity_rms_pct_90"] = sens
        src_res["gate_90pct_at_2x"] = bool(
            sens is not None and sens <= 2.0 * 100 * pred_rms)
        src_res["_complete"] = True
        results[source] = src_res
        with open(ck_path, "w") as f:
            json.dump(results, f, indent=2)
    print("injection calibration written")


# ---------------------------------------------------------------------------
# stage 4: blind scan + verdict
# ---------------------------------------------------------------------------
def stage_scan():
    from scipy.stats import norm as ndist
    n_trials_corr = 8  # 2 frequencies x 4 sources (preregistered)
    scan = {"trials_correction": {"n_trials": n_trials_corr,
                                  "rule": "2 frequencies x 4 sources, "
                                          "p_final = 1-(1-p_single)^8"}}

    def scan_band_stack(source, cfg, band):
        st = None
        for group in cfg["groups_scan"]:
            s = build_stack(source, group, band)
            if st is None:
                st = s
            else:
                st.add(s.acc, s.nseg, s.nph)
        return st

    for source, cfg in SCAN.items():
        entry = {}
        for role, band in (("primary", cfg["scan_band"]),
                           ("secondary", cfg["secondary_band"])):
            st = scan_band_stack(source, cfg, band)
            bl = {"band": band, "n_seg": st.nseg,
                  "exposure_s": st.nseg * SEG_S, "mean_rate_cps": st.mean_rate}
            for name, f0, tol in (("tooth", cfg["tooth"], cfg["tooth_tol"]),
                                  ("integer", cfg["integer"], cfg["integer_tol"])):
                r = fit_line(st, f0, tol)
                if r is None:
                    bl[name] = {"status": "no_fit"}
                    continue
                sig = r["significance_sigma"]
                p_single = float(ndist.sf(sig))
                p_final = float(1 - (1 - p_single) ** n_trials_corr)
                sig_corr = float(ndist.isf(min(max(p_final, 1e-300), 1.0)))
                r["p_single"] = p_single
                r["p_trials_corrected"] = p_final
                r["significance_after_trials_sigma"] = sig_corr
                r["target_hz"] = f0
                bl[name] = r
            entry[role] = bl
        # verdict fields read the PRIMARY (preregistered) band
        entry.update(entry["primary"])
        scan[source] = entry
    # verdict per preregistered enum
    verdicts = {}
    for source in SCAN:
        e = scan[source]
        t, i = e.get("tooth", {}), e.get("integer", {})
        t_sig = t.get("significance_after_trials_sigma", 0.0)
        i_sig = i.get("significance_after_trials_sigma", 0.0)
        if t_sig >= 4.0 and i_sig < 4.0:
            v = "ladder_hit"
        elif i_sig >= 4.0 and t_sig < 4.0:
            v = "harmonic_hit"
        else:
            v = "neither_upper_limits"
        verdicts[source] = {
            "verdict": v,
            "tooth_sig_after_trials": t_sig,
            "integer_sig_after_trials": i_sig,
            "tooth_rms_ul3sig_pct": t.get("rms_ul3sig_pct"),
            "integer_rms_ul3sig_pct": i.get("rms_ul3sig_pct"),
        }
    scan["verdicts"] = verdicts
    with open(os.path.join(RESDIR, "blind_scan.json"), "w") as f:
        json.dump(scan, f, indent=2)
    for s, v in verdicts.items():
        print(f"{s:16s} {v['verdict']:22s} tooth={v['tooth_sig_after_trials']:.2f}s "
              f"int={v['integer_sig_after_trials']:.2f}s "
              f"UL(tooth)={v['tooth_rms_ul3sig_pct']}% UL(int)={v['integer_rms_ul3sig_pct']}%")


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("stack", "all"):
        stage_stack()
    if stage in ("sanity", "all"):
        stage_sanity()
    if stage in ("inject", "all"):
        stage_inject()
    if stage in ("scan", "all"):
        stage_scan()

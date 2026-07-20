#!/usr/bin/env python3
"""Plots for the H3 archival scan: per-source stacked PDS around the tooth
and integer frequencies (primary band), full-range PDS, and the injection
recovery curves. Reads the cached stacks; writes PNGs to results/archival/."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pds_core import FREQ, Stack
from run_scan import RESDIR, SCAN, build_stack

OUT = RESDIR


def scan_stack(source, cfg, band):
    st = None
    for group in cfg["groups_scan"]:
        s = build_stack(source, group, band)
        if st is None:
            st = s
        else:
            st.add(s.acc, s.nseg, s.nph)
    return st


def rebin(P, nseg, df):
    nfac = max(1, int(round(df / (FREQ[1] - FREQ[0]))))
    n = len(FREQ) // nfac
    f = FREQ[:n * nfac].reshape(n, nfac).mean(axis=1)
    p = P[:n * nfac].reshape(n, nfac).mean(axis=1)
    e = p / np.sqrt(nfac * nseg)
    return f, p, e


def main():
    with open(os.path.join(RESDIR, "blind_scan.json")) as fh:
        scan = json.load(fh)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for ax, (source, cfg) in zip(axes.ravel(), SCAN.items()):
        st = scan_stack(source, cfg, cfg["scan_band"])
        P = st.leahy()
        f, p, e = rebin(P, st.nseg, df=4.0)
        m = (f > 50) & (f < 1200)
        ax.errorbar(f[m], p[m], yerr=e[m], fmt=".", ms=2, lw=0.5, alpha=0.6,
                    color="0.4")
        for f0, c, lbl in ((cfg["tooth"], "crimson", "tooth 1.5 nu_u"),
                           (cfg["integer"], "royalblue", "integer 4 nu_0"),
                           (SCAN[source].get("nu_u"), "green", "nu_u")):
            if f0:
                ax.axvline(f0, color=c, ls="--", lw=1, label=f"{lbl} {f0:g} Hz")
        v = scan.get(source, {}).get("primary", {})
        t = v.get("tooth", {})
        i = v.get("integer", {})
        ax.set_title(f"{source}  [{cfg['scan_band']}]  "
                     f"tooth {t.get('significance_sigma', 0):.1f}s / "
                     f"UL {t.get('rms_ul3sig_pct', float('nan')):.2f}%rms; "
                     f"int {i.get('significance_sigma', 0):.1f}s", fontsize=9)
        ax.set_xscale("log")
        ax.set_xlabel("frequency (Hz)")
        ax.set_ylabel("Leahy power")
        ax.legend(fontsize=7)
        lo = np.percentile(p[m], 1)
        hi = np.percentile(p[m], 99.8)
        ax.set_ylim(lo - 0.01, hi + 0.05)
    fig.suptitle("hfqpo-ladder H3 archival scan: stacked Leahy PDS "
                 "(preregistered primary bands)", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "pds_scan_overview.png"), dpi=150)
    print("wrote pds_scan_overview.png")

    # zoomed tooth/integer panels
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for ax, (source, cfg) in zip(axes.ravel(), SCAN.items()):
        st = scan_stack(source, cfg, cfg["scan_band"])
        P = st.leahy()
        df = max(1.0, cfg["tooth"] / 150.0)
        f, p, e = rebin(P, st.nseg, df=df)
        lo, hi = cfg["integer"] / 1.35, cfg["tooth"] * 1.35
        m = (f > lo) & (f < hi)
        ax.errorbar(f[m], p[m], yerr=e[m], fmt="o", ms=2.5, lw=0.7,
                    color="0.3", alpha=0.8)
        ax.axvspan(cfg["tooth"] - cfg["tooth_tol"], cfg["tooth"] + cfg["tooth_tol"],
                   color="crimson", alpha=0.15, label="tooth window")
        ax.axvspan(cfg["integer"] - cfg["integer_tol"],
                   cfg["integer"] + cfg["integer_tol"],
                   color="royalblue", alpha=0.15, label="integer window")
        ax.set_title(f"{source} zoom [{cfg['scan_band']}]", fontsize=9)
        ax.set_xlabel("frequency (Hz)")
        ax.set_ylabel("Leahy power")
        ax.legend(fontsize=7)
    fig.suptitle("tooth (1.5 nu_u) vs integer (4 nu_0) windows", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "pds_scan_zoom.png"), dpi=150)
    print("wrote pds_scan_zoom.png")

    # injection recovery curves
    inj_path = os.path.join(RESDIR, "injection_calibration.json")
    if os.path.exists(inj_path):
        with open(inj_path) as fh:
            inj = json.load(fh)
        fig, ax = plt.subplots(figsize=(7, 5))
        for source, d in inj.items():
            if "levels" not in d:
                continue
            xs, ys = [], []
            for lv in sorted(d["levels"].values(),
                             key=lambda z: z["injected_rms_pct"]):
                xs.append(lv["injected_rms_pct"])
                ys.append(lv["recovery_frac"])
            ax.plot(xs, ys, "o-", label=f"{source} ({d.get('tooth_hz')} Hz)")
        ax.axhline(0.9, color="k", ls=":", lw=1)
        ax.set_xlabel("injected rms (%)")
        ax.set_ylabel("recovery fraction (>=3 sigma at tooth)")
        q_inj = next((d.get("q_injected") for d in inj.values()
                      if isinstance(d, dict) and d.get("q_injected")), "?")
        ax.set_title(f"injection-recovery calibration (Q={q_inj:g} Lorentzian)")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(OUT, "injection_recovery.png"), dpi=150)
        print("wrote injection_recovery.png")


if __name__ == "__main__":
    main()

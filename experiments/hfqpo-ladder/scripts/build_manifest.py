#!/usr/bin/env python3
"""Freeze the ObsID manifest for the H3 archival RXTE PCA scan (hfqpo-ladder stage 2).

Run BEFORE any event data is downloaded. Maps published detection epochs
(MJD / interval tables from the papers cited per group) to archived ObsIDs via
the HEASARC xtemaster catalog dumps in data/archive/catalog/*.txt.

Output: data/archive/obsid_manifest.json  (the frozen manifest)
"""
import json
import os
import re
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CATDIR = os.path.join(ROOT, "data", "archive", "catalog")
OUT = os.path.join(ROOT, "data", "archive", "obsid_manifest.json")

MJD0 = datetime(1858, 11, 17)


def parse_catalog(fname):
    """Parse a w3query BatchDisplay dump -> list of dicts with obsid, mjd_start, duration."""
    rows = []
    with open(os.path.join(CATDIR, fname)) as f:
        for line in f:
            if not line.startswith("|") or line.startswith("|obsid") or line.startswith("+"):
                continue
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) < 10 or not parts[0]:
                continue
            if "archived" not in parts[2]:
                continue  # scheduled-only rows never reached the archive
            obsid, time_s, dur = parts[0], parts[8], parts[9]
            if not time_s:
                continue
            try:
                dt = datetime.strptime(time_s[:19], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            mjd = (dt - MJD0).total_seconds() / 86400.0
            try:
                duration = float(dur)
            except ValueError:
                duration = 0.0
            rows.append({"obsid": obsid, "mjd_start": mjd, "duration_s": duration})
    return rows


def find_obsids_for_mjd(cat, mjd, prefix=None, pad_days=0.35):
    """ObsIDs whose start lies within pad_days of the published (midpoint) MJD."""
    hits = []
    for r in cat:
        if prefix and not r["obsid"].startswith(prefix):
            continue
        end = r["mjd_start"] + max(r["duration_s"], 3000) / 86400.0
        if (r["mjd_start"] - pad_days) <= mjd <= (end + pad_days):
            hits.append((abs(r["mjd_start"] - mjd), r["obsid"]))
    hits.sort()
    return [h[1] for h in hits]


j1655 = parse_catalog("GRO_J1655-40.txt")
j1550 = parse_catalog("XTE_J1550-564.txt")
grs = parse_catalog("GRS_1915_105.txt")
# wide-radius query: program 80146 pointed at XTE_J1746-319, 19' off the
# nominal H1743-322 position, so the narrow query missed most rows
h1743 = parse_catalog("H1743-322_wide.txt")

manifest = {
    "comment": (
        "Frozen ObsID manifest for the preregistered H3 archival scan "
        "(hypotheses/hfqpo_v1.yaml, archival_design). Created BEFORE event-data "
        "download; every group cites the published source of its selection."
    ),
    "frozen_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "prereg_deviations": [
        "H1743-322: prereg YAML says ObsIDs 80138-06-*; the 111-interval / 130-observation "
        "program of Remillard et al. 2006 (ApJ 637, 1002, Sec. 2) is actually program ID "
        "80146. The manifest uses 80146-01-* (the published selection).",
        "Mapping correction after first download pass (no scope change): xtemaster rows "
        "with status != archived are excluded, so the Belloni+2012 MJD 50394.884 epoch of "
        "GRO J1655-40 maps to 10255-01-20-00 (10255-01-19-00 was scheduled but never "
        "archived, HTTP 404). H1743-322 interval obsid 80146-01-57-01 exists in the "
        "archive only as its -01G variant (fetch script tries the G suffix on 404).",
        "GRS 1915+105: the 113/168 Hz pair epochs were never published with an ObsID list "
        "(Remillard et al. 2003 is a BAAS abstract; RM06 cites it without a table). Proxy "
        "selection: the published HFQPO-pair detection epochs with ObsID lists - Strohmayer "
        "2001b Table 1 (41/69 Hz, gamma class) and Belloni & Altamirano 2013 (34/68 Hz, "
        "delta class, 80701-01-28-00/01/02) plus the two strongest 67-Hz epochs of BA12 "
        "(10408-01-04-00/-06-00, Morgan et al. 1997). The 252-Hz tooth scan on this proxy "
        "stack is therefore a WEAKER test than preregistered (different state than the "
        "168/113 stack); reported as such.",
    ],
    "sources": {},
}

# --------------------------------------------------------------------------
# GRO J1655-40  (nu_u 441 -> tooth 661.5 Hz, integer line 588 Hz)
# --------------------------------------------------------------------------
b1 = ["10255-01-06-01", "10255-01-07-00", "10255-01-17-00"]
b2 = ["10255-01-09-00", "10255-01-10-00"]
# Belloni+2012 Tab.2 total-band ~300 Hz detections (MJD): map to ObsIDs
b2012_mjd_T = [50296.311, 50301.665, 50324.380, 50394.884]
extra = []
for m in b2012_mjd_T:
    ids = find_obsids_for_mjd(j1655, m, prefix="10255-01")
    if ids:
        extra.append(ids[0])
extra = sorted(set(extra) - set(b1) - set(b2))
manifest["sources"]["GRO_J1655-40"] = {
    "nu_l": 298.0, "nu_u": 441.0,
    "tooth_hz": 661.5, "tooth_sigma_hz": 3.0, "harmonic_4nu0_hz": 588.0,
    "sanity_pair": [298.0, 441.0],
    "sanity_note": "B1 stack must show ~441 Hz (hard band, ~4.5% rms) and ~298 Hz; "
                   "B2/hard stack ~450 Hz (Strohmayer 2001, Motta et al. 2014a).",
    "band_note": "450 Hz QPO is hard-band only (13-27 keV, E_1us_4A_50_8s); "
                 "~300 Hz strongest in total band.",
    "groups": {
        "B1_triplet": {
            "obsids": b1,
            "provenance": "Motta et al. 2014a (MNRAS 437, 2554) Table 2 sample B1: "
                          "type-C 17.3 Hz + 298 Hz + 441 Hz simultaneous.",
        },
        "B2_450Hz": {
            "obsids": b2,
            "provenance": "Motta et al. 2014a Table 2 sample B2 (451/446 Hz hard band); "
                          "= Strohmayer 2001 / Belloni et al. 2012 MJD 50330.254 & 50335.913.",
        },
        "T300_epochs": {
            "obsids": extra,
            "provenance": "Belloni et al. 2012 (MNRAS 426, 1701) Table 2 total-band "
                          "273-313 Hz detections at MJD 50296.311, 50301.665, 50324.380, "
                          "50394.884, mapped to 10255-01-* via xtemaster.",
        },
    },
}

# --------------------------------------------------------------------------
# XTE J1550-564  (nu_u 276 -> tooth 414 Hz, integer line 368 Hz)
# --------------------------------------------------------------------------
b2012_1550 = {
    "hard_280": [51115.281, 51241.802, 51242.507, 51255.158, 51258.497, 51259.253],
    "total_180": [51076.000, 51108.076, 51245.354, 51247.979],
    "outburst2000_270": [51664.409, 51664.637, 51665.406, 51668.829],
}
groups_1550 = {}
for gname, mjds in b2012_1550.items():
    ids = []
    for m in mjds:
        found = find_obsids_for_mjd(j1550, m)
        if found:
            ids.append(found[0])
        else:
            ids.append(f"UNRESOLVED_MJD_{m}")
    groups_1550[gname] = {
        "obsids": sorted(set(i for i in ids if not i.startswith("UNRESOLVED"))),
        "unresolved": [i for i in ids if i.startswith("UNRESOLVED")],
        "provenance": "Belloni et al. 2012 (MNRAS 426, 1701) Table 2 XTE J1550-564 "
                      f"detections, group {gname} (MJDs {mjds}); SIMS/HSS states "
                      "(type-A/B LFQPO per Remillard et al. 2002, ApJ 580, 1030).",
    }
manifest["sources"]["XTE_J1550-564"] = {
    "nu_l": 184.0, "nu_u": 276.0,
    "tooth_hz": 414.0, "tooth_sigma_hz": 4.5, "harmonic_4nu0_hz": 368.0,
    "sanity_pair": [184.0, 276.0],
    "sanity_note": "hard-band stack of hard_280 group must show ~276-284 Hz (3.6-5.2% rms); "
                   "total-band stack of total_180 group ~180-185 Hz (~1-1.7% rms).",
    "band_note": "~180 Hz detections in total band, ~280 Hz in hard band (Belloni+2012).",
    "groups": groups_1550,
}

# --------------------------------------------------------------------------
# GRS 1915+105  (nu_u 168 -> tooth 252 Hz, integer line 224 Hz)  [proxy states]
# --------------------------------------------------------------------------
manifest["sources"]["GRS_1915+105"] = {
    "nu_l": 113.0, "nu_u": 168.0,
    "tooth_hz": 252.0, "tooth_sigma_hz": 4.5, "harmonic_4nu0_hz": 224.0,
    "sanity_pair": [41.5, 69.2],
    "sanity_note": "gamma-class stack must reproduce the Strohmayer 2001b 41/69 Hz pair "
                   "(13-27 keV; 2.4%/1.9% rms); delta-class stack the 34/68 Hz pair "
                   "(Belloni & Altamirano 2013; 68 Hz at 24 sigma).",
    "band_note": "41 Hz only >13 keV. 168/113 epochs unpublished at ObsID level "
                 "(see prereg_deviations) - tooth scan on proxy states only.",
    "groups": {
        "gamma_1997_41_69": {
            "obsids": ["20402-01-38-00", "20402-01-39-00", "20402-01-39-02",
                        "20402-01-55-00", "20402-01-56-00"],
            "provenance": "Strohmayer 2001b (ApJ 554, L169) Table 1: 67-69 Hz QPO + "
                          "41 Hz pair, gamma-class.",
        },
        "gamma_1996_67": {
            "obsids": ["10408-01-04-00", "10408-01-06-00"],
            "provenance": "Morgan, Remillard & Greiner 1997; the two >10-sigma 67-Hz "
                          "epochs of Belloni & Altamirano 2012 (Obs #3, #5).",
        },
        "delta_2003_34_68": {
            "obsids": ["80701-01-28-00", "80701-01-28-01", "80701-01-28-02"],
            "provenance": "Belloni & Altamirano 2013 (MNRAS 432, 10): 34+68 Hz integer "
                          "pair, 2003 Oct 21, delta-class.",
        },
    },
}

# --------------------------------------------------------------------------
# H1743-322  (nu_u 242 -> tooth 363 Hz, integer line 322.7 Hz)
# --------------------------------------------------------------------------
# Remillard et al. 2006 (ApJ 637, 1002) Table 1: 111 intervals of program 80146.
# 'q' intervals split at 430 c/s/PCU (7-35 keV): >430 -> 166 Hz group (9),
# <430 -> 242 Hz group (26).
q_high = [(52750.31, 608.2), (52750.81, 495.2), (52751.32, 882.2), (52752.97, 575.7),
          (52765.87, 1083.3), (52786.35, 597.7), (52794.56, 636.5), (52798.54, 675.5),
          (52785.48, 432.0)]
q_low = [(52751.09, 384.3), (52751.71, 365.6), (52751.99, 326.9), (52755.96, 414.6),
         (52756.23, 364.1), (52756.71, 204.2), (52763.10, 300.3), (52763.62, 390.0),
         (52764.91, 392.5), (52784.57, 409.6), (52788.51, 240.0), (52789.26, 327.2),
         (52790.24, 296.6), (52791.63, 272.1), (52792.39, 296.6), (52793.61, 286.8),
         (52795.38, 236.5), (52796.27, 307.2), (52797.58, 325.6), (52799.46, 233.7),
         (52800.73, 215.4), (52801.91, 260.7), (52802.96, 272.1), (52803.57, 259.6),
         (52804.62, 298.8), (52805.47, 278.3)]


# Global assignment: each 80146-01 ObsID goes to the SINGLE nearest interval
# midpoint (R06 intervals span <=0.48 d, 1-2 observations each). This prevents
# the same ObsID from entering both flux groups.
all_intervals = [(m, "hi") for m, _ in q_high] + [(m, "lo") for m, _ in q_low]
ids_hi, ids_lo = [], []
for r in h1743:
    if not r["obsid"].startswith("80146-01"):
        continue
    mid = r["mjd_start"] + max(r["duration_s"], 3000) / 2.0 / 86400.0
    d, grp = min(((abs(mid - m), g) for m, g in all_intervals), key=lambda x: x[0])
    if d <= 0.25:
        (ids_hi if grp == "hi" else ids_lo).append(r["obsid"])
ids_hi, ids_lo = sorted(set(ids_hi)), sorted(set(ids_lo))
un_hi, un_lo = [], []
manifest["sources"]["H1743-322"] = {
    "nu_l": 166.0, "nu_u": 242.0,
    "tooth_hz": 363.0, "tooth_sigma_hz": 4.5, "harmonic_4nu0_hz": 322.6667,
    "sanity_pair": [166.0, 242.0],
    "sanity_note": "q-low stack (7-35 keV) must show ~242 Hz (1.1% rms, 6 sigma in R06); "
                   "q-high stack (2-35 keV) ~166 Hz (0.6% rms, 4.1 sigma).",
    "band_note": "242 Hz found at 7-35 keV, 166 Hz at 2-35 keV (Remillard et al. 2006).",
    "groups": {
        "q_high_166": {
            "obsids": ids_hi, "unresolved_mjd": un_hi,
            "provenance": "Remillard et al. 2006 Table 1: the 9 'q' intervals with "
                          "7-35 keV rate > 430 c/s/PCU (166 Hz group).",
        },
        "q_low_242": {
            "obsids": ids_lo, "unresolved_mjd": un_lo,
            "provenance": "Remillard et al. 2006 Table 1: the 26 'q' intervals with "
                          "7-35 keV rate < 430 c/s/PCU (242 Hz group).",
        },
    },
}

n_total = sum(len(g.get("obsids", []))
              for s in manifest["sources"].values() for g in s["groups"].values())
manifest["n_obsids_total"] = n_total

with open(OUT, "w") as f:
    json.dump(manifest, f, indent=2)
print(f"manifest frozen: {OUT}")
print(f"total obsids: {n_total}")
for sname, s in manifest["sources"].items():
    for gname, g in s["groups"].items():
        print(f"  {sname:16s} {gname:22s} n={len(g.get('obsids', [])):3d} "
              f"unresolved={g.get('unresolved', g.get('unresolved_mjd', []))}")

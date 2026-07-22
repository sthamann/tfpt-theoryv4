# extension-nicer-laxpc — third-tooth search on non-RXTE archives (NICER / LAXPC)

> **Firewall (inherited unchanged from `../README.md`):** TFPT's 3/2 is a
> relaxation-ladder step, **not** a two-oscillator frequency ratio; TFPT derives no
> HFQPO production mechanism. Only the ladder discriminator (geometric tooth at
> `(3/2) × anchor` vs integer harmonic lines) carries weight, and even a ladder hit
> would be `[C]`-tier. Nothing here is `[E]`; this is a **search target, not a claim**.
> The parent RXTE stage-2 well-powered null (2026-07-20) stands and is **not re-opened**.

## What this extension is

The parent experiment ran the preregistered H3 archival scan on RXTE PCA data
(4 sources, 77 ObsIDs, verdict: well-powered `null`). This extension applies the
**same frozen kernel and the same decision rule** to new public archives — no
re-tuning of the prediction. Everything was preregistered in
`hypotheses/hfqpo_ext_v1.yaml` (frozen 2026-07-22 **before** any photon download):
archive selection rationale, targets, tolerances, fit windows, budget gates,
triage rule, trials correction, verdict mapping.

**Single-QPO extension rule** (frozen in the prereg): for a source with a published
single HFQPO (no 3:2 pair), the anchor is that published centroid; the ladder
reading predicts the next tooth at `(3/2) × anchor` and forbids integer lines; the
harmonic alternative predicts `2 × anchor`. A single-QPO test is a priori **weaker**
than a pair test (no 3:2 pair anchors the ladder phase) and is never pooled with
the parent pair results.

## Archive feasibility (metadata-only, before the freeze)

| archive | verdict | basis |
|---|---|---|
| **NICER / MAXI J1820+070** | **selected** | published in-instrument anchor: ATel #11951 (Zhang et al. 2018) — 55.12 ± 0.06 Hz HFQPO, FWHM 2.0 Hz, ~1% rms, ObsIDs 1200120107…120, weak ~110 Hz second harmonic reported; public scriptable HEASARC FTP |
| AstroSat/LAXPC | **infrastructure_blocked** | scientifically the strongest channel (published ~70 Hz HFQPOs of GRS 1915+105: Belloni+2019, Sreehari+2020, Majumder+2022) but the ISSDC archive (astrobrowse/PRADAN) is login-gated; no anonymous or scriptable path (probed 2026-07-22) |
| NICER / GRS 1915+105 | not_selected | no published NICER detection of the 67–70 Hz line; hard-band-dominant feature vs heavily absorbed soft band; a scan without a published anchor cannot pass the sanity-gate design |
| NICER / MAXI J1535−571 | not_selected | no published HFQPO at all → no frozen tooth target |
| NuSTAR | not_selected | ~2.5 ms dead time caps effective rates near ~400 c/s/module; even with Bachetti+2015 FPMA/FPMB co-spectra the sensitivity is an order of magnitude below NICER on the same source |

## Data (frozen manifest, budget-gated)

`data/manifest_ext.json` — frozen before download; sizes via HTTP HEAD only. Pool =
14 ObsIDs of the ATel QPO epoch (56.3 GB total). Triage rule (frozen): discovery
ObsID 1200120107 mandatory, then ascending file size, hard stop before 15.0 GB.
Selected: **1200120107, 1200120113, 1200120114, 1200120115, 1200120117, 1200120119**
= **13.22 GB** downloaded (log: `data/download_log_ext.json`, 0 errors, gate never
tripped). Files: merged-MPU cleaned events `ni*_0mpu7_cl.evt.gz` from
`heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2018_0{3,4}/`.

## Method

Identical machinery to the parent (`../scripts/pds_core.py` imported directly):
Leahy PDS from 16-s segments at dt = 1/4096 s, stacked per band; Lorentzian line
fit with `significance = norm/σ_norm`; 3σ rms upper limits over the fixed-Q grid;
piecewise-coherent QPO injection by binomial thinning (Q = 10). New code is only
the NICER loader (TIME/PI + GTIs, PI band cut) and an explicit-window variant of
the line fit — the parent's geometric fit window (×/1.6) would have put the strong
55 Hz anchor inside the 82.7 Hz tooth window; the frozen windows
(`fit_windows_hz` in the YAML) keep the anchor, tooth and integer regions disjoint.
Bands: primary `tot` = PI 30–1000 (0.3–10 keV, the anchor's detection band),
secondary `hard` = PI 300–1200 (3–12 keV). Barycentring skipped (≤ 0.011 Hz at
110 Hz — negligible); NICER dead time < 1% at ~2 × 10⁴ c/s (no co-spectrum needed).
Trials correction: n = 4 (2 frequencies × 1 source × 2 bands); detection = 4σ
after trials.

## Results (executed 2026-07-22; `results/`)

**Stack:** 2013 segments × 16 s = 32.2 ks at 19 050 c/s (primary band).

**Sanity gate PASS:** the published anchor is reproduced in the stack —
55.03 Hz, 0.94% rms, 3.8σ, Q ≈ 25 (published: 55.12 Hz, ~1% rms). Hard band
shows the line at 0.89% rms but only 1.5σ (1.4 kc/s rate; secondary, non-gating).

**Injection calibration PASS:** ≥ 90% recovery (8/8) at 0.93% rms injected at the
tooth frequency; analytic prediction 0.46%; gate `sens ≤ 2× prediction` holds.

**Blind scan (primary band):**

| target | freq (Hz) | σ single-trial | σ after trials | 3σ rms UL |
|---|---|---|---|---|
| tooth `(3/2)×55.12` | 82.68 | 0.69 | −0.46 | **0.75%** |
| integer `2×55.12` | 110.24 | 4.15 | **3.82** | 1.45% (fit rms 0.59%) |

- **No tooth.** The 3σ upper limit (0.75% rms) is below the strength of the
  detected 55 Hz anchor line (0.94% rms) in the same stack — a tooth as strong as
  the known QPO is excluded.
- The integer line at ~110.6 Hz comes out at 3.82σ after trials — **below the
  preregistered 4σ threshold**, so the decision rule returns
  `neither_upper_limits`, not `harmonic_hit`. It is reported as a sub-threshold
  excess consistent with the weak second harmonic already noted in ATel #11951.
  Direction-wise it again favours the integer-harmonic (GR/resonance) side, like
  the parent's anti-kernel record (92 = 184/2, 34/68 Hz) — but it is **not** a
  detection under the frozen rule.

## Verdicts (extension enum, per archive/source)

| channel | verdict |
|---|---|
| NICER / MAXI J1820+070 (tooth) | **`null_with_sensitivity`** (90%-recovery sensitivity 0.93% rms ≤ anchor line 0.94% rms; injection gate PASS) |
| AstroSat/LAXPC | **`infrastructure_blocked`** |
| NICER / GRS 1915+105, MAXI J1535−571, NuSTAR | not_selected (see feasibility table) |
| **Overall** | the parent RXTE `null` stands; this extension adds one well-powered single-QPO null on an independent instrument and source |

**Recommendation:** the RXTE + NICER nulls now cover five sources on two
instruments with sub-percent to few-percent rms limits — the tooth channel should
be put **dormant**. The only materially stronger remaining probe is AstroSat/LAXPC
(GRS 1915+105 ~70 Hz states); it stays blocked until someone with ISSDC credentials
fetches the Level-2 event files. If those ever land in `data/`, the pipeline here
runs unchanged apart from a LAXPC loader.

## Reproduce

```bash
. ../../tfpt-discovery/.venv/bin/activate      # shared venv (numpy/scipy/astropy)
python scripts/build_manifest_ext.py           # freeze manifest (already frozen)
python scripts/fetch_nicer.py                  # download (15 GB abort gate, idempotent)
python scripts/run_scan_ext.py stack           # segment caches + stack report
python scripts/run_scan_ext.py sanity          # 55 Hz anchor gate (must PASS)
python scripts/run_scan_ext.py inject          # injection-recovery calibration (must PASS)
python scripts/run_scan_ext.py scan            # blind tooth+integer scan + verdicts
python scripts/write_summary_ext.py            # combined results_ext.json
```

## Layout

```
hypotheses/hfqpo_ext_v1.yaml   # preregistered protocol (frozen before download)
data/manifest_ext.json         # frozen ObsID manifest (HEAD sizes, triage)
data/download_log_ext.json     # download log (13.22 GB, 0 errors)
data/raw/<obsid>/              # NICER cleaned event files (fetched, not committed)
scripts/build_manifest_ext.py  # manifest freeze (metadata only)
scripts/fetch_nicer.py         # parallel-range downloader, 15 GB abort gate
scripts/nicer_core.py          # NICER loader + explicit-window line fit
scripts/run_scan_ext.py        # stack | sanity | inject | scan stages
scripts/write_summary_ext.py   # combined summary -> results/results_ext.json
results/results_ext.json       # deterministic summary (scorecard source, later step)
results/{stack_report,sanity_gate,injection_calibration,blind_scan}_ext.json
results/cache/                 # per-obsid per-band 16-s segment caches (npz)
```

**Not done here (by design):** no scorecard row, no website/paper/ledger edits —
that is a separate integration step. The parent `../` RXTE results, manifests and
scripts are untouched.

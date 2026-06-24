# Data provenance

The `data/` directory is **gitignored** (`data/*` in the repo-root and local
`.gitignore`); **only this `README.md` and the small derived `frb01_subband_toas.csv`
are committed.** Every downloaded/large table below is gitignored and re-obtained from
the cited source (mostly `python scripts/fetch_data.py`). Raw pulse archives live in
`../new-data/` (also gitignored; FRB.01 source material).

**Blinkverse + ScienceDB pol:** `python scripts/fetch_user_data.py` — Blinkverse via
public REST export; ScienceDB pol catalog needs a free login drop-in (or
`SCIENCEDB_COOKIE` env var).

## Fetchable tables (`scripts/fetch_data.py`)

| File | Dataset | N | Source |
|---|---|---|---|
| `chime_catalog1.tsv` | CHIME/FRB Catalogue 1 | 600 | CHIME/FRB 2021, ApJS 257, 59 (VizieR `J/ApJS/257/59`) |
| `frb20121102_fast_li2021_1652.tsv` | FRB 20121102A, FAST (per-burst energy) | 1652 | Li et al. 2021, Nature 598, 267 (VizieR `J/other/Nat/598.267`) |
| `frb20121102_aggarwal2021.tsv` | FRB 20121102A bursts | 144 | Aggarwal et al. 2021, ApJ 922, 115 (VizieR `J/ApJ/922/115`) |
| `frb_dmz_adb84d_table4.txt` | localized FRBs, full DM budget | 36 | ApJ `10.3847/1538-4357/adb84d` |
| `frb_dmz_adeb72_table1.txt` | Sharma+2024 host sample | 117 | ApJ `10.3847/1538-4357/adeb72` |
| `frb_pol_pandhi2024_table1.txt` | CHIME non-repeater RM | 118 | Pandhi et al. 2024, ApJ 968, 50 |

## User-supplied tables

- `FAST_FRB20240114A_pol_catalog*.csv` — FRB 20240114A FAST polarimetry, 6134
  bursts (`MJD_topo, RM, DM, Weff, S/N, DOL, DOC, PA_mean`). Wang et al. 2026
  (arXiv:2603.20663; ScienceDB `10.57760/sciencedb.Fastro.00040`). `..._v5` is
  preferred. Drives **FRB.04** + parts of FRB.06/FRB.08.
- `blinkverse_bursts.csv` — Blinkverse multi-source DB (~8808 bursts for 4 repeaters
  via `fetch_user_data.py`; full DB ~22k). Per-burst `energy, fluence, rm_qufit/rm_syn,
  polar_l/polar_c, width, mjd, source`. No PA angles (pol fractions only).

## Derived

- `frb01_subband_toas.csv` — per-burst, per-sub-band arrival times
  (`burst_id, source, freq_mhz, toa_s, toa_err_s, snr`) extracted from the raw
  archives. Small + committed so **FRB.01 is reproducible without the ~14 GB raw**.
  Currently **152 bursts across 2 sources** (119 usable for the drift-corrected fit):
  - 2 bright FRB 20121102A `.calibP` bursts (8 + 10 sub-bands) — `extract_subband_toas.py`;
  - 150 FRB 20201124A bursts streamed from `FRB20201124A.tar.gz` — `extract_ar_toas.py`.

## Raw pulse archives (`../new-data/`) — read via astropy (no PSRCHIVE)

PSRCHIVE `.calibP` / `.ar` and PSRFITS `.fits` single-burst archives are PSRFITS, so
`src/frb_tfpt/psrfits.py` reads them with astropy (calibrated Stokes; accepts a path
**or an in-memory file object**). The bright FRB 20121102A bursts (`burst1.calibP`,
`20191003_1032.calibP`, S/N 80–90, 1–1.5 GHz, IQUV) feed **FRB.01**. Other raw items
(provenance / further FRB.01 material): SIGPROC `.fil` (FRB 20190520B; 1-bit, only
~5σ incoherent → unused), `.TSDb4` + `PulsarData.txt` (calibration pulsars).

**Large burst archives** (gitignored; streamed member-by-member, never unpacked):
- `FRB20201124A.tar.gz` (892 MB) — **1863 `.ar`** PSRCHIVE waterfalls (FAST, 512 ch,
  1000–1500 MHz, Stokes-I). `extract_ar_toas.py` keeps 150 bright bursts → FRB.01.
- `FRB20240114A_Morphology_Public_Dataset…zip` (9 GB) — **2729 `.ar`** + PNG plots
  (FAST, 4096 ch, 192 phase bins). A curated **narrow-band / drifting** morphology
  set: yields **0** bursts with ≥5 broadband sub-bands, so it does **not** feed
  FRB.01 (honest data limit — it is built for drift-rate/morphology, not timing).
- `FRB20121102A_new_bursts.zip` (4 GB) — **3844 burst _PDF plots_** (not raw arrays);
  filenames encode per-burst MJD/ToA/DM/box-width. Not usable for sub-band timing.

## `FRB_Catalog2_Clustering_UMAP.csv` — CHIME/FRB Catalog 2 morphology embedding

4527 bursts with `tns_name, repeater_name, group, embedding_x, embedding_y` (UMAP
morphology clustering). Population/morphology context only — no per-burst
energy/RM → no direct kernel test; not wired into the pipeline.

## Data-acquisition note

The FRB 20240114A polarisation catalog and most FAST burst archives are ScienceDB
downloads (free login). The Blinkverse export is from blinkverse.top. The raw
`.calibP/.fits` archives are read without PSRCHIVE (they are PSRFITS → astropy).

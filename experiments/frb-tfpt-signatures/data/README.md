# Data provenance

Two **real, public** FRB datasets, both fetched from the CDS VizieR service via
`scripts/fetch_data.py`. They are committed here for reproducibility; re-fetch
any time with `python scripts/fetch_data.py`.

## `chime_catalog1.tsv` — CHIME/FRB Catalogue 1

- 600 bursts (the first large, uniform public FRB sample).
- Source: **CHIME/FRB Collaboration et al. 2021, ApJS 257, 59**
  (VizieR `J/ApJS/257/59`, table2).
- Columns used: `Name`, `RpName` (repeater id), `Fluence` (Jy ms, **lower
  limit**), `Flux`, `MJD400` (arrival), `Fpk`/`b_Freq`/`B_Freq` (frequency),
  `DMfitb`, `Nsb` (sub-burst index).
- Caveat: CHIME fluences are *lower limits* (unknown beam position) and most
  sources have no redshift, so the absolute energetics are coarse. This
  catalogue's strength is breadth (repeaters, DM, sub-burst drift), not energy.

## `frb20121102_aggarwal2021.tsv` — FRB 20121102A burst sample

- 144 burst components of the repeater **FRB 20121102A**, all from a single
  source in a single epoch (MJD 57644–57645), so the component fluence `S`
  is a clean, distance-independent **energy proxy** — the ideal input for the
  per-source energy-cascade test.
- Source: **Aggarwal et al. 2021, ApJ 922, 115** (VizieR `J/ApJ/922/115`,
  table5).
- Columns used: `S` (component fluence, Jy ms), `MJD`, `muf` (mean spectral
  frequency), `DM`.

## `frb_dmz_adb84d_table4.txt` — localized FRBs with full DM budget

- 36 localized FRBs with **measured spectroscopic host redshift** and a full
  DM decomposition: `DM_obs`, `DM_MW(disk; NE2001)`, `DM_MW(halo)`, `DM_IGM`,
  `DM_host^s` (source frame). Used by the **FRB.05 baryon (Ω_b) test**: the
  cosmic DM is `DM_obs − DM_MW − DM_host_obs`.
- Source: ApJ paper, DOI `10.3847/1538-4357/adb84d`, Table A1 (IOPscience
  machine-readable supplement).

## `frb_dmz_adeb72_table1.txt` — Sharma et al. 2024 host sample

- 117 localized FRBs with host redshift, `DM`, and `DM_exc = DM − DM_MW`
  (NE2001). Larger sample, no per-FRB host model (a constant rest-frame host
  prior is subtracted in `load_dmz_sharma`). Cross-check for FRB.05.
- Source: Sharma et al. 2024, DOI `10.3847/1538-4357/adeb72`, Table 1.

## `frb_pol_pandhi2024_table1.txt` — CHIME non-repeater polarimetry

- 118 CHIME non-repeating FRBs with `RM_obs`, `RM_MW`, `L/I`, depolarisation.
  Source: Pandhi et al. 2024, ApJ 968, 50 (DOI `10.3847/1538-4357/ad40aa`),
  Table 1. Used for the (data-limited) **FRB.04 polarisation** axis.
- Limitation: these are *non-repeaters* (one burst each), so the strong μ4/D4
  test `spec(T_PA) = {1,(2/3)⁶,(1/3)⁶}` (which needs a per-repeater PA/RM
  *sequence*) cannot be run. A repeater RM/PA time series (e.g. FRB 20201124A,
  FRB 20190520B) would activate `rm_staircase` / `pa_angle_classes` directly.

## `frb20121102_fast_li2021_1652.tsv` — FAST 1652-burst FRB 20121102A

- 1652 bursts of FRB 20121102A from a single FAST campaign, **with per-burst
  energy** (erg), plus MJD, DM, width, bandwidth, peak flux, fluence.
- Source: **Li et al. 2021, Nature 598, 267** (VizieR `J/other/Nat/598.267`,
  table s1). Same source ⇒ energy is distance-independent.
- Enables the real **FRB.02** session-aware echo test and the energy spacing
  ladder (the 144-burst Aggarwal set was too thin).

## `FAST_FRB20240114A_pol_catalog*.csv` — FAST polarimetry of FRB 20240114A

- **6134 bursts** of the hyper-active repeater FRB 20240114A with per-burst
  `MJD_topo, RM, DM, Weff, Bandwidth, S/N, DOL (=L/I), DOC (=V/I), PA_mean`,
  spanning 488 days / 95 nights; RM evolves smoothly from ~330 to ~230 rad/m²
  (span ~213). **Activates FRB.04** (PA/RM Markov spectrum) and `rm_staircase`.
- Source: **Wang et al. 2026, FAST Polarization Catalog of FRB 20240114A**
  (arXiv:2603.20663; ScienceDB DOI `10.57760/sciencedb.Fastro.00040`,
  CC BY-NC-ND). User-supplied (ScienceDB requires a free login, see audit below).
- Three files were provided; `load_fast_20240114A_pol` prefers
  `..._v5.csv` (cleanest header + full-precision MJD), then the base CSV, then
  `..._v4.csv` (has an extra index column).

## Drop-in repeater catalogue still pending

- `frb20240619D_wideband.tsv` — **FRB 20240619D** wideband burst table
  (1539 bursts; arXiv:2505.08372). Needs columns `MJD, fluence, DM, RM,
  freq_low/high`. Drop in `data/` (aliases in `data_io._COL_ALIASES`) to activate
  the RM-memory / session-decay / frequency-window stress tests.

## Data-acquisition audit (2026-06)

The **FAST FRB 20240114A polarisation catalog** is on ScienceDB and **login-walled**
for anonymous download (now resolved: user supplied the CSVs after a free login).
For the record, the blocked anonymous routes (all verified):

- ScienceDB DOI `10.57760/sciencedb.Fastro.00040`, dataset id
  `3fe21485a0b84f328f63a5ca8807b3e5` (6 files, 3.31 MB).
- arXiv source `2603.20663` = LaTeX + figures only, no CSV; DataCite metadata has
  no `contentUrl`; Croissant / JSON-LD exports are client-side JS (return the SPA
  shell); the ScienceDB file-tree API returns `User Not Login` **even from the
  page's own origin with cookies**; the open `download.scidb.cn/download?fileId=…`
  endpoint works but the 6 file ids are not exposed anonymously.
- Path used: a free ScienceDB account → download the CSVs. (Authors are also
  reachable: wangpei@nao.cas.cn, gaohe@bnu.edu.cn, zhuww@nao.cas.cn.)

**Non-login alternatives found but insufficient** (not bundled): `SukiYume/RMS`
(FRB 20201124A RM, ~23+9 bursts, single-epoch, RM≈const, no MJD); FRB 20190520B
(Anna-Thomas; code-only on Zenodo, RM table in paywalled Science supplement);
FRB 20240619D (journal/CDS supplement, absent from the arXiv source).

## Curated (in code, with citations): periodic-repeater activity windows

`activity_windows.PERIODIC_REPEATERS` encodes the only two robustly periodic
repeaters with published periods + activity-window widths (FRB 20180916B,
CHIME/FRB 2020; FRB 20121102A, Rajwade et al. 2020). Add rows as new periodic
repeaters are confirmed.

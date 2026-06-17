# Data — GW ringdown echo

The `data/` directory is **gitignored** (`data/*`); only this `README.md` is tracked.
The data file is **downloaded**, not committed:

## `gwtc_events.csv` — gitignored, re-downloadable

- **What:** the real LVK catalogue (391 events, GWTC-1 … **GWTC-5.0**; 390 canonical
  confident events), columns `name, catalog, snr, m1, m2, mtot, mfinal, z` (catalogue-level
  summary parameters only).
- **Where to get it:** `python scripts/fetch_catalog.py`, which pulls
  <https://gwosc.org/eventapi/json/GWTC/> (the cumulative GWTC event API). ~20 kB.
- **Why gitignored:** re-downloadable in seconds; the 390-vs-391 reconciliation is in
  [`../event_count_audit.md`](../event_count_audit.md).

## `strain/` — real GWOSC strain (32 s HDF5), provenance JSON tracked, blobs gitignored

- **What:** per-event 32 s, 4 kHz strain HDF5 for the **Stage-1 real-data echo search**
  (`real_echo_search.py`), one file per detector (~1 MB each).
- **Where to get it:** `python scripts/fetch_strain.py GW150914 GW190521`, which resolves the
  per-detector URLs via the GWOSC event API (32 s tutorial files for O1 events) and downloads
  with `urllib` + reads with `h5py` (no gwpy). It writes `strain/<event>_meta.json` (GPS, final
  mass, file list).
- **Tracked vs ignored:** the tiny `*_meta.json` provenance files **are committed**; the
  `*.hdf5` blobs are **gitignored** (re-downloadable in seconds).
- **Used by:** `tfpt-gw realdata --events GW150914 GW190521` (PSD-whitened matched filter +
  Kerr-QNM subtraction + off-source background + free-ratio control).

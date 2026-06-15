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

The full echo search additionally needs GWOSC **strain** (~GB/event) — not downloaded here.

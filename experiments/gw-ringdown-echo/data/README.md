# Data — GW ringdown echo

`gwtc_events.csv` is the **real LVK catalogue**, downloaded from the GWOSC event API
by `scripts/fetch_catalog.py`:

- source: <https://gwosc.org/eventapi/json/GWTC/> (cumulative GWTC event list)
- 391 events (GWTC-1 … GWTC-5.0), columns: `name, catalog, snr, m1, m2, mtot, mfinal, z`
- only catalogue-level summary parameters (network matched-filter SNR, source-frame
  masses, final mass, redshift) — enough for the **sensitivity forecast**.

The full echo search needs GWOSC **strain** (~GB/event), which is *not* downloaded
here. Refresh the catalogue with `python scripts/fetch_catalog.py`.

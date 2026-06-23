# A1 magnetar light curves — data drop

Put one **normalised** post-outburst X-ray light curve per file here:

```
<source>.csv          header:  t_days,flux[,flux_err]
```

- `t_days` — time **since outburst onset**, in days (must be > 0).
- `flux` — unabsorbed flux *or* count rate, any consistent unit (the comb is a *fractional*
  log-periodic modulation, so the absolute normalisation does not matter; > 0 required).
- `flux_err` — optional 1σ error (not yet used by the detector).

The A1 channel ingests **every** `*.csv` here, works in `y = ln(flux)`, applies the per-curve
ln(t)-range gate (≥ 2.8 comb periods ≈ 6.8 in `ln t`, i.e. ≳ 3 decades in time), and **stacks**
all sufficiently-ranged outbursts to test the TFPT kernel `ω = 2π/ln((3/2)⁶) = 2.583`.

## How to populate (real data only — never fabricate)

```bash
# list curated transient-magnetar targets (name, onset MJD, RA/Dec, source)
tfpt-combdomains fetch-magnetar --list

# best-effort auto (needs `pip install swifttools`): Swift-XRT long-term light curves
tfpt-combdomains fetch-magnetar --swift

# guaranteed: normalise a table you downloaded (Swift/XRT UKSSDC, or Coti Zelati+2018 MOOC)
tfpt-combdomains fetch-magnetar --normalize raw_lc.qdp --source Swift_J1822.3-1606 \
    --time-col 0 --flux-col 1 --err-col 2 --mjd
```

## Sources

- **Swift/XRT** "build your own light curve": <https://www.swift.ac.uk/user_objects/>
- **Magnetar Outburst Online Catalogue** (Coti Zelati et al. 2018, MNRAS 474, 961),
  "download all data": <http://magnetars.ice.csic.es>

Cite the originating mission/paper per source when using these data. Raw downloads under
`raw/` are gitignored; only the small normalised `<source>.csv` files are committed.

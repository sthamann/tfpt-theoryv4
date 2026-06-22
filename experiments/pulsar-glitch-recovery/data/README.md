# Data provenance

The `data/` directory is **gitignored** (`data/*`); **only this `README.md` and the
small derived `jbo_glitches.csv` are committed**, so the analysis reproduces
without the ~1.8 MB raw HTML download.

## Source

| File | Dataset | N | Source |
|---|---|---|---|
| `gTable.html` (gitignored) | Jodrell Bank Glitch Catalogue (raw HTML) | 726 glitches / 222 pulsars | `https://www.jb.man.ac.uk/pulsar/glitches/gTable.html` |
| `jbo_glitches.csv` (committed) | parsed derived size table | 726 rows (723 with `dF/F`) | parsed by `scripts/fetch_glitches.py` |
| `1211.2035` e-print (gitignored) | Yu+2013 arXiv source tarball | — | `https://arxiv.org/e-print/1211.2035` |
| `yu2013_recovery.csv` (committed) | parsed `expTab.tex` recovery table | 60 components / 46 glitches | parsed by `scripts/fetch_recovery.py` |
| `crab2.txt` (gitignored) | Jodrell Bank Crab monthly ephemeris (raw text) | ~580 rows | `https://www.jb.man.ac.uk/pulsar/crab/crab2.txt` |
| `crab_ephemeris.csv` (committed) | parsed `nu`/`nudot`(t) monthly series | 479 points, 1988–2026 | parsed by `scripts/fetch_crab_ephemeris.py` |

Cite **Basu et al. 2022, MNRAS 510, 4049** (size catalogue), **Yu et al. 2013,
MNRAS 429, 688** (recovery table) — plus the per-row original references in
`yu2013_recovery.csv` (e.g. `cdk88`=Cordes+1988, `wbl01`=Wong+2001, `dml02`=Dodson+2002,
`lps93`=Lyne+1993) — and the **Jodrell Bank Crab Pulsar Monthly Ephemeris** (Lyne,
Pritchard & Graham-Smith 1993, MNRAS 265, 1003; updated monthly) when using these data.

## Re-fetch

```bash
python scripts/fetch_glitches.py        # gTable.html -> data/jbo_glitches.csv  (sizes, PG.01/02/03)
python scripts/fetch_recovery.py        # arXiv 1211.2035 expTab.tex -> data/yu2013_recovery.csv  (Q/tau_d, PG.04)
python scripts/fetch_crab_ephemeris.py  # crab2.txt -> data/crab_ephemeris.csv  (nu/nudot(t), PG.05 dynamic comb)
```

## `crab_ephemeris.csv` — the Crab nu(t) waveform (PG.05)

Columns: `mjd, nu, sigma_nu, nudot, sigma_nudot`. The monthly spin frequency `nu` (Hz)
and spin-down rate `nudot` (`1e-15 s^-2`) over ~38 yr. Unlike the static size/`Q`/`tau_d`
tables, this is a *time-resolved recovery waveform*: each inter-glitch interval is a
months-to-years relaxation sampled over ~1.5 decades in `ln(time)` — the wide-baseline
input the dynamic log-periodic recovery comb (`omega = 2pi/ln((3/2)^6) = 2.58`) needs and
that PG.01–04 lacked. The file is parsed by VALUE (the layout changes 3× over the archive's
history), so `nu~29-30 Hz` and `nudot~-3.7e5` are located robustly.

## Derived columns (`jbo_glitches.csv`)

`pulsar, jname, glitch_no, mjd, df_f, df_f_err, df1_f1, df1_f1_err, reference`

- `df_f`   — fractional spin-up `Δν/ν` in units of `1e-9` (the glitch **size**);
  drives PG.01 (size discreteness) and PG.02 (per-pulsar size ladder).
- `df1_f1` — fractional spin-down-rate change `Δν̇/ν̇` (`1e-3`).
- `glitch_no` / `mjd` — per-pulsar running index + epoch; drive PG.02/PG.03
  (per-pulsar ladders, waiting times).
- Non-numeric cells (`X`, upper limits, blank errors) parse to empty/`None`.

## `yu2013_recovery.csv` — the recovery (PG.04) table

Columns: `psr_j, epoch_mjd, dnu_g, Q, Q_err, tau_d, tau_d_err, comp_index, reference`.
The per-glitch **healing fraction `Q`** and **decay timescale `τ_d`** (days) are taken
from Yu+2013's compiled exponential-recovery table (`expTab.tex`), with `comp_index`
labelling the decay component within a multi-component recovery (Vela/Crab have 2–3) —
exactly the input for PG.04a (`Q` clustering at `φ₀`-multiples) and PG.04b (`τ_d`
multi-timescale ladder). The `Q`/`τ_d` are **not** in the Jodrell Bank size catalogue,
so this is a genuinely independent, reproducibly-fetched second dataset (not faked from
the sizes). PG.04 is therefore no longer `data_limited`.

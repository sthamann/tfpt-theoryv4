# Crust-cooling data — provenance (honest)

Each `*.csv` is a small **derived** cooling curve with header
`t_days_since_outburst,kT_eff_eV,err` (plus `#`-comment provenance lines). `kT_eff` is the
**redshift-corrected effective surface temperature** seen by an observer at infinity (eV).

**All points are transcribed from published spectral-fit _tables_** (`ingest = transcribed`), not
digitised from figures and not fabricated. Transcribing a printed table is more accurate than
figure digitisation; crust-cooling curves are not distributed as machine-readable VizieR/FITS
catalogues, so this is the honest ceiling. `t` is computed from the paper's own end-of-outburst
epoch `t0` (either `MJD − t0`, or the paper's `t − t0` directly). Regenerate with
`python scripts/fetch_crust_cooling.py`.

| file | source | N | t range (d) | ≈comb periods | provenance | caveat |
|---|---|---|---|---|---|---|
| `KS1731-260.csv` | KS 1731−260 | 8 | 65–5312 | 1.81 | Merritt+2016, ApJ 833, 186, Tab. 1 (t0=MJD 51930.5) | reached floor ~64 eV |
| `MXB1659-29_ob1.csv` | MXB 1659−29 (OB I) | 6 | 36–2422 | 1.73 | Parikh+2019, A&A 624, A84, Tab. 1 (t0=MJD 52162) | outburst-I epoch |
| `MXB1659-29_ob2.csv` | MXB 1659−29 (OB II) | 7 | 12–505 | 1.53 | Parikh+2019, A&A 624, A84, Tab. 1 (t0=MJD 57809.7) | outburst-II epoch |
| `XTEJ1701-462.csv` | XTE J1701−462 | 13 | 3–1159 | 2.45 | Fridriksson+2011, ApJ 736, 162, Tab. 1 (t0=MJD 54321.95) | XMM-3 flare row dropped |
| `EXO0748-676.csv` | EXO 0748−676 | 11 | 42–1791 | 1.55 | Degenaar+2014, ApJ 791, 47, Tab. 2 (t0=MJD 54714) | shallow swing 129→110 eV |
| `MAXIJ0556-332_ob1.csv` | MAXI J0556−332 (OB I) | 11 | 5–1223 | 2.23 | Parikh+2017, ApJL 851, L28, Tab. 1 (t0=end OB I) | OB II did not reheat |
| `MAXIJ0556-332_ob3.csv` | MAXI J0556−332 (OB III) | 6 | 8–350 | 1.57 | Parikh+2017, ApJL 851, L28, Tab. 1 | **t0(OB III) ESTIMATED** |
| `AqlX-1_2016.csv` | Aql X-1 (2016) | 5 | 28–209 | 0.83 | Li/Ootes+2019, MNRAS 488, 99, Tab. 1 | **t0 ESTIMATED**; recurrent (crust never fully cools) |

**Two `t0` values are estimates** (`t0_estimated`, flagged in the CSV header + the fetch script):
MAXI J0556−332 outburst III (paper gives the last point as "~350 d after outburst III", not an MJD)
and Aql X-1 2016 (outburst "ceased 2016 September"). Both affected curves are **range-blind**
anyway, so the estimate cannot move any verdict.

Every individual curve spans **< 2.8 comb periods** for the `(3/2)⁶` kernel — the hard ln-range
gate is not cleared by any single source (the honest, expected outcome for a density-poor domain).
The union ln-range across all episodes (`≈3.1` periods) is what the superposed-epoch pooled stack
uses.

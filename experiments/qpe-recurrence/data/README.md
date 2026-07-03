# QPE timing data — provenance

## `ero_qpe2_arrival_times.csv` (32 eruption arrival times, machine-extracted)

Table B.1 of "Even a precessing clock is right twice per orbit — the super-periods of
eRO-QPE2" (arXiv:2604.09788, ApJ 2026; extracted programmatically from the arXiv HTML,
no hand transcription). Columns: `n_qpe` (event number of the O−C solution), `t_obs_s`
(observed arrival time in seconds since the start of the XMM1 observation,
MJD 60489.6419), `t_err_s` (1σ), `t_calc_s` (computed from the constant-period
ephemeris `P_est = 8055.71 s`), `instrument` (xmm/xrt/nicer/ep). Only consecutive
events (`ΔN_QPE = 1`) enter recurrence sequences.

## `gsn069_recurrence_times.csv` (9 recurrence times, curated)

Table A.1 of Miniutti et al. 2023, A&A 670, A93 (`T_rec` between consecutive QPEs,
0.4–1 keV Gaussian fits; XMM3–XMM6 + Chandra). **Curation rule (honesty):** only rows
whose value AND 1σ error were fully legible in the retrieved table are committed; two
rows with truncated errors in the retrieval (XMM6 first `T_rec = 26428`, Chandra
`33551`) are omitted rather than guessed — this costs one XMM6 ratio pair and one
Chandra pair. `order` preserves the within-campaign sequence, so consecutive-ratio
analysis uses only adjacent `order` values within one campaign.

# Recovery comb across domains — one detector, six channels

> **Firewall:** search targets / consistency checks, **never** load-bearing claims. TFPT predicts
> the dynamic comb in **boundary/horizon-recovery** relaxations; channels are typed by how
> legitimate that mapping is, and nothing is upgraded to a detection.

The "new" TFPT signature is not a number but a **shape**: a system relaxing to a fixed point
through the frozen geometric mode ladder leaves a **log-periodic (discrete-scale-invariance)
comb** on its recovery curve,

```
R(t) = (power law) * (1 + eps cos(omega ln t + phi))
omega = 2 pi / ln(lambda),  lambda = (3/2)^6   ->  omega = 2.583
eps  ~ exp(-pi^2 / ln lambda) ~ 0.017   (the QT.02 amplitude-suppression law)
```

All from the two axioms (`c3 = 1/(8π)`, `g_car = 5`); no domain number enters. This experiment
applies **one injection-validated comb detector** (`comb.py`) to recovery curves from six
channels (A1–A3b / B4–B5), and reports each honestly.

## The detector (`comb.py`) — injection-validated, with the hard ln-range gate

`detect_comb` asks whether the comb at the **kernel** `omega` is *special* in a recovery curve, by
ranking its comb gain against a periodogram of off-kernel log-frequencies (a degree-2
polynomial-in-`ln t` baseline absorbs the smooth recovery trend, so a pure power law is **not**
flagged). Validation (`validate_detector`, deterministic over seeds): comb present + sufficient
range → detected **96%**, false-positive **0%**; **range-blind below ~2.8 comb periods** (~0% at
1.9) — a hard `ln(t)`-range requirement no stacking can relax.

## The stacked meta-test (`stacked_comb_test`) — the A1 sharpening

A single ~3-decade recovery curve localises a ~2% comb only weakly. But the kernel `ω` is the
**same** in every relaxation (fixed by the axioms) — only the phase differs — so many outbursts are
combined by summing the phase-insensitive per-curve comb gain at `ω` and ranking it with a
**permutation null** (each curve's kernel gain swapped for a random off-kernel gain from its matched
band). The hard ln(t)-range gate stays **per curve** (stacking raises amplitude SNR, never ln-range).
Injection-validated (`validate_stack`): a faint `ε = 3–5 %` comb that a single curve misses
(~10–45 %) is recovered by the stack (~75–100 %), with a bounded false-positive (~10 %; mildly
anti-conservative at ~3 periods, so a stacked hit is **escalate → independent cross-check**, never a
claim).

## The seven channels (`channels.py`)

| ch | domain | firewall legitimacy | data status | result |
|---|---|---|---|---|
| **A1** | magnetar flux relaxation (stacked) | surface (borderline) | **real** | 6 Swift-XRT/LSXPS outbursts; 2 clear the gate; **stacked ω=2.58 NOT special (p≈0.99) → clean NULL** (surface caveat) |
| **A2** | BH late-time ringdown tail / QNM `ln3` | horizon | `data_limited` | horizon-legit but below single-event SNR (see gw-ringdown-spectroscopy) |
| **A3** | FRB burst tail (FAST/GBT, stacked) | horizon-residual | **real** | **8 bright bursts / 3 repeaters**, 7 clear the gate; **stacked ω=2.58 not special (p≈0.34) → clean NULL** (weak: scattering-dominated, ~2% comb) |
| **A3b** | CHIME baseband FRB tail (stacked) | horizon-residual | **real** | **8 distinct FRBs**, 2.56 µs coherently-dedispersed full-Stokes (DOI 10.11570/23.0029); all 8 clear the gate; **stacked ω=2.58 not special (p≈0.67) → clean NULL** (genuine scattering tails, still ~2% ceiling) |
| **A4** | GRB X-ray afterglow plateau (stacked) | surface (borderline) | **real** | **22 Swift-XRT afterglows** (UKSSDC), **17 clear the gate at 3–4.4 comb periods** — the widest-ln(t) astrophysical recovery in hand; **stacked ω=2.58 NOT special (p≈0.13) → well-powered NULL** (not data-limited; central-engine/accretion, surface firewall) |
| **B4** | BEC analog-horizon Hawking/Page | analog | `needs_experiment` | most direct boundary-recovery analog; theory = recovery-channel; needs analog-gravity data |
| **B5** | quantum-simulator geometric ladder | internal | `needs_experiment` | comb by construction (quantum-testbed synthetic); needs a built simulator |

**A1 is now sharp and run on real data: a clean NULL.** Across 6 Swift-XRT/LSXPS transient-magnetar
recoveries, the 2 that clear the ln(t)-range gate (1E 1547.0−5408, periods≈3.5; SGR 1745−2900,
periods≈2.9) stack to **p≈0.99 — the kernel ω=2.58 is not special** (with the magnetospheric/surface
firewall caveat). A3 (FRB tail) is now **stacked over 7 bright bursts across 3 repeaters**
(FRB 20121102A ×5 FAST, FRB 20190520B ×2 GBT, FRB 20201124A ×1 GBT) → also a **clean NULL**
(stacked ω=2.58 not special, p≈0.34; sharpens the earlier single-burst weak null p≈0.25, still
scattering-dominated). **A3b adds the CHIME baseband upgrade** — 8 distinct FRBs at 2.56 µs,
coherently dedispersed, full-Stokes (DOI 10.11570/23.0029); all 8 clear the gate on **genuine
scattering tails** (not noise-filled range), and the stack is again a **clean NULL** (ω=2.58 not
special, p≈0.67). A2 (BH late-time tail) is the
horizon-legitimate but data-limited channel; B4/B5 need bespoke experiments. The comb is intrinsically
a ~2% effect needing a clean, wide-range recovery — the search space is genuinely narrow. **No claim.**

**A4 (GRB X-ray afterglow plateau) is the widest-ln(t) astrophysical channel and the first that is
NOT data-limited.** A Swift-XRT afterglow flux curve spans ~100 s … 10⁶–10⁷ s = **4–5 decades in
ln(t)**, so a *single* GRB clears the 2.8-period gate that the ms FRB tails cannot, and the public
UKSSDC repository has >1000 of them. Across **22 curated long/plateau GRBs** (`fetch-grb`), **17
clear the gate** (3.0–4.4 comb periods; e.g. GRB 130427A 4.42, GRB 060729 4.35, GRB 060124/050416A
4.1) and the phase-incoherent **stack is a clean, well-powered NULL** — the kernel ω=2.58 is **not
special, p≈0.13**. Two individual GRBs show low single-curve p (130427A 0.004, 050416A 0.06) but
these are *uncorrected* over 17 trials and the proper combined statistic (the stack) is null. The
firewall is the same as A1: a GRB plateau is a **central-engine / accretion** relaxation (magnetar
spin-down or fallback), **not a horizon recovery** — a comb here would be a universal-DSI coincidence,
and this NULL is informative precisely because it is **well-powered, not data-limited**.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .   # numpy only (A3 reuses the FRB reader + astropy)
tfpt-combdomains analyze    # detector + stack validation + all 6 channels -> results/recovery_comb_domains.json
# or: PYTHONPATH=src python -m tfpt_combdomains.cli analyze
```

## Real magnetar data (A1)

```bash
tfpt-combdomains fetch-magnetar --list      # curated transient-magnetar targets (name, onset MJD, RA/Dec)
tfpt-combdomains fetch-magnetar --swift     # Swift-XRT/LSXPS long-term light curves (needs: pip install swifttools setuptools)
# or normalise a manual download (Swift/XRT UKSSDC build-your-own, or the Coti Zelati+2018 MOOC):
tfpt-combdomains fetch-magnetar --normalize raw.qdp --source Swift_J1822.3-1606 \
    --time-col 0 --flux-col 1 --err-col 2 --mjd
```

Each `data/magnetar/*.csv` (`t_days,flux[,flux_err]`, onset-relative) is ingested as `y = ln(flux)`,
gated, and stacked. The `--swift` path resolves each curated position to its LSXPS source by cone
search and pulls the observation-binned total-band rate curve. **First real run = a clean NULL**
(stacked `p ≈ 0.99`). swifttools needs `distutils`, so on Python ≥ 3.12 install `setuptools` too.

## Real GRB afterglow data (A4)

```bash
tfpt-combdomains fetch-grb     # pull the curated Swift-XRT plateau-GRB flux light curves (UKSSDC)
tfpt-combdomains analyze       # A4 ingests data/grb/*.csv, gates, and stacks
```

`fetch-grb` downloads public Swift-XRT flux light curves
(`https://www.swift.ac.uk/xrt_curves/<8-digit targetID>/flux.qdp`, Evans et al. 2007/2009) for a
curated long/plateau-GRB list and normalises each to `data/grb/<name>.csv` (`t_s,flux,flux_err`,
T0-relative seconds). The real GRB name is read from the file header, so a wrong target id simply
misses (never fabricated). The small normalised curves are committed (like the magnetar set); the
recovery observable is `y = ln(flux)` and the detector's degree-2 ln-t baseline absorbs the
power-law plateau/break.

## Real CHIME baseband (A3b)

The A3b channel reads CHIME/FRB **Baseband Catalog 1** beamformed files (CHIME/FRB Coll. 2024,
ApJ 969 145; CANFAR DOI `10.11570/23.0029`) — 2.56 µs, 1024 channels, full-Stokes, coherently
dedispersed. Fetch a subset with the CADC `vos` client (anonymous, no account):

```bash
pip install vos h5py
vls "vos:AstroDataCitationDOI/CISTI.CANFAR/23.0029/data/beamformed_files"      # list the 140 files
vcp "vos:AstroDataCitationDOI/CISTI.CANFAR/23.0029/data/beamformed_files/FRB20181231C_24366209_beamformed.h5" \
    frb-tfpt-signatures/new-data/chime-baseband/                               # ~0.15–4 GB each
```

`chime.py` loads `tiedbeam_power`, **incoherently dedisperses across channels** (using `time0` +
`DM_coherent`, the official recipe) — without this the dispersion sweep fakes a wide tail — sums
over frequency, and feeds the post-peak tail to the stacked detector. The smallest ~8 files (≈3 GB)
are enough for an 8-burst stack; raw HDF5 stays gitignored under `new-data/`.

## Microshot cascade (`microshots`) — the intra-burst dynamic-kernel test (B1)

```bash
tfpt-combdomains microshots   # -> results/microshot_cascade.json
```

The dynamic kernel also predicts an intra-burst **cascade**: within one ultra-bright FRB the resolved
**microshots** should obey the resummed recovery clock (gap ratio `ln3/ln(3/2)=2.71`, hard wall at
`N_fam=3`, v124) and/or a log-periodic time-comb. We use the **vetted, published** microshot arrival
times of FRB 20220912A bursts **B1 (27 shots)** and **B2 (18 shots)** — manually identified by Hewitt
et al. 2023 (MNRAS 526, 2039; Zenodo `10552561`), so there is no noise-vs-shot ambiguity — and test the
gap-clock, the wall, and the time-DSI comb against gap-shuffle nulls + placebo ratios.

> **Firewall:** a search target (horizon-residual), never a claim; N≤2 bursts, intra-burst point process.

**Result (clean NULL, all channels):** the gap ratio does **not** pile up at 2.71 above the shuffle
null + placebo (B1 enrichment 1.47, p≈0.16, vs placebo 1.26; B2 below chance); there is **no**
protected wall (B1's longest decreasing-gap run is 5 > 3); the time-DSI comb is **range-limited**
(1.5–1.6 periods < 2.8) and not special; and the **amplitude echo-ratio** (the FRB.02 `64/729`/`8/27`
kernel, now run on the **real NRT peak fluxes** via the published `prep_burst` recipe) is **not
enriched** (B1 energy enr 0.80, p≈0.75; a *free* quotient hits 9× vs ≈0 at the kernel). So the
microshot forest carries no recovery-kernel echo, clock, wall, or comb. The NRT filterbanks
(`b_59881.fil` etc., Zenodo `10552561`) live gitignored under `new-data/eclat-microshots/`; the
microshot times are hard-coded so the times-based tests reproduce without the download.

## Earthquake aftershocks — the FULL TFPT signature battery (`quake`)

```bash
tfpt-combdomains quake     # fetch USGS aftershock sequences -> results/quake_tfpt_signatures.json
```

Aftershock decay (Omori `rate ~ t^-p`) is the data-richest **terrestrial** relaxation with the wide
`ln t` range *and* high counts the faint ~2% comb needs (6 sequences here span up to **5.4 comb
periods** with thousands of events — finally **not** data-limited). It tests the **whole** TFPT
battery, not just one kernel: (1) the comb at **every** TFPT log-period `λ ∈ {3/2, φ, 2, 3, 4, 5, 8,
(3/2)⁶, 30}` (stacked, per-λ ln-range+Nyquist gate, **Bonferroni look-elsewhere**); (2) a **free-fit**
of seismicity's own dominant log-period; (3) the Omori exponent vs TFPT rationals.

> **Firewall:** earthquakes are a crustal/critical relaxation, **not** a boundary/horizon recovery.
> Any hit is a *universal-DSI shape* coincidence, **never** TFPT confirmation.

**Result (well-powered NULL):** no TFPT log-period is special after look-elsewhere (Bonferroni global
`p ≈ 0.77`); seismicity's own scale is `λ_fit ≈ 2.3–2.6` (the standard value, 12–16% off the nearest
TFPT ratio in ln); the tempting `p ≈ 0.84 ≈ 5/6` is a 0-bit simple-rational coincidence (per-sequence
`p` scatters 0.67–1.11, no clustering). Unlike the astro nulls this one is **not** data-limited — the
signature is robustly absent in data that *could* have shown it.

## Layout

```
src/tfpt_combdomains/comb.py      # detector + injection validation + ln-range gate + STACKED permutation meta-test
src/tfpt_combdomains/channels.py  # the 6 channels (A1 magnetar stacked; A2 BH tail; A3 FAST/GBT FRB stacked; A3b CHIME baseband stacked; B4, B5)
src/tfpt_combdomains/chime.py     # CHIME baseband-catalog HDF5 reader (incoherent cross-channel dedispersion -> true profile+tail)
src/tfpt_combdomains/fetch.py     # real magnetar light curves (swifttools/LSXPS cone search + manual --normalize)
src/tfpt_combdomains/quake.py     # FULL TFPT signature battery vs USGS earthquake aftershocks (look-elsewhere-corrected)
src/tfpt_combdomains/microshots.py # (B1) intra-burst microshot cascade kernel test (vetted Hewitt+2023 catalog)
src/tfpt_combdomains/cli.py       # `tfpt-combdomains {analyze, fetch-magnetar, quake, microshots}`
scripts/fetch_magnetar.py         # thin CLI wrapper for the fetcher
data/magnetar/*.csv               # normalised light curves (committed); data/{magnetar/raw,quake}/ gitignored
results/recovery_comb_domains.json  # committed summary (detector + stack validation + per-channel status)
results/quake_tfpt_signatures.json  # committed summary (battery + free-fit + Omori, look-elsewhere-corrected)
```

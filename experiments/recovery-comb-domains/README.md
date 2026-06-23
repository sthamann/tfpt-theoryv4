# Recovery comb across domains — one detector, five channels

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
applies **one injection-validated comb detector** (`comb.py`) to recovery curves from five
domains (the A1–A3 / B4–B5 options), and reports each honestly.

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

## The five channels (`channels.py`)

| ch | domain | firewall legitimacy | data status | result |
|---|---|---|---|---|
| **A1** | magnetar flux relaxation (stacked) | surface (borderline) | **real** | 6 Swift-XRT/LSXPS outbursts; 2 clear the gate; **stacked ω=2.58 NOT special (p≈0.99) → clean NULL** (surface caveat) |
| **A2** | BH late-time ringdown tail / QNM `ln3` | horizon | `data_limited` | horizon-legit but below single-event SNR (see gw-ringdown-spectroscopy) |
| **A3** | FRB burst tail (stacked) | horizon-residual | **real** | **8 bright bursts / 3 repeaters**, 7 clear the gate; **stacked ω=2.58 not special (p≈0.34) → clean NULL** (weak: scattering-dominated, ~2% comb) |
| **B4** | BEC analog-horizon Hawking/Page | analog | `needs_experiment` | most direct boundary-recovery analog; theory = recovery-channel; needs analog-gravity data |
| **B5** | quantum-simulator geometric ladder | internal | `needs_experiment` | comb by construction (quantum-testbed synthetic); needs a built simulator |

**A1 is now sharp and run on real data: a clean NULL.** Across 6 Swift-XRT/LSXPS transient-magnetar
recoveries, the 2 that clear the ln(t)-range gate (1E 1547.0−5408, periods≈3.5; SGR 1745−2900,
periods≈2.9) stack to **p≈0.99 — the kernel ω=2.58 is not special** (with the magnetospheric/surface
firewall caveat). A3 (FRB tail) is now **stacked over 7 bright bursts across 3 repeaters**
(FRB 20121102A ×5 FAST, FRB 20190520B ×2 GBT, FRB 20201124A ×1 GBT) → also a **clean NULL**
(stacked ω=2.58 not special, p≈0.34; sharpens the earlier single-burst weak null p≈0.25, still
scattering-dominated); A2 (BH late-time tail) is the
horizon-legitimate but data-limited channel; B4/B5 need bespoke experiments. The comb is intrinsically
a ~2% effect needing a clean, wide-range recovery — the search space is genuinely narrow. **No claim.**

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .   # numpy only (A3 reuses the FRB reader + astropy)
tfpt-combdomains analyze    # detector + stack validation + all 5 channels -> results/recovery_comb_domains.json
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
src/tfpt_combdomains/channels.py  # the 5 channels (A1 magnetar stacked; A2 BH tail; A3 FRB now multi-burst stacked; B4, B5)
src/tfpt_combdomains/fetch.py     # real magnetar light curves (swifttools/LSXPS cone search + manual --normalize)
src/tfpt_combdomains/quake.py     # FULL TFPT signature battery vs USGS earthquake aftershocks (look-elsewhere-corrected)
src/tfpt_combdomains/cli.py       # `tfpt-combdomains {analyze, fetch-magnetar, quake}`
scripts/fetch_magnetar.py         # thin CLI wrapper for the fetcher
data/magnetar/*.csv               # normalised light curves (committed); data/{magnetar/raw,quake}/ gitignored
results/recovery_comb_domains.json  # committed summary (detector + stack validation + per-channel status)
results/quake_tfpt_signatures.json  # committed summary (battery + free-fit + Omori, look-elsewhere-corrected)
```

# watch-channels — live measurements vs. the frozen TFPT bands

> **Firewall:** a **pure monitor**, never a claim. This folder mutates nothing outside
> itself (only its own `state.json`): no scorecard, no ledger, no papers, no website.
> An `ALERT` is a prompt for a *human* to re-run the relevant experiment pipeline and
> follow the normal scorecard/promotion workflow — statuses are never upgraded or
> downgraded from here.

## Purpose

The TFPT predictions are frozen (`verification/predictions_frozen.json`, freeze
2026-06-09); the experiments keep publishing. This checker makes the confrontation
**reproducible and diff-able**: one command compares the current measurement state
against the frozen targets + preregistered kill windows, computes pulls and the
distance to each kill criterion, and flags status changes against the previous run.

## Channels

| Rank | Channel | TFPT (frozen) | Watching |
|---|---|---|---|
| primary | `sin2_theta12` (prediction of record) | 0.306747 | JUNO updates |
| primary | `beta_birefringence_deg` | 0.242435° | ACT / SO / LiteBIRD |
| primary | `w_dark_energy` | w = −1 exactly | DESI w₀wₐ (DR3), Euclid |
| primary | `br_kplus_pinunu` | 9.45×10⁻¹¹ | NA62 final / KOTO II |
| primary | `alpha_s_running` | −7.6×10⁻⁴ (band [−8.0,−5.6]×10⁻⁴) | Planck/ACT combos, CMB-S4 |
| secondary | `sin2_theta13` | 0.023108 | JUNO / global fits |
| secondary | `delta_pmns_deg` | 240° | NuFIT / DUNE / Hyper-K |
| secondary | `n_s` | band [0.9600, 0.9667] | Planck / DESI combos |
| secondary | `r_tensor` | band [0.0033, 0.0048] | BK18 / CMB-S4 / LiteBIRD |

## Files

- `frozen_bands.json` — the TFPT side: frozen values, formulas, kill windows, provenance
  per channel (extracted verbatim from `verification/predictions_frozen.json` and the
  evidence-scorecard rows). **Never changes with new data.**
- `measurements.json` — the live side: current measurements with source + date; every
  entry carries `entered: YYYY-MM-DD`. One entry per channel is `"record": true` and
  drives the status; superseded entries stay in place as history.
- `check.py` — stdlib-only comparator. Pull convention `(TFPT − measured)/σ` (same as
  the scorecard; TFPT-side error bar for asymmetric errors). Status per channel:
  `PASS` / `WATCH` / `ALERT` (= preregistered kill criterion met at face value).
  Channel types: `gaussian` (point + kill σ, optional kill window on the central
  value), `band` (N★ bands), `upper_limit` (r), `exclusion` (w = −1, where the
  measurement *is* an exclusion significance; kill at 5σ per the watchdog).
- `state.json` — written by `check.py`; last run's per-channel statuses, used to flag
  `[CHANGED ...]` lines. Committed, so status flips are visible in git history.

## Run

```bash
python experiments/watch-channels/check.py            # exit 0 = no ALERT, 1 = ALERT, 2 = config error
python experiments/watch-channels/check.py --dry-run  # report only, state.json untouched
```

## Update process (the honest way — by hand)

When a new result appears (JUNO release, SO β, DESI DR3, NA62 final, …):

1. Add a new entry to that channel in `measurements.json` with `value`/`sigma` (or
   `exclusion_sigma` / `upper_limit`), `source` (paper/arXiv), `date`, and
   `entered: <today>`.
2. Move `"record": true` to the entry that should drive the status; keep the old
   entries as history.
3. Run `check.py` — it reports the new pulls and flags any status change against
   `state.json`.
4. If a status changed materially, follow up in the *owning* experiment
   (`neutrino-mixing`, `dark-energy-w-watchdog`, `rare-kaon-bridge`, …) and the normal
   scorecard workflow — **not** here.

**Deliberately NOT built: auto-scrapers.** NuFIT tables, DESI papers, NA62 releases
and arXiv abstracts have no stable machine API; scrapers silently break or, worse,
silently ingest wrong numbers into a kill-criterion monitor. A hand-curated
`measurements.json` with provenance per entry is auditable and is the same convention
the experiments already use (`neutrino-mixing/data/measurements.json`,
`dark-energy-w-watchdog/data/measurements.json`).

## Cron (weekly reminder run)

The checker is deterministic given the two JSON files, so a cron run is mainly a
scheduled reminder that prints the current pulls/kill margins and any status drift:

```cron
0 9 * * 1  cd /Users/stefanhamann/Projekte/tfpt-theoryv4 && python3 experiments/watch-channels/check.py >> experiments/watch-channels/cron.log 2>&1
```

(`cron.log` is disposable; the auditable trail is `state.json` + git.)

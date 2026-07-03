# cosmic-dipole-watchdog — the number-count dipole anomaly vs TFPT's FLRW foundation

**Status: `data_limited` (watch) — the excess is real in every catalog; its significance as
an FLRW violation is contested at the level of the clustering/mask error budget (2026-07-03).**

> **Firewall:** standalone **frontier dissolution watchdog** — a search surface, never a
> load-bearing claim. Nothing here upgrades any TFPT status; a triggered kill would be
> routed to the ledger by the parent, not by this experiment.

## The open question (no model explains it)

The Ellis–Baldwin test: our peculiar motion (CMB dipole, `v = 369.8 km/s`) must induce a
matching kinematic dipole in the number counts of distant sources. Measured instead:

- **CatWISE2020 quasars** (Secrest+2021, 1.36M sources): `D_obs = 15.54×10⁻³` vs kinematic
  expectation `≈ 7.4×10⁻³` — **~2.1× too large**, aligned with the CMB dipole within ~27°,
  claimed **4.9σ**. Bayesian re-analysis (Dam+2023): 2.7×, **5.7σ**. Extended catalog
  (Secrest+2022): **4.4σ**.
- **Radio decomposition** (Wagenveld+2025): best-fit *non-kinematic residual* dipole
  `D_resid = (0.81±0.14)×10⁻²` at **5.4σ**, CMB-aligned.
- **RMP Colloquium** (Rev. Mod. Phys. 97, 041001 (2025)): "the discrepancy now exceeds 5σ —
  a serious challenge to FLRW cosmology."
- **But**: the 2026 FLASK reassessment (arXiv:2511.00822) with lognormal large-scale
  structure, shot noise, the exact mask and a clustering dipole reduces the significance to
  **3.63σ** (no clustering dipole) / **3.44σ** (random) / **3.27σ** (CMB-aligned clustering);
  the octopole-leakage reading (Abghari+2024) is contested.

If real, the matter and radiation rest frames disagree — a direct strike at the
cosmological principle underneath ΛCDM *and* underneath TFPT's cosmology branch.

## The TFPT reading (dissolution watchdog)

TFPT's cosmology branch is built **on** FLRW: the parameter-free flat budget closure
(`h = 0.6715`), the Λ/H₀ engine, `Ω_b` (Macquart), the CMB seed line. The `μ4` clock /
`PSL(2,ℂ)` boundary orientation allows at most a **tiny** global orientation remnant (same
expectation as `cosmic-handedness`), and there is **no mechanism for an intrinsic
super-Hubble matter dipole**. So — like steriles (`N_fam=3`), evolving DE (`w=−1`),
Cabibbo, X17 and `R_D(*)` — this is a **dissolution prediction**: the excess must resolve
into clustering/mask/selection systematics.

**Frozen kill rule (pre-registered):** a clustering-marginalized, mask-controlled
non-kinematic dipole at **≥5σ**, replicated in **≥2 independent selections** (e.g.
LSST/Euclid + SKA-MALS), surviving the aligned-clustering scenario → strikes the FLRW
foundation of the TFPT cosmology branch (flat budget, Λ/H₀ engine) — **not** the compiler
core (α, masses, mixings are local physics).

**Deciders:** LSST + Euclid + SKA/MALS number-count dipoles (independent selections,
deeper flux limits), DESI QSO spectroscopic dipole, joint clustering-marginalized analyses.

## Run

```bash
. experiments/tfpt-discovery/.venv/bin/activate
cd experiments/cosmic-dipole-watchdog && PYTHONPATH=src python -m tfpt_dipole.cli analyze
```

Deterministic; published values only (`data/measurements.json`, retrieved 2026-07-03);
writes `results/results.json`.

## Relation to `cosmic-handedness`

Same watchdog family (global isotropy/orientation of the TFPT boundary), different
observable: handedness watches a parity **monopole** in galaxy spins; this watches the
**dipole** in source counts. Both are typed `search_target`/frontier and share the
honest-systematics caveat (aberration/selection for spins; clustering/mask here).

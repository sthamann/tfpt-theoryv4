# TFPT CMB seed-line — one `φ0` for birefringence `β` *and* baryons `Ω_b`

A **cross-domain consistency test** (Priority 1 of `search.txt`). TFPT couples a
single retarded seed `φ0` to two observables that normally live in completely
separate analyses:

```
φ0       = (4/3) c₃ + 48 c₃⁴          (c₃ = 1/(8π); origin_theory v60)
β_rad    = φ0 / (4π)                  → β = 0.242435°   (cosmic birefringence)
Ω_b      = (4π − 1) · β_rad           → Ω_b = 0.04894   (baryon fraction)
```

so both must sit on the **frozen line** `Ω_b / β_rad = 4π − 1 = 11.566`. Because
birefringence, the baryon fraction and flavour are usually fit in different
pipelines, this *joint* line is rarely (if ever) used as a shared-seed test — which
is exactly what makes it hard to fake: a single number `φ0` has to land two
independent measurements at once.

## Firewall

Search target, **not** a claim. `β = 0.2424°` is a genuine TFPT prediction (it shares
the seed that fixes the Cabibbo angle), but the current `β` errors are wide, so this
is a **consistency** test, not a detection. A systematics-controlled `β` that breaks
the line at ≳3σ would falsify the shared-seed reading.

## What it tests (`src/tfpt_cmb/seed_line.py`) — four explicit modes

1. **`beta_only`** — `β_TFPT` vs ACT DR6 / Planck PR4.
2. **`omega_b_only`** — `Ω_b,TFPT` vs Planck / BBN (`Ω_b` derived unit-safely as
   `Ω_b h² / h²`).
3. **`joint_independent`** — the frozen line `Ω_b/β_rad = 4π−1` + single-seed coherence
   (`φ0^β` vs `φ0^Ω`), **assuming** `cov(β, Ω_b)=0`.
4. **`joint_covariance_placeholder`** — the same line, flagged that `cov(β, Ω_b)` is
   **not** modelled, so **no combined significance is claimed** (ACT β + Planck Ω_b are
   both CMB-derived → use the BBN `Ω_b` leg for a genuinely CMB-independent test).

A hard **unit guard** fails loudly on the two classic slips: `β` is always in radians
internally; `Ω_b` (~0.049) is never confused with `Ω_b h²` (~0.022), and BBN values
declare `Ω_b h²` + `h` explicitly.

## Result (deterministic; published values in `data/measurements.json`)

| mode | quantity | measured | TFPT | distance | status |
|---|---|---|---|---|---|
| beta_only | β (ACT DR6) | 0.215 ± 0.074° | 0.2424° | **0.37σ** | consistent |
| beta_only | β (Planck PR4) | 0.30 ± 0.11° | 0.2424° | 0.52σ | consistent |
| omega_b_only | Ω_b (Planck) | 0.0493 ± 0.0009 | 0.04894 | 0.42σ | consistent |
| omega_b_only | Ω_b (BBN D/H) | 0.0489 ± 0.0014 | 0.04894 | **0.04σ** | consistent |
| joint_independent | line Ω_b/β_rad | 13.14 ± 4.53 | 11.566 | 0.35σ | consistent |
| joint_independent | seed coherence | φ0^β vs φ0^Ω | — | 0.39σ | consistent |
| joint_covariance_placeholder | — | — | — | — | no combined significance |

→ **consistent with the seed line** (not *validated*): one frozen `φ0` fits both
observables and the line holds within errors. The β errors are wide and the joint
covariance is unmodelled, so no combined significance is claimed. The BBN `Ω_b` leg
(CMB-independent) at 0.04σ is the sharpest single point.

## Shared-seed meta-test — one `φ0` → **four** independent observables

The same retarded seed `φ0` fixes four observables in completely different sectors
(`shared_seed.py`):

```
β_rad         = φ0/(4π)              (CMB birefringence)
Ω_b           = (4π−1)φ0/(4π)        (baryon fraction)
sin²θ₁₃       = φ0·e^(−5/6)          (reactor neutrino angle)   = 0.0231
λ_Cabibbo     = √(φ0(1−φ0))          (CKM Cabibbo angle)        = 0.224376
```

Inverting each measurement back to the seed it implies:

| observable | measured | → implied φ0 | vs frozen 0.05317 |
|---|---|---|---|
| β (ACT DR6) | 0.215° | 0.04715 | −0.37σ |
| Ω_b (BBN, h fixed) | 0.02218 h² | 0.05311 | −0.05σ |
| sin²θ₁₃ (NuFIT 6.0) | 0.02195 | 0.05051 | **−2.0σ** (known mild tension) |
| λ_Cabibbo (PDG) | 0.22431 | 0.05314 | **−0.08σ** |

→ **combined χ²/dof = 1.23** (deviation from the joint best-fit seed, dof = n−1 — the proper
internal-agreement statistic, canonical and identical to `seed-consistency`), max |z| = 2.0:
four independent data worlds (CMB, BBN, reactor neutrinos, CKM) point at the *same* seed `φ0`.
Strongest meta-signature, but **not validated** — sector covariances are unmodelled and
θ₁₃/Cabibbo are seed-anchored low-energy predictions (RG/short-distance completion not computed
here). The dominant pull is θ₁₃ (see `seed-consistency` for the full LOO/dominant-pull/PPC).

## β meta-analysis — combine the birefringence measurements, shared-systematic aware (`birefringence_meta.py`)

The single-measurement modes compare β_TFPT to ACT and Planck *separately*. The meta-analysis
**combines** the published β values — but honestly, because CMB birefringence measurements are
**not independent**: the Planck-based values (PR3 Minami&Komatsu 2020, PR4 Eskilt 2022) share
Planck data + the dominant **absolute-angle / EB-foreground calibration** systematic. So:

| combination | β [deg] | TFPT 0.2424° | note |
|---|---|---|---|
| **naive IVW** (all 3 as independent) | 0.259 ± 0.056 | **−0.29σ** | *lower bound* on the error (double-counts Planck) |
| **family-aware** (ACT + best-Planck, +0.10° shared calib. syst.) | 0.241 ± 0.117 | **+0.01σ** | the honest error |
| **CMB-independent** (BBN Ω_b → β) | — | **+0.04σ** | the cleanest cross-check |

Inputs are mutually consistent (χ²/dof = 0.46). **TFPT's 0.2424° sits essentially on the
family-aware meta-estimate** and on the BBN-independent leg — **consistent, not a detection**: the
shared calibration systematic dominates, so the family-aware (not the naive) error is the honest
one, and a real frequency/foreground null needs the raw per-frequency EB spectra (not recomputed
here; the per-experiment frequency-robustness is taken from the cited papers).

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-cmb analyze            # seed-line + shared-seed + beta meta-analysis -> results/results.json
# or: PYTHONPATH=src python -m tfpt_cmb.cli analyze
```

## Layout

```
src/tfpt_cmb/constants.py        # φ0, β, Ω_b, the 4π−1 line — all from c₃ (no SI input)
src/tfpt_cmb/seed_line.py        # per-observable + single-seed-coherence + line tests
src/tfpt_cmb/shared_seed.py      # one φ0 -> β + Ω_b + θ13 + Cabibbo meta-test
src/tfpt_cmb/birefringence_meta.py  # β meta-analysis (naive vs family-aware, BBN cross-check)
src/tfpt_cmb/cli.py              # `tfpt-cmb analyze`
data/measurements.json           # published β (ACT/Planck PR4/PR3, with data_family) + Ω_b + refs
```

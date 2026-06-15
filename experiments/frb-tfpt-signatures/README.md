# TFPT signatures in real Fast Radio Burst data

A **preregistered, multi-dataset, surrogate-calibrated** search for residual
TFPT *boundary-recovery* signatures in real, public FRB data. The pipeline is
built to either find a replicated, multi-source eigenvalue fingerprint **or kill
the FRB trace cleanly** — not to "find more numbers".

- **Standalone:** an exploration experiment under `experiments/`. **Not** wired
  into the verification suite, ledger, or website; it makes **no** load-bearing
  TFPT claim.
- **Firewall:** every result is a **search target, not a claim** (§1).
- **Frozen kernel:** the recovery ratios are exact rationals derived from the two
  axioms; no fitted exponents (guarded by `tests/`, §4).
- **Current verdict (v1.1, deterministic at `--seed 0`):** `not_confirmed_not_refuted`.
  One **candidate** (FRB.03 activity window), two **nulls** (FRB.02 echo ratio,
  FRB.04 polarisation), one **consistency** axis (FRB.05 Ω_b), one **data-limited**
  axis (FRB.01). No replicated, discriminating support.
- **v1.1 correction (important):** the earlier FRB.02 "8/27 candidate" was an
  **observable-semantics error** — `8/27` is the *amplitude* root, but the FAST
  column is *energy* in erg. Under the correct split (energy ratio → `64/729`;
  `√(energy ratio)` → `8/27`) **both theory channels are null**; the `8/27`
  pile-up survived only in a flagged *audit* channel (channel mismatch).
- **v1.2 completion (full null batteries):** with the four preregistered FRB.04
  nulls (stationary-Markov, time-shuffle, block-shuffle, **AR(1)-drift**) and two
  extra FRB.02 nulls (**AR(1)-energy storm**, censoring), the two remaining
  seductive patterns are **explained away**: the FRB.02 `8/27` audit anomaly
  disappears under the storm null (all channels q=1.0), and the v2 RM≈`{2/3,1/3}`
  hint has **AR(1)-drift null p=0.92** ⇒ a smooth magneto-ionic drift, not a
  discrete spectrum. A data-derived FRB.03 window (HDI of folded CHIME phases)
  and a full VAR(1) shared model were also added (§7–§8).

---

## 1. Firewall — what TFPT may and may not say about FRBs

FRBs are **not** new gravity and **not** a direct Hawking signature:

```
FRB = compact magnetised source + plasma transfer (DM, RM, scattering, lensing)
      + (possible) boundary-recovery kernel residual
```

The only admissible statement:

> **IF** the TFPT boundary recovery is real, **THEN** FRB repeaters may show a
> few *dimensionless* echoes of the recovery kernel *after* standard plasma is
> removed.

**Language rules (enforced; `hypotheses/frb_tfpt_v1.yaml`):**

- Forbidden: "FRBs confirm TFPT" · "FRBs show the boundary kernel" ·
  "FRB 20180916B proves the recovery formula" · "DM(z) confirms TFPT Ω_b".
- Allowed: "FRBs provide a preregistered search space …" · "FRB 20180916B is a
  single window candidate, not replicated" · "FRB.02 shows a single-source 8/27
  candidate that fails the q<0.01 / replication bar" · "FRB.05 is consistent but
  not discriminating vs Planck".

---

## 2. How I proceeded (procedure, in order)

1. **Read and separated the hypotheses.** Started from `problem_b.txt` (the
   qualitative "phi-attractor cascade" picture) and then the refined note that
   recast FRBs as a probe of the **boundary-recovery kernel** with a specific
   eigenvalue spectrum. Adopted the firewall (§1) as the governing constraint.
2. **Froze the kernel from the axioms** (`recovery_kernel.py`): the recovery
   ratios are exact `Fraction`s built from `2/3 = |Z₂|/N_fam` and the transport
   exponent `6` — no FRB number and no fitted exponent enters the prediction
   layer (§3).
3. **Preregistered** the search (`hypotheses/frb_tfpt_v1.yaml`): fixed kernel
   ratios, tolerances, null models, per-target success criteria, and the language
   rules. Added guard tests (`tests/test_recovery_kernel_constants.py`, §4) so the
   kernel cannot be edited after seeing data.
4. **Ran a data-acquisition campaign** (§5, and `data/README.md` →
   *Data-acquisition audit*). For each target I went to the primary source
   (VizieR, IOPscience machine-readable supplements, ScienceDB, arXiv ancillary,
   Zenodo, GitHub), recorded what was downloadable anonymously, and what was
   login/supplement-walled. Bundled everything that was cleanly public.
5. **Implemented one test per signature** (§6–§7), each with: a fixed kernel
   ratio (never refit), an explicit **null model** (surrogates or a systematic
   floor), a significance statistic, a `[0,1]` score, and a written success
   criterion.
6. **Hardened the aggregator** (`fingerprint.py`): an `EvidenceAxis` carries
   `status`, `q_value`, `discriminating`, `replicated`. `aggregate_axes` promotes
   an axis to **support** only if it is replicated, discriminating, and `q<0.01`;
   otherwise it stays candidate / null / consistency / data-limited. The overall
   verdict can only become `confirmed` on real support.
7. **Ran deterministically** (`frb-tfpt analyze --seed 0`), wrote
   `results/results.json` + plots, and recorded the verdict (§8). Re-ran after
   each dataset arrival (the FAST 1652 energy table, then the FRB 20240114A
   polarimetry) and updated the axis statuses accordingly.

The two pivotal data events: (a) obtaining the **FAST 1652-burst FRB 20121102A
energy table** turned FRB.02 into a real test; (b) obtaining the **FAST
6134-burst FRB 20240114A polarimetry** turned FRB.04 from `data_limited` into a
real **null**.

8. **v1.1 review response (after an external methodological review).** Added an
   **observable-semantics layer** (`observable_semantics.py`) that forbids testing
   an energy ratio against an amplitude number; this reclassified the FRB.02 8/27
   result as an *audit anomaly* (the theory channels are null). Added: FRB.02
   per-session / leave-one-session-out diagnostics and a second null (local-block
   shuffle); a v2 exploratory RM step-relaxation channel
   (`rm_relaxation_step.py`); a structure-vs-kernel score split; a fix to the
   shared-eigenvalue CI (pair/block bootstrap instead of IID resampling, which had
   collapsed the CI); explicit N-accounting (`n_raw=6134`); a YAML language patch
   (flagged `language_patch_after_results`); and three new guard tests.
9. **v1.2 null-battery completion.** Wired the **four preregistered FRB.04 nulls**
   (stationary-Markov, time-shuffle, block-shuffle, AR(1)-drift; + a Dirichlet
   diagnostic), with a conservative overall p = max over the four and a proper
   **moving-block bootstrap** for the eigenvalue CI (the old IID bootstrap had
   collapsed it). Added two FRB.02 storm/threshold nulls (AR(1)-energy, censoring).
   Added **Package E** (`window_extraction.py`: data-derived HDI windows from
   folded CHIME phases) and **Package G** (`recovery_observable_model.var1_spectrum`:
   a true multivariate VAR(1)). The kernel and targets stayed frozen throughout —
   only readouts, nulls and result-language changed.

---

## 3. Theory coupling — the frozen recovery kernel

Everything below is **derived** from the two TFPT axioms (identical to
`verification/tfpt_constants.py`); no SI value and no FRB number is hard-coded
into `recovery_kernel.py` / `tfpt_ladder.py`.

```
P1   c3    = 1/(8*pi)                 = 0.03978874     (seam/boundary constant)
P2   g_car = 5                                          (carrier rank)
     phi0  = 1/(6*pi) + 3/(256*pi^4)  = 0.05317392     (retained seed)
     N_fam = 3,  |Z2| = 2
```

Two structural ingredients build the **Page / boundary-recovery spectrum**:

- the attractor ratio `2/3 = |Z₂|/N_fam` (the Koide IR attractor; `1/3 = 1/N_fam`);
- the transport exponent `6` = the Z₆/A₃ transport cycle that also sets the gap
  `Δ = 6 ln(3/2) = 2.4327902`.

```
energy channel     spec(T) = { 1, (2/3)^6, (1/3)^6 } = { 1, 64/729,  1/729 }
                                                      = { 1, 0.0877915, 0.00137174 }
amplitude channel  roots   = { 1, (2/3)^3, (1/3)^3 } = { 1, 8/27,    1/27   }
                                                      = { 1, 0.296296, 0.0370370 }
sub-burst channel          = { 1,  2/3,     1/3   }   = { 1, 0.666667, 0.333333 }
```

Why three channels, no new numbers: an **energy/information** observable reads
the eigenvalue `λ`; a **field-amplitude / visibility** observable reads `√λ`
(hence the cube roots `8/27`, `1/27`); a raw **sub-burst** step reads the
unpowered ratio. They are the same kernel under three readouts.

**Seed block (cosmology coupling), same retained seed `phi0`:**

```
beta_rad = phi0/(4*pi)            = 0.00423097 rad = 0.242435 deg
Omega_b  = (4*pi - 1) * beta_rad  = 0.0489410
```

`frb-tfpt audit` prints all of the above as exact fractions + float views.

---

## 4. Preregistration & kernel freeze (anti-exponent-shopping)

- `hypotheses/frb_tfpt_v1.yaml` — the **frozen hypothesis**. Contains the kernel
  ratios (as exact strings `64/729`, `1/729`, `8/27`, `1/27`, `2/3`, `1/3`), the
  tolerances (`tolerance_dex_echo: 0.10`, `tolerance_window_relative: 0.10`), the
  global rules (`no_refitted_exponents`, `require_surrogate_calibration`,
  `require_multi_source_replication`, `single_source_match_is_candidate_only`,
  `q_threshold: 0.01`), the per-target observables / null models / success
  criteria, and the allowed/forbidden language.
- `tests/test_recovery_kernel_constants.py` — 7 guard tests (run with
  `python tests/test_recovery_kernel_constants.py`; pytest optional). They assert:
  (i) the energy/field/step ratios are exact `Fraction`s; (ii) the float views
  equal the fractions; (iii) the prediction layer imports no data module and
  contains **no FRB magic numbers** (denylist: `16.35`, `528.9`, `1652`, `6131`,
  `1539`, source ids, `rad m`, `Jy`); (iv) no symbol named `*fit_exponent*`;
  (v) the YAML ratios equal `kernel_fractions()` exactly. **Status: 7/7 pass.**

---

## 5. Data — exact details (real, public)

`python scripts/fetch_data.py` re-downloads the VizieR + IOPscience tables.
Full provenance + acquisition audit in `data/README.md`.

| File | Source / how obtained | N | Columns used (units) |
|---|---|---|---|
| `frb20121102_fast_li2021_1652.tsv` | Li et al. 2021, Nature 598, 267 — VizieR `J/other/Nat/598.267/tables1` (asu-tsv) | 1652 | `Burst`, `MJD`, `DM`, `Width`, `Bandwidth`, `Fp`, `Fluence`, **`E` (erg)** |
| `FAST_FRB20240114A_pol_catalog_v5.csv` | Wang et al. 2026, arXiv:2603.20663 — ScienceDB `10.57760/sciencedb.Fastro.00040` (free login; user-supplied) | 6134 | `MJD_topo` (d), `RM` (rad m⁻²), `DM`, `Weff` (ms), `Bandwidth` (MHz), `S/N`, `DOL`=L/I (%), `DOC`=V/I (%), `PA_mean` (deg) |
| `frb_dmz_adb84d_table4.txt` | ApJ `10.3847/1538-4357/adb84d` Table A1 (IOP suppdata) | 36 | `z_spec`, `DM_obs`, `DM_MW(disk+halo)`, `DM_host^s` (pc cm⁻³) |
| `frb_dmz_adeb72_table1.txt` | Sharma et al. 2024, ApJ `10.3847/1538-4357/adeb72` Table 1 | 117 | `Redshift`, `DM`, `DM_exc` (pc cm⁻³) |
| `frb_pol_pandhi2024_table1.txt` | Pandhi et al. 2024, ApJ 968, 50 Table 1 (IOP suppdata) | 118 | `RM_obs,FDF`, `RM_MW`, `L/I` |
| `frb20121102_aggarwal2021.tsv` | Aggarwal et al. 2021, ApJ 922, 115 — VizieR `J/ApJ/922/115/table5` | 144 | `S` (Jy ms), `MJD`, `muf`, `DM` |
| `chime_catalog1.tsv` | CHIME/FRB 2021, ApJS 257, 59 — VizieR `J/ApJS/257/59/table2` | 600 | `Fluence`, `MJD400`, `Fpk`, `DMfitb`, `RpName`, `Nsb` |
| *curated in `activity_windows.py`* | CHIME/FRB 2020 (arXiv:2001.10275); Rajwade+2020 (MNRAS 495, 3551) | 2 | `P`, `W_broad`, `W_core` (+ errors), days |

**FRB 20240114A specifics** (the FRB.04 enabler): 6134 bursts spanning
MJD 60337.2–60824.9 = **487.7 d over 95 nights**; `RM` ranges **212.5 → 425.3**
rad m⁻² (the ~200 rad m⁻² secular evolution, span 212.8); `DM` stable
524.4–536.3; `PA_mean` ∈ [−85.1°, +85.7°]. The loader
`load_fast_20240114A_pol` prefers `..._v5.csv` (clean header + full-precision
MJD) over the base CSV and `..._v4.csv` (extra index column).

**Acquisition audit (summary).** The FRB 20240114A catalog is on ScienceDB and
login-walled for anonymous download; I verified that arXiv source (LaTeX +
figures only), DataCite (no `contentUrl`), Croissant/JSON-LD (client-side JS),
the ScienceDB file-tree API (returns `User Not Login` even from the page origin
with cookies), and direct download-id enumeration are all blocked — only a free
account works. Non-login alternatives found but **insufficient** (not bundled):
`SukiYume/RMS` (FRB 20201124A RM, ~32 bursts, single-epoch, no MJD),
FRB 20190520B (Anna-Thomas; code-only on Zenodo, RM table paywalled),
FRB 20240619D (journal/CDS supplement, absent from the arXiv source). Full record
in `data/README.md`.

**Still pending drop-in:** `frb20240619D_wideband.tsv` (1539 bursts;
arXiv:2505.08372) → activates the RM-memory / session-decay / frequency-window
stress tests. Loaders read column aliases from `data_io._COL_ALIASES`; an absent
file makes the dependent axis report `data_limited` rather than guessing.

---

## 6. The TFPT signatures searched

Each signature maps a **fixed** kernel ratio onto an FRB observable. "Channel"
indicates whether the observable reads `λ` (energy), `√λ` (field/visibility), or
the unpowered step.

| ID | Signature | Predicted value(s) | Channel | Observable |
|---|---|---|---|---|
| **FRB.01** | no native (non-plasma) dispersion | `A_TFPT = 0` | — | residual `t(ν)` after DM, scattering removal |
| **FRB.02** | recovery / echo ratios | `E_{n+1}/E_n ≈ 64/729`; amp `8/27`; step `2/3` (+ inverses) | energy / field / step | consecutive within-session energy ratios |
| **FRB.03** | activity-window eigenwidths | `W_broad/P ≈ 8/27`, `W_core/P ≈ 1/27` | field / visibility | periodic-repeater phase-window widths |
| **FRB.04** | PA/RM Markov spectrum (strong μ4/D4) | `spec(T) = {1, 64/729, 1/729}` | energy | per-burst PA-class / RM-residual state transitions |
| **FRB.04b** | RM step-relaxation (**v2 exploratory**) | `spec(T_RM) = {1, 2/3, 1/3}` | step | RM-residual state transitions (env. relaxation, not μ4) |
| **FRB.05** | baryon fraction | `Ω_b = 0.0489` | seed block | Macquart `DM(z)` slope of localized FRBs |
| *generic* | energy cascade | adjacent log-E spacings = a single kernel ratio | energy | GMM cluster centres of one source's energies |
| *shared* | multi-channel recovery memory | same eigenvalue in ≥2 observables | mixed | AR(1) memory of `log E`, `RM_resid`, `log Δt` |

---

## 7. Analysis methods — exact algorithms

All surrogate p-values use the `(1 + #{null ≥ obs}) / (n_surrogate + 1)` estimator.

### FRB.05 — DM(z) baryon test (`dmz_baryon.py`, `cosmology.py`)
- **Model:** Macquart relation
  `⟨DM_cosmic(z)⟩ = (3 c H₀ Ω_b f_IGM χ)/(8π G m_p) · I(z)`,
  `I(z)=∫₀ᶻ (1+z′)/E(z′) dz′`, `E(z)=√(Ω_m(1+z)³+Ω_Λ)`.
  Constants: `Ω_m=0.315`, `Ω_Λ=0.685`, `h=0.674`, `χ=7/8=0.875`, `f_IGM=0.84`.
- **Per FRB:** `DM_cosmic = DM_obs − DM_MW − DM_host_obs` (adb84d uses the
  published budget; Sharma uses `DM_exc` minus a 60/(1+z) pc cm⁻³ host prior).
- **Fit:** one-parameter weighted LSQ of `Ω_b` through the origin vs `I(z)`,
  per-point `σ = √((0.2·DM_cosmic)² + 80²)`; bootstrap `n_boot=2000`.
- **Error:** systematics-dominated — a **15 % floor** is added in quadrature
  (`σ = √(σ_boot² + (0.15·Ω_b)²)`) for f_IGM + host-model uncertainty.
- **Success:** consistency only — `Ω_b(TFPT)=0.0489` vs `Ω_b(Planck)=0.0493`
  differ <1 %, far below FRB scatter, so this can never discriminate TFPT.

### FRB.03 — activity-window population (`periodic_population.py`)
- **Statistic:** per source `W_broad/P` (rel-err to `8/27`), `W_core/P` (to
  `1/27`), with Gaussian error propagation from `P, W_broad, W_core` errors.
- **Nulls:** random duty-cycle windows `~U(0,1)`, `n_null=5000`; the population
  statistic is the median broad rel-err. **Leave-one-out**: does removing any one
  source flip "median rel-err < 0.10"?
- **Success:** `≥5` periodic repeaters, median broad rel-err `<0.10`, `≥3` sources
  with a core window near `1/27`, LOO-stable, and `null q<0.01`. Only 2 robust
  periodic repeaters exist ⇒ best attainable status is **candidate**.

### FRB.02 — semantics-correct echo ratios (`echo_ratio.evaluate_echo_semantic`)
- **Observable split (the v1.1 fix, `observable_semantics.py`):** the raw column
  is *energy* `E` (erg). The consecutive energy ratio `R_E = E_{n+1}/E_n` is tested
  in three explicit channels: **energy** (`R_E` vs `{64/729, 1/729}`),
  **amplitude** (`√R_E` vs `{8/27, 1/27}`, i.e. `R_E` vs `(8/27)²=64/729`), and a
  flagged **audit** channel (`R_E` vs `{8/27, 1/27}` — a *channel mismatch*, never
  theory). Only the energy + amplitude channels feed the axis score.
- **Statistic:** per channel, count `log10`-ratios (and inverses) within
  `±0.10 dex` of each target; enrichment = obs/mean-null; **BH q-values** within
  the channel.
- **Four nulls** (`n_surrogate=1000` each; the conservative max-p is kept):
  within-session energy shuffle, **local-block shuffle** (blocks of 10), an
  **AR(1)-energy "storm" null** (per-session AR(1) in log-energy with matched
  mean/std/lag-1), and a **censoring null** (session lognormal truncated at the
  detection floor).
- **Session diagnostics:** per-session contribution + leave-one-session-out for
  any excess (robust ⟺ no single session >25 % and ≥5 sessions contribute).
- **Success:** `q<0.01`, enrichment `>1.2`, in a **theory** channel, in **≥2
  sources**. A single-source theory-channel excess = candidate; an excess only in
  the audit channel = **audit anomaly, not a candidate**.

### FRB.04 — PA/RM Markov spectrum (`markov_spectrum.py`)
- **States (`n_states=4`):** PA → four D4 sectors `[0,45),[45,90),[90,135),[135,180)`
  after **per-session circular-mean detrending**; RM → cubic-detrended residual
  quantised into 4 equal-occupancy bins.
- **Matrix:** row-stochastic transition matrix; take the two non-trivial
  `|eigenvalues|` (drop the ≈1 stationary one).
- **Comparison:** Euclidean distance of `(λ₂,λ₃)` to the kernel `(64/729, 1/729)`;
  a **moving-block bootstrap CI** on the eigenvalues (`n_boot=800`, block=25 — the
  earlier IID bootstrap scrambled the order and collapsed the CI to 0); and the
  **four preregistered nulls** (`n_null=1000` each), with `null_p = P(d_null ≤
  d_obs)`:
  - *stationary_markov* — random reversible chain with the observed stationary
    distribution; *time_shuffle* — permute the state sequence; *block_shuffle* —
    shuffle blocks of states; *ar1_drift* — quantise a simulated AR(1) with the
    observed lag-1 autocorrelation (the *memory-preserving* null).
  The reported **overall null p = max over the four** (the most permissive null);
  a Dirichlet matrix is kept as a 5th diagnostic.
- **Success:** the bootstrap CI must **contain** the kernel pair **and** overall
  `null p<0.01`. Score `= [CI∋kernel ∧ p<0.01]·exp(−(dist/0.05)²)`.

### FRB.04b — RM step-relaxation (v2 exploratory, `rm_relaxation_step.py`)
- Identical machinery (incl. all four nulls), but the RM-residual transition
  spectrum is compared to the **unpowered step kernel `{2/3, 1/3}`**. **Not
  preregistered against this kernel** → it can never rescue v1 and is promotion-
  locked behind external replication. The **ar1_drift null is decisive**: if a
  smooth AR(1) drift reproduces the proximity, the "match" is environmental
  relaxation, not a discrete spectrum.

### Package E — data-derived windows (`window_extraction.py`)
- Fold a repeater's raw arrival times at its period and compute the windows as
  preregistered **highest-density intervals**: `W_broad/P` = minimal phase arc
  with 90 % of bursts, `W_core/P` = minimal arc with 50 %. Removes the "FRB
  20180916B defines broad/core" circularity. Applied to CHIME FRB 20180916B
  (33 bursts folded at 16.33 d).

### Package G — multivariate VAR(1) (`recovery_observable_model.var1_spectrum`)
- Build the time-ordered, standardised matrix of the available continuous
  observables (e.g. `log_energy, dm_resid` for FAST 1652; `rm_resid, dm_resid,
  pa_sin, pa_cos, linear_frac` for FRB 20240114A), fit `X_{n+1}=A X_n`, and
  compare `|eig(A)|` to the kernel memory set with a row-shuffle null. A kernel
  eigenvalue in `spec(A)` is shared across channels *by construction*; reported
  descriptively (the row-shuffle null is permissive, so this is not promotable).

### FRB.01 — no native dispersion (`no_native_dispersion.py`)
- **Model:** `t(ν)=t₀ + K·DM·ν⁻² + A_scat·ν⁻⁴ + A_TFPT·ν^index`; weighted LSQ;
  **kill test** = `A_TFPT` must be `≤2σ` from 0. Needs per-burst sub-band timing
  (raw/baseband), absent from catalogues ⇒ `raw_data_required`.

### Generic cascade (`energy_clusters.py`)
- **Null fit:** log-normal in energy + KS test. **Multimodality:** Gaussian-
  mixture BIC scan `k=1..6`. **Spacing ladder** (`fit_spacing_ladder`): if `≥3`
  clusters, compare the adjacent log-E spacings to preregistered ratios
  (`(3/2)⁶=729/64`, `(3/2)³=27/8`; audit-only: `3/2`, `2`, `5/3`) within `0.10`;
  smooth-null surrogates `n_surrogate=150`. **Log-periodicity:** Rayleigh power on
  the log-energy axis over spacing ratios `1.3–6.0` (`n_freq=400`), surrogate-
  calibrated (`n_surrogate=400`).

### Shared eigenvalue (`recovery_observable_model.py`)
- **Per observable** (`log_energy`, `rm_residual`, `log_waiting`): AR(1) memory
  coefficient `a` (lag-1 regression), **pair/block-bootstrap** CI (`n_boot=1000`;
  v1.1 fix — IID resampling had scrambled the lag-1 structure and collapsed the
  CI toward 0), nearest kernel memory value in `{2/3, 1/3, 8/27, 64/729}`,
  `delta_to_nearest`, and `kernel_in_a_ci`. **Score rises only if ≥2 channels'
  CIs contain the same kernel value** — coincidences are not stacked.

### Verdict gating (`fingerprint.py`)
- `EvidenceAxis(status, score, p_value, q_value, discriminating, replicated)`;
  `aggregate_axes` → an axis is **support** only if `status==support ∧
  discriminating ∧ replicated ∧ q<0.01`; else it is bucketed candidate / null /
  consistency / data-limited. Overall `confirmed` requires ≥1 support axis.

---

## 8. Results — exact numbers (`--seed 0`)

**OVERALL: `not_confirmed_not_refuted`** — support: none · candidate:
`FRB03_activity_window` · null: `FRB02_echo_ratio`, `FRB04_polarisation` ·
consistency: `FRB05_baryon` · data-limited: `FRB01_dispersion`.

### FRB.05 — baryon `Ω_b` → consistency (non-discriminating), score 1.00
- adb84d (n=36): `Ω_b = 0.0483 ± 0.0072` (stat 0.0001, syst-floored). TFPT
  `0.0489` at **0.1σ**; Planck `0.0493` at 0.1σ.
- Sharma (n=117, constant host prior): `Ω_b = 0.0663 ± 0.0103`; TFPT at 1.7σ.
  The inter-sample spread (0.048 vs 0.066) **is** the host-model systematic.
- Verdict: TFPT consistent with the clean-budget sample; cannot single out TFPT
  from Planck.

### FRB.03 — activity windows → candidate, score 0.66
- Curated FRB 20180916B: `W_broad/P = 0.3058` vs `8/27` (**3.2 %**);
  `W_core/P = 0.0367` vs `1/27` (**0.9 %**). FRB 20121102A misses (78 %).
- **Data-derived (Package E):** folding 33 CHIME bursts at 16.33 d with consistent
  HDIs gives `W_broad/P = 0.137` (**54 %** off 8/27) and `W_core/P = 0.038`
  (**4 %** off 1/27). So the *broad* match was definition-dependent (the 90 % HDI
  is much narrower than the curated "5-day window") and **does not** hold; only the
  *core* window survives at the 4 % level.
- Population: `n=2 < 5` required, random-window null `p=0.112`, leave-one-out **not**
  stable ⇒ candidate, not support — and now weaker for the broad window.

### FRB.02 — echo ratios on FAST 1652 → null, score 0.00
- 1652 bursts, **1611 within-session pairs**, 41 sessions; raw column = `E` (erg);
  **four nulls** (within-session, local-block, AR(1)-energy storm, censoring).
- **Energy channel** (`E_{n+1}/E_n` vs `{64/729, 1/729}`): best **q=1.0** → null.
- **Amplitude channel** (`√(E_{n+1}/E_n)` vs `{8/27, 1/27}`): best **q=1.0** → null.
- **Audit channel** (`E_{n+1}/E_n` vs `{8/27, 1/27}`, *channel mismatch*): under
  the two weaker (v1.1) nulls the `8/27` pile-up reached q≈0.02, but it **does not
  survive the AR(1)-energy storm null** (v1.2): best **q=1.0**. So the `8/27`
  feature was a within-storm energy-memory artefact at the *wrong* channel number.
  **FRB.02 axis = null, audit anomaly gone.**

### FRB.04 — PA/RM Markov spectrum on FRB 20240114A (6134 bursts) → null, score 0.00
- **4-null framework**, conservative overall p = max over the four; N-accounting
  `n_raw=6134, n_used_pa=6133, n_used_rm=6134`.
- **RM channel:** eigenvalues `(0.616, 0.309)` vs kernel `(0.0878, 0.0014)`;
  overall **null p=1.0** (worst null: time_shuffle). RM(t) is a smooth wandering
  drift (330→400→230 rad m⁻²). **Clean null.**
- **PA channel:** eigenvalues `(0.056, 0.022)`; overall **null p=0.49** (worst
  null: block_shuffle) — i.e. a block-shuffle reproduces the PA spectrum, so it is
  **not** special; CI does not contain the kernel. **Null.** (Per-null p:
  stationary 0.001, time 0.003, block 0.49, ar1 0.014.)
- **Strong μ4/D4 prediction not supported.**

### FRB.04b — RM step-relaxation (v2 exploratory) → killed by the AR(1)-drift null
- RM-residual eigenvalues `(0.616, 0.309)` vs the **step kernel** `(0.667, 0.333)`
  (≈7 % each). Memory-destroying nulls give p≈0.001 (the proximity beats them),
  **but the AR(1)-drift null gives p=0.92** — a smooth autocorrelated drift
  reproduces the proximity. Overall **null p=0.92** ⇒ the RM≈`{2/3,1/3}` pattern
  is **environmental relaxation, not a discrete step spectrum**. The intriguing v2
  hint is *explained away*; not promotable.

### Generic / shared (FAST 1652 energies)
- **Structure vs kernel are scored separately:** `structure_score=0.74`
  (log-normal **rejected**, KS p=2e-23; GMM best `k=3`, ΔBIC=315) but
  `kernel_score=0.00`. Cluster centres `log10 E = [37.63, 37.75, 38.52]` → adjacent
  spacings `[0.12, 0.77] dex` (**non-uniform**); closest single ratio `27/8` at
  **77 %** off. ⇒ real structure, **no equal-spaced kernel cascade**. The
  structure_score is deliberately **kept out of** the kernel verdict.
- Shared eigenvalue (pair-bootstrap CIs): `log_energy` AR(1) `a=0.343`,
  CI `[0.289, 0.394]` — which **does contain `1/3=0.333`** (single-channel hint);
  `log_waiting` `a=−0.04`. Only **1** channel ⇒ **no** shared kernel eigenvalue.
- **VAR(1) (Package G):** FAST 1652 `|eig(A)|=[0.341, 0.072]` (leading 2 % from
  `1/3`, echoing the `log_energy` memory); FRB 20240114A `|eig(A)|=[0.757, 0.133,
  0.084, 0.049, 0.038]` (0.757 from the RM drift; `pa_sin` eig 0.084 is 4 % from
  `64/729`). Row-shuffle null p=0.002 is permissive (shuffling kills memory), so
  these are **descriptive, not promotable** — no clean kernel match across ≥2
  sources.
- CHIME sanity: drift downward fraction 0.76 (the ordinary "sad trombone");
  FRB 20180916B folds at 16.33 d with Rayleigh `z=28.7` (timing pipeline OK).

| Macquart Ω_b (FRB.05) | FAST 1652 echo ratios (FRB.02) | PA/RM Markov spectrum (FRB.04) |
|---|---|---|
| ![](results/frb05_macquart.png) | ![](results/frb02_fast_echo_ratio.png) | ![](results/frb04_markov_spectrum.png) |
| **RM(t) staircase (FRB.04)** | **activity windows (FRB.03)** | **fingerprint summary** |
| ![](results/frb04_rm_staircase.png) | ![](results/frb03_population_windows.png) | ![](results/frb_fingerprint_summary.png) |

---

## 9. Red-team rules (enforced in code)

A pattern counts as **support** only if it satisfies **all**: (1) the fixed kernel
ratio, no refitted exponent; (2) surrogate calibration or a realistic systematic
floor; (3) `q < 0.01`; (4) replication in ≥2 independent sources or channels. The
gating in `fingerprint.py` refuses to promote single-source results — both
`FRB02_echo_ratio` and `FRB03_activity_window` stay **candidate** despite nonzero
scores, and `FRB04_polarisation` is **null** despite the PA leading-eigenvalue
near-coincidence.

---

## 10. Reproduce

```bash
cd experiments/frb-tfpt-signatures
. ../tfpt-discovery/.venv/bin/activate            # numpy/scipy/sklearn/matplotlib/pyyaml
for t in tests/test_*.py; do python "$t"; done     # 4 guard files, 21 tests, all pass
PYTHONPATH=src python -m frb_tfpt.cli audit        # print the frozen kernel + ratios
PYTHONPATH=src python -m frb_tfpt.cli analyze --seed 0   # full search -> results/
python scripts/fetch_data.py                       # refresh the VizieR + IOPscience tables
```

Guard tests: `test_recovery_kernel_constants.py` (kernel freeze + no data leak, 7),
`test_observable_semantics.py` (channel mapping, 6), `test_language_rules_current.py`
(post-results language + verdict, 5), `test_n_accounting.py` (6134 accounting, 3).

`analyze` is deterministic at fixed `--seed` (~50 s on the bundled data; all
RNGs and `GaussianMixture(random_state=seed)` are seeded).

---

## 11. Outputs

- `results/results.json` — every number: per-axis results under
  `search_targets` / `generic`, the typed `axes` list, and the `overall` verdict
  buckets.
- Plots: `frb05_macquart.png`, `frb03_population_windows.png`,
  `frb02_fast_echo_ratio.png`, `frb04_markov_spectrum.png`,
  `frb04_rm_staircase.png`, `frb_fingerprint_summary.png`, `frb121102_energy.png`,
  `frb121102_logperiodogram.png`, `frb121102_waiting.png`.

---

## 12. Module layout

```
hypotheses/frb_tfpt_v1.yaml     # frozen preregistration (kernel, nulls, success, language)
tests/                          # 4 guard files, 21 tests (run each: python tests/<f>.py)
  test_recovery_kernel_constants.py   # kernel freeze + no-data-leak (7)
  test_observable_semantics.py        # FRB.02 channel mapping (6)
  test_language_rules_current.py      # post-results language + verdict (5)
  test_n_accounting.py                # 6134 burst-count accounting (3)
src/frb_tfpt/
  recovery_kernel.py     # FROZEN kernel (exact Fractions) + seed block (derived)
  tfpt_ladder.py         # generic cascade ratios (derived)
  observable_semantics.py # FRB.02 channel mapping (energy/amplitude/audit) + guard
  cosmology.py           # Macquart relation E(z), I(z), DM_cosmic, Omega_b fit
  dmz_baryon.py          # FRB.05 Omega_b consistency
  activity_windows.py    # FRB.03 per-source windows (curated, cited, with errors)
  periodic_population.py # FRB.03 population test (LOO + nulls)
  echo_ratio.py          # FRB.02 semantic channels + session diag + BH q + 4 nulls
  markov_spectrum.py     # FRB.04 spectrum: 4 nulls + moving-block bootstrap (kernel arg)
  rm_relaxation_step.py  # FRB.04b v2 exploratory RM step-relaxation {2/3,1/3}
  window_extraction.py   # Package E: HDI activity windows from folded phases
  recovery_observable_model.py  # shared AR(1) (pair bootstrap) + VAR(1) (Package G)
  no_native_dispersion.py       # FRB.01 kill test
  energy_clusters.py     # GMM + log-periodicity + fit_spacing_ladder
  drift_freq.py, timing.py, polarization.py, rm_steps.py
  fingerprint.py         # EvidenceAxis (+observable_semantics_valid) + aggregate_axes
  data_io.py             # all loaders + drop-in repeater column contracts
  cli.py                 # `frb-tfpt audit` / `frb-tfpt analyze`
scripts/fetch_data.py    # re-download the VizieR/IOP datasets
data/  results/          # real catalogues + provenance; generated outputs
```

---

## 13. What would change the verdict

1. **FRB.02 → candidate/support:** a *theory-channel* excess (energy ratio near
   `64/729`, or `√(energy ratio)` near `8/27`) — **not** the audit `8/27` — at
   `q<0.01`, replicated in a second large single-source sample (a second FAST storm
   or FRB 20240619D). The current `8/27` audit anomaly does **not** count.
2. **FRB.04b (v2) → essentially closed:** the RM≈`{2/3,1/3}` proximity is
   reproduced by an AR(1)-drift null (p=0.92), i.e. it is environmental relaxation.
   It would only revive if a second repeater showed the proximity **and** it beat
   the AR(1)-drift null (p<0.01) there — unlikely for a smooth-drift quantity.
3. **FRB.03 → testable:** ≥5 confirmed periodic repeaters with measured
   `P, W_broad, W_core`.
4. **Shared eigenvalue:** the `log_energy` AR(1) ≈1/3 hint (CI contains 1/3)
   appearing in a **second** observable or source (≥2 channels required).

A clean multi-source null is itself a result: it would show FRBs are not a good
carrier of the boundary-recovery kernel. *Nature owes us no drama.*

---

## 14. References

CHIME/FRB Collab. 2021 (ApJS 257, 59); CHIME/FRB Collab. 2020 (Nature 582, 351,
FRB 20180916B period); Li et al. 2021 (Nature 598, 267, FAST 1652 bursts);
Wang et al. 2026 (arXiv:2603.20663; ScienceDB 10.57760/sciencedb.Fastro.00040,
FRB 20240114A polarimetry); Aggarwal et al. 2021 (ApJ 922, 115); Pandhi et al.
2024 (ApJ 968, 50); Sharma et al. 2024 (ApJ 10.3847/1538-4357/adeb72);
localized-FRB DM budget (ApJ 10.3847/1538-4357/adb84d); Rajwade et al. 2020
(MNRAS 495, 3551); Macquart et al. 2020 (Nature 581, 391); FRB 20240619D
(arXiv:2505.08372).

## License

MIT.

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
- **Current verdict (v1.8, deterministic at `--seed 0`):** `not_confirmed_not_refuted`.
  One **candidate** (FRB.03 activity window); seven **nulls** (FRB.02 echo ratio,
  FRB.02b free-quotient, FRB.04 polarisation, FRB.06 pol-fraction, FRB.07 width-echo,
  FRB.08 PA classes, FRB.09 recovery-clock dynamics); two **consistency** axes
  (FRB.05 Ω_b; FRB.01 no-native-dispersion, replicated across 2 sources / 119 bursts).
  **No data-limited axis remains.** No replicated, discriminating *support*.
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
- **v1.3 multi-source replication (Blinkverse DB):** a 10,890-burst multi-source
  database lets the frozen tests run across many repeaters. **FRB.02 is now a clean
  multi-source null across 4 repeaters** (FRB20121102A, 20201124A, 20220912A,
  20230607A — no theory *or* audit excess anywhere), and the **FRB.04 RM spectrum
  is null across 3 sources** (0/3 for both the v1 μ4 spectrum and the v2
  step-relaxation; the AR(1)-drift null reproduces the RM proximity in every
  source). The two single-source candidates are now robust multi-source nulls.
- **v1.7 FRB.09 — the recovery-clock dynamics (the one untested black-hole structure):**
  a gap analysis of the Origin Theory found that every prior axis tests the recovery
  kernel's *eigenvalues* (the ratios), but none tests its **dynamics** — the resummed
  clock `rate(n) = −6 ln(1−n/N_fam)` (verification `v124`). FRB.09 adds the two
  firewall-compliant predictions that follow: **(A) the wall** — a recovery cascade
  diverges at `n=N_fam=3`, so monotone-decay burst runs must be **capped at length 3**
  (long cascades suppressed vs a within-session energy shuffle); **(B) the
  acceleration** — within a 3-burst cascade the gaps obey `g1/g2 = ln3/ln(3/2) =
  2.7095`. Across 4 sources (FAST 1652 + Blinkverse FRB 20121102A/20201124A/20220912A)
  both are a **clean null** (wall 0/4, acceleration 0/4), with a placebo of arbitrary
  gap ratios confirming the clock value is not special. The horizon-*direct*
  structures (Hod QNM `ln3`, Hawking power `1920`) are deliberately **outside the
  firewall** — the theory says FRBs are not direct Hawking emission, so they are not
  expected and not tested here.
- **v1.6 FRB.01 scaled to many bursts / multiple sources (large archives):** the two
  multi-GB raw archives in `new-data/` are streamed **member-by-member in-memory**
  (no 14 GB unpack) by `scripts/extract_ar_toas.py`: the **FRB 20201124A** tar.gz
  (1863 PSRCHIVE `.ar`) and the **FRB 20240114A** morphology zip (2729 `.ar`). This
  turns FRB.01 from 2 bursts into **119 usable bursts across 2 sources**
  (FRB 20121102A ×2 from the `.calibP`, FRB 20201124A ×117; the FRB 20240114A
  morphology archives are curated narrow-band/drift cut-outs and yield **0** bursts
  with ≥5 broadband sub-bands — an honest data limit, documented below). The test is
  also re-framed around the **physical arbiter**: the fitted non-plasma term
  `A_TFPT·ν⁻³` implies an extra **cross-band delay**, which is compared to the
  per-burst **ToA precision**. In *both* sources the implied delay is ~10⁻¹⁹–10⁻²⁰ s
  vs a ~5×10⁻⁵ s ToA floor (worst delay/precision ≈ 3×10⁻¹⁵) ⇒ **no native dispersion
  is required** ⇒ **consistency**, now **replicated across 2 sources**. (The bare
  `A_TFPT` coefficient is units-sensitive over the narrow FAST band, where ν⁻², ν⁻³,
  ν⁻⁴ are near-collinear; the implied-delay test is robust to that degeneracy.)
- **v1.5 FRB.01 on real waterfalls (no more `data_limited`):** raw PSRCHIVE/PSRFITS
  archives (read with astropy, no PSRCHIVE needed) yield bright single-burst
  dynamic spectra. The no-native-dispersion kill test is run as a **cross-burst /
  cross-source universality** test: a real propagation term would give the *same*
  A_TFPT (and a measurable common delay) in every source, but the per-source values
  imply delays far below the ToA precision ⇒ the residual is **intrinsic
  drift / DM-fit leakage, not a universal non-plasma delay** ⇒ **consistent** with
  TFPT's shared Lorentz cone. **Every axis is now tested on real data**
  (`data_limited_axes` is empty).
- **v1.4 overlooked-signature sweep (3 new tests, all null):** previously unused
  channels were tested — **FRB.06** polarisation-degree vs the kernel fractions
  {2/3,1/3,8/27,1/27} (a placebo-control kills a thin-tailed-null artifact at
  |V|/I≈2/3); **FRB.07** width-relaxation echo vs the step kernel {2/3,1/3}; and
  **FRB.08** static PA μ4 angle-classes. All three are nulls — though FRB.08 finds
  *significant* PA structure at the **m=2 (orthogonal-mode) fundamental, not the
  μ4 m=4** prediction. Net: more channels searched, no new TFPT signature.

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
| `blinkverse_bursts.csv` | **Blinkverse FRB DB** (user export) — multi-source | 10,890 | `source`, `mjd`, `energy`, `fluence`, `rm_qufit`/`rm_syn`, `polar_l`/`polar_c`, `width`, `freq_*` |
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
| **FRB.02b** | free-quotient null (**anti-numerology**) | free `q*∈[0.01,0.5]` must land on `8/27`/`1/27` or lose to M0 | amplitude | LEE-corrected scan of the best free echo quotient + injection recovery |
| **FRB.03** | activity-window eigenwidths | `W_broad/P ≈ 8/27`, `W_core/P ≈ 1/27` | field / visibility | periodic-repeater phase-window widths |
| **FRB.04** | PA/RM Markov spectrum (strong μ4/D4) | `spec(T) = {1, 64/729, 1/729}` | energy | per-burst PA-class / RM-residual state transitions |
| **FRB.04b** | RM step-relaxation (**v2 exploratory**) | `spec(T_RM) = {1, 2/3, 1/3}` | step | RM-residual state transitions (env. relaxation, not μ4) |
| **FRB.05** | baryon fraction | `Ω_b = 0.0489` | seed block | Macquart `DM(z)` slope of localized FRBs |
| **FRB.06** | polarisation-degree quantisation (**new**) | L/I, \|V\|/I near `{2/3,1/3,8/27,1/27}` | fraction | per-burst linear / circular fractions |
| **FRB.07** | width-relaxation echo (**new**) | `W_{n+1}/W_n ≈ 2/3` or `1/3` | step | consecutive within-session widths |
| **FRB.08** | static PA μ4 classes (**new**) | 4 PA classes 45° apart | μ4 angle | per-burst PA values (Rayleigh m=4) |
| **FRB.09** | recovery-clock dynamics (**new**) | cascade length ≤ `N_fam=3`; gap ratio `g1/g2 = ln3/ln(3/2) ≈ 2.71` | time | within-session monotone-decay cascades: run length + gap ratio |
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

### FRB.06 — polarisation-degree quantisation (`pol_fraction.py`, NEW)
- Do `L/I` or `|V|/I` pile up at a kernel fraction `{2/3,1/3,8/27,1/27}`? **Null:**
  a smooth Beta fitted to the same fractions. **Placebo control (essential):** the
  same test at a grid of 22 *non-kernel* control fractions; a kernel value counts
  only if `p<0.05` **and** its enrichment exceeds the 90th-percentile control
  enrichment — so a thin-tailed-null misfit (which inflates the count at *every*
  high fraction, e.g. the rare-high-`|V|` tail near 2/3) cannot fake a signal.
  Multi-source. (Firewall: `L/I` is propagation-affected.)

### FRB.07 — width-relaxation echo (`width_echo.py`, NEW)
- Consecutive within-session **width** ratios vs the **step kernel** `{2/3,1/3}`
  (and inverses) — width is a timescale, so the channel is fixed up front (no
  energy/amplitude ambiguity). Within-session + local-block shuffle nulls, BH q.
  Multi-source.

### FRB.08 — static PA μ4 classes (`polarization.pa_angle_classes`, NEW wiring)
- A Rayleigh test (PA period 180°) for the *fundamental* number of equally-spaced
  PA classes. μ4 predicts the fundamental `m=4` (45° spacing). Returns the
  smallest significant `m`; counts as a μ4 match only if that fundamental is 4.

### FRB.02b — free-quotient null (`free_quotient.py`, NEW, anti-numerology gate)
- The central numerology guard for the echo channel. On within-session **amplitude**
  ratios it compares three models: **M0** (no echo), **M_fixed** (echo at the frozen
  `q∈{8/27,1/27}`), **M_free** (echo at a free `q*∈[0.01,0.5]`). The free quotient is
  scanned on a log grid; the **look-elsewhere-corrected** max-`z` (vs within-session
  shuffle surrogates) gives M_free's global p-value.
- **Decision:** if M_free is significant but `q*` is *not* a kernel value → **NOT TFPT**
  (the free template wins elsewhere); if `q*` coincides with `8/27`/`1/27` → consistent;
  if nothing is significant → M0. An **injection-recovery** check confirms the scan
  recovers `q*≈8/27` when a real echo at that quotient is injected.
- **Result:** M0 in all 4 sources (best `q*` not at a kernel value; LEE p ≥ 0.31);
  injection recovery validates the method (recovers `q≈0.290 ≈ 8/27`). No FRB echo
  result is admissible unless the free quotient first fails to beat the fixed TFPT one.

### FRB.09 — recovery-clock dynamics (`recovery_clock.py`, NEW)
- Tests the recovery kernel's **dynamics** (the resummed clock
  `rate(n) = −6 ln(1−n/N_fam)`, verification `v124`), not its eigenvalues. Two
  firewall-compliant sub-tests on within-session, time-ordered burst sequences
  (energy + MJD):
  - **(A) the wall.** Maximal **strictly-decreasing-energy** runs (recovery
    cascades) must be capped at `N_fam=3` elements. Statistic: number of cascades
    longer than 3; a TFPT wall is a *deficit* vs a within-session energy shuffle
    (`p_deficit = (1+#{null ≤ obs})/(n+1)`, support iff `p<0.05` and enrichment `<1`).
  - **(B) the acceleration.** For monotone-decay **triplets** the gap ratio
    `g1/g2` must pile up at the clock value `ln3/ln(3/2) = 2.7095`. Calibrated
    against the same within-session energy shuffle **and a placebo** of arbitrary
    non-clock ratios `{1.7, 2.2, 3.3, 4.5}`; an excess counts only if it beats both
    the null (`p<0.05`, enrichment `>1.2`) *and* every placebo ratio.
  - Multi-source (FAST 1652 + Blinkverse 20121102A/20201124A/20220912A); a sub-test
    is "replicated" only if supported in ≥2 sources.
- Deliberately **out of scope** (horizon-direct, outside the firewall): the Hod
  quasinormal `ω_R/T_H = ln3` ringdown and the Hawking power `1920 = |W(D₅)|` — the
  theory states FRBs are not direct Hawking emission, so these are not expected in
  FRB data and are not tested here.

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

### FRB.01 — no native dispersion (`psrfits.py` + `dispersion.py`, NOW on real data, multi-source)
- **Raw input:** PSRCHIVE `.calibP` / `.ar` / PSRFITS `.fits` single-burst archives
  read with **astropy** (`read_archive`, no PSRCHIVE), calibrated to a Stokes-I
  dynamic spectrum. `read_archive` accepts a path **or an in-memory file object**,
  so the multi-GB repeater archives are streamed member-by-member without unpacking.
- **Two extractors → one tiny table** (`data/frb01_subband_toas.csv`, reproducible
  without the ~14 GB raw):
  - `scripts/extract_subband_toas.py` — the bright `.calibP` FRB 20121102A bursts;
  - `scripts/extract_ar_toas.py` — streams `FRB20201124A.tar.gz` (1863 `.ar`) and
    `FRB20240114A_Morphology_*.zip` (2729 `.ar`), samples across each campaign,
    keeps bursts with ≥5 sub-bands above S/N 5.5 (≤150/source), and **appends** the
    `.ar` rows while preserving the `.calibP` rows.
- **Sub-band ToAs:** the band is split into ≤12 sub-bands (window adaptive to the
  archive length); each sub-band's peak time is measured with a parabolic refinement
  and an S/N-based error; non-finite/zero-error sub-bands are rejected.
- **Model:** `t(ν)=t₀ + K·ν⁻² + A_scat·ν⁻⁴ + D·ν(intrinsic drift) + A_TFPT·ν^index`,
  fit per burst with floored inverse-variance weights (no infinite weights).
- **Two complementary tests** in `frb01_universality`:
  1. **Implied delay vs. precision (the physical arbiter):** the fitted
     `A_TFPT·ν⁻³` term implies an extra **cross-band delay**
     `|A_TFPT|·|ν_lo⁻³−ν_hi⁻³|`, compared to that source's median **ToA precision**.
     If the implied delay is below precision in *every* source, no native dispersion
     is *required*. This is robust to the narrow-band coefficient degeneracy (over
     1000–1500 MHz, ν⁻², ν⁻³, ν⁻⁴ are near-collinear, so the bare `A_TFPT` value is
     units-sensitive — the *delay* is not).
  2. **Cross-source universality:** a real propagation term is the **same A_TFPT for
     every source** (different DM, redshift, telescope). A_TFPT is aggregated per
     source and tested for a common non-zero value. A common non-zero term whose
     **delay exceeds precision in all sources** would be a genuine **kill** of this
     firewall.
- *Caveat:* the FRB 20240114A morphology release is a curated narrow-band / drifting
  cut-out set (192 phase bins, signal in a few channels), so it yields **0** bursts
  with enough broadband sub-bands — FRB.01 currently rests on FRB 20121102A +
  FRB 20201124A.

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

### Multi-source replication (v1.3, Blinkverse DB)
- **FRB.02 — clean multi-source null across 4 repeaters.** The semantics-correct
  echo test on FRB20121102A, FRB20201124A, FRB20220912A, FRB20230607A shows **no
  theory-channel and no audit-channel excess in any source** (`multi_source_echo`).
- **FRB.04 RM — null across 3 sources.** FRB20240114A, FRB20201124A, FRB20220912A:
  **0/3** for the v1 μ4 spectrum and **0/3** for the v2 step-relaxation; per-source
  AR(1)-drift null p = 0.92 / 1.0 / 0.85 ⇒ the RM≈`{2/3,1/3}` proximity is smooth
  drift everywhere. The PA channel stays single-source (only FRB20240114A has PA).

### FRB.01 — no native dispersion (v1.6) → consistency, **replicated across 2 sources**
- **119 usable bursts / 2 sources** from the raw archives: FRB 20121102A (×2,
  `.calibP`) and FRB 20201124A (×117, streamed from the 892 MB `.ar` tar). The
  FRB 20240114A morphology zip (2729 `.ar`) yields 0 broadband-timing bursts (narrow
  band) — an honest data limit.
- **Implied non-plasma delay ≪ ToA precision in both sources:**

  | source | bursts | A_TFPT (ν⁻³) | implied cross-band delay | ToA floor | delay/precision |
  |---|---|---|---|---|---|
  | FRB 20121102A | 2 | 3.7×10⁻¹⁰ | 1.7×10⁻¹⁹ s | 5.6×10⁻⁵ s | 3.1×10⁻¹⁵ |
  | FRB 20201124A | 117 | 4.3×10⁻¹¹ | 2.7×10⁻²⁰ s | 5.2×10⁻⁵ s | 5.1×10⁻¹⁶ |

  The fitted non-plasma term implies an extra delay **~15 orders of magnitude below
  the measurement precision** in *both* sources ⇒ **no native dispersion is
  required** ⇒ **consistent** with TFPT's shared Lorentz cone, now **replicated**.
  A common non-zero term with an above-precision delay across sources would have
  *failed* this kill test; it does not. (The per-source A_TFPT *coefficients* differ
  and are individually tiny — within-source DM-fit leakage over the near-collinear
  ν⁻²/ν⁻³/ν⁻⁴ FAST band — which is exactly why the **delay**, not the coefficient,
  is the arbiter.)

### FRB.09 — recovery-clock dynamics (v1.7) → null across 4 sources
- **(A) the wall:** monotone-decay cascades are **not** suppressed (per-source
  `enrichment ≈ 0.9–1.25`, `p_deficit = 0.29–0.98`) — if anything FAST 1652 has a
  mild *excess* of long descending runs (slow within-storm drift), the opposite of a
  wall. **0/4 sources.**
- **(B) the acceleration:** the gap ratio `g1/g2` shows no excess at the clock value
  `2.7095` that survives the placebo (e.g. FRB 20201124A reaches enrichment 1.40 but
  an arbitrary ratio reaches 1.30 with `p=0.18`; FAST 1652 enrichment 1.34 vs placebo
  1.51). **0/4 sources.**
- ⇒ the recovery-clock leaves **no trace** in burst timing: `wall null (0/4),
  acceleration null (0/4)`. A clean, firewall-expected negative.

### Overlooked-signature sweep (v1.4) — all null
- **FRB.06 (polarisation degree):** across FRB20240114A, 20201124A, 20220912A, **no
  kernel fraction stands out above the control fractions**. A naive Beta-null run
  flagged `|V|/I≈2/3` (enrichment ~4–5, replicated in 2 sources), but the placebo
  control (arbitrary fractions reach even higher enrichment in the heavy `|V|`
  tail) shows it is a **null-model artifact**, not a 2/3 signature. → null.
- **FRB.07 (width relaxation):** clean null across FRB20121102A, 20201124A,
  20220912A (no BH q<0.05 width-step excess; up to 2813 within-session pairs).
- **FRB.08 (PA μ4 classes):** the PA of FRB20240114A is **significantly structured
  (p≈0)** but the *fundamental is m=2* (orthogonal-mode, 90° PA jumps — a known
  emission/propagation effect), **not the μ4 m=4** prediction. → null for μ4.

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
  psrfits.py             # PSRCHIVE/PSRFITS archive reader (astropy; calibrated Stokes)
  dispersion.py          # FRB.01 sub-band ToAs + cross-burst universality kill test
  multi_source.py        # multi-source replication (FRB.02 echo, FRB.04 RM) across repeaters
  pol_fraction.py        # FRB.06 polarisation-degree vs kernel fractions (+ placebo control)
  recovery_clock.py      # FRB.09 recovery-clock dynamics (cascade wall + accelerating gaps)
  free_quotient.py       # FRB.02b free-quotient null (M0/Mfixed/Mfree + injection recovery)
  width_echo.py          # FRB.07 width-relaxation echo vs step kernel {2/3,1/3}
  window_extraction.py   # Package E: HDI activity windows from folded phases
  recovery_observable_model.py  # shared AR(1) (pair bootstrap) + VAR(1) (Package G)
  no_native_dispersion.py       # FRB.01 kill test
  energy_clusters.py     # GMM + log-periodicity + fit_spacing_ladder
  drift_freq.py, timing.py, polarization.py, rm_steps.py
  fingerprint.py         # EvidenceAxis (+observable_semantics_valid) + aggregate_axes
  data_io.py             # all loaders incl. Blinkverse multi-source + drop-in contracts
  cli.py                 # `frb-tfpt audit` / `frb-tfpt analyze`
scripts/fetch_data.py    # re-download the VizieR/IOP datasets
scripts/extract_subband_toas.py  # FRB.01 sub-band ToAs from bright .calibP bursts
scripts/extract_ar_toas.py       # FRB.01 sub-band ToAs streamed from the multi-GB .ar archives
data/  results/          # real catalogues + provenance; generated outputs
new-data/                # raw PSRCHIVE archives (gitignored; ToA CSV is the committed artifact)
```

---

## 13. What would change the verdict

1. **FRB.02 → essentially closed (now a 4-source null):** a *theory-channel*
   excess (energy ratio near `64/729`, or `√(energy ratio)` near `8/27`) would have
   to appear at `q<0.01` and **replicate across ≥2 repeaters**; it currently
   appears in **none** of the four tested. The audit `8/27` does not count and is
   itself gone under the storm null.
2. **FRB.04b (v2) → closed across 3 sources:** the RM≈`{2/3,1/3}` proximity is
   reproduced by an AR(1)-drift null in **all three** repeaters (it is environmental
   relaxation). Revival would need a repeater where it beats the AR(1)-drift null
   (p<0.01) — not seen.
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

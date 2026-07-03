# fixed-point-watchdog — TFPT exact fixed points: zero-drift kill tests

**Status: armed, not triggered — A `tension`, B `consistent`, C `consistent`, D `consistent`,
E `consistent`, F `consistent`, G `tension` (2026-07-03).**

TFPT predicts several observables as **exact fixed points**. They are not fit parameters:
any confirmed deviation kills the corresponding branch (or, for the compiler outputs, the
theory). The seven fixed points under watch:

1. `w = −1` exactly — dark energy is a true cosmological constant (Λ/H₀ engine).
2. `Σm_ν = 0.0588 eV` — the normal-ordering floor `m₃(1+√|J|)`, `m₁ ≈ 0` (ledger v272/v468).
3. `α⁻¹ = 137.0359992168`, **constant in time** (`α̇/α = 0`; v3).
4. Koide `Q = 2/3` exactly, from the charged-lepton pole masses.
5. The **α–Λ lock**: `ρ_Λ/M̄_Pl⁴ = (3/4π²)·e^(−2α⁻¹)` (v60/v274), which locks the drifts:
   `d ln ρ_Λ/dt = 2α⁻¹·(α̇/α)` — a fractional α drift is amplified by `2α⁻¹ ≈ 274.07` in Λ.
6. `N_fam = 3` exactly — the compiler (`D5 ⊕ A3 + μ4 ⇒ E8`) leaves **no spare slot for a
   4th light family/sterile state**, so TFPT *requires* every short-baseline anomaly to
   dissolve.
7. `λ_C = √(φ₀(1−φ₀)) = 0.2243762` exactly + **exact CKM first-row unitarity** (frozen v84
   assembly) — this fixes `V_ud = 0.97450` and, via the Czarnecki–Marciano–Sirlin master
   formula, a **parameter-free neutron lifetime** `τ_n = 4906.4 s / (V_ud²(1+3g_A²))`
   (axis E). The same no-slot counting as (6) forbids a light dark state, i.e. the
   `n → χ` dark-decay exit of the beam–bottle puzzle.

## Seven test axes (all from public published values)

### A. Σm_ν × w pincer — verdict `tension`

DESI DR2 + CMB squeeze the joint TFPT point `(w=−1, Σm_ν=0.0588 eV)` from both sides,
and the squeeze is **model-dependent** — so both readings are computed:

- **ΛCDM reading** (`w=−1` held, as TFPT demands): the effective-mass posterior
  `Σm_ν,eff = −0.101 +0.047/−0.056 eV` puts the TFPT floor at **+3.1σ** (the paper's own
  number vs the 0.059 eV oscillation floor: 3.0σ). The floor still sits *inside* the
  standard 95% bound (0.0588 < 0.0642 eV) but *outside* the boundary-corrected
  Feldman–Cousins bound (0.053 eV).
- **w0waCDM reading**: the ν bound relaxes to 0.163 eV and the effective-mass posterior
  peaks at 0 — the TFPT floor is fully compatible (**+0.65σ**). But then `(w0,wa)=(−1,0)`
  itself is disfavoured at **3.1–4.4σ** (2-D Gaussian distance 3.07/3.87/4.37σ; published
  2.8/3.8/4.2σ per SN sample — validates the inputs). Joint (3 dof) ≈ **3.7σ** equivalent.

The pincer: **no published model reading lets both fixed points sit below ~3σ at once.**
Honest caveats: Gaussian approximations of published posteriors; Σm_ν bounds are
model-dependent; the three SN compilations overlap and are never stacked (same rule as
`dark-energy-w-watchdog`).

### B. α–Λ lock — verdict `consistent` (and a built-in mutual exclusion)

- PTB Yb⁺ E3/E2 optical clocks: `α̇/α = 1.8(2.5)×10⁻¹⁹/yr` (Filzinger et al., PRL 130,
  253001 (2023) — still the strictest published limit). Consistent with zero, exactly as
  TFPT demands.
- Through the lock, this bounds `|d ln ρ_Λ/dt| < ~1.4×10⁻¹⁶/yr` (2σ).
- If the DESI DR2 `(w0,wa)` preference were **real** dark-energy dynamics, the implied
  drift today is `|d ln ρ_DE/dt| = 3|1+w0|·H₀ ≈ 3.4–6.9×10⁻¹¹/yr` — via the lock that
  would require `α̇/α ≈ 1.2–2.5×10⁻¹³/yr`, violating the clock bound by a factor
  **~2.4–5.0×10⁵ (~5.7 orders of magnitude)**.

So the lock makes "TFPT + real w(z) evolution" **internally impossible**: TFPT stands or
falls with the joint point (`w=−1` *and* `α` static). If the DESI evolution is ever
confirmed as real DE dynamics, axis B kills the lock immediately — no new experiment
needed beyond the clocks we already have.

### C. Koide-τ kill window — verdict `consistent`

- `Q = 0.666664463 ± 5.08×10⁻⁶` from CODATA-2022 `m_e`, `m_μ` + PDG 2024/2025
  `m_τ = 1776.93 ± 0.09 MeV` → pull **−0.43σ** vs 2/3 (σ_Q is entirely τ-dominated).
- `Q = 2/3` predicts `m_τ = 1776.9690 MeV` (±0.00004 from `m_e`, `m_μ`).
- PDG 2024/2025 central: −0.43σ; Belle II 2023 (1777.09 ± 0.14): +0.86σ. Both consistent.
- **Kill window**: a 5σ kill needs `|m_τ − 1776.9690| ≥ 5σ(m_τ)`. At the current PDG
  central (gap 0.039 MeV) that means `σ(m_τ) < 0.008 MeV`; at the Belle II central
  (gap 0.121 MeV), `σ(m_τ) < 0.024 MeV`. Belle II's full dataset targets
  O(0.01–0.05) MeV — the window is live this decade.

### D. Sterile-neutrino dissolution (`N_fam = 3`) — verdict `consistent`

`N_fam = 3` is an exact compiler output, so TFPT does not merely *survive* the death of
the sterile-neutrino hypothesis — it **requires** every short-baseline anomaly to
dissolve. Front-by-front status (2025/26):

- **MicroBooNE two-beam** (Nature 648, 64–69 (2025), arXiv:2512.07159): excludes the
  single light sterile (3+1) interpretation of the LSND and MiniBooNE anomalies at
  **95% CL** and rules out a significant portion of the gallium/BEST parameter space —
  the first use of two accelerator beams (BNB 0.57% intrinsic ν_e, NuMI 4.6%) to break
  the ν_e appearance/disappearance degeneracy.
- **Gallium/BEST**: the ~20% counting deficit itself **persists unexplained**
  (SAGE/GALLEX + BEST 2022, `R_in = 0.79 ± 0.05`, `R_out = 0.77 ± 0.05`, ≳4–5σ
  combined) — but BEST sees *no distance dependence* (no oscillation signature), and
  the large mixing a sterile explanation needs is disfavoured by solar/reactor data.
- **JSNS²** (arXiv:2602.06274, first results 2026): direct LSND test, 2 events observed
  vs 2.3 ± 0.4 expected background (LSND would add 1.1 ± 0.5) — no excess, not yet
  conclusive; JSNS²-II near+far running since Nov 2025.
- **SBN program**: ICARUS first results (Apr 2026) see no ν_μ disappearance (90% CL
  limits on 3+1); the joint SBND+ICARUS analysis will decide this decade.

The dissolution prediction is being confirmed; the unexplained gallium deficit is the
honest caveat (a deficit without an oscillation signature is not a sterile signal).

### E. Cabibbo dissolution + parameter-free neutron lifetime — verdict `consistent`

The Cabibbo axis named on 2026-07-03 (third dissolution axis), now implemented — **plus a
new leg that had never been written down**: the beam–bottle neutron-lifetime puzzle.

- **First row**: PDG26 `|V_ud|²+|V_us|²+|V_ub|² = 0.9983(7)` (+2.4σ deficit) must dissolve
  (the frozen assembly is exactly unitary). TFPT says *where*: `λ_C` sits at **+0.08σ** on
  the PDG26 kaon average (S=2.5), *between* Kl3 (+2.03σ) and the Kμ2 route (−1.63σ) — the
  two kaon routes must converge onto 0.22438. On the `V_ud` side, **superallowed 0⁺→0⁺ is
  the outlier (+2.58σ)** while every neutron/pion route agrees with the TFPT-unitarity
  value 0.97450 (<1σ): the deficit resolves on the nuclear-structure/RC side.
- **Neutron lifetime (new)**: `V_ud = 0.97450` (exact) + `g_A = 1.27641(56)` (PERKEO III)
  in the CMS master formula `|V_ud|²·τ_n·(1+3g_A²) = 4906.4(1.7) s` gives

  ```
  τ_n(TFPT) = 877.53 ± 0.71 s        (σ from the master-formula constant + g_A only)
  ```

  Confrontation: UCNτ final (bottle) 877.82±0.30 → **−0.38σ**; magnetic/grav storage
  average 878.15±0.20 → −0.85σ; **beam average (proton counting) 888.1±2.0 → −4.98σ**;
  J-PARC *electron-counting* beam 877.2±1.7+4.0/−3.6 → +0.08σ. TFPT takes the **bottle
  side** of the ~4σ beam–bottle puzzle with no dial, predicts the proton-counting beam
  result carries a systematic, and — via the `N_fam=3` no-slot counting — **forbids the
  `n → χ` dark-decay explanation** of the split. Deciders: NIST BL2/BL3, J-PARC full
  dataset, τSPECT; plus PIONEER, lattice `f₊(0)`, superallowed NS/RC re-evaluations for
  the first row.

### F. X17 dissolution — verdict `consistent`

No E8 slot for a ~17 MeV boson with the required couplings → the ATOMKI anomaly family
(⁸Be/⁴He/¹²C internal-pair peaks, `M_X = 16.85(4)` MeV) must dissolve. Status 2025/26:
**MEG II** (EPJ C 85 (2025) 763) finds **no signal** in the same ⁷Li(p,e⁺e⁻)⁸Be reaction
(90% CL limits `R_17.6 < 1.8×10⁻⁶`, `R_18.1 < 1.2×10⁻⁵`; still ~1.5σ compatible with the
ATOMKI combination per Barducci+ JHEP 04 (2025) 035 — not yet a kill); **PADME Run III**
(JHEP 11 (2025) 007) resonant `e⁺e⁻` scan is background-consistent except a **1.8–2.0σ
global** excess at 16.90 MeV. PADME Run IV (upgraded tracker, 2025/26) is the decisive
dataset. Kill: a confirmed ≥5σ X17 resonance replicated outside ATOMKI.

### G. R_D(*) lepton-universality dissolution — verdict `tension`

The frozen CKM assembly is exactly unitary and the compiler leaves no light charged
mediator (leptoquark/W′) — `b → cτν` universality must return to SM. HFLAV CKM 2025:
`R(D) = 0.358±0.024` (+2.5σ), `R(D*) = 0.281±0.011` (+2.2σ), **combined 3.8σ** (3.5σ with
FLAG24 lattice SM) — the most significant currently-standing dissolution target of this
watchdog. Belle II full dataset + LHCb Run 3 decide. Kill: a ≥5σ confirmed excess with
independent tagging and consolidated SM form factors.

## Run

```bash
. experiments/tfpt-discovery/.venv/bin/activate
cd experiments/fixed-point-watchdog && PYTHONPATH=src python -m tfpt_fixedpoint.cli analyze
```

Deterministic; writes `results/results.json`.

## Data sources (`data/measurements.json`, retrieved 2026-07-02)

- **DESI DR2 neutrino constraints**: Elbers et al., arXiv:2503.14744 (2025) — ΛCDM
  `Σm_ν < 0.0642 eV` (95%), Feldman–Cousins `< 0.053 eV`, effective-mass posterior
  `−0.101 +0.047/−0.056 eV`; w0waCDM `< 0.163 eV`, eff. posterior `0.000 +0.10/−0.081 eV`.
- **DESI DR2 CPL fits**: DESI DR2 Results II, arXiv:2503.14738 (2025) — same `(w0,wa)`
  values as `experiments/dark-energy-w-watchdog` (2.8/3.8/4.2σ per SN sample).
- **α-drift clock limit**: Filzinger et al., PRL 130, 253001 (2023), arXiv:2301.03433.
- **Lepton masses**: CODATA 2022 (`m_e`, `m_μ`); PDG 2024 + 2025 update
  (`m_τ = 1776.93 ± 0.09 MeV`, S. Navas et al., PRD 110, 030001); Belle II
  arXiv:2305.19116 (`1777.09 ± 0.08 ± 0.11 MeV`).
- **Short-baseline sterile status**: MicroBooNE, Nature 648, 64–69 (2025),
  arXiv:2512.07159; BEST 2022 gallium ratios; JSNS² arXiv:2602.06274 (2026);
  Fermilab SBN/ICARUS first results (Apr 2026).
- **Neutron lifetime** (retrieved 2026-07-03): UCNτ final arXiv:2409.05560; beam/bottle
  averages per the Symmetry 16 (2024) 956 review; J-PARC electron-counting beam
  arXiv:2412.19519; master formula `|V_ud|²τ_n(1+3g_A²) = 4906.4(1.7) s`
  (arXiv:1907.06737 eq. 49); `g_A = 1.27641(56)` PERKEO III (arXiv:1812.04666).
- **Cabibbo/first row** (retrieved 2026-07-03): PDG 2026 rev. "Vud, Vus, the Cabibbo
  Angle, and CKM Unitarity" — same frozen table as
  `experiments/tfpt-discovery/electron_sector_cabibbo_probe.py`.
- **X17** (retrieved 2026-07-03): MEG II EPJ C 85 (2025) 763 (arXiv:2411.07994); PADME
  Run III JHEP 11 (2025) 007; Barducci et al. JHEP 04 (2025) 035; ATOMKI PRL 116 042501,
  PRC 104 044003, PRC 106 L061601.
- **R_D(*)** (retrieved 2026-07-03): HFLAV CKM 2025 averages (incl. LHCb PRL 134 061801
  and Belle II PRD 112 032010).

## Verdict enums and kill rules

Per axis: `consistent | tension | data_limited`. Frozen kill rules:

```
A: joint (w=-1, Sigma m_nu=0.0588 eV) excluded at >= 5 sigma under BOTH model readings
   (LCDM-nu AND w0waCDM) in a single systematics-controlled combination.
B: any confirmed alpha_dot/alpha != 0, or a confirmed Lambda drift violating
   d ln rho_Lambda/dt = 2 alpha^-1 d ln alpha/dt.
C: |m_tau - m_tau(Q=2/3)| >= 5 sigma(m_tau), systematics-controlled.
D: any confirmed sterile oscillation signal at >= 5 sigma (systematics-controlled;
   e.g. joint SBND+ICARUS or JSNS2-II).
E: converged all-route V_us (S~1) with |V_us - 0.224376| >= 5 sigma; OR a
   systematics-converged first-row deficit >= 5 sigma; OR a confirmed beam-bottle split
   established as real new physics (dark decay) at >= 5 sigma; OR bottle tau_n drifting
   >= 5 sigma from 877.5 s at fixed gA.
F: a confirmed >= 5 sigma X17 resonance (systematics-controlled, replicated outside
   ATOMKI; e.g. PADME Run IV or MEG II full data).
G: R_D(*) excess confirmed at >= 5 sigma with independent tagging methods and
   consolidated SM form factors.
```

Anti double-counting: axis E is `independence_group = phi0_seed` (λ_C is φ₀-derived) —
the τ_n leg is a *new measurement sector* (neutron decay) reading the *same* frozen seed,
never an independent hit.

## Firewall

Standalone watchdog — a search surface, **not** a load-bearing claim. Not in the
verification suite, ledger, or website. The fixed points under test are TFPT compiler
outputs / branch readouts (`w=−1` and the lock are the cosmology branch; `Σm_ν` is the
seesaw NO floor; Koide `Q=2/3` is an `F_transfer` frontier bridge — never a primitive
compiler output; `N_fam=3` is an exact compiler output whose *sterile-dissolution
reading* on axis D is a confrontation, not a claim). A `consistent` or `tension`
verdict here upgrades nothing; a triggered kill would be reported honestly and routed
to the ledger by the parent, not by this experiment. **The firewall is intact.**

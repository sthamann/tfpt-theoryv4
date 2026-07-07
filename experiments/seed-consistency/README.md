# TFPT shared-seed stress test — is θ13 the first crack?

One retarded seed `φ0` fixes four observables in **distinct pipelines**:

```
β_rad          = φ0/(4π)              (CMB — ACT DR6)
Ω_b            = (4π−1)φ0/(4π)        (BBN — D/H, CMB-independent)
sin²θ13        = φ0·e^(−5/6)          (reactor — NuFIT 6.0)
λ_Cabibbo      = √(φ0(1−φ0))          (CKM — PDG)
```

Each measurement is inverted to the seed it implies; an inverse-variance **joint fit**,
a **leave-one-out** (Δχ² on removal), and the **dominant pull** (χ² share) decide whether
the seed block is coherent and which leg stresses it.

## Result

| leg | pipeline | implied φ0 | z(frozen) | z(joint) | Δχ²(LOO) |
|---|---|---|---|---|---|
| β | CMB | 0.04715 ± 0.01623 | −0.37 | −0.35 | +0.13 |
| Ω_b | BBN | 0.05311 ± 0.00132 | −0.05 | +0.15 | +0.03 |
| **θ13** | **reactor** | 0.05051 ± 0.00133 | **−2.00** | **−1.80** | **+3.54** |
| Cabibbo | CKM | 0.05314 ± 0.00043 | −0.08 | +0.54 | +1.67 |

- joint `φ0_hat = 0.052910`, **χ²/dof = 1.23** → the shared-seed block **HOLDS**.
- **θ13 is the dominant pull** (88% of χ², −1.80σ from the common seed; removing it drops
  χ² by 3.54) — the first real seed stress, but **< 3σ**, so no transfer correction is
  triggered and the block does not fall.

**Acceptance rules (frozen):** θ13 > 3σ from the common seed → flag PMNS θ13 as
transfer-corrected (μτ-breaking); two legs > 3σ → the shared-seed block falls. Neither
is met today; watch θ13 as global fits tighten.

## v2 — covariance-aware (`tfpt-seed v2`)

The v2 stress test hardens the points raised in review:

- **θ13 split** into a **reactor-only** leg (Daya Bay final 2023, `0.02175 ± 0.00065`) that
  enters the fit and a **global** leg (NuFIT 6.0) carried only as a *shadow* — never both in
  the fit, since the global PMNS fit already contains the reactor data (~0.9 correlated).
- a **covariance matrix** drives a generalised-least-squares fit (diagonal by construction;
  the off-diagonals are the honest slot for a shared systematic).
- **leave-one-experiment-family-out** (drop CMB / BBN / reactor / CKM) and a **posterior
  predictive check** (is the leg scatter consistent with one seed?).

Result: reactor-θ13 **χ²/dof = 1.37, PPC p = 0.25**, θ13 dominant at **−1.92σ (90 % of χ²)**;
reactor-only and global θ13 give the **same verdict** (block holds). The seed is coherent, but
θ13 is the first serious crack candidate.

## v3 — per-reactor-experiment θ13 (`tfpt-seed v3`)

Goes one level deeper than v2: the **individual reactor experiments** (Daya Bay, RENO,
Double Chooz — genuinely independent detectors) are combined inverse-variance into the
reactor-only leg; the NuFIT global fit stays a shadow. Same verdict: block holds.

## v4 — shared-vs-free + hostile decoder battery (`tfpt-seed v4`, 2026-07-06)

v1–v3 asked "is the leg scatter consistent with one seed?". v4 asks the two sharper
architecture questions (exploratory, no upgrade language):

1. **Shared vs free:** the 1-parameter shared-latent decoder
   (`β = u/4π`, `Ω_b = (4π−1)/(4π)·u`, `sin²θ13 = e^(−5/6)·u`, `λ_C² = u(1−u)`) fitted on
   the **raw measurements** gives `χ² = 4.10` (dof 3, p = 0.25) at `û = 0.052921`; the
   frozen `u = φ0` point gives `χ² = 4.51` (dof 4, p = 0.34). **AIC prefers the shared
   decoder over the saturated per-channel model (6.1 < 8.0)** — one latent u *is* the
   preferred description of the four channels.
2. **Hostile decoder battery:** every rival gets its **own free u** (the discriminating
   content is the cross-channel *ratios*, in which u cancels):
   - **0/14 single-swap neighbour decoders beat TFPT** (β divisor 4π → {π, 2π, 8π, 16π};
     Ω_b slope → {1, (2π−1)/2π, (8π−1)/8π}; θ13 exponent 5/6 → {1/2, 2/3, 3/4, 1, 7/6};
     Cabibbo link → {u, u(1−2u)}). Closest rival: `λ_C² = u` at χ² = 4.29 (the (1−u)
     factor is only a ~5% effect, weakly constrained today).
   - **Random placebo decoders** (n = 2000, all four constants scaled log-uniform ×[1/3, 3],
     same complexity class): TFPT sits at the **0.0th percentile** (placebo median
     χ² ≈ 1200) — the cross-channel ratios are architecture-specific, not generic.

Frozen kill extension: >2 neighbour decoders beating the TFPT links, or a placebo
percentile >10%, voids the architecture reading. **Verdict: shared decoder specific and
preferred — architecture consistency, not proof.**

## v5 — leave-one-out PREDICTION (`tfpt-seed v5`, 2026-07-06)

v5 turns the block into dated **forward numbers**: each channel is predicted from the
other three (GLS, reactor-only θ13) — the left-out measurement never enters its own fit.

| predict | from | predicted | measured | z |
|---|---|---|---|---|
| **β** | Cabibbo+θ13+Ω_b | **0.2413 ± 0.0018°** | 0.215 ± 0.074° (ACT DR6) | −0.36 |
| Ω_b h² | β+θ13+Cabibbo | 0.02209 ± 0.00017 | 0.02218 ± 0.00055 | +0.15 |
| sin²θ13 | β+Ω_b+Cabibbo | 0.02309 ± 0.00018 | 0.02175 ± 0.00065 | −1.99 |
| \|V_us\| | β+Ω_b+θ13 | 0.2215 ± 0.0020 | 0.22431 ± 0.00085 | +1.28 |

Every channel is predicted by the other three within 2σ (worst leg: θ13, the known
crack candidate from v1–v3). **Flagship (dated, falsifiable):** Cabibbo + θ13 + Ω_b
predict **β = 0.2413 ± 0.0018°** — a band ~40× narrower than today's ACT error.
**LiteBIRD / Simons Observatory (σ_β ~ 0.02°) will test this band blind**, since β
never entered the fit. Architecture consistency, not proof.

## v6 — retarded-tail ablation (`tfpt-seed v6`, 2026-07-06)

The seed is tree + topological tail: `u_tree = 1/(6π) = 0.053052` vs
`u_ret = 1/(6π) + 3/(256π⁴) = 0.053172` (+0.23%). v6 asks whether the data see the
tail — **today they cannot** (|Δχ²| = 0.30, marginally pro tree via the θ13 crack;
the tail shifts every channel by < 0.3σ, best Cabibbo at 0.28σ). The output is the
**dated prequential decision ladder**: σ(V_us) ≈ 8·10⁻⁵ (kaon/lattice — the realistic
decider, ~10× beyond PDG), σ(sin²θ13) ≈ 1.8·10⁻⁵, σ(ω_b h²) ≈ 1.7·10⁻⁵; **β can never
see the tail** (needs 1.8·10⁻⁴° — LiteBIRD tests the seed, not the tail). Frozen crack
condition: ≥ 2 channels preferring the tree seed at ≥ 3σ kill the retarded reading.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-seed analyze    # v1 (global theta13, chi2/dof=1.23)
tfpt-seed v2         # v2 (reactor-only theta13, GLS + family-LOO + PPC)
tfpt-seed v3         # v3 (per-reactor-experiment theta13)
tfpt-seed v4         # v4 (shared-vs-free + hostile decoder battery)
tfpt-seed v5         # v5 (leave-one-out prediction; the LiteBIRD forward band)
tfpt-seed v6         # v6 (retarded-tail ablation; dated precision deciders)
```

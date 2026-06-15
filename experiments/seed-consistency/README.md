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

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-seed analyze    # v1 (global theta13, chi2/dof=1.23)
tfpt-seed v2         # v2 (reactor-only theta13, GLS + family-LOO + PPC)
```

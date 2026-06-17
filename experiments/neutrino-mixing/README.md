# TFPT mixing angles — PMNS (θ12/θ13/θ23 + δ_PMNS) + CKM δ

Compiler-level **predictions of record** (the most belastbar tier — sharper than the
FRB/GW search targets), all from `c₃`/`φ₀`:

```
sin²θ12 = 1/3 − φ0/2     = 0.306747      (TBM + seam misalignment)
sin²θ13 = φ0·e^(−5/6)    = 0.0231        (seed × carrier-trace)
sin²θ23 = 1/2                            (μτ-symmetric; octant not selected)
δ_CKM   = π/3 + 3λ²      = 68.65°        (CKM CP phase; frozen of record, canonical v88)
δ_PMNS  = 4π/3           = 240°          (leptonic CP phase; hexagonal μ6 unit, sheet)
```

## Result (deterministic; published global fits in `data/measurements.json`)

| observable | TFPT | data | pull |
|---|---|---|---|
| sin²θ12 | 0.306747 | NuFIT 6.0 0.307±0.012 | **−0.02σ** |
| sin²θ12 | 0.306747 | JUNO 0.3092±0.0087 | −0.28σ |
| sin²θ13 | 0.0231 | NuFIT 6.0 0.02195±0.00058 | **+2.0σ** (mild tension) |
| sin²θ23 | 0.5 | NuFIT 6.0 0.470±0.017 | +1.76σ (octant open) |
| δ_CKM | 68.65° | LHCb γ 64.6°±2.8 | +1.45σ |
| δ_PMNS | 240° | NuFIT 6.0 NO best fit 212°⁺²⁶₋₄₁ | **+1.08σ** (consistent) |
| δ_PMNS | 240° | NuFIT 6.0 NO (no SK) 177°⁺¹⁹₋₂₀ | +3.32σ (non-preferred fit) |

→ **θ12 is a sharp hit** (essentially on NuFIT/JUNO); **θ13 carries the known ~2σ
tension** (the one place TFPT is pulled); θ23 consistent with maximal (octant
ambiguous); the CKM δ is consistent with the LHCb γ. `θ12/θ13/θ23` are PMNS predictions
of record; `δ_CKM` is the CKM phase. θ13 shares the seed `φ0` with the CMB birefringence
(see `cmb-birefringence-seed` shared-seed test).

### Leptonic CP phase `δ_PMNS = 240°` — the v231/v233 sharpening

The latest structural round (`verification/v220→v225→v231→v233`) turns `δ_PMNS` from a
free "phase-lattice" reading into a **structurally forced** value tied to `δ_CKM`. Both
CP phases are **one** hexagonal CM unit `ρ = e^{iπ/3}` (the `j=0` Eisenstein modulus, the
phase fiber over the square `μ4` seam), read on the two sheets (`ρ³ = −1`):

```
δ_CKM,lead = arg(ρ¹) = π/3   = 60°     (quark sector, bare hexagonal phase)
δ_PMNS     = arg(ρ⁴) = 4π/3  = 240°    (lepton sector)
⇒ δ_PMNS = δ_CKM,lead + π   (the exact Z2 sheet flip; rho^4 = -rho)
```

The Jarlskog orientation flips sign between the sectors (`+21·sin(π/3)` quark,
`−21·sin(π/3)` lepton; `v225`/`v231`), i.e. `sin δ_PMNS = sin 240° = −√3/2 < 0`.

**Existing-data confrontation.** `δ_PMNS = 240°` sits at **+1.08σ** of the NuFIT 6.0
normal-ordering best fit (`212°⁺²⁶₋₄₁`, incl. Super-K) and inside the 3σ range
`124°→364°`; it lies in the **CP-violating** region the data mildly prefer (NuFIT: CP
conservation only within 1σ for NO, disfavoured at >3.6σ for IO). The non-preferred
no-SK fit (`177°⁺¹⁹₋₂₀`) pulls it to +3.32σ. Kill: a global fit excluding 240° at ≥3σ.

**Firewall typing.** This is a **`[C]` downstream bridge**, *not* a primitive compiler
output: the seam DECK stays `Z/4` (the `v215` kill-test selects the square modulus); CP
lives in the hexagonal PHASE FIBER over it. Discriminative power is currently **weak**
(the δ_CP error is large) — sharpens decisively with DUNE/Hyper-K. The same `δ_PMNS =
4π/3` is the Dirac phase used in the `ftransfer/leptogenesis_boltzmann` `η_B` solve.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-neutrino analyze    # or: PYTHONPATH=src python -m tfpt_neutrino.cli analyze
```

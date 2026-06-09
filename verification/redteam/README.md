# TFPT Red Team / Stress Test layer

A **deliberately adversarial** pass over the five load-bearing reductions of the
package (the v78-review request). Unlike the confirmatory suite
(`verification/v*.py`), whose checks are designed to pass, every script here
tries to **break** a reduction. A red-team `check(...)` asserts an *adversarial*
fact — that a counterexample really exists, that a hidden assumption is really
needed, or that a firewall really holds — and the honest outcome of each target
is carried by an explicit **status**, never by a green pass.

## The five targets (Alessandro A–E)

| Script | Target | Status | Residual risk |
|---|---|---|---|
| `rt_A_e8net.py` | (E8)₁ boundary-net identification (`G_metric` ambient) | **reduced, not closed** | holomorphy proof + constructive map + bulk uniqueness |
| `rt_B_pascal.py` | carrier-rank / Pascal condition (upstream of Theorem A) | **survives (narrowed)** | boundary derivation of half-spinor exhaustion |
| `rt_C_kc3.py` | `k = c₃/2` seam-area coefficient (dimensional firewall) | **survives** | absolute `1/G` (UV-sensitive) is the one anchor |
| `rt_D_upoint.py` | `U_point → v_geo` amplitude bijection | **survives (narrowed)** | CP phases (δ_CKM/PMNS) not covered by `v_geo` |
| `rt_E_vgeo.py` | `v_geo` as the unique dimensional floor | **survives (narrowed)** | EW / reheating / leptogenesis scales + seam=Planck id |

## Protocol

Each target runs Alessandro's fixed eight-step protocol:

1. minimal statement · 2. assumptions · 3. logical chain · 4. validity conditions
· 5. counterexample search · 6. limiting/degenerate cases · 7. alternative
structures · 8. provisional verdict

and emits the narrow output: verified result, formula/code used, assumptions
needed, where it works, where it could fail, residual risk.

Allowed verdicts: **SURVIVES** (stands as worded), **SURVIVES (narrowed)**
(stands only after a silent assumption is named), **REDUCED, not closed** (the
conservative wording is correct), **BROKEN** (an actual failure — none occurred).

## How to run

```bash
cd verification/redteam
python run_redteam.py        # runs A–E, prints each protocol + the summary table
python rt_A_e8net.py         # any single target also runs standalone
```

Exit code = number of **failed adversarial checks**: a non-zero exit means a
stress test could not confirm its own counterexample/firewall (a real problem to
investigate), *not* that TFPT is wrong. `run_redteam.py` writes the summary as
`redteam_table.txt`, which the LaTeX note `../../tfpt_5_redteam.tex` mirrors.

## Files

| File | Role |
|---|---|
| `rt_common.py` | shared harness: import bootstrap, protocol printers, verdict/report builder |
| `rt_A…rt_E` | the five adversarial targets |
| `rt_table.py` | aggregates the per-target `REPORT` dicts into the summary table |
| `run_redteam.py` | runs the whole layer end-to-end |
| `redteam_table.txt` | generated summary artifact (mirrored by the LaTeX note) |

Ledger rows `REDTEAM.A.01 … REDTEAM.E.01` in `../status_ledger.csv` record the
verdicts; the note `tfpt_5_redteam.tex` (added to `build.sh` NOTES) presents them.

## Follow-up — what the next stage actually closed (`../v83_…`)

The adversarial verdicts were then used as a worklist. `../v83_e8net_holomorphic_uniqueness.py`
(ledger `GATE.METRIC.04`, `CAR.PASCAL.01`) **closes the first residual of Target A** and
**reduces Target B**:

- **Target A, residual 1 — closed [L].** At level 1 the number of primaries equals
  `det(Cartan) = |fundamental group|` (A3=4, D5=4, D8=4, **E8=1**). So holomorphy (μ-index 1)
  is *necessary* — it excludes the same-`c` rival `(D8)₁=SO(16)₁` (c=120/15=8 but 4 primaries) —
  **and sufficient**: a holomorphic c=8 chiral CFT is the lattice theory of the **unique** even
  unimodular rank-8 lattice E8 (Minkowski–Siegel mass `= 1/|W(E8)| = 1/696729600`). Target A now
  drops from **three residuals to two**: (i) boundary-net holomorphy + c=8, (ii) bulk-reconstruction
  uniqueness — both still `[P]/[A]`.
- **Target B — reduced [I]/[L].** The "K=2 Pascal truncation" is not free: `K=(g−1)/2` is the
  Pascal-row midpoint `Σ_{k≤(g−1)/2} C(g,k)=2^(g−1)` (the half-spinor split). The residual reduces
  to the standard input "carrier = half-spinor of Spin(2·g_car)" (`Λ^even(C⁵)=1+10+5=16`).

Still genuinely open (typed honestly): Target A (i)+(ii); Target D's CP-phase residual
(`v_geo` fixes magnitudes only); Target E's reheating/leptogenesis scales + the seam=Planck
identification. Target C is a dimensional **floor**, not a gap.

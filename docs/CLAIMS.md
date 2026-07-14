# Claims and their status

> TFPT's discipline is that **nothing is marked closed that is not machine-verified**, and **no
> dimensionful quantity is claimed as a derivation from pure numbers**. The authoritative,
> per-claim status is the versioned ledger [`verification/status_ledger.csv`](../verification/status_ledger.csv);
> this page is the human-readable summary. When in doubt, **the ledger wins**.

## The headline claims and their epistemic status

Not everything here has the same epistemic status — and saying so is the point. The five strongest
statements, made explicit:

| Claim | Result | Status |
|---|---|---|
| `E8` closure | `(D5 ⊕ A3) + μ4 ≅ E8`, 240 roots, glue index 4 | **Exact** — machine-proven lattice identity `[E]` |
| Number of generations | `N_fam = 3` | **Exact within the compiler** — `= rank A3 = dim H₁(P¹∖μ4)` `[E]` |
| Fine-structure constant | `α⁻¹ = 137.0359992` | **Exact numerical identity** — unique root of the boundary Ward identity, interval-verified `[E]` (1.9σ from CODATA-2022) |
| Physical origin of the seam | the `1/(8π)` area law / `SEAM.EQUIV.01` | **Open** — closed *modulo a cited theorem*, not proven end-to-end `[O]` |
| Cosmic birefringence | `β = φ₀/(4π) ≈ 0.2424°` | **Falsifiable prediction** — frozen, decided by CMB polarimetry `[X]` |

Read this as: the discrete/algebraic compiler is closed and exact; the *physical identification*
of the boundary object is the honest open frontier; and there are sharp numbers that observation
can kill. See [`FALSIFICATION.md`](FALSIFICATION.md) for the kill tests and
[`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) for the frontier.

## Status markers

Used consistently across all documents and the ledger. The **documents** show a simplified
four-class display marker; the **ledger** keeps the fine-grained per-claim type (Axiom / Formal /
Lattice / Numerical / Identity / Physical), so no fidelity is lost.

| Display marker | Meaning | Ledger fine types it covers |
|---|---|---|
| `[E]` | exact / machine-proven | Identity, Lattice (Lie/lattice), Formal (Lean), Numerical |
| `[C]` | conditional (holds under named hypotheses) | Physical, bridge, readout |
| `[O]` | open / axiom (declared input or genuine gap) | Axiom |
| `[X]` | falsifiable kill test | — |

The ledger is *append-only and versioned*: superseded rows are marked `active=false` with a
`canonical_status` pointer, so the current authoritative status of any claim is unambiguous. A
status marker is **never silently upgraded**.

## The four layers (where each kind of claim lives)

| Layer | Content | Status |
|---|---|---|
| **1. Closed compiler** | `E8` glue, carrier, `α⁻¹`, `(R,K,Q,L)`, lepton/quark *ratios* | `[I]/[L]/[N]` |
| **2. Protected IR physics** | `R+R²`, admissible gapped transfer sector; the boundary QFT as one relative object | `[I]/[P]` |
| **3. Anchors** | `π`, one dimensionful induced-gravity scale, `U_point` absolute amplitude norm | `[A]` (declared, not "missing") |
| **4. Interfaces** | `m_p/m_e`, `η_B` (leptogenesis), Koide, axion relic, full ambient QG measure | `[P]/[A]` |

## How every claim is kept honest

Every script cited in [`verification/run_all.py`](../verification/run_all.py) is also cited inline
in the theory documents via `\veri{vN_*.py}` (enforced in **both** directions by
[`verification/audit_sync.py`](../verification/audit_sync.py)), and the status heatmap is generated
directly from `status_ledger.csv`. So the papers, the suite, the ledger and the website stay in
lock-step: a claim cannot appear in a paper without a machine check behind it, and a check cannot
exist without a ledger row typing its status.

- **472 numbered claim checks** (`v1_*.py … v472_*.py`), one per claim cluster.
- **Independent Wolfram path** (`116/116` base, `368/368` extension) re-derives the exact
  algebraic/identity/lattice results on a second engine.
- **Lean 4** machine-formalises the carrier-rigidity core (`[F]`): no `sorry`/`admit`; every
  headline theorem's `#print axioms` returns only the three standard kernel axioms.
- **Red Team** (`redteam/run_redteam.py`) actively tries to break the five load-bearing reductions.

See [`VERIFICATION.md`](VERIFICATION.md) to reproduce any of this.

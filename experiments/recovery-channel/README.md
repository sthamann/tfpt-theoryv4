# TFPT recovery kernel as a quantum channel `R: H_bulk → H_observable`

The boundary-recovery kernel `{1, (2/3)⁶, (1/3)⁶}` made **explicit as a CPTP quantum
channel** and checked against the standard quantum-information axioms — the
data-independent "Test C" (information projector between bulk and observable space).

This packages, as a runnable channel, what the verification suite already proves
structurally: the recovery transport is the Bogoliubov second quantisation `Γ(t)` of a
one-particle contraction (`v161`), the boundary state is the compression of a
contraction (`v155`), it is quasi-free with vanishing higher cumulants and a unique
Perron–Frobenius fixed ray (`v160`), and it is a self-counting code channel (`v112`).

## What it checks (`src/tfpt_recovery/`)

Each kernel eigenvalue `λ` is realised as a qubit amplitude-damping channel with
excited-state survival `λ` (the protected `λ=1` "law" mode + two contracted modes).

1. **CPTP** — trace-preserving (`Σ Kᵢ†Kᵢ = I`) and completely positive (Choi matrix
   PSD) for all three modes.
2. **Recovery rate** — `R` applied `n` times damps the population by `λⁿ = (2/3)^{6n}`
   = the Page recovery `Iₙ`.
3. **Data-processing inequality** — relative entropy contracts,
   `S(R ρ ‖ R σ) ≤ S(ρ ‖ σ)` (the channel never creates information).
4. **QEC** — the `λ=1` mode is a **decoherence-free / Knill–Laflamme code** (the
   protected "law"/attractor); the contracted modes violate KL on the full code (the
   spectral gap `(2/3)⁶` is the leakage rate).
5. **Page curve** (Test B, folded in) — with the TFPT Hawking law `P_H = c₃/(1920 M²)`,
   `S_BH(t)/S₀ = (1−t/τ)^{2/3}` and the island/unitary min-prescription
   `S_page = min(S_BH, S_rad)` turns over at **`t/τ = 1−(1/2)^{3/2} = 0.6464`**, which is
   *exactly* the TFPT Page time `t_Page = (1−1/(2√2))τ`.

## Result (deterministic, no external data)

- all three modes are **CPTP** (Choi min-eig ≈ 0 to machine precision);
- recovery `Iₙ = (2/3)^{6n}` reproduced exactly;
- **data-processing holds** in every mode;
- the **protected `λ=1` code is decoherence-free** (KL satisfied), the contracted modes
  are not correctable;
- the **Page turnover lands at `t_Page` (0.6466 vs 0.6464)**.

→ **structural confirmation** that the recovery kernel is a genuine CPTP channel with a
protected code and the correct unitary Page turnover — *not* a new empirical result.
The remaining open content is the suite's premise-A / seam-net identification
(`v160`/`v165`), unchanged.

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate && pip install -e .
tfpt-recovery analyze       # or: PYTHONPATH=src python -m tfpt_recovery.cli analyze
```

## Layout

```
src/tfpt_recovery/constants.py   # frozen kernel {1,(2/3)^6,(1/3)^6}, c3, p2, N_fam
src/tfpt_recovery/channel.py     # Kraus, Choi, CPTP, recovery rate, data-processing, QEC
src/tfpt_recovery/page_curve.py  # TFPT Hawking law -> island Page curve -> t_Page turnover
src/tfpt_recovery/cli.py         # `tfpt-recovery analyze`
```

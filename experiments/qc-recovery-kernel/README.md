# QC recovery kernel — the TFPT recovery channel as a quantum circuit

> **Firewall:** this is an **analog / simulator validation** of the frozen kernel's
> dynamic signature plus a **hardware-feasibility study** — **never external evidence
> for TFPT**. `evidence_class = internal_consistency`, `stage = not_applicable`
> (same basket as `quantum-testbed` / `recovery-channel`). Running it on an IBM
> device tests *whether a programmable quantum processor can carry the signature
> through its noise*, not whether nature realises the kernel.

This experiment **activates the parked analog domain** (`quantum-recovery-analog`)
in the only honest way available today: instead of waiting for a natural per-step
recovery dataset, it *engineers* the frozen seam-transfer channel as an executable
quantum circuit (Kraus / unitary dilation) — runnable on exact and noisy simulators
now, and on IBM's free open plan later. `quantum-testbed` is the **classical**
simulator of the walled clock (QT.01–QT.05); this project is the **quantum-circuit
realisation** of the same object.

## Physics → circuit

The frozen seam transfer `T` has spectrum `{1, (2/3)⁶, (1/3)⁶}` on the 3 flavor
modes (Perron mode 1 protected). One transfer step = a CPTP map whose one-step
survivals on the two decaying modes are

| reading | mode 2 | mode 3 | carried by |
|---|---|---|---|
| **energy** | `λ₂ = (2/3)⁶ = 64/729` | `λ₃ = (1/3)⁶ = 1/729` | qubit **populations** |
| **amplitude** | `(2/3)³ = 8/27` | `(1/3)³ = 1/27` | qubit **coherences** |

Each decaying mode gets an **amplitude-damping channel** (Kraus rank 2,
`K0 = |0⟩⟨0| + √s|1⟩⟨1|`, `K1 = √(1−s)|0⟩⟨1|`) realised by the standard dilation

```
CRy(θ) system→ancilla   with sin²(θ/2) = p = 1 − s
CX     ancilla→system
reset  ancilla                      (fresh environment per block)
```

One transfer step is resolved into **6 carrier substeps** (`p2 = 6`) with per-block
survivals `s₂ = 2/3`, `s₃ = 1/3`, giving the resolved relaxation curve. **Which
semantics does the circuit realise?** The *same* energy-semantics circuit carries
**both**: an amplitude-damping block multiplies the excited **population** by `s`
(energy reading, `λ_k` per 6 blocks) and the **coherence** `ρ₀₁` by `√s` (amplitude
reading, `√λ_k = (2/3)³, (1/3)³` per 6 blocks). Both are verified exactly; the
default measured observable (populations, `initial='excited'`) realises the
**energy reading**. An explicit `semantics="amplitude"` circuit family (per-block
survivals `√(2/3)`, `√(1/3)`) puts the amplitude reading into populations instead.

5 qubits: `q0` Perron (protected — **no gate ever touches it**), `q1`/`q2` the two
flavor modes, `q3`/`q4` their ancillas. After `k` transfer steps the populations
decay as `λ₂ᵏ`, `λ₃ᵏ`; the combined observable

```
R(m) = w₀·P_Perron(m) + w₁·P₂(m) + w₂·P₃(m)   →   w₀ + w₁ λ₂^{m/6} + w₂ λ₃^{m/6}
```

carries the **walled-clock bend** `ln λ₃ / ln λ₂ = ln3/ln(3/2) = 2.7095`, the
**protected floor** `w₀` (Perron) and the **hard wall** (architecturally exactly two
damping channels — no third decay mode can exist). This is the QT.04 signature on a
quantum device. Fitting mirrors QT.04: **fixed-bend template vs free-ratio control**
(anti-numerology: the free fit must *recover* 2.7095, not assume it).

## Results (committed `results/results.json`)

- **Exact tier** (Aer density matrix, both semantics): per-step survivals exact to
  ≤2.4e-15 (`64/729`, `1/729` after 6 blocks; coherences at `½·8/27`, `½·1/27`),
  Perron exactly protected; the free-ratio fit recovers the bend
  **2.709511291351** (target `ln3/ln(3/2) = 2.709511291351`, bias `−3.8e-14`) —
  the circuit *is* the channel.
- **Noisy tier** (Aer + `FakeBrisbane` 127-qubit Eagle noise model: T1/T2, gate +
  readout errors, ISA-transpiled at optimization level 3, max depth 158 / 48 ECR):
  the bend survives hardware-level noise. Circuit-native **per-mode decode**
  (`p_k(m) = c + a·e^{−r_k m}`, bend `= r₃/r₂`): **2.65–2.69** (bias ≈ `−0.05`,
  −2%) already at **256 shots**. Blind combined **QT.04 free-ratio fit**: needs
  **16384 shots** for 3/3-seed detection (`2.89 ± 0.12`, bias `+0.19` ≈ +7%,
  pulled up by readout floors); at ≤1024 shots the free two-exponential fit can
  degenerate. **One transfer step (6 blocks) already suffices** at 16384 shots
  (free ratio 2.79, on-bend). Protected floor retention after 12 blocks: **0.993**.
- **Verdict enum** (`verdict` in `results.json`): `consistent` (bend identifiable
  under the device noise model by either decode) / `tension` (not identifiable at
  any tested shot count) / `not_run`. Current verdict: **`consistent`**.

## Reproduce

```bash
cd experiments/qc-recovery-kernel
python3.14 -m venv .venv && . .venv/bin/activate
pip install -e .                       # qiskit 2.4 + qiskit-aer 0.17 + qiskit-ibm-runtime 0.47
tfpt-qckernel audit                    # frozen-kernel identities (guards constants)
tfpt-qckernel analyze                  # exact + noisy tiers -> results/results.json
# or:  PYTHONPATH=src python -m tfpt_qckernel.cli analyze
```

## Hardware hook (prepared, NOT executed)

The submission path to IBM Quantum (free open plan) is **fully prepared but has not
been run** — it needs *your* IBM token and consumes your open-plan minutes:

1. Get a token at <https://quantum.cloud.ibm.com> (free account).
2. Save it once:

```bash
.venv/bin/python -c "from qiskit_ibm_runtime import QiskitRuntimeService; \
QiskitRuntimeService.save_account(channel='ibm_quantum_platform', \
token='<YOUR_IBM_TOKEN>', set_as_default=True)"
```

3. Submit / retrieve:

```bash
tfpt-qckernel hardware --dry-run       # ISA transpilation check, no token needed
tfpt-qckernel hardware                 # submits 13 circuits (job mode, least-busy device)
tfpt-qckernel hardware --fetch <JOB_ID>  # bend analysis -> results/hardware_results.json
```

No token is stored in this repository; nothing here phones home until you run
`hardware` without `--dry-run`.

## Layout

```
src/tfpt_qckernel/constants.py   # frozen kernel, both readings, bend (mirrors recovery-channel)
src/tfpt_qckernel/circuits.py    # Kraus dilation blocks + relaxation circuit family
src/tfpt_qckernel/fitting.py     # QT.04-mirror: fixed-bend template vs free-ratio control
src/tfpt_qckernel/sim.py         # exact (density matrix) + noisy (fake-backend) tiers
src/tfpt_qckernel/hardware.py    # IBM runtime submission hook (open plan, job mode)
src/tfpt_qckernel/cli.py         # tfpt-qckernel audit|analyze|hardware
results/results.json             # committed summary (both tiers)
```

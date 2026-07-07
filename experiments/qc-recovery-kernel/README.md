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
quantum circuit (Kraus / unitary dilation) — run on exact and noisy simulators
**and (2026-07-03) on real IBM hardware** (`ibm_marrakesh`, see the hardware section).
`quantum-testbed` is the **classical**
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
  readout errors): the bend survives hardware-level noise in the **circuit-native
  per-mode decode** (`p_k(m) = c + a·e^{−r_k m}`, bend `= r₃/r₂`) from the first
  tested shot count; current run gives `min_shots_per_mode = 256` and mean
  per-mode bend **2.46 / 2.69 / 2.68 / 2.65** over 256 / 1024 / 4096 / 16384
  shots. The blind combined **QT.04 free-ratio fit** is weaker in the fresh run:
  detection fractions **0% / 0% / 33% / 67%**, so `min_shots_identifiable = null`
  under the strict 3/3-seed rule. At 16384 shots the first-seed one-step and
  two-step fits are on-bend (`2.787`, `2.806`), while the all-seed combined
  detector remains floor-sensitive. Protected floor retention after 12 blocks:
  **0.993**.
- **Verdict enum** (`verdict` in `results.json`): `consistent` (bend identifiable
  under the device noise model by either decode) / `tension` (not identifiable at
  any tested shot count) / `not_run`. Current verdict remains **`consistent`** via
  per-mode decode, with the combined waveform fit explicitly marked weaker.

## Reproduce

```bash
cd experiments/qc-recovery-kernel
python3.14 -m venv .venv && . .venv/bin/activate
pip install -e .                       # qiskit 2.4 + qiskit-aer 0.17 + qiskit-ibm-runtime 0.47
tfpt-qckernel audit                    # frozen-kernel identities (guards constants)
tfpt-qckernel analyze                  # exact + noisy tiers -> results/results.json
# or:  PYTHONPATH=src python -m tfpt_qckernel.cli analyze
```

## Hardware run (EXECUTED 2026-07-03) — first real-device execution, `data_limited`

The prepared hook was executed on the free open plan: **job `d93ppd6vtlqs73ftdu5g` on
`ibm_marrakesh` (156-qubit Heron R2), 13 circuits × 16,384 shots** (committed:
`results/hardware_job.json`, `results/hardware_results.json`). Honest outcome:

- **The kernel's one-step survivals are reproduced on real hardware**: after the first
  transfer block the measured survivals are `0.639` (mode 2, target `2/3`, **−4.2%**) and
  `0.363` (mode 3, target `1/3`, **+8.9%**); the two-mode hierarchy and the protected
  floor are qualitatively present (Perron retention after 12 blocks **0.860** — vs 0.993
  under the FakeBrisbane noise model: the real device decays the idle protected qubit
  noticeably faster).
- **The blind 12-block bend decode does NOT recover 2.7095 on this device**: the QT.04
  free-ratio fit gives **1.964** and the per-mode decode **1.943** (bias −28%). A
  floor-aware refit localises the bias: mode 3 stays near-kernel (`s₃ = 0.303` vs 1/3,
  −9%) but mode 2 accumulates extra per-block decay (`s₂ = 0.541` vs 2/3, −19%) from
  gate/T1 noise over the deep ISA circuit, plus readout floors of ~0.17/0.08 — real
  Heron noise exceeds the Eagle fake-backend model that predicted identifiability.
- **Hardware-tier verdict: `data_limited`** (bend not identifiable at this depth/shots
  on this device; the simulator-tier `consistent` verdicts are unchanged). The named
  improvement path: dynamical decoupling on the idle qubits, measurement-error
  mitigation, fewer blocks (1-step already suffices in the noisy sim), or an
  error-suppressed session — all beyond the open-plan job mode used here.

Reproduce / re-run (needs your IBM token, consumes open-plan minutes):

```bash
.venv/bin/python -c "from qiskit_ibm_runtime import QiskitRuntimeService; \
QiskitRuntimeService.save_account(channel='ibm_quantum_platform', \
token='<YOUR_IBM_TOKEN>', set_as_default=True)"
tfpt-qckernel hardware --dry-run       # ISA transpilation check, no token needed
tfpt-qckernel hardware                 # submits 13 circuits (job mode, least-busy device)
tfpt-qckernel hardware --fetch <JOB_ID>  # bend analysis -> results/hardware_results.json
```

No token is stored in this repository.

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

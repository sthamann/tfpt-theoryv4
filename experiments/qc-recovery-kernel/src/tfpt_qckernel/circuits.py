"""Quantum-circuit (Kraus / unitary-dilation) realisation of the frozen recovery channel.

One carrier substep of the seam transfer acts on each decaying flavor mode as an
amplitude-damping channel with survival probability s_k (Kraus rank 2):

    K0 = |0><0| + sqrt(s_k) |1><1| ,     K1 = sqrt(1 - s_k) |0><1| .

Standard dilation (system qubit + fresh |0> ancilla per block):

    CRy(theta_k) [system -> ancilla],  sin^2(theta_k / 2) = p_k = 1 - s_k
    CX           [ancilla -> system]
    reset        [ancilla]                      (fresh environment each block)

After the block the excited-state POPULATION of the system qubit is multiplied by
s_k and its COHERENCE (off-diagonal rho_01) by sqrt(s_k) -- so the same circuit
carries the energy reading in populations and the amplitude reading in coherences.

Register layout (5 qubits):

    q0  Perron mode   (lambda = 1)  -- protected: NO damping block ever touches it
    q1  flavor mode 2 (survival 2/3 per substep, (2/3)^6 = 64/729 per transfer step)
    q2  flavor mode 3 (survival 1/3 per substep, (1/3)^6 = 1/729  per transfer step)
    q3  ancilla for q1
    q4  ancilla for q2

The hard wall is architectural: there are exactly two damping channels, a third
decay mode cannot arise from the circuit.
"""

from __future__ import annotations

import math

from qiskit import QuantumCircuit

from .constants import CARRIER_SURVIVAL, SUBSTEPS_PER_STEP

SYS_PERRON, SYS_MODE2, SYS_MODE3, ANC_MODE2, ANC_MODE3 = range(5)

SEMANTICS = ("energy", "amplitude")


def survival_per_block(semantics: str = "energy") -> tuple[float, float]:
    """Per-substep survival probabilities (mode 2, mode 3) for the chosen reading.

    energy    -> populations decay by (2/3)^6, (1/3)^6 per transfer step (6 blocks)
    amplitude -> populations decay by (2/3)^3, (1/3)^3 per transfer step (6 blocks)
    """
    if semantics == "energy":
        return CARRIER_SURVIVAL[1], CARRIER_SURVIVAL[2]
    if semantics == "amplitude":
        return math.sqrt(CARRIER_SURVIVAL[1]), math.sqrt(CARRIER_SURVIVAL[2])
    raise ValueError(f"semantics must be one of {SEMANTICS}, got {semantics!r}")


def damping_theta(p: float) -> float:
    """Ry angle of the dilation: sin^2(theta/2) = p (damping probability)."""
    return 2.0 * math.asin(math.sqrt(p))


def append_damping_block(qc: QuantumCircuit, system: int, ancilla: int,
                         survival: float) -> None:
    qc.cry(damping_theta(1.0 - survival), system, ancilla)
    qc.cx(ancilla, system)
    qc.reset(ancilla)


def relaxation_circuit(n_blocks: int, *, semantics: str = "energy",
                       measure: bool = True, initial: str = "excited") -> QuantumCircuit:
    """The three-mode relaxation circuit after ``n_blocks`` carrier substeps.

    initial='excited' (|1> on all system qubits) probes populations (energy reading);
    initial='plus' (|+>) probes coherences (amplitude reading, exact tier only).
    """
    s2, s3 = survival_per_block(semantics)
    qc = QuantumCircuit(5, 3 if measure else 0,
                        name=f"tfpt_recovery_{semantics}_{n_blocks}blocks")
    for q in (SYS_PERRON, SYS_MODE2, SYS_MODE3):
        if initial == "excited":
            qc.x(q)
        elif initial == "plus":
            qc.h(q)
        else:
            raise ValueError(f"initial must be 'excited' or 'plus', got {initial!r}")
    qc.barrier()
    for _ in range(n_blocks):
        append_damping_block(qc, SYS_MODE2, ANC_MODE2, s2)
        append_damping_block(qc, SYS_MODE3, ANC_MODE3, s3)
        qc.barrier()
    if measure:
        qc.measure([SYS_PERRON, SYS_MODE2, SYS_MODE3], [0, 1, 2])
    return qc


def relaxation_family(n_blocks_max: int = 2 * SUBSTEPS_PER_STEP, *,
                      semantics: str = "energy", measure: bool = True,
                      initial: str = "excited") -> list[QuantumCircuit]:
    """Circuits for n_blocks = 0 .. n_blocks_max (the resolved relaxation curve)."""
    return [relaxation_circuit(m, semantics=semantics, measure=measure, initial=initial)
            for m in range(n_blocks_max + 1)]


def populations_from_counts(counts: dict[str, int]) -> tuple[float, float, float]:
    """Marginal P(qubit = 1) for (Perron, mode 2, mode 3) from a counts dict.

    Classical bits: c0 = Perron, c1 = mode 2, c2 = mode 3; qiskit bitstrings are
    little-endian (c0 is the rightmost character).
    """
    total = sum(counts.values())
    ones = [0, 0, 0]
    for key, n in counts.items():
        for i in range(3):
            if key[-1 - i] == "1":
                ones[i] += n
    return ones[0] / total, ones[1] / total, ones[2] / total

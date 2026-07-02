"""Two simulator tiers for the circuit realisation of the recovery channel.

exact tier  -- Aer density-matrix simulation (noise-free): validates that the
               dilation circuit IS the frozen channel (populations, coherences,
               per-transfer-step survivals, bend to machine precision).
noisy tier  -- Aer with the noise model of a real IBM device (fake provider:
               FakeBrisbane / FakeTorino, i.e. T1/T2, gate + readout errors):
               tests whether hardware-level noise preserves bend identifiability,
               with the QT.04 fixed-template vs free-ratio control.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import partial_trace
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeBrisbane, FakeTorino

from .circuits import (
    SYS_MODE2,
    SYS_MODE3,
    SYS_PERRON,
    populations_from_counts,
    relaxation_family,
)
from .constants import (
    BEND,
    CARRIER_SURVIVAL,
    LAMBDA_AMPLITUDE,
    LAMBDA_ENERGY,
    QT04_WEIGHTS,
    SUBSTEPS_PER_STEP,
)
from .fitting import bend_report, direct_bend, fit_single_exp

FAKE_BACKENDS = {"fake_brisbane": FakeBrisbane, "fake_torino": FakeTorino}
DEFAULT_N_BLOCKS = 2 * SUBSTEPS_PER_STEP        # 2 transfer steps, resolved per substep


def combined_curve(p_perron: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> np.ndarray:
    """The QT.04 observable R(m) = w0*P_perron + w1*P_mode2 + w2*P_mode3."""
    w0, w1, w2 = QT04_WEIGHTS
    return w0 * np.asarray(p_perron) + w1 * np.asarray(p2) + w2 * np.asarray(p3)


# --------------------------------------------------------------------------- exact tier
def _exact_populations_and_coherences(circuits: list[QuantumCircuit]
                                      ) -> tuple[np.ndarray, np.ndarray]:
    """Density-matrix run: per circuit the P(q=1) populations and |rho_01| coherences
    of the three system qubits (Perron, mode 2, mode 3)."""
    sim = AerSimulator(method="density_matrix")
    pops, cohs = [], []
    for qc in circuits:
        qc = qc.copy()
        qc.save_density_matrix()
        rho = sim.run(transpile(qc, sim), shots=1).result().data(0)["density_matrix"]
        row_p, row_c = [], []
        for q in (SYS_PERRON, SYS_MODE2, SYS_MODE3):
            red = np.asarray(rho.probabilities([q]))
            row_p.append(float(red[1]))
            r1q = partial_trace(rho, [k for k in range(qc.num_qubits) if k != q])
            row_c.append(float(abs(r1q.data[0, 1])))
        pops.append(row_p)
        cohs.append(row_c)
    return np.array(pops), np.array(cohs)


@dataclass
class ExactResult:
    semantics: str
    n_blocks: int
    populations: list[list[float]]            # [m][Perron, mode2, mode3]
    coherences: list[list[float]]             # from the |+> preparation
    per_step_survival: dict                   # populations after 6 blocks vs frozen kernel
    coherence_step_survival: dict             # coherences after 6 blocks (sqrt semantics)
    perron_protected: bool
    max_population_error: float               # vs the analytic s^m curves
    direct_bend: float
    bend_report: dict


def run_exact(semantics: str = "energy", n_blocks: int = DEFAULT_N_BLOCKS) -> ExactResult:
    fam_pop = relaxation_family(n_blocks, semantics=semantics, measure=False,
                                initial="excited")
    fam_coh = relaxation_family(n_blocks, semantics=semantics, measure=False,
                                initial="plus")
    pops, _ = _exact_populations_and_coherences(fam_pop)
    _, cohs = _exact_populations_and_coherences(fam_coh)
    m = np.arange(n_blocks + 1, dtype=float)

    if semantics == "energy":
        s2, s3 = CARRIER_SURVIVAL[1], CARRIER_SURVIVAL[2]
        step_target = (LAMBDA_ENERGY[1], LAMBDA_ENERGY[2])
    else:
        s2, s3 = math.sqrt(CARRIER_SURVIVAL[1]), math.sqrt(CARRIER_SURVIVAL[2])
        step_target = (LAMBDA_AMPLITUDE[1], LAMBDA_AMPLITUDE[2])

    analytic = np.column_stack([np.ones_like(m), s2 ** m, s3 ** m])
    max_err = float(np.max(np.abs(pops - analytic)))
    k = SUBSTEPS_PER_STEP
    per_step = {
        "mode2_after_6_blocks": float(pops[k, 1]), "mode2_target": step_target[0],
        "mode3_after_6_blocks": float(pops[k, 2]), "mode3_target": step_target[1],
        "ok": bool(abs(pops[k, 1] - step_target[0]) < 1e-12
                   and abs(pops[k, 2] - step_target[1]) < 1e-12),
    }
    # coherences decay with sqrt(survival) per block: after 6 blocks sqrt(lambda_step)
    coh_target = (0.5 * math.sqrt(step_target[0]), 0.5 * math.sqrt(step_target[1]))
    coh_step = {
        "mode2_coherence_after_6_blocks": float(cohs[k, 1]), "mode2_target": coh_target[0],
        "mode3_coherence_after_6_blocks": float(cohs[k, 2]), "mode3_target": coh_target[1],
        "ok": bool(abs(cohs[k, 1] - coh_target[0]) < 1e-12
                   and abs(cohs[k, 2] - coh_target[1]) < 1e-12),
    }
    curve = combined_curve(pops[:, 0], pops[:, 1], pops[:, 2])
    report = bend_report(m, curve)
    return ExactResult(
        semantics, n_blocks, pops.tolist(), cohs.tolist(), per_step, coh_step,
        perron_protected=bool(np.max(np.abs(pops[:, 0] - 1.0)) < 1e-12),
        max_population_error=max_err,
        direct_bend=direct_bend(pops[:, 1], pops[:, 2], m),
        bend_report=report.to_dict(),
    )


# --------------------------------------------------------------------------- noisy tier
@dataclass
class NoisyRun:
    shots: int
    seed: int
    free_ratio: float
    bend_bias: float
    on_bend: bool
    is_kernel_relaxation: bool
    per_mode_bend: float                     # circuit-native decode: r3/r2 per-mode fits


@dataclass
class NoisyResult:
    backend: str
    n_blocks: int
    shots_grid: list[int]
    n_seeds: int
    transpiled_depth_max: int
    transpiled_ops_max: dict
    populations_best: list[list[float]]      # highest-shots, first-seed curve
    runs: list[NoisyRun] = field(default_factory=list)
    per_shots_summary: dict = field(default_factory=dict)
    min_shots_identifiable: int | None = None        # blind combined QT.04 fit
    min_shots_per_mode: int | None = None            # circuit-native per-mode decode
    steps_needed: dict = field(default_factory=dict)
    floor_retention_final: float = 0.0       # P_perron after n_blocks (T1 sag of the floor)
    verdict: str = "not_run"


def _noisy_populations(tqcs: list[QuantumCircuit], sim: AerSimulator,
                       shots: int, seed: int) -> np.ndarray:
    result = sim.run(tqcs, shots=shots, seed_simulator=seed).result()
    return np.array([populations_from_counts(result.get_counts(i))
                     for i in range(len(tqcs))])


def _analyze_curve(m: np.ndarray, pops: np.ndarray) -> tuple[dict, float]:
    curve = combined_curve(pops[:, 0], pops[:, 1], pops[:, 2])
    report = bend_report(m, curve)
    r2 = fit_single_exp(m, pops[:, 1]).rate
    r3 = fit_single_exp(m, pops[:, 2]).rate
    return report.to_dict(), r3 / r2


def run_noisy(backend_name: str = "fake_brisbane", n_blocks: int = DEFAULT_N_BLOCKS,
              shots_grid: tuple[int, ...] = (256, 1024, 4096, 16384),
              n_seeds: int = 3) -> NoisyResult:
    backend = FAKE_BACKENDS[backend_name]()
    sim = AerSimulator.from_backend(backend)
    fam = relaxation_family(n_blocks, semantics="energy", measure=True,
                            initial="excited")
    tqcs = [transpile(qc, sim, optimization_level=3, seed_transpiler=7) for qc in fam]
    depth_max = max(t.depth() for t in tqcs)
    ops_max = {k: int(v) for k, v in tqcs[-1].count_ops().items()}
    m = np.arange(n_blocks + 1, dtype=float)

    out = NoisyResult(backend.name, n_blocks, list(shots_grid), n_seeds,
                      depth_max, ops_max, populations_best=[])
    best_pops = None
    for shots in shots_grid:
        for seed in range(n_seeds):
            pops = _noisy_populations(tqcs, sim, shots, seed + 1)
            report, per_mode = _analyze_curve(m, pops)
            out.runs.append(NoisyRun(
                shots, seed + 1, report["free"]["ratio"], report["bend_bias"],
                report["on_bend"], report["is_kernel_relaxation"], per_mode))
            if shots == shots_grid[-1] and seed == 0:
                best_pops = pops
                # steps needed: refit on the first transfer step only (m = 0..6)
                short, short_pm = _analyze_curve(m[:SUBSTEPS_PER_STEP + 1],
                                                 pops[:SUBSTEPS_PER_STEP + 1])
                out.steps_needed = {
                    "one_transfer_step_blocks": SUBSTEPS_PER_STEP,
                    "one_step_free_ratio": short["free"]["ratio"],
                    "one_step_on_bend": short["on_bend"],
                    "one_step_per_mode_bend": short_pm,
                    "two_steps_blocks": n_blocks,
                    "two_steps_free_ratio": report["free"]["ratio"],
                    "two_steps_on_bend": report["on_bend"],
                    "two_steps_per_mode_bend": per_mode,
                }
    out.populations_best = best_pops.tolist()
    out.floor_retention_final = float(best_pops[-1, 0])
    for shots in shots_grid:
        rs = [r for r in out.runs if r.shots == shots]
        out.per_shots_summary[str(shots)] = {
            "mean_free_ratio": float(np.mean([r.free_ratio for r in rs])),
            "mean_bias": float(np.mean([r.bend_bias for r in rs])),
            "std_free_ratio": float(np.std([r.free_ratio for r in rs])),
            "mean_per_mode_bend": float(np.mean([r.per_mode_bend for r in rs])),
            "detection_fraction": float(np.mean([r.is_kernel_relaxation for r in rs])),
        }
        if (out.min_shots_identifiable is None
                and all(r.is_kernel_relaxation for r in rs)):
            out.min_shots_identifiable = shots
        pm_ok = all(abs(math.log(r.per_mode_bend / BEND)) < math.log(1.15) for r in rs)
        if out.min_shots_per_mode is None and pm_ok:
            out.min_shots_per_mode = shots
    # consistent if the bend is identifiable under the device noise model by EITHER
    # decode (the blind QT.04 waveform fit or the circuit-native per-mode fit)
    out.verdict = ("consistent" if (out.min_shots_identifiable is not None
                                    or out.min_shots_per_mode is not None)
                   else "tension")
    return out

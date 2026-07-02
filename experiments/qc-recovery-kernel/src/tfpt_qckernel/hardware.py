"""IBM Quantum hardware hook (free open plan) — fully prepared, NOT executed here.

Requires the user's IBM Quantum token, saved ONCE via

    from qiskit_ibm_runtime import QiskitRuntimeService
    QiskitRuntimeService.save_account(channel="ibm_quantum_platform",
                                      token="<YOUR_IBM_TOKEN>", set_as_default=True)

then

    tfpt-qckernel hardware            # submit the relaxation family (job mode)
    tfpt-qckernel hardware --dry-run  # validate ISA transpilation, no token needed
    tfpt-qckernel hardware --fetch <JOB_ID>   # retrieve + run the bend analysis

Job mode (SamplerV2 on a backend, no Session) is what the open plan supports.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

from .circuits import populations_from_counts, relaxation_family
from .fitting import bend_report, fit_single_exp
from .sim import DEFAULT_N_BLOCKS, combined_curve

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"

TOKEN_HELP = (
    "No saved IBM Quantum account found.\n"
    "Save your token ONCE (free open plan, https://quantum.cloud.ibm.com):\n\n"
    "    .venv/bin/python -c \"from qiskit_ibm_runtime import QiskitRuntimeService; "
    "QiskitRuntimeService.save_account(channel='ibm_quantum_platform', "
    "token='<YOUR_IBM_TOKEN>', set_as_default=True)\"\n\n"
    "then re-run:  tfpt-qckernel hardware"
)


def _isa_circuits(backend, n_blocks: int):
    fam = relaxation_family(n_blocks, semantics="energy", measure=True,
                            initial="excited")
    return transpile(fam, backend=backend, optimization_level=3, seed_transpiler=7)


def dry_run(n_blocks: int = DEFAULT_N_BLOCKS) -> dict:
    """Validate the ISA transpilation against a fake 127-qubit Eagle backend
    (FakeBrisbane) without any token or network access."""
    backend = FakeBrisbane()
    tqcs = _isa_circuits(backend, n_blocks)
    info = {
        "mode": "dry_run",
        "backend": backend.name,
        "n_circuits": len(tqcs),
        "depth": [t.depth() for t in tqcs],
        "ops_final": {k: int(v) for k, v in tqcs[-1].count_ops().items()},
        "ready": True,
    }
    return info


def submit(shots: int = 16384, n_blocks: int = DEFAULT_N_BLOCKS) -> dict:
    """Submit the relaxation family to the least-busy real device (job mode)."""
    try:
        service = QiskitRuntimeService()
    except Exception as exc:                       # no saved account / bad credentials
        raise SystemExit(f"{TOKEN_HELP}\n\n(original error: {exc})") from exc
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=5)
    tqcs = _isa_circuits(backend, n_blocks)
    sampler = SamplerV2(mode=backend)
    job = sampler.run(tqcs, shots=shots)
    record = {
        "mode": "submitted",
        "job_id": job.job_id(),
        "backend": backend.name,
        "shots": shots,
        "n_blocks": n_blocks,
        "submitted_utc": datetime.now(timezone.utc).isoformat(),
        "fetch_with": f"tfpt-qckernel hardware --fetch {job.job_id()}",
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "hardware_job.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def fetch(job_id: str) -> dict:
    """Retrieve a finished hardware job and run the same bend analysis as the
    simulator tiers (combined QT.04 fit + per-mode decode)."""
    try:
        service = QiskitRuntimeService()
    except Exception as exc:
        raise SystemExit(f"{TOKEN_HELP}\n\n(original error: {exc})") from exc
    job = service.job(job_id)
    result = job.result()
    pops = []
    for pub in result:
        counts = pub.data.c.get_counts() if hasattr(pub.data, "c") else \
            next(iter(pub.data.values())).get_counts()
        pops.append(populations_from_counts(counts))
    pops = np.array(pops)
    m = np.arange(len(pops), dtype=float)
    curve = combined_curve(pops[:, 0], pops[:, 1], pops[:, 2])
    report = bend_report(m, curve)
    r2 = fit_single_exp(m, pops[:, 1]).rate
    r3 = fit_single_exp(m, pops[:, 2]).rate
    out = {
        "mode": "hardware_result",
        "job_id": job_id,
        "backend": job.backend().name,
        "populations": pops.tolist(),
        "combined_bend_report": report.to_dict(),
        "per_mode_bend": r3 / r2,
        "floor_retention_final": float(pops[-1, 0]),
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "hardware_results.json").write_text(json.dumps(out, indent=2) + "\n")
    return out

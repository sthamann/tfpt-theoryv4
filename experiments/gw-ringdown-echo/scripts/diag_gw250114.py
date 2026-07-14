"""Diagnostic: why does GW250114 (loudest event) get a tiny whitened A220 in the echo
pipeline?  Load the real local strain, whiten, locate the actual ringdown power, and compare
the claimed merger index against where the whitened power really peaks.

Run:  PYTHONPATH=src python scripts/diag_gw250114.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tfpt_gw.strain_data import (  # noqa: E402
    apply_whitening, detector_frame_mass, fit_and_subtract_qnm, qnm_220, read_hdf5,
    whitening_filter_gated,
)

STRAIN = Path(__file__).resolve().parents[1] / "data" / "strain"
EVENTS = ["GW250114_082203", "GW150914", "GW200129_065458", "GW190521"]


def _mf_snr(white: np.ndarray, start: int, f0: float, tau: float, dt: float) -> float:
    """Whitened matched-filter SNR of the (2,2,0) template over [start, start+6tau]:
    rho = <white, t> / ||t|| with t the cos-only unit-norm damped sinusoid."""
    from tfpt_gw.strain_data import damped_sinusoid
    n = len(white)
    end = min(n, start + int(6.0 * tau / dt))
    t = damped_sinusoid(n, start, f0, tau, dt, 0.0)
    sl = slice(start, end)
    norm = float(np.linalg.norm(t[sl])) or 1.0
    return float(np.dot(white[sl], t[sl]) / norm)


def diag(event: str, hires: bool = False) -> None:
    suffix = "_meta16k.json" if hires else "_meta.json"
    tag = "16k" if hires else "4k"
    meta = json.loads((STRAIN / f"{event}{suffix}").read_text())
    merger_gps, mf_src = float(meta["gps"]), float(meta["mf"])
    mf = detector_frame_mass(event, mf_src)
    f0, tau = qnm_220(mf, 0.69)
    print(f"\n=== {event} [{tag}]  (mf_det={mf:.1f}, f0={f0:.1f} Hz, tau={tau*1e3:.2f} ms) ===")
    for det, fname in meta["files"].items():
        s = read_hdf5(str(STRAIN / Path(fname).name))
        merger = s.index_at(merger_gps)
        # GATED whitening (exclude the event window from the PSD estimate) -- the
        # pipeline's method; avoids the self-whitening bias that suppresses loud signals.
        gate_pre = merger - int(0.10 / s.dt)
        gate_post = merger + int(0.30 / s.dt)
        psd_i, scale = whitening_filter_gated(s.data, s.dt, gate_pre, gate_post)
        white = apply_whitening(s.data, psd_i, scale)

        _, amp_nom = fit_and_subtract_qnm(white, merger, f0, tau, s.dt)

        # WIDE scan: slide the QNM start over +-1.0 s to find the true loud ringdown
        # (in case the catalog merger GPS is imprecise by more than ~0.1 s).
        span = int(1.0 / s.dt)
        starts = np.arange(merger - span, merger + span)
        amps = np.array([fit_and_subtract_qnm(white, int(k), f0, tau, s.dt)[1]
                         for k in starts])
        best = int(starts[int(np.argmax(amps))])
        amp_best = float(amps.max())
        off_ms = (best - merger) * s.dt * 1e3
        # also the max WITHIN +-0.1 s (near the nominal merger)
        near = np.abs(starts - merger) <= int(0.1 / s.dt)
        amp_near = float(amps[near].max())
        print(f"  {det}: A220@nominal={amp_nom:7.3f}  |  best(+-0.1s)={amp_near:7.3f}  |  "
              f"best(+-1s)={amp_best:7.3f} at {off_ms:+.0f} ms")


if __name__ == "__main__":
    for ev in EVENTS:
        try:
            diag(ev, hires=False)
        except FileNotFoundError as exc:
            print(f"\n=== {ev} === SKIP (missing file: {exc})")

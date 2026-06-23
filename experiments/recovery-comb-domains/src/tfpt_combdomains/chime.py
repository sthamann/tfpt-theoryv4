"""CHIME/FRB Baseband Catalog 1 reader (CHIME/FRB Coll. 2024, ApJ 969 145;
CANFAR DOI 10.11570/23.0029) for the A3b stacked-tail channel.

Each beamformed HDF5 stores ``tiedbeam_power`` (frequency, polarization, time) at the
instrumental 2.56 us resolution, coherently dedispersed *within* each channel. The channels
still START at different times (the inter-channel dispersion sweep), so a naive frequency sum
would smear the burst across the whole ~100 ms sweep and FAKE a wide tail. We therefore
incoherently dedisperse across channels (the official ``Example_make_waterfall.py`` recipe,
DM = ``DM_coherent``) before summing -> the true burst profile + its genuine scattering tail.

Firewall unchanged: this is a search target (horizon-residual), never a claim. The only gain
over the FAST/GBT .calibP path is data QUALITY (coherent dedispersion, full-Stokes, calibrated),
not a wider physical recovery -- a ms burst still has no 3-decade recovery.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np

try:                                  # h5py is optional; the channel reports its absence honestly
    import h5py
except Exception:                     # noqa: BLE001
    h5py = None

K_DM = 2.41e-4                        # MHz^-2 pc^-1 cm^3 s, the dispersion constant (example value)


def read_chime_profile(path: Path):
    """Frequency-summed, incoherently-dedispersed Stokes-I time series of one CHIME beamformed
    HDF5. Returns (dt_s, profile, source) or None (missing h5py / unreadable file)."""
    if h5py is None:
        return None
    try:
        with h5py.File(str(path), "r") as f:
            power = np.asarray(f["tiedbeam_power"][:], dtype=float)   # (freq_present, pol, time)
            dt = float(f.attrs["delta_time"])                        # s (2.56e-6)
            dm = float(f["tiedbeam_power"].attrs["DM_coherent"])
            freq_id = np.asarray(f["index_map"]["freq"]["id"]).astype(int)
            freq = np.asarray(f["index_map"]["freq"]["centre"], dtype=float)
            t0 = np.asarray(f["time0"]["ctime"], dtype=float)
        with warnings.catch_warnings():                              # all-NaN channels -> empty slice
            warnings.simplefilter("ignore", RuntimeWarning)
            stokes_i = np.nanmean(power, axis=1)                      # (freq_present, time)
        ntime = stokes_i.shape[1]
        full = np.full((1024, ntime), np.nan)
        full[freq_id] = stokes_i
        t0 = t0 - np.nanmin(t0)
        freq_ref = float(np.nanmax(freq))
        aligned = np.full_like(full, np.nan)
        for t, fc, fid in zip(t0, freq, freq_id):
            dm_delay = dm / K_DM * (fc ** -2 - freq_ref ** -2)
            shift = int(round((t - dm_delay) / dt))
            aligned[fid] = np.roll(full[fid], shift)
        profile = np.nansum(aligned, axis=0)
        return dt, profile, path.stem.split("_")[0]                  # source = FRB name from filename
    except Exception:                                                # noqa: BLE001
        return None

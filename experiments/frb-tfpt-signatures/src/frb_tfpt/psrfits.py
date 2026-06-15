"""Minimal PSRFITS / PSRCHIVE-archive reader (via astropy.io.fits, no PSRCHIVE).

PSRCHIVE ``.ar``/``.calibP`` files and search/fold ``.fits`` are PSRFITS, which
astropy reads directly. This returns a calibrated single-burst dynamic spectrum
in Stokes I (and optionally Q,U,V), with the frequency axis and time resolution
-- everything the FRB.01 sub-band-timing test and the within-burst polarisation
tests need. Heavy raw archives stay in ``new-data/``; only the tiny derived
sub-band ToA table is persisted.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from astropy.io import fits


@dataclass
class Archive:
    path: str
    source: str
    freqs: np.ndarray          # MHz, per channel
    tbin: np.ndarray | float   # s per phase bin
    wts: np.ndarray            # per-channel weights (0 = zapped)
    I: np.ndarray              # Stokes I (nchan, nbin), calibrated, baseline-removed
    Q: np.ndarray | None
    U: np.ndarray | None
    V: np.ndarray | None
    pol_type: str

    @property
    def nchan(self) -> int:
        return self.I.shape[0]

    @property
    def nbin(self) -> int:
        return self.I.shape[1]


def read_archive(path, full_stokes: bool = False, name: str | None = None) -> Archive:
    """Read a PSRFITS/PSRCHIVE archive. ``path`` may be a filename or a file-like
    object (e.g. a BytesIO streamed from a zip/tar member); ``name`` overrides the
    stored label."""
    hd = fits.open(path, ignore_missing_end=True)
    s = hd["SUBINT"]
    sh = s.header
    npol, nch, nbin = sh["NPOL"], sh["NCHAN"], sh["NBIN"]
    data = np.asarray(s.data["DATA"]).astype(np.float32).reshape(npol, nch, nbin)
    scl = np.asarray(s.data["DAT_SCL"]).reshape(npol, nch)
    off = np.asarray(s.data["DAT_OFFS"]).reshape(npol, nch)
    wts = np.asarray(s.data["DAT_WTS"]).reshape(nch).astype(np.float32)
    freqs = np.asarray(s.data["DAT_FREQ"]).reshape(nch).astype(float)
    try:
        tbin = float(sh["TBIN"])               # may be '*' (undefined) in some archives
    except (KeyError, ValueError, TypeError):
        tbin = float(np.asarray(s.data["TSUBINT"]).ravel()[0]) / nbin
    pol_type = sh.get("POL_TYPE", "")
    src = hd[0].header.get("SRC_NAME", "")
    hd.close()

    def cal(p):
        x = data[p] * scl[p][:, None] + off[p][:, None]
        x = x * (wts[:, None] > 0)
        return x - np.median(x, axis=1, keepdims=True)

    p = [cal(i) for i in range(npol)]
    if pol_type.startswith("IQUV"):
        I, Q, U, V = p[0], p[1], p[2], p[3]
    elif pol_type.startswith("AABBCRCI"):
        I, Q, U, V = p[0] + p[1], p[0] - p[1], 2 * p[2], 2 * p[3]
    else:                                   # unknown -> treat pol0 as I
        I = p[0]
        Q = U = V = None
    if not full_stokes:
        Q = U = V = None
    label = name or getattr(path, "name", None) or str(path)
    return Archive(str(label), src, freqs, tbin, wts, I, Q, U, V, pol_type)

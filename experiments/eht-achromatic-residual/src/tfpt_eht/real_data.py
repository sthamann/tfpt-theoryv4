"""Ingest REAL EHT M87 2017 polarimetric uvfits and run the achromaticity diagnostic.

The TFPT achromatic-residual test needs the GRMHD-subtracted residual intercept on a
reconstructed image (per-pixel chi(r)) -- that requires polarimetric imaging
(eht-imaging) + a GRMHD library, which is out of scope here, so the 1/r^2-profile and
sign-flip nulls stay data-limited. What we CAN do on the raw real data is the
**frequency / achromaticity** diagnostic: the EHT observes in two bands
(hi ~229.1 GHz, lo ~227.1 GHz), so the band-to-band rotation of the net polarisation
angle measures the Faraday lambda^2 chromaticity of the source directly.

A purely TFPT-residual term would be achromatic (no lambda^2 tail); the raw source EVPA
need not be. So this is an honest first step: ingest real data, measure the raw
band-to-band EVPA rotation and the implied rotation measure, and flag the residual
(GRMHD-subtracted) nulls as the remaining, data-limited work.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from astropy.io import fits

C_M_S = 2.99792458e8
DATA = Path(__file__).resolve().parents[2] / "data" / "eht_m87_2017"


@dataclass
class BandVis:
    band: str
    freq_hz: float
    lambda_m: float
    q_net: float            # I-weighted vector-averaged Stokes Q / I
    u_net: float
    evpa_deg: float         # 0.5 atan2(U, Q)
    m_lin_net: float        # net linear polarisation fraction (diagnostic)
    n_vis: int


def read_uvfits_band(path: str | Path) -> BandVis:
    """Read a polarimetric uvfits, return the I-weighted net Stokes (Q,U)/I + EVPA."""
    with fits.open(path) as hd:
        g = hd[0]
        freq = float(g.header["CRVAL4"])
        data = np.asarray(g.data.data)            # (nvis,...,STOKES=4, COMPLEX=3)
        d = data.reshape(data.shape[0], 4, 3)     # collapse singleton axes
    re, im, wt = d[:, :, 0], d[:, :, 1], d[:, :, 2]
    vis = re + 1j * im                            # (nvis, 4): RR, LL, RL, LR
    w = np.clip(wt, 0.0, None)
    rr, ll, rl, lr = vis[:, 0], vis[:, 1], vis[:, 2], vis[:, 3]
    wgt = np.minimum.reduce([w[:, 0], w[:, 1], w[:, 2], w[:, 3]])
    ok = wgt > 0
    rr, ll, rl, lr, wgt = rr[ok], ll[ok], rl[ok], lr[ok], wgt[ok]
    # circular-basis Stokes
    stokes_i = 0.5 * (rr + ll)
    stokes_q = 0.5 * (rl + lr)
    stokes_u = 0.5j * (lr - rl)                   # U = i(LR - RL)/2
    # I-amplitude-weighted vector average (robust net-polarisation diagnostic)
    amp_i = np.abs(stokes_i) * wgt
    W = amp_i.sum() or 1.0
    q_net = float(np.real((stokes_q * wgt).sum()) / W)
    u_net = float(np.real((stokes_u * wgt).sum()) / W)
    i_net = float((np.abs(stokes_i) * wgt).sum() / (wgt.sum() or 1.0))
    evpa = 0.5 * np.degrees(np.arctan2(u_net, q_net))
    m_lin = float(np.hypot(q_net, u_net) / (i_net or 1.0))
    return BandVis(Path(path).stem, freq, C_M_S / freq, q_net, u_net, evpa, m_lin, int(ok.sum()))


@dataclass
class AchromaticityResult:
    available: bool
    days: list[str] = field(default_factory=list)
    per_band: dict = field(default_factory=dict)
    delta_evpa_deg: float = float("nan")          # lo - hi net EVPA rotation
    rotation_measure: float = float("nan")        # rad/m^2 implied by the two bands
    verdict: str = ""


def _unwrap_deg(d: float) -> float:
    while d > 90:
        d -= 180
    while d < -90:
        d += 180
    return d


def run_real_achromaticity() -> AchromaticityResult:
    files = sorted(DATA.glob("*_hi.uvfits"))
    if not files:
        return AchromaticityResult(False, verdict="no real EHT uvfits in data/eht_m87_2017 "
                                                   "(run scripts/fetch_eht_data.py)")
    res = AchromaticityResult(True)
    dchi, rms = [], []
    for hi in files:
        day = hi.stem.replace("_hi", "")
        lo = DATA / f"{day}_lo.uvfits"
        if not lo.exists():
            continue
        bh, bl = read_uvfits_band(hi), read_uvfits_band(lo)
        res.days.append(day)
        res.per_band[day] = {"hi": vars(bh), "lo": vars(bl)}
        d_evpa = _unwrap_deg(bl.evpa_deg - bh.evpa_deg)
        dlam2 = bl.lambda_m**2 - bh.lambda_m**2
        rm = np.radians(d_evpa) / dlam2 if dlam2 != 0 else float("nan")
        dchi.append(d_evpa)
        rms.append(rm)
    res.delta_evpa_deg = float(np.mean(dchi)) if dchi else float("nan")
    res.rotation_measure = float(np.mean(rms)) if rms else float("nan")
    res.verdict = (
        f"REAL EHT M87 2017 polarimetry ingested ({len(res.days)} days x 2 bands). "
        f"Raw band-to-band net-EVPA rotation = {res.delta_evpa_deg:+.2f} deg "
        f"(implied RM ~ {res.rotation_measure:.2e} rad/m^2). This is the RAW source "
        f"chromaticity; the TFPT achromatic-residual nulls (1/r^2 profile, sign-flip) "
        f"need the GRMHD-subtracted residual image (eht-imaging + GRMHD library) -> "
        f"those remain DATA-LIMITED. Step 1 (real-data ingest + achromaticity diagnostic) done."
    )
    return res

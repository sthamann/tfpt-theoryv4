"""KC.05/KC.06: non-tooth operator-proxy tests on FRB polarization data.

These are exploratory astro proxies for the 2026-07-06 signature reclassification:

* KC.05 tests whether a PA-derived four-character transition operator suppresses
  off-character leakage, the S8 idea translated into the only available FRB
  polarization observable. This is not a core QGEO test: the transduction B is
  unproven, so a null/hit is surface-leakage only.
* KC.06 tests an S2a-style multivariate lag operator spectrum on the polarization
  state, not a 2/3 tooth or a log-time comb.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .data import Bursts, sessions

N_NULL = 2000
MIN_LI_PCT = 10.0
TARGET_SPECTRUM = np.array([1.0, (2.0 / 3.0) ** 6, (1.0 / 3.0) ** 6])


@dataclass
class Mu4BlockProxy:
    source: str
    n_pairs: int
    c4_off_fraction: float
    shuffle_median: float
    p_low: float
    z3_off_fraction: float
    generic4_median: float
    generic4_min: float
    verdict: str


@dataclass
class SpectrumProxy:
    source: str
    n_pairs: int
    n_features: int
    eig_abs_norm: list[float]
    target_spectrum: list[float]
    distance_to_target: float
    shuffle_median_distance: float
    p_close: float
    verdict: str


@dataclass
class OperatorProxyResult:
    mu4_block: Mu4BlockProxy
    multivariate_spectrum: SpectrumProxy


def _valid_pol_mask(b: Bursts, *, require_vsign: bool = False) -> np.ndarray:
    if b.pa_deg is None or b.li_pct is None:
        return np.zeros(len(b.mjd), dtype=bool)
    mask = np.isfinite(b.pa_deg) & np.isfinite(b.li_pct) & (b.li_pct >= MIN_LI_PCT)
    if require_vsign:
        if b.vsign is None:
            return np.zeros(len(b.mjd), dtype=bool)
        mask &= np.isfinite(b.vsign)
    return mask


def _valid_session_sequences(mask: np.ndarray, b: Bursts) -> list[np.ndarray]:
    seqs = []
    for idx in sessions(b):
        keep = idx[mask[idx]]
        if len(keep) >= 3:
            seqs.append(keep)
    return seqs


def _pa_classes(pa_deg: np.ndarray, n_class: int) -> np.ndarray:
    # Linear polarization lives in P = L exp(2 i PA); 2*PA unwraps the PA mod-pi ambiguity.
    out = np.full(len(pa_deg), -1, dtype=int)
    valid = np.isfinite(pa_deg)
    phase = np.mod(2.0 * pa_deg[valid], 360.0)
    out[valid] = np.floor(phase / (360.0 / n_class)).astype(int) % n_class
    return out


def _transition_matrix(class_series: list[np.ndarray], n_class: int) -> np.ndarray:
    mat = np.zeros((n_class, n_class), dtype=float)
    for seq in class_series:
        if len(seq) < 2:
            continue
        for a, b in zip(seq[:-1], seq[1:], strict=False):
            mat[int(a), int(b)] += 1.0
    return mat


def _off_fraction(mat: np.ndarray) -> float:
    total = float(np.sum(mat * mat))
    if total <= 0:
        return math.nan
    off = mat.copy()
    np.fill_diagonal(off, 0.0)
    return float(np.sum(off * off) / total)


def _block_proxy(b: Bursts, *, seed: int = 0) -> Mu4BlockProxy:
    rng = np.random.default_rng(seed)
    mask = _valid_pol_mask(b)
    seqs = _valid_session_sequences(mask, b)
    c4 = _pa_classes(b.pa_deg, 4)
    z3 = _pa_classes(b.pa_deg, 3)

    c4_seqs = [c4[idx] for idx in seqs]
    z3_seqs = [z3[idx] for idx in seqs]
    mat = _transition_matrix(c4_seqs, 4)
    obs = _off_fraction(mat)
    n_pairs = int(np.sum(mat))

    null = []
    for _ in range(N_NULL):
        shuffled = []
        for seq in c4_seqs:
            shuffled.append(rng.permutation(seq))
        null.append(_off_fraction(_transition_matrix(shuffled, 4)))
    null_arr = np.asarray(null)
    p_low = float((1 + np.sum(null_arr <= obs)) / (len(null_arr) + 1))

    phase = np.mod(2.0 * b.pa_deg[mask], 360.0)
    generic = []
    # Unequal random 4-mark partitions are negative controls for "any arbitrary marking".
    for _ in range(500):
        cuts = np.sort(rng.uniform(0.0, 360.0, size=3))
        all_classes = np.searchsorted(cuts, phase, side="right")
        class_by_index = np.full(len(b.mjd), -1, dtype=int)
        class_by_index[np.where(mask)[0]] = all_classes
        generic_seqs = [class_by_index[idx] for idx in seqs]
        generic.append(_off_fraction(_transition_matrix(generic_seqs, 4)))
    generic_arr = np.asarray(generic)
    z3_obs = _off_fraction(_transition_matrix(z3_seqs, 3))

    detected = bool(p_low < 0.01 and obs < np.nanpercentile(generic_arr, 5))
    verdict = (
        "ESCALATE -- C4 off-character leakage is suppressed relative to the shuffle and "
        "generic-mark controls; surface-leakage only until a transduction B is proven."
        if detected else
        "NULL -- the PA-derived C4 transition operator is not unusually block-diagonal "
        "relative to shuffle/generic controls; no visible S8-style mu4 block protection "
        "in this FRB polarization proxy."
    )
    return Mu4BlockProxy(
        b.source,
        n_pairs=n_pairs,
        c4_off_fraction=round(obs, 4),
        shuffle_median=round(float(np.nanmedian(null_arr)), 4),
        p_low=round(p_low, 4),
        z3_off_fraction=round(z3_obs, 4),
        generic4_median=round(float(np.nanmedian(generic_arr)), 4),
        generic4_min=round(float(np.nanmin(generic_arr)), 4),
        verdict=verdict,
    )


def _features(b: Bursts, idx: np.ndarray) -> np.ndarray:
    pa = np.deg2rad(2.0 * b.pa_deg[idx])
    li = b.li_pct[idx] / 100.0
    v = b.vsign[idx]
    return np.column_stack([np.cos(pa), np.sin(pa), li, v])


def _fit_spectrum(pairs_x: np.ndarray, pairs_y: np.ndarray) -> np.ndarray:
    x_mean = pairs_x.mean(axis=0)
    x_std = pairs_x.std(axis=0)
    x_std[x_std == 0] = 1.0
    x = (pairs_x - x_mean) / x_std
    y = (pairs_y - x_mean) / x_std
    ridge = 1e-6 * np.eye(x.shape[1])
    beta = np.linalg.solve(x.T @ x + ridge, x.T @ y)
    eig = np.sort(np.abs(np.linalg.eigvals(beta)))[::-1]
    if eig[0] > 0:
        eig = eig / eig[0]
    return eig


def _spectrum_distance(eig: np.ndarray) -> float:
    padded = np.ones(3)
    take = min(3, len(eig))
    padded[:take] = eig[:take]
    return float(np.linalg.norm(padded - TARGET_SPECTRUM))


def _spectrum_proxy(b: Bursts, *, seed: int = 1) -> SpectrumProxy:
    rng = np.random.default_rng(seed)
    mask = _valid_pol_mask(b, require_vsign=True)
    seqs = _valid_session_sequences(mask, b)

    xs, ys = [], []
    seq_features = []
    for idx in seqs:
        f = _features(b, idx)
        seq_features.append(f)
        xs.append(f[:-1])
        ys.append(f[1:])
    x = np.vstack(xs)
    y = np.vstack(ys)
    eig = _fit_spectrum(x, y)
    dist = _spectrum_distance(eig)

    null_dist = []
    for _ in range(N_NULL):
        nx, ny = [], []
        for f in seq_features:
            perm = rng.permutation(len(f))
            fp = f[perm]
            nx.append(fp[:-1])
            ny.append(fp[1:])
        null_eig = _fit_spectrum(np.vstack(nx), np.vstack(ny))
        null_dist.append(_spectrum_distance(null_eig))
    null_arr = np.asarray(null_dist)
    p_close = float((1 + np.sum(null_arr <= dist)) / (len(null_arr) + 1))

    detected = bool(p_close < 0.01 and dist < 0.25)
    verdict = (
        "ESCALATE -- multivariate lag spectrum is unusually close to the frozen S2a "
        "target relative to the shuffle null; surface-leakage only until B is proven."
        if detected else
        "NULL -- the multivariate polarization lag operator is not unusually close to "
        "the S2a spectrum {1,64/729,1/729} relative to the shuffle null."
    )
    return SpectrumProxy(
        b.source,
        n_pairs=int(x.shape[0]),
        n_features=int(x.shape[1]),
        eig_abs_norm=[round(float(v), 5) for v in eig.tolist()],
        target_spectrum=[round(float(v), 5) for v in TARGET_SPECTRUM.tolist()],
        distance_to_target=round(dist, 5),
        shuffle_median_distance=round(float(np.median(null_arr)), 5),
        p_close=round(p_close, 4),
        verdict=verdict,
    )


def run(pol: Bursts) -> OperatorProxyResult:
    return OperatorProxyResult(
        mu4_block=_block_proxy(pol),
        multivariate_spectrum=_spectrum_proxy(pol),
    )

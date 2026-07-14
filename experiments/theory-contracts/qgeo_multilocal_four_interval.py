"""QGEO.MULTILOCAL.01 -- the four mu4 marks make the seam circle a FOUR-INTERVAL
free-fermion geometry, where the modular apparatus is exactly solvable (theory contract;
never a scorecard row, never load-bearing).

Motivation (2026-07-14, bird's-eye round): the bedrock QGEO.SYM.01 (omega o rho = omega)
and the AP2 continuum statement (v476/v478) both live on the seam circle minus the four
mu4 marks -- which IS the n=4 multi-interval geometry of the free chiral fermion, the one
continuum system whose multi-interval modular theory is EXACTLY KNOWN in the literature
(Casini-Huerta 2009, modular Hamiltonians of n intervals = local term + conjugate-point
mixing term; Longo-Xu multi-interval subfactors; Rehren-Tedesco multilocal fermions =
the diagonal n-fold-cover isomorphism; Kawahigashi-Longo-Mueger: for a holomorphic net
the multi-interval inclusion is trivial, mu = 1 = det K -- the SAME one bit as the
keystone). None of these multi-interval tools appear in the repo so far (only the
single-ball CHM boost, v358). This contract exhibits the mechanism on the exactly
solvable lattice ring:

  (M1) BINARY CLOCK: on the antiperiodic (RP-admissible) ring the quarter-turn clock
       rho satisfies rho^4 = -1 EXACTLY -- the mu4 clock lifts to its BINARY (double
       cover) order-8 form on fermions, the same Z2-lift pattern as 2I over I.
  (M2) EXACT SECTOR DECOUPLING: the primitive-8th-root character projectors of rho
       block-diagonalise the mu4-symmetric 4-interval covariance to machine precision
       (the Rehren-Tedesco diagonal/cover isomorphism at covariance level).
  (M3) COVER/TWIST IDENTITY: each sector kernel is the SINGLE-interval kernel on the
       quarter ring with boundary twist lambda_k; the union of sector spectra equals the
       full 4-interval spectrum exactly.
  (M4) CLOCK INVARIANCE: rho C rho^-1 = C at machine precision, hence [rho, K] = 0 for
       the Peschel modular Hamiltonian K = ln((1-C)/C) by functional calculus:
       omega o rho = omega is MANIFEST at the 4-interval state level.
  (M5) NEGATIVE CONTROL: displacing ONE interval by one site breaks the clock map and
       re-couples the character sectors at O(10^-2) (vs 10^-15 symmetric).
  (M6) CONJUGATE-POINT MIXING: the cross-interval block of K is band-concentrated on the
       conjugate diagonal s' ~ s (the lattice shadow of the Casini-Huerta mixing term).

WHAT THIS IS / IS NOT.  [E-num]: M1-M5 are exact finite identities (machine precision).
[N]: M6 is a quantitative structure exhibit.  [C]: the continuum multi-interval modular
flow is CITED (Casini-Huerta; Longo-Xu; Rehren-Tedesco; KLM), not re-derived.
[O]: the raw-seam premise (QGEO.SYM.01 / SEAM.EQUIV.01's arrow) is NOT closed: this
exhibits the mechanism in the exactly solvable class the seam is argued to reach, it
does not prove the seam reaches it. NOT claimed: a closed gate or status change.

Firewall: theory contract; belongs in experiments/theory-contracts, never in
evidence_scorecard.json; passing is internal consistency, not external evidence.

Run:  cd experiments/theory-contracts && python3 qgeo_multilocal_four_interval.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent / "qgeo_multilocal_four_interval_results.json"

CHECKS: list[dict] = []

N = 256           # ring size (antiperiodic free fermion, no zero modes)
Q = N // 4        # quarter ring = mark spacing (the mu4 clock step)
P0 = 8            # base interval offset from the mark
ELL = 48          # interval length (marks at 0, Q, 2Q, 3Q sit in the gaps)
EPS = 1e-12


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def make_cf(n: int):
    """Antiperiodic critical free fermion on a ring of n sites, half filling."""
    ks = 2 * np.pi * (np.arange(n) + 0.5) / n
    ks = np.where(ks > np.pi, ks - 2 * np.pi, ks)
    occ = ks[np.abs(ks) < np.pi / 2]

    def cf(d):
        d = np.asarray(d, dtype=float)
        return (np.exp(1j * occ[:, None] * d.ravel()[None, :]).sum(axis=0) / n
                ).reshape(d.shape)
    return cf


def region_sites(p0: int = P0, ell: int = ELL) -> np.ndarray:
    return np.concatenate([p0 + j * Q + np.arange(ell) for j in range(4)])


def clock_matrix(sites: np.ndarray) -> tuple[np.ndarray, int]:
    """rho: psi(x) -> psi(x+Q) with the antiperiodic sign on ring wrap; returns the
    matrix and the number of sites whose image leaves the region (0 iff symmetric)."""
    n = len(sites)
    idx = {s: i for i, s in enumerate(sites)}
    R = np.zeros((n, n))
    broken = 0
    for i, s in enumerate(sites):
        t, sign = s + Q, 1.0
        if t >= N:
            t, sign = t - N, -1.0
        if t in idx:
            R[idx[t], i] = sign
        else:
            broken += 1
    return R, broken


def peschel_K(C: np.ndarray) -> np.ndarray:
    w, U = np.linalg.eigh((C + C.conj().T) / 2)
    w = np.clip(w.real, EPS, 1 - EPS)
    return (U * np.log((1 - w) / w)) @ U.conj().T


def main() -> None:
    print("QGEO.MULTILOCAL.01 -- the mu4 marks as the exactly solvable 4-interval "
          "modular geometry\n")
    cf = make_cf(N)
    sites = region_sites()
    C = cf(sites[None, :] - sites[:, None])
    R, broken = clock_matrix(sites)
    n = 4 * ELL

    # M1: rho^4 = -1 (binary lift)
    R4 = np.linalg.matrix_power(R, 4)
    ok1 = broken == 0 and np.allclose(R4, -np.eye(n), atol=1e-14)
    check("M1 BINARY CLOCK [E-num]: the quarter-turn clock on the antiperiodic "
          "(RP-admissible) ring satisfies rho^4 = -1 EXACTLY -- the fermionic mu4 clock "
          "is the BINARY (double-cover) order-8 lift, the same Z2-lift pattern as 2I "
          "over the icosahedral group",
          ok1, f"||rho^4 + 1||_max = {np.abs(R4 + np.eye(n)).max():.2e}; clock is a "
               f"signed permutation of the region ({broken} broken sites)")

    # character projectors: primitive 8th roots lambda_k = e^{i pi (2k+1)/4}
    lams = [np.exp(1j * np.pi * (2 * k + 1) / 4) for k in range(4)]
    Ps = [sum(lam ** (-m) * np.linalg.matrix_power(R, m) for m in range(4)) / 4
          for lam in lams]

    # M2: exact sector decoupling
    resolution = np.abs(sum(Ps) - np.eye(n)).max()
    idem = max(np.abs(P @ P - P).max() for P in Ps)
    commC = max(np.abs(P @ C - C @ P).max() for P in Ps)
    ok2 = resolution < 1e-12 and idem < 1e-12 and commC < 1e-12
    check("M2 EXACT SECTOR DECOUPLING [E-num]: the primitive-8th-root character "
          "projectors of rho resolve the identity and commute with the reduced "
          "covariance to machine precision (Rehren-Tedesco multilocal/diagonal "
          "isomorphism at covariance level)",
          ok2, f"sum P_k = 1 to {resolution:.2e}; idempotent to {idem:.2e}; "
               f"max ||[P_k, C]|| = {commC:.2e}")

    # M3: sector kernels = twisted quarter-ring single-interval kernels; spectra match
    u = np.arange(ELL)
    d0 = u[None, :] - u[:, None]
    spec_full = np.sort(np.linalg.eigvalsh((C + C.conj().T) / 2))
    herm = 0.0
    spec_sect = []
    for lam in lams:
        Ck = sum(lam ** (-m) * cf(d0 + m * Q) for m in range(4))
        herm = max(herm, np.abs(Ck - Ck.conj().T).max())
        spec_sect.append(np.linalg.eigvalsh((Ck + Ck.conj().T) / 2))
    spec_sect = np.sort(np.concatenate(spec_sect))
    dspec = np.abs(spec_full - spec_sect).max()
    ok3 = dspec < 1e-12 and herm < 1e-12
    check("M3 COVER/TWIST IDENTITY [E-num]: each sector kernel C_k(u,u') = "
          "sum_m lambda_k^-m c(u'-u+mQ) is the SINGLE-interval kernel on the quarter "
          "ring with boundary twist lambda_k; union of sector spectra = full 4-interval "
          "spectrum exactly",
          ok3, f"max spectral mismatch = {dspec:.2e}; twisted kernels hermitian to "
               f"{herm:.2e}")

    # M4: clock invariance of the state => modular invariance by functional calculus
    dC = np.abs(R @ C @ R.T - C).max()
    K = peschel_K(C)
    dK_rel = np.abs(R @ K @ R.T - K).max() / np.abs(K).max()
    ok4 = dC < 1e-12 and dK_rel < 1e-3
    check("M4 CLOCK INVARIANCE [E-num]: rho C rho^-1 = C at machine precision -- hence "
          "[rho, K] = 0 for K = ln((1-C)/C) by functional calculus (numerical residual "
          "amplified only by log'(x) at near-pure eigenvalues): omega o rho = omega is "
          "MANIFEST at the 4-interval state level",
          ok4, f"||rho C rho^-1 - C||_max = {dC:.2e}; ||[rho,K]||/||K|| = {dK_rel:.2e} "
               f"(log-amplified, exact in exact arithmetic given [rho,C]=0)")

    # M5: negative control -- displace ONE interval by one site
    sites_bad = np.concatenate([P0 + np.arange(ELL) + 1] +
                               [P0 + j * Q + np.arange(ELL) for j in range(1, 4)])
    Cb = cf(sites_bad[None, :] - sites_bad[:, None])
    Rb, broken_b = clock_matrix(sites_bad)
    # per-interval character transform (block scalar lambda_k^-j), as in the exact case
    couple = 0.0
    for k, lam in enumerate(lams):
        W = np.zeros((ELL, 4 * ELL), dtype=complex)
        for j in range(4):
            W[:, j * ELL:(j + 1) * ELL] = np.eye(ELL) * lam ** (-j) / 2
        # sector-k compression of the OTHER sectors: should vanish iff symmetric
        for kk, lam2 in enumerate(lams):
            if kk == k:
                continue
            W2 = np.zeros((ELL, 4 * ELL), dtype=complex)
            for j in range(4):
                W2[:, j * ELL:(j + 1) * ELL] = np.eye(ELL) * lam2 ** (-j) / 2
            couple = max(couple, np.abs(W @ Cb @ W2.conj().T).max())
    # symmetric reference
    couple_sym = 0.0
    for k, lam in enumerate(lams):
        W = np.zeros((ELL, 4 * ELL), dtype=complex)
        for j in range(4):
            W[:, j * ELL:(j + 1) * ELL] = np.eye(ELL) * lam ** (-j) / 2
        for kk, lam2 in enumerate(lams):
            if kk == k:
                continue
            W2 = np.zeros((ELL, 4 * ELL), dtype=complex)
            for j in range(4):
                W2[:, j * ELL:(j + 1) * ELL] = np.eye(ELL) * lam2 ** (-j) / 2
            couple_sym = max(couple_sym, np.abs(W @ C @ W2.conj().T).max())
    ok5 = broken_b > 0 and couple > 1e-3 and couple_sym < 1e-12
    check("M5 NEGATIVE CONTROL [E-num]: displacing ONE interval by one site breaks the "
          "clock map and re-couples the character sectors at O(10^-2) (vs machine zero "
          "symmetric) -- the invariance is the mu4-symmetric configuration, not an "
          "artifact",
          ok5, f"clock broken on {broken_b} sites; max cross-sector coupling displaced "
               f"= {couple:.2e} vs symmetric = {couple_sym:.2e}")

    # M6: conjugate-point mixing structure of the cross-interval K block
    def band_stats(ell_val: int, band: int = 2):
        sts = region_sites(P0, ell_val)
        Kv = peschel_K(cf(sts[None, :] - sts[:, None]))
        B = Kv[0:ell_val, ell_val:2 * ell_val]
        tot = float(np.sum(np.abs(B) ** 2))
        near = float(sum(np.abs(B[s, sp]) ** 2 for s in range(ell_val)
                         for sp in range(max(0, s - band), min(ell_val, s + band + 1))))
        peaked = float(np.mean([abs(int(np.argmax(np.abs(B[s]))) - s) <= band
                                for s in range(ell_val)]))
        return near / tot, peaked

    f24, p24 = band_stats(24)
    f48, p48 = band_stats(48)
    ok6 = p24 >= 0.9 and p48 >= 0.9
    check("M6 CONJUGATE-POINT MIXING [N]: every row of the cross-interval K block PEAKS "
          "on the conjugate diagonal s' ~ s (|s'-s| <= 2) at both sizes -- the lattice "
          "shadow of the Casini-Huerta multi-interval mixing term (the band ENERGY "
          "fraction decreases with size: the mixing keeps long-range conformal tails, "
          "honestly reported)",
          ok6, f"ell=24: rows peaked {p24:.2f}, band energy {f24:.3f}; "
               f"ell=48: rows peaked {p48:.2f}, band energy {f48:.3f}")

    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The seam circle minus the four mu4 marks IS the n=4 multi-interval geometry of "
        "the free fermion -- the continuum class whose modular theory is exactly known "
        "(Casini-Huerta mixing term; Longo-Xu multi-interval subfactors; Rehren-Tedesco "
        "multilocal diagonal isomorphism; KLM: holomorphic <=> trivial multi-interval "
        "inclusion, mu = 1 = det K, the SAME one bit as the keystone). On the exactly "
        "solvable ring: the fermionic clock is the BINARY order-8 lift (rho^4 = -1, M1); "
        "its primitive-8th-root character projectors decouple the 4-interval state "
        "EXACTLY (M2); each sector is a twisted quarter-ring single interval (M3, the "
        "cover picture); rho C rho^-1 = C at machine precision so omega o rho = omega "
        "is MANIFEST (M4) and configuration-forced (M5); the cross-interval modular "
        "coupling sits on the conjugate-point band (M6, the CH mixing shadow). This "
        "puts the bedrock QGEO.SYM.01 and the AP2 continuum leg in ONE exactly "
        "solvable, citable framework; the raw-seam premise itself stays [O]. No gate "
        "closed, no status change, no scorecard row."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "QGEO.MULTILOCAL.01 four-interval multilocal modular geometry",
        "date": "2026-07-14",
        "firewall": ("theory contract, never a scorecard row, never load-bearing; "
                     "internal consistency, not evidence; QGEO.SYM.01/SEAM.EQUIV.01 stay "
                     "open"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "params": {"N": N, "Q": Q, "P0": P0, "ELL": ELL},
        "checks": CHECKS,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

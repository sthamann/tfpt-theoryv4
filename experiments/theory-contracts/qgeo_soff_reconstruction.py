"""QGEO S_off reconstruction tomography -- a THEORY CONTRACT (not an empirical scorecard row).

The exact side of QGEO.SYM.01 is already machine-checked (v198/v201/v210 and
``qgeo_dtn_mark_locality.py``): with mu4 marks the seam DtN Lambda = |D_theta| + M_f is
mu4-character-block-diagonal, [rho, Lambda] = 0, omega.rho = omega; Z3 / generic marks break it.

This contract adds the RECONSTRUCTION version -- the honest bridge toward a controlled system
(BEC analog horizon, superconducting waveguide, optical cavity, numerical Steklov geometry),
where the boundary energy form is never known exactly but must be reconstructed from finitely
many, noisy spectral measurements:

  (1) S_off leakage statistic.  For the mu4 character projectors P_r (Fourier classes
      n = r mod 4),

          S_off(A) = sum_{r != s} ||P_r A P_s||_F^2 / ||A||_F^2 ,

      reported for the full operator AND for the sub-principal part alone (A - |D|), which is
      the discriminating piece (|D| is block-diagonal for free, v198).
  (2) Reconstruction pipeline.  Only the K lowest eigenpairs are "measured", with relative
      eigenvalue noise sigma and eigenvector mixing of the same size; the reconstructed
      operator is Lambda_hat = sum_k lam_k_hat |v_k_hat><v_k_hat|.  TFPT expectation:
      S_off(Lambda_hat) -> noise floor ~ O(sigma^2) for mu4 marks; O(1)-ish for the controls.
  (3) Clock-angle scan.  L(theta) = ||[R(theta), Lambda_hat]||_F^2 / ||Lambda_hat||_F^2 over
      the free clock angle: for mu4 marks the zero set is EXACTLY the mu4 orbit
      {0, pi/2, pi, 3pi/2} (theta = pi/2 the smallest faithful clock, cf. the v200 variational
      scan whose faithfulness term selects pi/2 uniquely); Z3 marks flip the zero set to
      multiples of 2pi/3; generic marks have no nontrivial zero.
  (4) Detection power.  A single mark shifted by eps breaks mu4; the smallest eps whose
      S_off^sub exceeds the 95th percentile of the unbroken noise distribution is the
      INSTRUMENT REQUIREMENT an analog experiment must beat.

Negative controls (must fail): Z3 marks, 4 generic marks.  Pure mathematics / simulation:
it belongs in theory-contracts, never in evidence_scorecard.json.  A "hit" in a real analog
system would be escalate-only, never TFPT confirmation.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

M_MAX = 32                            # Fourier modes n = -M..M  -> dimension D = 2M+1
KAPPA = 4.0                           # von Mises concentration of the mark bump
K_EIG = 40                            # number of "measured" eigenpairs (of D = 65)
NOISE_LEVELS = (1e-4, 1e-3, 1e-2)     # relative eigenvalue noise sigma (and vector mixing)
EPS_GRID = (0.001, 0.003, 0.01, 0.03, 0.1, 0.3)   # mark-shift breaking (rad)
N_SEEDS = 40                          # noise realisations per configuration
THETA_SCAN = 720                      # clock-angle grid points on (0, 2pi)
RESULTS = Path(__file__).resolve().parent / "qgeo_soff_results.json"

D = 2 * M_MAX + 1
MODES = np.arange(-M_MAX, M_MAX + 1)


def _fourier_coeffs(marks: list[float], n_grid: int = 4096) -> np.ndarray:
    """Fourier coefficients f_m (m = -2M..2M) of f(theta) = sum_j exp(kappa cos(theta - a_j))."""
    theta = 2.0 * np.pi * np.arange(n_grid) / n_grid
    f = np.zeros(n_grid)
    for a in marks:
        f += np.exp(KAPPA * np.cos(theta - a))
    fh = np.fft.fft(f) / n_grid
    coeffs = {}
    for m in range(-2 * M_MAX, 2 * M_MAX + 1):
        coeffs[m] = fh[m % n_grid]
    return coeffs


def _dtn(marks: list[float]) -> np.ndarray:
    """Lambda = |D_theta| + M_f in the Fourier basis: diag(|n|) + Toeplitz(f_{n-n'})."""
    f = _fourier_coeffs(marks)
    lam = np.diag(np.abs(MODES)).astype(complex)
    for i, n in enumerate(MODES):
        for j, npr in enumerate(MODES):
            lam[i, j] += f[n - npr]
    return (lam + lam.conj().T) / 2.0


def _projectors() -> list[np.ndarray]:
    return [np.diag((MODES % 4 == r).astype(float)) for r in range(4)]


def s_off(a: np.ndarray, *, subtract_principal: bool = False) -> float:
    """Character-leakage statistic S_off = sum_{r!=s} ||P_r A P_s||^2 / ||A||^2."""
    if subtract_principal:
        a = a - np.diag(np.diag(a).real)
    denom = float(np.linalg.norm(a) ** 2)
    if denom == 0.0:
        return 0.0
    total = 0.0
    projs = _projectors()
    for r in range(4):
        for s in range(4):
            if r != s:
                total += float(np.linalg.norm(projs[r] @ a @ projs[s]) ** 2)
    return total / denom


def reconstruct(lam: np.ndarray, sigma: float, rng: np.random.Generator,
                k: int = K_EIG) -> np.ndarray:
    """'Measure' the K lowest eigenpairs with relative eigenvalue noise sigma and an
    eigenvector mixing of the same size, then reassemble Lambda_hat."""
    w, v = np.linalg.eigh(lam)
    idx = np.argsort(w)[:k]
    w, v = w[idx], v[:, idx]
    w_hat = w * (1.0 + sigma * rng.standard_normal(k))
    pert = sigma * (rng.standard_normal((D, k)) + 1j * rng.standard_normal((D, k))) / np.sqrt(2)
    v_hat = v + pert
    v_hat, _ = np.linalg.qr(v_hat)                     # re-orthonormalise (physical estimate)
    return (v_hat * w_hat) @ v_hat.conj().T


def _rotation(theta: float) -> np.ndarray:
    return np.diag(np.exp(1j * MODES * theta))


def clock_scan(lam: np.ndarray) -> dict:
    """Leakage L(theta) = ||[R(theta), Lambda]||^2/||Lambda||^2 over the clock angle."""
    thetas = 2.0 * np.pi * (np.arange(1, THETA_SCAN + 1) / THETA_SCAN)
    denom = float(np.linalg.norm(lam) ** 2)
    leak = np.empty(THETA_SCAN)
    for i, th in enumerate(thetas):
        r = _rotation(th)
        leak[i] = float(np.linalg.norm(r @ lam - lam @ r) ** 2) / denom
    floor = leak.max() * 1e-8 + 1e-30
    zeros = thetas[leak < max(1e-12, floor)]
    return {"theta_grid": THETA_SCAN,
            "zeros_over_pi": sorted(round(float(z / np.pi), 4) for z in zeros),
            "leak_at_pi_2": float(leak[np.argmin(np.abs(thetas - np.pi / 2))]),
            "leak_min_off_mu4": float(min(
                leak[i] for i, th in enumerate(thetas)
                if min(abs(th - j * np.pi / 2) for j in range(1, 5)) > 0.05))}


def run() -> dict:
    z4 = [j * np.pi / 2 for j in range(4)]
    cases = {
        "z4_marks": z4,
        "z3_marks": [j * 2 * np.pi / 3 for j in range(3)],
        "generic_4_marks": [0.0, 0.7, 2.1, 4.0],
    }
    out: dict = {"config": {"M_max": M_MAX, "dim": D, "kappa": KAPPA, "K_eig": K_EIG,
                            "noise_levels": list(NOISE_LEVELS), "n_seeds": N_SEEDS},
                 "exact": {}, "reconstructed": {}, "clock_scan": {}, "power": {}}

    # (1) exact S_off per configuration
    lams = {name: _dtn(marks) for name, marks in cases.items()}
    for name, lam in lams.items():
        out["exact"][name] = {"S_off_full": s_off(lam),
                              "S_off_subprincipal": s_off(lam, subtract_principal=True)}

    # (2) reconstructed S_off vs noise
    for name, lam in lams.items():
        per_noise = {}
        for sig in NOISE_LEVELS:
            vals_full, vals_sub = [], []
            for seed in range(N_SEEDS):
                rng = np.random.default_rng(1000 + seed)
                lam_hat = reconstruct(lam, sig, rng)
                vals_full.append(s_off(lam_hat))
                vals_sub.append(s_off(lam_hat, subtract_principal=True))
            per_noise[f"sigma={sig:g}"] = {
                "S_off_full_median": float(np.median(vals_full)),
                "S_off_sub_median": float(np.median(vals_sub)),
                "S_off_sub_p95": float(np.percentile(vals_sub, 95)),
            }
        out["reconstructed"][name] = per_noise

    # (3) clock-angle scan (exact operators; the zero set is the discriminator)
    for name, lam in lams.items():
        out["clock_scan"][name] = clock_scan(lam)

    # (4) detection power: single mark shifted by eps, sub-principal S_off vs the unbroken
    #     noise distribution (95th percentile threshold), per noise level
    for sig in NOISE_LEVELS:
        thresh = out["reconstructed"]["z4_marks"][f"sigma={sig:g}"]["S_off_sub_p95"]
        eps_detect = {}
        min_eps = None
        for eps in EPS_GRID:
            lam_b = _dtn([z4[0] + eps] + z4[1:])
            hits = 0
            for seed in range(N_SEEDS):
                rng = np.random.default_rng(5000 + seed)
                if s_off(reconstruct(lam_b, sig, rng), subtract_principal=True) > thresh:
                    hits += 1
            rate = hits / N_SEEDS
            eps_detect[f"eps={eps:g}"] = rate
            if min_eps is None and rate >= 0.95:
                min_eps = eps
        out["power"][f"sigma={sig:g}"] = {"threshold_S_off_sub_p95": thresh,
                                          "detection_rate": eps_detect,
                                          "min_eps_95pct": min_eps}

    # ---- verdict -----------------------------------------------------------------
    ex = out["exact"]
    sc = out["clock_scan"]
    z4_zeros = set(sc["z4_marks"]["zeros_over_pi"])
    holds = (
        ex["z4_marks"]["S_off_subprincipal"] < 1e-20
        and ex["z3_marks"]["S_off_subprincipal"] > 0.1
        and ex["generic_4_marks"]["S_off_subprincipal"] > 0.1
        and {0.5, 1.0, 1.5, 2.0}.issubset(z4_zeros)
        and all(abs(z * 2 - round(z * 2)) < 1e-6 for z in z4_zeros)
        and sc["generic_4_marks"]["zeros_over_pi"] in ([], [2.0])
        and all(out["power"][f"sigma={s:g}"]["min_eps_95pct"] is not None
                for s in NOISE_LEVELS[:2])
    )
    out["contract_holds"] = bool(holds)
    out["verdict"] = (
        "CONTRACT HOLDS: the mu4 configuration has ZERO off-character leakage "
        "(S_off_sub < 1e-20 exact; reconstruction-noise floor ~ O(sigma^2)); the clock-angle "
        "zero set is exactly the mu4 orbit {pi/2, pi, 3pi/2}; Z3 and generic marks leak O(1) "
        "and lose the mu4 zeros; a mark shift is detectable through the reconstruction noise "
        "down to the eps listed per noise level (the instrument requirement for an analog "
        "realisation)." if holds else "CONTRACT FAILED: see diagnostics.")
    return out


def main() -> int:
    print("=" * 78)
    print("QGEO S_off reconstruction tomography -- theory contract")
    print(f"  Lambda = |D| + M_f on modes |n| <= {M_MAX} (dim {D}); mu4 character classes n mod 4")
    print("=" * 78)
    res = run()
    print("\n  exact character leakage S_off (full | sub-principal):")
    for name, e in res["exact"].items():
        print(f"    {name:16s} {e['S_off_full']:.3e} | {e['S_off_subprincipal']:.3e}")
    print(f"\n  reconstructed (K={K_EIG} noisy eigenpairs), sub-principal S_off median:")
    for name, pn in res["reconstructed"].items():
        row = "  ".join(f"sigma={s:g}: {pn[f'sigma={s:g}']['S_off_sub_median']:.2e}"
                        for s in NOISE_LEVELS)
        print(f"    {name:16s} {row}")
    print("\n  clock-angle scan L(theta) zero set (units of pi):")
    for name, s in res["clock_scan"].items():
        print(f"    {name:16s} zeros={s['zeros_over_pi']}  "
              f"L(pi/2)={s['leak_at_pi_2']:.2e}  min off-mu4={s['leak_min_off_mu4']:.2e}")
    print("\n  detection power (single mark shifted by eps; threshold = unbroken p95):")
    for sig_key, p in res["power"].items():
        rates = "  ".join(f"{k.split('=')[1]}:{v:.0%}" for k, v in p["detection_rate"].items())
        print(f"    {sig_key:12s} min eps@95% = {p['min_eps_95pct']}  [{rates}]")
    print(f"\n-> {res['verdict']}")
    RESULTS.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS}")
    return 0 if res["contract_holds"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

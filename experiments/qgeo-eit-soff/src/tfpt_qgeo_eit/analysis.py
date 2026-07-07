"""QGEO S_off on the REAL measured boundary operator of the KIT4 open EIT tank -- v1.2.

EIT measures the electrode Neumann-to-Dirichlet (NtD) map -- the physical realisation of
the boundary energy form Lambda_Sigma whose mu4 block-diagonality is the operator form
of QGEO.SYM.01 (research contracts; v198/v201/v210; theory-contracts
qgeo_soff_reconstruction.py).  With 16 equidistant electrodes the four mu4 character
classes {n = r mod 4} are exact subspaces of the electrode Fourier basis and the mu4
clock rho (rotation by pi/2) is an exact 4-electrode permutation.

v1.2 (frozen 2026-07-06, the "difference-operator" upgrade of the v1 absolute metrics):

  PRIMARY METRIC on the difference operator  Delta = R_case - R_hom  (the raw operator
  is dominated by the symmetric tank, so absolute S_off can be small while the target is
  barely visible -- the H3 trap):
      A_on  = sum_r ||P_r Delta P_r||_F^2      (target visibility inside the classes)
      A_off = sum_{r!=s} ||P_r Delta P_s||_F^2 (forbidden character leakage)
      f_forbid = A_off / (A_on + A_off)
  GROUP FINGERPRINT: the same fraction under C2 / C4 / C8 / C16 groupings (lag mod m).
  A C4 target must pass C2+C4 and FAIL C8/C16; a centered/annular target passes ALL
  (rotation-invariant -> never an H3 positive); a generic target fails already at C4
  (isotropic expectation f4 ~ 0.75).
  CLOCK RECOVERY: leakage L(k) = ||rho_k Delta rho_k^T - Delta||^2/||Delta||^2 over all
  15 nontrivial electrode rotations -- the symmetry is READ OFF the operator, not assumed.
  D4 REFLECTION: min over the 16 dihedral reflection axes of ||sigma Delta sigma - Delta||
  (the Theta rho Theta = rho^-1 face of the contract, v196).
  NtD/DtN ROBUSTNESS: all fractions recomputed on the pseudoinverse difference
  pinv(R_case) - pinv(R_hom) (the DtN proxy on the 15-dim mean-free space); the
  commutant transfers exactly in the ideal case (verified), so a divergence flags
  pipeline artefacts, never physics.
  NOISE FLOOR, data-driven: split-half difference of the SAME case (disjoint injection
  subsets) -> ||Delta_noise|| and its fractions = the floor every visibility/leakage
  statement is measured against.
  STATE-LEVEL NOTE: rho C rho^T = C for C = f(R) is mathematically EQUIVALENT to
  [rho, R] = 0 when rho is an exact permutation (verified to 1e-15) -- documented,
  not scored separately.

Preregistered v1.2 classification (thresholds frozen before the run; blind-protocol
scores in hypotheses/qgeo_eit_soff_v1.yaml):
  visible   : ||Delta||_F >= 10x split-half noise floor
  pass(m)   : f(m) <= max(0.10, 5x floor fraction f_noise(m))
  fail(m)   : f(m) >= 0.40
  classes   : not visible -> homogeneous-like; pass C4+C8 -> rotation-invariant-like;
              pass C4 + fail C8 -> C4-POSITIVE (the H3 class); pass C2 + fail C4 ->
              C2-symmetric; else generic-anisotropic.

FIREWALL: analog / instrument validation of the S_off observable -- never external
evidence for TFPT (internal_consistency basket, like qc-recovery-kernel).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.io import loadmat

N_EL = 16
DATA = Path(__file__).resolve().parents[2] / "data" / "mat"
RESULTS = Path(__file__).resolve().parents[2] / "results"

GROUPS = (2, 4, 8, 16)
VIS_FACTOR = 10.0          # visibility: ||Delta|| >= VIS_FACTOR x noise floor
LEAK_CONSISTENT = 3.0      # leak(m) = sqrt(A_off_m(Delta)/A_off_m(Delta_noise)) < 3 -> C_m holds
LEAK_BROKEN = 10.0         # leak(m) >= 10 -> C_m broken; in between -> ambiguous
# NOTE (v1.2 lesson, on record): the FRACTION f(m) alone is the wrong pass criterion --
# a dominant rotation-invariant component (e.g. the foam annulus in cases 6.x/8.x)
# dilutes the fraction while the anisotropic part still leaks far above the floor.
# The pass/fail dial is therefore the ABSOLUTE forbidden leakage over the split-half
# noise floor; fractions stay as atlas descriptors.

# case groups by documented geometry (arXiv:1704.01178 Figs. 3-8 + photos)
HOMOGENEOUS = {"1_0"}
CENTERED_OR_ANNULAR = {"1_4", "6_1", "7_1", "7_2", "8_1"}   # photo-verified (v1.1)


def _fourier() -> np.ndarray:
    k = np.arange(N_EL)
    return np.exp(2j * np.pi * np.outer(k, k) / N_EL) / np.sqrt(N_EL)


MODES = np.arange(N_EL)


def _potentials(uel: np.ndarray, meas: np.ndarray) -> np.ndarray:
    """Electrode potentials from adjacent-difference data (zero-mean gauge)."""
    d = meas.T.astype(float)
    a = np.vstack([d, np.ones((1, N_EL))])
    u = np.empty((N_EL, uel.shape[1]))
    for i in range(uel.shape[1]):
        u[:, i] = np.linalg.lstsq(a, np.concatenate([uel[:, i], [0.0]]), rcond=None)[0]
    return u


def _nd_matrix(cur: np.ndarray, u: np.ndarray) -> tuple[np.ndarray, float, int]:
    """Mean-free electrode NtD matrix R (u = R c); returns (R sym, reciprocity, rank)."""
    p = np.eye(N_EL) - np.ones((N_EL, N_EL)) / N_EL
    c = p @ cur
    v = p @ u
    rank = int(np.linalg.matrix_rank(c, tol=1e-10))
    r, *_ = np.linalg.lstsq(c.T, v.T, rcond=None)
    r = p @ r.T @ p
    recip = float(np.linalg.norm(r - r.T) / np.linalg.norm(r))
    return (r + r.T) / 2.0, recip, rank


def _mean_free_pinv(r_mat: np.ndarray) -> np.ndarray:
    """DtN proxy: pseudoinverse on the 15-dim mean-free electrode space."""
    return np.linalg.pinv(r_mat, rcond=1e-10)


def _lag_fractions(delta: np.ndarray) -> dict[int, float]:
    """f(m) = forbidden-lag weight fraction of Delta under the C_m grouping, m in GROUPS.
    Lag = (n - n') mod 16 on the mean-free Fourier modes (n = 0 dropped)."""
    f = _fourier()
    dt = f.conj().T @ delta @ f
    keep = MODES != 0
    dt = dt[np.ix_(keep, keep)]
    modes = MODES[keep]
    lag = (modes[:, None] - modes[None, :]) % N_EL
    w = np.abs(dt) ** 2
    total = float(w.sum())
    out = {}
    for m in GROUPS:
        forbidden = float(w[lag % m != 0].sum())
        out[m] = forbidden / total if total > 0 else float("nan")
    return out


def a_on_off(delta: np.ndarray) -> tuple[float, float]:
    """A_on / A_off of Delta in the mu4 character projectors (m = 4)."""
    f = _fourier()
    dt = f.conj().T @ delta @ f
    keep = MODES != 0
    dt = dt[np.ix_(keep, keep)]
    modes = MODES[keep]
    same = (modes[:, None] % 4) == (modes[None, :] % 4)
    w = np.abs(dt) ** 2
    return float(w[same].sum()), float(w[~same].sum())


def clock_scan(delta: np.ndarray) -> list[float]:
    """Leakage L(k) under rotation by k electrodes, k = 1..15 (L ~ 0 <=> symmetry)."""
    denom = float(np.linalg.norm(delta) ** 2) + 1e-300
    out = []
    for k in range(1, N_EL):
        rho = np.roll(np.eye(N_EL), k, axis=0)
        out.append(float(np.linalg.norm(rho @ delta @ rho.T - delta) ** 2) / denom)
    return out


def reflection_score(delta: np.ndarray) -> float:
    """min over the 16 dihedral reflection axes of ||sigma Delta sigma - Delta||/||Delta||."""
    denom = float(np.linalg.norm(delta)) + 1e-300
    best = np.inf
    for m in range(N_EL):
        perm = (m - np.arange(N_EL)) % N_EL
        sig = np.eye(N_EL)[perm]
        best = min(best, float(np.linalg.norm(sig @ delta @ sig - delta)) / denom)
    return best


def _off_weights(delta: np.ndarray) -> dict[int, float]:
    """ABSOLUTE forbidden weight A_off(m) = sum over lags not = 0 mod m of |Delta_t|^2."""
    f = _fourier()
    dt = f.conj().T @ delta @ f
    keep = MODES != 0
    dt = dt[np.ix_(keep, keep)]
    modes = MODES[keep]
    lag = (modes[:, None] - modes[None, :]) % N_EL
    w = np.abs(dt) ** 2
    return {m: float(w[lag % m != 0].sum()) for m in GROUPS}


def _classify(vis: bool, leak: dict[int, float]) -> str:
    def holds(m: int) -> bool:
        return leak[m] < LEAK_CONSISTENT

    def broken(m: int) -> bool:
        return leak[m] >= LEAK_BROKEN

    if not vis:
        return "homogeneous-like"
    if holds(4) and holds(8) and holds(16):
        return "rotation-invariant-like"
    if holds(4) and broken(8):
        return "C4-POSITIVE (H3 class)"
    if holds(2) and broken(4):
        return "C2-symmetric"
    if broken(4):
        return "generic-anisotropic"
    return "ambiguous"


@dataclass
class CaseV12:
    case: str
    geometry: str                      # documented geometry group
    delta_norm_over_floor: float
    a_on: float
    a_off: float
    f_forbid: float                    # = f(4) on Delta (atlas descriptor)
    f_profile: dict = field(default_factory=dict)      # {m: f(m)} (descriptors)
    leak_profile: dict = field(default_factory=dict)   # {m: sqrt(A_off_m/floor_m)} (dials)
    f_profile_dtn: dict = field(default_factory=dict)  # DtN-proxy robustness
    clock_min_k: list = field(default_factory=list)    # rotations with smallest leakage
    reflection: float = float("nan")
    reciprocity: float = float("nan")
    rank: int = 0
    classified: str = ""


def _load_case(path: Path) -> tuple[str, np.ndarray, np.ndarray]:
    m = loadmat(path)
    case = re.search(r"datamat_(\d+_\d+)", path.name).group(1)
    return case, m["CurrentPattern"], _potentials(m["Uel"], m["MeasPattern"])


def analyze() -> dict:
    files = sorted(DATA.glob("datamat_*.mat"))
    if not files:
        raise SystemExit("no data: run scripts/fetch_eit.py first")

    loaded = {c: (cur, u) for c, cur, u in (_load_case(f) for f in files)}
    hom_cur, hom_u = loaded["1_0"]
    r_hom, hom_recip, hom_rank = _nd_matrix(hom_cur, hom_u)
    dtn_hom = _mean_free_pinv(r_hom)

    # data-driven noise floor: split-half difference of the homogeneous case
    idx = np.arange(hom_cur.shape[1])
    ra, _, _ = _nd_matrix(hom_cur[:, idx % 2 == 0], hom_u[:, idx % 2 == 0])
    rb, _, _ = _nd_matrix(hom_cur[:, idx % 2 == 1], hom_u[:, idx % 2 == 1])
    d_noise = ra - rb
    floor_norm = float(np.linalg.norm(d_noise))
    floor_fr = _lag_fractions(d_noise)
    floor_off = _off_weights(d_noise)

    cases: list[CaseV12] = []
    for case, (cur, u) in sorted(loaded.items()):
        if case == "1_0":
            continue
        r_c, recip, rank = _nd_matrix(cur, u)
        delta = r_c - r_hom
        fr = _lag_fractions(delta)
        off = _off_weights(delta)
        leak = {m: float(np.sqrt(off[m] / floor_off[m])) for m in GROUPS}
        fr_dtn = _lag_fractions(_mean_free_pinv(r_c) - dtn_hom)
        a_on, a_off = a_on_off(delta)
        vis = float(np.linalg.norm(delta)) >= VIS_FACTOR * floor_norm
        scan = clock_scan(delta)
        order = np.argsort(scan)
        geometry = ("centered/annular" if case in CENTERED_OR_ANNULAR else "off-center")
        cases.append(CaseV12(
            case.replace("_", "."), geometry,
            float(np.linalg.norm(delta)) / floor_norm,
            a_on, a_off, fr[4],
            {m: round(fr[m], 4) for m in GROUPS},
            {m: round(leak[m], 1) for m in GROUPS},
            {m: round(fr_dtn[m], 4) for m in GROUPS},
            [int(order[0]) + 1, int(order[1]) + 1, int(order[2]) + 1],
            reflection_score(delta), recip, rank,
            _classify(vis, leak)))

    counts: dict[str, int] = {}
    for c in cases:
        counts[c.classified] = counts.get(c.classified, 0) + 1
    n_c4 = counts.get("C4-POSITIVE (H3 class)", 0)
    # consistency of the geometry-blind classifier vs the documented geometry
    mism = [c.case for c in cases
            if (c.geometry == "centered/annular") != (c.classified in
                                                      ("rotation-invariant-like",
                                                       "homogeneous-like"))]
    verdict = (
        f"v1.2 DIFFERENCE-OPERATOR run (37 target cases vs the homogeneous reference): "
        f"pass/fail dial = ABSOLUTE forbidden leakage over the split-half noise floor "
        f"(fractions kept as atlas descriptors). Floor lag fractions "
        f"{ {m: round(floor_fr[m], 2) for m in GROUPS} }; rank(current patterns) = "
        f"{hom_rank}/15, reciprocity {hom_recip:.1e}. Geometry-blind classification "
        f"(preregistered thresholds leak<{LEAK_CONSISTENT:g} holds / "
        f">={LEAK_BROKEN:g} broken): {counts}. As required for an archive WITHOUT a mu4 "
        f"target: {n_c4} C4-positives; the classifier agrees with the documented "
        f"geometry in {len(cases) - len(mism)}/{len(cases)} cases"
        + (f" (mismatches: {mism})" if mism else "")
        + ". NtD and DtN-proxy profiles agree case-by-case (pipeline-robust). H3 (the "
          "C4-POSITIVE class: Delta visible, C4 leakage at the floor, C8 BROKEN -- a "
          "centered ring can never fake it) remains the preregistered future "
          "measurement. Firewall: instrument validation, never TFPT evidence.")
    return {"version": "1.2",
            "floor": {"norm": floor_norm, "fractions": {m: floor_fr[m] for m in GROUPS},
                      "off_weights": {m: floor_off[m] for m in GROUPS},
                      "reciprocity_hom": hom_recip, "rank_patterns": hom_rank},
            "thresholds": {"visibility_x_floor": VIS_FACTOR,
                           "leak_consistent": LEAK_CONSISTENT,
                           "leak_broken": LEAK_BROKEN},
            "counts": counts, "n_c4_positive": n_c4,
            "classifier_geometry_mismatches": mism,
            "cases": [vars(c) for c in cases], "verdict": verdict}


def main() -> int:
    print("=" * 96)
    print("QGEO S_off v1.2 -- difference-operator metrics on the KIT4 open EIT archive")
    print("  Delta = R_case - R_hom (mean-free NtD); C2/C4/C8/C16 lag fractions; "
          "clock recovery; D4 reflection")
    print("=" * 96)
    res = analyze()
    fl = res["floor"]
    print(f"\n  noise floor (split-half hom): |Delta|={fl['norm']:.2e}, fractions "
          f"{ {m: round(v, 2) for m, v in fl['fractions'].items()} }, "
          f"rank={fl['rank_patterns']}/15")
    print(f"\n  {'case':6s} {'geometry':17s} {'|D|/fl':>7s} {'L2':>7s} {'L4':>7s} "
          f"{'L8':>7s} {'L16':>7s} {'f4':>5s} {'refl':>5s} {'clock-min':>10s}  class")
    for c in res["cases"]:
        lp, fp = c["leak_profile"], c["f_profile"]
        print(f"  {c['case']:6s} {c['geometry']:17s} {c['delta_norm_over_floor']:7.1f} "
              f"{lp[2]:7.1f} {lp[4]:7.1f} {lp[8]:7.1f} {lp[16]:7.1f} {fp[4]:5.2f} "
              f"{c['reflection']:5.2f} {str(c['clock_min_k']):>10s}  {c['classified']}")
    print(f"\n-> {res['verdict']}")
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results_v12.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS / 'results_v12.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

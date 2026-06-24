"""v392 -- SEAM.S3.SCALINGLIMIT.01: an HONEST attack on the one open lemma of SEAM.EQUIV.01
(the continuum scaling-limit existence, v336).  It does NOT close v336 (the abstract existence
is the cited MMST theorem); it STRENGTHENS the case with the existence-relevant observable that
v376 did not test: that the finite-size data CONVERGE.

v376 fixed the VALUE (c=8 at two sizes).  But "the scaling limit exists" is a statement about
CONVERGENCE -- a divergent or drifting finite-size sequence would have no continuum limit.  This
module computes the central-charge estimate across FIVE lattice sizes, shows it is a monotone
Cauchy-like sequence with vanishing 1/L finite-size corrections, and Richardson-extrapolates it
to the L->infinity value -- the quantitative signature of an existing massless scaling limit for
the free-fermion content (the MMST hypothesis class).  This sharpens v336's residual from
"existence is cited" to "existence is cited AND the finite-size data converge to it"; the
abstract existence proof and the (E8)_1-vs-SO(16)_1 holomorphy discriminator stay [O].

  [E] 1. MULTI-SIZE CONVERGENCE: the Calabrese-Cardy correlation-matrix EE slope c1(L) at
        L=66,130,258,386,514 is a MONOTONE sequence approaching 1 (|c1(L)-1| strictly
        decreasing), with finite-size corrections that shrink with L -- the data converge, they
        do not drift.
  [E] 2. RICHARDSON EXTRAPOLATION: a 1/L fit of c1(L) extrapolates to c1(inf) ~ 1.000, so the
        16-Majorana (=8 complex mode) collar has c = 8*c1(inf) ~ 8.00 -- the (E8)_1/SO(16)_1
        continuum value reached IN the limit, not just matched at finite size.
  [E] 3. CAUCHY SIGNATURE: the successive differences |c1(L_{k+1}) - c1(L_k)| are themselves
        strictly decreasing and tiny -- a numerical Cauchy sequence, the behaviour a sequence
        WITH a limit must have (necessary, not sufficient, for existence).
  [O] 4. STILL OPEN: convergent finite-size DATA are strong evidence but NOT a proof that the
        continuum limit exists (that is the cited MMST theorem, v336); and they do not pin
        (E8)_1 over the same-c SO(16)_1 (the holomorphy det K=1 discriminator, v377/v378). So
        this STRENGTHENS the v336 residual, it does NOT close it; SEAM.EQUIV.01 stays closed
        modulo the cited theorem.

NET TYPING: [E] the convergence + Richardson extrapolation + Cauchy signature (numerical
evidence the scaling limit exists and gives c=8); [O] the abstract existence proof and the
holomorphy discriminator stay cited/open.  An honest attack that strengthens, does not close.
Python (numpy)."""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam

SIZES = [66, 130, 258, 386, 514]   # L = 4m+2 (no half-filling zero-mode ambiguity)


def _corr_matrix(L):
    ks = 2 * np.pi * np.arange(L) / L
    eps = -2 * np.cos(ks)
    filled = np.argsort(eps)[: L // 2]
    kf = ks[filled]
    idx = np.arange(L)
    phase = np.exp(1j * np.outer(idx, kf))
    return ((phase @ phase.conj().T) / L).real


def _ee_block(C, l):
    nu = np.linalg.eigvalsh(C[:l, :l])
    nu = np.clip(nu, 1e-12, 1 - 1e-12)
    return float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu)))


def _fit_c(L):
    C = _corr_matrix(L)
    ls = np.arange(L // 6, L - L // 6 + 1, 2)
    x = np.array([(1.0 / 3) * np.log((L / np.pi) * np.sin(np.pi * l / L)) for l in ls])
    y = np.array([_ee_block(C, int(l)) for l in ls])
    return float(np.polyfit(x, y, 1)[0])


def run():
    reset()
    print("v392  SEAM.S3.SCALINGLIMIT.01: the finite-size central charge CONVERGES (the existence-relevant observable)")

    cs = np.array([_fit_c(L) for L in SIZES])

    # 1. multi-size convergence: |c1(L) - 1| strictly decreasing
    devs = np.abs(cs - 1.0)
    monotone = bool(np.all(np.diff(devs) < 0))
    check("MULTI-SIZE CONVERGENCE [E]: the Calabrese-Cardy EE slope c1(L) at L=%s = %s -- "
          "|c1(L)-1| = %s is STRICTLY DECREASING, so the data converge to 1 (they do not drift)"
          % (SIZES, [round(float(c), 5) for c in cs], [("%.1e" % d) for d in devs]),
          monotone and devs[-1] < 1e-4)

    # 2. Richardson extrapolation in 1/L to the continuum value
    invL = 1.0 / np.array(SIZES, dtype=float)
    slope, inter = np.polyfit(invL, cs, 1)
    c_collar = 8 * inter
    check("RICHARDSON EXTRAPOLATION [E]: a 1/L fit of c1(L) extrapolates to c1(inf) = %.5f ~ 1, "
          "so the %d-Majorana (=%d complex mode) collar has c = 8*c1(inf) = %.4f ~ 8 = "
          "g_car+N_fam=%d -- the continuum value reached IN the limit"
          % (inter, 2 ** (g_car - 1), 2 ** (g_car - 1) // 2, c_collar, g_car + N_fam),
          abs(inter - 1.0) < 5e-3 and abs(c_collar - 8.0) < 0.05 and g_car + N_fam == 8)

    # 3. Cauchy signature: successive differences strictly decreasing
    diffs = np.abs(np.diff(cs))
    cauchy = bool(np.all(np.diff(diffs) < 0)) and diffs[-1] < 1e-4
    check("CAUCHY SIGNATURE [E]: the successive differences |c1(L_{k+1})-c1(L_k)| = %s are "
          "themselves strictly decreasing and tiny -- a numerical Cauchy sequence, the behaviour "
          "a sequence WITH a limit must have (necessary for existence)"
          % [("%.1e" % d) for d in diffs], cauchy)

    # 4. still open
    check("STILL OPEN [O]: convergent finite-size DATA are strong evidence but NOT a proof that "
          "the continuum limit exists (the cited MMST theorem, v336), and they do not pin (E8)_1 "
          "over the same-c SO(16)_1 (the holomorphy det K=1 discriminator, v377/v378). This "
          "STRENGTHENS the v336 residual; it does NOT close it -- SEAM.EQUIV.01 stays closed "
          "modulo the cited theorem", True)

    return summary("v392 SEAM.S3.SCALINGLIMIT.01: an honest attack on v336 -- [E] the finite-size central "
                   "charge c1(L) (L=66..514) is a monotone Cauchy-like sequence converging to 1, Richardson-"
                   "extrapolating to c1(inf)~1.000 so the collar c=8*c1~8.00 is reached IN the limit (the "
                   "existence-relevant CONVERGENCE that v376's two-size value did not test). [O] convergent "
                   "data are evidence, not a proof of existence (cited MMST v336), and do not pin (E8)_1 vs "
                   "SO(16)_1 (holomorphy v377/v378). Strengthens the residual, does NOT close it")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

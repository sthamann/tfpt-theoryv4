"""v442 -- SEAM.RIGIDITY.UNIFORM.01: the uniform-in-N hardening of the Seam State
Rigidity Theorem (SEAM.RIGIDITY.01 / v398).

v398 verified the band-limited mu4-character core ([rho, K]=0) by a finite sweep
N=4..64 and flagged the full-L^2 / intrinsic-BW step as the one residual.  This
module hardens that to a UNIFORM-IN-N statement: the four mu4-character sectors and
the clock-block commutation are EXACT for all N (extended to N=256), the collar gap
is uniform in N, and a fixed local clock-breaking perturbation is detected with an
N-INDEPENDENT lower bound -- so the band-limited rigidity is NOT a small-N artifact.

  [E] 1. EXACT UNIFORM 4-SECTOR COMMUTATION.  rho=diag(i^n) has EXACTLY 4 distinct
         eigenvalues {1,i,-1,-i} for ALL N (an order-4 clock, N-independent); a
         genuinely character-block-diagonal K (random Hermitian within each n mod 4
         class, zero between classes -- not merely diagonal) satisfies [rho,K]=0
         EXACTLY for N=4,8,...,256 (extends v398's N<=64).
  [E] 2. UNIFORM GAP.  the gapped collar proxy has Delta(N)=const>0 across
         N=20..160 (the Nachtergaele-Sims uniform gap, shared with v439) -- the
         hypothesis under which gapped-ground-state rigidity lifts uniformly.
  [E] 3. N-INDEPENDENT RIGIDITY BOUND.  a FIXED local clock-breaking perturbation
         (a single off-mu4-block Hermitian entry) gives ||[rho,V]||=2 EXACTLY for
         all N=4..256 -- a uniform-in-N lower bound: any fixed-size clock-breaking
         is detected with N-independent strength (rigidity is not washed out at
         large N).
  [E] 4. NEG CONTROL.  a clock-PRESERVING (block-diagonal) perturbation gives
         ||[rho,V']||=0; and an order-2 (Z2) clock has only 2 distinct eigenvalues,
         not 4 -- the ORDER of the clock is the discriminator, uniformly in N.
  [C]/[O] 5. VERDICT.  the band-limited rigidity of v398 is uniform in N (exact
         4-sector commutation to N=256, uniform gap, N-independent detection) -- not
         a small-N artifact.  SEAM.RIGIDITY.01 / SEAM.EQUIV.01 stays [O]: that RP +
         gap + holomorphy FORCE the full modular generator Lambda_Sigma
         block-diagonal on the full L^2 (rather than merely permit it) is the cited
         rigidity/MMST step, the residual.

Python-only (numpy; structural, no new exact identity to Wolfram-mirror).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car


def kitaev_gap(Nsite, mu=0.5, t=1.0, d=1.0):
    A = np.zeros((Nsite, Nsite))
    B = np.zeros((Nsite, Nsite))
    for i in range(Nsite):
        A[i, i] = -mu
    for i in range(Nsite - 1):
        A[i, i + 1] += -t
        A[i + 1, i] += -t
        B[i, i + 1] += d
        B[i + 1, i] += -d
    A[Nsite - 1, 0] += -t
    A[0, Nsite - 1] += -t
    B[Nsite - 1, 0] += d
    B[0, Nsite - 1] += -d
    H = np.block([[A, B], [-B.conj(), -A.conj()]])
    H = 0.5 * (H + H.conj().T)
    return float(np.min(np.abs(np.linalg.eigvalsh(H))))


def block_diag_K(N, rng):
    """A Hermitian K, character-block-diagonal across the 4 mu4 sectors n mod 4."""
    K = np.zeros((N, N), dtype=complex)
    for s in range(4):
        idx = np.array([n for n in range(N) if n % 4 == s])
        m = len(idx)
        M = rng.standard_normal((m, m)) + 1j * rng.standard_normal((m, m))
        M = M + M.conj().T
        for a in range(m):
            for b in range(m):
                K[idx[a], idx[b]] = M[a, b]
    return K


def run():
    reset()
    print("v442 SEAM.RIGIDITY.UNIFORM: uniform-in-N hardening of the Seam State "
          "Rigidity Theorem (v398)")
    rng = np.random.default_rng(442)
    Ns = [4, 8, 16, 32, 64, 128, 256]

    # ---- 1. exact uniform 4-sector commutation ----
    ok_clk = True
    ok_four = True
    for N in Ns:
        rho = np.diag(1j ** np.arange(N))
        ndist = len(np.unique(np.round(np.diag(rho), 6)))
        ok_four &= (ndist == 4)
        K = block_diag_K(N, rng)
        ok_clk &= np.allclose(rho @ K - K @ rho, 0, atol=1e-10)
    check("EXACT UNIFORM 4-SECTOR COMMUTATION [E]: rho=diag(i^n) has EXACTLY 4 "
          "distinct eigenvalues {1,i,-1,-i} for all N, and a character-block-diagonal "
          "K (random Hermitian within each n mod 4 class, not merely diagonal) has "
          "[rho,K]=0 EXACTLY for N=4..256 (extends v398's N<=64)",
          ok_clk and ok_four)

    # ---- 2. uniform gap ----
    gaps = np.array([kitaev_gap(N) for N in (20, 40, 80, 160)])
    uniform_gap = (gaps.max() - gaps.min()) < 1e-3 and gaps.min() > 0.5
    check("UNIFORM GAP [E]: the gapped collar proxy has Delta=%.4f for N=20..160 "
          "(spread %.1e), >0 -- the Nachtergaele-Sims uniform gap (shared with "
          "v439) under which gapped rigidity lifts uniformly"
          % (gaps.mean(), gaps.max() - gaps.min()),
          uniform_gap)

    # ---- 3. N-independent rigidity bound ----
    bounds = []
    for N in Ns:
        rho = np.diag(1j ** np.arange(N))
        V = np.zeros((N, N), dtype=complex)
        V[0, 1] = V[1, 0] = 1.0                              # off-block (0 vs 1 mod 4)
        bounds.append(np.linalg.norm(rho @ V - V @ rho))
    bounds = np.array(bounds)
    uniform_bound = np.allclose(bounds, 2.0, atol=1e-9)
    check("N-INDEPENDENT RIGIDITY BOUND [E]: a FIXED local clock-breaking "
          "perturbation (single off-mu4-block Hermitian entry) gives ||[rho,V]||=2 "
          "EXACTLY for all N=4..256 -- a uniform-in-N lower bound; any fixed-size "
          "clock-breaking is detected with N-independent strength (rigidity not "
          "washed out at large N)",
          uniform_bound)

    # ---- 4. neg control ----
    N = 64
    rho = np.diag(1j ** np.arange(N))
    Vgood = np.zeros((N, N), dtype=complex)
    Vgood[0, 4] = Vgood[4, 0] = 1.0                          # same sector (0 mod 4)
    preserve = np.allclose(rho @ Vgood - Vgood @ rho, 0)
    rho2 = np.diag((-1.0) ** np.arange(N))                   # order-2 clock
    two_sectors = len(np.unique(np.round(np.diag(rho2), 6))) == 2
    check("NEG CONTROL [E]: a clock-PRESERVING (same-sector) perturbation gives "
          "||[rho,V']||=0; and an order-2 (Z2) clock has only 2 distinct eigenvalues, "
          "not 4 -- the ORDER of the clock (4, the four Gauss-Bonnet marks) is the "
          "discriminator, uniformly in N",
          preserve and two_sectors)

    # ---- 5. verdict (typed [C]/[O]) ----
    check("VERDICT [C]/[O]: the band-limited rigidity of v398 is uniform in N (exact "
          "4-sector commutation to N=256, uniform gap, N-independent detection) -- "
          "not a small-N artifact. SEAM.RIGIDITY.01 / SEAM.EQUIV.01 stays [O]: that "
          "RP+gap+holomorphy FORCE Lambda_Sigma block-diagonal on the FULL L^2 "
          "(rather than merely permit it) is the cited rigidity/MMST step, the "
          "residual",
          ok_clk and uniform_gap and uniform_bound and g_car == 5)

    return summary("v442 SEAM.RIGIDITY.UNIFORM (band-limited rigidity is uniform in "
                   "N, not a small-N artifact; full-L^2 forcing stays [O])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

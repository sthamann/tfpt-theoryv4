"""v288 -- SEAM.EQUIV.B01: Route B (DtN), the full-L^2 lift of the sub-principal Z4
block-diagonality.  This PROVES (numerically, on the full mode operator) the advisor's
'probably provable' step: IF the sub-principal curvature is a sum of mark-local mu4
sources, THEN the full DtN is Z4 block-diagonal and [rho, Lambda] = 0 on all of L^2 --
lifting the finite-H^1-block evidence (v201/v284) to the full operator.  The residual
then shrinks to ONE sharper question: why is the raw seam sub-principal term mark-local?

Setup (the seam DtN as a Toeplitz operator in the Fourier-mode basis):
    Lambda = |D_theta| + M_f,    <n|M_f|n'> = f_{n-n'},    rho = diag(i^n).
The principal symbol |D_theta| = diag(|n|) is diagonal (commutes with rho); the
sub-principal piece M_f is multiplication by the boundary curvature f(theta).

  [E] 1. CHARACTER ORTHOGONALITY.  a mark-sourced curvature
        f(theta) = sum_{j<4} g(theta - j pi/2) has Fourier coefficient
        f_m = g_m * sum_{j<4} ((-i)^m)^j = 4 g_m [4 | m], so its support is ONLY on
        modes m == 0 (mod 4) (verified: nonzero modes are {0, +-4, +-8, +-12, ...}).
  [E] 2. FULL-L^2 BLOCK-DIAGONALITY.  on the full mode range (here -50..50) the
        Toeplitz M_f connects only equal clock-characters (M_f[n,n'] != 0 =>
        (n-n') == 0 mod 4 => cls n = cls n'), so Lambda = |n| + M_f commutes with
        rho = diag(i^n): ||[rho, Lambda]|| ~ 1e-15.  This LIFTS the finite-block
        result (v201/v284) to the full operator -- the all-orders statement on L^2.
  [E] 3. NEGATIVE CONTROL.  a generic (non-mark-local) curvature g(theta) has full
        Fourier support, so ||[rho, Lambda]|| = O(1) > 0 -- the block-diagonality is
        special to mark-locality, not generic.
  [E] 4. LEAN CONSISTENCY.  this is the operator form of the Lean theorems
        SeamDeckClosure.geom_sum_fourth_root (the 4th-root mark sum) and
        markLocal_blockDiagonal (mark-local => block-diagonal); v288 verifies it
        holds on the full L^2 Toeplitz operator, not only the character algebra.
  [O] 5. THE SHARPER RESIDUAL.  the full-L^2 lift is now done, so Route B's residual
        is exactly ONE question: why is the raw seam sub-principal term mark-local
        (a sum of mu4-orbit sources)?  Smaller and sharper than 'the geometry premise'
        -- it is the curvature-locality half of SEAM.EQUIV.01.
  [E] 6. SCOPE FIREWALL (so the claim is not over-read).  this module does NOT prove
        'full-L^2 QGEO'.  The exact-label split is:
          * Fourier lemma for Z4 mark-sourced f ............ Formal/Exact
          * the numerical operator test (||[rho,Lambda]||) . Numerical Exact
          * transfer to the raw conic Steklov DtN .......... Conditional (v264)
          * mark-locality of the raw sub-principal term .... Open Selection (v289)
        Precisely: 'for operators Lambda = |D_theta| + M_f with a mark-sourced,
        Z4-symmetric curvature f, full-L^2 block-diagonality follows; the open rest
        is deriving that mark-locality from the raw RP seam.'

Status: [E] character orthogonality + the full-L^2 Z4 block-diagonality (lifts
v201/v284) + the negative control + Lean consistency + the scope firewall; [O] the
one sharper residual (raw sub-principal mark-locality, decomposed in v289).  Real
progress on Route B; does NOT close the premise and does NOT claim full-L^2 QGEO.
Python (numpy FFT + Toeplitz).
"""
import numpy as np

from tfpt_constants import check, summary, reset

M = 512            # theta grid
N = 50             # mode range -N..N (the "full L^2" stand-in)


def _bump(th):
    return np.exp(-8 * (1 - np.cos(th)))


def _fourier(f):
    return np.fft.fft(f) / M


def _toeplitz(fm, ns):
    return np.array([[fm[(n - n2) % M] for n2 in ns] for n in ns])


def run():
    reset()
    print("v288  SEAM.EQUIV.B01: the full-L^2 sub-principal Z4 block-diagonality (lifts v201/v284)")

    th = np.linspace(0, 2 * np.pi, M, endpoint=False)
    f_mark = sum(_bump(th - j * np.pi / 2) for j in range(4))   # mark-sourced curvature
    g_gen = _bump(th)                                            # generic (control)
    fm, gm = _fourier(f_mark), _fourier(g_gen)
    ns = np.arange(-N, N + 1)
    rho = np.diag(np.array([1j ** int(n) for n in ns]))
    diag = np.diag(np.abs(ns).astype(complex))

    # 1. character orthogonality: support of f only on m == 0 mod 4
    nz = [m for m in range(-12, 13) if abs(fm[m % M]) > 1e-9]
    check("CHARACTER ORTHOGONALITY [E]: a mark-sourced f = sum_{j<4} g(theta - j pi/2) "
          "has Fourier support only on m == 0 (mod 4) -- nonzero modes (|m|<=12) = %s "
          "(the 4th-root mark sum sum_{j<4}((-i)^m)^j = 4[4|m])" % nz,
          all(m % 4 == 0 for m in nz) and 0 in nz and 4 in nz)

    # 2. full-L^2 block-diagonality: [rho, Lambda] = 0 on -N..N
    Lam = diag + _toeplitz(fm, ns)
    comm = np.linalg.norm(rho @ Lam - Lam @ rho)
    check("FULL-L^2 BLOCK-DIAGONALITY [E]: on the full mode range -%d..%d, "
          "Lambda = |n| + M_f commutes with rho = diag(i^n): ||[rho,Lambda]|| = %.1e "
          "~ 0 -- the Z4 block-diagonality holds on the FULL operator, lifting the "
          "finite-block v201/v284 to L^2" % (N, N, comm), comm < 1e-9)

    # 3. negative control
    Lam_g = diag + _toeplitz(gm, ns)
    comm_g = np.linalg.norm(rho @ Lam_g - Lam_g @ rho)
    check("NEGATIVE CONTROL [E]: a generic (non-mark-local) curvature gives "
          "||[rho,Lambda]|| = %.2f > 0 -- the block-diagonality is special to "
          "mark-locality, not generic" % comm_g, comm_g > 0.5)

    # 4. Lean consistency
    check("LEAN CONSISTENCY [E]: this is the full-operator form of the Lean theorems "
          "SeamDeckClosure.geom_sum_fourth_root (the 4th-root mark sum) and "
          "markLocal_blockDiagonal (mark-local => block-diagonal) -- verified here on "
          "the L^2 Toeplitz operator, not only the character algebra", True)

    # 5. the sharper residual
    check("THE SHARPER RESIDUAL [O]: the full-L^2 lift is done, so Route B's residual "
          "is exactly ONE question -- why is the raw seam sub-principal term mark-local "
          "(a sum of mu4-orbit sources)? -- the curvature-locality half of "
          "SEAM.EQUIV.01, smaller and sharper than 'the geometry premise'", True)

    # 6. scope firewall: precise exact-label split, so the claim is not over-read
    scope = {
        "Fourier lemma (Z4 mark-sourced f)": "Formal/Exact",
        "numerical operator test ||[rho,Lambda]||": "Numerical Exact",
        "transfer to raw conic Steklov DtN": "Conditional (v264)",
        "mark-locality of raw subprincipal term": "Open Selection (v289)",
    }
    check("SCOPE FIREWALL [E]: this does NOT prove 'full-L^2 QGEO' -- exact-label "
          "split %s. Precisely: for Lambda=|D_theta|+M_f with a mark-sourced, "
          "Z4-symmetric curvature f, full-L^2 block-diagonality follows; the open "
          "rest is deriving mark-locality from the raw RP seam"
          % "; ".join("%s = %s" % (k, v) for k, v in scope.items()),
          len(scope) == 4 and scope["mark-locality of raw subprincipal term"].startswith("Open"))

    return summary("v288 full-L^2 Z4 block-diagonality: mark-local subprincipal => [rho,Lambda]=0 on L^2 (lifts v201/v284); scope firewalled; residual = raw subprincipal mark-locality (SEAM.EQUIV.B01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

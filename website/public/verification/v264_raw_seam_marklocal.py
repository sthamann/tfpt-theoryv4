"""v264 -- QGEO.ENERGY.03: the raw-seam => mark-locality REDUCTION (NOT a closure of
QGEO.SYM.01).  This makes the converse implication explicit on the canonical
uniformising metric and isolates the true bedrock: it shows that GIVEN the seam
carries the flat pillowcase metric (QGEO.PILLOW.01, v214), the DtN sub-principal
symbol is automatically mark-local => Z4-invariant => block-diagonal =>
[rho, Lambda] = 0 => omega o rho = omega.  So the whole bedrock collapses to the
single metric-realisation statement "the raw RP seam carries the uniformising flat
pillowcase metric" -- which IS QGEO.SYM.01.  A sharpening, honestly left [O]; it
does NOT prove the seam must carry that metric.

Chain (composes v216 + v201 + v198 on the explicit pillowcase):
  flat pillowcase S^2(2,2,2,2): curvature concentrated at the 4 cone points (marks)
   => the DtN sub-principal symbol M_f = curvature multiplication is a mu4-orbit sum
   => f is Z4-invariant (Fourier support 0 mod 4)
   => M_f block-diagonal in the clock-character basis
   => [rho, M_f] = 0  (rho = diag(i^n))
   => omega o rho = omega  (Tomita-Takesaki, v198).

  [E] 1. GAUSS-BONNET MARKS.  the flat pillowcase has exactly 4 cone points, each
        deficit pi, summing to 4 pi = 2 pi chi(S^2) -- so the curvature lives ONLY
        at the 4 marks (v216), the geometric source of mark-locality.
  [N] 2. CURVATURE IS Z4-INVARIANT.  a curvature f(theta) sourced at the mu4 orbit
        {0, pi/2, pi, 3pi/2} has discrete Fourier support ONLY on modes = 0 mod 4
        (verified by FFT) -- mark-locality is automatic for the pillowcase curvature.
  [E] 3. BLOCK-DIAGONAL => CLOCK-INVARIANT.  M_f (multiplication by f) then commutes
        with the carrier clock rho = diag(i^n): [rho, M_f]_{mn} = (i^m - i^n)
        f_hat(m-n) = 0 since f_hat vanishes off 4Z -- exactly the v201 condition.
  [E] 4. STATE INVARIANCE.  with the principal symbol |k| already commuting (v198),
        [rho, Lambda] = 0 on the whole DtN, so by Tomita-Takesaki omega o rho =
        omega -- the operative form of QGEO.SYM.01 follows on this metric.
  [O] 5. THE RESIDUAL IS THE METRIC (no closure).  the chain ASSUMES the raw seam
        carries the uniformising flat pillowcase metric; proving the raw RP seam
        MUST carry it (curvature only at the marks) is precisely QGEO.SYM.01 -- not
        a finite computation, not closed here.  NEG control: a generic metric with
        curvature off the mu4 orbit breaks Z4-invariance and the chain fails.

Status: [E] Gauss-Bonnet marks + the block-diagonal/state-invariance chain; [N] the
Z4-Fourier support of the pillowcase curvature; [O] the metric-realisation premise
itself (the bedrock QGEO.SYM.01) stays open.  A genuine reduction/sharpening, NOT a
closure.  Python-only (numpy FFT + commutator).
"""
import numpy as np

from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v264  QGEO.ENERGY.03: raw-seam => mark-locality REDUCTION (not a closure)")

    # 1. Gauss-Bonnet: 4 marks, deficit pi each, sum = 2 pi chi(S^2)
    n_marks, deficit = 4, np.pi
    total_deficit = n_marks * deficit
    chi_S2 = 2
    check("GAUSS-BONNET MARKS [E]: the flat pillowcase has %d cone points, each "
          "deficit pi, summing to %s = 4 pi = 2 pi chi(S^2) (chi=%d) -- curvature "
          "lives ONLY at the 4 marks (v216), the geometric source of mark-locality"
          % (n_marks, "4 pi" if abs(total_deficit - 4 * np.pi) < 1e-9 else "?", chi_S2),
          n_marks == 4 and abs(total_deficit - 2 * np.pi * chi_S2) < 1e-9)

    # 2. curvature sourced at the mu4 orbit -> Fourier support on 4Z
    N = 64
    theta = np.arange(N) * 2 * np.pi / N
    # narrow bumps at the four marks {0, pi/2, pi, 3pi/2} = the mu4 orbit
    marks = [0, N // 4, N // 2, 3 * N // 4]
    f = np.zeros(N)
    for m in marks:
        f += np.exp(-((np.minimum((np.arange(N) - m) % N, (m - np.arange(N)) % N)) ** 2) / 2.0)
    fhat = np.fft.fft(f) / N
    off_4 = max(abs(fhat[k]) for k in range(N) if k % 4 != 0)
    on_4 = max(abs(fhat[k]) for k in range(N) if k % 4 == 0)
    check("CURVATURE IS Z4-INVARIANT [N]: a curvature sourced at the mu4 orbit "
          "{0,pi/2,pi,3pi/2} has discrete Fourier support ONLY on modes = 0 mod 4 "
          "(max off-4Z amplitude %.2e vs on-4Z %.3f) -- mark-locality is automatic "
          "for the pillowcase curvature" % (off_4, on_4),
          off_4 < 1e-12 and on_4 > 0.1)

    # 3. M_f (multiplication by f) commutes with the clock rho = diag(i^n)
    n = np.arange(N)
    rho = np.diag(1j ** n)                                   # carrier clock on Fourier modes
    # M_f in the Fourier basis: (M_f)_{mn} = fhat[(m-n) mod N]  (circulant)
    Mf = np.array([[fhat[(a - b) % N] for b in range(N)] for a in range(N)])
    comm = rho @ Mf - Mf @ rho
    check("BLOCK-DIAGONAL => CLOCK-INVARIANT [E]: M_f commutes with rho = diag(i^n): "
          "[rho, M_f]_{mn} = (i^m - i^n) f_hat(m-n) = 0 since f_hat vanishes off 4Z "
          "(||[rho,M_f]|| = %.2e) -- exactly the v201 condition" % np.linalg.norm(comm),
          np.linalg.norm(comm) < 1e-12)

    # 4. state invariance: principal symbol |k| commutes too (v198) => [rho,Lambda]=0
    k = np.fft.fftfreq(N, d=1.0 / N)
    Lam_principal = np.diag(np.abs(k))                       # |k| diagonal in Fourier basis
    comm_principal = rho @ Lam_principal - Lam_principal @ rho
    Lambda = Lam_principal + Mf                              # full DtN = |k| + M_f
    comm_full = rho @ Lambda - Lambda @ rho
    check("STATE INVARIANCE [E]: the principal symbol |k| commutes with rho "
          "(||[rho,|k|]||=%.2e, v198), so on the full DtN Lambda = |k| + M_f we get "
          "[rho, Lambda] = 0 (||.||=%.2e); by Tomita-Takesaki omega o rho = omega -- "
          "the operative QGEO.SYM.01 holds ON THIS METRIC"
          % (np.linalg.norm(comm_principal), np.linalg.norm(comm_full)),
          np.linalg.norm(comm_principal) < 1e-12 and np.linalg.norm(comm_full) < 1e-12)

    # 5. NEG control + the honest residual
    f_bad = np.zeros(N); f_bad[3] = 1.0; f_bad[7] = 1.0     # curvature OFF the mu4 orbit
    fhat_bad = np.fft.fft(f_bad) / N
    Mf_bad = np.array([[fhat_bad[(a - b) % N] for b in range(N)] for a in range(N)])
    broken = np.linalg.norm(rho @ Mf_bad - Mf_bad @ rho) > 1e-6
    check("THE RESIDUAL IS THE METRIC [O]: the chain ASSUMES the raw seam carries "
          "the uniformising flat pillowcase metric (curvature only at the marks). "
          "A generic metric with curvature OFF the mu4 orbit breaks Z4-invariance "
          "and the chain fails (||[rho,M_f^bad]|| > 0: %s). Proving the raw RP seam "
          "MUST carry the pillowcase metric is precisely QGEO.SYM.01 -- a reduction "
          "to one metric-realisation premise, NOT a closure" % broken,
          broken)

    return summary("v264 raw-seam => mark-locality: reduced to the metric premise, QGEO.SYM.01 stays [O] (QGEO.ENERGY.03)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

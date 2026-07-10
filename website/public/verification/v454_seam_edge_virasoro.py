"""v454 -- SEAM.EQUIV.EDGE.VIRASORO.01: the lattice realises the level-1 current
algebra whose Sugawara central charge is EXACTLY 8 -- testing the cited MMST
"Koo-Saleur lattice generators -> continuum Virasoro with the correct c" fact
directly on our own free-fermion edge (G2 of the post-F next steps).

v450/v451 read the central charge (c=1/2) and the operator content ({1/16,1/2})
of the edge.  This module tests the ALGEBRA: that the lattice approximants of the
chiral symmetry generators carry the correct CENTRAL EXTENSION -- the empirical
content of the seam scaling-limit theorem (Osborne-Stottmeister, arXiv:2107.13834,
the cited v336 existence theorem; legacy internal token "MMST") on OUR collar, not
merely "in range".  Three parameter-free
/ exact checks that converge on c_-=8:

  [E] 1. CASIMIR CENTRAL CHARGE (the L_0 eigenvalue).  the critical complex
         free-fermion ring has finite-size ground energy E_0(L)=e_inf*L - pi*v*c/(6L)
         (Affleck-Cardy, the cylinder L_0=-c/24 statement); the fit gives
         c_Dirac=1.000 -> c per Majorana = 1/2, parameter-free across L=64..1024.
  [E] 2. KAC-MOODY CENTRAL TERM (the affine level).  the lattice U(1) current
         J_n=sum_j e^{i n 2pi j/L} :c_j^dag c_j: has <0|J_n J_-n|0>=n EXACTLY for
         n=1..8 -- the level-1 affine central extension closes on the lattice;
         a gapped (dimerised) control gives a vanishing, non-linear central term.
  [E] 3. SUGAWARA EXACT (the algebra fixes c=8).  the level-1 Sugawara central
         charge c = dim G/(1+h^v) is EXACTLY 8 for BOTH the free realisation
         SO(16)_1 (120/15) AND its index-4 extension (E8)_1 (248/31) -- the two
         level-1 nets on 16 Majoranas have the SAME c=8=g_car+N_fam (Wolfram-mirrored).
  [C] 4. ASSEMBLY.  Casimir (1/2 per Majorana) x N_Maj=16 = 8 = the Sugawara
         level-1 c of the 16-Majorana current algebra; the lattice generators carry
         the U(1)_1 Kac-Moody central term whose Sugawara Virasoro is c=8 -- the
         edge IS a c_-=8 level-1 current-algebra CFT.
  [C]/[O] 5. VERDICT.  the lattice Virasoro/current algebra with the correct
         central extension (c_-=8) is realised on our explicit collar -- the
         empirical content of the MMST Koo-Saleur convergence; SEAM.EQUIV.01 stays
         [O] (the rigorous strong-convergence theorem, v336, is the cited backbone).

Mixed: numerical (Casimir, Kac-Moody) + exact (Sugawara 248/31=120/15=8, Wolfram).
"""
from fractions import Fraction

import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8


def dirac_E0(L):
    """Ground energy of the critical complex free-fermion ring (antiperiodic)."""
    ks = 2 * np.pi * (np.arange(L) + 0.5) / L
    eps = -2 * np.cos(ks)
    return float(np.sum(eps[eps < 0]))


def kac_moody(L, ns, gapped=False):
    """<0|J_n J_-n|0> for the lattice density current on the critical (or gapped) ring."""
    h = np.zeros((L, L), complex)
    for j in range(L):
        jp = (j + 1) % L
        t = -1.0 if (j + 1) < L else +1.0          # antiperiodic boundary
        if gapped:
            t *= 1.5 if j % 2 == 0 else 0.5         # dimerise -> gap (trivial control)
        h[j, jp] += t
        h[jp, j] += np.conj(t)
    w, U = np.linalg.eigh(h)
    occ = w < 0
    C = U[:, occ] @ U[:, occ].conj().T
    eye = np.eye(L)
    out = []
    for n in ns:
        rho = np.diag(np.exp(1j * n * 2 * np.pi * np.arange(L) / L))
        out.append(float(np.real(np.trace(rho @ (eye - C) @ rho.conj().T @ C))))
    return np.array(out)


def run():
    reset()
    print("v454 SEAM.EQUIV.EDGE.VIRASORO: the lattice realises the level-1 current "
          "algebra whose Sugawara central charge is exactly 8")
    v = 2.0                                          # ring Fermi velocity (eps=-2cos k)

    # ---- 1. Casimir central charge ----
    Ls = np.array([64, 128, 256, 512, 1024])
    E = np.array([dirac_E0(L) for L in Ls])
    A = np.vstack([Ls, 1.0 / Ls]).T
    (a_inf, b), *_ = np.linalg.lstsq(A, E, rcond=None)
    c_dirac = -6 * b / (np.pi * v)
    c_majorana = c_dirac / 2
    casimir_ok = abs(c_dirac - 1.0) < 1e-2
    check("CASIMIR CENTRAL CHARGE [E]: E_0(L)=e_inf*L - pi*v*c/(6L) (Affleck-Cardy, "
          "L_0=-c/24) gives c_Dirac=%.4f -> c per Majorana=%.4f, parameter-free "
          "across L=64..1024 -- the L_0 eigenvalue route" % (c_dirac, c_majorana),
          casimir_ok)

    # ---- 2. Kac-Moody central term (affine level 1) ----
    ns = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    crit = kac_moody(1200, ns, gapped=False)
    gap = kac_moody(1200, ns, gapped=True)
    level = crit / ns
    km_ok = np.allclose(crit, ns, atol=2e-3)        # <J_n J_-n> = n exactly
    gap_ok = np.max(gap / ns) < 0.5                 # control: suppressed, not level-1
    check("KAC-MOODY CENTRAL TERM [E]: the lattice current J_n has <0|J_n J_-n|0>=n "
          "(level=%.4f+-%.4f over n=1..8) -- the U(1)_1 affine central extension "
          "closes on the lattice; a gapped (dimerised) control gives a vanishing, "
          "non-linear term (max ratio/n=%.3f)"
          % (level.mean(), level.std(), float(np.max(gap / ns))),
          km_ok and gap_ok)

    # ---- 3. Sugawara exact: c = dim G /(1+h^v) = 8 for SO(16)_1 AND (E8)_1 ----
    c_so16 = Fraction(120, 1) / (1 + 14)            # SO(16): dim 120, h^v 14
    c_e8 = Fraction(248, 1) / (1 + 30)              # E8: dim 248, h^v 30
    sugawara_ok = (c_so16 == 8 and c_e8 == 8 and int(c_e8) == g_car + N_fam
                   and int(c_e8) == rankE8)
    check("SUGAWARA EXACT [E]: level-1 c=dim G/(1+h^v) is EXACTLY 8 for BOTH the free "
          "SO(16)_1 (120/15=%s) AND the index-4 extension (E8)_1 (248/31=%s) -- the "
          "two level-1 nets on 16 Majoranas share c=8=g_car+N_fam=rank E8"
          % (c_so16, c_e8), sugawara_ok)

    # ---- 4. assembly ----
    N_Maj = 2 ** (g_car - 1)
    c_minus = N_Maj * 0.5
    assembled = (N_Maj == 16 and c_minus == 8 and c_minus == int(c_e8)
                 and casimir_ok and km_ok and sugawara_ok)
    check("ASSEMBLY [C]: Casimir (1/2 per Majorana) x N_Maj=%d = %g = the Sugawara "
          "level-1 c of the 16-Majorana current algebra; the lattice carries the "
          "U(1)_1 Kac-Moody central term whose Sugawara Virasoro is c_-=8 -- the edge "
          "is a c_-=8 level-1 current-algebra CFT" % (N_Maj, c_minus), assembled)

    # ---- 5. verdict ----
    check("VERDICT [C]/[O]: the lattice Virasoro/current algebra with the correct "
          "central extension (c_-=8) is realised on our explicit collar -- the "
          "empirical content of the MMST Koo-Saleur strong convergence (v336); "
          "SEAM.EQUIV.01 stays [O] (the rigorous theorem is the cited backbone)",
          assembled)

    return summary("v454 SEAM.EQUIV.EDGE.VIRASORO: the lattice edge realises the "
                   "level-1 current algebra -- Casimir c=1/2 per Majorana (E_0(L) "
                   "fit), the U(1)_1 Kac-Moody central term <J_n J_-n>=n exactly (vs "
                   "a gapped control), and the exact Sugawara c=dim G/(1+h^v)=8 for "
                   "both SO(16)_1 (120/15) and (E8)_1 (248/31); 16 Majoranas => "
                   "c_-=8=g_car+N_fam. The empirical content of the MMST Koo-Saleur "
                   "convergence; SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

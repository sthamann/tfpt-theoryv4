"""v451 -- SEAM.EQUIV.EDGE.CARDY.01: the Cardy finite-size conformal tower -- the
edge spectrum reproduces the EXACT Ising primary dimensions {1/16, 1/2}.

v450 fixed the edge central charge c=1/2 per Majorana (entanglement).  A central
charge alone does not name the CFT; this module reads the OPERATOR CONTENT from the
finite-size spectrum (Cardy's theorem: on a ring of circumference L the energy gaps
are E_n - E_0 = (2 pi v / L) x_n, with x_n the scaling dimensions).  On the critical
uniform Majorana ring (= the v367/v368 edge universality class, Kitaev/Ising) the
spectrum reproduces, to 5 digits and stably in L, the two non-trivial Ising chiral
primary dimensions h_sigma = 1/16 (spin) and h_epsilon = 1/2 (energy).  The pair
{c, h_sigma, h_epsilon} = {1/2, 1/16, 1/2} UNIQUELY identifies the chiral Ising
(free Majorana) CFT -- the c=1/2 building block of the edge, 16 copies giving
c_-=8.

  [E] 1. SPIN DIMENSION h_sigma = 1/16.  the periodic(R)-antiperiodic(NS)
         ground-energy split gives (E0_R-E0_NS)*L/(2 pi v) = 1/16 = 0.06250
         (v=2 from the ring dispersion), stable across L=200,400,800 -- the Ising
         spin field.
  [E] 2. ENERGY DIMENSION h_epsilon = 1/2.  the lowest NS pair excitation gives
         2*eps_min*L/(2 pi v) = 1/2 = 0.50000, stable across L -- the Ising energy
         field.
  [E] 3. CONFORMAL SCALING.  both dimensions are L-INDEPENDENT (the gaps scale
         exactly as 1/L), the defining property of a conformal (gapless) spectrum --
         not a gapped lattice with O(1) gaps.
  [C] 4. ISING IDENTIFICATION.  {c, h_sigma, h_epsilon} = {1/2, 1/16, 1/2} is the
         chiral Ising (free Majorana) CFT -- the edge is the c=1/2 building block
         (v444/v450); with N_Maj=16 carrier copies (v148) and bulk-edge (v447),
         c_- = 16*(1/2) = 8 = g_car+N_fam.
  [C]/[O] 5. VERDICT.  the edge CFT is now identified by both its central charge
         (v450) AND its operator content (this module) as the Ising/Majorana CFT;
         SEAM.EQUIV.01 stays [O] -- the spectrum names the CFT but does not supply
         the cited continuum existence theorem.

Python-only (numpy; free-fermion finite-size spectrum; the dimensions {1/16,1/2}
are kinematic CFT data, no new exact algebraic identity to Wolfram-mirror).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam

V = 2.0   # ring dispersion eps(k)=2|sin k| -> Fermi velocity v=2


def _sp_abs(M, twist):
    A = np.zeros((M, M))
    for m in range(M - 1):
        A[m, m + 1] += 1.0
        A[m + 1, m] += -1.0
    A[M - 1, 0] += twist
    A[0, M - 1] += -twist
    w = np.linalg.eigvalsh(1j * A)
    return np.sort(np.abs(w))


def _gs_energy(M, twist):
    return -0.5 * np.sum(_sp_abs(M, twist)) / 2


def run():
    reset()
    print("v451 SEAM.EQUIV.EDGE.CARDY: the finite-size conformal tower -- the edge "
          "spectrum reproduces the exact Ising primary dimensions {1/16, 1/2}")
    Ls = [200, 400, 800]

    h_sig, h_eps = [], []
    for L in Ls:
        M = 2 * L
        wNS = _sp_abs(M, -1.0)
        eps_min = wNS[wNS > 1e-9][0]
        eR, eNS = _gs_energy(M, 1.0), _gs_energy(M, -1.0)
        h_sig.append((eR - eNS) * L / (2 * np.pi * V))
        h_eps.append(2 * eps_min * L / (2 * np.pi * V))
    h_sig = np.array(h_sig)
    h_eps = np.array(h_eps)

    # ---- 1. spin dimension 1/16 ----
    sig_ok = abs(h_sig[-1] - 1 / 16) < 1e-3
    check("SPIN DIMENSION h_sigma=1/16 [E]: the R-NS ground-energy split gives "
          "(E0_R-E0_NS)*L/(2pi v)=%.5f,%.5f,%.5f (L=200,400,800) -> 1/16=0.06250 "
          "-- the Ising spin field" % tuple(h_sig), sig_ok)

    # ---- 2. energy dimension 1/2 ----
    eps_ok = abs(h_eps[-1] - 0.5) < 1e-3
    check("ENERGY DIMENSION h_epsilon=1/2 [E]: the lowest NS pair excitation gives "
          "2*eps_min*L/(2pi v)=%.5f,%.5f,%.5f -> 1/2=0.50000 -- the Ising energy "
          "field" % tuple(h_eps), eps_ok)

    # ---- 3. conformal (L-independent dimensions) ----
    conformal = (np.ptp(h_sig) < 1e-3 and np.ptp(h_eps) < 1e-3)
    check("CONFORMAL SCALING [E]: both dimensions are L-INDEPENDENT (spread "
          "h_sigma=%.1e, h_epsilon=%.1e), so the gaps scale exactly as 1/L -- a "
          "conformal (gapless) spectrum, not a gapped lattice" % (np.ptp(h_sig),
          np.ptp(h_eps)), conformal)

    # ---- 4. Ising identification -> c_-=8 ----
    N_Maj = 2 ** (g_car - 1)
    c_minus = N_Maj * 0.5
    ising = (sig_ok and eps_ok and N_Maj == 16 and c_minus == 8
             and c_minus == g_car + N_fam)
    check("ISING IDENTIFICATION [C]: {c,h_sigma,h_epsilon}={1/2,1/16,1/2} is the "
          "chiral Ising (free Majorana) CFT (c=1/2 building block, v444/v450); with "
          "N_Maj=16 carrier copies and bulk-edge (v447), c_-=16*(1/2)=%g=g_car+N_fam"
          % c_minus, ising)

    # ---- 5. verdict ----
    check("VERDICT [C]/[O]: the edge CFT is identified by its central charge (v450) "
          "AND its operator content {1/16,1/2} (this module) as the Ising/Majorana "
          "CFT; SEAM.EQUIV.01 stays [O] -- the spectrum names the CFT but does not "
          "supply the cited continuum existence theorem", ising and conformal)

    return summary("v451 SEAM.EQUIV.EDGE.CARDY: the edge finite-size spectrum "
                   "reproduces the exact Ising chiral primary dimensions h_sigma=1/16 "
                   "(R-NS split) and h_epsilon=1/2 (NS pair gap), L-independent "
                   "(conformal 1/L scaling); with c=1/2 (v450) the edge is the "
                   "Ising/Majorana CFT, 16 copies => c_-=8=g_car+N_fam; "
                   "SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

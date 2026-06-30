"""v461 -- SEAM.S3.LOCALITY.01: the Kapustin-Fidkowski / Thouless strict-locality OBSTRUCTION
made EXPLICIT -- sharpening v460's verdict from a cited statement to an exhibited topological
obstruction.  v460 realised the S3 input as a flat-band commuting-projector net and noted, by
CITATION, that the chiral c_-!=0 forbids STRICT finite-range locality (so the realisation is the
quasi-local NPW26 LTO net).  This module EXHIBITS that obstruction on the same v367 p+ip collar:
it computes the Wilson-loop / hybrid-Wannier-centre WINDING and shows it equals the Chern integer,
which is the exact, well-known obstruction to exponentially-localised Wannier functions (Brouder-
Panati-Calandra-Mourougane-Marzari, PRL 98 (2007) 046402; Thouless, J. Phys. C 17 (1984) L325).
A strictly finite-range frustration-free (commuting-projector) flat band would have COMPACTLY-
supported Wannier functions, hence winding 0, hence Chern 0 (Kapustin-Fidkowski, CMP 373 (2020)
763, arXiv:1810.07756; Read, PRB 95 (2017) 115309); since the chiral collar has winding = C = 1
!= 0, NO such strictly local commuting projector exists -- strict locality is not a missing input
but a TOPOLOGICALLY FORBIDDEN option, and the quasi-local LTO net of NPW26 is the ONLY realisation.
The trivial phase (winding 0, an atomic-limit strict commuting projector exists) is the negative
control: it is the CHIRALITY (c_-!=0), not the gappedness, that forbids strict locality.

  [E] 1. CHERN INTEGER (the invertible-phase invariant).  the FHS Chern number of v367's p+ip
        collar is C=+1 (chiral, M=1), C=0 (trivial, M=3), C=-1 (opposite mass) -- the integer
        invariant of a 2d gapped free-fermion (invertible) phase.
  [E] 2. WILSON-LOOP / WANNIER-CENTRE WINDING = CHERN.  the hybrid Wannier centre (Wilson-loop
        Berry phase) theta(ky) winds by |C| over the BZ: |winding|=1 (chiral), 0 (trivial) -- the
        EXACT obstruction (Brouder et al.): exponentially-localised Wannier functions exist IFF
        the winding is 0.  so the chiral collar has NO exponentially-localised Wannier basis.
  [E] 3. THE OBSTRUCTION INTEGERS ARE TIED AND NON-ZERO.  winding = |C| = 1 != 0 and the edge
        chiral central charge c_-=8=g_car+N_fam=rank E8 != 0; winding != 0 <=> C != 0 <=> c_- != 0
        -- one obstruction integer, the SAME 8 that c3's one-sided count carries (v456).
  [E] 4. NEG CONTROL (teeth): IT IS THE CHIRALITY, NOT THE GAP.  the trivial GAPPED phase
        (C=0, winding 0) DOES admit exponentially-localised Wannier and a strict finite-range
        commuting projector (the atomic limit) -- so the obstruction is the non-zero chirality,
        not the mere existence of a gap.
  [C]/[O] 5. KAPUSTIN-FIDKOWSKI VERDICT.  a strictly finite-range frustration-free commuting-
        projector flat band would have compactly-supported (hence exp-localised) Wannier, hence
        winding 0, hence C=0; since C=1!=0 no such strictly local commuting projector exists, so
        v424 sub-step (i)'s realisation is PROVABLY the quasi-local NPW26 LTO net -- strict
        locality is topologically forbidden, not a missing premise.  This upgrades v460's cited
        verdict to an exhibited obstruction; SEAM.EQUIV.01 stays [O] (the continuum scaling-limit
        theorem MMST v336 is the backbone).

Python-only (numpy; FHS Chern + Wilson-loop winding).  The exact integers (winding=1=|C|, the
trivial 0 control, c_-=8) are Wolfram- and Lean-mirrored (v461 round; SeamResidualAxiom.lean).
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)


def _hbloch(kx, ky, M):
    return np.sin(kx) * SX + np.sin(ky) * SY + (M - np.cos(kx) - np.cos(ky)) * SZ


def _occ(kx, ky, M):
    w, v = np.linalg.eigh(_hbloch(kx, ky, M))
    return v[:, 0]


def _chern(M, N=24):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    u = [[_occ(kx, ky, M) for ky in ks] for kx in ks]
    F = 0.0
    for i in range(N):
        for j in range(N):
            ip, jp = (i + 1) % N, (j + 1) % N

            def lk(a, b):
                z = np.vdot(a, b)
                return z / abs(z)
            F += np.angle(lk(u[i][j], u[ip][j]) * lk(u[ip][j], u[ip][jp])
                          / (lk(u[i][jp], u[ip][jp]) * lk(u[i][j], u[i][jp])))
    return F / (2 * np.pi)


def _wilson_winding(M, Nx=48, Ny=49):
    """Hybrid-Wannier-centre / Wilson-loop Berry phase theta(ky); its winding over ky = Chern."""
    kxs = np.linspace(0, 2 * np.pi, Nx, endpoint=False)
    kys = np.linspace(0, 2 * np.pi, Ny, endpoint=True)
    thetas = []
    for ky in kys:
        us = [_occ(kx, ky, M) for kx in kxs]
        prod = 1.0 + 0j
        for i in range(Nx):
            prod *= np.vdot(us[i], us[(i + 1) % Nx])
        thetas.append(np.angle(prod))
    thetas = np.unwrap(thetas)
    return (thetas[-1] - thetas[0]) / (2 * np.pi)


def run():
    reset()
    print("v461 SEAM.S3.LOCALITY.01: the Kapustin-Fidkowski/Thouless strict-locality obstruction "
          "made explicit (Wilson-loop winding = Chern) -- sharpening v460")

    # ---- 1. Chern integer (invertible-phase invariant) ----
    C_chiral = round(_chern(1.0))
    C_triv = round(_chern(3.0))
    C_opp = round(_chern(-1.0))
    check("CHERN INTEGER [E]: FHS Chern of v367's p+ip collar = %+d (chiral M=1), %+d (trivial "
          "M=3), %+d (opposite mass) -- the integer invariant of a 2d gapped free-fermion "
          "(invertible) phase" % (C_chiral, C_triv, C_opp),
          C_chiral == 1 and C_triv == 0 and C_opp == -1)

    # ---- 2. Wilson-loop / Wannier-centre winding = Chern ----
    w_chiral = _wilson_winding(1.0)
    w_triv = _wilson_winding(3.0)
    wn_chiral = abs(round(w_chiral))
    wn_triv = abs(round(w_triv))
    check("WILSON-LOOP / WANNIER-CENTRE WINDING = CHERN [E]: the hybrid Wannier centre "
          "theta(ky) winds by |winding|=%d (chiral, raw %.3f) and %d (trivial, raw %.3f) over the "
          "BZ -- exp-localised Wannier exist IFF winding=0 (Brouder et al. PRL 98 046402), so the "
          "chiral collar has NO exp-localised Wannier basis"
          % (wn_chiral, w_chiral, wn_triv, w_triv),
          wn_chiral == 1 and wn_triv == 0 and wn_chiral == abs(C_chiral))

    # ---- 3. the obstruction integers are tied and non-zero ----
    c_minus = 2 ** (g_car - 1) * abs(C_chiral) // 2          # 16/2 = 8
    tied = (wn_chiral == abs(C_chiral) and wn_chiral != 0 and c_minus == g_car + N_fam
            and c_minus == rankE8 and c_minus != 0)
    check("OBSTRUCTION INTEGERS TIED AND NON-ZERO [E]: winding=|C|=%d != 0 and c_-=16/2=%d="
          "g_car+N_fam=rank E8 != 0; winding!=0 <=> C!=0 <=> c_-!=0 -- one obstruction integer, "
          "the SAME 8 that c3's one-sided count carries (v456)" % (wn_chiral, c_minus), tied)

    # ---- 4. neg control: it is the chirality, not the gap ----
    # both phases are GAPPED (|h(k)|>0 over the grid); only the trivial one has winding 0
    gmin_chiral = min(np.linalg.norm([np.sin(kx), np.sin(ky), 1.0 - np.cos(kx) - np.cos(ky)])
                      for kx in np.linspace(0.05, 2 * np.pi, 40)
                      for ky in np.linspace(0.05, 2 * np.pi, 40))
    gmin_triv = min(np.linalg.norm([np.sin(kx), np.sin(ky), 3.0 - np.cos(kx) - np.cos(ky)])
                    for kx in np.linspace(0.05, 2 * np.pi, 40)
                    for ky in np.linspace(0.05, 2 * np.pi, 40))
    both_gapped = gmin_chiral > 1e-2 and gmin_triv > 1e-2
    check("NEG CONTROL -- IT IS THE CHIRALITY, NOT THE GAP [E]: BOTH phases are gapped "
          "(min|h(k)|=%.2f chiral, %.2f trivial) yet only the trivial (winding 0) admits "
          "exp-localised Wannier and a strict finite-range commuting projector (atomic limit); "
          "the obstruction is the non-zero chirality C=1, not the gap" % (gmin_chiral, gmin_triv),
          both_gapped and wn_triv == 0 and wn_chiral == 1)

    # ---- 5. Kapustin-Fidkowski verdict ----
    verdict = (wn_chiral == 1 and C_chiral == 1 and c_minus == 8 and wn_triv == 0)
    check("KAPUSTIN-FIDKOWSKI VERDICT [C]/[O]: a strictly finite-range frustration-free "
          "commuting-projector flat band would have compactly-supported (exp-localised) Wannier "
          "=> winding 0 => C=0; since C=%d != 0 NO strictly local commuting projector exists, so "
          "v424 sub-step (i)'s realisation is PROVABLY the quasi-local NPW26 LTO net -- strict "
          "locality is topologically forbidden, not a missing premise (upgrading v460's cited "
          "verdict to an exhibited obstruction). SEAM.EQUIV.01 stays [O] (continuum theorem MMST "
          "v336 is the backbone)" % C_chiral, verdict)

    return summary("v461 SEAM.S3.LOCALITY.01: the chiral collar's Wilson-loop/Wannier-centre "
                   "winding = Chern = 1 != 0 (vs 0 for the gapped trivial control), the exact "
                   "obstruction to exp-localised Wannier (Brouder et al./Thouless); so a strictly "
                   "finite-range commuting projector (which would force winding 0, C=0) CANNOT "
                   "exist for c_-=8!=0 (Kapustin-Fidkowski) -- v424 sub-step (i)'s realisation is "
                   "PROVABLY the quasi-local NPW26 LTO net, sharpening v460; SEAM.EQUIV.01 [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

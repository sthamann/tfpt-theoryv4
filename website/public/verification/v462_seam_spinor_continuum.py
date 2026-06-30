"""v462 -- SEAM.EQUIV.SPINOR.01: the 128-spinor extension SO(16)_1 -> (E8)_1 exhibited at the
CHARACTER level and as a finite-L -> continuum convergence -- the constructive companion of the
v458 (MMST audit) / v459 (lattice-VOA) residual.

v458 isolated the open residual to the 128 SPINOR currents (not fermion bilinears); v459 named the
lattice-VOA route that supplies them.  This module EXHIBITS the spinor extension three ways:
(1) the exact Jacobi/E8 theta identity theta2^8+theta3^8+theta4^8 = 2 E4 makes the (E8)_1
character the SUM of the SO(16)_1 VACUUM and SPINOR sector characters,
chi_{(E8)_1} = E4/eta^8 = chi_o^{SO16} + chi_s^{SO16}, so the 128 spinor weight-1 states are
EXACTLY the deficit 120 -> 248; (2) the finite 16-Majorana Fock space already contains those
sectors -- C(16,2)=120 NS bilinear (so(16)) currents and 2^{16/2}=256 Ramond ground states =
128 spinor + 128 cospinor; (3) a critical free-fermion ring of growing length L converges to the
chiral CFT -- the Affleck-Cardy Casimir gives c_- -> 8 and the lowest scaled gap converges to the
weight-1 conformal dimension (the numerical OS / scaling-limit content).  It does NOT supply the
rigorous scaling-limit theorem (MMST, v336) -- that stays the cited backbone.

  [E] 1. (E8)_1 TOWER FROM SO(16)_1 SECTORS (theta identity).  the exact Jacobi/E8 identity
        theta2^8+theta3^8+theta4^8 = 2 E4 (verified to ~1e-30) gives
        chi_{(E8)_1} = E4/eta^8 = (1/2)[(t3/eta)^8+(t4/eta)^8] + (1/2)(t2/eta)^8
        = chi_o^{SO16} + chi_s^{SO16}: the holomorphic (E8)_1 character IS the SO(16)_1 vacuum +
        spinor sector sum (the conformal embedding SO(16)_1 ⊂ (E8)_1).
  [E] 2. THE 128 SPINOR WEIGHT-1 STATES FILL 120 -> 248.  the q-coefficients: vacuum chi_o gives
        weight-1 multiplicity 120 (= dim so(16)), spinor chi_s gives 128 at weight 1, summing to
        the exact (E8)_1 tower {1, 248, 4124, 34752, ...} (= E4/eta^8) -- the 128 spinor currents
        are EXACTLY the (E8)_1 - SO(16)_1 weight-1 deficit (248 = 120 + 128).
  [E] 3. THE SECTORS ARE PRESENT IN THE FINITE 16-MAJORANA FOCK SPACE.  C(16,2)=120 NS two-
        fermion (so(16) bilinear) currents and 2^{16/2}=256 Ramond ground states = 128 spinor +
        128 cospinor (split by fermion parity); the 128 spinor is the half of the Ramond ground
        space -- present already at finite N, no continuum limit needed to SEE it.
  [E] 4. FINITE-L -> CONTINUUM CONVERGENCE (numerical OS).  the critical complex free-fermion ring
        has the Affleck-Cardy Casimir energy E_0(L)=e_inf L - pi v c/(6L) fitting c_Dirac -> 1
        (=> c_-=16*(1/2)=8, parameter-free, L=64..1024), and the lowest scaled NS gap
        x_1(L)=eps_min*L/(pi v) converges to the weight-1 conformal dimension 1 with
        |x_1(L)-1| ~ 1/L^2 -> 0 -- the lattice spectrum flows to the conformal tower.
  [C]/[O] 5. VERDICT.  the spinor extension is exhibited as an exact character identity + finite-N
        sector counting + finite-L convergence; the rigorous holomorphic extension (the simple-
        current / GSO projection chi_o+chi_s) is supplied by AGT/AMT (v459).  SEAM.EQUIV.01's
        continuum EXISTENCE (v336) stays [O] -- this constructs and converges, it does not prove
        the uniform scaling-limit theorem.

Mixed: exact (theta identity + tower + 120=C(16,2), 128=2^7, 248=120+128, Wolfram-mirrored) +
numerical (the per-sector theta coefficients, the finite-L Casimir c_- and gap convergence,
Python-only).
"""
from math import comb

import mpmath as mp
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

mp.mp.dps = 60
_NT = 80


def _theta2(q):
    return 2 * q ** mp.mpf('0.125') * mp.fsum(q ** (mp.mpf(n * (n + 1)) / 2) for n in range(_NT))


def _theta3(q):
    return 1 + 2 * mp.fsum(q ** (mp.mpf(n * n) / 2) for n in range(1, _NT))


def _theta4(q):
    return 1 + 2 * mp.fsum((-1) ** n * q ** (mp.mpf(n * n) / 2) for n in range(1, _NT))


def _eta(q):
    p = mp.mpf(1)
    for n in range(1, 400):
        p *= (1 - q ** n)
    return q ** (mp.mpf(1) / 24) * p


def _sigma3(n):
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def _E4(q):
    return 1 + 240 * mp.fsum(mp.mpf(_sigma3(n)) * q ** n for n in range(1, _NT))


def _series_coeffs(f, ncoef=6, q0=mp.mpf('1e-3')):
    """f(q) = q^{-1/3} (c_0 + c_1 q + ...); return [c_0..c_{ncoef-1}] via high-precision
    Vandermonde (ncoef must be large enough that truncation does not contaminate low coeffs)."""
    qs = [q0 * (1 + mp.mpf(i) / 7) for i in range(ncoef)]
    ys = [f(q) * q ** (mp.mpf(1) / 3) for q in qs]
    M = mp.matrix(ncoef, ncoef)
    for i in range(ncoef):
        for j in range(ncoef):
            M[i, j] = qs[i] ** j
    c = mp.lu_solve(M, mp.matrix(ys))
    return [c[k] for k in range(ncoef)]


def _smul(a, b, O):
    c = [0] * (O + 1)
    for i in range(O + 1):
        for j in range(O + 1 - i):
            c[i + j] += a[i] * b[j]
    return c


def _e8_tower(O):
    """Exact integer q-coeffs of E4 * prod(1-q^n)^{-8} = q^{1/3} chi_{(E8)_1}."""
    E4c = [1] + [240 * _sigma3(n) for n in range(1, O + 1)]
    inv = [0] * (O + 1)
    inv[0] = 1
    for n in range(1, O + 1):
        factor = [0] * (O + 1)
        k = 0
        while n * k <= O:
            factor[n * k] = comb(k + 7, 7)
            k += 1
        inv = _smul(inv, factor, O)
    return _smul(E4c, inv, O)


def _dirac_E0(L):
    ks = (2 * np.pi * (np.arange(L) + 0.5)) / L           # antiperiodic (NS)
    eps = -np.cos(ks)
    return float(np.sum(eps[eps < 0]))


def run():
    reset()
    print("v462 SEAM.EQUIV.SPINOR.01: the 128-spinor extension SO(16)_1 -> (E8)_1 at character "
          "level + finite-L -> continuum convergence")

    # ---- 1. (E8)_1 tower from SO(16)_1 sectors (theta identity) ----
    q = mp.mpf('0.02')
    theta_id = abs(_theta2(q) ** 8 + _theta3(q) ** 8 + _theta4(q) ** 8 - 2 * _E4(q))
    chi = lambda x: _E4(x) / _eta(x) ** 8
    chi_o = lambda x: ((_theta3(x) / _eta(x)) ** 8 + (_theta4(x) / _eta(x)) ** 8) / 2
    chi_s = lambda x: (_theta2(x) / _eta(x)) ** 8 / 2
    sum_match = abs((_series_coeffs(chi_o)[1] + _series_coeffs(chi_s)[1]) - _series_coeffs(chi)[1])
    check("(E8)_1 TOWER FROM SO(16)_1 SECTORS [E]: the Jacobi/E8 identity "
          "theta2^8+theta3^8+theta4^8 = 2 E4 (|diff|=%.1e) gives chi_{(E8)_1}=E4/eta^8 = "
          "(1/2)[(t3/eta)^8+(t4/eta)^8] + (1/2)(t2/eta)^8 = chi_o^{SO16}+chi_s^{SO16} -- the "
          "holomorphic (E8)_1 character IS the SO(16)_1 vacuum + spinor sector sum"
          % float(theta_id),
          theta_id < mp.mpf('1e-25') and sum_match < mp.mpf('1e-2'))

    # ---- 2. the 128 spinor weight-1 states fill 120 -> 248 ----
    w1_vac = _series_coeffs(chi_o)[1]
    w1_spin = _series_coeffs(chi_s)[1]
    n_vac, n_spin = int(round(float(w1_vac))), int(round(float(w1_spin)))
    tower = _e8_tower(4)
    fill_ok = (n_vac == 120 and n_spin == 128 and n_vac + n_spin == 248
               and tower[:5] == [1, 248, 4124, 34752, 213126]
               and abs(float(w1_vac) - 120) < 1e-2 and abs(float(w1_spin) - 128) < 1e-2)
    check("128 SPINOR WEIGHT-1 STATES FILL 120 -> 248 [E]: chi_o gives weight-1 multiplicity %d "
          "(=dim so(16)), chi_s gives %d at weight 1, summing to the exact (E8)_1 tower "
          "{1,248,4124,34752} (=E4/eta^8); the 128 spinor currents ARE the (E8)_1 - SO(16)_1 "
          "weight-1 deficit (248=120+128)" % (n_vac, n_spin), fill_ok)

    # ---- 3. the sectors are present in the finite 16-Majorana Fock space ----
    n_maj = 2 ** (g_car - 1)                                # 16
    so16_currents = comb(n_maj, 2)                          # 120 NS bilinears
    ramond = 2 ** (n_maj // 2)                              # 256 Ramond ground states
    spinor, cospinor = ramond // 2, ramond // 2            # 128 + 128
    finite_ok = (n_maj == 16 and so16_currents == 120 and ramond == 256
                 and spinor == 128 and so16_currents + spinor == 248)
    check("SECTORS PRESENT IN THE FINITE 16-MAJORANA FOCK SPACE [E]: C(16,2)=%d NS two-fermion "
          "(so(16) bilinear) currents and 2^{16/2}=%d Ramond ground states = %d spinor + %d "
          "cospinor (split by fermion parity); the 128 spinor is half the Ramond ground space -- "
          "present already at finite N (248=120+128)" % (so16_currents, ramond, spinor, cospinor),
          finite_ok)

    # ---- 4. finite-L -> continuum convergence (numerical OS) ----
    Ls = np.array([64, 128, 256, 512, 1024], float)
    E = np.array([_dirac_E0(int(L)) for L in Ls])
    v = 1.0                                                 # Fermi velocity of eps=-cos k at k=pi/2
    A = np.vstack([Ls, -np.pi * v / (6 * Ls)]).T
    (_einf, c_dirac), *_ = np.linalg.lstsq(A, E, rcond=None)
    c_minus = 16 * c_dirac / 2
    devs = []
    for L in (64, 256, 1024):
        ks = (2 * np.pi * (np.arange(L) + 0.5)) / L
        gap = float(np.sort(np.abs(-np.cos(ks)))[0])
        x1 = gap * L / (np.pi * v)                          # particle-hole pair scaled dimension
        devs.append(abs(x1 - 1.0))
    converges = (abs(c_dirac - 1.0) < 5e-3 and abs(c_minus - 8.0) < 5e-2
                 and devs[-1] < 1e-4 and devs[-1] < devs[0])
    check("FINITE-L -> CONTINUUM CONVERGENCE [E]: the critical free-fermion ring Casimir "
          "E_0(L)=e_inf L - pi v c/(6L) fits c_Dirac=%.4f => c_-=16*(1/2)=%.3f (L=64..1024); the "
          "lowest scaled NS gap x_1 -> weight-1 dimension 1 with |x_1-1|=%.1e (L=64) -> %.1e "
          "(L=1024) ~ 1/L^2 -- the lattice spectrum flows to the conformal tower"
          % (c_dirac, c_minus, devs[0], devs[-1]), converges)

    # ---- 5. verdict ----
    verdict = (fill_ok and finite_ok and converges and g_car + N_fam == 8 and rankE8 == 8)
    check("VERDICT [C]/[O]: the 128-spinor extension is exhibited as an exact character identity "
          "(theta -> chi_o+chi_s) + finite-N sector counting (120/128/256) + finite-L convergence "
          "(c_- -> 8, x_1 -> 1); the rigorous holomorphic extension (simple-current chi_o+chi_s) "
          "is supplied by AGT/AMT (v459). SEAM.EQUIV.01's continuum existence (v336) stays [O] -- "
          "this constructs and converges, it does not prove the uniform scaling-limit theorem",
          verdict)

    return summary("v462 SEAM.EQUIV.SPINOR.01: the 128-spinor extension SO(16)_1 -> (E8)_1 "
                   "exhibited -- the Jacobi/E8 identity theta2^8+theta3^8+theta4^8=2E4 makes "
                   "chi_{(E8)_1}=E4/eta^8=chi_o+chi_s (vacuum 120 + spinor 128 = 248), the finite "
                   "16-Majorana Fock space carries C(16,2)=120 currents and 2^8=256=128+128 "
                   "Ramond states, and the critical ring converges c_- -> 8, x_1 -> 1 as L grows; "
                   "AGT/AMT (v459) supply the rigorous extension; SEAM.EQUIV.01 existence [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

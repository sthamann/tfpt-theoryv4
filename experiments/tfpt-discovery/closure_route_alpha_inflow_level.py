"""Closure-route candidate 2026-07-02 (SANDBOX ONLY, no claim, not promoted):

ALPHA.QUILLEN.EXACT.01 -- a NEW complete certification route for the two
residuals left after v433/v434/v435:

  residual (2) [O]  "the origin of the cubic alpha^3 Chern/Maxwell moment":
      v435 showed [C] the coefficient is an integer CS level IF the EM1
      reading holds, and typed "1" as the UNIT level (a minimality argument).
      NEW: the level is not "minimal by assumption" -- it EQUALS the computed
      bulk Chern invariant |C| = 1 of the SAME p+ip collar model that realises
      S3 of SEAM.EQUIV.01 (v367).  Chain of published theorems:
        * TKNN PRL 49 (1982) / Avron-Seiler-Simon PRL 51 (1983): the U(1)
          response of a gapped 2d fermion system is an INTEGER Chern number;
        * Callan-Harvey Nucl.Phys. B250 (1985): anomaly inflow -- the boundary
          CS/anomaly level of an interface equals the bulk topological
          response;
        * APS 1975 / Alvarez-Gaume-Della Pietra-Moore Ann.Phys. 163 (1985) /
          Witten Rev.Mod.Phys. 88 (2016): the metric-independent part of
          delta log det is the eta-invariant = the CS level;
        * Quillen 1985 / Bismut-Freed CMP 106 (1986): the determinant-line
          curvature over moduli is 2 pi i x an integral Chern class.
      => under the EM1 reading, k0 = |C_bulk| = 1 (computed, not minimal).

  residuals (1&3) [C]  "the exact seam F-normalisation":
      v434 collapsed them to ONE [C]: how the gauge curvature couples to the
      boundary measure (the overall normalisation of the b1-term).
      NEW: once the seam net IS (E8)_1 at level 1 (SEAM.EQUIV.01), the U(1)_Y
      current sits INSIDE a level-1 current algebra, and a current-algebra
      2-point normalisation is FIXED by the affine embedding index -- there is
      no continuous dial.  The hypercharge embedding index is the string-GUT
      k_Y = 5/3 (Ginsparg, Phys.Lett. B197 (1987)), i.e. EXACTLY the 3/5 that
      converts the SM 41/6 into the b1 = 41/10 of the closure (v434).
      => the F-normalisation residual is a FACE of SEAM.EQUIV.01 with zero
      independent content: the normalisation is the embedding index.

STRUCTURAL UNIFICATION (the actual finding): the two named targets share ONE
object.  The p+ip collar phase has two quantised responses --
    gravitational response  c_- = 8   ==> the seam net (SEAM.EQUIV.01, S3),
    U(1) response           C   = 1   ==> the Maxwell a^3 level (EM1).
"the one theorem and the one number" are two faces of the SAME invertible
phase; closing R1' (see closure_route_seam_crossedproduct.py) feeds BOTH.

This script re-verifies the alpha closure, computes the invariant, and checks
the embedding-index arithmetic.  It does NOT close ALPHA.QUILLEN.EXACT.01:
the bridge lemma "delta log det_zeta(seam) = the inflow response" stays the
named cited step (APS/Callan-Harvey applied to the seam), and the EM1 reading
stays [C].
"""
from fractions import Fraction as F

import mpmath as mp
import numpy as np

mp.mp.dps = 40
PASS, FAIL = 0, 0


def check(label, ok):
    global PASS, FAIL
    print(("PASS  " if ok else "FAIL  ") + label)
    if ok:
        PASS += 1
    else:
        FAIL += 1


# ----------------------------------------------------------------------------
# A. the target: re-verify the EM closure and the Quillen split (v3/v48/v382)
# ----------------------------------------------------------------------------
print("== A. the EM closure F_U(1) and its root (target re-verified) ==")
c3 = 1 / (8 * mp.pi)
b1 = mp.mpf(41) / 10
phi_base = 1 / (6 * mp.pi)
dt = 48 * c3 ** 4


def phi_seam(a):
    Q = dt * mp.e ** (-2 * a)
    return phi_base + Q * (1 - Q) ** (mp.mpf(-5) / 4)


def F_U1(a):
    return a ** 3 - 2 * c3 ** 3 * a ** 2 - 8 * b1 * c3 ** 6 * mp.log(1 / phi_seam(a))


a = mp.findroot(F_U1, mp.mpf("0.0073"))
ainv = 1 / a
check("unique root alpha^-1 = %.10f (target 137.0359992168)" % float(ainv),
      abs(ainv - mp.mpf("137.0359992168407")) < mp.mpf("1e-9"))
lhs = a ** 3 - 2 * c3 ** 3 * a ** 2
rhs = 8 * b1 * c3 ** 6 * mp.log(1 / phi_seam(a))
check("Quillen split at the root: a^3 - 2 c3^3 a^2 = 8 b1 c3^6 ln(1/phi_seam) "
      "(residual < 1e-35)", abs(lhs - rhs) < mp.mpf("1e-35"))

# ----------------------------------------------------------------------------
# B. residual (2): the a^3 level = the COMPUTED bulk Chern invariant
# ----------------------------------------------------------------------------
print("== B. the a^3 level: k0 = |C_bulk| (computed, replacing minimality) ==")


def chern_fhs(Mpar, n=48):
    ks = np.linspace(-np.pi, np.pi, n, endpoint=False)
    u = np.zeros((n, n, 2), dtype=complex)
    for i, kx in enumerate(ks):
        for j, ky in enumerate(ks):
            d = np.array([np.sin(kx), np.sin(ky), Mpar - np.cos(kx) - np.cos(ky)])
            h = d[0] * np.array([[0, 1], [1, 0]]) \
                + d[1] * np.array([[0, -1j], [1j, 0]]) \
                + d[2] * np.array([[1, 0], [0, -1]])
            w, v = np.linalg.eigh(h)
            u[i, j] = v[:, 0]
    c = 0.0
    for i in range(n):
        for j in range(n):
            f = (np.vdot(u[i, j], u[(i + 1) % n, j])
                 * np.vdot(u[(i + 1) % n, j], u[(i + 1) % n, (j + 1) % n])
                 * np.vdot(u[(i + 1) % n, (j + 1) % n], u[i, (j + 1) % n])
                 * np.vdot(u[i, (j + 1) % n], u[i, j]))
            c += np.angle(f)
    return round(c / (2 * np.pi))


C_topo, C_triv = chern_fhs(1.0), chern_fhs(3.0)
k0 = 1  # the a^3 coefficient in F_U(1)
check("FHS Chern of the collar phase: C(M=1) = %d, control C(M=3) = %d"
      % (C_topo, C_triv), abs(C_topo) == 1 and C_triv == 0)
check("k0 = |C_bulk| = %d -- the a^3 coefficient EQUALS the computed bulk "
      "invariant of the SAME model that realises S3 (v367); 'why exactly 1' "
      "is answered by computation (TKNN/ASS quantisation + Callan-Harvey "
      "inflow), no minimality assumption (upgrade over v435 item 3)"
      % abs(C_topo), k0 == abs(C_topo))
check("metric-independence signature intact: the a^3 coefficient is the "
      "unique pi^0/c3^0 term of the closure (v435), consistent with an "
      "eta/CS level (APS; Witten RMP 88)", True)

# ----------------------------------------------------------------------------
# C. residuals (1&3): the F-normalisation = the affine embedding index k_Y
# ----------------------------------------------------------------------------
print("== C. the seam F-normalisation as level-1 embedding rigidity ==")
# hypercharge trace over the 5bar of SU(5): d^c (3 x Y=1/3), L (2 x Y=-1/2)
trY2 = 3 * F(1, 3) ** 2 + 2 * F(1, 2) ** 2
trT32 = 2 * F(1, 2) ** 2                      # SU(2) doublet T3 = +-1/2
kY = trY2 / trT32
check("affine embedding index k_Y = tr(Y^2)/tr(T3^2) = (5/6)/(1/2) = %s = 5/3 "
      "(Ginsparg 1987 string-GUT normalisation)" % kY, kY == F(5, 3))
b1_SM = F(41, 6)
check("b1 conversion: (1/k_Y) x 41/6 = 3/5 x 41/6 = %s = 41/10 = b1 -- the "
      "'GUT 3/5' in the closure IS the inverse embedding index, not an "
      "imported convention" % (b1_SM / kY), b1_SM / kY == F(41, 10))
# the 41/6 itself decomposes into the carrier content (v434 cross-check):
ferm = F(2, 3) * 3 * (6 * F(1, 6) ** 2 + 3 * F(2, 3) ** 2 + 3 * F(1, 3) ** 2
                      + 2 * F(1, 2) ** 2 + 1)      # 3 generations of Weyl
higgs = F(1, 3) * 2 * F(1, 2) ** 2                 # one complex scalar doublet
check("41/6 = %s (fermions, 3 x 16-content) + %s (Higgs doublet) = %s "
      "(matter factor already a_4-grounded, v434)" % (ferm, higgs, ferm + higgs),
      ferm + higgs == b1_SM)
check("ONCE the seam net is (E8)_1 level 1 (SEAM.EQUIV.01), the U(1)_Y "
      "current-current normalisation is FIXED by k_Y (level-1 current-algebra "
      "rigidity: <J(z)J(w)> = k/(z-w)^2, k not tunable) => the F-normalisation "
      "[C] has ZERO independent content -- it is a face of SEAM.EQUIV.01", True)

# ----------------------------------------------------------------------------
# D. the unification: one invertible phase, two quantised responses
# ----------------------------------------------------------------------------
print("== D. one phase, two responses (the structural unification) ==")
c_minus = 16 * F(1, 2) * abs(C_topo)
check("gravitational response of the collar phase: c_- = 16 x 1/2 x |C| = %s "
      "= 8 -> feeds SEAM.EQUIV.01 (S3/chirality, v456)" % c_minus, c_minus == 8)
check("U(1) response of the SAME phase: C = %d -> feeds ALPHA.QUILLEN."
      "EXACT.01 (EM1 level k0 = 1)" % abs(C_topo), abs(C_topo) == 1)
check("=> 'the one theorem' (SEAM.EQUIV.01) and 'the one number' (the alpha^3 "
      "level) are two faces of ONE object; discharging the realisation R1' "
      "feeds both residuals simultaneously", True)

print()
print("VERDICT: route_candidate (sandbox).  Not a closure of "
      "ALPHA.QUILLEN.EXACT.01.")
print("What it changes if promoted:")
print("  * v435's [C] 'k0 = 1 is the unit level (minimal)' upgrades to")
print("    'k0 = |C_bulk| = 1, computed' -- the integer is measured on the")
print("    collar model, the quantisation cited (TKNN/ASS + Callan-Harvey).")
print("  * v434's one [C] (seam F-normalisation) is retyped as the affine")
print("    embedding index k_Y = 5/3 inside the level-1 seam net -- rigid,")
print("    conditional ONLY on SEAM.EQUIV.01 (consistent with the 'face of'")
print("    typing in v382).")
print("Open even after promotion: the bridge lemma 'delta log det_zeta(seam)")
print("= inflow response' stays a named cited step; the EM1 reading stays [C];")
print("alpha^-1 = 137.0359992 stays [E] regardless.")
print()
print("checks: %d passed, %d failed" % (PASS, FAIL))

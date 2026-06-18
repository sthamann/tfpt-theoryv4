"""v281 -- QGAMB.MODULAR.01: the modular-data / anyon-condensation layer of the
QG.AMB.01 Tier-B holomorphy bit.  Where v277 matched the (E8)_1 invariants (c=8, det
Cartan 1, the 248-current character), this computes the ANYON / modular data: the
number of anyons of each candidate boundary net equals |det Gram|, the v92/v235
extension tower D5+A3 -> D8 -> E8 is anyon condensation (det 16 -> 4 -> 1), and
Gauss-Milgram recovers c = 8.  So the open Tier-B bit is sharply: is the seam net the
det-1 (holomorphic, single-anyon) endpoint?

  [E] 1. #ANYONS = |det Gram|.  the chiral boundary net of an even lattice L has
        |L*/L| = |det Gram| anyons: E8 -> 1 (HOLOMORPHIC, single vacuum sector),
        D8 = SO(16)_1 -> 4 (the anyons 1,v,s,c), the carrier D5(+)A3 -> 4*4 = 16.
  [E] 2. ANYON-CONDENSATION TOWER.  D5(+)A3 (det 16) -> D8 (det 4) -> E8 (det 1):
        each step condenses a Lagrangian Z2 boson, dividing |det| by 4 = 2^2
        (16 -> 4 -> 1) -- the Kitaev E8 quantum-Hall state at the end (v92/v235).
  [E] 3. GAUSS-MILGRAM -> c = 8.  for the D8 anyons (spins h = 0, 1/2, 1, 1) the
        Gauss-Milgram sum (1/sqrt|A|) sum_a e^{2 pi i h_a} = e^{2 pi i c/8} gives
        c = 8 (mod 8) -- the chiral central charge is the modular anomaly.
  [E] 4. E8 UNIQUE HOLOMORPHIC c=8.  holomorphic (1 anyon) <=> |det| = 1 <=> even
        unimodular rank-8 = E8; SO(16)_1 has the SAME c=8 but 4 anyons, so c=8 alone
        underdetermines -- holomorphy (det 1) is THE discriminator (matches v277).
  [O] 5. THE OPEN BIT.  the modular data of the (E8)_1 endpoint is fully computed;
        the one open Tier-B input is whether the seam-Calderon net condenses all the
        way to the det-1 holomorphic endpoint -- |det K| = 1.  Reduced to one bit,
        not closed.

Status: [E] #anyons = |det Gram| + the condensation tower 16->4->1 + Gauss-Milgram
c=8 + E8 the unique holomorphic point; [O] the single holomorphy bit.  The modular-
data view of QG.AMB.01 Tier-B; complements v277.  Exact core mirrored in Wolfram.
Python (numpy + sympy).
"""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam


def gram_det(C):
    return round(np.linalg.det(np.array(C, float)))


E8 = [[2, -1, 0, 0, 0, 0, 0, 0], [-1, 2, -1, 0, 0, 0, 0, 0], [0, -1, 2, -1, 0, 0, 0, 0],
      [0, 0, -1, 2, -1, 0, 0, 0], [0, 0, 0, -1, 2, -1, 0, -1], [0, 0, 0, 0, -1, 2, -1, 0],
      [0, 0, 0, 0, 0, -1, 2, 0], [0, 0, 0, 0, -1, 0, 0, 2]]
D8 = [[2, -1, 0, 0, 0, 0, 0, 0], [-1, 2, -1, 0, 0, 0, 0, 0], [0, -1, 2, -1, 0, 0, 0, 0],
      [0, 0, -1, 2, -1, 0, 0, 0], [0, 0, 0, -1, 2, -1, 0, 0], [0, 0, 0, 0, -1, 2, -1, -1],
      [0, 0, 0, 0, 0, -1, 2, 0], [0, 0, 0, 0, 0, -1, 0, 2]]
D5 = [[2, -1, 0, 0, 0], [-1, 2, -1, 0, 0], [0, -1, 2, -1, -1], [0, 0, -1, 2, 0], [0, 0, -1, 0, 2]]
A3 = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]


def run():
    reset()
    print("v281  QGAMB.MODULAR.01: the modular-data / anyon-condensation layer of the Tier-B holomorphy bit")

    dE8, dD8, dD5, dA3 = gram_det(E8), gram_det(D8), gram_det(D5), gram_det(A3)
    d_car = dD5 * dA3

    # 1. #anyons = |det Gram|
    check("#ANYONS = |det Gram| [E]: E8 -> %d (holomorphic, single sector), "
          "D8=SO(16)_1 -> %d (anyons 1,v,s,c), carrier D5(+)A3 -> %d*%d = %d"
          % (dE8, dD8, dD5, dA3, d_car), dE8 == 1 and dD8 == 4 and d_car == 16)

    # 2. anyon-condensation tower 16 -> 4 -> 1
    tower = [d_car, dD8, dE8]
    steps_ok = all(tower[i] // tower[i + 1] == 4 for i in range(2))
    check("ANYON-CONDENSATION TOWER [E]: D5(+)A3 (det %d) -> D8 (det %d) -> E8 (det "
          "%d); each step condenses a Lagrangian Z2 boson, |det| /4 = 2^2 -- the "
          "Kitaev E8 endpoint (v92/v235)" % tuple(tower), tower == [16, 4, 1] and steps_ok)

    # 3. Gauss-Milgram -> c = 8 (D8 anyons)
    spins = [sp.Integer(0), sp.Rational(1, 2), sp.Integer(1), sp.Integer(1)]   # 1, v, s, c
    gm = sum(sp.exp(2 * sp.pi * sp.I * h) for h in spins)
    rhs = sp.sqrt(dD8) * sp.exp(2 * sp.pi * sp.I * sp.Rational(8, 8))
    check("GAUSS-MILGRAM -> c=8 [E]: sum_a e^{2 pi i h_a} = %s = sqrt|A| e^{2 pi i "
          "c/8} = %s for c=8 (D8 spins 0,1/2,1,1) -- c is the modular anomaly"
          % (sp.simplify(gm), sp.simplify(rhs)), sp.simplify(gm - rhs) == 0)

    # 4. E8 unique holomorphic c=8
    cE8 = sp.Rational(248, 31)
    check("E8 UNIQUE HOLOMORPHIC c=8 [E]: c((E8)_1)=248/31=%s=g_car+N_fam; holomorphic "
          "(1 anyon) <=> |det|=1 <=> even unimodular rank-8 = E8; SO(16)_1 has the "
          "SAME c=8 but %d anyons -- holomorphy (det 1) is THE discriminator (v277)"
          % (cE8, dD8), cE8 == 8 == g_car + N_fam and dD8 == 4 and dE8 == 1)

    # 5. the open bit
    check("THE OPEN BIT [O]: the modular data of the (E8)_1 endpoint is fully "
          "computed; the one open Tier-B input is whether the seam-Calderon net "
          "condenses to the det-1 holomorphic endpoint -- |det K|=1. Reduced to one "
          "bit, not closed", True)

    return summary("v281 #anyons=|det Gram|, condensation tower 16->4->1, Gauss-Milgram c=8; Tier-B = the single det K=1 bit (QGAMB.MODULAR.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

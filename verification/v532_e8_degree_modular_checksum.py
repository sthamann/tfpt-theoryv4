"""v532 -- The E8 dual-degree modular checksum 744 and the prime-totative
fingerprint.  AUDIT-TYPED: exact arithmetic [E], explicitly NON-exclusive
(the D16 control passes the same checksum), no derivation feeds on it --
recorded under the no-free-pattern rule with its own negative controls.

  [E] 1. DUAL PRODUCTS.  The E8 invariant degrees d = (2,8,12,14,18,20,24,30)
         (v66) satisfy d_i + d_{9-i} = 32 = h+2.  The four dual products
             (2*30, 8*24, 12*20, 14*18) = (60, 192, 240, 252)
         satisfy SIMULTANEOUSLY
             sum  = 744 = 3*248 = 3 dim E8,
             prod = 696729600 = |W(E8)|  (= prod of all degrees, v66),
             gcd  = 12 = dim g_SM,
             /12  = (5, 16, 20, 21) = (g_car, dim S^+, det L, N_fam*7).
  [E] 2. MODULAR ANCHOR.  744 is the constant coefficient of the modular
         j-function: j = E4^3/Delta = q^-1 + 744 + 196884 q + ..., recomputed
         here from scratch (E4 = theta_E8, Delta = q prod(1-q^n)^24), i.e.
         chi_{(E8)_1}^3 = j (the v496 series cubed).  The finite invariant
         degrees know the first regular coefficient of the affine character
         cube: a finite-to-affine checksum.
  [E] 3. NEGATIVE CONTROL (the checksum is NOT E8-exclusive).  D16 (degrees
         2,4,...,30 and 16; same h = 30, rank 16) gives dual-product sum
             1488 = 3*496 = 2*744,
         exactly matching dim(E8xE8) = dim SO(32) = 496: the checksum
         measures the common rank-16 / Coxeter-30 heterotic structure, not
         E8 uniqueness (the honest reading of the v496/tfpt_1 '496' box).
         All non-heterotic controls FAIL the 3*dim rule: A8 (100 vs 240),
         D8 (200 vs 360), E6 (117 vs 234), E7 (316 vs 399), F4 (72 vs 156),
         G2 (12 vs 42) -- half-pair convention, self-dual middle once.
  [E] 4. PRIME-TOTATIVE FINGERPRINT (audit-only).
             {2,3,5} u (Exp(E8) minus {1}) = {2,3,5,7,11,13,17,19,23,29}
         = ALL primes below 30; every totative of 30 except 1 is prime; and
         30 is the LARGEST integer with this property (exact scan to 10^4;
         full list {1,2,3,4,6,8,12,18,24,30} -- the classical maximal
         'prime-totative' number).  So h(E8) = 30 = |Z2| N_fam g_car is the
         maximal Coxeter number whose live phases are all prime.  Recorded
         as an audit fingerprint: NO derivation uses it (no-free-pattern).

HONEST TYPING.  All checks are exact integer / q-series arithmetic [E].
The module is a CHECKSUM + fingerprint: it feeds no readout, kills no
alternative on its own (D16 passes), and is registered audit-only -- exactly
the typing the no-free-pattern rule demands.  Mirrored in
wolfram/tfpt_readouts_extension.wl.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam, dim_Splus

DEG_E8 = [2, 8, 12, 14, 18, 20, 24, 30]
DIM_E8 = 248
W_E8 = 696729600
DIM_GSM = 12
DET_L = 20


def half_dual_sum(degs):
    s = sorted(degs)
    n = len(s)
    tot = sum(s[i] * s[n - 1 - i] for i in range(n // 2))
    if n % 2 == 1:
        tot += s[n // 2] ** 2
    return tot


def run():
    reset()
    print("v532 E8 dual-degree modular checksum 744 + prime fingerprint "
          "[AUDIT]")

    # 1. dual products
    check("degree duality [E]: d_i + d_{9-i} = 32 = h+2 for all four pairs",
          all(DEG_E8[i] + DEG_E8[7 - i] == 32 for i in range(8)))
    dp = [DEG_E8[i] * DEG_E8[7 - i] for i in range(4)]
    check("dual products = (60,192,240,252)", dp == [60, 192, 240, 252])
    check("sum = 744 = 3*248 = 3 dim E8; prod = 696729600 = |W(E8)|; "
          "gcd = 12 = dim g_SM",
          sum(dp) == 744 == 3 * DIM_E8 and sp.prod(dp) == W_E8
          and sp.igcd(*dp) == DIM_GSM)
    check("normalised (5,16,20,21) = (g_car, dim S^+, det L, N_fam*7)",
          [p // 12 for p in dp] == [g_car, dim_Splus, DET_L, N_fam * 7])

    # 2. modular anchor recomputed from scratch
    q = sp.symbols('q')
    NTR = 6
    E4 = 1 + 240 * sum(sum(d**3 for d in sp.divisors(n)) * q**n
                       for n in range(1, NTR + 1))
    prod24 = sp.prod([(1 - q**n)**24 for n in range(1, NTR + 1)])
    qj = sp.series(sp.expand(E4**3)
                   * sp.series(1 / prod24, q, 0, NTR).removeO(),
                   q, 0, 3).removeO()
    qjp = sp.Poly(sp.expand(qj), q)
    check("MODULAR ANCHOR [E]: j = E4^3/Delta = q^-1 + 744 + 196884 q + ... "
          "(chi_{(E8)_1}^3 = j, v496) -- 744 recomputed from the q-series",
          (qjp.coeff_monomial(1), qjp.coeff_monomial(q),
           qjp.coeff_monomial(q**2)) == (1, 744, 196884))

    # 3. negative controls
    deg_d16 = sorted([2 * i for i in range(1, 16)] + [16])
    check("D16 CONTROL [E]: 16 degrees (2,4,...,30 + 16), same duality "
          "d + d' = 32; dual-product sum 1488 = 3*496 = 2*744 -- the "
          "checksum is heterotic (rank 16, h 30), NOT E8-exclusive",
          all(deg_d16[i] + deg_d16[15 - i] == 32 for i in range(16))
          and half_dual_sum(deg_d16) == 1488 == 3 * 496 == 2 * 744
          and 496 == 2 * DIM_E8)
    controls = {'A8': ([2, 3, 4, 5, 6, 7, 8, 9], 80),
                'D8': ([2, 4, 6, 8, 8, 10, 12, 14], 120),
                'E6': ([2, 5, 6, 8, 9, 12], 78),
                'E7': ([2, 6, 8, 10, 12, 14, 18], 133),
                'F4': ([2, 6, 8, 12], 52),
                'G2': ([2, 6], 14)}
    sums = {n: half_dual_sum(d) for n, (d, _) in controls.items()}
    check("NON-HETEROTIC CONTROLS FAIL [E]: A8 100/240, D8 200/360, "
          "E6 117/234, E7 316/399, F4 72/156, G2 12/42 (sum vs 3*dim)",
          all(sums[n] != 3 * dim for n, (_, dim) in controls.items())
          and sums == {'A8': 100, 'D8': 200, 'E6': 117, 'E7': 316,
                       'F4': 72, 'G2': 12})
    check("convention sanity: half_dual_sum(E8) = 744 under the same "
          "half-pair rule", half_dual_sum(DEG_E8) == 744)

    # 4. prime-totative fingerprint
    exps = [1, 7, 11, 13, 17, 19, 23, 29]
    check("PRIME FINGERPRINT [E, audit]: {2,3,5} u (Exp(E8)\\{1}) = all "
          "primes below 30",
          sorted(set([2, 3, 5]) | set(exps[1:]))
          == list(sp.primerange(2, 30)))
    check("every totative of 30 except 1 is prime",
          all(sp.isprime(m) for m in exps[1:]))
    maximal = [n for n in range(1, 10001)
               if all(m == 1 or sp.isprime(m)
                      for m in range(1, n) if sp.igcd(m, n) == 1)]
    check("30 is the LARGEST n (scan to 10^4) whose totatives are all 1 or "
          "prime; full list {1,2,3,4,6,8,12,18,24,30} -- h(E8) is the "
          "maximal prime-totative Coxeter number [audit-only, feeds nothing]",
          max(maximal) == 30
          and maximal == [1, 2, 3, 4, 6, 8, 12, 18, 24, 30])

    return summary("v532 dual-degree checksum (744 = 3*248, D16 control "
                   "1488, primes < 30)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

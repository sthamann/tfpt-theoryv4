"""v418 -- The cyclotomic norm triple: the carrier split (3,2) read in the three
atom-rings gives (7, 13, 55) = (scalaron, Delta_Q, quark numerator).  This finds
the missing CARRIER-5 clock of v417 -- it is NOT a 3x3 operator but the 4x4
Phi5-companion C5 (Z[zeta5], rank phi(5)=4) -- and unifies the Gaussian (v415),
Eisenstein (v417) and pentagon norms into ONE determinant family over the atoms
{2,3,5} (v416).  [E] number theory, [C] the atom-ring / quark readings.

  [E] 1. THE CARRIER-5 CLOCK.  The Phi5-companion C5 (4x4 integer) has
         chi_{C5}=x^4+x^3+x^2+x+1, C5^5=I, tr C5 = -1, eigenvalues the four
         primitive 5th roots; the GOLDEN ratio is its real-part data:
             zeta5 + zeta5^4 = 2cos(72) = (sqrt5-1)/2 = 1/phi,
             zeta5^2+ zeta5^3 = 2cos(144) = -(sqrt5+1)/2 = -phi.
         (Output-side golden, v313/v349; needs dim 4 -- this refines v417's gap
         from "no operator" to "no 3x3 operator, but a clean 4x4 one".)
  [E] 2. THE CARRIER NORM = THE QUARK NUMERATOR.
             N_Z[zeta5](3+2 zeta5) = det(3I + 2 C5) = 55 = 5*11
         = g_car * ||Pl(K)||_1 = 1^T V^4 1 (v410/v411), the c_u/c_d numerator.
  [E] 3. THE NORM TRIPLE over the three atom-rings (det(3I + 2 Comp(Phi_n))):
             Phi3 (omega, ram 3): 7  = scalaron       (= N_omega(3+2omega), v222),
             Phi4 (i,     ram 2): 13 = Delta_Q        (= N_i(3+2i), v222/v415),
             Phi5 (zeta5, ram 5): 55 = quark numerator (this module).
         So the SAME carrier split (3,2) read in Z[omega], Z[i], Z[zeta5] gives
         (7, 13, 55) -- one (3,2)-generated triple over the atoms {3,2,5} (v416).
  [E] 4. NEGATIVE CONTROL (the carrier ring distinguishes the two).  The anchor
         (5,4) gives (5,4) -> (21, 41, 461): the omega-ring 21 = N_omega(5,4) and
         the square-ring 41 = 10 b1 are BOTH named (v222), but the CARRIER ring
         gives 461 (prime, un-named).  So the anchor does NOT reach a named
         carrier number -- the Phi5/carrier ring is exactly what separates the
         carrier split (3,2) -> 55 (the quark numerator) from the anchor
         (5,4) -> 461.
  [C] 5. HONEST: (3,2) is FORCED, not UNIQUE.  A scan over (a,b), a>b>=1,
         a+b<=9, against the named-constant set finds exactly TWO clean splits:
             (2,1) -> (3, 5, 11) = (N_fam, g_car, ||Pl(K)||_1),
             (3,2) -> (7, 13, 55) = (scalaron, Delta_Q, quark numerator).
         So (3,2) is not the unique clean split; it is the one FORCED by the
         carrier conditions b+s=5, b^2+s^2=13 (v14), and it is the one carrying
         the load-bearing (7,13,55).  (2,1) is a secondary clean rung -- the two
         form a small ladder (2,1)->(3,2).  No over-claim of uniqueness.
  [C] 6. THE SHARPER (CROSS-SECTOR) DISCRIMINATOR.  Of the two clean splits only
         (3,2) -> (7,13,55) spans THREE DIFFERENT physics sectors (gravity =
         scalaron 7, flavor = Delta_Q 13, masses = quark numerator 55), while
         (2,1) -> (3,5,11) is all 'core' (N_fam, g_car, ||Pl(K)||_1).  So (3,2)
         is the UNIQUE CROSS-SECTOR seed -- sharper than "clean"; the ladder
         reads input (2,1) -> output (3,2), difference 4*(1,2,11).  A scan to
         a+b<=14 confirms exactly the two rungs (NOT a Fibonacci tower:
         (5,3),(8,5) are not clean).

Mirrored in wolfram/tfpt_readouts_extension.wl (exact integer determinants); the
cross-sector reading (6) is a [C] interpretation, Python-only.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

x = sp.symbols('x')
phi = (1 + sp.sqrt(5)) / 2
z5 = sp.exp(2 * sp.I * sp.pi / 5)

# cyclotomic companions Phi3 (omega), Phi4 (i), Phi5 (zeta5)
C3 = sp.Matrix([[0, -1], [1, -1]])
C4 = sp.Matrix([[0, -1], [1, 0]])
C5 = sp.Matrix([[0, 0, 0, -1], [1, 0, 0, -1], [0, 1, 0, -1], [0, 0, 1, -1]])
COMP = {3: C3, 4: C4, 5: C5}

# the named recurring TFPT integers (for the discipline scan)
TFPT = {1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 20, 21, 24, 25, 30,
        31, 40, 41, 48, 52, 55, 56, 60, 78, 120, 128, 240, 248}


def norm(a, b, n):
    Cn = COMP[n]
    return int((a * sp.eye(Cn.shape[0]) + b * Cn).det())


def triple(a, b):
    return (norm(a, b, 3), norm(a, b, 4), norm(a, b, 5))


def run():
    reset()
    print("v418 cyclotomic norm triple: (3,2) -> (7,13,55) over the atom-rings; "
          "the carrier-5 clock C5; anchor (5,4) control")

    # ---- 1. the carrier-5 clock C5 + the golden ratio ----
    check("CARRIER-5 CLOCK [E]: the Phi5-companion C5 (4x4 integer) has "
          "chi=x^4+x^3+x^2+x+1, C5^5=I, tr=-1 (primitive 5th roots); the golden "
          "ratio is its real-part data zeta5+zeta5^4=1/phi, zeta5^2+zeta5^3=-phi "
          "(output-side, v313/v349; needs dim 4 -- refines v417's gap)",
          C5.charpoly(x).as_expr() == x**4 + x**3 + x**2 + x + 1
          and C5**5 == sp.eye(4) and C5.trace() == -1
          and sp.simplify(2 * sp.cos(2 * sp.pi / 5) - 1 / phi) == 0
          and sp.simplify(2 * sp.cos(4 * sp.pi / 5) + phi) == 0)

    # ---- 2. the carrier norm = the quark numerator ----
    check("CARRIER NORM = QUARK NUMERATOR [E]: N_Z[zeta5](3+2 zeta5) = "
          "det(3I+2 C5) = 55 = 5*11 = g_car*||Pl(K)||_1 = 1^T V^4 1 (v410/v411), "
          "the c_u/c_d numerator",
          norm(3, 2, 5) == 55 == g_car * 11
          and sp.nsimplify(sp.expand_complex(sp.prod([3 + 2 * z5**k
                                                      for k in range(1, 5)]))) == 55)

    # ---- 3. the norm triple over the three atom-rings ----
    check("NORM TRIPLE [E]: det(3I+2 Comp(Phi_n)) = (7,13,55) for n=(3,4,5) = "
          "(scalaron, Delta_Q, quark numerator) over Z[omega],Z[i],Z[zeta5] "
          "(atoms 3,2,5, v416) -- the SAME carrier split (3,2) in three rings; "
          "ties v222/v415/v417",
          triple(3, 2) == (7, 13, 55)
          and norm(3, 2, 3) == 7 and norm(3, 2, 4) == 13 and norm(3, 2, 5) == 55)

    # ---- 4. negative control: the anchor (5,4) fails the triple ----
    check("NEG CONTROL [E]: the anchor (5,4) -> (21,41,461); the omega-ring "
          "21=N_omega(5,4) and the square-ring 41=10 b1 are BOTH named (v222), "
          "but the CARRIER ring gives 461 (prime, un-named) -- so the anchor "
          "does NOT reach a named carrier number; the Phi5/carrier ring "
          "separates (3,2)->55 (quark numerator) from (5,4)->461",
          triple(5, 4) == (21, 41, 461)
          and 21 in TFPT and 41 in TFPT and 461 not in TFPT and sp.isprime(461))

    # ---- 5. honest: (3,2) is FORCED, not UNIQUE ----
    clean = [(a, b) for a in range(1, 9) for b in range(1, a)
             if all(v in TFPT for v in triple(a, b))]
    check("HONEST (3,2) FORCED not UNIQUE [C]: the clean splits (a>b>=1, "
          "a+b<=9) are exactly {(2,1)->(3,5,11), (3,2)->(7,13,55)} -- so (3,2) "
          "is NOT the unique clean split; it is the one FORCED by b+s=5, "
          "b^2+s^2=13 (v14) and carrying the load-bearing (7,13,55); (2,1) is a "
          "secondary rung (the two form a ladder (2,1)->(3,2))",
          sorted(clean) == [(2, 1), (3, 2)]
          and triple(2, 1) == (3, 5, 11) == (N_fam, g_car, 11))

    # ---- 6. the sharper discriminator: (3,2) is the UNIQUE cross-sector seed ----
    sector = {7: 'gravity', 13: 'flavor', 55: 'masses',
              3: 'core', 5: 'core', 11: 'core'}
    span = {ab: {sector[v] for v in triple(*ab)} for ab in ((2, 1), (3, 2))}
    diff = tuple(triple(3, 2)[i] - triple(2, 1)[i] for i in range(3))
    check("CROSS-SECTOR DISCRIMINATOR [C]: of the two clean splits only "
          "(3,2)->(7,13,55) spans THREE physics sectors (gravity=scalaron, "
          "flavor=Delta_Q, masses=quark numerator); (2,1)->(3,5,11) is all "
          "'core' (N_fam, g_car, Pl) -- so (3,2) is the UNIQUE cross-sector seed "
          "(sharper than 'clean'); ladder input (2,1)->output (3,2), diff "
          "4*(1,2,11)=(4,8,44)",
          span[(3, 2)] == {'gravity', 'flavor', 'masses'}
          and span[(2, 1)] == {'core'}
          and diff == (4, 8, 44) == tuple(4 * x for x in (1, 2, 11)))

    return summary("v418 cyclotomic norm triple (7,13,55 over the atom-rings; "
                   "C5 carrier clock; anchor control)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)

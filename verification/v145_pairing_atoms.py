"""v145 -- The pairing values are ATOM IDENTITIES: given the exponent-
duality lift n = w0(sigma) + |mu_4| e_3 (the v139 audit identity, with
w0 = the A_3 exponent duality m <-> h-m), ALL THREE R4' pairings reduce
to atom arithmetic -- including a new clean closure |mu_4| + g_car =
N_fam^2 (4 + 5 = 9).  R4' collapses from 'derive two values' to 'derive
ONE map'.  [I] exact; the lift mechanism itself stays [P].

v142 reduced R4' to the two line pairings (|Z2|, rank E8).  This module
shows the VALUES carry no independent information once the v139 lift is
read structurally:

  [I] 1. THE LIFT IS THE EXPONENT DUALITY.  'reverse' in the v139 audit
         identity n = reverse(sigma) + |mu_4| e_3 is w0: the A_3
         exponent duality m <-> h(A_3) - m = 4 - m (swaps the Q_+
         degrees 1 <-> 3, fixes 2) -- an established Lie-theoretic
         involution (exponents pair to the Coxeter number), not an ad
         hoc permutation; the lift slot e_3 is the top-exponent
         (anchor/tau) line, the lift size is the glue order.
  [I] 2. FIRST PAIRING = GLUE/SHEET ATOM IDENTITY.
             n . 1 = sigma . 1 + |mu_4| = -|Z_2| + |mu_4| = |Z_2|
         (uses sigma.1 = -|Z_2|, v136); the value 2 says exactly
         |mu_4| = 2|Z_2| -- the glue order is the doubled sheet.
  [I] 3. SECOND PAIRING = A NEW ATOM CLOSURE.  sigma is orthogonal to
         the dual-ordered anchor:
             sigma . w0(a) = 2|Z_2| - N_fam^2 + g_car = 0
             <=>  |mu_4| + g_car = N_fam^2   (4 + 5 = 9),
         and then n . a = sigma . w0(a) + |mu_4| a_3 = 0 + 4*2 = 8 =
         rank E8: the rank pairing is the glue order times the anchor
         top entry, riding on the closure 4 + 5 = 9.
  [I] 4. THIRD PAIRING = NORM ARITHMETIC.  With ||sigma||^2 = |Z_2|^2 +
         N_fam^4 + g_car^2 = 110 = |Z_2| g_car ||Pl(K)||_1:
             n . sigma = ||sigma||^2 - N_fam^2 + |mu_4| g_car
                       = 110 - 9 + 20 = 121 = ||Pl(K)||_1^2
         -- the square the v139 selector picks is itself atom
         arithmetic of the spectral normal.
  [P] 5. RESIDUE (recorded): R4' = derive the ONE map
         n = w0(sigma) + |mu_4| e_3 (why the torsion normal is the
         exponent-dual of the spectral normal plus a glue lift on the
         top-exponent line).  All three pairing VALUES are then atom
         identities -- no independent number remains.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, g_car

Z2, MU4 = 2, 4
ONE = sp.Matrix([1, 1, 1])
A = sp.Matrix([1, 1, 2])
SIGMA = sp.Matrix([2, -9, 5])
N = sp.Matrix([5, -9, 6])
E3 = sp.Matrix([0, 0, 1])


def w0(v):
    """A_3 exponent duality m <-> 4-m on the degree-(1,2,3) coordinates."""
    return sp.Matrix([v[2], v[1], v[0]])


def run():
    reset()
    print("v145 pairing atoms (R4': two values -> one map)")

    check("THE LIFT IS THE EXPONENT DUALITY: n = w0(sigma) + |mu_4| e_3 "
          "exactly, with w0 the A_3 exponent duality m <-> 4-m (swaps "
          "Q_+ degrees 1<->3, fixes 2; exponents pair to h(A_3) = 4 = "
          "|mu_4|); lift slot = the top-exponent line, lift size = the "
          "glue order",
          w0(SIGMA) + MU4 * E3 == N
          and [4 - m for m in (1, 2, 3)] == [3, 2, 1])

    check("FIRST PAIRING = GLUE/SHEET IDENTITY: n.1 = sigma.1 + |mu_4| "
          "= -|Z_2| + |mu_4| = |Z_2| -- the value 2 says exactly "
          "|mu_4| = 2|Z_2| (the glue order is the doubled sheet)",
          SIGMA.dot(ONE) == -Z2
          and N.dot(ONE) == -Z2 + MU4 == Z2
          and MU4 == 2 * Z2)

    check("SECOND PAIRING = NEW ATOM CLOSURE: sigma . w0(a) = 2|Z_2| - "
          "N_fam^2 + g_car = 0 <=> |mu_4| + g_car = N_fam^2 (4+5=9); "
          "then n.a = 0 + |mu_4|*a_3 = 4*2 = 8 = rank E8",
          SIGMA.dot(w0(A)) == 2 * Z2 - N_fam ** 2 + g_car == 0
          and MU4 + g_car == N_fam ** 2
          and N.dot(A) == MU4 * A[2] == 8)

    check("THIRD PAIRING = NORM ARITHMETIC: ||sigma||^2 = |Z_2|^2 + "
          "N_fam^4 + g_car^2 = 110 = |Z_2| g_car ||Pl(K)||_1; "
          "n.sigma = ||sigma||^2 - N_fam^2 + |mu_4| g_car = 121 = "
          "||Pl(K)||_1^2",
          SIGMA.dot(SIGMA) == Z2 ** 2 + N_fam ** 4 + g_car ** 2 == 110
          and 110 == Z2 * g_car * 11
          and N.dot(SIGMA) == 110 - N_fam ** 2 + MU4 * g_car == 121 == 11 ** 2)

    check("CONSISTENCY: the lift reproduces the v139 uniqueness data "
          "(frame volume 11, line z(t) = 11(11+t) at t = 0) and the "
          "v142 congruence x - 3y + z = 0 mod 11 holds on the atom "
          "triple (2, 8, 121)",
          sp.Matrix.hstack(ONE, A, SIGMA).det() == 11
          and (2 - 3 * 8 + 121) % 11 == 0)

    check("RESIDUE [P] (recorded): R4' = derive the ONE map n = "
          "w0(sigma) + |mu_4| e_3; all three pairing values are atom "
          "identities given it -- no independent number remains", True)

    return summary("v145 pairing atoms")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
